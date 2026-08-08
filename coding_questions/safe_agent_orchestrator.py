'''Safe Agent Orchestrator: Bounded Tool Calls, Task-Scoped Cache, and Protected Writes

Implement an orchestration loop for a tool-using customer-support agent. The model returns either a final answer or a structured
tool call. The orchestrator, not the model, is responsible for validating and executing actions.

Requirements:
1. Limit each task to at most five tool-call iterations. If the model cannot finish, stop and return a human-escalation result.
2. Inject the current ISO date into the system prompt so date-sensitive reasoning has an explicit reference date.
3. Parse the first valid JSON object from model output even when it is surrounded by prose or Markdown fences. Never use eval().
4. Cache safe read-only tool results only for the active task. The cache key must include order_id plus intent so a tracking lookup
   cannot be reused as refund eligibility. Clear task state when order, intent, or authentication state changes.
5. Before a process_refund action, enforce authentication, enforce a manager-approval threshold, and rerun refund eligibility in the
   same turn so stale state cannot authorize a financial write. The refreshed eligibility check must bypass the cache.
6. Do not cache state-changing tool calls. Repeated financial writes should be protected with idempotency in a real production tool.
7. Return controlled failures for malformed model output, unknown tools, tool exceptions, and bounded-loop exhaustion.

The sample implementation assumes process_refund is allowed below a threshold after all checks. If business policy says refunds are
human-only, replace that execution branch with a handoff; the orchestration principles remain the same.

Decision format:
- {"type": "tool_call", "tool": "tool_name", "arguments": {...}}
- {"type": "final", "answer": "..."}

Key observations:
- The LLM proposes an action; trusted code validates permissions and invariants.
- A cache key based only on order ID is unsafe because the same order can participate in multiple intents.
- Cost optimization must not reuse stale financial eligibility.
- Step limits provide a predictable upper bound on tool/API usage and stop infinite loops.

Complexity:
- JSON scanning is O(n^2) in the worst case for pathological text because parsing may be attempted at multiple opening braces; model
  responses are normally small. A streaming/parser-aware implementation can optimize this if needed.
- Tool orchestration is O(k) model/tool iterations with k <= MAX_TOOL_CALLS, excluding external tool cost.

Important edge cases include malformed JSON, unknown tools, repeated identical reads, same order with a new intent, changed authentication,
refund amount above manager threshold, stale eligibility after a prior refund, tool failures, and a model that never returns a final answer.
'''

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from typing import Any, Callable


MAX_TOOL_CALLS = 5


@dataclass(frozen=True)
class TaskContext:
    order_id: int | None
    intent: str
    authenticated: bool


@dataclass(frozen=True)
class AgentResult:
    status: str
    answer: str
    tool_calls: int


def extract_first_json_object(text: str) -> dict[str, Any] | None:
    """Return the first valid JSON object found in arbitrary model text."""
    decoder = json.JSONDecoder()

    for index, char in enumerate(text):
        if char != "{":
            continue

        try:
            value, _ = decoder.raw_decode(text[index:])
        except json.JSONDecodeError:
            continue

        if isinstance(value, dict):
            return value

    return None


