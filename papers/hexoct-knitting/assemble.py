#!/usr/bin/env python3
"""paper.src.html + swatch sections from studies/2026-10-31-hexoct-knitting/gen -> paper.html"""
import os, sys
H = os.path.dirname(os.path.abspath(__file__))
G = os.path.join(H, '../../studies/2026-10-31-hexoct-knitting/gen')
sys.path.insert(0, os.path.join(H, '../../studies/2026-10-31-hexoct-knitting/scripts'))
COMMON = open(os.path.join(H, '../../studies/2026-10-31-hexoct-knitting/scripts/hexknit.py')).read().split("COMMON = '''")[1].split("'''")[0]
COMMON = COMMON.replace('<h2>How to knit every swatch</h2>', '<h3>How to knit every swatch</h3>')
parts = []
for i, n in enumerate(['4H', '3C', '2H', '6H', 'Fibonacci']):
    s = open(os.path.join(G, n, 'section.html')).read().replace('<h3>', f'<h3>{chr(65 + i)}. ', 1)
    pre = ('<h2>Appendix: the five swatches</h2>' + COMMON) if i == 0 else ''
    parts.append(f'<div class="app">{pre}{s}</div>')
src = open(os.path.join(H, 'paper.src.html')).read()
open(os.path.join(H, 'paper.html'), 'w').write(src.replace('<!--APPENDIX-->', '\n'.join(parts)))
print('paper.html written')
