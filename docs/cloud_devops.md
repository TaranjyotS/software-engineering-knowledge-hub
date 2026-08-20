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

> AWS, Azure, Terraform, Docker, Kubernetes, Git, CI/CD pipelines, deployment patterns, infrastructure, containers, and cloud architecture.

---

### 7. AWS, CI/CD, Docker & Kubernetes

#### 7.1 AWS deployment methods

|      Service      |              Use Case               |
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

|           Merge           |             Rebase             |
| ------------------------- | ------------------------------ |
| Preserves branch history  | Creates cleaner linear history |
| Adds merge commit         | Rewrites commits               |
| Safer for shared branches | Good for local cleanup         |

#### 16.3 Interview Line

> "I use Git for feature branches, pull requests, code reviews, version control, and collaboration. For shared branches I prefer merge, while for cleaning up local commits before a PR, rebase can be useful."

---

### 17. Cloud / AWS Topics

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

| Component  |            Meaning             |
| ---------- | ------------------------------ |
| Pod        | Smallest deployable unit       |
| Deployment | Manages desired number of pods |
| Service    | Stable endpoint to reach pods  |
| Ingress    | Routes external traffic        |
| ConfigMap  | Non-secret configuration       |
| Secret     | Sensitive configuration        |
| HPA        | Horizontal Pod Autoscaler      |

#### 18.4 Docker vs Kubernetes

Docker and Kubernetes solve complementary problems rather than competing directly.

|                  Docker                  |                               Kubernetes                               |
| ---------------------------------------- | ---------------------------------------------------------------------- |
| Builds portable OCI-compatible images    | Orchestrates containers created from those images                      |
| Runs containers on a host                | Schedules workloads across a cluster                                   |
| Provides packaging and runtime isolation | Provides scaling, self-healing, service discovery, and rollout control |
| Common for local development and CI      | Common for production workloads that need orchestration                |

Docker Compose is useful for running several related containers on one machine, such as an API, PostgreSQL, and Redis during local development. Kubernetes is justified when the workload needs cluster-level availability, horizontal scaling, controlled rollouts, service discovery, or standardized operations across many services.

Kubernetes does not require the Docker Engine runtime. Modern clusters commonly use runtimes such as `containerd`, while still running OCI-compatible images that may have been built with Docker.

#### 18.5 Interview Line

> "Docker packages an application and its dependencies into a portable container image. Kubernetes operates those containerized workloads across a cluster by handling scheduling, scaling, service discovery, health management, and rolling updates. I use Docker for packaging and Kubernetes when the operational requirements justify orchestration."

#### 18.6 What Happens When a Pod Crashes?

> "Kubernetes continuously monitors pod health. If a pod crashes, the deployment controller creates a replacement pod to maintain the desired state."

---

### 20. Azure / Terraform Deployment Question

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

### 7. Cloud, AWS, Kubernetes, and GenAI Deployment

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

### 8. Docker, Git, and CI/CD

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

---

#### AWS Services

##### Interview Question

**What AWS services have you worked with or would use?**

##### Common Services

|  Service   |             Use             |
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

|               EC2               |             Lambda              |
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

| Term |            Meaning             |
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

|  Concept  |                      Meaning                      |
| --------- | ------------------------------------------------- |
| Image     | Blueprint/package containing app and dependencies |
| Container | Running instance of an image                      |

---

### 11. Kubernetes & Deployment Basics

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

### 12. CI/CD

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

### 13. Cloud Platforms

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

|     Concept     |              Explanation              |
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

## Platform Engineering, Golden Paths & Developer Experience

Platform engineering treats the internal engineering platform as a product whose users are application developers. The goal is not to hide every infrastructure detail; it is to make the secure, observable, repeatable path the easiest path.

### Golden Paths and Paved Roads

A golden path is a supported, opinionated workflow for a common engineering task. A production service template might provide:

- Repository and application skeleton.
- Dockerfile and image-build conventions.
- Reusable Terraform modules.
- CI/CD pipeline defaults.
- Secrets integration.
- Authentication and authorization hooks.
- Security scanning and policy checks.
- Health checks and readiness/liveness probes.
- Logs, metrics, traces, dashboards, and alerts.
- Safe deployment and rollback behavior.
- Runbook and ownership metadata.

Developers should provide only the information genuinely unique to the service. The platform should encode common operational decisions once instead of making every product team rediscover them.

**Interview answer:**

