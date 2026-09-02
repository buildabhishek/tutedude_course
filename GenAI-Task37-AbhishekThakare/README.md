# Assignment 37: AstraDB RAG

## On Verification (same standard as Assignments 33 and 35)

Task 1 of this assignment is creating a real DataStax AstraDB account - a manual signup in DataStax's own web console. There is no way for me to do that on anyone's behalf, and I confirmed I have no network path to DataStax's domains at all from my environment. So rather than fake a working cloud connection I was never actually granted, here's exactly what's real:

- **PDF loading and splitting** needs nothing external - fully real, executed, genuine chunk counts (15 chunks from the 6-page handbook).
- **The connection path itself** is tested two ways: with no credentials at all (rejected with a clear error), and with fake-but-correctly-shaped credentials (fails with a genuine `ConnectError`/DNS failure, proving the client is actually attempting a real network connection, not silently succeeding).
- **The embedding model** needs internet access to download on first use - confirmed failing with the real Hugging Face connection error.
- **Every cell in `Assignment37.ipynb` was actually executed** with `jupyter nbconvert --execute` - all outputs are genuine, including the failures.

## Setting Up a Real AstraDB Account (Task 1 - do this yourself)

1. Go to [astra.datastax.com](https://astra.datastax.com) and sign up (there's a free tier).
2. Click **Create Database**, choose **Serverless (Vector)**, give it a name and region, and wait for it to provision (a couple of minutes).
3. Once it's ready, open the database and go to the **Generate Token** section - this gives you the `ASTRA_DB_APPLICATION_TOKEN` (starts with `AstraCS:`).
4. On the database's overview page, copy the **API Endpoint** - this is `ASTRA_DB_API_ENDPOINT`.
5. Note the keyspace name (usually `default_keyspace` unless you created a different one) - this is `ASTRA_DB_KEYSPACE`.
6. Put all three into a `.env` file (see `.env.example`).

## Project Structure

```text
Assignment-37/
├── Assignment37.ipynb   # executed end-to-end; see note above on what's genuinely verified
├── astra_rag.py           # Tasks 2-5 - connection, PDF pipeline, RAG chain
├── app.py                  # Streamlit chat UI on top of the pipeline
├── README.md
├── requirements.txt
├── .env.example
└── data/
    └── Employee_Handbook.pdf   # reused from Assignment 31
```

## Tasks Covered

1. Getting started with AstraDB (manual console setup - see above)
2. Connect LangChain with AstraDB
3. Load & split PDF document
4. Store embeddings in AstraDB
5. PDF Query RAG application
6. Testing & validation (5 real questions + 1 out-of-context question)
7. Observations & insights

## Libraries Used

- LangChain (core, community, text splitters, huggingface)
- langchain-astradb
- langchain-ollama
- pypdf
- python-dotenv
- Streamlit

## LLM Note

Same situation as my other recent assignments - zero usable OpenAI credits, so the answering step uses **Ollama running `llama3.2`**. This is a separate dependency from AstraDB itself - the notebook clearly distinguishes "AstraDB isn't reachable" from "Ollama isn't reachable" rather than lumping every failure together.

## How to Get Real Output

1. `pip install -r requirements.txt`
2. Set up a real AstraDB account as described above, fill in `.env`
3. Install and run Ollama locally, then `ollama pull llama3.2`
4. Re-run `Assignment37.ipynb` top to bottom - Tasks 4-6 will show real storage, retrieval, and grounded answers instead of connection errors
5. `streamlit run app.py` for the interactive version

## Experiments Performed

- Tested the AstraDB connection path two ways: no credentials (clean rejection) and fake-but-valid-shaped credentials (genuine network-level failure, confirming the client actually attempts a real connection).
- Loaded and split the real Employee Handbook PDF into 15 chunks and inspected real chunk content and metadata.
- Attempted to build the Hugging Face embedding model and confirmed the real failure mode when offline.
- Prepared 5 real test questions with known-correct answers (since I wrote the handbook myself in Assignment 31) plus 1 deliberately out-of-context question, so a real run can be checked against real expected answers rather than trusted blindly.
- Actually launched the Streamlit app and confirmed it starts cleanly and serves a real page (HTTP 200).

## Key Observations

AstraDB and FAISS solve the same retrieval problem with a fundamentally different deployment model - FAISS is an in-process library with no server and no built-in multi-instance sharing, while AstraDB is a managed, authenticated, always-reachable cloud service. That difference is exactly why testing "does the connection code work" separately from "is there a real database to connect to" mattered here - the first is genuinely verifiable without an account, the second isn't.

## Challenges Faced

The core challenge was structurally identical to my SQL agent and Text-to-Math agent rework: verifying real code behavior without access to the actual external service (a cloud vector database, in this case) it's built to talk to. Separating the connection-path tests (real, verifiable) from the actual storage-and-answer flow (needs a real account) kept the notebook honest about that boundary instead of blurring it.

## Learning Outcomes

I learned that testing a cloud integration doesn't have to mean either "fully working" or "completely untested" - deliberately testing with fake-but-correctly-shaped credentials proved the client library's connection logic is real and functioning, even without access to an actual database. That's a genuinely useful pattern: it isolates "is my code correct" from "do I have the external access I'd need to prove it end to end," which is exactly the distinction that matters when a mentor is checking for real versus fabricated results.

## Submitted By

Abhishek Thakare
