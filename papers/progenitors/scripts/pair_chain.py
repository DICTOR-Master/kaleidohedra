# Progenitors (DICTO 2026-10-16: "imagine the Ogdoecontahedron and its dual as the progenitors of a new cycle"). Step 1, exact in Q(sqrt5):
# the Hecatodihedron H and its polar O (the Ogdoecontahedron, unit sphere) as endless shells of each other, as the icosahedron and dodecahedron
# are in the Chain of Karma: the least s with H ⊂ s·O, the least t with O ⊂ t·H, which corners touch, and the two-step ratio s·t.
# -> data/pair-chain.txt
import os, io, sys, contextlib, itertools
PD = '/home/dicto/kaleidohedra/studies/2026-10-16-polar-dharma'; here = os.getcwd(); os.chdir(PD)
sys.argv = ['polar.py', 'data/dharma_cycle.json']
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('scripts/polar.py').read())
os.chdir(here)
st = dict(stations)
def true_corners(V):
    Vf = np.array([[x.f() for x in v] for v in V]); h = ConvexHull(Vf)
    return [V[i] for i in range(len(V)) if np.linalg.matrix_rank(np.array([e[:3] for e in h.equations if abs(Vf[i] @ e[:3] + e[3]) < 1e-7]), tol=1e-6) == 3]
H = true_corners(st['Hecatodihedron']); O = true_corners(polar(H))
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
def contain(A, B):               # least s with A ⊂ s·B: max over corners of A and faces of B of (n·a)/d; and how many corners of A touch
    pl = planes_exact(B); best = None
    for a in A:
        for n, d in pl:
            r = dot(n, a) / d
            if best is None or r.f() > best.f(): best = r
    touch = sum(1 for a in A if any(dot(n, a) / d == best for n, d in pl))
    return best, touch
s, ts = contain(H, O); t, tt = contain(O, H)
r2 = lambda V: max((dot(v, v) for v in V), key=lambda q: q.f())
out = ['DICTO · dictospheres.com', 'Progenitors step 1: the Hecatodihedron H and the Ogdoecontahedron O (its polar in the unit sphere) as shells of each other (exact, Q(√5))',
       f'  H: {len(H)} corners, corner radius² {r2(H)!r} = {r2(H).f():.6f};  O: {len(O)} corners, corner radius² {r2(O)!r} = {r2(O).f():.6f}',
       f'  H ⊂ s·O with s = {s!r} = {s.f():.9f}; {ts} corners of H touch faces of s·O',
       f'  O ⊂ t·H with t = {t!r} = {t.f():.9f}; {tt} corners of O touch faces of t·H',
       f'  two-step ratio s·t = {(s * t)!r} = {(s * t).f():.9f} (H ⊂ s·O ⊂ s·t·H ⊂ ...)']
print('\n'.join(out)); open('data/pair-chain.txt', 'w').write('\n'.join(out) + '\n')
