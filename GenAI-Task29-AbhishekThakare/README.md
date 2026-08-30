# Assignment 29: Q&A Chatbot Application (OpenAI & Ollama)

## Objective

Build a plain conversational Q&A chatbot - no RAG - twice: once against OpenAI and once against Ollama, then wrap both behind one switchable function and a simple CLI app.

## Project Structure

```text
Assignment-29/
├── Assignment29.ipynb   # build + test everything (Tasks 1-9)
├── qa_chatbot.py         # get_answer() - shared model-switch logic
├── app.py                 # Task 8 - simple CLI chatbot app
├── README.md
├── requirements.txt
└── .env.example
```

`qa_chatbot.py` holds the actual chat logic so the notebook and `app.py` both
call the same `get_answer()` function instead of two versions of the same
code.

## Tasks Covered

1. OpenAI setup
2. Basic OpenAI Q&A chatbot (tested with 5 questions)
3. Multi-turn Q&A (optional)
4. Ollama setup
5. Ollama chat model with LangChain (same prompt template as OpenAI)
6. Compare OpenAI vs Ollama outputs
7. Model switch logic (`get_answer(question, model_type="openai")`)
8. Build simple app (CLI)
9. Conceptual questions / observations

## Libraries Used

- langchain-core
- langchain-openai
- langchain-ollama
- python-dotenv

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env        # fill in OPENAI_API_KEY
ollama pull llama3           # exact model this assignment asks for
python app.py
```

## OpenAI / Ollama Note

Same running situation as my other assignments - zero usable OpenAI credits
right now, so Part 1 (Tasks 1-3) is real, working code that shows a quota
error rather than a real answer when I run it. Part 2 (Ollama) is where I
actually get real output, same as Assignment 24 - it's local, free, and
doesn't need any billing to work.

Task 7's `get_answer()` correctly rejects an unrecognized `model_type` with a
plain `ValueError` instead of doing something silently wrong, which I
specifically tested for rather than just assumed.

## Experiments Performed

- Set up `ChatOpenAI` and `ChatOllama` behind the same `ChatPromptTemplate`.
- Tested the basic chatbot with 5 different questions on each model.
- Added an optional `chat_history` (via `MessagesPlaceholder`) for multi-turn follow-ups.
- Timed a single question against both models and compared them on response quality, latency, cost, and privacy.
- Pulled the model-switch logic into one `get_answer(question, model_type)` function and tested both valid model types plus an invalid one.
- Built a simple CLI app (`app.py`) that lets the user pick a model up front, switch mid-conversation, and exit cleanly.

## Key Observations

- **Response quality**: hosted models tend to be more consistently polished; a smaller local model can be more variable, especially on anything needing careful reasoning.
- **Latency**: Ollama has no network round-trip since it runs locally, but is limited by local hardware; OpenAI has a network hop but likely stronger backend hardware per request.
- **Cost**: OpenAI is pay-per-token; Ollama is free to run once the model's downloaded, aside from local compute/electricity.
- **Privacy**: with Ollama, questions never leave the machine; with OpenAI, they go to a third party's servers.

## Challenges Faced

The same OpenAI credits issue that's shown up in my last few assignments blocks Tasks 1-3 and half of Task 6 from producing real output here. Ollama also needs to actually be running locally with `llama3` pulled, so Task 6's comparison could only be verified structurally (both calls made, both timed) rather than with genuinely compared answers in this run.

## Learning Outcomes

The main thing I took from this one is that `get_answer()` really doesn't care which model is behind it - the prompt template, the multi-turn history handling, even the parsing logic stayed completely identical between OpenAI and Ollama. Only the one line building the actual LLM object changes, which made the case for treating the model as a parameter from the start rather than hardcoding one provider everywhere.

## Submitted By

Abhishek Thakare
