"""Step 1. (a) Reproduce #88's ten Platonic golden cuts exactly. (b) The Archimedean solids and the elongated square
gyrobicupola: exact golden depth of every face kind, the ratio of every other face kind there, the count of cuts that
make ALL faces golden, and the cuts that make every face golden or regular. Exact in sympy; every cut is also built
in floating point and checked (convex truncation with |F|+|V| faces, ratios agree with the exact values to 1e-9).

Definitions (as #88). Every solid here has unit edges, regular faces and all corners on one sphere, so the plane
perpendicular to the centre-corner line at a fixed depth meets every edge at that corner at the same distance x; the
cut is the same x at every corner. A face of n sides becomes a 2n-gon with sides c_n x (corner sides, c_n = 2cos(pi/n))
and 1 - 2x (original sides); it is golden when the longer over the shorter is phi.
usage: python s1_platonic_archimedean.py   -> ../data/s1-archimedean.json
"""
import json, os, collections
import numpy as np
import sympy as sp
import gcb

phi = (1 + sp.sqrt(5)) / 2
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, '..', 'data')
CHECKS = []


def check(name, ok):
    CHECKS.append({'check': name, 'pass': bool(ok)}); print(('PASS ' if ok else 'FAIL ') + name, flush=True)
    assert ok, name


def c(n):
    return sp.nsimplify(sp.radsimp(2 * sp.cos(sp.pi / n)), [sp.sqrt(2), sp.sqrt(3), sp.sqrt(5)]) if n in (3, 4, 5, 6) else sp.simplify(2 * sp.cos(sp.pi / n))


C = {3: sp.Integer(1), 4: sp.sqrt(2), 5: phi, 6: sp.sqrt(3), 8: sp.sqrt(2 + sp.sqrt(2)), 10: sp.sqrt((5 + sp.sqrt(5)) / 2)}
for n, v in C.items():
    check(f'c_{n} = 2cos(pi/{n}) exactly', sp.simplify(sp.expand_trig(2 * sp.cos(sp.pi / n)) - v) == 0 or abs(sp.N(2 * sp.cos(sp.pi / n) - v, 60)) < 1e-55)


def xG(k): return sp.radsimp(phi / (k + 2 * phi))      # corner sides long
def xL(k): return sp.radsimp(1 / (phi * k + 2))        # original sides long


def ratio(k, x):                                         # long/short of a face with corner factor k at cut x
    a, b = k * x, 1 - 2 * x
    return sp.radsimp(a / b) if sp.N(a - b) >= 0 else sp.radsimp(b / a), ('corner' if sp.N(a - b) > 0 else ('equal' if a == b else 'orig'))


def eq0(e):
    e = sp.nsimplify(e) if False else e
    v = sp.N(e, 80)
    return abs(v) < sp.Float('1e-70')


def s(e): return str(sp.nsimplify(sp.simplify(e)))
def d(e): return float(sp.N(e, 20))


# ---------------------------------------------------------------- (a) #88 reproduced
ref = {  # golden-cuts-exact.md of #88 (edge 1): (greater, lesser)
    'dodecahedron': (sp.Rational(1, 3), sp.Rational(7, 22) - sp.sqrt(5) / 22),
    'icosahedron': (sp.Rational(3, 2) - sp.sqrt(5) / 2, sp.Rational(1, 2) - sp.sqrt(5) / 10),
    'cube': ((-3 * sp.sqrt(2) - 2 + sp.sqrt(10) + 2 * sp.sqrt(5)) / 4, (-2 * sp.sqrt(5) - 2 + sp.sqrt(10) + 3 * sp.sqrt(2)) / 4),
    'tetrahedron': (sp.Rational(3, 2) - sp.sqrt(5) / 2, sp.Rational(1, 2) - sp.sqrt(5) / 10),
    'octahedron': (sp.Rational(3, 2) - sp.sqrt(5) / 2, sp.Rational(1, 2) - sp.sqrt(5) / 10)}
