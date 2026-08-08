# Testing, QA, Security, Observability & Reliability

> **Purpose:** Pytest, code quality, QA, AI QA, security, privacy, PII handling, monitoring, logging, metrics, incidents, runbooks, and reliability.
> **Use this file for:** backend, AI platform, production support, and SRE-adjacent interviews

---

## Recommended Study Flow

1. Read the **Quick Summary** first.
2. Review the **Key Concepts** and tables.
3. Practice the **Interview Questions & Answers** out loud.
4. Use the code snippets and examples to explain trade-offs clearly.
5. Finish with the **Common Mistakes** and **Revision Checklist** sections.

---

## Quick Summary

This is a new topic file created because the attached repository files did not have a dedicated Markdown page for this subject. It is merged from the organized topic-wise interview-prep pack and follows the same repository style as the existing notes.

---

## Consolidated Interview Questions & Technical Notes

> Pytest, code quality, QA strategy, AI QA, monitoring, logging, metrics, production reliability, incidents, runbooks, security, privacy, PII, and access control.

---

### 6. Production Monitoring, Usage Tracking & Reliability
#### 6.1 Traditional production metrics

- Latency
- Throughput
- Error rate
- CPU
- Memory
- Disk
- Availability
- Request volume

---

#### 6.2 AI-specific production metrics

- Token usage
- Cost per request
- Prompt tokens
- Completion tokens
- Hallucination rate
- Retrieval quality
- Tool success rate
- Prompt failure rate
- User feedback
- Model/version performance
- Citation accuracy

---

#### 6.3 Tracking which user calls which API and token usage
##### Usage table

```text
api_usage
---------
request_id
user_id
endpoint
model_name
prompt_tokens
completion_tokens
total_tokens
latency_ms
cost_usd
status_code
created_at
```

##### FastAPI middleware example

```python
import time
import uuid
import logging
from fastapi import FastAPI, Request

app = FastAPI()
logger = logging.getLogger(__name__)


@app.middleware("http")
async def track_request_usage(request: Request, call_next):
    start = time.time()
    request_id = str(uuid.uuid4())
    user_id = request.headers.get("x-user-id", "anonymous")

    response = await call_next(request)
    latency_ms = (time.time() - start) * 1000

    logger.info({
        "request_id": request_id,
        "user_id": user_id,
        "endpoint": request.url.path,
        "method": request.method,
        "status_code": response.status_code,
        "latency_ms": latency_ms,
    })

    return response
```

##### LLM token tracking

```python
result = llm_client.chat.completions.create(...)
usage = result.usage

prompt_tokens = usage.prompt_tokens
completion_tokens = usage.completion_tokens
total_tokens = usage.total_tokens
```

**Interview answer:**

> I would track token usage at the application layer, not only at the LLM provider dashboard. Each request should have user ID, endpoint, model, prompt tokens, completion tokens, total tokens, latency, cost, status, and timestamp. This allows cost visibility, quota enforcement, abuse detection, debugging, and capacity planning.

---

#### 6.4 Reliability patterns

- Retries with backoff
- Timeouts
- Circuit breakers
- Fallback models
- Rate limiting
- Queues for long-running jobs
- Health checks
- Rollbacks
- Feature flags
- Human-in-the-loop approval
- Audit logs

---

### 13. Testing, Quality Engineering & AI QA
#### 13.1 Testing Strategy

**Interview answer:**

> I follow a layered testing strategy. I start with unit tests, then integration tests, API tests, end-to-end tests, regression tests, performance tests, and security tests. For AI systems, I also test prompts, RAG retrieval, hallucination behavior, tool-calling accuracy, and agent workflows.

---

#### 13.2 Testing Pyramid

```text
        E2E Tests
     Integration Tests
        Unit Tests
```

Most tests should be unit tests because they are fast and reliable.

---

#### 13.3 Software testing types

|  Test Type  |                    Purpose                    |
| ----------- | --------------------------------------------- |
| Unit        | Test individual functions/classes             |
| Integration | Test component interactions                   |
| API         | Validate endpoints, schemas, status codes     |
| E2E         | Simulate full user workflow                   |
| Regression  | Ensure existing features still work           |
| Performance | Check latency, throughput, load               |
| Security    | Auth, injection, data leakage, access control |

---

#### 13.4 AI Testing

For AI systems, test:

- Prompt consistency
- Retrieval quality
- Faithfulness
- Hallucination rate
- Citation accuracy
- Tool selection
- Tool arguments
- Agent step sequence
- Fallback behavior
- Safety and policy compliance
- Prompt injection resistance

---

#### 13.5 Quality Engineering Standards

**Interview answer:**

> I define quality criteria before testing: correctness, factuality, instruction following, safety, latency, reliability, and user impact. I create representative test cases including normal scenarios, edge cases, and negative cases. I use both automated and human evaluation, integrate tests into CI/CD, and monitor production behavior continuously.

