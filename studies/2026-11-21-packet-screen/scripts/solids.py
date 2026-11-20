# Packet screen 2026-11-21, step 1: every piece built exactly.
# Platonic + 11 Archimedean: exact textbook coordinates from studies/2026-11-02-dicto-vacuus/data/classical (copied to data/inputs);
# snub cube (field Q(t), tribonacci) and snub dodecahedron (field Q(xi), xi^3 - 2 xi = phi): exact coordinates built here;
# 13 Catalan solids: exact polar reciprocals of the unit-edge Archimedean solids in the midsphere (canonical form);
# square antiprism (field Q(2^(1/4))), pentagonal antiprism (icosahedron minus two opposite corners).
# Scale: Platonic, Archimedean, antiprisms: edge 1.  Catalan: dual of the edge-1 Archimedean (same midsphere).
# Every piece: list of edges (kind, squared length, sign of cos, cos^2 of the dihedral angle), all exact in the piece's field.
# Floats are used only to find faces (convex hull) and to fix signs (checked far from zero).
import sys, json, itertools, glob, os
from fractions import Fraction as Fr
import numpy as np
from scipy.spatial import ConvexHull
import sympy as sp
sys.path.insert(0, os.path.dirname(__file__))
from nf import fields, A_consts

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = fields(); KA = F['A']; S2, S5 = A_consts(KA)
FAIL = []
def check(label, ok):
    print(('ok   ' if ok else 'FAIL ') + label, flush=True)
    if not ok: FAIL.append(label)

def parseA(s):
    e = sp.expand(sp.sympify(s)); out = KA.q(0)
    for d, r in ((2, S2), (5, S5)):
        b = e.coeff(sp.sqrt(d)); e = sp.expand(e - b * sp.sqrt(d))
        out = KA.add(out, KA.scal(Fr(str(b)), r))
    assert e.is_Rational, s
    return KA.add(out, KA.q(Fr(str(e))))

def cross(K, u, w):
    return (K.sub(K.mul(u[1], w[2]), K.mul(u[2], w[1])), K.sub(K.mul(u[2], w[0]), K.mul(u[0], w[2])), K.sub(K.mul(u[0], w[1]), K.mul(u[1], w[0])))

def numv(K, v): return np.array([float(K.num(c)) for c in v])

def faces_of(K, V):
    P = np.array([numv(K, v) for v in V]); h = ConvexHull(P); out = {}
    for eq in h.equations:
        n, d = eq[:3], eq[3]
        S = tuple(sorted(i for i in range(len(P)) if abs(P[i] @ n + d) < 1e-7))
        out[S] = n
    faces = []
    for S, n in out.items():
        c = P[list(S)].mean(0); u = P[S[0]] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
        ang = [np.arctan2((P[i] - c) @ w, (P[i] - c) @ u) for i in S]
        faces.append([S[k] for k in np.argsort(ang)])
    # exact planarity and convexity check: every corner of a face on its plane, all other corners strictly inside
    for f in faces:
        nrm = cross(K, K.vsub(V[f[1]], V[f[0]]), K.vsub(V[f[2]], V[f[0]])); d = K.dot(nrm, V[f[0]])
        s = K.sign(d)
        assert s != 0
        for i, v in enumerate(V):
            t = K.sub(K.dot(nrm, v), d)
            if i in f: assert K.iszero(t), 'face not planar'
            else: assert K.sign(t) == -s, 'not convex / not a face'
    return faces

def edges_of(faces):
    E = {}
    for fi, f in enumerate(faces):
        for k in range(len(f)):
            a, b = f[k], f[(k + 1) % len(f)]; E.setdefault(tuple(sorted((a, b))), []).append(fi)
    assert all(len(v) == 2 for v in E.values())
    return E

def cosrec(K, u, w):
    uw = K.dot(u, w); return K.sign(uw), K.div(K.mul(uw, uw), K.mul(K.dot(u, u), K.dot(w, w)))

