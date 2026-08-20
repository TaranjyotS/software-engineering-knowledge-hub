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

> Microservices, distributed architecture, service communication, queues, Celery, Redis, RabbitMQ, feature flags, architecture trade-offs, and domain system design.

---

### 1. Backend and Microservices Architecture

#### 1.1 Pros and cons of microservices

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

#### 1.2 Database ownership in microservices

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

#### 1.3 Service communication patterns

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

#### 1.4 API Gateway and BFF/API composition

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

### 2. Caching, Rate Limiting, Abuse Prevention, and Feature Flags

#### 2.1 Cache consistency when target URL changes

##### Approach

- Treat DB as source of truth.
- Update DB first.
- Invalidate or update cache immediately after commit.
- Use versioned cache keys or short TTLs for safety.

##### Example

```text
Update destination URL in DB → delete Redis key short_code:abc → next redirect reloads fresh value.
```

#### 2.2 Rate limiting URL/order creation endpoints

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

#### 2.3 Protecting against automated abuse beyond rate limits

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

#### 2.4 Feature flag system for safe releases

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

#### 2.5 Fast and reliable runtime flag checks

##### Best practice

Evaluate flags locally from memory, not by calling the flag service on every request.

##### Why

- Lower latency.
- Higher reliability.
- No network dependency in hot path.

---

### 3. Distributed Systems: Celery, Redis, RabbitMQ

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

### 4. Code Reviews & Architecture Discussions

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

### 5. E-Commerce / Logistics / Fintech Domain Topics

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

## AI-Enabled Backend Versus Agentic Architecture

AI integration does not automatically make a product agentic. The distinction affects architecture, testing, cost, and operational risk.

|   Architecture    |                   Control Flow                    |               Typical Use Case               |
| ----------------- | ------------------------------------------------- | -------------------------------------------- |
| AI-enabled        | Application code chooses when and how to call AI  | Summarization, extraction, classification    |
| Workflow-based AI | Predetermined sequence of model and service steps | RAG, document processing, content generation |
| Agentic AI        | Model dynamically chooses actions or tools        | Multi-step investigation and task completion |

### AI-Enabled Product Flow

```text
API request
  -> deterministic validation
  -> domain service
  -> optional model call
  -> output validation
  -> persistence
  -> API response
```

The application remains responsible for control flow. The model provides a bounded capability inside a normal backend system.

### Agentic Product Flow

```text
User goal
  -> planner/model
  -> select tool
  -> execute tool
  -> observe result
  -> repeat or finish
```

This requires stronger controls around tool permissions, iteration limits, state, audit trails, and recovery from partial execution.

### Design Principle: Preserve a Stable Backend Core

Keep domain rules independent of the model:

```text
Routes -> Application Services -> Domain Rules
                              -> Model Adapter
                              -> Repositories
                              -> External Services
```

Benefits:

- Model vendors can be replaced without rewriting routes.
- Deterministic business rules remain testable without an LLM.
- Model failures can use fallback or degraded behavior.
- Cost, latency, and token usage can be measured at one boundary.
- AI can be added gradually rather than redesigning the whole platform.

### Backend Engineering Skills That Transfer Across AI Systems

The domain may change, but the production concerns remain familiar:

- API contracts and backward compatibility.
- Authentication, authorization, and data protection.
- Database consistency and idempotency.
- Retries, timeouts, queues, and failure isolation.
- Horizontal scaling and stateless service design.
- Structured logs, metrics, traces, and alerts.
- Deployment safety and rollback.

The added AI concerns are model quality, prompt/version management, retrieval quality, nondeterminism, token cost, and hallucination risk.

### Architecture Tradeoff Answer

> I would start with an AI-enabled deterministic workflow unless the use case genuinely requires dynamic planning. It is easier to test, operate, secure, and explain. I would introduce agentic behavior only where flexible tool selection creates measurable value, and I would bound it with explicit permissions, step limits, validation, and audit logging.

---

## Monolith Versus Microservices: Decision Framework

A monolith packages most business capabilities into one deployable application. Microservices split capabilities into smaller services that can be deployed and scaled independently. Neither is automatically better; the right choice depends on team size, domain boundaries, scaling needs, and operational maturity.

|     Area      |    Monolith / Modular Monolith     |                   Microservices                   |
| ------------- | ---------------------------------- | ------------------------------------------------- |
| Deployment    | One deployable unit                | Independent service deployments                   |
| Scaling       | Scale the whole application        | Scale only the constrained service                |
| Communication | In-process calls                   | Network calls, events, or messaging               |
| Data          | Often one database/schema          | Prefer service-owned data                         |
| Debugging     | Easier local tracing               | Distributed tracing is important                  |
| Failure model | Larger shared blast radius         | Better isolation when designed well               |
| Team overhead | Lower                              | Higher operational and ownership overhead         |
| Best fit      | Small/medium team, evolving domain | Clear boundaries, independent scale/release needs |

### When to Start With a Modular Monolith

Prefer a modular monolith when:

- The product or domain is still changing rapidly.
- One team owns most of the application.
- Independent scaling is not yet necessary.
- Operational simplicity is more valuable than deployment independence.
- Clear internal modules can preserve boundaries without network calls.

### When Microservices Become Justified

Microservices become more attractive when:

- Different capabilities have materially different scaling requirements.
- Multiple teams need independent ownership and release cycles.
- A failure in one capability should be isolated from the rest.
- The domain has stable service boundaries.
- The organization can support service discovery, observability, CI/CD, and distributed failure handling.

**Interview answer:**

> I would not choose microservices by default. A modular monolith is often the better starting point because it is simpler to build, test, deploy, and debug. I would introduce microservices when there are clear business boundaries, independent scaling or release requirements, or multiple teams that need separate ownership. The benefit is deployment and scaling flexibility, but the trade-off is distributed-system complexity around networking, data consistency, observability, and operations.

---

## Async I/O Versus Background Processing

`async`/`await` and background processing solve different problems.

### Async I/O Inside a Request

Use `async`/`await` when the request still needs the result, but the work spends time waiting on I/O such as:

- External APIs.
- Databases.
- LLM providers.
- Vector databases.
- Object storage.

```text
Request
  -> async API handler
  -> await external service
  -> event loop handles other requests while waiting
  -> return response
```

This improves concurrency, but the original HTTP request is still open.

### Background Processing Outside the Request

Use a queue and worker when the work is long-running, retryable, or does not need to finish before the HTTP response.

```text
Client
  -> POST /reports
  -> API creates job and returns 202 + job_id
  -> queue
  -> background worker
  -> result store / database
  -> client polls or receives notification
```

Typical use cases:

- Large document processing.
- Embedding generation.
- Email and notification delivery.
- Report generation.
- Batch data processing.
- Long-running AI workflows.

### Production Concerns for Background Jobs

