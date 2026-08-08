# GenAI, LLMs, Prompting, Agents, RAG & Evaluation

> **Purpose:** Generative AI concepts, prompt engineering, RAG, embeddings, vector databases, AI agents, tool calling, hallucination reduction, guardrails, and LLM evaluation.
> **Use this file for:** AI engineer, GenAI engineer, AI platform engineer, and LLM application interviews

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

> Generative AI, LLMs, prompt engineering, AI agents, tool calling, RAG, embeddings, vector databases, hallucination, guardrails, model comparison, and LLM evaluation.

### Topic Sections

1. Core GenAI & Agentic AI — `Interview_Prep_Topics_and_Questions.md`
2. RAG, Retrieval, Chunking & Vector Search — `Interview_Prep_Topics_and_Questions.md`
3. LLM Evaluation, Hallucination & Model Comparison — `Interview_Prep_Topics_and_Questions.md`
4. System Design for AI Assistants — `Interview_Prep_Topics_and_Questions.md`
5. AI Agents — `ai_engineer_interview_prep_topics.md`
6. RAG Systems — `ai_engineer_interview_prep_topics.md`
7. LLM Evaluation & Metadata — `ai_engineer_interview_prep_topics.md`
8. Prompt Engineering — `ai_engineer_interview_prep_topics.md`
9. Productionizing AI Agents — `ai_engineer_interview_prep_topics.md`
10. Current GenAI Role Explanation — `ai_engineer_interview_prep_topics.md`
11. LLM / GenAI Application Development — `deloitte_python_genai_interview_prep_topics.md`
12. Prompt Engineering & Context Construction — `deloitte_python_genai_interview_prep_topics.md`
13. RAG: Retrieval-Augmented Generation — `deloitte_python_genai_interview_prep_topics.md`
14. Embeddings & Vector Databases — `deloitte_python_genai_interview_prep_topics.md`
15. LLM Evaluation, Guardrails, and Safety — `deloitte_python_genai_interview_prep_topics.md`
16. Model Selection, Fine-Tuning, LoRA/QLoRA — `deloitte_python_genai_interview_prep_topics.md`
17. Multimodal AI Familiarity — `deloitte_python_genai_interview_prep_topics.md`
18. GenAI, ChatGPT API, and Prompt Engineering — `interview_prep_python_rest_fastapi_genai.md`
19. LLMs, RAG, Prompt Engineering, and GenAI Evaluation — `interview_questions_topics_technical_prep.md`
20. LLMs & Generative AI — `ML_AI_Systems_Interview_Prep_Handbook.md`
21. RAG: Retrieval-Augmented Generation — `ML_AI_Systems_Interview_Prep_Handbook.md`
22. AI Agents & Tool Calling — `ML_AI_Systems_Interview_Prep_Handbook.md`
23. Embeddings, Vector Databases & Indexing — `ML_AI_Systems_Interview_Prep_Handbook.md`
24. LLM Evaluation & Hallucination Reduction — `ML_AI_Systems_Interview_Prep_Handbook.md`
25. AI / LLM / GenAI Integration — `Interview_Topics_and_Technical_Prep.md`

---

### 1. Core GenAI & Agentic AI
#### 1.1 What is Generative AI?

**Interview answer:**

> Generative AI refers to AI systems that generate new content such as text, code, images, summaries, or responses based on a prompt. In the LLM context, the model predicts the most likely next tokens to generate useful language outputs.

**Examples:**

- Summarizing a document
- Writing code
- Generating a cover letter
- Creating a chatbot response
- Explaining a security alert

---

#### 1.2 What is Agentic AI?

**Interview answer:**

> Agentic AI builds on Generative AI by enabling an LLM-powered system to reason, plan, use external tools, maintain state, and execute multi-step workflows toward a goal. Unlike a regular chatbot that gives one response, an agent can decide what action to take next, call APIs, retrieve data, validate outputs, and iterate until the task is complete.

##### Agent flow

```text
User Goal
   ↓
Planner / Reasoning Layer
   ↓
Tool Selection
   ↓
External APIs / DB / Search / Vector DB
   ↓
Observation
   ↓
Next Action or Final Answer
```

---

#### 1.3 Agentic AI vs Generative AI

| Generative AI                      | Agentic AI                                     |
| ---------------------------------- | ---------------------------------------------- |
| Generates content                  | Completes tasks                                |
| Single prompt → response           | Multi-step workflow                            |
| Mostly reactive                    | Goal-driven                                    |
| Limited tool use                   | Uses APIs, databases, search, code execution   |
| Limited memory                     | Maintains state/context                        |
| Good for summarization and writing | Good for workflow automation and investigation |

**60-second answer:**

> Generative AI focuses on generating content such as text, code, images, or summaries. Agentic AI extends that by giving the system the ability to reason, plan, use tools, maintain context, and execute multi-step workflows. For example, a Generative AI model can summarize a report, while an AI agent can retrieve reports, compare them, call APIs, generate an analysis, and send the result for approval. In production, agents require stronger guardrails, monitoring, access control, and failure handling.

---

#### 1.4 What makes an AI agent production-grade?

A demo agent may simply call an LLM and return an answer. A production-grade agent needs:

- Authentication and authorization
- Tool access control
- Human-in-the-loop approval for sensitive actions
- Retry and fallback logic
- Observability and audit logging
- Cost and token tracking
- Evaluation datasets
- Prompt/version control
- Guardrails and validation
- Failure handling
- Rollback strategy

**Interview line:**

> Production AI agents are not just prompts. They are distributed systems with LLM reasoning, tools, orchestration, observability, evaluation, guardrails, and operational controls.

---

#### 1.5 Tool Calling

**Interview answer:**

> Tool calling allows an LLM or agent to invoke external functions, APIs, databases, search systems, or internal services instead of relying only on its own generated text. The model decides which tool to call, passes structured parameters, receives the result, and uses that result to continue reasoning or produce the final answer.

##### Example flow

```text
User: "Show my recent orders"
   ↓
LLM decides to call get_orders(user_id)
   ↓
Backend API queries database
   ↓
Tool returns order list
   ↓
LLM summarizes result
```

##### Tool-calling concerns

- Validate tool arguments
- Restrict allowed tools
- Avoid exposing sensitive data
- Add retries/timeouts
- Log tool calls
- Require human approval for risky actions

---

#### 1.6 Prompt Engineering

**Interview answer:**

> Prompt engineering is the process of designing instructions, context, examples, constraints, and output formats so that the LLM produces consistent, accurate, and useful responses. In production systems, prompt engineering is closely tied to context engineering, RAG, evaluation, and guardrails.

##### Good prompt components

```text
Role: You are a support assistant.
Task: Answer the user's question using only the provided context.
Context: <retrieved documents>
Rules:
- Do not invent facts.
- Cite sources.
- If context is insufficient, say you don't know.
Output format: JSON with answer and sources.
```

---

#### 1.7 RLHF

**Interview answer:**

> RLHF stands for Reinforcement Learning from Human Feedback. It improves LLM behavior using human preference data. Human reviewers compare or rate model outputs, those preferences help train a reward model, and the LLM is optimized to produce responses that better align with human expectations for helpfulness, correctness, and safety.

##### Your experience positioning

> I contributed to LLM training through RLHF by evaluating model outputs, generating high-quality preference data, identifying failure modes, and improving model behavior across coding, reasoning, safety, and instruction-following tasks.

---

### 2. RAG, Retrieval, Chunking & Vector Search
#### 2.1 What is RAG?

**Interview answer:**

> Retrieval-Augmented Generation, or RAG, combines information retrieval with LLM generation. Instead of relying only on the model's training data, the system retrieves relevant documents or chunks from a knowledge base and provides that context to the LLM before generating an answer. This improves factual accuracy, reduces hallucinations, and allows the system to use private or frequently changing enterprise data without retraining the model.