PFACE = {'dodecahedron': 5, 'icosahedron': 3, 'cube': 4, 'tetrahedron': 3, 'octahedron': 3}
out = {'platonic': [], 'archimedean': []}
for name in gcb.PLATONIC:
    k = C[PFACE[name]]; g1, l1 = xG(k), xL(k)
    check(f'#88 reproduced: {name} greater x = {s(g1)}', sp.simplify(g1 - ref[name][0]) == 0)
    check(f'#88 reproduced: {name} lesser x = {s(l1)}', sp.simplify(l1 - ref[name][1]) == 0)
    V = gcb.platonic(name); F = gcb.faces(V)
    for lab, x in (('greater', g1), ('lesser', l1)):
        y = [d(x)] * len(V)
        ok, nf = gcb.check_cut_is_convex_truncation(V, F, y)
        _, sides = gcb.cut(V, F, y)
        rs = [max(a for _, a in sd) / min(a for _, a in sd) for sd in sides]
        check(f'{name} {lab}: convex truncation ({nf} faces), every face ratio phi (float)', ok and max(abs(r - d(phi)) for r in rs) < 1e-9)
        out['platonic'].append({'solid': name, 'cut': lab, 'x': s(x), 'x_decimal': d(x)})

# ---------------------------------------------------------------- (b) Archimedean
# the general rule, checked exactly on the face sizes that occur
sizes = [3, 4, 5, 6, 8, 10]
vals = {}
for n in sizes:
    vals[('G', n)] = xG(C[n]); vals[('L', n)] = xL(C[n])
keys = list(vals)
for i in range(len(keys)):
    for j in range(i + 1, len(keys)):
        a, b = vals[keys[i]], vals[keys[j]]
        check(f'golden depths distinct: x_{keys[i][0]}({keys[i][1]}) != x_{keys[j][0]}({keys[j][1]})', not eq0(a - b))
# regular-other-face coincidences: at x_L(n) an m-gon is regular iff c_m = phi c_n; at x_G(n) iff c_n = phi c_m
coinc = []
for n in sizes:
    for m in sizes:
        if m == n: continue
        if eq0(C[m] - phi * C[n]): coinc.append(('L', n, m))
        if eq0(C[n] - phi * C[m]): coinc.append(('G', n, m))
check(f'only golden/regular coincidences: {coinc}', coinc == [('L', 3, 5), ('G', 5, 3)])

for name in gcb.ARCH + ['elongated square gyrobicupola']:
    V = gcb.archimedean(name); F = gcb.faces(V)
    S = sorted(set(len(f) for f in F)); cnt = collections.Counter(len(f) for f in F)
    rows = []
    for n in S:
        for lab, x in (('greater', xG(C[n])), ('lesser', xL(C[n]))):
            others = {}
            gold_or_reg = True
            for m in S:
                r, longer = ratio(C[m], x)
                others[m] = {'ratio_long_over_short': s(r), 'decimal': d(r), 'long_sides': longer}
                if m != n and not (eq0(r - 1) or eq0(r - phi)): gold_or_reg = False
                if m == n: check(f'{name}: {n}-gons golden at {lab} x', eq0(r - phi))
            y = [d(x)] * len(V)
            ok, nf = gcb.check_cut_is_convex_truncation(V, F, y)
            _, sides = gcb.cut(V, F, y)
            fl = True
            for f, sd in zip(F, sides):
                cs = [a for k_, a in sd if k_ == 'corner']; os_ = [a for k_, a in sd if k_ == 'orig']
                r = max(cs[0], os_[0]) / min(cs[0], os_[0])
                fl &= (max(cs) - min(cs) < 1e-9 and max(os_) - min(os_) < 1e-9 and abs(r - others[len(f)]['decimal']) < 1e-9)
            check(f'{name}: {lab} cut of the {n}-gons (x={d(x):.6f}) builds as a convex truncation with {nf} faces; float ratios agree', ok and fl)
            all_golden = all(eq0(sp.sympify(o['ratio_long_over_short']) - phi) for o in others.values())
            rows.append({'face': n, 'cut': lab, 'x': s(x), 'x_decimal': d(x), 'other_faces': others,
                         'all_faces_golden': all_golden, 'every_face_golden_or_regular': gold_or_reg})
    n_all = sum(r['all_faces_golden'] for r in rows)
    check(f'{name}: {n_all} cuts make all faces golden (theorem: 0)', n_all == 0)
    out['archimedean'].append({'solid': name, 'faces': dict(sorted(cnt.items())), 'vertices': len(V), 'cuts': rows,
                               'all_golden_count': n_all, 'golden_or_regular': [(r['face'], r['cut'], r['x']) for r in rows if r['every_face_golden_or_regular']]})
    print(name, 'golden-or-regular:', out['archimedean'][-1]['golden_or_regular'])