- Idempotency so retries do not duplicate side effects.
- Bounded retries with exponential backoff.
- Dead-letter queue for repeatedly failing jobs.
- Explicit states such as `queued`, `running`, `completed`, and `failed`.
- Timeouts and cancellation.
- Queue-depth and worker-latency monitoring.
- Handling at-least-once delivery and possible duplicate messages.

**Interview answer:**

> Async I/O helps a service handle many concurrent I/O-bound requests while each request remains active. Background processing moves work out of the request-response cycle entirely. For a quick database or LLM call I may use async/await; for a multi-minute report, ingestion pipeline, or retryable workflow I would return `202 Accepted`, enqueue a job, and process it with a worker.

---

## Capacity Planning, Load Testing & Scaling Under Unexpected Demand

Capacity planning should model the work the system performs, not only the number of requests entering the API. One customer action may fan out into several service calls, database queries, cache lookups, or background jobs, so top-level request count can underestimate the effective workload.

### Build the Capacity Model from the End-to-End Request Path

Start with business demand and translate it into technical load:

```text
expected users / transactions
        ↓
peak concurrency and requests per second
        ↓
request fan-out and downstream operations
        ↓
CPU, memory, DB connections, I/O, queue work
        ↓
required capacity + growth/failure headroom
```

Important inputs include:

- Sustained peak traffic, not only daily averages.
- Burstiness and concurrency.
- Per-request CPU and memory cost.
- Database operations and connection usage.
- Calls to downstream services.
- Retry amplification during partial failures.
- Background work generated by foreground requests.
- Expected growth.
- Capacity needed when an instance or availability zone is unavailable.

### Detecting an Underestimated Workload

A production-like load test should increase traffic progressively and compare incoming traffic with internal resource consumption.

Monitor:

- Throughput/RPS.
- p50, p95, and p99 latency.
- Error and timeout rates.
- CPU and memory saturation.
- Pod/instance count and autoscaling events.
- Database query latency and connection-pool usage.
- Queue depth and worker lag.
- Downstream call volume and latency.
- Cache hit ratio.

If effective work grows much faster than incoming RPS, trace representative requests to identify request amplification, fan-out, retries, or unexpectedly expensive data access.

**Interview answer:**

> I would start from expected peak business volume and convert it into concurrency, RPS, database work, and downstream calls. Then I would validate those assumptions with progressive load tests. If the system consumes roughly twice the expected resources, I would compare top-level traffic with traces and downstream operation counts to find amplification, update the model, and retest with growth and failure headroom.

### Customer Experience Is Part of the Capacity Test

A system can remain technically "up" while the user experience has already failed. Track the important customer journey, not just aggregate infrastructure health.

For a transactional workflow, measure stage-level latency and success rate for operations such as:

- Loading data required to begin the workflow.
- Availability or eligibility lookup.
- Validation.
- Transaction submission.
- Confirmation.

A common degradation pattern is:

```text
healthy latency
   ↓
increasing concurrency
   ↓
p95/p99 latency rises
   ↓
timeouts and retries appear
   ↓
retries add more load
   ↓
error rate or outage
```

### Vertical vs Horizontal Scaling

|            Strategy            |                         Best Use                          |                               Trade-Off                               |
| ------------------------------ | --------------------------------------------------------- | --------------------------------------------------------------------- |
| Vertical scaling / scale up    | Immediate headroom, stateful systems, short-term recovery | Has hardware limits, larger failure unit, can be costly               |
| Horizontal scaling / scale out | Stateless services and sustained growth                   | Requires load balancing, distributed coordination, good observability |

A practical incident may use both: scale vertically first to restore headroom, then move to a sustainable horizontally scaled design.

### Horizontal Scaling Requires Stateless Services

Horizontal scaling works best when any healthy instance can handle any request. Keep shared state in external systems such as databases, Redis, object storage, or durable queues rather than process memory.

Typical architecture:

```text
Clients
   ↓
Load Balancer
   ↓
Stateless API replicas  ←→  Redis/cache
   ↓
Database / downstream services
```

Autoscaling should trigger before the service reaches saturation. Useful signals can include CPU, memory, request count, queue depth, and latency, depending on the workload.

### Add Caching Selectively

Caching reduces repeated expensive reads, but correctness determines what may be cached.

Good candidates:

- Reference/configuration data.
- Product/catalog-style reads.
- Expensive query results with acceptable staleness.
- Read-heavy external lookups.

Use short TTLs or explicit invalidation where appropriate. Avoid treating the cache as the source of truth for rapidly changing or transaction-critical state unless the consistency model explicitly supports it.

### Do Not Move the Bottleneck Downstream

Adding application replicas can overload the database or another dependency. Before scaling the application aggressively, inspect:

- Query plans and indexes.
- Slow or repeated queries.
- Database CPU/I/O.
- Connection-pool limits.
- Per-instance connection counts.
- Lock contention.
- Dependency rate limits.
- Retry behavior.

Useful protections include connection pooling/proxies, per-instance limits, backpressure, read replicas for suitable workloads, asynchronous handling of non-critical work, and graceful degradation.

### Choosing the Ideal Long-Term Scaling Strategy

A sound decision sequence is:

1. Measure the actual bottleneck before adding capacity.
2. Use a low-risk short-term mitigation if customers are actively affected.
3. Optimize clearly inefficient work.
4. Keep the application stateless where practical.
5. Prefer horizontal scaling for sustained application-tier growth.
6. Add caching only where staleness is acceptable.
7. Protect databases and downstream dependencies from amplified load.
8. Plan for peak demand plus growth and failure headroom.
9. Retest at expected peak and beyond it.
10. Confirm graceful degradation and recovery, not just maximum throughput.

**Interview answer:**

> My preferred long-term approach is not simply to add CPU. I would identify the actual bottleneck, keep the application stateless, scale the application tier horizontally behind a load balancer, use selective caching for safe read-heavy data, optimize the database and connection pools, and plan enough headroom to survive both peak traffic and a component failure. I would validate the design with progressive load tests and p95/p99 latency, throughput, errors, saturation, database connections, and cache effectiveness.

---

## Design Sequencing, Storage Fit & Messaging Resilience

Several system-design questions become easier when the answer is framed around **what stage of design we are in** and **what access pattern the workload actually needs**.

### What Does System Overload Mean?

A system is overloaded when incoming work exceeds the sustainable capacity of one or more resources: application CPU/memory, worker slots, database connections, queue consumers, cache capacity, or a downstream dependency.

```text
incoming load
    ↓
API tier
    ↓
DB / queue / downstream service

if arrival rate > sustainable service rate
→ queues grow
→ latency rises
→ timeouts/retries amplify load
→ failures cascade
```

A senior response should not be only "add more servers." First identify the bottleneck and protect dependencies.

Useful overload controls:

