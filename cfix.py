#!/usr/bin/env python3
import sys
from fixer.syntax_fix import quick_syntax_checks_and_fix
from analyzer.ast_analyze import analyze_with_pycparser

def main():
    if len(sys.argv) < 2:
        print("Usage: python cfix.py file.c [--autofix]")
        return
    path = sys.argv[1]
    autofix = "--autofix" in sys.argv

    with open(path, 'r', encoding='utf-8') as f:
        code = f.read()

    fixed_code, issues = quick_syntax_checks_and_fix(code, autofix=autofix)
    print("--- Syntax/Heuristic Issues ---")
    for it in issues:
        print(it)

    # Try AST-based analysis (needs syntactically valid C)
    print("\n--- AST Semantic Analysis ---")
    analyze_with_pycparser(fixed_code)

    if autofix:
        out = path.replace('.c', '_fixed.c')
        with open(out, 'w', encoding='utf-8') as f:
            f.write(fixed_code)
        print(f"\nAuto-fixed code saved to: {out}")

if __name__ == "__main__":
    main()
