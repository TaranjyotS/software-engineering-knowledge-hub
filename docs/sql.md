# SQL, Databases, ORM, Caching & Idempotency

> **Purpose:** SQL fundamentals, analytical SQL, data modeling, ORM, caching, transactions, idempotency, and database performance.
> **Use this file for:** SQL interviews, backend database rounds, and data engineering interviews

---

## Recommended Study Flow

1. Read the **Quick Summary** first.
2. Review the **Key Concepts** and tables.
3. Practice the **Interview Questions & Answers** out loud.
4. Use the code snippets and examples to explain trade-offs clearly.
5. Finish with the **Common Mistakes** and **Revision Checklist** sections.

---

## Quick Summary

This file has been refreshed to keep the original repository topic while merging relevant detailed Q&A from the consolidated topic-wise interview-prep pack. Use the top sections for fast revision and the consolidated section for deeper interview preparation.

---

## Core Topics to Master

- DDL, DML, DCL, TCL
- Primary keys, foreign keys, unique constraints
- JOINs, GROUP BY, HAVING, subqueries
- Window functions: ROW_NUMBER, RANK, DENSE_RANK
- Transactions and ACID
- Indexes and query optimization
- ORM performance and N+1 queries
- Caching and idempotency patterns

---

## Consolidated Interview Questions & Technical Notes

> SQL patterns, joins, window functions, relational modeling, ORM performance, Django/SQLAlchemy, caching, idempotency, transactions, and data consistency.

---

### 11. SQL Interview Patterns

#### 11.1 Top 3 orders per customer

```sql
SELECT *
FROM (
    SELECT
        o.*,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY amount DESC
        ) AS rn
    FROM orders o
) t
WHERE rn <= 3;
```

**Pattern:** Top N per group using `ROW_NUMBER()`.

---

#### 11.2 Type 2 SCD as-of join

```sql
SELECT *
FROM orders o
JOIN customer_address a
  ON o.customer_id = a.customer_id
 AND o.order_date >= a.effective_start
 AND (
      o.order_date < a.effective_end
      OR a.effective_end IS NULL
 );
```

**Pattern:** Join facts to the dimension version active at the event date.

---

#### 11.3 Monthly spend increased for 3 consecutive months

```sql
WITH m AS (
  SELECT
      customer_id,
      DATE_TRUNC('month', order_date) AS month,
      SUM(amount) AS total_amount
  FROM orders
  GROUP BY customer_id, DATE_TRUNC('month', order_date)
),
x AS (
  SELECT
      *,
      CASE
          WHEN total_amount > LAG(total_amount) OVER (
              PARTITION BY customer_id
              ORDER BY month
          ) THEN 1
          ELSE 0
      END AS increased
  FROM m
)
SELECT
    customer_id,
    month,
    total_amount
FROM x
QUALIFY SUM(increased) OVER (
    PARTITION BY customer_id
    ORDER BY month
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
) = 3;
```

**Pattern:** Aggregate monthly, compare with `LAG`, then use a rolling window.

---

### 10. Databases, ORM, and Data Modeling

#### Topics to revise

- Relational databases.
- SQL basics.
- Indexing.
- Normalization.
- Transactions.
- SQLAlchemy ORM.
- Migrations.
- Connection pooling.
- Data modeling.

#### Example: SQLAlchemy model

```python
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    storage_path = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
```

#### Common interview questions

1. What is an ORM?
2. What are the benefits and risks of using an ORM?
3. How do indexes improve query performance?
4. How would you model documents and embeddings?
5. How do you handle migrations?

---

### 16. Databases, Caching, and Messaging Systems

#### Databases

Topics mentioned or implied:

- PostgreSQL.
- MySQL.
- SQLAlchemy.
- Data modeling.
- Transactions.
- Indexes.

#### Redis

Redis can be used for:

- Caching.
- Rate limiting.
- Session storage.
- Job status tracking.
- Semantic cache metadata.

