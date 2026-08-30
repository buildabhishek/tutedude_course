"""
rag_groq.py

Core RAG logic for Assignment 30 - load/split/embed/retrieve, plus the
ChatGroq-backed answering chain with message history. Both the notebook and
app.py import from here, so there's one copy of the actual pipeline instead
of the Streamlit app and the notebook drifting apart.
"""

import os
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

load_dotenv()

GROQ_MODEL = "llama-3.3-70b-versatile"

RAG_SYSTEM_MESSAGE = (
    "You are a fast, grounded document Q&A assistant powered by Groq. Answer "
    "the question using ONLY the context below - do not use outside "
    "knowledge. If the answer isn't in the context, say 'I don't know based "
    "on the documents provided.' instead of guessing.\n\nContext:\n{context}"
)

rag_prompt = ChatPromptTemplate.from_messages([
    ("system", RAG_SYSTEM_MESSAGE),
    MessagesPlaceholder("chat_history"),
    ("human", "{question}"),
])


def get_llm(temperature: float = 0.3):
    """Built lazily so importing this file doesn't blow up just because
    GROQ_API_KEY isn't set yet - it only matters once something calls it."""
    from langchain_groq import ChatGroq

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Add it to a .env file or export it "
            "before running this."
        )
    return ChatGroq(model=GROQ_MODEL, api_key=api_key, temperature=temperature)


def load_documents(paths) -> list:
    """Task 3: load PDF or text files - whichever this file happens to be,
    picked based on the extension."""
    docs = []
    for path in paths:
        if path.lower().endswith(".pdf"):
            docs.extend(PyPDFLoader(path).load())
        else:
            docs.extend(TextLoader(path).load())
    return docs


def split_documents(docs, chunk_size: int = 500, chunk_overlap: int = 100):
    """Task 3: split into chunks small enough to embed and retrieve cleanly."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(docs)


def build_retriever(paths, k: int = 3):
    """Task 4: embed the chunks and store them in FAISS, then return a
    retriever ready to plug into the RAG chain."""
    docs = load_documents(paths)
    chunks = split_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embeddings)

    return vectorstore.as_retriever(search_kwargs={"k": k})


def format_docs(docs) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


def build_rag_chain(retriever):
    """Task 6: User Question -> Retriever -> Context -> Prompt -> ChatGroq -> Answer,
    with chat_history threaded through so follow-ups work."""
    llm = get_llm()
    context_step = RunnablePassthrough.assign(
        context=(lambda x: x["question"]) | retriever | RunnableLambda(format_docs)
    )
    return context_step | rag_prompt | llm | StrOutputParser()


if __name__ == "__main__":
    r = build_retriever(["data/notes.txt", "data/policies.txt"])
    chain = build_rag_chain(r)
    print(chain.invoke({"question": "What is the leave policy?", "chat_history": []}))