##### RAG flow

```text
User Query
   ↓
Query Embedding
   ↓
Vector Search
   ↓
Top-k Relevant Chunks
   ↓
Prompt Construction
   ↓
LLM
   ↓
Grounded Answer + Sources
```

---

#### 2.2 RAG vs Fine-Tuning

| RAG                           | Fine-tuning                          |
| ----------------------------- | ------------------------------------ |
| Best for changing knowledge   | Best for changing behavior/style     |
| Uses latest documents         | Knowledge can become stale           |
| Cheaper to update             | Requires training pipeline           |
| Good for enterprise documents | Good for domain adaptation           |
| Can cite sources              | Does not guarantee factual grounding |

**Answer:**

> If the knowledge changes frequently, I prefer RAG because documents can be updated and re-indexed without retraining the model. Fine-tuning is better when we want to change the model's style, format, behavior, or specialized task performance.

---

#### 2.3 Embeddings

**Interview answer:**

> Embeddings are dense numerical vector representations of text that capture semantic meaning. Similar concepts have vectors close to each other in vector space, which enables semantic search.

Example:

```text
"car" and "vehicle" → close vectors
"car" and "banana" → far apart vectors
```

Used for:

- Semantic search
- RAG
- Similarity matching
- Recommendations
- Clustering

---

#### 2.4 Vector Databases

Vector databases store embeddings and support similarity search.

Examples:

- FAISS
- Chroma
- Pinecone
- Weaviate
- OpenSearch Vector Search

**Interview answer:**

> A vector database stores document or chunk embeddings and allows nearest-neighbor search against a query embedding. In a RAG system, it helps retrieve the most semantically relevant chunks to ground the LLM response.

---

#### 2.5 Vector Indexing Strategies
##### Flat index

- Compares against every vector
- Highest accuracy
- Slow for large datasets
- Good for testing or small data

##### HNSW

- Graph-based approximate nearest neighbor index
- Very fast search
- High recall
- Higher memory usage
- Common for production RAG

##### IVF

- Clusters vectors and searches selected clusters
- Good for large datasets
- Lower memory than HNSW
- Recall depends on tuning

##### Product Quantization (PQ)

- Compresses vectors
- Saves memory
- Slight loss in accuracy
- Useful for very large-scale retrieval

| Index |     Speed |    Recall | Memory | Best Use               |
| ----- | --------: | --------: | -----: | ---------------------- |
| Flat  |      Slow | Excellent |   High | Small datasets/testing |
| HNSW  | Very fast | Excellent |   High | Production RAG         |
| IVF   |      Fast |      Good | Medium | Large datasets         |
| PQ    |      Fast |      Good |    Low | Billion-scale storage  |

**60-second answer:**

> For production RAG, I usually prefer HNSW because it provides strong recall and low latency. For very large datasets with memory constraints, I would consider IVF or IVF with Product Quantization. The final choice depends on the trade-off between recall, latency, memory, and indexing cost.

---

#### 2.6 Different Chunking Strategies
##### 1. Fixed-size chunking

Split by fixed token or word count.

```text
Chunk 1: tokens 1–500
Chunk 2: tokens 401–900
Chunk 3: tokens 801–1300
```

Good because it is simple, but it may split related content.

---

##### 2. Recursive chunking

Split in this order:

```text
Section → Paragraph → Sentence → Words
```

Best for preserving meaning while staying within chunk size.

---

##### 3. Sentence-based chunking

Keeps sentences intact. Useful for articles and policies.

---

##### 4. Paragraph-based chunking

Keeps full paragraphs together. Useful for documentation, manuals, and policies.

---

##### 5. Semantic chunking

Splits when the topic changes. Higher quality but more expensive.

---

##### 6. Sliding window / overlapping chunks

Uses overlap so context is not lost at boundaries.

Typical values:

- Chunk size: **300–500 tokens**
- Overlap: **50–100 tokens**

---

##### 7. Metadata-based chunking

Preserves fields such as:

- Document name
- Page number
- Section heading
- Department
- Date/version

**Interview answer:**

> For enterprise RAG, I usually prefer recursive chunking with overlap and metadata. A common starting point is 300–500 tokens with 50–100 token overlap, but I tune it based on retrieval quality, document structure, latency, and answer correctness.

---

#### 2.7 RAG Endpoint Design

A production RAG backend can expose:

| Endpoint                 | Purpose                             |
| ------------------------ | ----------------------------------- |
| `POST /upload`           | Upload document                     |
| `POST /parse`            | Extract text from uploaded document |
| `POST /index`            | Chunk, embed, and store vectors     |
| `POST /query`            | Ask a question                      |
| `POST /chat`             | Conversational RAG with memory      |
| `GET /documents`         | List indexed documents              |
| `DELETE /documents/{id}` | Delete document and embeddings      |
| `POST /reindex/{id}`     | Re-index updated document           |
| `GET /health`            | Health check                        |
| `GET /metrics`           | Monitoring metrics                  |

##### FastAPI skeleton

```python
from fastapi import FastAPI, UploadFile

app = FastAPI()

@app.post("/upload")
async def upload_document(file: UploadFile):
    return {"status": "uploaded", "filename": file.filename}

@app.post("/query")
async def query_rag(question: str):
    # embed query → retrieve chunks → build prompt → call LLM
    return {"answer": "...", "sources": []}
```

---

#### 2.8 Building a RAG System from PDFs
##### Pipeline

```text
PDFs
 ↓
Text extraction using pypdf/PyMuPDF
 ↓
OCR fallback if scanned
 ↓
Clean text
 ↓
Chunk text
 ↓
Generate embeddings
 ↓
Store in vector DB
 ↓
Retrieve top-k chunks
 ↓
Build grounded prompt
 ↓
LLM response with citations
```

##### PDF extraction example

```python
from pypdf import PdfReader


def extract_pdf_text(path: str):
    reader = PdfReader(path)
    pages = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        pages.append({
            "page": i + 1,
            "text": text
        })

    return pages
```

##### Simple chunking example

```python
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100):
    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunks.append(" ".join(words[start:end]))
        start += chunk_size - overlap

    return chunks
```

**Key point:**

> RAG quality depends heavily on parsing, chunking, metadata, retrieval, and prompt construction. A stronger model cannot fully compensate for poor context.

---

### 3. LLM Evaluation, Hallucination & Model Comparison
#### 3.1 What is LLM Evaluation?

**Interview answer:**

> LLM evaluation is the process of systematically measuring a language model's performance across correctness, factual accuracy, reasoning, instruction following, safety, groundedness, latency, cost, and user satisfaction. The goal is to ensure the model behaves reliably before and after deployment.

---

#### 3.2 What do you evaluate?

- Correctness
- Faithfulness / groundedness
- Instruction following
- Reasoning quality
- Safety
- Toxicity
- PII leakage
- Tool usage accuracy
- Latency
- Token usage
- Cost
- User satisfaction

---

#### 3.3 Offline vs Online Evaluation

| Offline Evaluation             | Online Evaluation             |
| ------------------------------ | ----------------------------- |
| Before deployment              | In production                 |
| Uses benchmark/golden datasets | Uses real user traffic        |
| Easier to reproduce            | Captures real behavior        |
| Helps compare models/prompts   | Helps detect drift/regression |

---

#### 3.4 Human vs Automated Evaluation
##### Human evaluation

Good for:

- Reasoning quality
- Helpfulness
- Safety review
- Preference comparison

##### Automated evaluation

Examples:

- LLM-as-a-judge
- RAGAS
- DeepEval
- LangSmith
- Custom scoring scripts
- BLEU/ROUGE/BERTScore for certain NLP tasks

---

#### 3.5 How to Evaluate a RAG System as a Whole

Evaluate three layers:

##### 1. Retrieval quality

Metrics:

- Precision@K
- Recall@K
- Hit Rate
- MRR
- Context precision
- Context recall

##### 2. Generation quality

Metrics:

- Correctness
- Faithfulness
- Relevance
- Completeness
- Citation accuracy
- Hallucination rate
- Instruction following

##### 3. System performance

Metrics:

- Latency
- Throughput
- Token usage
- Cost per request
- Error rate
- Availability
- User feedback

**60-second answer:**

> I evaluate a RAG system in layers. First, I measure whether the retrieval system finds the right chunks using Precision@K, Recall@K, Hit Rate, and MRR. Second, I evaluate the generated answer for correctness, faithfulness, relevance, citation accuracy, and hallucination rate. Third, I monitor production metrics like latency, cost, token usage, errors, and user feedback. This helps isolate whether failures come from retrieval, prompt construction, or the LLM.

---

#### 3.6 Hallucination

**Interview answer:**

> Hallucination occurs when an LLM generates information that is incorrect, fabricated, or unsupported while presenting it confidently as true. LLMs can hallucinate because they predict likely text rather than verifying facts against a trusted source.

##### Causes

- Missing context
- Outdated training data
- Ambiguous prompt
- Poor retrieval
- High temperature
- Weak output validation

##### Reduction strategies

- RAG with trusted documents
- Better context engineering
- Prompt constraints
- Citations
- Output validation
- Confidence thresholds
- Human review
- Retrieval evaluation
- Lower temperature for factual tasks

**Interview line:**

> Hallucinations cannot be eliminated completely, but they can be significantly reduced with grounding, validation, evaluation, and monitoring.

---

#### 3.7 BLEU and ROUGE
##### BLEU

- Precision-oriented
- Often used in machine translation
- Measures word/phrase overlap with reference output

##### ROUGE

- Recall-oriented
- Often used in summarization
- Measures how much reference content is captured

| BLEU                    | ROUGE                      |
| ----------------------- | -------------------------- |
| Precision-oriented      | Recall-oriented            |
| Translation             | Summarization              |
| Exact/near word overlap | Reference content coverage |

**Limitation:**

> BLEU and ROUGE rely heavily on lexical overlap, so they may score a semantically correct LLM answer poorly if it uses different wording. For modern LLMs, semantic evaluation, human review, groundedness, faithfulness, and LLM-as-a-judge are often more useful.

---

#### 3.8 How to say which model is better

**Strong answer:**

> I would not say one model is better based only on benchmark scores. I would define the application requirements and compare models using representative evaluation data. I would evaluate factual accuracy, reasoning quality, instruction following, faithfulness, safety, latency, cost, consistency, and tool-use performance. The best model is the one that meets the business requirements with the right balance of quality, reliability, latency, and cost.

##### Model comparison dimensions

| Dimension    | Why it matters                        |
| ------------ | ------------------------------------- |
| Accuracy     | Correctness of answer                 |
| Faithfulness | Whether answer is grounded in context |
| Reasoning    | Logical consistency                   |
| Safety       | Avoids harmful or sensitive output    |
| Latency      | User experience                       |
| Cost         | Production feasibility                |
| Consistency  | Stable behavior across runs           |
| Tool success | Agent reliability                     |

---

#### 3.9 Accuracy, Precision, Recall, F1
##### If 2 out of 5 predictions are correct

That is usually **accuracy**:

```text
Accuracy = correct predictions / total predictions
Accuracy = 2 / 5 = 40%
```

##### Precision

```text
Precision = TP / (TP + FP)
```

Of everything predicted positive, how many were actually positive?

##### Recall

```text
Recall = TP / (TP + FN)
```

Of all actual positives, how many did we catch?

##### F1

```text
F1 = 2 × Precision × Recall / (Precision + Recall)
```

Useful for imbalanced datasets.

---

### 15. System Design for AI Assistants
#### 15.1 Design a production AI assistant
##### Architecture

```text
User
 ↓
Frontend / Chat UI
 ↓
API Gateway / Load Balancer
 ↓
FastAPI Backend
 ↓
Auth + Rate Limiting
 ↓
Agent Orchestrator
 ↓             ↓             ↓
Vector DB      LLM API       External Tools
 ↓             ↓             ↓
Monitoring + Logging + Audit
 ↓
Response + Citations
```

---

#### 15.2 Core components

- Frontend UI
- FastAPI backend
- Authentication and RBAC
- Agent orchestrator
- RAG pipeline
- Vector database
- LLM provider/model layer
- Tool calling layer
- Cache
- Database
- Logging and monitoring
- Evaluation pipeline
- Guardrails

---

#### 15.3 Production concerns

- Access control
- Data privacy
- Prompt injection
- PII redaction
- Tool allowlisting
- Audit logging
- Token and cost control
- Rate limits
- Human approval
- Retry/fallback
- Evaluation and monitoring

---

#### 15.4 Security-focused AI assistant example

```text
Security Logs / Events
   ↓
Streaming / Batch Ingestion
   ↓
Context Pipeline
   ↓
Vector DB + Search Index
   ↓
Agent Orchestrator
   ↓
LLM + Security Tools
   ↓
Analyst Review / Human Approval
   ↓
Incident Summary / Recommended Action
```

Use cases:

- Threat summarization
- Log analysis
- Alert correlation
- Incident response assistance
- Playbook generation
- Root cause explanation

---

### 4. AI Agents
#### 4.1 What Is an AI Agent?

> "An AI agent is a software system that uses an LLM along with tools, memory, external APIs, decision logic, and workflows to complete tasks. Unlike a simple chatbot, an agent can take actions, call APIs, retrieve data, create tickets, check order status, and complete multi-step workflows."

#### 4.2 Chatbot vs AI Agent

| Chatbot                    | AI Agent                 |
| -------------------------- | ------------------------ |
| Mostly answers questions   | Can perform actions      |
| Usually conversation-based | Workflow/task-based      |
| Limited external access    | Can call APIs/tools      |
| Often static               | Can reason through steps |
| Usually reactive           | Can be goal-oriented     |

#### 4.3 Components of an AI Agent

- LLM
- Prompt / system instructions
- Tools / API functions
- Memory or conversation history
- Knowledge base
- Retrieval system
- Authentication and permissions
- Logging and monitoring
- Evaluation framework
- Human escalation path

#### 4.4 Example: Customer Support AI Agent

A customer support AI agent may:

1. Understand the user query
2. Retrieve relevant policy or support documentation
3. Check user account status through an API
4. Create or update a support ticket
5. Escalate to a human if confidence is low
6. Log the conversation for monitoring and evaluation

```text
User
  ↓
React/TypeScript UI
  ↓
Backend API
  ↓
Agent Orchestration
  ↓
Tools / APIs / Knowledge Base
  ↓
LLM Response
  ↓
User
```

#### 4.5 Agent Evaluation Metrics

- Task completion rate
- Conversation success rate
- Escalation rate
- Hallucination rate
- API success/failure rate
- Latency
- Token cost
- User satisfaction
- Safety issue rate

---

### 5. RAG Systems
#### 5.1 What Is RAG?

> "RAG stands for Retrieval-Augmented Generation. It allows an LLM to retrieve relevant information from an external knowledge source before generating an answer. This helps make responses more accurate, grounded, and up to date."

#### 5.2 Simple RAG Flow

```text
Documents
  ↓
Chunking
  ↓
Embeddings
  ↓
Vector Database
  ↓
User Query
  ↓
Query Embedding
  ↓
Similarity Search
  ↓
Relevant Chunks
  ↓
LLM
  ↓
Final Answer
```

#### 5.3 Interview Answer: RAG System You Worked On

> "A typical RAG system I have worked with or evaluated involves document ingestion, chunking, embedding generation, vector storage, retrieval, and LLM response generation. When the user asks a question, the system retrieves the most relevant chunks and passes them to the LLM as context. This improves accuracy and reduces hallucinations compared to relying only on the model's internal knowledge."