---

### 9. Security for AI Applications
#### 9.1 Why Security Matters in AI Agent Development

> "Security is very important because AI agents may connect to APIs, databases, customer records, internal tools, or sensitive business systems. I would not treat it like just a chatbot; I would secure the full flow."

#### 9.2 Security Areas to Mention
##### Authentication

- JWT
- OAuth
- SSO
- API keys

##### Authorization

- Role-based access control
- Permission checks
- Least privilege access

##### Data Protection

- Masking sensitive data
- Avoiding unnecessary logging of PII
- Encryption in transit and at rest

##### Secrets Management

- Environment variables
- AWS Secrets Manager
- Azure Key Vault
- HashiCorp Vault

##### API Security

- Rate limiting
- Input validation
- Request size limits
- HTTPS
- Secure headers

##### AI-Specific Security

- Prompt injection protection
- Tool-use restrictions
- Output filtering
- Guardrails
- Human escalation
- Audit logs

#### 9.3 Strong Interview Answer

> "For AI agents, I would secure both the traditional application layer and the AI-specific layer. That means authentication, authorization, secure API access, secret management, input validation, prompt-injection protection, restricted tool access, logging, monitoring, and human escalation for risky workflows."

---

### 21. Testing, Monitoring & Continuous Improvement
#### 21.1 Testing AI Agents

Types of tests:

- Unit tests
- Integration tests
- End-to-end tests
- Prompt regression tests
- Simulation tests
- Retrieval tests
- API tool-calling tests
- Safety tests
- Edge-case tests

#### 21.2 Simulation Tests

> "Simulation tests are scripted user journeys used to check how the agent behaves across expected and edge-case scenarios before going live."

Examples:

- User asks a supported question
- User asks unsupported question
- User provides missing information
- API returns timeout
- Retrieved context is empty
- User asks for sensitive information
- Agent needs to escalate to human

#### 21.3 Reviewing Live Conversations

Steps:

1. Review failed or negative conversations
2. Identify issue type
3. Categorize failure
4. Create bug/issue
5. Improve prompt, retrieval, or API handling
6. Re-test
7. Deploy fix
8. Monitor whether the issue decreases

#### 21.4 Production Metrics

- Conversation success rate
- Resolution rate
- Escalation rate
- Hallucination rate
- Latency
- Token usage
- User satisfaction
- API failure rate
- Retrieval accuracy
- Cost per conversation
- Error rate

#### 21.5 Strong Interview Line

> "For production AI systems, improvement is continuous. I would review live conversations, analyze failure patterns, create issues, improve prompts or retrieval, test again, and monitor metrics after deployment."

---

### 11. Testing & Code Quality

The role emphasizes high-quality tested code.

#### Topics to revise

- Unit testing.
- Integration testing.
- Test fixtures.
- Mocking.
- Pytest.
- Linting.
- Formatting.
- Type checking.
- Code reviews.
- Test coverage.

---

#### Example: Pytest unit test

```python
from app.services.pricing import calculate_total


def test_calculate_total_with_tax() -> None:
    result = calculate_total(price=100.0, tax_rate=0.13)
    assert result == 113.0
```

---

#### Example: Mocking an external LLM call

```python
from unittest.mock import Mock


def test_answer_generation_uses_context() -> None:
    mock_llm = Mock()
    mock_llm.generate.return_value = "The policy allows refunds within 30 days."

    context = "Refunds are allowed within 30 days of purchase."
    question = "Can I get a refund?"

    answer = mock_llm.generate(question=question, context=context)

    assert "30 days" in answer
    mock_llm.generate.assert_called_once()
```

**Interview explanation:**

For LLM systems, tests should not only check code paths but also validate prompt formatting, retrieval behavior, fallback logic, and safety handling.

---

### 14. Observability & Production Monitoring
#### Topics to revise

- Structured logging.
- Metrics.
- Distributed tracing.
- Dashboards.
- Alerting.
- Error rates.
- Latency percentiles.
- Token usage monitoring for LLM apps.
- Cost dashboards.
- Incident response.
- Post-incident learning.

#### Example structured log

```python
import logging

logger = logging.getLogger(__name__)


def log_llm_request(user_id: str, model: str, tokens: int, latency_ms: float) -> None:
    logger.info(
        "llm_request_completed",
        extra={
            "user_id": user_id,
            "model": model,
            "tokens": tokens,
            "latency_ms": latency_ms,
        },
    )
```

#### Useful production metrics

|   Area   |                           Metrics                            |
| -------- | ------------------------------------------------------------ |
| API      | request count, error rate, p95 latency, p99 latency          |
| Database | slow queries, connection pool usage, lock waits              |
| LLM      | token count, cost, latency, model errors, fallback rate      |
| RAG      | retrieval precision, empty retrieval rate, citation accuracy |
| System   | CPU, memory, pod restarts, queue depth                       |

---

