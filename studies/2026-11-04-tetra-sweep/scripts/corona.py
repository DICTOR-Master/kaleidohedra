#!/usr/bin/env python3
"""Local test: around one S(2) at the origin, can every octet cell within radius R be covered by non-overlapping copies (cell-aligned, the 2 orientations,
fcc translations)? If not for some R, S(2) has no cell-aligned tiling of space at all (periodic or not). Algorithm X with secondary columns (cells outside the ball)."""
import sys, itertools, json, numpy as np
sys.argv, R = [sys.argv[0]], float(sys.argv[1])
exec(open('scripts/tile_octet.py').read().split("if __name__")[0])
cl = PIECES['S2'](); kinds = [c[0] for c in cl]; pts = np.array([c[1] for c in cl]); cen = pts.mean(0)
orients = []; seen = set()
for perm in itertools.permutations(range(3)):
    for sg in itertools.product((1, -1), repeat=3):
        M = np.zeros((3, 3))
        for i in range(3): M[i, perm[i]] = sg[i]
        Q = (pts - cen) @ M.T + cen
        k = frozenset((kd, tuple(np.round(q - Q.min(0), 6))) for kd, q in zip(kinds, Q))
        if k not in seen: seen.add(k); orients.append(Q)
def ck(kind, p): return (kind, tuple(np.round(p*2).astype(int)))
ball = {ck(k, np.array(p)) for k, p in cells(int(R) + 8) if np.linalg.norm(np.array(p) - cen) <= R}
rows = []; ori = {}; shifts = [B @ np.array(v, float) for v in itertools.product(range(-int(R) - 8, int(R) + 9), repeat=3)]
for oi, Q in enumerate(orients):
    for s in shifts:
        if np.linalg.norm(Q.mean(0) + s - cen) > R + 6: continue
        r = tuple(ck(k, q + s) for k, q in zip(kinds, Q))
        if any(c in ball for c in r): rows.append(r); ori[tuple(sorted(r))] = (oi, [float(x) for x in s])
rows = list(set(rows)); base = tuple(ck(k, q) for k, q in zip(kinds, pts))
allc = sorted({c for r in rows for c in r}); idx = {c: i for i, c in enumerate(allc)}
ORI = [ori[tuple(sorted(r))] for r in rows]; rows = [tuple(idx[c] for c in r) for r in rows]; prim = {idx[c] for c in ball}
X = {j: set() for j in range(len(allc))}
for i, r in enumerate(rows):
    for j in r: X[j].add(i)
def sel(i):
    cols = []
    for j in rows[i]:
        for k in X[j]:
            for l in rows[k]:
                if l != j: X[l].discard(k)
        cols.append(X.pop(j))
    return cols
def desel(i, cols):
    for j in reversed(rows[i]):
        X[j] = cols.pop()
        for k in X[j]:
            for l in rows[k]:
                if l != j: X[l].add(k)
nodes = [0]; chosen = []
def rec():
    nodes[0] += 1
    P = [j for j in X if j in prim]
    if not P: return True
    j = min(P, key=lambda c: (len(X[c]), np.linalg.norm(np.array(allc[c][1])/2 - cen)))
    for i in list(X[j]):
        cols = sel(i); chosen.append(i)
        if rec(): return True
        desel(i, cols); chosen.pop()
    return False
b = tuple(idx[c] for c in base); ib = rows.index(tuple(sorted(b, key=lambda x: x))) if tuple(sorted(b)) in [tuple(sorted(r)) for r in rows] else None
ib = [tuple(sorted(r)) for r in rows].index(tuple(sorted(b))); sel(ib)
ok = rec()
pl = [ORI[i] for i in chosen] + [ORI[ib]]
json.dump(pl, open(f'data/patch-R{int(R)}.json', 'w'))
print(json.dumps({"R": R, 'ball_cells': len(ball), 'placements': len(rows), 'nodes': nodes[0], 'patch_exists': ok}))
