# REST API & Backend APIs

> **Purpose:** REST, FastAPI, Flask, backend API design, security, validation, idempotency, gRPC, GraphQL, and API scalability.
> **Use this file for:** backend API interviews and Python web-service roles

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

- REST fundamentals and HTTP methods
- FastAPI and Flask API implementation
- Request validation with Pydantic
- Status codes and error handling
- Authentication and authorization
- Pagination, filtering, sorting, versioning
- Idempotency keys for safe retries
- gRPC and GraphQL comparisons

---

## Consolidated Interview Questions & Technical Notes

> Backend API design, FastAPI, Flask, REST, gRPC, GraphQL, request validation, API security, pagination, scaling APIs, and clean architecture.

### 1. API Integration Topics

#### 1.1 API Integration in AI Agents

An AI agent may call APIs to:

- Fetch customer details
- Retrieve order status
- Create support tickets
- Update records
- Trigger workflows
- Search databases
- Retrieve documents

### 2. Scaling FastAPI Applications

#### 2.1 Scaling FastAPI from 5 Pods to 100 Pods

> "To scale a FastAPI application from 5 pods to 100 pods, I would use Kubernetes Horizontal Pod Autoscaler. First, I would make sure the application is stateless, containerized properly, and has health checks. Then Kubernetes can scale pods based on CPU, memory, or custom request metrics."

#### 2.2 Key Steps

- Make application stateless
- Containerize with Docker
- Deploy to Kubernetes
- Configure HPA
- Add readiness and liveness probes
- Use Kubernetes Service / Load Balancer
- Move sessions to Redis
- Use managed database
- Add connection pooling
- Monitor CPU, memory, latency, errors
- Watch external API rate limits
- Monitor LLM latency and token cost

#### 2.3 Example Kubernetes HPA

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: fastapi-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: fastapi-app
  minReplicas: 5
  maxReplicas: 100
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

#### 2.4 Readiness and Liveness Probe Example

```yaml
readinessProbe:
  httpGet:
    path: /health/ready
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 5

livenessProbe:
  httpGet:
    path: /health/live
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10
```

#### 2.5 Strong Interview Line

> "Scaling pods is easy; the real challenge is making sure the database, cache, external APIs, vector database, and LLM provider can handle the increased traffic too."

---

### 3. Backend API Development

#### Topics to revise

- API design principles.
- Request/response lifecycle.
- HTTP methods: GET, POST, PUT, PATCH, DELETE.
- Status codes.
- Validation.
- Authentication and authorization.
- Pagination.
- Rate limiting.
- Idempotency.
- Error handling.
- Versioning.
- API documentation.

#### Common interview questions

1. How do you design a reliable backend API?
2. What is the difference between PUT and PATCH?
3. How do you handle API errors?
4. How do you secure an API?
5. How do you validate incoming data?
6. How do you design APIs for high traffic?
7. How do you handle backward compatibility?

---

#### Example: API error response format

```json
{
  "error": {
    "code": "INVALID_INPUT",
    "message": "The provided document_id is invalid.",
    "details": {
      "field": "document_id",
      "reason": "Must be a valid UUID"
    }
  }
}
```

**Interview explanation:**

Consistent error formats make APIs easier to consume, debug, monitor, and document.

### 4. Flask

Flask may be discussed because the role mentioned FastAPI/Flask.

#### Topics to revise

- Flask app structure.
- Routes.
- Blueprints.
- Middleware-like hooks.
- Request validation.
- Error handling.
- When Flask is suitable vs FastAPI.

#### FastAPI vs Flask

|     Area      |                   FastAPI                    |                     Flask                      |
| ------------- | -------------------------------------------- | ---------------------------------------------- |
| Async support | Built-in and modern                          | Possible, but not the main design focus        |
| Validation    | Pydantic-based                               | Usually manual or with extensions              |
| API docs      | Automatic OpenAPI                            | Requires extensions                            |
| Best fit      | Modern APIs, typed services, async workloads | Lightweight apps, simple services, legacy apps |

---

### Django Request Flow and MVT

Django is a batteries-included Python web framework. A normal request can be explained as:

```text
client
  ↓
middleware
  ↓
URL router
  ↓
view
  ↓
service/business logic
  ↓
model / Django ORM / database
  ↓
template or JSON response
```

Django is commonly described with **MVT**:

- **Model:** persistent/domain data and ORM mapping.
- **View:** request handling and application logic.
- **Template:** server-rendered presentation.

Django also includes migrations, authentication, sessions, admin tooling, middleware, forms, and a mature ORM. For API-heavy systems, Django REST Framework is a common addition.

Interview answer:

> Django is a higher-level, batteries-included framework. Requests pass through middleware and URL routing into a view, which may use models through the ORM and return either rendered HTML or an API response. I would choose Django when built-in ORM, auth, admin, migrations, and convention are valuable; I would choose a lighter framework when I want a smaller API-first surface.

---

### Flask Application Context vs Request Context

Flask uses context-local proxies so code can access the active app/request without passing those objects through every function.

|       Context       |   Typical Objects    |                           Meaning                            |
| ------------------- | -------------------- | ------------------------------------------------------------ |
| Application context | `current_app`, `g`   | The active Flask application and context-local scratch state |
| Request context     | `request`, `session` | One specific HTTP request and its request/session data       |

For a normal HTTP request, Flask pushes the request context and the corresponding application context, then removes them when request processing ends.

```text
request starts
   ↓
application context available
request context available
   ↓
view executes
   ↓
request context removed
application context removed
```

A common error outside an active context is:

```text
RuntimeError: Working outside of application context
```

For work that needs an application context without an incoming request:

```python
with app.app_context():
    # current_app and application-bound extensions are available here
    ...
```

