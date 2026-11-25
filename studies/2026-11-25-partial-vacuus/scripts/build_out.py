# DICTO · partial Vacuus, part 2: building out the core (26 Nov 2026). With Claude (Anthropic).
# DICTO: "can we build out the core of any vacuus to make an excavated solid" / "they should coincide with the ones we already have".
# Start from the Vacuus of a Platonic solid P (every plate runs from an edge to the centre O). Build the centre out into a core: the dual
# of P, scaled by lam (its corners on P's face axes). Each plate then runs from its edge to the core corner on that face's axis: the plates
# are the walls of pits and the body is an excavated solid. lam = 0: the Vacuus; lam = lam_max: the core corner reaches the face (solid).
# Found here, by this route alone (no use of part 1):
#   (1) the special sizes: lam at which every wall lies flat on a face of the core (the core corners adjacent across a wall lie in it);
#   (2) the allowed range: pits interior-disjoint (sampled), core inside;
# then compared with part 1's depths (s = apex distance / face distance). Exact renders at s = 0.25, 0.5, 0.75 and at the special s.
# Usage: python build_out.py <renders dir>      (house renderer render3d.py of study 2026-11-21-scutoid-stand-in)
import sys, os, itertools, json
import numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); OUTD = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '../renders')
sys.path.insert(0, os.path.join(HERE, '../../2026-11-21-scutoid-stand-in/renders/scripts'))
import render3d as R3
ph = (1 + 5 ** .5) / 2
def cyc(v): return [v, (v[1], v[2], v[0]), (v[2], v[0], v[1])]
def signs(v): return list({tuple(s * x for s, x in zip(sg, v)) for sg in itertools.product((1, -1), repeat=3)})
SOL = {'tetrahedron': [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)],
       'octahedron': [w for v in cyc((1, 0, 0)) for w in signs(v)], 'cube': signs((1, 1, 1)),
       'icosahedron': [w for v in cyc((0, 1, ph)) for w in signs(v)],
       'dodecahedron': signs((1, 1, 1)) + [w for v in cyc((0, ph, 1 / ph)) for w in signs(v)]}
COL = {'dodecahedron': (138, 92, 196), 'icosahedron': (58, 112, 205), 'cube': (72, 142, 72), 'tetrahedron': (205, 62, 40), 'octahedron': (232, 200, 82)}
DUALNAME = {'tetrahedron': 'tetrahedron', 'octahedron': 'cube', 'cube': 'octahedron', 'icosahedron': 'dodecahedron', 'dodecahedron': 'icosahedron'}
PART1 = {('dodecahedron', 'icosahedron'): 5 - 2 * 5 ** .5, ('icosahedron', 'dodecahedron'): 3 * 5 ** .5 - 6}
def hull(V):
    V = np.array(V, float); F = []
    for i, j, k in itertools.combinations(range(len(V)), 3):
        n = np.cross(V[j] - V[i], V[k] - V[i])
        if np.linalg.norm(n) < 1e-9: continue
        sv = (V - V[i]) @ n
        if (sv <= 1e-9).all() or (sv >= -1e-9).all():
            on = frozenset(np.where(np.abs(sv) < 1e-9)[0])
            if on not in [f[0] for f in F]: F.append((on, n if (sv <= 1e-9).all() else -n))
    faces = []
    for on, n in F:
        on = list(on); c = V[on].mean(0); u = V[on[0]] - c; w = np.cross(n, u)
        faces.append(sorted(on, key=lambda m: np.arctan2((V[m] - c) @ w, (V[m] - c) @ u)))
    return V, faces
def body(P, s):
    """the excavated solid: for each face its pit walls (triangles edge + apex); apex at s * face distance on the face axis."""
    V, F = hull(SOL[P]); tris, apexes = [], []
    for f in F:
        c = V[f].mean(0); n = c / np.linalg.norm(c); d = n @ V[f[0]]; a = s * d * n; apexes.append(a)
        for x, y in zip(f, f[1:] + f[:1]): tris.append((V[x], V[y], a))
    return V, F, tris, np.array(apexes)
def flatness(P, s):
    """max over walls of the distance from the wall plane to the nearest face plane of the core (the hull of the apexes); 0 when every
    wall lies on a face of the core."""
    V, F, tris, A = body(P, s)
    CV, CF = hull(A); cpl = []
    for f in CF:
        n = np.cross(CV[f[1]] - CV[f[0]], CV[f[2]] - CV[f[0]]); n /= np.linalg.norm(n)
        d = n @ CV[f[0]]
        if d < 0: n, d = -n, -d
        cpl.append((n, d))
    worst = 0.0
    for fi, f in enumerate(F):
        for x, y in zip(f, f[1:] + f[:1]):
            n = np.cross(V[y] - V[x], A[fi] - V[x]); n /= np.linalg.norm(n); d = n @ V[x]
            if d < 0: n, d = -n, -d
            worst = max(worst, min(np.linalg.norm(n - m) + abs(d - e) for m, e in cpl))
    return worst
