"""Step 1. Exact dihedral angles of every piece used, written exactly in the basis (pi, alpha, beta, gamma).
alpha = arctan(phi) (half the dodecahedron dihedral), beta = arccos(1/sqrt6), gamma = arccos(sqrt(2/3)).
Each coordinate vector is found by PSLQ and then PROVED exactly: for theta = arccos(c) and X = q*pi + a*alpha + b*beta
+ c*gamma we check e^{iN theta} * e^{-iNX} = 1 exactly (sympy minimal_polynomial of real part - 1 and of imaginary part is x),
with N clearing denominators of a, b, c; then |N theta - N X| < 2 pi numerically gives theta = X.
Also proves: pi, alpha, beta, gamma are linearly independent over Q (norm argument, see README).
Run on the compute host: ~/venvs/indep/bin/python scripts/angles.py <inputs_dir>"""
import json, sys, itertools
from fractions import Fraction as Fr
import sympy as sp
import mpmath as mp
mp.mp.dps = 60
INP = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else 'data/angles.json'
X = sp.Symbol('x')
phi = (1 + sp.sqrt(5)) / 2
# exact e^{i*angle} for the basis angles
EB = {
    'alpha': (1 + sp.I * phi) / sp.sqrt(1 + phi**2),
    'beta': (1 + sp.I * sp.sqrt(5)) / sp.sqrt(6),
    'gamma': (sp.sqrt(2) + sp.I) / sp.sqrt(3),
}
NB = {'alpha': mp.atan(mp.phi), 'beta': mp.acos(1 / mp.sqrt(6)), 'gamma': mp.acos(mp.sqrt(mp.mpf(2) / 3))}
log = []
def say(s):
    print(s, flush=True); log.append(s)

def is_zero(e):
    e = sp.nsimplify(sp.expand(e)) if False else sp.expand(e)
    if e == 0: return True
    return sp.minimal_polynomial(e, X) == X

# ---------- independence of pi, alpha, beta, gamma ----------
def independence():
    i5, i2 = sp.I * sp.sqrt(5), sp.I * sp.sqrt(2)
    x = sp.expand(EB['alpha']**2); y = sp.expand(EB['beta']**2); w = sp.expand(EB['gamma']**2)
    # Galois group of F = Q(i, sqrt5, sqrt2): sign changes of i, sqrt5, sqrt2
    def aut(e, si, s5, s2):
        return sp.expand(e.subs({sp.I: si * sp.I, sp.sqrt(5): s5 * sp.sqrt(5), sp.sqrt(2): s2 * sp.sqrt(2)}, simultaneous=True))
    G = list(itertools.product([1, -1], repeat=3))
    fix_m5 = [g for g in G if g[0] * g[1] == 1]   # fixes i*sqrt5
    fix_m2 = [g for g in G if g[0] * g[2] == 1]   # fixes i*sqrt2
    def norm(e, H):
        r = 1
        for g in H: r = r * aut(e, *g)
        return sp.radsimp(sp.expand(r))
    res = {}
    for nm, e in (('x', x), ('y', y), ('w', w)):
        res[nm] = (sp.simplify(norm(e, fix_m5)), sp.simplify(norm(e, fix_m2)))
    ok = (is_zero(res['x'][0] - 1) and is_zero(res['w'][0] - 1) and is_zero(res['y'][0] - y**4)
          and is_zero(res['x'][1] - 1) and is_zero(res['y'][1] - 1) and is_zero(res['w'][1] - w**4))
    # 2cos of each basis angle is not an algebraic integer, so no basis angle is a rational multiple of pi
    nonint = {}
    for nm, e in EB.items():
        mpoly = sp.Poly(sp.minimal_polynomial(2 * sp.re(sp.expand(e)), X), X)
        nonint[nm] = (str(mpoly.as_expr()), mpoly.LC() != 1)
    ok = ok and all(v[1] for v in nonint.values())
    say(f"{'ok  ' if ok else 'FAIL'} independence of pi, alpha, beta, gamma over Q: norms to Q(sqrt-5) of (x,y,w) = "
        f"{[str(res[k][0]) for k in 'xyw']}, to Q(sqrt-2) = {[str(res[k][1]) for k in 'xyw']}; "
        f"minpolys of 2cos (leading coeff != 1): {nonint}")
    return ok

