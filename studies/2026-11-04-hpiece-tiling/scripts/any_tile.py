#!/usr/bin/env python3
"""Single-piece tiling search for one-ball-cell pieces (DICTO 4 Nov: the Narcissus + half-RD hybrids). Anchors: every ball / hole position (lattice
offsets 0, 1/3, 2/3) at heights in quarter layers; placements = 24 orientations (6 turns x mirror x z-flip) x (piece corner -> anchor), mod a torus
box of n x n cells and 6 layers (fits ABC and AB). Exact cover by SAT on random samples + piece count; solutions re-checked by overlap volume.
Pieces: covenant (calibration: tiles), twistedcube (needs the brick: must fail alone), hyb0, hyb60. Usage: any_tile.py <piece> <n> <samples>"""
import os, sys, math, itertools, json, time, numpy as np
from scipy.spatial import ConvexHull, Delaunay, HalfspaceIntersection
from scipy.optimize import linprog
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
exec(open(os.path.expanduser('~/study-runs/2026-11-04-dehn-screen/scripts/halfcell.py')).read().split('print("RD"')[0])
name, n, NS = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
Hh = math.sqrt(2/3); s3 = math.sqrt(3)
def rz(t): return np.array([[math.cos(t), -math.sin(t), 0], [math.sin(t), math.cos(t), 0], [0, 0, 1]])
N = np.array([[0,0,0],[0,1/s3,-Hh/2],[0,1/s3,0],[.5,-1/(2*s3),-Hh/2],[.5,-1/(2*s3),0],[.5,1/(2*s3),-Hh],[.5,s3/2,0],[1,0,0],[1,1/s3,-Hh/2],[1,1/s3,0]])
cN = np.array([.5, 1/(2*s3), 0]); Nc = N - cN; T = half(RD, True)
import itertools as _it
_PP = np.array(sorted({tuple(s*v for s, v in zip(sg, p)) for p in _it.permutations((1, 2, 3)) for sg in _it.product((1, -1), repeat=3)}), float)
_a = np.array([1, 1, 1])/math.sqrt(3); _z = np.array([0, 0, 1.]); _v = np.cross(_a, _z); _K = np.array([[0, -_v[2], _v[1]], [_v[2], 0, -_v[0]], [-_v[1], _v[0], 0]]); _R = np.eye(3) + _K + _K @ _K*((1 - _a @ _z)/np.linalg.norm(_v)**2)
_PP = _PP @ _R.T; _hp = ConvexHull(_PP)
def _halfP(top):
    Hs = np.vstack([_hp.equations, [0, 0, -1 if top else 1, 0]]); return HalfspaceIntersection(Hs, np.array([0, 0, 1e-3 if top else -1e-3])).intersections
_TP = np.vstack([_halfP(True), _halfP(False) @ rz(math.pi/3).T]); _TP = _TP*(math.sqrt(2)/2/ConvexHull(_TP).volume)**(1/3)
PIECES = {'twistedB3': _TP, 'covenant': np.vstack([Nc, (Nc*np.array([1, 1, -1])) @ rz(math.pi/3).T]), 'twistedcube': np.vstack([Nc, Nc*np.array([1, 1, -1])]),
          'hyb0': np.vstack([Nc, T]), 'hyb60': np.vstack([Nc, T @ rz(math.pi/3).T])}
P0 = PIECES[name]; P0 = np.unique(np.round(P0[ConvexHull(P0).vertices], 9), axis=0) + cN   # hexagon corners back on lattice points
vol = ConvexHull(P0).volume
def cart(u, v, z): return np.array([u + v/2, v*s3/2, z*Hh])
a1, a2, a3 = cart(n, 0, 0), cart(0, n, 0), cart(0, 0, 6); Lm = np.array([a1, a2, a3]).T; Li = np.linalg.inv(Lm)
def wrap(x): f = Li @ x; f -= np.floor(f + 1e-9); return Lm @ f
anch = np.unique(np.round(np.array([wrap(cart(i + a, j + a, k/4)) for i in range(n) for j in range(n) for a in (0, 1/3, 2/3) for k in range(24)]), 7), axis=0)
OR = []
for k in range(6):
    for mx in (1, -1):
        for fz in (1, -1):
            G = rz(k*math.pi/3) @ np.diag([mx, 1, fz]); Q = P0 @ G.T; key = frozenset(map(tuple, np.round(Q - Q.min(0), 6)))
            if all(key != o[1] for o in OR): OR.append((G, key))
