# Polar Dharma step 3 (2026-10-16): the pieces exactly. Each piece corner is where three exact planes meet (the outer solid's faces, the
# inner face, the cone planes through the centre and the inner face's edges), solved exactly in Q(sqrt5) by Cramer's rule; then exact
# volumes, sums against the exact layers, and each piece's shape (edge lengths squared, face kinds, regular faces?).
import json, itertools, numpy as np
from scipy.spatial import ConvexHull
import sys, io, contextlib
TIGHT = sys.argv[1:] == ['tight']                      # step 4: the tight nest (both loose ends tightened exactly)
sys.argv = ['polar.py', 'data/dharma_cycle.json']
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('scripts/polar.py').read())                  # rebuilds the exact reversed chain `rev`, with Q, S, volume, det3
f = lambda V: np.array([[x.f() for x in v] for v in V])
def plane_through(a, b, c):
    u = [b[i] - a[i] for i in range(3)]; w = [c[i] - a[i] for i in range(3)]
    n = [u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]]
    return n, sum(n[i] * a[i] for i in range(3))
def exact_planes(V):
    Vf = f(V); h = ConvexHull(Vf); out = []
    for e in h.equations:
        idx = [i for i in range(len(V)) if abs(Vf[i] @ e[:3] + e[3]) < 1e-7]
        if any(set(idx) == set(o[0]) for o in out): continue
        for i0, i1, i2 in itertools.combinations(idx, 3):
            n, d = plane_through(V[i0], V[i1], V[i2])
            if any(x.f() != 0 for x in n): break
        s = 1 if sum(n[i].f() * e[i] for i in range(3)) > 0 else -1   # outward
        out.append((idx, [x * s for x in n], d * s))
    return out
def solve3(P3):
    (n1, d1), (n2, d2), (n3, d3) = P3
    det = det3(n1, n2, n3)
    if det.f() == 0: return None
    cols = lambda k: [[(d1 if i == 0 else d2 if i == 1 else d3) if j == k else (n1, n2, n3)[i][j] for j in range(3)] for i in range(3)]
    return [det3(*cols(k)) / det for k in range(3)]
def sq(a, b): return sum(((a[i] - b[i]) * (a[i] - b[i]) for i in range(3)), Q(0))
if TIGHT:
    def grow(A, B):                                         # exact largest s with s*A inside B: min over B's faces of d / max(A . n)
        best = None
        for idx, n, d in exact_planes(B):
            m = max((sum((n[i] * a[i] for i in range(3)), Q(0)) for a in A), key=lambda x: x.f()); s = d / m
            if best is None or s.f() < best.f(): best = s
        return best
    s0 = grow(rev[0][1], rev[1][1]); s6 = Q(1) / grow(rev[-2][1], rev[-1][1])
    rev[0] = (rev[0][0], [[x * s0 for x in v] for v in rev[0][1]]); rev[-1] = (rev[-1][0], [[x * s6 for x in v] for v in rev[-1][1]])
    print(f'inner dodecahedron x {s0!r} = {s0.f():.9f}; outer dodecahedron x {s6!r} = {s6.f():.9f}')
    cl = sum((rev[-1][1][0][i] * rev[-1][1][0][i] for i in range(3)), Q(0)) / sum((rev[0][1][0][i] * rev[0][1][0][i] for i in range(3)), Q(0))
    print(f'closure, outer / inner dodecahedron: squared linear ratio {cl!r} = {cl.f():.9f}, linear {cl.f() ** 0.5:.9f}, volume ratio {cl.f() ** 1.5:.9f}')
FL = json.load(open('data/polar-tight-pieces.json' if TIGHT else 'data/polar-pieces.json'))
out = []
for k in range(len(rev) - 1):
    (na, A), (nb, B) = rev[k], rev[k + 1]
    PB = exact_planes(B); PA = exact_planes(A)
    layer_float = FL[list(FL)[k]]; total = Q(0); shapes = set(); vols = set()
    for Vf_piece in layer_float:
        Vp = np.array(Vf_piece); cand = []
        # the inner face this piece sits on, and its cone planes
        c = Vp.mean(0)
        uc = c / np.linalg.norm(c)                               # the ray from the centre through the piece crosses its inner face
        Fi = min((p for p in PA if sum(p[1][i].f() * uc[i] for i in range(3)) > 1e-12), key=lambda p: p[2].f() / sum(p[1][i].f() * uc[i] for i in range(3)))
        planes = [(p[1], p[2]) for p in PB] + [(Fi[1], Fi[2])]
        ring = Fi[0]
        for i0, i1 in itertools.combinations(ring, 2):
            a, b = A[i0], A[i1]; n = [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
            if all(x.f() == 0 for x in n): continue
            planes.append((n, Q(0)))
        Ve = []
        for v in Vp:
            act = [p for p in planes if abs(sum(p[0][i].f() * v[i] for i in range(3)) - p[1].f()) < 1e-7 * max(1, np.linalg.norm([x.f() for x in p[0]]))]
            sol = None
            for P3 in itertools.combinations(act, 3):
                sol = solve3(P3)
                if sol is not None: break
            assert sol is not None and max(abs(sol[i].f() - v[i]) for i in range(3)) < 1e-7, ('no exact corner', v)
            Ve.append(sol)
        vol = volume(Ve, Vp); total = total + vol; vols.add(vol)
        h = ConvexHull(Vp); E = {tuple(sorted((int(a), int(b)))) for s in h.simplices for a, b in itertools.combinations(s, 2)}
        L2 = sorted({(sq(Ve[a], Ve[b]).a, sq(Ve[a], Ve[b]).b) for a, b in E if True})
        shapes.add(tuple(L2))
    lay = volume(B, f(B)) - volume(A, f(A))
    out.append(f'{na} -> {nb}: {len(layer_float)} pieces; one volume each: {len(vols) == 1}; piece volume {next(iter(vols))!r}; '
               f'sum - layer = {total - lay!r}')
out = ([f'inner dodecahedron x {s0!r}; outer dodecahedron x {s6!r}; squared closure ratio {cl!r} (linear {cl.f() ** 0.5:.9f})'] if TIGHT else []) + out
print('\n'.join(out)); open('data/polar-tight-exact.txt' if TIGHT else 'data/polar-exact.txt', 'w').write('\n'.join(out) + '\n')
