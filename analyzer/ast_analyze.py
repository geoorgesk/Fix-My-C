from pycparser import c_parser, c_ast, parse_file
import sys
import tempfile

def analyze_with_pycparser(code):
    parser = c_parser.CParser()
    try:
        ast = parser.parse(code)
    except Exception as e:
        print("pycparser failed to parse code:", e)
        print("Run the tool with --autofix and fix syntax issues first.")
        return

    # Traverse AST to find declarations and uses (simple)
    decls = {}
    uses = []

    class VarVisitor(c_ast.NodeVisitor):
        def visit_Decl(self, node):
            if isinstance(node.type, c_ast.TypeDecl):
                name = node.name
                decls[name] = node.coord
        def visit_ID(self, node):
            uses.append((node.name, node.coord))

    v = VarVisitor()
    v.visit(ast)

    # Find IDs used before declaration (very naive: compare line numbers)
    for name, coord in uses:
        if name in decls:
            decl_line = decls[name].line
            use_line = coord.line
            if use_line < decl_line:
                print(f"[WARNING] Variable '{name}' used before declaration (use line {use_line}, decl line {decl_line})")

    # Unused variables
    for name, coord in list(decls.items()):
        used = any(u == name for u, _ in uses)
        if not used:
            print(f"[INFO] Declared variable '{name}' at line {coord.line} seems unused")

    print("AST analysis complete (basic checks).")

