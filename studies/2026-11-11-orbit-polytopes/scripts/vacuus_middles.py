"""The Vacuus of the middles of every 4D chain (DICTO 11 Nov: "go on with the other groups' middles"). For A4 (3-3-3), B4 (3-3-4),
F4 (3-4-3) and H4 (5-3-3): build the orbit polytope of a seed by Wythoff's construction (reflections in the simple roots), take its
hull, cells and 2-faces, and ask for every 2-face: does its central hyperplane belong to the group's mirrors, and which two cells
(kinds) share it. Seeds: the two ends (regular polytopes, controls) and the middle (0,1,1,0). H4 is the control against
vacuus_queens.py (bitruncated 600-cell: each of the 60 mirrors carries 20 triangles + 12 pentagons, the 2400 hexagons scatter)."""
import sys, itertools
import numpy as np
from collections import Counter
from scipy.spatial import ConvexHull
s5 = 5 ** .5; phi = (1 + s5) / 2
def unit(v): v = np.array(v, float); return v / np.linalg.norm(v)
# A4 in the 4D hyperplane sum = 0 of R^5
B = np.linalg.svd(np.ones((1, 5)))[2][1:]
A4 = [unit(B @ (np.eye(5)[i] - np.eye(5)[i + 1])) for i in range(4)]
B4 = [unit([1, -1, 0, 0]), unit([0, 1, -1, 0]), unit([0, 0, 1, -1]), unit([0, 0, 0, 1])]
F4 = [unit([0, 1, -1, 0]), unit([0, 0, 1, -1]), unit([0, 0, 0, 1]), unit([.5, -.5, -.5, -.5])]
def h4_roots():
    # roots from the 600-cell's 120 unit vertices; choose a simple system by a generic linear functional
    V = []
    for s in itertools.product((1, -1), repeat=4): V.append(np.array(s) / 2)
    for i in range(4):
        for sg in (1, -1): e = np.zeros(4); e[i] = sg; V.append(e)
    for p in itertools.permutations(range(4)):
        sgn = 1
        for i in range(4):
            for j in range(i + 1, 4):
                if p[i] > p[j]: sgn = -sgn
        if sgn != 1: continue
        for s in itertools.product((1, -1), repeat=3):
            base = [s[0] * phi / 2, s[1] * .5, s[2] / (2 * phi), 0.]
            v = np.zeros(4)
            for i in range(4): v[p[i]] = base[i]
            V.append(v)
    V = np.unique(np.round(np.array(V), 12), axis=0)
    f = np.array([1, .37, .113, .0271]); pos = [v for v in V if v @ f > 0]
    from scipy.optimize import nnls
    P = np.array(pos); simple = []
    for i, v in enumerate(pos):      # simple = not a nonnegative combination of the other positive roots
        others = np.delete(P, i, axis=0).T; c, r = nnls(others, v)
        if r > 1e-7: simple.append(v)
    assert len(simple) == 4, len(simple)
    return [unit(s) for s in simple]
H4 = h4_roots()
def chain(R):
    """order the simple roots along the Coxeter chain; return order and bond labels"""
    m = lambda a, b: int(round(np.pi / (np.pi - np.arccos(np.clip(a @ b, -1, 1))))) if abs(a @ b) > 1e-9 else 2
    n = len(R); deg = [sum(m(R[i], R[j]) > 2 for j in range(n) if j != i) for i in range(n)]
    order = [min(range(n), key=lambda i: (deg[i], -max(m(R[i], R[j]) for j in range(n) if j != i)))]
    while len(order) < n:
        order.append(next(j for j in range(n) if j not in order and m(R[order[-1]], R[j]) > 2))
    return [R[i] for i in order], [m(R[order[i]], R[order[i + 1]]) for i in range(n - 1)]
def group(R):
    G = [np.eye(4)]; gens = [np.eye(4) - 2 * np.outer(r, r) for r in R]; seen = {tuple(np.round(np.eye(4), 6).ravel())}; fr = list(G)
    while fr:
        nf = []
        for g in fr:
            for s in gens:
                h = s @ g; k = tuple(np.round(h, 6).ravel())
                if k not in seen: seen.add(k); G.append(h); nf.append(h)
        fr = nf
    return G
