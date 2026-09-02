title: GenAI Task 39 - Abhishek Thakare
emoji: 💻
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
---

# Assignment 39: GenAI App Deployment

**Name:** Abhishek Thakare

## Project

This project is a small GenAI coding assistant built using Streamlit.

The application can:

- Generate Python code
- Explain code
- Debug code
- Suggest improvements and optimize code

The application was initially developed to run locally using **Ollama with CodeLlama 7B**.

During cloud deployment, I added **Groq API** as a remote inference backend because a cloud-hosted application cannot directly access Ollama running on my personal computer.

---

# 1. Technologies Used

- Python
- Streamlit
- LangChain
- Ollama
- CodeLlama 7B
- Groq API
- Qwen model through Groq
- Hugging Face Spaces
- Docker
- GitHub

---

# 2. Application Features

The application provides four coding assistant tasks.

### Generate Code

Generates Python code based on the user's requirement.

Example:

```text
Write a Python function to check whether a number is prime.
````

### Explain Code

Explains the purpose and working of the given code in simple terms.

### Debug Code

Identifies possible errors and provides a corrected version of the code.

### Optimize Code

Reviews the code and suggests improvements related to readability, structure and performance.

---

# 3. Project Structure

```text
GenAI-Task39-AbhishekThakare/
│
├── app.py
├── prompts.py
├── requirements.txt
├── Dockerfile
├── README.md
├── .env.example
├── .gitignore
│
└── tests/
    └── test_prompts.py
```

---

# 4. Local Development

The original application was designed to work locally with Ollama and CodeLlama.

The local architecture is:

```text
User
  |
  v
Streamlit Application
  |
  v
Ollama
  |
  v
CodeLlama 7B
```

Ollama runs locally on:

```text
http://localhost:11434
```

## Setup

### Step 1: Create a virtual environment

```powershell
python -m venv .venv
```

### Step 2: Activate the virtual environment

```powershell
.venv\Scripts\activate
```

### Step 3: Install dependencies

```powershell
pip install -r requirements.txt
```

### Step 4: Pull CodeLlama

```powershell
ollama pull codellama:7b
```

### Step 5: Run the Streamlit application

```powershell
streamlit run app.py
```

When a Groq API key is not configured, the application uses:

```text
Ollama + CodeLlama 7B
```

---

# 5. Cloud Deployment Problem

During the Streamlit Cloud deployment, the application initially tried to connect to:

```text
localhost:11434
```

This worked on my personal computer because Ollama was running locally.

However, after deployment, Streamlit Cloud runs the application on a remote server.

Therefore:

```text
localhost
```

refers to the cloud server itself and not my personal computer.

The deployed application therefore could not connect to my locally running Ollama instance.

The error received was:

```text
Could not connect to Ollama.

[Errno 99] Cannot assign requested address
```

This helped me understand an important difference between local development and cloud deployment.

---

# 6. Cloud Deployment Solution

To make the GenAI application usable after deployment, I added **Groq API** as a remote LLM backend.

The application now supports two backends.

## Local

```text
Streamlit
    |
    v
Ollama
    |
    v
CodeLlama 7B
```

## Cloud

```text
Streamlit Cloud
    |
    v
Groq API
    |
    v
