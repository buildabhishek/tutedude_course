import os

import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama

from prompts import build_prompt

load_dotenv()


st.set_page_config(
    page_title="CodeLlama Coding Assistant",
    page_icon="💻",
    layout="wide",
)


st.title("💻 CodeLlama Coding Assistant")
st.write(
    "A simple coding assistant for generating, explaining, debugging and optimizing code."
)


# Choose the LLM backend
groq_api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", "")
use_groq = bool(groq_api_key)


def get_llm():
    if use_groq:
        return ChatGroq(
            model="qwen/qwen3.8-27b",
            groq_api_key=groq_api_key,
            temperature=0,
        )

    return ChatOllama(
        model=os.getenv("OLLAMA_MODEL", "qwen/qwen3.8-27b"),
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        temperature=0,
    )


task_type = st.selectbox(
    "Select task",
    [
        "Generate Code",
        "Explain Code",
        "Debug Code",
        "Optimize Code",
    ],
)


user_input = st.text_area(
    "Enter your code or request",
    height=250,
    placeholder="Example: Write a Python function to check whether a number is prime.",
)


if st.button("Run Assistant", type="primary"):
    if not user_input.strip():
        st.warning("Please enter a code or request first.")
    else:
        prompt = build_prompt(task_type, user_input)

        with st.spinner("Generating response..."):
            try:
                llm = get_llm()
                response = llm.invoke(prompt)

                st.subheader("Assistant Response")
                st.code(response.content, language="python")

                if use_groq:
                    st.caption("Backend: Groq API")
                else:
                    st.caption("Backend: Local Ollama + CodeLlama")

            except Exception as e:
                st.error(f"Unable to generate a response: {e}")