#### 5.4 Why Use RAG?

- Reduces hallucinations
- Improves factual grounding
- Allows domain-specific answers
- Uses up-to-date company knowledge
- Helps with compliance and traceability
- Supports citations or source references

#### 5.5 How to Improve a RAG System

> "I would improve a RAG system by tuning chunking, improving embeddings, using better retrieval strategies, adding reranking, improving prompts, and evaluating both retrieval quality and answer quality."

##### Improvement Areas

| Area       | Improvement                           |
| ---------- | ------------------------------------- |
| Chunking   | Adjust chunk size and overlap         |
| Embeddings | Use domain-suitable embedding model   |
| Retrieval  | Use hybrid search or metadata filters |
| Ranking    | Add reranking model                   |
| Prompt     | Make instructions clearer             |
| Evaluation | Measure retrieval and answer quality  |

#### 5.6 RAG Quality Metrics

Split evaluation into two parts:

##### Retrieval Quality

- Are the correct documents retrieved?
- Are retrieved chunks relevant?
- Is important context missing?

Metrics:

- Precision@K
- Recall@K
- Context relevance
- Context coverage
- Retrieval accuracy

##### Response Quality

- Is the answer correct?
- Is it grounded in retrieved context?
- Is it complete?
- Is it relevant?
- Does it hallucinate?

Metrics:

- Accuracy
- Relevance
- Completeness
- Groundedness
- Hallucination rate
- User satisfaction

#### 5.7 Strong RAG Interview Line

> "Even if the LLM is strong, poor retrieval will lead to poor answers. That is why I evaluate both retrieval quality and response quality."

---

### 6. LLM Evaluation & Metadata
#### 6.1 Simple Explanation

> "When evaluating an LLM or AI agent, I look at whether the answer is correct, useful, safe, and grounded. I also track metadata such as latency, token usage, model version, prompt version, retrieved documents, user feedback, and conversation outcome."

#### 6.2 What Metadata Would You Track?
##### Prompt Metadata

- Prompt version
- System instructions
- User query
- Few-shot examples used
- Prompt template

##### Model Metadata

- Model name/version
- Temperature
- Token usage
- Latency
- Cost per request

##### Retrieval Metadata

- Retrieved document IDs
- Similarity scores
- Number of chunks retrieved
- Source documents used
- Retrieval latency

##### User Interaction Metadata

- User feedback
- Escalation status
- Conversation success/failure
- Number of turns
- Drop-off point

#### 6.3 Simple Interview Answer

> "I track whether the model gave the correct answer, how fast it responded, how many tokens it used, whether it hallucinated, whether users were satisfied, and whether the right documents were retrieved in RAG-based flows."

#### 6.4 Metrics for LLM / Agent Evaluation

- Accuracy
- Relevance
- Groundedness
- Hallucination rate
- Latency
- Token usage
- Cost
- User satisfaction
- Conversation success rate
- Escalation rate
- Safety issue rate

#### 6.5 How Do You Know an Agent Is Improving?

> "I compare metrics before and after changes. If hallucinations decrease, conversation success increases, latency stays acceptable, and user satisfaction improves, then the agent is improving."

---

### 7. Prompt Engineering
#### 7.1 What Is Prompt Engineering?

> "Prompt engineering is the process of designing instructions, examples, constraints, and output formats to guide an LLM toward reliable and consistent responses."

#### 7.2 Prompt Engineering Techniques

- Zero-shot prompting
- Few-shot prompting
- Role-based prompting
- Structured output prompting
- Tool-calling instructions
- Guardrail instructions
- Context injection
- Output formatting
- Chain-of-thought style reasoning guidance, where appropriate

#### 7.3 Example Prompt Template

```text
You are a customer support AI assistant.

Your goal:
- Answer only using the provided company policy context.
- If the answer is not available in the context, say you do not have enough information.
- Keep the response concise and helpful.
- Escalate to a human if the issue involves billing disputes or legal complaints.

User question:
{user_question}

Retrieved context:
{retrieved_context}

Answer:
```

#### 7.4 What Is Temperature?

> "Temperature controls randomness in model responses. Lower temperature makes answers more deterministic and consistent. Higher temperature makes answers more creative but less predictable."

| Temperature | Behavior                  |
| ----------- | ------------------------- |
| 0.0 - 0.2   | Deterministic, consistent |
| 0.3 - 0.7   | Balanced                  |
| 0.8+        | Creative, more variable   |

#### 7.5 Interview Line

> "For customer support or enterprise agents, I usually prefer lower temperature because consistency and reliability matter more than creativity."

---

### 8. Productionizing AI Agents
#### 8.1 What Does It Mean to Take an Agent to Production?

> "Taking an AI agent into production means moving it from a prototype or demo into a reliable system that real users can use safely. It includes API integrations, authentication, testing, monitoring, logging, deployment, fallback handling, and continuous evaluation."

#### 8.2 Production Checklist

- Clear scope and supported workflows
- API/database integrations
- Authentication and authorization
- Secure secret management
- Simulation tests
- Edge-case testing
- Monitoring and logging
- Human escalation path
- Rate limiting
- Error handling
- Cost monitoring
- Feedback loop
- Version control
- CI/CD pipeline
- Rollback strategy

#### 8.3 Strong Interview Answer

> "First, I would define the agent's scope and supported workflows. Then I would integrate the required APIs or databases, add authentication and permissions, and test common and edge-case user journeys. Before release, I would run simulation tests and evaluate accuracy, hallucinations, latency, and failure cases. After deployment, I would monitor live conversations, review negative feedback, create issues for failures, and continuously improve prompts, retrieval, and API handling."

#### 8.4 Common Production Failure Cases

- Hallucinated response
- Wrong API called
- Missing context
- User asks unsupported question
- External API timeout
- Permission issue
- Sensitive data leakage
- High latency
- High token cost
- Retrieval failure
- Poor escalation handling

---

### 10. Current GenAI Role Explanation
#### 10.1 Simple Explanation

> "My current GenAI work focuses on LLM evaluation, prompt engineering, AI quality assessment, response analysis, and model behavior improvement. I review AI responses, identify hallucinations or weak reasoning, compare outputs, and provide structured feedback to improve accuracy, consistency, safety, and user experience."

#### 10.2 How to Connect It to AI Engineering

> "This experience helps me understand how GenAI systems behave in real-world scenarios. I have worked with evaluation criteria, edge cases, prompt strategies, and conversation flows. Now I want to apply that knowledge more directly in building and deploying AI agents end-to-end."

#### 10.3 Key Skills to Mention

- LLM evaluation
- Prompt engineering
- Response quality assessment
- Hallucination detection
- Model behavior analysis
- AI workflow assessment
- Agentic workflow evaluation
- Data quality
- Structured feedback
- Production readiness

---

### 17. LLM / GenAI Application Development
#### Topics to revise

- Hosted LLM APIs.
- Azure OpenAI.
- OpenAI.
- Anthropic.
- Prompt design.
- Context construction.
- Chaining/orchestration.
- Tool/function calling.
- RAG systems.
- Summarization.
- Classification.
- Code assistants.
- Evaluation.
- Guardrails.
- Cost and latency management.

#### Common interview questions

1. How have you worked with LLMs?
2. What is RAG?
3. How do you reduce hallucinations?
4. How do you evaluate an LLM application?
5. How do you manage token cost?
6. What are guardrails?
7. What is prompt engineering?
8. What is context construction?
9. How do you monitor LLM applications in production?

---

#### Example: Simple LLM wrapper pattern

