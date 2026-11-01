# The classical solids for the DICTO Vacuus study, generated exactly: 5 Platonic, 11 Archimedean (all but the two snubs) in Q, Q(sqrt2),
# Q(sqrt5) from their textbook coordinates; the 11 matching Catalan solids as exact polar reciprocals (poles N / (N.p) of the faces).
# The snub cube, snub dodecahedron and their duals (cubic fields) are taken in float64 from krp-core's registry (classical-krp.json).
# Every hull is checked exactly (each face point on its plane, every other corner strictly inside), and each generated solid is matched
# against krp-core's registry by its scaled squared-distance key (1e-6).
# Usage: classical.py <classical-krp.json> <out dir>   -> <out>/<id>.json in the DICTO Solids format (vertices exact + decimal, faces, field)
import sys, os, json, itertools, numpy as np
from fractions import Fraction as Fr
from scipy.spatial import ConvexHull
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qf import QF, vsub, dot, cross
KRP, OUT = sys.argv[1:3]; os.makedirs(OUT, exist_ok=True)

def cyc(p): return [p, [p[1], p[2], p[0]], [p[2], p[0], p[1]]]
def allperm(p): return [list(q) for q in itertools.permutations(p)]
def evenperm(p): return [[p[i], p[j], p[k]] for i, j, k in ((0, 1, 2), (1, 2, 0), (2, 0, 1))]
def signs(p):
    out = []
    for s in itertools.product((1, -1), repeat=3):
        q = [x * si for x, si in zip(p, s)]
        out.append(q)
    return out
def uniq(P):
    seen = {}; [seen.setdefault(tuple((x.a, x.b) for x in p), p) for p in P]; return list(seen.values())
def evensign(p):
    return [[x * si for x, si in zip(p, s)] for s in itertools.product((1, -1), repeat=3) if s.count(-1) % 2 == 0]

def gen(name, d):
    QF.D = d
    q = lambda a, b=0: QF(a, b)
    if d == 5: phi = q(Fr(1, 2), Fr(1, 2)); iphi = phi - 1
    if d == 2: r2 = q(0, 1)
    P = []
    if name == 'TETRAHEDRON': P = evensign([q(1), q(1), q(1)])
    elif name == 'CUBE': P = signs([q(1), q(1), q(1)])
    elif name == 'OCTAHEDRON': P = [p for x in allperm([q(1), q(0), q(0)]) for p in signs(x)]
    elif name == 'ICOSAHEDRON': P = [p for c in cyc([q(0), q(1), phi]) for p in signs(c)]
    elif name == 'DODECAHEDRON': P = signs([q(1), q(1), q(1)]) + [p for c in cyc([q(0), iphi, phi]) for p in signs(c)]
    elif name == 'TRUNCATED_TETRAHEDRON': P = [p for x in allperm([q(3), q(1), q(1)]) for p in evensign(x)]
    elif name == 'CUBOCTAHEDRON': P = [p for x in allperm([q(1), q(1), q(0)]) for p in signs(x)]
    elif name == 'TRUNCATED_OCTAHEDRON': P = [p for x in allperm([q(0), q(1), q(2)]) for p in signs(x)]
    elif name == 'TRUNCATED_CUBE': P = [p for x in allperm([r2 - 1, q(1), q(1)]) for p in signs(x)]
    elif name == 'RHOMBICUBOCTAHEDRON': P = [p for x in allperm([q(1), q(1), r2 + 1]) for p in signs(x)]
    elif name == 'TRUNCATED_CUBOCTAHEDRON': P = [p for x in allperm([q(1), r2 + 1, 2 * r2 + 1]) for p in signs(x)]
    elif name == 'ICOSIDODECAHEDRON':
        P = [p for x in allperm([q(0), q(0), phi]) for p in signs(x)] + [p for c in cyc([q(Fr(1, 2)), phi / 2, phi * phi / 2]) for p in signs(c)]
    elif name == 'TRUNCATED_ICOSAHEDRON':
        P = [p for t in ([q(0), q(1), 3 * phi], [q(1), 2 + phi, 2 * phi], [phi, q(2), phi * phi * phi]) for c in cyc(t) for p in signs(c)]
    elif name == 'TRUNCATED_DODECAHEDRON':
        P = [p for t in ([q(0), iphi, 2 + phi], [iphi, phi, 2 * phi], [phi, q(2), phi + 1]) for c in cyc(t) for p in signs(c)]
    elif name == 'RHOMBICOSIDODECAHEDRON':
        P = [p for t in ([q(1), q(1), phi * phi * phi], [phi * phi, phi, 2 * phi], [2 + phi, q(0), phi * phi]) for c in cyc(t) for p in signs(c)]
    elif name == 'TRUNCATED_ICOSIDODECAHEDRON':
        P = [p for t in ([iphi, iphi, 3 + phi], [2 * iphi, phi, 1 + 2 * phi], [iphi, phi * phi, 3 * phi - 1], [2 * phi - 1, q(2), 2 + phi],
                         [phi, q(3), 2 * phi]) for c in cyc(t) for p in signs(c)]
    return uniq(P)

