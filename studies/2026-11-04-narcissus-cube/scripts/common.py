#!/usr/bin/env python3
"""Smallest common dissection of Narcissus and the cube (DICTO 4 Nov: "by being halved" -> Sydler: equal volume, both Dehn-zero, so a common
dissection exists; find a small one). Stage 1: 2-piece candidates. For cube placements (24 rotations x the Narcissus axis frames x translations on a
grid of step 1/24): shared piece I = N ∩ C; leftovers A = N \\ C and B = C \\ N (equal volumes). A hit = A and B each one convex piece and congruent
(distance multiset, with and without mirror). Near-misses (A, B convex, volumes equal, different shapes) logged for stage 2 (split each in two)."""
import math, itertools, json, time, sys, numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
H = math.sqrt(2/3); s3 = math.sqrt(3)
N = np.array([[0,0,0],[0,1/s3,-H/2],[0,1/s3,0],[.5,-1/(2*s3),-H/2],[.5,-1/(2*s3),0],[.5,1/(2*s3),-H],[.5,s3/2,0],[1,0,0],[1,1/s3,-H/2],[1,1/s3,0]])
N = N - N.mean(0); hN = ConvexHull(N); VN = hN.volume
e = 1/math.sqrt(2); C0 = np.array(list(itertools.product((-e/2, e/2), repeat=3)))
# cube frames: body diagonal along z (the natural c-layer orientation) and edge along z; plus all 24 cube rotations
def rot_to(a, b):
    a = a/np.linalg.norm(a); b = b/np.linalg.norm(b); v = np.cross(a, b); s = np.linalg.norm(v); c = a @ b
    if s < 1e-12: return np.eye(3) if c > 0 else -np.eye(3)
    K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]]); return np.eye(3) + K + K @ K*((1 - c)/s**2)
def rz(t): return np.array([[math.cos(t), -math.sin(t), 0], [math.sin(t), math.cos(t), 0], [0, 0, 1]])
CUBE_ROT = []
for perm in itertools.permutations(range(3)):
    for sg in itertools.product((1, -1), repeat=3):
        M = np.zeros((3, 3))
        for i in range(3): M[i, perm[i]] = sg[i]
        if np.linalg.det(M) > 0: CUBE_ROT.append(M)
BASES = [rot_to(np.array([1, 1, 1.]), np.array([0, 0, 1.])), np.eye(3)]
def planes(P): h = ConvexHull(P); return h.equations
def poly(eqs, inner):
    try: return np.unique(np.round(HalfspaceIntersection(eqs, inner).intersections, 9), axis=0)
    except Exception: return None
def interior(eqs):
    from scipy.optimize import linprog
    A = eqs[:, :3]; b = -eqs[:, 3]; nrm = np.linalg.norm(A, axis=1)
    r = linprog([0, 0, 0, -1], A_ub=np.c_[A, nrm], b_ub=b, bounds=[(None, None)]*3 + [(0, None)])
    return (r.x[:3], r.x[3]) if r.success else (None, 0)
def pieces_outside(P_eq, Q_eq):
    """convex cells of P outside Q: P ∩ (complement of Q) split by Q's planes (standard sequential decomposition)."""
    out = []; acc = list(P_eq)
    for q in Q_eq:
        cell = np.vstack([acc, -q[None, :] * 1])   # beyond plane q:  -(n·x + d) <= 0  ->  n·x + d >= 0
        c, r = interior(np.array(cell))
        if r > 1e-7:
            X = poly(np.array(cell), c)
            if X is not None and len(X) >= 4: out.append(X)
        acc.append(q)                              # stay inside q for the next planes
    return out
def sig(P, mirror=False):
    P = P[ConvexHull(P).vertices]; D = np.linalg.norm(P[:, None] - P[None], axis=2); return (len(P), tuple(np.round(np.sort(D.ravel()), 5)))
hits, near = [], []; t0 = time.time(); tried = 0
grid = np.arange(-6, 7)/24
for B0 in BASES:
    for R in CUBE_ROT:
        for spin in (0, math.pi/6):
            Rc = rz(spin) @ B0 @ R; Cb = C0 @ Rc.T
            for t in itertools.product(grid, repeat=3):
                C = Cb + np.array(t); tried += 1
                cN, cC = planes(N), planes(C)
                A = pieces_outside(cN, cC); Bp = pieces_outside(cC, cN)
                if len(A) == 0 or len(Bp) == 0: continue
                UA = np.vstack(A); UB = np.vstack(Bp)
                vA = sum(ConvexHull(x).volume for x in A); vB = sum(ConvexHull(x).volume for x in Bp)
                if abs(vA - vB) > 1e-7: continue
                convA = abs(ConvexHull(UA).volume - vA) < 1e-7; convB = abs(ConvexHull(UB).volume - vB) < 1e-7
                if convA and convB:
                    rec = {'t': [float(x) for x in t], 'spin': spin, 'base': BASES.index(B0) if False else int(any(np.allclose(B0, b) for b in BASES[:1])), 'vol_leftover': vA, 'shared_vol': VN - vA}
                    if sig(UA) == sig(UB): hits.append(rec); print('HIT', json.dumps(rec), flush=True)
                    else: near.append(rec)
    print(f'base done: tried {tried}, hits {len(hits)}, near-misses {len(near)}, {time.time() - t0:.0f} s', flush=True)
json.dump({'hits': hits, 'near': near[:500], 'tried': tried}, open('data/common-stage1.json', 'w'), indent=1)
print('stage 1 done', tried, 'placements;', len(hits), 'two-piece hits;', len(near), 'convex near-misses')