Important nuance: the application context usually does **not** mean "the entire lifetime of the server process." Its lifetime is the active context, which during normal request handling is typically request-scoped.

---

### Flask Application Factory Pattern

Instead of creating and configuring one global application at import time, construct it through a factory:

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_object: str | None = None) -> Flask:
    app = Flask(__name__)

    if config_object:
        app.config.from_object(config_object)

    db.init_app(app)

    from .routes import api_blueprint
    app.register_blueprint(api_blueprint)

    return app
```

Why it helps:

- Different development/test/production configurations.
- Cleaner tests that create isolated app instances.
- Extensions are created once but bound with `init_app(app)`.
- Reduced circular-import pressure.
- Easier blueprint/module registration.

Interview answer:

> The application factory pattern moves Flask construction into `create_app()`. That lets me create independently configured app instances, initialize extensions against a specific app, improve testability, and reduce global coupling/circular imports.

---

### Production Flask Deployment

Do not treat Flask's development server as the production serving layer. A traditional Flask deployment uses a production **WSGI server** such as Gunicorn (or another production-capable WSGI server), often behind a load balancer or reverse proxy.

```text
client
  ↓
load balancer / reverse proxy
  ↓
Gunicorn worker processes
  ↓
Flask application created by create_app()
  ↓
DB / cache / downstream APIs
```

Example factory-style Gunicorn target:

```bash
gunicorn "app:create_app()"
```

The WSGI server owns worker/process lifecycle and accepts production traffic; Flask still owns routing, contexts, views, and application behavior.

---

### 5. REST, gRPC, and API Design

#### REST

REST is commonly used for web APIs. It uses HTTP methods, resources, and status codes.

Example:

```text
GET /documents/{document_id}
POST /documents
DELETE /documents/{document_id}
```

#### gRPC

gRPC is often used for internal service-to-service communication where performance, strict contracts, and streaming are important.

#### Common interview question

##### When would you choose gRPC over REST?

**Answer:**

Use gRPC when services need strong contracts, low latency, efficient binary serialization, streaming, and internal service-to-service communication. Use REST when simplicity, broad compatibility, and public-facing API access matter more.

---

### 6. Clean Architecture & Code Organization

#### Topics to revise

- Separation of concerns.
- Controllers/routes.
- Services/use cases.
- Repositories/data access.
- Domain models.
- Dependency inversion.
- Testability.

#### Example folder structure

```text
app/
  api/
    routes.py
  core/
    config.py
    security.py
  services/
    document_service.py
    rag_service.py
  repositories/
    document_repository.py
  models/
    document.py
  schemas/
    document_schema.py
  tests/
    test_documents.py
```

#### Interview explanation

Clean architecture keeps business logic separate from frameworks and databases. This makes the system easier to test, maintain, and change.

---

### 7. REST API Fundamentals

#### 7.1 What is a REST API?

##### Answer

A REST API is a way for applications to communicate over HTTP using standard methods like GET, POST, PUT, PATCH, and DELETE.

It is commonly used for:

- Frontend to backend communication
- Mobile app to backend communication
- Service-to-service communication
- Third-party integrations

---

##### Example

Request:

```http
GET /restaurants
```

Response:

```json
[
  {
    "name": "Pizza Place",
    "rating": 4.5
  }
]
```

---

#### 7.2 REST API characteristics

|    Characteristic    |            Explanation             |
| -------------------- | ---------------------------------- |
| Stateless            | Each request is independent        |
| Resource-based       | Uses URLs like `/users`, `/orders` |
| Uses HTTP methods    | GET, POST, PUT, PATCH, DELETE      |
| Usually JSON         | Data is commonly exchanged in JSON |
| Language independent | Any language can consume REST APIs |

---

#### 7.3 Common HTTP methods

| Method |           Purpose           |
| ------ | --------------------------- |
| GET    | Fetch data                  |
| POST   | Create/send/upload data     |
| PUT    | Replace entire resource     |
| PATCH  | Partially update a resource |
| DELETE | Remove data                 |

---

#### 7.4 GET API example

##### FastAPI Example

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {
        "id": user_id,
        "name": "Alex"
    }
```

Request:

```http
GET /users/1
```

Response:

```json
{
  "id": 1,
  "name": "Alex"
}
```

##### Interview Explanation

> GET APIs are used to retrieve data from the server. They should generally be read-only and should not modify server data.

---

#### 7.5 Query parameter example

```python
@app.get("/search")
def search(name: str):
    return {"result": name}
```

Request:

```http
GET /search?name=alex
```

Response:

```json
{
  "result": "alex"
}
```

---

#### 7.6 POST API example

POST is used to send or create data on the server.

##### FastAPI Example

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    email: str

@app.post("/users")
def create_user(user: User):
    return {
        "message": "User created",
        "data": user
    }
```

Request:

```http
POST /users
```

Body:

```json
{
  "name": "Alex",
  "email": "alex@example.com"
}
```

Response:

```json
{
  "message": "User created",
  "data": {
    "name": "Alex",
    "email": "alex@example.com"
  }
}
```

---

#### 7.7 POST file upload example

POST is commonly used for uploading files such as resumes, images, or documents.

```python
from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}
```

Request:

```http
POST /upload
```

Content type:

```text
multipart/form-data
```

Response:

```json
{
  "filename": "resume.pdf"
}
```

---

#### 7.8 How do you fetch one specific record?

Use a path parameter or query parameter.

##### Path Parameter

```http
GET /cars/5
```

FastAPI:

```python
@app.get("/cars/{car_id}")
def get_car(car_id: int):
    return {
        "car_id": car_id,
        "price": 25000
    }
```

Response:

```json
{
  "car_id": 5,
  "price": 25000
}
```

##### Query Parameter

```http
GET /cars?price=25000
```

FastAPI:

```python
@app.get("/cars")
def get_car(price: int):
    return {"price": price}
