#!/usr/bin/env python3
"""Inspect / download from the public OpenNeuro Narratives dataset (ds002345) WITHOUT the AWS CLI
or credentials. Uses botocore (installed with awscli) + UNSIGNED requests.

Default = SCAN ONLY (lists keys, downloads nothing): tells us exactly what preprocessed BOLD and
word-onset files exist, so we don't pull GBs blindly.

    python fetch_narratives.py                       # scan + report (no download)
    python fetch_narratives.py --get <KEY> [<KEY>..] # stream-download specific keys to --out
    python fetch_narratives.py --out D:\narr --get ds002345/derivatives/.../bold.nii.gz
"""
import os, sys, shutil, argparse
from collections import defaultdict
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
        r=s3.list_objects_v2(**kw)
        keys+=[o["Key"] for o in r.get("Contents",[])]
        if not r.get("IsTruncated"): break
        tok=r.get("NextContinuationToken")
    return keys

def scan():
    print(f"listing ALL keys under s3://{BUCKET}/{DS}/ (no bytes downloaded)…")
    allk=list_keys(f"{DS}/"); print(f"total keys: {len(allk)}\n")
    # top-level structure (second path component)
    tops=defaultdict(int)
    for k in allk:
        p=k.split("/")
        tops[p[1] if len(p)>1 else "(root)"]+=1
    print("top-level entries under the dataset:")
    for t,n in sorted(tops.items(), key=lambda x:-x[1]): print(f"  {t:<24} {n}")
    def show(label, keys):
        print(f"\n{label}: {len(keys)}")
        for k in sorted(keys)[:8]: print("   ",k)
    L=lambda s:s.lower()
    show("preproc/MNI BOLD (preproc_bold + MNI152)",
         [k for k in allk if "preproc_bold.nii" in k and "MNI152" in k])
    show("ANY derivatives/ keys",
         [k for k in allk if "/derivatives/" in k or k.startswith(f"{DS}/derivatives")])
    show("pieman BOLD (any)",
         [k for k in allk if "task-pieman" in k and k.endswith("bold.nii.gz")])
    show("word timing? (gentle/align/transcript/textgrid/.csv/.tsv)",
         [k for k in allk if any(t in L(k) for t in ("gentle","align","transcript","textgrid"))
          or (k.endswith((".csv",".tsv")) and "participants" not in L(k))])
    print("\n=> Paste this output back. If preproc/MNI BOLD and word-timing both exist, I'll give "
          "the exact --get keys. If derivatives/alignments are NOT in this bucket, we switch plan "
          "(they live in the Narratives GitHub/derivatives release, or we pick a dataset that "
          "bundles everything).")

def get(keys, outdir):
    os.makedirs(outdir, exist_ok=True)
    for key in keys:
        dst=os.path.join(outdir, os.path.basename(key))
        print(f"downloading {key}\n  -> {dst}")
        body=s3.get_object(Bucket=BUCKET, Key=key)["Body"]
        with open(dst,"wb") as f: shutil.copyfileobj(body, f, length=1024*1024)
    print("done.")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--get", nargs="*", default=None, help="specific S3 keys to download")
    ap.add_argument("--out", default="narratives_data")
    a=ap.parse_args()
    if a.get: get(a.get, a.out)
    else: scan()

if __name__=="__main__": main()
