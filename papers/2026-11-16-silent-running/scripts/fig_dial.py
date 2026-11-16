#!/usr/bin/env python3
"""Figure 5, the dial along the two edge circles of the golden twist, redrawn with label colours only (16 Nov 2026, DICTO: app
colours only for the solid they stand for). The drawing is section D of studies/2026-11-15-twisted-silence-groups/scripts/dial_a5.py
(same points and layout; one fix: the angle is now measured in an orthonormal basis of the circle's plane.
The study drew the C3 edge with its u and v, which are not perpendicular, so there its dots sat off the zeros of their curves;
every dot is now checked to lie on a zero of its curve), split out so that the figure can be redrawn without rerunning that study's searches.
Data: that study's data/dial_a5_edges.json (exact special points on each edge circle with their silence signatures).
Dots: teal = silent in two or more degrees above 2 (multi-silent), slate = a single silence (label colours of Figures 1, 2 and 6).
Usage: fig_dial.py dial_a5_edges.json out.png   (ends FINAL ok / FINAL FAIL)"""
import sys, json, math, itertools
import numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt

# Label colours (16 Nov 2026): labels only, no element or solid meaning; the palette of Silent Running and Walls of Silence.
LABEL = {'teal': (32, 168, 158), 'slate': (100, 112, 136)}
LHEX = {k: '#%02x%02x%02x' % v for k, v in LABEL.items()}
fails = []
def check(ok, msg):
    print(('CHECK ok   ' if ok else 'CHECK FAIL ') + msg, flush=True)
    if not ok: fails.append(msg)

A5 = [p for p in itertools.permutations(range(5)) if sum(1 for i in range(5) for j in range(i + 1, 5) if p[i] > p[j]) % 2 == 0]
check(len(A5) == 60, 'A5 has 60 elements')
def cheb_coeffs(k): return [((-1) ** j * math.comb(k - j, j) * 2 ** (k - 2 * j), k - 2 * j) for j in range(k // 2 + 1)]
def F_at(xv, k):   # as dial_a5.py: sum over A5 of |x|^2k U_k(<gx,x>/|x|^2)
    nn = sum(t * t for t in xv); tot = 0
    for g in A5:
        c = sum(xv[g[i]] * xv[i] for i in range(5))
        for coef, e in cheb_coeffs(k): tot += coef * c ** e * nn ** (k - e)
    return tot
EDGES = {'C3 edge (a,a,a,b,c)': ([1, 1, 1, -3, 0], [0, 0, 0, 1, -1]), 'C2 edge (a,a,b,b,c)': ([1, 1, -1, -1, 0], [1, 1, 1, 1, -4])}
rep = json.load(open(sys.argv[1]))
check(set(rep) == set(EDGES), 'the data has both edge circles')

fig, axs = plt.subplots(2, 1, figsize=(9, 6.5))
nmulti = nsingle = 0
for ax, (ename, (u, v)) in zip(axs, EDGES.items()):
    th = np.linspace(0, np.pi, 1441)
    uu = np.array(u, float); vv = np.array(v, float); vv /= np.linalg.norm(vv)
    uu = uu - (uu @ vv) * vv; uu /= np.linalg.norm(uu)   # orthonormal basis of the circle's plane (the C3 edge's u and v are not perpendicular)
    check(abs(uu @ vv) < 1e-12, f'{ename}: orthonormal basis, so the axis is a true angle')
    scale = {}
    for k in range(3, 16):
        vals = np.array([F_at(list(np.cos(t) * vv + np.sin(t) * uu), k) for t in th]); scale[k] = np.abs(vals).max()
        ax.plot(np.degrees(th), k + 0.8 * vals / vals.max(), lw=0.8, color='0.35')
    for p in rep[ename]['points']:
        multi = len([q for q in p['signature'] if q > 2]) >= 2
        for s in p['s_values']:
            xx = s * np.array(u, float) + np.array(v, float)
            t = np.arctan2(np.dot(xx, uu), np.dot(xx, vv)) % np.pi
            for k in p['signature']:
                if 3 <= k < 16:
                    xs = list(np.cos(t) * vv + np.sin(t) * uu)
                    check(abs(F_at(xs, k)) < 1e-7 * scale[k], f'{ename}: tone {k} vanishes at {np.degrees(t):.2f} deg')
                    ax.plot(np.degrees(t), k, 'o', ms=4, color=LHEX['teal'] if multi else LHEX['slate'])
                    nmulti += multi; nsingle += not multi
    ax.set_title(f'{ename}: silence of degree k (rows) as the base point turns; teal = multi-silent, slate = single', fontsize=9)
    ax.set_ylabel('degree k'); ax.set_yticks(range(3, 16))
axs[-1].set_xlabel('angle along the edge circle (degrees)')
fig.text(0.99, 0.005, 'DICTO · dictospheres.com', ha='right', fontsize=6, color='#999')
fig.tight_layout(); fig.savefig(sys.argv[2], dpi=150)
check(nmulti > 0 and nsingle > 0, f'{nmulti} multi-silent and {nsingle} single-silence dots drawn')
print('FINAL ok' if not fails else f'FINAL FAIL ({len(fails)})')
