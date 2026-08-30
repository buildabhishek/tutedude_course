"""
rag.py

Optional RAG layer on top of groq_chatbot.py. Reusing the same onboarding
notes + FAQ csv from the last couple of assignments, and the same
Hugging Face + FAISS combo since that one doesn't need an API key.
"""

from langchain_community.document_loaders import TextLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from groq_chatbot import groq_chat

RAG_SYSTEM_MESSAGE = (
    "You are the Personal Knowledge Assistant for new employees. Answer the "
    "question using ONLY the context provided. If the answer isn't in the "
    "context, say you don't know instead of guessing."
)

RAG_PROMPT_TEMPLATE = """Context:
{context}

Question: {question}
Answer:"""


def build_retriever(data_dir: str = "data", k: int = 3):
    """Load -> split -> embed -> store, same pipeline as Assignment 22/25."""
    docs = TextLoader(f"{data_dir}/notes.txt").load()
    docs += CSVLoader(f"{data_dir}/data.csv").load()

    chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100).split_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embeddings)

    return vectorstore.as_retriever(search_kwargs={"k": k})


def rag_answer(question: str, retriever) -> str:
    """Task 3 + 4: retrieve context, drop it into the structured prompt
    template, and pass the whole thing to Groq."""
    retrieved_docs = retriever.invoke(question)
    context = "\n\n".join(doc.page_content for doc in retrieved_docs)

    prompt = RAG_PROMPT_TEMPLATE.format(context=context, question=question)
    return groq_chat(prompt, system=RAG_SYSTEM_MESSAGE)


if __name__ == "__main__":
    r = build_retriever()
    print(rag_answer("What is the leave policy?", r))