#### Kafka / SQS / Queue Systems

Messaging systems are used for asynchronous workloads.

Examples:

- Document ingestion.
- Embedding generation.
- Email notifications.
- Background LLM processing.
- Event-driven pipelines.

#### Common interview question

##### When would you use a queue?

**Answer:**

Use a queue when a task is slow, asynchronous, retryable, or should not block the API request. For example, document parsing and embedding generation can be queued so the API remains responsive while background workers process the document.

---

### 3. REST API Design and Idempotency

#### 3.1 Idempotent HTTP methods

##### Idempotent methods

- `GET`
- `PUT`
- `DELETE`
- `HEAD`
- `OPTIONS`

##### Not idempotent by default

- `POST`

##### Why it matters

Idempotency determines whether clients can safely retry after timeouts or network failures.

##### Example

```text
GET /orders/123      → safe to retry
PUT /profile/123     → safe if same payload
DELETE /users/123    → safe final state remains deleted
POST /orders         → unsafe unless idempotency key is used
```

---

#### 3.2 Safely retriable POST endpoint

##### Problem

A client retries `POST /orders` after timeout. Without protection, duplicate orders may be created.

##### Solution

Use an `Idempotency-Key`.

```http
POST /api/v1/orders
Authorization: Bearer <token>
Idempotency-Key: 7f6d2a91-8c4e-4b8b-9c2e-12345
Content-Type: application/json
```

##### Store

- Client/user ID.
- Idempotency key.
- Request hash.
- Status: `PROCESSING`, `SUCCEEDED`, `FAILED`.
- Response body.
- Status code.
- Safe response headers.

---

#### 3.3 Request/response contract for idempotent create order

##### First response

```http
201 Created
Location: /api/v1/orders/order_789
```

```json
{
  "order_id": "order_789",
  "status": "created"
}
```

##### Retry with same key and same body

Return the same stored response.

```http
201 Created
```

```json
{
  "order_id": "order_789",
  "status": "created"
}
```

##### Same key but different body

```http
409 Conflict
```

```json
{
  "error": "Idempotency key reused with different request payload"
}
```

##### Original request still processing

```http
202 Accepted
Retry-After: 2
```

```json
{
  "status": "processing"
}
```

---

#### 3.4 Exactly-once behavior with RDS and DynamoDB

##### Topic covered

How to avoid duplicate order creation without distributed transactions.

##### Recommended approach

- Use DynamoDB for fast idempotency lookup/replay.
- Use RDS unique constraint as the final correctness guardrail.

##### RDS uniqueness

```sql
UNIQUE (client_id, idempotency_key)
```

##### Why

Even if DynamoDB and RDS are not atomically committed together, RDS prevents duplicate order rows.

##### Recovery scenario

If RDS commits but DynamoDB update fails:

- Retry sees idempotency record stuck in `PROCESSING`.
- Backend checks RDS by `(client_id, idempotency_key)`.
- If order exists, rebuild response and mark DynamoDB `SUCCEEDED`.

---

#### 3.5 Django implementation of idempotency

##### Model example

```python
class IdempotencyKey(models.Model):
    key = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_hash = models.CharField(max_length=64)
    status = models.CharField(max_length=20)  # PROCESSING, SUCCEEDED, FAILED
    response_body = models.JSONField(null=True, blank=True)
    response_status_code = models.IntegerField(null=True, blank=True)
    response_headers = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "key"],
                name="unique_idempotency_key_per_user",
            )
        ]
```

##### Transaction and lock