```

---

#### 7.9 GET vs POST

|              GET              |             POST             |
| ----------------------------- | ---------------------------- |
| Fetches data                  | Sends/creates/uploads data   |
| Parameters usually in URL     | Data usually in request body |
| Should not modify server data | Can modify server data       |
| Usually cacheable             | Usually not cacheable        |
| Idempotent                    | Not always idempotent        |

---

#### 7.10 Common HTTP status codes

| Code |        Meaning        |
| ---- | --------------------- |
| 200  | Success               |
| 201  | Created               |
| 400  | Bad Request           |
| 401  | Unauthorized          |
| 403  | Forbidden             |
| 404  | Not Found             |
| 409  | Conflict              |
| 500  | Internal Server Error |

### 8. Async APIs and Concurrent Requests

#### 8.1 What is async support in FastAPI?

FastAPI supports `async` and `await` using ASGI.

This allows non-blocking request handling.

---

#### 8.2 API without async

```python
@app.get("/users")
def get_users():
    data = call_external_api()
    return data
```

Here, the request is blocking.

If `call_external_api()` takes 5 seconds, the worker waits for 5 seconds.

Good for:

- Simple APIs
- CPU-heavy logic
- Libraries that are not async
- Basic CRUD apps

---

#### 8.3 API with async

```python
@app.get("/users")
async def get_users():
    data = await call_external_api_async()
    return data
```

Here, the request is non-blocking.

If the external API takes 5 seconds, FastAPI can handle other requests while waiting.

Good for:

- External API calls
- Database calls
- File operations
- GenAI/LLM calls
- Vector database calls

---

#### 8.4 Async vs sync interview answer

> The main difference is blocking versus non-blocking execution. In a synchronous API, the worker waits until the task finishes. In an async API, when the code is waiting for an I/O operation like a database call or external API call, the event loop can process other requests. Async improves concurrency and scalability for I/O-heavy workloads, especially GenAI APIs where LLM calls may take several seconds.

Important:

> Async does not automatically make CPU-heavy code faster. It mainly helps when the API spends time waiting on I/O.

---

#### 8.5 What happens when two users hit the same API at the same time?

##### Answer

The backend treats them as two independent HTTP requests.

Each request has its own:

- Request object
- Headers
- Body
- Authentication token
- Response lifecycle

---

##### Read-only API scenario

Example:

```http
GET /cars/available
```

If both users are checking available cars, both can get the same response.

Response:

```json
{
  "car_id": 101,
  "status": "available"
}
```

This is usually fine because no data is being modified.

---

##### Write API scenario

Example:

```http
POST /cars/101/book
```

If two users try to book the same car at the same time, this can create a **race condition**.

Bad scenario:

1. User A checks car 101 is available.
2. User B also checks car 101 is available.
3. Both try to book it.
4. Without proper controls, both may get success.

That is incorrect.

---

#### 8.6 How to handle race conditions in APIs

Use:

- Database transactions
- Row-level locking
- Unique constraints
- Optimistic locking
- Idempotency keys
- Proper status checks

##### Safe Booking Example

```python
@app.post("/cars/{car_id}/book")
def book_car(car_id: int, user_id: int):
    car = (
        db.query(Car)
        .filter(Car.id == car_id)
        .with_for_update()
        .first()
    )

    if car.status != "available":
        return {"message": "Car already booked"}

    car.status = "booked"
    car.booked_by = user_id
    db.commit()

    return {"message": "Booking successful"}
```

Expected behavior:

First user:

```json
{
  "message": "Booking successful"
}
```

Second user:

```json
{
  "message": "Car already booked"
}
```

Better HTTP status for second user:

```http
409 Conflict
```

##### Important Interview Point

> Async helps the API handle concurrent requests efficiently, but it does not solve data consistency problems by itself. Race conditions must be handled using database-level consistency controls.

---

### 9. Code Review and API Fix Case Topics

#### 9.1 User API endpoint defects identified

##### Issues covered

- `SELECT *` returns unnecessary/sensitive fields.
- `password_hash` leaked in response.
- Deleted/soft-deleted users still returned.
- SQL injection risk due to string concatenation.
- Missing input validation.
- Invalid filters silently return all users.
- N+1 query pattern for posts per user.
- No pagination on large table.
- In-memory filtering instead of DB filtering.
- No request-level field filtering based on caller type.

---

#### 9.2 Which issue to fix first?

##### Highest priority options

- SQL injection vulnerability.
- Password hash leakage.

##### Reason

Security issues have the highest blast radius and can expose sensitive data or allow data compromise.

##### Suggested answer

> I would fix the security issue first, especially password hash leakage or SQL injection, because those create immediate risk beyond performance degradation.

---

#### 9.3 Corrected API implementation pattern

##### Pseudocode

```javascript
app.get('/api/users', async (req, res) => {
  const allowedFilters = ['active', 'inactive'];
  const filter = req.query.filter;
  const limit = Math.min(parseInt(req.query.limit || '50', 10), 100);
  const cursor = req.query.cursor;

  if (filter && !allowedFilters.includes(filter)) {
    return res.status(400).json({ error: 'Invalid filter' });
  }

  const params = [];
  let where = 'WHERE deleted_at IS NULL';

  if (filter === 'active') {
    where += ' AND last_login IS NOT NULL';
  }

  if (cursor) {
    params.push(cursor);
    where += ` AND id > $${params.length}`;
  }

  params.push(limit);

  const users = await db.query(
    `SELECT id, username, display_name, avatar_url, last_login
     FROM users
     ${where}
     ORDER BY id
     LIMIT $${params.length}`,
    params
  );

  const userIds = users.rows.map(u => u.id);

  const posts = await db.query(
    `SELECT user_id, id, title, created_at
     FROM posts
     WHERE user_id = ANY($1)`,
    [userIds]
  );

  const postsByUser = groupBy(posts.rows, 'user_id');

  const response = users.rows.map(user => ({
    ...user,
    posts: postsByUser[user.id] || []
  }));

  res.json({ data: response, next_cursor: getNextCursor(response) });
});
```

##### What this fixes

- Prevents SQL injection through parameterized queries.
- Excludes deleted users.
- Removes password hash.
- Validates filters.
- Adds pagination.
- Avoids N+1 posts query.
- Projects only required fields.

---

#### 9.4 One performance improvement to recommend

##### Best choices

1. Pagination.
2. Batch query/JOIN to eliminate N+1.
3. Database indexes on filter columns.
4. Caching for hot users.

##### Strongest general answer

For a large user table and list endpoint, **pagination** is usually the first stability improvement because it limits response size and DB load.

##### If the known bottleneck is N+1

Choose **batch query/JOIN** because it directly removes hundreds/thousands of extra DB queries.

##### If many requests target same top users

Choose **Redis/in-memory caching for hot users**.

---

### Backend API Security & Monitoring

#### API Security

##### Interview Question

**How can you secure an API?**

##### Answer

API security can be implemented through:

- Authentication
- Authorization
- HTTPS
- JWT tokens
- OAuth2
- API keys
- Rate limiting
- Input validation
- CORS configuration
- Logging and monitoring
- Secrets management

##### JWT Example Concept

```text
Client logs in
→ server verifies credentials
→ server issues JWT
→ client sends JWT in Authorization header
→ API validates token before processing request
```

---

#### API Monitoring

##### Interview Question

**How would you track which user calls which API and token usage?**

##### Answer

Track request-level metadata.

##### What to Log

- User ID
- Endpoint
- Timestamp
- Request ID
- Response status
- Latency
- Token usage
- Cost estimate
- Error message if failed

##### Example Logging Middleware

```python
import time
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()

    response = await call_next(request)

    latency_ms = (time.time() - start) * 1000

    print({
        "path": request.url.path,
        "method": request.method,
        "status_code": response.status_code,
        "latency_ms": round(latency_ms, 2)
    })

    return response
