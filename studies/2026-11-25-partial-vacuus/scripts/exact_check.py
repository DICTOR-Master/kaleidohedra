# DICTO · Vacuus-Solids: EXACT check of the special sizes (eleven; the twelfth of the float list is a correction, see below) (26 Nov 2026). With Claude (Anthropic).
# Every number lives in Q(sqrt r) (r = 5 or 2) as a pair of Fractions; floats are used only to FIND candidates (hull combinatorics,
# which face of Q a wall might lie on); every claim printed is then proved by exact arithmetic.
# Solids: Platonic from their standard coordinates; Catalan Q = polar of the Archimedean solid (standard coordinates), so the face
# planes of Q are a.x = 1 for the corners a of the Archimedean solid. P's faces are found exactly (every corner checked on its plane).
# Pit on face f: apex s*p_f, p_f the foot of O on the face plane. Wall through edge (u,v): normal m = (u - s p) x (v - s p).
# Claim checked for each of the 12: for ONE rotation of Q among the 24 axis rotations, every wall plane of P at s is a face plane
# of lam*Q with ONE lam > 0 (exact). Also reported, exactly: how many of Q's faces carry a wall (all = the walls build the core).
# Controls: positive = the two classics (dodecahedron on icosahedron 5-2sqrt5, icosahedron on dodecahedron 3sqrt5-6);
# negative = the same pairs at s +- 1/1000 must FAIL.
import itertools, sys
from fractions import Fraction as Fr
import numpy as np
from scipy.spatial import ConvexHull

class K:
    __slots__ = ('a', 'b', 'r')
    def __init__(s, a, b=0, r=5): s.a = Fr(a); s.b = Fr(b); s.r = r
    def _c(s, o): return o if isinstance(o, K) else K(o, 0, s.r)
    def __add__(s, o): o = s._c(o); return K(s.a + o.a, s.b + o.b, s.r)
    __radd__ = __add__
    def __neg__(s): return K(-s.a, -s.b, s.r)
    def __sub__(s, o): return s + (-s._c(o))
    def __rsub__(s, o): return s._c(o) - s
    def __mul__(s, o): o = s._c(o); return K(s.a * o.a + s.r * s.b * o.b, s.a * o.b + s.b * o.a, s.r)
    __rmul__ = __mul__
    def __truediv__(s, o):
        o = s._c(o); n = o.a * o.a - s.r * o.b * o.b; assert n != 0
        return s * K(o.a / n, -o.b / n, s.r)
    def __rtruediv__(s, o): return s._c(o) / s
    def iszero(s): return s.a == 0 and s.b == 0
    def __eq__(s, o): return (s - s._c(o)).iszero()
    def __float__(s): return float(s.a) + float(s.b) * s.r ** 0.5
    def sign(s):  # exact sign of a + b sqrt r
        a, b, r = s.a, s.b, s.r
        if b == 0: return (a > 0) - (a < 0)
        if a == 0: return (b > 0) - (b < 0)
        if (a > 0) == (b > 0): return 1 if a > 0 else -1
        return (1 if a > 0 else -1) * (1 if a * a > r * b * b else -1)
    def __repr__(s): return f'{s.a}+{s.b}√{s.r}' if s.b else f'{s.a}'

def cross(u, v): return (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])
def dot(u, v): return u[0]*v[0] + u[1]*v[1] + u[2]*v[2]
def sub(u, v): return tuple(a - b for a, b in zip(u, v))
def scl(t, u): return tuple(t * a for a in u)
def flt(u): return np.array([float(x) for x in u])

def solid(name, r):
    P = K(Fr(1, 2), Fr(1, 2), 5)        # phi
    k = lambda a, b=0: K(a, b, r)
    def cyc(t): return [t, (t[1], t[2], t[0]), (t[2], t[0], t[1])]
    def signs(t): return [tuple(x if sg > 0 else -x for x, sg in zip(t, sgn)) for sgn in itertools.product((1, -1), repeat=3)]
    def allp(t): return list(itertools.permutations(t))
    def gen(ts, perm=cyc):
        out = []
        for t in ts:
            for q in perm(t):
                for z in signs(q):
                    if not any(all((a - b).iszero() for a, b in zip(z, w)) for w in out): out.append(z)
        return out
    if r == 5: one, phi = K(1, 0, 5), P
    else: one, phi = K(1, 0, 2), None
    z = one * 0
    if name == 'tetrahedron': return [t for t in gen([(one, one, one)], allp) if sum(float(x) < 0 for x in t) % 2 == 0]
    if name == 'octahedron': return gen([(one, z, z)], allp)
    if name == 'dodecahedron': return gen([(one, one, one), (z, one / phi, phi)])
    if name == 'icosahedron': return gen([(z, one, phi)])
    if name == 'icosidodecahedron': return gen([(z, z, phi), (one / 2, phi / 2, phi * phi / 2)])
    if name == 'truncated dodecahedron': return gen([(z, one / phi, 2 + phi), (one / phi, phi, 2 * phi), (phi, one * 2, phi + 1)])
    if name == 'truncated icosahedron': return gen([(z, one, 3 * phi), (one, 2 + phi, 2 * phi), (phi, one * 2, phi ** 3 if False else phi * phi * phi)])
    if name == 'rhombicosidodecahedron': return gen([(one, one, phi * phi * phi), (phi * phi, phi, 2 * phi), (2 + phi, z, phi * phi)])
    if name == 'truncated icosidodecahedron':
        ip = one / phi
        return gen([(ip, ip, 3 + phi), (2 * ip, phi, 1 + 2 * phi), (ip, phi * phi, -1 + 3 * phi), (2 * phi - 1, one * 2, 2 + phi), (phi, one * 3, 2 * phi)])
    if name == 'truncated cube': return gen([(k(-1, 1), one, one)], allp)
    if name == 'truncated tetrahedron': return [t for t in gen([(one * 3, one, one)], allp) if sum(float(x) < 0 for x in t) % 2 == 0]
    raise KeyError(name)

