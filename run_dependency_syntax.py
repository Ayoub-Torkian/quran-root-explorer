"""One-shot local runner for MODALITY #47 (dependency-syntax).

WHAT IT DOES (automatically):
  1. installs `stanza` if missing
  2. downloads the Arabic UD model (~first run only)
  3. runs sequence_tests/dependency_syntax.py
  4. writes the full output to  evidence_47_results.txt  (paste that back to continue #47)

RUN:  python run_dependency_syntax.py
(That's it. First run downloads ~500MB of model + torch; later runs are fast.)
"""
import subprocess, sys, os, io, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "evidence_47_results.txt")


def ensure(pkg, import_name=None):
    try:
        __import__(import_name or pkg)
        return
    except ImportError:
        print(f"[setup] installing {pkg} ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])


def main():
    ensure("stanza")
    import stanza
    # download Arabic model once (no-op if already present)
    try:
        print("[setup] ensuring Arabic UD model (downloads on first run) ...")
        stanza.download("ar", verbose=False)
    except Exception as e:
        print(f"[setup] model download issue: {e!r}")
        print("        If this is a network error, run again on a connected machine.")
        return

    sys.path.insert(0, os.path.join(HERE, "sequence_tests"))
    sys.path.insert(0, HERE)
    import dependency_syntax as DS

    buf = io.StringIO()
    print("[run] parsing corpora and computing dependency metrics (this can take a few minutes) ...")
    try:
        with contextlib.redirect_stdout(buf):
            DS.main()
    except Exception as e:
        buf.write(f"\nERROR during run: {e!r}\n")
        import traceback; buf.write(traceback.format_exc())

    text = buf.getvalue()
    print(text)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"\n[done] results written to:\n  {OUT}\nPaste that file's contents back to complete EVIDENCE #47 + Lens 13.")


if __name__ == "__main__":
    main()
