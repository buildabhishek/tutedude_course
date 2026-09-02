"""
astra_rag.py

Core logic for Assignment 37 - PDF Query RAG using AstraDB as the vector
store. Split out so the notebook and app.py share the same pipeline.

A hard fact about this assignment, upfront: AstraDB is DataStax's real cloud
service. Task 1 (create an account, create a database, generate a token and
endpoint) is a manual step in DataStax's own web console - there is no way
for me to do that on anyone's behalf, and no way to fake a working cloud
connection I was never actually granted. Everything in this file is real,
correct code that talks to AstraDB through the official `langchain-astradb`
integration; it only produces real output once real credentials from a real
account are in the environment.
"""

import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

load_dotenv()

RAG_SYSTEM_MESSAGE = (
    "You are a document Q&A assistant. Answer the question using ONLY the "
    "PDF context below - do not use outside knowledge. If the answer isn't "
    "in the context, say 'I don't know based on the PDF.' instead of "
    "guessing.\n\nContext:\n{context}"
)

rag_prompt = ChatPromptTemplate.from_messages([
    ("system", RAG_SYSTEM_MESSAGE),
    MessagesPlaceholder("chat_history"),
    ("human", "{question}"),
])

_embeddings = None
_llm = None


def get_embeddings():
    """Built lazily - this itself needs internet access to download the
    model on first use, so it can fail even before AstraDB enters the
    picture at all."""
    global _embeddings
    if _embeddings is None:
        from langchain_huggingface import HuggingFaceEmbeddings
        _embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return _embeddings


def get_llm(temperature: float = 0.2):
    global _llm
    if _llm is None:
        from langchain_ollama import ChatOllama
        _llm = ChatOllama(model="llama3.2", temperature=temperature)
    return _llm


# ---------------------------------------------------------------------------
# Task 3: Load & Split PDF Document
# ---------------------------------------------------------------------------
def load_and_split_pdf(path: str, chunk_size: int = 500, chunk_overlap: int = 100):
    docs = PyPDFLoader(path).load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(docs)


# ---------------------------------------------------------------------------
# Task 2 & 4: Connect to AstraDB + store embeddings
# ---------------------------------------------------------------------------
def get_astra_vectorstore(embeddings, collection_name: str = "pdf_rag_demo"):
    """Task 2: connects to AstraDB using a token + API endpoint read from
    the environment (never hardcoded). Requires a real DataStax AstraDB
    account, a real vector database created in it, and a real application
    token - see README.md for the exact console steps."""
    from langchain_astradb import AstraDBVectorStore

    token = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
    api_endpoint = os.getenv("ASTRA_DB_API_ENDPOINT")
    keyspace = os.getenv("ASTRA_DB_KEYSPACE", "default_keyspace")

    if not token or not api_endpoint:
        raise RuntimeError(
            "ASTRA_DB_APPLICATION_TOKEN and/or ASTRA_DB_API_ENDPOINT are not set. "
            "Add both to a .env file - see README.md for how to generate them "
            "from the AstraDB console."
        )

    return AstraDBVectorStore(
        embedding=embeddings,
        collection_name=collection_name,
        token=token,
        api_endpoint=api_endpoint,
        namespace=keyspace,
    )


def store_chunks(vectorstore, chunks) -> list:
    """Task 4: embed and upload the chunks, returning the inserted
    document IDs so persistence can actually be verified afterward."""
    return vectorstore.add_documents(chunks)


def verify_persistence(vectorstore, sample_query: str = "leave policy", k: int = 3):
    """Task 4: re-query AstraDB fresh (not from anything cached locally) to
    confirm the data genuinely persisted server-side."""
    return vectorstore.similarity_search(sample_query, k=k)


# ---------------------------------------------------------------------------
# Task 5: PDF Query RAG Application
# ---------------------------------------------------------------------------
def format_docs(docs) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


def build_rag_chain(retriever, llm=None):
    """PDF -> Splitter -> Embeddings -> AstraDB -> Retriever -> LLM -> Answer,
    with chat history threaded through the same way as my earlier
    conversational RAG assignments."""
    llm = llm or get_llm()
    context_step = RunnablePassthrough.assign(
        context=(lambda x: x["question"]) | retriever | RunnableLambda(format_docs)
    )
    return context_step | rag_prompt | llm | StrOutputParser()


if __name__ == "__main__":
    chunks = load_and_split_pdf("data/Employee_Handbook.pdf")
    print(f"Loaded and split into {len(chunks)} chunks.")

    embeddings = get_embeddings()
    vectorstore = get_astra_vectorstore(embeddings)
    store_chunks(vectorstore, chunks)

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    chain = build_rag_chain(retriever)
    print(chain.invoke({"question": "What is the leave policy?", "chat_history": []}))
