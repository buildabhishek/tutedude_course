"""
math_agent.py

Core logic for Assignment 35 - a Text-to-Math agent built with LangChain's
current agent API (`create_agent`, which is what LangChain 1.x actually
ships now - the older `initialize_agent` / `create_react_agent` +
AgentExecutor pattern from earlier LangChain versions is gone).

The calculator tool itself is plain, deterministic Python - it needs no LLM
at all and is fully tested on its own. The *agent* (understanding a word
problem, deciding to call the tool, forming the final answer) does need a
live LLM.
"""

import ast
import operator

from langchain_core.tools import tool
from langchain.agents import create_agent

_llm = None


def get_llm(temperature: float = 0.0):
    """Built lazily so importing this file doesn't fail just because
    Ollama isn't running yet. Temperature 0 - math answers should be
    consistent, not creative."""
    global _llm
    if _llm is None:
        from langchain_ollama import ChatOllama
        _llm = ChatOllama(model="llama3.2", temperature=temperature)
    return _llm


# ---------------------------------------------------------------------------
# The calculator tool - a safe expression evaluator, not raw eval(). This
# part needs no LLM and is fully deterministic, so it's testable on its own.
# ---------------------------------------------------------------------------
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
    ast.Mod: operator.mod,
}


def _safe_eval(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant: {node.value!r}")
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported operator: {op_type.__name__}")
        return _ALLOWED_OPERATORS[op_type](_safe_eval(node.left), _safe_eval(node.right))
    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported operator: {op_type.__name__}")
        return _ALLOWED_OPERATORS[op_type](_safe_eval(node.operand))
    raise ValueError(f"Unsupported expression: {ast.dump(node)}")


def safe_calculate(expression: str) -> float:
    """Evaluate a plain arithmetic expression safely - only numbers and
    +, -, *, /, **, % are allowed, so this can't execute arbitrary code the
    way a raw eval() call could."""
    tree = ast.parse(expression, mode="eval")
    return _safe_eval(tree.body)


@tool
def calculator(expression: str) -> str:
    """Evaluate a plain arithmetic expression, e.g. '15 * 0.20' or '(45 - 12) / 3',
    and return the numeric result as a string. Use this for any actual
    calculation instead of computing it yourself."""
    try:
        result = safe_calculate(expression)
        return str(result)
    except Exception as e:
        return f"Error evaluating '{expression}': {e}"


# ---------------------------------------------------------------------------
# Task 2: the actual agent - LLM + calculator tool
# ---------------------------------------------------------------------------
MATH_AGENT_SYSTEM_PROMPT = (
    "You are a math problem-solving assistant. When given a word problem:\n"
    "1. Read it carefully and figure out what calculation(s) are needed.\n"
    "2. Break the problem into clear steps.\n"
    "3. Use the calculator tool for every actual arithmetic calculation - "
    "never compute a number yourself without it.\n"
    "4. State the final answer clearly at the end.\n"
    "If a question is ambiguous or missing information needed to solve it, "
    "say so instead of guessing."
)


def build_math_agent(llm=None):
    """Task 2: builds the agent using LangChain's current create_agent API."""
    llm = llm or get_llm()
    return create_agent(model=llm, tools=[calculator], system_prompt=MATH_AGENT_SYSTEM_PROMPT)


def ask_math_agent(agent, question: str, history=None) -> str:
    """Send one question to the agent, optionally with prior conversation
    messages for context, and return the final assistant message text."""
    messages = list(history) if history else []
    messages.append({"role": "user", "content": question})

    result = agent.invoke({"messages": messages})
    final_message = result["messages"][-1]
    return final_message.content


if __name__ == "__main__":
    print("2 + 2 =", safe_calculate("2 + 2"))
    print("15% of 240 =", safe_calculate("240 * 0.15"))

    agent = build_math_agent()
    print(ask_math_agent(agent, "If a shirt costs $40 and is discounted by 15%, what is the final price?"))
