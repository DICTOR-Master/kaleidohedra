"""Kaleidohedra target search, both ways (2026-10-01).

Target: every equal-edge space-filling zonohedron (Fedorov's five types)
whose edge directions meet only at special angles -- the regularity
meter's set: 36, 45, 60, arccos(1/3) = 70.53, 72 and 90 degrees. Faces are
then squares, rhombi of those angles, and equal-edged hexagons (regular
when all three angles are 60).

Top-down: build every direction set exactly. Three independent directions
are fixed (up to rotation) by their three angles; every further direction
is fixed by its angles to those three. Keep the sets that fill space.

Bottom-up: search continuously over every cell shape of each type (the
same space the sliders move through) for shapes whose angles all land on
the special set, from many random starts, independent of the top-down
construction. The two lists must agree.
"""
import itertools, math, json, sys
import numpy as np
from enumerate_lib import is_parallelohedron, planes, canon, volume

SPECIAL = [36, 45, 60, math.degrees(math.acos(1 / 3)), 72, 90]
COS = sorted({round(s * math.cos(math.radians(a)), 12) for a in SPECIAL for s in (1, -1)})
TOL = 1e-7

def line_angle(a, b):
    return math.degrees(math.acos(min(1.0, abs(float(a @ b)))))

def all_special(S):
    return all(min(abs(line_angle(a, b) - s) for s in SPECIAL) < 1e-5 for a, b in itertools.combinations(S, 2))

def fedorov_type(S):
    f = 2 * len(planes(S))
    n = len(S)
    return {6: 'parallelepiped', 8: 'hexagonal prism', 14: 'truncated octahedron'}.get(f) or ('rhombic dodecahedron' if n == 4 else 'elongated dodecahedron')

def faces(S):
    """Face shapes, as a count per kind (opposite faces both counted)."""
    out = {}
    used = set()
    for n in planes(S):
        inplane = [i for i, g in enumerate(S) if abs(float(g @ n)) < 1e-7]
        angs = sorted(round(line_angle(S[i], S[j]), 2) for i, j in itertools.combinations(inplane, 2))
        if len(inplane) == 2:
            kind = 'square' if angs[0] == 90 else f'rhombus {angs[0]:g}'
        else:
            kind = 'regular hexagon' if all(a == 60 for a in angs) else 'hexagon ' + '/'.join(f'{c:g}' for c in hex_corners([S[i] for i in inplane]))
        out[kind] = out.get(kind, 0) + 2
    return dict(sorted(out.items()))

def hex_corners(zone):
    """Interior corners of the zonogon of three directions in one plane, each twice, largest first.

    Lines sorted by their angle in the plane (theta1 < theta2 < theta3, in [0, 180)): the edges turn
    by theta2 - theta1, theta3 - theta2 and 180 - (theta3 - theta1), so the corners are
    180 - (theta2 - theta1), 180 - (theta3 - theta2) and theta3 - theta1 (their sum is 360).
    """
    a, b = zone[0], zone[1]
    n = np.cross(a, b)
    e2 = np.cross(n, a)
    e2 = e2 / np.linalg.norm(e2)
    th = sorted((math.atan2(float(g @ e2), float(g @ a)) % math.pi) for g in zone)
    deg = lambda r: round(math.degrees(r), 6)
    return sorted([180 - deg(th[1] - th[0]), 180 - deg(th[2] - th[1]), deg(th[2] - th[0])], reverse=True)

def record(S):
    S = [np.array(g) / np.linalg.norm(g) for g in S]
    return {'type': fedorov_type(S), 'directions': len(S), 'faces': faces(S),
            'line_angles': sorted(round(line_angle(a, b), 2) for a, b in itertools.combinations(S, 2)),
            'volume': round(volume(S), 6), 'gram': [[round(float(a @ b), 9) for b in S] for a in S]}

def quick_key(S):
    return tuple(sorted(round(abs(float(a @ b)), 6) for a, b in itertools.combinations(S, 2)))

def add(found, S):
    """Add S if it fills space and is new up to congruence. Returns True if new."""
    if not is_parallelohedron(S): return False
    q = quick_key(S)
    bucket = found.setdefault((len(S), q), [])
    key = canon(S)
    if any(k == key for k, _ in bucket): return False
    bucket.append((key, S))
    return True

# ---- top-down -------------------------------------------------------------
def bases():
    for c12 in [c for c in COS if c >= 0]:
        for c13 in [c for c in COS if c >= 0]:
            for c23 in COS:
                d1 = np.array([0, 0, 1.0])
                d2 = np.array([math.sqrt(1 - c12 ** 2), 0, c12])
                if d2[0] < TOL: continue
                x = c13; y = (c23 - c12 * c13) / d2[0] if False else None
                # d3 = (a, b, c13) with d3.d2 = c23
                c = c13
                a = (c23 - c12 * c) / d2[0]
                b2 = 1 - a * a - c * c
                if b2 < TOL: continue  # coplanar or impossible: need independent base
                yield [d1, d2, np.array([a, math.sqrt(b2), c])]

def extras(B):
    M = np.array(B)
    Minv = np.linalg.inv(M)
    out = []
    for cs in itertools.product(COS, repeat=3):
        v = Minv @ np.array(cs)
        if abs(v @ v - 1) > 1e-9: continue
        if any(abs(abs(v @ g) - 1) < 1e-9 for g in B): continue
        if any(abs(abs(v @ w) - 1) < 1e-9 for w in out): continue
        out.append(v)
    return out