### 15. Security, Privacy, and PII Handling
#### Topics to revise

- Secrets management.
- Least privilege access.
- Input validation.
- Authentication.
- Authorization.
- Encryption at rest.
- Encryption in transit.
- Secure coding.
- PII handling.
- Data retention.
- Audit logs.
- Prompt injection risks.
- Safe output handling.

#### Common interview questions

1. How do you protect secrets?
2. How do you handle PII in an LLM system?
3. What is least privilege?
4. What is prompt injection?
5. How do you validate user input?
6. How do you prevent sensitive data leakage?

#### Example answer: Handling PII in GenAI systems

```text
I would avoid sending unnecessary PII to the model, mask or redact sensitive fields where possible, enforce access controls, log only safe metadata, encrypt data at rest and in transit, and define clear retention policies. I would also add guardrails to prevent the model from exposing sensitive information in outputs.
```

---

### 22. LLM Cost, Latency, and Reliability Optimization
#### Topics to revise

- Token usage tracking.
- Prompt compression.
- Context pruning.
- Caching.
- Semantic caching.
- Batching.
- Streaming responses.
- Smaller/faster model routing.
- Fallback models.
- Retry logic.
- Timeout handling.
- Circuit breakers.

#### Example: Cost tracking idea

```python
MODEL_PRICES = {
    "example-model": {
        "input_per_1k": 0.001,
        "output_per_1k": 0.002,
    }
}


def estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    price = MODEL_PRICES[model]
    return (
        (input_tokens / 1000) * price["input_per_1k"]
        + (output_tokens / 1000) * price["output_per_1k"]
    )
```

#### Common interview question
##### How do you reduce LLM cost and latency?

**Answer:**

I would reduce unnecessary context, use efficient chunk retrieval, cache repeated responses, choose the smallest model that meets quality requirements, batch requests when appropriate, stream responses for user experience, monitor token usage, and route complex requests to stronger models only when necessary.

---

### 10. API Security
#### 10.1 How can we secure an API?
##### Strong Answer

> To secure an API, I would apply security at multiple layers: authentication, authorization, input validation, transport security, rate limiting, proper CORS, secrets management, and monitoring.

---

#### 10.2 Common API security methods

|           Area           |               How to secure                |
| ------------------------ | ------------------------------------------ |
| Authentication           | JWT, OAuth2, API keys                      |
| Authorization            | RBAC, permissions, scopes                  |
| Transport security       | HTTPS/TLS                                  |
| Input validation         | Pydantic/schema validation                 |
| Rate limiting            | Prevent abuse and DDoS                     |
| CORS                     | Allow only trusted frontend domains        |
| Secrets                  | Store in env vars or secret manager        |
| SQL injection prevention | ORM or parameterized queries               |
| Logging/monitoring       | Track suspicious behavior                  |
| Token expiry             | Short-lived access tokens + refresh tokens |

---

#### 10.3 FastAPI security-style example

```python
from fastapi import Depends, FastAPI, HTTPException, status

app = FastAPI()

def verify_token(token: str):
    if token != "valid-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return True

@app.get("/secure-data")
def secure_data(is_auth: bool = Depends(verify_token)):
    return {"message": "Secure API response"}
```

---

#### 10.4 Strong one-liner

> API security is not just authentication; it includes authentication, authorization, validation, encryption, rate limiting, CORS, secrets management, and observability.

---

### 12. AI Production Challenges
#### 12.1 What is the most challenging problem you faced while working with AI?
##### Recommended Answer: Hallucinations and response reliability

> One of the biggest challenges I encountered while working with AI systems was ensuring response reliability and reducing hallucinations. Large language models can sometimes generate confident but incorrect information, which becomes a serious issue when the output is used for resumes, recommendations, job applications, or business decisions.
>
> To address this, I used structured prompts, validation layers, output schemas, and context grounding. For example, in resume optimization workflows, I restricted the model to work only with information already present in the resume and job description instead of allowing it to invent new experience or skills.
>
> The key lesson I learned is that building a production AI system is often more about controlling and validating model outputs than simply calling an LLM API.

---

#### 12.2 Other AI challenges to mention
##### Latency and scalability

Traditional APIs may respond in milliseconds, but LLM calls can take seconds.

Ways to improve:

- Async FastAPI endpoints
- Caching
- Prompt optimization
- Background workers
- Request queues
- Streaming responses

---

##### Context management

Too little context leads to poor answers.
Too much context increases cost, latency, and token usage.

Solutions:

- Chunking
- Embeddings
- Vector search
- Reranking
- Context window management

---

##### Evaluation difficulty

AI outputs are harder to test than deterministic software.

Possible evaluation methods:

- Golden datasets
- Human review
- Automated scoring
- Exact match for structured tasks
- Semantic similarity
- Hallucination checks
- Regression testing

---

#### 12.3 What is RAG?

RAG stands for **Retrieval-Augmented Generation**.

