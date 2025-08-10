#!/usr/bin/env python3
import sys
from fixer.syntax_fix import quick_syntax_checks_and_fix
from analyzer.ast_analyze import analyze_with_pycparser
from fixer.format import format_c_code
from analyzer.dsa_suggest import dsa_suggestions

def main():
    if len(sys.argv) < 2:
        print("Usage: python cfix.py file.c [--autofix]")
        return
    path = sys.argv[1]
    autofix = "--autofix" in sys.argv

    with open(path, 'r', encoding='utf-8') as f:
        code = f.read()

    # Step 1: Syntax & heuristic fixes
    fixed_code, issues = quick_syntax_checks_and_fix(code, autofix=autofix)
    print("--- Syntax/Heuristic Issues ---")
    for it in issues:
        print(it)

    # Step 2: AST semantic analysis
    print("\n--- AST Semantic Analysis ---")
    analyze_with_pycparser(fixed_code)

    # Step 3: DSA suggestions
    print("\n--- DSA Suggestions ---")
    for sug in dsa_suggestions(fixed_code):
        print(sug)

    # Step 4: Save formatted fixed code (if autofix)
    if autofix:
        fixed_code = format_c_code(fixed_code)
        out = path.replace('.c', '_fixed.c')
        with open(out, 'w', encoding='utf-8') as f:
            f.write(fixed_code)
        print(f"\nAuto-fixed & formatted code saved to: {out}")

if __name__ == "__main__":
    main()
