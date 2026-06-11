"""One-shot helper: add the Two Books lens to the grouped nav in state.py.
Safe, idempotent, preserves UTF-8 and line endings. Run once:  python add_nav.py
"""
import io, sys

F = "state.py"
NEW_KEY = "24_Two_Books_Genome"
ANCHOR = "23_Structural_Twins.py"
# "Two Books · Genome" with a middle dot (U+00B7) and the DNA emoji (U+1F9EC)
NEW_TUPLE = '("pages/24_Two_Books_Genome.py", "Two Books · Genome", "\U0001f9ec"),'

src = io.open(F, encoding="utf-8").read()
if NEW_KEY in src:
    print("already present - nothing to do")
    sys.exit(0)

nl = "\r\n" if "\r\n" in src else "\n"
lines = src.split(nl)
out, inserted = [], False
for ln in lines:
    out.append(ln)
    if ANCHOR in ln and not inserted:
        indent = ln[:len(ln) - len(ln.lstrip())]
        out.append(indent + NEW_TUPLE)
        inserted = True

if not inserted:
    print("could not find the Structural Twins line - state.py unchanged")
    sys.exit(1)

io.open(F, "w", encoding="utf-8", newline="").write(nl.join(out))
print("added the Two Books lens to the nav. Now run: .\\deploy.bat")
