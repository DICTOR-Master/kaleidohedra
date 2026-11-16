#!/usr/bin/env python3
"""Figure: the Red Queen's (120-cell's) 720 pentagons in the H4 Coxeter plane, each drawn as a pentagon mark at its centre, coloured by
the polar-dual cat copy whose fins cover it, in a fewest-copies cover by A* copies (from s5: 16 copies, proved minimal). Hue = the
S5 the copy comes from (8 S5s); solid = one of its two A*-type copies, pale = the other; ring = a second copy covering the same
pentagon. Style and dark ground of fig_pairs.py.   usage: fig_dual_cats.py OUTDIR out.png"""
import os, sys, pickle
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rq_lib import *
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
OUT, PNG = sys.argv[1], sys.argv[2]; C = Checks()
d = pickle.load(open(os.path.join(OUT, 'dual_cover.pkl'), 'rb')); m = pickle.load(open(os.path.join(OUT, 'dual_min_cover.pkl'), 'rb'))
copies = d['copies']; WPn = [set(x) for x in d['whole_p']]; cover = m['covers']['A*']; mir = m['mir']
C(set().union(*[WPn[t] for t in cover]) == set(range(720)), f'the {len(cover)} chosen A* copies cover all 720 pentagons')
Wd = World(); Qf = Wd.Qf; Pf = Wd.Pf
on = Wd.PP.facets[0][0]; v = [flt(to5(Wd.PP.P[i])) for i in on]
rays = [v[0], v[0] + v[1], v[0] + v[1] + v[2], v[0] + v[1] + v[2] + v[3]]
simple = [Pf[a] for a in Wd.mirror_axes if sum(abs(Pf[a] @ r) < 1e-9 for r in rays) == 3]
C(len(simple) == 4, 'four walls of an H4 Coxeter chamber')
M = np.eye(5)
for n in simple: M = M @ (np.eye(5) - 2*np.outer(n, n)/(n @ n))
ev, vec = np.linalg.eig(M); k = np.argmin(np.abs(np.angle(ev) - 2*np.pi/30))
u = np.real(vec[:, k]); w = np.imag(vec[:, k]); u /= np.linalg.norm(u); w -= (w @ u)*u; w /= np.linalg.norm(w)
x, y = Qf @ u, Qf @ w
D2 = ((Qf[:, None] - Qf[None])**2).sum(-1); mm = np.min(D2[D2 > 1e-9]); E = np.argwhere(np.triu(np.abs(D2 - mm) < 1e-6, 1))
C(len(E) == 1200, '1200 edges')
# pentagon centres: the 5 Q corners q with p1.q = p2.q = R2Q for the pentagon's 600-cell edge (p1, p2)
R2Q = float(Wd.R2Q); cen = []
for a, b in d['pent_edge']:
    qs = np.where((np.abs(Qf @ Pf[a] - R2Q) < 1e-6) & (np.abs(Qf @ Pf[b] - R2Q) < 1e-6))[0]; assert len(qs) == 5; cen.append(Qf[qs].mean(0))
cen = np.array(cen); px, py = cen @ u, cen @ w
C(len({(round(a, 5), round(b, 5)) for a, b in zip(px, py)}) == 720, 'all 720 pentagon centres land on distinct points')
# group the cover by S5 (its 10 mirrors)
s5 = {}
for t in cover: s5.setdefault(frozenset(mir[k] for k in WPn[t]), []).append(t)
groups = sorted(s5.values(), key=lambda g: min(g))
C(all(len(g) == 2 for g in groups), f'the cover uses {len(groups)} S5s, both A*-type copies of each')
HUE = ['#8a5cc4', '#3a70cd', '#488e48', '#cd3e28', '#e8c852', '#2fa8a0', '#e0803a', '#d45f9e']
BG = '#121418'
def pale(c, f=0.5): return tuple(a*f + 0.88*(1 - f) for a in to_rgb(c))   # tint toward light grey
colof = {}
for h, g in enumerate(groups):
    colof[g[0]] = HUE[h]; colof[g[1]] = pale(HUE[h])
cov = [[t for t in cover if k in WPn[t]] for k in range(720)]
fig = plt.figure(figsize=(13, 14), facecolor=BG)
ax = fig.add_axes([0.03, 0.12, 0.94, 0.85]); ax.set_facecolor(BG)
for a, b in E: ax.plot([x[a], x[b]], [y[a], y[b]], color='#3c414b', lw=0.4, zorder=1)
r = np.hypot(px, py); order = np.argsort(r)
fill = [colof[cov[k][0]] for k in order]; ring = [colof[cov[k][1]] if len(cov[k]) > 1 else colof[cov[k][0]] for k in order]
ax.scatter(px[order], py[order], s=70, marker='p', c=fill, edgecolors=ring, linewidths=2.2, zorder=3)
ax.set_aspect('equal'); ax.axis('off'); R = max(np.hypot(x, y).max(), r.max())*1.04; ax.set_xlim(-R, R); ax.set_ylim(-R, R)
ia = fig.add_axes([0.05, 0.015, 0.30, 0.09]); ia.set_facecolor(BG); ia.axis('off')
for h in range(len(groups)):
    ia.scatter([h], [0], s=110, marker='p', c=[HUE[h]], edgecolors=[HUE[h]], linewidths=2)
    ia.scatter([h], [-1], s=110, marker='p', c=[pale(HUE[h])], edgecolors=[pale(HUE[h])], linewidths=2)
ia.set_xlim(-0.8, len(groups) - 0.2); ia.set_ylim(-1.8, 1.0)
ia.text(-0.6, 0.55, 'one colour per S5: its two A* copies (full, pale)', color='#c8ccd4', fontsize=9, ha='left')
mult = Counter(len(c) for c in cov)
fig.text(0.40, 0.065, "The 120-cell's 720 pentagons (H4 Coxeter plane), each marked at its centre.\n"
         "Colour = the polar dual of a truncated 5-cell (A*) whose fins cover it.\n"
         f"{len(cover)} A* copies cover every pentagon (the fewest possible);\n"
         f"ring = a second copy ({mult[1]} pentagons once, {mult[2]} twice, {mult[3]} three times).\n"
         "Every pentagon of the 120-cell is covered whole by 10 A*, 10 B* and 5 C3* copies.", color='#d8dbe2', fontsize=10.5, va='center')
fig.text(0.975, 0.012, 'DICTO · dictospheres.com', color='#9aa0aa', fontsize=10, ha='right')
fig.savefig(PNG, dpi=150, facecolor=BG); C(os.path.getsize(PNG) > 50000, 'figure written')
C.final()
