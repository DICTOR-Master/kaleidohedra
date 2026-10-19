# The Penrose-core kit's boundary pieces at twin planes, exact in Q(sqrt5) (DICTO 2026-10-20; float run gyr_boundary.py).
# Same construction: every octet edge is shared by two octahedra; its middle piece = H minus both OGs, H = hull of the two OGs' five-fold
# stars nearest the edge (M0 when the OGs face by inversion, Mg at a twin-plane edge). Caps (6 vertex regions per octahedron) and
# tetrahedra are notched by every middle piece. All by convex pieces:
#   vol M = vol H - vol(H & OG_a) - vol(H & OG_b);  notch of a convex region P by M = vol(P & H) - vol(P & H & OG_a) - vol(P & H & OG_b)
# Checks (exact): octet run gives #37's values; middle pieces pairwise disjoint and outside every other OG; the origin octahedron and
# one cell sum exactly; the boundary pieces' volumes for the single twin plane equal those of the gyrated octet.
# Stackings round layer 0 (octahedra centred on R(a,b,c), a+b+c = 0): octet, single (one twin plane x+y+z = R), gyrated (A B A B).
import os, sys, json, itertools, numpy as np
ME = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(ME, '..', '2026-10-18-ocd-octet', 'scripts'))
from q5 import *
from exactpoly import planes_of, intersect, volume
ok = lambda c, m: print(('PASS ' if c else 'FAIL ') + m, flush=True)
qstr = lambda x: f'{x[0]} + {x[1]}*sqrt5 = {qf(x):.6f}'
D = json.load(open(os.path.join(ME, '..', '2026-10-18-ocd-octet', 'data', 'step1-ocd-exact.json')))
V = [[q(c) for c in v] for v in D['V']]; R = q(D['R']); F = D['faces']
r2 = [dot(v, v) for v in V]; top = max(r2, key=qf); FIVE = [i for i in range(len(V)) if r2[i] == top]
STAR = {i: sorted({j for f in F if i in f for j in f}) for i in FIVE}
OGP = planes_of(V)
QM = lambda rows: [[qr(Fr(x)) for x in row] for row in rows]
EYE = QM([[1, 0, 0], [0, 1, 0], [0, 0, 1]]); MIR = QM([[Fr(1, 3), Fr(-2, 3), Fr(-2, 3)], [Fr(-2, 3), Fr(1, 3), Fr(-2, 3)], [Fr(-2, 3), Fr(-2, 3), Fr(1, 3)]])
ZV = [Z, Z, Z]
mv = lambda A, x: [dot(A[i], x) for i in range(3)]
mm = lambda A, B: [[dot(A[i], [B[k][j] for k in range(3)]) for j in range(3)] for i in range(3)]
def comp(a, b): return (mm(a[0], b[0]), vadd(mv(a[0], b[1]), a[1]))
ap = lambda m, x: vadd(mv(m[0], x), m[1])
def mir(k): return (MIR, [qm(R, qr(Fr(2 * k, 3)))] * 3)
SH = lambda v: (EYE, v)
def pl_ap(m, P):   # planes under x -> A x + t, A orthogonal: n' = A n, d' = d + n'.t
    out = []
    for n, d in P: n2 = mv(m[0], n); out.append((n2, qa(d, dot(n2, m[1]))))
    return out
def layer_maps(kind, n=2):
    out = {0: (EYE, ZV)}
    for k in range(1, n + 1):
        for s in (1, -1):
            j = s * k
            if kind == 'octet' or (kind == 'single' and s < 0): out[j] = SH(vmul([ONE, ONE, Z], qm(R, qr(j))))
            elif kind == 'gyrated': out[j] = comp(mir(2 * j - s), out[j - s])
            else: out[j] = comp(mir(1), out[1 - j])
    return out
Rf = qf(R); fl = lambda P: np.array([[qf(c) for c in p] for p in P])
OCT = [[R if (i == j and s > 0) else (qn(R) if i == j else Z) for j in range(3)] for i in range(3) for s in (1, -1)]
cent0 = [vmul([qr(a), qr(b), qr(c)], R) for a, b, c in itertools.product(range(-3, 4), repeat=3) if a + b + c == 0]
e2 = qm(qr(2), qm(R, R))
EDGES = [(a, b) for a, b in itertools.combinations(range(6), 2) if dot(vsub(OCT[a], OCT[b]), vsub(OCT[a], OCT[b])) == e2]
half = qr(Fr(1, 2)); third = qm(R, qr(Fr(1, 3)))
CORNER = [ZV, [Z, Z, R], [qm(R, half), Z, qm(R, half)], [qm(R, qn(half)), Z, qm(R, half)], [Z, qm(R, half), qm(R, half)], [Z, qm(R, qn(half)), qm(R, half)]] + \
         [[qm(third, qr(a)), qm(third, qr(b)), third] for a in (1, -1) for b in (1, -1)]
ROTS = []
for p in itertools.permutations(range(3)):
    for s in itertools.product((1, -1), repeat=3):
        A = np.diag(s) @ np.eye(3)[list(p)]
        if np.linalg.det(A) > 0: ROTS.append(QM(A.astype(int).tolist()))
