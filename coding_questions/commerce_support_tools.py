"""Commerce Support Tools: Database Queries, Refund Rules, Live Stock, and Tool Schemas

Build a small tool layer for a customer-support AI agent. The agent must be able to read order details, search a stale product
catalog, determine refund eligibility, and check live warehouse stock through a command-line integration.

The exercise has four parts:

1. get_order_details(order_id)
   - Read the order, customer, and order items from SQLite.
   - Calculate each line using the purchase-time unit price.
   - If the purchase-time price is NULL, fall back to the product's current catalog price.
   - Preserve legitimate zero prices; only NULL triggers the fallback.

2. search_products(query)
   - Perform a case-insensitive partial name search.
   - Use parameterized SQL so input such as quotes or SQL syntax is treated as data rather than executable SQL.

3. check_refund_eligibility(order_id, now)
   - Only completed orders are eligible.
   - Use delivery time as the reference time; if it is missing, fall back to creation time.
   - The standard window is 30 days inclusive.
   - Any final-sale item makes the whole standard refund ineligible.
   - Subtract all prior refunds and clamp the remaining amount at zero.

4. check_realtime_stock(sku)
   - Invoke an external warehouse command as [binary, "CHECK", sku] without shell=True.
   - Enforce a two-second timeout.
   - Parse common JSON, labelled, pipe-separated, or natural-language output variations.
   - Return a controlled error status for timeout, process failure, or malformed output.

Also define OpenAI-compatible function schemas for all four tools.

Key observations:
- Business calculations should remain deterministic and testable outside the LLM.
- SQL parameters protect values, while table/column names should remain application-controlled.
- A zero purchase price is not the same as a missing purchase price.
- Refund calculations must use authoritative stored data rather than model-generated arithmetic.
- External CLI output is untrusted input and should be parsed defensively.

Complexity:
- get_order_details is O(i) for i order items after indexed lookups.
- search_products is O(p) without a suitable search index; the exact database cost depends on indexing and query plan.
- check_refund_eligibility is O(i + r) for order items and prior refund rows.
- check_realtime_stock is dominated by the external process call.

Important edge cases include nonexistent orders, orders with no items, NULL and zero prices, mixed-case search, SQL-injection-like
input, exactly 30 days versus more than 30 days, malformed dates, final-sale items, multiple previous refunds, stock quantity zero,
warehouse timeout, non-zero process exit, and malformed warehouse output.
"""

from __future__ import annotations

import json
import re
import sqlite3
import subprocess
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Any, Callable

WAREHOUSE_TIMEOUT_SECONDS = 2


