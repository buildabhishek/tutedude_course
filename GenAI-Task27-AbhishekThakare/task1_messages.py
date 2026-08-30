import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
)

load_dotenv()

llm = ChatGroq(
    model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0,
)

messages = [
    SystemMessage(
        content="You are a helpful Python tutor."
    ),
    HumanMessage(
        content="What is a Python list?"
    ),
    AIMessage(
        content=(
            "A Python list is an ordered, mutable collection "
            "that can store multiple values."
        )
    ),
    HumanMessage(
        content="Can you give me a simple example?"
    ),
]

print("=== MESSAGE HISTORY ===")

for message in messages:
    print(f"{type(message).__name__}:")
    print(message.content)
    print()

print("=== GROQ RESPONSE ===")

response = llm.invoke(messages)

print(response.content)
