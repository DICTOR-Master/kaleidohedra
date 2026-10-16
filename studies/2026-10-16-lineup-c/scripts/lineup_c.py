# Line-up C (DICTO 2026-10-16, from Fable's advice on P4): the Spheres of Dharma with the icosahedron 3·I (the truncated icosahedron
# with its 12 caps restored) as the seventh station instead of the Hecatodihedron. Step 1, all exact in Q(sqrt5):
#   the chain I ⊂ ID ⊂ D ⊂ TI ⊂ 3·I ⊂ RT ⊂ I·φ³ (nesting, touching), its polar reversal (unit sphere), and for both toggle settings
#   (rho² = φ²/4 and 3φ²/4) which stations the two cycles share at any turn; then every rho² that makes two stations coincide.
# -> data/lineup-c-step1.txt
import os, io, sys, contextlib, itertools
PD = '/home/dicto/kaleidohedra/studies/2026-10-16-polar-dharma'; here = os.getcwd(); os.chdir(PD)
sys.argv = ['polar.py', 'data/dharma_cycle.json']
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('scripts/polar.py').read())
os.chdir(here)
st = dict(stations); P3 = Q(2, 1)                                   # φ³ = 2 + √5
I3 = [[x * 3 for x in v] for v in st['icosahedron']]
def true_corners(V):                       # drop listed points that lie on a face or edge but are not corners (rank test on the face normals)
    Vf = np.array([[x.f() for x in v] for v in V]); h = ConvexHull(Vf); keep = []
    for i in range(len(V)):
        ns = [e[:3] for e in h.equations if abs(Vf[i] @ e[:3] + e[3]) < 1e-7]
        if np.linalg.matrix_rank(np.array(ns), tol=1e-6) == 3: keep.append(V[i])
    return keep
st = {n: true_corners(V) for n, V in st.items()}; I3 = true_corners(I3)
C = [('I', st['icosahedron']), ('ID', st['icosidodecahedron']), ('D', st['dodecahedron']), ('TI', st['truncated icosahedron']),
     ('3·I', I3), ('RT', st['rhombic triacontahedron']), ('I·φ³', st['icosahedron (phi^3)'])]
key = lambda V: frozenset(tuple((x.a, x.b) for x in v) for v in V)
dot = lambda a, b: sum((a[i] * b[i] for i in range(3)), Q(0))
def planes_exact(V):
    out = []
    for idx in planes(V):
        for i0, i1, i2 in itertools.combinations(idx, 3):
            a, b, c = V[i0], V[i1], V[i2]; u = [b[i] - a[i] for i in range(3)]; w = [c[i] - a[i] for i in range(3)]
            n = [u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]]
            if any(x.f() != 0 for x in n): break
        d = dot(n, a)
        if d.f() < 0: n = [-x for x in n]; d = -d
        out.append((n, d))
    return out
out = ['DICTO · dictospheres.com', 'Line-up C: I ⊂ ID ⊂ D ⊂ TI ⊂ 3·I ⊂ RT ⊂ I·φ³ (exact, Q(√5))', '1. Nesting']
for (n1, A), (n2, B) in zip(C, C[1:]):
    pl = planes_exact(B); side = [[(dot(n, v) - d) for n, d in pl] for v in A]
    inside = all(s.f() <= 1e-12 for row in side for s in row); exact_in = all(not (s.f() > 0) for row in side for s in row)
    touch = sum(1 for row in side if any(s == 0 for s in row))
    out.append(f'  {n1} ⊂ {n2}: inside {inside and exact_in}; {touch} of {len(A)} corners of {n1} on faces of {n2}')
# polar reversal in the unit sphere and recognition by corner count / shape
rev = [(n, polar(V)) for n, V in C]
out.append('2. Polar reversal (unit sphere), outer to inner of the original = inner to outer of the reversed:')
for n, V in reversed(rev): out.append(f'  polar of {n}: {len(V)} corners, {len(planes(V))} faces')
# toggle: which stations coincide, any turn k (scale φ^{3k})
def scaled(V, s): return [[x * s for x in v] for v in V]
powers = {k: (P3 ** k if k >= 0 else Q(1) / (P3 ** -k)) for k in range(-3, 4)} if hasattr(Q, '__pow__') else None
pw = {0: Q(1)}
for k in range(1, 4): pw[k] = pw[k - 1] * P3; pw[-k] = pw[-k + 1] / P3
orig_keys = {(n, k): key(scaled(V, pw[k])) for n, V in C for k in range(-3, 4)}
for label, rho2 in (('ends', Q(3, 1) / 8), ('middle', Q(9, 3) / 8)):
    sh = []
    for n, V in rev:
        kk = key(scaled(V, rho2))
        for (m, k), K in orig_keys.items():
            if kk == K: sh.append(f'polar of {n} = {m}' + (f'·φ^{3 * k}' if k else ''))
    out.append(f'3. Toggle {label} (rho² = {rho2!r}): shared {len(sh)}: ' + '; '.join(sh))
# every rho² making some polar station equal some original station: polar_rho(X) = rho² · polar(X); compare circumradius² ratios
out.append('4. All rho² (up to φ³ turns) that make a pair coincide (shape match, exact):')
def r2(V): return max((dot(v, v) for v in V), key=lambda q: q.f())
cand = {}
for n, V in rev:
    for m, W in C:
        if len(V) != len(W): continue
        t = r2(W) / r2(V)                                              # rho⁴ if rho² · V = W
        # rho² = sqrt(t) must lie in Q(√5): try t = s² with s = a + b√5 by checking candidate s from float and verifying exactly
        sf = t.f() ** 0.5
        for qd in range(1, 400):
            b = round(((sf - round(sf * qd) / qd) if False else 0) * qd) if False else None
        cand.setdefault((n, m), t)
import math
from fractions import Fraction as Fr
def sqrtQ(t):
    f = math.sqrt(t.f())
    for den in range(1, 97):
        for bb in range(-200, 201):
            b = Fr(bb, den); a = Fr(round((f - float(b) * 5 ** .5) * den), den); s = Q(a, b)
            if s * s == t and s.f() > 0: return s
    return None
found = []
for (n, m), t in cand.items():
    s = sqrtQ(t)
    if s is None: continue
    V = scaled(dict(rev)[n], s)
    if key(V) == key(dict(C)[m]): found.append((s.f(), f'rho² = {s!r} ≈ {s.f():.6f}: polar of {n} = {m}'))
for _, line in sorted(found): out.append('  ' + line)
print('\n'.join(out)); open('data/lineup-c-step1.txt', 'w').write('\n'.join(out) + '\n')
