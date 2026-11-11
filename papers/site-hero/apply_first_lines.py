#!/usr/bin/env python3
"""Put the everyday first lines (card-first-lines/make.py NEW) above the ten hardest cards' text, and take the DOI
out of #22's title (it stays in the card's DOI badge). Usage: apply_first_lines.py <index.html> (edits in place)."""
import re, sys, importlib.util, html
p = sys.argv[1]; s = open(p).read()
spec = importlib.util.spec_from_file_location('fl', '~/k-research/papers/card-first-lines/make.py')
src = open('~/k-research/papers/card-first-lines/make.py').read()
NEW = {}; exec(src[src.index('NEW = {'):src.index('ORDER =')], {}, ns := {}); NEW = ns['NEW']
n = 0
for k, line in NEW.items():
    pat = re.compile(r'(<span class="num">' + re.escape(k) + r'</span>.*?</span>)(<span class="s">)', re.S)
    s, c = pat.subn(lambda m: m.group(1) + '<span class="ev">' + html.escape(line, quote=False) + '</span>' + m.group(2), s, count=1)
    assert c == 1, k; n += 1
old22 = ' <span class="soon">DOI 10.5281/zenodo.23310541</span>'
assert s.count(old22) == 1; s = s.replace(old22, '')
css = '    .paper .ev { color: var(--text); font-size: 14px; line-height: 1.45; padding: 4px 12px 6px; border-left: 3px solid var(--gold); margin: 6px 12px 6px; }\n'
s = s.replace('    .paper .s { color: var(--muted);', css + '    .paper .s { color: var(--muted);', 1)
assert '.paper .ev' in s
open(p, 'w').write(s); print('first lines', n, '+ #22 title fixed')
