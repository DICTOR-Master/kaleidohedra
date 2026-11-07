"""Family nets kit (roadmap step 5): the five Platonic solids in D·I·C·T·O order + the rhombic dodecahedron,
one A4 page each, one colour per solid, every cut edge numbered on both sides so matching edges are easy to find.
Geometry and net search copied from studies/2026-11-06-five-in-octet/cardkit/nest_kit.py (spanning-tree unfolding,
shapely overlap check). Every net is checked: no overlap, each cut edge has exactly one glue tab, fits the page.
Run on dicto-big-brother with ~/geom/bin/python.  Usage: family_kit.py [edge_mm] [out.pdf]"""
import sys, math, itertools, numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy.spatial import ConvexHull
from shapely.geometry import Polygon
EDGE = float(sys.argv[1]) if len(sys.argv) > 1 else 40.0; OUT = sys.argv[2] if len(sys.argv) > 2 else 'family-kit.pdf'
phi = (1 + 5 ** .5) / 2
A4W, A4H = 210.0, 297.0; FW, FH = 186.0, 226.0
def cyc(v): return [v, (v[1], v[2], v[0]), (v[2], v[0], v[1])]
def orbit(v):
    S = set()
    for s in itertools.product((1, -1), repeat=3): S.update(cyc(tuple(a * b for a, b in zip(s, v))))
    return np.array(sorted(S), float)
STD = {'octahedron': orbit((1, 0, 0)), 'icosahedron': orbit((0, 1, phi)), 'dodecahedron': np.vstack([orbit((1, 1, 1)), orbit((0, 1 / phi, phi))]),
       'cube': np.array(list(itertools.product((-1, 1), repeat=3)), float), 'tetrahedron': np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float)}
ORDER = [('octahedron', 1.0), ('icosahedron', math.sqrt(2) / phi ** 2), ('dodecahedron', math.sqrt(1 / 3 - math.sqrt(5) / 9)), ('cube', math.sqrt(2) / 3), ('tetrahedron', 2 / 3)]
COL = {'octahedron': '#f3e3a6', 'icosahedron': '#b9cdf2', 'dodecahedron': '#d6c1ea', 'cube': '#bfe0bf', 'tetrahedron': '#f2b8ad'}
def faces(V):
    h = ConvexHull(V); F = {}
    for eq, sp in zip(h.equations, h.simplices): F.setdefault(tuple(np.round(eq, 6)), set()).update(sp)
    out = []
    for k, idx in F.items():
        idx = list(idx); n = np.array(k[:3]); c = V[idx].mean(0); u = V[idx[0]] - c; w = np.cross(n, u)
        out.append(sorted(idx, key=lambda i: math.atan2((V[i] - c) @ w, (V[i] - c) @ u)))
    return out
def unfold(V, F, root, order_key):
    """lay faces flat along a BFS spanning tree from root; returns {face: 2D polygon (by vertex id)}, tree edges"""
    def edges(f): return [(f[i], f[(i + 1) % len(f)]) for i in range(len(f))]
    adj = {}
    for fi, f in enumerate(F):
        for a, b in edges(f): adj.setdefault(frozenset((a, b)), []).append(fi)
    # root face flat
    f0 = F[root]; P = V[f0]; c = P.mean(0); n = np.cross(P[1] - P[0], P[2] - P[0]); n /= np.linalg.norm(n)
    u = P[0] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
    pos = {root: {v: np.array([(V[v] - c) @ u, (V[v] - c) @ w]) for v in f0}}
    tree = []; queue = [root]; seen = {root}
    while queue:
        fi = queue.pop(0)
        for a, b in sorted(edges(F[fi]), key=order_key):
            for fj in adj[frozenset((a, b))]:
                if fj in seen: continue
                # place fj: reflect its 3D shape across the shared edge in 2D
                A2, B2 = pos[fi][a], pos[fi][b]; fjv = F[fj]
                ea = V[b] - V[a]; L = np.linalg.norm(ea); ex = ea / L
                nj = np.cross(V[fjv[1]] - V[fjv[0]], V[fjv[2]] - V[fjv[0]]); nj /= np.linalg.norm(nj); ey = np.cross(nj, ex)
                e2 = (B2 - A2) / np.linalg.norm(B2 - A2); n2 = np.array([-e2[1], e2[0]])
                # which side is fi's interior? place fj on the other side
                ci = np.mean([pos[fi][v] for v in F[fi]], axis=0); side = -np.sign((ci - A2) @ n2)
                cj3 = V[fjv].mean(0); s3 = np.sign((cj3 - V[a]) @ ey)
                pos[fj] = {v: A2 + ((V[v] - V[a]) @ ex) * e2 + side * s3 * ((V[v] - V[a]) @ ey) * n2 for v in fjv}
                tree.append((fi, fj, frozenset((a, b)))); seen.add(fj); queue.append(fj)
    return pos, tree, adj
