#!/usr/bin/env python3
"""Method B: count the pieces of ONE Coxeter chamber C of W(H4), independently of the global
lattice and of the group action.  Zaslavsky's theorem for an open convex set C:
    #regions of A inside C = sum over flats X of A with X ∩ C nonempty of |mu(0, X)|,
and mu(0, X) only involves the walls through X, all of which meet C when X does.  So only the
walls meeting C are used.  C = {x : alpha_i . x > 0}, alpha_i the simple roots; its rays are
omega_j (alpha_i . omega_j = 0 for i != j, > 0 for i = j).  All tests exact in Z[phi].
  wall n meets C      <=> n.omega_j takes both strict signs
  plane X meets C     <=> some e1 d_i + e2 d_j is in C, d_i = direction of X ∩ alpha_i^perp
                          (the closure of X ∩ C is a pointed sector bounded by two such rays)
  line d meets C      <=> d or -d in C
Then: if all 60 mirrors of W are walls of A, every region lies in one chamber and
#regions = 14400 * #pieces of C.   (written from scratch; usage: chamber.py walls.npz NAME OUT.json)
"""
import sys, os, json, itertools, time
from math import comb
from collections import Counter
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import zphi as Z

NPZ, NAME, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
D = np.load(NPZ)
N = D[NAME]; alpha = D['alpha']; n = len(N)
t0 = time.time()
def say(*a): print(f'[{time.time() - t0:7.1f}s]', *a, flush=True)

def in_C(x):            # x [..., 4, 2] -> bool, strictly inside the open chamber
    s = Z.sign(Z.dot(x[..., None, :, :], alpha))
    return (s > 0).all(-1)

# rays of C
om = []
for j in range(4):
    o = [alpha[i] for i in range(4) if i != j]
    w = Z.reduce(Z.cross3(*o))
    sg = Z.sign(Z.dot(w, alpha[j])); assert sg != 0
    om.append(w if sg > 0 else -w)
om = np.array(om)
for i in range(4):
    for j in range(4):
        s = Z.sign(Z.dot(alpha[i], om[j]))
        assert (s > 0) if i == j else (s == 0)

# mirrors of W in A?
mir = Z.canon(D['A60']); keys = {tuple(k) for k in Z.canon(N)}
mirrors_in = all(tuple(k) in keys for k in mir)
say(f'{NAME}: {n} walls; all 60 mirrors of W(H4) are walls: {mirrors_in}')

sg = Z.sign(Z.dot(N[:, None, :, :], om[None]))            # [n, 4]
meets = (sg > 0).any(1) & (sg < 0).any(1)
M = np.nonzero(meets)[0]; m = len(M)
say('walls meeting the open chamber:', m)
NM = N[M]

# for each a, classes of b by projection (exact)
hp = np.zeros((m, m), np.int64)
for a in range(m):
    others = np.array([b for b in range(m) if b != a])
    na = NM[a]
    p = Z.mul(Z.dot(na, na)[None, None, :], NM[others]) - Z.mul(Z.dot(NM[others], na)[:, None, :], na[None])
    _, inv = np.unique(Z.canon(p), axis=0, return_inverse=True); inv = inv.ravel()
    hp[a, others] = np.bincount(inv)[inv] + 1
assert (hp == hp.T).all()
# distinct planes, each by its exact member set: c is in plane(a,b) iff n_a, n_b, n_c are
# dependent iff cross3(n_a, n_b, n_c) = 0
planes = {}
E4 = np.zeros((4, 4, 2), np.int64)
for i in range(4): E4[i, i, 0] = 1
for a in range(m):
    for b in range(a + 1, m):
        dep = np.all(Z.cross3(NM[a][None], NM[b][None], NM) == 0, axis=(-1, -2))
        mem = tuple(np.nonzero(dep)[0].tolist())
        assert len(mem) == hp[a, b]
        planes.setdefault(mem, (a, b))
say('planes spanned by walls meeting C:', len(planes))
sumX = 0; nX = Counter()
for mem, (a, b) in planes.items():
    d = []
    for i in range(4):
        v = Z.cross3(NM[a], NM[b], alpha[i])
        if np.any(v != 0): d.append(Z.reduce(v))
    hit = False
    for x, y in itertools.combinations(d, 2):
        for e1, e2 in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
            if in_C(e1 * x + e2 * y): hit = True; break
        if hit: break
    if hit:
        sumX += len(mem) - 1; nX[len(mem)] += 1
say('planes meeting C by walls through them:', dict(nX), ' sum |mu| =', sumX)

# lines: triples of walls in M
tri = np.array(list(itertools.combinations(range(m), 3))).reshape(-1, 3)
d = Z.cross3(NM[tri[:, 0]], NM[tri[:, 1]], NM[tri[:, 2]]) if len(tri) else np.zeros((0, 4, 2), np.int64)
nonzero = np.any(d != 0, axis=(-1, -2))
d = Z.reduce(d[nonzero])
keys_, first = np.unique(Z.canon(d), axis=0, return_index=True) if len(d) else (np.zeros((0, 9)), np.zeros(0, int))
dl = d[first]
inside = (in_C(dl) | in_C(-dl)) if len(dl) else np.zeros(0, bool)
dl = dl[inside]
say('distinct lines spanned by walls meeting C:', len(keys_), '; meeting C:', len(dl))
inc = (Z.dot(NM[None], dl[:, None]) == 0).all(-1) if len(dl) else np.zeros((0, m), bool)
hs = inc.sum(1)
summu = 0; types = Counter()
for i in range(len(dl)):
    S = np.nonzero(inc[i])[0]; h = len(S)
    # sum over planes X through L of (h_X - 1) = sum over pairs 2/h_X
    tot = 0; flats = set()
    for a, b in itertools.combinations(S, 2):
        dep = np.all(Z.cross3(NM[a][None], NM[b][None], NM[S]) == 0, axis=(-1, -2))
        flats.add(tuple(S[dep].tolist()))
    sx = sum(len(f) - 1 for f in flats)
    mu = -1 + h - sx
    assert mu < 0
    summu += -mu
    types[(h, mu)] += 1
say('lines meeting C by (walls through, mu):', dict(sorted(types.items())), ' sum |mu| =', summu)
pieces = 1 + m + sumX + summu
say(f'pieces of one chamber = 1 + {m} + {sumX} + {summu} = {pieces};  x 14400 = {14400 * pieces}')
json.dump(dict(arrangement=NAME, walls=n, mirrors_are_walls=bool(mirrors_in), walls_meeting_chamber=m,
               planes_meeting_chamber={str(k): v for k, v in sorted(nX.items())}, planes_sum_mu=sumX,
               lines_meeting_chamber={f'{k[0]},{k[1]}': v for k, v in sorted(types.items())},
               lines_sum_abs_mu=summu, pieces=pieces, regions=14400 * pieces),
          open(OUT, 'w'), indent=1)
print('FINAL ok' if mirrors_in else 'FINAL FAIL mirrors not all walls')
