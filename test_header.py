import ast
from pathlib import Path

STUDENT_FILE = "header1.py"


def test_function_header():

    # Read student's source code
    source = Path(STUDENT_FILE).read_text(encoding="utf-8-sig")

    # Parse without executing the program
    tree = ast.parse(source)

    # Find function definitions
    functions = [
        node for node in tree.body
        if isinstance(node, ast.FunctionDef)
    ]

    # Find calc_area
    matches = [
        func for func in functions
        if func.name == "my_function1"
    ]

    assert len(matches) == 1, \
        "Function calc_area must be defined exactly once."

    func = matches[0]

    # Check exactly 2 ordinary parameters
    assert len(func.args.args) == 0, \
        "calc_area must have exactly 0 parameters."

    # Reject additional parameter types
    assert not func.args.posonlyargs
    assert not func.args.kwonlyargs
    assert func.args.vararg is None
    assert func.args.kwarg is None

    # Reject default values
    assert not func.args.defaults
    assert not func.args.kw_defaults

    print("Function header is correct!")
