"""The nest as a card kit (DICTO 11-06: "a nested paper card model", the nest kit suggested earlier; build A: coloured card shells that open
like Russian dolls). Five nets at the nest's sizes (octahedron edge OE mm): O 1 > I sqrt2/phi^2 > D (edge^2 = 1/3 - sqrt5/9) > C sqrt2/3 >
T 2/3, each inner shell a further 2% smaller for the card's thickness. Each net: a spanning tree of the face graph laid flat (checked: no
overlap), glue tabs on half of the cut edges (each cut edge gets exactly one tab), and one LID face hinged on one edge whose other edges
carry tuck flaps (no glue), so each shell can be opened and the next one put in. Lines: cut solid, fold dashed. A3 pages, 50 mm scale
bar. Usage: nest_kit.py [OE] [out.pdf]"""
import sys, math, itertools, numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy.spatial import ConvexHull
from shapely.geometry import Polygon
OE = float(sys.argv[1]) if len(sys.argv) > 1 else 150.0; OUT = sys.argv[2] if len(sys.argv) > 2 else 'nest-kit.pdf'
phi = (1 + 5 ** .5) / 2; SHR = 0.98
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
            if span[0] + 16 <= 400 and span[1] + 16 <= 245:
                score = span[0] * span[1]
                if best is None or score < best[0]:
                    pr = {fi: {v: R @ p for v, p in d.items()} for fi, d in pos.items()}; best = (score, pr, tree, adj)
    return best
pdf = PdfPages(OUT); A3W, A3H = 420.0, 297.0
size = OE; report = []
for k, (name, rel) in enumerate(ORDER):
    V = STD[name]; e0 = min(np.linalg.norm(V[i] - V[j]) for i, j in itertools.combinations(range(len(V)), 2)); V = V / e0
    edge_mm = OE * rel * (SHR ** k); Vm = V * edge_mm; F = faces(Vm)
    res = try_net(Vm, F)
    if res is None: print(name, 'no net fits A3'); continue
    area, pos, tree, adj = res
    treeedges = {e for _, _, e in tree}
    # lid: a leaf face of the tree (appears once as child, never as parent)
    parents = {p for p, _, _ in tree}; leaves = [c for _, c, _ in tree if c not in parents]; lid = leaves[0]
    fig, ax = plt.subplots(figsize=(A3W / 25.4, A3H / 25.4)); ax.set_aspect('equal'); ax.axis('off')
    allp = np.vstack([np.array(list(p.values())) for p in pos.values()]); lo, hi = allp.min(0), allp.max(0)
    off = np.array([A3W / 2, (18 + A3H - 30) / 2]) - (lo + hi) / 2
    tabbed = set(); FACEPOLY = [Polygon([pos[fi][v] + off for v in f]) for fi, f in enumerate(F)]; TABS = []
    def tab_poly(A, B, ci, kind, h):
        d = B - A; L = np.linalg.norm(d); nrm = np.array([-d[1], d[0]]) / L
        if (ci - A) @ nrm > 0: nrm = -nrm
        inset = 0.18 * L if kind == 'glue' else 0.08 * L
        return np.array([A, A + d / L * inset + nrm * h, B - d / L * inset + nrm * h, B])
    def clear(Q):
        pq = Polygon(Q).buffer(-0.05)
        return all(pq.intersection(fp).area < 1e-6 for fp in FACEPOLY) and all(pq.intersection(t).area < 1e-6 for t in TABS)
    for fi, f in enumerate(F):
        P = np.array([pos[fi][v] for v in f]) + off
        ax.fill(P[:, 0], P[:, 1], color=COL[name], lw=0)
        for i in range(len(f)):
            a, b = f[i], f[(i + 1) % len(f)]; e = frozenset((a, b)); A, B = P[i], P[(i + 1) % len(f)]
            if e in treeedges: ax.plot([A[0], B[0]], [A[1], B[1]], ls=(0, (4, 3)), color='#555', lw=0.8); continue
            ax.plot([A[0], B[0]], [A[1], B[1]], color='black', lw=1.0)
            # tab: once per cut edge; the lid's free edges get tuck flaps (on the lid), its neighbours none
            other = [g for g in adj[e] if g != fi][0]
            if fi == lid: kind = 'tuck'
            elif other == lid: continue
            elif e in tabbed: continue
            else: kind = 'glue'
            tabbed.add(e)
            ci = P.mean(0); L = np.linalg.norm(B - A); Q = None
            for h in (min(7.0, 0.22 * L), 4.5, 3.0):
                cand = tab_poly(A, B, ci, kind, h)
                if clear(cand): Q = cand; break
            if Q is None and kind == 'glue':
                tabbed.discard(e); continue          # leave it for the face on the other side of this edge
            if Q is None: Q = tab_poly(A, B, ci, kind, 2.0)
            TABS.append(Polygon(Q))
            ax.fill(Q[:, 0], Q[:, 1], color='#e8e8e8' if kind == 'glue' else '#fff6d8', lw=0)
            ax.plot(Q[:, 0], Q[:, 1], color='black', lw=0.8); ax.plot([A[0], B[0]], [A[1], B[1]], ls=(0, (4, 3)), color='#555', lw=0.8)
        c = P.mean(0)
        if fi == lid: ax.text(c[0], c[1], 'LID\n(tuck, no glue)', ha='center', va='center', fontsize=7, color='#333')
    ax.text(12, A3H - 14, f"DICTO · Five in the Octet · nest kit · {k + 1}/5  {name.upper()}  edge {edge_mm:.1f} mm", fontsize=12, weight='bold')
    ax.text(12, A3H - 22, f"Build the tetrahedron first; close each shell over the one inside with its lid. Cut solid lines, fold dashed lines; glue grey tabs, tuck the cream flaps. Inner shells are {100*(1-SHR):.0f}% under the exact nest size for the card.", fontsize=7.5)
    ax.plot([12, 62], [10, 10], color='black', lw=2); ax.text(12, 13, '50 mm', fontsize=7)
    ax.text(A3W - 12, 10, 'dictospheres.com', ha='right', fontsize=7, color='#666')
    ax.set_xlim(0, A3W); ax.set_ylim(0, A3H); fig.subplots_adjust(0, 0, 1, 1)
    fits = lo[0] + off[0] > 10 - 0 and hi[0] + off[0] < A3W - 10 and lo[1] + off[1] > 22 and hi[1] + off[1] < A3H - 34
    cut = {frozenset((f[i], f[(i + 1) % len(f)])) for f in F for i in range(len(f))} - treeedges
    lid_edges = {frozenset((F[lid][i], F[lid][(i + 1) % len(F[lid])])) for i in range(len(F[lid]))}
    missing = len(cut - tabbed - lid_edges) + len((lid_edges & cut) - tabbed)
    report.append((name, round(edge_mm, 1), len(F), fits and missing == 0))
    print(f"{name}: cut edges {len(cut)}, with a tab or flap {len(cut & tabbed)}, missing {missing}")
    pdf.savefig(fig); plt.close(fig)
pdf.close()
for r in report: print(f"{r[0]:13s} edge {r[1]:6.1f} mm, {r[2]} faces, fits A3: {r[3]}")
print("FINAL", "ok" if all(r[3] for r in report) else "CHECK FIT")
