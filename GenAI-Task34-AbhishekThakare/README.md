# Assignment 34: Text Summarization using LangChain

## Objective

Build and compare four different ways to summarize the same long document using LangChain: a plain prompt-based summary, and three summarization chains - stuff, map-reduce, and refine.

## Project Structure

```text
Assignment-34/
├── Assignment34.ipynb
├── summarizer.py
├── README.md
├── requirements.txt
└── data/
    └── long_article.txt
```

`summarizer.py` holds all four summarization approaches plus the unified `summarize_document(text, method=...)` function, so the notebook is testing the same code a reusable module would expose.

## Input Files

`long_article.txt` - an original ~1,300-word (7,850+ character) article I wrote about Retrieval-Augmented Generation, long enough to require chunking. Writing it myself sidesteps any copyright question about summarizing someone else's text, and it ties naturally into the RAG work from my earlier assignments.

## A Real Version Compatibility Issue

`load_summarize_chain` - the function Tasks 5, 8, and 11 specifically ask for - lives in LangChain's older "legacy chains" API and was **removed entirely when LangChain hit version 1.0**. I confirmed this myself: importing it under the newest LangChain (1.3.x) throws `ModuleNotFoundError: No module named 'langchain.chains'`, and it only works once pinned back to `langchain==0.3.27` / `langchain-community==0.3.27`. `requirements.txt` pins these versions deliberately, with a comment explaining why - a plain `pip install langchain` will silently install a version where half of this assignment can't even import.

## Tasks Covered

1. Load and prepare text
2. Prompt-based summarization
3. Prompt variations (short vs bullet-point)
4. Why the stuff chain is needed (conceptual)
5. Implement the stuff summarization chain
6. Comparison with the prompt-based summary
7. Why map-reduce is needed (conceptual)
8. Implement the map-reduce summarization chain
9. Analyze map outputs (intermediate per-chunk summaries)
10. Understanding the refine chain (conceptual)
11. Implement the refine summarization chain
12. Comparison of all four summarization methods
13. Build a reusable `summarize_document()` function
14. Observations & insights

## Libraries Used

- langchain (pinned to 0.3.27)
- langchain-community (pinned to 0.3.27)
- langchain-text-splitters
- langchain-ollama (pinned to 0.3.10, compatible with the pinned core version)

## LLM Note

Same as my last few assignments - "LangChain + LLM of choice" as the restriction, so with zero usable OpenAI credits I'm using **Ollama running `llama3.2`** locally. Every summarization function is wrapped so it fails gracefully with a clear message instead of crashing when Ollama isn't reachable.

## Experiments Performed

- Loaded the article and confirmed its length (7,853 characters).
- Built a plain `PromptTemplate`-based summarizer with two style variations (short paragraph vs bulleted list).
- Split the article into 9 real chunks with `RecursiveCharacterTextSplitter` and confirmed the chunk sizes.
- Built and tested the stuff, map-reduce, and refine chains via `load_summarize_chain`.
- Used `return_intermediate_steps=True` on the map-reduce chain to inspect the per-chunk summaries before the reduce step combines them.
- Built `summarize_document(text, method=...)` as a single switchable entry point, and tested all four methods plus an invalid method name to confirm it's rejected with a clear `ValueError`.

## Key Observations

Map-reduce and refine solve the same fundamental problem (documents too large for one prompt) with different trade-offs: map-reduce's per-chunk summaries are independent and can run in parallel, while refine's sequential "update the running summary" approach tends to read more coherently at the cost of losing that parallelism.

The prompt-based approach and the stuff chain are doing essentially the same thing under the hood for a document this size - the chain abstraction only starts paying off once the document is too large for a single prompt, which is exactly where stuff stops working and map-reduce/refine become necessary.

## Challenges Faced

The actual challenge in this assignment wasn't the summarization logic itself - it was discovering that the exact function this assignment asks for doesn't exist in the current version of LangChain, and having to track down which older version still has it. Beyond that, the usual dependency remains: every chain needs Ollama actually running locally to produce a real summary, so most of the comparisons in Tasks 6 and 12 are reasoned about structurally rather than confirmed against real, compared output in this particular run.

## Learning Outcomes

I learned that "map-reduce" and "refine" aren't just two settings on the same underlying process - they represent a genuine trade-off between parallel-but-disconnected summarization and sequential-but-coherent summarization, and picking between them should depend on whether speed or read-quality matters more for a given use case. I also learned to actually verify a library API still exists before building an assignment around it, rather than assuming a widely-documented function like `load_summarize_chain` is still there in whatever version happens to get installed.

## Submitted By

Abhishek Thakare
