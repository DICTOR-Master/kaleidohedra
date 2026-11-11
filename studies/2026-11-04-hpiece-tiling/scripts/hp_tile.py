#!/usr/bin/env python3
"""Does the HexOct tetrahedral h-piece tile space ALONE for 5/24 <= λ < 3/8 (both necessary tests pass there)? DICTO 4 Nov.
Placements: the piece in the 24 orientations (triangular-lattice point group x z-flip, about the ball), translated so that one of its corners lands on a
corner of the HexOct h-tiling (AB) — finite set modulo a torus box (n x n cells, 2 layers). Exact cover by SAT over random sample points (each covered
exactly once) plus the piece count = box volume / piece volume. Any solution is re-checked with real polytopes (overlaps, coverage).
Calibrations: Narcissus (λ = 3/8) must tile; the c-tile tetrahedral piece at λ = 1/4 (Dehn nonzero, exact_dehn.py) must fail.
Usage: hp_tile.py <h|c> <λ> <n> <samples>"""
import os, sys, math, itertools, json, time, numpy as np
from fractions import Fraction as Fr
from scipy.spatial import ConvexHull, Delaunay
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
sys.path.insert(0, os.path.expanduser('~/study-runs/2026-11-04-tetra-sweep/scripts/_lib')); import methods as M
HEX = os.path.expanduser('~/work/hexoct-scripts'); sys.path.insert(0, HEX); here = os.getcwd(); os.chdir(HEX)
import tiles as Tl
os.chdir(here)
kind, lam, n, NS = sys.argv[1], Fr(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
Hh = math.sqrt(2/3); s3 = math.sqrt(3)
def cart(p): return np.array([float(p[0]) + float(p[1])/2, float(p[1])*s3/2, float(p[2])*Hh])
word, L = ('AB', 0) if kind == 'h' else ('ABC', 1)
os.chdir(HEX); pcs, _ = Tl.tile(word, L, lam); os.chdir(here)
piece = next(np.unique(np.round(np.array([cart(p) for p in P]), 10), axis=0) for k, up, s_, P, J in pcs if k == 'tet')
vol = ConvexHull(piece).volume
# reference corners: all corners of all pieces of the tiling of the AB (or ABC) stacking in one period, shifted by lattice
period = len(word)
ref = []
for LL in range(period):
    os.chdir(HEX); pp, _ = Tl.tile(word, LL, lam); os.chdir(here)
    ball = cart((*Tl.POS[word[LL]], LL))
    for k, up, s_, P, J in pp: ref += [cart(p) + ball for p in P]
a1, a2, a3 = cart((n, 0, 0)), cart((0, n, 0)), cart((0, 0, period))
Lm = np.array([a1, a2, a3]).T; Li = np.linalg.inv(Lm)
def wrap(x): f = Li @ x; f -= np.floor(f + 1e-9); return Lm @ f
refw = np.unique(np.round(np.array([wrap(cart((i, j, 0)) + r) for r in ref for i in range(n) for j in range(n)]), 7), axis=0)
# orientations: rotations by k·60° about z, mirror x -> -x, flip z
def rz(t): return np.array([[math.cos(t), -math.sin(t), 0], [math.sin(t), math.cos(t), 0], [0, 0, 1]])
OR = []
for k in range(6):
    for mx in (1, -1):
        for fz in (1, -1):
            G = rz(k*math.pi/3) @ np.diag([mx, 1, fz])
            Q = piece @ G.T; key = frozenset(map(tuple, np.round(Q - Q.min(0), 6)))
            if all(key != o[1] for o in OR): OR.append((G, key))
print(f'{kind}-piece λ={lam}: corners {len(piece)}, volume {vol:.6f}, distinct orientations {len(OR)}, reference corners {len(refw)}', flush=True)
box_vol = abs(np.linalg.det(Lm)); npieces = box_vol/vol; print('pieces per box', round(npieces, 6), flush=True)
if abs(npieces - round(npieces)) > 1e-6: print('volume does not divide the box: UNSAT trivially'); sys.exit(0)
npieces = int(round(npieces))
places = {}
for G, _ in OR:
    Q = piece @ G.T
    for q in Q:
        for v in refw:
            P = Q + (v - q); c = wrap(P.mean(0)); P = P + (c - P.mean(0)); key = tuple(np.round(c, 5)) + (id(G) % 997,)
            k2 = tuple(sorted(map(tuple, np.round(P - c, 5)))) + tuple(np.round(c, 5))
            places.setdefault(k2, P)
places = list(places.values()); print('candidate placements', len(places), flush=True)
rng = np.random.default_rng(1); S = (Lm @ rng.random((3, NS))).T
imgs = [Lm @ np.array(t) for t in itertools.product((-1, 0, 1), repeat=3)]
cover = [[] for _ in range(NS)]; t0 = time.time()
for pi, P in enumerate(places):
    D = Delaunay(P); c = P.mean(0); R = np.max(np.linalg.norm(P - c, axis=1))
    for sh in imgs:
        Y = S + sh; near = np.where(np.linalg.norm(Y - c, axis=1) <= R + 1e-9)[0]
        if len(near): hit = near[D.find_simplex(Y[near]) >= 0]
        else: continue
        for s in hit: cover[s].append(pi + 1)
print(f'coverage built {time.time() - t0:.0f} s; uncovered samples {sum(1 for c in cover if not c)}', flush=True)
if any(not c for c in cover): print('some sample point cannot be covered: UNSAT'); json.dump({'kind': kind, 'lam': str(lam), 'n': n, 'result': 'UNSAT (uncovered point)'}, open(f'data/hp-{kind}-{sys.argv[2].replace("/", "_")}-n{n}.json', 'w')); sys.exit(0)
cnf = []; top = len(places)
for c in cover:
    e = CardEnc.equals(sorted(set(c)), 1, top_id=top, encoding=EncType.seqcounter); top = max(top, e.nv); cnf += e.clauses
e = CardEnc.equals(list(range(1, len(places) + 1)), npieces, top_id=top, encoding=EncType.seqcounter); cnf += e.clauses
with Cadical153(bootstrap_with=cnf) as Sv:
    ok = Sv.solve(); model = Sv.get_model() if ok else None
res = {'kind': kind, 'lam': str(lam), 'n': n, 'samples': NS, 'placements': len(places), 'pieces': npieces, 'sat': bool(ok)}
if ok:
    chosen = [places[i] for i in range(len(places)) if model[i] > 0]
    cop = [P + sh for P in chosen for sh in imgs]; cen = [p.mean(0) for p in cop]
    from scipy.spatial import HalfspaceIntersection
    from scipy.optimize import linprog
    def ivol(A, B):
        H = np.vstack([ConvexHull(A).equations, ConvexHull(B).equations]); nrm = np.linalg.norm(H[:, :3], axis=1)
        r = linprog([0, 0, 0, -1], A_ub=np.c_[H[:, :3], nrm], b_ub=-H[:, 3], bounds=[(None, None)]*3 + [(0, None)])
        if not r.success or r.x[3] < 1e-6: return 0.0
        return ConvexHull(HalfspaceIntersection(H, r.x[:3]).intersections).volume
    ov = sum(1 for i, j in itertools.combinations(range(len(cop)), 2) if np.linalg.norm(cen[i] - cen[j]) < 2.5 and M.overlap(cop[i], cop[j]) and ivol(cop[i], cop[j]) > 1e-7)
    X = (Lm @ np.random.default_rng(7).random((3, 3000))).T; cnt = np.zeros(len(X), int)
    for p in cop: cnt += Delaunay(p).find_simplex(X) >= 0
    res.update(verify_overlaps=int(ov), verify_coverage={int(k): int(v) for k, v in zip(*np.unique(cnt, return_counts=True))}, chosen=len(chosen))
print(json.dumps(res), flush=True); json.dump(res, open(f'data/hp-{kind}-{sys.argv[2].replace("/", "_")}-n{n}.json', 'w'))
