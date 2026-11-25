# DICTO · partial Vacuus, part 3 (26 Nov 2026): building out the core of ANY Vacuus, and how solid the result is. With Claude (Anthropic).
# DICTO: "can we build out the core of any vacuus to make an excavated solid"; "cuboctahedron and mcooeys too"; buildability yardstick
# "just the classics for models" (excavated dodecahedron, great dodecahedron).
# Solid P (corners V, faces F, outward unit normals n_f, face distances d_f). Core = P's polar dual scaled by lam: its corners
# lam * n_f / d_f lie on P's face axes. Each pit: the face with apex lam n_f / d_f (inside the face while lam < d_f^2), so
# t = lam / min_f d_f^2 runs over (0, 1): t -> 0 the Vacuus, t -> 1 the first pits close (the solid). (Platonic: t = s of part 1.)
# Per solid, over a grid of t and refined:
#   special t: every pit wall lies on a face plane of the core (hull of the apexes);
#   solidity: the material between two pits sharing an edge is a wedge; its angle is the angle between the two walls along that edge
#     (0 at the Vacuus, where both walls are the same plate). min over edges = the thinnest wedge;
#   pits interior-disjoint (sampled).
# Yardstick (DICTO): the thinnest wedge of the excavated dodecahedron and of the great dodecahedron (the classics as models). A size is
# marked "as solid as the classics" when its thinnest wedge is at least the smaller of the two.
# Solids: SET=platonic+cubo (the five + cuboctahedron, from polyhedra.json of study 2026-11-25-tacitus; controls) or SET=mccooey
# (162 self-duals of study 2026-11-26-self-dual-forms, his data files, used as given, his names).
import sys, os, json, glob, itertools
import numpy as np
from scipy.spatial import ConvexHull
from scipy.optimize import minimize_scalar
HERE = os.path.dirname(os.path.abspath(__file__))
SET = os.environ.get('SET', 'platonic+cubo'); OUT = os.path.join(HERE, '../data-build-out-%s.json' % SET.replace('+', '-'))
def normals(V, F):
    N, D = [], []
    for f in F:
        P = V[f]; c = P.mean(0); n = np.zeros(3)
        for a, b in zip(P, np.roll(P, -1, 0)): n += np.cross(a - c, b - c)
        n /= np.linalg.norm(n)
        if n @ c < 0: n = -n
        N.append(n); D.append(n @ P[0])
    return np.array(N), np.array(D)
def load():
    out = []
    if SET == 'mccooey':
        sys.path.insert(0, os.path.join(HERE, '../../2026-11-26-self-dual-forms/scripts'))
        from forms import parse
        src = os.path.join(HERE, '../../2026-11-26-self-dual-forms/source')
        for f in sorted(glob.glob(os.path.join(src, '*SelfDual*.txt'))):
            if 'SelfDuals' in os.path.basename(f): continue
            name, V, F = parse(f); out.append((name, V, F))
    else:
        P = json.load(open(os.path.join(HERE, '../../2026-11-25-tacitus/data/polyhedra.json')))
        for p in P:
            if SET == 'catalogue' or p['name'] in ('tetrahedron', 'cube', 'octahedron', 'dodecahedron', 'icosahedron', 'cuboctahedron'):
                V = np.array(p['verts'], float); V -= V.mean(0); out.append((p['name'], V, p['faces']))
    return out
class Body:
    def __init__(s, V, F):
        s.V = np.asarray(V, float); s.F = [list(f) for f in F]; s.N, s.D = normals(s.V, s.F)
        s.lmax = float(np.min(s.D ** 2))
        s.E = {}
        for fi, f in enumerate(s.F):
            for a, b in zip(f, f[1:] + f[:1]): s.E.setdefault((min(a, b), max(a, b)), []).append(fi)
    def apex(s, t): return (t * s.lmax) * s.N / s.D[:, None]
    def wall(s, fi, a, b, A):
        u, v = s.V[a], s.V[b]; n = np.cross(v - u, A[fi] - u); n /= np.linalg.norm(n)
        return n if n @ u >= 0 else -n
    def flat(s, t):
        A = s.apex(t)
        try: H = ConvexHull(A)
        except Exception: return 1.0
        cp = []
        for eq in H.equations:
            n, d = eq[:3], -eq[3]; cp.append((n, d))
        worst = 0.0
        for fi, f in enumerate(s.F):
            for a, b in zip(f, f[1:] + f[:1]):
                n = s.wall(fi, a, b, A); d = n @ s.V[a]
                worst = max(worst, min(np.linalg.norm(n - m) + abs(d - e) for m, e in cp))
        return worst
    def wedge(s, t):
        """thinnest material wedge (degrees) between the two pits along any edge"""
        A = s.apex(t); m = 180.0
        for (a, b), fs in s.E.items():
            if len(fs) != 2: continue
            w1, w2 = s.wall(fs[0], a, b, A), s.wall(fs[1], a, b, A)
            m = min(m, np.degrees(np.arccos(np.clip(abs(w1 @ w2), -1, 1))))
        return m
    def disjoint(s, t, rng=np.random.default_rng(0), k=30):
        A = s.apex(t); pyr = [(s.V[f], A[i]) for i, f in enumerate(s.F)]
        def inside(x, base, ap):
            c = (base.sum(0) + ap) / (len(base) + 1)
            pls = [(base[i], base[(i + 1) % len(base)], ap) for i in range(len(base))] + [(base[0], base[1], base[2])]
            for a, b, d in pls:
                n = np.cross(b - a, d - a); sx = n @ (x - a)
                if abs(sx) < 1e-9 * np.linalg.norm(n) or np.sign(sx) != np.sign(n @ (c - a)): return False
            return True
        for i, (b, a) in enumerate(pyr):
            for _ in range(k):
                w = rng.dirichlet(np.ones(len(b) + 1)); x = w[:-1] @ b + w[-1] * a
                if any(j != i and inside(x, bj, aj) for j, (bj, aj) in enumerate(pyr)): return False
        return True
