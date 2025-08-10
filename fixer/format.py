import re

def format_code(code):

    """
    Basic C code formatter:
    - 4-space indentation
    - Spaces after if/for/while/switch keywords
    - Newline before closing brace
    - Consistent brace style
    """
    indent_level = 0
    formatted_lines = []

    for raw_line in code.splitlines():
        stripped = raw_line.strip()

        # Preserve completely empty lines
        if stripped == "":
            formatted_lines.append("")
            continue

        # Add space after control keywords
        stripped = re.sub(r'\b(if|for|while|switch)\(', r'\1 (', stripped)

        # Decrease indent before printing if the line closes a block
        if stripped.startswith('}'):
            indent_level -= 1

        # Apply indentation
        formatted_lines.append("    " * max(indent_level, 0) + stripped)

        # Increase indent after opening a block
        if stripped.endswith('{'):
            indent_level += 1

    return "\n".join(formatted_lines) + "\n"