- Horizontal scaling of stateless application instances.
- Admission control/rate limiting.
- Backpressure and bounded queues.
- Caching where staleness is acceptable.
- Async queues for non-critical/offline work.
- Timeouts and bounded retries with jitter.
- Circuit breaking/fallbacks for unhealthy dependencies.
- Database connection limits, indexing, query optimization, and read scaling where valid.
- Graceful degradation instead of total failure.

Interview answer:

> I would first determine which resource is saturated rather than assuming the API tier is the bottleneck. Then I would scale the correct tier and add protection such as rate limiting, backpressure, bounded queues, timeouts, and graceful degradation so overload does not propagate into the database or downstream services.

### Sequence Architecture Work by Project Stage

Do not treat every engineering activity as equally urgent on day one.

For a new system whose requirements are still being established:

1. Clarify customer/business requirements and non-functional constraints.
2. Define core use cases and failure cases.
3. Sketch the high-level architecture and critical data flow.
4. Identify the highest-risk assumptions.
5. Build a focused proof of concept only for uncertain/high-risk constructs.
6. Review the proposed architecture with senior engineers and affected teams.
7. Finalize detailed schemas/contracts and implementation plan.
8. Add production dashboards, alarms, runbooks, and operational documentation before launch.

Operational readiness is essential before production, but creating dashboards before the workload, architecture, and service boundaries are understood is usually premature.

**Interview answer:**

> I start by clarifying the problem and non-functional requirements, then sketch the end-to-end architecture and identify the riskiest assumptions. I use a proof of concept to validate those risks rather than building arbitrary production code early. Once the design is coherent, I review it with the relevant engineers, then complete implementation and operational readiness including metrics, alarms, runbooks, and load testing.

### Choosing a Data Store by Access Pattern

Consider a short, extremely bursty write window where millions of clients submit and may update a value, and the service must remain available while totals are refreshed frequently.

|         Technology          |                              Fit                               |                                  Why                                  |
| --------------------------- | -------------------------------------------------------------- | --------------------------------------------------------------------- |
| Distributed key-value store | Very strong                                                    | Direct keyed reads/writes, horizontal scale, predictable access path  |
| Document database           | Strong when each record has evolving document-shaped metadata  | Flexible schema but more capability than a simple key lookup may need |
| Relational database         | Viable with careful partitioning/scaling                       | Strong constraints/transactions, but burst pattern must be designed   |
| Ledger database             | Useful for audit history, not necessarily the primary hot path | Append-only traceability is different from low-latency mutable access |
| Graph database              | Poor fit for simple vote/state lookup                          | Relationship traversal is not the main access pattern                 |
| Batch/distributed processor | Analytics/aggregation layer, not transactional source of truth | Processing engine rather than primary request-time storage            |

A common key design is one record per user/entity combination so an update replaces the previous value idempotently rather than creating duplicate votes/actions.

### Images and Thumbnails

Binary images should normally live in object/cloud file storage, not inside the primary relational or search database.

```text
client
  ↓
CDN / object storage URL
  ↓
thumbnail object

metadata DB
  └─ object key, dimensions, owner, checksum, content type
```

Why object storage is the default:

- Cheap durable blob storage.
- Horizontal scale.
- CDN integration.
- Lifecycle/retention policies.
- Avoids bloating transactional database pages and backups.

A local filesystem may be acceptable for a prototype or single-host tool, but it is a weak SaaS production choice because instances are replaceable and storage is not naturally shared. Elasticsearch is for search/indexing, not primary binary storage.

### High Availability: What Actually Prevents Outage

Availability mechanisms should reduce dependency on manual intervention and remove single-instance capacity limits.

High-value actions include:

- Run multiple stateless instances across failure domains.
- Support horizontal scaling/autoscaling as demand changes.
- Load test expected peak and failure scenarios before launch.
- Use health checks and automatic replacement/failover.
- Externalize regional/environment configuration so instances are replaceable and consistent.
- Add dependency timeouts, backpressure, and bounded retries.

Important distinction:

> Backups improve recoverability and durability. They are important, but a daily backup does not by itself keep the live service available when an instance or database endpoint fails.

Similarly, debug-level logging can help diagnosis but does not make the service highly available and can increase cost/noise if enabled globally in production.

### Designing a Versioned Message Envelope

For queued messages produced by heterogeneous devices or services, define a stable envelope before optimizing individual payloads.

Useful envelope fields include:

```text
message_id
message_type / purpose
schema_version
producer_id
created_at / event_timestamp
correlation_id or trace_id
content_type / encoding
payload or payload_reference
checksum
```

Priorities during design:

1. List the distinct purposes/messages that must be represented.
2. Research/adopt an established serialization/message format where it fits rather than inventing one unnecessarily.
3. Define versioning and backward/forward compatibility rules.
4. Define binary serialization for component payloads where size/latency matters.
5. Define timestamps, checksums, identifiers, and validation rules.
6. Understand queue size limits, delivery semantics, retry behavior, and poison-message handling.
7. Add dashboards after the contract and processing path are clear.

### Large Payloads: Keep the Queue Small

Message brokers are optimized for messages, not arbitrary large blobs. A strong default is:

```text
producer
  ↓
write large payload to object storage
  ↓
queue small message containing metadata + object reference + checksum
  ↓
consumer downloads payload
```

This separates transport metadata from large binary data and avoids broker size limits.

Alternative approaches have trade-offs:

|          Approach           |          When It Helps          |                                 Trade-Off                                  |
| --------------------------- | ------------------------------- | -------------------------------------------------------------------------- |
| Fragment into many messages | Broker-only environments        | Requires ordering, completeness detection, retry/reassembly, deduplication |
| Streaming protocol          | Continuous/very large transfer  | More protocol/session complexity and backpressure handling                 |
| Send during low-volume time | Non-urgent bandwidth-heavy work | Does not solve hard broker message-size limits and adds scheduling latency |
| Physical/manual transfer    | Exceptional offline migration   | Not a scalable online service design                                       |

### Queue Resilience After Dropped Messages

For an at-least-once queueing system, resilience comes from preserving failed work and making retries safe.

High-value controls:

- Review retry count, backoff, and visibility timeout/lease configuration.
- Add a dead-letter queue for messages that repeatedly fail.
- Alert on DLQ depth, age of oldest message, retry rate, and consumer lag.
- Retain source messages long enough to survive downstream outages and permit replay.
- Make consumers idempotent so retries do not duplicate side effects.
- Store enough metadata to diagnose why a message failed.

A separate queue of already successful messages is usually not the first resilience mechanism; durable source retention/audit storage is more useful when replay or forensic history is required.

Time-to-live for successfully processed messages can be useful for retention control, but it does not replace retry/DLQ handling for messages that never completed successfully.

**Interview answer:**

> For dropped messages I would first verify delivery semantics, retry/backoff, visibility timeout, and consumer idempotency. Repeated failures should move to a dead-letter queue with alerts rather than being lost or retried forever. I would keep enough source retention for replay and monitor queue depth, age, retry rate, DLQ volume, and consumer lag. For very large payloads, I would store the blob in object storage and queue only a small reference plus metadata and checksum.

