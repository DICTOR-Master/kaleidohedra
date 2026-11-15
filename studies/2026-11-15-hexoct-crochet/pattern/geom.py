"""Exact Narcissus and cube for the crochet pattern: faces with outward orientation, edges labelled in assembly order,
dihedral angles, consistent (unmirrored) unfolding, and the split of each core net into pieces that fit an A4 text column.
Narcissus corners: paper #98 (ball spacing a = 1). L = a/sqrt(2) = square side."""
import math, itertools, numpy as np
from scipy.spatial import ConvexHull
from shapely.geometry import Polygon as SPoly
s3 = math.sqrt(3); H = math.sqrt(2/3)
XN = np.array([(0,0,0),(0,1/s3,-H/2),(0,1/s3,0),(.5,-1/(2*s3),-H/2),(.5,-1/(2*s3),0),(.5,1/(2*s3),-H),(.5,s3/2,0),(1,0,0),(1,1/s3,-H/2),(1,1/s3,0)])
XC = np.array([(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)], float)/math.sqrt(2)   # cube of side L = 1/sqrt(2)
def solid(X):
    """faces as corner lists counter-clockwise seen from outside, with outward normals"""
    h = ConvexHull(X); fs = {}
    for eq, s in zip(h.equations, h.simplices): fs.setdefault(tuple(np.round(eq, 7)), set()).update(s)
    F, N = [], []
    for k, idx in fs.items():
        n = np.array(k[:3]); idx = list(idx); c = X[idx].mean(0); u = X[idx[0]] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
        F.append(sorted(idx, key=lambda i: math.atan2((X[i]-c) @ w, (X[i]-c) @ u))); N.append(n)
    return F, np.array(N)
def kind(f): return {3: 'triangle', 4: 'square', 6: 'hexagon'}[len(f)]
def edge_list(F):
    E = {}
    for i, f in enumerate(F):
        for k in range(len(f)): E.setdefault(frozenset((f[k], f[(k+1) % len(f)])), []).append(i)
    return E
def label_edges(X, F, N):
    """letters A, B, ... in assembly order. Narcissus: hexagon-triangle (round the hexagon), triangle-triangle, square-square,
    square-triangle. Cube: bottom square's 4 edges, 4 upright edges, 4 top edges."""
    E = edge_list(F); out = {}
    def ang(e, c, ax):
        m = X[list(e)].mean(0) - c; u = np.cross(ax, [1, 0.1, 0.2]); u /= np.linalg.norm(u); w = np.cross(ax, u); return math.atan2(m @ w, m @ u)
    if len(F) == 10:
        hx = next(i for i, f in enumerate(F) if len(f) == 6); c = X[F[hx]].mean(0); ax = N[hx]
        groups = [lambda a, b: {kind(F[a]), kind(F[b])} == {'hexagon', 'triangle'}, lambda a, b: kind(F[a]) == kind(F[b]) == 'triangle',
                  lambda a, b: kind(F[a]) == kind(F[b]) == 'square', lambda a, b: {kind(F[a]), kind(F[b])} == {'square', 'triangle'}]
    else:
        bot = int(np.argmin(N[:, 2])); top = int(np.argmax(N[:, 2])); c = X.mean(0); ax = np.array([0, 0, 1.])
        groups = [lambda a, b: bot in (a, b), lambda a, b: bot not in (a, b) and top not in (a, b), lambda a, b: top in (a, b)]
    letters = iter('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    for g in groups:
        es = sorted([e for e, fs in E.items() if g(*fs) and e not in out], key=lambda e: ang(e, c, ax))
        for e in es: out[e] = next(letters)
    assert len(out) == len(E), (len(out), len(E))
    return out, E
def dihedral(N, a, b): return 180 - math.degrees(math.acos(np.clip(N[a] @ N[b], -1, 1)))
def local2d(X, f, n):
    P = X[f]; c = P.mean(0); u = P[0] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
    return {v: np.array([(X[v]-c) @ u, (X[v]-c) @ w]) for v in f}
def unfold(X, F, N, faces, tree_edges, root):
    """unmirrored net seen from outside; tree_edges: list of (face, face)"""
    E = edge_list(F); placed = {root: local2d(X, F[root], N[root])}; todo = [root]
    adj = {i: [] for i in faces}
    for a, b in tree_edges: adj[a].append(b); adj[b].append(a)
    while todo:
        i = todo.pop()
        for j in adj[i]:
            if j in placed: continue
            a, b = next(tuple(e) for e, fs in E.items() if set(fs) == {i, j})
            L2 = local2d(X, F[j], N[j]); pa, pb = placed[i][a], placed[i][b]; ma, mb = L2[a], L2[b]
            t = math.atan2(*(pb - pa)[::-1]) - math.atan2(*(mb - ma)[::-1]); R = np.array([[math.cos(t), -math.sin(t)], [math.sin(t), math.cos(t)]])
            placed[j] = {v: R @ (p - ma) + pa for v, p in L2.items()}; todo.append(j)
    return {i: np.array([placed[i][v] for v in F[i]]) for i in placed}
def overlap(polys):
    ks = list(polys); return max([SPoly(polys[a]).intersection(SPoly(polys[b])).area for a, b in itertools.combinations(ks, 2)] + [0])
def best_rotation(polys, W, Hm):
    P = np.vstack(list(polys.values())); best = None
    for d in np.arange(0, 180, 0.5):
        t = math.radians(d); R = np.array([[math.cos(t), -math.sin(t)], [math.sin(t), math.cos(t)]]); Q = P @ R.T
        w, h = np.ptp(Q[:, 0]), np.ptp(Q[:, 1])
        if w <= W and h <= Hm and (best is None or w*h < best[0]): best = (w*h, d, w, h)
    return best
def connected(nodes, edges):
    par = {n: n for n in nodes}
    def fd(x):
        while par[x] != x: x = par[x]
        return x
    for a, b in edges: par[fd(a)] = fd(b)
    return len({fd(n) for n in nodes}) == 1
def split_net(X, F, N, W, Hm, scale):
    """every connected face set whose unmirrored unfolding (some spanning tree, no overlap) fits W x Hm (mm) in some rotation;
    then the partition into the fewest such pieces (ties: largest smallest piece)."""
    Xs = X*scale; E = edge_list(F); fe = [tuple(fs) for fs in E.values()]; nF = len(F); fits = {}
    for r in range(1, nF + 1):
        for S in itertools.combinations(range(nF), r):
            ie = [e for e in fe if e[0] in S and e[1] in S]
            if not connected(S, ie): continue
            if r > 1 and not any(set(S) - {x} and frozenset(set(S) - {x}) in fits for x in S): continue   # grow from fitting sets
            best = None
            for T in itertools.combinations(ie, r - 1):
                if not connected(S, T): continue
                P = unfold(Xs, F, N, S, T, S[0])
                if overlap(P) > 1e-6: continue
                b = best_rotation(P, W, Hm)
                if b and (best is None or b[0] < best[0]): best = (b[0], b[1], T, P)
            if best: fits[frozenset(S)] = best
    sols = []
    def rec(left, parts):
        if not left: sols.append(list(parts)); return
        if sols and len(parts) >= min(len(s) for s in sols): return
        f0 = min(left)
        for S in sorted(fits, key=len, reverse=True):
            if f0 in S and S <= left: rec(left - S, parts + [S])
    rec(frozenset(range(nF)), [])
    m = min(len(s) for s in sols); sols = [s for s in sols if len(s) == m]
    sols.sort(key=lambda s: -min(len(p) for p in s))
    return sols[0], fits