def bbox(P): P = fl(P); return P.min(0), P.max(0)
meets = lambda a, b: bool(np.all(a[0] < b[1] - 1e-9) and np.all(b[0] < a[1] - 1e-9))
vol = lambda planes: volume(intersect(planes))
def run(kind):
    LM = layer_maps(kind); octs = []
    for k, m in LM.items():
        for c in cent0:
            mc = comp(m, SH(c)); cc = ap(mc, ZV)
            if np.linalg.norm([qf(x) for x in cc]) < 3.2 * Rf:
                W = [ap(mc, v) for v in V]; octs.append(dict(m=mc, c=cc, P=pl_ap(mc, OGP), W=W, bb=bbox(W)))
    edges = {}
    for idx, o in enumerate(octs):
        for a, b in EDGES:
            mid = ap(o['m'], vmul(vadd(OCT[a], OCT[b]), half)); edges.setdefault(tuple(round(qf(x), 6) for x in mid), (mid, []))[1].append(idx)
    Ms = []
    for key, (mid, ids) in edges.items():
        if np.linalg.norm(key) > 2.0 * Rf or len(ids) != 2: continue
        pts = []
        for idx in ids:
            W = octs[idx]['W']; i = min(FIVE, key=lambda i: np.linalg.norm(fl([W[i]])[0] - np.array(key))); pts += [W[j] for j in STAR[i]]
        H = planes_of(pts); a, b = (octs[i] for i in ids)
        v = qs(qs(vol(H), vol(H + a['P'])), vol(H + b['P']))
        twin = (qf(det3(*a['m'][0])) > 0) != (qf(det3(*b['m'][0])) > 0)
        Ms.append(dict(mid=mid, key=key, H=H, bb=bbox(pts), ids=ids, v=v, twin=twin, plane=round(qf(dot([ONE, ONE, ONE], mid)) / Rf)))
    return octs, Ms
def notch(Pp, Pbb, Ms, octs):
    t = Z
    for M in Ms:
        if not meets(Pbb, M['bb']): continue
        x = vol(Pp + M['H'])
        if x == Z: continue
        for i in M['ids']:
            if meets(Pbb, octs[i]['bb']): x = qs(x, vol(Pp + M['H'] + octs[i]['P']))
        t = qa(t, x)
    return t