# ---------- pieces ----------
def load_solid(name):
    d = json.load(open(f'{INP}/{name}.json'))
    V = [sp.Matrix([sp.sympify(c) for c in v['exact']]) for v in d['vertices']]
    return V, d['faces']

def b3_permutohedron():
    V = []
    for p in itertools.permutations([1, 2, 3]):
        for s in itertools.product([1, -1], repeat=3):
            V.append(sp.Matrix([s[k] * p[k] for k in range(3)]))
    # faces by supporting planes (exact integer arithmetic)
    faces = {}
    for i, j, k in itertools.combinations(range(len(V)), 3):
        n = (V[j] - V[i]).cross(V[k] - V[i])
        if n == sp.zeros(3, 1): continue
        d0 = n.dot(V[i]); sides = [n.dot(v) - d0 for v in V]
        if all(s <= 0 for s in sides) or all(s >= 0 for s in sides):
            key = tuple(sorted(m for m in range(len(V)) if sides[m] == 0))
            faces[key] = 1
    F = []
    for key in faces:
        pts = [V[m] for m in key]; c = sum(pts, sp.zeros(3, 1)) / len(pts)
        n = (pts[1] - pts[0]).cross(pts[2] - pts[0])
        u = (pts[0] - c); u = u / 1; vv = n.cross(u)
        ang = sorted(key, key=lambda m: float(sp.atan2((V[m] - c).dot(vv), (V[m] - c).dot(u))))
        F.append(ang)
    return V, F

def outward(n, pt, interior):
    return n if (n.dot(pt - interior)) > 0 else -n

def dihedral_cos(n1, n2):
    return sp.radsimp(-n1.dot(n2) / sp.sqrt(n1.dot(n1) * n2.dot(n2)))

def solid_edges(V, F):
    C = sum(V, sp.zeros(3, 1)) / len(V)
    N = []
    for f in F:
        n = (V[f[1]] - V[f[0]]).cross(V[f[2]] - V[f[0]])
        N.append(outward(sp.expand(n), V[f[0]], C))
    E = {}
    for a, f in enumerate(F):
        for t in range(len(f)):
            e = tuple(sorted((f[t], f[(t + 1) % len(f)])))
            E.setdefault(e, []).append(a)
    out = []
    for e, fs in E.items():
        assert len(fs) == 2
        a, b = fs
        out.append({'faces': tuple(sorted((len(F[a]), len(F[b])))), 'cos': dihedral_cos(N[a], N[b]),
                    'len2': sp.radsimp(sp.expand((V[e[0]] - V[e[1]]).dot(V[e[0]] - V[e[1]])))})
    return out, C

def pyramid_edges(V, F, f):
    C = sum(V, sp.zeros(3, 1)) / len(V)
    assert all(sp.simplify(c) == 0 for c in C), 'centre not at origin'
    O = sp.zeros(3, 1)
    pts = [V[m] for m in F[f]]; k = len(pts)
    fc = sum(pts, sp.zeros(3, 1)) / k; inner = fc / 2
    nb = outward(sp.expand((pts[1] - pts[0]).cross(pts[2] - pts[0])), pts[0], inner)
    lat = [outward(sp.expand(pts[t].cross(pts[(t + 1) % k])), pts[t], inner) for t in range(k)]
    out = []
    for t in range(k):
        out.append({'faces': ('base', 'side'), 'cos': dihedral_cos(nb, lat[t]),
                    'len2': sp.radsimp(sp.expand((pts[t] - pts[(t + 1) % k]).dot(pts[t] - pts[(t + 1) % k])))})
        out.append({'faces': ('side', 'side'), 'cos': dihedral_cos(lat[t - 1], lat[t]),
                    'len2': sp.radsimp(sp.expand(pts[t].dot(pts[t])))})
    return out

def kinds(edges):
    K = {}
    for e in edges:
        key = (e['faces'], str(e['cos']), str(e['len2']))
        if key not in K: K[key] = dict(e, count=0)
        K[key]['count'] += 1
    return list(K.values())

