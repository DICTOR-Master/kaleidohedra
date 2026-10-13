# Build paper.html from paper.md (markdown-it-py) for printing to paper.pdf (headless Chromium, print.mjs). Run on dicto-node.
# DICTO · dictospheres.com
import sys, os
from markdown_it import MarkdownIt
HERE = os.path.dirname(os.path.abspath(__file__))
md = MarkdownIt('commonmark', {'html': False}).enable('table')
body = md.render(open(os.path.join(HERE, 'paper.md'), encoding='utf-8').read())
css = """
@page { size: A4; margin: 16mm 15mm 18mm; }
body { font: 9.6pt/1.45 "Noto Serif", "DejaVu Serif", Georgia, serif; color: #1b1f24; margin: 0; }
h1 { font: 700 20pt/1.2 "Noto Sans", "DejaVu Sans", sans-serif; margin: 0 0 3mm; }
h2 { font: 700 12.5pt/1.3 "Noto Sans", "DejaVu Sans", sans-serif; margin: 6mm 0 2mm; color: #9a3f00; }
p, li { text-align: justify; hyphens: auto; }
table { border-collapse: collapse; width: 100%; font: 7pt/1.3 "Noto Sans", "DejaVu Sans", sans-serif; margin: 2mm 0 3mm; page-break-inside: auto; }
th, td { border-bottom: 0.4pt solid #ccd; padding: 1.2mm 1mm; vertical-align: top; text-align: left; }
th { background: #fff3e9; }
tr { page-break-inside: avoid; }
img { width: 100%; display: block; margin: 3mm 0 1mm; page-break-inside: avoid; }
p:has(> img) { page-break-inside: avoid; }
code { font-size: 8pt; }
hr { border: 0; border-top: 0.5pt solid #ccc; }
"""
html = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Capturing the In-betweens (DICTO, draft)</title><style>{css}</style></head><body>{body}</body></html>'
open(os.path.join(HERE, 'paper.html'), 'w', encoding='utf-8').write(html)
print('ok', len(html))