```python
from django.db import transaction, IntegrityError
from rest_framework.response import Response

with transaction.atomic():
    try:
        record = IdempotencyKey.objects.create(
            user=request.user,
            key=idempotency_key,
            request_hash=request_hash,
            status="PROCESSING",
        )
        is_owner = True
    except IntegrityError:
        record = (
            IdempotencyKey.objects
            .select_for_update()
            .get(user=request.user, key=idempotency_key)
        )
        is_owner = False

    if record.request_hash != request_hash:
        return Response(
            {"error": "Idempotency key reused with different request"},
            status=409,
        )

    if not is_owner:
        if record.status == "SUCCEEDED":
            return Response(
                record.response_body,
                status=record.response_status_code,
                headers=record.response_headers or {},
            )
        return Response({"status": "processing"}, status=202)
```

##### Key idea

Use unique constraints plus row-level locks to ensure two simultaneous requests do not both process.

---

#### 3.6 REST API versioning

##### Preferred external API style

```text
/api/v1/orders
/api/v2/orders
```

##### Why URL versioning

- Clear for external clients.
- Easy to document.
- Easy to route and monitor.
- Simple deprecation tracking.

##### Three decision factors

1. Client simplicity.
2. Operational visibility.
3. Type of change: breaking vs non-breaking.

---

#### 3.7 Deprecating an old API version

##### Safe process

1. Announce deprecation.
2. Add headers:

```http
Deprecation: true
Sunset: <date>
Link: </api/v2/docs>; rel="successor-version"
```

1. Monitor usage by client/API key.
2. Provide migration guide.
3. Keep old version running during migration window.
4. Sunset only after usage is low and clients are migrated.

---

#### 3.8 Client SDK design

##### SDK responsibilities

- Authentication.
- Timeouts.
- Retries.
- Pagination.
- Error mapping.
- API version compatibility.

##### Example

```python
client = UrlShortenerClient(api_key="...", base_url="https://api.example.com")

client.create_url(long_url, expiry=None, custom_alias=None)
client.get_url(short_code)
client.list_urls(limit=50, cursor=None)
client.delete_url(short_code)
```

##### Custom errors

```python
class RateLimitError(Exception): pass
class AuthenticationError(Exception): pass
class ValidationError(Exception): pass
class NotFoundError(Exception): pass
```

---

### 4. Django and ORM Performance

#### 4.1 Avoiding N+1 queries in nested serialization

##### Use `select_related`

For single-valued relationships:

```python
queryset = Order.objects.select_related("customer")
```

##### Use `prefetch_related`

For many-to-many or reverse FK relationships:

```python
queryset = Order.objects.prefetch_related("items")
```

##### Use `Prefetch` for nested optimization

```python
from django.db.models import Prefetch

queryset = Order.objects.prefetch_related(
    Prefetch("items", queryset=OrderItem.objects.select_related("product"))
)
```

##### Signals of N+1

- Query count grows with row count.
- Same SQL repeated many times.
- Django Debug Toolbar shows repetitive queries.
- APM shows DB time dominating request latency.

---

#### 4.2 Structuring large list endpoints with optional filters

##### Recommended pattern

Use a query builder or custom manager instead of putting all logic in the view.

```python
def build_order_queryset(params):
    qs = Order.objects.all()
    qs = apply_base_selects(qs)
    qs = apply_filters(qs, params)
    qs = apply_annotations(qs, params)
    qs = apply_sorting(qs, params)
    return qs
```

##### Efficient annotations

```python
from django.db.models import Exists, OuterRef, Count, Q

def apply_annotations(qs, params):
    recent_payment = Payment.objects.filter(
        order_id=OuterRef("pk"),
        created_at__gte=params.get("recent_since"),
    )

    return qs.annotate(
        has_recent_payment=Exists(recent_payment),
        failed_payment_count=Count(
            "payments",
            filter=Q(payments__status="failed"),
        ),
    )
```

##### Why this helps

- Readable.
- Testable.
- Easier to optimize.
- Avoids one giant view function.

---

#### 4.3 RESTful filtering and sorting with validation

##### Query parameter example

```http
GET /api/orders?status=paid&customer_id=123&created_after=2026-01-01&sort=-created_at&limit=50
```

