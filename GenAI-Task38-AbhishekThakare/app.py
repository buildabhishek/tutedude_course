import os

import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama


MODEL_NAME = os.getenv("OLLAMA_MODEL", "codellama:7b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")


PROMPTS = {
    "Generate Code": """
You are a practical coding assistant.

Write a complete solution for the user's request.
Requirements:
- Use clear, beginner-friendly Python unless the user asks for another language.
- Return runnable code.
- Keep the solution simple and avoid unnecessary libraries.
- Briefly explain how to run it after the code.

User request:
{user_input}
""",
    "Explain Code": """
You are helping a developer understand code.

Explain the code below in simple technical language.
Cover:
1. What the code does
2. How the main parts work
3. Important Python concepts used
4. Any assumptions or limitations

Code or question:
{user_input}
""",
    "Debug Code": """
You are a careful debugging assistant.

Review the code/problem below.
1. Identify the likely error or bug.
2. Explain why it happens.
3. Provide the corrected code.
4. Mention any edge cases worth checking.

Code or problem:
{user_input}
""",
    "Optimize Code": """
You are a code review assistant.

Review the code below and suggest practical improvements.
Focus on:
- readability
- unnecessary work
- error handling
- maintainability
- performance where it actually matters

Show an improved version of the code and explain the main changes.

Code:
{user_input}
""",
}


@st.cache_resource
def get_llm():
    return ChatOllama(
        model=MODEL_NAME,
        base_url=OLLAMA_BASE_URL,
        temperature=0.2,
    )


def build_prompt(task_type: str, user_input: str) -> str:
    template = PromptTemplate.from_template(PROMPTS[task_type])
    return template.format(user_input=user_input)


def ask_ollama(task_type: str, user_input: str) -> str:
    prompt = build_prompt(task_type, user_input)
    llm = get_llm()
    response = llm.invoke(prompt)
    return response.content


st.set_page_config(
    page_title="CodeLlama Coding Assistant",
    page_icon="💻",
    layout="wide",
)

st.title("💻 CodeLlama Coding Assistant")
st.caption("A small local coding assistant built with Streamlit, LangChain and Ollama.")

with st.sidebar:
    st.header("Task")
    task_type = st.selectbox(
        "What would you like CodeLlama to do?",
        list(PROMPTS.keys()),
    )

    st.markdown("---")
    st.write(f"**Model:** `{MODEL_NAME}`")
    st.write(f"**Ollama:** `{OLLAMA_BASE_URL}`")

st.subheader(task_type)

placeholders = {
    "Generate Code": "Example: Write a Python function that checks whether a number is prime.",
    "Explain Code": "Paste the code you want explained here.",
    "Debug Code": "Paste the code and include the error message if you have one.",
    "Optimize Code": "Paste the code you want to improve here.",
}

user_input = st.text_area(
    "Enter your request or code",
    height=280,
    placeholder=placeholders[task_type],
)

if st.button("Run CodeLlama", type="primary"):
    if not user_input.strip():
        st.warning("Please enter a request or some code first.")
    else:
        with st.spinner("CodeLlama is working..."):
            try:
                answer = ask_ollama(task_type, user_input)
                st.subheader("Response")
                st.markdown(answer)
            except Exception as exc:
                st.error(
                    "I could not connect to Ollama. Make sure Ollama is running "
                    "and the selected model has been pulled."
                )
                st.code(str(exc))
                st.info(
                    f"Try: `ollama pull {MODEL_NAME}` and then start Ollama again."
                )
