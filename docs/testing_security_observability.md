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

The section below is merged from the previously organized topic-wise interview-prep pack so the repository keeps the detailed technical Q&A in one place.

> Pytest, code quality, QA strategy, AI QA, monitoring, logging, metrics, production reliability, incidents, runbooks, security, privacy, PII, and access control.
> Consolidated from the uploaded Markdown interview-prep files and reorganized by reusable topic. Source labels are retained for traceability.

### Topic Sections

1. Production Monitoring, Usage Tracking & Reliability — `Interview_Prep_Topics_and_Questions.md`
2. Testing, Quality Engineering & AI QA — `Interview_Prep_Topics_and_Questions.md`
3. Security for AI Applications — `ai_engineer_interview_prep_topics.md`
4. Testing, Monitoring & Continuous Improvement — `ai_engineer_interview_prep_topics.md`
5. Testing & Code Quality — `deloitte_python_genai_interview_prep_topics.md`
6. Observability & Production Monitoring — `deloitte_python_genai_interview_prep_topics.md`
7. Security, Privacy, and PII Handling — `deloitte_python_genai_interview_prep_topics.md`
8. LLM Cost, Latency, and Reliability Optimization — `deloitte_python_genai_interview_prep_topics.md`
9. API Security — `interview_prep_python_rest_fastapi_genai.md`
10. AI Production Challenges — `interview_prep_python_rest_fastapi_genai.md`
11. Production Reliability, Observability, Incidents, and Runbooks — `interview_questions_topics_technical_prep.md`
12. Security, Privacy, PII, and Access Control — `interview_questions_topics_technical_prep.md`
13. Monitoring, Logging, Reliability & Alerts — `transaction_etl_sql_data_engineering_interview_handbook.md`
14. Testing With Pytest — `Interview_Topics_and_Technical_Prep.md`
15. Monitoring, Logging & Production Support — `Interview_Topics_and_Technical_Prep.md`

---

### 6. Production Monitoring, Usage Tracking & Reliability

> Source: `Interview_Prep_Topics_and_Questions.md`

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

> Source: `Interview_Prep_Topics_and_Questions.md`

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

| Test Type   | Purpose                                       |
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

> Source: `ai_engineer_interview_prep_topics.md`

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

> Source: `ai_engineer_interview_prep_topics.md`

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

> Source: `deloitte_python_genai_interview_prep_topics.md`

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

> Source: `deloitte_python_genai_interview_prep_topics.md`

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

| Area     | Metrics                                                      |
| -------- | ------------------------------------------------------------ |
| API      | request count, error rate, p95 latency, p99 latency          |
| Database | slow queries, connection pool usage, lock waits              |
| LLM      | token count, cost, latency, model errors, fallback rate      |
| RAG      | retrieval precision, empty retrieval rate, citation accuracy |
| System   | CPU, memory, pod restarts, queue depth                       |

---

### 15. Security, Privacy, and PII Handling

> Source: `deloitte_python_genai_interview_prep_topics.md`

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

> Source: `deloitte_python_genai_interview_prep_topics.md`

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

> Source: `interview_prep_python_rest_fastapi_genai.md`

#### 10.1 How can we secure an API?

##### Strong Answer

> To secure an API, I would apply security at multiple layers: authentication, authorization, input validation, transport security, rate limiting, proper CORS, secrets management, and monitoring.

---

#### 10.2 Common API security methods

| Area                     | How to secure                              |
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

> Source: `interview_prep_python_rest_fastapi_genai.md`

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

> Source: `interview_questions_topics_technical_prep.md`

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

> Source: `interview_questions_topics_technical_prep.md`

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

> Source: `transaction_etl_sql_data_engineering_interview_handbook.md`

#### What to Monitor

| Area                     | Example Metric                              |
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

| Pattern           | Purpose                    |
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

> Source: `Interview_Topics_and_Technical_Prep.md`

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

> Source: `Interview_Topics_and_Technical_Prep.md`

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