```python
from dataclasses import dataclass


@dataclass
class LLMResponse:
    text: str
    model: str
    prompt_tokens: int
    completion_tokens: int


class LLMClient:
    def __init__(self, provider: str, model: str) -> None:
        self.provider = provider
        self.model = model

    def generate(self, prompt: str) -> LLMResponse:
        # In real code, call provider SDK/API here.
        return LLMResponse(
            text="Sample generated answer",
            model=self.model,
            prompt_tokens=len(prompt.split()),
            completion_tokens=10,
        )
```

**Interview explanation:**

Wrapping LLM providers behind an internal interface makes it easier to switch providers, add retries, track cost, implement fallback routing, and standardize logging.

---

### 18. Prompt Engineering & Context Construction
#### Prompt engineering topics

- Clear instructions.
- Role/context setting.
- Constraints.
- Examples/few-shot prompting.
- Output format control.
- Chain-of-thought alternatives such as concise reasoning summaries.
- Prompt versioning.
- Prompt testing.

#### Context construction topics

- Selecting relevant retrieved chunks.
- Avoiding irrelevant context.
- Managing token limits.
- Ordering documents by relevance.
- Adding metadata.
- Separating system, developer, and user instructions.

#### Example prompt template

```text
You are a technical assistant. Answer the user's question using only the provided context.

Context:
{retrieved_context}

Question:
{question}

Rules:
- If the context does not contain the answer, say you do not know.
- Do not invent facts.
- Cite the document section used.
- Keep the answer concise.
```

#### Common interview question
##### How do you reduce hallucinations using prompt design?

**Answer:**

I would ground the model with retrieved context, explicitly instruct it to answer only from the provided context, require it to say when information is missing, add citations or source references, and evaluate outputs against expected answers. Prompting helps, but it should be combined with retrieval quality, guardrails, and monitoring.

---

### 19. RAG: Retrieval-Augmented Generation

RAG is one of the most important technical areas for this role.

#### RAG pipeline

```text
Documents
   ↓
Ingestion
   ↓
Parsing / Cleaning
   ↓
Chunking
   ↓
Embedding Generation
   ↓
Vector Database
   ↓
Retriever
   ↓
Prompt Construction
   ↓
LLM Generation
   ↓
Evaluation / Monitoring
```

#### Topics to revise

- Document ingestion.
- Chunking strategies.
- Embeddings.
- Vector search.
- Hybrid search.
- Metadata filtering.
- Reranking.
- Prompt construction.
- Citation generation.
- Evaluation.
- Monitoring.

---

#### Example: Simple RAG pseudocode

```python
class RAGService:
    def __init__(self, vector_store, llm_client) -> None:
        self.vector_store = vector_store
        self.llm_client = llm_client

    def answer(self, question: str) -> str:
        chunks = self.vector_store.search(query=question, top_k=5)
        context = "\n\n".join(chunk.text for chunk in chunks)

        prompt = f"""
        Answer the question using only this context.

        Context:
        {context}

        Question:
        {question}
        """

        return self.llm_client.generate(prompt).text
```

---

#### Chunking strategies

| Strategy                 | Use case                                           |
| ------------------------ | -------------------------------------------------- |
| Fixed-size chunks        | Simple documents, fast baseline                    |
| Sliding window           | Preserves context across chunk boundaries          |
| Semantic chunking        | Better for topic-based documents                   |
| Structure-aware chunking | PDFs, Markdown, HTML, legal/financial docs         |
| Hierarchical chunking    | Long documents where section-level retrieval helps |

#### Common interview question
##### How would you build a RAG system?

**Answer:**

I would design an ingestion pipeline to parse and clean documents, split them into meaningful chunks, generate embeddings, store them in a vector database with metadata, retrieve relevant chunks at query time, optionally rerank the results, construct a grounded prompt, call the LLM, return the answer with citations, and monitor retrieval quality, hallucination rate, latency, and cost.

---

### 20. Embeddings & Vector Databases
#### Embeddings

Embeddings are numerical representations of text that capture semantic meaning. Similar text should have similar vectors.

#### Vector databases mentioned or relevant

- FAISS.
- pgvector.
- Pinecone.
- Other managed vector stores.

#### Topics to revise

- Cosine similarity.
- Approximate nearest neighbor search.
- Embedding model selection.
- Metadata filtering.
- Hybrid search.
- Reranking.
- Vector index refresh.
- Embedding drift.

#### Example: Cosine similarity concept

```python
import numpy as np


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
```

#### Common interview questions

1. What are embeddings?
2. What is a vector database?
3. What is semantic search?
4. What is hybrid search?
5. How do you choose chunk size?
6. How do you evaluate retrieval quality?

---

### 21. LLM Evaluation, Guardrails, and Safety
#### Evaluation topics

- Accuracy.
- Relevance.
- Completeness.
- Faithfulness/groundedness.
- Hallucination rate.
- Toxicity/safety.
- Instruction following.
- Human-in-the-loop review.
- Automated evaluation.
- Regression testing for prompts.

#### Guardrails topics

- Input validation.
- Output validation.
- Policy filters.
- PII redaction.
- Prompt injection detection.
- Grounding requirements.
- Safe fallback responses.
- Human escalation.

#### Example LLM evaluation checklist

```text
For each generated answer:
1. Is it grounded in retrieved context?
2. Does it answer the actual question?
3. Is any unsupported claim present?
4. Is sensitive information exposed?
5. Is the tone appropriate?
6. Is the output format correct?
7. Does it include citations where required?
```

#### Common interview question
##### How would you evaluate a RAG system?

**Answer:**

I would evaluate both retrieval and generation. For retrieval, I would measure whether the correct documents or chunks appear in the top-k results. For generation, I would measure groundedness, factual accuracy, answer relevance, completeness, hallucination rate, and user satisfaction. I would use a mix of automated metrics, curated test sets, and human review.

---

### 23. Model Selection, Fine-Tuning, LoRA/QLoRA
#### Model selection topics

- Quality.
- Latency.
- Cost.
- Context window.
- Compliance requirements.
- Data residency.
- Provider reliability.
- Task type.

#### Fine-tuning topics

- When fine-tuning is useful.
- When RAG is better.
- Dataset quality.
- Evaluation before/after tuning.
- Overfitting risk.

#### LoRA / QLoRA

LoRA and QLoRA are parameter-efficient fine-tuning techniques used to adapt models without updating all model parameters.

#### Common interview question
##### When would you use RAG vs fine-tuning?

**Answer:**

I would use RAG when the model needs access to changing or private knowledge, such as internal documents or policies. I would consider fine-tuning when the model needs to learn a specific style, format, domain behavior, or task pattern that cannot be solved well through prompting and retrieval alone.

---

### 24. Multimodal AI Familiarity

The role mentions familiarity with models that can handle text, images, or structured data.

#### Topics to revise

- Text + image models.
- OCR/document understanding.
- Table extraction.
- Structured data reasoning.
- Multimodal prompt design.
- Safety concerns for images/documents.

#### Possible interview question
##### How would multimodal AI be useful in business applications?

**Answer:**

Multimodal AI can help process documents, screenshots, forms, invoices, charts, and images. For example, it can extract information from PDFs, summarize visual reports, classify document types, or support workflows where users upload screenshots or scanned files.

---

### 11. GenAI, ChatGPT API, and Prompt Engineering
#### 11.1 What is the ChatGPT API?
##### Answer

The ChatGPT API allows developers to integrate large language model capabilities into applications.

Instead of using ChatGPT through a website, applications can send prompts programmatically from:

- Web apps
- Mobile apps
- Backend services
- Automation tools
- Enterprise systems

The API receives input, processes it using a language model, and returns a generated response.

---

#### 11.2 Simple ChatGPT API flow

```text
User/Application
      ↓
Backend API
      ↓
ChatGPT / LLM API
      ↓
Generated Response
      ↓
Application UI
```

---

#### 11.3 Common use cases of ChatGPT API

