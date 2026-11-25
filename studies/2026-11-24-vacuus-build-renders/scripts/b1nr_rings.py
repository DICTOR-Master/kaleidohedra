"""B1NR cube as DICTO built it (25 Nov): bottle rings folded into rounded triangles. Each of the 12 fins (centre O + one cube edge) is a 3 x 3
triangular grid of 9 rounded-triangle rings; neighbours share sides (touch, no overlap); no struts; the rounded corners leave an open space
where the 12 fins meet at the centre. Cube [-1,1]^3. Usage: python b1nr_rings.py <out.html>. House renderer render3d.py (unchanged)."""
import sys, os, itertools, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../2026-11-21-scutoid-stand-in/renders/scripts'))
import render3d
O = np.zeros(3)
CV = [np.array(p, float) for p in itertools.product((-1, 1), repeat=3)]
CE = [(p, q) for p, q in itertools.combinations(CV, 2) if abs(np.linalg.norm(p - q) - 2) < 1e-9]
assert len(CE) == 12
W, R, GAP = 0.10, 0.125, 0.006          # band width (across the fin), corner radius (very round, as the photo), half-gap
WHITE = '#f4f3ee'
def rounded(A, B, C, n):
    """outline of the ring in the small triangle ABC: the triangle offset inward by R + GAP, then outward by R (rounded corners)"""
    la, lb, lc = np.linalg.norm(B - C), np.linalg.norm(C - A), np.linalg.norm(A - B)
    I = (la * A + lb * B + lc * C) / (la + lb + lc); rho = np.linalg.norm(np.cross(B - A, C - A)) / (la + lb + lc)
    d = R + GAP; assert d < rho
    T = [I + (V - I) * (rho - d) / rho for V in (A, B, C)]
    pts = []
    for k in range(3):
        P0, P1, P2 = T[k - 1], T[k], T[(k + 1) % 3]
        def outn(p, q):
            e = (q - p) / np.linalg.norm(q - p); m = np.cross(e, n); return m if np.dot(m, p - I) > 0 else -m
        n1, n2 = outn(P0, P1), outn(P1, P2)
        a1 = np.arctan2(np.dot(np.cross(n1, n2), n), np.dot(n1, n2))
        u = n1; v = np.cross(n, n1)
        for t in np.linspace(0, a1, 10): pts.append(P1 + R * (np.cos(t) * u + np.sin(t) * v))
    return pts
def band(pts, n, col):
    V, Tr = [], []
    K = len(pts)
    for p in pts: V += [p + n * W / 2, p - n * W / 2]
    for k in range(K):
        a, b, c, d = 2 * k, 2 * k + 1, 2 * ((k + 1) % K), 2 * ((k + 1) % K) + 1
        Tr += [[a, b, c], [b, d, c], [a, c, b], [b, c, d]]       # both windings: visible from both sides
    return V, Tr
def fin_rings(a, b):
    n = np.cross(a, b); n /= np.linalg.norm(n)
    P = lambda i, j: O + a * i / 3 + b * j / 3
    tri = [(P(i, j), P(i + 1, j), P(i, j + 1)) for i in range(3) for j in range(3 - i)] + \
          [(P(i + 1, j), P(i + 1, j + 1), P(i, j + 1)) for i in range(2) for j in range(2 - i)]
    assert len(tri) == 9
    return [(rounded(*t, n), n) for t in tri]
def part(fins, shift=np.zeros(3)):
    V, T, C = [], [], []
    for a, b in fins:
        for pts, n in fin_rings(a, b):
            v, t = band(pts, n, WHITE); off = len(V); V += [x - shift for x in v]; T += [[x + off for x in tt] for tt in t]; C += [WHITE] * len(t)
    return {'v': np.round(np.array(V), 6).tolist(), 't': T, 'c': C, 'a': 1.0, 'tubes': [], 'rad': 0.01, 'balls': []}
rings = sum(len(fin_rings(a, b)) for a, b in CE)
a0, b0 = CE[0]; n0 = np.cross(a0, b0); n0 /= np.linalg.norm(n0)
centre_space = min(np.linalg.norm(p) for a, b in CE for pts, n in fin_rings(a, b) for p in pts)
print('rings', rings, 'fins', len(CE), 'open space radius at the centre %.4f (cube half-edge 1)' % centre_space)
scenes = [{'E': 1.95, 'dir': [1.0, 0.62, 1.45], 'parts': [part(CE)]},
          {'E': 1.25, 'dir': list(n0 + 0.35 * (CE[0][0] + CE[0][1]) / np.linalg.norm(CE[0][0] + CE[0][1])), 'parts': [part([CE[0]], (CE[0][0] + CE[0][1]) / 3)]}]
render3d.write(sys.argv[1], scenes)
print('FINAL ok' if rings == 108 and centre_space > 0 else 'FINAL FAIL')