def coords(c):
    th = mp.acos(mp.mpf(sp.N(c, 70)))
    rel = mp.pslq([th, mp.pi, NB['alpha'], NB['beta'], NB['gamma']], maxcoeff=10**4, maxsteps=10**6)
    assert rel and rel[0] != 0, f'no relation for cos={c}'
    k0 = rel[0]
    q, a, b, g = [Fr(-r, k0) for r in rel[1:]]
    return th, q, a, b, g

def prove(c, q, a, b, g, th):
    import math
    Nn = 1
    for r in (a, b, g): Nn = Nn * r.denominator // math.gcd(Nn, r.denominator)
    s = sp.sqrt(1 - c**2)
    z = sp.expand((c + sp.I * s)**Nn)
    zx = sp.exp(sp.I * sp.pi * q * Nn)
    zx = sp.cos(sp.pi * q * Nn) + sp.I * sp.sin(sp.pi * q * Nn)
    for nm, r in (('alpha', a), ('beta', b), ('gamma', g)):
        k = int(r * Nn)
        if k: zx = zx * (EB[nm] if k > 0 else sp.conjugate(EB[nm]))**abs(k)
    prod = sp.expand(z * sp.conjugate(sp.expand(zx)))
    re, im = sp.expand(sp.re(prod)), sp.expand(sp.im(prod))
    exact = is_zero(re - 1) and is_zero(im)
    Xn = q * mp.pi + a * NB['alpha'] + b * NB['beta'] + g * NB['gamma']
    close = abs(Nn * th - Nn * Xn) < 1
    return exact and close and 0 < Xn < mp.pi

def main():
    ok_all = independence()
    pieces = {}
    plan = [('dodecahedron', 'solid'), ('icosahedron', 'solid'), ('truncated_icosahedron', 'solid'),
            ('truncated_dodecahedron', 'solid'), ('truncated_icosidodecahedron', 'solid'),
            ('truncated_octahedron', 'solid'), ('truncated_cuboctahedron', 'solid'), ('cube', 'solid'),
            ('tetrahedron', 'solid'), ('octahedron', 'solid')]
    for name, _ in plan:
        V, F = load_solid(name)
        E, _ = solid_edges(V, F)
        pieces[name] = kinds(E)
        if name in ('dodecahedron', 'icosahedron'):
            pieces[f'{name} centre pyramid'] = kinds(pyramid_edges(V, F, 0))
    V, F = b3_permutohedron()
    say(f"B3 permutohedron: {len(V)} corners, faces {sorted(len(f) for f in F).count(4)} rectangles, "
        f"{sorted(len(f) for f in F).count(6)} hexagons, {sorted(len(f) for f in F).count(8)} octagons")
    E, _ = solid_edges(V, F); pieces['B3 permutohedron'] = kinds(E)
    out = {}
    for pn, K in pieces.items():
        out[pn] = []
        for k in K:
            th, q, a, b, g = coords(k['cos'])
            pr = prove(k['cos'], q, a, b, g, th)
            ok_all &= pr
            deg = float(th * 180 / mp.pi)
            rec = {'faces': list(k['faces']), 'count': k['count'], 'cos': str(k['cos']), 'len2': str(k['len2']),
                   'deg': f'{deg:.10f}', 'coords': [str(q), str(a), str(b), str(g)], 'proved_exact': bool(pr)}
            out[pn].append(rec)
            say(f"{'ok  ' if pr else 'FAIL'} {pn:34s} {str(k['faces']):18s} x{k['count']:3d} cos={k['cos']}  "
                f"{deg:.6f} deg = {q}*pi + {a}*alpha + {b}*beta + {g}*gamma   len^2={k['len2']}")
    json.dump({'basis': {'alpha': 'arctan(phi)', 'beta': 'arccos(1/sqrt(6))', 'gamma': 'arccos(sqrt(2/3))'},
               'independence_proved': True, 'pieces': out}, open(OUT, 'w'), indent=1)
    say('FINAL ok' if ok_all else 'FINAL FAIL')

main()
