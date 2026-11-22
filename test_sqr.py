# Write a Python3 function *sqr(n)* that returns the square of its numeric parameter *n*.
"""Sample code
def sqr(n):
    return n * n
"""
import ast
import pytest
from tabulate import tabulate


def test_sqr():

    # 1. Read student file
    with open("exercise_1.py", encoding="utf-8-sig") as f:
        source = f.read()

    # 2. Check Python syntax
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        pytest.fail(
            f"Syntax error: {e.msg}",
            pytrace=False
        )

    # 3. Find sqr function
    func = next(
        (
            node for node in tree.body
            if isinstance(node, ast.FunctionDef)
            and node.name == "sqr"
        ),
        None
    )

    if func is None:
        pytest.fail(
            "Incorrect or missing function name. Expected 'sqr'.",
            pytrace=False
        )

    # 4. Check parameter
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
        pytest.fail(
            "Incorrect parameters. Expected exactly (n).",
            pytrace=False
        )

    # 5. Check return statement
    if not any(
        isinstance(node, ast.Return)
        for node in ast.walk(func)
    ):
        pytest.fail(
            "Missing return statement. "
            "The function must return the square of n.",
            pytrace=False
        )

    # 6. Load only the function
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
    except Exception as e:
        pytest.fail(
            f"Unable to load function: {type(e).__name__}: {e}",
            pytrace=False
        )

    sqr = namespace["sqr"]

    # 7. Test cases
    test_cases = [
        (1, 1),
        (5, 25),
        (-3, 9),
        (0, 0),
        (1.5, 2.25),
        (-2.5, 6.25)
    ]

    results = []
    passed = 0

    # 8. Run each test case
    for n, expected in test_cases:

        try:
            actual = sqr(n)

            if (
                isinstance(actual, (int, float))
                and not isinstance(actual, bool)
                and actual == pytest.approx(expected)
            ):
                status = "PASS"
                passed += 1
            else:
                status = "FAIL"

        except Exception as e:
            actual = f"Error: {type(e).__name__}"
            status = "FAIL"

        results.append([
            n,
            expected,
            actual,
            status
        ])

    # 9. Display results table
    print("\nFUNCTION TEST RESULTS: sqr(n)\n")

    print(tabulate(
        results,
        headers=[
            "Test Input (n)",
            "Expected Output",
            "Student Output",
            "Status"
        ],
        tablefmt="grid"
    ))

    # 10. Display summary
    total = len(test_cases)
    failed = total - passed

    print("\n" + "=" * 40)
    print(f"Total Tests  : {total}")
    print(f"Passed       : {passed}")
    print(f"Failed       : {failed}")
    print(f"Score        : {passed}/{total}")
    print("=" * 40)

    # 11. Final pytest result without traceback
    if failed > 0:
        pytest.fail(
            f"{failed} out of {total} test cases failed.",
            pytrace=False
        )
