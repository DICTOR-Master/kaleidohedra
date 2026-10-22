#!/usr/bin/env python3
# DICTO · dictospheres.com — Created by DICTO. Licence CC BY-SA 4.0.
# Standalone verifier for the DICTO math-data dataset: needs only python3 and sympy.
# It reads solids/*.json and packings/*.json and re-proves every stated property EXACTLY:
#   solids:   exact strings parse into Q(sqrt d); decimals agree with them; faces are valid index cycles; the surface is a closed
#             2-manifold (each directed edge once, its reverse once, each vertex link one cycle), consistently wound; Euler
#             characteristic 2; every face exactly planar; exact volume (positive, so the winding is outward) equals the stated value;
#             for solids stated convex: every face is a strictly convex polygon wound counter-clockwise seen from outside and every
#             other corner lies strictly inside its plane; f-vector, faces by sides, squared edge lengths and their counts; the full
#             symmetry group (orthogonal maps of the corner set about its centroid) has the stated order, rotation count and inversion,
#             consistent with the stated Schoenflies symbol; every value marked "published" equals the computed one.
#   packings: lattice vectors exact; the cell volume |det| as stated; piece rotations exactly orthogonal; the sum of the piece
#             volumes equals the cell volume exactly; no two pieces (all lattice translates that could meet) overlap: for every pair
#             either their float bounding boxes are apart by more than 1e-9 (coordinates are within 1e-14 of the exact values, so
#             the boxes are apart exactly too) or an exact separating plane is found (separating-axis theorem for convex polyhedra:
#             face normals of either piece and cross products of edge directions). Volume sum = cell volume plus no overlap
#             proves that the translates fill space (a tiling).
#   packings-nonfilling: published packings that do NOT fill space: lattice vectors exact (decimals agree, nonzero cell); cell volume as
#             stated; rotations exactly orthogonal, pieces convex; density = sum of the piece volumes / cell volume, exactly, equal to the
#             stated exact density (the published closed form) and its decimal, and the published percentage equals that decimal at the
#             published precision; no two pieces overlap (same exact separating-plane test as above).
#   unit volume: for every solid, the stated scale is exactly (stated volume)^(-1/3) (checked to 50 digits), the centre is the exact
#             corner centroid, every decimal unit-volume corner is centre + s (corner - centre) (1e-14), and the decimal unit-volume solid
#             has volume 1 (1e-12); the *-unit-volume.off files match.
# Usage: python3 check.py            (prints a PASS/FAIL table; exit code 0 only if everything passes)
import glob, itertools, json, math, os, sys
from fractions import Fraction as Fr
import sympy

HERE = os.path.dirname(os.path.abspath(__file__))


