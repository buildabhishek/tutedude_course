# Assignment 32: AI Agents using LangChain

## Objective

Move past a simple chatbot and build an actual AI Agent - something that can
reason about a query, decide which tool it needs, call that tool, and
explain its steps along the way, instead of just generating a response in
one pass. Covers built-in tools, custom tools/toolkits, binding tools to an
LLM, and a ReAct-style agent that ties all of it together.

## Resubmission Note

The first submission was rejected for two real problems, not just wording:

1. **The agent didn't actually work.** The default model was `llama3`,
   which doesn't support Ollama's tool calling API - `bind_tools()` runs
   without error, but the model never returns anything in `tool_calls`, so
   Task 6 (manual tool-calling flow), Task 9 (ReAct agent tests), and Task
   10 (mini project) all failed silently. Fixed by switching the default
   model to `llama3.1` in `get_llm()`, which does support tool calling in
   Ollama.
2. **The notebook and README described successful runs that never
   happened.** That was wrong regardless of the model bug. This version
   only claims a result where there's real output to back it up - anything
   that needs a live Ollama call is explicitly marked as not run in the
   environment this was authored in, with the expected outcome stated
   separately from any actual output, instead of narrated as if it had been
   observed.

While fixing the model, I also found two unrelated breakages in the first
submission's code that would have failed even with a tool-capable model:
`LLMMathChain` no longer exists in current LangChain (removed from
`langchain.chains`), so the calculator tool now calls `numexpr` directly
instead of routing through a chain. And `langchain.agents.create_react_agent`
(the hub-prompt-based agent used before) has also been removed from current
LangChain - Task 8 is rebuilt on `langgraph.prebuilt.create_react_agent`,
the current supported way to build this.

## Project Structure

```text
GenAI-Task32-Abhishek/
├── Assignment32_AI_Agents_LangChain.ipynb   # build + test, all 5 parts
├── agents_lib.py                              # shared tool/agent logic
├── requirements.txt
├── .env.example
└── README.md
```

`agents_lib.py` holds the actual tool definitions, the toolkit, the manual
tool-calling flow, and the ReAct agent builder, so the notebook cells are
testing the real functions instead of redefining everything inline - same
split as `rag_groq.py` in Assignment 30.

## Tasks Covered

1. Understanding tools (conceptual)
2. Built-in tools - calculator, Wikipedia, web search
3. Custom tool - company policy lookup (mock data)
4. Custom toolkit - grouping policy lookup, employee DB lookup, date/time
5. Tool binding to the LLM
6. Manual tool-calling flow (query -> LLM -> tool selection -> execution -> answer)
7. ReAct agent overview (conceptual)
8. Building a ReAct agent (`langgraph.prebuilt.create_react_agent`)
9. Testing the ReAct agent - factual, calculation, multi-step queries
10. Mini project - reusing the ReAct agent as a general assistant
11. Observations & insights

## Libraries Used

- LangChain (`langchain`, `langchain-community`)
- langchain-ollama
- langgraph
- langchain-tavily
- wikipedia, numexpr
- python-dotenv

## Setup

```bash
ollama pull llama3.1
ollama serve

pip install -r requirements.txt
cp .env.example .env        # optional - fill in TAVILY_API_KEY for web search
```

Then open `Assignment32_AI_Agents_LangChain.ipynb` and run the cells top to
bottom. Ollama needs to already be running with `llama3.1` pulled for any of
the LLM-dependent cells (Tasks 6, 8, 9, 10) to work.

## A note on testing

I don't have Ollama installed in the environment I authored this in, so
anything requiring a live model call (Tasks 6, 8, 9, 10) was **not executed
here** - the notebook says so explicitly at each of those cells rather than
describing a result. What I could and did run for real: the calculator tool
(including catching and fixing a real bug where `"18% of 4500"` failed to
parse until I added a percent-rewrite step), the custom company tools
(`company_policy_lookup`, `employee_db_lookup`, `current_datetime`), and the
`CompanyToolkit` grouping - all plain Python with no external dependency, so
those outputs in the notebook are genuine, not narrated.

I also confirmed, by actually trying to import them in this environment,
that `langchain.chains.LLMMathChain` and `langchain.agents.create_react_agent`
no longer exist in the current LangChain version - those weren't
assumptions, I hit real `ImportError`s and rewrote around them.

What's still unverified: whether `llama3.1` actually returns tool calls
correctly for these specific queries, and whether the LangGraph ReAct agent
completes the multi-step queries as expected. Both should be checked by
whoever runs this next, with Ollama actually running - the notebook prints
explicit warnings (e.g. "no tool calls were made") if the same silent
failure from the first submission happens again with a different model.

## Experiments Performed

- Actually ran the calculator, including a real bug I hit and fixed (percent-of expressions failing to parse under `numexpr`).
- Actually ran `company_policy_lookup`, `employee_db_lookup`, `current_datetime`, and `CompanyToolkit` - all confirmed working with genuine output.
- Actually confirmed `LLMMathChain` and `langchain.agents.create_react_agent` no longer import in the current LangChain version, and rewrote `agents_lib.py` around both removals.
- Wrote `run_tool_calling_flow()` to explicitly return an empty `calls` list (rather than silently returning normal-looking text) when the model doesn't produce a tool call, so that specific failure mode is visible in the notebook's output instead of hidden.
- Wrote out the expected results for the Task 9 and Task 10 queries by hand from the tool logic, so there's something concrete to check the real run against once it's executed with Ollama.

## Key Observations

The most important thing this resubmission surfaced: tool calling support
isn't something you can assume from "the model is a chat model" - it's a
specific capability some models have and others don't, and a model without
it fails in a way that looks exactly like a normal, successful response
(`.invoke()` still returns a clean `AIMessage`), just with an empty
`tool_calls` list nobody was checking. That's a much easier bug to miss than
an exception, which is exactly what happened.

## Challenges Faced

Diagnosing why the previous agent "worked" but never actually called
anything - there was no error to chase, since `bind_tools()` on a
non-tool-calling model doesn't raise. Also ran into two LangChain API
removals (`LLMMathChain`, `langchain.agents.create_react_agent`) while
rebuilding this, which meant checking the current package version's actual
import surface directly rather than trusting how the API used to look.

## Learning Outcomes

Two separate lessons here. On the LangChain side: APIs in a fast-moving
library can disappear between versions, so it's worth actually trying an
import rather than assuming code that looked right before still does. On
the agent side: "the code ran without an exception" and "the code did what
it was supposed to do" are different claims, and the second one needs to be
checked explicitly - `if not ai_msg.tool_calls` is now a real check in
`run_tool_calling_flow()`, not just an afterthought.

## Submitted By

Abhishek Thakare
