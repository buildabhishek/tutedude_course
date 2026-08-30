# Assignment 32: AI Agents using LangChain

## Objective

Move past a simple chatbot and build an actual AI Agent - something that can
reason about a query, decide which tool it needs, call that tool, and
explain its steps along the way, instead of just generating a response in
one pass. Covers built-in tools, custom tools/toolkits, binding tools to an
LLM, and a ReAct-style agent that ties all of it together.

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
8. Building a ReAct agent (`create_react_agent` + `AgentExecutor`)
9. Testing the ReAct agent - factual, calculation, multi-step queries
10. Mini project - reusing the ReAct agent as a general assistant
11. Observations & insights

## Libraries Used

- LangChain (`langchain`, `langchain-community`)
- langchain-ollama
- langchain-tavily
- wikipedia, numexpr
- python-dotenv

## Setup

```bash
ollama pull llama3
ollama serve

pip install -r requirements.txt
cp .env.example .env        # optional - fill in TAVILY_API_KEY for web search
```

Then open `Assignment32_AI_Agents_LangChain.ipynb` and run the cells top to
bottom. Ollama needs to already be running for any of the LLM calls to work.

## A note on testing

I ran this myself with Ollama up locally and a real Tavily key loaded, and
the built-in tools, the custom tools, the manual tool-calling flow, and the
ReAct agent all worked as expected - including the multi-step query
actually producing multiple Thought/Action/Observation cycles in the
verbose trace before landing on a final answer, which is the part I was
most trying to confirm actually happens rather than assuming it would.
Without a Tavily key, the web search tool is skipped automatically
(`get_web_search_tool()` returns `None`) instead of the notebook crashing -
that part I also tested by unsetting the key and re-running, to make sure
the fallback path actually works and not just the happy path.

## Experiments Performed

- Set up `ChatOllama` (llama3) the same way as Assignment 24, reused as the base LLM for every part.
- Built and tested the calculator, Wikipedia, and Tavily tools individually before combining anything.
- Wrote `company_policy_lookup` with mock data and tested it against a few different query phrasings, including one with no match.
- Grouped three custom tools into `CompanyToolkit` and printed each tool's name/description.
- Bound the full tool list to the LLM and ran `run_tool_calling_flow()` against a single-tool query and a two-tool query, printing which tools actually got called each time.
- Built a ReAct agent with `create_react_agent` + `AgentExecutor(verbose=True)` and ran it against a factual, a calculation, and a multi-step reasoning question.
- Reused the same agent as the Part 5 "assistant" across a mixed set of queries to confirm it generalizes rather than only working on the exact test questions from Part 4.

## Key Observations

The manual flow in Task 6 and the ReAct agent in Task 8 look similar on the
surface but behave differently once a query needs more than one step - the
manual flow does exactly one round of tool calls and stops, while the ReAct
loop keeps going, observing each result and deciding whether it needs
another action, which is what let it handle the three-part multi-step query
in Task 9 properly instead of just answering the first part.

Splitting `agents_lib.py` out from the notebook meant the "does the tool
actually work" testing and the "does the agent reason correctly" testing
could both happen against the same real functions, not a simplified
notebook version of them - same lesson from keeping `rag_groq.py` separate
in Assignment 30.

## Challenges Faced

A local model is noticeably less consistent at formatting tool calls than a
larger hosted model - llama3 occasionally produced a slightly malformed
action input during testing, which is why `handle_parsing_errors=True` is
set on the `AgentExecutor` rather than letting one bad step kill the whole
run. Web search also depends on a Tavily key being present, so that tool is
allowed to be missing entirely without breaking the rest of the notebook,
same "don't let one missing credential take down everything else" approach
as the Groq/embedding-model fallbacks in Assignment 30.

## Learning Outcomes

The biggest difference from the RAG assignments is that there's no fixed
pipeline here - Assignments 25 through 30 always ran retrieve-then-generate
in that order, and the only thing that changed between them was the
provider or the serving layer. An agent doesn't have a fixed shape like
that, the sequence of steps is something the model decides per query, which
is really the whole point of giving it tools and a reasoning loop instead
of just a bigger prompt.

## Submitted By

Abhishek Thakare
