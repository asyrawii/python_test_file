# Disclaimer :- This is from ChatGPT
# Write a Python3 function *print_hello()* that prints "Hello world!".
"""Sample code
def print_hello():
    print("Hello world!")
"""


import ast
import pytest

def test_print_hello():

    with open("exercise.py", encoding="utf-8-sig") as f:
        source = f.read()

    errors = []

    # 1. Check Python syntax
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        pytest.fail(
            f"Invalid Python syntax: {e.msg}",
            pytrace=False
        )

    # 2. Find function definition
    functions = [
        node for node in tree.body
        if isinstance(node, ast.FunctionDef)
    ]

    func = next(
        (f for f in functions if f.name == "print_hello"),
        None
    )

    if func is None:
        errors.append(
            "Missing or incorrect function name. "
            "Expected 'print_hello'."
        )

    else:
        # 3. Check parameters
        args = func.args

        if (
            args.posonlyargs or args.args
            or args.kwonlyargs
            or args.vararg is not None
            or args.kwarg is not None
        ):
            errors.append(
                "Function print_hello() must not have parameters."
            )

        # 4. Check print statement
        print_found = False

        for statement in func.body:
            if isinstance(statement, ast.Expr):
                call = statement.value

                if isinstance(call, ast.Call):
                    if (
                        isinstance(call.func, ast.Name)
                        and call.func.id == "print"
                        and len(call.args) == 1
                        and not call.keywords
                        and isinstance(call.args[0], ast.Constant)
                        and call.args[0].value == "Hello world!"
                    ):
                        print_found = True

        if not print_found:
            errors.append(
                'Missing or incorrect print statement. '
                'Expected print("Hello world!").'
            )

    # 5. Display feedback
    if errors:
        feedback = "\n".join(
            f"{i}. {error}"
            for i, error in enumerate(errors, 1)
        )

        pytest.fail(
            "\nFUNCTION ERRORS:\n" + feedback,
            pytrace=False
        )