> I think of platform engineering as treating developers as internal customers. A good platform provides supported golden paths for provisioning, deployment, observability, and operations so teams can move quickly without repeatedly making the same infrastructure and security decisions. The standard path should be opinionated, but there should be documented escape hatches for legitimate exceptions.

### Secure and Stable by Default

A self-service platform should make safe defaults automatic:

- Least-privilege IAM/RBAC.
- Encryption in transit and at rest.
- Managed secrets instead of secrets in source control.
- Restricted network exposure.
- Required tests and security scans before deployment.
- Standard observability and audit logging.
- Resource requests/limits and health checks.
- Controlled promotion and rollback.
- Policy-as-code for non-negotiable controls.

This reduces cognitive load and prevents safety from depending on every developer remembering every requirement manually.

### Measuring Whether the Platform Is Working

Useful platform and developer-experience metrics include:

- Time to create a new service or environment.
- Deployment frequency and deployment lead time.
- Change failure rate and mean time to recovery.
- Golden-path adoption rate.
- Number of manual infrastructure/support tickets.
- Exception or escape-hatch rate.
- Developer satisfaction and qualitative feedback.

A technically elegant platform that engineers avoid is not successful.

### Modernizing Legacy Infrastructure Incrementally

Avoid a rewrite-first approach. A safer modernization sequence is:

1. Map the current architecture, dependencies, manual changes, and major failure modes.
2. Add enough observability to establish a baseline.
3. Bring configuration and infrastructure changes under version control.
4. Convert repeatable infrastructure into reusable IaC modules.
5. Introduce safe deployment patterns and automated validation.
6. Migrate high-risk or high-toil paths incrementally.
7. Preserve compatibility and rollback paths while old and new systems coexist.

**Interview answer:**

> I would modernize incrementally rather than replace everything at once. I would first identify the highest-risk manual processes and observability gaps, establish a baseline, bring configuration under version control, introduce reusable IaC and deployment standards, and migrate in small reversible steps. The objective is to leave the system more stable and secure after every change.

### Terraform in a Production Platform

Important production Terraform practices include:

- Remote, encrypted state with restricted access.
- State locking to prevent concurrent modification.
- Small reusable modules with clear inputs and outputs.
- Versioned module releases rather than copying infrastructure definitions.
- `fmt`, `validate`, security/policy checks, and `plan` in CI.
- Human or policy approval for high-impact production changes.
- Drift detection and a preference for code-reviewed changes over manual console edits.
- Separate environment configuration without duplicating the whole codebase.
- Recovery planning for state and provider failures.

A safe pipeline is often:

```text
change → fmt/validate → security/policy checks → plan → review/approval → apply → post-change validation
```

### Eliminating Toil Rather Than Automating It Faster

Toil is repetitive, manual, automatable operational work that grows with system scale. The stronger platform response is to remove the recurring category of work:

```text
Repeated manual deployment ticket
        ↓
Identify common inputs and policy requirements
        ↓
Encode them in a supported self-service workflow
        ↓
Automated validation + audit trail + rollback
        ↓
Product team deploys safely without a platform-team ticket
```

**Interview answer:**

> I look for recurring manual work that should stop existing. If the platform team repeatedly performs the same safe provisioning or deployment task, I would turn the proven workflow into a self-service capability with guardrails rather than simply creating a faster manual checklist.

---

---

## Senior CI/CD, Containers & Deployment Interview Addendum

### Jenkins Pipeline Stages

A strong default pipeline explanation is:

```text
Checkout
   ↓
Dependency install / build
   ↓
Lint / static analysis
   ↓
Unit tests + coverage
   ↓
Security scan
   ↓
Package / Docker image build
   ↓
Integration tests
   ↓
Push artifact/image
   ↓
Deploy to environment
   ↓
Smoke / health checks
   ↓
Promotion or rollback
```

The exact stages depend on the application, but the ordering should fail cheap and deterministic checks before expensive packaging/deployment work.

#### Why CI/CD is more than automation

A useful pipeline must also provide:

- Fast, actionable failure feedback
- Reproducibility
- Clear promotion rules
- Artifact traceability
- Secrets handled outside source code
- Rollback strategy
- Deployment health verification
- Auditability

Strong interview answer:

> I think of CI/CD as a repeatable quality and delivery control, not just a Jenkinsfile. The pipeline should make failures understandable to developers, preserve artifact/version traceability, and reduce manual release risk.

---

