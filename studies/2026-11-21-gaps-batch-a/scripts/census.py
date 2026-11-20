# Halo and star census (DICTO 2026-11-02), one shape per call. For a shape of the Star Cores book:
#  - centre halo: hull of the tips t x (foot of the perpendicular from the centre O to each face plane) [#78/#79]; up to similarity the
#    same for every t, so computed once (t = 1: the hull of the feet);
#  - polar halo (convex shapes): hull of the polar points rho^2 N / (N.p) of the face planes [#79 polar spikes]; up to similarity the same
#    for every rho, i.e. the polar reciprocal of the solid about O;
#  - stars, t = 2 and t = phi: the solid with each face pyramid turned outwards (apex t x foot), as a surface: the triangles (edge of a
#    face, its tip), coplanar neighbours merged.
# Exact in Q(sqrt5) (incl. Q) via a small field class: the hull facets of each halo are checked exactly (every facet point on the
# facet plane, every other point strictly inside), and star faces merged only when exactly coplanar. Shapes in other fields (Q(t),
# Q(2^(1/3)), Q(sqrt3)): float64 only (flagged). Corners, faces by sides, symmetry (orthogonal maps of the corner set, 1e-7) and a
# similarity key (sorted squared corner distances over the largest, 1e-7) are written to data/shapes/<slug>.json.
# Usage: census.py <dataset dir> <slug> <out dir>
import json, os, sys, math, itertools, numpy as np
from fractions import Fraction as Fr
from scipy.spatial import ConvexHull
DS, SLUG, OUT = sys.argv[1:4]; PHI = (1 + 5 ** .5) / 2

