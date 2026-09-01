"""
Shared logic for Assignment 32.

Reworked after mentor feedback on the first submission - two real bugs, not
just a documentation problem:

1. The default model was "llama3", which does not support Ollama's tool
   calling API. bind_tools() on it doesn't error, it just silently never
   produces a tool call, so Task 6, Task 9, and Task 10 all failed with no
   error message, just wrong-looking output. Switched the default to
   "llama3.1", which does support tool calling in Ollama. Also fine:
   "llama3-groq-tool-use" or "qwen2.5", both tagged as tool-capable models
   on Ollama's library.

2. LLMMathChain (used for the calculator tool) no longer exists in current
   LangChain - it was removed from langchain.chains. Rewrote the calculator
   to call numexpr directly instead of routing through an LLM chain, which
   is also just a better design for a calculator tool - no reason to make
   an extra model call to parse "245 * 12 + 89".

3. langchain.agents.create_react_agent (the hub-prompt-based classic ReAct
   agent) has also been removed from current LangChain. Rebuilt Task 8 on
   langgraph.prebuilt.create_react_agent instead, which is the current
   supported way to build a ReAct-style tool-calling agent - and this one
   genuinely needs a tool-calling-capable model too, same reason as #1.
"""

import os
import re
from datetime import datetime

import numexpr
from langchain_ollama import ChatOllama
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent as _build_langgraph_react_agent

try:
    from langchain_tavily import TavilySearch
    TAVILY_AVAILABLE = True
except ImportError:
    TAVILY_AVAILABLE = False


def get_llm(model="llama3.1", temperature=0):
    """Defaults to llama3.1, not llama3 - see the module docstring for why
    that switch matters here specifically."""
    return ChatOllama(model=model, temperature=temperature)


_PERCENT_OF_RE = re.compile(r"(\d+(?:\.\d+)?)\s*%\s*of\s*(\d+(?:\.\d+)?)", re.IGNORECASE)


@tool
def calculator(expression: str) -> str:
    """Evaluates a numeric arithmetic expression, e.g. '245 * 12 + 89' or '18% of 4500', and returns the result."""
    cleaned = _PERCENT_OF_RE.sub(r"(\1/100)*\2", expression.strip())
    try:
        result = numexpr.evaluate(cleaned).item()
        return str(result)
    except Exception as e:
        return f"Couldn't evaluate that expression: {e}"


def get_math_tool(llm=None):
    # llm kept as an accepted-but-unused argument so existing call sites
    # that pass one don't break - the calculator itself no longer needs it.
    return calculator


def get_wikipedia_tool():
    return WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(top_k_results=1))


def get_web_search_tool():
    # Returns None instead of raising if there's no Tavily key set, so the
    # rest of the notebook can still run with the other tools instead of
    # dying on an import/auth error right at the top.
    if not TAVILY_AVAILABLE:
        return None
    if not os.getenv("TAVILY_API_KEY"):
        return None
    try:
        return TavilySearch(max_results=3)
    except Exception:
        return None


MOCK_POLICIES = {
    "leave": "Employees get 18 paid leave days per year, plus public holidays.",
    "wfh": "Work from home is allowed up to 2 days a week with manager approval.",
    "reimbursement": "Travel and client-related expenses are reimbursed within 15 working days of submitting a receipt.",
}


@tool
def company_policy_lookup(query: str) -> str:
    """Returns company policy information for a topic like leave, wfh, or reimbursement."""
    query = query.lower()
    for key, value in MOCK_POLICIES.items():
        if key in query:
            return value
    return "No policy found for that topic. Try leave, wfh, or reimbursement."


MOCK_DB = {
    "emp001": {"name": "Aditi Rao", "department": "Engineering"},
    "emp002": {"name": "Rohan Mehta", "department": "Sales"},
}


@tool
def employee_db_lookup(employee_id: str) -> str:
    """Looks up an employee's name and department by their employee id, e.g. emp001."""
    record = MOCK_DB.get(employee_id.lower())
    if record:
        return f"{record['name']} - {record['department']}"
    return "Employee not found."


@tool
def current_datetime(_: str = "") -> str:
    """Returns the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class CompanyToolkit:
    """Groups the mock company tools together - policy lookup, employee DB, date/time."""

    def get_tools(self):
        return [company_policy_lookup, employee_db_lookup, current_datetime]


def get_all_tools(llm=None):
    """Builtin tools (calculator, wikipedia, web search if a key is present)
    plus the custom company toolkit, combined into one flat list for
    binding/agent use."""
    tools = [get_math_tool(), get_wikipedia_tool()]

    web_search = get_web_search_tool()
    if web_search is not None:
        tools.append(web_search)

    tools.extend(CompanyToolkit().get_tools())
    return tools


def run_tool_calling_flow(llm, tools, query):
    """Manual version of the tool-calling loop for Task 6 - lets a call site
    see each step instead of an agent's built-in loop hiding it. Requires
    llm to be a tool-calling-capable model - see get_llm()'s docstring."""
    llm_with_tools = llm.bind_tools(tools)
    tool_map = {t.name: t for t in tools}

    messages = [HumanMessage(content=query)]
    ai_msg = llm_with_tools.invoke(messages)
    messages.append(ai_msg)

    if not ai_msg.tool_calls:
        # This is the exact failure mode from the first submission - a
        # model without tool support returns here every time with an empty
        # tool_calls list, so nothing ever actually gets executed.
        return ai_msg.content, []

    calls_made = []
    for call in ai_msg.tool_calls:
        calls_made.append((call["name"], call["args"]))
        selected_tool = tool_map[call["name"]]
        result = selected_tool.invoke(call["args"])
        messages.append({"role": "tool", "content": str(result), "tool_call_id": call["id"]})

    final = llm_with_tools.invoke(messages)
    return final.content, calls_made


def build_react_agent(llm, tools):
    """Task 8 - built on langgraph's create_react_agent, which is the
    current supported way to do this (langchain.agents.create_react_agent
    no longer exists in current LangChain). This is a tool-calling agent
    under the hood, same requirement as run_tool_calling_flow above: llm
    needs real tool-calling support or every step here fails the same way
    Task 6 did in the first submission."""
    return _build_langgraph_react_agent(llm, tools)


def run_react_agent(agent, query, verbose=True):
    """Runs the agent and, if verbose, prints each message in the
    conversation - tool calls the model requested, the tool's result, and
    the final answer - so the reasoning steps are visible instead of only
    the last message."""
    result = agent.invoke({"messages": [HumanMessage(content=query)]})
    messages = result["messages"]

    if verbose:
        for m in messages:
            role = type(m).__name__
            tool_calls = getattr(m, "tool_calls", None)
            if tool_calls:
                print(f"[{role}] requested tool call(s): {tool_calls}")
            elif getattr(m, "content", None):
                print(f"[{role}] {m.content}")

    return messages[-1].content