---

## Senior 60-Minute System Design Interview Framework

> **Goal:** Derive the architecture live instead of presenting a prebuilt diagram. Every major component should be justified by a requirement, bottleneck, failure mode, or ownership/scaling boundary.

This section consolidates a reusable backend/API system-design approach for a 60-minute senior interview. It deliberately emphasizes the gaps that commonly appear when candidates know individual concepts but do not clearly connect them into one executable request path.

### Core Interview Opening

A strong opening is:

> I’ll stay at the high level initially. I’ll clarify the functional and non-functional requirements, define the major APIs and data model, and start with the simplest architecture that satisfies those requirements. As we encounter scaling or reliability concerns, I’ll evolve the design, explain why each component is needed, how it works, its trade-offs and failure modes, and we can zoom into any component you’d like.

This signals:

```text
requirements
    ↓
APIs/resources
    ↓
simplest HLD
    ↓
access patterns/data model
    ↓
measured bottleneck
    ↓
justified evolution
    ↓
critical deep dive
    ↓
reliability/security/observability
```

### 60-Minute Pacing

|   Time    |                                  Focus                                  |
| --------- | ----------------------------------------------------------------------- |
| 0–3 min   | Frame the discussion and core functional scope.                         |
| 3–8 min   | Non-functional requirements and scale assumptions.                      |
| 8–13 min  | API/resource design and authentication assumptions.                     |
| 13–18 min | Simplest architecture and service/module boundaries.                    |
| 18–25 min | Scaling, statelessness, routing, data model, indexes.                   |
| 25–32 min | Cache/CDN where relevant and database read scaling.                     |
| 32–47 min | One or two system-defining deep dives.                                  |
| 47–54 min | Async processing, failure handling, consistency, sharding if justified. |
| 54–58 min | Security, observability, cost, operational concerns.                    |
| 58–60 min | Final evolved diagram and concise recap.                                |

Do not attempt to deep-dive every possible subsystem. Breadth establishes the architecture; depth should concentrate on the defining problem.

---

### 1. Functional vs Non-Functional Requirements

Functional requirements answer:

> What must the product do?

Examples:

- Create/read/update a resource.
- Subscribe/unsubscribe.
- Book/cancel.
- Upload/download.
- Match users/resources.
- View an ordered feed.

Non-functional requirements answer:

> How well must it do those things?

Always resolve these five questions early:

1. How many users/requests/entities are we designing for, and how quickly are they growing?
2. Is the workload read-heavy or write-heavy?
3. Which data can never be lost, and which data can be reconstructed?
4. What latency is acceptable for the critical workflows?
5. What are the cost constraints?

Also clarify where relevant:

- Availability target
- Consistency expectations
- Geographic scope
- Peak/burst traffic
- Retention period
- Security/multi-tenancy
- RPO/RTO

A component introduced later should trace back to one of these constraints.

For example, an onboarding and learning platform may need signup, interest selection, course enrollment, progress tracking, and recommendations. Its NFRs could require fast content delivery, secure authentication, scalable media delivery, reliable progress persistence, and bounded recommendation latency; the same features can lead to different architectures when those constraints change.

---

### 2. Put APIs Early in the Design

For backend/API interviews, concrete endpoints expose the resources and operations the architecture must support.

Example resource API:

```http
POST /v1/jobs
GET /v1/jobs/{job_id}
POST /v1/jobs/{job_id}/cancel
GET /v1/jobs?limit=50&cursor=...
```

Discuss where relevant:

- HTTP method semantics
- 200 vs 201 vs 202 vs 204
- Idempotency keys
- Authentication and authorization
- Cursor pagination
- Optimistic concurrency
- Versioning
- Structured errors
- Async job semantics

#### Important `201` vs `202` nuance

A long-running operation does **not** automatically require `202 Accepted`.

If the API synchronously creates a durable job resource:

```text
POST /jobs
   ↓
DB commits Job(id=123, state=QUEUED)
   ↓
201 Created
Location: /jobs/123
```

Execution can continue asynchronously afterward.

Use `202` when the request has been accepted but the final resource/operation has not yet been completed or durably created in the way the API contract promises.

#### Idempotency for unsafe retries

For retry-sensitive `POST` workflows:

```http
POST /v1/payments
Idempotency-Key: 6f...
```

Store a uniqueness scope such as:

```text
(tenant_id, idempotency_key)
```

plus a normalized request hash and the created resource/response. Reusing the same key with a different payload should fail explicitly rather than silently returning the wrong result.

---

### 3. Server, Service, Module, Instance, Gateway, Load Balancer

These terms should never be blurred together.

#### Server / instance

A server instance is **running compute** executing application code.

Examples:

- Process
- VM
- Container
- Kubernetes pod

#### Service

A service is a **logical business/platform capability** exposed through an interface/API.

Examples:

```text
Feed Service
Subscription Service
Payment Service
Inventory Service
```

One service may run on many instances:

```text
Feed Service
   |
   +-- Feed instance #1
   +-- Feed instance #2
   +-- Feed instance #3
```

#### Module

A module is a logical code boundary **inside the same deployable application**.

```text
App Instance
-------------
Auth Module
Feed Module
Subscription Module
Podcast Module
```

A module call within one process does not require a network hop.

#### API Gateway / router

The gateway answers:

> Which logical service owns this request?

Example:

```text
/feed/*          → Feed Service
/podcasts/*      → Podcast Service
/subscriptions/* → Subscription Service
```

#### Load balancer

A load balancer answers:

> Which equivalent running instance should handle this request?

Example:

```text
Feed Service LB
   |
   +-- Feed #1
   +-- Feed #2
   +-- Feed #3
```

The two routing decisions are different:

```text
Client
  |
  v
API Gateway
  |  chooses logical service
  v
Service Load Balancer
  |  chooses equivalent instance
  v
Running service instance
```

Do not draw one generic load balancer randomly selecting between unrelated services unless it is explicitly doing route-aware L7 proxying and that responsibility is explained.

---

### 4. Start with a Modular Monolith When It Is Enough

Do not begin with microservices only because the interview is called “system design.”

A strong first version is often:

```text
                    Client
                      |
                      v
                Load Balancer
                 /    |    \
                v     v     v
             App #1 App #2 App #3
                |     |     |
        +-------+-----+-----+-------+
        |             |             |
      Module A      Module B      Module C
                \     |     /
                 \    |    /
                  PostgreSQL
```

Every app instance contains all modules, so any endpoint can be routed to any healthy app instance.

#### Why this can be better initially

- Simple deployments
- Easier local development/debugging
- Transactions remain local
- Fewer network failure modes
- Less observability/operational overhead