### CI vs Continuous Delivery vs Continuous Deployment

- **Continuous Integration:** merge frequently with automated build/test/quality checks.
- **Continuous Delivery:** every passing change is kept releasable; production may still require an approval.
- **Continuous Deployment:** every passing change automatically reaches production.

Do not use “CI/CD” as if all three models are identical.

---

### Security Scanning Rollout Pattern

When introducing a new static security scanner into an existing codebase, do not immediately fail every build on every finding.

A practical rollout:

```text
Identify security gap
   ↓
Build POC on representative repositories
   ↓
Review true positives / false positives
   ↓
Set severity + confidence policy
   ↓
Agree suppressions / baselines
   ↓
Run informationally in CI
   ↓
Make high-value findings blocking
   ↓
Document local reproduction + remediation
   ↓
Tighten policy over time
```

This balances security quality with developer velocity and adoption.

For Python, Bandit is a common static-analysis tool for security-oriented source checks. The reusable lesson is the **incremental enforcement strategy**, not a specific scanner brand.

---

### Docker: What It Solves

Docker packages:

```text
application
runtime
system dependencies
configuration interface
```

into a repeatable container image.

Benefits:

- Consistent environments
- Reproducible deployment artifact
- Isolation
- Easier CI/CD promotion

Docker does **not** itself provide multi-host scheduling, autoscaling, service discovery, or cluster failover.

---

### Kubernetes: What It Adds

Kubernetes orchestrates containers across a cluster and manages desired state.

Core responsibilities:

- Scheduling pods
- Replica management
- Service discovery/networking
- Rolling deployment primitives
- Restart/replacement of failed pods
- Config/secret integration
- Autoscaling support
- Health/readiness integration

Good interview answer:

> Docker gives me a portable container image. Kubernetes manages many running instances of those images across machines and continuously reconciles the actual state toward the desired state.

---

### Pod vs Service vs Application Service

Avoid terminology confusion:

```text
Application service
= logical business capability

Kubernetes Pod
= one deployable/running group of containers

Kubernetes Service object
= stable networking abstraction/load-balancing endpoint for pods
```

These are related but not interchangeable meanings of “service.”

---

### Liveness vs Readiness

#### Liveness

Question:

> Is this process alive or irrecoverably wedged?

Failure can trigger restart.

#### Readiness

Question:

> Can this instance safely receive traffic right now?

Failure should remove it from routing without necessarily restarting it.

Example:

```text
startup/migration/warm cache not complete
→ not ready yet
→ do not route traffic

process deadlocked
→ liveness fails
→ restart
```

Do not make liveness depend on every downstream service being healthy; otherwise one dependency outage can cause a restart storm.

---

### Horizontal Scaling Requires Statelessness

If five API instances all need the same user/session/job state, do not keep the authoritative copy only in one process memory.

```text
Load Balancer
  /   |   \
A1    A2   A3
 \    |    /
  shared durable/session state
```

This allows any healthy instance to serve the next request.

---

### Autoscaling: What Signal Should Drive It?

CPU can be useful, but not every workload is CPU-bound.

Possible scaling signals:

- CPU/memory utilization
- Request rate
- Request latency
- In-flight requests
- Queue depth
- Queue **age**
- Worker utilization
- Custom business workload metric

Strong answer:

> I choose an autoscaling signal that correlates with the actual bottleneck. A queue worker may need scaling based on backlog age rather than API CPU utilization.

---

### Secure CI/CD Authentication to AWS and EC2

Separate two questions:

```text
1. How does CI/CD authenticate to AWS APIs?
2. How does the deployment mechanism reach/manage an EC2 host?
```

#### CI/CD → AWS: prefer temporary role credentials

Preferred pattern for hosted CI systems such as GitHub Actions:

```text
CI job
  ↓ OIDC identity token
AWS IAM trust policy
  ↓ AssumeRoleWithWebIdentity
AWS STS temporary credentials
  ↓
ECR / EC2 / S3 / SSM / deployment APIs
```

This avoids long-lived access keys in repository secrets.

Example GitHub Actions shape:

```yaml
permissions:
  id-token: write
  contents: read

steps:
  - uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: arn:aws:iam::123456789012:role/deploy-role
      aws-region: us-east-1

  - run: aws sts get-caller-identity
```

The IAM role should have only the deployment permissions the pipeline actually needs.

For Jenkins, strong options are:

