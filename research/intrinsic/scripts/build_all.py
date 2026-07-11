import subprocess, os, shutil, sys
ROOT="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2/research/intrinsic"
P=ROOT+"/papers"; S=ROOT+"/scripts"; FIGD=ROOT+"/kawthar_figs"
DELIV="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2/Kawthar_Paper"
WIDE=[FIGD+"/chronology_web.png", FIGD+"/fig_kawthar_synthesis.png", FIGD+"/fig_inner_self_net.png", FIGD+"/fig_inner_self_graph.png", FIGD+"/fig_inner_self_organ_core.png"]
jobs=[("kawthar_EN_technical.md","Surah_al-Kawthar_EN_technical",False),
      ("kawthar_EN_plain.md","Surah_al-Kawthar_EN_plain",False),
      ("kawthar_FA_plain.md","Surah_al-Kawthar_FA_plain",True)]
def run(c):
    r=subprocess.run(c,cwd=S,capture_output=True,text=True,timeout=600)
    tail=(r.stdout+r.stderr).strip().splitlines()[-2:] if (r.stdout+r.stderr).strip() else []
    print("  $", " ".join(os.path.basename(x) if "/" in x else x for x in c[:3]),"->", " | ".join(tail))
    return r
for md,base,rtl in jobs:
    print("==== building", base, "====")
    land=P+"/"+md.replace(".md","_land.md")
    run(["python3",S+"/landscapeify.py", P+"/"+md, land])
    docx=P+"/"+base+".docx"; pdf=P+"/"+base+".pdf"
    cmd=["python3",S+"/build_toc.py", land, docx, pdf]+(["rtl"] if rtl else [])
    run(cmd)
    for fig in WIDE:
        run(["python3",S+"/resize_fig.py", docx, fig, "9.3"])
    # re-export pdf after resize (single soffice pass)
    run(["soffice","--headless","--convert-to","pdf","--outdir",P,docx])
    # copy to deliverables (best-effort; user may have a file open/locked)
    for ext in (".docx",".pdf"):
        srcf=P+"/"+base+ext; dstf=DELIV+"/"+base+ext
        try:
            shutil.copy(srcf,dstf); print("  copied ->",os.path.basename(dstf))
        except Exception as e:
            alt=DELIV+"/"+base+"__UPDATED"+ext; shutil.copy(srcf,alt)
            print("  LOCKED, wrote ->",os.path.basename(alt),"(",e,")")
print("DONE")
