# Assignment 25: Prompting & LangChain Chains

## Objective

This assignment builds on top of Assignment 22. That one was only about retrieval - loading documents, chunking them, and comparing embeddings. This one actually wires an LLM on top of that retrieval setup.

It covers prompt templates, structured output with Pydantic, simple/conditional/parallel chains, and Runnables & LCEL.

## Project Structure

```text
Assignment-25/
├── Assignment25.ipynb
├── README.md
├── requirements.txt
└── data/
    ├── notes.txt
    └── data.csv
```

## Input Files

Same knowledge base as Assignment 22, reused as-is:

- `notes.txt` - onboarding notes for the Personal Knowledge Assistant project (leave policy, IT support, onboarding process, etc.)
- `data.csv` - a small FAQ file loaded with `CSVLoader`.

## Tasks Covered

1. PromptTemplate
2. ChatPromptTemplate & message prompt templates
3. Pydantic output schema
4. Validation & error handling
5. Simple chain
6. Conditional chain
7. Parallel chain
8. Runnables basics
9. LCEL-based RAG chain
10. Observations and insights

## Libraries Used

- LangChain
- langchain-community
- langchain-text-splitters
- langchain-openai
- langchain-huggingface
- langchain-ollama
- sentence-transformers
- FAISS
- ChromaDB
- pypdf
- beautifulsoup4
- pandas
- python-dotenv
- ollama

## OpenAI Limitation

Same situation as Assignment 22 - my OpenAI account still has zero usable credits. Every chain in this notebook that needs a chat model is written against **Ollama running `llama3.2`** instead, since that one actually works without any API key or billing.

The chain code itself doesn't really care which model it's talking to - that's the whole point of LangChain's `Runnable` interface. If OpenAI access comes through later, swapping `ChatOllama` for `ChatOpenAI` is a one-line change and the rest of the pipeline stays exactly the same.

If Ollama isn't running when a cell executes, it doesn't crash - the cell catches the connection error and prints a placeholder message instead of a real answer, so the logic is still visible even without the model up.

## Experiments Performed

- Rendered a plain `PromptTemplate` with multiple onboarding questions.
- Built a `ChatPromptTemplate` out of System/Human/AI message templates and compared it against the plain version.
- Reused the FAISS vector store setup from Assignment 22 to get a retriever for the chains below.
- Defined a Pydantic schema (`answer`, `confidence`, `source`) and parsed both valid and intentionally broken LLM-style outputs through it.
- Built a simple chain (Prompt → LLM → Output).
- Built a conditional chain that classifies a question as factual or casual and routes it - factual questions go through the retriever, casual ones go straight to the LLM.
- Built a parallel chain that generates an answer, a summary, and follow-up questions from the same question at once.
- Wrapped a plain Python function in `RunnableLambda` and used `RunnablePassthrough` to carry the original question alongside the retrieved context.
- Built a full LCEL RAG chain (`Retriever | Prompt | LLM | Output Parser`) and tested it on a few different onboarding questions.

## Key Observations

Structured output matters once you actually want to use an LLM's answer in code rather than just reading it - a Pydantic schema either gives back a real typed object or a clear error, not a paragraph you have to parse by hand.

LCEL makes chains easier to reuse. The same `retriever` built once in the dataset-setup section got reused unchanged in both the conditional chain and the LCEL RAG chain later.

Parallel chains and conditional chains solve different problems - parallel is for getting several independent outputs from one input at the same time, conditional is for picking exactly one path depending on what the input actually is.

## Challenges Faced

The main limitation, again, is not having a working OpenAI key - so every chain here is built and tested against Ollama locally instead. The retrieval side depends on the same Hugging Face embedding model from Assignment 22, so it needs that model available locally (or internet access the first time to download it) before the retriever-based chains will actually return real answers.

## Learning Outcomes

I learned that once a retriever is built, it isn't tied to any one use case - the exact same retriever object worked inside a hand-written conditional chain and inside a proper LCEL pipeline without any changes.

I also saw the practical difference between a plain `PromptTemplate` and a `ChatPromptTemplate` - the second one keeps the system instruction separate from whatever the user actually asks, which is closer to how real chat models are meant to be used.

The most useful part of this assignment was seeing the whole thing end to end - a question goes in, gets classified, optionally pulled through retrieval, passed through a prompt, answered by the LLM, and (when needed) validated against a schema before it's considered a "real" answer.

## Submitted By

Abhishek Thakare