def faces(V):
    """exact faces of conv(V): list of (corner indices in cyclic order, normal N, d) with N.x = d on the face, N.x < d inside"""
    X = np.array([flt(v) for v in V]); H = ConvexHull(X); out = []; seen = []
    for eq in H.equations:
        n = eq[:3]
        if any(np.allclose(n, m, atol=1e-9) for m in seen): continue
        seen.append(n)
        idx = [i for i in range(len(V)) if abs(X[i] @ n + eq[3]) < 1e-9]
        a, b, c = (V[i] for i in idx[:3]); N = cross(sub(b, a), sub(c, a))
        for t in idx[2:]:   # make sure the first three are not collinear
            if all(x.iszero() for x in N): N = cross(sub(b, a), sub(V[t], a))
        d = dot(N, a)
        if d.sign() < 0: N = scl(-1, N); d = -d
        assert all(dot(N, V[i]) == d for i in idx), 'face not exactly planar'
        assert all((dot(N, V[i]) - d).sign() < 0 for i in range(len(V)) if i not in idx), 'not a face'
        c0 = X[idx].mean(0); e1 = X[idx[0]] - c0; e2 = np.cross(n, e1)
        idx.sort(key=lambda i: np.arctan2((X[i] - c0) @ e2, (X[i] - c0) @ e1))
        out.append((idx, N, d))
    return out

def polar(V): return [scl(1 / d, N) for _, N, d in faces(V)]

FRAMES = []
for perm in itertools.permutations(range(3)):
    for sg in itertools.product((1, -1), repeat=3):
        M = np.zeros((3, 3), int)
        for i, j in enumerate(perm): M[i, j] = sg[i]
        if round(np.linalg.det(M)) == 1: FRAMES.append(M)
def rot(M, v): return tuple(sum((int(M[i, j]) * v[j] for j in range(3) if M[i, j]), v[0] * 0) for i in range(3))

def body(name, r):
    if name in ('tetrahedron', 'octahedron', 'dodecahedron', 'icosahedron'): return solid(name, r)
    arch = {'rhombic triacontahedron': 'icosidodecahedron', 'triakis icosahedron': 'truncated dodecahedron',
            'deltoidal hexecontahedron': 'rhombicosidodecahedron', 'pentakis dodecahedron': 'truncated icosahedron',
            'disdyakis triacontahedron': 'truncated icosidodecahedron', 'triakis octahedron': 'truncated cube',
            'triakis tetrahedron': 'truncated tetrahedron'}[name]
    return polar(solid(arch, r))

def check(Pn, Qn, s, r):
    VP = body(Pn, r); FP = faces(VP); VQ = body(Qn, r); FQ = faces(VQ)
    walls = []
    for idx, N, d in FP:
        p = scl(d / dot(N, N), N); ap = scl(s, p)
        for i, j in zip(idx, idx[1:] + idx[:1]):
            u, v = VP[i], VP[j]; walls.append((cross(sub(u, ap), sub(v, ap)), u))
    best = None
    for M in FRAMES:
        Q = [(rot(M, N), d) for _, N, d in FQ]; Qf = [flt(N) / np.linalg.norm(flt(N)) for N, _ in Q]
        lam = None; hit = set(); ok = True
        for m, u in walls:
            mf = flt(m); mf /= np.linalg.norm(mf)
            cand = [q for q in range(len(Q)) if abs(abs(mf @ Qf[q]) - 1) < 1e-6]
            good = False
            for q in cand:
                w, h = Q[q]
                if not all(x.iszero() for x in cross(m, w)): continue
                i = next(t for t in range(3) if not w[t].iszero()); kk = m[i] / w[i]
                L = dot(m, u) / (kk * h)
                if L.sign() <= 0: continue
                if lam is None: lam = L
                if not (L == lam): continue
                good = True; hit.add(q); break
            if not good: ok = False; break
        if ok: best = (lam, len(hit), len(Q), len(walls), len(FP)); break
    return best

