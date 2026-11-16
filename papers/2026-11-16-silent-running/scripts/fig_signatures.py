#!/usr/bin/env python3
"""Figure 6, the silence-signature chart: every class or set of the law-giving census (its section 4 table) and of the
twisted-silence groups study (Table 3b of the paper) as a row of degree tiles k = 1 .. 20, grouped by the kind of law.
A silent tile is grey when the set's family already forces it (the census rows: the t = 2 neighbour on the same Wythoff
family is silent there too; the Table 3b rows: the twist group has no invariant there, the "forced" column), and takes the
colour of its kind when only this member is silent there. Kinds: (T) twisted silence Fire red, (X) extra symmetry Wind
yellow, (P) parity Water blue, (E) evenness Earth green, and the classical latitude or cosine-rule zeros (L) Void violet.
Open candidates are hatched. Ringing tiles are dark.
Data: data/fig-tones.json (scripts/fig_tones.py: census members, their neighbours, the 2I classes, X, F; zero patterns
asserted there) and, for the binary-octahedral, binary-tetrahedral, dihedral and matrix-sphere classes, the signatures of
Table 3b as stated in the paper (from studies/2026-11-15-twisted-silence-groups, data/tw_*.log), cut at k = 20.
Usage: fig_signatures.py tones.json out.png   (ends FINAL ok / FINAL FAIL)"""
import sys, json
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

GROUND = '#05050a'; INK = '#e6e1d3'; DIM = '#8d8a82'; RING = '#161924'; RINGE = '#2a2f3c'; GREY = '#7b7d84'
EL = {'Fire': '#cd3e28', 'Wind': '#e8c852', 'Water': '#3a70cd', 'Earth': '#488e48', 'Void': '#8a5cc4'}
KIND = {'T': ('(T) twisted silence', EL['Fire']), 'X': ('(X) extra symmetry', EL['Wind']), 'P': ('(P) parity', EL['Water']),
        'E': ('(E) evenness', EL['Earth']), 'L': ('(L) latitude or cosine rule, classical', EL['Void']),
        'O': ('open: candidates in 16 dimensions', '#c9c6bd'), 'N': ('twists with no unforced silence', GREY)}
fails = []
def check(ok, msg):
    print(('CHECK ok   ' if ok else 'CHECK FAIL ') + msg, flush=True)
    if not ok: fails.append(msg)
d = json.load(open(sys.argv[1])); S = d['sets']; K = 20
ALL = set(range(1, K + 1)); ODD = {k for k in ALL if k % 2}
def census(key, label, kind, law, nbkey=None):
    s = set(S[key]['silent']); nb = set(S[nbkey]['silent']) if nbkey else set(S[key].get('neighbour_silent', S[key]['silent'])); check(nb <= s, f'{key}: neighbour silences are a subset')
    return (kind, label, s, nb, set(), law)
def table(label, kind, silent, forced, law, open_=()):
    silent, forced = set(silent), set(forced); check(forced <= silent, f'{label}: forced within silent')
    return (kind, label, silent, forced, set(open_), law)
ROWS = [
    census('X', 'X, −X: perms of (φ², φ², φ², φ, 0) (20)', 'T', 'twisted characters of 2I', 'ctrl-X (3,3,3,2,0)'),
    census('F', 'F, −F: perms of (φ², φ², 1, 1, 0) (30)', 'T', 'twisted characters of 2I', 'ctrl-F (3,3,2,2,0)'),
    census('cuboctahedron (A3 x3o3t, t=1)', 'cuboctahedron (A3 line, t = 1)', 'X', 'centre of symmetry'),
    census('bitruncated 5-cell (A4 o3x3t3o, t=1)', 'bitruncated 5-cell (A4)', 'X', 'centre of symmetry'),
    census('runcinated 5-cell = R (A4 x3o3o3t, t=1)', 'runcinated 5-cell = R, the A4 roots', 'X', 'centre of symmetry'),
    census('omnitruncated 5-cell (A4 x3x3x3t, t=1)', 'omnitruncated 5-cell (A4)', 'X', 'centre of symmetry'),
    census('bitruncated 24-cell (F4 o3x4t3o, t=1)', 'bitruncated 24-cell (F4)', 'X', 'extended group [[3,4,3]]'),
    census('runcinated 24-cell (F4 x3o4o3t, t=1)', 'runcinated 24-cell (F4)', 'X', 'extended group [[3,4,3]]'),
    census('omnitruncated 24-cell (F4 x3x4x3t, t=1)', 'omnitruncated 24-cell (F4)', 'X', 'extended group [[3,4,3]]'),
    census('Icosaxes (B3 x3t4o, t=φ)', 'Icosaxes (#94; B3 line, t = φ)', 'X', 'two icosahedral halves'),
    table('2I, 30-point class (equator)', 'X', ODD, set(), 'antipodal (−1)'),
    table('2O twisted, 12-, 6-, 2-point classes', 'X', ODD, {1}, 'antipodal (−1)'),
    census('Kelvin truncated octahedron (B3 x3t4o, t=1)', "Kelvin's truncated octahedron", 'P', 'Dehn invariant 0 (site swap)'),
    census('24-cell (tesseract-16-cell line, μ=2)', '24-cell (tesseract–16-cell line)', 'P', 'Dehn invariant 0 (site swap)'),
    census('D4 o3o3x *b3x (t=1)', 'D4 member o3o3x *b3x', 'E', 'tones critical, Mahler maximal'),
    census('turn fixed point (cube-octahedron line, μ=√3)', 'turn fixed point μ = √3 (#81)', 'E', 'shortest edge maximal'),
    table('2I, 12-point classes', 'L', S['2I 12-point class (w = φ/2)']['silent'], set(), 'sin 5θ = 0'),
    table('2I, 20-point classes', 'L', S['2I 20-point class (w = 1/2)']['silent'], set(), 'sin 3θ = 0'),
    table('2O twisted, 8-point classes', 'L', {1, 2}, {1}, 'latitude pair'),
    table('2T twisted, 6-point classes', 'L', {3}, set(), 'one hyperplane'),
    table('D16, σ₇: rectangle (4)', 'L', ALL - {2, 6, 8, 10, 14, 16, 18}, ODD, 'cos 4α = 0'),
    table('D24, σ₇: 6 points', 'L', ALL - {3, 9, 12, 15}, {k for k in ALL if k % 3}, 'cosine rule'),
    table('W⁺(H4), Galois both: 600, 900', 'O', {1, 2, 3}, {1, 2}, 'full symmetry not tested', {3}),
    table('W(H4), Galois: 1200, 900', 'O', {1, 2, 3}, {1, 2}, 'candidate', {3}),
    table('W⁺(H4), Galois left: 30, 360', 'O', {1, 3}, {1}, 'candidate', {3}),
    table('W⁺(H4), Galois left: 600', 'O', {1, 2, 3}, {1}, 'candidate', {2, 3}),
    table('W(H3), Galois: 10, 20, 30', 'N', {1}, {1}, 'reduces to 2I'),
    table('Sym6, exceptional ξ', 'N', {1}, {1}, 'no new silence'),
]
check(sum(1 for r in ROWS if r[0] == 'T') == 2, 'two twisted-silence rows')
tcol = [r for r in ROWS if r[2] - r[3] - r[4] and r[0] == 'T']
check(len(tcol) == 2 and tcol[0][2] - tcol[0][3] == {5, 7} and tcol[1][2] - tcol[1][3] == {3, 6}, 'only X (5, 7) and F (3, 6) carry red tiles')
check(S['24-cell (tesseract-16-cell line, μ=2)']['silent'] != S['24-cell (tesseract-16-cell line, μ=2)']['neighbour_silent'],
      '24-cell: silences beyond its line (F4 symmetry), drawn in the X colour')