class QF:
    __slots__ = ('a', 'b', 'd')
    def __init__(s, a, b=0, d=5): s.a, s.b, s.d = Fr(a), Fr(b), d
    def _c(s, o): return o if isinstance(o, QF) else QF(o, 0, s.d)
    def __add__(s, o): o = s._c(o); return QF(s.a + o.a, s.b + o.b, s.d)
    __radd__ = __add__
    def __neg__(s): return QF(-s.a, -s.b, s.d)
    def __sub__(s, o): return s + (-s._c(o))
    def __rsub__(s, o): return s._c(o) - s
    def __mul__(s, o): o = s._c(o); return QF(s.a * o.a + s.d * s.b * o.b, s.a * o.b + s.b * o.a, s.d)
    __rmul__ = __mul__
    def __truediv__(s, o):
        o = s._c(o); n = o.a * o.a - s.d * o.b * o.b
        if n == 0: raise ZeroDivisionError
        return s * QF(o.a / n, -o.b / n, s.d)
    def sign(s):
        a, b, d = s.a, s.b, s.d
        if b == 0: return (a > 0) - (a < 0)
        if a == 0: return (b > 0) - (b < 0)
        if (a > 0) == (b > 0): return 1 if a > 0 else -1
        return (1 if a > 0 else -1) if a * a > d * b * b else (1 if b > 0 else -1)
    def __eq__(s, o): o = s._c(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def f(s): return float(s.a) + float(s.b) * math.sqrt(s.d)


def parse(txt, d):
    """exact string -> a + b sqrt(d), refusing anything outside Q(sqrt d)."""
    e = sympy.expand(sympy.sympify(txt))
    a = Fr(0); b = Fr(0)
    for t, c in e.as_coefficients_dict().items():
        if not c.is_Rational: raise ValueError(txt)
        c = Fr(int(c.p), int(c.q))
        if t == 1: a += c
        elif d > 1 and t == sympy.sqrt(d): b += c
        else: raise ValueError(f'{txt} is not in Q(sqrt({d}))')
    return QF(a, b, d)


dot = lambda u, v: u[0] * v[0] + u[1] * v[1] + u[2] * v[2]
sub = lambda u, v: (u[0] - v[0], u[1] - v[1], u[2] - v[2])
cross = lambda u, v: (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
det3 = lambda a, b, c: dot(a, cross(b, c))
RESULTS = []


def rec(item, test, ok, note=''):
    RESULTS.append((item, test, bool(ok), note))
    return ok


def field_of(doc):
    f = doc['field']; return 1 if f == 'Q' else int(f[f.index('sqrt(') + 5:f.index(')')])


def load_vertices(doc, d):
    V = [tuple(parse(x, d) for x in v['exact']) for v in doc['vertices']]
    dec_ok = all(abs(float(s) - x.f()) < 1e-14 for v, w in zip(doc['vertices'], V) for s, x in zip(v['decimal'], w))
    return V, dec_ok


def newell(V, f):
    n = (QF(0, 0, V[0][0].d),) * 3
    for i in range(len(f)):
        a, b = V[f[i]], V[f[(i + 1) % len(f)]]; c = cross(a, b); n = (n[0] + c[0], n[1] + c[1], n[2] + c[2])
    return n


def volume(V, F):
    s = QF(0, 0, V[0][0].d)
    for f in F:
        for k in range(1, len(f) - 1): s = s + det3(V[f[0]], V[f[k]], V[f[k + 1]])
    return s / 6


def symmetry(V):
    d = V[0][0].d; n = len(V); Z = QF(0, 0, d)
    c = tuple(sum((v[k] for v in V), Z) / n for k in range(3)); W = [sub(v, c) for v in V]; S = set(W)
    norms = [dot(w, w) for w in W]; cnt = {}
    for x in norms: cnt[x] = cnt.get(x, 0) + 1
    order = sorted(range(n), key=lambda i: (cnt[norms[i]], norms[i].f()))
    a = order[0]
    fl = [[x.f() for x in w] for w in W]
    dist = lambda i, j: math.dist(fl[i], fl[j])
    b = min((i for i in order if any(x.sign() for x in cross(W[a], W[i]))), key=lambda i: (cnt[norms[i]], dist(i, a)))
    ab = cross(W[a], W[b])
    cc = min((i for i in order if dot(ab, W[i]).sign()), key=lambda i: (cnt[norms[i]], dist(i, a)))
    A = [W[a], W[b], W[cc]]; G = [[dot(A[i], A[j]) for j in range(3)] for i in range(3)]
    Dt = det3(*A); adj = [cross(A[1], A[2]), cross(A[2], A[0]), cross(A[0], A[1])]
    pick = lambda i, cons: [j for j in range(n) if norms[j] == G[i][i] and all(dot(W[j], W[k]) == G[i][m] for m, k in cons)]
    out = []
    for ja in pick(0, []):
        for jb in pick(1, [(0, ja)]):
            for jc in pick(2, [(0, ja), (1, jb)]):
                B = [W[ja], W[jb], W[jc]]
                M = [[sum((B[k][i] * adj[k][j] for k in range(3)), Z) / Dt for j in range(3)] for i in range(3)]
                if all(tuple(dot(M[i], w) for i in range(3)) in S for w in W): out.append(M)
    detsign = [det3(*M).sign() for M in out]
    inv = any(all(M[i][j] == (QF(-1, 0, d) if i == j else Z) for i in range(3) for j in range(3)) for M in out)
    return len(out), sum(1 for s in detsign if s > 0), inv


# Schoenflies symbol -> (order, rotations, contains inversion); 'n' symbols handled generically
def schoenflies(sym):
    fixed = {'Ih': (120, 60, True), 'I': (60, 60, False), 'Oh': (48, 24, True), 'O': (24, 24, False), 'Th': (24, 12, True),
             'Td': (24, 12, False), 'T': (12, 12, False), 'C1': (1, 1, False), 'Ci': (2, 1, True), 'Cs': (2, 1, False)}
    if sym in fixed: return fixed[sym]
    import re
    m = re.fullmatch(r'([CDS])(\d+)([hvd]?)', sym); L, k, t = m.group(1), int(m.group(2)), m.group(3)
    if L == 'C' and t == '': return (k, k, False)
    if L == 'C' and t == 'v': return (2 * k, k, False)
    if L == 'C' and t == 'h': return (2 * k, k, k % 2 == 0)
    if L == 'S': return (k, k // 2, (k // 2) % 2 == 1)
    if L == 'D' and t == '': return (2 * k, 2 * k, False)
    if L == 'D' and t == 'h': return (4 * k, 2 * k, k % 2 == 0)
    if L == 'D' and t == 'd': return (4 * k, 2 * k, k % 2 == 1)
    raise ValueError(sym)


def check_solid(path):
    doc = json.load(open(path)); slug = os.path.basename(path)[:-5]; d = field_of(doc)
    V, dec_ok = load_vertices(doc, d); F = doc['faces']; nV = len(V)
    rec(slug, 'exact strings parse; decimals agree (1e-14)', dec_ok)
    rec(slug, 'corners distinct', len(set(V)) == nV)
    valid = all(len(f) >= 3 and len(set(f)) == len(f) and all(0 <= i < nV for i in f) for f in F)
    rec(slug, 'faces are valid index cycles', valid)
    E = {}
    for fi, f in enumerate(F):
        for a, b in zip(f, f[1:] + f[:1]): E[(a, b)] = E.get((a, b), 0) + 1
    closed = all(m == 1 for m in E.values()) and all((b, a) in E for (a, b) in E)
    # vertex links: faces round each vertex form one cycle
    link_ok = True
    for v in range(nV):
        nxt = {}
        for f in F:
            if v in f:
                k = f.index(v); nxt[f[k - 1]] = f[(k + 1) % len(f)]
        if not nxt: link_ok = False; break
        s = next(iter(nxt)); cur = s; steps = 0
        while True:
            cur = nxt.get(cur); steps += 1
            if cur is None or steps > len(nxt): link_ok = False; break
            if cur == s: break
        if steps != len(nxt): link_ok = False
    rec(slug, 'closed 2-manifold, consistently wound (each edge once each way; vertex links single cycles)', closed and link_ok)
    nE = len(E) // 2
    rec(slug, 'Euler characteristic V - E + F = 2', nV - nE + len(F) == 2, f'{nV} - {nE} + {len(F)}')
    planar = True; normals = []
    for f in F:
        n = newell(V, f); normals.append(n)
        if not any(x.sign() for x in n) or any(dot(n, sub(V[i], V[f[0]])).sign() for i in f): planar = False
    rec(slug, 'every face exactly planar', planar)
    vol = volume(V, F)
    rec(slug, 'exact volume positive (outward winding) and equal to stated', vol.sign() > 0 and vol == parse(doc['volume']['exact'], d), doc['volume']['exact'])
    rec(slug, 'stated volume decimal agrees', abs(float(doc['volume']['decimal']) - vol.f()) < 1e-12)
    if doc.get('convex'):
        cv = True
        for f, n in zip(F, normals):
            fs = set(f)
            for i in range(nV):
                sg = dot(n, sub(V[i], V[f[0]])).sign()
                if (i in fs and sg != 0) or (i not in fs and sg >= 0): cv = False
            for k in range(len(f)):
                a, b, c = V[f[k]], V[f[(k + 1) % len(f)]], V[f[(k + 2) % len(f)]]
                if dot(cross(sub(b, a), sub(c, b)), n).sign() <= 0: cv = False
        rec(slug, 'convex: faces strictly convex, CCW from outside, all other corners strictly inside', cv)
    fv = doc['f_vector']
    rec(slug, 'f-vector as stated', (fv['vertices'], fv['edges'], fv['faces']) == (nV, nE, len(F)))
    fk = {}
    for f in F: fk[str(len(f))] = fk.get(str(len(f)), 0) + 1
    rec(slug, 'faces by number of sides as stated', fk == doc['faces_by_sides'])
    edges = {tuple(sorted(e)) for e in E}
    el = {}
    for a, b in edges:
        x = dot(sub(V[a], V[b]), sub(V[a], V[b])); el[x] = el.get(x, 0) + 1
    stated = {parse(e['exact'], d): e['count'] for e in doc['squared_edge_lengths']}
    rec(slug, 'squared edge lengths and counts as stated', el == stated)
    order, rot, inv = symmetry(V); sy = doc['symmetry']
    rec(slug, f"symmetry group order {order}, rotations {rot}, inversion {inv} as stated", (order, rot, inv) == (sy['order'], sy['rotations'], sy['contains_inversion']))
    rec(slug, f"Schoenflies {sy['schoenflies']} consistent with order/rotations/inversion", schoenflies(sy['schoenflies']) == (order, rot, inv))
    pub = doc.get('published_values', {})
    if pub:
        ok = True
        for k, v in pub.items():
            if k == 'volume': ok &= parse(v, d) == vol
            elif k == 'f_vector': ok &= tuple(v) == (nV, nE, len(F))
            elif k == 'faces_by_sides': ok &= {str(a): b for a, b in v.items()} == fk
            elif k == 'squared_edge_lengths': ok &= {parse(x, d) for x in v} == set(el)
            elif k == 'symmetry_order': ok &= v == order
        rec(slug, 'agrees with the published values recorded (' + ', '.join(pub) + ')', ok)
    if 'unit_volume' in doc: check_unit_volume(slug, doc, V, F, vol, d)
    return V, F, vol, d


def check_unit_volume(slug, doc, V, F, vol, d):
    import mpmath
    mpmath.mp.dps = 60
    uv = doc['unit_volume']; Z = QF(0, 0, d)
    e = sympy.sympify(uv['scale_exact']); Vs = sympy.sympify(doc['volume']['exact'])
    rec(slug, 'unit volume: scale_exact = (stated volume)^(-1/3) (50 digits)', vol == parse(doc['volume']['exact'], d) and
        e.free_symbols == set() and abs(sympy.N(e ** -3 - Vs, 60)) < sympy.Float('1e-50'), uv['scale_exact'])
    s = mpmath.mpf(str(sympy.N(e, 60)))
    rec(slug, 'unit volume: scale decimal agrees (1e-14)', abs(float(uv['scale_decimal']) - float(s)) < 1e-14)
    c = tuple(sum((v[k] for v in V), Z) / len(V) for k in range(3))
    rec(slug, 'unit volume: centre = exact corner centroid; decimals agree', tuple(parse(x, d) for x in uv['centre']['exact']) == c and
        all(abs(float(a) - x.f()) < 1e-14 for a, x in zip(uv['centre']['decimal'], c)))
    mq = lambda x: mpmath.mpf(x.a.numerator) / x.a.denominator + mpmath.mpf(x.b.numerator) / x.b.denominator * mpmath.sqrt(d)
    W = [[float(x) for x in w] for w in uv['vertices_decimal']]
    rec(slug, 'unit volume: every corner = centre + s (corner - centre) (1e-14)', len(W) == len(V) and
        all(abs(W[i][k] - float(mq(c[k]) + s * (mq(V[i][k]) - mq(c[k])))) < 1e-14 for i in range(len(V)) for k in range(3)))
    vu = 0.0
    for f in F:
        for k in range(1, len(f) - 1):
            a, b, cc = W[f[0]], W[f[k]], W[f[k + 1]]
            vu += a[0] * (b[1] * cc[2] - b[2] * cc[1]) + a[1] * (b[2] * cc[0] - b[0] * cc[2]) + a[2] * (b[0] * cc[1] - b[1] * cc[0])
    rec(slug, 'unit volume: the decimal unit-volume solid has volume 1 (1e-12)', abs(vu / 6 - 1) < 1e-12, f'{vu / 6:.15f}')


def emax(L):
    m = L[0]
    for x in L[1:]:
        if (x - m).sign() > 0: m = x
    return m


def emin(L): return -emax([-x for x in L])


def sat_disjoint(A, B):
    """A, B: (vertices, faces) of convex polyhedra, exact. True if an exact separating plane exists (interiors disjoint)."""
    (VA, FA), (VB, FB) = A, B
    axes = [newell(VA, f) for f in FA] + [newell(VB, f) for f in FB]
    eA = {sub(VA[f[(k + 1) % len(f)]], VA[f[k]]) for f in FA for k in range(len(f))}
    eB = {sub(VB[f[(k + 1) % len(f)]], VB[f[k]]) for f in FB for k in range(len(f))}
    def gap(n):
        nf = [x.f() for x in n]; a = [sum(p[i].f() * nf[i] for i in range(3)) for p in VA]; b = [sum(p[i].f() * nf[i] for i in range(3)) for p in VB]
        return max(min(b) - max(a), min(a) - max(b)) / (math.sqrt(sum(x * x for x in nf)) or 1)
    cand = axes + [cross(u, v) for u in eA for v in eB]
    cand = [n for n in cand if any(x.sign() for x in n)]
    cand.sort(key=lambda n: -gap(n))
    for n in cand:
        pa = [dot(n, p) for p in VA]; pb = [dot(n, p) for p in VB]
        if (emax(pa) - emin(pb)).sign() <= 0 or (emax(pb) - emin(pa)).sign() <= 0: return True
    return False


def check_packing(path, solids, filling=True):
    doc = json.load(open(path)); slug = os.path.basename(path)[:-5]; d = field_of(doc)
    L = [tuple(parse(x, d) for x in v['exact']) for v in doc['lattice_vectors']]
    if not filling:
        rec(slug, 'kind: "packing, not a fill"', doc.get('kind') == 'packing, not a fill')
        rec(slug, 'lattice vectors exact; decimals agree (1e-14); cell nonzero', det3(*L).sign() != 0 and
            all(abs(float(a) - x.f()) < 1e-14 for v, w in zip(doc['lattice_vectors'], L) for a, x in zip(v['decimal'], w)))
    cv = det3(*L); cv = cv if cv.sign() > 0 else -cv
    rec(slug, 'cell volume |det(lattice)| as stated', cv.sign() > 0 and cv == parse(doc['cell_volume']['exact'], d), doc['cell_volume']['exact'])
    pieces = []; vsum = QF(0, 0, d); orth = True
    for p in doc['pieces']:
        V, F, vol, _ = solids[p['solid']]
        R = [[parse(x, d) for x in r] for r in p['rotation']]; t = tuple(parse(x, d) for x in p['translation'])
        RRt = [[sum((R[i][k] * R[j][k] for k in range(3)), QF(0, 0, d)) for j in range(3)] for i in range(3)]
        orth &= all(RRt[i][j] == (1 if i == j else 0) for i in range(3) for j in range(3))
        sgn = det3(*[tuple(R[i][k] for i in range(3)) for k in range(3)]).sign()
        W = [tuple(sum((R[i][k] * v[k] for k in range(3)), QF(0, 0, d)) + t[i] for i in range(3)) for v in V]
        FF = F if sgn > 0 else [f[::-1] for f in F]
        if not json.load(open(os.path.join(HERE, 'solids', p['solid'] + '.json'))).get('convex'): orth = False
        pieces.append((W, FF)); vsum = vsum + vol
    rec(slug, 'piece rotations exactly orthogonal; pieces convex', orth)
    if filling:
        rec(slug, 'sum of piece volumes = cell volume (exact)', vsum == cv)
    else:
        dens = vsum / cv; st = doc['density']
        rec(slug, 'density = sum of piece volumes / cell volume, exactly the stated (published) closed form', dens == parse(st['exact'], d), st['exact'])
        rec(slug, 'stated density decimal agrees (1e-14); below 1 (not a fill)', abs(float(st['decimal']) - dens.f()) < 1e-14 and (dens - 1).sign() < 0)
        pp = st['published_percent']; places = len(pp.split('.')[1]) if '.' in pp else 0
        rec(slug, f'published percentage {pp}% = the exact density rounded to {places} places', f'{dens.f() * 100:.{places}f}' == pp, f'{dens.f() * 100:.6f}%')
    ok, nexact = no_overlaps(L, pieces, d)
    rec(slug, f'no overlaps: {nexact} nearby piece pairs each separated by an exact plane', ok)
    if filling: rec(slug, 'volume sum = cell volume and no overlaps => the pieces tile space', ok and vsum == cv)


def no_overlaps(L, pieces, d):
    # all translates that could meet: lattice combinations with |t| <= 2 * max radius (+ margin)
    Lf = [[x.f() for x in v] for v in L]
    rad = max(max(math.dist([x.f() for x in w], [0, 0, 0]) for w in W) for W, _ in pieces)
    G = [[sum(Lf[i][k] * Lf[j][k] for k in range(3)) for j in range(3)] for i in range(3)]
    # bound on coefficients: |c_i| <= (2 rad + 1e-6) * sqrt((G^-1)_ii)
    Gs = sympy.Matrix(G).inv(); K = [int(math.ceil((2 * rad + 1e-6) * math.sqrt(float(Gs[i, i])))) for i in range(3)]
    ok = True; nexact = 0
    for c in itertools.product(*[range(-k, k + 1) for k in K]):
        t = tuple(sum((L[i][k] * c[i] for i in range(3)), QF(0, 0, d)) for k in range(3))
        for i, (WA, FA) in enumerate(pieces):
            for j, (WB, FB) in enumerate(pieces):
                if c == (0, 0, 0) and j <= i: continue
                WBt = [tuple(w[k] + t[k] for k in range(3)) for w in WB]
                fa = [[x.f() for x in w] for w in WA]; fb = [[x.f() for x in w] for w in WBt]
                if any(min(q[k] for q in fb) - max(p[k] for p in fa) > 1e-9 or min(p[k] for p in fa) - max(q[k] for q in fb) > 1e-9 for k in range(3)): continue
                nexact += 1
                if not sat_disjoint((WA, FA), (WBt, FB)): ok = False
    return ok, nexact


def main():
    solids = {}
    for p in sorted(glob.glob(os.path.join(HERE, 'solids', '*.json'))):
        try: solids[os.path.basename(p)[:-5]] = check_solid(p)
        except Exception as e: rec(os.path.basename(p)[:-5], 'checks ran', False, repr(e))
    for p in sorted(glob.glob(os.path.join(HERE, 'packings', '*.json'))):
        try: check_packing(p, solids)
        except Exception as e: rec(os.path.basename(p)[:-5], 'checks ran', False, repr(e))
    for p in sorted(glob.glob(os.path.join(HERE, 'packings-nonfilling', '*.json'))):
        try: check_packing(p, solids, filling=False)
        except Exception as e: rec(os.path.basename(p)[:-5], 'checks ran', False, repr(e))
    # also the OFF files: same corners (decimals) and faces as the JSON
    for p in sorted(glob.glob(os.path.join(HERE, 'solids', '*.off'))):
        unit = p.endswith('-unit-volume.off'); slug = os.path.basename(p)[:-(len('-unit-volume.off') if unit else 4)]
        doc = json.load(open(os.path.join(HERE, 'solids', slug + '.json')))
        lines = [l for l in open(p).read().split('\n') if l and not l.startswith('#')]
        nv, nf, _ = map(int, lines[1].split())
        vs = [list(map(float, l.split())) for l in lines[2:2 + nv]]; fs = [list(map(int, l.split()))[1:] for l in lines[2 + nv:2 + nv + nf]]
        ref = doc['unit_volume']['vertices_decimal'] if unit else [w['decimal'] for w in doc['vertices']]
        rec(slug, ('unit-volume ' if unit else '') + 'OFF file matches the JSON', lines[0] == 'OFF' and len(vs) == len(ref) and fs == doc['faces'] and all(abs(a - float(b)) < 1e-14 for v, w in zip(vs, ref) for a, b in zip(v, w)))
    items = {}
    for it, t, ok, note in RESULTS: items.setdefault(it, []).append(ok)
    w = max(len(i) for i in items)
    print('DICTO math-data dataset · check.py · Created by DICTO · dictospheres.com')
    print(f"{'item'.ljust(w)}  tests  result")
    for it, oks in items.items(): print(f"{it.ljust(w)}  {len(oks):5d}  {'PASS' if all(oks) else 'FAIL'}")
    bad = [(it, t, note) for it, t, ok, note in RESULTS if not ok]
    for it, t, note in bad: print('FAIL', it, '-', t, note)
    print(f'TOTAL: {len(RESULTS)} checks, {len(RESULTS) - len(bad)} passed, {len(bad)} failed; '
          f'{len(solids)} solids, {len(glob.glob(os.path.join(HERE, "packings", "*.json")))} packings (fills), '
          f'{len(glob.glob(os.path.join(HERE, "packings-nonfilling", "*.json")))} packings (not fills)')
    if '-v' in sys.argv:
        for it, t, ok, note in RESULTS: print('PASS' if ok else 'FAIL', it, '|', t, '|', note)
    sys.exit(0 if not bad else 1)


if __name__ == '__main__':
    main()
