# Assignment 31: Conversational PDF Q&A Chatbot with Message History

## Objective

Build a conversational RAG chatbot over PDF documents specifically - same message-history pattern as Assignment 28, but with `PyPDFLoader` doing the loading instead of plain text files.

## Project Structure

```text
Assignment-31/
├── Assignment31.ipynb
├── pdf_chat.py
├── README.md
├── requirements.txt
└── data/
    └── Employee_Handbook.pdf
```

`pdf_chat.py` holds the actual pipeline - loading, splitting, the retriever, the conversational chain, trimming, and a small `ConversationalPDFChatbot` class - so the notebook is testing the same code a real app would use.

## Input Files

`Employee_Handbook.pdf` - a proper 6-page PDF I put together for this assignment, combining the onboarding/leave/reimbursement/IT-support/code-of-conduct content from my earlier assignments into one actual document instead of scattered text files, specifically so there's a real PDF long enough to need chunking.

## Tasks Covered

1. Load PDF documents
2. Text splitting
3. Create embeddings
4. Vector store setup
5. RAG prompt template with message history
6. Build the conversational RAG chain
7. Maintain message history
8. Trim chat history
9. Follow-up Q&A testing
10. Build the final conversational PDF chatbot
11. Observations & insights

## Libraries Used

- LangChain (core, community, text splitters, huggingface, ollama)
- FAISS
- sentence-transformers
- pypdf

## LLM Note

Same as Assignment 25/28 - this assignment's restriction is "LangChain + any LLM," so with my OpenAI account still at zero usable credits, I'm using **Ollama running `llama3.2`** locally plus the same Hugging Face embedding model. Every retriever/chain cell fails gracefully with a clear message instead of crashing when Ollama or the embedding model isn't reachable - the logic itself doesn't change once either is available.

## Experiments Performed

- Built an actual multi-page PDF (`Employee_Handbook.pdf`) with reportlab, combining prior knowledge-base content into one real document, and confirmed `PyPDFLoader` reads it back correctly (6 pages, real text and metadata).
- Split the loaded PDF pages into chunks with `RecursiveCharacterTextSplitter`.
- Built a Hugging Face + FAISS retriever over the chunks.
- Built the conversational prompt template (system + `MessagesPlaceholder` + human) and confirmed it renders correctly.
- Built the full conversational RAG chain (retriever → PDF context → prompt + history → LLM → answer).
- Wrapped message history management and trimming into a `ConversationalPDFChatbot` class, and verified the trimming logic directly with a fake 8-message conversation (no LLM needed for that part, so it's genuinely confirmed working).
- Tested a 3-turn conversation: an initial factual question from the PDF, a follow-up that only makes sense with the previous answer in mind, and a clarification question.
- Wrapped everything into a simple interactive chatbot loop for the mini project.

## Key Observations

The retrieval pipeline is identical to Assignment 28's - `PyPDFLoader` just replaces `TextLoader`/`DirectoryLoader` as the entry point, and everything downstream (splitting, embedding, retrieving, the conversational chain) works exactly the same regardless of where the text originally came from.

Wrapping the chat history + trimming logic into a small class made it much easier to reuse the same conversation state across the trimming test, the multi-turn test, and the final chatbot loop, instead of managing a `chat_history` list by hand in three separate places.

## Challenges Faced

Same recurring dependency as my last few RAG assignments - the embedding model needs internet access to download the first time, and the LLM needs Ollama actually running locally. Both fail gracefully here, but it means Task 9's multi-turn test could only be verified structurally (the right questions, in the right order) rather than confirming the answers were genuinely grounded and context-aware end to end.

## Learning Outcomes

Building a real PDF for this (instead of reusing plain text files) made it obvious that the document format really doesn't matter to the rest of the pipeline - once `PyPDFLoader` hands off a list of `Document` objects, everything from that point on (splitting, embedding, retrieval, the conversational chain) is completely unaware of whether the original source was a `.txt` file or a PDF.

## Submitted By

Abhishek Thakare
