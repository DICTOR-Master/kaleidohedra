# helper for the one-off fills of 13 Nov 2026: replace a NEW marker, or insert after/before an anchor, each exactly once
import os, re
C = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'chapters')
def edit(fn, pairs):
    p = os.path.join(C, fn); s = open(p, encoding='utf8').read()
    for kind, a, b in pairs:
        n = s.count(a)
        if n != 1: raise SystemExit(f'{fn}: anchor found {n} times: {a[:80]!r}')
        if kind == 'rep': s = s.replace(a, b)
        elif kind == 'after': s = s.replace(a, a + b)
        elif kind == 'before': s = s.replace(a, b + a)
    open(p, 'w', encoding='utf8').write(s); print('edited', fn)
def FIG(src, key, alt, cap, style=''):
    st = f' style="{style}"' if style else ''
    return f'<figure{st}><img src="figures/new/{src}" alt="{alt}"><figcaption><b>Figure {{{{F:{key}}}}}.</b> {cap}</figcaption></figure>\n'
def W(title, body): return f'<div class="worked"><b class="wt">Worked example: {title}.</b> {body}</div>\n'
def OPEN(t): return f'<p class="opener">{t}</p>\n'
def HAND(t): return f'<p class="handoff">{t}</p>\n'
