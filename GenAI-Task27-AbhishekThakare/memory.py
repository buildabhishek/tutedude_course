from langchain_core.messages import HumanMessage, AIMessage


class ConversationMemory:
    """
    Manage conversation history while keeping complete
    Human + AI conversation turns.
    """

    def __init__(self, max_messages: int = 8):
        if max_messages < 2:
            raise ValueError(
                "max_messages must be at least 2."
            )

        if max_messages % 2 != 0:
            raise ValueError(
                "max_messages must be an even number."
            )

        self.max_messages = max_messages
        self.messages = []

    def add_user_message(self, message: str):
        """Store a user message."""
        self.messages.append(
            HumanMessage(content=message)
        )

    def add_ai_message(self, message: str):
        """Store an assistant response and trim history."""
        self.messages.append(
            AIMessage(content=message)
        )
        self._trim_history()

    def _trim_history(self):
        """
        Keep only the most recent complete conversation turns.
        """
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def get_messages(self):
        """Return a copy of the conversation history."""
        return self.messages.copy()

    def clear(self):
        """Clear all conversation history."""
        self.messages.clear()

    def message_count(self):
        """Return the number of stored messages."""
        return len(self.messages)

    def turn_count(self):
        """Return the number of complete conversation turns."""
        return len(self.messages) // 2

    def get_max_messages(self):
        """Return the configured message limit."""
        return self.max_messages