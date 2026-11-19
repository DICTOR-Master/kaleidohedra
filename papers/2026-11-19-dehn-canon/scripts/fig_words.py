# Figure 1: the three words CLEO, AXE, FUJI as see-through solids, every edge drawn in the colour of its angle class.
# Corners and faces: pieces.json, copied from studies/2026-10-14-axe-cleo-fuji/nets/pieces.json (9 digits; exact in Q(sqrt5)
# in studies 2026-11-19-lean-dehn-4 and -5). Faces in the app colours of the three solids (AXE cyan, CLEO and FUJI lilac);
# edge colours are labels only (neutral palette). Orthographic view; back edges dashed. Checks every edge's angle class.
import json, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D

D = json.load(open('pieces.json'))
r5 = 5 ** 0.5; g = (r5 - 1) / 2
A = np.degrees(np.arccos(1 / r5)); G = np.degrees(np.arccos(r5 / 3))
B = np.degrees(np.arccos((3 - r5) / (3 * (10 - 2 * r5)) ** 0.5))
EPS = np.degrees(np.arccos((r5 + 1) / (3 * (10 - 2 * r5)) ** 0.5))
CLASSES = [('α', A, '#1f1f1f'), ('β', B, '#9a6a2e'), ('γ', G, '#5b6f8a'), ('ε', EPS, '#a3a3a3'), ('π − ε', 180 - EPS, '#a3a3a3')]
FACE = {'CLEO': '#c792ea', 'AXE': '#4dd0e1', 'FUJI': '#c792ea'}
TITLE = {'CLEO': 'CLEO\n3 ⊗ α + 3g ⊗ β', 'AXE': 'AXE\n(1 + g) ⊗ α + 6 ⊗ β', 'FUJI': 'FUJI\n(9 − 3g) ⊗ α + (12 − 3g) ⊗ β'}
VIEW = {'CLEO': (0.35, -0.55, 0.76), 'AXE': (-0.62, -0.28, 0.73), 'FUJI': (-0.30, -0.42, 0.86)}
EXPECT = {'CLEO': {('α', 1): 3, ('β', 0): 3}, 'AXE': {('α', 0): 1, ('β', 1): 4, ('γ', 1): 1},
          'FUJI': {('π − ε', 1): 6, ('γ', 1): 3, ('ε', 0): 3}}
def best_view(V, F, c):
    # the view direction (grid search) that keeps every corner far from every other corner and from every edge
    # not at that corner, so no two edges overlap in the drawing
    E = sorted({tuple(sorted((a, b))) for f in F for a, b in zip(f, f[1:] + f[:1])})
    best, bv = -1, None
    for th in np.linspace(0.05, np.pi - 0.05, 60):
        for ph in np.linspace(0, 2 * np.pi, 120, endpoint=False):
            v = np.array([np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th)])
            u1 = np.cross([0.31, 0.17, 0.93], v); u1 /= np.linalg.norm(u1); u2 = np.cross(v, u1)
            P = np.c_[(V - c) @ u1, (V - c) @ u2]; s = 1e9
            for i in range(len(V)):
                for (a, b) in E:
                    if i in (a, b): continue
                    d = P[b] - P[a]; t = np.clip((P[i] - P[a]) @ d / (d @ d), 0, 1)
                    s = min(s, np.linalg.norm(P[a] + t * d - P[i]))
            s /= np.abs(P).max()
            if s > best: best, bv = s, v
    return bv
L = np.array([0.3, 0.5, 0.81]); L /= np.linalg.norm(L)

fig, axs = plt.subplots(1, 3, figsize=(12, 4.6), dpi=220)
for ax, k in zip(axs, ['CLEO', 'AXE', 'FUJI']):
    V = np.array(D[k]['vertices']); F = D[k]['faces']; c = V.mean(0)
    def normal(f):
        P = V[f]; n = np.cross(P[1] - P[0], P[2] - P[0]); n /= np.linalg.norm(n)
        return n if n @ (P[0] - c) > 0 else -n
    N = [normal(f) for f in F]
    v = best_view(V, F, c)
    u1 = np.cross([0, 0, 1], v); u1 /= np.linalg.norm(u1); u2 = np.cross(v, u1)
    P2 = np.c_[(V - c) @ u1, (V - c) @ u2]
    E = {}
    for i, f in enumerate(F):
        for a, b in zip(f, f[1:] + f[:1]): E.setdefault(tuple(sorted((a, b))), []).append(i)
    assert all(len(x) == 2 for x in E.values())
    count = {}
    front = [N[i] @ v > 0 for i in range(len(F))]
    base = np.array(matplotlib.colors.to_rgb(FACE[k]))
    for i, f in enumerate(F):          # back faces faint, front faces translucent and shaded
        if not front[i]: ax.add_patch(Polygon(P2[f], closed=True, fc=base, alpha=0.10, ec='none', zorder=1))
    for i, f in enumerate(F):
        if front[i]:
            sh = 0.72 + 0.28 * max(0.0, float(N[i] @ L))
            ax.add_patch(Polygon(P2[f], closed=True, fc=np.clip(base * sh, 0, 1), alpha=0.42, ec='none', zorder=3))
    for (a, b), (i, j) in E.items():
        th = np.degrees(np.pi - np.arccos(np.clip(N[i] @ N[j], -1, 1)))
        name, _, col = min(CLASSES, key=lambda t: abs(t[1] - th))
        assert abs([t[1] for t in CLASSES if t[0] == name][0] - th) < 1e-4, (k, a, b, th)
        L_e = np.linalg.norm(V[a] - V[b]); long = abs(L_e - 1) < 1e-6
        assert long or abs(L_e - g) < 1e-6
        count[(name, int(long))] = count.get((name, int(long)), 0) + 1
        vis = front[i] or front[j]
        ax.plot(*P2[[a, b]].T, color=col, lw=3.0 if vis else 1.4, ls='-' if vis else (0, (3, 2.5)),
                solid_capstyle='round', zorder=5 if vis else 2)
        m = P2[[a, b]].mean(0); off = m - P2.mean(0); off = off / (np.linalg.norm(off) + 1e-9) * 0.075
        ax.text(*(m + off), name, ha='center', va='center', fontsize=10.5, color=col, zorder=7,
                fontweight='bold', bbox=dict(boxstyle='round,pad=0.12', fc='white', ec='none', alpha=0.85 if vis else 0.6))
    assert count == EXPECT[k], (k, count)
    ax.scatter(*P2.T, s=9, color='#1f1f1f', zorder=6)
    r = np.abs(P2).max() * 1.22
    ax.set_xlim(-r, r); ax.set_ylim(-r, r); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title(TITLE[k], fontsize=11)
hs = [Line2D([], [], color=c, lw=3) for _, _, c in CLASSES[:4]] + [Line2D([], [], color='#666', lw=1.4, ls=(0, (3, 2.5)))]
fig.legend(hs, ['α = arccos(1/√5) ≈ 63.43°', 'β ≈ 79.19°', 'γ = arccos(√5/3) ≈ 41.81°', 'ε ≈ 37.38° and π − ε', 'hidden edge'],
           loc='lower center', ncol=5, fontsize=9, frameon=False)
plt.subplots_adjust(left=0.01, right=0.99, top=0.86, bottom=0.10, wspace=0.04)
plt.savefig('../figures/fig-words.png', facecolor='white')
print('edge classes', {k: EXPECT[k] for k in EXPECT}); print('FINAL ok')
