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

The section below is merged from the previously organized topic-wise interview-prep pack so the repository keeps the detailed technical Q&A in one place.

> Backend API design, FastAPI, Flask, REST, gRPC, GraphQL, request validation, API security, pagination, scaling APIs, and clean architecture.
> Consolidated from the uploaded Markdown interview-prep files and reorganized by reusable topic. Source labels are retained for traceability.

### Topic Sections

1. FastAPI & Backend API Design — `Interview_Prep_Topics_and_Questions.md`
2. API Integration Topics — `ai_engineer_interview_prep_topics.md`
3. FastAPI Topics — `ai_engineer_interview_prep_topics.md`
4. Scaling FastAPI Applications — `ai_engineer_interview_prep_topics.md`
5. Backend API Development — `deloitte_python_genai_interview_prep_topics.md`
6. FastAPI — `deloitte_python_genai_interview_prep_topics.md`
7. Flask — `deloitte_python_genai_interview_prep_topics.md`
8. REST, gRPC, and API Design — `deloitte_python_genai_interview_prep_topics.md`
9. Clean Architecture & Code Organization — `deloitte_python_genai_interview_prep_topics.md`
10. REST API Fundamentals — `interview_prep_python_rest_fastapi_genai.md`
11. FastAPI and Flask — `interview_prep_python_rest_fastapi_genai.md`
12. Async APIs and Concurrent Requests — `interview_prep_python_rest_fastapi_genai.md`
13. Code Review and API Fix Case Topics — `interview_questions_topics_technical_prep.md`
14. Backend Engineering & FastAPI — `ML_AI_Systems_Interview_Prep_Handbook.md`
15. Backend APIs: REST, GraphQL, FastAPI, Flask — `Interview_Topics_and_Technical_Prep.md`

---

### 5. FastAPI & Backend API Design

> Source: `Interview_Prep_Topics_and_Questions.md`

#### 5.1 What is FastAPI?

**Interview answer:**

> FastAPI is a modern high-performance Python framework for building REST APIs. It is built on Starlette for ASGI/async request handling and Pydantic for validation. It uses Python type hints to provide automatic request validation, serialization, and OpenAPI/Swagger documentation.

---

#### 5.2 Why FastAPI?

- Native async support
- High performance with ASGI
- Pydantic validation
- Automatic OpenAPI docs
- Dependency injection
- Easy testing
- Strong fit for AI APIs and microservices

---

#### 5.3 FastAPI vs Flask

| Flask                  | FastAPI                |
| ---------------------- | ---------------------- |
| WSGI                   | ASGI                   |
| Mostly sync            | Native async           |
| Manual validation      | Pydantic validation    |
| Swagger via extensions | Built-in OpenAPI       |
| Lightweight            | Better for modern APIs |

---

#### 5.4 Request flow

```text
Client
  ↓
Load Balancer / API Gateway
  ↓
FastAPI
  ↓
Middleware
  ↓
Pydantic Validation
  ↓
Business Logic
  ↓
Database / Vector DB / LLM API
  ↓
JSON Response
```

---

#### 5.5 Pydantic Example

```python
from pydantic import BaseModel


class UserRequest(BaseModel):
    name: str
    age: int
```

If `age` is not an integer, FastAPI automatically returns a validation error.

---

#### 5.6 Dependency Injection

Use for:

- Database sessions
- Authentication
- Configuration
- Logging
- Reusable services

```python
from fastapi import Depends, FastAPI

app = FastAPI()


def get_db():
    db = "database_session"
    return db


@app.get("/items")
async def get_items(db=Depends(get_db)):
    return {"db": db}
```

---

#### 5.7 FastAPI for AI Applications

**Answer:**

> FastAPI is a strong fit for AI applications because LLM calls, vector database queries, and external API calls are I/O-bound. Async endpoints allow the service to handle many concurrent requests efficiently. FastAPI also integrates naturally with Python AI libraries, Pydantic validation, Docker, Kubernetes, and CI/CD pipelines.

---

### 13. API Integration Topics

> Source: `ai_engineer_interview_prep_topics.md`

#### 13.1 REST vs GraphQL

| REST                          | GraphQL                      |
| ----------------------------- | ---------------------------- |
| Multiple endpoints            | Single endpoint              |
| Server defines response shape | Client requests exact fields |
| Simple and widely used        | Flexible for complex data    |
| Can over-fetch/under-fetch    | Reduces over-fetching        |

