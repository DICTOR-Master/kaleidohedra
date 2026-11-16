#!/usr/bin/env python3
"""Part 4, the Red Queen (120-cell) by corners, solids and walls (DICTO's proposal, 16 Nov 2026). Exact in Q(sqrt5).
The 120-cell Q = the 600 cell centres of the 600-cell P (dual-aligned, in the same sum-zero R^5 where S5 permutes coordinates).
 corners: inscribed 600-cells and 24-cells (counts, disjoint splits; Denney et al. 2020), S5 orbits and their hulls;
 solids:  control pyramids over the 120 dodecahedra; 12 rings of 10 dodecahedra (Hopf, Clifford-parallel decagons; Coxeter,
          Sadoc-Mosseri); caps of Q over the facets of an inscribed 600-cell and of an inscribed 24-cell;
 walls:   plates of the S5-orbit hulls against the 60 mirrors + 300 cross walls (the shared wall system of the walls study).
Also here: which of the 84 covers of P by 12 great decagons are Hopf fibrations (all pairs Clifford parallel = isoclinic).
Usage: s4_redqueen.py out.json"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qlib import *
OUT = sys.argv[1]; C = Checks(); t0 = time.time(); out = {}
P5, X, Y = build_600(); n = len(P5); Pk = {vkey(p): i for i, p in enumerate(P5)}
P4 = [to4(p) for p in P5]; PP = Poly(P4); VP = PP.volume(); a2P = min(sqd(P5[0], q) for q in P5[1:])
Q4 = [tuple(sum((P4[i][c] for i in on), Q5())/4 for c in range(4)) for on, nn, d in PP.facets]
Q5s = [to5(q) for q in Q4]; m = len(Q5s); Qk = {vkey(q): i for i, q in enumerate(Q5s)}
R2 = dot(Q5s[0], Q5s[0]); C(all(dot(q, q) == R2 for q in Q5s), '600 cell centres on one sphere')
QQ = Poly(Q4, '120-cell'); V = QQ.volume()
C([vkey(p) for p in QQ.P] == [vkey(q) for q in Q4], 'hull keeps the corner order')
C(QQ.fvec == (600, 1200, 720, 120) and cell_census(QQ) == {'dodecahedron': 120}, f'120-cell f-vector {QQ.fvec}, 120 dodecahedra')
a2 = min(sqd(to5(QQ.P[a]), to5(QQ.P[b])) for a, b in (tuple(e) for e in QQ.edges))
C(all(sqd(to5(QQ.P[a]), to5(QQ.P[b])) == a2 for a, b in (tuple(e) for e in QQ.edges)), 'all 1200 edges equal')
C(V == Q5(15)/4*(Q5(105) + 47*SQ5)*a2*a2, f'120-cell volume = (15/4)(105 + 47 sqrt5) a^4 exactly (float {float(V):.6f})')
out['vol120'] = str(V); out['vol120_over_vol600P'] = str(V/VP)
ORIG = (Q5(0),)*4

pyr = []
for on, nn, d in QQ.facets:
    sub = Poly([ORIG] + [Q4[i] for i in on]); pyr.append(sub.volume())
C(sum(pyr, Q5()) == V and len({v.key() for v in pyr}) == 1, 'control: 120 dodecahedral pyramids from the centre sum exactly to the 120-cell, all equal')
# cell <-> P corner (cell normal parallel to a P corner)
cellP = []
for on, nn, d in QQ.facets:
    n5 = tuple(list(nn) + [Q5(0)])   # y-normal; compare via 5D: find the P corner whose y-projection is parallel to the centroid of the cell
    cen = tuple(sum((Q4[i][c] for i in on), Q5()) for c in range(4)); cellP.append(next(i for i in range(n) if parallel(P4[i], cen) and dot(P5[i], to5(cen)).sign() > 0))
C(sorted(cellP) == list(range(120)), 'the 120 dodecahedra point at the 120 corners of P (duality)')

# ---------- Hopf decagon covers (both Queens) ----------
Pf = np.array([flt(p) for p in P5]); D10 = set()
for i in range(n):
    for j in range(i + 1, n):
        if sqd(P5[i], P5[j]) == a2P:
            Qm, _ = np.linalg.qr(np.vstack([Pf[i], Pf[j]]).T); pr = Pf @ Qm @ Qm.T
            D10.add(frozenset(np.where(np.linalg.norm(pr - Pf, axis=1) < 1e-6)[0].tolist()))
D10 = sorted(D10, key=sorted)
def covers(sets, universe, limit):
    cols = {u: [k for k, s in enumerate(sets) if u in s] for u in universe}; sol = []; found = []
    def rec(rem, used):
        if len(found) >= limit: return
        if not rem: found.append(list(sol)); return
        u = min(rem, key=lambda x: sum(1 for k in cols[x] if not (sets[k] & used)))
        for k in cols[u]:
            if sets[k] & used: continue
            sol.append(k); rec(rem - sets[k], used | sets[k]); sol.pop()
    rec(frozenset(universe), frozenset()); return found
dcov = covers(D10, range(n), 10**6)
def isoclinic(S, T):
    """exact: the planes of decagons S, T are isoclinic (Clifford parallel): with u, v spanning S, the projections of u and v
    to T have equal length and are orthogonal (using the T-plane Gram matrix)"""
    s = sorted(S); t = sorted(T); u, v = P5[s[0]], next(P5[k] for k in s[1:] if not parallel(P5[k], P5[s[0]]))
    a, b = P5[t[0]], next(P5[k] for k in t[1:] if not parallel(P5[k], P5[t[0]]))
    Gt = [[dot(a, a), dot(a, b)], [dot(a, b), dot(b, b)]]
    def proj_gram(x, y):  # <Px, Py> with P the projection to span(a, b)
        cx = solve(Gt, [dot(a, x), dot(b, x)]); cy = solve(Gt, [dot(a, y), dot(b, y)])
        return cx[0]*(cy[0]*Gt[0][0] + cy[1]*Gt[0][1]) + cx[1]*(cy[0]*Gt[1][0] + cy[1]*Gt[1][1])
    uu, vv, uv = proj_gram(u, u), proj_gram(v, v), proj_gram(u, v)
    # isoclinic iff P restricted to S is a similarity: <Pu,Pu>/<u,u> = <Pv,Pv>/<v,v> and <Pu,Pv> = c <u,v>
    c = uu/dot(u, u)
    return (vv - c*dot(v, v)).iszero() and (uv - c*dot(u, v)).iszero()
hopf = [cv for cv in dcov if all(isoclinic(D10[x], D10[y]) for x, y in itertools.combinations(cv, 2))]
out['decagon_covers'] = len(dcov); out['decagon_covers_hopf'] = len(hopf)
print('decagon covers', len(dcov), 'of which Hopf (pairwise Clifford parallel)', len(hopf), flush=True)
C(len(hopf) > 0, 'some decagon covers are Hopf fibrations')
# rings of 10 dodecahedra over a Hopf cover
cell_of_P = {p: k for k, p in enumerate(cellP)}
fac = [set(on) for on, nn, d in QQ.facets]
ring_ok = True
for D in (D10[k] for k in hopf[0]):
    cyc = [min(D)]
    while len(cyc) < 10:
        cyc.append(next(j for j in D if j not in cyc and sqd(P5[cyc[-1]], P5[j]) == a2P))
    for k in range(10):
        A_, B_ = fac[cell_of_P[cyc[k]]], fac[cell_of_P[cyc[(k + 1) % 10]]]
        ring_ok &= len(A_ & B_) == 5
C(ring_ok, 'over a Hopf cover: 12 rings of 10 dodecahedra, each consecutive pair sharing a pentagon (120 cells, each once)')
out['rings'] = {'rings': 12, 'per_ring': 10, 'ring_fraction': str(Q5(Fr(1, 12)))}

# ---------- inscribed 600-cells and 24-cells ----------
Qf = np.array([flt(q) for q in Q5s]); fk = {tuple(np.round(Qf[i], 6) + 0.0): i for i in range(m)}; Rf = float(R2)
Gq = Qf @ Qf.T
def fclosure(idx, cap_):
    S = set(idx); fr = set(idx)
    while fr:
        new = set()
        for a in S:
            A = Qf[a]
            for b in (S if a in fr else fr):
                c = Qf[b] - 2*(A @ Qf[b])/(A @ A)*A; k = tuple(np.round(c, 6) + 0.0)
                if k not in fk: return None
                j = fk[k]
                if j not in S: new.add(j)
        S |= new; fr = new
        if len(S) > cap_: return None
    return frozenset(S)
c36 = Rf*(1 + 5**.5)/4
gens = []
for p in Pf:
    R = Qf - 2*np.outer(Qf @ p, p)/(p @ p); gens.append(np.array([fk[tuple(np.round(r, 6) + 0.0)] for r in R]))
GQ = group_closure(gens); C(len(GQ) == 14400, f'W(H4) acting on the 120-cell corners: order {len(GQ)}')
def all_images(S):
    im = np.sort(GQ[:, sorted(S)], axis=1); return {frozenset(r.tolist()) for r in np.unique(im, axis=0)}
found600 = set()
for u in [0]:
    W = [w for w in range(m) if abs(Gq[u, w] - c36) < 1e-6]
    for a, b, c in itertools.combinations(W, 3):
        if abs(Gq[a, b] - c36) < 1e-6 and abs(Gq[a, c] - c36) < 1e-6 and abs(Gq[b, c] - c36) < 1e-6:
            S = fclosure([u, a, b, c], 120)
            if S is not None and len(S) == 120: found600.add(S)
per_corner = len(found600)
found600 = set().union(*[all_images(S) for S in found600])
F600 = sorted(found600, key=sorted)
def exact_closed(S):
    L = [Q5s[i] for i in S]; K = {vkey(p) for p in L}
    return all(vkey(vsub(b, vscale(2*dot(a, b)/R2, a))) in K for a in L for b in L)
C(all(exact_closed(S) for S in F600), f'{len(F600)} inscribed 600-cells, each exactly closed under its own reflections')
inc = [sum(i in S for S in F600) for i in range(m)]
out['inscribed_600cells'] = len(F600); out['600cells_per_corner'] = sorted(set(inc))
c600 = covers(F600, range(m), 10**5); out['splits_into_5_disjoint_600cells'] = len(c600)
print('inscribed 600-cells', len(F600), 'per corner', sorted(set(inc)), 'splits into 5 disjoint', len(c600), flush=True)
meet6 = {}
for S, T in itertools.combinations(F600, 2): k = len(S & T); meet6[k] = meet6.get(k, 0) + 1
out['600cell_pair_meetings'] = meet6
H6 = Poly([Q4[i] for i in F600[0]]); C(H6.fvec == (120, 720, 1200, 600), 'an inscribed 600-cell has the 600-cell lattice')
V6 = H6.volume(); out['vol_inscribed600_fraction'] = str(V6/V)
C(5*V6 != V, 'control: five disjoint inscribed 600-cells do not add up to the 120-cell volume (corner split, not a solid split)')
found24 = set()
for u in [0]:
    W = [w for w in range(m) if abs(Gq[u, w] + Rf/2) < 1e-6]
    for a, b, c in itertools.combinations(W, 3):
        if abs(Gq[a, b]) < 1e-6 and abs(Gq[a, c]) < 1e-6 and abs(Gq[b, c]) < 1e-6:
            S = fclosure([u, a, b, c], 24)
            if S is not None and len(S) == 24: found24.add(S)
found24 = set().union(*[all_images(S) for S in found24])
F24 = sorted(found24, key=sorted)
C(all(exact_closed(S) for S in F24), f'{len(F24)} inscribed 24-cells, each exactly closed under its own reflections')
inc24 = [sum(i in S for S in F24) for i in range(m)]
c24 = covers(F24, range(m), 1000)
out['inscribed_24cells'] = len(F24); out['24cells_per_corner'] = sorted(set(inc24)); out['splits_into_25_disjoint_24cells_cap1000'] = len(c24)
in600 = [sum(1 for S in F600 if T <= S) for T in F24]; out['24cells_inside_how_many_600cells'] = sorted(set(in600))
print('inscribed 24-cells', len(F24), 'per corner', sorted(set(inc24)), 'covers (cap 1000)', len(c24), 'each inside', sorted(set(in600)), '600-cells', flush=True)

# ---------- S5 orbits of the 120-cell ----------
perms = list(itertools.permutations(range(5)))
orbs, seen = [], set()
for i, q in enumerate(Q5s):
    if i in seen: continue
    o = sorted({Qk[vkey(tuple(q[s] for s in sg))] for sg in perms}); seen |= set(o); orbs.append(o)
ONE = (Q5(1),)*5
def canon_dir(v):
    i = next(k for k in range(5) if not v[k].iszero()); return vkey(vscale(v[i].inv(), v))
mir = {canon_dir(p) for p in P5}; cross = {canon_dir(q) for q in Q5s}
def plates(poly):
    s = set()
    for g in poly.two:
        pts = [to5(poly.P[i]) for i in sorted(g)[:3]]; s.add(canon_dir(cofactor_normal([pts[0], pts[1], pts[2], ONE])))
    return s
C(plates(QQ) == mir, "control: the 120-cell's 720 pentagons lie on exactly the 60 mirrors")
orows = []; allpl = set(); hv = {}
for o in sorted(orbs, key=lambda o: (len(o), sorted(o))):
    rep = Q5s[o[0]]; xs, blocks, gaps = orbit_pattern(rep)
    Hh = Poly([Q4[i] for i in o]); vol = Hh.volume(); pl = plates(Hh); allpl |= pl
    antip = {Qk[vkey(vneg(Q5s[i]))] for i in o} == set(o)
    row = {'size': len(o), 'antipodal': antip, 'blocks': blocks, 'A4_type': A4NAME.get(tuple(blocks), '?'),
           'coords_shifted': [str(x - xs[-1]) for x in xs], 'fvec': Hh.fvec, 'cells': cell_census(Hh), 'fraction': str(vol/V),
           'fraction_float': float(vol/V), 'plates': len(pl), 'mirrors': len(pl & mir), 'cross': len(pl & cross), 'none': len(pl - mir - cross)}
    orows.append(row); print('Q-ORBIT', json.dumps(row), flush=True)
C(sum(len(o) for o in orbs) == 600, f'S5 orbits of the 120-cell: sizes {sorted(len(o) for o in orbs)}')
out['S5_orbits'] = orows
out['S5_orbit_walls_union'] = {'mirrors': len(allpl & mir), 'cross': len(allpl & cross), 'none': len(allpl - mir - cross)}

# ---------- caps of the 120-cell over an inscribed 600-cell and an inscribed 24-cell ----------
def cap_report(inner, name):
    cs = [c for c in (cap(QQ, nn, d) for on, nn, d in inner.facets) if c is not None]
    s = sum((c.volume() for c in cs), Q5()); exc = inner.volume() + s - V
    inv = {}
    for c in cs: inv.setdefault(dist_invariant([to5(q) for q in c.P]), []).append(c)
    r = {'inner': name, 'caps': len(cs), 'dissection': exc.iszero(), 'overlap': str(exc), 'overlap_float_V': float(exc/V),
         'classes': [{'count': len(v), 'fvec': v[0].fvec, 'cells': cell_census(v[0]), 'fraction': str(v[0].volume()/V),
                      'corners_of_Q': sum(1 for q in v[0].P if vkey(to5(q)) in Qk)} for v in inv.values()]}
    print('CAPS', json.dumps(r, default=str), flush=True)
    C(exc.sign() >= 0, f'{name}: caps cover the rest of the 120-cell (excess >= 0)')
    return r
out['caps_600'] = cap_report(H6, 'inscribed 600-cell')
H24 = Poly([Q4[i] for i in F24[0]]); out['caps_24'] = cap_report(H24, 'inscribed 24-cell')
out['seconds'] = time.time() - t0
json.dump(out, open(OUT, 'w'), indent=1, default=str)
C.final()
