"""
Shared logic for Assignment 32.
Compatible with modern LangChain 1.x + Ollama.
"""

import os
import ast
import operator
from datetime import datetime

from langchain_ollama import ChatOllama
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import tool

try:
    from langchain_tavily import TavilySearch

    TAVILY_AVAILABLE = True
except ImportError:
    TAVILY_AVAILABLE = False


# -------------------------------------------------------------------
# LLM
# -------------------------------------------------------------------


def get_llm(model="llama3", temperature=0):
    return ChatOllama(
        model=model,
        temperature=temperature,
    )


# -------------------------------------------------------------------
# Calculator
# -------------------------------------------------------------------

_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _safe_eval(node):
    """Safely evaluate basic arithmetic expressions."""

    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numbers are allowed.")

    if isinstance(node, ast.BinOp):
        op_type = type(node.op)

        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError("Operator not allowed.")

        left = _safe_eval(node.left)
        right = _safe_eval(node.right)

        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)

        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError("Operator not allowed.")

        return _ALLOWED_OPERATORS[op_type](_safe_eval(node.operand))

    raise ValueError("Unsupported expression.")


@tool
def calculator(query: str) -> str:
    """
    Useful for math. Evaluates arithmetic expressions and returns
    a numeric answer.
    """

    try:
        expression = query.strip()

        tree = ast.parse(expression, mode="eval")
        result = _safe_eval(tree)

        return str(result)

    except Exception as e:
        return f"Could not calculate '{query}': {e}"


def get_math_tool(llm=None):
    """
    Returns the calculator tool.

    The llm argument is retained for compatibility with the
    original Assignment 32 notebook.
    """
    return calculator


# -------------------------------------------------------------------
# Wikipedia
# -------------------------------------------------------------------


def get_wikipedia_tool():
    return WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(top_k_results=1))


# -------------------------------------------------------------------
# Tavily web search
# -------------------------------------------------------------------


def get_web_search_tool():

    if not TAVILY_AVAILABLE:
        return None

    if not os.getenv("TAVILY_API_KEY"):
        return None

    try:
        return TavilySearch(max_results=3)
    except Exception:
        return None


# -------------------------------------------------------------------
# Company policies
# -------------------------------------------------------------------

MOCK_POLICIES = {
    "leave": ("Employees get 18 paid leave days per year, " "plus public holidays."),
    "wfh": ("Work from home is allowed up to 2 days a week " "with manager approval."),
    "reimbursement": (
        "Travel and client-related expenses are reimbursed "
        "within 15 working days of submitting a receipt."
    ),
}


@tool
def company_policy_lookup(query: str) -> str:
    """
    Returns company policy information for a topic like
    leave, wfh, or reimbursement.
    """

    query = query.lower()

    for key, value in MOCK_POLICIES.items():
        if key in query:
            return value

    return "No policy found for that topic. " "Try leave, wfh, or reimbursement."


# -------------------------------------------------------------------
# Employee database
# -------------------------------------------------------------------

MOCK_DB = {
    "emp001": {
        "name": "Aditi Rao",
        "department": "Engineering",
    },
    "emp002": {
        "name": "Rohan Mehta",
        "department": "Sales",
    },
}


@tool
def employee_db_lookup(employee_id: str) -> str:
    """
    Looks up an employee's name and department by employee ID.
    """

    record = MOCK_DB.get(employee_id.lower())

    if record:
        return f"{record['name']} - {record['department']}"

    return "Employee not found."


# -------------------------------------------------------------------
# Date/time
# -------------------------------------------------------------------


@tool
def current_datetime(_: str = "") -> str:
    """Returns the current date and time."""

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# -------------------------------------------------------------------
# Company toolkit
# -------------------------------------------------------------------


class CompanyToolkit:
    """
    Groups the mock company tools together.
    """

    def get_tools(self):
        return [
            company_policy_lookup,
            employee_db_lookup,
            current_datetime,
        ]


# -------------------------------------------------------------------
# All tools
# -------------------------------------------------------------------


def get_all_tools(llm=None):
    """
    Returns all tools:
    calculator, Wikipedia, Tavily (if configured),
    and the custom company tools.
    """

    tools = [
        get_math_tool(llm),
        get_wikipedia_tool(),
    ]

    web_search = get_web_search_tool()

    if web_search is not None:
        tools.append(web_search)

    tools.extend(CompanyToolkit().get_tools())

    return tools


# -------------------------------------------------------------------
# Manual tool-calling flow
# -------------------------------------------------------------------


def run_tool_calling_flow(llm, tools, query):
    """
    Manual tool-calling loop.

    Returns:
        final_response, calls_made
    """

    from langchain_core.messages import (
        HumanMessage,
        ToolMessage,
    )

    llm_with_tools = llm.bind_tools(tools)

    tool_map = {tool_obj.name: tool_obj for tool_obj in tools}

    messages = [HumanMessage(content=query)]

    ai_msg = llm_with_tools.invoke(messages)

    messages.append(ai_msg)

    if not ai_msg.tool_calls:
        return ai_msg.content, []

    calls_made = []

    for call in ai_msg.tool_calls:

        calls_made.append(
            (
                call["name"],
                call["args"],
            )
        )

        selected_tool = tool_map.get(call["name"])

        if selected_tool is None:
            result = f"Unknown tool: {call['name']}"
        else:
            result = selected_tool.invoke(call["args"])

        messages.append(
            ToolMessage(
                content=str(result),
                tool_call_id=call["id"],
            )
        )

    final = llm_with_tools.invoke(messages)

    return final.content, calls_made


# -------------------------------------------------------------------
# Agent
# -------------------------------------------------------------------


def build_react_agent(llm, tools, verbose=True):
    """
    Compatibility wrapper.

    In LangChain 1.x, the recommended approach is to use
    create_agent rather than the legacy create_react_agent API.
    """

    from langchain.agents import create_agent

    return create_agent(
        model=llm,
        tools=tools,
    )
