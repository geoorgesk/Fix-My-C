import os
import sys
import tempfile
from pycparser import parse_file
import fixer.format as format_fixer
import fixer.syntax_fix as syntax_fixer

# Location of pycparser's fake libc includes
FAKE_LIBC_INCLUDE = os.path.join(
    os.path.dirname(__file__),
    "fake_libc_include"
)

def autofix_code(input_path):
    """Fix syntax and formatting issues before parsing."""
    with open(input_path, "r") as f:
        code = f.read()

    fixed_code = syntax_fixer.fix_syntax(code)
    fixed_code = format_fixer.format_code(fixed_code)

    fixed_path = input_path.replace(".c", "_fixed.c")
    with open(fixed_path, "w") as f:
        f.write(fixed_code)

    return fixed_path


def analyze_with_pycparser(file_path):
    """Parse code with pycparser using fake includes."""
    try:
        ast = parse_file(
            file_path,
            use_cpp=True,
            cpp_path="gcc",  # or 'clang' if on macOS
            cpp_args=[f"-E", f"-I{FAKE_LIBC_INCLUDE}"]
        )
        ast.show()
    except Exception as e:
        print(f"[ERROR] pycparser failed: {e}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python cfix.py <file.c>")
        sys.exit(1)

    input_file = sys.argv[1]

    # Always autofix before analyzing
    fixed_file = autofix_code(input_file)

    print(f"[INFO] Fixed file saved as: {fixed_file}")
    print("[INFO] Running pycparser AST analysis...\n")

    analyze_with_pycparser(fixed_file)


if __name__ == "__main__":
    main()
