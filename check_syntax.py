"""Quick syntax sanity check for every .py file in this folder.

Exits with code 0 if everything parses, 1 if any file has a SyntaxError.
Skips dot-folders and __pycache__.
"""
from __future__ import annotations

import ast
import pathlib
import sys


def main() -> int:
    here = pathlib.Path(__file__).resolve().parent
    errors = 0
    for p in here.rglob("*.py"):
        rel = p.relative_to(here)
        if any(part.startswith(".") or part == "__pycache__"
               for part in rel.parts):
            continue
        try:
            ast.parse(p.read_text(encoding="utf-8"))
        except SyntaxError as e:
            print(f"  SYNTAX ERROR in {rel}: {e}")
            errors += 1
    if errors:
        return 1
    print("  All .py files parse cleanly.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