class CommerceSupportTools:
    def __init__(
        self,
        connection: sqlite3.Connection,
        *,
        warehouse_binary: str = "./warehouse_cli",
        process_runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        self.connection = connection
        self.connection.row_factory = sqlite3.Row
        self.warehouse_binary = warehouse_binary
        self.process_runner = process_runner

    def get_order_details(self, order_id: int) -> dict[str, Any] | None:
        order = self.connection.execute(
            """
            SELECT
                o.id AS order_id,
                o.status,
                o.created_at,
                o.delivered_at,
                u.id AS user_id,
                u.name AS user_name,
                u.email AS user_email
            FROM orders AS o
            JOIN users AS u ON u.id = o.user_id
            WHERE o.id = ?
            """,
            (order_id,),
        ).fetchone()

        if order is None:
            return None

        rows = self.connection.execute(
            """
            SELECT
                oi.product_id,
                oi.quantity,
                oi.unit_price AS purchase_unit_price,
                p.name,
                p.sku,
                p.price AS current_price,
                p.is_final_sale
            FROM order_items AS oi
            JOIN products AS p ON p.id = oi.product_id
            WHERE oi.order_id = ?
            ORDER BY oi.id
            """,
            (order_id,),
        ).fetchall()

        items: list[dict[str, Any]] = []
        total = Decimal("0")

        for row in rows:
            purchase_price = row["purchase_unit_price"]
            unit_price = Decimal(
                str(row["current_price"] if purchase_price is None else purchase_price)
            )
            quantity = int(row["quantity"])
            subtotal = unit_price * quantity
            total += subtotal

            items.append(
                {
                    "product_id": row["product_id"],
                    "name": row["name"],
                    "sku": row["sku"],
                    "quantity": quantity,
                    "unit_price": float(unit_price),
                    "subtotal": float(subtotal),
                    "is_final_sale": bool(row["is_final_sale"]),
                }
            )

        return {
            "order_id": order["order_id"],
            "status": order["status"],
            "created_at": order["created_at"],
            "delivered_at": order["delivered_at"],
            "user": {
                "id": order["user_id"],
                "name": order["user_name"],
                "email": order["user_email"],
            },
            "items": items,
            "total": float(total),
        }

    def search_products(self, query: str) -> list[dict[str, Any]]:
        rows = self.connection.execute(
            """
            SELECT id, name, sku, price, is_final_sale
            FROM products
            WHERE name LIKE ? COLLATE NOCASE
            ORDER BY name, id
            """,
            (f"%{query}%",),
        ).fetchall()
        return [dict(row) for row in rows]

    def check_refund_eligibility(
        self,
        order_id: int,
        *,
        now: datetime | None = None,
    ) -> dict[str, Any]:
        details = self.get_order_details(order_id)
        if details is None:
            return {
                "eligible": False,
                "refundable_amount": 0.0,
                "reason": "order_not_found",
            }

        if str(details["status"]).lower() != "completed":
            return {
                "eligible": False,
                "refundable_amount": 0.0,
                "reason": "order_not_completed",
            }

        reference_value = details["delivered_at"] or details["created_at"]
        reference_time = _parse_iso_datetime(reference_value)
        if reference_time is None:
            return {
                "eligible": False,
                "refundable_amount": 0.0,
                "reason": "invalid_reference_date",
            }

        if now is None:
            now = datetime.now(reference_time.tzinfo or timezone.utc)
        elif reference_time.tzinfo is None and now.tzinfo is not None:
            reference_time = reference_time.replace(tzinfo=now.tzinfo)
        elif reference_time.tzinfo is not None and now.tzinfo is None:
            now = now.replace(tzinfo=reference_time.tzinfo)

        age = now - reference_time
        if age < timedelta(0) or age > timedelta(days=30):
            return {
                "eligible": False,
                "refundable_amount": 0.0,
                "reason": "outside_refund_window",
            }

        if any(item["is_final_sale"] for item in details["items"]):
            return {
                "eligible": False,
                "refundable_amount": 0.0,
                "reason": "contains_final_sale_item",
            }

        refund_row = self.connection.execute(
            """
            SELECT COALESCE(SUM(amount), 0) AS refunded_amount
            FROM refunds
            WHERE order_id = ?
            """,
            (order_id,),
        ).fetchone()
        previously_refunded = Decimal(str(refund_row["refunded_amount"]))
        refundable = max(Decimal("0"), Decimal(str(details["total"])) - previously_refunded)

        return {
            "eligible": refundable > 0,
            "refundable_amount": float(refundable),
            "reason": "eligible" if refundable > 0 else "no_refundable_balance",
        }

    def check_realtime_stock(self, sku: str) -> dict[str, Any]:
        try:
            result = self.process_runner(
                [self.warehouse_binary, "CHECK", sku],
                capture_output=True,
                text=True,
                timeout=WAREHOUSE_TIMEOUT_SECONDS,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return {"sku": sku, "quantity": 0, "status": "TIMEOUT"}
        except OSError:
            return {"sku": sku, "quantity": 0, "status": "ERROR"}

        if result.returncode != 0:
            return {"sku": sku, "quantity": 0, "status": "ERROR"}

        try:
            return _parse_stock_output(result.stdout, requested_sku=sku)
        except (ValueError, TypeError, json.JSONDecodeError):
            return {"sku": sku, "quantity": 0, "status": "ERROR"}


TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_order_details",
            "description": "Retrieve customer and line-item details for a specific order.",
            "parameters": {
                "type": "object",
                "properties": {"order_id": {"type": "integer"}},
                "required": ["order_id"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": (
                "Search the database product catalog by name. Catalog inventory may be stale; "
                "use check_realtime_stock for live quantity of a known SKU."
            ),
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_refund_eligibility",
            "description": "Evaluate the standard refund policy and remaining refundable amount.",
            "parameters": {
                "type": "object",
                "properties": {"order_id": {"type": "integer"}},
                "required": ["order_id"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_realtime_stock",
            "description": "Check current warehouse quantity and availability for a known SKU.",
            "parameters": {
                "type": "object",
                "properties": {"sku": {"type": "string"}},
                "required": ["sku"],
                "additionalProperties": False,
            },
        },
    },
]


def _parse_iso_datetime(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None

    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"

    try:
        return datetime.fromisoformat(normalized)
    except ValueError:
        return None


def _normalize_status(value: str) -> str:
    return re.sub(r"[\s-]+", "_", value.strip().upper())


def _parse_stock_output(text: str, *, requested_sku: str) -> dict[str, Any]:
    payload_text = text.strip()
    if not payload_text:
        raise ValueError("empty output")

    try:
        payload = json.loads(payload_text)
    except json.JSONDecodeError:
        payload = None

    if isinstance(payload, dict):
        quantity = next(
            (payload[key] for key in ("quantity", "qty", "stock") if key in payload),
            None,
        )
        if quantity is None:
            raise ValueError("quantity missing")
        status = next(
            (payload[key] for key in ("status", "state", "availability") if key in payload),
            "UNKNOWN",
        )
        return {
            "sku": str(payload.get("sku", requested_sku)),
            "quantity": int(quantity),
            "status": _normalize_status(str(status)),
        }

    quantity_match = re.search(
        r"\b(?:qty|quantity|stock)\s*[:=]?\s*(-?\d+)\b",
        payload_text,
        re.IGNORECASE,
    ) or re.search(r"\b(-?\d+)\s*units?\b", payload_text, re.IGNORECASE)
    if quantity_match is None:
        raise ValueError("quantity missing")

    sku_match = re.search(
        r"\bSKU\s*[:=]?\s*([A-Za-z0-9._-]+)",
        payload_text,
        re.IGNORECASE,
    )
    status_match = re.search(
        r"\b(?:status|state|availability)\s*[:=]?\s*([A-Za-z][A-Za-z _-]*)",
        payload_text,
        re.IGNORECASE,
    )

    if status_match is not None:
        status = status_match.group(1).strip(" |,;")
    else:
        lowered = payload_text.lower()
        if "out of stock" in lowered:
            status = "OUT_OF_STOCK"
        elif "in stock" in lowered:
            status = "IN_STOCK"
        elif "not found" in lowered:
            status = "NOT_FOUND"
        elif "available" in lowered:
            status = "AVAILABLE"
        else:
            status = "UNKNOWN"

    return {
        "sku": sku_match.group(1) if sku_match else requested_sku,
        "quantity": int(quantity_match.group(1)),
        "status": _normalize_status(status),
    }


def _seed_database() -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.executescript(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        );

        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            sku TEXT NOT NULL UNIQUE,
            price REAL NOT NULL,
            is_final_sale INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            delivered_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE order_items (
            id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        );

        CREATE TABLE refunds (
            id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id)
        );
        """
    )
    connection.executemany(
        "INSERT INTO users(id, name, email) VALUES (?, ?, ?)",
        [(1, "Avery", "avery@example.com")],
    )
    connection.executemany(
        "INSERT INTO products(id, name, sku, price, is_final_sale) VALUES (?, ?, ?, ?, ?)",
        [
            (10, "Travel Mug", "MUG-10", 25.0, 0),
            (11, "Sample Sticker", "STICKER-11", 3.0, 0),
            (12, "Clearance Hat", "HAT-12", 15.0, 1),
        ],
    )
    connection.executemany(
        "INSERT INTO orders(id, user_id, status, created_at, delivered_at) VALUES (?, ?, ?, ?, ?)",
        [
            (100, 1, "completed", "2026-07-01T10:00:00+00:00", "2026-07-05T10:00:00+00:00"),
            (101, 1, "completed", "2026-07-01T10:00:00+00:00", "2026-07-05T10:00:00+00:00"),
        ],
    )
    connection.executemany(
        "INSERT INTO order_items(id, order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?, ?)",
        [
            (1, 100, 10, 2, 20.0),
            (2, 100, 11, 1, None),
            (3, 101, 12, 1, 12.0),
        ],
    )
    connection.execute("INSERT INTO refunds(order_id, amount) VALUES (?, ?)", (100, 10.0))
    connection.commit()
    return connection


def run_sample_tests() -> None:
    connection = _seed_database()

    calls: list[dict[str, Any]] = []

    def fake_runner(command: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        calls.append({"command": command, **kwargs})
        return subprocess.CompletedProcess(
            command,
            returncode=0,
            stdout="SKU=MUG-10 | quantity: 7 | status: in stock",
            stderr="",
        )

    tools = CommerceSupportTools(connection, process_runner=fake_runner)

    details = tools.get_order_details(100)
    assert details is not None
    # Purchase price 20 * 2 plus NULL fallback to current product price 3.
    assert details["total"] == 43.0
    assert details["items"][0]["unit_price"] == 20.0
    assert details["items"][1]["unit_price"] == 3.0
    assert tools.get_order_details(999) is None

    assert [row["sku"] for row in tools.search_products("mUg")] == ["MUG-10"]
    # SQL-looking input is handled as a search value and does not alter the database.
    assert tools.search_products("%' OR 1=1 --") == []
    assert connection.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 3

    now = datetime(2026, 8, 4, 10, 0, tzinfo=timezone.utc)  # exactly 30 days after delivery
    eligibility = tools.check_refund_eligibility(100, now=now)
    assert eligibility == {
        "eligible": True,
        "refundable_amount": 33.0,
        "reason": "eligible",
    }

    too_late = tools.check_refund_eligibility(
        100,
        now=datetime(2026, 8, 4, 10, 0, 1, tzinfo=timezone.utc),
    )
    assert not too_late["eligible"]
    assert too_late["reason"] == "outside_refund_window"

    final_sale = tools.check_refund_eligibility(101, now=now)
    assert not final_sale["eligible"]
    assert final_sale["reason"] == "contains_final_sale_item"

    stock = tools.check_realtime_stock("MUG-10")
    assert stock == {"sku": "MUG-10", "quantity": 7, "status": "IN_STOCK"}
    assert calls[0]["timeout"] == 2
    assert calls[0]["command"] == ["./warehouse_cli", "CHECK", "MUG-10"]

    assert {schema["function"]["name"] for schema in TOOL_SCHEMAS} == {
        "get_order_details",
        "search_products",
        "check_refund_eligibility",
        "check_realtime_stock",
    }

    connection.close()
    print("All commerce support tool sample tests passed.")


if __name__ == "__main__":
    run_sample_tests()


"""
Explanation:
1. SQL values are always passed through placeholders. The query text is controlled by the application, while user-provided search
   strings and IDs are values only.
2. Order totals use the historical purchase price whenever it exists. The explicit `is None` check preserves a legitimate zero.
3. Refund eligibility composes deterministic business rules: status, time window, final-sale restriction, then remaining balance.
4. Live stock uses a bounded external process call and treats stdout as untrusted input. Parsing accepts several common formats but
   returns a controlled error instead of inventing missing quantity data.
5. The function schemas explain both the input shape and the semantic difference between catalog search and real-time inventory.

Summary:
- Keep authoritative calculations outside the model.
- Parameterize SQL and validate external-system output.
- Treat exact date boundaries and NULL-versus-zero semantics deliberately.
- Give agents narrow, well-described tools instead of broad database or shell access.
"""
