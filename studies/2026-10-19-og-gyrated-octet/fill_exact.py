# DICTO Fill sets, exact in Q(sqrt5) (DICTO 2026-10-20; float runs dbt_fill.py, kits_page_data.py).
#   DICTO Fill set 1 (DBT) F1: grown bipyramid, gyrated octet      DICTO Fill set 2 (OTT) F1: grown bipyramid, gyrated octet
#   DICTO Fill set 2 (OTT) F2, F3: grown tetrahedra, octet
# A fill piece = the Voronoi region of its site (bipyramid centre = twin-plane face centre; tetrahedron centre) minus the solids.
# Proved here, for every site round the central solid:
#   1. volume = vol(Voronoi region) - sum over solids of vol(region & solid)  (convex pieces; solids pairwise disjoint), = the expected value
#   2. congruence: an exact isometry of the whole local arrangement (solids and sites) takes the first site to each other site;
#      whether a proper one exists (same hand) or only an improper one (mirror image)
#   3. the piece's own symmetry from the arrangement: the maps fixing the site; an improper one = the piece is its own mirror image
# Not proved here (float, kits_page_data.py): that each piece is one solid.
import os, sys, json, itertools, numpy as np
ME = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(ME, '..', '2026-10-18-ocd-octet', 'scripts'))
from q5 import *
from exactpoly import planes_of, intersect, volume
ok = lambda c, m: print(('PASS ' if c else 'FAIL ') + m, flush=True)
qstr = lambda x: f'{x[0]} + {x[1]}*sqrt5 = {qf(x):.6f}'
D = json.load(open(os.path.join(ME, '..', '2026-10-18-ocd-octet', 'data', 'step1-ocd-exact.json'))); R = q(D['R']); Rf = qf(R)
SOL = {'DBT': [[q(c) for c in v] for v in json.load(open(os.path.join(ME, 'dbt-exact.json')))['V']],
       'OTT': [[q(c) for c in v] for v in json.load(open(os.path.join(ME, 'cut8-exact.json')))['V']]}
QM = lambda rows: [[qr(Fr(x)) for x in row] for row in rows]
EYE = QM(np.eye(3).astype(int).tolist()); MIR = QM([[Fr(1, 3), Fr(-2, 3), Fr(-2, 3)], [Fr(-2, 3), Fr(1, 3), Fr(-2, 3)], [Fr(-2, 3), Fr(-2, 3), Fr(1, 3)]])
ZV = [Z, Z, Z]; mv = lambda A, x: [dot(A[i], x) for i in range(3)]
mm = lambda A, B: [[dot(A[i], [B[k][j] for k in range(3)]) for j in range(3)] for i in range(3)]
comp = lambda a, b: (mm(a[0], b[0]), vadd(mv(a[0], b[1]), a[1])); ap = lambda m, x: vadd(mv(m[0], x), m[1])
mir = lambda k: (MIR, [qm(R, qr(Fr(2 * k, 3)))] * 3)
detq = lambda A: det3(*A)
def layer_maps(stack, n=3):
    out = {0: (EYE, ZV)}
    for k in range(1, n + 1):
        for s in (1, -1):
            j = s * k
            out[j] = comp(mir(2 * j - s), out[j - s]) if stack == 'gyrated' else (EYE, vmul([ONE, ONE, Z], qm(R, qr(j))))
    return out
nf = lambda v: float(np.linalg.norm([qf(x) for x in v]))
cent0 = [vmul([qr(a), qr(b), qr(c)], R) for a, b, c in itertools.product(range(-4, 5), repeat=3) if a + b + c == 0]
def solids(name, stack, rad):
    out = []
    for k, m in layer_maps(stack).items():
        for c in cent0:
            mc = comp(m, (EYE, c)); cc = ap(mc, ZV)
            if nf(cc) < rad: out.append(dict(c=cc, V=[ap(mc, v) for v in SOL[name]], m=mc))
    return out
def sites(stack, rad):
    if stack == 'octet':
        return [vmul([qr(Fr(a, 2)), qr(Fr(b, 2)), qr(Fr(c, 2))], R) for a, b, c in itertools.product(range(-7, 8, 2), repeat=3) if np.linalg.norm([a, b, c]) * Rf / 2 < rad]
    pts = [vmul([qr(a), qr(b), qr(c)], R) for a, b, c in itertools.product(range(-2, 3), repeat=3) if (a + b + c) % 2]
    e2 = qm(qr(2), qm(R, R)); s3 = lambda p: dot([ONE, ONE, ONE], p)
    sl = [p for p in pts if abs(abs(qf(s3(p))) - Rf) < 1e-9]
    base = []
    for Q in itertools.combinations(sl, 4):
        if all(dot(vsub(a, b), vsub(a, b)) == e2 for a, b in itertools.combinations(Q, 2)):
            t = vmul(vadd(vadd(Q[0], Q[1]), vadd(Q[2], Q[3])), qr(Fr(1, 4))); k = 1 if qf(s3(t)) > 0 else -1
            f = vadd(t, [qm(qs(qm(R, qr(k)), s3(t)), qr(Fr(1, 3)))] * 3)
            for i, j in itertools.product(range(-5, 6), repeat=2):
                base.append(vadd(f, vadd(vmul([ONE, qn(ONE), Z], qm(R, qr(i))), vmul([Z, ONE, qn(ONE)], qm(R, qr(j))))))
    out = {}
    for k, m in layer_maps('gyrated').items():
        for b in base:
            c = ap(m, b)
            if nf(c) < rad: out[tuple(c)] = c
    return list(out.values())