It combines information retrieval with LLM generation.

##### Flow

```text
User query
   ↓
Create embedding
   ↓
Search vector database
   ↓
Retrieve relevant context
   ↓
Send context + query to LLM
   ↓
Generate grounded answer
```

---

#### 12.4 Why use RAG?

RAG helps:

- Reduce hallucinations
- Use private/company documents
- Improve factual grounding
- Keep answers up to date with external knowledge
- Avoid putting everything into the prompt manually

---

#### 12.5 What are embeddings?

Embeddings convert text into numerical vectors that capture semantic meaning.

They are used for:

- Semantic search
- Similarity matching
- Clustering
- Recommendations
- RAG pipelines

---

#### 12.6 Vector databases

Common examples:

- FAISS
- ChromaDB
- Pinecone
- Weaviate

They store embeddings and support similarity search.

---

### 9. Production Reliability, Observability, Incidents, and Runbooks
#### 9.1 Diagnosing latency and incorrect predictions in ML API
##### Step-by-step approach

1. Treat as production incident.
2. Assess user/business impact.
3. Stabilize with rollback/fallback if needed.
4. Compare p50/p95/p99 latency against baseline.
5. Correlate incorrect predictions with latency windows.
6. Check recent deployments/config changes.
7. Validate model inputs and feature freshness.
8. Replay golden test cases.
9. Apply targeted fix.
10. Add missing observability.

---

#### 9.2 Distinguishing infra vs data pipeline vs model degradation
##### Infrastructure signals

- CPU/GPU/memory saturation.
- Pod restarts.
- Autoscaling events.
- DB/cache latency.
- Traffic spikes.

##### Data pipeline signals

- Schema changes.
- Null/default spikes.
- Feature freshness issues.
- Drift.
- Failed upstream jobs.

##### Model degradation signals

- Model/config version changed.
- Golden test performance dropped.
- Prediction confidence distribution shifted.
- Same clean input produces worse output.

---

#### 9.3 Handling contradictory monitoring data
##### Decision principle

> Do not force data to fit the first hypothesis. Choose the lowest-risk reversible action that protects users.

##### Safe actions

- Rollback.
- Route to fallback.
- Disable new feature flag.
- Increase human review for high-risk outputs.
- Preserve logs/metrics for later RCA.

---

#### 9.4 Alerting without alert fatigue
##### Principles

- Alert on symptoms, not every metric.
- Use severity levels.
- Use time windows.
- Group related alerts.
- Alert only when action is required.
- Every alert should have a runbook.

##### Example

Bad:

```text
Single pod restarted once
```

Good:

```text
p99 redirect latency > SLA for 5 minutes and error rate > threshold
```

---

#### 9.5 Game day / incident readiness testing
##### Scenarios

- Cache outage.
- DB replica lag.
- Region failure.
- Traffic spike.
- Bad deployment.
- Dependency timeout.

##### Measure

- Time to detect.
- Time to mitigate.
- Alert quality.
- Runbook usefulness.
- Escalation path.
- Customer impact.

---

#### 9.6 On-call runbooks
##### Runbook structure

- Service overview.
- Critical dependencies.
- Common alerts.
- Investigation steps.
- Recovery actions.
- Safety notes.
- Escalation path.
- Validation checks.
- Post-incident actions.

##### Measuring effectiveness

- MTTR.
- Escalation frequency.
- Game day performance.
- On-call feedback.
- Repeat incident recovery time.

---

#### 9.7 Disaster recovery
##### Key terms

- **RTO:** how fast service must recover.
- **RPO:** acceptable data loss.

##### DR design

- Multi-AZ deployment.
- Automated backups.
- Point-in-time recovery.
- Cross-region replication for critical systems.
- Stateless services.
- DNS/traffic failover.
- Regular restore testing.

##### Validating DR

- Failover drills.
- Backup restoration tests.
- Data consistency checks.
- Chaos/game day exercises.
- Measure actual RTO/RPO.

---

### 14. Security, Privacy, PII, and Access Control
#### 14.1 Handling PII in GenAI systems
##### Main principle

> Sensitive data should not be sent to the model unless absolutely necessary, and should be masked/tokenized whenever possible.

##### Steps

1. Detect PII.
2. Minimize data sent.
3. Mask/tokenize sensitive values.
4. Keep raw PII in secure backend services.
5. Redact logs/traces.
6. Filter outputs for leakage.
7. Use compliant/private model endpoints.
8. Define retention and audit policy.

##### Example masking

```text
John Smith → [CUSTOMER_NAME]
9876543210 → [PHONE_NUMBER]
123 Main Street → [ADDRESS]
```

---

#### 14.2 Authentication and authorization for public APIs
##### First-party web/mobile

- OAuth2/OIDC.
- Short-lived JWTs.
- Refresh tokens.
- HttpOnly cookies for browser clients.
- Secure storage for mobile.

