"""Exact enumeration of equal-edge zonohedral parallelohedra on the 15
icosahedral two-fold directions (the target list's starting set), up to
congruence. A zonohedron with equal-length edges is fixed, up to rotation,
by the Gram matrix of its directions up to signed permutation; all are
centrally symmetric, so mirror images are the same shape."""
import itertools, math, json
import numpy as np
P = (1 + 5 ** 0.5) / 2
L = []
for k in range(3):
    e = [0, 0, 0]; e[k] = 1; L.append(e)
    for s1 in (1, -1):
        for s2 in (1, -1):
            q = [0, 0, 0]; q[k] = .5; q[(k + 1) % 3] = s1 * P / 2; q[(k + 2) % 3] = s2 / (2 * P); L.append(q)
L = [np.array(v) / np.linalg.norm(v) for v in L]

from enumerate_lib import planes, is_parallelohedron, canon, volume

TYPES = {6: 'parallelepiped (cube type)', 8: 'hexagonal prism', 12: None, 14: 'truncated octahedron'}

def phi_form(x):
    for d in (1, 2, 4):
        for a in range(-12, 13):
            for b in range(-12, 13):
                if abs(x - (a + b * P) / d) < 1e-9:
                    s = ('' if a == 0 else str(a)) + ('' if b == 0 else ('+' if a and b > 0 else '') + ('' if abs(b) == 1 else str(b)) + ('-' if b == -1 else '') + 'φ')
                    return (s or '0') + ('' if d == 1 else f'/{d}')
    for d in (1, 2, 4):
        for k in range(1, 40):
            if abs(x - math.sqrt(k) / d) < 1e-9 or abs(x - k / d) < 1e-9: pass
    return f'{x:.6f}'

classes = {}
for n in range(3, 7):
    for S in itertools.combinations(L, n):
        S = list(S)
        if not is_parallelohedron(S): continue
        f = 2 * len(planes(S))
        typ = TYPES.get(f) or ('rhombic dodecahedron' if n == 4 else 'elongated dodecahedron')
        key = canon(S)
        if key in classes: continue
        angs = sorted(round(math.degrees(math.acos(min(1, abs(a @ b))))) for a, b in itertools.combinations(S, 2))
        faces = {}
        for a, b in itertools.combinations(S, 2):
            t = round(math.degrees(math.acos(min(1, abs(a @ b)))))
            nm = 'square' if t == 90 else f'{t}° rhombus'
            # each direction pair is one face pair, plus merges in hexagons for coplanar triples (counted by planes)
            faces[nm] = faces.get(nm, 0) + 2
        classes[key] = {'type': typ, 'directions': n, 'faces': 2 * len(planes(S)), 'line_angles': angs, 'volume': phi_form(volume(S))}
out = sorted(classes.values(), key=lambda c: (c['directions'], c['type'], c['line_angles']))
json.dump(out, open('targets.json', 'w'), indent=1, ensure_ascii=False)
from collections import Counter
print(Counter(c['type'] for c in out), len(out))