#### 13.2 How to Secure APIs

Mention:

- HTTPS
- JWT / OAuth
- API keys
- Rate limiting
- RBAC
- Input validation
- Request logging
- Secrets management
- CORS configuration
- Error handling without leaking details

#### 13.3 API Integration in AI Agents

An AI agent may call APIs to:

- Fetch customer details
- Retrieve order status
- Create support tickets
- Update records
- Trigger workflows
- Search databases
- Retrieve documents

#### 13.4 Strong Interview Line

> "When integrating APIs into an AI agent, I focus on authentication, permissions, input validation, error handling, timeout handling, retries, logging, and making sure the agent only has access to tools it is allowed to use."

---

### 14. FastAPI Topics

> Source: `ai_engineer_interview_prep_topics.md`

#### 14.1 What Is FastAPI?

> "FastAPI is a modern Python web framework for building APIs. It supports async endpoints, automatic documentation, Pydantic validation, dependency injection, and high performance."

#### 14.2 Dependency Injection in FastAPI

> "Dependency injection in FastAPI is used to provide reusable components such as database sessions, authentication, configuration, or service classes to endpoints using `Depends`."

##### Example

```python
from fastapi import Depends, FastAPI

app = FastAPI()

async def get_current_user():
    return {"username": "taran"}

@app.get("/profile")
async def get_profile(user=Depends(get_current_user)):
    return {"user": user}
```

#### 14.3 Benefits of Dependency Injection

- Loose coupling
- Reusable dependencies
- Cleaner code
- Better testing
- Centralized resource management
- Easier mocking
- Better separation of concerns

#### 14.4 Async Endpoints in FastAPI

> "Async endpoints help improve concurrency when the application is waiting on I/O operations like database queries, external APIs, vector database retrievals, or LLM calls."

##### Example

```python
from fastapi import FastAPI

app = FastAPI()

async def call_llm_api(query: str) -> str:
    # Simulated async external API call
    return f"Answer for: {query}"

@app.get("/agent-response")
async def agent_response(query: str):
    result = await call_llm_api(query)
    return {"answer": result}
```

#### 14.5 When to Use Async

Use async for:

- External API calls
- Database calls with async drivers
- LLM provider calls
- Vector DB retrieval
- File/network I/O
- Streaming responses

Do not expect async to improve CPU-heavy tasks by itself.

#### 14.6 FastAPI Troubleshooting

##### Step-by-Step Approach

1. Check logs and traceback
2. Validate request input
3. Check Pydantic model
4. Test with Swagger UI, Postman, or curl
5. Check dependencies
6. Check authentication/authorization
7. Check async issues such as missing `await`
8. Check database connection/session
9. Check external API failures
10. Check response model mismatch

##### Common FastAPI Issues

- 422 validation errors
- Missing required fields
- Incorrect data types
- Dependency failure
- Auth failure
- Missing `await`
- Blocking call inside async route
- DB session issue
- External API timeout
- Response model mismatch

##### Strong Interview Line

> "Most FastAPI endpoint issues come from validation errors, dependency failures, missing awaits, database/session problems, external API failures, or response model mismatches."

---

### 19. Scaling FastAPI Applications

> Source: `ai_engineer_interview_prep_topics.md`

#### 19.1 Scaling FastAPI from 5 Pods to 100 Pods

> "To scale a FastAPI application from 5 pods to 100 pods, I would use Kubernetes Horizontal Pod Autoscaler. First, I would make sure the application is stateless, containerized properly, and has health checks. Then Kubernetes can scale pods based on CPU, memory, or custom request metrics."

#### 19.2 Key Steps

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

#### 19.3 Example Kubernetes HPA

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

#### 19.4 Readiness and Liveness Probe Example

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

#### 19.5 Strong Interview Line

> "Scaling pods is easy; the real challenge is making sure the database, cache, external APIs, vector database, and LLM provider can handle the increased traffic too."

---

### 5. Backend API Development

> Source: `deloitte_python_genai_interview_prep_topics.md`

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

---

### 6. FastAPI

> Source: `deloitte_python_genai_interview_prep_topics.md`

FastAPI is a strong match for Python backend and GenAI services because it supports async endpoints, automatic OpenAPI docs, dependency injection, and Pydantic validation.

#### Topics to revise

- FastAPI routing.
- Pydantic models.
- Dependency injection.
- Request validation.
- Response models.
- Async endpoints.
- Middleware.
- Exception handlers.
- Background tasks.
- Authentication dependencies.
- Testing with `TestClient`.