##### DRF validation example

```python
class OrderListParamsSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=["pending", "paid", "failed"],
        required=False,
    )
    customer_id = serializers.IntegerField(required=False)
    created_after = serializers.DateField(required=False)
    sort = serializers.ChoiceField(
        choices=["created_at", "-created_at", "amount", "-amount"],
        required=False,
    )
```

##### Safe sort mapping

```python
SORT_MAP = {
    "created_at": "created_at",
    "-created_at": "-created_at",
    "amount": "total_amount",
    "-amount": "-total_amount",
}

order_by = SORT_MAP[validated_data.get("sort", "-created_at")]
qs = qs.order_by(order_by)
```

##### Avoid

```python
qs.order_by(request.GET["sort"])
```

Raw user input should not be passed directly into query construction.

---

### 5. Databases and Data Modeling

#### 5.1 Primary key vs unique constraint

##### Primary key

- Main identifier for a row.
- Cannot be null.
- One primary key per table.
- Common target for foreign keys.

##### Unique constraint

- Enforces business uniqueness.
- Multiple allowed per table.
- Null behavior depends on database.

##### Example

```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    email VARCHAR(255) UNIQUE
);
```

---

#### 5.2 Many-to-many modeling

##### Join table example

```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY
);

CREATE TABLE roles (
    id BIGINT PRIMARY KEY
);

CREATE TABLE user_roles (
    user_id BIGINT NOT NULL,
    role_id BIGINT NOT NULL,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (role_id) REFERENCES roles(id)
);
```

##### Add metadata if needed

```sql
CREATE TABLE user_roles (
    id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    role_id BIGINT NOT NULL,
    assigned_by BIGINT,
    created_at TIMESTAMP NOT NULL,
    UNIQUE (user_id, role_id)
);
```

---

#### 5.3 MongoDB embedding vs referencing

##### Embed when

- Data is read together.
- Child belongs to parent.
- Data is small and bounded.
- Updates happen together.

Example:

```json
{
  "order_id": "123",
  "items": [
    {"sku": "A1", "quantity": 2},
    {"sku": "B2", "quantity": 1}
  ]
}
```

##### Reference when

- Data is large or unbounded.
- Data is shared.
- Data updates independently.
- Independent querying/indexing is needed.

---

#### 5.4 INNER JOIN vs LEFT JOIN

##### INNER JOIN

Returns only rows with matches in both tables.

```sql
SELECT *
FROM orders o
INNER JOIN customers c
ON o.customer_id = c.id;
```

##### LEFT JOIN

Returns all left table rows and nulls for missing right-side matches.

```sql
SELECT *
FROM orders o
LEFT JOIN customers c
ON o.customer_id = c.id;
```

##### Expected result if no right-side match

- `INNER JOIN`: row excluded.
- `LEFT JOIN`: row included with `NULL` right-side columns.

---

#### 5.5 Strong consistency vs eventual consistency

##### Strong consistency when

- Duplicate order creation is unacceptable.
- Money movement is involved.
- Inventory limits matter.
- Permissions/security decisions are involved.
- Stale data violates business rules.

##### Eventual consistency when

- Analytics counters.
- Notifications.
- Search indexes.
- Activity feeds.
- Reporting dashboards.

##### Signal

> If stale/conflicting data breaks an invariant or causes financial/security risk, use strong consistency. If the system can correct itself later and the user can tolerate delay, eventual consistency is acceptable.

---

#### 5.6 Preventing duplicate processing in eventual consistency

##### Techniques

- Idempotency key/event ID.
- Inbox pattern.
- Outbox pattern.
- Unique constraints.
- Idempotent state transitions.

##### Inbox pattern

```text
Consumer receives event → inserts event_id into inbox table → processes only if insert succeeds.
```

##### Outbox pattern

```text
Business update + outbox event written in same DB transaction → background publisher sends event.
```

##### Transaction handling

