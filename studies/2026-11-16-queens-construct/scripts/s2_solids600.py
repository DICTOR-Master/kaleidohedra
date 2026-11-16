#!/usr/bin/env python3
"""Part 2, the White Queen (600-cell) by solids (DICTO's proposal, 16 Nov 2026). Exact in Q(sqrt5).
 (a) control: 600 pyramids from the centre over the cells; a wrong split (24 icosahedral pyramids with apex at the centre) must fail;
 (b) snub 24-cell + 24 icosahedral pyramids (the 600-cell less one inscribed 24-cell's corners; Gosset 1900, Coxeter 8.4);
 (c) grand antiprism (Conway-Guy 1965) and the pieces of its complement;
 (d) the 20 rings of 30 tetrahedra (Boerdijk-Coxeter helices; Coxeter 1985, Sadoc 2001);
 (e) caps of the 600-cell over the facets of an inscribed 24-cell.
Certificate used for caps: the caps over the facets of an inner convex polytope I cover P minus I, so vol(P) = vol(I) + sum of
caps exactly iff the caps meet only in their boundaries (a dissection); a larger sum measures the overlap.
Usage: s2_solids600.py out.json"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qlib import *
OUT = sys.argv[1]; C = Checks(); t0 = time.time(); out = {}
P5, X, Y = build_600(); n = len(P5); Pk = {vkey(p): i for i, p in enumerate(P5)}
r2 = dot(P5[0], P5[0]); a2 = min(sqd(P5[0], q) for q in P5[1:])
P4 = [to4(p) for p in P5]
PP = Poly(P4, '600-cell'); V = PP.volume()
C([vkey(p) for p in PP.P] == [vkey(p) for p in P4], 'hull keeps the corner order')
G = weyl_perms(P5); C(len(G) == 14400, f'W(H4) as corner permutations: order {len(G)}')
ORIG = (Q5(0),)*4
def piece_row(name, polys, total=None):
    vols = [p.volume() for p in polys]; s = sum(vols, Q5())
    inv = {}
    for p in polys: inv.setdefault(dist_invariant([to5(q) for q in p.P]), []).append(p)
    classes = [{'count': len(v), 'fvec': v[0].fvec, 'cells': cell_census(v[0]), 'volume': str(v[0].volume()),
                'vol_fraction': str(v[0].volume()/V)} for v in inv.values()]
    return s, {'name': name, 'pieces': len(polys), 'classes_by_distance_multiset': classes, 'sum': str(s)}
def caps_of(inner):
    cs = []
    for on, nn, d in inner.facets:
        c = cap(PP, nn, d)
        if c is not None: cs.append(c)
    return cs

# (a) pyramids over cells, from the centre
pv = [vol_simplex([ORIG] + [P4[i] for i in on]) for on, nn, d in PP.facets]
C(sum(pv, Q5()) == V, 'control: 600 cell pyramids from the centre sum exactly to the 600-cell')
C(len({v.key() for v in pv}) == 1, 'all 600 cell pyramids have one volume (V/600)')
out['a_pyramids'] = {'pieces': 600, 'each': str(pv[0]), 'fraction': str(pv[0]/V)}

# 24-cell (a D4 sub-root system: closure of a corner and three mutually orthogonal corners at 120 degrees)
u = 0; W = [j for j in range(n) if dot(P5[u], P5[j]) == -r2/2]
abc = next(t for t in itertools.combinations(W, 3) if all(dot(P5[x], P5[y]).iszero() for x, y in itertools.combinations(t, 2)))
T24 = sorted(Pk[vkey(p)] for p in closure([P5[u]] + [P5[x] for x in abc], cap=200))
C(len(T24) == 24, f'inscribed 24-cell: {len(T24)} corners')
H24 = Poly([P4[i] for i in T24]); V24 = H24.volume()
# (b) snub 24-cell + icosahedral pyramids
SN = Poly([P4[i] for i in range(n) if i not in T24]); VS = SN.volume()
caps = caps_of(SN)
s, row = piece_row('icosahedral pyramids on the snub 24-cell', caps)
C(len(caps) == 24 and all(c.fvec[0] == 13 for c in caps), f'snub 24-cell: {len(caps)} caps, each with 13 corners (icosahedral pyramid)')
C(all(cell_census(c) == {'icosahedron': 1, 'tetrahedron': 20} for c in caps), 'each cap = an icosahedral pyramid (icosahedron + 20 tetrahedra)')
C(VS + s == V, 'snub 24-cell + 24 icosahedral pyramids = 600-cell, volumes exact')
apex_ok = all(any(vkey(q) == vkey(P4[i]) for q in c.P for i in T24) for c in caps)
C(apex_ok, 'each pyramid apex is a corner of the removed 24-cell')
C(len(row['classes_by_distance_multiset']) == 1, 'the 24 pyramids are one class')
# wrong split control: icosahedral pyramids with apex at the centre
bad = sum((Poly([ORIG] + [q for q in c.P if not any(vkey(q) == vkey(P4[i]) for i in T24)]).volume() for c in caps), Q5())
C(VS + bad != V, 'control: the same split with the apex at the centre fails the volume sum')
out['b_snub'] = {'snub_volume': str(VS), 'snub_fraction': str(VS/V), 'pyramid': row, 'pyramid_fraction_each': str(caps[0].volume()/V)}
# also P around the 24-cell itself
caps24 = caps_of(H24); s24, row24 = piece_row('caps of P over the 24-cell facets', caps24)
C(len(caps24) == 24, f'24 caps over the 24-cell octahedra ({len(caps24)})')
out['e_caps_over_24cell'] = row24; out['e_caps_over_24cell']['overlap'] = str(V24 + s24 - V)
out['e_caps_over_24cell']['dissection'] = (V24 + s24 == V)
print('caps over 24-cell: dissection', V24 + s24 == V, 'classes', row24['classes_by_distance_multiset'], flush=True)

# (c) grand antiprism
nb0 = next(j for j in range(n) if sqd(P5[0], P5[j]) == a2)
D1 = [j for j in range(n) if rank([P5[0], P5[nb0], P5[j]]) == 2]
D2 = [j for j in range(n) if dot(P5[j], P5[0]).iszero() and dot(P5[j], P5[nb0]).iszero()]
C(len(D1) == 10 and len(D2) == 10, f'two completely orthogonal great decagons ({len(D1)}, {len(D2)})')
GA = Poly([P4[i] for i in range(n) if i not in D1 + D2]); VGA = GA.volume()
C(GA.fvec == (100, 500, 720, 320), f'grand antiprism f-vector {GA.fvec}')
C(cell_census(GA) == {'pentagonal antiprism': 20, 'tetrahedron': 300}, f'grand antiprism cells {cell_census(GA)}')
gacaps = caps_of(GA); sg, rowg = piece_row('caps of P over the grand antiprism facets', gacaps)
C(len(gacaps) == 20, f'20 caps (over the pentagonal antiprisms; tetrahedral facets are 600-cell cells): {len(gacaps)}')
over = VGA + sg - V
C(over.sign() > 0, f'the 20 caps (icosahedral pyramids) overlap: excess {over} = {float(over/V):.6f} V')
# pieces: pentagonal-antiprism pyramids and edge joins
pa_pyr, joins = [], []
for D in (D1, D2):
    # order the decagon cyclically
    cyc = [D[0]]
    while len(cyc) < 10:
        nxt = [j for j in D if sqd(P5[cyc[-1]], P5[j]) == a2 and j not in cyc]; cyc.append(nxt[0])
    for k in range(10):
        v, w, uprev = cyc[k], cyc[(k + 1) % 10], cyc[k - 1]
        link = [j for j in range(n) if sqd(P5[v], P5[j]) == a2]
        pa = [j for j in link if j not in (w, uprev)]
        pent = [j for j in link if sqd(P5[w], P5[j]) == a2]
        C(len(pa) == 10 and len(pent) == 5, 'link of a ring corner: pentagonal antiprism + 2 poles; edge link a pentagon') if k == 0 else None
        pa_pyr.append(Poly([P4[v]] + [P4[j] for j in pa])); joins.append(Poly([P4[v], P4[w]] + [P4[j] for j in pent]))
s1_, r1_ = piece_row('pentagonal antiprism pyramids', pa_pyr); s2_, r2_ = piece_row('edge joins (segment * pentagon)', joins)
C(VGA + s1_ + s2_ == V, 'grand antiprism + 20 pentagonal-antiprism pyramids + 20 edge joins = 600-cell, volumes exact')
C(all(c.volume() == pa_pyr[0].volume() + joins[0].volume()*2 for c in gacaps), 'each icosahedral cap = its antiprism pyramid + 2 edge joins (volume), so the pieces cover the caps')
C(over == s2_, 'cap overlap = the 20 edge joins, each counted twice')
out['c_grand_antiprism'] = {'GA_volume': str(VGA), 'GA_fraction': str(VGA/V), 'caps': rowg, 'cap_overlap': str(over),
                            'pa_pyramids': r1_, 'edge_joins': r2_}
print('GA', out['c_grand_antiprism'], flush=True)

# (d) rings of 30 tetrahedra
cells = [frozenset(on) for on, nn, d in PP.facets]; cid = {c: k for k, c in enumerate(cells)}
tri = {}
for k, c in enumerate(cells):
    for t in itertools.combinations(sorted(c), 3): tri.setdefault(frozenset(t), []).append(k)
C(all(len(v) == 2 for v in tri.values()) and len(tri) == 1200, 'each triangle in exactly 2 cells')
helices = {}
for c in cells:
    for o in itertools.permutations(sorted(c)):
        seq = list(o); cs = [cid[c]]
        for step in range(200):
            last = frozenset(seq[-3:]); cur = cid[frozenset(seq[-4:])]
            k = [x for x in tri[last] if x != cur][0]; e = next(iter(cells[k] - last))
            seq.append(e)
            if seq[-4:] == list(o): break
            cs.append(k)
        helices.setdefault(frozenset(cs), len(cs))
lens = {}
for h, L in helices.items(): lens[len(h)] = lens.get(len(h), 0) + 1
C(set(lens) == {30}, f'every face-to-face chain (Boerdijk-Coxeter helix) closes after 30 tetrahedra: {lens}')
H = list(helices)
C(len(H) == 600*12//30, f'{len(H)} rings (600 cells x 12 helix directions / 30)')
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
rc = covers(H, range(600), 2000)
C(len(rc) > 0 and all(len(c) == 20 for c in rc), f'the 600 cells split into 20 disjoint rings of 30: {len(rc)} ways (cap 2000)')
out['d_rings'] = {'rings': len(H), 'covers_by_20_rings': len(rc)}
ringverts = [frozenset().union(*[cells[k] for k in H[j]]) for j in rc[0]]
C(all(len(r) == 30 for r in ringverts), 'each ring has 30 corners')
C(len({canon_set(G, sorted(r)) for r in ringverts}) == 1, 'the 20 rings of a split are congruent (one W(H4) orbit)')
C(sum((pv[k] for j in rc[0] for k in H[j]), Q5()) == V, 'ring pyramids (30 cells each, from the centre) sum to the 600-cell; each = V/20')
# rings: Clifford parallel?  ring axis = the decagons wholly inside the ring's corners
Pf = np.array([flt(p) for p in P5]); D10 = set()
for i in range(n):
    for j in range(i + 1, n):
        if sqd(P5[i], P5[j]) == a2:
            Qm, _ = np.linalg.qr(np.vstack([Pf[i], Pf[j]]).T); pr = Pf @ Qm @ Qm.T
            D10.add(frozenset(np.where(np.linalg.norm(pr - Pf, axis=1) < 1e-6)[0].tolist()))
C(len(D10) == 72 and all(rank([P5[k] for k in D]) == 2 for D in D10), '72 great decagons (exact planarity)')
indec = [sum(1 for D in D10 if D <= r) for r in ringverts]
out['d_rings']['decagons_inside_each_ring'] = indec
print('decagons inside each ring', indec, flush=True)
out['seconds'] = time.time() - t0
json.dump(out, open(OUT, 'w'), indent=1, default=str)
C.final()