- Run Jenkins on AWS compute with an attached IAM role/instance profile where appropriate.
- Use an identity-federation/role-assumption setup that produces temporary STS credentials.
- If static credentials are unavoidable in an older environment, keep them in Jenkins Credentials/secret storage, rotate them, scope them narrowly, and treat migration to short-lived credentials as the preferred direction.

#### CI/CD → EC2 host

Prefer AWS Systems Manager (SSM) for host management when the environment supports it:

```text
CI/CD with IAM permission
      ↓
AWS Systems Manager
      ↓
EC2 instance with SSM agent + instance role
```

This can avoid opening SSH broadly or distributing private keys. If SSH is required, store the private key in a secure credential store, restrict network access/security groups, verify host keys, and rotate credentials.

#### EC2 workload → AWS services

The application running on EC2 should normally use an **instance profile/IAM role**, not embedded `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` values.

```text
EC2 application
   ↓ instance metadata / role credentials
STS-managed temporary credentials
   ↓
S3 / SQS / Secrets Manager / other allowed AWS APIs
```

Interview answer:

> I separate pipeline identity from instance identity. The CI/CD job assumes a least-privilege IAM role and receives temporary STS credentials—OIDC is preferred for hosted CI. For managing EC2 I prefer Systems Manager when possible rather than distributing SSH keys. The EC2 workload itself gets an instance profile so application code does not contain long-lived AWS credentials.

---

### Deployment to AWS: Reusable Flow

One common containerized deployment pattern:

```text
Git commit
   ↓
CI pipeline
   ↓
tests / scans
   ↓
build image
   ↓
push image to registry
   ↓
deploy/update workload
   ↓
load balancer routes only ready instances
   ↓
metrics / logs / smoke tests
```

Possible AWS building blocks depend on architecture:

- EC2 for VM-hosted workloads
- ECS/EKS for container orchestration
- ECR for container images
- ALB/NLB for traffic distribution
- RDS for relational databases
- S3 for artifacts/object storage
- CloudWatch for AWS-native metrics/logs
- IAM roles for workload identity

Do not claim all of these are required together. Name only what the design actually uses.

---

### Safe Release Across Multiple Products/Services

When one shared change affects several consuming products, treat compatibility as a release-management problem rather than only a code-change problem.

Useful controls:

- Compatibility matrix
- Contract/integration tests
- Versioned artifacts
- Staged rollout
- Release notes
- Consumer upgrade order when required
- Feature flags where behavior can be decoupled from deployment
- Monitoring after promotion
- Rollback plan

A compatibility matrix can represent which producer/framework/server versions support which consumers rather than maintaining many undocumented one-to-one assumptions.

---

### Backward Compatibility Matrix Example

```text
             Client v1   Client v2   Client v3
Server v1       ✓           ✗           ✗
Server v2       ✓           ✓           ✗
Server v3       ✓           ✓           ✓
```

The matrix can directly drive automated contract tests:

```text
supported combination
→ expected success behavior

unsupported combination
→ explicit predictable error / upgrade requirement
```

This reduces scattered special-case logic and makes release risk visible.

---

### Deployment Failure Questions

#### What if a new release is unhealthy?

- Stop promotion.
- Remove unhealthy instances through readiness/health checks.
- Roll back to known-good artifact if necessary.
- Preserve logs/metrics/traces for diagnosis.
- Avoid changing database schema in ways that make immediate rollback impossible without a compatibility plan.

#### Blue/green vs rolling deployment?

- **Rolling:** gradually replace old instances; lower duplicate-capacity cost, but versions coexist during rollout.
- **Blue/green:** maintain old/new environments and switch traffic; fast rollback, but higher temporary capacity/cost and data/schema compatibility still matters.

#### Canary deployment?

Send a small percentage of traffic/users to the new version, evaluate health/business signals, then expand.

---

## Quick DevOps Revision Card

```text
CI vs delivery vs deployment
Pipeline: checkout → build → lint → unit → security → package → integration → deploy → smoke
Static security POC → tune → informational → blocking
Docker packages runtime; Kubernetes orchestrates replicas
Pod vs K8s Service vs logical application service
Liveness vs readiness
Stateless horizontal scaling
Autoscale on real bottleneck signal
CI/CD → AWS: OIDC/role assumption/STS temporary credentials
EC2 management: prefer SSM; EC2 workload uses instance profile
Compatibility matrix for multi-product releases
Staged/canary/rollback strategy
```
