# -*- coding: utf-8 -*-
"""Regenerate figures with the embedded 'Figure N.' caption-title REMOVED (it duplicates the
markdown caption, and is English even in the FA paper). Panel titles (not starting with 'Figure')
are kept. Usage: python run_notitle.py <script1.py> <script2.py> ..."""
import sys, os
import matplotlib; matplotlib.use('Agg')
import matplotlib.axes, matplotlib.figure, matplotlib.pyplot as plt

def _is_fig(t): return isinstance(t,str) and t.strip().lower().startswith('figure')
_st=matplotlib.axes.Axes.set_title
def _skip_st(self,label='',*a,**k):
    if _is_fig(label): return self.title
    return _st(self,label,*a,**k)
matplotlib.axes.Axes.set_title=_skip_st
_sup=matplotlib.figure.Figure.suptitle
def _skip_sup(self,t='',*a,**k):
    if _is_fig(t): return None
    return _sup(self,t,*a,**k)
matplotlib.figure.Figure.suptitle=_skip_sup
# pyplot.title/suptitle delegate to the above, but patch defensively
_pt=plt.title; plt.title=lambda label='',*a,**k:(None if _is_fig(label) else _pt(label,*a,**k))
_ps=plt.suptitle; plt.suptitle=lambda t='',*a,**k:(None if _is_fig(t) else _ps(t,*a,**k))

SD="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2/research/intrinsic/scripts"
for s in sys.argv[1:]:
    path=s if os.path.isabs(s) else f"{SD}/{s}"
    print("### running (no Figure-title):", os.path.basename(path))
    g={'__name__':'__main__','__file__':path}
    try:
        exec(compile(open(path,encoding='utf-8').read(),path,'exec'), g)
    except SystemExit:
        pass
print("done.")
