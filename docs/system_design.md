# System Design, Microservices & Distributed Systems

> **Purpose:** Scalability, microservices, distributed architecture, service communication, queues, caching, feature flags, and production trade-offs.
> **Use this file for:** system design interviews and senior backend engineering rounds

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

- Horizontal vs vertical scaling
- Load balancing and caching
- Database replication and sharding
- Message queues and async processing
- Microservices and database-per-service
- Feature flags and safe rollouts
- Reliability, observability, and incident response
- URL shortener, chat system, rate limiter, and other design patterns

---

## Consolidated Interview Questions & Technical Notes

The section below is merged from the previously organized topic-wise interview-prep pack so the repository keeps the detailed technical Q&A in one place.

> Microservices, distributed architecture, service communication, queues, Celery, Redis, RabbitMQ, feature flags, architecture trade-offs, and domain system design.
> Consolidated from the uploaded Markdown interview-prep files and reorganized by reusable topic. Source labels are retained for traceability.

### Topic Sections

1. Backend and Microservices Architecture — `interview_questions_topics_technical_prep.md`
2. Caching, Rate Limiting, Abuse Prevention, and Feature Flags — `interview_questions_topics_technical_prep.md`
3. Distributed Systems: Celery, Redis, RabbitMQ — `Interview_Topics_and_Technical_Prep.md`
4. Code Reviews & Architecture Discussions — `Interview_Topics_and_Technical_Prep.md`
5. E-Commerce / Logistics / Fintech Domain Topics — `Interview_Topics_and_Technical_Prep.md`

---

### 2. Backend and Microservices Architecture

> Source: `interview_questions_topics_technical_prep.md`

#### 2.1 Pros and cons of microservices

##### Pros

- Independent deployment.
- Independent scaling.
- Clear service ownership.
- Technology flexibility.
- Fault isolation when designed well.

##### Cons

- Distributed system complexity.
- More network latency.
- Harder debugging and tracing.
- Data consistency challenges.
- Deployment and observability overhead.

##### Interview wording

> Microservices help with scale and independent ownership, but the trade-off is operational complexity. You need strong observability, API contracts, CI/CD, and clear ownership to make them work well.

---

#### 2.2 Database ownership in microservices

##### Topic covered

How services handle data when one service needs user information while another owns transactions.

##### Best practice

Each service should own its database. Other services should access data through APIs/events/read models rather than directly joining across databases.

##### Patterns

- Service API call for real-time lookup.
- Cached read model.
- Event-driven replication.
- API composition/BFF layer.
- Avoid shared database coupling.

##### Example

```text
Transaction Service → needs user risk tier
User Service → owns user profile
Solution → Transaction Service calls User Service API or reads a replicated user summary table.
```

---

#### 2.3 Service communication patterns

##### Synchronous communication

Use when immediate response is required.

Examples:

- Authorization check.
- Payment validation.
- User lookup needed immediately.

##### Asynchronous communication

Use when work can happen later.

Examples:

- Notifications.
- Analytics.
- Audit events.
- Email dispatch.

##### Interview wording

> I keep critical request-path operations synchronous and move non-critical operations async to reduce latency and improve resilience.

---

#### 2.4 API Gateway and BFF/API composition

##### Question covered

How to expose one public API without coupling clients to each microservice.

##### Recommended design

```text
Client → API Gateway → BFF/API Composition Layer → Internal Microservices
```

##### API Gateway handles

- Authentication.
- TLS termination.
- Rate limiting.
- Routing.
- Request limits.
- Basic observability.

##### BFF/composition layer handles

- Aggregating multiple service calls.
- Shaping responses for web/mobile/partners.
- Hiding internal service boundaries.

##### Interview wording

> I use API Gateway for edge concerns and a BFF/composition layer for orchestration. That keeps clients decoupled from internal microservice changes.

---

### 6. Caching, Rate Limiting, Abuse Prevention, and Feature Flags

> Source: `interview_questions_topics_technical_prep.md`

#### 6.1 Cache consistency when target URL changes

##### Approach

- Treat DB as source of truth.
- Update DB first.
- Invalidate or update cache immediately after commit.
- Use versioned cache keys or short TTLs for safety.

##### Example

```text
Update destination URL in DB → delete Redis key short_code:abc → next redirect reloads fresh value.
```

---

#### 6.2 Preventing cache stampede

##### Techniques

- Distributed lock using Redis `SETNX`.
- Stale-while-revalidate.
- Jittered TTL.
- Request coalescing.

##### Interview wording

> Only one request should rebuild the cache; others should wait briefly or serve stale data rather than all hitting the database.

---

#### 6.3 Graceful degradation if cache is unavailable

##### Design

- Cache is optimization, not source of truth.
- Short cache timeout.
- Fallback to DB.
- Circuit breaker for cache failures.
- Protect DB with backpressure/rate limiting.
- Local in-memory LRU cache for very hot keys.

---

#### 6.4 Rate limiting URL/order creation endpoints

##### Best approach

Use Redis-backed distributed rate limiting at gateway/middleware.

##### Dimensions

- Per IP.
- Per user.
- Per API key.
- Per tenant/org.

##### Algorithms

- Token bucket.
- Sliding window.

##### Response

```http
429 Too Many Requests
Retry-After: 60
```

---

#### 6.5 Protecting against automated abuse beyond rate limits

##### Techniques

- API keys/authentication.
- Bot detection.
- CAPTCHA/challenge for suspicious traffic.
- URL reputation checks.
- Malware/phishing domain scanning.
- Behavior-based anomaly detection.
- Progressive enforcement.
- Async moderation pipeline.

---

#### 6.6 Feature flag system for safe releases

##### Design principles

