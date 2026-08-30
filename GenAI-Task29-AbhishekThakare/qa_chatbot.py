"""
qa_chatbot.py

Core logic for Assignment 29 - a plain Q&A chatbot (no RAG) that can run on
either OpenAI or Ollama. Both the notebook and app.py import from here so
there's one copy of the actual chat logic, not two.
"""

import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

OPENAI_MODEL = "gpt-4o-mini"
OLLAMA_MODEL = "llama3"

# Same prompt template used for both models, per Task 5 ("use the same
# prompt template as OpenAI").
qa_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful, general-purpose Q&A assistant. Answer clearly and directly."),
    MessagesPlaceholder("chat_history"),
    ("human", "{question}"),
])

_openai_llm = None
_ollama_llm = None


def get_openai_llm():
    """Built lazily so importing this file doesn't fail just because
    OPENAI_API_KEY isn't set - it only matters once something actually
    tries to call it."""
    global _openai_llm
    if _openai_llm is None:
        from langchain_openai import ChatOpenAI
        if not os.getenv("OPENAI_API_KEY"):
            os.environ["OPENAI_API_KEY"] = "sk-placeholder-no-real-credits"
        _openai_llm = ChatOpenAI(model=OPENAI_MODEL, temperature=0.3)
    return _openai_llm


def get_ollama_llm():
    global _ollama_llm
    if _ollama_llm is None:
        from langchain_ollama import ChatOllama
        _ollama_llm = ChatOllama(model=OLLAMA_MODEL, temperature=0.3)
    return _ollama_llm


def get_answer(question: str, model_type: str = "openai", chat_history=None) -> str:
    """Task 7: single entry point that routes to whichever model was asked
    for. chat_history is optional - pass a list of HumanMessage/AIMessage
    objects to get multi-turn behaviour (Task 3), or leave it as None for a
    plain one-off question."""
    if chat_history is None:
        chat_history = []

    if model_type == "openai":
        llm = get_openai_llm()
    elif model_type == "ollama":
        llm = get_ollama_llm()
    else:
        raise ValueError(f"Unknown model_type '{model_type}' - use 'openai' or 'ollama'.")

    chain = qa_prompt | llm | StrOutputParser()
    return chain.invoke({"question": question, "chat_history": chat_history})


if __name__ == "__main__":
    print(get_answer("What is LangChain, in one sentence?", model_type="openai"))