r5 = lambda a, b=0, den=1: K(Fr(a, den), Fr(b, den), 5)
r2 = lambda a, b=0, den=1: K(Fr(a, den), Fr(b, den), 2)
TWELVE = [
    ('dodecahedron', 'icosahedron', r5(5, -2), 5), ('dodecahedron', 'triakis icosahedron', r5(10, -3, 11), 5),
    ('dodecahedron', 'deltoidal hexecontahedron', r5(0, 1, 3), 5), ('icosahedron', 'dodecahedron', r5(-6, 3), 5),
    ('icosahedron', 'pentakis dodecahedron', r5(-9, 6, 11), 5), ('icosahedron', 'deltoidal hexecontahedron', r5(30, -9, 11), 5),
    ('rhombic triacontahedron', 'rhombic triacontahedron', r5(3, -1), 5),
    ('triakis icosahedron', 'deltoidal hexecontahedron', r5(42, -11, 19), 5),
    ('tetrahedron', 'triakis octahedron', r2(9, -6), 2),
    ('octahedron', 'deltoidal hexecontahedron', r5(12, -3, 11), 5), ('octahedron', 'disdyakis triacontahedron', r5(15, -6, 5), 5)]

# CORRECTION (exact, 26 Nov): octahedron / triakis tetrahedron at s = 3/5 was listed as special by the float search, which accepted
# a wall on a face plane of -lam Q. Exactly: 12 walls lie on face planes of Q (lam = 1) and 12 on those of -Q (lam = -1); the
# octahedron is centrally symmetric, Q is not, so no single lam works. Not special; checked below as a control that must FAIL,
# with the Q-or-minus-Q statement proved.
def both_sides(Pn, Qn, s, r):
    VP = body(Pn, r); FP = faces(VP); FQ = faces(body(Qn, r)); lams = set(); n = 0
    for _, N, d in FP: pass
    for idx, N, d in FP:
        p = scl(d / dot(N, N), N); ap = scl(s, p)
        for i, j in zip(idx, idx[1:] + idx[:1]):
            u, v = VP[i], VP[j]; m = cross(sub(u, ap), sub(v, ap))
            for w, h in [(N2, d2) for _, N2, d2 in FQ]:
                if all(x.iszero() for x in cross(m, w)):
                    t = next(t for t in range(3) if not w[t].iszero()); lams.add(repr(dot(m, u) / ((m[t] / w[t]) * h))); n += 1; break
    return n, sorted(lams)
fails = 0
nb, lb = both_sides('octahedron', 'triakis tetrahedron', r2(3, 0, 5), 2)
okc = check('octahedron', 'triakis tetrahedron', r2(3, 0, 5), 2) is None and nb == 24 and lb == ['-1', '1']
print('control (correction): octahedron / triakis tetrahedron at 3/5: one-lam check', 'FAILS (correct)' if okc else 'UNEXPECTED',
      f'; all {nb} walls on face planes of Q or -Q, lam values {lb}', flush=True)
if not okc: fails += 1
print('controls: negative (must fail) at s +- 1/1000 for the two classics', flush=True)
for Pn, Qn, s, r in TWELVE[:1] + TWELVE[3:4]:
    for e in (Fr(1, 1000), Fr(-1, 1000)):
        res = check(Pn, Qn, s + e, r); print(f'  {Pn} on {Qn} at s{"+" if e > 0 else "-"}1/1000:', 'FAILS (good)' if res is None else 'PASSES (BAD)', flush=True)
        if res is not None: fails += 1
print('the eleven (exact):', flush=True)
for n, (Pn, Qn, s, r) in enumerate(TWELVE):
    res = check(Pn, Qn, s, r)
    c1 = -2 * s.a; c0 = s.a * s.a - r * s.b * s.b      # minimal polynomial of s (monic): x^2 + c1 x + c0, or linear if b = 0
    poly = f'x - {s.a}' if s.b == 0 else f'x^2 + ({c1}) x + ({c0})'
    if res is None: fails += 1; print(f'  FAIL {Pn} on {Qn} s = {s}', flush=True)
    else:
        lam, hit, nq, nw, nf = res
        print(f'  OK {Pn} ({nf} faces, {nw} walls) on {Qn}: s = {s} [{poly}], lam = {lam}; walls on {hit} of {nq} faces of lam Q'
              f' ({"whole core" if hit == nq else "planes only"})', flush=True)
    print(f'PROGRESS {(n + 1) / len(TWELVE):.3f} {Pn} on {Qn}', flush=True)
print('FINAL ok' if fails == 0 else f'FINAL FAIL ({fails})')