def disjoint(P, s, rng=np.random.default_rng(0)):
    V, F, tris, A = body(P, s)
    pyr = [(V[f], A[i]) for i, f in enumerate(F)]
    def inside(x, base, ap):
        c = (base.sum(0) + ap) / (len(base) + 1)
        pls = [(base[i], base[(i + 1) % len(base)], ap) for i in range(len(base))] + [(base[0], base[1], base[2])]
        return all(np.sign(np.cross(b - a, d - a) @ (x - a)) == np.sign(np.cross(b - a, d - a) @ (c - a)) and abs(np.cross(b - a, d - a) @ (x - a)) > 1e-9 for a, b, d in pls)
    for i, (b, a) in enumerate(pyr):
        for _ in range(80):
            w = rng.dirichlet(np.ones(len(b) + 1)); x = w[:-1] @ b + w[-1] * a
            if any(j != i and inside(x, bj, aj) for j, (bj, aj) in enumerate(pyr)): return False
    return True
res = []
for P in SOL:
    grid = np.linspace(0.001, 0.999, 999); fl = [flatness(P, s) for s in grid]
    special = []
    for i in range(1, len(grid) - 1):
        if fl[i] < fl[i - 1] and fl[i] <= fl[i + 1] and fl[i] < 5e-2:
            from scipy.optimize import minimize_scalar
            r = minimize_scalar(lambda s: flatness(P, s), bounds=(grid[i - 1], grid[i + 1]), method='bounded', options={'xatol': 1e-12})
            if r.fun < 1e-6: special.append(float(r.x))   # the flatness has a corner at the special size; Brent stops near 1e-8
    lo = min((s for s in grid[::50] if disjoint(P, s)), default=None)
    ok_all = all(disjoint(P, s) for s in (0.05, 0.25, 0.5, 0.75, 0.95))
    match = {k: v for k, v in PART1.items() if k[0] == P}
    agree = all(any(abs(sp - v) < 1e-7 for sp in special) for v in match.values()) and (len(special) == len(match))
    res.append(dict(P=P, core=DUALNAME[P], special_s=special, part1=list(match.values()), coincide=agree, pits_disjoint_all_sizes_tested=ok_all))
    print(f"{P:13s} core {DUALNAME[P]:13s} special s (this route): {[round(x, 10) for x in special]}  part 1: {[round(v, 10) for v in match.values()]}  coincide: {agree}  pits disjoint at s=0.05..0.95: {ok_all}", flush=True)
json.dump(res, open(os.path.join(HERE, '../data-build-out.json'), 'w'), indent=1)
# renders: the excavated body (pale) with its core (the dual, scaled, see-through, in the core solid's colour)
def hx(c): return '#%02x%02x%02x' % c
scenes, meta = [], []
for r in res:
    P = r['P']
    for s in [0.25, 0.5, 0.75] + r['special_s']:
        V, F, tris, A = body(P, s)
        verts = []; T = []
        for tri in tris:
            k = len(verts); verts += [tri[0], tri[1], tri[2]]; T.append([k, k + 1, k + 2])
        part = {'v': np.round(np.array(verts), 6).tolist(), 't': T, 'c': ['#e9e4da'] * len(T), 'a': 1.0,
                'tubes': [[t[0], t[1], '#2b261e', None] for t in T] + [[t[1], t[2], '#2b261e', None] for t in T] + [[t[2], t[0], '#2b261e', None] for t in T], 'rad': 0.006, 'balls': []}
        CV, CF = hull(A); ct = []
        for f in CF:
            for b, c in zip(f[1:-1], f[2:]): ct.append([int(f[0]), int(b), int(c)])
        core = {'v': np.round(CV, 6).tolist(), 't': ct, 'c': [hx(COL[r['core']])] * len(ct), 'a': 0.55, 'tubes': [], 'rad': 0.004, 'balls': []}
        E = 1.15 * np.abs(np.array(SOL[P], float)).max() * (3 ** .5 if P in ('cube', 'dodecahedron') else 1.6)
        scenes.append({'E': float(E), 'dir': [0.55, 0.35, 1.0], 'parts': [part, core]}); meta.append(dict(P=P, s=s, special=s in r['special_s']))
os.makedirs(OUTD, exist_ok=True); R3.write(os.path.join(OUTD, 'build_out.html'), scenes); json.dump(meta, open(os.path.join(OUTD, 'build_out_meta.json'), 'w'), indent=1)
good = all(r['coincide'] for r in res)
print('scenes', len(scenes)); print('FINAL ok' if good else 'FINAL FAIL (special sizes do not coincide with part 1)')