```

---

### 10. REST API Examples, Pagination & Idempotency

#### REST API Example With FastAPI

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class OrderCreate(BaseModel):
    customer_id: int
    total_amount: float
    currency: str = "CAD"

orders = {}

@app.post("/orders", status_code=201)
def create_order(payload: OrderCreate):
    order_id = len(orders) + 1

    orders[order_id] = {
        "id": order_id,
        "customer_id": payload.customer_id,
        "total_amount": payload.total_amount,
        "currency": payload.currency,
        "status": "created",
    }

    return orders[order_id]

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")

    return orders[order_id]
```

##### Interview Explanation

This demonstrates:

- Request validation with Pydantic
- Proper status codes
- Clear resource-oriented design
- Error handling with HTTP exceptions

#### API Pagination Example

```python
@app.get("/orders")
def list_orders(limit: int = 50, offset: int = 0):
    limit = min(limit, 100)

    all_orders = list(orders.values())
    return {
        "items": all_orders[offset : offset + limit],
        "limit": limit,
        "offset": offset,
        "total": len(all_orders),
    }
```

##### Interview Explanation

Pagination prevents:

- Huge responses
- Slow queries
- Memory pressure
- Poor frontend performance

---

#### API Idempotency

##### Question

How do you prevent duplicate payment/order creation when a client retries?

##### Answer

Use an idempotency key.

```python
processed_requests = {}

def create_payment(idempotency_key: str, payload: dict):
    if idempotency_key in processed_requests:
        return processed_requests[idempotency_key]

    payment = charge_customer(payload)
    processed_requests[idempotency_key] = payment
    return payment
```

##### Interview Explanation

This is important when:

- Clients retry after timeout
- Payment APIs are involved
- Order creation must not duplicate records

---

## Production-Style AI-Enabled Backend Project Walkthrough

A strong project explanation should make it clear that the application is a backend product with an AI capability, not merely a prompt demo.

### Example Architecture

```text
Client
  |
  v
FastAPI Routes
  |
  +--> Authentication and authorization
  +--> Pydantic request validation
  |
  v
Application Services
  |
  +--> Resume/profile domain logic
  +--> Job-description processing
  +--> AI workflow orchestration
  |
  +--> PostgreSQL repositories
  +--> Model-provider adapter
  |
  v
External LLM / Embedding Provider
```

### Backend Responsibilities

A complete implementation can include:

- REST endpoint design and OpenAPI documentation.
- JWT-based authentication and authorization checks.
- Pydantic request and response schemas.
- PostgreSQL persistence and repository abstractions.
- Service-layer business logic.
- Model-provider integration behind an adapter.
- Structured errors and consistent HTTP status codes.
- Unit, integration, and API tests.
- Docker packaging, logging, and deployment configuration.

### Keep AI Logic Out of the Route Layer

Routes should handle transport concerns and delegate business behavior:

```python
@router.post("/resumes/{resume_id}/tailor", response_model=TailoredResumeResponse)
def tailor_resume(
    resume_id: int,
    payload: TailorResumeRequest,
    service: ResumeService = Depends(get_resume_service),
) -> TailoredResumeResponse:
    return service.tailor_resume(
        resume_id=resume_id,
        job_description=payload.job_description,
    )
```

The service can coordinate storage, prompt construction, model invocation, validation, and response formatting. This keeps the API independent of a specific model vendor.

### Suggested Delivery Timeline

A practical phased approach is:

1. Define use cases, API contracts, and database entities.
2. Implement authentication and core CRUD endpoints.
3. Add the application-service and repository layers.
4. Integrate the model through a provider interface.
5. Add validation, error handling, and observability.
6. Write unit and integration tests.
7. Containerize and validate deployment readiness.
8. Treat the agreed feature set as the MVP boundary.