- Separate deployment from release.
- Centralized flag config.
- Local in-memory evaluation.
- Background refresh.
- Percentage rollout.
- Tenant/user/region targeting.
- Sticky assignment using hashing.
- Audit all changes.
- Safe default if flag service fails.

##### Example rollout

```text
internal users → 1% → 5% → 25% → 50% → 100%
```

---

#### 6.7 Fast and reliable runtime flag checks

##### Best practice

Evaluate flags locally from memory, not by calling the flag service on every request.

##### Why

- Lower latency.
- Higher reliability.
- No network dependency in hot path.

---

### 7. Distributed Systems: Celery, Redis, RabbitMQ

> Source: `Interview_Topics_and_Technical_Prep.md`

#### Likely Questions

- What are background jobs?
- Why use Celery?
- What is Redis used for?
- What is RabbitMQ used for?
- How do you handle retries?
- How do you avoid duplicate job execution?
- How do you design async processing for slow tasks?
- What happens if a worker crashes?
- How do you monitor background jobs?

---

#### Why Use Background Jobs?

Use background jobs for work that should not block the API response:

- Sending emails
- Generating reports
- Syncing with third-party APIs
- Processing uploads
- Running scheduled tasks
- Retrying failed integrations

---

#### Celery Example

```python
from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
)


@celery_app.task(bind=True, max_retries=3)
def sync_order_to_partner(self, order_id: int):
    try:
        response = external_partner_api.sync_order(order_id)
        return response

    except TemporaryAPIError as exc:
        raise self.retry(exc=exc, countdown=60)
```

##### Interview Explanation

This shows:

- Redis as broker/backend
- Async background execution
- Retry handling
- Protection from temporary external API failures

---

#### Redis Use Cases

Redis can be used for:

- Caching
- Rate limiting
- Distributed locks
- Session storage
- Celery broker
- Temporary counters
- Idempotency keys

---

#### Redis Cache Example

```python
import json
import redis

cache = redis.Redis(host="localhost", port=6379, decode_responses=True)


def get_customer_profile(customer_id: int):
    key = f"customer:{customer_id}"

    cached = cache.get(key)
    if cached:
        return json.loads(cached)

    profile = database.fetch_customer(customer_id)
    cache.setex(key, 300, json.dumps(profile))

    return profile
```

---

#### Distributed Lock Example

```python
def process_order(order_id: int):
    lock_key = f"lock:order:{order_id}"

    lock_acquired = cache.set(lock_key, "1", nx=True, ex=60)

    if not lock_acquired:
        return "Order is already being processed"

    try:
        # process order safely
        return "processed"
    finally:
        cache.delete(lock_key)
```

##### Interview Explanation

Distributed locks prevent multiple workers from processing the same item at the same time.

---

### 16. Code Reviews & Architecture Discussions

> Source: `Interview_Topics_and_Technical_Prep.md`

#### Likely Questions

- How do you approach code reviews?
- How do you give feedback?
- How do you receive feedback?
- How do you make architecture tradeoffs?
- How do you handle disagreement?
- How do you improve legacy code safely?

---

#### Code Review Checklist

Check for:

- Correctness
- Readability
- Simplicity
- Tests
- Error handling
- Security
- Performance
- Database impact
- Backward compatibility
- Observability
- Maintainability

---

#### Good Code Review Comment Example

```text
This works, but I wonder if we should move this validation closer to the service layer. 
That would keep the API handler thinner and make the rule easier to reuse from background jobs.
```

##### Why This Is Good

- Specific
- Respectful
- Explains reasoning
- Suggests improvement
- Does not attack the person

---

#### Refactoring Legacy Code Safely

Good strategy:

1. Add tests around current behavior
2. Identify risky areas
3. Refactor in small steps
4. Keep external behavior stable
5. Use feature flags if needed
6. Monitor after release

---

### 17. E-Commerce / Logistics / Fintech Domain Topics

> Source: `Interview_Topics_and_Technical_Prep.md`

These are general domain concepts that may come up in product engineering interviews for commerce, logistics, payments, or ERP-style platforms.

#### Likely Questions

- How would you design an order management workflow?
- How do you handle inventory updates?
- How do you prevent duplicate payments?
- How do you handle third-party shipping integrations?
- How do you reconcile financial transactions?
- How do you handle webhook retries?
- How do you design for eventual consistency?

---

#### Order Lifecycle Example

```text
created
   ↓
paid
   ↓
confirmed
   ↓
packed
   ↓
shipped
   ↓
delivered
```

Possible exception states:

```text
cancelled
refunded
payment_failed
shipment_failed
returned
```

---

#### Webhook Handling Example

```python
@app.post("/webhooks/shipping")
def handle_shipping_webhook(payload: dict, idempotency_key: str):
    if webhook_already_processed(idempotency_key):
        return {"status": "already_processed"}

    validate_signature(payload)
    save_webhook_event(payload, idempotency_key)
    process_shipping_update.delay(payload)

    return {"status": "accepted"}
```

##### Interview Explanation

Webhook handlers should:

- Validate signatures
- Be idempotent
- Respond quickly
- Process heavy work asynchronously
- Store raw event for audit/debugging
- Retry safely

---

#### Inventory Race Condition Example

##### Problem

Two users buy the last item at the same time.

##### Solution Ideas

- Database row locking
- Atomic update
- Reservation system
- Idempotent order processing

```sql
UPDATE inventory
SET quantity = quantity - 1
WHERE sku = 'ABC123'
  AND quantity > 0;
```

Then check affected rows. If zero rows were updated, inventory was unavailable.

---

#### Payment Idempotency

Payment systems should prevent duplicate charges when clients retry.

```text
Client sends payment request with idempotency key
   ↓
Server checks if key already exists
   ↓
If yes, return previous result
   ↓
If no, process payment and store result
```

---
