# EXACT check of the UP cycle (DICTO 2026-10-19): ID -> RT -> golden truncated icosahedron -> Q -> ID, scale exactly 10/phi^4.
# Arithmetic in Q(sqrt5) with Fractions: a number is a + b*sqrt5; signs are decided exactly. The step rule needs no square
# roots: the face through corner v at right angles to v is  v . x = v . v.  Float is used only to GUESS which three faces meet
# at each corner; every guess is then proved exactly:
#   (1) each corner solves its three faces exactly and satisfies every face  v.x <= v.v  exactly (so it is in the solid);
#   (2) each listed face holds >= 3 corners exactly, all other corners strictly inside it, so it is a true face of their hull;
#   (3) the listed faces close up: every edge lies in exactly two of them (Euler V - E + F = 2), so they are ALL the hull's faces,
#       hence hull(corners) = the solid cut out by the planes, and the corner list is complete.
import itertools, json, os
from fractions import Fraction as Fr
import numpy as np

class Q5:
    __slots__ = ('a', 'b')
    def __init__(s, a, b=0): s.a, s.b = Fr(a), Fr(b)
    def __add__(s, o): o = o if isinstance(o, Q5) else Q5(o); return Q5(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __neg__(s): return Q5(-s.a, -s.b)
    def __sub__(s, o): return s + (-(o if isinstance(o, Q5) else Q5(o)))
    def __rsub__(s, o): return Q5(o) - s
    def __mul__(s, o): o = o if isinstance(o, Q5) else Q5(o); return Q5(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def __truediv__(s, o):
        o = o if isinstance(o, Q5) else Q5(o); n = o.a * o.a - 5 * o.b * o.b; assert n != 0
        return s * Q5(o.a / n, -o.b / n)
    def sign(s):                      # exact sign of a + b sqrt5
        if s.b == 0: return (s.a > 0) - (s.a < 0)
        if s.a == 0: return (s.b > 0) - (s.b < 0)
        if (s.a > 0) == (s.b > 0): return 1 if s.a > 0 else -1
        return (1 if s.a > 0 else -1) * (1 if s.a * s.a > 5 * s.b * s.b else -1)
    def __eq__(s, o): o = o if isinstance(o, Q5) else Q5(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def f(s): return float(s.a) + float(s.b) * 5 ** .5
    def __repr__(s): return f'{s.a}+{s.b}r5'

PHI = Q5(Fr(1, 2), Fr(1, 2))
dot = lambda u, v: u[0] * v[0] + u[1] * v[1] + u[2] * v[2]
def det3(M): return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
                     + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
def solve3(A, b):                     # Cramer, exact
    d = det3(A); out = []
    for c in range(3):
        M = [[(b[r] if k == c else A[r][k]) for k in range(3)] for r in range(3)]; out.append(det3(M) / d)
    return tuple(out)
fv = lambda v: np.array([x.f() for x in v])

def step(S):
    """Exact next solid of the UP rule, proved as in the header. Returns its corners (exact)."""
    P = [(v, dot(v, v)) for v in S]                                  # faces  v.x <= v.v
    Nf = np.array([fv(v) for v in S]); df = np.array([c.f() for _, c in P])
    from scipy.spatial import HalfspaceIntersection
    X = HalfspaceIntersection(np.hstack([Nf, -df[:, None]]), np.zeros(3)).intersections
    X = X[np.unique(np.round(X, 8), axis=0, return_index=True)[1]]
    C = []
    for x in X:                                                       # guess 3 independent tight faces, then solve exactly
        tight = [i for i in range(len(P)) if abs(Nf[i] @ x - df[i]) < 1e-7]
        for tri in itertools.combinations(tight, 3):
            if abs(np.linalg.det(Nf[list(tri)])) > 1e-6: break
        c = solve3([list(P[i][0]) for i in tri], [P[i][1] for i in tri]); C.append(c)
    C = list(dict.fromkeys(C))
    # (1) every corner inside every face, exactly
    T = [[(dot(v, c) - h).sign() for (v, h) in P] for c in C]
    assert all(t <= 0 for row in T for t in row), 'a corner lies outside a face'
    # (2) faces of the hull: planes holding >= 3 corners (all others strictly inside by (1) unless also tight)
    faces = [[j for j in range(len(C)) if T[j][i] == 0] for i in range(len(P))]
    faces = [f for f in faces if len(f) >= 3]
    for f in faces:
        pts = np.array([fv(C[j]) for j in f]); assert np.linalg.matrix_rank(pts - pts[0], tol=1e-9) == 2
    for j in range(len(C)): assert sum(T[j][i] == 0 for i in range(len(P))) >= 3, 'not a corner'
    # (3) closed surface: order each face's corners, every edge in exactly two faces, Euler
    edges = {}
    for f in faces:
        pts = np.array([fv(C[j]) for j in f]); c0 = pts.mean(0); n = np.cross(pts[1] - pts[0], pts[2] - pts[0])
        B = np.linalg.svd(pts - c0)[2][:2]; order = [f[k] for k in np.argsort(np.arctan2((pts - c0) @ B[1], (pts - c0) @ B[0]))]
        for a, b in zip(order, order[1:] + order[:1]): edges[frozenset((a, b))] = edges.get(frozenset((a, b)), 0) + 1
    assert all(m == 2 for m in edges.values()), 'surface not closed'
    assert len(C) - len(edges) + len(faces) == 2, 'Euler fails'
    return C, len(faces), len(edges)

if __name__ == '__main__':
    h, p, p2 = Q5(Fr(1, 2)), PHI / 2, PHI * PHI / 2                    # ID of radius phi (standard coordinates)
    ID = set()
    for perm in range(3):
        for s in itertools.product((1, -1), repeat=1):
            v = [Q5(0)] * 3; v[perm] = PHI * s[0]; ID.add(tuple(v))
        for s in itertools.product((1, -1), repeat=3):
            base = [h * s[0], p * s[1], p2 * s[2]]; ID.add(tuple(base[(k - perm) % 3] for k in range(3)))
    ID = sorted(ID, key=lambda v: tuple(x.f() for x in v)); assert len(ID) == 30
    assert all(dot(v, v) == PHI * PHI for v in ID)                    # all on radius phi, exactly
    log = {'mark': 'DICTO Universal PiTet (UP), exact cycle check, 2026-10-19', 'start': 'icosidodecahedron, radius phi, standard coordinates'}
    S = ID; names = ['RT', 'golden truncated icosahedron', 'Q (pentakis type)', 'ID again']
    for nm in names:
        S, nf, ne = step(S); log[nm] = {'corners': len(S), 'faces': nf, 'edges': ne}; print(nm, log[nm], flush=True)
    k = Q5(35, -15); assert (k - Q5(10) / (PHI * PHI * PHI * PHI)) == Q5(0)    # 10/phi^4 = 35 - 15 sqrt5
    target = {tuple(k * x for x in v) for v in ID}
    log['returns_exactly_scaled_by_10_over_phi4'] = set(S) == target
    print('ID returns exactly, scaled by 10/phi^4 = 35 - 15 sqrt5:', log['returns_exactly_scaled_by_10_over_phi4'])
    json.dump(log, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'exact_cycle.json'), 'w'), indent=1)