def hull(PE):
    """faces (ccw seen from outside) of the hull of exact points PE; exact check. returns faces, ok"""
    PF = np.array([[float(x) for x in p] for p in PE]); H = ConvexHull(PF); groups = {}; ok = True
    for sm, eq in zip(H.simplices, H.equations): groups.setdefault(tuple(np.round(eq / np.abs(eq[:3]).max(), 7)), eq)
    faces = []
    for eq in groups.values():
        on = [i for i in range(len(PF)) if abs(eq[:3] @ PF[i] + eq[3]) < 1e-9 * max(1, np.abs(PF).max())]
        p0 = PE[on[0]]
        nrm = next(c for a, b in itertools.combinations(on[1:], 2) for c in [cross(vsub(PE[a], p0), vsub(PE[b], p0))] if any(x.sign() for x in c))
        off = dot(nrm, p0)
        if any((dot(nrm, PE[i]) - off).sign() != 0 for i in on): ok = False
        sg = {(dot(nrm, PE[i]) - off).sign() for i in range(len(PE)) if i not in on}
        if len(sg) != 1 or 0 in sg: ok = False
        n = eq[:3]; c = PF[on].mean(0); u = PF[on[0]] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
        ang = [np.arctan2((PF[i] - c) @ w, (PF[i] - c) @ u) for i in on]
        faces.append([on[k] for k in np.argsort(ang)])           # ccw about the outward normal n
    return faces, ok
def key(P):
    P = np.array(P, float); P = P - P.mean(0); D = ((P[:, None] - P[None]) ** 2).sum(-1); v = np.sort(D[np.triu_indices(len(P), 1)]); return v / v[-1]
def polar(PE, faces):
    """exact polar reciprocal about the origin (unit sphere): pole of face = N / (N.p)"""
    P = []
    for f in faces:
        N = [QF(0)] * 3
        for k in range(len(f)): N = [x + y for x, y in zip(N, cross(PE[f[k]], PE[f[(k + 1) % len(f)]]))]
        s = dot(N, PE[f[0]]); P.append([x / s for x in N])
    return P
def write(id_, family, field, PE, faces, ok, krpkey, note=''):
    d = QF.D
    fs = lambda x: str(x)
    V = [{'exact': [fs(x) for x in p], 'decimal': [repr(float(x)) for x in p]} for p in PE]
    m = bool(krpkey is not None and len(krpkey) == len(key(PE)) and np.allclose(key(PE), krpkey, atol=1e-6))
    json.dump(dict(name=id_.replace('_', ' ').title(), family=family, field=field, convex=True, vertices=V, faces=faces,
                   checks=dict(exact_hull=ok, matches_krp_registry=m), note=note), open(os.path.join(OUT, id_.lower() + '.json'), 'w'), indent=0)
    print(id_, family, field, len(PE), len(faces), 'exact hull', ok, 'krp match', m, flush=True)