def study(name, V, F, grid=400):
    B = Body(V, F); T = np.linspace(1e-3, 1 - 1e-3, grid); fl = [B.flat(t) for t in T]; sp = []
    for i in range(1, grid - 1):
        if fl[i] < fl[i - 1] and fl[i] <= fl[i + 1] and fl[i] < 5e-2:
            r = minimize_scalar(B.flat, bounds=(T[i - 1], T[i + 1]), method='bounded', options={'xatol': 1e-12})
            if r.fun < 1e-6: sp.append(float(r.x))
    wd = [B.wedge(t) for t in T[::8]]
    dj = {round(float(t), 2): B.disjoint(t) for t in (0.1, 0.3, 0.5, 0.7, 0.9)}
    return B, dict(name=name, F=len(F), special_t=sp, special_wedge=[B.wedge(t) for t in sp], wedge_curve=[[round(float(t), 4), round(w, 4)] for t, w in zip(T[::8], wd)], disjoint=dj)
if __name__ == '__main__':
    # yardstick from the classics (computed here, not assumed)
    ref = {p[0]: p for p in [x for x in load()] if p[0] in ('dodecahedron', 'icosahedron')} if SET != 'mccooey' else None
    if ref is None:
        ref = {}
        P = json.load(open(os.path.join(HERE, '../../2026-11-25-tacitus/data/polyhedra.json')))
        for p in P:
            if p['name'] in ('dodecahedron', 'icosahedron'): V = np.array(p['verts'], float); ref[p['name']] = (p['name'], V - V.mean(0), p['faces'])
    yard = {}
    for nm, s_exact in (('dodecahedron', 5 - 2 * 5 ** .5), ('icosahedron', 3 * 5 ** .5 - 6)):
        B = Body(ref[nm][1], ref[nm][2]); yard[nm] = B.wedge(s_exact); assert B.flat(s_exact) < 1e-9, nm
    Y = min(yard.values()); print('yardstick wedges (deg):', {k: round(v, 4) for k, v in yard.items()}, 'use', round(Y, 4), flush=True)
    res = []; L = load(); lim = int(os.environ.get('LIMIT', '0')) or len(L)
    for k, (name, V, F) in enumerate(L[:lim]):
        fam = next((p.get('family') for p in json.load(open(os.path.join(HERE, '../../2026-11-25-tacitus/data/polyhedra.json'))) if p['name'] == name), 'McCooey') if SET != 'mccooey' else 'McCooey'
        try:
            B, r = study(name, V, F)
            r['family'] = fam; r['t_as_solid_as_classics'] = next((t for t, w in r['wedge_curve'] if w >= Y), None)
            res.append(r)
            print(f"{name[:44]:44s} F{len(F):3d} special t {[round(x, 8) for x in r['special_t']]} wedge there {[round(w, 2) for w in r['special_wedge']]}  classic-solid from t = {r['t_as_solid_as_classics']}  disjoint {all(r['disjoint'].values())}", flush=True)
        except Exception as ex:
            res.append(dict(name=name, err=str(ex)[:120])); print('ERR', name, ex, flush=True)
        if (k + 1) % 20 == 0: print('PROGRESS', k + 1, '/', lim, flush=True)
    json.dump(dict(yardstick_deg=yard, solids=res), open(OUT, 'w'), indent=1)
    errs = [r for r in res if 'err' in r]
    ctrl = True
    if SET != 'mccooey':
        g = {r['name']: r for r in res}
        ctrl = 'dodecahedron' in g and any(abs(t - (5 - 2 * 5 ** .5)) < 1e-6 for t in g['dodecahedron']['special_t']) and any(abs(t - (3 * 5 ** .5 - 6)) < 1e-6 for t in g['icosahedron']['special_t'])
        print('control (both classics found again):', ctrl)
    print('solids', len(res), 'errors', len(errs)); print('FINAL ok' if ctrl and not errs else 'FINAL FAIL')
