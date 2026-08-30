from memory import ConversationMemory


memory = ConversationMemory()

print("Initial message count:", memory.message_count())


memory.add_user_message(
    "What is a Python list?"
)

memory.add_ai_message(
    "A Python list is an ordered and mutable collection."
)


memory.add_user_message(
    "Can you give me an example?"
)

memory.add_ai_message(
    'Example: fruits = ["apple", "banana", "cherry"]'
)


print("\n=== STORED CONVERSATION ===")

for message in memory.get_messages():
    print(f"{type(message).__name__}:")
    print(message.content)
    print()


print(
    "Final message count:",
    memory.message_count()
)