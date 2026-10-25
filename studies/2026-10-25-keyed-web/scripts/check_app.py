# Float cross-check: the app's own keyed network (app_dump.mjs -> ../data/app-keyed.json, size 2, all keyed): for the central Lotus
# Jewel Axes (anchor 0) and Dodecaxes (anchor (φ/2)(1,1,1)) sum the overlap areas of coplanar, oppositely facing mesh faces (convex polygons) with
# every other piece; compare with the exact closed forms of keyed_web_exact.py.
import json, math, os
from collections import defaultdict
D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'app-keyed.json')))
PHI = (1 + 5 ** .5) / 2; t36 = math.tan(math.pi / 5)
sub = lambda a, b: [a[i] - b[i] for i in range(3)]; dot = lambda a, b: sum(a[i] * b[i] for i in range(3))
cr = lambda a, b: [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
def tris(p):
    for f in p['F']:
        P = [p['V'][k] for k in f]; A = [0, 0, 0]
        for i in range(len(P)): A = [A[k] + c for k, c in enumerate(cr(P[i], P[(i + 1) % len(P)]))]
        L = math.sqrt(dot(A, A))
        if L > 1e-12: yield [x / L for x in A], P, L / 2
def clip(poly, n, a, b):
    m = cr(n, sub(b, a)); out = []
    for i in range(len(poly)):
        p, q = poly[i], poly[(i + 1) % len(poly)]; vp, vq = dot(m, sub(p, a)), dot(m, sub(q, a))
        if vp >= -1e-12: out.append(p)
        if (vp > 1e-12 and vq < -1e-12) or (vp < -1e-12 and vq > 1e-12): out.append([p[k] + vp / (vp - vq) * (q[k] - p[k]) for k in range(3)])
    return out
def area(poly, n):
    A = [0, 0, 0]
    for i in range(len(poly)): A = [A[k] + c for k, c in enumerate(cr(poly[i], poly[(i + 1) % len(poly)]))]
    return abs(dot(A, n)) / 2
def overlap(na, A, nb, B):
    if dot(na, nb) > -1 + 1e-9 or abs(dot(na, sub(B[0], A[0]))) > 1e-9: return 0.0
    R = A
    B = B if dot(nb, na) > 0 else B[::-1]   # turn B positively about na
    for i in range(len(B)):
        if len(R) < 3: return 0.0
        R = clip(R, na, B[i], B[(i + 1) % len(B)])
    return area(R, na) if len(R) >= 3 else 0.0
T = [list(tris(p)) for p in D]
def bonds(i):
    out = defaultdict(float); ci = D[i]['anchor']
    for j, q in enumerate(D):
        if j == i or math.dist(ci, q['anchor']) > 2 * PHI: continue
        for na, A, _ in T[i]:
            for nb, B, _ in T[j]: out[j] += overlap(na, A, nb, B)
    return {j: a for j, a in out.items() if a > 1e-9}
H = 3 ** .5 * 3 / (8 * PHI) + 0.75 * t36
ok = True
for anchor, other_kind, sq in [([0, 0, 0], 'gsSmall', 0.5), ([PHI / 2] * 3, 'gsBig', 1 / (2 * PHI ** 2))]:
    i = min(range(len(D)), key=lambda k: math.dist(D[k]['anchor'], anchor))
    b = bonds(i); surf = sum(s for *_, s in T[i])
    kinds = sorted((D[j]['role'], round(a, 9)) for j, a in b.items())
    hexes = [a for j, a in b.items() if D[j]['role'] == other_kind]; sqs = [a for j, a in b.items() if D[j]['role'] == D[i]['role']]
    good = len(hexes) == 8 and len(sqs) == 6 and max(abs(a - H) for a in hexes) < 1e-9 and max(abs(a - sq) for a in sqs) < 1e-9 and abs(surf - sum(b.values())) < 1e-9
    ok &= good
    print(('PASS ' if good else 'FAIL ') + f"app {D[i]['role']} at {D[i]['n']}: {len(hexes)} keyed hexagons (max err {max(abs(a - H) for a in hexes):.1e}), {len(sqs)} squares (max err {max(abs(a - sq) for a in sqs):.1e}), surface {surf:.10f} = sum of bonds (err {abs(surf - sum(b.values())):.1e})")
print('ALL PASS' if ok else 'SOME FAIL')
