# Assignment 27 — Stateful Groq Chatbot with LangChain Memory

## Overview

This project demonstrates how to build a **stateful conversational chatbot** using the Groq API and LangChain message abstractions.

Unlike a stateless LLM call, where every question is treated independently, this chatbot maintains conversation history and sends relevant previous messages along with the current question.

The project also demonstrates how to control memory growth by trimming older conversation history after a configurable limit.

---

## Objectives

The main objectives of this assignment are to:

- Understand LangChain message types.
- Work with `SystemMessage`, `HumanMessage`, and `AIMessage`.
- Construct structured conversational prompts.
- Maintain conversation history across multiple interactions.
- Implement reusable conversation memory.
- Limit conversation history using message trimming.
- Build a stateful interactive chatbot using the Groq API.
- Configure API credentials and model names using environment variables.
- Handle API configuration errors cleanly.

---

## Technologies Used

- **Python 3.11**
- **Groq API**
- **LangChain Core**
- **python-dotenv**
- **PowerShell** for local testing

---

## Project Structure

```text
GenAI-Task27-AbhishekThakare/
│
├── Assignment27.ipynb       # Main assignment notebook
│
├── task1_messages.py        # Task 1: LangChain message types
├── task2_prompt.py          # Task 2: Structured prompt construction
├── memory.py                # Reusable conversation memory
├── task3_memory.py          # Task 3: Conversation memory demonstration
├── task4_trimming.py        # Task 4: Conversation history trimming
├── chatbot.py               # Stateful Groq chatbot
│
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
├── .gitignore               # Files excluded from version control
├── README.md                # Project documentation
│
└── data/

```


# Setup

## 1. Create or open the project directory

```powershell
cd C:\Users\abhis\Desktop\Tutedude_Course\GenAI-Task27-AbhishekThakare
```

## 2. Install dependencies

Install the required Python packages:

```powershell
pip install -r requirements.txt
```

The project uses:

```text
groq
langchain-core
python-dotenv
```

---

## 3. Configure environment variables

Create a `.env` file in the project root.

Example:

```text
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
```

The `.env.example` file is provided as a template.

> **Security:** The actual `.env` file contains the API key and must never be committed to GitHub or included in the final public repository.

---

# Assignment Tasks

## Task 1 — LangChain Message Types

**File:** `task1_messages.py`

This task demonstrates the basic LangChain message abstractions used to represent a conversation.

The implementation uses:

* `SystemMessage`
* `HumanMessage`
* `AIMessage`

A conversation can therefore be represented as a sequence such as:

```text
SystemMessage
      ↓
HumanMessage
      ↓
AIMessage
      ↓
HumanMessage
      ↓
AIMessage
```

The message sequence is then passed to the Groq-powered chatbot.

### Example

```text
SystemMessage:
You are a helpful Python tutor.

HumanMessage:
What is a Python list?

AIMessage:
A Python list is an ordered and mutable collection of items.

HumanMessage:
Can you give me a simple example?
```

This demonstrates how conversational context can be represented explicitly instead of sending only a single string prompt.

---

# Task 2 — Structured Prompt Construction

**File:** `task2_prompt.py`

This task demonstrates how a structured conversation can be constructed using LangChain message objects.

The conversation contains:

1. System instructions
2. Previous user questions
3. Previous assistant answers
4. The current user question

Example:

```text
SystemMessage:
You are a helpful and concise Python tutor.

HumanMessage:
What is a Python list?

AIMessage:
A Python list is an ordered and mutable collection of items.

HumanMessage:
Can you give me an example?

AIMessage:
Sure. For example: fruits = ["apple", "banana", "cherry"]

HumanMessage:
How do I add another fruit?
```

The complete message sequence is sent to Groq so the model can answer the current question using the previous conversation context.

---

# Task 3 — Conversation Memory

**File:** `memory.py`

**Demonstration:** `task3_memory.py`

This task introduces reusable conversation memory.

The memory stores messages using:

```python
HumanMessage
AIMessage
```

A typical conversation is stored as:

```text
HumanMessage → AIMessage
HumanMessage → AIMessage
HumanMessage → AIMessage
```

The memory class provides functionality for:

* Adding user messages.
* Adding assistant responses.
* Retrieving stored messages.
* Counting stored messages.
* Counting conversation turns.
* Clearing the conversation.
* Limiting the maximum number of stored messages.