import random
def try_net(V, F, tries=600):
    """many spanning trees (random orders) x rotations; keep the net with the smallest bounding box that fits the A3 frame"""
    best = None; rng = random.Random(1)
    for t in range(tries):
        root = rng.randrange(len(F)); salt = [rng.random() for _ in range(len(V))]
        key = (lambda e, s_=salt: s_[e[0]] + s_[e[1]])
        pos, tree, adj = unfold(V, F, root, key)
        polys = [Polygon([pos[fi][v] for v in F[fi]]) for fi in range(len(F))]
        if not all(polys[i].intersection(polys[j]).area < 1e-9 for i, j in itertools.combinations(range(len(F)), 2)): continue
        allp = np.vstack([np.array(list(p.values())) for p in pos.values()])
        for ang in np.radians(np.arange(0, 180, 3)):
            R = np.array([[math.cos(ang), -math.sin(ang)], [math.sin(ang), math.cos(ang)]]); Q = allp @ R.T; span = np.ptp(Q, axis=0)
            # room for tabs (+16 mm) inside the frame 400 x 245
            if span[0] + 16 <= FW and span[1] + 16 <= FH:
                score = span[0] * span[1]
                if best is None or score < best[0]:
                    pr = {fi: {v: R @ p for v, p in d.items()} for fi, d in pos.items()}; best = (score, pr, tree, adj)
    return best

STD['rhombic dodecahedron'] = np.vstack([np.array(list(itertools.product((-1, 1), repeat=3)), float), orbit((2, 0, 0))])
KIT = [('dodecahedron', 'D', '12 pentagons', 'harder'), ('icosahedron', 'I', '20 triangles', 'medium'), ('cube', 'C', '6 squares', 'easy'),
       ('tetrahedron', 'T', '4 triangles', 'easy'), ('octahedron', 'O', '8 triangles', 'easy'),
       ('rhombic dodecahedron', '+', '12 rhombi: fills space by itself, like the cube', 'harder')]