- Chatbots
- Resume analysis
- Cover letter generation
- Document summarization
- Code assistance
- Customer support automation
- Search assistants
- Content generation
- Workflow automation

---

#### 11.4 Pros of ChatGPT API

| Advantage                       | Explanation                           |
| ------------------------------- | ------------------------------------- |
| Easy integration                | Can be used from backend services     |
| Powerful language understanding | Handles natural language well         |
| Flexible                        | Useful across many domains            |
| Saves development time          | No need to train a model from scratch |
| Scalable                        | Can support many AI features          |
| Useful for automation           | Helps automate repetitive text tasks  |

---

#### 11.5 Cons of ChatGPT API

| Limitation            | Explanation                                        |
| --------------------- | -------------------------------------------------- |
| Hallucinations        | Model can generate confident but incorrect answers |
| Cost                  | Token usage can become expensive                   |
| Latency               | LLM responses can take seconds                     |
| Data privacy concerns | Sensitive data must be handled carefully           |
| Output inconsistency  | Same prompt can produce slightly different answers |
| Dependency risk       | Application depends on external model/provider     |
| Context limits        | Large documents may exceed context size            |

---

#### 11.6 What is prompt engineering?
##### Answer

Prompt engineering is the process of designing prompts to get accurate, relevant, structured, and consistent outputs from an AI model.

It includes:

- Clear instructions
- Context
- Examples
- Output format
- Constraints
- Tone/style guidance
- Validation rules

---

#### 11.7 How do you know if a prompt is good?
##### Strong Interview Answer

> A good prompt is one that consistently produces accurate, relevant, and structured outputs aligned with the intended objective. I do not judge a prompt by a single response; I judge it based on repeatability, clarity, and output quality across multiple test cases.

---

#### 11.8 Criteria for a good prompt
##### 1. Clarity

Bad prompt:

```text
Write about Python.
```

Good prompt:

```text
Explain Python multithreading in less than 200 words with one real-world example.
```

---

##### 2. Specificity

Bad prompt:

```text
Improve my resume.
```

Good prompt:

```text
Optimize my resume for a Senior Python Developer role focusing on FastAPI, AWS, and GenAI while maintaining a 2-page limit.
```

---

##### 3. Output structure

Good prompt:

```text
Return the answer as JSON with fields:
- score
- strengths
- weaknesses
- recommendations
```

---

##### 4. Hallucination control

Good prompt:

```text
Use only the information provided in the resume and job description.
Do not invent experience, skills, companies, or projects.
```

---

##### 5. Consistency

A good prompt should produce similar quality outputs across multiple runs and multiple test cases.

---

##### 6. Business alignment

A prompt is good if it solves the intended business problem.

Examples:

- Resume AI: better resume-job alignment
- Chatbot: accurate customer answers
- RAG system: grounded responses
- Support bot: fewer escalations

---

### 13. LLMs, RAG, Prompt Engineering, and GenAI Evaluation
#### 13.1 LLM model selection
##### Models discussed generally

- GPT-style models.
- Claude-style models.
- LLaMA/open-source models.
- Gemini-style models.
- Smaller/mini models.
- Embedding models.

##### Selection criteria

- Accuracy/reasoning.
- Latency.
- Cost.
- Context window.
- Data privacy.
- Deployment control.
- Fine-tuning/customization.
- Ecosystem/integration.

##### Interview wording

> I choose the model based on use case constraints, not popularity. The main trade-offs are accuracy, latency, cost, privacy, and deployment control.

---

#### 13.2 Claude-style model use cases
##### Strengths

- Long-context document analysis.
- Safer/controlled outputs.
- Structured summarization.
- Enterprise workflows.

##### When to use

- Large document processing.
- Compliance-heavy tasks.
- Internal knowledge assistants.

---

#### 13.3 Why use RAG?
##### RAG solves

- Hallucinations.
- Need for private enterprise data.
- Need for up-to-date information.
- Need for traceability/auditability.
- Avoiding retraining for every knowledge update.

##### One-line answer

> RAG grounds the model in retrieved trusted context before generation.

##### Banking/regulated style answer

> In regulated domains, RAG is important because answers must be grounded, traceable, and auditable instead of relying on pure model memory.

---

#### 13.4 RAG evaluation
##### Evaluate retrieval separately

- Did we retrieve the right chunks?
- Top-k relevance.
- Context precision/recall.

##### Evaluate generation separately

- Correctness.
- Groundedness.
- Completeness.
- Hallucination rate.
- Citation/source accuracy.

---

#### 13.5 Prompt engineering
##### Effective prompt structure

1. Clear task.
2. Relevant context.
3. Constraints.
4. Output format.
5. Examples/few-shot if needed.
6. Safety instructions.
7. Evaluation/iteration.

##### Example

```text
You are a risk analyst.
Analyze the following transaction data.
Use only the provided data.
If information is missing, say "Insufficient information".
Return JSON with risk_level and reason.
```

---

#### 13.6 Prompt versioning
##### Production principle

> Treat prompts like code: versioned, tested, deployed, monitored, and rollbackable.

##### Track

- Prompt version.
- Model version.
- Retrieval config.
- Temperature/top_p.
- Dataset used.
- Evaluation metrics.
- Latency/cost.

---

#### 13.7 MLflow for prompt/model experiments
##### What to log

- Prompt version.
- Model version.
- Parameters.
- Evaluation metrics.
- Latency.
- Token usage/cost.
- Sample outputs.
- Error cases.

##### Best practice

Use Git/config for source control and MLflow for experiment tracking.

---

#### 13.8 LLM evaluation and factual accuracy
##### Criteria

- Factual correctness.
- Groundedness.
- Relevance.
- Completeness.
- Consistency.
- Safety/compliance.
- Latency/cost.

##### Consistency and objectivity

- Fixed golden dataset.
- Structured scoring rubrics.
- Blind comparisons when possible.
- Automated + human evaluation.
- Versioned prompts/models.

---

#### 13.9 Stabilizing AI systems with regression tests
##### Golden evaluation set

Include:

- Common prompts.
- Edge cases.
- Known failures.
- Risky compliance/finance cases.
- Expected behaviors.

##### Release gate

Block deployment if:

- Correctness drops.
- Hallucination rises.
- Groundedness falls.
- Latency/cost exceeds threshold.

---

### LLMs & Generative AI

---

#### What Is a Large Language Model?
##### Interview Question

**What is an LLM?**

##### Answer

A Large Language Model is a deep learning model trained on large amounts of text to understand and generate human-like language. Most modern LLMs are based on the Transformer architecture.

##### Common Capabilities

- Text generation
- Summarization
- Question answering
- Code generation
- Classification
- Reasoning assistance
- Information extraction

---

#### Transformers
##### Interview Question

**Why are Transformers important in modern AI?**

##### Answer

Transformers use self-attention to understand relationships between tokens in a sequence. This allows them to process context more effectively than older architectures like RNNs.

##### Key Concepts

- Tokenization
- Embeddings
- Self-attention
- Multi-head attention
- Positional encoding
- Feed-forward layers

---

#### RLHF
##### Interview Question

**Explain RLHF.**

##### Answer

RLHF stands for **Reinforcement Learning from Human Feedback**. It is used to align model outputs with human preferences.

##### Typical RLHF Pipeline

1. Pretrain a base model
2. Collect human preference data
3. Train a reward model
4. Fine-tune the model using reinforcement learning
5. Evaluate output quality and safety

##### Strong Sample Answer

```text
RLHF is a technique used to improve the behavior of language models using human feedback. Instead of only training on next-token prediction, the model is further optimized based on human preferences, such as helpfulness, correctness, clarity, and safety.
```

---

#### Prompt Engineering
##### Interview Question

**What makes a good prompt?**

##### Answer

A good prompt is clear, specific, contextual, and testable.

##### Good Prompt Characteristics