def vor_planes(S, c):
    out = []
    for p in S:
        if p == c: continue
        if nf(vsub(p, c)) > 2.6 * Rf: continue
        n = vsub(p, c); out.append((n, qm(qs(dot(p, p), dot(c, c)), qr(Fr(1, 2)))))
    return out
SOLP = {k: planes_of(V) for k, V in SOL.items()}
def pl_ap(m, P):
    out = []
    for n, d in P: n2 = mv(m[0], n); out.append((n2, qa(d, dot(n2, m[1]))))
    return out
G48 = []
for p in itertools.permutations(range(3)):
    for s in itertools.product((1, -1), repeat=3): G48.append(QM((np.diag(s) @ np.eye(3)[list(p)]).astype(int).tolist()))
OPS = G48 + [mm(MIR, g) for g in G48]
def maps_to(A, s0, s1, solA, sitesA, solB_set, sitesB_set):
    t = vsub(s1, mv(A, s0)); g = (A, t)
    for so in solA:
        if frozenset(tuple(ap(g, v)) for v in so['V']) not in solB_set: return None
    for p in sitesA:
        if tuple(ap(g, p)) not in sitesB_set: return None
    return g
res = {}
for label, name, stack, expect in (('DICTO Fill set 1 (DBT) F1, gyrated', 'DBT', 'gyrated', (Fr(968, 81), Fr(-392, 81))),
                                    ('DICTO Fill set 2 (OTT) F1, gyrated', 'OTT', 'gyrated', (Fr(704, 81), Fr(-272, 81))),
                                    ('DICTO Fill set 2 (OTT) F2/F3, octet', 'OTT', 'octet', (Fr(352, 81), Fr(-136, 81)))):
    print(f'\n== {label}', flush=True)
    SO = solids(name, stack, 6.5 * Rf); S = sites(stack, 5.5 * Rf)
    solset = {frozenset(tuple(v) for v in so['V']) for so in SO}; siteset = {tuple(s) for s in S}
    near = [s for s in S if nf(s) < 1.9 * Rf]
    # the pieces that touch the central solid
    P0 = SOLP[name]; touch = []
    for s in near:
        x = volume(intersect(vor_planes(S, s) + P0))
        if x != Z: touch.append(s)
    vols = []
    for s in touch:
        VP = vor_planes(S, s); v = volume(intersect(VP))
        for so in SO:
            if nf(vsub(so['c'], s)) < 2.6 * Rf:
                x = volume(intersect(VP + pl_ap(so['m'], P0)))
                v = qs(v, x)
        vols.append(v)
    ok(all(v == expect for v in vols), f'{len(touch)} pieces touch the central solid; every one has volume {qstr(expect)}')
    # congruence and hands: local arrangement round each site (solids and sites within 3.2R) mapped exactly
    s0 = touch[0]; loc = lambda s: ([so for so in SO if nf(vsub(so['c'], s)) < 3.2 * Rf], [p for p in S if nf(vsub(p, s)) < 3.2 * Rf])
    solA, sitA = loc(s0); hands = []
    for s1 in touch:
        found = {}
        for A in OPS:
            g = maps_to(A, s0, s1, solA, sitA, solset, siteset)
            if g: found['proper' if qf(detq(A)) > 0 else 'improper'] = True
        hands.append(found)
    ok(all(h for h in hands), f'each piece is the image of the first under an exact isometry of the arrangement (solids and sites within 3.2R)')
    same = sum(1 for h in hands if 'proper' in h); only_m = sum(1 for h in hands if 'proper' not in h)
    stab = {('proper' if qf(detq(A)) > 0 else 'improper') for A in OPS if maps_to(A, s0, s0, solA, sitA, solset, siteset)}
    print(f'      reached by a turn (same hand): {same}; only by a mirror: {only_m}; maps fixing the site: {sorted(stab)}')
    if 'improper' in stab: ok(True, 'a mirror of the arrangement fixes the site: the piece is its own mirror image (one hand)')
    else: ok(only_m > 0, 'no mirror fixes the site and some pieces are reached only by a mirror: left and right hands (unless the piece has a symmetry of its own beyond the arrangement; float check in fill_hands.py)')
    res[label] = dict(volume=qs_(expect), pieces=len(touch), proper=same, mirror_only=only_m, stabiliser=sorted(stab))
json.dump(dict(mark='DICTO · dictospheres.com', **res), open(os.path.join(ME, 'fill-exact.json'), 'w'), indent=1, ensure_ascii=False)
print('saved fill-exact.json')
