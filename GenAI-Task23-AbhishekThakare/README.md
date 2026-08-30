# Assignment 23: OpenAI & Retrieval-Augmented Generation (RAG)

## Objective

This assignment is about building RAG systems using OpenAI and LangChain - starting from a basic OpenAI call, moving through a Wikipedia retriever and a custom vector store, then a few advanced retrieval strategies (MMR, multi-query, contextual compression), and finishing with a small end-to-end project: a chatbot that answers questions from a YouTube video's transcript.

## Project Structure

```text
Assignment-23/
├── Assignment23.ipynb
├── README.md
├── requirements.txt
└── data/
    └── notes.txt
```

## Input Files

- `notes.txt` - the same onboarding notes file reused from Assignment 22/25, used here as the custom text source for the vector store retriever in Task 3.
- The YouTube chatbot part (Part 4) pulls its own transcript directly from a video URL, so no local file is needed for that.

## Tasks Covered

1. OpenAI setup & basic prompt
2. Wikipedia retriever
3. Vector store retriever (OpenAI embeddings + FAISS)
4. Maximal Marginal Relevance (MMR) retriever
5. Multi-query retriever
6. Contextual compression retriever
7. Load YouTube content
8. Build vector store for YouTube content
9. Build YouTube RAG chatbot
10. Testing & evaluation
11. Conceptual questions / observations

## Libraries Used

- LangChain
- langchain-community
- langchain-openai
- langchain-text-splitters
- FAISS
- ChromaDB
- wikipedia
- youtube-transcript-api
- pypdf
- python-dotenv

## OpenAI Limitation

Same account, same problem as Assignment 22 - zero usable OpenAI credits. This assignment's restrictions specifically say LangChain, OpenAI, and FAISS/Chroma only, so unlike Assignment 25 I couldn't substitute Ollama here to get around it.

Every OpenAI-dependent cell (the basic prompt in Task 1, the embeddings in Task 3, and everything built on top of that in Tasks 4-9) is real, working code wrapped in a try/except. When run on this account, they print the actual error instead of a made-up answer. Task 2 (Wikipedia retriever) is the one part that doesn't need OpenAI at all, so it's the one piece that's expected to genuinely work regardless of credits.

If credits get added later, nothing in the code changes - rerunning the notebook top to bottom would let the vector store actually build, which unblocks Tasks 4-6, and the YouTube chatbot in Part 4 would start returning real, transcript-grounded answers instead of placeholder messages.

## Experiments Performed

- Sent a basic prompt through `ChatOpenAI` to confirm the setup.
- Used `WikipediaRetriever` to pull real Wikipedia content for a query (worked without needing any OpenAI call).
- Built a FAISS vector store over the reused onboarding notes using OpenAI embeddings, then searched it with a retriever.
- Compared a plain similarity-search retriever against an MMR retriever (`search_type="mmr"`) built off the same vector store.
- Wrapped the vector store retriever in a `MultiQueryRetriever` so the LLM generates a few reformulated versions of the question before retrieving.
- Wrapped it again in a `ContextualCompressionRetriever` with `LLMChainExtractor` to trim each retrieved chunk down to just the relevant part.
- Loaded a YouTube video transcript with `YoutubeLoader` and split it into chunks.
- Built a second FAISS vector store over the transcript chunks.
- Wrote a small chatbot loop that retrieves relevant transcript chunks, answers using only that context, and keeps a running chat history.
- Tested the chatbot with 5 video-related questions plus 1 unrelated question, specifically to check that it says "I don't know" instead of making something up when the answer isn't in the transcript.

## Key Observations

Retriever-based RAG is different from just prompting the model directly - RAG adds a lookup step first, so the model answers from documents it was actually handed instead of whatever it happens to remember from training.

Vector stores are what make RAG practical past a handful of documents - without one, there's no way to only pull in the small number of chunks that are actually relevant to a given question.

MMR, multi-query, and contextual compression are all tweaks to the retrieval step itself, not the final answering step - they change what context the LLM sees, not how it generates the answer once it has that context.

## Challenges Faced

The recurring issue through this whole notebook is the same one from Assignment 22 - no usable OpenAI credits, which blocks every embedding call and every direct LLM call. Because this assignment specifically restricts the toolset to OpenAI, I couldn't route around it with a local model the way I did in Assignment 25, so most of Parts 2-4 are "correct code, blocked by billing" rather than genuinely tested end to end.

## Learning Outcomes

I learned that a lot of the "advanced" retrievers (MMR, multi-query, contextual compression) aren't really separate systems - they're all just wrappers around a base retriever that change either how results get selected (MMR) or add an LLM step before/after the search (multi-query generates queries first, contextual compression trims results after).

I also saw that the YouTube chatbot in Part 4 is really the exact same RAG pattern as Task 3, just pointed at a transcript instead of a text file - loading, splitting, embedding, and retrieving works the same way no matter where the documents originally came from.

## Submitted By

Abhishek Thakare