| Characteristic      | Meaning                       |
| ------------------- | ----------------------------- |
| Clear goal          | The model knows what to do    |
| Context             | Provides necessary background |
| Constraints         | Defines boundaries            |
| Output format       | Specifies structure           |
| Examples            | Shows expected behavior       |
| Evaluation criteria | Makes quality measurable      |

##### Example

Weak prompt:

```text
Summarize this.
```

Better prompt:

```text
Summarize the following technical incident report in 5 bullet points. Focus on root cause, customer impact, mitigation, long-term fix, and unresolved risks. Avoid adding assumptions not supported by the text.
```

---

#### Prompt Orchestration
##### Interview Question

**What is prompt orchestration?**

##### Answer

Prompt orchestration is the process of coordinating multiple prompts, tools, memory, retrieved context, and intermediate reasoning steps to complete a complex task.

##### Example Workflow

```text
User query
→ intent classification
→ retrieval
→ prompt construction
→ tool call if needed
→ response generation
→ validation
→ final answer
```

---

### RAG: Retrieval-Augmented Generation

---

#### What Is RAG?
##### Interview Question

**Explain RAG.**

##### Answer

RAG stands for **Retrieval-Augmented Generation**. It combines search/retrieval with LLM generation.

Instead of relying only on the model's internal knowledge, a RAG system retrieves relevant external context and gives that context to the model before generation.

##### RAG Pipeline

```text
Documents
→ chunking
→ embeddings
→ vector database
→ user query
→ query embedding
→ similarity search
→ retrieve top-k chunks
→ prompt with context
→ LLM response
```

---

#### Why Use RAG?
##### Benefits

- Reduces hallucination
- Adds current knowledge
- Supports enterprise/private data
- Avoids expensive full model fine-tuning
- Improves traceability through sources

---

#### RAG Code Example

```python
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

documents = [
    "Python is commonly used for machine learning.",
    "FastAPI is a modern Python web framework.",
    "Vector databases store embeddings for similarity search."
]

model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(documents)
embeddings = np.array(embeddings).astype("float32")

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

query = "What is used for similarity search?"
query_embedding = model.encode([query]).astype("float32")

distances, indices = index.search(query_embedding, k=2)

for idx in indices[0]:
    print(documents[idx])
```

---

#### Chunking Strategies
##### Interview Question

**What are different ways to chunk documents for RAG?**

##### Types of Chunking

| Strategy            | Description                    | Best For            |
| ------------------- | ------------------------------ | ------------------- |
| Fixed-size chunking | Split by token/character count | Simple documents    |
| Sliding window      | Overlapping chunks             | Preserving context  |
| Sentence-based      | Split by sentence boundaries   | Clean text          |
| Paragraph-based     | Split by paragraphs            | Reports/articles    |
| Semantic chunking   | Split by topic meaning         | Complex documents   |
| Structure-aware     | Split by headings/sections     | PDFs, manuals, docs |

##### Example

```python
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks

sample_text = "A" * 2000
chunks = chunk_text(sample_text)

print(len(chunks))
```

---

#### RAG Evaluation
##### Interview Question

**How do you evaluate a RAG system as a whole?**

##### Evaluation Areas

| Area               | Question                                       |
| ------------------ | ---------------------------------------------- |
| Retrieval quality  | Did we retrieve the right context?             |
| Generation quality | Did the answer use the context correctly?      |
| Faithfulness       | Is the answer grounded in retrieved documents? |
| Relevance          | Does the answer address the user query?        |
| Completeness       | Is anything important missing?                 |
| Latency            | Is the system fast enough?                     |
| Cost               | Are token and infrastructure costs acceptable? |

##### Useful Metrics

- Recall@K
- Precision@K
- MRR
- NDCG
- Faithfulness score
- Answer relevance
- Context relevance
- Hallucination rate

---

### AI Agents & Tool Calling

---

#### What Is an AI Agent?
##### Interview Question

**What is an AI agent?**

##### Answer

An AI agent is an LLM-powered system that can plan steps, use tools, observe results, and iterate toward completing a goal.

##### Agent Workflow

```text
User goal
→ planning
→ tool selection
→ tool execution
→ observation
→ reasoning
→ final response
```

---

#### Agent vs Generative AI
##### Interview Question

**What is the difference between Agentic AI and Generative AI?**

##### Answer

| Generative AI                       | Agentic AI                                      |
| ----------------------------------- | ----------------------------------------------- |
| Generates content                   | Takes actions toward a goal                     |
| Usually single-turn or prompt-based | Multi-step workflow                             |
| Produces text/images/code           | Uses tools/APIs/systems                         |
| Example: summarize document         | Example: investigate incident and create report |

##### Strong Answer

```text
Generative AI produces outputs such as text, code, or summaries. Agentic AI goes further by planning, calling tools, checking results, and iterating until it completes a task.
```

---

#### Tool Calling
##### Interview Question

**What is tool calling in LLM systems?**

##### Answer

Tool calling allows an LLM to call external functions, APIs, databases, or services when it needs information or actions beyond text generation.

##### Example Tool Calling Flow

```text
User: What is the status of order 123?
LLM identifies required tool: get_order_status(order_id=123)
Tool returns data
LLM summarizes answer to user
```

##### Python-Style Tool Example

```python
def get_order_status(order_id: str) -> dict:
    return {
        "order_id": order_id,
        "status": "shipped",
        "estimated_delivery": "2026-07-05"
    }

def agent_response(order_id: str) -> str:
    status = get_order_status(order_id)
    return (
        f"Order {status['order_id']} is {status['status']} "
        f"and is expected by {status['estimated_delivery']}."
    )

print(agent_response("123"))
```

---

### Embeddings, Vector Databases & Indexing

---

#### Embeddings
##### Interview Question

**What is an embedding?**

##### Answer

An embedding is a numerical vector representation of data such as text, images, or audio. It captures semantic meaning so similar items are close together in vector space.

##### Example

```text
"car" and "vehicle" should have similar embeddings.
"car" and "banana" should be farther apart.
```

---

#### Vector Databases
##### Interview Question

**Why use a vector database?**

##### Answer

A vector database stores embeddings and supports similarity search. It is commonly used in RAG systems and recommendation systems.

##### Examples

- FAISS
- ChromaDB
- Pinecone
- Weaviate
- Milvus
- Qdrant

---

#### Similarity Search
##### Common Similarity Metrics

| Metric             | Use                           |
| ------------------ | ----------------------------- |
| Cosine similarity  | Measures angle/direction      |
| Dot product        | Common in embedding retrieval |
| Euclidean distance | Measures direct distance      |

##### Simple Cosine Similarity Example

```python
import numpy as np

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

vector_1 = [1, 2, 3]
vector_2 = [1, 2, 4]

print(cosine_similarity(vector_1, vector_2))
```

---

#### Indexing Strategies
##### Interview Question

**What are indexing strategies for vector search?**

##### Answer

Indexing strategies improve retrieval speed and scalability.

| Strategy      | Description                                     |
| ------------- | ----------------------------------------------- |
| Flat index    | Exact search, slower at scale                   |
| HNSW          | Graph-based approximate nearest neighbor search |
| IVF           | Clusters vectors before search                  |
| PQ            | Compresses vectors to reduce memory             |
| Hybrid search | Combines keyword + vector search                |

##### Strong Answer

```text
For small datasets, exact search may be enough. For large-scale systems, approximate nearest neighbor indexes like HNSW or IVF are better because they reduce latency while maintaining high recall.
```

---

### LLM Evaluation & Hallucination Reduction

---

#### What Is Hallucination?
##### Interview Question

**What is hallucination in LLMs?**

##### Answer

Hallucination happens when an LLM generates information that sounds confident but is false, unsupported, or not grounded in the provided context.

---

#### How to Reduce Hallucinations
##### Techniques

