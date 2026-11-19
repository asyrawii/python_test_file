import ast

def test_function_header():
    with open("header2.py", encoding="utf-8") as f:
        header = f.read().strip()

    # Add temporary body
    code = header + "\n    pass"

    tree = ast.parse(code)
    func = tree.body[0]

    # Check function name
    assert isinstance(func, ast.FunctionDef)
    assert func.name == "my_function2"

    # Check exact parameter names and order
    params = [arg.arg for arg in func.args.args]
    assert params == ["x", "y"]

    # Reject extra parameters or default values
    assert not func.args.posonlyargs
    assert not func.args.kwonlyargs
    assert func.args.vararg is None
    assert func.args.kwarg is None
    assert not func.args.defaults
    assert not func.args.kw_defaults