```text
Begin transaction
  Insert inbox event
  Apply business update
  Mark inbox event processed
Commit
```

If transaction fails, retry starts cleanly.

---

#### 5.7 Optimizing equality queries without an index

##### Techniques

- Check execution plan.
- Filter early.
- Avoid functions around filtered columns.
- Select only needed columns.
- Partition/cluster/sort data around common filters.
- Precompute smaller tables for frequent queries.

##### Example

```sql
EXPLAIN SELECT id, status, created_at
FROM orders
WHERE customer_id = 123;
```

##### DuckDB-specific note

Sorting or clustering data can help zone-map pruning skip row groups even without a traditional index.

---

### 3. SQL Interview Questions

#### 3.1 Successful Revenue by Region

##### Interview Question

> **“How do you calculate successful revenue by region?”**

```sql
SELECT
    region,
    SUM(amount) AS total_revenue,
    COUNT(*) AS successful_transactions
FROM transactions
WHERE status = 'SUCCESS'
GROUP BY region
ORDER BY total_revenue DESC;
```

##### Explanation

- `WHERE status = 'SUCCESS'` filters only successful transactions.
- `GROUP BY region` groups revenue by region.
- `SUM(amount)` calculates revenue.
- `COUNT(*)` counts successful transactions.

---

#### 3.2 Top One Transaction Per Customer

##### Interview Question

> **“For each customer, find the top one transaction.”**

If **top** means highest transaction amount:

```sql
SELECT
    transaction_id,
    customer_id,
    amount,
    transaction_date
FROM (
    SELECT
        transaction_id,
        customer_id,
        amount,
        transaction_date,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY amount DESC
        ) AS rn
    FROM transactions
) t
WHERE rn = 1;
```

##### Explanation

|          SQL Part          |                 Meaning                  |
| -------------------------- | ---------------------------------------- |
| `PARTITION BY customer_id` | Creates separate ranking per customer    |
| `ORDER BY amount DESC`     | Highest transaction comes first          |
| `ROW_NUMBER()`             | Assigns unique rank within each customer |
| `WHERE rn = 1`             | Selects top transaction per customer     |

##### Interview Answer

> “I would use `ROW_NUMBER()` as a window function. I partition by `customer_id`, order by amount descending, and select only rows where row number is 1. This gives exactly one top transaction per customer.”

---

#### 3.3 Top Transaction With Ties

##### Follow-Up Question

> **“What if two transactions have the same highest amount?”**

Use `RANK()` instead of `ROW_NUMBER()`:

```sql
SELECT
    transaction_id,
    customer_id,
    amount
FROM (
    SELECT
        transaction_id,
        customer_id,
        amount,
        RANK() OVER (
            PARTITION BY customer_id
            ORDER BY amount DESC
        ) AS rnk
    FROM transactions
) t
WHERE rnk = 1;
```

##### Difference

|    Function    |                    Behavior                     |
| -------------- | ----------------------------------------------- |
| `ROW_NUMBER()` | Returns exactly one row per customer            |
| `RANK()`       | Returns all tied top rows, but leaves rank gaps |
| `DENSE_RANK()` | Returns all tied top rows, no rank gaps         |

---

#### 3.4 Latest Transaction Per Customer

If **top** means most recent transaction:

```sql
SELECT
    transaction_id,
    customer_id,
    transaction_date,
    amount
FROM (
    SELECT
        transaction_id,
        customer_id,
        transaction_date,
        amount,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY transaction_date DESC
        ) AS rn
    FROM transactions
) t
WHERE rn = 1;
```

---

#### 3.5 Customers With More Than One Paid Transaction

##### Interview Question

> **“Find customers with more than one paid transaction only.”**

```sql
SELECT
    customer_id,
    COUNT(*) AS paid_transaction_count
FROM transactions
WHERE status = 'PAID'
GROUP BY customer_id
HAVING COUNT(*) > 1;
```

