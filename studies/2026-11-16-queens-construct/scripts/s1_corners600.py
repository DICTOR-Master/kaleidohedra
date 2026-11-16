#!/usr/bin/env python3
"""Part 1, the White Queen (600-cell) by corners (DICTO's proposal, 16 Nov 2026: construct/deconstruct the Queens from/into polytopes).
Splits of the 120 corners into corner sets of named polytopes, all exact in Q(sqrt5):
 (a) the five S5 orbits (20+20+20+30+30; Koca, Ozdes Koca, Al-Ajmi 2012) and each orbit's hull (f-vector, cells, volume);
 (b) the 25 inscribed 24-cells, their meeting sizes and the ways to choose 5 disjoint ones (Coxeter; Denney et al. 2020);
 (c) one 24-cell + the snub 24-cell (Gosset 1900; Coxeter, Regular Polytopes 8.4);
 (d) great polygons: 72 decagons, 200 hexagons, 450 squares and covers by disjoint ones (Hopf fibrations);
 (e) layers along a vertex, edge, triangle and cell axis (Coxeter, Regular Polytopes, Table V).
Control: a non-golden twin (t = 3/2 in place of phi) must fail to close into 120 points or to lie on P.
Usage: s1_corners600.py out.json"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qlib import *
OUT = sys.argv[1]; C = Checks(); t0 = time.time(); out = {}
P5, X, Y = build_600(); n = len(P5)
C(n == 120, f'closure of X has 120 points ({n})')
P5, X, Y = build_600(); n = len(P5)
C(n == 120, f'closure of X has 120 points ({n})')
r2 = dot(X[0], X[0]); C(all(dot(p, p) == r2 for p in P5), 'all 120 on one sphere')
Pk = {vkey(p): i for i, p in enumerate(P5)}
C(all(vkey(y) in Pk for y in Y), 'Y = perms (phi^2,phi^2,1,1,0) lies in P exactly, no rescaling')
prof = {}
for q in P5: k = (dot(P5[0], q)/r2).key(); prof[k] = prof.get(k, 0) + 1
C(sorted(prof.values()) == sorted([1, 12, 20, 12, 30, 12, 20, 12, 1]), 'distance profile from a corner 1,12,20,12,30,12,20,12,1')
a2 = min(sqd(P5[0], q) for q in P5[1:]); out['r2'] = str(r2); out['edge2'] = str(a2)
PH3 = PHI*PHI*PHI
C((r2/a2) == PHI*PHI, 'circumradius/edge = phi (600-cell)')
PP = Poly([to4(p) for p in P5], '600-cell')
C(PP.fvec == (120, 720, 1200, 600), f'600-cell f-vector {PP.fvec}')
C(cell_census(PP) == {'tetrahedron': 600}, '600 tetrahedral cells')
V600 = PP.volume(); out['vol600'] = str(V600); out['vol600_over_a4'] = str(V600/(a2*a2))
C(V600 == Q5(25, 0)/4*PH3*a2*a2, f'600-cell volume = 25 phi^3 a^4 / 4 exactly ({V600}, float {float(V600):.6f}, qhull {PP.float_vol:.6f})')
C(abs(float(V600) - PP.float_vol) < 1e-9, 'exact volume = qhull volume')

# ---------- (a) the five S5 orbits ----------
perms = list(itertools.permutations(range(5)))
orbs, seen = [], set()
for i, p in enumerate(P5):
    if i in seen: continue
    o = sorted({Pk[vkey(tuple(p[s] for s in sg))] for sg in perms}); seen |= set(o); orbs.append(o)
C(sorted(len(o) for o in orbs) == [20, 20, 20, 30, 30], f'S5 orbits {sorted(len(o) for o in orbs)}')
Xs = {Pk[vkey(x)] for x in X}; Ys = {Pk[vkey(y)] for y in Y}
Xm = {Pk[vkey(vneg(x))] for x in X}; Ym = {Pk[vkey(vneg(y))] for y in Y}
lab = {}
for o in orbs:
    so = set(o)
    lab[{frozenset(Xs): 'C1', frozenset(Xm): 'C2', frozenset(Ys): 'C4', frozenset(Ym): 'C5'}.get(frozenset(so), 'C3')] = o
C(sorted(lab) == ['C1', 'C2', 'C3', 'C4', 'C5'], 'orbits are X, -X, Y, -Y and one more (C3)')
C({Pk[vkey(vneg(P5[i]))] for i in lab['C3']} == set(lab['C3']), 'C3 is antipodal (C3 = -C3)')
hulls = {}; orbit_rows = []
for k in ['C1', 'C2', 'C3', 'C4', 'C5']:
    o = lab[k]; rep = max((P5[i] for i in o), key=lambda p: tuple(float(x) for x in sorted(p, key=float, reverse=True)))
    xs, blocks, gaps = orbit_pattern(rep)
    # shift so that the smallest coordinate is 0 (orbit up to the centre)
    sh = [x - xs[-1] for x in xs]
    H = Poly([to4(P5[i]) for i in o], k); hulls[k] = H
    e2 = sorted({sqd(to5(H.P[a]), to5(H.P[b])).key() for a, b in (tuple(e) for e in H.edges)})
    v = H.volume()
    row = {'orbit': k, 'size': len(o), 'coords_shifted': [str(x) for x in sh], 'blocks': blocks, 'gaps': [str(g) for g in gaps],
           'A4_type': A4NAME.get(tuple(blocks), '?'), 'uniform_gaps': len({g.key() for g in gaps}) == 1,
           'fvec': H.fvec, 'cells': cell_census(H), 'edge_lengths2': [str(Q5(*kk)) for kk in e2],
           'volume': str(v), 'vol_fraction_of_600': str(v/V600), 'vol_fraction_float': float(v/V600)}
    C(H.euler == 0, f'{k}: Euler f0-f1+f2-f3 = 0 {H.fvec}')
    C(abs(float(v) - H.float_vol) < 1e-9, f'{k}: exact volume = qhull volume')
    C(len(H.P) == len(o), f'{k}: every orbit point is a vertex of its hull')
    orbit_rows.append(row); print('ORBIT', json.dumps(row), flush=True)
out['orbits'] = orbit_rows
C(orbit_rows[0]['A4_type'] == 'truncated 5-cell' and orbit_rows[3]['A4_type'] == 'cantellated 5-cell', 'A is a truncated 5-cell, B a cantellated 5-cell (combinatorially)')
C(orbit_rows[0]['fvec'] == orbit_rows[1]['fvec'] and orbit_rows[3]['fvec'] == orbit_rows[4]['fvec'], 'C2 like C1, C5 like C4')
# nesting: which hull contains which orbit's corners
nest = {}
for a in hulls:
    for b in hulls:
        if a != b: nest[f'{b} in hull {a}'] = sum(hulls[a].contains(q) for q in hulls[b].P)
out['nesting_counts'] = nest; print('NEST', nest)
C(all(v < len(hulls[k.split()[0]].P) for k, v in nest.items()), 'no orbit hull contains another orbit (all corners on one sphere)')

# ---------- control: non-golden twin ----------
T32 = Q5(Fr(3, 2))
def cen(v): m = sum(v, Q5())/5; return tuple(x - m for x in v)
Xbad = uniq([cen(t) for t in itertools.permutations((T32*T32, T32*T32, T32*T32, T32, Q5(0)))])
Pbad = closure(Xbad, cap=400)
C(Pbad is None or len(Pbad) != 120, f'control: t = 3/2 in place of phi does not close into a 120-point 600-cell ({None if Pbad is None else len(Pbad)})')
Ybad = uniq([cen(t) for t in itertools.permutations((PHI*PHI, PHI*PHI, Q5(Fr(6, 5)), Q5(Fr(6, 5)), Q5(0)))])
C(not all(vkey(y) in Pk for y in Ybad), 'control: perms (phi^2,phi^2,6/5,6/5,0) do not lie in P')

# ---------- (b) the 24-cells ----------
Pf = np.array([flt(p) for p in P5]); rf = float(r2)
fk = {tuple(np.round(Pf[i], 6) + 0.0): i for i in range(n)}
def fclosure(idx, Pf, fk, cap):
    S = set(idx); fr = set(idx)
    while fr:
        new = set()
        for a in S | fr:
            A = Pf[a]
            for b in (S if a in fr else fr):
                c = Pf[b] - 2*(A @ Pf[b])/(A @ A)*A; k = tuple(np.round(c, 6) + 0.0)
                if k not in fk: return None
                j = fk[k]
                if j not in S and j not in new: new.add(j)
        S |= new; fr = new
        if len(S) > cap: return None
    return frozenset(S)
def find_24cells(Pf, fk, r2f):
    G = Pf @ Pf.T; found = set()
    for u in range(len(Pf)):
        W = [w for w in range(len(Pf)) if abs(G[u, w] + r2f/2) < 1e-6]
        for a, b, c in itertools.combinations(W, 3):
            if abs(G[a, b]) < 1e-6 and abs(G[a, c]) < 1e-6 and abs(G[b, c]) < 1e-6:
                S = fclosure([u, a, b, c], Pf, fk, 24)
                if S is not None and len(S) == 24: found.add(S)
    return sorted(found, key=sorted)
def exact_24(S, Pts):
    """exact: closed under reflection in its members, inner products of a 24-cell (D4 roots)"""
    L = [Pts[i] for i in S]; K = {vkey(p) for p in L}; rr = dot(L[0], L[0])
    ok = all(vkey(vsub(b, vscale(2*dot(a, b)/rr, a))) in K for a in L for b in L)
    vals = {}
    for b in L: c = (dot(L[0], b)/rr).key(); vals[c] = vals.get(c, 0) + 1
    return ok and sorted(vals.values()) == [1, 1, 6, 8, 8]
T24 = find_24cells(Pf, fk, rf)
C(len(T24) == 25, f'the 600-cell has 25 inscribed 24-cells ({len(T24)})')
C(all(exact_24(S, P5) for S in T24), 'each is exactly a 24-cell (closed under its reflections; profile 1,8,6,8,1)')
inc = {}
for i in range(n): inc[i] = sum(i in S for S in T24)
C(set(inc.values()) == {5}, 'every corner lies in exactly 5 of the 25')
meet = {}
for S, T in itertools.combinations(T24, 2): m = len(S & T); meet[m] = meet.get(m, 0) + 1
out['24cell_pair_meetings'] = meet; print('24-cell pair meetings', meet)
disj = {i: {j for j in range(25) if j != i and not (T24[i] & T24[j])} for i in range(25)}
parts = []
def grow(ch, cand):
    if len(ch) == 5: parts.append(tuple(ch)); return
    for j in sorted(cand):
        if j > ch[-1]: grow(ch + [j], cand & disj[j])
for i in range(25): grow([i], disj[i])
out['disjoint_24cell_quintuples'] = len(parts); print('ways to choose 5 disjoint 24-cells:', len(parts))
C(all(len(set().union(*[T24[j] for j in p])) == 120 for p in parts), 'every 5 pairwise disjoint 24-cells cover all 120 corners')
C(len(parts) > 0, f'number of ways to split the 600-cell into 5 disjoint 24-cells: {len(parts)}')
H24 = Poly([to4(P5[i]) for i in T24[0]], '24-cell')
C(H24.fvec == (24, 96, 96, 24) and cell_census(H24) == {'octahedron': 24}, f'24-cell hull {H24.fvec}')
V24 = H24.volume(); out['vol24_fraction'] = str(V24/V600)
# split per S5 orbit: how does a 24-cell meet the five orbits
spl = sorted({tuple(len(T & set(lab[k])) for k in ['C1', 'C2', 'C3', 'C4', 'C5']) for T in T24})
out['24cell_meets_orbits'] = spl; print('24-cells meet C1..C5 in', spl)

# ---------- (c) 24-cell + snub 24-cell ----------
rest = [i for i in range(n) if i not in T24[0]]
SN = Poly([to4(P5[i]) for i in rest], 'snub 24-cell')
e2s = {sqd(to5(SN.P[a]), to5(SN.P[b])).key() for a, b in (tuple(e) for e in SN.edges)}
C(SN.fvec == (96, 432, 480, 144), f'the other 96 corners: hull f-vector {SN.fvec} = snub 24-cell')
C(cell_census(SN) == {'icosahedron': 24, 'tetrahedron': 120}, f'snub cells {cell_census(SN)}')
C(len(e2s) == 1 and Q5(*list(e2s)[0]) == a2, 'all snub edges equal the 600-cell edge (uniform)')
VS = SN.volume(); out['vol_snub'] = str(VS); out['vol_snub_fraction'] = str(VS/V600)

# ---------- (d) great polygons ----------
G = Pf @ Pf.T
planes = {}
for i in range(n):
    for j in range(i + 1, n):
        if abs(abs(G[i, j]) - rf) < 1e-6: continue
        M = np.vstack([Pf[i], Pf[j]]); Q, _ = np.linalg.qr(M.T); proj = Pf @ Q @ Q.T
        S = frozenset(np.where(np.linalg.norm(proj - Pf, axis=1) < 1e-6)[0].tolist())
        planes.setdefault(S, None)
bysize = {}
for S in planes: bysize.setdefault(len(S), []).append(S)
cnt = {k: len(v) for k, v in sorted(bysize.items())}; out['great_polygons'] = cnt; print('great polygons by corner count', cnt)
C(cnt.get(10) == 72 and cnt.get(6) == 200 and cnt.get(4) == 450, f'72 great decagons, 200 hexagons, 450 squares ({cnt})')
C(all(rank([P5[i] for i in S]) == 2 for S in bysize[10]), 'each decagon exactly planar through the centre')
def covers(sets, universe, limit):
    """exact covers (Algorithm X, Knuth) up to limit"""
    cols = {u: [k for k, s in enumerate(sets) if u in s] for u in universe}; sol = []; found = []
    def rec(rem, used):
        if len(found) >= limit: return
        if not rem: found.append(list(sol)); return
        u = min(rem, key=lambda x: sum(1 for k in cols[x] if not (sets[k] & used)))
        for k in cols[u]:
            if sets[k] & used: continue
            sol.append(k); rec(rem - sets[k], used | sets[k]); sol.pop()
    rec(frozenset(universe), frozenset()); return found
cov = {}
for m, need in ((10, 12), (6, 20), (4, 30)):
    f = covers(bysize[m], range(n), 2000)
    cov[m] = len(f); C(len(f) > 0 and all(len(c) == need for c in f), f'corners split into {need} disjoint great {m}-gons ({len(f)} covers found, cap 2000)')
out['polygon_covers_found_cap2000'] = cov
# Clifford parallel test for the first decagon cover: all pairs at the same angle set (isoclinic)
dec_cover = covers(bysize[10], range(n), 1)[0]
out['decagon_cover_example'] = [sorted(bysize[10][k]) for k in dec_cover]
# count all decagon covers exactly (small)
alld = covers(bysize[10], range(n), 10**6); out['decagon_covers_total'] = len(alld); print('decagon covers (all):', len(alld))
C(len(alld) < 10**6, f'all decagon covers counted: {len(alld)}')

# ---------- (e) layers ----------
def layer_name(pts5):
    if len(pts5) == 1: return 'point'
    if len(pts5) == 2: return 'segment'
    A = np.array([flt(p) for p in pts5]); c = A.mean(0); B = A - c
    U, s, Vt = np.linalg.svd(B); dim = int((s > 1e-7).sum())
    Z = B @ Vt[:dim].T
    if dim < 3: return f'{len(pts5)} points, flat ({dim}D)'
    h = ConvexHull(Z); fac = {}
    for eq, sp in zip(h.equations, h.simplices): fac.setdefault(tuple(np.round(eq, 6) + 0.0), set()).update(sp)
    faces = sorted(len(f) for f in fac.values()); ed = set()
    for f in fac.values():
        f = sorted(f)
        for a, b in itertools.combinations(f, 2):
            mid = (Z[a] + Z[b])/2
            # edge iff a,b on two common facets
            if sum(1 for g in fac.values() if a in g and b in g) >= 2: ed.add((a, b))
    lens = sorted({sqd(pts5[a], pts5[b]).key() for a, b in ed})
    nm3 = {(4, 6, 4, (3,)*4): 'tetrahedron', (6, 12, 8, (3,)*8): 'octahedron', (8, 12, 6, (4,)*6): 'cube', (12, 30, 20, (3,)*20): 'icosahedron',
           (20, 30, 12, (5,)*12): 'dodecahedron', (30, 60, 32, (3,)*20 + (5,)*12): 'icosidodecahedron', (12, 24, 14, (3,)*8 + (4,)*6): 'cuboctahedron',
           (12, 18, 8, (3,)*4 + (6,)*4): 'truncated tetrahedron', (6, 9, 5, (3, 3, 4, 4, 4)): 'triangular prism',
           (24, 36, 14, (4,)*6 + (6,)*8): 'truncated octahedron', (10, 15, 7, (4,)*5 + (5,)*2): 'pentagonal prism',
           (12, 18, 8, (4,)*6 + (6,)*2): 'hexagonal prism', (8, 18, 12, (3,)*12): 'hexagonal bipyramid', (7, 15, 10, (3,)*10): 'pentagonal bipyramid',
           (10, 20, 12, (3,)*10 + (5,)*2): 'pentagonal antiprism', (8, 16, 10, (3,)*8 + (4,)*2): 'square antiprism'}
    key = (len(pts5), len(ed), len(fac), tuple(faces))
    nm = nm3.get(key, f'f=({len(pts5)},{len(ed)},{len(fac)}) faces {dict((k, faces.count(k)) for k in sorted(set(faces)))}')
    return nm + ('' if len(lens) == 1 else f', {len(lens)} edge lengths')
axes = {'vertex': P5[0]}
nb = [j for j in range(n) if sqd(P5[0], P5[j]) == a2]
axes['edge'] = vadd(P5[0], P5[nb[0]])
tri = next((P5[0], P5[a], P5[b]) for a, b in itertools.combinations(nb, 2) if sqd(P5[a], P5[b]) == a2)
axes['triangle'] = vadd(vadd(tri[0], tri[1]), tri[2])
cell0 = PP.facets[0][0]; axes['cell'] = to5(tuple(sum((PP.P[i][c] for i in cell0), Q5()) for c in range(4)))
layers = {}
for nm, ax in axes.items():
    lv = {}
    for i, p in enumerate(P5): lv.setdefault(dot(p, ax).key(), []).append(i)
    ks = sorted(lv, key=lambda k: -float(Q5(*k)))
    layers[nm] = [(len(lv[k]), layer_name([P5[i] for i in lv[k]])) for k in ks]
    C(sum(len(lv[k]) for k in ks) == 120, f'{nm} axis: layers sum to 120')
    print('LAYERS', nm, layers[nm], flush=True)
out['layers'] = layers
C([c for c, _ in layers['vertex']] == [1, 12, 20, 12, 30, 12, 20, 12, 1], 'vertex-first layers 1,12,20,12,30,12,20,12,1')
C([nm for _, nm in layers['vertex']][1:5] == ['icosahedron', 'dodecahedron', 'icosahedron', 'icosidodecahedron'], 'vertex-first layers icosahedron, dodecahedron, icosahedron, icosidodecahedron')
out['seconds'] = time.time() - t0
json.dump(out, open(OUT, 'w'), indent=1, default=str)
C.final()