COL['rhombic dodecahedron'] = '#f5cfa0'
pdf = PdfPages(OUT); report = []
for k, (name, letter, faces_txt, level) in enumerate(KIT):
    V = STD[name]; e0 = min(np.linalg.norm(V[i] - V[j]) for i, j in itertools.combinations(range(len(V)), 2)); V = V / e0
    Vm = V * EDGE; F = faces(Vm); res = try_net(Vm, F)
    if res is None: print(name, 'NO NET FITS A4'); report.append((name, False)); continue
    area, pos, tree, adj = res; treeedges = {e for _, _, e in tree}
    fig, ax = plt.subplots(figsize=(A4W / 25.4, A4H / 25.4)); ax.set_aspect('equal'); ax.axis('off')
    allp = np.vstack([np.array(list(p.values())) for p in pos.values()]); lo, hi = allp.min(0), allp.max(0)
    off = np.array([A4W / 2, (22 + A4H - 42) / 2]) - (lo + hi) / 2
    FACEPOLY = [Polygon([pos[fi][v] + off for v in f]) for fi, f in enumerate(F)]; TABS = []; tabbed = set()
    cut = sorted({frozenset((f[i], f[(i + 1) % len(f)])) for f in F for i in range(len(f))} - treeedges, key=lambda e: sorted(e))
    num = {e: i + 1 for i, e in enumerate(cut)}
    def tab_poly(A, B, ci, h):
        d = B - A; L = np.linalg.norm(d); nrm = np.array([-d[1], d[0]]) / L
        if (ci - A) @ nrm > 0: nrm = -nrm
        return np.array([A, A + d / L * 0.18 * L + nrm * h, B - d / L * 0.18 * L + nrm * h, B])
    def clear(Q):
        pq = Polygon(Q).buffer(-0.05)
        return all(pq.intersection(fp).area < 1e-6 for fp in FACEPOLY) and all(pq.intersection(t).area < 1e-6 for t in TABS)
    for fi, f in enumerate(F):
        P = np.array([pos[fi][v] for v in f]) + off; ci = P.mean(0)
        ax.fill(P[:, 0], P[:, 1], color=COL[name], lw=0)
        for i in range(len(f)):
            a, b = f[i], f[(i + 1) % len(f)]; e = frozenset((a, b)); A, B = P[i], P[(i + 1) % len(f)]
            if e in treeedges: ax.plot([A[0], B[0]], [A[1], B[1]], ls=(0, (4, 3)), color='#555', lw=0.8); continue
            ax.plot([A[0], B[0]], [A[1], B[1]], color='black', lw=1.0)
            m = (A + B) / 2; ins = m + (ci - m) * 0.22
            ax.text(ins[0], ins[1], str(num[e]), ha='center', va='center', fontsize=6.5, color='#333', weight='bold')
            if e in tabbed: continue
            tabbed.add(e); L = np.linalg.norm(B - A); Q = None
            for h in (min(7.0, 0.22 * L), 4.5, 3.0):
                cand = tab_poly(A, B, ci, h)
                if clear(cand): Q = cand; break
            if Q is None: tabbed.discard(e); continue
            TABS.append(Polygon(Q)); ax.fill(Q[:, 0], Q[:, 1], color='#e8e8e8', lw=0); ax.plot(Q[:, 0], Q[:, 1], color='black', lw=0.8)
            ax.plot([A[0], B[0]], [A[1], B[1]], ls=(0, (4, 3)), color='#555', lw=0.8)
    title = f"{letter} · {name.upper()}" if letter != '+' else f"BONUS · {name.upper()}"
    ax.text(12, A4H - 14, title, fontsize=13, weight='bold', color='#333')
    ax.text(12, A4H - 21, f"{faces_txt} · edge {EDGE:.0f} mm · {level}", fontsize=8.5, color='#444')
    ax.text(12, A4H - 27.5, "Print at 100%. Cut the solid lines, fold the dashed lines, glue the grey tabs. Edges with the same number meet.", fontsize=7, color='#444')
    ax.plot([12, 62], [12, 12], color='black', lw=2); ax.text(12, 15, '50 mm: check your print', fontsize=6.5)
    ax.text(A4W - 12, 12, 'DICTO · dictospheres.com', ha='right', fontsize=7, color='#666')
    ax.set_xlim(0, A4W); ax.set_ylim(0, A4H); fig.subplots_adjust(0, 0, 1, 1)
    fits = lo[0] + off[0] > 8 and hi[0] + off[0] < A4W - 8 and lo[1] + off[1] > 22 and hi[1] + off[1] < A4H - 34
    ok = fits and set(cut) <= tabbed
    report.append((name, ok)); print(f"{name}: faces {len(F)}, cut edges {len(cut)}, tabbed {len(tabbed & set(cut))}, fits {fits}")
    pdf.savefig(fig); plt.close(fig)
pdf.close()
print("FINAL", "ok" if all(r[1] for r in report) else "CHECK")