### What Makes the MVP Complete

A personal project does not need endless features. It can be considered complete when the planned vertical slice works end to end:

- Authenticated request enters the API.
- Domain data is validated and persisted.
- The AI workflow executes through a replaceable adapter.
- Output is validated and returned through a documented schema.
- Failures are logged and translated into safe API errors.
- Core behavior is covered by automated tests.
- The service can be started consistently through Docker.

Possible later phases include analytics, feedback loops, rate limiting, model fallback, asynchronous jobs, and load-based scaling.

### Explaining Recent API Experience Accurately

When recent work has focused more on model evaluation than endpoint ownership, separate the two clearly:

> My recent responsibilities concentrated on AI evaluation, prompt workflows, Python automation, and supporting integrations rather than owning a public production API end to end. My earlier backend roles and personal projects included production-style REST services, database integration, testing, containerization, and deployment. The API fundamentals remain current because I continued writing Python and working across service boundaries.

This answer is stronger than overstating recent API ownership because it identifies both proven experience and the exact ramp-up area.

### Technical Ramp-Up Plan for a Backend Platform

The main ramp-up should be project-specific rather than a relearning of backend fundamentals:

- Map the request path from gateway to storage and downstream services.
- Read API contracts, architecture decisions, and operational runbooks.
- Run the service and test suite locally.
- Trace one production-like request through logs and metrics.
- Ship a small bug fix or endpoint change first.
- Review current framework, dependency, security, and deployment conventions.

The transferable foundation is Python, HTTP semantics, data modeling, testing, observability, and production debugging.

---

## Create-Endpoint Debugging: Persistence, Nested Resources & Business Identifiers

A create endpoint can look superficially correct because it parses JSON and returns `201 Created`, while still failing its actual contract if nothing is persisted or the response body is incomplete.

### Trace the Complete Request Path

For a broken create API, trace the full path rather than editing the first suspicious line:

```text
route
  ↓
authentication / middleware
  ↓
request parsing and validation
  ↓
foreign-key / related-object lookups
  ↓
business identifier generation
  ↓
persistence
  ↓
secondary side effects / audit activity
  ↓
serialization
  ↓
status code + response body
```

A useful debugging comparison is a nearby working read/update handler because it often shows the repository's established lookup, `select_related`, error, and serialization patterns.

### Validate Before Mutating

For a typical issue/task create endpoint:

1. Require authentication.
2. Validate non-blank `title`.
3. Resolve `teamId`; return `404` if the team does not exist.
4. Resolve optional assignee.
5. Resolve optional parent item and validate relationship invariants.
6. Generate the team-local business identifier.
7. Set creator from the authenticated principal.
8. Persist the record.
9. Create audit/activity data if required.
10. Serialize the persisted object and return `201`.

Do not return success before step 8.

### Use Authenticated Identity for Audit Fields

Do not trust request-body fields such as `creator` when the authenticated principal already establishes identity.

```python
issue = Issue.objects.create(
    ...,
    creator=request.user,
)
```

This prevents callers from spoofing ownership/audit metadata.

### Nested Resources Through the Same Create Endpoint

A sub-item can use the same endpoint with an optional `parentIssue` field rather than requiring a second create route.

Validate:

- Parent exists.
- Parent and child belong to the expected scope/team.
- Parent relationship is persisted.
- The response exposes the parent identifier in the contract's expected shape.

The UI is not an integrity boundary; parent-child rules should be enforced in the backend as well.

### Sequential Business Identifiers

A business identifier such as:

```text
TEAM-1
TEAM-2
TEAM-3
```

must be independent per team.

Avoid:

```python
number = Issue.objects.count() + 1
```

Problems:

- It is global rather than team-local.
- Deletions can cause reused numbers.
- Concurrent requests can compute the same next value.

A production-safe design typically uses a serialized per-team sequence source, for example:

```text
transaction.atomic()
  ↓
lock team-sequence row with SELECT ... FOR UPDATE
  ↓
read and increment next_number
  ↓
create issue with TEAM_KEY-number
  ↓
commit
```

Keep a database uniqueness constraint on the final identifier as a last line of defense. A simpler `MAX(suffix) + 1` query may be enough for a coding exercise but is still not concurrency-safe without serialization/retry.

### Error Shape Is Part of the API Contract

These are not equivalent contracts:

```json
{}
```

and:

```json
{
  "message": "Authentication required"
}
```

Even if both return `401`, clients and tests may depend on the documented body shape. Avoid route-specific middleware exceptions unless the API explicitly requires them.

### Success Response Should Reflect Persisted State

Prefer returning the canonical serializer representation of the saved entity:

```python
return JsonResponse({"issue": issue.to_dict()}, status=201)
```

If relationships are required by the serializer, reload with `select_related(...)` or otherwise ensure the returned object contains the expected data.

**Interview answer:**

> For a broken create endpoint, I trace route, auth, validation, lookups, persistence, side effects, and serialization as one flow. A `201` response is meaningless if the write never happened. I validate required fields and relationships first, derive creator from the authenticated user, allocate any business identifier safely, persist the entity, record audit activity, then return the canonical serialized representation. I also verify error body shape, because status code alone is not the full API contract.

See `coding_questions/issue_creation_workflow.py` for a runnable generalized version of this debugging exercise.

---

## Senior Backend API Interview Addendum

This section consolidates reusable API/FastAPI material that commonly appears in senior backend rounds, especially when the interviewer follows a high-level answer with “what exactly happens in the request?”, “how do you persist it?”, “how do you test it?”, or “what happens under concurrency?”

### HTTP Method Semantics