- Use RAG with trusted sources
- Require citations or source references
- Add instruction to avoid unsupported claims
- Use validation checks
- Use structured outputs
- Use retrieval confidence thresholds
- Use human review for high-risk cases
- Evaluate outputs against ground truth

##### Example Prompt Instruction

```text
Answer only using the provided context. If the context does not contain the answer, say: "I do not have enough information to answer."
```

---

#### LLM Evaluation
##### Interview Question

**How do you evaluate an LLM system?**

##### Evaluation Dimensions

| Dimension    | Meaning                               |
| ------------ | ------------------------------------- |
| Accuracy     | Is the answer correct?                |
| Relevance    | Does it answer the question?          |
| Faithfulness | Is it grounded in context?            |
| Completeness | Does it cover necessary details?      |
| Safety       | Does it avoid harmful output?         |
| Consistency  | Similar inputs produce stable outputs |
| Latency      | Response time                         |
| Cost         | Token and infrastructure cost         |

##### Evaluation Methods

- Human evaluation
- Golden test sets
- LLM-as-judge
- Automated metrics
- A/B testing
- Regression testing

---

#### BLEU and ROUGE
##### Interview Question

**What are BLEU and ROUGE?**

##### Answer

BLEU and ROUGE are text evaluation metrics.

| Metric | Common Use          |
| ------ | ------------------- |
| BLEU   | Machine translation |
| ROUGE  | Summarization       |

##### BLEU

BLEU measures n-gram overlap between generated text and reference text.

##### ROUGE

ROUGE measures overlap, recall, and similarity between generated summaries and reference summaries.

##### Important Limitation

```text
BLEU and ROUGE can be useful, but they do not always capture semantic correctness, factuality, or usefulness. For LLM applications, human evaluation and task-specific metrics are often needed.
```

---

### 8. AI / LLM / GenAI Integration
#### Likely Questions

- What is your experience with LLMs?
- Have you worked with OpenAI or Claude?
- How do you integrate AI into a production workflow?
- What is prompt engineering?
- What is hallucination?
- How do you reduce hallucinations?
- What is RAG?
- What is structured output?
- How do you evaluate LLM responses?
- How do you use AI tools while maintaining code quality?
- Difference between ML research and AI product integration?
- How do you secure AI features?

---

#### How to Explain Your AI Experience

> I have worked with LLM evaluation, prompt-based workflows, model output analysis, and AI quality assessment. My interest is not only in evaluating models, but in building software systems that integrate AI into practical workflows.

---

#### Prompt Engineering
##### Good Prompt Structure

```text
You are an assistant helping summarize customer orders.

Task:
Summarize the order issue in 3 bullet points.

Rules:
- Do not invent missing information.
- If the customer did not provide a shipping address, say "shipping address not provided".
- Keep the summary under 80 words.

Input:
{customer_message}
```

##### Why This Is Good

- Defines role
- Gives a specific task
- Adds constraints
- Defines output style
- Reduces hallucination

---

#### Structured Output Example

```python
from pydantic import BaseModel
from typing import Literal


class OrderIssue(BaseModel):
    issue_type: Literal["shipping_delay", "payment_issue", "return_request", "other"]
    urgency: Literal["low", "medium", "high"]
    summary: str
```

##### Interview Explanation

Structured outputs help because:

- Backend services need predictable formats.
- JSON is easier to validate.
- Pydantic can reject invalid responses.
- Downstream systems can safely consume the result.

---

#### LLM Integration Pseudocode

```python
def classify_customer_message(message: str) -> OrderIssue:
    prompt = build_prompt(message)

    response = llm_client.generate(
        prompt=prompt,
        response_format="json"
    )

    return OrderIssue.model_validate_json(response)
```

##### Production Considerations

- Validate model output
- Add retries and timeouts
- Log prompt/version metadata
- Avoid sending sensitive data unnecessarily
- Have fallback behavior
- Monitor cost and latency
- Evaluate quality over time

---

#### Hallucination Reduction

Use:

- Clear instructions
- Source-grounded context
- RAG
- Structured outputs
- Confidence thresholds
- Human review for high-risk actions
- Refusal rules
- Post-generation validation

##### Example Guardrail

```python
def safe_answer(question: str, retrieved_docs: list[str]) -> str:
    if not retrieved_docs:
        return "I do not have enough information to answer that."

    prompt = (
        "Answer only using the provided context. "
        "If the answer is not in the context, say you do not know.\n\n"
        f"Context:\n{retrieved_docs}\n\n"
        f"Question:\n{question}"
    )

    return llm_client.generate(prompt)
```

---

#### RAG High-Level Flow

```text
User question
   ↓
Embed question
   ↓
Search vector database
   ↓
Retrieve relevant documents
   ↓
Send context + question to LLM
   ↓
Generate grounded answer
   ↓
Validate / cite / log response
```

##### Interview Explanation

RAG is useful when the model needs company-specific, document-specific, or fresh information that is not reliably stored in its training data.

---

#### AI Evaluation Criteria

Evaluate outputs for:

- Correctness
- Relevance
- Completeness
- Faithfulness to source
- Safety
- Tone
- Format compliance
- Latency
- Cost
- User usefulness

---

#### Using AI Tools as an Engineer
##### Good Answer

> I use AI tools to move faster with drafting, debugging ideas, boilerplate, test generation, and code review support. But I treat AI output as a suggestion, not as final code. I still review logic, security, edge cases, tests, and production impact before shipping anything.

---

## AI Evaluation Work Versus AI Product Engineering

AI-focused roles can contain both model-quality work and software engineering. Interview answers should distinguish the activities rather than describing all AI work as prompt writing.

### Evaluation and Prompting Responsibilities

- Design representative evaluation cases.
- Compare model outputs against rubrics or reference behavior.
- Analyze hallucination, relevance, safety, and instruction-following failures.
- Refine prompts and structured output requirements.
- Validate retrieval quality and grounding.
- Review tool selection and tool arguments.
- Track regressions across model or prompt versions.

### Engineering Responsibilities Around Evaluation

- Build Python automation for repeatable evaluations.
- Normalize datasets and model responses.
- Create scoring and aggregation pipelines.
- Integrate model, retrieval, and tool APIs.
- Persist experiment results and metadata.
- Add retries, rate limits, concurrency controls, and error handling.
- Produce logs, reports, and dashboards for failure analysis.

A credible explanation can state an approximate split only when it reflects the real role. The more important point is to identify which deliverables were code and which were human evaluation.

### Production API Ownership Versus Supporting Integrations

These are different levels of ownership:

| Level                    | Typical Responsibility                                                          |
| ------------------------ | ------------------------------------------------------------------------------- |
| Model evaluation         | Rubrics, test cases, output analysis, regression findings                       |
| Evaluation engineering   | Python harnesses, datasets, scoring, automation, reporting                      |
| AI integration           | Calling model/retrieval services from an application workflow                   |
| Production API ownership | Contracts, auth, persistence, deployment, SLOs, on-call, backward compatibility |

Do not claim end-to-end production API ownership when the recent role mainly covered the first two levels. Instead, connect that work to earlier backend experience and current personal implementations.

### Transitioning from Evaluation to Backend Platform Work

The transition is not from nontechnical work to engineering. It is a shift in where the engineering effort is concentrated.

Transferable skills include:

- Python development and debugging.
- Data transformation and schema validation.
- External API integration.
- Test design and regression analysis.
- Reliability controls for model calls.
- Clear separation between deterministic and probabilistic behavior.

The platform-specific refresh should focus on the team's current web framework, service conventions, database patterns, deployment pipeline, and operational tooling.

### AI as an Additional Capability

A useful positioning statement is:

> My backend foundation remains the core. Recent AI work added experience with model behavior, evaluation, prompt workflows, retrieval, and AI reliability. I can apply those capabilities inside a conventional production platform without assuming every workflow should become agentic.
