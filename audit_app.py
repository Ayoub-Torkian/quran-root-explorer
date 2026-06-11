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


def title_of(p):
    return re.sub(r"^\d+[a-z]?_", "", os.path.basename(p)[:-3]).replace("_", " ")


def main():
    hard = []
    soft = []
    print(f"{'page':36} {'NAV':4} {'DEPLOY':6} {'HELP':5} {'ABOUT':5}")
    print("-" * 62)
    for p in sorted(glob.glob("pages/*.py")):
        if p.endswith(".bak"):
            continue
        hf = MAP.get(p, p)
        in_nav = (p in NAV) or (hf in NAV)
        in_dep = (p in MAP) or (p in MANI_SRC)
        t = title_of(p)
        tok = t.split()[0].lower()
        in_help = tok in HELP or t.lower() in HELP
        in_about = tok in APP or t.lower() in APP
        obs = p in OBSOLETE
        print(f"{os.path.basename(p):36} {('✔' if in_nav else '✘'):^4}"
              f"{('✔' if in_dep else '✘'):^6} {('✔' if in_help else '·'):^5}"
              f"{('✔' if in_about else '·'):^5}")
        if not obs:
            if not in_nav:
                hard.append(f"{os.path.basename(p)} missing from NAV_SECTIONS (state.py)")
            if not in_dep:
                hard.append(f"{os.path.basename(p)} missing from deploy manifest (deploy_git.py)")
            if not in_help:
                soft.append(f"{os.path.basename(p)} not mentioned in Help (0_Help.py)")
            if not in_about:
                soft.append(f"{os.path.basename(p)} not mentioned in Home/About (app.py)")
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
