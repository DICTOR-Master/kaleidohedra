#!/usr/bin/env python3
"""Figure for Golden Ladder ch. 2: the sweep as weight shapes. Top: 3D sweep μ ∈ [1,3] with SU(4)/SO(7) multiplets, Fibonacci ladders to φ and 3−φ (gold),
Pell ladder to 1+√2 (silver), musical intervals. Bottom: 4D sweep μ ∈ [1,4] with SO(9) multiplets and the Fibonacci ladders to the All-Golden stations."""
import math, os
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
phi = (1 + 5**.5)/2; GOLD = '#b8862e'; SILV = '#7d8a96'; INK = '#333'
fig, ax = plt.subplots(2, 1, figsize=(12, 6.2), gridspec_kw={'hspace': 0.75})
def axis(a, lo, hi, title):
    a.set_xlim(lo - 0.05, hi + 0.05); a.set_ylim(-1.45, 1.6); a.axhline(0, color=INK, lw=1); a.set_yticks([]); a.set_title(title, fontsize=10.5, loc='left')
    for s in ('left', 'right', 'top'): a.spines[s].set_visible(False)
def mark(a, x, top, bottom='', col=INK, y=0.25, size=7.5):
    a.plot([x, x], [-0.12, 0.12], color=col, lw=1.6); a.text(x, y, top, ha='center', va='bottom', fontsize=size, color=col)
    if bottom: a.text(x, -0.3, bottom, ha='center', va='top', fontsize=size, color=col)
a = ax[0]; axis(a, 1, 3, 'Three dimensions: the cube–octahedron sweep  C ∩ μC*  =  weight shapes of SU(4) ≅ SO(6) (μ ≤ 2) and SO(7) (μ ≥ 2)')
for x, t, b in ((1, 'octahedron\n6', 'unison'), (4/3, '175', 'fourth'), (1.5, 'Kelvin\n64', 'fifth'), (2, 'cuboctahedron\n15 = 21', 'octave'), (3, 'cube\n8', 'twelfth')):
    mark(a, x, t, b)
for k, (p, q) in enumerate(((1, 1), (2, 1), (3, 2), (5, 3), (8, 5))):
    x = 1 + p/(p+q); a.plot(x, 0, 'o', color=GOLD, ms=4)
for k, (p, q) in enumerate(((1, 2), (2, 3), (3, 5), (5, 8))):
    x = 1 + p/(p+q); a.plot(x, 0, 'o', color=GOLD, ms=4)
mark(a, phi, 'Icosaxes φ', '', GOLD, y=0.75, size=8); a.text(phi, -0.62, 'golden interval', ha='center', va='top', fontsize=7.5, color=GOLD); mark(a, 3 - phi, 'Unborn Axes 3 − φ', '', GOLD, y=0.75, size=8)
for (b, c) in ((1, 1), (2, 3), (5, 7), (12, 17)):
    a.plot((4*b + 3*c)/(2*b + c), 0, 'o', color=SILV, ms=4)
mark(a, 1 + 2**.5, 'truncated cube 1 + √2', 'silver', SILV, y=0.75, size=8)
mG = 4 + 1.5*2**.5 - 5**.5 - .5*10**.5; mL = 4 - 1.5*2**.5 + 5**.5 - .5*10**.5
mark(a, mG, '', '', '#8a4f2a'); mark(a, mL, '', '', '#8a4f2a'); a.text(mG, -0.62, 'Greater GCC', ha='center', va='top', fontsize=7, color='#8a4f2a'); a.text(mL, -0.62, 'Lesser GCC', ha='center', va='top', fontsize=7, color='#8a4f2a')
a.text(1.02, -1.2, 'gold dots: Fibonacci multiplets (64, 300, 2156, … and 175, 1470, …)   grey dots: Pell multiplets of SO(7) (112, 4928, 905520, …)', fontsize=7.5, color=INK)
a = ax[1]; axis(a, 1, 4, 'Four dimensions: the tesseract–16-cell sweep  K ∩ μK*  =  weight shapes of SO(9)')
for x, t in ((1, '16-cell\n9'), (2, '24-cell\n36'), (3, 'rectified tesseract\n84'), (4, 'tesseract\n16')): mark(a, x, t)
F = [1, 1, 2, 3, 5, 8, 13]
for i in range(1, 6):
    a.plot(2 + F[i]/(F[i-1] + F[i]), 0, 'o', color=GOLD, ms=4); a.plot(2 + F[i-1]/(F[i-1] + F[i]), 0, 'o', color=GOLD, ms=4)
mark(a, phi**2, '', '', GOLD); mark(a, 2 + 1/phi**2, '', '', GOLD); a.text(phi**2 + 0.03, 0.75, 'All-Golden (8 Icosaxes)', ha='left', fontsize=8, color=GOLD); a.text(2 + 1/phi**2 - 0.03, 0.75, 'All-Golden (8 Unborn Axes)', ha='right', fontsize=8, color=GOLD)
a.text(1.02, -0.95, 'gold dots: Fibonacci multiplets (0, F_n, F_{n+1}, 0) of SO(9): 1650, 27027, 1527552, …', fontsize=7.5, color=INK)
fig.text(0.99, 0.01, 'DICTO · dictospheres.com', ha='right', fontsize=8, color='#888')
out = os.path.expanduser('~/work/gl2-fig1-ladders.png'); fig.savefig(out, dpi=180, bbox_inches='tight'); print(out)