##### External partners

- OAuth2 client credentials.
- Client ID/secret.
- Scopes.
- Optional mTLS for sensitive partners.

##### Authorization

- RBAC/ABAC.
- Tenant isolation.
- Scope checks.
- Audit logs.

---

#### 14.3 Credential and signing key rotation without downtime
##### JWT signing keys

- Use `kid` header.
- Publish JWKS.
- Add new key before using it.
- Start signing with new key.
- Accept old key until tokens expire.
- Remove old key after safe window.

##### Client secrets

- Support multiple active secrets.
- Add new secret.
- Partner migrates.
- Monitor usage.
- Revoke old secret.

---

#### 14.4 Internal component access control
##### Design

- Each service gets identity.
- Least privilege.
- mTLS or signed JWT for service-to-service calls.
- Policy enforcement.
- Secrets isolation.
- Audit sensitive actions.

##### Example

```text
Redirect service → read URL mappings only
Creation service → create/update mappings
Analytics service → write events only
Admin service → restricted elevated access
```

---

#### 14.5 Auditing permissions over time
##### Practices

- Central inventory of service identities and permissions.
- Automated policy checks.
- Detect wildcard permissions.
- Detect unused permissions.
- Periodic access reviews.
- Drift detection between IaC and live environment.
- Audit trail of permission changes.

---

#### 14.6 Tamper-resistant audit logs
##### Requirements

- Append-only logs.
- Strict access control.
- Actor/action/resource/timestamp/IP/request ID/reason.
- Immutable storage such as WORM/S3 Object Lock.
- Hash each log entry.
- Optional hash chaining.

##### Example event

```json
{
  "actor": "admin_123",
  "action": "DISABLE_SHORT_LINK",
  "resource": "short_abc",
  "timestamp": "2026-01-01T12:00:00Z",
  "request_id": "req_789",
  "reason": "phishing report"
}
```

---

### 13. Monitoring, Logging, Reliability & Alerts
#### What to Monitor

|           Area           |               Example Metric                |
| ------------------------ | ------------------------------------------- |
| Pipeline success/failure | Job status                                  |
| Freshness                | Latest transaction date                     |
| Volume                   | Number of records processed                 |
| Data quality             | Failed validation count                     |
| Duplicates               | Duplicate transaction count                 |
| Latency                  | Time from S3 arrival to report availability |
| Cost                     | Compute and storage cost                    |
| Error records            | Quarantine count                            |

#### Reliability Patterns

|      Pattern      |          Purpose           |
| ----------------- | -------------------------- |
| Retries           | Handle transient failures  |
| Dead-letter queue | Store failed events        |
| Quarantine folder | Store invalid records      |
| Checkpointing     | Resume processing safely   |
| Watermarking      | Track incremental progress |
| Idempotent writes | Prevent duplicate data     |
| Alerts            | Notify failures quickly    |

#### Example Monitoring Flow

```text
ETL Job
  ├── Logs → CloudWatch / Logging System
  ├── Metrics → Dashboard
  ├── Failures → Alert via Email/SNS/Slack
  └── Bad Records → Quarantine Folder
```

##### Interview Answer

> “I would monitor pipeline health, record counts, data freshness, validation failures, duplicate rate, and job latency. I would also add retries, alerting, quarantine handling, and idempotent writes to make the pipeline reliable.”

---

### 9. Testing With Pytest
#### Likely Questions

- How do you write tests in Python?
- What is pytest?
- Difference between unit, integration, and end-to-end tests?
- How do you test APIs?
- How do you mock external services?
- How do you test background jobs?
- How do you test AI features?
- What should be included in CI?

---

#### Unit Test Example

```python
def calculate_order_total(items):
    return sum(item["price"] * item["quantity"] for item in items)


def test_calculate_order_total():
    items = [
        {"price": 10.0, "quantity": 2},
        {"price": 5.0, "quantity": 1},
    ]

    assert calculate_order_total(items) == 25.0
```

---

#### FastAPI Test Example

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_order():
    response = client.post(
        "/orders",
        json={
            "customer_id": 1,
            "total_amount": 99.99,
            "currency": "CAD",
        },
    )

    assert response.status_code == 201
    assert response.json()["status"] == "created"
```

---

#### Mocking External API Example

```python
from unittest.mock import Mock


def test_sync_order_success():
    fake_client = Mock()
    fake_client.sync_order.return_value = {"status": "ok"}

    result = sync_order(order_id=123, client=fake_client)

    assert result["status"] == "ok"
    fake_client.sync_order.assert_called_once_with(123)
```

---

#### Testing AI Features

For AI features, test:

- Prompt construction
- Input validation
- Output schema validation
- Fallback behavior
- Empty context behavior
- Safety checks
- Logging metadata

```python
def test_invalid_llm_output_is_rejected():
    invalid_response = '{"issue_type": "unknown", "urgency": "extreme"}'

    with pytest.raises(ValidationError):
        OrderIssue.model_validate_json(invalid_response)
