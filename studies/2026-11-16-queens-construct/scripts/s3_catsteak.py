#!/usr/bin/env python3
"""Part 3, DICTO's question (16 Nov 2026): "if this is the steak, where is the cat; if this is the cat, where is the steak":
can the 600-cell be assembled from A (hull of C1 = perms (phi^2,phi^2,phi^2,phi,0)), B (hull of C4 = perms (phi^2,phi^2,1,1,0))
and their partner orbits (C2 = -C1, C5 = -C4, C3)?  Three ways, exact in Q(sqrt5):
 corners: the five S5 orbits are disjoint and cover the 120 corners;
 solids:  the orbit hulls inside the 600-cell: volumes, pairwise and higher intersections, the union (inclusion-exclusion),
          the caps of the 600-cell over the facets of A and of B (dissection or overlap);
 walls:   the central plates (hyperplanes through the centre spanned by 2-faces) of the five hulls, against the 600-cell's
          60 mirrors and 300 cross walls (central hyperplanes parallel to a pair of opposite cells; studies/2026-11-16-600cell-walls).
Controls: P's own plates are all 60 mirrors; an ordinary orbit (t = 3/2) is not all walls; a wrong volume split fails.
Usage: s3_catsteak.py out.json"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qlib import *
OUT = sys.argv[1]; C = Checks(); t0 = time.time(); out = {}
P5, X, Y = build_600(); n = len(P5); Pk = {vkey(p): i for i, p in enumerate(P5)}
P4 = [to4(p) for p in P5]; PP = Poly(P4, '600-cell'); V = PP.volume()
perms = list(itertools.permutations(range(5)))
orbs, seen = {}, set()
Xs = frozenset(Pk[vkey(x)] for x in X); Ys = frozenset(Pk[vkey(y)] for y in Y)
Xm = frozenset(Pk[vkey(vneg(x))] for x in X); Ym = frozenset(Pk[vkey(vneg(y))] for y in Y)
for i, p in enumerate(P5):
    if i in seen: continue
    o = frozenset(Pk[vkey(tuple(p[s] for s in sg))] for sg in perms); seen |= o
    orbs[{Xs: 'C1', Xm: 'C2', Ys: 'C4', Ym: 'C5'}.get(o, 'C3')] = sorted(o)
NM = {'C1': 'A', 'C2': '-A', 'C3': 'C3 hull', 'C4': 'B', 'C5': '-B'}
C(sorted(orbs) == ['C1', 'C2', 'C3', 'C4', 'C5'] and sum(len(o) for o in orbs.values()) == 120 and len(set().union(*map(set, orbs.values()))) == 120,
  'corners: the five S5 orbits are disjoint and cover the 600-cell (A, -A, C3, B, -B)')
H = {k: Poly([P4[i] for i in orbs[k]], NM[k]) for k in orbs}; HV = {k: H[k].volume() for k in H}

# ---------- walls ----------
ONE = (Q5(1),)*5
def canon_dir(v):
    i = next(k for k in range(5) if not v[k].iszero()); return vkey(vscale(v[i].inv(), v))
mir = {canon_dir(p) for p in P5}
cellc = [to5(tuple(sum((P4[i][c] for i in on), Q5()) for c in range(4))) for on, nn, d in PP.facets]
cross = {canon_dir(c) for c in cellc}
C(len(mir) == 60 and len(cross) == 300 and not (mir & cross), '60 mirrors and 300 cross walls, distinct')
def plates(poly):
    out = set()
    for g in poly.two:
        pts = [to5(poly.P[i]) for i in sorted(g)[:3]]
        nrm = cofactor_normal([pts[0], pts[1], pts[2], ONE]); out.add(canon_dir(nrm))
    return out
PLm = plates(PP); C(PLm == mir, "control: the 600-cell's own plates are exactly its 60 mirrors")
pl = {k: plates(H[k]) for k in H}
rows = {}
for k in H:
    rows[k] = {'plates': len(pl[k]), 'mirrors': len(pl[k] & mir), 'cross': len(pl[k] & cross), 'none': len(pl[k] - mir - cross)}
    print('WALLS', NM[k], rows[k], flush=True)
C(rows['C1'] == {'plates': 30, 'mirrors': 30, 'cross': 0, 'none': 0}, 'A: 30 plates, all mirrors (repeat of the walls study)')
C(rows['C4'] == {'plates': 80, 'mirrors': 40, 'cross': 40, 'none': 0}, 'B: 80 plates = 40 mirrors + 40 cross walls (repeat)')
C(pl['C1'] == pl['C2'] and pl['C4'] == pl['C5'], '-A has the plates of A, -B those of B (central plates are unchanged by x -> -x)')
T32 = Q5(Fr(3, 2))
def cen(v): m = sum(v, Q5())/5; return tuple(x - m for x in v)
Ob = uniq([cen(t) for t in itertools.permutations((PHI*PHI, PHI*PHI, PHI*PHI, T32, Q5(0)))])
plb = plates(Poly([to4(p) for p in Ob])); C(len(plb - mir - cross) > 0, f'control: ordinary orbit (phi^2,phi^2,phi^2,3/2,0) has {len(plb - mir - cross)} of {len(plb)} plates in no wall')
AB = pl['C1'] | pl['C4']; ALL = AB | pl['C3']
used = {'A+B': {'mirrors': len(AB & mir), 'cross': len(AB & cross)}, 'A+B+C3': {'mirrors': len(ALL & mir), 'cross': len(ALL & cross)},
        'A and B share': len(pl['C1'] & pl['C4'])}
# S5 x {+-1} orbits of walls
def act(sg, key): v = tuple(Q5(*key[s]) for s in sg); return canon_dir(v)
def worbits(S):
    S = set(S); res = []
    while S:
        w = S.pop(); o = {act(sg, w) for sg in perms}; S -= o; res.append(len(o))
    return sorted(res)
used['mirror orbits under S5'] = worbits(mir); used['cross orbits under S5'] = worbits(cross)
used['A mirrors orbits'] = worbits(pl['C1'] & mir); used['B mirror orbits'] = worbits(pl['C4'] & mir); used['B cross orbits'] = worbits(pl['C4'] & cross)
used['C3 plates'] = rows['C3']; used['C3 mirror orbits'] = worbits(pl['C3'] & mir); used['C3 cross orbits'] = worbits(pl['C3'] & cross)
used['left mirrors (A+B)'] = worbits(mir - AB); used['left cross (A+B)'] = worbits(cross - AB)
used['left mirrors (all five)'] = worbits(mir - ALL); used['left cross (all five)'] = worbits(cross - ALL)
s5mir = {canon_dir(tuple(Q5(1) if c == i else Q5(-1) if c == j else Q5(0) for c in range(5))) for i, j in itertools.combinations(range(5), 2)}
used['the 10 S5 mirrors (x_i = x_j) are H4 mirrors'] = s5mir <= mir
used['A uses the 10 S5 mirrors'] = s5mir <= pl['C1']; used['B uses the 10 S5 mirrors'] = s5mir <= pl['C4']
out['walls'] = {'per_hull': {NM[k]: rows[k] for k in rows}, **used}
print('WALLS-USE', used, flush=True)
C(s5mir <= mir, 'the 10 S5 mirrors are among the 60 H4 mirrors')

# ---------- solids ----------
for k in H:
    C(abs(float(HV[k]) - H[k].float_vol) < 1e-9, f'{NM[k]}: exact volume = qhull volume')
out['hull_volume_fractions'] = {NM[k]: [str(HV[k]/V), float(HV[k]/V)] for k in H}
inter = {}
keys = ['C1', 'C2', 'C3', 'C4', 'C5']
for r in range(1, 6):
    for sub in itertools.combinations(keys, r):
        if r == 1: inter[sub] = HV[sub[0]]; continue
        hs = sum((H[k].halfspaces() for k in sub), [])
        Q = hs_intersect(hs); inter[sub] = Q.volume() if Q is not None else Q5()
        if r == 5: core = Q
union = sum(((Q5(-1) if len(s) % 2 == 0 else Q5(1))*v for s, v in inter.items()), Q5())
out['intersections'] = {'+'.join(NM[k] for k in s): [str(v/V), float(v/V)] for s, v in inter.items()}
out['union_of_five_hulls_fraction'] = [str(union/V), float(union/V)]
out['core_all_five'] = {'fvec': core.fvec, 'cells': cell_census(core), 'fraction': str(inter[tuple(keys)]/V)}
print('UNION fraction', float(union/V), 'core', out['core_all_five'], flush=True)
C(union.sign() > 0 and (union - V).sign() <= 0, 'union of the five hulls lies in the 600-cell')
C(float(sum(HV.values())/V) > 1, 'the five hulls together exceed the 600-cell volume: they overlap (all contain the centre), so they cannot tile it')
# caps of P over A's and B's facets
capres = {}
for k in ['C1', 'C4', 'C3']:
    cs = [c for c in (cap(PP, nn, d) for on, nn, d in H[k].facets) if c is not None]
    s = sum((c.volume() for c in cs), Q5()); exc = HV[k] + s - V
    inv = {}
    for c in cs: inv.setdefault(dist_invariant([to5(q) for q in c.P]), []).append(c)
    capres[NM[k]] = {'caps': len(cs), 'dissection': exc.iszero(), 'overlap': str(exc), 'overlap_float_V': float(exc/V),
                     'classes': [{'count': len(v), 'fvec': v[0].fvec, 'cells': cell_census(v[0]), 'fraction': str(v[0].volume()/V),
                                  'corners_of_P': sum(1 for q in v[0].P if vkey(to5(q)) in Pk)} for v in inv.values()]}
    print('CAPS', NM[k], capres[NM[k]], flush=True)
    C(exc.sign() >= 0, f'{NM[k]}: caps cover P minus the hull (excess >= 0)')
out['caps'] = capres
# a wrong split must fail: A + B + C3 volumes are not V
C(HV['C1'] + HV['C4'] + HV['C3'] != V, 'control: vol A + vol B + vol C3 is not the 600-cell volume')
out['seconds'] = time.time() - t0
json.dump(out, open(OUT, 'w'), indent=1, default=str)
C.final()
