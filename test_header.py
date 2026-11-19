import ast

def test_function_header():
    with open("header1.py") as f:
        header = f.read().strip()

    # Add temporary body
    code = header + "\n    pass"

    tree = ast.parse(code)
    func = tree.body[0]

    # Check function name
    assert isinstance(func, ast.FunctionDef)
    assert func.name == "calc_area"

    # Check exactly 2 parameters
    assert len(func.args.args) == 2

    # Reject extra parameter types and default values
    assert not func.args.posonlyargs
    assert not func.args.kwonlyargs
    assert func.args.vararg is None
    assert func.args.kwarg is None
    assert not func.args.defaults
    assert not func.args.kw_defaults
