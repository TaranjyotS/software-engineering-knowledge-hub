# Cloud, DevOps, Docker, Kubernetes & CI/CD

> **Purpose:** AWS, Azure, Terraform, Docker, Kubernetes, Git, Jenkins, GitHub Actions, CI/CD, deployment, and cloud architecture.  
> **Use this file for:** DevOps, backend platform, cloud engineering, and production deployment interviews  

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

> AWS, Azure, Terraform, Docker, Kubernetes, Git, CI/CD pipelines, deployment patterns, infrastructure, containers, and cloud architecture.
> Consolidated from the uploaded Markdown interview-prep files and reorganized by reusable topic. Source labels are retained for traceability.

### Topic Sections

1. AWS, CI/CD, Docker & Kubernetes — `Interview_Prep_Topics_and_Questions.md`
2. Git / Version Control — `ai_engineer_interview_prep_topics.md`
3. Cloud / AWS Topics — `ai_engineer_interview_prep_topics.md`
4. Kubernetes / Docker Topics — `ai_engineer_interview_prep_topics.md`
5. Azure / Terraform Deployment Question — `ai_engineer_interview_prep_topics.md`
6. CI/CD, Git, and Engineering Workflow — `deloitte_python_genai_interview_prep_topics.md`
7. Docker, Containers, Kubernetes, and Cloud — `deloitte_python_genai_interview_prep_topics.md`
8. Cloud, AWS, Kubernetes, and GenAI Deployment — `interview_questions_topics_technical_prep.md`
9. Docker, Git, and CI/CD — `interview_questions_topics_technical_prep.md`
10. Cloud, DevOps & Monitoring — `ML_AI_Systems_Interview_Prep_Handbook.md`
11. Docker & Containerization — `Interview_Topics_and_Technical_Prep.md`
12. Kubernetes & Deployment Basics — `Interview_Topics_and_Technical_Prep.md`
13. CI/CD — `Interview_Topics_and_Technical_Prep.md`
14. Cloud Platforms — `Interview_Topics_and_Technical_Prep.md`

---

### 7. AWS, CI/CD, Docker & Kubernetes

> Source: `Interview_Prep_Topics_and_Questions.md`

#### 7.1 AWS deployment methods

| Service           | Use Case                            |
| ----------------- | ----------------------------------- |
| EC2               | Full control over VM deployment     |
| ECS               | Managed Docker containers           |
| EKS               | Managed Kubernetes                  |
| Lambda            | Serverless event-driven functions   |
| Elastic Beanstalk | Simple app deployment               |
| App Runner        | Simple containerized app deployment |
| SageMaker         | ML training and model endpoints     |

---

#### 7.2 FastAPI deployment on AWS

```text
Developer
   ↓
GitHub
   ↓
CI/CD Pipeline
   ↓
Run tests
   ↓
Build Docker image
   ↓
Push to Amazon ECR
   ↓
Deploy to EC2/ECS/EKS
   ↓
Load Balancer
   ↓
Users
```

**Interview answer:**

> I would containerize the FastAPI application using Docker, push the image to Amazon ECR, and deploy it on EC2, ECS, or EKS depending on scale. I would use Jenkins or GitHub Actions for CI/CD, place an Application Load Balancer in front, store secrets in AWS Secrets Manager, and monitor using CloudWatch or Prometheus/Grafana.

---

#### 7.3 CI/CD

**Interview answer:**

> CI/CD automates software delivery. Continuous Integration ensures each code change is built, tested, and validated before merge. Continuous Deployment automates releasing validated changes to environments. A good pipeline includes linting, unit tests, integration tests, security scans, Docker image builds, deployment, smoke tests, and rollback capability.

##### CI/CD flow

```text
Git Push
   ↓
Lint + Unit Tests
   ↓
Integration Tests
   ↓
Security Scan
   ↓
Build Docker Image
   ↓
Push Image
   ↓
Deploy
   ↓
Smoke Test
   ↓
Monitor
```

---

#### 7.4 Docker

**Interview answer:**