qwen/qwen3.8-27b
```

The application checks whether `GROQ_API_KEY` is available.

If the key is available:

```text
Groq API
```

is used.

If the key is not available:

```text
Local Ollama + CodeLlama
```

is used.

This allows the same application to work in both local and cloud environments.

---

# 7. Groq Configuration

The Groq API key is stored as a deployment secret.

The actual API key is **not stored in the source code or GitHub repository**.

The environment variable used by the application is:

```text
GROQ_API_KEY
```

The deployed Groq model used by this project is:

```text
qwen/qwen3.8-27b
```

The model was selected from the models available to the Groq API account used for this project.

Example environment configuration:

```text
GROQ_API_KEY=
```

Only the variable name is included in the example file.

---

# 8. Streamlit Cloud Deployment

The application was deployed using Streamlit Community Cloud.

## Deployment steps

1. The project was pushed to GitHub.
2. A Streamlit Cloud application was created.
3. The GitHub repository was selected.
4. The `main` branch was selected.
5. `app.py` was selected as the application entry point.
6. The `GROQ_API_KEY` was added through Streamlit Cloud Secrets.
7. The application was deployed.
8. The live application was tested.

## Live Application

The deployed Streamlit application is available at:

```text
https://genai-task39-abhishekthakare-jcanxd2fafvxjht2hmtcmy.streamlit.app/
```

The live application successfully generated responses using the Groq backend.

The application displays:

```text
Backend: Groq API
```

when the cloud backend is being used.

---

# 9. Streamlit Cloud Testing

The deployed application was tested using the available coding assistant features.

## Test 1: Generate Code

Example input:

```text
Write a Python function to check whether a number is prime.
```

The application generated a Python response.

## Test 2: Explain Code

Example:

```python
def square(n):
    return n * n
```

The application provided an explanation of the code.

## Test 3: Debug Code

Example:

```python
def add(a, b):
    return a + c
```

The application identified the variable problem and suggested a correction.

## Test 4: Optimize Code

A simple Python code example was provided and the application suggested improvements.

---

# 10. Hugging Face Spaces Deployment

A Hugging Face Space was also created for this project.

The Space was initially created with a static configuration.

It was then configured for a Docker-based deployment.

The Hugging Face configuration in this README uses:

```yaml
sdk: docker
app_port: 7860
```

The project also contains a `Dockerfile`.

The Dockerfile starts the Streamlit application on port `7860`.

---

# 11. Docker Configuration

The Dockerfile used for the Hugging Face deployment is:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=7860"]
```

The Docker container installs the Python dependencies and starts the Streamlit application.

---

# 12. Hugging Face Deployment Limitation

The Hugging Face Space was configured with the required Docker files and application files.

However, when trying to restart the Space, Hugging Face returned an account-level compute limitation.

The error displayed was:

```text
403

You've reached your cpu-basic quota limit, please
upgrade your account, or pause your previous
Spaces to restart this one
```

Because of this CPU Basic quota limitation, the Hugging Face Space could not be started for live application testing using the available account resources.

I did not use a fake endpoint or claim that the Hugging Face application was running when it was not.

The Docker configuration and application files were prepared for the Space, but the final live runtime was blocked by the account's available compute quota.

---

# 13. Testing the Project

The prompt-building functions were tested separately.

Run:

```powershell
python tests/test_prompts.py
```

Expected output:

```text
All prompt tests passed.
```

This test checks that the correct prompt is created for:

* Generate Code
* Explain Code
* Debug Code
* Optimize Code

The actual GenAI responses were tested separately through the local/cloud application.

---

# 14. Environment Variables

The project uses environment variables for configuration.

Example:

```text
OLLAMA_MODEL=codellama:7b
OLLAMA_BASE_URL=http://localhost:11434
GROQ_API_KEY=
HUGGINGFACE_API_KEY=
TAVILY_API_KEY=
```

The real API keys are not included in the project.

The `.gitignore` file also excludes local secret files such as:

```text
.env
.streamlit/secrets.toml
```

---

# 15. Streamlit Cloud vs Hugging Face Spaces

| Feature            | Streamlit Cloud               | Hugging Face Spaces                  |
| ------------------ | ----------------------------- | ------------------------------------ |
| Main purpose       | Streamlit applications        | ML and GenAI applications            |
| Streamlit support  | Direct                        | Docker-based                         |
| GitHub integration | Yes                           | Yes                                  |
| Docker support     | Not required for this project | Used in this project                 |
| Setup difficulty   | Easier                        | Slightly higher                      |
| Customization      | Good                          | Higher with Docker                   |
| Best suited for    | Quick Streamlit apps          | ML/GenAI demos and custom containers |

