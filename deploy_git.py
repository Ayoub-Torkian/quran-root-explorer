"""Git-based deploy to the Hugging Face Space (no HF_TOKEN at runtime).

Strategy
--------
HF Spaces are themselves git repos.  Instead of using the HF API + write
token, we:
  1. Clone the Space repo into a hidden shadow workdir   .deploy_workdir/
     (only on first run — re-used on later runs)
  2. Copy every v1.2 file from this folder into the shadow tree, applying
     the local-name -> HF-name rename mapping
  3. git add / commit / push  ->  HF auto-rebuilds the Space

Auth: the FIRST push prompts for "Username" and "Password".  Use your HF
username for the username, and a WRITE token (hf_...) as the password.
Windows Credential Manager (or `git config --global credential.helper manager`)
caches it after that, so subsequent deploys need no token at all — that is
the "bypass" we are after.

Run from the v1.2 folder:
    python deploy_git.py
or via the one-click   deploy.bat .
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

REPO_URL = "https://huggingface.co/spaces/QuranProject/quran-root-explorer"
BRANCH   = "main"

HERE       = Path(__file__).resolve().parent
WORKDIR    = HERE / ".deploy_workdir"
TOKEN_FILE = HERE / ".hf_token"


def _get_token() -> str:
    """Return the HF write token, reading or prompting for it once."""
    if TOKEN_FILE.exists():
        t = TOKEN_FILE.read_text(encoding="utf-8").strip()
        if t.startswith("hf_"):
            return t
    print()
    print("Paste your Hugging Face WRITE token (starts with hf_):")
    print("  Create one at https://huggingface.co/settings/tokens/new?tokenType=write")
    t = input("Token: ").strip()
    if not t.startswith("hf_"):
        raise SystemExit("ERROR: token must start with hf_")
    TOKEN_FILE.write_text(t, encoding="utf-8")
    print(f"Saved to {TOKEN_FILE} (only on your computer).")
    return t


def _push_url(token: str) -> str:
    """Embed the token in the remote URL so git push doesn't prompt."""
    # HF accepts any username when paired with a write token.
    return REPO_URL.replace("https://", f"https://user:{token}@")

