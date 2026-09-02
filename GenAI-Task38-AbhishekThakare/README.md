# Assignment 38: CodeLlama with Ollama

**Student:** Abhishek Thakare

## Problem Statement

This project is a small coding assistant that runs through Ollama and uses CodeLlama for the actual language-model response.

The application can:

- Generate Python code
- Explain code
- Debug code
- Suggest code improvements

The interface is built with Streamlit so the model can be used through a simple browser page.

## What I Built

The flow is:

`User input -> Prompt template -> LangChain -> Ollama -> CodeLlama -> Streamlit response`

I kept the project intentionally small. The main point of the assignment is to understand how a locally running model can be connected to an application rather than hiding the model call behind a large framework.

## Project Structure

```text
GenAI-Task38-AbhishekThakare/
├── app.py
├── prompts.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── tests/
    └── test_prompts.py
```

## Prerequisites

1. Python 3.10 or newer
2. Ollama installed and running
3. CodeLlama pulled locally

Install CodeLlama:

```powershell
ollama pull codellama:7b
```

Check the installed model:

```powershell
ollama list
```

## Installation

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Install the Python packages:

```powershell
pip install -r requirements.txt
```

## Run the Application

Make sure Ollama is running, then:

```powershell
streamlit run app.py
```

Open the local Streamlit URL shown in the terminal.

## Task 1: Set Up Ollama

The application expects:

```text
Ollama -> codellama:7b
```

The default Ollama endpoint is:

```text
http://localhost:11434
```

The model name and endpoint can also be changed with environment variables:

```text
OLLAMA_MODEL
OLLAMA_BASE_URL
```

## Task 2: Basic CodeLlama Interaction

The application uses `ChatOllama` from `langchain-ollama`.

For example, selecting **Generate Code** and entering:

```text
Write a Python function that checks whether a number is prime.
```

sends a structured prompt to CodeLlama and displays the returned response in Streamlit.

## Task 3: Code Assistant Features

### 1. Generate Code

Creates a runnable solution from a natural-language request.

### 2. Explain Code

Breaks down what a supplied code snippet is doing and points out the important concepts.

### 3. Debug Code

Looks for likely bugs, explains the reason, and returns a corrected version.

### 4. Optimize Code

Reviews code for readability, unnecessary work, maintainability, error handling and practical performance improvements.

## Task 4: Streamlit Code Assistant App

The Streamlit page contains:

- A task selector
- A text area for code or a prompt
- A button to run CodeLlama
- A response section
- Basic connection/error handling
- Model and Ollama endpoint information in the sidebar

## Task 5: Prompt Engineering

I used separate prompt templates for each task instead of sending every request with the same instruction.

The prompts are deliberately:

- Clear
- Structured
- Specific about the expected output
- Easy to change later

This makes the response more consistent than using one generic prompt for all four operations.

## Testing

The `tests/test_prompts.py` file checks that the four prompt types are being constructed correctly.

Run:

```powershell
python tests/test_prompts.py
```

Expected result:

```text
All prompt tests passed.
```

This test does not pretend to verify the model itself. It verifies the local prompt-building logic. The actual CodeLlama response should be checked by running the application with Ollama.

## Common Problems

### `ollama` is not recognized

Install Ollama and restart PowerShell.

### Model not found

Run:

```powershell
ollama pull codellama:7b
```

### Connection refused

Make sure Ollama is running.

### Streamlit starts but the model request fails

Check:

```powershell
ollama list
```

and confirm that the model name matches `OLLAMA_MODEL`.

## Observation

The useful part of this setup is that the application does not need an external LLM API for normal local use. Ollama provides a local HTTP endpoint and LangChain handles the model interaction from Python.

At the same time, model quality and response speed depend on the computer running the model. A local model is convenient for development and privacy, but it is not automatically better than a hosted model.

## Learning Outcome

Through this assignment I connected the application layer and the LLM layer directly:

`Streamlit -> LangChain -> Ollama -> CodeLlama`

The biggest takeaway is that the LLM is one component of the application. Prompt design, error handling, UI, and testing are still normal software-development responsibilities.

**Submitted By:** Abhishek Thakare