```

---

### 14. Monitoring, Logging & Production Support
#### Likely Questions

- How do you handle production issues?
- How do you debug a production incident?
- What metrics do you monitor?
- What logs are useful?
- What is alert fatigue?
- How do you write useful logs?
- What is a postmortem?
- How do you decide whether to rollback?

---

#### Production Incident Answer Format

Use this structure:

1. Assess user/business impact
2. Communicate status clearly
3. Check recent deployments
4. Review logs, metrics, and traces
5. Mitigate quickly
6. Rollback if needed
7. Fix root cause
8. Add tests/monitoring
9. Write postmortem if serious

##### Sample Answer

> When production issues happen, I first assess the impact and severity. Then I check logs, metrics, recent deployments, dependency health, and database behavior. If the issue is actively affecting users, I focus on mitigation first, such as rollback, feature flag disablement, or temporary workaround. After stabilizing, I investigate root cause and add tests, monitoring, or process improvements to prevent recurrence.

---

#### Structured Logging Example

```python
import logging

logger = logging.getLogger(__name__)


def process_payment(order_id: int, amount: float):
    logger.info(
        "Processing payment",
        extra={
            "order_id": order_id,
            "amount": amount,
            "component": "payments",
        },
    )

    try:
        result = payment_gateway.charge(order_id, amount)
        logger.info("Payment successful", extra={"order_id": order_id})
        return result

    except Exception:
        logger.exception("Payment failed", extra={"order_id": order_id})
        raise
```

---

#### Useful Metrics

Monitor:

- Request latency
- Error rate
- Throughput
- Queue depth
- Job failure rate
- Database query latency
- CPU/memory
- API dependency failures
- LLM cost/latency/error rate
- Payment/order failure rate

---

#### Postmortem Template

```text
Incident:
Impact:
Timeline:
Root Cause:
Detection:
Resolution:
What went well:
What went wrong:
Action items:
Owner:
Due date:
```

---

## Reliability Lessons from an Incident Alert Router

Small control-flow mistakes can create serious operational errors in incident systems.

### Do Not Return Failure Before the Search Is Complete

This implementation is incorrect:

```python
for alert in alerts:
    if alert.service == service:
        return alert.resolved_at is None
