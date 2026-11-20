# Write a Python3 function *add_numbers(x, y)* that returns the sum of two numeric values parameter *x* and *y*.

import ast
import pytest


def test_add_numbers():

    with open("exercise_2.py", encoding="utf-8-sig") as f:
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
        (f for f in functions if f.name == "add_numbers"),
        None
    )

    if func is None:
        errors.append(
            "Missing or incorrect function name. "
            "Expected 'add_numbers'."
        )

    else:
        # 3. Check exact parameters
        args = func.args
        params = [arg.arg for arg in args.args]

        if (
            params != ["x", "y"]
            or args.posonlyargs
            or args.kwonlyargs
            or args.vararg is not None
            or args.kwarg is not None
            or args.defaults
            or args.kw_defaults
        ):
            errors.append(
                "Incorrect parameters. Expected exactly (x, y)."
            )

        # 4. Check return statement
        has_return = any(
            isinstance(node, ast.Return)
            for node in ast.walk(func)
        )

        if not has_return:
            errors.append(
                "Missing return statement. "
                "The function must return the sum."
            )

    # Display structural errors
    if errors:
        feedback = "\n".join(
            f"{i}. {error}"
            for i, error in enumerate(errors, 1)
        )

        pytest.fail(
            "\nFUNCTION ERRORS:\n" + feedback,
            pytrace=False
        )

    # 5. Execute only the function definition
    module = ast.Module(
        body=[func],
        type_ignores=[]
    )

    ast.fix_missing_locations(module)

    namespace = {}

    try:
        exec(
            compile(module, "<student>", "exec"),
            namespace
        )

        add_numbers = namespace["add_numbers"]

        # 6. Test function outputs
        test_cases = [
            (2, 3, 5),
            (10, 20, 30),
            (-5, 3, -2),
            (0, 0, 0),
            (1.5, 2.5, 4.0),
            (-2.5, -1.5, -4.0)
        ]

        for x, y, expected in test_cases:
            result = add_numbers(x, y)

            assert result == pytest.approx(expected), (
                f"Incorrect result for x={x}, y={y}. "
                f"Expected {expected}, but got {result}."
            )

    except AssertionError:
        raise

    except Exception as e:
        pytest.fail(
            f"Error while executing add_numbers(x, y): {e}",
            pytrace=False
        )