> Docker packages an application and all dependencies into a portable container so it runs consistently across development, testing, and production environments.

##### Simple Dockerfile for FastAPI

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

#### 7.5 Kubernetes

**Interview answer:**

> Kubernetes orchestrates containers by handling scheduling, scaling, rolling updates, self-healing, service discovery, and load balancing. It is useful for running microservices reliably at scale.

Key concepts:

- Pod
- Deployment
- Service
- ConfigMap
- Secret
- Ingress
- Horizontal Pod Autoscaler
- Liveness/readiness probes

---

### 16. Git / Version Control

> Source: `ai_engineer_interview_prep_topics.md`

#### 16.1 Typical Git Workflow

```bash
git checkout -b feature/agent-api
git add .
git commit -m "Add agent response endpoint"
git push origin feature/agent-api
## Create pull request
## Code review
## Merge after approval
```

#### 16.2 Merge vs Rebase

| Merge                     | Rebase                         |
| ------------------------- | ------------------------------ |
| Preserves branch history  | Creates cleaner linear history |
| Adds merge commit         | Rewrites commits               |
| Safer for shared branches | Good for local cleanup         |

#### 16.3 Interview Line

> "I use Git for feature branches, pull requests, code reviews, version control, and collaboration. For shared branches I prefer merge, while for cleaning up local commits before a PR, rebase can be useful."

---

### 17. Cloud / AWS Topics

> Source: `ai_engineer_interview_prep_topics.md`

#### 17.1 EC2 vs Lambda

##### When to Use EC2

Use EC2 when you need:

- Long-running services
- Full control over environment
- Custom dependencies
- Persistent connections
- Background workers
- WebSockets
- Containerized services
- More networking control

##### When to Use Lambda

Use Lambda when you need:

- Short-lived event-driven tasks
- Serverless execution
- Auto-scaling without server management
- S3 triggers
- Queue processing
- Lightweight background jobs

#### 17.2 Interview Answer: Why EC2 Instead of Lambda?

> "I would choose EC2 when the application needs long-running processes, custom runtime setup, persistent connections, background workers, or more control over CPU, memory, networking, and installed dependencies. Lambda is great for short-lived event-driven tasks, but EC2 is better for continuously running services like a FastAPI backend, AI agent server, vector database worker, or LLM integration service."

#### 17.3 AWS Preparations for Scaling

For scaling a backend/AI application:

- Use EKS or ECS for containers
- Place service behind Application Load Balancer
- Configure autoscaling
- Use RDS for managed database
- Add read replicas if needed
- Use connection pooling
- Use ElastiCache/Redis for caching
- Store documents/files in S3
- Use CloudWatch for logs and metrics
- Use Secrets Manager for secrets
- Configure IAM roles properly
- Configure security groups and VPC networking
- Monitor external API limits and latency

#### 17.4 GenAI-Specific AWS Considerations

- LLM provider rate limits
- Embedding API throughput
- Vector database scaling
- Token cost monitoring
- Response streaming
- Async processing
- Background evaluation jobs
- Queue-based workloads
- Logging and audit trails

---

### 18. Kubernetes / Docker Topics

> Source: `ai_engineer_interview_prep_topics.md`

#### 18.1 What Is Kubernetes?

> "Kubernetes is a container orchestration platform used to deploy, manage, scale, and monitor containerized applications. It automates deployment, scaling, load balancing, self-healing, and rolling updates."

#### 18.2 Why Use Kubernetes?

- Auto scaling
- Load balancing
- Self-healing
- Rolling updates
- High availability
- Service discovery
- Better container management

#### 18.3 Core Kubernetes Components

| Component  | Meaning                        |
| ---------- | ------------------------------ |
| Pod        | Smallest deployable unit       |
| Deployment | Manages desired number of pods |
| Service    | Stable endpoint to reach pods  |
| Ingress    | Routes external traffic        |
| ConfigMap  | Non-secret configuration       |
| Secret     | Sensitive configuration        |
| HPA        | Horizontal Pod Autoscaler      |

#### 18.4 Docker vs Kubernetes

