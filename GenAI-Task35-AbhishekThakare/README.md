# Assignment 35: Text-to-Math Agent

## On Verification (same standard as Assignment 33's rework)

I have no live LLM reachable in my current environment (no Ollama running, no working OpenAI/Groq/Anthropic key), so this is built and documented the same honest way as my SQL agent rework:

- The **calculator tool** is plain, deterministic Python - no LLM involved at all. It's rigorously tested on its own, including deliberately trying to break it with code-injection-style input (`__import__("os").system(...)`, `open("/etc/passwd").read()`) to confirm it genuinely refuses to execute anything beyond arithmetic, not just documented to.
- The **agent object** (`create_agent` wired to the calculator tool + llama3.2) builds successfully without a live connection.
- The **actual agent conversation** needs a real, reachable model. In this environment it genuinely fails with a plain connection error - that's what `Assignment35.ipynb` shows, because I executed the whole notebook with `jupyter nbconvert --execute` and the saved outputs are real, not hand-written.
- Ground-truth answers to all three test word problems are computed independently first, so a real run's agent answers can be checked against real numbers rather than trusted at face value.

## A Real Technical Finding

LangChain 1.x replaced the older `initialize_agent` / `create_react_agent` + `AgentExecutor` pattern entirely with a new `create_agent` function built on LangGraph. I confirmed this by trying the older import first (`ImportError`), then finding `create_agent` in its place. `math_agent.py` uses the current API.

## Project Structure

```text
Assignment-35/
├── Assignment35.ipynb   # executed end-to-end - real, saved outputs
├── math_agent.py          # calculator tool + agent construction (Tasks 1-2)
├── app.py                  # Streamlit chat app with session state (Task 3)
├── README.md
└── requirements.txt
```

## Tasks Covered

1. Text-to-Math agent overview (conceptual)
2. Build the Text-to-Math agent (calculator tool + LLM), tested with arithmetic, percentage, and algebra word problems
3. Session state for the Streamlit application

## Libraries Used

- LangChain (`create_agent`)
- langchain-ollama
- Streamlit

## LLM Note

Same situation as my other recent assignments - zero usable OpenAI credits, so this uses **Ollama running `llama3.2`**. Building the agent doesn't need Ollama to be running at all; only actually asking it a question does.

## How to Get Real Agent Output

1. `pip install -r requirements.txt`
2. Install and run Ollama locally, then `ollama pull llama3.2`
3. Re-run `Assignment35.ipynb` top to bottom - the agent cells will show real answers instead of connection errors, checkable against Part 0's ground truth (62, 60, and 5 respectively)
4. `streamlit run app.py` for the interactive chat version

## Experiments Performed

- Built a safe arithmetic evaluator using Python's `ast` module (only numbers and `+ - * / ** %` allowed) instead of raw `eval()`, and tested it against both correct-answer cases and deliberate code-injection attempts.
- Built the agent with `create_agent`, confirmed it constructs without a live model connection.
- Attempted all three test word problems (arithmetic, percentage, algebra) and confirmed the failure is a clean connection error, not a construction or logic bug.
- Actually launched the Streamlit app (`streamlit run app.py --server.headless true`) and confirmed it starts cleanly and serves a real page (HTTP 200).

## Key Observations

The calculator tool and the agent's reasoning about *when* to use it are two different kinds of correctness - the tool is deterministically right or wrong and provable without any LLM at all, while whether the agent decides to call it on the right expression for a given word problem is a separate question only a live model can actually answer. Keeping ground-truth answers computed independently (Part 0) is what turns "the agent said something" into "the agent said something checkable."

## Challenges Faced

Same recurring limitation as my last couple of assignments - no live LLM reachable in this environment, so the actual agent conversation and the live Streamlit chat experience couldn't be demonstrated with real, model-generated answers here. Everything up to that point (the tool, the agent construction, the app's session-state plumbing) is genuinely verified.

## Learning Outcomes

I learned that LangChain's agent-building API changed significantly between versions - the pattern this kind of assignment is often written around (`initialize_agent`, `AgentExecutor`) isn't the current way to do it anymore, and checking that an API still exists before relying on it is worth doing rather than assuming. I also reinforced the lesson from Assignment 33: separating what's deterministically testable from what needs a live model, and being explicit about which is which, produces a more honest and more useful deliverable than blurring the two together.

## Submitted By

Abhishek Thakare