out = {}
octv = qm(qr(Fr(4, 3)), qm(R, qm(R, R))); tetv = qm(octv, qr(Fr(1, 4))); cellv = qa(octv, qm(qr(2), tetv)); OGv = volume(V)
cap0 = qm(qs(octv, OGv), qr(Fr(1, 6)))
for kind in ('octet', 'single', 'gyrated'):
    print(f'\n== {kind}', flush=True)
    octs, Ms = run(kind)
    mvs = {}
    for M in Ms: mvs.setdefault('Mg' if M['twin'] else 'M0', set()).add(M['v'])
    for k, s in mvs.items(): ok(len(s) == 1, f'{k}: {sum(1 for M in Ms if ("Mg" if M["twin"] else "M0") == k)} middle pieces, all {qstr(next(iter(s)))}')
    # middle pieces pairwise disjoint, and outside every OG but their own two
    bad = 0; pairs = 0
    near = [M for M in Ms if np.linalg.norm(M['key']) < 1.3 * Rf]
    for A in near:
        for B in Ms:
            if A is B or not meets(A['bb'], B['bb']): continue
            pairs += 1; x = vol(A['H'] + B['H'])
            for i in set(A['ids']) | set(B['ids']): x = qs(x, vol(A['H'] + B['H'] + octs[i]['P']))
            if x != Z: bad += 1
        for i, o in enumerate(octs):
            if i not in A['ids'] and meets(A['bb'], o['bb']) and vol(A['H'] + o['P']) != Z: bad += 1
    ok(bad == 0, f'middle pieces near the origin octahedron: no two overlap ({pairs} touching pairs checked) and none enters a third OG')
    caps = []
    for A in ROTS:
        Cp = [mv(A, p) for p in CORNER]; v = mv(A, [Z, Z, R])
        if any(v == c['v'] for c in caps): continue
        Pp = planes_of(Cp); bb = bbox(Cp)
        x = qs(qs(vol(Pp), vol(Pp + OGP)), notch(Pp, bb, Ms, octs))
        caps.append(dict(v=v, x=x, plane=round(qf(dot([ONE, ONE, ONE], v)) / Rf)))
    assert len(caps) == 6
    pts0 = [vmul([qr(a), qr(b), qr(c)], R) for a, b, c in itertools.product(range(-2, 3), repeat=3) if (a + b + c) % 2]
    tets = []
    on_oct = lambda p: sum(abs(qf(x)) for x in p) - Rf
    slab = [p for p in pts0 if abs(abs(qf(dot([ONE, ONE, ONE], p))) - Rf) < 1e-9 and abs(on_oct(p)) < 1e-9]
    far = [p for p in pts0 if abs(abs(qf(dot([ONE, ONE, ONE], p))) - Rf) < 1e-9]
    for tri in itertools.combinations(slab, 3):
        if not all(dot(vsub(a, b), vsub(a, b)) == e2 for a, b in itertools.combinations(tri, 2)): continue
        s = [round(qf(dot([ONE, ONE, ONE], p)) / Rf) for p in tri]
        if len(set(s)) == 1: continue   # a face of the octahedron in a layer plane (the next cell is across the plane)
        for d in far:
            if any(all(x == y for x, y in zip(d, p)) for p in tri): continue
            if all(dot(vsub(d, p), vsub(d, p)) == e2 for p in tri) and on_oct(d) > 1e-9:
                Q = list(tri) + [d]; Pp = planes_of(Q); face = max(set(s + [round(qf(dot([ONE, ONE, ONE], d)) / Rf)]), key=(s + [round(qf(dot([ONE, ONE, ONE], d)) / Rf)]).count)
                tets.append(dict(Q=Q, face=face, x=qs(tetv, notch(Pp, bbox(Q), Ms, octs))))
    assert len(tets) == 6, len(tets)
    for c in caps: print(f'      cap at v{tuple(round(qf(x) / Rf) for x in c["v"])} (layer plane {c["plane"]:+d}): {qstr(c["x"])}')
    for t in tets: print(f'      tetrahedron with its face on plane {t["face"]:+d}: {qstr(t["x"])}')
    # the origin octahedron sums exactly: OG + 6 caps + every middle piece's part inside it
    octP = planes_of(OCT); inside = Z
    for M in Ms:
        if meets(bbox(OCT), M['bb']):
            x = vol(octP + M['H'])
            if x != Z: inside = qa(inside, qs(x, vol(octP + M['H'] + OGP)))
    tot = qa(qa(OGv, inside), Z)
    for c in caps: tot = qa(tot, c['x'])
    ok(tot == octv, f'origin octahedron: OG + 6 caps + middle pieces inside = octahedron {qstr(octv)}')
    out[kind] = dict(caps={str(c['plane']) + ':' + ','.join(str(round(qf(x) / Rf)) for x in c['v']): qs_(c['x']) for c in caps},
                     tets=[dict(face=t['face'], v=qs_(t['x'])) for t in tets], middle={k: qs_(next(iter(s))) for k, s in mvs.items()})
    if kind != 'single':
        nM = {'octet': {'M0': 6}, 'gyrated': {'M0': 3, 'Mg': 3}}[kind]
        up = next(t['x'] for t in tets if t['face'] > 0); dn = next(t['x'] for t in tets if t['face'] < 0)
        tot = qa(qa(OGv, up), dn)
        for c in caps: tot = qa(tot, c['x'])
        for k, n in nM.items(): tot = qa(tot, qm(qr(n), next(iter(mvs[k]))))
        ok(tot == cellv, f'one cell: OG + 6 caps + 2 tetrahedra + {nM} = cell {qstr(cellv)}')
    out[kind]['raw'] = dict(caps=[c['x'] for c in caps], tets=[(t['face'], t['x']) for t in tets])
O, S, G = out['octet']['raw'], out['single']['raw'], out['gyrated']['raw']
capO, tetO = set(O['caps']), {x for f, x in O['tets']}; capG, tetG = set(G['caps']), {x for f, x in G['tets']}
ok(capO == {(Fr(32, 243), Fr(-8, 243))} and tetO == {qm(qs(qs(qs(cellv, OGv), qm(qr(6), (Fr(32, 243), Fr(-8, 243)))), qm(qr(6), (Fr(310, 4617), Fr(26, 4617)))), qr(Fr(1, 2)))},
   'octet: notched cap (32 - 8sqrt5)/243 as #37, and keyless notched tetrahedron = (cell - OG - 6 caps - 6 M0)/2 from #37 exact values')
ok(len(capG) == 1 and len(tetG) == 1, f'gyrated: all 6 caps equal, boundary cap {qstr(next(iter(capG)))}; all 6 tetrahedra equal, boundary tetrahedron {qstr(next(iter(tetG)))}')
ok(sorted(S['caps'], key=qf) == sorted([next(iter(capG))] * 3 + [next(iter(capO))] * 3, key=qf), 'single twin plane: the 3 caps on the plane are boundary caps, the other 3 octet caps')
ok(sorted([x for f, x in S['tets']], key=qf) == sorted([next(iter(tetG))] * 3 + [next(iter(tetO))] * 3, key=qf) and all((x in tetG) == (f > 0) for f, x in S['tets']),
   'single twin plane: the 3 tetrahedra with a face on it are boundary tetrahedra, the other 3 octet tetrahedra')
cg, tg = next(iter(capG)), next(iter(tetG))
print(f'      boundary cap = octet cap - {qstr(qs(next(iter(capO)), cg))}; boundary tetrahedron = octet tetrahedron + {qstr(qs(tg, next(iter(tetO))))}')
for k in out: out[k].pop('raw')
json.dump(dict(mark='DICTO · dictospheres.com', study='2026-10-19-og-gyrated-octet', **out), open(os.path.join(ME, 'gyr-boundary-exact.json'), 'w'), indent=1, ensure_ascii=False)
print('saved gyr-boundary-exact.json')
