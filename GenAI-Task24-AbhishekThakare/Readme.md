# Assignment 24 - Ollama Chatbot

## About the Project

For this assignment, I built a simple chatbot using a **local LLM with Ollama**.

Instead of sending prompts to a cloud-based LLM API, the model runs locally on my computer. I used **Llama 3** with **LangChain's `ChatOllama` wrapper** to connect my Python application to Ollama.

I also connected the application to **LangSmith** so that I could track and inspect the LLM calls made by the chatbot.

## What I Built

The project demonstrates:

* Running Llama 3 locally using Ollama
* Connecting Ollama with Python using LangChain
* Sending a prompt to the local LLM and displaying the response
* Creating a simple chatbot function
* Running an interactive terminal chatbot
* Tracking LLM calls using LangSmith

## Technologies Used

* **Python**
* **Ollama**
* **Llama 3**
* **LangChain**
* **LangSmith**
* **Jupyter Notebook**

## Project Structure

```text
GenAI-Task24-AbhishekThakare/
│
├── Assignment24_Ollama_Chatbot.ipynb
├── README.md
└── screenshots/
    └── langsmith_trace.png
```

## Setup

### 1. Install Ollama

Download and install Ollama from:

https://ollama.com/download

After installation, make sure Ollama is running.

### 2. Download the Llama 3 model

Open PowerShell or Command Prompt and run:

```bash
ollama pull llama3
```

I used Llama 3 for this assignment.

You can check the installed models with:

```bash
ollama list
```

### 3. Create and activate the Python virtual environment

From the project folder:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, the execution policy can be changed for the current user:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. Install the Python dependencies

With the virtual environment activated:

```bash
pip install langchain-ollama langsmith jupyter
```

## Running the Project

Open the notebook:

```bash
jupyter notebook
```

Then open:

```text
Assignment24_Ollama_Chatbot.ipynb
```

The notebook first connects LangChain to the locally running Llama 3 model using:

```python
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3",
    temperature=0.3
)
```

A simple prompt can then be sent using:

```python
response = llm.invoke("Your prompt here")
print(response.content)
```

The notebook also contains an interactive chatbot where I can keep entering questions until I type:

```text
exit
```

## LangSmith Tracing

I used **LangSmith** to monitor the LLM calls made by the application.

To enable tracing, I configured the following environment variables:

```python
import os
import getpass

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = getpass.getpass("LangSmith API key: ")
os.environ["LANGSMITH_PROJECT"] = "ollama-chatbot-assignment24"
```

The API key is entered at runtime instead of being written directly into the notebook.

After running a prompt, the corresponding run can be viewed in the LangSmith project.

The trace can be used to inspect details such as:

* Input prompt
* Model output
* Execution time / latency
* Run information

A screenshot of the LangSmith trace is included with the assignment submission.

## Important Note

The **LLM inference is local**.

The prompt is sent from the Python application to Ollama running on my computer, and Ollama runs the Llama 3 model locally.

LangSmith is used separately for **tracing and observability**.

Therefore, an OpenAI or Anthropic API key is not required for the actual LLM response.

Only the LangSmith API key is required if LangSmith tracing is enabled.

## What I Learned

Through this assignment, I learned how to:

1. Run an LLM locally using Ollama.
2. Connect a locally running model to a Python application.
3. Use LangChain's `ChatOllama` integration.
4. Build a basic interactive chatbot.
5. Use LangSmith to trace and monitor LLM calls.

This gave me a better understanding of how a local LLM application works from the model layer up to the application and observability layers.