def solid_edges(K, V, faces, s2):
    out = []
    for (a, b), (f1, f2) in edges_of(faces).items():
        p, q = V[a], V[b]; d = K.vsub(q, p)
        r1 = next(V[i] for i in faces[f1] if i not in (a, b)); r2 = next(V[i] for i in faces[f2] if i not in (a, b))
        sg, c2 = cosrec(K, K.perp(K.vsub(r1, p), d), K.perp(K.vsub(r2, p), d))
        out.append(('edge', K.div(K.dot(d, d), s2), sg, c2))
    return out

def pyramid_edges(K, V, f, s2):
    n = len(f); out = []; O = (K.q(0),) * 3
    for k in range(n):
        p, q, r = V[f[k]], V[f[(k + 1) % n]], V[f[(k + 2) % n]]; d = K.vsub(q, p)
        sg, c2 = cosrec(K, K.perp(K.vsub(r, p), d), K.perp(K.vsub(O, p), d))
        out.append(('base', K.div(K.dot(d, d), s2), sg, c2))
    for k in range(n):
        v, a, b = V[f[k]], V[f[k - 1]], V[f[(k + 1) % n]]
        sg, c2 = cosrec(K, K.perp(a, v), K.perp(b, v))
        out.append(('lateral', K.div(K.dot(v, v), s2), sg, c2))
    return out

def keyof(edges):
    return tuple(sorted((k, L, s, c) for k, L, s, c in edges))

def edge2(K, V, faces):
    E = list(edges_of(faces)); vals = set()
    for a, b in E:
        d = K.vsub(V[b], V[a]); vals.add(K.dot(d, d))
    return vals

def dual(K, V, faces):
    E = list(edges_of(faces)); rho = set()
    for a, b in E:
        m = tuple(K.scal(Fr(1, 2), K.add(x, y)) for x, y in zip(V[a], V[b])); rho.add(K.dot(m, m))
    assert len(rho) == 1, 'midsphere'
    rho = rho.pop(); D = []
    for f in faces:
        nrm = cross(K, K.vsub(V[f[1]], V[f[0]]), K.vsub(V[f[2]], V[f[0]])); d = K.dot(nrm, V[f[0]])
        D.append(K.vscal(K.div(rho, d), nrm))
    return D

def evenperms(t): a, b, c = t; return [(a, b, c), (b, c, a), (c, a, b)]
def oddperms(t): a, b, c = t; return [(b, a, c), (a, c, b), (c, b, a)]

def snub_cube():
    K = F['T']; t = K.el([0, 1]); it = K.inv(t); one = K.q(1); V = []
    for perms, parity in ((evenperms, 0), (oddperms, 1)):
        for s in itertools.product([1, -1], repeat=3):
            if (sum(1 for x in s if x > 0) % 2) != parity: continue
            base = tuple(K.scal(si, c) for si, c in zip(s, (one, it, t)))
            V += perms(base)
    return K, V

def snub_dodecahedron():
    K = F['X']; xi = K.el([0, 1]); phi = K.sub(K.mul(xi, K.mul(xi, xi)), K.scal(2, xi))
    assert K.eq(K.mul(phi, phi), K.add(phi, K.q(1)))
    ip = K.inv(phi); ix = K.inv(xi)
    al = K.sub(xi, ix); be = K.add(K.add(K.mul(xi, phi), K.mul(phi, phi)), K.mul(phi, ix))
    def L(*terms):
        s = K.q(0)
        for c, *fs in terms:
            t = K.q(c)
            for f in fs: t = K.mul(t, f)
            s = K.add(s, t)
        return s
    one = K.q(1)
    trip = [
        (K.scal(2, al), K.q(2), K.scal(2, be)),
        (L((1, al), (1, be, ip), (1, phi)), L((-1, al, phi), (1, be), (1, ip)), L((1, al, ip), (1, be, phi), (-1, one))),
        (L((-1, al, ip), (1, be, phi), (1, one)), L((-1, al), (1, be, ip), (-1, phi)), L((1, al, phi), (1, be), (-1, ip))),
        (L((-1, al, ip), (1, be, phi), (-1, one)), L((1, al), (-1, be, ip), (-1, phi)), L((1, al, phi), (1, be), (1, ip))),
        (L((1, al), (1, be, ip), (-1, phi)), L((1, al, phi), (-1, be), (1, ip)), L((1, al, ip), (1, be, phi), (1, one))),
    ]
    V = []
    for b in trip:
        for s in itertools.product([1, -1], repeat=3):
            if sum(1 for x in s if x > 0) % 2: continue
            V += evenperms(tuple(K.scal(si, c) for si, c in zip(s, b)))
    return K, V

