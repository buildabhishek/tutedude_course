import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)

from memory import ConversationMemory


load_dotenv()


class StatefulChatbot:
    """Groq chatbot with conversation history."""

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        model = os.getenv(
            "GROQ_MODEL",
            "openai/gpt-oss-120b"
        )

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY is not set. "
                "Please add it to your .env file."
            )

        self.llm = ChatGroq(
            model=model,
            api_key=api_key,
            temperature=0,
        )

        self.memory = ConversationMemory()

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        "You are a helpful and concise AI assistant. "
                        "Use the conversation history to understand "
                        "follow-up questions and maintain context."
                    ),
                ),
                MessagesPlaceholder(
                    variable_name="history"
                ),
                (
                    "human",
                    "{question}"
                ),
            ]
        )

    def chat(self, question: str) -> str:
        """
        Send a question using the existing conversation history,
        then store both the question and the AI response.
        """

        question = question.strip()

        if not question:
            raise ValueError(
                "Question cannot be empty."
            )

        messages = self.prompt.format_messages(
            history=self.memory.get_messages(),
            question=question,
        )

        response = self.llm.invoke(messages)

        answer = response.content

        self.memory.add_user_message(question)
        self.memory.add_ai_message(answer)

        return answer

    def get_history(self):
        """Return the current conversation history."""
        return self.memory.get_messages()

    def clear_history(self):
        """Clear the current conversation."""
        self.memory.clear()

    def history_count(self):
        """Return the number of stored messages."""
        return self.memory.message_count()


if __name__ == "__main__":
    chatbot = StatefulChatbot()

    print("=== STATEFUL GROQ CHATBOT ===")
    print("Type 'exit' to stop.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() == "exit":
            print("Goodbye!")
            break

        try:
            answer = chatbot.chat(question)

            print(f"\nAssistant: {answer}\n")

            print(
                f"[History: "
                f"{chatbot.history_count()} messages]\n"
            )

        except Exception as exc:
            print(f"\nError: {exc}\n")