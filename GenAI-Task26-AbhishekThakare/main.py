"""
main.py

The actual backend service. Two endpoints - a health check, and a /chat
endpoint that answers using RAG if the vector store built okay at startup,
otherwise just falls back to a plain Groq call.
"""

import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from groq_chatbot import groq_chat
from rag import build_retriever, rag_answer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("groq-chatbot-api")

app = FastAPI(title="Groq Chatbot API", version="1.0.0")

retriever = None


@app.on_event("startup")
def startup_event():
    """Try to build the RAG retriever once when the app starts, instead of
    on every single request. If it fails (missing data files, embedding
    model not available, whatever) the API still comes up - it just answers
    without RAG instead of refusing to start."""
    global retriever
    try:
        retriever = build_retriever()
        logger.info("Vector store built - /chat will use RAG.")
    except Exception as e:
        logger.warning(f"Couldn't build the retriever, RAG is disabled for this run: {e}")
        retriever = None


class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, description="The user's question")


class ChatResponse(BaseModel):
    answer: str


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        if retriever is not None:
            answer = rag_answer(request.query, retriever)
        else:
            answer = groq_chat(request.query)
        return ChatResponse(answer=answer)

    except RuntimeError as e:
        # this is the "GROQ_API_KEY not set" case from groq_chatbot.py -
        # a config problem, not something the caller did wrong
        logger.error(f"Config error on /chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        # anything else (Groq being down, rate limited, network hiccup) -
        # surface it as a clean 502 instead of a raw traceback
        logger.error(f"Groq request failed: {e}")
        raise HTTPException(status_code=502, detail=f"Upstream Groq request failed: {e}")
