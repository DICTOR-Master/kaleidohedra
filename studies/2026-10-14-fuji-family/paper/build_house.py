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
html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>The FUJI Family</title><style>{css}
.logo {{ float: right; width: 30mm; margin: 0 0 4mm 6mm; }}
.watermark {{ position: fixed; top: 50%; left: 50%; width: 120mm; transform: translate(-50%, -50%); opacity: .05; z-index: -1; }}
img {{ max-width: 100%; }}
.lead {{ width: 100%; margin: 2mm 0 4mm; }}
table {{ font-size: 7pt; }}
</style></head><body>
<img class="watermark" src="dicto-logo.png" alt="">
<img class="logo" src="dicto-logo.png" alt="DICTO">
<h1>The FUJI Family</h1>
<p class="sub">Pyramids on flat-ended triangles: from the tetrahedron through FUJI to the flat hexagon, the antiprism theorem, and the members found in tilings, crystals and our sculpture</p>
<div class="meta">
<b>DICTO</b> (artist, Osaka, Japan) · contact@dictospheres.com · https://dictospheres.com<br>
Version 4 · 14 October 2026 · DICTO DOI: 10.5281/zenodo.23357896 (all versions) · Licence CC BY 4.0 · Data, scripts, proofs and checks: studies/2026-10-14-fuji-family at https://github.com/DICTOR-Master/kaleidohedra.<br>
The family, FUJI, the dictospheres, the sculptures and all names are DICTO's. Computation, proofs and checking with Claude (Anthropic).
</div>
<div class="abstract"><b>Abstract.</b> {md.render(abstract.strip())}</div>
{body}
</body></html>'''
open(os.path.join(HERE, 'paper-house.html'), 'w', encoding='utf-8').write(html)
print('ok', len(html))
