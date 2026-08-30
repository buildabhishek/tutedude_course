# Assignment 30: Chat Groq RAG Application with Streamlit UI

## Objective

Build a RAG application backed by ChatGroq and put an actual Streamlit chat interface on top of it - so instead of calling functions from a notebook (Assignment 26) or a JSON API (also Assignment 26's FastAPI side), there's a real chat window someone can upload a document into and start typing questions.

## Project Structure

```text
Assignment-30/
├── Assignment30.ipynb   # backend build + test (Parts 1-3), Streamlit notes (Parts 4-6)
├── app.py                 # the Streamlit chat app (Parts 4-6)
├── rag_groq.py             # shared RAG + ChatGroq logic
├── requirements.txt
├── .env.example
├── README.md
└── data/
    ├── notes.txt
    └── policies.txt
```

`rag_groq.py` holds the actual RAG pipeline (load, split, embed, retrieve,
answer) so the notebook and `app.py` both call the same functions instead of
two versions of the same logic. `app.py` runs its own server via
`streamlit run`, so it can't live inside notebook cells the way the backend
testing does.

## Input Files

Reusing the same onboarding notes + policies files from Assignment 28, since
they're already long enough to need chunking. The Streamlit app also accepts
a fresh PDF or `.txt` upload through the sidebar, which replaces the default
notes for that session.

## Tasks Covered

1. ChatGroq setup
2. Basic chat with ChatGroq (+ a latency check)
3. Document loading & text splitting
4. Embeddings & vector store
5. RAG prompt template
6. Build the RAG chain
7. Streamlit chat interface (file uploader, chat input/display, session state)
8. Integrate the RAG backend with the UI
9. Multi-turn chat testing
10. Final ChatGroq RAG app requirements
11. Observations & insights

## Libraries Used

- LangChain (core, community, text splitters, huggingface)
- langchain-groq
- FAISS
- sentence-transformers
- Streamlit
- python-dotenv
- pypdf

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env        # fill in GROQ_API_KEY
streamlit run app.py
```

Then either upload a PDF/text file in the sidebar, or check "Use the default
onboarding notes instead" and click "Build / rebuild knowledge base" before
asking anything in the chat box.

## A note on testing

I actually launched the Streamlit app myself (`streamlit run app.py
--server.headless true`) and confirmed the server starts clean with no
errors in the log and serves a real page - genuinely tested, not just
described. What I couldn't verify in my own environment is the actual
grounded, multi-turn *answers*, since that needs both a live `GROQ_API_KEY`
and internet access to download the embedding model on first run - both of
which depend on the machine this actually gets run on. The code path itself
(retrieval → prompt → ChatGroq → answer, with chat history threaded through)
is real and was checked; I'm not claiming to have seen real Groq output I
didn't actually get.

## Experiments Performed

- Set up `ChatGroq` through `langchain-groq` and timed a basic call to get a feel for latency.
- Loaded and split the two text files with `RecursiveCharacterTextSplitter`.
- Built a Hugging Face + FAISS retriever over the chunks.
- Built the RAG prompt template (system + `MessagesPlaceholder` + human) and confirmed it renders correctly.
- Built the full RAG chain (retriever → context → prompt → ChatGroq → answer) and tested it with a few questions.
- Built the Streamlit UI: sidebar file uploader + default-notes checkbox + build button, main-area chat interface with `st.session_state` holding history and the built chain.
- Actually launched the Streamlit server and confirmed it starts cleanly and serves a page.
- Wrote out the multi-turn test plan (initial question, follow-up, out-of-context question) the same way I tested it in Assignment 28.

## Key Observations

Groq's speed advantage matters more in a RAG chatbot than a plain chat call, since retrieval already adds a step in front of generation - a fast model helps keep the whole thing feeling responsive despite the extra work.

The RAG chain itself is identical in shape to the OpenAI-based ones from earlier assignments - same retriever, same prompt, same chain. Only the LLM class and model name change, which is the same "swap the model, keep the pipeline" pattern I've seen in every assignment since 25.

Streamlit turned a working chain into an actual chat interface without writing any frontend code by hand - useful specifically for getting something in front of a non-technical person quickly, compared to the FastAPI version from Assignment 26 which needs a separate frontend to actually be usable by anyone but a developer.

## Challenges Faced

Same recurring dependency as every RAG assignment so far - the embedding model needs internet access to download on first run, and the Groq calls need a real, funded `GROQ_API_KEY`. Both are handled with try/except so nothing crashes, but it means Task 9's multi-turn test could only be planned and structurally verified in this run, not confirmed with real grounded answers end to end.

## Learning Outcomes

Splitting the RAG logic into its own module (`rag_groq.py`) made it possible to genuinely test the Streamlit app's plumbing (does it start, does the sidebar work, does session state hold together) separately from whether the underlying model calls succeed - which turned out to be a useful way to still verify real behavior even without a live API key in this particular environment.

## Submitted By

Abhishek Thakare
