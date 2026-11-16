#!/usr/bin/env python3
"""Figure: the 120-cell's 600 corners in the H4 Coxeter plane (30-fold view), each corner drawn as a dot whose FILL is the colour of
the first-state inscribed 600-cell it lies in and whose RING is the colour of the second-state 600-cell (every corner lies in exactly
one of each). Inset: the 5 x 5 pairs, each pair sharing a 24-cell of 24 corners. App colours on a dark ground.
usage: fig_pairs.py OUTDIR out.png"""
import os, sys, pickle, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rq_lib import *
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
OUT, PNG = sys.argv[1], sys.argv[2]; C = Checks()
st = pickle.load(open(os.path.join(OUT, 'state.pkl'), 'rb')); F600 = [set(S) for S in st['F600']]; S1, S2 = st['states']
Wd = World(); Qf = Wd.Qf; Pf = Wd.Pf
# chamber walls -> Coxeter element (float), Coxeter plane = eigenplane of exp(2 pi i / 30)
on = Wd.PP.facets[0][0]; v = [flt(to5(Wd.PP.P[i])) for i in on]
rays = [v[0], v[0] + v[1], v[0] + v[1] + v[2], v[0] + v[1] + v[2] + v[3]]
simple = [Pf[a] for a in Wd.mirror_axes if sum(abs(Pf[a] @ r) < 1e-9 for r in rays) == 3]
C(len(simple) == 4, 'four walls of an H4 Coxeter chamber')
M = np.eye(5)
for n in simple: M = M @ (np.eye(5) - 2*np.outer(n, n)/(n @ n))
ev, vec = np.linalg.eig(M); k = np.argmin(np.abs(np.angle(ev) - 2*np.pi/30))
C(abs(np.angle(ev[k]) - 2*np.pi/30) < 1e-9, 'Coxeter element has the eigenvalue exp(2 pi i/30) (Coxeter number 30)')
u = np.real(vec[:, k]); w = np.imag(vec[:, k]); u /= np.linalg.norm(u); w -= (w @ u)*u; w /= np.linalg.norm(w)
x, y = Qf @ u, Qf @ w
pts = np.round(np.c_[x, y], 6); C(len({tuple(p) for p in pts}) == 600, 'all 600 corners land on distinct points in the Coxeter plane')
D2 = ((Qf[:, None] - Qf[None])**2).sum(-1); m = np.min(D2[D2 > 1e-9]); E = np.argwhere(np.triu(np.abs(D2 - m) < 1e-6, 1))
C(len(E) == 1200, '1200 edges')
COL = ['#8a5cc4', '#3a70cd', '#488e48', '#cd3e28', '#e8c852']
f1 = {i: COL[S1.index(k)] for k in S1 for i in F600[k]}; f2 = {i: COL[S2.index(k)] for k in S2 for i in F600[k]}
C(len(f1) == 600 and len(f2) == 600, 'every corner has one first-state and one second-state 600-cell')
BG = '#121418'
fig = plt.figure(figsize=(13, 14), facecolor=BG)
ax = fig.add_axes([0.03, 0.12, 0.94, 0.85]); ax.set_facecolor(BG)
for a, b in E: ax.plot([x[a], x[b]], [y[a], y[b]], color='#4a4f5a', lw=0.45, zorder=1)
r = np.hypot(x, y); order = np.argsort(r)
ax.scatter(x[order], y[order], s=46, c=[f1[i] for i in order], edgecolors=[f2[i] for i in order], linewidths=3.0, zorder=3)
ax.set_aspect('equal'); ax.axis('off'); R = r.max()*1.04; ax.set_xlim(-R, R); ax.set_ylim(-R, R)
ia = fig.add_axes([0.06, 0.015, 0.30, 0.10]); ia.set_facecolor(BG); ia.axis('off')
for a in range(5):
    for b in range(5):
        ia.scatter([b], [-a], s=80, c=COL[a], edgecolors=COL[b], linewidths=3.2)
ia.set_xlim(-1.2, 4.6); ia.set_ylim(-4.6, 0.8)
ia.text(-0.9, 0.55, 'ring: second state', color='#c8ccd4', fontsize=9, ha='left')
ia.text(-1.1, -2, 'fill: first state', color='#c8ccd4', fontsize=9, rotation=90, va='center', ha='center')
fig.text(0.40, 0.07, "The 120-cell's 600 corners (H4 Coxeter plane).\n"
         "It holds 10 inscribed 600-cells in two whole states of 5.\n"
         "Every corner lies in exactly two: one from each state.\n"
         "Fill = its 600-cell in the first state, ring = in the second.\n"
         "Each of the 25 fill-ring pairs is a 24-cell of 24 corners.", color='#d8dbe2', fontsize=10.5, va='center')
fig.text(0.975, 0.012, 'DICTO · dictospheres.com', color='#9aa0aa', fontsize=10, ha='right')
fig.savefig(PNG, dpi=150, facecolor=BG); C(os.path.getsize(PNG) > 50000, 'figure written')
C.final()