If the dataset uses `SUCCESS` instead of `PAID`:

```sql
SELECT
    customer_id,
    COUNT(*) AS successful_transaction_count
FROM transactions
WHERE status = 'SUCCESS'
GROUP BY customer_id
HAVING COUNT(*) > 1;
```

##### Why `HAVING`?

- `WHERE` filters rows before aggregation.
- `HAVING` filters grouped/aggregated results.

##### If They Want Full Transaction Details

```sql
SELECT *
FROM transactions
WHERE status = 'PAID'
  AND customer_id IN (
      SELECT customer_id
      FROM transactions
      WHERE status = 'PAID'
      GROUP BY customer_id
      HAVING COUNT(*) > 1
  );
```

##### Interview Answer

> “I would first filter paid transactions using `WHERE status = 'PAID'`, then group by customer and use `HAVING COUNT(*) > 1` because `HAVING` is used to filter aggregate results.”

---

### 6. Databases, ORMs & PostgreSQL

#### Likely Questions

- What is relational data modeling?
- How do you design tables for orders/customers/payments?
- What is normalization?
- What are indexes?
- What is a foreign key?
- How do you use SQLAlchemy or Django ORM?
- How do you avoid N+1 queries?
- How do transactions work?
- How do you handle migrations?
- How do you optimize slow queries?

---

#### Basic Relational Model Example

```sql
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    status VARCHAR(50) NOT NULL,
    total_amount NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    amount NUMERIC(10, 2) NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

##### Interview Explanation

- `customers` owns customer data.
- `orders` references customers.
- `payments` references orders.
- Foreign keys enforce data integrity.
- Separate tables reduce duplication and improve consistency.

---

#### SQLAlchemy Model Example

```python
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)

    orders = relationship("Order", back_populates="customer")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    status = Column(String, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)

    customer = relationship("Customer", back_populates="orders")
```

---

#### Avoiding N+1 Queries

##### Problem

If you load 100 orders and then separately query the customer for each order, you may execute 101 queries.

##### SQLAlchemy Fix

```python
from sqlalchemy.orm import joinedload

orders = (
    session.query(Order)
    .options(joinedload(Order.customer))
    .all()
)
```

##### Interview Explanation

Use eager loading when related data is needed upfront.

---

#### Index Example

```sql
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_status_created_at ON orders(status, created_at);
```

##### When to Add Indexes

Add indexes on:

- Foreign keys
- Frequently filtered columns
- Frequently sorted columns
- Columns used in joins

##### Tradeoff

Indexes speed up reads but slow down writes and take storage.

---

#### Transaction Example

```python
def create_order_with_payment(session, order_data, payment_data):
    try:
        order = Order(**order_data)
        session.add(order)
        session.flush()

        payment = Payment(order_id=order.id, **payment_data)
        session.add(payment)

        session.commit()
        return order

    except Exception:
        session.rollback()
        raise
```

##### Interview Explanation

Use transactions when multiple database changes must either all succeed or all fail.

---

## Relational Versus NoSQL Databases and ACID

### Relational Databases

Relational databases such as PostgreSQL and MySQL are a strong fit when the application needs structured relationships, transactions, joins, constraints, and strong consistency.

Typical strengths:

- Primary and foreign keys.
- Referential integrity.
- Transactions.
- Complex joins and reporting.
- Mature indexing and query optimization.

### NoSQL Databases

NoSQL is a broad category rather than one database model. Common forms include document stores, key-value stores, wide-column databases, and graph databases.

Use a NoSQL database when its access pattern or data model provides a concrete advantage, for example:

- Flexible document-shaped data.
- Extremely high-scale key-based access.
- Specialized graph relationships.
- Simple horizontally distributed lookups.

The choice should be based on access patterns, consistency needs, relationships, scale, and operational requirements rather than choosing SQL or NoSQL by default.

### ACID Transactions

|  Property   |                                                  Meaning                                                   |
| ----------- | ---------------------------------------------------------------------------------------------------------- |
| Atomicity   | All operations in a transaction succeed or all are rolled back.                                            |
| Consistency | A committed transaction preserves database rules and invariants.                                           |
| Isolation   | Concurrent transactions do not expose unsafe intermediate state to one another.                            |
| Durability  | Once committed, data survives process or machine failures according to the database durability guarantees. |

Example transfer:

```sql
BEGIN;

