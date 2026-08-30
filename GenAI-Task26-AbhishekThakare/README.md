# Assignment 26: Groq API Chatbot, RAG & FastAPI Serving

## Objective

Build a chatbot backed by the Groq API, add a Retrieval-Augmented Generation (RAG) layer using local embeddings and FAISS, and expose the application through a FastAPI REST API.

The project separates the chatbot logic, RAG pipeline, and API serving layer so that the same core functions can be tested independently from the notebook and then reused by FastAPI.

---

## Architecture

```text
                         ┌─────────────────────┐
                         │      User Query     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   FastAPI /chat     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   RAG Retriever     │
                         └──────────┬──────────┘
                                    │
                     ┌──────────────┴──────────────┐
                     │                             │
                     ▼                             ▼
              Sentence Transformer             FAISS
                     │                             │
                     └──────────────┬──────────────┘
                                    │
                                    ▼
                         Retrieved Context
                                    │
                                    ▼
                         Structured RAG Prompt
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      Groq API       │
                         │ openai/gpt-oss-120b │
                         └──────────┬──────────┘
                                    │
                                    ▼
                              Final Answer
```

---

## Project Structure

```text
Assignment-26/
│
├── Assignment26.ipynb
├── main.py
├── groq_chatbot.py
├── rag.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
└── data/
    ├── notes.txt
    └── data.csv
```

### File responsibilities

| File                 | Purpose                                                                   |
| -------------------- | ------------------------------------------------------------------------- |
| `Assignment26.ipynb` | Exploration, experiments, API tests and evaluation                        |
| `groq_chatbot.py`    | Core Groq API wrapper                                                     |
| `rag.py`             | Document loading, chunking, embeddings, FAISS retrieval and RAG prompting |
| `main.py`            | FastAPI application                                                       |
| `data/notes.txt`     | Text knowledge source                                                     |
| `data/data.csv`      | Employee structured-data source                                           |
| `.env.example`       | Environment-variable template                                             |
| `requirements.txt`   | Python dependencies                                                       |
| `README.md`          | Documentation                                                             |

---

# Tasks Covered

1. Groq API setup and basic chat
2. Reusable `groq_chat()` function
3. RAG pipeline using local embeddings and FAISS
4. Structured RAG prompt
5. FastAPI `/health` and `/chat` endpoints
6. Groq integration, validation and error handling
7. Local API testing
8. Environment configuration and logging
9. End-to-end RAG evaluation
10. Observations, limitations and learning outcomes

---

# Technologies Used

* Python
* Groq Python SDK
* Groq `openai/gpt-oss-120b`
* FastAPI
* Uvicorn
* Pydantic
* python-dotenv
* LangChain Community
* LangChain Text Splitters
* LangChain Hugging Face
* Sentence Transformers
* FAISS

The Groq API currently supports `openai/gpt-oss-120b` as a production model, and the Chat Completions API accepts the model ID directly.

---

# Data Sources

The RAG implementation indexes two local files:

```text
data/notes.txt
data/data.csv
```

### `notes.txt`

The notes describe a Personal Knowledge Assistant, document loaders, chunking, ingestion and the role of these steps in a RAG pipeline.

### `data.csv`

The CSV contains employee records with:

* employee ID
* name
* department
* role
* years of experience
* location

The project deliberately answers only from the indexed context. If the supplied documents do not contain enough information, the RAG prompt instructs the model not to invent an answer.

---

# Setup

## 1. Clone or copy the project

Open a terminal in the project directory:

```bash
cd Assignment-26
```

## 2. Create a virtual environment

### Windows

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure the environment

Copy `.env.example` to `.env`.

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

Then edit `.env`:

```env
GROQ_API_KEY=your_real_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
RAG_TOP_K=5
```

Do not commit or submit the real `.env` file.

---

# How to Run

## Start FastAPI

Run:

```bash
python -m uvicorn main:app --reload
```

The server starts at:

```text
http://127.0.0.1:8000
```

On startup the application loads the local embedding model and builds the FAISS retriever.

A successful startup logs:

```text
RAG retriever built successfully.
Application startup complete.
```

---

# API Endpoints

## GET `/health`

Checks whether the API is running and whether RAG initialization succeeded.

Example:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok",
  "rag_enabled": true
}
```

---

## POST `/chat`

Accepts a JSON request containing a question.

Example:

```powershell
Invoke-RestMethod `
  -Uri http://127.0.0.1:8000/chat `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"query":"Who is the ML Engineer?"}'
