# Wrap each WIDE figure in its own LANDSCAPE section (tight margins so the resized figure fits one page).
import sys, re
src, dst = sys.argv[1], sys.argv[2]
WIDE = ['chronology_web.png', 'fig_kawthar_synthesis.png', 'fig_inner_self_net.png', 'fig_inner_self_graph.png', 'fig_inner_self_organ_core.png']
PORT = '\n```{=openxml}\n<w:p><w:pPr><w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" w:bottom="1440" w:left="1440" w:right="1440" w:header="720" w:footer="720"/></w:sectPr></w:pPr></w:p>\n```\n'
LAND = '\n```{=openxml}\n<w:p><w:pPr><w:sectPr><w:pgSz w:w="15840" w:h="12240" w:orient="landscape"/><w:pgMar w:top="540" w:bottom="540" w:left="720" w:right="720" w:header="360" w:footer="360"/></w:sectPr></w:pPr></w:p>\n```\n'
lines = open(src, encoding='utf-8').read().split('\n')
out = []; n = 0
for ln in lines:
    if ln.lstrip().startswith('![') and any(w in ln for w in WIDE):
        ln = re.sub(r'\{[^}]*\}\s*$', '', ln).rstrip()
        out.append(PORT.rstrip('\n')); out.append(ln); out.append(LAND.rstrip('\n')); n += 1
    else:
        out.append(ln)
open(dst, 'w', encoding='utf-8').write('\n'.join(out))
print("landscapeified figures:", n, "->", dst)
