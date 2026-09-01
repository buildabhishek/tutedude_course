"""
pdf_chat.py

Core logic for Assignment 31 - a conversational RAG chatbot over PDF
documents, with message history and trimming. Pulled into its own module so
the notebook isn't the only place this logic lives.
"""

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.messages import HumanMessage, AIMessage, trim_messages

PDF_SYSTEM_MESSAGE = (
    "You are a Conversational PDF Assistant. Answer the question using ONLY "
    "the PDF context below - do not use outside knowledge. If the answer "
    "isn't in the context, say 'I don't know based on the PDF.' instead of "
    "guessing.\n\nContext:\n{context}"
)

pdf_qa_prompt = ChatPromptTemplate.from_messages([
    ("system", PDF_SYSTEM_MESSAGE),
    MessagesPlaceholder("chat_history"),
    ("human", "{question}"),
])


def load_pdfs(paths) -> list:
    """Task 1: load one or more PDFs."""
    docs = []
    for path in paths:
        docs.extend(PyPDFLoader(path).load())
    return docs


def split_documents(docs, chunk_size: int = 500, chunk_overlap: int = 100):
    """Task 2: split PDF content into chunks."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(docs)


def build_retriever(paths, embeddings, k: int = 3):
    """Task 3 & 4: embed the chunks and store them in FAISS."""
    from langchain_community.vectorstores import FAISS

    docs = load_pdfs(paths)
    chunks = split_documents(docs)
    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": k})


def format_docs(docs) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


def build_conversational_chain(retriever, llm):
    """Task 6: User Question -> Retriever -> PDF Context -> Prompt + Message
    History -> LLM -> Answer."""
    context_step = RunnablePassthrough.assign(
        context=(lambda x: x["question"]) | retriever | RunnableLambda(format_docs)
    )
    return context_step | pdf_qa_prompt | llm | StrOutputParser()


def trim_history(history, max_messages: int = 6):
    """Task 8: keep only the most recent `max_messages` messages, oldest
    ones dropped first once the limit is passed."""
    return trim_messages(
        history,
        max_tokens=max_messages,
        token_counter=len,  # counting messages, not real tokens, for simplicity
        strategy="last",
        start_on="human",
    )


class ConversationalPDFChatbot:
    """Task 7 & 8 wrapped up together - keeps its own chat_history and trims
    it after every turn, so the notebook (or any app) doesn't have to manage
    that bookkeeping by hand."""

    def __init__(self, chain, max_history_messages: int = 6):
        self.chain = chain
        self.max_history_messages = max_history_messages
        self.chat_history = []

    def ask(self, question: str) -> str:
        answer = self.chain.invoke({"question": question, "chat_history": self.chat_history})
        self.chat_history.append(HumanMessage(content=question))
        self.chat_history.append(AIMessage(content=answer))
        self.chat_history = trim_history(self.chat_history, self.max_history_messages)
        return answer

    def reset(self):
        self.chat_history = []
