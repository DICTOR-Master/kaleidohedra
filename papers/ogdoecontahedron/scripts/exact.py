# Theaetetus, exact (paper groundwork, 2026-10-15): every corner of every piece snapped to its exact value a + b*sqrt5 (a, b rational),
# then every volume computed exactly in Q(sqrt5) and the sums checked with no remainder. A wrong snap anywhere would break the exact sums,
# so the check proves itself. Inputs: data/cut102.json (the 102 cut) and data/cleo_heca.json + cleo_heca_fusions.json (the 215 stations).
import json, itertools, sys, numpy as np
from fractions import Fraction as Fr
from scipy.spatial import ConvexHull
S5 = 5 ** .5
class Q:
    """a + b*sqrt5 with a, b rational."""
    __slots__ = ('a', 'b')
    def __init__(s, a, b=0): s.a, s.b = Fr(a), Fr(b)
    def __add__(s, o): o = o if isinstance(o, Q) else Q(o); return Q(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __sub__(s, o): o = o if isinstance(o, Q) else Q(o); return Q(s.a - o.a, s.b - o.b)
    def __neg__(s): return Q(-s.a, -s.b)
    def __mul__(s, o): o = o if isinstance(o, Q) else Q(o); return Q(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def __truediv__(s, o):
        o = o if isinstance(o, Q) else Q(o); n = o.a * o.a - 5 * o.b * o.b; return s * Q(o.a / n, -o.b / n)
    def __eq__(s, o): o = o if isinstance(o, Q) else Q(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def f(s): return float(s.a) + float(s.b) * S5
    def __repr__(s):
        if s.b == 0: return f'{s.a}'
        if s.a == 0: return f'{s.b}√5'
        return f'{s.a} {"+" if s.b > 0 else "-"} {abs(s.b)}√5'
def snap(x, tol=1.5e-5, qmax=48):
    best = None
    for q in range(1, qmax + 1):
        for p in range(-6 * q, 6 * q + 1):
            b = Fr(p, q); a = Fr(round((x - float(b) * S5) * q * 1), q) if False else None
            r = x - float(b) * S5
            for qa in (q, 2 * q, 4 * q):
                a = Fr(round(r * qa), qa); err = abs(float(a) - r)
                if err < tol:
                    cand = (a.denominator + b.denominator, Q(a, b))
                    if best is None or cand[0] < best[0]: best = cand
        if best and best[0] <= 2 * q: break
    if best is None: raise ValueError(f'no snap for {x}')
    return best[1]
cache = {}
def S(x):
    k = round(x, 6)
    if k not in cache: cache[k] = snap(x)
    return cache[k]
def det3(a, b, c): return a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0])
def volume(V, Vf):
    """Exact volume of a convex polytope: exact corners V, combinatorics from the float hull."""
    h = ConvexHull(Vf); c = [sum((v[i] for v in V), Q(0)) / len(V) for i in range(3)]
    tot = Q(0)
    for s in h.simplices:
        a, b, d = ([V[j][i] - c[i] for i in range(3)] for j in s)
        x = det3(a, b, d); tot = tot + (x if x.f() > 0 else -x)
    return tot / 6
def exact_piece(m):
    Vf = np.array(m['v']); V = [[S(x) for x in v] for v in Vf]
    err = max(abs(V[i][j].f() - Vf[i][j]) for i in range(len(V)) for j in range(3)); return V, Vf, err
out = []
for name, files in (('102 clean pieces', ['cut102.json']), ('stations', ['cleo_heca.json', 'cleo_heca_fusions.json'])):
    G = {}
    for fn in files:
        for k, L in json.load(open('data/' + fn)).items(): G[k] = L
    if name == 'stations':
        G = {k: G[k] for k in ('core icosahedron', 'flat pentagonal pyramid', 'X', 'Y', 'Cleo-Ico + tripyr (to dodecahedron)', 'twisted pentagonal frustum', 't1', 'cap (to Hecatodihedron)')}
    out.append(f'== {name}')
    total, worst, allV = Q(0), 0, []
    for k, L in G.items():
        vols = set()
        for m in L:
            V, Vf, err = exact_piece(m); worst = max(worst, err); v = volume(V, Vf); vols.add(v); total = total + v; allV += [tuple(x) for x in V]
        out.append(f'  {len(L):3d} {k}: volume {" | ".join(map(repr, vols))}  (= {next(iter(vols)).f():.9f})')
    out.append(f'  largest snap correction {worst:.1e}; total volume {total!r} = {total.f():.9f}')
    uniq = list({tuple((x.a, x.b) for x in v): v for v in allV}.values())
    Hf = np.array([[x.f() for x in v] for v in uniq]); h = ConvexHull(Hf); hull_V = [uniq[i] for i in h.vertices]
    hv = volume(hull_V, Hf[h.vertices])
    out.append(f'  the hull (Hecatodihedron): {len(h.vertices)} corners, volume {hv!r}; pieces minus hull = {total - hv!r}')
print('\n'.join(out)); open('data/exact.txt', 'w').write('\n'.join(out) + '\n')