def top_down():
    found = {}
    for B in bases():
        add(found, B)
        E = extras(B)
        ok = lambda S: all_special(S)
        for k in (1, 2, 3):
            for extra in itertools.combinations(E, k):
                S = B + list(extra)
                if ok(S): add(found, S)
    return found

# ---- bottom-up ------------------------------------------------------------
def unit(v): return v / np.linalg.norm(v)
def sph(t, p): return np.array([math.sin(t) * math.cos(p), math.sin(t) * math.sin(p), math.cos(t)])

PARAMS = {  # type -> (number of parameters, build directions from parameters)
    'parallelepiped': (6, lambda x: [sph(x[0], x[1]), sph(x[2], x[3]), sph(x[4], x[5])]),
    'hexagonal prism': (5, lambda x: [np.array([1, 0, 0.]), np.array([math.cos(x[0]), math.sin(x[0]), 0]), np.array([math.cos(x[1]), math.sin(x[1]), 0]), sph(x[2], x[3])]),
    'rhombic dodecahedron': (8, lambda x: [sph(x[2 * i], x[2 * i + 1]) for i in range(4)]),
    'elongated dodecahedron': (8, lambda x: (lambda d: d + [unit(np.cross(np.cross(d[0], d[1]), np.cross(d[2], d[3])))])([sph(x[2 * i], x[2 * i + 1]) for i in range(4)])),
    'truncated octahedron': (9, lambda x: (lambda p: [unit(p[i] - p[j]) for i, j in itertools.combinations(range(4), 2)])([np.zeros(3), x[0:3], x[3:6], x[6:9]])),
}

def miss(S, sigma):
    s = 0.0
    for a, b in itertools.combinations(S, 2):
        t = line_angle(a, b)
        d = min(abs(t - x) for x in SPECIAL)
        s += 1 - math.exp(-d * d / (2 * sigma * sigma))
    return s

def bottom_up(starts, seed=1):
    from scipy.optimize import minimize
    rng = np.random.default_rng(seed)
    found = {}
    for typ, (n, build) in PARAMS.items():
        for _ in range(starts):
            x = rng.uniform(0, 2 * math.pi, n) if typ != 'truncated octahedron' else rng.normal(size=n)
            for sigma in (12, 6, 3, 1.5, 0.75, 0.3):
                try:
                    x = minimize(lambda y: miss(build(y), sigma), x, method='Nelder-Mead', options={'xatol': 1e-10, 'fatol': 1e-12, 'maxiter': 4000}).x
                except (ValueError, ZeroDivisionError, FloatingPointError):
                    break
            try:
                S = [unit(g) for g in build(x)]
            except Exception:
                continue
            if not all(np.isfinite(g).all() for g in S): continue
            if any(abs(abs(a @ b) - 1) < 1e-6 for a, b in itertools.combinations(S, 2)): continue
            if not all(min(abs(line_angle(a, b) - s) for s in SPECIAL) < 1e-3 for a, b in itertools.combinations(S, 2)): continue
            S = snap(S)
            if S is not None and all_special(S): add(found, S)
    return found

def snap(S):
    """Rebuild an almost-special set exactly: re-solve from three independent directions."""
    for i, j, k in itertools.combinations(range(len(S)), 3):
        if abs(np.linalg.det(np.array([S[i], S[j], S[k]]))) > 1e-3: break
    else:
        return None
    order = [i, j, k] + [m for m in range(len(S)) if m not in (i, j, k)]
    S = [S[m] for m in order]
    nearest = lambda c: min(COS, key=lambda x: abs(x - c))
    G = np.array([[1.0 if a is b else nearest(float(a @ b)) for b in S] for a in S])
    w, V = np.linalg.eigh(G)
    if w[:-3].size and abs(w[:-3]).max() > 1e-7 or w[-3:].min() < 1e-7: return None
    X = V[:, -3:] * np.sqrt(w[-3:])
    return [X[m] for m in range(len(S))]

def flatten(found):
    return [S for bucket in found.values() for _, S in bucket]

if __name__ == '__main__':
    starts = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    td = top_down()
    print('top-down:', len(flatten(td)), flush=True)
    bu = bottom_up(starts)
    print('bottom-up:', len(flatten(bu)), flush=True)
    keys_td = {canon(S) for S in flatten(td)}
    keys_bu = {canon(S) for S in flatten(bu)}
    print('bottom-up shapes missing from top-down:', len(keys_bu - keys_td))
    out = sorted((record(S) for S in flatten(td)), key=lambda r: (r['directions'], r['type'], r['line_angles'], r['volume']))
    for r, S in zip(out, []): pass
    for r in out: r['bottom_up_also_found'] = None
    bu_keys = keys_bu
    recs = []
    for S in flatten(td):
        r = record(S); r['bottom_up_also_found'] = canon(S) in bu_keys; recs.append(r)
    recs.sort(key=lambda r: (r['directions'], r['type'], r['line_angles'], r['volume']))
    extra = [record(S) for S in flatten(bu) if canon(S) not in keys_td]
    json.dump({'special_angles': [round(s, 4) for s in SPECIAL], 'targets': recs, 'bottom_up_only': extra}, open('data/geometry-targets.json', 'w'), indent=1)
    from collections import Counter
    print(Counter(r['type'] for r in recs))
    print('found both ways:', sum(r['bottom_up_also_found'] for r in recs), 'of', len(recs))
