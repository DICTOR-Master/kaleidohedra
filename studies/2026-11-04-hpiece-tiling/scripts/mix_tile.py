#!/usr/bin/env python3
"""Do the two halves mix? (DICTO 4 Nov.) Pieces: H = the RD/TRD half (hexagon centred on a ball) and N = Narcissus (hexagon centred on a hole,
balls at its corners); both volume √2/4. Tile a torus box (n x n cells, 6 layers) by copies of H and N in all orientations, anchored on ball/hole
positions at quarter-layer heights; exact cover by SAT on samples, with at least MIN copies of EACH kind. Then classify every hexagon contact
(which two kinds meet on a hexagon, straight or turned) and count the pairings; re-check by overlap volume and fresh points.
Usage: mix_tile.py <n> <samples> <min_each>"""
import os, sys, math, itertools, json, numpy as np
from scipy.spatial import ConvexHull, Delaunay, HalfspaceIntersection
from scipy.optimize import linprog
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
exec(open(os.path.expanduser('~/study-runs/2026-11-04-dehn-screen/scripts/halfcell.py')).read().split('print("RD"')[0])
n, NS, MIN = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
Hh = math.sqrt(2/3); s3 = math.sqrt(3)
def rz(t): return np.array([[math.cos(t), -math.sin(t), 0], [math.sin(t), math.cos(t), 0], [0, 0, 1]])
Nn = np.array([[0,0,0],[0,1/s3,-Hh/2],[0,1/s3,0],[.5,-1/(2*s3),-Hh/2],[.5,-1/(2*s3),0],[.5,1/(2*s3),-Hh],[.5,s3/2,0],[1,0,0],[1,1/s3,-Hh/2],[1,1/s3,0]])
Hc = half(RD, False)                       # hexagon at z = 0 centred on the ball at the origin, body below
KINDS = {'N': Nn, 'H': np.unique(np.round(Hc[ConvexHull(Hc).vertices], 9), axis=0)}
def cart(u, v, z): return np.array([u + v/2, v*s3/2, z*Hh])
Lm = np.array([cart(n, 0, 0), cart(0, n, 0), cart(0, 0, 6)]).T; Li = np.linalg.inv(Lm)
def wrap(x): f = Li @ x; f -= np.floor(f + 1e-9); return Lm @ f
anch = np.unique(np.round(np.array([wrap(cart(i + a, j + a, k/4)) for i in range(n) for j in range(n) for a in (0, 1/3, 2/3) for k in range(24)]), 7), axis=0)
places, kind_of, hexc = {}, [], []
for kn, P0 in KINDS.items():
    hx = P0[np.abs(P0[:, 2]) < 1e-9].mean(0)   # hexagon centre (z = 0 face)
    seen = []
    for k in range(6):
        for mx in (1, -1):
            for fz in (1, -1):
                G = rz(k*math.pi/3) @ np.diag([mx, 1, fz]); Q = P0 @ G.T; key = frozenset(map(tuple, np.round(Q - Q.min(0), 6)))
                if key in seen: continue
                seen.append(key)
                for q in Q:
                    for v in anch:
                        P = Q + (v - q); c = wrap(P.mean(0)); d = c - P.mean(0); P = P + d
                        kk = tuple(sorted(map(tuple, np.round(P, 5))))
                        if kk not in places: places[kk] = (P, kn, G @ hx + (v - q) + d, G)
places = list(places.values()); print('placements', len(places), '(N', sum(1 for p in places if p[1] == 'N'), ', H', sum(1 for p in places if p[1] == 'H'), ')', flush=True)
vol = ConvexHull(KINDS['N']).volume; npc = int(round(abs(np.linalg.det(Lm))/vol)); print('pieces per box', npc, flush=True)
S = (Lm @ np.random.default_rng(1).random((3, NS))).T; imgs = [Lm @ np.array(t) for t in itertools.product((-1, 0, 1), repeat=3)]
cover = [[] for _ in range(NS)]
for pi, (P, kn, hc, G) in enumerate(places):
    D = Delaunay(P); c = P.mean(0); R = np.max(np.linalg.norm(P - c, axis=1))
    for sh in imgs:
        Y = S + sh; near = np.where(np.linalg.norm(Y - c, axis=1) <= R + 1e-9)[0]
        if len(near):
            for s in near[D.find_simplex(Y[near]) >= 0]: cover[s].append(pi + 1)