---

# 16. Streamlit Cloud Advantages

* Easy deployment for Streamlit applications
* GitHub integration
* Simple application management
* Easy secret management
* Automatic deployment when the repository is updated
* Good option for small GenAI demonstrations

---

# 17. Streamlit Cloud Disadvantages

* The deployed application cannot directly access services running on my personal computer.
* Local Ollama cannot be accessed through `localhost`.
* A remote LLM API or hosted model backend is required for cloud inference.

---

# 18. Hugging Face Spaces Advantages

* Useful for machine learning and GenAI demonstrations
* Docker provides more control over the application environment
* Supports different types of AI applications
* Useful for sharing AI demos

---

# 19. Hugging Face Spaces Disadvantages

* Docker deployment requires additional configuration
* Compute availability depends on the account and selected hardware
* The free/available compute quota can limit whether a Space can run

---

# 20. Important Deployment Learning

The main learning from this assignment was that deploying an application is different from running it locally.

Locally, the application could use:

```text
localhost:11434
```

because Ollama was running on my computer.

After deployment, the application was running on a remote server, so it could not use the Ollama service on my computer.

Adding Groq provided a remote backend that could be accessed from the cloud application.

This showed the importance of considering the complete application architecture when deploying a GenAI application.

---

# 21. Security Learning

API keys should not be hardcoded in Python files or committed to GitHub.

For this project:

```text
GROQ_API_KEY
```

is stored as a deployment secret.

The `.env` file and Streamlit secrets file are excluded using `.gitignore`.

This prevents accidentally exposing API credentials in the source repository.

---

# 22. Deployment Status

| Component                    | Status                     |
| ---------------------------- | -------------------------- |
| Local Streamlit application  | Completed                  |
| Ollama integration           | Completed                  |
| CodeLlama 7B                 | Completed                  |
| Groq integration             | Completed                  |
| GitHub repository            | Completed                  |
| Streamlit Cloud deployment   | Completed                  |
| Streamlit Cloud live testing | Completed                  |
| Hugging Face Space           | Created                    |
| Docker configuration         | Completed                  |
| Hugging Face live runtime    | Blocked by CPU Basic quota |

---

# 23. Screenshots

The following screenshots can be included as deployment evidence:

```text
screenshots/
├── 01-local-streamlit-test.png
├── 02-github-repository.png
├── 03-streamlit-cloud.png
├── 04-streamlit-live-url.png
├── 05-huggingface-space.png
└── 06-huggingface-quota-error.png
```

### Screenshot 01

Local Streamlit application running with the local Ollama + CodeLlama backend.

### Screenshot 02

GitHub repository containing the project files.

### Screenshot 03

Streamlit Cloud deployment/dashboard.

### Screenshot 04

Live Streamlit application generating a response through the Groq backend.

### Screenshot 05

Hugging Face Space showing the Docker-based project configuration.

### Screenshot 06

Hugging Face CPU Basic quota error encountered while trying to start the Space.

Only screenshots that were actually taken during the project should be included.

---

# 24. Conclusion

This assignment helped me understand the practical side of deploying a GenAI application.

I learned how to:

* Build a Streamlit GenAI application
* Connect an application to Ollama
* Use CodeLlama locally
* Work with a remote LLM API
* Deploy an application using Streamlit Cloud
* Configure a Docker-based Hugging Face Space
* Manage API keys using secrets
* Understand the difference between local and cloud networking
* Troubleshoot deployment problems

The most important practical lesson was that a cloud application cannot directly access services running on my local computer.

For local development, Ollama + CodeLlama was used.

For cloud inference, Groq was added as a remote backend.

This made the application more suitable for real deployment while keeping the original local Ollama setup.

---

## Submitted By : Abhishek Thakare