|  Method  | Safe | Idempotent by semantics |                       Typical use                        |
| -------- | ---- | ----------------------- | -------------------------------------------------------- |
| `GET`    | Yes  | Yes                     | Read a resource/query.                                   |
| `POST`   | No   | No                      | Create under server-assigned identity, commands/actions. |
| `PUT`    | No   | Yes                     | Create/replace resource at a known identity.             |
| `PATCH`  | No   | Not guaranteed          | Partial update.                                          |
| `DELETE` | No   | Yes in effect           | Ensure resource is absent.                               |

`DELETE` being idempotent does not mean every repeated response must have the same status code; it means repeating the operation should not create additional state changes after the resource is already absent.

---

### `200` vs `201` vs `202` vs `204`

- `200 OK`: successful request with a response representation.
- `201 Created`: a resource was created; often include `Location`.
- `202 Accepted`: request accepted for processing, but the promised operation/resource creation is not yet complete.
- `204 No Content`: successful request with no response body.

Important long-running-job nuance:

```text
POST /jobs
  ↓
create durable Job(id=123, state=QUEUED)
  ↓
commit DB
  ↓
201 Created + Location: /jobs/123
  ↓
worker executes asynchronously
```

A long-running job can still return `201` if the job resource itself is durably created synchronously.

---

### Authentication: Do Not Trust `user_id` from the Request Body

Client:

```http
GET /v1/feed
Authorization: Bearer <access-token>
```

Backend flow:

```text
request
  ↓
auth middleware validates token
  ↓
trusted identity / user_id in request context
  ↓
authorization
  ↓
business logic
```

The caller may submit resource IDs needed for the operation, but the server should derive the caller identity from trusted authentication context when possible.

Authentication answers “who are you?” Authorization answers “are you allowed to do this?”

---

### Cursor Pagination

For fast-changing ordered data, cursor pagination is usually safer than offset pagination.

Example:

```http
GET /v1/feed?limit=50&cursor=<opaque-token>
```

Underlying stable ordering might be:

```text
(created_at, id)
```

or:

```text
(published_at, episode_id)
```

The cursor can encode the last returned ordering tuple. New rows inserted at the top do not shift all later pages the way offsets can.

---

### Optimistic Concurrency with ETag / Version

For update races:

```http
GET /v1/resources/123
ETag: "v7"
```

Client update:

```http
PUT /v1/resources/123
If-Match: "v7"
```

If the resource is now version 8, reject the stale write rather than silently overwriting a newer update.

At the database layer the same concept may be implemented with a version column and conditional `UPDATE`.

---

### REST vs GraphQL

|     Topic      |        REST        |            GraphQL            |
| -------------- | ------------------ | ----------------------------- |
| Data fetching  | Multiple endpoints | Single endpoint               |
| Response shape | Server-defined     | Client-defined                |
| Over-fetching  | Common             | Reduced                       |
| Caching        | Easier with HTTP   | More complex                  |
| Learning curve | Lower              | Higher                        |
| Best for       | Standard CRUD APIs | Flexible UI-driven data needs |

REST is usually the simpler choice for resource-oriented public APIs and standard HTTP caching. GraphQL is useful when clients need flexible response shapes across related data and the team can support query-cost controls and resolver observability.

---

### REST vs gRPC

Use REST/HTTP+JSON when:

- Broad client/browser interoperability matters.
- Public APIs need easy debugging/tooling.
- Human-readable payloads and standard HTTP semantics are valuable.

Use gRPC when:

- Internal service-to-service contracts are strongly typed.
- Efficient binary serialization matters.
- Streaming is important.
- Client/server code generation is useful.

Good interview answer:

> I would not choose gRPC simply because it is faster. I would choose it when the service boundary benefits from strongly typed generated contracts or streaming and all consumers can support the protocol. REST remains a strong default for external/public APIs.

---

### Polling vs SSE vs WebSocket

|     Mechanism      |                       Best fit                        |
| ------------------ | ----------------------------------------------------- |
| Polling            | Simple, low-frequency status checks.                  |
| Server-Sent Events | Server → client streaming over HTTP; one-way updates. |
| WebSocket          | Bidirectional low-latency messaging.                  |

Choose the simplest communication model that meets the update/interaction requirement.

---

## FastAPI: Interview-Ready Architecture

### Why FastAPI?

Strong answer:

> FastAPI is a good fit for Python APIs because type annotations integrate with Pydantic validation, OpenAPI documentation is generated automatically, dependency injection keeps infrastructure concerns explicit, and async endpoints work well for I/O-bound concurrency when the full dependency chain is async-compatible. I still choose sync versus async from the workload rather than assuming async automatically makes the service faster.

### Where Async Helps

Use async when the endpoint spends meaningful time waiting for async-capable I/O:

- HTTP calls
- Async database driver calls
- Object storage/network calls
- Multiple independent I/O operations that can overlap

Example:

```python
import asyncio

async def build_dashboard(client, urls):
    results = await asyncio.gather(
        *(client.get(url) for url in urls)
    )
    return results
```

This can overlap seven independent I/O waits rather than performing them sequentially.

Do **not** use async to make CPU-heavy Python work magically parallel. CPU-heavy work can block the event loop; use process workers/background compute where appropriate.

---

### Pydantic Models

Use Pydantic to define API contracts and validation boundaries.

```python
from pydantic import BaseModel, Field

class CreateUserRequest(BaseModel):
    email: str
    age: int = Field(ge=0, le=130)

class UserResponse(BaseModel):
    id: int
    email: str
```

Pydantic helps with:

- Parsing and validation
- Serialization
- Clear request/response schemas
- OpenAPI generation
- Useful validation errors

It does not replace:

- Domain/business validation
- Authorization
- Database uniqueness/foreign-key constraints
- Transactional invariants

---

### SQL Access in FastAPI with SQLAlchemy