```

Example response:

```text
answer
------
Rahul Verma.
```

---

# Swagger UI

FastAPI automatically generates interactive API documentation.

Open this in a web browser:

```text
http://127.0.0.1:8000/docs
```

The Swagger interface provides interactive access to:

```text
GET  /health
POST /chat
```

---

# RAG Pipeline

The RAG implementation follows this process:

```text
notes.txt + data.csv
        ↓
Document Loading
        ↓
Recursive Character Text Splitting
        ↓
Sentence Transformer Embeddings
        ↓
FAISS Vector Store
        ↓
Similarity Retrieval
        ↓
Retrieved Context
        ↓
Structured Prompt
        ↓
Groq
        ↓
Grounded Answer
```

The embedding model used is:

```text
sentence-transformers/all-MiniLM-L6-v2
```

The embedding model runs locally, so OpenAI credits are not required for the retrieval layer.

The Groq API is used only for answer generation.

---

# Grounding Strategy

The RAG system uses explicit grounding instructions:

```text
Answer using only the supplied context.
Do not invent facts.
If the context does not contain enough information,
say that you do not know based on the provided documents.
```

This is important because retrieval-augmented generation is not only about finding documents; the generation step must also be prevented from filling missing information with unsupported assumptions.

---

# Testing and Evaluation

The application was tested against both supported and unsupported questions.

## Test 1 — Employee lookup

Question:

```text
Who is the ML Engineer?
```

Result:

```text
Rahul Verma.
```

Status:

```text
PASS
```

---

## Test 2 — Document understanding

Question:

```text
Why is chunking important in a RAG system?
```

Result:

The application returned an explanation grounded in the notes, including the limited context window of language models and the benefit of breaking documents into smaller semantic chunks.

Status:

```text
PASS
```

---

## Test 3 — Unknown information

Question:

```text
What is the company leave policy?
```

Result:

```text
I don't know.
```

There is no leave-policy information in the indexed documents.

Status:

```text
PASS
```

This test is important because the expected behavior is to avoid hallucinating an answer.

---

## Test 4 — Request validation

An empty query was submitted:

```json
{
  "query": ""
}
```

FastAPI/Pydantic rejected the request with a validation error because the query must contain at least one character.

Status:

```text
PASS
```

---

## Test 5 — Missing field validation

An empty JSON object was submitted:

```json
{}
```

FastAPI rejected the request because the required `query` field was missing.

Status:

```text
PASS
```

---

# Retrieval Quality Experiment

During testing, the default retriever used a small top-k value.

A broader question:

```text
Who are the employees based in Pune?
```

initially produced an incomplete answer when only three documents were retrieved.

A direct retrieval experiment with:

```text
k = 8
```

returned all eight employee records, including all four Pune employees:

```text
Priya Nair
Vikram Singh
Ananya Sharma
Sneha Iyer
```

A similar experiment for:

```text
Who has the most years of experience?
```

showed that the relevant record for:

```text
Arjun Reddy — 6 years
```

was available when the larger retrieval set was used.

This experiment demonstrated an important RAG trade-off:

> A small top-k value is efficient for focused questions, but broader questions over structured data may require more retrieved context.

For this assignment, `RAG_TOP_K=5` is used as a practical compromise for the small demonstration dataset.

---

# Error Handling

The API handles several failure modes.

## Missing Groq API key

If `GROQ_API_KEY` is not configured, the application returns a clean configuration error rather than exposing an uncontrolled Python traceback.

## Groq/API failure

Unexpected upstream failures are returned as an HTTP `502 Bad Gateway`.

## Invalid request

FastAPI/Pydantic automatically returns validation errors for:

* missing `query`
* empty `query`

## RAG initialization failure

The API attempts to build the RAG retriever during startup.

If the embedding model, input files or vector-store construction fails, the application can continue running and fall back to plain Groq chat.

This keeps a local RAG dependency failure from preventing the API service itself from starting.

---

# Environment Variables

| Variable       | Purpose                    | Example               |
| -------------- | -------------------------- | --------------------- |
| `GROQ_API_KEY` | Authentication with Groq   | `gsk_...`             |
| `GROQ_MODEL`   | Groq model ID              | `openai/gpt-oss-120b` |
| `RAG_TOP_K`    | Number of retrieved chunks | `5`                   |

The API key is intentionally kept outside the source code.

---

# Production-Readiness Basics

The project includes several basic production-oriented practices:

* environment-based secrets
* configurable model name
* configurable retrieval size
* lazy Groq client initialization
* application logging
* startup initialization of the retriever
* request validation
* structured API responses
* HTTP error handling
* separation of business logic from API serving
* `.gitignore` protection for secrets and generated Python files

This is still a learning project and is not intended to represent a complete production deployment.

---

# Design Decisions

## Why separate `groq_chatbot.py`?

The Groq wrapper is independent from FastAPI so the same function can be tested from the notebook and imported by the API.

This avoids maintaining separate copies of chatbot logic.

## Why separate `rag.py`?

RAG is an additional capability on top of the chatbot.

Keeping it separate makes it possible to:

```text
Plain Groq chatbot
```

and:

```text
Groq + RAG
```

independently.

## Why FAISS?

FAISS provides a simple local vector-search implementation and does not require a hosted vector database for this assignment.

## Why local Hugging Face embeddings?

The embedding layer can run locally using:

```text
sentence-transformers/all-MiniLM-L6-v2
```

This avoids requiring OpenAI embedding credits.

## Why Groq?

Groq provides the remote LLM inference layer used to generate the final response. The application uses the Groq Python SDK and the `openai/gpt-oss-120b` model available to the configured Groq project.

---

# Challenges Faced

### 1. Groq model availability

The initially configured model:

```text
llama-3.3-70b-versatile
```

was not accessible through the configured Groq project.

The Groq Models API was used to inspect the models actually available to the account, and:

```text
openai/gpt-oss-120b
```

was selected instead.

This is preferable to assuming that every model ID is available to every project. Groq also supports organization/project-level model permissions.

### 2. Local embedding initialization

The first RAG startup requires the Sentence Transformer model to be available locally. The environment therefore needs internet access when the model has not previously been downloaded.

### 3. Retrieval completeness

Testing showed that top-k retrieval affects answer quality for broader structured-data questions.

This was observed directly rather than assumed.

### 4. Dataset limitations

The supplied CSV contains employee records rather than a company policy/FAQ dataset.

Therefore questions such as:

```text
What is the company leave policy?
```

correctly return an unknown answer instead of fabricated information.

---

# Key Observations

### Observation 1 — Retrieval quality matters

A powerful LLM cannot recover information that was never retrieved into its context.

The experiment with `k=3` versus `k=8` demonstrated this directly.

### Observation 2 — RAG reduces unsupported answers

The grounded prompt instructed the model to use only retrieved context.

When the leave-policy question had no supporting context, the model returned:

```text
I don't know.
```

instead of inventing a policy.

### Observation 3 — FastAPI handles validation cleanly

Pydantic automatically validates the request model, so malformed requests can be rejected before reaching the Groq API.

### Observation 4 — Separation of concerns simplifies testing

Keeping:

```text
groq_chatbot.py
rag.py
main.py
```

separate makes each layer easier to understand and test.

### Observation 5 — RAG is not just an LLM call

The quality of the final answer depends on:

```text
document quality
      +