The criteria for splitting modules into services are consolidated in [Monolith Versus Microservices: Decision Framework](#monolith-versus-microservices-decision-framework).

### 5. Explain What the Server Actually Does

If an interviewer asks “what does the server do?”, answer literally.

For `GET /v1/feed`:

```text
App instance receives HTTP request
   |
   +-- parse request
   +-- authenticate token
   +-- derive trusted user identity
   +-- authorize operation
   +-- execute feed business logic
   +-- query cache/database/downstream services
   +-- merge/rank/filter results
   +-- serialize JSON
   +-- return HTTP response
```

The server is not an unnecessary forwarding box. It is the compute executing the service/module code.

---

### 6. Mandatory End-to-End Request Trace

For the most important workflow, always walk one request from client to response.

Use this checklist:

```text
What does the user do?
        ↓
What HTTP request is created?
        ↓
How is the caller authenticated?
        ↓
Where does the request first arrive?
        ↓
How is it routed?
        ↓
Which running instance executes it?
        ↓
What business code runs?
        ↓
What data does it read?
        ↓
From which datastore/cache/service?
        ↓
What computation/transformation occurs?
        ↓
What response is created?
        ↓
How does the client use it?
```

Avoid vague statements such as:

> The feed service handles it.

Replace them with the exact data flow and transformation.

---

### 7. Scaling: Vertical First, Horizontal When Justified

Vertical scaling:

```text
same instance
   ↓
more CPU / memory
```

Advantages:

- Simple
- Minimal application changes
- Useful short-term capacity increase

Limitations:

- Hardware ceiling
- Still one failure domain

Horizontal scaling:

```text
           +-- App #1
Client--LB-+-- App #2
           +-- App #3
```

Use when:

- Capacity exceeds one host
- Availability requires multiple replicas
- Failure isolation matters
- Workloads need independent scale

High availability can justify horizontal replicas **before** the vertical capacity ceiling is reached.

---

### 8. Stateless Application Instances

Critical cross-request state should not live only in one process.

Bad:

```text
User session created on App #1
next request reaches App #3
App #3 has no session
```

Better:

```text
App #1 --+
App #2 --+--> shared session/state store
App #3 --+
```

or use an appropriate signed token model where the required session claims are carried by the client and verified by the backend.

#### Sticky sessions

Sticky sessions can preserve affinity, but they are a trade-off rather than a complete solution:

- Can produce uneven load
- Complicate failover
- Reduce routing flexibility
- Do not remove the need for load balancing

---

### 9. Derive the Data Model from Access Patterns

Before creating tables, ask:

> What will the application repeatedly need to answer?

Example:

```text
Which podcasts does user 123 follow?
Does user 123 follow podcast 42?
What are podcast 42's latest episodes?
What are the newest eligible items for user 123?
```

Then derive tables/indexes.

This is stronger than inventing a generic schema and hoping it supports the workload.

---

### 10. SQL vs NoSQL Decision Framework

Do not say “NoSQL because scale.”

Evaluate:

- Relationships and joins
- ACID transactions
- Constraints/uniqueness
- Consistency requirements
- Query flexibility
- Access-pattern stability
- Write throughput
- Schema flexibility
- Operational experience

A relational database is often a strong default for control-plane/business state that has meaningful invariants. A specialized store can be introduced later for a distinct read/write pattern.

---

### 11. Indexing: Query First, Index Second

Example query:

```sql
SELECT *
FROM episode
WHERE podcast_id = ?
ORDER BY published_at DESC, episode_id DESC
LIMIT 50;
```

Candidate index:

```text
(podcast_id, published_at DESC, episode_id DESC)
```

Explain the trade-off:

> The index reduces read work for this access pattern, but it consumes storage and increases write/update work.

Do not add indexes without naming the query they optimize.

---

### 12. Cache Only After Identifying a Hot Read

Basic flow:

```text
request
  ↓
cache
 /   \
hit   miss
 |      |
return  DB
         |
         v
      populate
         |
         v
       return
```

#### TTL vs invalidation

- TTL is simple but allows bounded staleness.
- Active invalidation/update reduces staleness but adds coordination.
- A combination is often practical: invalidate on known writes and keep a TTL as a safety net.

#### Cache stampede

A hot key expires:

```text
10,000 requests
      |
      v
     MISS
      |
      v
     DB
```

Defenses:

- Single-flight / request coalescing
- Stale-while-refresh
- Jittered TTLs

#### Cache failure

The cache should usually be an optimization rather than the only source of correctness.

```text
cache unavailable
     ↓
short timeout
     ↓
fallback to authoritative store
     ↓
rate-limit/backpressure to protect it
```

---

### 13. Replication and Read-After-Write

Single-primary model:

```text
             Primary
             /     \
            v       v
       Replica 1 Replica 2
```

In this architecture:

```text
writes → primary
eligible stale-tolerant reads → replicas
```

#### Replication lag

If a user writes and immediately reads from a replica, the new state may be missing.

Options for a workflow requiring read-after-write:

- Route the immediate read to primary.
- Use a consistency/session token.
- Wait for a confirmed replication position where supported.

Normal analytics/feed reads may tolerate small lag while permission/inventory/ownership checks may not.

#### Failover

```text
Primary fails
   ↓
protect/pause ambiguous writes
   ↓
promote sufficiently current replica
   ↓
routing moves to new primary
```

Discuss synchronous vs asynchronous replication if RPO/write latency matters.

---

### 14. Queue Choice and Async Work

Introduce a queue when work:

- Is long-running
- Can complete after the request
- Arrives in bursts
- Benefits from buffering/backpressure
- Should be decoupled from the producer

Different semantics matter:

|                    Need                    |  Better abstraction   |
| ------------------------------------------ | --------------------- |
| One task should be processed by one worker | Work queue            |
| Many independent consumers need the event  | Pub/sub               |
| Consumers need replay/order/history        | Replayable log/stream |

Do not reflexively choose Kafka when a simple work queue is sufficient.

---

### 15. At-Least-Once Delivery + Idempotent Consumer

Avoid casually promising “exactly once.”

Practical design:

```text
message delivered
   ↓
worker processes
   ↓
ack lost / worker crashes
   ↓
message redelivered
```

Therefore the consumer must tolerate duplicates.

Use:

- Stable event/message IDs
- Unique database constraints
- Conditional state transitions
- Idempotency records

A strong answer:

> I prefer at-least-once delivery with idempotent consumers and durable state transitions rather than relying on a vague exactly-once claim.

---

### 16. Transactional Outbox

Problem:

```text
DB commit      ✓
publish event  ✗
process crash
```

The business state exists, but downstream consumers never hear about it.

Outbox pattern:

```text
BEGIN
  write business row
  write outbox row
COMMIT

outbox publisher
   ↓
message broker
```

The business update and intent-to-publish are committed atomically. The publisher can retry independently. Consumers still need idempotency because the event may be published more than once.

---

### 17. Retries, Timeouts, Circuit Breakers, Backpressure

#### Retry strategy

Retry only failures that are plausibly transient and retry-safe.

Use:

- Timeout
- Bounded retries
- Exponential backoff
- Jitter

Do not retry permanent validation failures.

#### Why jitter?

Without jitter, thousands of clients that fail together can retry on the same schedule and create another synchronized traffic spike.

#### Circuit breaker

When a dependency is persistently failing, stop sending it full request volume for a period and fail/fallback quickly. This protects both the caller and the unhealthy dependency.

#### Backpressure

If downstream capacity is lower than incoming demand, prevent unbounded work growth through:

- Bounded queues
- Admission control
- Rate limits
- Producer slowing
- Load shedding

---

### 18. Concurrency and Authoritative State Transitions

For scarce resources such as seats, inventory, driver assignments, quotas, or job ownership, do not make the final allocation decision from stale cache/read-replica state.

Example conditional update:

```sql
UPDATE resource
SET status = 'ALLOCATED'
WHERE id = :id
  AND status = 'AVAILABLE';
```

Interpret result:

```text
1 row changed → success
0 rows changed → conflict/lost race
```

Other tools:

- Optimistic version columns
- Transactions
- Row locks
- Leases
- Heartbeats
- Reconciliation

Choose based on conflict probability and workflow duration.

---

### 19. Leases and Worker Failure

For long-running work, a worker should not own a job forever merely because it dequeued it once.

Example model:

```text
job_id
state
lease_owner
lease_expires_at
attempt
```

Worker flow:

```text
claim job with conditional update
   ↓
set lease expiry
   ↓
heartbeat/extend lease while running
   ↓
complete → final state
```

If the worker dies, the lease expires and a reconciler/new worker can safely reclaim the job.

---

### 20. Sharding Comes Late

Prefer a progression such as:

```text
query optimization
      ↓
indexes
      ↓
vertical scaling
      ↓
caching
      ↓
read replicas
      ↓
partitioning/archival
      ↓
sharding when necessary
```

If sharding is required, discuss:

- Shard key
- Routing
- Hot shards
- Rebalancing
- Cross-shard queries
- Cross-shard transactions
- Operational complexity

Important:

> Sharding does not automatically solve a single hot key or one celebrity/event receiving most of the traffic.

---

### 21. Security and Multi-Tenancy

Cover where relevant:

- TLS
- Authentication
- Authorization
- Service-to-service identity
- Secrets management
- Tenant scoping
- Rate limiting
- Input validation
- Audit logging
- Signed URLs
- PII handling

Keep authentication and authorization distinct:

```text
Authentication → who are you?
Authorization  → are you allowed to perform this action?
```

Do not trust `user_id` from request body as identity when a verified token/context already establishes the caller.

---

### 22. Observability

API/service metrics:

- Request rate
- Error rate
- p50/p95/p99 latency
- Saturation

Database:

- Query latency
- Connection usage
- Lock waits
- Replication lag

Cache:

- Hit/miss rate
- Evictions
- Rebuild latency
- Fallback-to-DB volume

Queue:

- Depth
- **Age of oldest message**
- Consumer lag
- Retry rate
- Dead-letter volume

The age of the oldest queued item can be more actionable than depth alone: a small queue containing one task stuck for hours can be more serious than a large queue draining normally.

Trace with identifiers such as:

```text
request_id
trace_id
user_id / tenant_id
resource_id
job_id
```

---

### 23. Cost

Tie cost to the architecture rather than saying “cost matters.”

Examples:

- Media-heavy product → object storage and egress
- Personalized feed → database reads and cache cardinality
- Realtime service → connection count and fan-out
- Logging platform → ingestion and retention
- Performance-test platform → executor compute

A design can be technically scalable but economically poor.

---

## Complete Example: Podcast Subscription and Latest-Episode Feed

This example is intentionally explicit about the complete request path, what the server does, what the feed logic does, and how the architecture evolves.

### Requirements

Core workflows:

1. Subscribe/unsubscribe to podcasts.
2. View the latest episodes from subscribed podcasts.
3. Register/update podcast and episode metadata through a separate scraper/ingestion process.
4. Actual audio/video remains hosted by the publisher.

Assumptions for discussion:

```text
10M users
hundreds of thousands of podcasts
read-heavy
subscriptions + metadata durable
feed/cache reconstructible
few-hundred-ms feed target
cost matters
```

### APIs

```http
PUT /v1/subscriptions/{podcast_id}
DELETE /v1/subscriptions/{podcast_id}
GET /v1/subscriptions?limit=50&cursor=...
GET /v1/feed?limit=50&cursor=...
GET /v1/podcasts/{podcast_id}
GET /v1/episodes/{episode_id}
```

Internal ingestion:

```http
POST /v1/internal/podcasts
POST /v1/internal/podcasts/{podcast_id}/episodes
```

`PUT` is a good subscription operation because the logical resource identity is naturally `(authenticated_user_id, podcast_id)` and repeated calls can be idempotent.

### Initial HLD: Modular Backend

```text
                 Web / Mobile
                      |
                    HTTPS
                      |
                      v
                Load Balancer
                      |
          +-----------+-----------+
          |           |           |
          v           v           v
       App #1      App #2      App #3
          |           |           |
          +-----------+-----------+
                      |
                      v
                  PostgreSQL

Scraper
   |
   v
internal authenticated endpoint
```

Each app instance contains:

```text
Auth Module
Subscription Module
Podcast Module
Episode Module
Feed Module
Ingestion Module
```

No network hop exists between these modules inside the same application process.

### Data Model

```text
User
----
user_id
email
created_at

Podcast
-------
podcast_id
title
feed_url
website_url
created_at
updated_at

Episode
-------
episode_id
podcast_id
source_episode_id
title
published_at
media_url
created_at

Subscription
------------
user_id
podcast_id
created_at
```

Constraints/indexes:

```text
UNIQUE(user_id, podcast_id)
UNIQUE(podcast_id, source_episode_id)
INDEX subscription(user_id, podcast_id)
INDEX episode(podcast_id, published_at DESC, episode_id DESC)
```

### Exact Feed Request Flow

Client sends:

```http
GET /v1/feed?limit=50
Authorization: Bearer <token>
```

End-to-end:

```text
Web / Mobile
    |
    | GET /v1/feed
    | Authorization token
    v
DNS / Edge
    |
    v
Load Balancer
    |
    | choose healthy app instance
    v
App #2
    |
    +-- authentication middleware validates token
    |       ↓
    |    trusted user_id = 123
    |
    +-- Feed module
            |
            +-- query subscriptions for user 123
            |       ↓
            |    [pod_A, pod_C, pod_F]
            |
            +-- fetch eligible recent episodes
            |
            +-- merge/order by published_at DESC
            |
            +-- take 50 + create cursor
            v
         JSON response
            |
            v
          Client
```

The subscription graph determines **eligibility**. `published_at` determines the basic **ordering** when the product requirement says “latest.” A recommendation model is unnecessary unless personalized ranking becomes a separate requirement.

### Simple SQL Feed

```sql
SELECT e.*
FROM subscription AS s
JOIN episode AS e
  ON e.podcast_id = s.podcast_id
WHERE s.user_id = :user_id
ORDER BY e.published_at DESC, e.episode_id DESC
LIMIT 50;
```

Start here if it meets the latency/scale requirement.

### Large Subscription Set: K-Way Merge

If a user follows many podcasts, retrieve a small newest-first stream per podcast and merge only enough heads to produce the requested page.

```text
Podcast A: 12:30, 11:50, 10:20
Podcast C: 12:25, 11:40
Podcast F: 12:10, 11:30
                |
                v
          heap of stream heads
                |
                v
           newest top 50
```

With P streams and N returned items, the merge work is approximately:

```text
O(N log P)
```

rather than sorting all historical episodes from every subscribed podcast.

### Cursor Pagination

Use an opaque cursor representing ordering position, for example the last:

```text
(published_at, episode_id)
```

This is more stable than offsets when new episodes are inserted at the top between page requests.

### Caching

Prefer reusable podcast-level building blocks before millions of personalized full-feed entries:

```text
podcast:A:latest
podcast:C:latest
podcast:F:latest
```

Then:

```text
user subscriptions
       |
       v
[A, C, F]
 |  |  |
 v  v  v
shared recent-episode cache entries
       |
       v
merge/paginate
```

A full cache key such as `feed:user_123` can be useful later if measurement shows merge/query cost dominates, but it creates high cardinality and harder invalidation when popular podcasts publish.

### Scraper Ingestion

```http
POST /v1/internal/podcasts/pod_42/episodes
```

Payload includes a publisher/source episode identifier. The unique constraint:

```text
UNIQUE(podcast_id, source_episode_id)
```

makes retries safe against duplicate insertion.

For reliable downstream cache invalidation/projections:

```text
BEGIN
  INSERT episode
  INSERT outbox_event
COMMIT
```

The outbox publisher later emits `EPISODE_CREATED` and idempotent consumers invalidate/update read models.

### When to Split Services

If feed generation develops different scaling/failure characteristics:

```text
                        Client
                          |
                          v
                     API Gateway
                  /        |        \
                 v         v         v
          Feed Service  Podcast  Subscription
              LB        Service      Service
            / | \          |            |
           F1 F2 F3       ...          ...
```

Then `/feed` routing is:

```text
API Gateway chooses Feed Service
          ↓
Feed Service LB chooses F1/F2/F3
          ↓
running Feed Service instance executes the request
```

Avoid an N+1 service fan-out such as one network call per subscribed podcast. Use batched internal APIs, shared read models, or direct ownership-appropriate read stores.

---

## System-Specific Deep-Dive Patterns

### Ticketing / Seat Reservation

Core insight:

> Browsing availability may tolerate staleness; final allocation cannot.

#### Calendar availability read path

A calendar or event-list page usually needs a fast read model such as availability counts by event/date:

```text
GET /events/{event_id}/availability?date=2026-08-22
        ↓
availability/read model
        ↓
remaining counts / sections / coarse seat state
```

Those counts may be cached or slightly stale for browsing. Once the user selects a specific seat/ticket, the authoritative inventory store must perform an atomic conditional transition such as `AVAILABLE → HELD`. The UI read does not reserve inventory.

State machine:

```text
AVAILABLE
   |
   v
 HELD
 /   \
v     v
SOLD  AVAILABLE (expiry/cancel)
```

Use an authoritative transaction/conditional update for allocation. Do not hold a database lock for the entire external payment flow.

Flash crowd controls:

- Waiting room/admission control
- Per-event capacity protection
- Rate limiting
- Short holds
- Idempotent payment confirmation
- Reconciliation after uncertain payment states

Sharding by event can distribute normal load but does not eliminate one extremely hot event.

### Ride Matching

Core insight:

> Geospatial search finds candidate drivers; authoritative trip/driver state decides who actually owns the assignment.

Separate data characteristics:

```text
Driver location:
high write rate
loss of a few updates tolerable
geo-optimized

Trip assignment/payment:
stronger consistency
transactional state
```

Use a conditional transition such as `AVAILABLE → ASSIGNED` to prevent two riders from owning the same driver.

### Performance-Test Execution Platform

Typical flow:

```text
Clients/CI
   ↓
Gateway/Auth
   ↓
Run API
   ↓
Postgres + Outbox
   ↓
Scheduler
   ↓
Work Queue
   ↓
Executors / Load Generators
   ↓
Target Systems
```

Use:

- Durable `TestRun` state machine
- Idempotency key for submission
- Tenant quotas/fair scheduling
- Leases/heartbeats for worker ownership
- Object storage for large raw logs/results
- Queue depth **and age** monitoring
- Cancellation as a state transition rather than deleting history

### Photo / Media Application

Keep binary objects outside the relational metadata database:

```text
Client
   ↓
signed upload
   ↓
Object Storage
   ↓
image-processing queue/workers
   ↓
thumbnails/variants
   ↓
CDN
```

Store metadata, ownership, permissions, and object keys in the database.

For social feeds, start with fan-out-on-read and evolve toward fan-out-on-write/hybrid only when measured read cost requires it. Celebrities/high-fanout publishers often need a hybrid strategy.

---

## High-Probability System Design Follow-Up Questions

Practice answering these directly:

1. What exactly does this server do?
2. What is the difference between the service and the server/container/pod?
3. Why is this component a separate service rather than a module?
4. Which component receives this URL first?
5. How does the API know which user is making the request?
6. Why is `user_id` not accepted from the body as identity?
7. How does the gateway know which service owns the route?
8. How does the load balancer select an instance?
9. What happens if one application instance dies?
10. What happens if the load balancer/gateway fails?
11. Why do we need more than one server?
12. Why not just vertically scale?
13. Where is session state stored?
14. Do sticky sessions solve the problem?
15. Why SQL instead of NoSQL?
16. Which exact query does this index optimize?
17. What happens when the cache is stale?
18. What happens when the cache is completely unavailable?
19. How do you prevent a cache stampede?
20. What happens immediately after a write if a read goes to a lagging replica?
21. What if the primary fails?
22. Why do we need a queue?
23. Why this queue abstraction instead of Kafka/pub-sub/a work queue?
24. What happens if a worker crashes after performing the side effect but before acking?
25. How do you make retries safe?
26. What happens if DB commit succeeds but event publication fails?
27. What happens if two users try to allocate the same resource concurrently?
28. Why not use a cache to decide ownership/inventory?
29. What is the shard key?
30. What happens to one hot key/event after sharding?
31. How do you observe that the queue is stuck?
32. What metrics identify the actual latency bottleneck?
33. What is the largest cost driver in this architecture?
34. What happens at 10× traffic?
35. What data can be rebuilt after failure, and what must be durably protected?

---

## Common System Design Mistakes

- Starting with many microservices before establishing a reason for them.
- Drawing “server → service” as if the server is merely forwarding to code running nowhere.
- Using one load balancer to choose among unrelated services without explaining L7 routing.
- Saying “the service handles it” without explaining the request/data flow.
- Introducing Redis/Kafka/sharding because they are common interview buzzwords rather than because a bottleneck exists.
- Choosing NoSQL only because the workload is “large.”
- Treating a cache as authoritative for a scarce resource allocation.
- Assuming replicas are instantly consistent.
- Claiming read replicas universally cannot accept writes rather than describing the proposed replication topology.
- Promising exactly-once delivery without defining failure semantics.
- Retrying non-idempotent operations without an idempotency design.
- Using offsets for fast-changing feeds without discussing insertion drift.
- Saying `202` is always required for long-running work.
- Adding sharding before indexes/cache/replication are considered.
- Ignoring the full client → routing → compute → data → response path.

## Additional Senior System-Design Deep Dives

### Load Balancer Reliability and Algorithms

A load balancer should not become the new single point of failure.

In production, use a managed/redundant load-balancing tier or multiple proxy instances with failover rather than one manually managed process.

Common routing strategies:

- Round robin: distribute requests cyclically across healthy instances.
- Least connections: prefer the instance with fewer active connections.
- Weighted routing: send more traffic to larger/faster instances or during staged rollout.
- Consistent hashing: useful when affinity by key is intentionally required, but it should not be introduced casually.

Health checks determine which instances remain eligible for routing.

Strong interview line:

> The logical diagram shows one load-balancing tier, but I would deploy that tier redundantly or use a managed HA load balancer so it is not itself a single point of failure.

---

### Multi-Tenant Performance-Test Platform: Resource and API Details

Useful resources:

```text
TestConfiguration
TestRun
ResultSummary
Artifact
TenantQuota
```

Possible APIs:

```http
POST /v1/test-runs
Idempotency-Key: <key>

GET /v1/test-runs/{run_id}
POST /v1/test-runs/{run_id}/cancel
GET /v1/test-runs?limit=50&cursor=...
GET /v1/test-runs/{run_id}/results
```

If `POST /test-runs` durably creates:

```text
TestRun(id=R1, state=QUEUED)
```

then `201 Created` is valid even though execution continues later.

Control plane:

```text
Client / CI
    |
    v
Gateway + Auth
    |
    v
Run API
    |
    v
PostgreSQL
    |
    +-- transactional outbox
```

Execution plane:

```text
Scheduler
   |
   v
Work Queue
   |
   +-- Executor 1
   +-- Executor 2
   +-- Executor N
         |
         v
      target systems
```

Large raw test logs/artifacts:

```text
Executor
   ↓
Object Storage
   ↓
DB stores metadata/object key + summary
```

#### Fair scheduling

A simple global FIFO can let one tenant consume all executors.

Use tenant-aware quotas/fair scheduling, for example:

```text
Tenant A queue --+
Tenant B queue --+--> fair scheduler --> executor capacity
Tenant C queue --+
```

Possible controls:

- Per-tenant concurrent-run limit
- Weighted fair queues
- Priority with starvation protection
- Admission control when platform is saturated

#### Cancellation

Cancellation is not equivalent to deleting history.

```text
QUEUED → CANCELLED
RUNNING → CANCELLING → CANCELLED
```

Workers should periodically observe cancellation or receive a control signal. Final state transitions must remain idempotent.

---

### Ticketing: Payment and Hold State Details

A seat hold should be short-lived and represented durably:

```text
seat_id
state
hold_id
held_by
hold_expires_at
version
```

Allocation:

```sql
UPDATE seat
SET state = 'HELD',
    hold_id = :hold_id,
    held_by = :user_id,
    hold_expires_at = :expiry
WHERE seat_id = :seat_id
  AND state = 'AVAILABLE';
```

External payment should not keep the database row locked for the full payment interaction.

Payment state can be modeled separately:

```text
CREATED
  ↓
PROCESSING
 /        \
v          v
SUCCEEDED FAILED
   |
 uncertain callback/timeout
   v
RECONCILING
```

Use provider/idempotency IDs and reconciliation for cases where the payment provider may have succeeded but the local response was lost.

---

### Ride Matching: Candidate Search vs Ownership

Do not confuse “closest driver” with “assigned driver.”

```text
Geo store
   ↓
returns candidate drivers near rider
   ↓
Trip/Driver authoritative store
   ↓
conditional AVAILABLE → ASSIGNED
   ↓
winner owns trip
```

This separation is powerful because the geo index can tolerate rapidly changing/occasionally stale location signals while assignment requires a stronger invariant.

If multiple candidate drivers are attempted:

- Use bounded fan-out rather than contacting every nearby driver.
- Apply timeout to each offer.
- Avoid assigning one driver to two trips via conditional state.
- Release/reconcile stale reservations if the matching worker fails.

---

### Feed Generation: Fan-Out-on-Read vs Fan-Out-on-Write

#### Fan-out-on-read

At request time:

```text
user
  ↓
subscriptions/followees
  ↓
recent items per source
  ↓
merge/rank
  ↓
feed response
```

Pros:

- Simple writes
- No need to precompute feeds for inactive users
- Fresh relationship changes are easy to reflect

Cons:

- Expensive read-time fan-out for users following many sources

#### Fan-out-on-write

When publisher creates an item:

```text
new item
   ↓
find followers
   ↓
write item ID into follower feed projections
```

Pros:

- Fast feed reads

Cons:

- Write amplification
- Expensive celebrity/high-follower publishers
- More invalidation/replay complexity

#### Hybrid

Precompute for ordinary publishers; merge celebrity/high-fanout sources at read time.

A strong interview answer starts with fan-out-on-read if scale allows and introduces precomputation only after feed-read cost is shown to be the bottleneck.

---

## Reusable Mock-Interview Prompt Template

Use this template when practicing a new design:

> Act as me, the candidate, in a real 60-minute senior backend/API system-design interview. Start by clarifying functional and non-functional requirements, including scale, read/write ratio, durability, latency, and cost. Define concrete APIs and authentication assumptions early. Start with the simplest architecture and evolve it only when a requirement creates a bottleneck. At every major step show the current cumulative HLD and the relevant LLD/data flow. Be precise about server/instance vs service vs module, API gateway vs service load balancer, and trace at least one critical request end to end from client through routing, compute, data access, transformation, and response. Cover data model, SQL/NoSQL, indexes, caching, replication/read-after-write, queues/outbox/idempotency, concurrency/consistency, failure modes, security, observability, and cost where relevant. Spend most deep-dive time on the one or two system-defining problems. Keep the entire answer realistic for 60 minutes and finish with the final evolved architecture and a 60–90 second summary.