A common synchronous pattern is one DB session per request through dependency injection.

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg://user:pass@db/app"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Endpoint:

```python
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

For write workflows:

```text
request
  ↓
validate
  ↓
start/use transaction
  ↓
write all related rows
  ↓
commit
  ↓
return
```

On failure, rollback the transaction rather than leaving partially persisted state.

For an async stack, use SQLAlchemy async sessions with an async driver; do not mix blocking DB calls into an async endpoint under the assumption that `async def` alone makes them non-blocking.

---

### Service Layer Function Example

Keep HTTP-specific concerns thin when business logic is reused/tested independently.

```python
def create_subscription(db, user_id: int, podcast_id: int):
    existing = (
        db.query(Subscription)
        .filter_by(user_id=user_id, podcast_id=podcast_id)
        .one_or_none()
    )

    if existing is not None:
        return existing

    subscription = Subscription(
        user_id=user_id,
        podcast_id=podcast_id,
    )
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    return subscription
```

In a production implementation, a database uniqueness constraint should still enforce `(user_id, podcast_id)` so two concurrent requests cannot create duplicates even if both application checks initially see no row.

---

## Mocking External Services

Suppose the application uses an injected HTTP client abstraction:

```python
class WeatherClient:
    def get_weather(self, city: str) -> dict:
        ...
```

Service:

```python
def build_forecast(city: str, client: WeatherClient) -> dict:
    data = client.get_weather(city)
    return {"city": city, "temperature": data["temperature"]}
```

Unit test:

```python
from unittest.mock import Mock

def test_build_forecast():
    client = Mock()
    client.get_weather.return_value = {"temperature": 22}

    result = build_forecast("Toronto", client)

    assert result == {"city": "Toronto", "temperature": 22}
    client.get_weather.assert_called_once_with("Toronto")
```

Strong interview rule:

> Mock unstable or expensive external boundaries, not every internal method. If the behavior being tested depends on SQL constraints or ORM integration, a real test database is often more valuable than mocking the repository layer into meaninglessness.

## Request Flow: Explain It Literally

When an interviewer asks what happens when two users call an API, avoid a vague “FastAPI handles concurrency.”

A more precise explanation:

```text
Client connection
   ↓
ASGI server accepts request
   ↓
FastAPI/Starlette routing + middleware
   ↓
auth/dependencies
   ↓
endpoint/service code
   ↓
DB / cache / downstream I/O
   ↓
response serialization
```

Multiple requests may overlap depending on worker/process/thread/event-loop configuration and whether operations block. Shared mutable state and database invariants still need explicit correctness mechanisms.

---

## API Race Condition Example

Suppose two callers try to reserve the same seat.

Unsafe pattern:

```text
SELECT status = AVAILABLE
   ↓
request A sees available
request B sees available
   ↓
both write reserved
```

Safer conditional write:

```sql
UPDATE seat
SET status = 'HELD', held_by = :user_id
WHERE id = :seat_id
  AND status = 'AVAILABLE';
```

Check affected-row count to determine which request won.

The database remains the final authority even if the API also performs a preliminary availability read.

---

## Backward-Compatible API Evolution

When one backend/framework version supports multiple client versions, avoid uncontrolled pairwise special cases.

Useful tools:

- Explicit API versioning where contract changes are intentional.
- Capability flags/feature negotiation where appropriate.
- Compatibility matrix listing supported client/server combinations.
- Contract tests derived from supported combinations.
- Deprecation window and usage monitoring.

A compatibility matrix is especially useful when multiple client and server/framework versions coexist because it turns “which combinations work?” into explicit testable data rather than scattered conditionals.

## Async FastAPI, SQL, Service Layers, and Test Doubles

This section extends the basic examples with a production-shaped async PostgreSQL flow and layered tests.

### Async SQLAlchemy Session per Request

FastAPI does not execute SQL itself. Use a database driver or ORM, obtain a short-lived session from a pool, and inject it into the route/service.

```python
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/app"

engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

SessionFactory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionFactory() as session:
        yield session
```

Production points:

- Size the application pool against pod/worker count and the database connection limit.
- Keep transactions short and always roll back failed writes.
- Use an async driver throughout an async path; blocking database calls still block the event loop.
- Keep credentials in approved secret/configuration management.
- Use Alembic or another controlled migration workflow rather than creating schemas from request paths.

### ORM Model vs API Schema

Keep persistence models separate from public API contracts.

```python
from decimal import Decimal
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import Numeric, String
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    owner_name: Mapped[str] = mapped_column(String(100), nullable=False)
    balance: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

class AccountCreate(BaseModel):
    owner_name: str = Field(min_length=1, max_length=100)
    opening_balance: Decimal = Field(ge=0, max_digits=12, decimal_places=2)

class AccountResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    owner_name: str
    balance: Decimal
```

Use `Decimal`/`NUMERIC`, not binary floating point, for money.

### Repository and Parameterized Query

```python
from sqlalchemy import select, text

async def find_account(db: AsyncSession, account_id: UUID) -> Account | None:
    result = await db.execute(
        select(Account).where(Account.id == account_id)
    )
    return result.scalar_one_or_none()

async def find_account_raw(db: AsyncSession, account_id: UUID):
    result = await db.execute(
        text(
            """
            SELECT id, owner_name, balance
            FROM accounts
            WHERE id = :account_id
            """
        ),
        {"account_id": account_id},
    )
    return result.mappings().one_or_none()
```

Never interpolate untrusted values into an SQL string. Parameterization prevents input from being interpreted as SQL syntax; authorization remains a separate requirement.

### Small Endpoint with a Service-Layer Boundary

```python
from decimal import Decimal
from typing import Annotated, Protocol
from uuid import UUID

from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()

