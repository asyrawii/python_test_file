# Write a Python3 function *check_odd_even(n)* that returns "Odd" or "Even"

import ast
import pytest


def test_check_odd_even():

    with open("exercise_4.py", encoding="utf-8-sig") as f:
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
        (f for f in functions if f.name == "check_odd_even"),
        None
    )

    if func is None:
        errors.append(
            "Missing or incorrect function name. "
            "Expected 'check_odd_even'."
        )

    else:
        # 3. Check exact parameter
        args = func.args
        params = [arg.arg for arg in args.args]

        if (
            params != ["n"]
            or args.posonlyargs
            or args.kwonlyargs
            or args.vararg is not None
            or args.kwarg is not None
            or args.defaults
            or args.kw_defaults
        ):
            errors.append(
                "Incorrect parameters. Expected exactly (n)."
            )

        # 4. Check return statement
        has_return = any(
            isinstance(node, ast.Return)
            for node in ast.walk(func)
        )

        if not has_return:
            errors.append(
                "Missing return statement. "
                "The function must return 'Odd' or 'Even'."
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

        check_odd_even = namespace["check_odd_even"]

        # 6. Test function outputs
        test_cases = [
            (2, "Even"),
            (3, "Odd"),
            (0, "Even"),
            (1, "Odd"),
            (-2, "Even"),
            (-3, "Odd"),
            (100, "Even"),
            (101, "Odd")
        ]

        for n, expected in test_cases:
            result = check_odd_even(n)

            assert result == expected, (
                f"Incorrect result for n={n}. "
                f"Expected '{expected}', but got '{result}'."
            )

    except AssertionError:
        raise

    except Exception as e:
        pytest.fail(
            f"Error while executing check_odd_even(n): {e}",
            pytrace=False
        )