| Docker                               | Kubernetes                        |
| ------------------------------------ | --------------------------------- |
| Packages application into containers | Orchestrates containers           |
| Usually single-host focus            | Multi-host cluster management     |
| Builds and runs containers           | Deploys, scales, heals containers |

#### 18.5 Interview Line

> "Docker helps package the application, while Kubernetes helps deploy, scale, and manage those containers in production."

#### 18.6 What Happens When a Pod Crashes?

> "Kubernetes continuously monitors pod health. If a pod crashes, the deployment controller creates a replacement pod to maintain the desired state."

---

### 20. Azure / Terraform Deployment Question

> Source: `ai_engineer_interview_prep_topics.md`

#### 20.1 Client Question

> "I need to know Azure/Terraform experience — how did you deploy?"

#### 20.2 Safe Answer Strategy

Be truthful and avoid overstating experience.

A strong answer:

> "My primary hands-on production deployment experience has been with cloud deployments using Docker, Kubernetes, CI/CD, and infrastructure automation concepts. I have worked with Azure Database as part of backend application development and understand Terraform's Infrastructure-as-Code workflow, including declarative infrastructure definitions, state management, variables, modules, and automated provisioning.  
> Most of my production deployment experience has been on AWS-based environments, but Terraform principles are cloud-agnostic. The same workflow can be adapted to Azure resources such as resource groups, app services, container apps, Azure SQL, storage accounts, virtual networks, and Key Vault. I am comfortable working with Terraform-based Azure deployments and can quickly contribute using my cloud engineering and IaC background."

#### 20.3 Example Terraform Flow for Azure

```bash
terraform init
terraform fmt
terraform validate
terraform plan
terraform apply
```

#### 20.4 Example Terraform Structure

```text
terraform/
  main.tf
  variables.tf
  outputs.tf
  providers.tf
  environments/
    dev.tfvars
    prod.tfvars
```

#### 20.5 Example Azure Terraform Snippet

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "app_rg" {
  name     = "rg-fastapi-dev"
  location = "Canada Central"
}

resource "azurerm_storage_account" "app_storage" {
  name                     = "fastapistorageacct"
  resource_group_name      = azurerm_resource_group.app_rg.name
  location                 = azurerm_resource_group.app_rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}