class TransactionCreate(BaseModel):
    account_id: UUID
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    currency: str = Field(min_length=3, max_length=3)

class TransactionRepository(Protocol):
    async def create_if_absent(
        self,
        request: TransactionCreate,
        idempotency_key: str,
    ) -> dict: ...

class TransactionService:
    SUPPORTED_CURRENCIES = {"CAD", "USD"}

    def __init__(self, repository: TransactionRepository):
        self.repository = repository

    async def create(self, request, idempotency_key: str) -> dict:
        currency = request.currency.upper()
        if currency not in self.SUPPORTED_CURRENCIES:
            raise ValueError(f"unsupported currency: {currency}")

        normalized = request.model_copy(update={"currency": currency})
        return await self.repository.create_if_absent(
            normalized,
            idempotency_key,
        )

def get_transaction_service() -> TransactionService:
    raise NotImplementedError

@app.post("/transactions", status_code=status.HTTP_201_CREATED)
async def create_transaction(
    request: TransactionCreate,
    idempotency_key: Annotated[
        str,
        Header(alias="Idempotency-Key", min_length=8),
    ],
    service: Annotated[
        TransactionService,
        Depends(get_transaction_service),
    ],
):
    try:
        return await service.create(request, idempotency_key)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
```

The repository operation must enforce the idempotency key atomically, normally with a unique database constraint. A separate `SELECT` followed by `INSERT` has a race condition.

### Mock an External Async API Through Dependency Injection

Wrap an external API behind an application-owned protocol instead of calling `httpx` directly from every route.

```python
from typing import Protocol

import httpx

class FraudClient(Protocol):
    async def approve(self, account_id: UUID, amount: Decimal) -> bool: ...

class HttpFraudClient:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def approve(self, account_id: UUID, amount: Decimal) -> bool:
        response = await self.client.post(
            "/fraud/check",
            json={"account_id": str(account_id), "amount": str(amount)},
        )
        response.raise_for_status()
        return response.json()["approved"]

class FraudCheckRequest(BaseModel):
    account_id: UUID
    amount: Decimal = Field(gt=0)

def get_fraud_client() -> FraudClient:
    raise NotImplementedError

@app.post("/fraud-decisions")
async def check_fraud(
    request: FraudCheckRequest,
    fraud_client: Annotated[FraudClient, Depends(get_fraud_client)],
):
    approved = await fraud_client.approve(request.account_id, request.amount)
    return {"approved": approved}
```

Endpoint tests can replace the client dependency without a network call:

```python
from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

client = TestClient(app)

def test_transaction_uses_fraud_client():
    fraud_client = AsyncMock()
    fraud_client.approve.return_value = True

    account_id = "7a85a83e-c53e-4ca8-9616-b1de36114e07"

    app.dependency_overrides[get_fraud_client] = lambda: fraud_client
    try:
        response = client.post(
            "/fraud-decisions",
            json={"account_id": account_id, "amount": "100.00"},
        )
        assert response.status_code == 200
        assert response.json() == {"approved": True}
        fraud_client.approve.assert_awaited_once_with(
            UUID(account_id),
            Decimal("100.00"),
        )
    finally:
        app.dependency_overrides.clear()
```

Use `httpx.MockTransport` when testing the HTTP adapter itself, including path, headers, serialization, status mapping, and response parsing:

```python
async def test_http_fraud_client():
    account_id = UUID("7a85a83e-c53e-4ca8-9616-b1de36114e07")

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/fraud/check"
        return httpx.Response(200, json={"approved": True})

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(
        base_url="https://fraud-service.test",
        transport=transport,
    ) as http_client:
        fraud_client = HttpFraudClient(http_client)
        assert await fraud_client.approve(account_id, Decimal("100.00"))
```

### FastAPI Unit-Test Layers

Use different tests for different contracts:

|             Test             |                  Real pieces                  |                Replaced pieces                |
| ---------------------------- | --------------------------------------------- | --------------------------------------------- |
| Service unit test            | Business/service object                       | Repository, clock, external client            |
| Endpoint unit/component test | Routing, Pydantic, HTTP mapping, service call | Service/infrastructure dependencies           |
| Database integration test    | Repository, ORM, migrations, real test DB     | External APIs                                 |
| End-to-end test              | Deployed request path                         | Only uncontrollable third parties when needed |

Example endpoint test:

```python
from decimal import Decimal
from unittest.mock import AsyncMock

def test_create_transaction_success():
    service = AsyncMock()
    service.create.return_value = {
        "transaction_id": "txn-101",
        "status": "created",
    }
    app.dependency_overrides[get_transaction_service] = lambda: service
    account_id = "7a85a83e-c53e-4ca8-9616-b1de36114e07"

    try:
        response = client.post(
            "/transactions",
            headers={"Idempotency-Key": "request-123"},
            json={
                "account_id": account_id,
                "amount": "100.00",
                "currency": "cad",
            },
        )

        assert response.status_code == 201
        assert response.json()["status"] == "created"
        service.create.assert_awaited_once()
    finally:
        app.dependency_overrides.clear()
```

Test at least:

- Successful request and response schema
- Missing, malformed, and boundary values
- Authentication and authorization failures
- Not found and conflict/idempotency behavior
- Database rollback on failure
- External timeout, invalid JSON, and `4xx`/`5xx` mapping
- Correct dependency calls
- Concurrency-sensitive uniqueness/invariants in integration tests

Interview answer:

> I keep FastAPI routes thin and inject services, database sessions, authentication, and external clients with `Depends`. Endpoint unit tests use `TestClient` and `app.dependency_overrides`; async collaborators use `AsyncMock` or fakes. I test business rules directly at the service layer, the HTTP adapter with `MockTransport`, and persistence constraints against a disposable real database. That keeps unit tests fast without mocking away the behavior that only a real boundary can verify.
