#!/usr/bin/env python3
"""Two-panel figure (DICTO 16 Nov: "redraw in five colours but have as a and b"), same H4 Coxeter-plane view in both panels.
(a) "the five-colour cats" (simplified reading): the five kinds of dual cat X*, -X*, R* (= C3*), F*, -F* in the five colours of Silent Running's Fig. 2
    (fig_600orbits.py: X red, -X blue, R violet, F yellow, -F green). Taking the 8 S5s of panel (b), each pentagon's mark is split
    into wedges, one per kind among those 8 S5s' 40 duals that covers it (a reading; every pentagon is covered by 10 A*, 10 B*, 5 C3*). Labels: the coordinate S5 as in Silent Running; for another S5 they are carried
    over by one symmetry h (h maps the coordinate C3 onto that S5's C3*); swapping X and -X is the central inversion.
(b) "symmetry groups": the 16-copy A* cover, one colour per S5 symmetry group, full and pale for its two copies (as fig_dual_cats.py).
usage: fig_dual_cats_ab.py OUTDIR out.png"""
import os, sys, pickle
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rq_lib import *
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
from matplotlib.patches import Wedge, RegularPolygon
OUT, PNG = sys.argv[1], sys.argv[2]; C = Checks()
d = pickle.load(open(os.path.join(OUT, 'dual_cover.pkl'), 'rb')); m = pickle.load(open(os.path.join(OUT, 'dual_min_cover.pkl'), 'rb'))
st = pickle.load(open(os.path.join(OUT, 'state.pkl'), 'rb'))
copies = d['copies']; WPn = [set(x) for x in d['whole_p']]; cover = m['covers']['A*']; mir = m['mir']
Wd = World(); Qf = Wd.Qf; Pf = Wd.Pf; WP = Wd.W[:, :120]; Pk = Wd.Pk
# projection (identical to fig_pairs.py / fig_dual_cats.py)
on = Wd.PP.facets[0][0]; v = [flt(to5(Wd.PP.P[i])) for i in on]
rays = [v[0], v[0] + v[1], v[0] + v[1] + v[2], v[0] + v[1] + v[2] + v[3]]
simple = [Pf[a] for a in Wd.mirror_axes if sum(abs(Pf[a] @ r) < 1e-9 for r in rays) == 3]
M = np.eye(5)
for n in simple: M = M @ (np.eye(5) - 2*np.outer(n, n)/(n @ n))
ev, vec = np.linalg.eig(M); k = np.argmin(np.abs(np.angle(ev) - 2*np.pi/30))
u = np.real(vec[:, k]); w = np.imag(vec[:, k]); u /= np.linalg.norm(u); w -= (w @ u)*u; w /= np.linalg.norm(w)
x, y = Qf @ u, Qf @ w
D2 = ((Qf[:, None] - Qf[None])**2).sum(-1); mm = np.min(D2[D2 > 1e-9]); E = np.argwhere(np.triu(np.abs(D2 - mm) < 1e-6, 1))
C(len(E) == 1200, '1200 edges')
R2Q = float(Wd.R2Q); cen = []
for a, b in d['pent_edge']:
    qs = np.where((np.abs(Qf @ Pf[a] - R2Q) < 1e-6) & (np.abs(Qf @ Pf[b] - R2Q) < 1e-6))[0]; assert len(qs) == 5; cen.append(Qf[qs].mean(0))
cen = np.array(cen); px, py = cen @ u, cen @ w

# ---- (a) labels: the five duals of each S5 ----
Xs = sorted(Pk[vkey(p)] for p in Wd.X); Ys = sorted(Pk[vkey(p)] for p in Wd.Y)
Xm = sorted(int(Wd.antiP[i]) for i in Xs); Ym = sorted(int(Wd.antiP[i]) for i in Ys)
C3s = sorted(set(range(120)) - set(Xs) - set(Xm) - set(Ys) - set(Ym))
KIND = ['X*', '−X*', 'R*', 'F*', '−F*']; BASE = [Xs, Xm, C3s, Ys, Ym]
s5key = [frozenset(mir[k] for k in WPn[t]) for t in range(len(copies))]
byS5 = {}
for t, kk in enumerate(s5key): byS5.setdefault(kk, []).append(t)
C(len(byS5) == 60 and all(len(v) == 5 for v in byS5.values()), '60 S5s, five dual copies each')
coord = s5key[next(t for t, c in enumerate(copies) if c[0] == 'C3' and sorted(c[2]) == C3s)]
label = {}
for kk, ts in byS5.items():
    tc = next(t for t in ts if copies[t][0] == 'C3'); h = np.arange(120) if kk == coord else WP[copies[tc][1]]
    img = [frozenset(h[B].tolist()) for B in BASE]
    for t in ts:
        label[t] = img.index(copies[t][2])
C(all(sorted(label[t] for t in ts) == [0, 1, 2, 3, 4] for ts in byS5.values()), 'in every S5 the five duals get the five kinds once each')
# the same 8 S5 symmetry groups as panel (b) (the S5s of the 16-copy A* cover); no 6 S5s partition the 60 mirrors (exact-cover search: none)
s5b = {}
for t in cover: s5b.setdefault(s5key[t], []).append(t)
chosen = sorted(s5b, key=lambda kk: min(s5b[kk]))
C(len(chosen) == 8 and set().union(*chosen) == set(range(60)), 'the 8 S5s of the cover in (b) reach all 60 mirrors')
kinds_of = []
for kp in range(720):
    kinds_of.append(sorted({label[t] for kk in chosen if mir[kp] in kk for t in byS5[kk] if kp in WPn[t]}))
