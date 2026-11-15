# Non-heart Vacuus of the two golden 4-polytopes of "Silent Running: Twisted Silence" (DICTO 16 Nov 2026), EXACT in Q(sqrt5).
#   A = hull of the 20 permutations of (phi^2, phi^2, phi^2, phi, 0);  B = hull of the 30 permutations of (phi^2, phi^2, 1, 1, 0)
#   control: the n = 5 permutohedron, perms of (0,1,2,3,4) (#105: 150 ridges on 65 plates).
# The Vacuus (#105): the central plates = the hyperplanes through the centre spanned by each ridge (2-face); a slice = polytope cut by one.
# Steps: facets from the Rado faces x_S = min (every permutation-orbit polytope is a generalised permutohedron), checked against a float
# hull; edges and ridges from the facet incidences; plate normal = exact null vector; full symmetry group = every vertex permutation
# that keeps the centred Gram matrix (exact backtracking, so any symmetry beyond Sym5 would show); orbits of plates; one exact slice per
# orbit with its vertices, edges and faces (side lengths, angles and shape names, all exact).
# The Q5 class, Rado facets and edge test are taken from studies/2026-11-15-golden-a4-candidate/scripts/silent_render.py (same project).
# Run from the study folder: python scripts/vacuus_exact.py   -> data/vacuus-exact.txt, data/vacuus-exact.json; ends "FINAL ok".
import itertools, json, sys
from fractions import Fraction as Fr
import numpy as np
from scipy.spatial import ConvexHull
class Q5:
    __slots__ = ('a', 'b')
    def __init__(s, a, b=0): s.a, s.b = Fr(a), Fr(b)
    def __add__(s, o): o = o if isinstance(o, Q5) else Q5(o); return Q5(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __neg__(s): return Q5(-s.a, -s.b)
    def __sub__(s, o): return s + (-(o if isinstance(o, Q5) else Q5(o)))
    def __rsub__(s, o): return Q5(o) - s
    def __mul__(s, o): o = o if isinstance(o, Q5) else Q5(o); return Q5(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def inv(s): d = s.a * s.a - 5 * s.b * s.b; assert d != 0; return Q5(s.a / d, -s.b / d)
    def __truediv__(s, o): return s * (o if isinstance(o, Q5) else Q5(o)).inv()
    def zero(s): return s.a == 0 and s.b == 0
    def sign(s):
        if s.zero(): return 0
        sa, sb = (s.a > 0) - (s.a < 0), (s.b > 0) - (s.b < 0)
        if sa >= 0 and sb >= 0: return 1
        if sa <= 0 and sb <= 0: return -1
        return sa if s.a * s.a > 5 * s.b * s.b else sb
    def __eq__(s, o): return (s - o).zero()
    def __lt__(s, o): return (s - o).sign() < 0
    def __hash__(s): return hash((s.a, s.b))
    def __float__(s): return float(s.a) + float(s.b) * 5 ** 0.5
    def key(s): return (s.a, s.b)
    def __repr__(s):
        if s.b == 0: return str(s.a)
        if s.a == 0: return f'{s.b}*sqrt5'
        return f'{s.a}{"+" if s.b > 0 else "-"}{abs(s.b)}*sqrt5'
Z = Q5(0); PHI = Q5(Fr(1, 2), Fr(1, 2)); PHI2 = PHI * PHI
assert PHI2 == PHI + 1
def dot(u, v): return sum((x * y for x, y in zip(u, v)), Q5(0))
def sub(u, v): return [x - y for x, y in zip(u, v)]
def rref(rows):
    M = [list(r) for r in rows]; r = 0; piv = []; n = len(M[0]) if M else 0
    for c in range(n):
        p = next((i for i in range(r, len(M)) if not M[i][c].zero()), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]; iv = M[r][c].inv(); M[r] = [x * iv for x in M[r]]
        for i in range(len(M)):
            if i != r and not M[i][c].zero():
                f = M[i][c]; M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        piv.append(c); r += 1
    return M[:r], piv
def rank(rows): return len(rref(rows)[0]) if rows else 0
def affdim(P): return rank([sub(p, P[0]) for p in P[1:]]) if len(P) > 1 else 0
def nullvec(rows, n=5):
    R, piv = rref(rows); free = [c for c in range(n) if c not in piv]; assert len(free) == 1, ('null space not 1-dim', free)
    f = free[0]; v = [Q5(0)] * n; v[f] = Q5(1)
    for i, c in enumerate(piv): v[c] = -R[i][f]
    k = next(i for i in range(n) if not v[i].zero()); s = v[k].inv(); return [x * s for x in v]   # first nonzero entry = 1
# ------------------------------------------------------------------ readable exact numbers
def q5sqrt(q):
    """p + q sqrt5 with (p + q sqrt5)^2 = q, p + q sqrt5 > 0, or None."""
    a, b = q.a, q.b; N = a * a - 5 * b * b
    def rsqrt(x):
        if x < 0: return None
        n, d = x.numerator, x.denominator; rn, rd = int(round(n ** 0.5)), int(round(d ** 0.5))
        for u in (rn - 1, rn, rn + 1):
            for w in (rd - 1, rd, rd + 1):
                if u >= 0 and w > 0 and Fr(u, w) * Fr(u, w) == x: return Fr(u, w)
        return None
    s = rsqrt(N)
    if s is None: return None
    for p2 in ((a + s) / 2, (a - s) / 2):
        p = rsqrt(p2)
        if p is None: continue
        for pp in (p, -p):
            if pp != 0: qq = b / (2 * pp)
            elif b == 0: qq = rsqrt((a) / 5) if a >= 0 else None
            else: continue
            if qq is None: continue
            r = Q5(pp, qq)
            if r * r == q and r.sign() > 0: return r
    return None
def phiform(r):   # p + q sqrt5 = (p - q) + 2q phi
    u, v = r.a - r.b, 2 * r.b
    t = []
    if u != 0: t.append(str(u))
    if v != 0: t.append(('' if v == 1 else '-' if v == -1 else str(v)) + 'φ')
    s = ' + '.join(t).replace('+ -', '- ') if t else '0'
    return s
def _pw(x, k):
    r = Q5(1)
    for _ in range(k): r = r * x
    return r
def _phipow(k): return '' if k == 0 else 'φ' if k == 1 else 'φ' + '⁰¹²³⁴⁵⁶⁷⁸⁹'[k]
def length(q2):
    """Readable exact length from the squared length q2: first as (rational) x phi^k x sqrt(m), else (u + v phi) sqrt(m), else sqrt(...)."""
    tags = ((1, ''), (2, '√2'), (3, '√3'), (6, '√6'), (5, '√5'), (10, '√10'), (15, '√15'), (30, '√30'))
    for m, tag in tags:
        r = q5sqrt(q2 / m)
        if r is None: continue
        for k in sorted(range(-4, 5), key=abs):
            t = r / _pw(PHI if k >= 0 else PHI.inv(), abs(k))
            if t.b != 0: continue
            num, den = t.a.numerator, t.a.denominator
            top = (str(num) if num != 1 or (k <= 0 and not tag) else '') + _phipow(max(k, 0)) + tag
            bot = (str(den) if den != 1 else '') + _phipow(max(-k, 0))
            if not bot: return top
            return f'{top}/' + (f'({bot})' if (den != 1 and k < 0) else bot)
    for m, tag in tags:
        r = q5sqrt(q2 / m)
        if r is not None: s = phiform(r); return f'({s}){tag}' if tag else s
    if q2.b == 0:   # rational, not a square in Q(sqrt5): u sqrt(w) / d with w squarefree
        n, d = q2.a.numerator * q2.a.denominator, q2.a.denominator; u, w = 1, n; f = 2
        while f * f <= w:
            while w % (f * f) == 0: w //= f * f; u *= f
            f += 1
        g = __import__('math').gcd(u, d); u, d = u // g, d // g
        return (str(u) if u != 1 else '') + f'√{w}' + (f'/{d}' if d != 1 else '')
    d = q2.a.denominator * q2.b.denominator // __import__('math').gcd(q2.a.denominator, q2.b.denominator)
    a, b = int(q2.a * d), int(q2.b * d)
    inner = f'{a} {"+" if b > 0 else "−"} {"" if abs(b) == 1 else abs(b)}√5'
    return f'√({inner})' if d == 1 else f'√(({inner})/{d})'
def canon_sides(sides):
    """Side lengths of a polygon read from the start and direction that give the smallest sequence (so equal shapes print alike)."""
    k = len(sides); best = None
    for seq in (sides, sides[::-1]):
        for t in range(k):
            r = seq[t:] + seq[:t]; key = tuple((float(x), x.key()) for x in r)
            if best is None or key < best[0]: best = (key, r)
    return best[1]
# ------------------------------------------------------------------ polytope: facets, edges, ridges (exact)
def build(seed):
    seed = tuple(x if isinstance(x, Q5) else Q5(x) for x in seed)
    V = sorted({tuple(p) for p in itertools.permutations(seed)}, key=lambda v: tuple(float(x) for x in v))
    V = [list(v) for v in V]; n = len(V)
    c = [sum((v[k] for v in V), Q5(0)) / n for k in range(5)]
    facets = []
    for k in range(1, 5):
        for S in itertools.combinations(range(5), k):
            sums = [sum((v[i] for i in S), Q5(0)) for v in V]; m = min(sums)
            F = frozenset(i for i in range(n) if sums[i] == m)
            if affdim([V[i] for i in F]) == 3: facets.append((S, m, F))
    Bm = np.linalg.svd(np.eye(5) - np.ones((5, 5)) / 5)[0][:, :4]
    X = np.array([[float(x) for x in v] for v in V]); X = (X - X.mean(0)) @ Bm
    h = ConvexHull(X); nf = len({tuple(np.round(e, 7)) for e in h.equations}); assert nf == len(facets), ('float hull disagrees', nf, len(facets))
    inc = [set(fi for fi, f in enumerate(facets) if i in f[2]) for i in range(n)]
    edges = []
    for i, j in itertools.combinations(range(n), 2):
        cm = inc[i] & inc[j]
        if len(cm) >= 3 and frozenset.intersection(*[facets[f][2] for f in cm]) == {i, j}: edges.append((i, j))
    ridges = {}
    for a, b in itertools.combinations(range(len(facets)), 2):
        I = facets[a][2] & facets[b][2]
        if len(I) >= 3 and affdim([V[i] for i in I]) == 2: ridges.setdefault(I, []).append((a, b))
    assert all(len(v) == 1 for v in ridges.values()), 'a ridge lies on more than two facets'
    assert n - len(edges) + len(ridges) - len(facets) == 0, 'Euler 4D'
    return V, c, facets, edges, list(ridges)
def plate(V, c, R):
    P = [sub(V[i], c) for i in R]; base = [P[0]]
    for p in P[1:]:
        if rank(base + [p]) > len(base): base.append(p)
        if len(base) == 3: break
    assert len(base) == 3, 'centre lies in the ridge plane'
    return tuple(x.key() for x in nullvec([[Q5(1)] * 5] + base))
# ------------------------------------------------------------------ symmetry group (exact, as vertex permutations keeping the Gram matrix)
def symmetry_group(V, c):
    P = [sub(v, c) for v in V]; n = len(P)
    G = [[dot(P[i], P[j]).key() for j in range(n)] for i in range(n)]
    base = [0]
    for i in range(n):
        if rank([P[b] for b in base] + [P[i]]) > len(base): base.append(i)
        if len(base) == 4: break
    lut = {tuple(G[i][b] for b in base): i for i in range(n)}; assert len(lut) == n
    out = []
    def extend(img):
        k = len(img)
        if k == 4:
            perm = []
            for i in range(n):
                key = tuple(G[i][b] for b in base)   # image w of v_i must have <w, img_k> = <v_i, base_k>; find it among the vertices
                w = next((j for j in range(n) if tuple(G[j][m] for m in img) == key), None)
                if w is None: return
                perm.append(w)
            if len(set(perm)) == n and all(G[perm[i]][perm[j]] == G[i][j] for i in range(n) for j in range(i, n)): out.append(tuple(perm))
            return
        for j in range(n):
            if j in img: continue
            if G[j][j] != G[base[k]][base[k]]: continue
            if all(G[j][img[m]] == G[base[k]][base[m]] for m in range(k)): extend(img + [j])
    extend([])
    return out
def centrally_symmetric(V, c):
    S = {tuple(x.key() for x in v) for v in V}
    return all(tuple((2 * c[k] - v[k]).key() for k in range(5)) in S for v in V)
# ------------------------------------------------------------------ one exact slice
def slice_of(V, c, facets, edges, nrm):
    N = [Q5(*k) for k in nrm]; h = [dot(N, sub(v, c)) for v in V]
    pts, origin = [], []
    for i, v in enumerate(V):
        if h[i].zero(): pts.append(v); origin.append(('vertex', i))
    for i, j in edges:
        if h[i].sign() * h[j].sign() < 0:
            t = h[i] / (h[i] - h[j]); pts.append([x + t * (y - x) for x, y in zip(V[i], V[j])]); origin.append(('edge', i, j))
    assert affdim(pts) == 3
    faces = {}
    for fi, (S, m, F) in enumerate(facets):
        on = frozenset(k for k, p in enumerate(pts) if sum((p[i] for i in S), Q5(0)) == m)
        if len(on) >= 3 and affdim([pts[k] for k in on]) == 2: faces.setdefault(on, []).append(fi)
    fl = list(faces)
    sedges = set()
    for a, b in itertools.combinations(fl, 2):
        I = a & b
        if len(I) == 2: sedges.add(tuple(sorted(I)))
    nv, ne, nf = len(pts), len(sedges), len(fl); assert nv - ne + nf == 2, ('Euler 3D', nv, ne, nf)
    assert all(any(k in e for e in sedges) for k in range(nv))
    return pts, origin, fl, faces, sorted(sedges)
def cycle(F, sedges):
    adj = {k: [] for k in F}
    for i, j in sedges:
        if i in F and j in F: adj[i].append(j); adj[j].append(i)
    assert all(len(v) == 2 for v in adj.values()), 'face boundary not a cycle'
    cyc = [min(F)]; prev = None
    while len(cyc) < len(F):
        nx = [x for x in adj[cyc[-1]] if x != prev and x not in cyc][0]; prev = cyc[-1]; cyc.append(nx)
    return cyc
def describe_face(P):
    k = len(P); sides = [dot(sub(P[(t + 1) % k], P[t]), sub(P[(t + 1) % k], P[t])) for t in range(k)]
    angs = []   # exact signed cos^2 of each corner angle
    for t in range(k):
        u, w = sub(P[t - 1], P[t]), sub(P[(t + 1) % k], P[t]); d = dot(u, w)
        angs.append((d.sign(), (d * d / (dot(u, u) * dot(w, w))).key()))
    L = [length(s) for s in canon_sides(sides)]; eqs = len(set(s.key() for s in sides)) == 1; eqa = len(set(angs)) == 1
    base = {3: 'triangle', 4: 'quadrilateral', 5: 'pentagon', 6: 'hexagon', 7: 'heptagon', 8: 'octagon'}.get(k, f'{k}-gon')
    if k == 3:
        nm = 'equilateral triangle' if eqs else ('isosceles triangle' if len(set(s.key() for s in sides)) == 2 else 'scalene triangle')
        if any(a == (0, (Fr(0), Fr(0))) for a in angs): nm += ' (right-angled)'
    elif k == 4:
        if eqa: nm = 'square' if eqs else 'rectangle'
        elif eqs: nm = 'rhombus'
        else:
            par = [rank([sub(P[1], P[0]), sub(P[3], P[2])]) == 1, rank([sub(P[2], P[1]), sub(P[0], P[3])]) == 1]
            nm = 'parallelogram' if all(par) else ('trapezoid' + (' (isosceles)' if (sides[1] == sides[3] if par[0] else sides[0] == sides[2]) else '')) if any(par) else 'quadrilateral'
    else:
        nm = ('regular ' if eqs and eqa else 'equiangular ' if eqa else 'equal-sided ' if eqs else '') + base
    seq = ', '.join(L)
    if k > 3 and eqa and not eqs and k % 2 == 0 and all(sides[t] == sides[t + 2] for t in range(k - 2)): nm += f', sides {L[0]} and {L[1]} in turn'
    elif not eqs: nm += f', sides {seq}'
    else: nm += f', side {L[0]}'
    return nm, [float(s) ** 0.5 for s in sides]
def plane_basis(nrm):
    n = np.array([float(Q5(*k)) for k in nrm]); one = np.ones(5) / 5 ** 0.5; n = n - (n @ one) * one; n /= np.linalg.norm(n)
    B = []
    for e in np.eye(5):
        v = e - (e @ one) * one - (e @ n) * n
        for b in B: v -= (v @ b) * b
        if np.linalg.norm(v) > 1e-6 and len(B) < 3: B.append(v / np.linalg.norm(v))
    return np.array(B), n
def orbits(items, act):
    seen, orbs = set(), []
    for it in items:
        if it in seen: continue
        o = {it}; stack = [it]
        while stack:
            x = stack.pop()
            for y in act(x):
                if y not in o: o.add(y); stack.append(y)
        seen |= o; orbs.append(o)
    return orbs
def cellname(V, F, edges, ridges):
    nv = len(F); Ed = [(i, j) for i, j in edges if i in F and j in F]; ks = sorted(len(R) for R in ridges if R <= F)
    el = {dot(sub(V[i], V[j]), sub(V[i], V[j])).key() for i, j in Ed}
    if nv == 4: return 'tetrahedron'
    if nv == 6 and len(ks) == 8: return 'octahedron'
    if nv == 6 and len(ks) == 5: return 'triangular prism'
    if nv == 12 and ks == [3] * 4 + [6] * 4: return 'truncated tetrahedron'
    if nv == 12 and ks == [3] * 8 + [4] * 6: return 'cuboctahedron'
    if nv == 24 and ks == [4] * 6 + [6] * 8: return 'truncated octahedron'
    if nv == 12 and ks == [4] * 6 + [6] * 2: return 'hexagonal prism'
    if nv == 8 and ks == [4] * 6: return 'cube'
    return f'cell with {nv} corners'
def analyse(label, seed, expect, out, js):
    V, c, facets, edges, ridges = build(seed)
    nV, nE, nR, nF = len(V), len(edges), len(ridges), len(facets)
    cells = {}
    for S, m, F in facets: nm = cellname(V, F, edges, ridges); cells[nm] = cells.get(nm, 0) + 1
    plates = {}
    for R in ridges: plates.setdefault(plate(V, c, R), []).append(R)
    G = symmetry_group(V, c); cs = centrally_symmetric(V, c)
    out.append(f'== {label}\n  corners {nV}, edges {nE}, 2-faces (ridges) {nR}, cells {nF}: ' + ', '.join(f'{k} {nm}' for nm, k in sorted(cells.items(), key=lambda t: -t[1]))
               + f'\n  centrally symmetric: {cs}; symmetry group order (exact, all isometries fixing the centre): {len(G)}'
               + f'\n  distinct central plates spanned by the ridges: {len(plates)}; ridges per plate: ' + ', '.join(f'{k} on {v}' for k, v in sorted(_count(len(r) for r in plates.values()).items())))
    if expect: assert (nV, nE, nR, nF, len(plates)) == expect, (label, (nV, nE, nR, nF, len(plates)), expect)
    # orbits of plates under the full group: act on the normal through the vertex permutation (exact)
    # orbits: the group acts on ridge vertex sets; each ridge spans one plate
    rid_of = {R: p for p, Rs in plates.items() for R in Rs}
    ridge_orbs = orbits(list(ridges), lambda R: [frozenset(g[i] for i in R) for g in G])
    plate_orbs = []
    for ro in ridge_orbs:
        ps = {rid_of[R] for R in ro}
        if not any(ps & set(po) for po in plate_orbs): plate_orbs.append(sorted(ps))
    assert sum(len(po) for po in plate_orbs) == len(plates)
    jsol = {'label': label, 'V': [[float(x) for x in v] for v in V], 'centre': [float(x) for x in c], 'edges': edges,
            'ridges': [sorted(R) for R in ridges], 'cells': cells, 'group_order': len(G), 'central_symmetry': cs,
            'n_plates': len(plates), 'orbits': []}
    for oi, po in enumerate(plate_orbs):
        rep = po[0]; R = plates[rep][0]
        ridge_kinds = _count(len(Rr) for p in po for Rr in plates[p])
        pts, origin, fl, faces, sedges = slice_of(V, c, facets, edges, rep)
        # which face of the slice is the plate's own ridge(s)
        P_on = {}
        for Rr in plates[rep]:
            idx = frozenset(k for k, o in enumerate(origin) if o[0] == 'vertex' and o[1] in Rr); assert idx in faces, 'ridge is not a face of its slice'; P_on[idx] = True
        fdesc = []; ftypes = {}
        for F in fl:
            cyc = cycle(F, sedges); nm, sl = describe_face([pts[k] for k in cyc])
            srcs = sorted({cellname(V, facets[fi][2], edges, ridges) for fi in faces[F]})
            tag = nm + ('  [the plate\'s ridge]' if F in P_on else '') + f'  (cut from {" / ".join(srcs)})'
            ftypes[tag] = ftypes.get(tag, 0) + 1
            fdesc.append({'cycle': cyc, 'name': nm, 'ridge': F in P_on, 'cells': [facets[fi][0] for fi in faces[F]], 'cellnames': srcs})
        nverts_old = sum(1 for o in origin if o[0] == 'vertex')
        B3, nn = plane_basis(rep)
        X3 = np.array([[float(x) for x in p] for p in pts]); X3 = (X3 - np.array([float(x) for x in c])) @ B3.T
        kinds = sorted(len(F) for F in fl)
        rn = _ridge_shape(V, R)
        line = (f'  orbit {oi + 1}: {len(po)} plates, ridge = {rn}; slice: {len(pts)} corners ({nverts_old} corners of the solid, '
                f'{len(pts) - nverts_old} edge crossings), {len(sedges)} edges, {len(fl)} faces ' + str(dict(sorted(_count(kinds).items()))) + ' (sides: count)')
        out.append(line)
        for t, k in sorted(ftypes.items(), key=lambda t: (-t[1], t[0])): out.append(f'      {k} x {t}')
        jsol['orbits'].append({'n_plates': len(po), 'ridge_shape': rn, 'ridge_vertices': sorted(R), 'normal': [float(Q5(*k)) for k in rep],
                               'normal_exact': [repr(Q5(*k)) for k in rep],
                               'all_plates_ridges': [sorted(plates[p][0]) for p in po],
                               'slice': {'X3': X3.tolist(), 'basis': B3.tolist(), 'origin': origin, 'edges': sedges,
                                         'faces': fdesc, 'counts': [len(pts), len(sedges), len(fl)], 'face_types': ftypes}})
    js[label] = jsol
    return V, plates, G, plate_orbs
def _count(it):
    d = {}
    for x in it: d[x] = d.get(x, 0) + 1
    return d
def _ridge_shape(V, R):
    R = sorted(R); P = [V[i] for i in R]
    # order the ridge polygon by angle in its plane (exact names from describe_face)
    X = np.array([[float(x) for x in p] for p in P]); m = X.mean(0); U, S_, Wt = np.linalg.svd(X - m); a = np.arctan2((X - m) @ Wt[1], (X - m) @ Wt[0])
    return describe_face([P[k] for k in np.argsort(a)])[0]
if __name__ == '__main__':
    out, js = [], {}
    print('PROGRESS 0.00 start', flush=True)
    analyse('A: perms of (φ², φ², φ², φ, 0)', (PHI2, PHI2, PHI2, PHI, Z), (20, 40, 30, 10, 30), out, js); print('PROGRESS 0.20 A', flush=True)
    analyse('B: perms of (φ², φ², 1, 1, 0)', (PHI2, PHI2, Q5(1), Q5(1), Z), (30, 90, 80, 20, 80), out, js); print('PROGRESS 0.45 B', flush=True)
    analyse('CONTROL permutohedron n=5, perms of (0,1,2,3,4)', tuple(Q5(k) for k in range(5)), (120, 240, 150, 30, 65), out, js)
    print('PROGRESS 0.95 permutohedron', flush=True)
    # controls on the group and the background claims
    assert js['A: perms of (φ², φ², φ², φ, 0)']['group_order'] == 120 and js['B: perms of (φ², φ², 1, 1, 0)']['group_order'] == 120
    assert js['CONTROL permutohedron n=5, perms of (0,1,2,3,4)']['group_order'] == 240
    assert not js['A: perms of (φ², φ², φ², φ, 0)']['central_symmetry'] and not js['B: perms of (φ², φ², 1, 1, 0)']['central_symmetry']
    txt = '\n'.join(out); print(txt, flush=True)
    open('data/vacuus-exact.txt', 'w').write('# exact Vacuus analysis in Q(sqrt5), scripts/vacuus_exact.py; DICTO · dictospheres.com\n' + txt + '\n')
    json.dump(js, open('data/vacuus-exact.json', 'w'), ensure_ascii=False)
    print('FINAL ok', flush=True)
