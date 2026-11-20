import ast
import io
import re
import tokenize
import pytest


def test_function_header():

    with open("header1.py", encoding="utf-8-sig") as f:
        source = f.read()

    errors = []
    header = None

    # Ignore docstrings, comments and blank lines
    try:
        tokens = tokenize.generate_tokens(
            io.StringIO(source).readline
        )

        for token in tokens:
            if token.type in (
                tokenize.STRING,
                tokenize.COMMENT,
                tokenize.NL,
                tokenize.NEWLINE,
                tokenize.ENDMARKER,
                tokenize.ENCODING
            ):
                continue

            header = token.line.strip()
            break

    except (tokenize.TokenError, IndentationError):
        pass

    if not header:
        pytest.fail(
            "No function header found.",
            pytrace=False
        )

    # 1. Check def keyword
    if not re.match(r"^def\b", header):
        errors.append(
            "Missing or incorrect 'def' keyword."
        )

    # 2. Check function name
    match = re.match(
        r"^(?:\w+\s+)?([a-zA-Z_]\w*)\s*\(",
        header
    )

    if match:
        name = match.group(1)

        if name != "my_function1":
            errors.append(
                f"Incorrect function name '{name}'. "
                "Expected 'my_function1'."
            )
    else:
        errors.append(
            "Unable to identify the function name."
        )

    # 3. Check parentheses
    if "(" not in header:
        errors.append(
            "Missing opening parenthesis '('."
        )

    if ")" not in header:
        errors.append(
            "Missing closing parenthesis ')'."
        )

    # 4. Check colon
    if not header.endswith(":"):
        errors.append(
            "Missing colon ':' at the end."
        )

    # 5. Check parameters (must be empty)
    if "(" in header and ")" in header:
        start = header.index("(")
        end = header.index(")", start)

        params = header[start + 1:end].strip()

        if params:
            errors.append(
                "Function my_function1 must not have parameters."
            )

    # 6. Check Python syntax
    if not errors:
        try:
            tree = ast.parse(header + "\n    pass")
            func = tree.body[0]

            if not isinstance(func, ast.FunctionDef):
                errors.append(
                    "Invalid function definition."
                )

        except SyntaxError as e:
            errors.append(
                f"Invalid Python syntax: {e.msg}"
            )

    # Display all errors
    if errors:
        feedback = "\n".join(
            f"{i}. {error}"
            for i, error in enumerate(errors, 1)
        )

        pytest.fail(
            "\nFUNCTION HEADER ERRORS:\n" + feedback,
            pytrace=False
        )
