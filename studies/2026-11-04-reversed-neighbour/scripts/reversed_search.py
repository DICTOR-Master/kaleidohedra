#!/usr/bin/env python3
"""Reversed neighbour (Concordance gap 3; #92 open point 1, #93 open point 1). Tiles: T = centre pyramid of the regular tetrahedron
(edge 1). #92 Prop. 7: round every lateral edge e = XY (X apex) of a T pyramid lie exactly three T pyramids whose lateral edges are e.
So each of the two other sectors round e holds either the NORMAL piece (the tile rotated 120 deg about XY: apex X, its tetrahedron's
next pyramid) or the REVERSED piece (that one reflected in the perpendicular bisector plane of XY: apex Y).
Search: start with P and a reversed neighbour Q in one sector; repeatedly take a lateral edge with an unfilled sector, branch on
{normal, reversed}, keep candidates whose interior meets no placed tile (separating-axis test), or that coincide with a placed tile.
A branch dies when a sector has no candidate. If every branch dies the reversed neighbour is impossible (forced T pyramids alone
overlap); otherwise report surviving depth. Only forced pieces are placed, so a death is a proof (up to float tolerance 1e-9)."""
import itertools, math, sys, json, os
import numpy as np
EPS = 1e-9
def tet_vertices():
    v = np.array([(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)], float); return v / (2*math.sqrt(2))   # edge 1, centre 0
TV = tet_vertices()
def pyramid(apex, base): return np.array([apex, *base])
P0 = pyramid(np.zeros(3), TV[1:])          # apex at centre, base face (1,2,3)
def faces(t):
    return [(0, 1, 2), (0, 2, 3), (0, 1, 3), (1, 2, 3)]
def axes(t):
    ax = []
    for f in faces(t):
        n = np.cross(t[f[1]] - t[f[0]], t[f[2]] - t[f[0]]); ax.append(n / np.linalg.norm(n))
    return ax
def edges(t): return [t[j] - t[i] for i, j in itertools.combinations(range(4), 2)]
def overlap(a, b):
    """interiors of two tetrahedra intersect? separating axis theorem."""
    cand = axes(a) + axes(b)
    for ea in edges(a):
        for eb in edges(b):
            c = np.cross(ea, eb); n = np.linalg.norm(c)
            if n > 1e-12: cand.append(c / n)
    for n in cand:
        pa = a @ n; pb = b @ n
        if pa.max() <= pb.min() + EPS or pb.max() <= pa.min() + EPS: return False
    return True
def same(a, b):
    return np.allclose(a[0], b[0], atol=1e-7) and all(np.min(np.linalg.norm(b[1:] - p, axis=1)) < 1e-7 for p in a[1:])
def rot(points, X, Y, ang):
    k = (Y - X) / np.linalg.norm(Y - X); c, s = math.cos(ang), math.sin(ang)
    out = []
    for p in points:
        v = p - X; out.append(X + v*c + np.cross(k, v)*s + k*(k @ v)*(1 - c))
    return np.array(out)
def reflect_bisector(points, X, Y):
    m = (X + Y)/2; k = (Y - X)/np.linalg.norm(Y - X)
    return np.array([p - 2*((p - m) @ k)*k for p in points])
def candidates(t, li):
    """the two other sectors round lateral edge (apex t[0], base vertex t[li]); each: [normal, reversed]"""
    X, Y = t[0], t[li]; out = []
    for ang in (2*math.pi/3, -2*math.pi/3):
        n = rot(t, X, Y, ang)
        r = reflect_bisector(n, X, Y)            # apex now at Y
        # reorder r so that index 0 is its apex: the image of X is Y; apex of r = image of n[0] = Y
        out.append([n, r])
    return out
def search(tiles, todo, depth, maxdepth, stats):
    stats['nodes'] += 1
    if depth >= maxdepth: stats['survive'] += 1; return True
    while todo:
        ti, li, si = todo[0]
        t = tiles[ti]; cands = candidates(t, li)[si]
        # sector already filled by a placed tile that equals a candidate?
        filled = any(same(c, u) for c in cands for u in tiles)
        if filled: todo = todo[1:]; continue
        alive = False
        for c in cands:
            if any(overlap(c, u) for u in tiles): continue
            nt = tiles + [c]; k = len(tiles)
            nt_todo = todo[1:] + [(k, l, s) for l in (1, 2, 3) for s in (0, 1)]
            if search(nt, nt_todo, depth + 1, maxdepth, stats): alive = True
            if alive and stats['first_only']: return True
        return alive
    stats['closed'] += 1; return True
results = {}
for maxdepth in (int(a) for a in (sys.argv[1:] or ['6', '9', '12'])):
    stats = {'nodes': 0, 'survive': 0, 'closed': 0, 'first_only': True}
    P = P0
    Q = candidates(P, 1)[0][1]                    # reversed neighbour across one sector of P's lateral edge (apex, V1)
    assert not overlap(P, Q)
    todo = [(0, l, s) for l in (1, 2, 3) for s in (0, 1)] + [(1, l, s) for l in (1, 2, 3) for s in (0, 1)]
    ok = search([P, Q], todo, 2, maxdepth, stats)
    results[maxdepth] = {'some_branch_survives': ok, **stats}
    print(f'max tiles {maxdepth}: some branch survives = {ok}; nodes {stats["nodes"]}', flush=True)
    if not ok: print('every branch with a reversed neighbour dies: IMPOSSIBLE (forced T pyramids overlap)'); break
os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data'), exist_ok=True)
json.dump(results, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'reversed-search.json'), 'w'), indent=1)
