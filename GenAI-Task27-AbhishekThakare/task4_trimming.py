from memory import ConversationMemory


memory = ConversationMemory(max_messages=4)


print("Maximum messages:", memory.get_max_messages())


# Add five complete conversation turns.
for i in range(1, 6):
    memory.add_user_message(
        f"User question {i}"
    )

    memory.add_ai_message(
        f"Assistant answer {i}"
    )

    print(
        f"After turn {i}: "
        f"{memory.message_count()} messages"
    )


print("\n=== FINAL HISTORY ===")

for message in memory.get_messages():
    print(
        f"{type(message).__name__}: "
        f"{message.content}"
    )