from prompts import build_prompt


def test_generate_code_prompt():
    prompt = build_prompt("Generate Code", "Write a function to add two numbers.")
    assert "Write a complete solution" in prompt
    assert "Write a function to add two numbers." in prompt


def test_debug_prompt():
    prompt = build_prompt("Debug Code", "print(unknown_variable)")
    assert "Identify the likely error" in prompt
    assert "unknown_variable" in prompt


def test_all_task_types():
    tasks = ["Generate Code", "Explain Code", "Debug Code", "Optimize Code"]
    for task in tasks:
        prompt = build_prompt(task, "sample input")
        assert "sample input" in prompt


if __name__ == "__main__":
    test_generate_code_prompt()
    test_debug_prompt()
    test_all_task_types()
    print("All prompt tests passed.")