if any(not c for c in cover): print('uncovered: UNSAT'); sys.exit(0)
cnf = []; top = len(places)
for c in cover: e = CardEnc.equals(sorted(set(c)), 1, top_id=top, encoding=EncType.seqcounter); top = max(top, e.nv); cnf += e.clauses
e = CardEnc.equals(list(range(1, len(places) + 1)), npc, top_id=top, encoding=EncType.seqcounter); top = max(top, e.nv); cnf += e.clauses
for kn in ('N', 'H'):
    lits = [i + 1 for i, p in enumerate(places) if p[1] == kn]; e = CardEnc.atleast(lits, MIN, top_id=top, encoding=EncType.seqcounter); top = max(top, e.nv); cnf += e.clauses
with Cadical153(bootstrap_with=cnf) as Sv: ok = Sv.solve(); model = Sv.get_model() if ok else None
res = {'n': n, 'samples': NS, 'min_each': MIN, 'sat': bool(ok)}
if ok:
    ch = [places[i] for i in range(len(places)) if model[i] > 0]
    res['counts'] = {k: sum(1 for p in ch if p[1] == k) for k in ('N', 'H')}
    # hexagon contacts: two chosen pieces whose hexagon centres coincide (mod box)
    pair = {}
    for (Pa, ka, ha, Ga), (Pb, kb, hb, Gb) in itertools.combinations(ch, 2):
        if np.linalg.norm(wrap(ha - hb + Lm @ np.array([.5, .5, .5])) - Lm @ np.array([.5, .5, .5])) < 1e-6:
            # turned or straight: compare the two pieces' in-plane orientation of their hexagon corners after mirroring one through the hexagon plane
            Ha = Pa[np.abs(Pa[:, 2] - ha[2]) < 1e-6]; Hb = Pb[np.abs(Pb[:, 2] - hb[2]) < 1e-6]
            key = '+'.join(sorted((ka, kb)))
            pair[key] = pair.get(key, 0) + 1
    res['hexagon_pairings'] = pair
    cop = [p[0] + sh for p in ch for sh in imgs]; cen = [p.mean(0) for p in cop]
    def ivol(A, B):
        H = np.vstack([ConvexHull(A).equations, ConvexHull(B).equations]); nr = np.linalg.norm(H[:, :3], axis=1)
        r = linprog([0, 0, 0, -1], A_ub=np.c_[H[:, :3], nr], b_ub=-H[:, 3], bounds=[(None, None)]*3 + [(0, None)])
        return 0.0 if (not r.success or r.x[3] < 1e-6) else ConvexHull(HalfspaceIntersection(H, r.x[:3]).intersections).volume
    mid = Lm @ np.array([.5, .5, .5]); near = [i for i in range(len(cop)) if np.linalg.norm(cen[i] - mid) < 2.5]
    res['verify_overlaps'] = int(sum(1 for i, j in itertools.combinations(near, 2) if np.linalg.norm(cen[i] - cen[j]) < 2.2 and ivol(cop[i], cop[j]) > 1e-7))
    X = (Lm @ np.random.default_rng(99).random((3, 20000))).T; cnt = np.zeros(len(X), int)
    for p in cop: cnt += Delaunay(p).find_simplex(X) >= 0
    res['fresh_coverage'] = {int(k): int(v) for k, v in zip(*np.unique(cnt, return_counts=True))}
print(json.dumps(res), flush=True)