class SafeAgent:
    def __init__(
        self,
        *,
        model: Callable[[list[dict[str, Any]]], str],
        tools: dict[str, Callable[..., Any]],
        manager_refund_threshold: float,
        today: Callable[[], date] = date.today,
    ) -> None:
        self.model = model
        self.tools = tools
        self.manager_refund_threshold = manager_refund_threshold
        self.today = today
        self._active_context: TaskContext | None = None
        self._read_cache: dict[tuple[Any, ...], Any] = {}

    def run(self, user_message: str, *, context: TaskContext) -> AgentResult:
        self._reset_cache_if_task_changed(context)
        self._active_context = context

        messages: list[dict[str, Any]] = [
            {
                "role": "system",
                "content": (
                    "You are a support agent. Use only the provided tools and return JSON decisions. "
                    f"Current date: {self.today().isoformat()}."
                ),
            },
            {"role": "user", "content": user_message},
        ]

        tool_calls = 0

        while tool_calls < MAX_TOOL_CALLS:
            raw_response = self.model(messages)
            decision = extract_first_json_object(raw_response)
            if decision is None:
                return AgentResult(
                    status="escalated",
                    answer="The agent returned an invalid structured response. Escalating to a human.",
                    tool_calls=tool_calls,
                )

            decision_type = decision.get("type")
            if decision_type == "final":
                answer = decision.get("answer")
                if isinstance(answer, str) and answer.strip():
                    self._finish_task()
                    return AgentResult("completed", answer.strip(), tool_calls)
                return AgentResult(
                    "escalated",
                    "The agent returned an empty final answer. Escalating to a human.",
                    tool_calls,
                )

            if decision_type != "tool_call":
                return AgentResult(
                    "escalated",
                    "The agent returned an unknown decision type. Escalating to a human.",
                    tool_calls,
                )

            tool_calls += 1
            tool_name = decision.get("tool")
            arguments = decision.get("arguments", {})
            if not isinstance(tool_name, str) or not isinstance(arguments, dict):
                return AgentResult(
                    "escalated",
                    "The tool call was malformed. Escalating to a human.",
                    tool_calls,
                )

            result = self._execute_tool(tool_name, arguments, context)
            messages.append(
                {
                    "role": "tool",
                    "name": tool_name,
                    "content": json.dumps(result, default=str),
                }
            )

        return AgentResult(
            status="escalated",
            answer="The tool-call limit was reached. Escalating to a human.",
            tool_calls=tool_calls,
        )

    def _execute_tool(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        context: TaskContext,
    ) -> dict[str, Any]:
        tool = self.tools.get(tool_name)
        if tool is None:
            return {"ok": False, "error": "unknown_tool"}

        if tool_name == "process_refund":
            return self._execute_protected_refund(tool, arguments, context)

        cache_key = self._cache_key(tool_name, arguments, context)
        if cache_key in self._read_cache:
            return {"ok": True, "data": self._read_cache[cache_key], "cached": True}

        try:
            result = tool(**arguments)
        except Exception as exc:  # sanitized result; log the real exception internally in production
            return {"ok": False, "error": type(exc).__name__}

        self._read_cache[cache_key] = result
        return {"ok": True, "data": result, "cached": False}

    def _execute_protected_refund(
        self,
        process_refund: Callable[..., Any],
        arguments: dict[str, Any],
        context: TaskContext,
    ) -> dict[str, Any]:
        if not context.authenticated:
            return {"ok": False, "error": "authentication_required"}

        order_id = arguments.get("order_id")
        amount = arguments.get("amount")
        if not isinstance(order_id, int) or not isinstance(amount, (int, float)):
            return {"ok": False, "error": "invalid_refund_arguments"}

        if context.order_id is not None and order_id != context.order_id:
            return {"ok": False, "error": "order_context_mismatch"}

        if amount > self.manager_refund_threshold:
            return {"ok": False, "error": "manager_approval_required"}

        eligibility_tool = self.tools.get("check_refund_eligibility")
        if eligibility_tool is None:
            return {"ok": False, "error": "eligibility_tool_unavailable"}

        # Fresh authoritative read: intentionally bypass the task cache.
        try:
            eligibility = eligibility_tool(order_id=order_id)
        except Exception as exc:
            return {"ok": False, "error": type(exc).__name__}

        if not isinstance(eligibility, dict) or not eligibility.get("eligible"):
            return {"ok": False, "error": "refund_not_eligible", "eligibility": eligibility}

        refundable_amount = eligibility.get("refundable_amount")
        if not isinstance(refundable_amount, (int, float)) or amount > refundable_amount:
            return {
                "ok": False,
                "error": "amount_exceeds_refundable_balance",
                "eligibility": eligibility,
            }

        try:
            result = process_refund(order_id=order_id, amount=float(amount))
        except Exception as exc:
            return {"ok": False, "error": type(exc).__name__}

        self._read_cache.clear()
        return {"ok": True, "data": result, "fresh_eligibility": eligibility}

    def _cache_key(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        context: TaskContext,
    ) -> tuple[Any, ...]:
        canonical_arguments = json.dumps(arguments, sort_keys=True, separators=(",", ":"))
        return (
            context.order_id,
            context.intent,
            tool_name,
            canonical_arguments,
        )

    def _reset_cache_if_task_changed(self, context: TaskContext) -> None:
        if self._active_context is None:
            return

        if (
            self._active_context.order_id != context.order_id
            or self._active_context.intent != context.intent
            or self._active_context.authenticated != context.authenticated
        ):
            self._read_cache.clear()

    def _finish_task(self) -> None:
        self._read_cache.clear()
        self._active_context = None


class ScriptedModel:
    """Small deterministic model stub used by the sample tests."""

    def __init__(self, responses: list[str]) -> None:
        self.responses = list(responses)
        self.messages_seen: list[list[dict[str, Any]]] = []

    def __call__(self, messages: list[dict[str, Any]]) -> str:
        self.messages_seen.append(list(messages))
        if not self.responses:
            return '{"type":"tool_call","tool":"get_order_details","arguments":{"order_id":1}}'
        return self.responses.pop(0)