boxv = abs(np.linalg.det(Lm)); npc = boxv/vol
print(f'{name}: corners {len(P0)}, volume {vol:.6f} (ball cell {math.sqrt(2)/2:.6f}), orientations {len(OR)}, anchors {len(anch)}, pieces per box {npc:.4f}', flush=True)
if abs(npc - round(npc)) > 1e-6: print('volume does not divide the box'); sys.exit(0)
npc = int(round(npc)); places = {}
for G, _ in OR:
    Q = P0 @ G.T
    for q in Q:
        for v in anch:
            P = Q + (v - q); c = wrap(P.mean(0)); P = P + (c - P.mean(0)); places.setdefault(tuple(sorted(map(tuple, np.round(P, 5)))), P)
places = list(places.values()); print('placements', len(places), flush=True)
S = (Lm @ np.random.default_rng(1).random((3, NS))).T; imgs = [Lm @ np.array(t) for t in itertools.product((-1, 0, 1), repeat=3)]
cover = [[] for _ in range(NS)]
for pi, P in enumerate(places):
    D = Delaunay(P); c = P.mean(0); R = np.max(np.linalg.norm(P - c, axis=1))
    for sh in imgs:
        Y = S + sh; near = np.where(np.linalg.norm(Y - c, axis=1) <= R + 1e-9)[0]
        if len(near):
            for s in near[D.find_simplex(Y[near]) >= 0]: cover[s].append(pi + 1)
if any(not c for c in cover): print('uncovered sample: UNSAT'); sys.exit(0)
cnf = []; top = len(places)
for c in cover: e = CardEnc.equals(sorted(set(c)), 1, top_id=top, encoding=EncType.seqcounter); top = max(top, e.nv); cnf += e.clauses
cnf += CardEnc.equals(list(range(1, len(places) + 1)), npc, top_id=top, encoding=EncType.seqcounter).clauses
with Cadical153(bootstrap_with=cnf) as Sv: ok = Sv.solve(); model = Sv.get_model() if ok else None
res = {'piece': name, 'n': n, 'samples': NS, 'placements': len(places), 'pieces': npc, 'sat': bool(ok)}
if ok:
    ch = [places[i] for i in range(len(places)) if model[i] > 0]
    np.save(f'data/solution-{name}-n{n}.npy', np.array(ch)); np.save(f'data/box-{name}-n{n}.npy', Lm)
    cop = [P + sh for P in ch for sh in imgs]; cen = [p.mean(0) for p in cop]
    def ivol(A, B):
        H = np.vstack([ConvexHull(A).equations, ConvexHull(B).equations]); nr = np.linalg.norm(H[:, :3], axis=1)
        r = linprog([0, 0, 0, -1], A_ub=np.c_[H[:, :3], nr], b_ub=-H[:, 3], bounds=[(None, None)]*3 + [(0, None)])
        return 0.0 if (not r.success or r.x[3] < 1e-6) else ConvexHull(HalfspaceIntersection(H, r.x[:3]).intersections).volume
    near = [i for i in range(len(cop)) if np.linalg.norm(cen[i] - Lm @ np.array([.5, .5, .5])) < 2.5]
    ov = sum(1 for i, j in itertools.combinations(near, 2) if np.linalg.norm(cen[i] - cen[j]) < 2.2 and ivol(cop[i], cop[j]) > 1e-7)
    X = (Lm @ np.random.default_rng(99).random((3, 20000))).T; cnt = np.zeros(len(X), int)
    for p in cop: cnt += Delaunay(p).find_simplex(X) >= 0
    res.update(verify_overlaps=int(ov), fresh_coverage={int(k): int(v) for k, v in zip(*np.unique(cnt, return_counts=True))})
print(json.dumps(res), flush=True)