UPDATE accounts
SET balance = balance - 100
WHERE id = 1;

UPDATE accounts
SET balance = balance + 100
WHERE id = 2;

COMMIT;
```

If the second update cannot complete, the transaction should roll back rather than leaving only the debit applied.

### Database Ownership in Microservices

Prefer each service to own its persistence boundary. Other services should use an API, event, or replicated read model instead of directly querying another service's private tables. This reduces coupling but introduces eventual-consistency and distributed-workflow considerations.

**Interview answer:**

> I prefer a relational database when relationships, transactions, constraints, and reporting are central to the workload. I consider NoSQL when a document, key-value, graph, or horizontally distributed access pattern fits better. In microservices I also try to keep clear data ownership so one service does not depend directly on another service's internal schema.

---

## Backend Persistence & Concurrency Interview Patterns

### One Database Session / Transaction Boundary per Request

For typical request/response APIs, use one scoped database session/transaction context per request rather than one global mutable session shared across concurrent requests.

Conceptual flow:

```text
request
  ↓
open/request DB session
  ↓
read + validate
  ↓
perform atomic writes
  ↓
commit
  ↓
close session
```

On failure:

```text
exception
  ↓
rollback
  ↓
return mapped error
```

Long-running external work should generally not hold a database transaction open for the entire network call or user interaction.

---

### Constraints Are Part of Correctness

Application checks improve error messages but do not replace database constraints under concurrency.

Example subscription uniqueness:

```sql
CREATE UNIQUE INDEX uq_subscription_user_podcast
ON subscription(user_id, podcast_id);
```

Even if two concurrent API requests both execute:

```text
SELECT → no existing subscription
```

only one should be allowed to create the unique pair.

Useful constraints:

- Primary keys
- Unique keys
- Foreign keys
- `NOT NULL`
- Check constraints

Strong interview line:

> I use application validation for usability and domain rules, but I keep invariants that must survive concurrency enforced at the authoritative database boundary as well.

---

### Composite Indexes from Access Patterns

Example feed query:

```sql
SELECT *
FROM episode
WHERE podcast_id = :podcast_id
ORDER BY published_at DESC, episode_id DESC
LIMIT 50;
```

Useful index:

```sql
CREATE INDEX idx_episode_podcast_published
ON episode(podcast_id, published_at DESC, episode_id DESC);
```

Why column order matters:

The leading columns should match the high-value filtering/order pattern. A composite index is not equivalent to having independent single-column indexes for every query.

Trade-off:

- Faster qualifying reads
- More storage
- More write/update maintenance

---

### Optimistic Concurrency with a Version Column

Schema:

```text
id
state
version
```

Conditional update:

```sql
UPDATE job
SET state = 'RUNNING',
    version = version + 1
WHERE id = :job_id
  AND state = 'QUEUED'
  AND version = :expected_version;
```

Result:

```text
1 row updated → caller won
0 rows updated → state/version changed; handle conflict
```

This is useful when conflicts are possible but not common enough to justify holding pessimistic locks across normal reads.

---

### Conditional Allocation for Scarce Resources

Do not implement scarce-resource ownership as:

```text
SELECT available
then later UPDATE
```

without a concurrency guard.

Prefer one authoritative conditional write or a short transaction/lock:

```sql
UPDATE seat
SET status = 'HELD', held_by = :user_id
WHERE seat_id = :seat_id
  AND status = 'AVAILABLE';