### Example output

```text
Initial message count: 0

=== STORED CONVERSATION ===

HumanMessage:
What is a Python list?

AIMessage:
A Python list is an ordered and mutable collection.

HumanMessage:
Can you give me an example?

AIMessage:
Example: fruits = ["apple", "banana", "cherry"]

Final message count: 4
```

This demonstrates that conversation state can be maintained separately from the LLM itself.

---

# Task 4 — Conversation History Trimming

**File:** `task4_trimming.py`

Long conversations can continuously increase the amount of context sent to an LLM.

To prevent uncontrolled memory growth, the project implements a configurable maximum number of stored messages.

For example, with a maximum of four messages:

```text
Maximum messages: 4

After turn 1: 2 messages
After turn 2: 4 messages
After turn 3: 4 messages
After turn 4: 4 messages
After turn 5: 4 messages
```

The final history contains only the most recent complete conversation turns:

```text
HumanMessage:
User question 4

AIMessage:
Assistant answer 4

HumanMessage:
User question 5

AIMessage:
Assistant answer 5
```

This confirms that older conversation history is removed when the configured limit is exceeded.

### Why trimming matters

Without trimming:

```text
Conversation
    ↓
More messages
    ↓
More context
    ↓
Higher token usage
    ↓
Potentially slower / more expensive requests
```

With trimming:

```text
Conversation
    ↓
Controlled history
    ↓
Relevant recent context
    ↓
Predictable memory usage
```

---

# Task 5 — Stateful Groq Chatbot

**File:** `chatbot.py`

The final chatbot combines the concepts from the previous tasks.

It provides:

* Groq API integration.
* LangChain message objects.
* Conversation memory.
* Stateful interactions.
* Conversation history trimming.
* Environment-based configuration.

Run the chatbot with:

```powershell
python chatbot.py
```

The application starts an interactive conversation:

```text
=== STATEFUL GROQ CHATBOT ===
Type 'exit' to stop.

You:
```

The user can ask multiple questions without restarting the program.

To stop the chatbot:

```text
exit
```

---

# Example Conversation

The chatbot can maintain context across multiple questions:

```text
You: Explain Python lists.

Assistant: Python lists are ordered and mutable collections...

You: Give me a simple example.

Assistant: Here is a simple example...

You: How can I add an item to it?

Assistant: You can use list.append()...

You: What if I want to add multiple items?

Assistant: You can use list.extend()...
```

The important point is that later questions are processed as part of the same conversation rather than as completely independent requests.

---

# Conversation Architecture

The overall flow of the chatbot is:

```text
                 User
                  │
                  ▼
          Current Question
                  │
                  ▼
       Conversation Memory
                  │
                  ▼
       Previous Messages
                  │
                  ▼
        LangChain Messages
                  │
                  ▼
             Groq API
                  │
                  ▼
          Assistant Answer
                  │
                  ▼
        Store New AI Message
                  │
                  ▼
        Trim Old History
                  │
                  └──────────► Next Turn
```

This creates a stateful conversational loop.

---

# Memory Management

The chatbot maintains two types of conversational messages:

```text
HumanMessage
AIMessage
```

Each interaction therefore represents a complete conversation turn:

```text
HumanMessage
     +
AIMessage
```

The memory implementation can restrict the maximum number of stored messages.

For example:

```text
Maximum messages = 4
```

allows:

```text
Turn 1 → Human + AI
Turn 2 → Human + AI
```

while older turns are removed when additional messages are added.

This keeps the amount of conversational context bounded.

---

# Model Configuration

The model name is configured through the `.env` file:

```text
GROQ_MODEL=openai/gpt-oss-120b
```

The application does not need to hard-code the model name.

This makes it easier to change the model configuration without modifying the Python source code.

For example:

```text
Environment
    ↓
GROQ_MODEL
    ↓
Python application
    ↓
Groq client
```

---

# API Key Handling

The Groq API key is loaded from the environment:

```text
GROQ_API_KEY
```

The actual API key is not stored directly in the Python source code.

The project also includes:

```text
.env.example
```

which provides a safe template for configuration.

The `.gitignore` file excludes:

```text
.env
```

to reduce the risk of accidentally committing credentials.

---

# Error Handling

The chatbot checks for the required Groq API configuration before making API requests.