R = {x['id']: x for x in json.load(open(KRP))}
DUAL = {'TETRAHEDRON': 'TETRAHEDRON', 'CUBE': 'OCTAHEDRON', 'OCTAHEDRON': 'CUBE', 'ICOSAHEDRON': 'DODECAHEDRON', 'DODECAHEDRON': 'ICOSAHEDRON',
        'TRUNCATED_TETRAHEDRON': 'TRIAKIS_TETRAHEDRON', 'CUBOCTAHEDRON': 'RHOMBIC_DODECAHEDRON', 'TRUNCATED_OCTAHEDRON': 'TETRAKIS_HEXAHEDRON',
        'TRUNCATED_CUBE': 'TRIAKIS_OCTAHEDRON', 'RHOMBICUBOCTAHEDRON': 'DELTOIDAL_ICOSITETRAHEDRON', 'TRUNCATED_CUBOCTAHEDRON': 'DISDYAKIS_DODECAHEDRON',
        'ICOSIDODECAHEDRON': 'RHOMBIC_TRIACONTAHEDRON', 'TRUNCATED_ICOSAHEDRON': 'PENTAKIS_DODECAHEDRON', 'TRUNCATED_DODECAHEDRON': 'TRIAKIS_ICOSAHEDRON',
        'RHOMBICOSIDODECAHEDRON': 'DELTOIDAL_HEXECONTAHEDRON', 'TRUNCATED_ICOSIDODECAHEDRON': 'DISDYAKIS_TRIACONTAHEDRON'}
FIELD = {1: 'Q', 2: 'Q(sqrt(2))', 5: 'Q(sqrt(5))'}
for nm, cat in DUAL.items():
    d = 5 if any(k in nm for k in ('ICOSA', 'DODECA')) else 2 if nm in ('TRUNCATED_CUBE', 'RHOMBICUBOCTAHEDRON', 'TRUNCATED_CUBOCTAHEDRON') else 1
    PE = gen(nm, 5 if d == 1 else d); QF.D = 5 if d == 1 else d
    fam = 'Platonic' if nm in ('TETRAHEDRON', 'CUBE', 'OCTAHEDRON', 'ICOSAHEDRON', 'DODECAHEDRON') else 'Archimedean'
    F, ok = hull(PE); write(nm, fam, FIELD[d], PE, F, ok, key(np.array(R[nm]['vertices'])) if nm in R else None, note=f'dual: {cat}')
    if fam == 'Archimedean':
        DE = polar(PE, F); F2, ok2 = hull(DE)
        write(cat, 'Catalan', FIELD[d], DE, F2, ok2, key(np.array(R[cat]['vertices'])) if cat in R else None, note=f'dual: {nm} (exact polar reciprocal)')
# snubs: float64 from the registry
for nm, cat in (('SNUB_CUBE', 'PENTAGONAL_ICOSITETRAHEDRON'), ('SNUB_DODECAHEDRON', 'PENTAGONAL_HEXECONTAHEDRON')):
    for id_, fam in ((nm, 'Archimedean'), (cat, 'Catalan')):
        r = R[id_]; V = [{'exact': None, 'decimal': [repr(float(x)) for x in p]} for p in r['vertices']]
        json.dump(dict(name=id_.replace('_', ' ').title(), family=fam, field='float64 (cubic field; krp-core registry)', convex=True, vertices=V,
                       faces=r['faces'], checks=dict(exact_hull=None, matches_krp_registry=True), note='dual: ' + (cat if id_ == nm else nm)),
                  open(os.path.join(OUT, id_.lower() + '.json'), 'w'), indent=0)
        print(id_, fam, 'float64', len(r['vertices']), len(r['faces']), flush=True)
