import ast
import re
import tokenize
import io
import pytest


def test_function_header():

    with open("header2.py", encoding="utf-8-sig") as f:
        source = f.read()

    errors = []

    # Ignore docstrings, comments, and blank lines
    lines = []

    tokens = tokenize.generate_tokens(io.StringIO(source).readline)

    try:
        for token in tokens:
            if token.type in (
                tokenize.STRING,
                tokenize.COMMENT,
                tokenize.NL,
                tokenize.NEWLINE,
                tokenize.ENDMARKER
            ):
                continue

            if token.line.strip():
                if token.start[0] not in [n for n, _ in lines]:
                    lines.append((token.start[0], token.line.strip()))

    except (tokenize.TokenError, IndentationError):
        pass

    if not lines:
        pytest.fail("No function header found.", pytrace=False)

    # Get the first actual code line
    header = lines[0][1]

    # Check def keyword
    if not re.match(r"^def\b", header):
        errors.append("Missing or incorrect 'def' keyword.")

    # Check function name
    match = re.match(
        r"^(?:\w+\s+)?([a-zA-Z_]\w*)\s*\(",
        header
    )

    if match:
        name = match.group(1)

        if name != "my_function2":
            errors.append(
                f"Incorrect function name '{name}'. "
                "Expected 'my_function2'."
            )
    else:
        errors.append("Unable to identify the function name.")

    # Check parentheses
    if "(" not in header:
        errors.append("Missing opening parenthesis '('.")

    if ")" not in header:
        errors.append("Missing closing parenthesis ')'.")

    # Check colon
    if not header.endswith(":"):
        errors.append("Missing colon ':'.")

    # Check parameters
    if "(" in header and ")" in header:
        start = header.index("(")
        end = header.index(")", start)

        params = [
            p.strip()
            for p in header[start + 1:end].split(",")
        ]

        if params != ["x", "y"]:
            errors.append(
                "Incorrect parameters. Expected (x, y)."
            )

    # Check Python syntax
    if not errors:
        try:
            tree = ast.parse(header + "\n    pass")
            func = tree.body[0]

            if not isinstance(func, ast.FunctionDef):
                errors.append("Invalid function definition.")

            elif (
                func.args.posonlyargs
                or func.args.kwonlyargs
                or func.args.vararg is not None
                or func.args.kwarg is not None
                or func.args.defaults
                or func.args.kw_defaults
            ):
                errors.append(
                    "Only two ordinary parameters, x and y, are allowed."
                )

        except SyntaxError as e:
            errors.append(f"Invalid Python syntax: {e.msg}")

    if errors:
        feedback = "\n".join(
            f"{i}. {error}"
            for i, error in enumerate(errors, 1)
        )

        pytest.fail(
            "\nFUNCTION HEADER ERRORS:\n" + feedback,
            pytrace=False
        )
