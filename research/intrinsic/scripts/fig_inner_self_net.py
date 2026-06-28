# -*- coding: utf-8 -*-
"""Static print render of the inner-self NETWORK (matches the interactive app figure).
Bare Arabic labels (NO definite article) per the locked convention; valence-coloured edges;
دنیا (near) and آخرة (lasting) as two CO-PRESENT orientations; veil is perceptual; barzakh demoted. Nodes/edges MEASURED; layout INFERRED."""
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, FancyArrowPatch
import re, arabic_reshaper
from bidi.algorithm import get_display
_resh = arabic_reshaper.ArabicReshaper(configuration={'delete_harakat': False, 'support_ligatures': False})
_AR = re.compile(r'[؀-ۿ]+(?:\s+[؀-ۿ]+)*')
def A(s):
    return _AR.sub(lambda m: get_display(_resh.reshape(m.group().replace('ک','ك').replace('ی','ي'))), s) if s else s

INK = '#10243A'
ROLE = {'self': '#1D3557', 'cog': '#378ADD', 'act': '#0F6E56', 'up': '#1D9E75', 'down': '#E63946',
        'amp': '#EF9F27', 'bound': '#7A5AA6', 'dom': '#94A3B8', 'out_g': '#0F6E56', 'out_r': '#C1121F',
        'root': '#B5651D'}
VAL = {'g': '#1D9E75', 'r': '#E63946', 'o': '#EF9F27', 'n': '#94A3B8'}

N = {
 'allah': ['الله', 650, 66, 'root'],
 'nafs': ['نفس', 462, 452, 'self'], 'sadr': ['صدر', 366, 452, 'self'],
 'qalb': ['قلب', 414, 498, 'self'], 'fuad': ['فؤاد', 225, 560, 'self'],
 'ilm': ['علم·عقل', 590, 360, 'cog'], 'amal': ['عمل صالح', 590, 590, 'act'],
 'zann': ['ظنّ', 300, 690, 'down'], 'hawa': ['هوی', 150, 610, 'down'],
 'dhikr': ['ذکر', 230, 250, 'up'], 'taqwa': ['تقوی', 390, 180, 'up'],
 'iman': ['إیمان', 520, 165, 'up'], 'huda': ['هدی', 640, 195, 'up'],
 'lahw': ['لهو·لعب', 120, 400, 'down'], 'waswas': ['وسواس·شیطان', 150, 300, 'down'],
 'taswil': ['تسویل·نفس', 270, 500, 'down'], 'marad': ['مرض', 430, 660, 'down'],
 'tab': ['طبع·ختم', 560, 690, 'down'], 'zad': ['زاد', 730, 470, 'amp'],
 'barzakh': ['برزخ', 1150, 455, 'bound'], 'ghita': ['غطاء', 770, 300, 'bound'], 'dunya': ['دنیا', 1140, 600, 'dom'],
 'akhira': ['آخرة·حیوان', 1140, 310, 'dom'], 'kawthar': ['کوثر', 1040, 205, 'out_g'],
 'abtar': ['أبتر', 1030, 705, 'out_r'],
}
E = [
 ['ilm', 'amal', 'n', 0.0], ['amal', 'ilm', 'g', 0.35], ['amal', 'ilm', 'r', -0.35],
 ['dhikr', 'ilm', 'g', 0], ['taqwa', 'ilm', 'g', 0], ['iman', 'amal', 'g', 0],
 ['huda', 'qalb', 'g', 0], ['ilm', 'qalb', 'n', 0], ['amal', 'nafs', 'n', 0],
 ['zann', 'ilm', 'r', 0], ['hawa', 'nafs', 'r', 0], ['hawa', 'amal', 'r', 0.2],
 ['lahw', 'dhikr', 'r', 0], ['waswas', 'sadr', 'r', 0], ['taswil', 'nafs', 'r', 0],
 ['marad', 'qalb', 'r', 0], ['tab', 'qalb', 'r', 0], ['zad', 'kawthar', 'g', 0.2],
 ['zad', 'abtar', 'r', 0.2], ['ilm', 'zad', 'g', 0.1], ['marad', 'zad', 'r', 0.1],
 ['amal', 'dunya', 'r', 0.18], ['amal', 'akhira', 'g', -0.18], ['hawa', 'dunya', 'r', 0.1],
 ['lahw', 'dunya', 'r', 0], ['nafs', 'dunya', 'n', 0.12], ['nafs', 'akhira', 'n', -0.12],
 ['dunya', 'abtar', 'r', 0.12], ['akhira', 'kawthar', 'g', 0.12], ['qalb', 'akhira', 'g', 0.2],
 ['ghita', 'fuad', 'n', 0], ['ghita', 'akhira', 'g', 0.25], ['nafs', 'barzakh', 'n', 0],
 ['allah', 'qalb', 'n', 0], ['allah', 'zad', 'n', 0], ['sadr', 'qalb', 'n', 0], ['nafs', 'sadr', 'n', 0],
]
plt.rcParams.update({'font.family': 'DejaVu Sans', 'text.color': INK})
W, H = 1300.0, 780.0
fig, ax = plt.subplots(figsize=(15.2, 9.8)); ax.set_xlim(0, W); ax.set_ylim(-55, H); ax.axis('off'); ax.invert_yaxis()
ax.add_patch(FancyBboxPatch((8, 30), 1284, 736, boxstyle='round,pad=2,rounding_size=16', fc='none', ec='#E2E8F1', lw=1.4))
ax.add_patch(FancyBboxPatch((18, 36), 1264, 58, boxstyle='round,pad=2,rounding_size=12', fc='#F4EEE7', ec='#E3D3C4', lw=1))
ax.text(700, 66, 'the root — over all', fontsize=12, color='#8a6d2f', fontweight='bold', va='center')
ax.add_patch(FancyBboxPatch((60, 108), 1180, 648, boxstyle='round,pad=2,rounding_size=14', fc='#F8FAFC', ec='none'))
ax.text(1232, 150, 'oriented to the lasting (akhira) -> kawthar', ha='right', fontsize=12, color='#0F6E56', fontweight='bold')
ax.text(1232, 660, 'oriented to the near (dunya) -> abtar', ha='right', fontsize=12, color='#8a6d2f', fontweight='bold')
ax.text(20, -28, "The inner-self network — qalb processes · nafs acts · fuʾad senses; zad amplifies; outcome = kawthar or abtar",
        fontsize=16.5, fontweight='bold', color='#1D3557')