```

#### 20.6 Interview Line

> "The way I think about deployment is: define infrastructure using Terraform, validate the plan, provision the resources, deploy the application through CI/CD, store secrets securely, monitor through cloud logs/metrics, and maintain changes through version control."

---

### 12. CI/CD, Git, and Engineering Workflow

> Source: `deloitte_python_genai_interview_prep_topics.md`

#### Topics to revise

- Git branching.
- Pull requests.
- Code reviews.
- CI pipelines.
- Build/test/lint/type-check stages.
- CD deployment pipelines.
- Rollbacks.
- Environment variables.
- Secrets handling.

#### Example CI pipeline stages

```text
1. Install dependencies
2. Run linting
3. Run type checks
4. Run unit tests
5. Run integration tests
6. Build Docker image
7. Scan image/security dependencies
8. Deploy to staging
9. Run smoke tests
10. Promote to production
```

#### Common interview question

##### What should a good CI/CD pipeline include?

**Answer:**

A good CI/CD pipeline should automatically run linting, formatting checks, type checks, unit tests, integration tests, security scans, Docker builds, and deployment steps. It should also support rollback, environment-specific configuration, and release visibility.

---

### 13. Docker, Containers, Kubernetes, and Cloud

> Source: `deloitte_python_genai_interview_prep_topics.md`

#### Docker topics

- Dockerfile basics.
- Images vs containers.
- Multi-stage builds.
- Environment variables.
- Volumes.
- Container networking.
- Docker Compose.

#### Example Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Kubernetes topics

- Pods.
- Deployments.
- Services.
- ConfigMaps.
- Secrets.
- Ingress.
- Horizontal scaling.
- Health checks.
- Rolling updates.

#### Cloud topics

- AWS, Azure, or GCP basics.
- Serverless vs containers.
- Managed databases.
- Object storage.
- IAM/least privilege.
- Logs and metrics.
- Infrastructure as code.

#### Common interview questions

1. Why use Docker?
2. What problem does Kubernetes solve?
3. How do you scale a Python API?
4. How do you handle secrets in cloud applications?
5. What is the difference between a container and a VM?

---


---

### 7. Cloud, AWS, Kubernetes, and GenAI Deployment

> Source: `interview_questions_topics_technical_prep.md`

#### 7.1 Deploying GenAI applications on cloud/Kubernetes

##### Typical architecture

```text
Client → API service → Retrieval layer/vector DB → LLM endpoint → Response
```

##### Components

- FastAPI/Flask backend.
- LLM orchestration layer.
- RAG ingestion workers.
- Vector database.
- Redis cache.
- Object storage.
- Secrets manager.
- Observability stack.
- CI/CD.

---

#### 7.2 Kubernetes deployment components

##### Common manifests

- Deployment.
- Service.
- Ingress.
- ConfigMap.
- Secret.
- HPA.
- Readiness/liveness probes.

##### Production concerns

- Resource requests/limits.
- Autoscaling.
- Rolling/canary deployments.
- Secrets handling.
- Observability.
- Graceful shutdown.

---

#### 7.3 AWS stack for backend/GenAI apps

##### Common services

- EKS/ECS for compute.
- ECR for images.
- S3 for document/object storage.
- RDS/Aurora for relational data.
- DynamoDB for key-value/idempotency store.
- ElastiCache Redis for caching.
- Secrets Manager for credentials.
- CloudWatch/Prometheus/Grafana for monitoring.
- API Gateway/ALB for ingress.

---

#### 7.4 Choosing DynamoDB vs RDS for idempotency

##### DynamoDB advantages

- Low-latency key-value access.
- Conditional writes.
- TTL cleanup.
- High availability.
- Scales well for high retry traffic.

##### RDS advantage

- Strong relational transactions.
- Simpler if idempotency and business operation must commit together.

##### Hybrid answer

> Use DynamoDB as a fast idempotency/replay layer, but enforce final uniqueness in RDS when order data lives there.

---

#### 7.5 Securing AWS order-create endpoint

##### Security layers

- OAuth2/OIDC JWT validation.
- Cached JWKS validation.
- Scopes such as `orders:create`.
- IAM roles for AWS resources.
- Secrets Manager with local TTL cache.
- Private subnets.
- Security groups.
- RDS Proxy/connection pooling.
- Tenant-aware authorization.

---

#### 7.6 Autoscaling compute while protecting RDS

##### Compute scaling metrics

- CPU.
- Memory.
- Request count.
- Queue depth.
- p95/p99 latency.

##### RDS protection

- RDS Proxy or PgBouncer.
- Per-pod connection limits.
- Short transactions.
- Backpressure when DB is saturated.
- Read replicas for read-heavy workloads.
- Async queues for non-critical work.

---


---

### 8. Docker, Git, and CI/CD

> Source: `interview_questions_topics_technical_prep.md`

#### 8.1 Starting and creating Docker containers

##### Basic command

```bash
docker run <image_name>
```

##### Detached mode

```bash
docker run -d --name my-container my-image
```

##### Port mapping

```bash
docker run -p 8000:8000 my-image
```

##### Container vs image

- Image: blueprint/template.
- Container: running instance of an image.

A container is created from one image, but it may communicate with containers created from other images.

---

#### 8.2 Checking Docker image size

```bash
docker images
```

Specific image inspection:

```bash
docker image inspect <image_name> --format='{{.Size}}'
```

---

#### 8.3 Debugging a crashing Docker container

##### Commands

```bash
docker ps -a
docker logs <container_id>
docker inspect <container_id>
docker stats <container_id>
docker exec -it <container_id> sh
```

##### Things to check

- Exit code.
- OOM kill.
- Restart count.
- Environment variables.
- Mounted volumes.
- Network connectivity.
- Healthcheck status.
- Resource usage.

---

#### 8.4 Dockerized CI/CD pipeline

##### Pipeline flow

```text
lint/test → build image → scan image → push registry → deploy → monitor
```

##### Best practices

- Pin dependencies.
- Use lock files.
- Run vulnerability scans.
- Store images in registry.
- Use same image across environments.
- Inject config through env vars/secrets.
- Use rolling/canary deployment.
- Keep rollback image tags.

##### Kubernetes rollback

```bash
kubectl rollout undo deployment/app
```

---

#### 8.5 Git: remove file from last commit before push

##### Keep file locally but remove from commit

```bash
git rm --cached backup.zip
git commit --amend
```

##### Add to `.gitignore`

```bash
echo "*.zip" >> .gitignore
git add .gitignore
git commit --amend
```

---

#### 8.6 Git: remove experimental files from commit history

##### If only last commit

```bash
git reset --soft HEAD~1
git restore --staged experimental_file.py
git commit -m "Clean commit without experimental files"
```

##### If across multiple commits

```bash
git rebase -i HEAD~N
```

Then edit commits and remove unwanted files.

---

#### 8.7 Git: reconciling long-lived branches after restructuring

##### Safe process

1. Create backup branch.
2. Inspect commit graph.
3. Rebase/merge one branch at a time.
4. Resolve conflicts carefully.
5. Run tests after each major resolution.
6. Use interactive rebase to clean history.
7. Cherry-pick stable commits if merging entire branch is risky.

##### Commands

```bash
git log --oneline --graph --all
git diff branch1..branch2
git rebase main
git rebase -i HEAD~N
git cherry-pick <commit_hash>
```

---

### Cloud, DevOps & Monitoring

> Source: `ML_AI_Systems_Interview_Prep_Handbook.md`

---

#### AWS Services

##### Interview Question

**What AWS services have you worked with or would use?**

##### Common Services

| Service    | Use                         |
| ---------- | --------------------------- |
| EC2        | Virtual machines            |
| S3         | Object storage              |
| Lambda     | Serverless functions        |
| IAM        | Access control              |
| CloudWatch | Logs and monitoring         |
| ECS/EKS    | Container orchestration     |
| ECR        | Container registry          |
| RDS        | Managed relational database |
| SageMaker  | ML training/deployment      |

---

#### EC2 vs Lambda

##### Interview Question

**What is the difference between EC2 and Lambda?**

##### Answer

| EC2                             | Lambda                          |
| ------------------------------- | ------------------------------- |
| Server-based                    | Serverless                      |
| You manage instance             | AWS manages runtime             |
| Good for long-running workloads | Good for event-driven workloads |
| More control                    | Less operational overhead       |

---

#### Docker

##### Interview Question

**What is Docker and why use it?**

##### Answer

Docker packages an application and its dependencies into a container so it runs consistently across environments.

##### Dockerfile Example

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

---

#### Kubernetes

##### Interview Question

**What is Kubernetes used for?**

##### Answer

Kubernetes is used to orchestrate containers at scale.

##### It Handles

- Deployment
- Scaling
- Service discovery
- Load balancing
- Self-healing
- Rolling updates
- Configuration management

---

#### CI/CD

##### Interview Question

**What is CI/CD?**

##### Answer

CI/CD automates software testing and deployment.

| Term | Meaning                        |
| ---- | ------------------------------ |
| CI   | Continuous Integration         |
| CD   | Continuous Delivery/Deployment |

##### Pipeline Example

```text
Code push
→ lint
→ unit tests
→ integration tests
→ build Docker image
→ security scan
→ deploy to staging
→ deploy to production
```

---

#### Production Monitoring

##### Interview Question

**What would you monitor in production?**

##### Answer

Monitor both application and infrastructure health.

##### Metrics

- Request latency
- Error rate
- Throughput
- CPU/memory usage
- Disk usage
- API failures
- Queue length
- Model performance
- Drift
- Token usage
- Cost

##### Tools

- Prometheus
- Grafana
- CloudWatch
- Datadog
- ELK Stack
- OpenTelemetry

---

### 10. Docker & Containerization

> Source: `Interview_Topics_and_Technical_Prep.md`

#### Likely Questions

- What is Docker?
- Why use containers?
- What is a Dockerfile?
- What is Docker Compose?
- How do you reduce Docker image size?
- How do containers help in local development?
- Difference between image and container?
- How do you pass environment variables?
- How do you debug a container?

---

#### Dockerfile Example

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

##### Interview Explanation

- Base image provides Python runtime.
- `WORKDIR` sets app directory.
- Requirements are copied first for better Docker layer caching.
- App code is copied after dependencies.
- Uvicorn runs the FastAPI app.

---

#### Docker Compose Example

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db:5432/app
      REDIS_URL: redis://redis:6379/0
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: app
    ports:
      - "5432:5432"

  redis:
    image: redis:7
    ports:
      - "6379:6379"
```