# exact check of the two icosidodecahedron golden-or-regular cuts from exact Q(sqrt5) coordinates
def ev(v):
    a, b, cc = v
    return [(a, b, cc), (b, cc, a), (cc, a, b)]
P = set()
for seed in [(sp.Integer(0), sp.Integer(0), phi), (sp.Rational(1, 2), phi / 2, phi ** 2 / 2)]:
    for p in ev(seed):
        for sg in [(i, j, k) for i in (1, -1) for j in (1, -1) for k in (1, -1)]:
            P.add(tuple(sp.radsimp(sp.sympify(sg[t] * p[t])) for t in range(3)))
P = [sp.Matrix(p) for p in P]
check('icosidodecahedron exact: 30 corners', len(P) == 30)
E = [(i, j) for i in range(30) for j in range(i + 1, 30) if sp.simplify((P[i] - P[j]).dot(P[i] - P[j]) - 1) == 0]
check('icosidodecahedron exact: 60 unit edges', len(E) == 60)
idc = {}
for lab, x in (('triangles golden (lesser), decagons regular', xL(1)), ('pentagons golden (greater), hexagons regular', xG(phi))):
    pts = {}
    for i, j in E:
        pts[(i, j)] = P[i] + x * (P[j] - P[i]); pts[(j, i)] = P[j] + x * (P[i] - P[j])
    L2 = collections.Counter()
    for i, j in E:                                    # original sides: between the two cut points of an edge
        L2[sp.nsimplify(sp.radsimp(sp.expand((pts[(i, j)] - pts[(j, i)]).dot(pts[(i, j)] - pts[(j, i)]))))] += 1
    for v in range(30):                               # corner sides: between cut points of neighbouring edges at v
        nb = [j for i, j in E if i == v] + [i for i, j in E if j == v]
        for a in range(4):
            for b in range(a + 1, 4):
                q = sp.radsimp(sp.expand((P[nb[a]] - P[v]).dot(P[nb[b]] - P[v])))
                if sp.N(q) > -0.5:   # edges at 60 or 108 degrees share a face (cos 1/2, -0.309); opposite edges have cos -0.809
                    w = pts[(v, nb[a])] - pts[(v, nb[b])]
                    L2[sp.nsimplify(sp.radsimp(sp.expand(w.dot(w))))] += 1
    lens = {str(k): v for k, v in L2.items()}
    vals2 = sorted(L2, key=lambda t: float(t))
    check(f'icosidodecahedron, {lab}: exactly two squared edge lengths {lens}, ratio of lengths phi exactly',
          len(vals2) == 2 and sp.simplify(vals2[1] / vals2[0] - phi ** 2) == 0)
    # exact volume: icosidodecahedron volume minus 30 corner pyramids; corner pyramid volume = x^3 * unit corner pyramid
    vol_id = (45 + 17 * sp.sqrt(5)) / 6
    v0 = P[0]; nb = [j for i, j in E if i == 0] + [i for i, j in E if j == 0]
    # pyramid with apex v0 over the corner rectangle at distance 1 along the edges (split into two tetrahedra)
    q = [P[j] - v0 for j in nb]
    order = [0]                       # cyclic order of the four edges round v0: consecutive edges share a face
    while len(order) < 4:
        order.append(next(t for t in range(4) if t not in order and sp.N(q[order[-1]].dot(q[t])) > -0.5))
    q = [q[t] for t in order]
    unit = sp.Abs(sp.Matrix.hstack(q[0], q[1], q[2]).det()) / 6 + sp.Abs(sp.Matrix.hstack(q[0], q[2], q[3]).det()) / 6
    vol = sp.radsimp(sp.expand(vol_id - 30 * x ** 3 * unit))
    idc[lab] = {'x': s(x), 'x_decimal': d(x), 'edge_length2_counts': lens, 'volume_edge1': s(vol), 'volume_decimal': d(vol)}
    print(lab, idc[lab])
out['icosidodecahedron_exact'] = idc
out['checks'] = CHECKS
os.makedirs(DATA, exist_ok=True)
json.dump(out, open(os.path.join(DATA, 's1-archimedean.json'), 'w'), indent=1)
print(f'{sum(c_["pass"] for c_ in CHECKS)}/{len(CHECKS)} checks passed')