If the API key is unavailable, the application reports a configuration error rather than continuing with an invalid API request.

This makes configuration problems easier to identify during local development.

---

# Testing Performed

The following tests were performed during development.

## Message History Test

Verified that:

* `SystemMessage` is created correctly.
* `HumanMessage` is stored correctly.
* `AIMessage` is stored correctly.
* A complete message sequence can be sent to Groq.

---

## Prompt Construction Test

Verified that:

* System instructions are included.
* Previous conversation turns are included.
* The current user question is included.
* Groq receives the resulting conversational message sequence.

---

## Memory Test

Verified that:

```text
Initial message count: 0
```

increases as messages are added and that both user and assistant messages are stored.

---

## Trimming Test

Verified that the configured maximum history size is respected.

Example:

```text
Maximum messages: 4
After turn 1: 2 messages
After turn 2: 4 messages
After turn 3: 4 messages
After turn 4: 4 messages
After turn 5: 4 messages
```

---

## Stateful Chatbot Test

The chatbot was tested using a multi-turn conversation involving:

* Python lists
* List examples
* Adding items
* Adding multiple items

The chatbot successfully maintained conversation context across multiple interactions.

---

# Key Observations

## 1. Stateless vs Stateful LLM Calls

A stateless request treats every question independently:

```text
Question 1 → LLM
Question 2 → LLM
Question 3 → LLM
```

A stateful chatbot maintains the conversation:

```text
Question 1
    ↓
Answer 1
    ↓
Question 2 + Previous History
    ↓
Answer 2
    ↓
Question 3 + Previous History
    ↓
Answer 3
```

This allows follow-up questions to be understood in context.

---

## 2. Conversation Memory Is Application State

The LLM itself does not automatically remember previous requests.

The application is responsible for:

1. Storing previous messages.
2. Selecting which messages should be retained.
3. Sending the selected history with the next request.

Therefore, conversation memory is an important part of the application architecture.

---

## 3. History Trimming Controls Context Growth

Conversation history can grow continuously during a long session.

Trimming provides a simple mechanism for keeping the context bounded.

This improves predictability and prevents unnecessary accumulation of old messages.

---

## 4. Environment Variables Improve Configuration

Keeping configuration such as:

```text
GROQ_API_KEY
GROQ_MODEL
```

outside the source code makes the application easier and safer to configure.

---

# Challenges Faced

One practical challenge was ensuring that the chatbot's conversation memory remained synchronized with the messages sent to Groq.

Another important consideration was controlling conversation history growth. A chatbot that continuously stores every message can eventually accumulate a large amount of context, so a trimming mechanism was implemented.

The Groq model configuration was also made environment-based so that the application does not depend on a single hard-coded model name.

---

# Learning Outcomes

Through this assignment, I learned how to:

* Work with LangChain message abstractions.
* Use `SystemMessage`, `HumanMessage`, and `AIMessage`.
* Build structured conversational prompts.
* Maintain state across multiple LLM interactions.
* Implement reusable conversation memory.
* Trim conversation history.
* Build a stateful chatbot using the Groq API.
* Load configuration using environment variables.
* Protect API credentials using `.gitignore`.
* Separate chatbot logic from configuration.
* Understand the difference between stateless and stateful LLM applications.

---

# How to Run

## Install dependencies

```powershell
pip install -r requirements.txt
```

## Configure `.env`

```text
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
```

## Run individual demonstrations

### Task 1

```powershell
python task1_messages.py
```

### Task 2

```powershell
python task2_prompt.py
```

### Task 3

```powershell
python task3_memory.py
```

### Task 4

```powershell
python task4_trimming.py
```

### Task 5

```powershell
python chatbot.py
```

---

# Security Note

Do **not** share or commit the `.env` file.

The following should remain private:

```text
GROQ_API_KEY
```

Only `.env.example` should be included in a public repository or submission package.

---

# Conclusion

This assignment demonstrates how a basic LLM API call can be transformed into a stateful conversational application.

The key progression is:

```text
LLM API
   ↓
LangChain Messages
   ↓
Conversation History
   ↓
Memory Management
   ↓
History Trimming
   ↓
Stateful Chatbot
```

The project provides a practical foundation for more advanced conversational AI applications where maintaining context across multiple user interactions is required.

---

## Submitted By

**Abhishek Thakare**
