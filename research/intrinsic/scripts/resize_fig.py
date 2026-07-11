import sys, hashlib
from docx import Document
from docx.shared import Inches
docx_path, src_png, width_in = sys.argv[1], sys.argv[2], float(sys.argv[3])
src_md5=hashlib.md5(open(src_png,'rb').read()).hexdigest()
# png dims from header (no PIL dependency)
import struct
with open(src_png,'rb') as f:
    f.read(16); w,h=struct.unpack('>II', f.read(8))
d=Document(docx_path); n=0
for sh in d.inline_shapes:
    try:
        rId=sh._inline.graphic.graphicData.pic.blipFill.blip.embed
        part=d.part.related_parts[rId]
        if hashlib.md5(part.blob).hexdigest()==src_md5:
            sh.width=Inches(width_in); sh.height=Inches(width_in*h/w); n+=1
    except Exception: pass
d.save(docx_path)
print(f"resized {n} shape(s) to {width_in}in (png {w}x{h}, h->{width_in*h/w:.2f}in)")
