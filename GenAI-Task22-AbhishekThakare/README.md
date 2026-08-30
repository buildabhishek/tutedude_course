# Assignment 22: Embedding Models, Vector Stores & Similarity Search

## Objective

This assignment demonstrates the retrieval part of a small RAG system.

It covers document embeddings, similarity search, FAISS, ChromaDB, and a simple end-to-end retrieval pipeline.

## Project Structure

```text
Assignment-22/
├── assignment22.ipynb
├── README.md
└── data/
    ├── notes.txt
    ├── data.csv
    └── company_overview.pdf
```

## Input Files

- `notes.txt` - text content used for loading, chunking and embedding.
- `data.csv` - sample data loaded with `CSVLoader`.
- `company_overview.pdf` - PDF content loaded with `PyPDFLoader`.

## Tasks Covered

1. OpenAI embedding model
2. Hugging Face embedding model
3. OpenAI vs Hugging Face comparison
4. Manual cosine similarity search
5. LangChain similarity search
6. Ollama embedding model
7. FAISS vector store and persistence
8. ChromaDB vector store and persistence
9. FAISS vs ChromaDB comparison
10. Embedding and vector-store combinations
11. End-to-end retrieval pipeline
12. Observations and insights

## Libraries Used

- LangChain
- langchain-community
- langchain-huggingface
- langchain-ollama
- langchain-chroma
- sentence-transformers
- FAISS
- ChromaDB
- scikit-learn
- pandas
- OpenAI / langchain-openai
- PyPDF

## OpenAI Limitation

The OpenAI implementation is included in the notebook.

My current OpenAI API account has zero usable credits, so I cannot complete a genuine OpenAI embedding request at the moment. The notebook catches this failure and records it instead of using made-up values.

Because OpenAI vectors are not available in this run, OpenAI → FAISS and OpenAI → Chroma are also marked as not tested.

If credits become available, the OpenAI cell can be rerun and the two OpenAI vector-store tests can then be run.

## Performance Experiment

The notebook measures embedding time for the same document chunks.

The timing depends on the computer, local hardware, model loading, batching and network conditions. Therefore the numbers are measurements for the actual run and are not treated as universal benchmarks.

## Cost vs Performance

OpenAI's current documentation lists `text-embedding-3-small` at $0.02 per 1 million input tokens.

Example API costs:

| Input tokens | Approximate cost |
|---:|---:|
| 100,000 | $0.002 |
| 1,000,000 | $0.02 |
| 10,000,000 | $0.20 |
| 100,000,000 | $2.00 |

Source: https://developers.openai.com/api/docs/models/text-embedding-3-small

Hugging Face can run locally without an OpenAI API charge, but local inference still uses RAM, CPU/GPU, storage and electricity.

## Experiments Performed

- Created embeddings from the same document chunks.
- Measured local embedding time.
- Calculated cosine similarity manually.
- Added input validation to the similarity search function.
- Used LangChain FAISS and ChromaDB similarity search.
- Saved and reloaded FAISS.
- Persisted and reloaded ChromaDB.
- Tested different embedding/vector-store combinations when the embedding backend was available.

## Key Observations

Embeddings convert text into numerical vectors so that related text can be compared using vector similarity.

The embedding model and vector store have different jobs. The embedding model creates the vector representation, while the vector store keeps the vectors searchable.

FAISS is mainly focused on vector indexing and similarity search. ChromaDB provides a more database-like collection and persistence workflow.

The retrieval part of a RAG system is:

```text
Documents
    ↓
Chunks
    ↓
Embeddings
    ↓
Vector Store
    ↓
Similarity Search
    ↓
Relevant Context
    ↓
LLM
    ↓
Answer
```

## Challenges Faced

The main limitation in this run is the lack of OpenAI API credits. I kept the real OpenAI code in the notebook but did not fabricate its output.

Ollama also requires a local service and the `nomic-embed-text` model, so its results depend on whether Ollama is installed and running on the machine.

## Learning Outcomes

I learned that embeddings and vector stores solve different problems.

I also understood that similarity search first represents the query as a vector and then looks for document vectors that are close to it.

The most useful part of the assignment for me was seeing how the same retrieval idea can be used with different embedding models and vector stores.

## Submitted By

Abhishek Thakare