```

Affected-row count becomes the concurrency result.

This same pattern applies to:

- Inventory
- Driver assignment
- Job leasing
- Quota claims
- One-time tokens

---

### Idempotent Ingestion with Source IDs

When a scraper/partner can retry the same logical event, store a stable source identity:

```text
(podcast_id, source_episode_id)
```

and enforce uniqueness:

```sql
UNIQUE(podcast_id, source_episode_id)
```

A retry can then safely return/reuse the existing record rather than creating a duplicate.

The same principle applies to payment-provider event IDs, webhook IDs, and external order IDs.

---

### Transactional Outbox Schema

Example tables:

```text
business_table
--------------
id
state
...

outbox
------
event_id
aggregate_type
aggregate_id
event_type
payload
created_at
published_at nullable
```

Write in one DB transaction:

```sql
BEGIN;

INSERT/UPDATE business_table ...;
INSERT INTO outbox(...);

COMMIT;
```

A separate publisher reads unpublished outbox rows and sends them to the broker. Marking an event published must tolerate retries, and downstream consumers should be idempotent.

---

### Read Replicas and Read-After-Write

In a single-primary topology:

```text
writes → primary
eligible reads → replicas
```

Asynchronous replication can produce:

```text
write committed on primary
   ↓
immediate read on replica
   ↓
old value
```

For workflows requiring read-after-write consistency:

- Read from primary for a short session/window.
- Route based on a replication position/token where supported.
- Keep critical ownership/permission checks on the authoritative path.

Do not assume every query needs strong consistency; define it per workflow.

---

### SQL vs NoSQL Interview Decision

Ask:

```text
What are the relationships?
What transactions/constraints are required?
What are the dominant access patterns?
How stable is the schema?
What write/read scale is expected?
What consistency is required?
```

Relational databases are often strong for:

- Orders/payments
- Subscriptions
- User-resource ownership
- Workflow state
- Control-plane metadata

Specialized NoSQL stores can be strong for:

- Very high-scale simple key access
- Flexible documents
- Time-series/telemetry
- Geo/index-oriented access

A production architecture may use both, but every store adds operational and consistency complexity.

---

### Database Interview Quick Questions

#### Why PostgreSQL for a subscription/feed control plane?

Because users, subscriptions, podcasts, and episodes have clear relationships, uniqueness constraints, and transactional invariants. Read-heavy scale can first be addressed with indexes, caching, and replicas before assuming a different database model is necessary.

#### Why not cache the final allocation decision?

Caches can be stale and usually do not provide the same transactional invariant as the authoritative database. Use cache for discovery/read acceleration; use authoritative conditional state for ownership.

#### What is an N+1 query problem?

One parent query triggers one additional query per returned record, for example one query for 100 users plus 100 separate queries for each user's data. Fix with eager loading, batching, joins, or a deliberately designed aggregate query/read model depending on ownership boundaries.

#### What does a connection pool solve?

It reuses a bounded set of database connections instead of creating a new physical connection for every request. Pool size must respect database capacity; scaling app instances without adjusting aggregate connection demand can exhaust the database.

#### How do you debug a slow query?

- Identify the exact SQL and frequency.
- Examine execution plan (`EXPLAIN`/`EXPLAIN ANALYZE`).
- Check scans, join strategy, row estimates, sorts, lock waits.
- Verify indexes match predicates/order.
- Reduce unnecessary selected data.
- Check N+1 and repeated queries.
- Measure before/after rather than adding indexes blindly.

---

## Quick Persistence Revision Card

```text
Session/transaction scoped to request
Rollback on failure
DB constraints enforce concurrency invariants
Composite index follows access pattern
Optimistic version/conditional UPDATE
Unique source IDs for idempotent ingestion
Transactional outbox
Single-primary replicas + lag/read-after-write
Connection-pool capacity
SQL vs NoSQL from relationships/invariants/access patterns
```
