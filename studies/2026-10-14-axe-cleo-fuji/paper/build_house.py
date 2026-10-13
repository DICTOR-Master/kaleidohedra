# The AXE, CLEO and FUJI paper in DICTO's house style (copied from Capturing the In-betweens) (papers/paper.css; standing practice 2026-10-14): gold-ruled header with DICTO's credit line,
# version · date · DOI · licence · data, the gold DICTO logo, the abstract box, a faint logo watermark on every page; the footer
# (title · DICTO · dictospheres.com · DOI · page) is added when printing (print.mjs). Writes paper-house.html. Run on dicto-node.
import os, re
from markdown_it import MarkdownIt
HERE = os.path.dirname(os.path.abspath(__file__))
md = MarkdownIt('commonmark', {'html': False}).enable('table')
src = open(os.path.join(HERE, 'paper.md'), encoding='utf-8').read()
abstract = src.split('## Abstract', 1)[1].split('\n---', 1)[0]
rest = src.split('## 1. Introduction', 1)[1]
body = md.render('## 1. Introduction' + rest)
css = open(os.path.join(HERE, 'house.css'), encoding='utf-8').read()
html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>AXE, CLEO and FUJI</title><style>{css}
.logo {{ float: right; width: 30mm; margin: 0 0 4mm 6mm; }}
.watermark {{ position: fixed; top: 50%; left: 50%; width: 120mm; transform: translate(-50%, -50%); opacity: .05; z-index: -1; }}
img {{ max-width: 100%; }}
.lead {{ width: 100%; margin: 2mm 0 4mm; }}
table {{ font-size: 7pt; }}
</style></head><body>
<img class="watermark" src="dicto-logo.png" alt="">
<img class="logo" src="dicto-logo.png" alt="DICTO">
<h1>AXE, CLEO and FUJI</h1>
<p class="sub">The gap pieces of the icosahedron: the three pieces that close DICTO's thirteen-icosahedron cluster into one larger icosahedron, and where they recur</p>
<div class="meta">
<b>DICTO</b> (artist, Osaka, Japan) · contact@dictospheres.com · https://dictospheres.com<br>
Version 1 · 14 October 2026 · DOI 10.5281/zenodo.23351292 · Licence CC BY 4.0 · Data, scripts, figures, nets and checks: studies/2026-10-14-axe-cleo-fuji and studies/2026-10-10-icosa-13 at https://github.com/DICTOR-Master/kaleidohedra.<br>
The structures, the pieces and all their names, and the 63-piece build are DICTO's. Computation and checking with Claude (Anthropic).
</div>
<img class="lead" src="figures/fig1-pieces.jpg" alt="AXE, CLEO and FUJI"><p class="cap"><b>Figure 1.</b> (a) AXE, (b) CLEO and (c) FUJI, at one scale.</p>
<div class="abstract"><b>Abstract.</b> {md.render(abstract.strip())}</div>
{body}
</body></html>'''
open(os.path.join(HERE, 'paper-house.html'), 'w', encoding='utf-8').write(html)
print('ok', len(html))
