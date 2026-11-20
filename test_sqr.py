# Write a Python3 function *sqr(n)* that returns the square of its numeric parameter *n*.
"""Sample code
def sqr(n):
    return n * n
"""
import ast
import pytest


def test_sqr():

    with open("exercise_1.py", encoding="utf-8-sig") as f:
        source = f.read()

    errors = []

    # 1. Check syntax
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        pytest.fail(
            f"Invalid Python syntax: {e.msg}",
            pytrace=False
        )

    # 2. Find function
    functions = [
        node for node in tree.body
        if isinstance(node, ast.FunctionDef)
    ]

    func = next(
        (f for f in functions if f.name == "sqr"),
        None
    )

    if func is None:
        errors.append(
            "Missing or incorrect function name. Expected 'sqr'."
        )

    else:
        # 3. Check parameter
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
                "Missing return statement."
            )

    # Stop if structural errors exist
    if errors:
        pytest.fail(
            "\nFUNCTION ERRORS:\n" + "\n".join(errors),
            pytrace=False
        )

    # 5. Execute only the function definition
    module = ast.Module(body=[func], type_ignores=[])
    ast.fix_missing_locations(module)

    namespace = {}

    try:
        exec(compile(module, "<student>", "exec"), namespace)

        sqr = namespace["sqr"]

        # 6. Test function outputs
        test_cases = [
            (2, 4),
            (5, 25),
            (-3, 9),
            (0, 0),
            (1.5, 2.25)
        ]

        for value, expected in test_cases:
            result = sqr(value)

            assert result == pytest.approx(expected), (
                f"Incorrect result for n={value}. "
                f"Expected {expected}, but got {result}."
            )

    except AssertionError:
        raise

    except Exception as e:
        pytest.fail(
            f"Error while executing sqr(n): {e}",
            pytrace=False
        )