# local path in v1.2 folder  ->  path inside the HF Space repo
UPLOADS: dict[str, str] = {
    # Root-level python modules
    "topics.py":               "topics.py",
    "surface_divergence.py":   "surface_divergence.py",
    "interpret.py":            "interpret.py",
    "state.py":                "state.py",
    "analysis.py":             "analysis.py",
    "analytics.py":            "analytics.py",
    "plotly_charts.py":        "plotly_charts.py",
    "stats_charts.py":         "stats_charts.py",
    "stats_module.py":         "stats_module.py",
    "app.py":                  "app.py",
    "requirements.txt":        "requirements.txt",
    "README.md":               "README.md",
    "Book6.xlsx":              "Book6.xlsx",
    # v1.2 new root modules
    "pair_classification.py":  "pair_classification.py",
    "practical_lens.py":       "practical_lens.py",
    "CHANGELOG_v1.2.md":       "CHANGELOG_v1.2.md",
    # Pages with unchanged HF names
    "pages/0_Help.py":             "pages/0_Help.py",
    "pages/1_Per_Root_Profile.py": "pages/1_Per_Root_Profile.py",
    "pages/2_Network.py":          "pages/2_Network.py",
    "pages/3_Motifs.py":           "pages/3_Motifs.py",
    "pages/4_Ayah_Browser.py":     "pages/4_Ayah_Browser.py",
    "pages/5_Compare_Heatmaps.py": "pages/5_Compare_Heatmaps.py",
    "pages/6_Morphology.py":       "pages/6_Morphology.py",
    "pages/7_Statistics.py":       "pages/7_Statistics.py",
    "pages/9_Topic_Modeling.py":   "pages/9_Topic_Modeling.py",
    # v1.2 new pages — slotted into the open HF page numbers
    "pages/8e_Calibration.py":     "pages/8_Calibration.py",
    "pages/8f_Practical_Lens.py":  "pages/10_Practical_Lens.py",
    # Renamed pages
    "pages/8a_Interpret.py":       "pages/11_Interpret.py",
    "pages/8_Export.py":           "pages/12_Export.py",
    "pages/9_Usage.py":            "pages/13_Usage.py",
    # ── v1.3 Two Books section (names identical local↔HF so the nav resolves) ──
    "twobooks_stats.py":               "twobooks_stats.py",
    "pages/14_Disjoint_Letters.py":    "pages/14_Disjoint_Letters.py",
    "pages/15_Signal.py":              "pages/15_Signal.py",
    "pages/16_Biology.py":             "pages/16_Biology.py",
    "pages/17_Two_Books_Summary.py":   "pages/17_Two_Books_Summary.py",
    "CHANGELOG_v1.3.md":               "CHANGELOG_v1.3.md",
    "ROADMAP_TwoBooks.md":             "ROADMAP_TwoBooks.md",
    # ── v1.4 Spatial Patterns (point-pattern + areal GIS) ──
    "spatial_patterns.py":             "spatial_patterns.py",
    "spatial_forest.json":             "spatial_forest.json",
    "pages/18_Spatial_Patterns.py":    "pages/18_Spatial_Patterns.py",
    # ── v1.5 Deep Dives (concept + ayah-content, first-class endeavors) ──
    "deep_dive.py":                    "deep_dive.py",
    "report_dive.py":                  "report_dive.py",
    "pages/19_Concept_Deep_Dive.py":   "pages/19_Concept_Deep_Dive.py",
    "pages/20_Ayah_Deep_Dive.py":      "pages/20_Ayah_Deep_Dive.py",
    # ── v1.4 feedback/bug widgets (was missing from the whitelist!) ──
    "feedback.py":                     "feedback.py",
    "pages/21_Feedback_and_Bugs.py":   "pages/21_Feedback_and_Bugs.py",
    # ── v2.0 re-spine: Lens Lab + live lens runners + coverage embed + docs ──
    "lens_live.py":                    "lens_live.py",
    "pages/22_Lens_Lab.py":            "pages/22_Lens_Lab.py",
    "COVERAGE_MAP.html":               "COVERAGE_MAP.html",
    "CHANGELOG_v2.0.md":               "CHANGELOG_v2.0.md",
    "DESIGN_SYSTEM.md":                "DESIGN_SYSTEM.md",
}

# Files in the HF repo that should no longer exist (stale from earlier
# deploys).  Removed from the shadow tree before the commit.
OBSOLETE: list[str] = [
    "pages/8a_Interpret.py",
    "pages/8b_Topic_Map.py",
    "pages/8c_My_Topics.py",
    "pages/8d_Surface_Divergence.py",
    "pages/8e_Calibration.py",
    "pages/8f_Practical_Lens.py",
    "pages/8_Interpret.py",
    "pages/8_Export.py",
    "pages/9_Topic_Map.py",
    "pages/10_My_Topics.py",
    "pages/11_Surface_Divergence.py",
    # v1.3 Two Books pages renamed 8g–8j → 14–17 (remove the old letter-prefixed ones)
    "pages/8g_Disjoint_Letters.py",
    "pages/8h_Signal.py",
    "pages/8i_Biology.py",
    "pages/8j_Two_Books_Summary.py",
]


def run(cmd: list[str], *, cwd: Path | None = None, check: bool = True) -> int:
    """Run a command and stream output.  Returns exit code."""
    print(f"  $ {' '.join(cmd)}")
    r = subprocess.run(cmd, cwd=str(cwd) if cwd else None)
    if check and r.returncode != 0:
        print(f"  command failed with exit code {r.returncode}")
        sys.exit(r.returncode)
    return r.returncode