---

#### Image vs Container

| Concept   | Meaning                                           |
| --------- | ------------------------------------------------- |
| Image     | Blueprint/package containing app and dependencies |
| Container | Running instance of an image                      |

---

### 11. Kubernetes & Deployment Basics

> Source: `Interview_Topics_and_Technical_Prep.md`

#### Likely Questions

- What is Kubernetes?
- What is a pod?
- What is a deployment?
- What is a service?
- What is a config map?
- What is a secret?
- How does Kubernetes help with scaling?
- How do rolling deployments work?
- How do health checks work?

---

#### Kubernetes Deployment Example

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orders-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: orders-api
  template:
    metadata:
      labels:
        app: orders-api
    spec:
      containers:
        - name: orders-api
          image: orders-api:latest
          ports:
            - containerPort: 8000
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
```

##### Interview Explanation

- Deployment manages replicas.
- Pods run containers.
- Readiness probe decides if pod can receive traffic.
- Liveness probe restarts unhealthy containers.

---

#### Kubernetes Service Example

```yaml
apiVersion: v1
kind: Service
metadata:
  name: orders-api-service
spec:
  selector:
    app: orders-api
  ports:
    - port: 80
      targetPort: 8000
```

---


---

### 12. CI/CD

> Source: `Interview_Topics_and_Technical_Prep.md`

#### Likely Questions

- What is CI/CD?
- What steps should a CI pipeline include?
- How do you deploy safely?
- What is a rollback?
- How do you manage environment-specific configs?
- How do you ensure tests run before deployment?
- How do you handle database migrations in deployment?

---

#### Typical CI Pipeline

```text
Pull request opened
   ↓