---

#### Example: FastAPI endpoint

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Document QA API")


class QuestionRequest(BaseModel):
    document_id: str = Field(..., min_length=1)
    question: str = Field(..., min_length=5)


class AnswerResponse(BaseModel):
    answer: str
    confidence: float


@app.post("/ask", response_model=AnswerResponse)
def ask_question(payload: QuestionRequest) -> AnswerResponse:
    if payload.document_id != "demo-doc":
        raise HTTPException(status_code=404, detail="Document not found")

    return AnswerResponse(
        answer="This is a sample answer from the retrieval pipeline.",
        confidence=0.87,
    )
```

**Interview explanation:**

Pydantic validates request bodies automatically. FastAPI also generates API documentation and supports typed response models, which improves maintainability.

---

### 7. Flask

> Source: `deloitte_python_genai_interview_prep_topics.md`

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

| Area          | FastAPI                                      | Flask                                          |
| ------------- | -------------------------------------------- | ---------------------------------------------- |
| Async support | Built-in and modern                          | Possible, but not the main design focus        |
| Validation    | Pydantic-based                               | Usually manual or with extensions              |
| API docs      | Automatic OpenAPI                            | Requires extensions                            |
| Best fit      | Modern APIs, typed services, async workloads | Lightweight apps, simple services, legacy apps |

---

### 8. REST, gRPC, and API Design

> Source: `deloitte_python_genai_interview_prep_topics.md`

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

#### REST vs gRPC

| Area              | REST                     | gRPC                                        |
| ----------------- | ------------------------ | ------------------------------------------- |
| Transport         | HTTP/JSON                | HTTP/2 + Protocol Buffers                   |
| Human readability | High                     | Lower                                       |
| Browser support   | Easy                     | Less direct                                 |
| Performance       | Good                     | Very high                                   |
| Best for          | Public APIs, web clients | Internal microservices, low-latency systems |

#### Common interview question

##### When would you choose gRPC over REST?

**Answer:**

Use gRPC when services need strong contracts, low latency, efficient binary serialization, streaming, and internal service-to-service communication. Use REST when simplicity, broad compatibility, and public-facing API access matter more.

---

### 9. Clean Architecture & Code Organization

> Source: `deloitte_python_genai_interview_prep_topics.md`

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

> Source: `interview_prep_python_rest_fastapi_genai.md`

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

| Characteristic       | Explanation                        |
| -------------------- | ---------------------------------- |
| Stateless            | Each request is independent        |
| Resource-based       | Uses URLs like `/users`, `/orders` |
| Uses HTTP methods    | GET, POST, PUT, PATCH, DELETE      |
| Usually JSON         | Data is commonly exchanged in JSON |
| Language independent | Any language can consume REST APIs |

---

#### 7.3 Common HTTP methods

| Method | Purpose                     |
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
        "name": "Taran"
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
  "name": "Taran"
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
GET /search?name=taran
```

Response:

```json
{
  "result": "taran"
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
  "name": "Taran",
  "email": "taran@example.com"
}
```

Response:

```json
{
  "message": "User created",
  "data": {
    "name": "Taran",
    "email": "taran@example.com"
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

| GET                           | POST                         |
| ----------------------------- | ---------------------------- |
| Fetches data                  | Sends/creates/uploads data   |
| Parameters usually in URL     | Data usually in request body |
| Should not modify server data | Can modify server data       |
| Usually cacheable             | Usually not cacheable        |
| Idempotent                    | Not always idempotent        |

---

#### 7.10 Common HTTP status codes

| Code | Meaning               |
| ---- | --------------------- |
| 200  | Success               |
| 201  | Created               |
| 400  | Bad Request           |
| 401  | Unauthorized          |
| 403  | Forbidden             |
| 404  | Not Found             |
| 409  | Conflict              |
| 500  | Internal Server Error |

---

### 8. FastAPI and Flask

> Source: `interview_prep_python_rest_fastapi_genai.md`

#### 8.1 Have you worked with Flask and FastAPI?

##### Strong Answer

> Yes, I have worked with both Flask and FastAPI. Flask is a lightweight and flexible Python web framework, while FastAPI is a modern framework designed for high-performance APIs using Python type hints, async support, and automatic documentation.

---

#### 8.2 Major differences between Flask and FastAPI

| Flask                                   | FastAPI                                  |
| --------------------------------------- | ---------------------------------------- |
| Older, mature framework                 | Newer, modern API-first framework        |
| Mostly synchronous by default           | Native async/await support               |
| Manual validation usually required      | Built-in validation using Pydantic       |
| Swagger docs need extra setup           | Swagger/OpenAPI docs built in            |
| Very flexible and minimal               | More structured for API development      |
| Good for simple apps and custom control | Good for scalable, high-performance APIs |

---

##### Strong Interview Answer

> Flask gives more flexibility and is great for lightweight web apps or when we want full control over structure. FastAPI is better for modern REST APIs because it provides automatic Swagger documentation, request and response validation with Pydantic, native async support, and strong performance. I prefer FastAPI for API-first services, but Flask is still useful for simple services and quick prototypes.

---

#### 8.3 Why use FastAPI?

FastAPI is useful because it provides:

- Native async support
- Pydantic request validation
- Automatic Swagger documentation
- OpenAPI support
- Type hint-based development
- High performance
- Dependency injection
- Cleaner API development experience

---

### 9. Async APIs and Concurrent Requests

> Source: `interview_prep_python_rest_fastapi_genai.md`

#### 9.1 What is async support in FastAPI?

FastAPI supports `async` and `await` using ASGI.

This allows non-blocking request handling.

---

#### 9.2 API without async

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

#### 9.3 API with async

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

#### 9.4 Async vs sync interview answer

> The main difference is blocking versus non-blocking execution. In a synchronous API, the worker waits until the task finishes. In an async API, when the code is waiting for an I/O operation like a database call or external API call, the event loop can process other requests. Async improves concurrency and scalability for I/O-heavy workloads, especially GenAI APIs where LLM calls may take several seconds.

Important:

> Async does not automatically make CPU-heavy code faster. It mainly helps when the API spends time waiting on I/O.

---

#### 9.5 What happens when two users hit the same API at the same time?

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

#### 9.6 How to handle race conditions in APIs

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

### 15. Code Review and API Fix Case Topics

> Source: `interview_questions_topics_technical_prep.md`

#### 15.1 User API endpoint defects identified

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

#### 15.2 Which issue to fix first?

##### Highest priority options

- SQL injection vulnerability.
- Password hash leakage.

##### Reason

Security issues have the highest blast radius and can expose sensitive data or allow data compromise.

##### Suggested answer

> I would fix the security issue first, especially password hash leakage or SQL injection, because those create immediate risk beyond performance degradation.

---

#### 15.3 Corrected API implementation pattern

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

#### 15.4 One performance improvement to recommend

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

### Backend Engineering & FastAPI

> Source: `ML_AI_Systems_Interview_Prep_Handbook.md`

---

#### FastAPI

##### Interview Question

**Why use FastAPI?**

##### Answer

FastAPI is a modern Python web framework used for building APIs quickly and efficiently.

##### Benefits

- High performance
- Async support
- Pydantic validation
- Automatic OpenAPI documentation
- Easy dependency injection
- Strong typing support

##### FastAPI Example

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class PredictionRequest(BaseModel):
    text: str

class PredictionResponse(BaseModel):
    label: str
    confidence: float

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    return PredictionResponse(
        label="positive",
        confidence=0.92
    )
```

---

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

### 5. Backend APIs: REST, GraphQL, FastAPI, Flask

> Source: `Interview_Topics_and_Technical_Prep.md`

#### Likely Questions

- How do you design REST APIs?
- What is the difference between REST and GraphQL?
- What experience do you have with FastAPI?
- What experience do you have with Flask?
- How do you handle validation?
- How do you version APIs?
- How do you secure APIs?
- How do you handle pagination?
- How do you handle idempotency?
- How do you design APIs that are easy for frontend teams to consume?

---

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

---

#### REST vs GraphQL

| Topic          | REST               | GraphQL                       |
| -------------- | ------------------ | ----------------------------- |
| Data fetching  | Multiple endpoints | Single endpoint               |
| Response shape | Server-defined     | Client-defined                |
| Over-fetching  | Common             | Reduced                       |
| Caching        | Easier with HTTP   | More complex                  |
| Learning curve | Lower              | Higher                        |
| Best for       | Standard CRUD APIs | Flexible UI-driven data needs |

##### Example REST Request

```http
GET /orders/123
```

##### Example GraphQL Query

```graphql
query {
  order(id: 123) {
    id
    status
    customer {
      name
      email
    }
  }
}
```

---

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