def ensure_clone() -> None:
    """Clone the HF Space if the shadow workdir does not exist yet."""
    if (WORKDIR / ".git").is_dir():
        print(f"  shadow workdir already exists: {WORKDIR}")
        # Pull latest so we don't push on top of a stale base.
        run(["git", "fetch", "origin", BRANCH], cwd=WORKDIR)
        run(["git", "checkout", BRANCH],        cwd=WORKDIR, check=False)
        run(["git", "reset", "--hard", f"origin/{BRANCH}"], cwd=WORKDIR)
        return

    if WORKDIR.exists():
        # Half-baked state — clean it.
        shutil.rmtree(WORKDIR)

    print(f"  cloning {REPO_URL}  ->  {WORKDIR}")
    run(["git", "clone", "--branch", BRANCH, REPO_URL, str(WORKDIR)])


def sync_files() -> tuple[int, int, int]:
    """Copy v1.2 files into the shadow tree, applying rename mapping.

    Returns (copied, removed, skipped)."""
    copied = removed = skipped = 0

    # 1. Remove obsolete files from the shadow tree
    for rel in OBSOLETE:
        target = WORKDIR / rel
        if target.exists():
            target.unlink()
            print(f"  remove  {rel}")
            removed += 1

    # 2. Copy renamed files
    for local, remote in UPLOADS.items():
        src = HERE / local
        if not src.exists():
            print(f"  SKIP (missing): {local}")
            skipped += 1
            continue
        dst = WORKDIR / remote
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        size = dst.stat().st_size
        print(f"  copy    {local}  ({size:>7} B)  ->  {remote}")
        copied += 1

    return copied, removed, skipped


def commit_and_push() -> int:
    """git add / commit / push.  Returns exit code (0 = success)."""
    # Identity (only matters once, and only if not already set globally)
    run(["git", "config", "user.email", "deploy@local"],   cwd=WORKDIR, check=False)
    run(["git", "config", "user.name",  "Quran Root Deploy"], cwd=WORKDIR, check=False)

    run(["git", "add", "-A"], cwd=WORKDIR)

    # Is there anything to commit?
    rc = subprocess.run(["git", "diff", "--cached", "--quiet"],
                        cwd=str(WORKDIR)).returncode
    if rc == 0:
        print("  nothing changed — skipping commit / push.")
        return 0

    msg = "Deep Dives: concept plain report -> full IMRaD (one compact companion table), matching ayah; added gated sense-cohesion line (surface-form Jaccard: cohesive/mixed/split) to all three concept registers; pruned orphaned helpers. Ayah deep dive unchanged by design (root-level, multi-root unit has no single-root morphology anchor)."
    run(["git", "commit", "-m", msg], cwd=WORKDIR)

    print()
    print("  pushing to Hugging Face (token from .hf_token, no prompt)...")
    token   = _get_token()
    push_to = _push_url(token)
    # Push to the token-embedded URL, but DON'T print it (token would leak).
    cmd = ["git", "push", push_to, f"HEAD:{BRANCH}"]
    print(f"  $ git push <token-redacted-url> HEAD:{BRANCH}")
    r = subprocess.run(cmd, cwd=str(WORKDIR))
    return r.returncode


def main() -> int:
    print()
    print("=" * 60)
    print(f"Deploying to {REPO_URL}  (git push, token-auth)")
    print("=" * 60)

    ensure_clone()
    copied, removed, skipped = sync_files()
    print()
    print(f"  Copied: {copied}   Removed: {removed}   Skipped: {skipped}")
    print()

    rc = commit_and_push()

    print()
    if rc == 0:
        print("  push succeeded - HF will auto-rebuild the Space.")
        print("  Live URL: https://quranproject-quran-root-explorer.hf.space/")
    else:
        print(f"  git push exited with code {rc}.  See messages above.")
        print("  If auth failed, check that .hf_token is a WRITE token from")
        print("  https://huggingface.co/settings/tokens (must start with hf_).")
    return rc


if __name__ == "__main__":
    sys.exit(main())