chunking
      +
embeddings
      +
retrieval
      +
prompting
      +
LLM generation
```

An issue in an earlier stage can propagate into the final answer.

---

# Learning Outcomes

This assignment helped demonstrate how to:

* call an LLM through the Groq API
* build a reusable LLM wrapper
* separate application logic from API serving
* load and chunk documents
* generate local embeddings
* build a FAISS vector store
* retrieve semantically relevant context
* construct a grounded RAG prompt
* serve an LLM application through FastAPI
* validate requests with Pydantic
* handle API and configuration failures
* test positive and negative RAG cases
* reason about retrieval quality and top-k selection
* protect API credentials using environment variables

The most important lesson was that **RAG quality depends on the entire retrieval pipeline, not just the model used for generation**.

---

# Limitations and Future Improvements

This project intentionally remains a basic RAG implementation.

Possible improvements include:

1. Add PDF ingestion using the available company overview document.
2. Add metadata-aware retrieval.
3. Experiment with alternative embedding models.
4. Compare similarity search with MMR retrieval.
5. Add a reranking stage.
6. Add document-source citations to responses.
7. Add automated evaluation metrics.
8. Add persistent FAISS index storage instead of rebuilding at startup.
9. Add authentication and rate limiting to the API.
10. Add automated tests using `pytest`.
11. Add Docker-based deployment.
12. Add monitoring and structured request metrics.

---

# Final Result

The completed application provides:

```text
Groq chatbot
      +
Local embedding model
      +
FAISS retrieval
      +
Grounded RAG prompt
      +
FastAPI REST API
      +
Request validation
      +
Error handling
      +
Environment-based configuration
```

The final system was tested locally with real Groq API calls and real retrieval queries.

---

## Submitted By

**Abhishek Thakare**
