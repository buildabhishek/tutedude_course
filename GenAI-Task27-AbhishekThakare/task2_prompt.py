import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)

load_dotenv()

llm = ChatGroq(
    model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0,
)


# ---------------------------------------------------------
# TASK 2: ChatPromptTemplate + MessagesPlaceholder
# ---------------------------------------------------------

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful and concise Python tutor."
        ),
        MessagesPlaceholder(variable_name="history"),
        (
            "human",
            "{question}"
        ),
    ]
)


# Simulated previous conversation
history = [
    HumanMessage(
        content="What is a Python list?"
    ),
    AIMessage(
        content=(
            "A Python list is an ordered and mutable "
            "collection of items."
        )
    ),
    HumanMessage(
        content="Can you give me an example?"
    ),
    AIMessage(
        content=(
            'Sure. For example: fruits = '
            '["apple", "banana", "cherry"]'
        )
    ),
]


current_question = "How do I add another fruit?"


# Build the final message sequence
messages = prompt.format_messages(
    history=history,
    question=current_question,
)


print("=== FINAL MESSAGE SEQUENCE ===")

for message in messages:
    print(f"{type(message).__name__}:")
    print(message.content)
    print()


print("=== GROQ RESPONSE ===")

response = llm.invoke(messages)

print(response.content)