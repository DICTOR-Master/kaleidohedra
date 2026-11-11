"""Site card picture for paper #89 (dictospheres.com, 1200 x 900 JPEG): the five golden pairs of the Platonic solids,
Greater Golden Cut on top, Lesser Golden Cut below, in D.I.C.T.O order, each column labelled with its four-dimensional
home: dodecahedra and icosahedra 120-cell, cubes rectified tesseract, tetrahedra tesseract, octahedra (Icosaxes,
Unborn Axes) 24-cell. Reuses the renderer and house colours of figs.py (gold = golden face, lilac = corner face);
dark background as the #78 and #76 cards; DICTO mark bottom right.
usage (compute-host): python card89.py <out.jpg> <logo png>
"""
import os, sys
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image

OUTJPG, LOGO = sys.argv[1:3]
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
TMP = os.path.splitext(OUTJPG)[0] + '-tmp'
# reuse figs.py: its definitions only (everything before the first figure)
src = open(os.path.join(HERE, 'figs.py')).read().split('\nxL3, xG5')[0]
NS = {'__file__': os.path.join(HERE, 'figs.py'), '__name__': 'figs_defs'}
sys.argv = [sys.argv[0], TMP, LOGO]; exec(src, NS)
gcb, G, render, mark = NS['gcb'], NS['G'], NS['render'], NS['mark']

BG, FG, DIM = '#0e0d12', '#ece9f2', '#a9a4b8'
c = {3: 1.0, 4: 2 ** .5, 5: G}                                     # c_n = 2 cos(pi/n)
xG = lambda n: G / (c[n] + 2 * G); xL = lambda n: 1 / (G * c[n] + 2)
COLS = [('dodecahedron', 5, 'Dodecahedra', '120-cell', ('Greater', 'Lesser')),
        ('icosahedron', 3, 'Icosahedra', '120-cell', ('Greater', 'Lesser')),
        ('cube', 4, 'Cubes', 'rectified tesseract', ('Greater', 'Lesser')),
        ('tetrahedron', 3, 'Tetrahedra', 'tesseract', ('Greater', 'Lesser')),
        ('octahedron', 3, 'Octahedra', '24-cell', ('Icosaxes', 'Unborn Axes'))]

plt.rcParams.update({'text.color': FG, 'font.size': 12})
fig = plt.figure(figsize=(12, 9), dpi=100, facecolor=BG)
fig.text(0.5, 0.935, 'All five golden pairs are slices of four-dimensional solids', ha='center', fontsize=21, color=FG)
fig.text(0.5, 0.893, 'Greater Golden Cut above, Lesser below · golden faces gold, corner faces lilac', ha='center', fontsize=12.5, color=DIM)
W, H0, gap = 0.172, 0.27, 0.014; left = (1 - 5 * W - 4 * gap) / 2
for k, (name, n, plural, home, labs) in enumerate(COLS):
    x0 = left + k * (W + gap)
    V = gcb.platonic(name); F = gcb.faces(V)
    for r, x in enumerate((xG(n), xL(n))):
        ax = fig.add_axes([x0, 0.575 - r * 0.325, W, H0]); ax.set_facecolor(BG)
        S = gcb.cut(V, F, [x] * len(V))[0]
        render(ax, S, '', view=(20, 24) if name != 'tetrahedron' else (18, 30))
        lab = labs[r] if name == 'octahedron' else ''
        ax.text(0.5, -0.02, lab, transform=ax.transAxes, ha='center', va='top', fontsize=12, color=FG)
    fig.text(x0 + W / 2, 0.858, plural, ha='center', fontsize=15, color=FG, weight='bold')
    fig.text(x0 + W / 2, 0.165, home, ha='center', fontsize=15, color='#d4af37')
fig.text(0.5, 0.105, '4D homes: four pairs in regular solids, the cubes in the rectified tesseract', ha='center', fontsize=13, color=DIM)
fig.text(0.5, 0.06, 'DICTO #89 · Golden Cuts beyond Plato', ha='center', fontsize=12, color=DIM)
mark(fig)
png = TMP + '.png'; fig.savefig(png, dpi=100, facecolor=BG); plt.close(fig)
im = Image.open(png).convert('RGB'); assert im.size == (1200, 900), im.size
im.save(OUTJPG, quality=88, optimize=True, progressive=True); os.remove(png)
try: os.rmdir(TMP)
except OSError: pass
print('written', OUTJPG, im.size)