nk = Counter(len(s) for s in kinds_of)
C(min(nk) >= 1, f'every pentagon is covered by at least one kind of its S5 (kinds per pentagon: {dict(sorted(nk.items()))})')
patt = Counter(tuple(s) for s in kinds_of)
print('KINDS per pentagon', dict(sorted(nk.items())), 'patterns', {''.join(KIND[i] + ' ' for i in k).strip(): v for k, v in patt.items()}, flush=True)
EL = {'red': (205, 62, 40), 'blue': (58, 112, 205), 'violet': (138, 92, 196), 'yellow': (232, 200, 82), 'green': (72, 142, 72)}
KCOL = [tuple(c/255 for c in EL[n]) for n in ('red', 'blue', 'violet', 'yellow', 'green')]

# ---- (b) groups ----
s5 = {}
for t in cover: s5.setdefault(s5key[t], []).append(t)
groups = sorted(s5.values(), key=lambda g: min(g))
C(set().union(*[WPn[t] for t in cover]) == set(range(720)) and all(len(g) == 2 for g in groups), f'(b) {len(cover)} A* copies, {len(groups)} S5s x 2, cover all pentagons')
HUE = ['#8a5cc4', '#3a70cd', '#488e48', '#cd3e28', '#e8c852', '#2fa8a0', '#e0803a', '#d45f9e']
def pale(c, f=0.5): return tuple(a*f + 0.88*(1 - f) for a in to_rgb(c))
colof = {}
for h_, g in enumerate(groups): colof[g[0]] = HUE[h_]; colof[g[1]] = pale(HUE[h_])
cov = [[t for t in cover if kp in WPn[t]] for kp in range(720)]

BG = '#121418'; INK = '#d8dbe2'; DIM = '#aab0ba'
fig = plt.figure(figsize=(22, 12.6), facecolor=BG)
Rv = max(np.hypot(x, y).max(), np.hypot(px, py).max())*1.04
order = np.argsort(np.hypot(px, py)); rad = Rv*0.0165
def base(ax):
    ax.set_facecolor(BG)
    for a, b in E: ax.plot([x[a], x[b]], [y[a], y[b]], color='#3c414b', lw=0.4, zorder=1)
    ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-Rv, Rv); ax.set_ylim(-Rv, Rv)
axa = fig.add_axes([0.01, 0.15, 0.48, 0.80]); base(axa)
for kp in order:
    ks = kinds_of[kp]; c = (px[kp], py[kp])
    clip = RegularPolygon(c, 5, radius=rad, orientation=0, transform=axa.transData)
    n = len(ks)
    for j, kd in enumerate(ks):
        wdg = Wedge(c, rad*1.2, 90 + 360*j/n, 90 + 360*(j + 1)/n, color=KCOL[kd], zorder=3, lw=0)
        axa.add_patch(wdg); wdg.set_clip_path(clip)
    axa.add_patch(RegularPolygon(c, 5, radius=rad, orientation=0, fill=False, edgecolor=BG, lw=0.6, zorder=4))
axb = fig.add_axes([0.51, 0.15, 0.48, 0.80]); base(axb)
fill = [colof[cov[kp][0]] for kp in order]; ring = [colof[cov[kp][1]] if len(cov[kp]) > 1 else colof[cov[kp][0]] for kp in order]
axb.scatter(px[order], py[order], s=46, marker='p', c=fill, edgecolors=ring, linewidths=1.8, zorder=3)
for ax_, lab_, ttl in ((axa, 'a', 'the five-colour cats'), (axb, 'b', 'symmetry groups')):
    ax_.text(0.02, 0.985, lab_, transform=ax_.transAxes, color=INK, fontsize=26, fontweight='bold', va='top')
    ax_.text(0.075, 0.975, ttl, transform=ax_.transAxes, color=INK, fontsize=15, va='top')
# legends
la = fig.add_axes([0.03, 0.035, 0.44, 0.08]); la.set_facecolor(BG); la.axis('off'); la.set_xlim(0, 10); la.set_ylim(0, 2); la.set_aspect('equal')
for i, kd in enumerate(KIND):
    la.add_patch(RegularPolygon((0.3 + 2*i, 1.45), 5, radius=0.28, orientation=0, color=KCOL[i])); la.text(0.7 + 2*i, 1.45, kd, color=INK, fontsize=12, va='center')
la.text(0.0, 0.45, 'kinds of dual cat (the 8 S5s of b); one wedge per kind that covers the pentagon', color=DIM, fontsize=11, va='center')
lb = fig.add_axes([0.53, 0.035, 0.30, 0.08]); lb.set_facecolor(BG); lb.axis('off'); lb.set_xlim(-0.6, 8); lb.set_ylim(-1.8, 1.2)
for h_ in range(len(groups)):
    lb.scatter([h_], [0.55], s=110, marker='p', c=[HUE[h_]]); lb.scatter([h_], [-0.45], s=110, marker='p', c=[pale(HUE[h_])])
lb.text(-0.5, -1.5, 'one colour per S5 symmetry group: its two A* copies (full, pale); ring = a second copy', color=DIM, fontsize=11, va='center')
fig.text(0.985, 0.012, 'DICTO · dictospheres.com', color='#9aa0aa', fontsize=11, ha='right')
fig.savefig(PNG, dpi=110, facecolor=BG); C(os.path.getsize(PNG) > 50000, 'figure written')
C.final()