ax.text(20, -2, "all nodes & edges MEASURED on the rasm · layout an INFERRED reading · "
                "green → the lasting/openness · red → the near/severance · gold = zad feedback · grey = structure", fontsize=12.5, color=INK)
for a, b, val, cv in E:
    if a not in N or b not in N:
        continue
    x1, y1 = N[a][1], N[a][2]; x2, y2 = N[b][1], N[b][2]
    rad = (cv or 0) * 1.1
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), connectionstyle="arc3,rad=%g" % rad,
                 arrowstyle='-|>', mutation_scale=11, lw=1.7, color=VAL[val], alpha=.72, zorder=2,
                 shrinkA=15, shrinkB=15))
RAD = {'root': 26, 'self': 21, 'amp': 19, 'bound': 17, 'dom': 21, 'out_g': 22, 'out_r': 22}
for k, (lab, x, y, role) in N.items():
    r = RAD.get(role, 16); c = ROLE[role]
    ax.add_patch(Circle((x, y), r, fc=c, ec='#fff', lw=2.2, zorder=3))
    ax.text(x, y - r - 9, A(lab), ha='center', va='bottom', fontsize=13.5, color=c, fontweight='bold', zorder=4)
leg = [('self / organ', '#1D3557'), ('cognition', '#378ADD'), ('action', '#0F6E56'),
       ('up-driver (->open)', '#1D9E75'), ('down-driver (->severance)', '#E63946'),
       ('feedback (zad)', '#EF9F27'), ('veil / partition', '#7A5AA6'),
       ('outcome: kawthar', '#0F6E56'), ('outcome: abtar', '#C1121F'), ('divine root', '#B5651D')]
lx, ly = 20, 742
for name, col in leg:
    w = 30 + 8.1 * len(name)
    if lx + w > W - 10:
        lx, ly = 20, ly + 24
    ax.add_patch(Circle((lx, ly), 7, fc=col, ec='none'))
    ax.text(lx + 14, ly, name, fontsize=11.5, color=INK, va='center')
    lx += w
plt.tight_layout()
out = "/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2/research/intrinsic/kawthar_figs/fig_inner_self_net.png"
plt.savefig(out, dpi=150, bbox_inches='tight', facecolor='white'); print("wrote", out)
