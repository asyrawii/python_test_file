import ast
import re

def test_function_header():

    with open("header2.py", encoding="utf-8-sig") as f:
        header = f.read().strip()

    # 1. Check empty answer
    assert header, "Your answer is empty."

    # 2. Check 'def' keyword
    assert re.match(r"^def\b", header), (
        "Missing or incorrect 'def' keyword. "
        "A function definition must start with 'def'."
    )

    # 3. Check function name
    match = re.match(r"^def\s+([a-zA-Z_]\w*)", header)

    assert match, (
        "Invalid function name or missing space after 'def'."
    )

    function_name = match.group(1)

    assert function_name == "my_function2", (
        f"Incorrect function name '{function_name}'. "
        "Expected 'my_function2'."
    )

    # 4. Check parentheses
    assert "(" in header, (
        "Missing opening parenthesis '('."
    )

    assert ")" in header, (
        "Missing closing parenthesis ')'."
    )

    # 5. Check colon
    assert header.endswith(":"), (
        "Missing colon ':' at the end of the function header."
    )

    # 6. Check Python syntax
    try:
        tree = ast.parse(header + "\n    pass")
    except SyntaxError as e:
        assert False, f"Invalid Python syntax: {e.msg}"

    func = tree.body[0]

    assert isinstance(func, ast.FunctionDef), (
        "Invalid function definition."
    )

    # 7. Check parameters
    params = [arg.arg for arg in func.args.args]

    assert params == ["x", "y"], (
        f"Incorrect parameters {params}. "
        "Expected parameters ['x', 'y'] in that order."
    )

    # 8. Reject additional parameter types/defaults
    assert (
        not func.args.posonlyargs
        and not func.args.kwonlyargs
        and func.args.vararg is None
        and func.args.kwarg is None
        and not func.args.defaults
        and not func.args.kw_defaults
    ), "Only two ordinary parameters, x and y, are allowed."
