"""🐍 - Write Python with Emojis

"""

# Standard library imports
import ast
import pathlib
import sys

# Third party imports
import emoji

DELIMITERS = ("__pythonji_", "__")


def main():
    py_files = [f for f in sys.argv[1:] if f.endswith(".🐍")]
    for py_file in py_files:
        run(py_file)


def run(py_file):
    """Run 🐍 on the given file"""
    new_path = demojize(pathlib.Path(py_file).resolve())
    execute(py_file, new_path)


def demojize(py_path):
    """Replace emojis by strings in the given file"""
    py_text = py_path.read_text()
    python_text = emoji.demojize(py_text, delimiters=DELIMITERS)
    return emojize_literals(python_text)


class EmojiTransformer(ast.NodeTransformer):
    def visit_Str(self, node):
        return ast.copy_location(
            ast.Str(s=emoji.emojize(node.s, delimiters=DELIMITERS)), node
        )


def emojize_literals(text):
    """Translate emojis in literal strings back to emojis"""
    tree = ast.parse(text)
    for node in ast.walk(tree):
        node = EmojiTransformer().visit(node)

    return tree


def execute(py_path, python_ast):
    """Run Python on the given AST"""
    exec(compile(python_ast, py_path, mode="exec"))


if __name__ == "__main__":
    main()
