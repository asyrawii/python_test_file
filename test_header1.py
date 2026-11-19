import ast

def test_function_header():
    with open("header1.py", encoding="utf-8") as f:
        header = f.read().strip()

    # Add temporary function body
    code = header + "\n    pass"

    tree = ast.parse(code)
    func = tree.body[0]

    # Check function name
    assert isinstance(func, ast.FunctionDef)
    assert func.name == "my_function1"

    # Check no parameters
    assert len(func.args.args) == 0