order = 'TXPELON'; ROWS.sort(key=lambda r: order.index(r[0]))
nrows = len(ROWS); nb = len(set(r[0] for r in ROWS)); H = nrows + nb * 1.25 + 0.45
W_IN, DPI = 10.0, 220; H_IN = 0.205 * H + 0.9
fig = plt.figure(figsize=(W_IN, H_IN), dpi=DPI, facecolor=GROUND)
x0, x1 = 0.315, 0.735
ax = fig.add_axes([0.0, 0.055, 1.0, 1 - 0.055 - 0.035]); ax.set_xlim(0, 1); ax.set_ylim(H, 0); ax.axis('off')
tw = (x1 - x0) / K
y = 0.2; last = None
for kind, label, sil, forced, opn, law in ROWS:
    if kind != last:
        y += 0.25; name, col = KIND[kind]
        ax.text(0.012, y + 0.55, name, color=col, fontsize=8.6, fontweight='bold', va='center')
        y += 1.0; last = kind
    name, col = KIND[kind]
    for k in range(1, K + 1):
        xx = x0 + (k - 1) * tw
        if k in sil:
            if k in opn: fc, hatch, ec = RING, '/////', '#c9c6bd'
            elif k in forced: fc, hatch, ec = GREY, None, GREY
            else:
                extra_by_symmetry = kind == 'P' and k not in forced
                fc, hatch, ec = (EL['Wind'] if extra_by_symmetry else col), None, None
                ec = fc
        else: fc, hatch, ec = RING, None, RINGE
        ax.add_patch(Rectangle((xx + tw * 0.07, y + 0.1), tw * 0.86, 0.8, fc=fc, ec=ec, lw=0.7, hatch=hatch, zorder=2))
    ax.text(x0 - 0.008, y + 0.5, label, color=INK, fontsize=7.2, ha='right', va='center')
    ax.text(x1 + 0.008, y + 0.5, law, color=DIM, fontsize=6.9, ha='left', va='center')
    y += 1.0
check(y <= H + 1e-9, f'rows fit the frame ({y:.2f} <= {H:.2f})')
for k in range(1, K + 1): ax.text(x0 + (k - 0.5) * tw, 0.25, str(k), color=INK, fontsize=6.8, ha='center', va='center')
ax.text(x0 - 0.008, 0.25, 'degree k', color=DIM, fontsize=6.9, ha='right', va='center')
ax.text(x1 + 0.008, 0.25, 'what forces the law', color=DIM, fontsize=6.9, ha='left', va='center')
fig.text(0.012, 0.022, 'Tile: grey = silent and forced by the family or twist group; coloured = silent only at this member (colour of its kind; '
         'the 24-cell\'s extra tiles are F4 symmetry);', color=DIM, fontsize=6.4)
fig.text(0.012, 0.006, 'hatched = open; dark = ringing.', color=DIM, fontsize=6.4)
fig.text(0.988, 0.006, 'DICTO · dictospheres.com', color='#9a978f', fontsize=7.0, ha='right', va='bottom')
fig.savefig(sys.argv[2], dpi=DPI, facecolor=GROUND)
from PIL import Image
im = Image.open(sys.argv[2]); check(im.size == (int(W_IN * DPI), int(round(H_IN * DPI))) or abs(im.size[1] - H_IN * DPI) < 2, f'frame {im.size}')
print('FINAL ok' if not fails else 'FINAL FAIL', flush=True)
