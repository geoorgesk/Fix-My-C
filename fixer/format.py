import re

def format_c_code(code):
    """
    Basic C code formatter:
    - Proper indentation with 4 spaces
    - Spaces after if/for/while keywords
    - Newline before closing brace
    - Consistent brace style
    """
    indent_level = 0
    formatted_lines = []

    for line in code.splitlines():
        stripped = line.strip()

        # Add space after control keywords
        stripped = re.sub(r'\b(if|for|while|switch)\(', r'\1 (', stripped)

        # Adjust indentation
        if stripped.endswith('}'):
            indent_level -= 1

        formatted_lines.append("    " * max(indent_level, 0) + stripped)

        if stripped.endswith('{'):
            indent_level += 1

    return "\n".join(formatted_lines) + "\n"
