# fixer/syntax_fix.py
import re

def fix_syntax(code: str) -> str:
    """
    Fixes very simple syntax issues in C code.
    Wraps quick_syntax_checks_and_fix with autofix=True.
    """
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
    Heuristics:
      - Check unmatched braces { }
      - Check simple missing semicolons after lines that look like statements
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

    # 2) simple missing semicolon heuristic:
    lines = code.splitlines()
    new_lines = []
    stmt_like = re.compile(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*\s+)?[a-zA-Z_][a-zA-Z0-9_]*.*[^;{}\s]$')
    for i, ln in enumerate(lines, start=1):
        stripped = ln.strip()
        if stripped == "" or stripped.startswith('#') or stripped.endswith('{') or stripped.endswith('}') or stripped.startswith('//') or stripped.startswith('/*'):
            new_lines.append(ln)
            continue
        if stmt_like.match(ln):
            issues.append(f"Possible missing semicolon at line {i}: {ln.strip()}")
            if autofix:
                new_lines.append(ln + ';')
                issues.append(f"Auto-inserted ';' at line {i}")
                continue
        new_lines.append(ln)

    fixed_code = "\n".join(new_lines)
    return fixed_code, issues
