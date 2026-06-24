"""Structural coherence audit — run before each release / after adding or
re-versioning any tab. Catches the silent drift that reactive tweaks create:
a page that exists but isn't in the nav, the deploy manifest, the Help tour, or
the Home/About blurb. Run:  python audit_app.py   (exit code 1 if hard drift).

Best practice (see SpatialAnalysis/FINDINGS_LEDGER.md §0c): periodic AUDIT, not
per-change tweaks. Cross-cutting surfaces must move together with every tab.
"""
import glob
import os
import re
import subprocess
import sys

NAV = open("state.py", encoding="utf-8").read()
MANI_SRC = open("deploy_git.py", encoding="utf-8").read()
HELP = open("pages/0_Help.py", encoding="utf-8").read().lower()
APP = open("app.py", encoding="utf-8").read().lower()

# obsolete pages (declared dead in deploy_git.py) — local-only, expected absent live
OBSOLETE = set(re.findall(r'"(pages/[^"]+\.py)"', MANI_SRC[MANI_SRC.find("OBSOLETE"):]
                          if "OBSOLETE" in MANI_SRC else ""))
# local -> deployed(HF) path map from the UPLOADS manifest
MAP = dict(re.findall(r'"(pages/[^"]+\.py)":\s*"(pages/[^"]+\.py)"', MANI_SRC))
# admin-only page: reachable by direct URL, intentionally NOT in the public nav (see state.py note)
INTENTIONAL_NO_NAV = {"pages/9_Usage.py"}
# Deployment is `git push hf main` — it ships every TRACKED file, not the legacy UPLOADS dict.
# So "deployed" = git-tracked. (Fall back to the manifest text only if git is unavailable.)
try:
    _ls = subprocess.run(["git", "ls-files"], capture_output=True, text=True)
    TRACKED = set(x.replace("\\", "/") for x in _ls.stdout.splitlines()) if _ls.returncode == 0 else None
except Exception:
    TRACKED = None


def title_of(p):
    return re.sub(r"^\d+[a-z]?_", "", os.path.basename(p)[:-3]).replace("_", " ")


def nav_label(p):
    """The human-facing nav title for a page, e.g. 'The Sūra' — matched against Help/About."""
    m = re.search(r'"' + re.escape(p) + r'"\s*,\s*"([^"]+)"', NAV)
    return m.group(1) if m else ""


def main():
    hard = []
    soft = []
    print(f"{'page':36} {'NAV':4} {'DEPLOY':6} {'HELP':5} {'ABOUT':5}")
    print("-" * 62)
    for p in sorted(glob.glob("pages/*.py")):
        p = p.replace("\\", "/")           # normalise Windows separators to match state.py / manifest
        if p.endswith(".bak"):
            continue
        hf = MAP.get(p, p)
        in_nav = (p in NAV) or (hf in NAV)
        in_dep = (p in TRACKED) if TRACKED is not None else ((p in MAP) or (p in MANI_SRC))
        t = title_of(p)
        tok = t.split()[0].lower()
        label = nav_label(p)
        hits = [tok, t.lower()] + ([label.lower()] if label else [])
        in_help = any(h and h in HELP for h in hits)
        in_about = any(h and h in APP for h in hits)
        obs = p in OBSOLETE
        print(f"{os.path.basename(p):36} {('✔' if in_nav else '✘'):^4}"
              f"{('✔' if in_dep else '✘'):^6} {('✔' if in_help else '·'):^5}"
              f"{('✔' if in_about else '·'):^5}")
        if not obs and p not in INTENTIONAL_NO_NAV:
            if not in_nav:
                hard.append(f"{os.path.basename(p)} missing from NAV_SECTIONS (state.py)")
            if not in_dep:
                hard.append(f"{os.path.basename(p)} not git-tracked (won't ship in `git push`)")
            if not in_help:
                soft.append(f"{os.path.basename(p)} not mentioned in Help (0_Help.py)")
            if not in_about:
                soft.append(f"{os.path.basename(p)} not mentioned in Home/About (app.py)")

    # ---- LOCKED UI RULE: no font smaller than 12px anywhere (px or root-relative rem). ----
    # em units are parent-relative (a 0.6em verse number inside a 26px Arabic line ≈ 16px) so they are NOT
    # flagged; matplotlib `fontsize=` is in points on offline exports and is also excluded (we match `font-size:`).
    for fp in sorted(glob.glob("*.py") + glob.glob("pages/*.py")):
        fp = fp.replace("\\", "/")
        try:
            src = open(fp, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        for ln, line in enumerate(src.splitlines(), 1):
            if " in s" in line or " in src" in line:
                continue                                   # skip detection strings (e.g. apply_ledgers checks)
            for m in re.finditer(r'font-size\s*:\s*["\']?(\d+(?:\.\d+)?)\s*(px|rem|em|%)', line):
                val = float(m.group(1)); unit = m.group(2)
                if unit in ("em", "%"):
                    continue                               # parent-relative — indeterminate, not flagged
                px = val if unit == "px" else val * 16     # rem → root-relative (16px base)
                if px < 12 - 1e-9:
                    hard.append(f"{fp}:{ln} font-size {m.group(0).strip()} (~{px:.0f}px) — below the 12px floor")
            if ("<table" in line and "width:100%" in line
                    and "table-layout:fixed" not in line and "max-width" not in line):
                soft.append(f"{fp}:{ln} unbounded <table width:100%> without table-layout:fixed — add a colgroup, "
                            "a max-width, or a width:100% 'fill' column so it doesn't sprawl with gaps")
    print()
    if hard:
        print("HARD DRIFT (breaks the app — fix before release):")
        for d in hard:
            print("  ✘", d)
    else:
        print("HARD DRIFT: none — nav + deploy are coherent.")
    if soft:
        print("SOFT DRIFT (docs out of sync — advisory):")
        for d in soft:
            print("  ·", d)
    sys.exit(1 if hard else 0)


if __name__ == "__main__":
    main()