class Q5:
    __slots__ = ('a', 'b')
    def __init__(s, a, b=0): s.a = Fr(a); s.b = Fr(b)
    def __add__(s, o): o = o if isinstance(o, Q5) else Q5(o); return Q5(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __sub__(s, o): o = o if isinstance(o, Q5) else Q5(o); return Q5(s.a - o.a, s.b - o.b)
    def __neg__(s): return Q5(-s.a, -s.b)
    def __mul__(s, o): o = o if isinstance(o, Q5) else Q5(o); return Q5(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def __truediv__(s, o):
        o = o if isinstance(o, Q5) else Q5(o); n = o.a * o.a - 5 * o.b * o.b
        return Q5((s.a * o.a - 5 * s.b * o.b) / n, (s.b * o.a - s.a * o.b) / n)
    def sign(s):
        a, b = s.a, s.b
        if b == 0: return (a > 0) - (a < 0)
        if a == 0: return (b > 0) - (b < 0)
        if a > 0 and b > 0: return 1
        if a < 0 and b < 0: return -1
        d = a * a - 5 * b * b
        return ((d > 0) - (d < 0)) if a > 0 else -((d > 0) - (d < 0))
    def __float__(s): return float(s.a) + float(s.b) * 5 ** .5
    def __eq__(s, o): o = o if isinstance(o, Q5) else Q5(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def __str__(s): return f'{s.a}' if s.b == 0 else f'{s.a} + ({s.b})*sqrt(5)'
def parse(s):
    import sympy as sp
    r = sp.sqrt(5); e = sp.expand(sp.sympify(s, locals={'sqrt': sp.sqrt})); b = e.coeff(r); a = sp.expand(e - b * r)
    if not (a.is_Rational and b.is_Rational): raise ValueError('not in Q(sqrt5): ' + s)
    return Q5(Fr(int(a.p), int(a.q)), Fr(int(b.p), int(b.q)))
def vsub(p, q): return [p[i] - q[i] for i in range(3)]
def dot(p, q): return p[0] * q[0] + p[1] * q[1] + p[2] * q[2]
def cross(p, q): return [p[1] * q[2] - p[2] * q[1], p[2] * q[0] - p[0] * q[2], p[0] * q[1] - p[1] * q[0]]
def fl(P): return np.array([[float(x) for x in p] for p in P])

def sym_group(P, tol=1e-7):
    P = P - P.mean(0); r = np.linalg.norm(P, axis=1); scale = r.max(); P = P / scale; r = r / scale
    order = np.argsort(-r); i1 = order[0]; same1 = [i for i in range(len(P)) if abs(r[i] - r[i1]) < tol]
    i2 = next(i for i in order if np.linalg.norm(np.cross(P[i1], P[i])) > 1e-3)
    same2 = [i for i in range(len(P)) if abs(r[i] - r[i2]) < tol]
    B = np.array([P[i1], P[i2], np.cross(P[i1], P[i2])]); d12 = np.linalg.norm(P[i1] - P[i2]); G = []
    from scipy.spatial import cKDTree
    T = cKDTree(P)
    for a in same1:
        for b in same2:
            if abs(np.linalg.norm(P[a] - P[b]) - d12) > tol: continue
            for sg in (1, -1):
                C = np.array([P[a], P[b], sg * np.cross(P[a], P[b])]); M = np.linalg.solve(B, C)
                if not np.allclose(M @ M.T, np.eye(3), atol=1e-6): continue
                if np.all(T.query(P @ M)[0] < tol * 10): G.append(M.T)
    return G
def sym_name(G):
    g = len(G); rot = [M for M in G if np.linalg.det(M) > 0]; r = len(rot)
    inv = any(np.allclose(M, -np.eye(3), atol=1e-6) for M in G)
    mir = sum(1 for M in G if np.linalg.det(M) < 0 and abs(np.trace(M) - 1) < 1e-6)
    def ordr(M):
        c = max(-1, min(1, (np.trace(M) - 1) / 2)); th = math.acos(c)
        return 1 if th < 1e-6 else round(2 * math.pi / th)
    n = max(ordr(M) for M in rot)
    if r == 60: return 'Ih' if g == 120 else 'I'
    if r == 24: return 'Oh' if g == 48 else 'O'
    if r == 12 and n == 3 and sum(1 for M in rot if ordr(M) == 3) == 8: return ('Th' if inv else 'Td') if g == 24 else 'T'
    if g == 1: return 'C1'
    if r == 1: return 'Ci' if inv else 'Cs'
    if g == r: return f'C{n}' if r == n else f'D{n}'
    if r == n: return f'C{n}v' if mir == n else f'C{n}h' if mir == 1 else f'S{2 * n}'
    return f'D{n}h' if mir == n + 1 else f'D{n}d'
def sim_key(P):
    P = P - P.mean(0); D = ((P[:, None] - P[None]) ** 2).sum(-1); v = np.sort(D[np.triu_indices(len(P), 1)]); v = v / v[-1]
    return [round(float(x), 7) for x in v]

def halo(PE, PF, exact):
    """hull of points; facets merged by plane; exact check when PE given. Returns corners (indices), faces (lists of corner indices)."""
    H = ConvexHull(PF); groups = {}
    for sm, eq in zip(H.simplices, H.equations): groups.setdefault(tuple(np.round(eq / np.abs(eq[:3]).max(), 7)), (eq, set()))[1].update(sm.tolist())
    faces = []; ok = True
    allidx = set(range(len(PF)))
    for eq, ids in groups.values():
        ids = sorted(ids)
        # all points on this plane (numerically)
        on = [i for i in range(len(PF)) if abs(eq[:3] @ PF[i] + eq[3]) < 1e-9 * max(1, np.abs(PF).max())]
        if exact:
            p0 = PE[on[0]]; nrm = None
            for a, b in itertools.combinations(on[1:], 2):
                c = cross(vsub(PE[a], p0), vsub(PE[b], p0))
                if any(x.sign() != 0 for x in c): nrm = c; break
            off = dot(nrm, p0)
            if not all((dot(nrm, PE[i]) - off).sign() == 0 for i in on): ok = False
            sgn = {(dot(nrm, PE[i]) - off).sign() for i in allidx - set(on)}
            if len(sgn - {0}) > 1 or 0 in sgn: ok = False
        # polygon corners (2D hull of the points on the plane)
        n = eq[:3]; u = np.cross(n, [1, 0, 0] if abs(n[0]) < .9 else [0, 1, 0]); u /= np.linalg.norm(u); w = np.cross(n, u)
        Q = np.array([[PF[i] @ u, PF[i] @ w] for i in on]); h2 = ConvexHull(Q)
        faces.append([on[k] for k in h2.vertices])
    corners = sorted({i for f in faces for i in f})
    return corners, faces, ok
def summarize(PF, corners, faces, extra):
    C = PF[corners]; G = sym_group(C)
    sides = {}
    for f in faces: sides[len(f)] = sides.get(len(f), 0) + 1
    E = {tuple(sorted((f[k], f[(k + 1) % len(f)]))) for f in faces for k in range(len(f))}
    return dict(corners=len(corners), edges=len(E), faces=len(faces), faces_by_sides=dict(sorted(sides.items())), symmetry=sym_name(G),
                symmetry_order=len(G), key=sim_key(C), points=C.tolist(), face_list=[[corners.index(i) for i in f] for f in faces], **extra)

def star(VE, VF, F, t, exact):
    """surface: triangles (a, b, tip_f); coplanar neighbours merged (exactly when exact)."""
    tips_f, tips_e = [], []
    for f in F:
        if exact:
            N = [Q5(0)] * 3
            for k in range(len(f)): N = [x + y for x, y in zip(N, cross(VE[f[k]], VE[f[(k + 1) % len(f)]]))]
            foot = [x * (dot(N, VE[f[0]]) / dot(N, N)) for x in N]; tips_e.append([x * t[1] for x in foot])
        Nf = np.zeros(3)
        for k in range(len(f)): Nf += np.cross(VF[f[k]], VF[f[(k + 1) % len(f)]])
        tips_f.append(t[0] * (Nf @ VF[f[0]]) / (Nf @ Nf) * Nf)
    PF = np.vstack([VF, tips_f]); PE = (list(VE) + tips_e) if exact else None; n0 = len(VF)
    tris = [[f[k], f[(k + 1) % len(f)], n0 + i] for i, f in enumerate(F) for k in range(len(f))]
    def plane(tr):
        a, b, c = PF[tr]; n = np.cross(b - a, c - a); n /= np.linalg.norm(n); return n, n @ a
    E = {}
    for i, tr in enumerate(tris):
        for k in range(3): E.setdefault(tuple(sorted((tr[k], tr[(k + 1) % 3]))), []).append(i)
    par = list(range(len(tris)))
    def fd(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for e, l in E.items():
        if len(l) != 2: continue
        i, j = l; (n1, d1), (n2, d2) = plane(tris[i]), plane(tris[j])
        if np.linalg.norm(n1 - n2) < 1e-9 and abs(d1 - d2) < 1e-9 * max(1, abs(d1)):
            if exact:
                x = [v for v in tris[j] if v not in tris[i]][0]; a, b, c = (PE[v] for v in tris[i])
                if dot(cross(vsub(b, a), vsub(c, a)), vsub(PE[x], a)).sign() != 0: continue
            par[fd(i)] = fd(j)
    groups = {}
    for i in range(len(tris)): groups.setdefault(fd(i), []).append(i)
    faces = []
    for g in groups.values():
        cnt = {}
        for i in g:
            tr = tris[i]
            for k in range(3): e = (tr[k], tr[(k + 1) % 3]); cnt[e] = cnt.get(e, 0) + 1
        bd = [e for e in cnt if (e[1], e[0]) not in cnt]           # directed boundary edges
        nxt = {a: b for a, b in bd}; start = bd[0][0]; loop = [start]; cur = nxt[start]
        while cur != start and len(loop) <= len(bd): loop.append(cur); cur = nxt.get(cur, start)
        crn = [v for k, v in enumerate(loop) if np.linalg.norm(np.cross(PF[v] - PF[loop[k - 1]], PF[loop[(k + 1) % len(loop)]] - PF[v])) > 1e-9]
        faces.append(crn)
    corners = sorted({v for f in faces for v in f})
    return PF, corners, faces

if __name__ == '__main__':
    d = json.load(open(os.path.join(DS, 'solids', SLUG + '.json'))); F = [list(f) for f in d['faces']]
    VF = np.array([[float(x) for x in v['decimal']] for v in d['vertices']])
    exact = d.get('field') in ('Q(sqrt(5))', 'Q')
    VE = None
    if exact:
        VE = [[parse(x) for x in v['exact']] for v in d['vertices']]
        c = [sum((p[i] for p in VE), Q5(0)) / len(VE) for i in range(3)]; VE = [vsub(p, c) for p in VE]
        VF = fl(VE)
    else: VF = VF - VF.mean(0)
    convex = d.get('convex', d.get('checks', {}).get('convex', True))
    res = dict(slug=SLUG, name=d['name'], D=d.get('D') or d.get('dicto_number'), field=d.get('field'), exact=exact, convex=convex)
    # face normals and feet
    feetE, polE, feetF, polF = [], [], [], []
    for f in F:
        Nf = np.zeros(3)
        for k in range(len(f)): Nf += np.cross(VF[f[k]], VF[f[(k + 1) % len(f)]])
        feetF.append((Nf @ VF[f[0]]) / (Nf @ Nf) * Nf); polF.append(Nf / (Nf @ VF[f[0]]))
        if exact:
            N = [Q5(0)] * 3
            for k in range(len(f)): N = [x + y for x, y in zip(N, cross(VE[f[k]], VE[f[(k + 1) % len(f)]]))]
            s = dot(N, VE[f[0]]); feetE.append([x * (s / dot(N, N)) for x in N]); polE.append([x / s for x in N])
    feetF, polF = np.array(feetF), np.array(polF)
    cr, fc, ok = halo(feetE, feetF, exact); res['centre_halo'] = summarize(feetF, cr, fc, dict(exact_facets=ok if exact else None))
    if convex and min((np.cross(VF[f[1]] - VF[f[0]], VF[f[2]] - VF[f[0]]) @ VF[f[0]]) for f in F) > 0:
        cr, fc, ok = halo(polE, polF, exact); res['polar_halo'] = summarize(polF, cr, fc, dict(exact_facets=ok if exact else None))
    for tn, t in (('2', (2.0, Q5(2))), ('phi', (PHI, Q5(Fr(1, 2), Fr(1, 2))))):
        PF, cr, fc = star(VE, VF, F, t, exact); res['star_' + tn] = summarize(PF, cr, fc, dict(exact_merge=exact))
    os.makedirs(os.path.join(OUT, 'shapes'), exist_ok=True)
    json.dump(res, open(os.path.join(OUT, 'shapes', SLUG + '.json'), 'w'), default=float)
    print(SLUG, 'centre', res['centre_halo']['corners'], res['centre_halo']['faces_by_sides'], res['centre_halo']['symmetry'],
          '| polar', (res.get('polar_halo') or {}).get('faces_by_sides'), '| star2', res['star_2']['corners'], res['star_2']['faces'], res['star_2']['symmetry'], flush=True)
