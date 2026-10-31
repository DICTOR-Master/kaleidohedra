# Figures of paper B of Star Cores ("Core Cycles"), 2026-10-31.
# Figure 1: two turns of the core for the truncated icosahedron (Ih) and DICTO's Icosaxes (Oh), golden spikes t = phi, one scale per row:
#   S; the turn (the hull of the five-/four-fold tips and of the three-fold tips, see-through, round the core); the core C(S); C(C(S)),
#   which is t^2 c^2 S (asserted). Faces on the five-/four-fold axes gold, on the three-fold axes teal. Render standard: solid, crisp edges.
# Figure 2: study 3's depth windows for the edge-cut cube and dodecahedron (T closes late / early / stays open; cores period two in all).
# Usage: ~/geom/bin/python fig_paper_b.py <study data dir> <figures dir> <logo png>
import sys, os, json, numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from scipy.spatial import ConvexHull, HalfspaceIntersection
from itertools import product, permutations
DATA, FIG, LOGO = sys.argv[1:4]; phi = (1 + 5 ** .5) / 2
GOLD, TEAL, EDGE = '#d4af37', '#2bb3a3', '#1d1d24'
LIGHT = np.array([-0.35, 0.55, 0.76]); LIGHT /= np.linalg.norm(LIGHT)
def rot(elev, azim):
    a, e = np.radians(azim), np.radians(elev)
    Rz = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])
    Rx = np.array([[1, 0, 0], [0, np.cos(e), -np.sin(e)], [0, np.sin(e), np.cos(e)]])
    return Rx @ np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]]) @ Rz
def shade(col, n):
    c = np.array(matplotlib.colors.to_rgb(col)); k = 0.50 + 0.50 * max(0.0, float(n @ LIGHT)); return tuple(np.clip(c * k + 0.06 * (1 - k), 0, 1))
def hull_faces(Q):
    h = ConvexHull(Q); out = {}
    for eq in h.equations:
        k = tuple(np.round(eq, 6))
        if k in out: continue
        ids = [i for i, p in enumerate(Q) if abs(eq[:3] @ p + eq[3]) < 1e-7 * (1 + np.abs(Q).max())]
        R = Q[ids]; c = R.mean(0); n = eq[:3]; a = R[0] - c; a /= np.linalg.norm(a); b = np.cross(n, a)
        out[k] = (R[np.argsort(np.arctan2((R - c) @ b, (R - c) @ a))], n, -eq[3])
    return list(out.values())
def verts(hs):
    P = HalfspaceIntersection(np.array(hs), np.zeros(3)).intersections; P = P[ConvexHull(P).vertices]; keep = []
    for p in P:
        if all(np.linalg.norm(p - q) > 1e-9 for q in keep): keep.append(p)
    return np.array(keep)
def unit(v): v = np.array(v, float); return v / np.linalg.norm(v)
def ax_kind(n, U):
    return any(abs(abs(n @ u) - 1) < 1e-8 for u in U)
def core(Q, U, W, t):
    """the core of a turn: tips t * (foot of each face perpendicular), grouped by axis kind; the intersection of the two tip hulls"""
    F = hull_faces(Q); TU = [t * d * n for P, n, d in F if ax_kind(n, U)]; TW = [t * d * n for P, n, d in F if ax_kind(n, W)]
    assert len(TU) + len(TW) == len(F), 'a face off the two axis kinds'
    hs = []
    for T in (TU, TW):
        if len(T) >= 4: hs += [list(e) for e in ConvexHull(np.array(T)).equations]
    return verts(hs), np.array(TU), np.array(TW)
def solid(items, Q, U, M, layer, alpha=1.0):
    for P, n, d in hull_faces(Q):
        nn = M @ n
        if nn[2] <= 1e-9: continue
        W_ = P @ M.T; col = GOLD if ax_kind(n, U) else TEAL
        items.append((layer, W_[:, 2].mean(), W_[:, :2], shade(col, nn), EDGE, 0.6))
def shell(items, Q, M, col):
    rgb = matplotlib.colors.to_rgb(col)
    for P, n, d in hull_faces(Q):
        W_ = P @ M.T; front = (M @ n)[2] > 0
        items.append((2 if front else 0, W_[:, 2].mean(), W_[:, :2], rgb + ((0.13 if front else 0.07),),
                      tuple(0.55 * np.array(rgb)) + ((0.95 if front else 0.45),), 0.6 if front else 0.45))
