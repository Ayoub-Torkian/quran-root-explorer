#!/usr/bin/env python3
"""Build a minimal BIDS-valid dataset for ONE subject so fMRIPrep can run on it. fMRIPrep needs
the T1w anatomical + the BOLD + their JSON sidecars + dataset-level metadata — not just the loose
BOLD files we downloaded for steps 1–2. This pulls all of that from the public OpenNeuro mirror
(unsigned) into a `bids/` root, preserving BIDS paths.

    python fetch_bids_subject.py --sub sub-001 --out bids
    python fetch_bids_subject.py --sub sub-001 --tasks pieman --out bids   # only pieman func (smaller)

Then point fMRIPrep at the `bids/` directory (see FMRIPREP_SETUP.md).
"""
import os, sys, argparse, shutil
from botocore import UNSIGNED
from botocore.config import Config
import botocore.session

BUCKET="openneuro.org"; DS="ds002345"
s3=botocore.session.get_session().create_client("s3", config=Config(signature_version=UNSIGNED))

def list_keys(prefix):
    keys=[]; tok=None
    while True:
        kw=dict(Bucket=BUCKET, Prefix=prefix, MaxKeys=1000)
        if tok: kw["ContinuationToken"]=tok
        r=s3.list_objects_v2(**kw); keys+=[o["Key"] for o in r.get("Contents",[])]
        if not r.get("IsTruncated"): break
        tok=r.get("NextContinuationToken")
    return keys

def get(key, outroot):
    rel=key[len(DS)+1:]                      # strip "ds002345/"
    dst=os.path.join(outroot, rel); os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.exists(dst) and os.path.getsize(dst)>0: return
    print("  ", rel)
    body=s3.get_object(Bucket=BUCKET, Key=key)["Body"]
    with open(dst,"wb") as f: shutil.copyfileobj(body, f, length=1024*1024)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--sub", required=True)
    ap.add_argument("--tasks", nargs="*", default=["pieman"], help="func tasks to include (default pieman); use ALL for everything")
    ap.add_argument("--out", default="bids")
    a=ap.parse_args(); os.makedirs(a.out, exist_ok=True)

    # 1) dataset-level metadata (required for a valid BIDS root)
    print("dataset-level files:")
    for k in list_keys(f"{DS}/"):
        rel=k[len(DS)+1:]
        if "/" not in rel and (rel.endswith(".json") or rel in ("participants.tsv","README","CHANGES","dataset_description.json")):
            get(k, a.out)
        # top-level task sidecars like task-pieman_bold.json
        if "/" not in rel and rel.endswith("_bold.json"):
            get(k, a.out)

    # 2) the subject: all of anat/, and func/ filtered to the requested tasks
    print(f"subject {a.sub}:")
    subkeys=list_keys(f"{DS}/{a.sub}/")
    if not subkeys: raise SystemExit(f"no keys for {a.sub} — check the subject id.")
    want=lambda rel: ("/anat/" in rel) or ("/func/" in rel and (
        "ALL" in a.tasks or any(f"task-{t}" in rel for t in a.tasks))) or rel.endswith("_scans.tsv")
    got_anat=False
    for k in subkeys:
        rel=k[len(DS)+1:]
        if want(rel):
            if "/anat/" in rel: got_anat=True
            get(k, a.out)
    if not got_anat:
        print(f"  WARNING: no anat/ for {a.sub}. fMRIPrep needs a T1w; try another subject or "
              f"--tasks ALL to inspect. Listing anat candidates:")
        for k in subkeys:
            if "anat" in k.lower() or "T1w" in k: print("   ", k[len(DS)+1:])
    print(f"\nBIDS root ready at: {os.path.abspath(a.out)}")
    print("Validate (optional):  deno?/npx bids-validator", a.out)
    print("Next: see FMRIPREP_SETUP.md to run fMRIPrep on this BIDS root.")

if __name__=="__main__": main()