def square_antiprism():
    K = F['S4']; s = K.el([0, 1]); h2 = K.scal(Fr(1, 2), K.el([0, 0, 0, 1]))   # h/2 = 1/(2 s) = s^3/4
    h2 = K.scal(Fr(1, 2), h2); r = K.scal(Fr(1, 2), K.el([0, 0, 1]))            # 1/sqrt2 = s^2/2
    half = K.q(Fr(1, 2)); z = K.q(0); V = []
    for a, b in itertools.product([1, -1], repeat=2): V.append((K.scal(a, half), K.scal(b, half), h2))
    for v in [(r, z), (K.neg(r), z), (z, r), (z, K.neg(r))]: V.append((v[0], v[1], K.neg(h2)))
    return K, V

def loadA(name):
    d = json.load(open(os.path.join(HERE, 'data', 'inputs', name + '.json')))
    V = [tuple(parseA(c) for c in v['exact']) for v in d['vertices']]
    return V

PLATONIC = ['dodecahedron', 'icosahedron', 'cube', 'tetrahedron', 'octahedron']   # D I C T O
ARCH = [('truncated_tetrahedron', 'triakis_tetrahedron'), ('cuboctahedron', 'rhombic_dodecahedron'), ('truncated_cube', 'triakis_octahedron'),
        ('truncated_octahedron', 'tetrakis_hexahedron'), ('rhombicuboctahedron', 'deltoidal_icositetrahedron'),
        ('truncated_cuboctahedron', 'disdyakis_dodecahedron'), ('snub_cube', 'pentagonal_icositetrahedron'),
        ('icosidodecahedron', 'rhombic_triacontahedron'), ('truncated_dodecahedron', 'triakis_icosahedron'),
        ('truncated_icosahedron', 'pentakis_dodecahedron'), ('rhombicosidodecahedron', 'deltoidal_hexecontahedron'),
        ('truncated_icosidodecahedron', 'disdyakis_triacontahedron'), ('snub_dodecahedron', 'pentagonal_hexecontahedron')]
COUNTS = {'dodecahedron': (20, 12), 'icosahedron': (12, 20), 'cube': (8, 6), 'tetrahedron': (4, 4), 'octahedron': (6, 8),
          'truncated_tetrahedron': (12, 8), 'cuboctahedron': (12, 14), 'truncated_cube': (24, 14), 'truncated_octahedron': (24, 14),
          'rhombicuboctahedron': (24, 26), 'truncated_cuboctahedron': (48, 26), 'snub_cube': (24, 38), 'icosidodecahedron': (30, 32),
          'truncated_dodecahedron': (60, 32), 'truncated_icosahedron': (60, 32), 'rhombicosidodecahedron': (60, 62),
          'truncated_icosidodecahedron': (120, 62), 'snub_dodecahedron': (60, 92)}

def ser(K, a): return [str(x) for x in a]

