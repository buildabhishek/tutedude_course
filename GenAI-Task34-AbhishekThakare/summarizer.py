"""
summarizer.py

Core logic for Assignment 34 - four different summarization strategies
(prompt-based, stuff, map-reduce, refine) over the same long article, plus a
unified summarize_document() function to switch between them.

A quick note on versions: `load_summarize_chain` (used for the stuff,
map-reduce, and refine chains) lives in LangChain's older "legacy chains" API
and was removed when LangChain hit 1.0. This file - and requirements.txt -
deliberately pin to langchain==0.3.27 / langchain-community==0.3.27 so this
exact API is available, since that's what the assignment asks for by name.
"""

import os
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 150

_llm = None


def get_llm(temperature: float = 0.2):
    """Built lazily so importing this file doesn't fail just because
    Ollama isn't running yet - only matters once something actually calls it."""
    global _llm
    if _llm is None:
        from langchain_ollama import ChatOllama
        _llm = ChatOllama(model="llama3.2", temperature=temperature)
    return _llm


def load_text(path: str) -> str:
    """Task 1: load the raw text (plain read - the assignment allows manual
    loading as an alternative to a LangChain document loader for this part)."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def build_documents(text: str, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP):
    """Split raw text into LangChain Document chunks - needed for the stuff /
    map-reduce / refine chains, which all expect a list of Documents rather
    than a single string."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_text(text)
    return [Document(page_content=chunk) for chunk in chunks]


# ---------------------------------------------------------------------------
# Task 2 & 3: Prompt-based summarization (plain PromptTemplate + LLM, no
# chain abstraction at all)
# ---------------------------------------------------------------------------
short_summary_prompt = PromptTemplate(
    input_variables=["text"],
    template=(
        "You are an expert summarizer. Summarize the following text in "
        "5-6 lines, capturing only the most important points.\n\n"
        "Text:\n{text}\n\nSummary:"
    ),
)

bullet_summary_prompt = PromptTemplate(
    input_variables=["text"],
    template=(
        "You are an expert summarizer. Summarize the following text as a "
        "concise bulleted list of the key points (5-8 bullets).\n\n"
        "Text:\n{text}\n\nBullet-point summary:"
    ),
)


def summarize_with_prompt(text: str, style: str = "short", llm=None) -> str:
    """Task 2 & 3: a plain prompt-based summary, no summarization chain
    involved - just PromptTemplate -> LLM -> output."""
    llm = llm or get_llm()
    prompt = short_summary_prompt if style == "short" else bullet_summary_prompt
    chain = prompt | llm
    return chain.invoke({"text": text}).content


# ---------------------------------------------------------------------------
# Task 5: Stuff summarization chain
# ---------------------------------------------------------------------------
def summarize_stuff(docs, llm=None) -> str:
    llm = llm or get_llm()
    chain = load_summarize_chain(llm, chain_type="stuff")
    return chain.invoke(docs)["output_text"]


# ---------------------------------------------------------------------------
# Task 8 & 9: Map-Reduce summarization chain
# ---------------------------------------------------------------------------
def summarize_map_reduce(docs, llm=None, return_intermediate_steps: bool = False):
    llm = llm or get_llm()
    chain = load_summarize_chain(
        llm, chain_type="map_reduce", return_intermediate_steps=return_intermediate_steps
    )
    result = chain.invoke(docs)
    if return_intermediate_steps:
        return result["output_text"], result["intermediate_steps"]
    return result["output_text"]


# ---------------------------------------------------------------------------
# Task 11: Refine summarization chain
# ---------------------------------------------------------------------------
def summarize_refine(docs, llm=None) -> str:
    llm = llm or get_llm()
    chain = load_summarize_chain(llm, chain_type="refine")
    return chain.invoke(docs)["output_text"]


# ---------------------------------------------------------------------------
# Task 13: unified, reusable entry point
# ---------------------------------------------------------------------------
def summarize_document(text: str, method: str = "map_reduce", llm=None) -> str:
    """Switch between 'prompt', 'stuff', 'map_reduce', and 'refine' from one
    place, so callers don't need to know which chain-building function to
    call for a given method."""
    llm = llm or get_llm()

    if method == "prompt":
        return summarize_with_prompt(text, style="short", llm=llm)

    docs = build_documents(text)

    if method == "stuff":
        return summarize_stuff(docs, llm=llm)
    elif method == "map_reduce":
        return summarize_map_reduce(docs, llm=llm)
    elif method == "refine":
        return summarize_refine(docs, llm=llm)
    else:
        raise ValueError(f"Unknown method '{method}' - use 'prompt', 'stuff', 'map_reduce', or 'refine'.")


if __name__ == "__main__":
    article = load_text("data/long_article.txt")
    print(summarize_document(article, method="map_reduce"))