def norm_dir(n): n = unit(n); return n if n[np.argmax(np.abs(n))] > 0 else -n
def run(name, R, seeds):
    R, bonds = chain(R); G = group(R)
    mirrors = []; seenm = set()
    for g in G:
        for r in R:
            m = norm_dir(g @ r)
            if not mirrors or np.abs(np.array(mirrors) @ m).max() < 1 - 1e-7: mirrors.append(m)
    print(f"{name}: chain {bonds}, order {len(G)}, mirrors {len(mirrors)}", flush=True)
    Rm = np.array(R); out = {}
    for lab in seeds:
        x = np.linalg.solve(Rm, np.array(lab, float))       # r_i . x = label_i
        P = []
        for y in (g @ x for g in G):
            if not P or np.linalg.norm(np.array(P) - y, axis=1).min() > 1e-6: P.append(y)
        P = np.array(P)
        W = np.linalg.inv(Rm)            # columns: fundamental weights (r_i . w_j = delta_ij)
        cand = []; seenc = set()
        for j in range(4):
            for g in G:
                d = unit(g @ W[:, j])
                if not cand or (np.array(cand) @ d).max() < 1 - 1e-9: cand.append(d)
        cells = set()
        for d in cand:
            hv = P @ d; top = frozenset(np.where(hv > hv.max() - 1e-7)[0])
            if len(top) >= 4 and np.linalg.matrix_rank(P[list(top)] - P[list(top)].mean(0), tol=1e-7) == 3: cells.add(top)
        cells = list(cells); kind = [len(c) for c in cells]
        faces = {}
        for i, j in itertools.combinations(range(len(cells)), 2):
            sh = cells[i] & cells[j]
            if len(sh) >= 3 and np.linalg.matrix_rank(P[list(sh)] - P[list(sh)].mean(0), tol=1e-7) == 2:
                faces[sh] = tuple(sorted((kind[i], kind[j])))
        on = Counter(); off = Counter(); planes_on = Counter(); planes_off = {}
        for f, kk in faces.items():
            Q = P[list(f)]; n = np.linalg.svd(Q)[2][-1]
            key = (len(f), 'cells ' + '+'.join(map(str, kk)))
            mi = next((i for i, q in enumerate(mirrors) if abs(abs(n @ q) - 1) < 1e-7), None)
            if mi is not None: on[key] += 1; planes_on[mi] += 1
            else:
                nd = tuple(np.round(norm_dir(n), 6)); planes_off.setdefault(nd, 0); planes_off[nd] += 1; off[key] += 1
        tot = len(faces)
        print(f"  seed {lab}: {len(P)} corners, {len(cells)} cells (corners per cell {dict(Counter(kind))}), {tot} 2-faces; "
              f"on mirrors {sum(on.values())} [{', '.join(f'{k[0]}-gons between {k[1]}: {v}' for k, v in sorted(on.items()))}] "
              f"per mirror {dict(Counter(planes_on.values()))}; scattered {sum(off.values())} [{', '.join(f'{k[0]}-gons between {k[1]}: {v}' for k, v in sorted(off.items()))}] "
              f"on {len(planes_off)} planes, per plane {dict(Counter(planes_off.values()))}", flush=True)
        out[tuple(lab)] = (tot, sum(on.values()) + sum(off.values()))
    return out, len(G), len(mirrors)
res = {}
ok = True
for name, R, want_order, want_mirrors in [('A4 (5-cell chain)', A4, 120, 10), ('B4 (tesseract chain)', B4, 384, 16), ('F4 (24-cell chain)', F4, 1152, 24), ('H4 (Queens, control)', H4, 14400, 60)]:
    seeds = [(1, 0, 0, 0), (0, 1, 1, 0), (0, 0, 0, 1)]
    if name.startswith('H4') and '--no-h4' in sys.argv: continue
    if name.startswith('H4'): seeds = [(0, 1, 1, 0)]
    o, order, nm = run(name, R, seeds)
    ok &= order == want_order and nm == want_mirrors and all(a == b for a, b in o.values())
print('FINAL ok' if ok else 'FINAL FAIL')
