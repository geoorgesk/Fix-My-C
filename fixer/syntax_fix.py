# fixer/syntax_fix.py
import re

# Recognized leading type keywords (used to detect declarations/function signatures)
TYPE_KEYWORDS = r'(?:int|void|char|float|double|long|short|unsigned|signed|struct|const|static)'

# Regex: detect "declaration followed immediately by something else on same line"
_decl_and_rest_re = re.compile(
    r'^(?P<indent>\s*)'
    r'(?P<decl>' + TYPE_KEYWORDS + r'\b[^;{]*)'   # starts with a type keyword and continues (no semicolon/braces)
    r'\s+(?P<rest>[A-Za-z_].*)$'                   # then something else that starts with an identifier (likely a call)
)

def fix_syntax(code: str) -> str:
    fixed_code, issues = quick_syntax_checks_and_fix(code, autofix=True)

    if issues:
        print("[SYNTAX FIXER] Issues detected and fixed:")
        for issue in issues:
            print("  -", issue)
    else:
        print("[SYNTAX FIXER] No issues detected.")

    return fixed_code


def quick_syntax_checks_and_fix(code, autofix=False):
    """
    Safer heuristics:
      - Balance unmatched braces (append closing braces if needed)
      - Fix a few common argument mistakes in scanf/printf
      - Split lines where a declaration and another statement are accidentally combined
      - Add semicolons to statement-like lines conservatively
    Returns (fixed_code, issues_list)
    """
    issues = []

    # 1) unmatched braces
    open_braces = code.count('{')
    close_braces = code.count('}')
    if open_braces != close_braces:
        issues.append(f"Brace mismatch: {{ {open_braces} vs }} {close_braces}")
        if autofix and open_braces > close_braces:
            add = open_braces - close_braces
            code = code + ("\n" + ("}" * add)) + "\n"
            issues.append(f"Auto-inserted {add} '}}' at EOF")

    # Work line-by-line with safer handling
    lines = code.splitlines()
    new_lines = []

    for i, ln in enumerate(lines, start=1):
        stripped = ln.strip()

        # preserve blank lines and comments and preprocessor
        if stripped == "" or stripped.startswith('#') or stripped.startswith('//') or stripped.startswith('/*'):
            new_lines.append(ln)
            continue

        # preserve lines that are block starts/ends directly
        if stripped.endswith('{') or stripped.endswith('}'):
            new_lines.append(ln)
            continue

        # tiny arg fix for scanf/printf: "&a & b" -> "&a, &b"
        if autofix and ('scanf' in ln or 'printf' in ln):
            fixed_args = re.sub(r'(&\s*[A-Za-z_][A-Za-z0-9_]*)\s*&', r'\1, &', ln)
            if fixed_args != ln:
                issues.append(f"Fixed missing comma in args at line {i}: {ln.strip()} -> {fixed_args.strip()}")
                ln = fixed_args
                stripped = ln.strip()

        # If the line appears to be a function signature/prototype/declaration (starts with a type keyword and ends with ')')
        # we skip adding semicolons (they are separate constructs).
        # But if a declaration is accidentally concatenated with another statement on the same line, split it.
        m = _decl_and_rest_re.match(ln)
        if m:
            decl = m.group('decl').rstrip()
            rest = m.group('rest').lstrip()
            indent = m.group('indent') or ''
            # split into two lines: declaration + semicolon, then the rest
            new_decl_line = indent + decl + ';'
            new_rest_line = indent + rest
            issues.append(f"Split combined declaration+statement at line {i}: '{decl}' | '{rest[:40]}...'")
            new_lines.append(new_decl_line)
            new_lines.append(new_rest_line)
            continue

        # Conservative statement detection:
        # If the line contains a '(' (likely a function call) or '=' (assignment) and does NOT end with ';',
        # then it's probably a statement that needs a semicolon.
        if (('(' in stripped or '=' in stripped) and not stripped.endswith(';')):
            # avoid adding semicolon to control statements' header (if/for/while/switch)
            if not (stripped.startswith('if ') or stripped.startswith('for ') or stripped.startswith('while ') or stripped.startswith('switch ') or stripped.endswith(')')):
                # add semicolon
                issues.append(f"Possible missing semicolon at line {i}: {stripped}")
                if autofix:
                    new_lines.append(ln + ';')
                    issues.append(f"Auto-inserted ';' at line {i}")
                    continue

        # Default: keep the line as-is
        new_lines.append(ln)

    fixed_code = "\n".join(new_lines)
    return fixed_code, issues