Install dependencies
   ↓
Run linting
   ↓
Run unit tests
   ↓
Run integration tests
   ↓
Build Docker image
   ↓
Security checks
   ↓
Deploy to staging
   ↓
Manual/automatic promotion to production
```

---

#### GitHub Actions Example

```yaml
name: Python CI

on:
  pull_request:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run tests
        run: |
          pytest
```

---

#### Safe Deployment Practices

- Run automated tests before deploy
- Use staging environment
- Use feature flags for risky features
- Use rolling deployment
- Monitor errors after deployment
- Keep rollback plan ready
- Avoid manual production changes

---


---

### 13. Cloud Platforms

> Source: `Interview_Topics_and_Technical_Prep.md`

#### Likely Questions

- What cloud services have you used?
- How do you deploy a Python API?
- How do you store secrets?
- How do you monitor a cloud app?
- Difference between IaaS, PaaS, and serverless?
- How do you scale backend services?
- How do you handle environment variables?

---

#### Cloud Deployment Concepts

| Concept         | Explanation                           |
| --------------- | ------------------------------------- |
| Compute         | Runs application workloads            |
| Database        | Stores persistent data                |
| Object storage  | Stores files, logs, documents, images |
| Load balancer   | Distributes traffic                   |
| Secrets manager | Stores sensitive config               |
| Monitoring      | Tracks health, logs, metrics          |
| Auto-scaling    | Adds/removes capacity based on load   |

---

#### Environment Variables Example

```python
import os

DATABASE_URL = os.environ["DATABASE_URL"]
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
```

##### Interview Explanation

Use environment variables for config that changes by environment. Do not hardcode secrets in source code.

---