```

A resolved alert may appear before a later open alert for the same service. The correct predicate searches for any matching open alert:

```python
return any(
    alert.service == service and alert.resolved_at is None
    for alert in alerts
)
```

### Retry Backoff Validation

For each alert, sort delivery attempts by timestamp and compare adjacent attempts. A pair violates policy only when:

```python
current.attempted_at - previous.attempted_at < cooldown
```

A gap exactly equal to the cooldown is compliant.

### High-Value Tests

- Resolved alert followed by an open alert for the same service.
- Service with no alerts.
- Unknown alert ID when recording an attempt.
- Alert with no attempts, which must be omitted from count output.
- Attempts inserted out of order.
- Gap one unit below the cooldown.
- Gap exactly equal to the cooldown.
- Several violating pairs for one alert, which should produce one alert ID.

### Production Considerations

A list scan is acceptable for an interview exercise. A production router would usually add:

- An index keyed by alert ID for constant-time lookup.
- An index or query on `(service, resolved_at)` for open-alert checks.
- Durable storage and transactional updates.
- Idempotency keys for repeated delivery-attempt events.
- Metrics for attempts, failures, policy violations, and notification latency.
- Audit logs showing who was contacted and when.

---

## Security and Escalation Guardrails for Customer-Support Agents

Customer-support agents often combine public information with sensitive account data. The safest design is to define a hard verification boundary and enforce it in application code rather than relying only on prompt instructions.

### Verification Boundary

For an order-specific workflow:

1. Customer provides an order identifier plus the email address or phone number already on file.
2. The system returns the same generic response whether those details match or not, so it does not confirm account existence.
3. Send a one-time code only to the contact already stored on the account/order.
4. Rate-limit verification attempts.
5. Only after successful verification may order-specific tools be used.

Never ask for:

- Passwords.
- Full payment-card numbers.
- Security answers that the support system does not genuinely require.
- A new email or phone number as the destination for the verification code.

### Zero Order-Specific Disclosure Before Verification

Before verification, do not reveal or confirm:

- Whether the order exists.
- Order status.
- Products or quantities.
- Prices or totals.
- Tracking number or carrier tied to that order.
- Shipping or billing address.
- Refund history or eligibility.

Generic policies, product descriptions, and public catalog information can remain available without account verification.

### Minimize Disclosure After Verification

Successful verification does not mean every field should be shown. Return only what is necessary for the active task and mask sensitive fields where possible.

### High-Risk Actions and Warm Handoffs

Some workflows should remain human-controlled even after authentication. Examples include:

- Shipping-address changes.
- Order cancellation.
- Executing a refund.
- Policy exceptions for final-sale items.
- Fraud or account-takeover concerns.

The agent can still reduce support effort by collecting the relevant order number, requested change, reason, supporting evidence, and current state, then creating a warm handoff so the human does not need to repeat discovery.

### Damage, Defect, or Wrong-Item Reports

A support agent may request photos through a secure upload flow when they help a human reviewer. Photos should be optional supporting evidence rather than a reason to deny escalation when the customer cannot provide them.

Useful handoff fields:

- Affected item.
- Issue type: damaged, defective, or wrong item.
- Description.
- Photos when available.
- Preferred resolution.
- Verified order context.

### Escalation Triggers

Immediately route to a human when the conversation involves:

- Legal threats or requests for legal interpretation.
- Chargebacks or regulator complaints.
- Fraud or account-takeover concerns.
- Safety issues.
- Explicit request for a human.
- Severe anger or abuse where continued automation is unlikely to help.

The bot should remain calm, avoid arguing, avoid making legal admissions, and preserve the relevant conversation context for the reviewer.

### Multi-Tenant AI Data Isolation

For SaaS or financial systems with multiple organizations:

- Derive tenant identity from the authenticated session/token, never from model-generated arguments.
- Apply tenant and object-level authorization again when each tool executes.
- Filter vector/keyword retrieval by tenant before documents are returned to the LLM.
- Use least-privilege service credentials for external tools.
- Prevent one tenant's cache entries, embeddings, traces, or conversation state from being visible to another.
- Redact unnecessary PII and secrets from logs and model context.
- Keep auditable records of sensitive reads, writes, approvals, and escalations.

Prompt instructions are not an authorization mechanism. Even if a prompt-injection attempt asks the model to ignore tenant boundaries, the data and tool layers should make cross-tenant access impossible.

### Fresh-State and Audit Requirements

For any financial eligibility check or other time-sensitive decision:

- Re-read the authoritative record before handoff/action.
- Log who/what initiated the check.
- Record the policy result and source data version/timestamp where practical.
- Do not reuse cached eligibility from a different intent or earlier task.
- Clear task-local state when the order, intent, or authentication state changes.

### High-Value Security Tests

Test at least these cases:

1. Valid order ID but wrong email/phone does not reveal whether the order exists.
2. OTP is sent only to the stored contact destination.
3. Order tools are blocked before verification.
4. Authentication for one order cannot unlock a different order.
5. Intent change clears task-local sensitive cache.
6. Address change, cancellation, and refund execution always escalate when configured as human-only.
7. Final-sale exception requests route to a human.
8. Legal/fraud/chargeback language triggers immediate escalation.
9. Repeated OTP attempts are rate-limited.
10. Logs do not contain full OTPs, card numbers, or unnecessary PII.

**Interview answer:**

> I separate public support from account-specific support with a hard authentication boundary. Before verification, the agent cannot even confirm that an order exists. After order-plus-contact verification and an OTP sent only to the stored contact, it can access only the data needed for the active task. High-risk actions remain human-controlled, and legal, fraud, chargeback, or safety concerns escalate immediately with a context-rich handoff.

---

## Reliability Lessons from Load-Related Application Crashes

When an overloaded application is actively failing for customers, separate **incident mitigation** from **long-term remediation**.

### Mitigation vs Remediation

|    Phase    |                         Goal                         |                                         Examples                                         |
| ----------- | ---------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Mitigation  | Restore acceptable service with the lowest-risk move | Rollback, restart unhealthy instances, add temporary capacity, shed non-critical load    |
| Remediation | Remove the underlying failure mode                   | Horizontal scaling, caching, query optimization, autoscaling changes, architecture fixes |

Do not attempt a large redesign while the service is unavailable. First stabilize the customer-facing path, preserve evidence, and reduce the blast radius.

### Immediate Response to a Load-Related Crash

A safe sequence is:

1. Confirm the scope and customer impact.
2. Check CPU, memory, OOM events, restarts, latency, error rate, DB connections, queue depth, and dependency health.
3. Check recent deployments/configuration changes so a bad release is not mistaken for pure capacity pressure.
4. Apply the smallest reversible mitigation likely to restore service.
5. Preserve logs, traces, metrics, and timestamps for root-cause analysis.
6. Monitor closely while the service recovers.
7. Implement and validate the durable fix after stability is restored.

Possible short-term mitigations, depending on the system, include:

- Restart or replace unhealthy instances.
- Temporarily increase CPU/memory capacity.
- Add replicas if dependencies can safely absorb the load.
- Disable or defer non-essential background work.
- Rate-limit or shed expensive non-critical traffic.
- Disable a problematic feature with a feature flag.
- Roll back a recent change if it is contributing to the failure.

The correct action depends on evidence. Adding replicas blindly can worsen an already saturated database.

**Interview answer:**

> During an active incident, I separate mitigation from remediation. My first goal is to restore the core customer journey with the lowest-risk reversible action, while preserving enough telemetry for diagnosis. That may mean replacing unhealthy instances, adding temporary capacity, shedding non-critical work, or rolling back. Once the system is stable, I address the root cause through scaling, caching, query or connection-pool optimization, autoscaling changes, and stronger load testing.

### Observe the User Journey, Not Only Infrastructure

For overload incidents, correlate infrastructure metrics with user-facing service-level indicators:

- Request success rate.
- p95/p99 latency.
- Timeout and retry rate.
- Transaction completion rate.
- Stage-level latency for critical workflow steps.
- CPU/memory saturation.
- DB query latency and connection-pool exhaustion.
- Cache hit/miss ratio.
- Autoscaling activity.

A service that returns slowly enough to cause customer timeouts is functionally degraded even if every process is still running.

### Preventing the Repeat Incident

Post-incident actions should convert the lesson into engineering controls:

- Update capacity assumptions using measured peak behavior.
- Add missing load/stress tests.
- Define saturation indicators and alert thresholds.
- Tune autoscaling before saturation rather than after failure.
- Add dependency backpressure and rate limits.
- Reduce retry storms with bounded retries and jitter.
- Optimize slow queries and connection pools.
- Add cache where correctness permits.
- Update runbooks with tested recovery actions.
- Validate the fix above expected peak load and during dependency degradation.

A recurring incident should be treated as a prompt to remove the failure mode, not simply to make the on-call response faster.

---

## Repository Debugging Under Time Pressure

When a repository-level assessment has several failing tests, the fastest reliable path is usually to turn the tests into an executable specification before changing code.

### Start With the First Failing Test

Run the narrowest useful command first:

```bash
pytest -q test/test_app.py -x
```

`-x` stops on the first failure so one root cause is not hidden behind a long list of downstream failures. After fixing that failure class, run the full target file and finally the broader suite.

### Extract the Contract From Tests

For each failing test, write down:

- Endpoint and HTTP method.
- Authentication precondition.
- Required request fields.
- Expected status code.
- Required response keys and nested fields.
- Expected persistence side effects.
- Expected relationship or identifier behavior.

A failure such as:

```text
assert "issue" in {}
```

is more informative than just "test failed": it says the route returned a success status with the wrong response shape, so trace how the handler can reach an early success return.

### Trace by Layer

Use a consistent order:

```text
1. URL/route mapping
2. authentication decorator or middleware
3. handler/view
4. model/schema fields
5. serializer/to_dict response shape
6. related side effects such as activity/audit rows
```

This prevents random editing across the repository.

### Compare Broken and Working Paths

If `create_*` is broken but `update_*` or `get_*` works, compare them for established patterns:

- `DoesNotExist` handling.
- Foreign-key assignment.
- `select_related(...)` before serialization.
- Activity/audit creation.
- Error response conventions.
- Field naming differences between request JSON and model attributes.

The goal is not to copy the function blindly; it is to reuse repository conventions already proven by nearby code.

### High-Signal Failure Patterns

Common repository-repair failures include:

- Early `return` before `save()`/`objects.create()`.
- Parsed fields that are never used.
- Request field name differs from model field name.
- Auth wrapper returns a route-specific response body that violates tests.
- Required relation is never looked up.
- Business identifier is derived from the wrong scope.
- Broad `except Exception` converts a precise validation error into a generic `500`.
- A response is generated from stale/unpopulated relationships.

### Use AI as a Diagnostic Copilot, Not a Source of Unverified Patches

When an assessment permits an assistant for explanation but not direct implementation, use it to accelerate repository navigation and hypothesis testing.

Good diagnostic prompts are narrow and evidence-based:

```text
From these tests, summarize the exact POST contract: required fields, status codes,
response keys, identifier rules, and parent-child behavior. Cite the relevant test lines.
```

```text
Trace POST /api/issues from this URL file to the handler. Tell me which middleware runs first,
where persistence should happen, and any early return that can bypass it.
```

```text
Compare the broken create path with the working update path. Identify reusable patterns for
lookups, serialization, assignee handling, and activity creation. Do not modify unrelated files.
```

Then verify every suggestion against source and tests. The assistant is useful for search and comparison; the repository remains the source of truth.

### Final Validation Sequence

1. Focused first failure with `-x`.
2. Entire affected test module.
3. Static/syntax validation.
4. Full relevant suite.
5. Inspect changed files for accidental unrelated edits.
6. If there is a UI reproduction path, verify the customer-visible workflow after backend tests pass.

**Interview answer:**

> In an unfamiliar repository I start from the failing tests, extract the exact contract, and trace one request through route, auth, handler, model, and serializer. I compare the broken path with nearby working code rather than redesigning the repository. I fix one root cause at a time, rerun the narrow test, then expand to the full suite. That keeps the debugging loop evidence-driven and minimizes unrelated changes.
