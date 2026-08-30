"""
app.py

Task 8: a simple CLI Q&A chatbot app. Lets the user pick a model (openai or
ollama) up front, or switch mid-conversation by typing "switch", and keeps
a running conversation history per model so follow-ups work.

Run with:  python app.py
"""

from langchain_core.messages import HumanMessage, AIMessage
from qa_chatbot import get_answer


def choose_model() -> str:
    while True:
        choice = input("Which model? (openai / ollama): ").strip().lower()
        if choice in ("openai", "ollama"):
            return choice
        print("Please type 'openai' or 'ollama'.")


def main():
    print("Simple Q&A Chatbot - no RAG, just plain conversation.")
    print("Type 'switch' anytime to change models, or 'exit' to quit.\n")

    model_type = choose_model()
    chat_history = []

    print(f"\nUsing {model_type}. Ask away.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            print("Bot: Goodbye!")
            break

        if user_input.lower() == "switch":
            model_type = choose_model()
            chat_history = []  # starting fresh since the two models don't share context
            print(f"\nSwitched to {model_type}. Conversation history reset.\n")
            continue

        if not user_input:
            continue

        try:
            answer = get_answer(user_input, model_type=model_type, chat_history=chat_history)
            chat_history.append(HumanMessage(content=user_input))
            chat_history.append(AIMessage(content=answer))
            print(f"Bot ({model_type}):", answer)
        except Exception as e:
            print(f"Bot ({model_type}): [Something went wrong - {e}]")

        print()


if __name__ == "__main__":
    main()