def draw(ax, items, lim):
    items.sort(key=lambda t: (t[0], t[1]))
    ax.add_collection(PolyCollection([t[2] for t in items], facecolors=[t[3] for t in items], edgecolors=[t[4] for t in items],
                                     linewidths=[t[5] for t in items], joinstyle='round', antialiased=True))
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_aspect('equal'); ax.axis('off')
def cyc(v): return [v, (v[1], v[2], v[0]), (v[2], v[0], v[1])]
def sgn(v): return {tuple(s * x for s, x in zip(ss, v)) for ss in product((1, -1), repeat=3)}
ico = {p for v in sgn((0, 1, phi)) for p in cyc(v)}
dod = set(sgn((1, 1, 1))) | {p for v in sgn((0, phi, 1 / phi)) for p in cyc(v)}
U5 = [unit(v) for v in ico]; W3 = [unit(v) for v in dod]
U4 = [unit(v) for v in {p for v in sgn((1, 0, 0)) for p in cyc(v)}]; W3o = [unit(v) for v in sgn((1, 1, 1))]
TI = np.array(sorted({p for base in [(0, 1, 3 * phi), (1, 2 + phi, 2 * phi), (phi, 2, phi ** 3)] for v in sgn(base) for p in cyc(v)}))
ICX = np.array(sorted({p for v in sgn((0.5, phi / 2, 0)) for p in permutations(v)}))   # Icosaxes: all permutations of (+-1/2, +-phi/2, 0)
assert len(TI) == 60 and len(ICX) == 24
c2 = {'Ih': (5 + 2 * 5 ** .5) / 15, 'Oh': 1 / 3}
t = phi
rows = [('TI (Ih)', TI, U5, W3, 'Ih', 'pentagon', 'hexagon', 'icosahedron', 'dodecahedron'),
        ("Icosaxes (Oh)", ICX, U4, W3o, 'Oh', 'square', 'hexagon', 'octahedron', 'cube')]
fig, axs = plt.subplots(2, 4, figsize=(9.2, 5.3), gridspec_kw=dict(wspace=0.04, hspace=0.30))
M = rot(16, 24)
for r, (name, S, U, W, g, fu, fw, hu, hw) in enumerate(rows):
    C1, TU, TW = core(S, U, W, t); C2, _, _ = core(C1, U, W, t); k = t * t * c2[g]
    assert len(C2) == len(S) and all(min(np.linalg.norm(k * p - q) for q in C2) < 1e-8 for p in S), name   # C(C(S)) = t^2 c^2 S
    # the distances swap: u-planes of C1 at t c b, w-planes at t c a
    dS = {kind: sorted({round(d, 9) for P, n, d in hull_faces(S) if ax_kind(n, D_)}) for kind, D_ in (('u', U), ('w', W))}
    dC = {kind: sorted({round(d, 9) for P, n, d in hull_faces(C1) if ax_kind(n, D_)}) for kind, D_ in (('u', U), ('w', W))}
    c = c2[g] ** .5
    assert abs(dC['u'][0] - t * c * dS['w'][0]) < 1e-8 and abs(dC['w'][0] - t * c * dS['u'][0]) < 1e-8, name
    lim = 1.03 * max(np.linalg.norm(TU, axis=1).max(), np.linalg.norm(TW, axis=1).max(), np.linalg.norm(S, axis=1).max() * max(1, k))
    hU = ConvexHull(TU); hW = ConvexHull(TW)
    it = []; solid(it, S, U, M, 1); draw(axs[r, 0], it, lim)
    it = []; solid(it, C1, U, M, 1); shell(it, TU[hU.vertices], M, GOLD); shell(it, TW[hW.vertices], M, TEAL); draw(axs[r, 1], it, lim)
    it = []; solid(it, C1, U, M, 1); draw(axs[r, 2], it, lim)
    it = []; solid(it, C2, U, M, 1); draw(axs[r, 3], it, lim)
    ratio = dS['w'][0] / dS['u'][0]; ratio1 = dC['w'][0] / dC['u'][0]
    axs[r, 0].set_title(f'S: {name}\nb/a = {ratio:.4f}', fontsize=8)
    axs[r, 1].set_title(f'the turn: {hu}\nand {hw} of tips', fontsize=8)
    axs[r, 2].set_title(f'the core C(S)\nb/a = {ratio1:.4f} = 1/{1/ratio1:.4f}', fontsize=8)
    axs[r, 3].set_title(f'C(C(S)) = {k:.4f} · S\n= t²c² · S', fontsize=8)