def build():
    solids = []   # (name, family, fieldkey, K, V, faces, s2)
    for nm in PLATONIC:
        V = loadA(nm); fc = faces_of(KA, V); e = edge2(KA, V, fc); assert len(e) == 1
        solids.append((nm, 'Platonic', 'A', KA, V, fc, e.pop()))
    for nm, cat in ARCH:
        if nm == 'snub_cube': fk = 'T'; K, V = snub_cube()
        elif nm == 'snub_dodecahedron': fk = 'X'; K, V = snub_dodecahedron()
        else: fk = 'A'; K = KA; V = loadA(nm)
        fc = faces_of(K, V); e = edge2(K, V, fc)
        check(f'{nm}: {len(V)} corners, {len(fc)} faces, one edge length (exact)', (len(V), len(fc)) == COUNTS[nm] and len(e) == 1)
        s2 = e.pop()
        R = set(K.dot(v, v) for v in V); check(f'{nm}: all corners on one sphere (exact)', len(R) == 1)
        solids.append((nm, 'Archimedean', fk, K, V, fc, s2))
        D = dual(K, V, fc); fd = faces_of(K, D)
        check(f'{cat}: {len(D)} corners, {len(fd)} faces (polar of {nm})', len(D) == len(fc) and len(fd) == len(V))
        solids.append((cat, 'Catalan', fk, K, D, fd, s2))
    K, V = square_antiprism(); fc = faces_of(K, V); e = edge2(K, V, fc)
    check('square antiprism: 8 corners, 10 faces, edge 1 (exact)', len(fc) == 10 and e == {K.q(1)})
    solids.append(('square_antiprism', 'antiprism', 'S4', K, V, fc, K.q(1)))
    Vi = loadA('icosahedron'); top = max(Vi, key=lambda v: (KA.num(v[2]), KA.num(v[1])))
    Vp = [v for v in Vi if v != top and v != tuple(KA.neg(c) for c in top)]
    fc = faces_of(KA, Vp); e = edge2(KA, Vp, fc)
    check('pentagonal antiprism: 10 corners, 12 faces, one edge length', len(fc) == 12 and len(e) == 1)
    solids.append(('pentagonal_antiprism', 'antiprism', 'A', KA, Vp, fc, e.pop()))

    pieces = []
    for nm, fam, fk, K, V, fc, s2 in solids:
        E = solid_edges(K, V, fc, s2)
        pieces.append({'id': nm, 'kind': 'solid', 'family': fam, 'field': fk, 'solid': nm, 'faces': len(fc),
                       'edges': [[k, ser(K, L), s, ser(K, c)] for k, L, s, c in E]})
        if fam == 'antiprism': continue
        groups = {}
        for f in fc:
            pe = pyramid_edges(K, V, f, s2); k = keyof(pe)
            groups.setdefault(k, {'n': len(f), 'count': 0, 'edges': pe}); groups[k]['count'] += 1
        sizes = {}
        for g in groups.values(): sizes.setdefault(g['n'], []).append(g)
        for n, gs in sorted(sizes.items()):
            for j, g in enumerate(gs):
                pid = f'P[{nm}|{n}]' + (f'#{j + 1}' if len(gs) > 1 else '')
                pieces.append({'id': pid, 'kind': 'pyramid', 'family': fam, 'field': fk, 'solid': nm, 'face_sides': n, 'face_count': g['count'],
                               'edges': [[k, ser(K, L), s, ser(K, c)] for k, L, s, c in g['edges']]})
        print(f'{nm}: {len(fc)} faces -> {len(groups)} pyramid type(s): ' + ', '.join(f"{g['n']}-gon x{g['count']}" for g in groups.values()), flush=True)
    npyr = sum(1 for p in pieces if p['kind'] == 'pyramid')
    print(f'pieces: {len(pieces)} ({npyr} centre pyramids, {len(pieces) - npyr} solids)')
    json.dump(pieces, open(os.path.join(HERE, 'data', 'pieces.json'), 'w'))
    print('FINAL ok' if not FAIL else f'FINAL FAIL {FAIL}')

if __name__ == '__main__':
    build()