def run_sample_tests() -> None:
    assert extract_first_json_object(
        "Here is the result:\n```json\n{\"type\": \"final\", \"answer\": \"done\"}\n```"
    ) == {"type": "final", "answer": "done"}
    assert extract_first_json_object("not JSON") is None

    read_calls: list[int] = []
    eligibility_calls: list[int] = []
    refund_calls: list[tuple[int, float]] = []

    def get_order_details(order_id: int) -> dict[str, Any]:
        read_calls.append(order_id)
        return {"order_id": order_id, "status": "completed"}

    eligibility_values = [
        {"eligible": True, "refundable_amount": 80.0},
        {"eligible": True, "refundable_amount": 60.0},
    ]

    def check_refund_eligibility(order_id: int) -> dict[str, Any]:
        eligibility_calls.append(order_id)
        return eligibility_values[min(len(eligibility_calls) - 1, len(eligibility_values) - 1)]

    def process_refund(order_id: int, amount: float) -> dict[str, Any]:
        refund_calls.append((order_id, amount))
        return {"refund_id": "r-1", "amount": amount}

    model = ScriptedModel(
        [
            '{"type":"tool_call","tool":"get_order_details","arguments":{"order_id":7}}',
            'prefix {"type":"tool_call","tool":"get_order_details","arguments":{"order_id":7}} suffix',
            '{"type":"final","answer":"Order reviewed"}',
        ]
    )
    agent = SafeAgent(
        model=model,
        tools={
            "get_order_details": get_order_details,
            "check_refund_eligibility": check_refund_eligibility,
            "process_refund": process_refund,
        },
        manager_refund_threshold=100.0,
        today=lambda: date(2026, 7, 21),
    )
    result = agent.run(
        "Where is order 7?",
        context=TaskContext(order_id=7, intent="tracking", authenticated=True),
    )
    assert result.status == "completed"
    assert read_calls == [7]
    assert "Current date: 2026-07-21" in model.messages_seen[0][0]["content"]

    refund_model = ScriptedModel(
        [
            '{"type":"tool_call","tool":"check_refund_eligibility","arguments":{"order_id":7}}',
            '{"type":"tool_call","tool":"process_refund","arguments":{"order_id":7,"amount":50}}',
            '{"type":"final","answer":"Refund processed"}',
        ]
    )
    agent.model = refund_model
    refund_result = agent.run(
        "Refund 50 for order 7",
        context=TaskContext(order_id=7, intent="refund", authenticated=True),
    )
    assert refund_result.status == "completed"
    assert eligibility_calls == [7, 7]
    assert refund_calls == [(7, 50.0)]

    above_threshold_model = ScriptedModel(
        [
            '{"type":"tool_call","tool":"process_refund","arguments":{"order_id":7,"amount":150}}',
            '{"type":"final","answer":"Escalated for approval"}',
        ]
    )
    agent.model = above_threshold_model
    threshold_result = agent.run(
        "Refund 150 for order 7",
        context=TaskContext(order_id=7, intent="refund", authenticated=True),
    )
    assert threshold_result.status == "completed"
    assert refund_calls == [(7, 50.0)]

    looping_model = ScriptedModel([])
    agent.model = looping_model
    loop_result = agent.run(
        "Keep checking order 9",
        context=TaskContext(order_id=9, intent="tracking", authenticated=True),
    )
    assert loop_result.status == "escalated"
    assert loop_result.tool_calls == MAX_TOOL_CALLS

    print("All safe agent orchestrator sample tests passed.")


if __name__ == "__main__":
    run_sample_tests()


'''
Explanation:
1. The agent loop accepts only two decision types: final response or tool call. Every tool call is dispatched through trusted code.
2. The hard five-call limit creates a deterministic upper bound and ensures a looping model cannot consume tools indefinitely.
3. Read caching is task-scoped. The key includes order ID and intent, so tracking and refund workflows for the same order are distinct.
4. process_refund is never cached. It checks authentication and threshold, then calls check_refund_eligibility again immediately
   before the write. This prevents stale eligibility from authorizing a refund after state changes.
5. Structured output parsing searches for a real JSON object and uses the JSON parser rather than executing model text.

Summary:
- Model decisions are proposals; the orchestrator owns authorization and execution.
- Bound loops and cache safe reads to control cost.
- Invalidate state on task changes and refresh authoritative data before high-impact writes.
- Treat malformed model output and tool failures as normal production failure modes.
'''