fig.text(0.5, 0.03, 'b/a: distance of the three-fold planes (teal) over that of the five-fold (top) or four-fold (bottom) planes (gold). One scale per row; t = φ.',
         ha='center', fontsize=8)
logo = plt.imread(LOGO); la = fig.add_axes([0.93, 0.005, 0.06, 0.06 * 9.2 / 5.3]); la.imshow(logo); la.axis('off')
fig.savefig(os.path.join(FIG, 'core-cycle.png'), dpi=300, facecolor='white'); print('ok core-cycle.png')

# Figure 2: depth windows
A = {}
for f in ('study3.json', 'study3-fine.json'):
    for r in json.load(open(os.path.join(DATA, f))):
        if 'T' in r: A[(r['group'], tuple(r['axes']), tuple(r['s']))] = r
def sval(s): return eval(s.replace('sqrt(5)', '5**.5'))
CL, CE, OP = '#a8841c', '#14968a', '#7a4fc0'   # validated (dataviz validate_palette, light): closes late, closes early, open
fig, axs = plt.subplots(2, 1, figsize=(7.4, 3.1), gridspec_kw=dict(hspace=0.95))
for ax, (g, axes, title) in zip(axs, [('Oh', (4, 2), 'Cube with its edges cut back: planes x = ±1 (and cyclic) and (±1, ±1, 0)·x ≤ 2s'),
                                      ('Ih', (5, 2), 'Dodecahedron with its edges cut back: five-fold planes at foot 1, two-fold planes at foot s')]):
    rs = sorted((sval(k[2][1]), r) for k, r in A.items() if k[0] == g and k[1] == axes)
    for s, r in rs:
        T = r['T']; assert r['cores']['period'] == 2
        if T.get('period') is None: col, mk = OP, 'x'
        elif T['enters'] == 3: col, mk = CL, 'o'
        else: col, mk = CE, 's'
        ax.plot([s], [1], mk, color=col, ms=6, mew=1.6, mfc=col if mk != 'x' else None)
        ax.plot([s], [0], 'o', color='#555555', ms=4)
    lo = max(s for s, r in rs if r['T'].get('period') and r['T']['enters'] == 3); hi = min(s for s, r in rs if r['T'].get('period') and r['T']['enters'] == 1)
    o1 = min(s for s, r in rs if r['T'].get('period') is None); o2 = max(s for s, r in rs if r['T'].get('period') is None)
    ax.axvspan(o1, o2, color=OP, alpha=0.08, lw=0)
    ax.text((o1 + o2) / 2, 1.55, f'T-chain open: {o1:.4f} to {o2:.4f}', ha='center', fontsize=7.5, color='#333333')
    ax.set_yticks([0, 1]); ax.set_yticklabels(['cores: period 2', 'chain of T'], fontsize=7.5); ax.set_ylim(-0.6, 2.0)
    ax.set_title(title, fontsize=8, loc='left'); ax.tick_params(axis='x', labelsize=7.5); ax.set_xlabel('s', fontsize=8, labelpad=1)
    for sp_ in ('top', 'right', 'left'): ax.spines[sp_].set_visible(False)
    ax.grid(axis='x', color='#e6e6e6', lw=0.5); ax.set_axisbelow(True)
from matplotlib.lines import Line2D
h = [Line2D([], [], marker='o', ls='', color=CL, label='T closes, period 4, after 3 steps'),
     Line2D([], [], marker='s', ls='', color=CE, label='T closes, period 4, after 1 step'),
     Line2D([], [], marker='x', ls='', color=OP, mew=1.6, label='T open after 6–8 steps'),
     Line2D([], [], marker='o', ls='', color='#555555', ms=4, label='core cycle of period 2')]
fig.legend(handles=h, loc='lower center', ncol=4, fontsize=6.8, frameon=False, bbox_to_anchor=(0.47, -0.01))
logo = plt.imread(LOGO); la = fig.add_axes([0.925, 0.0, 0.07, 0.07 * 7.4 / 3.1]); la.imshow(logo); la.axis('off')
fig.subplots_adjust(left=0.13, right=0.97, top=0.88, bottom=0.25)
fig.savefig(os.path.join(FIG, 'depth-windows.png'), dpi=300, facecolor='white'); print('ok depth-windows.png')
