from langchain_core.prompts import PromptTemplate


PROMPTS = {
    "Generate Code": """
You are a practical coding assistant.

Write a complete solution for the user's request.
Requirements:
- Use clear, beginner-friendly Python unless another language is requested.
- Return runnable code.
- Keep the solution simple and avoid unnecessary libraries.
- Briefly explain how to run it after the code.

User request:
{user_input}
""",
    "Explain Code": """
You are helping a developer understand code.

Explain the code below in simple technical language.
Cover:
1. What the code does
2. How the main parts work
3. Important concepts used
4. Assumptions or limitations

Code or question:
{user_input}
""",
    "Debug Code": """
You are a careful debugging assistant.

Review the code/problem below.
1. Identify the likely error or bug.
2. Explain why it happens.
3. Provide corrected code.
4. Mention useful edge cases.

Code or problem:
{user_input}
""",
    "Optimize Code": """
You are a code review assistant.

Review the code below and suggest practical improvements.
Focus on readability, unnecessary work, error handling,
maintainability, and performance where it actually matters.

Show an improved version and explain the main changes.

Code:
{user_input}
""",
}


def build_prompt(task_type: str, user_input: str) -> str:
    template = PromptTemplate.from_template(PROMPTS[task_type])
    return template.format(user_input=user_input)
