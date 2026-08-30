# Assignment 28: Q&A RAG Chatbot with Message History

## Objective

Take the RAG pattern from my earlier assignments and add real conversation memory on top of it, so the bot can handle follow-up questions like "what about the previous point?" instead of treating every question as a clean slate.

## Project Structure

```text
Assignment-28/
├── Assignment28.ipynb
├── README.md
├── requirements.txt
└── data/
    ├── notes.txt
    └── policies.txt
```

## Input Files

- `notes.txt` - the same onboarding notes reused from Assignments 22/25/26.
- `policies.txt` - a new file with more detail on the same HR/IT policies, added so there are multiple text files with enough combined length to actually need chunking, per the dataset requirement.

## Tasks Covered

1. Load documents
2. Text splitting
3. Create embeddings
4. Store embeddings in a vector store & create a retriever
5. RAG prompt template (system + MessagesPlaceholder + human)
6. Build the RAG chain with message history
7. Maintain message history
8. Trim chat history
9. Multi-turn Q&A testing
10. Build the final conversational RAG chatbot
11. Observations & insights

## Libraries Used

- LangChain
- langchain-community
- langchain-text-splitters
- langchain-huggingface
- langchain-ollama
- FAISS
- sentence-transformers

## LLM Note

Restriction for this one is "LangChain + any LLM", so same as Assignment 25 - I'm using **Ollama running `llama3.2`** locally along with the same Hugging Face embedding model, since my OpenAI account still has zero usable credits. Every retriever/chain cell is wrapped so it fails gracefully with a clear message instead of crashing when Ollama or the embedding model isn't reachable in a given environment - the actual logic doesn't change once either one is available.

## Experiments Performed

- Loaded both `.txt` files with `DirectoryLoader` and printed the document count plus a content sample.
- Split the combined documents with `RecursiveCharacterTextSplitter` (chunk_size=500, chunk_overlap=100).
- Built a Hugging Face embedding model and a FAISS vector store + retriever over the chunks.
- Built a `ChatPromptTemplate` with a system message (RAG instructions), a `MessagesPlaceholder` for chat history, and a human message for the current question.
- Built the full chain: question → retriever → context → prompt (with history) → LLM → answer.
- Maintained `chat_history` as a plain list of `HumanMessage`/`AIMessage` objects, appended to after every turn.
- Implemented history trimming with `trim_messages`, capping the conversation to the most recent N messages, and tested the trimming logic directly with a fake 8-message conversation (this part doesn't need the LLM, so it's genuinely verified, not just written).
- Tested the chatbot with a 3-turn conversation: an initial factual question, a follow-up that only makes sense with the previous answer in mind, and a clarification question.
- Wrapped everything into a single interactive chatbot loop for the mini project.

## Key Observations

Conversational RAG isn't a different retrieval mechanism - the retriever still works exactly the same way as plain RAG. What changes is the prompt: adding a `MessagesPlaceholder` gives the model access to what was already said, so it can resolve vague follow-ups instead of treating every question in isolation.

Trimming chat history is really just list management dressed up in LangChain's message types - `trim_messages` isn't doing anything conceptually different from slicing the last N items off a list, it just does it in a way that's aware of message roles.

## Challenges Faced

Same recurring issue as my last couple of assignments - the embedding model needs internet access to download the first time, and the LLM needs Ollama actually running locally. Both are handled with try/except so the notebook doesn't crash, but it does mean Task 9's multi-turn test could only be verified structurally (the right questions, in the right order) rather than confirming the answers were actually correct and context-aware end to end.

## Learning Outcomes

I learned that adding memory to a RAG chain doesn't require a completely different architecture - it's the same load/split/embed/retrieve pipeline as before, with one extra input (`chat_history`) threaded through the prompt. I also saw firsthand why trimming matters: without it, a long conversation would just keep growing the prompt sent to the LLM on every single turn, which doesn't scale.

## Submitted By

Abhishek Thakare
