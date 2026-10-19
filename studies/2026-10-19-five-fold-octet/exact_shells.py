# EXACT check of the pieces in the four UP shells (DICTO 2026-10-19), in Q(sqrt5), on the exact solids of exact_cycle.py.
# Pieces: one per face F of the inner solid = (cone from the centre over F) cut by the outer solid and by F's plane. The cones over
# the faces of a convex solid round the centre fill space without overlap, so these pieces partition the gap by construction;
# what is checked exactly here is what they ARE: corners (proved as in exact_cycle.step), exact volumes, sum = gap exactly, which
# faces they share (walls), and that the faces of each kind form ONE symmetry orbit (so all pieces of a kind are congruent), using
# the 60 exact rotations of the icosahedral group. For the ID -> RT shell the finer stage-3 cut (12 + 20 pyramids + 60 valley
# tetrahedra) is checked exactly too: volumes sum to the gap and every piece lies inside the RT (no exact overlap test; the
# float random-point test in cyclecheck.py found no overlap).
import itertools, json, os
from collections import Counter
import numpy as np
from exact_cycle import Q5, Fr, PHI, dot, solve3, fv, step

def cross(u, v): return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
def sub(u, v): return tuple(a - b for a, b in zip(u, v))
def det3v(a, b, c): return dot(a, cross(b, c))

def polytope(H):
    """Exact corners and ordered faces of {x : n.x <= d for (n, d) in H}, proved: corners inside every half-space, each face
    holds >= 3 corners, every edge in exactly two faces, Euler."""
    from scipy.spatial import HalfspaceIntersection
    N = np.array([fv(n) for n, _ in H]); dd = np.array([d.f() for _, d in H])
    c0 = np.linalg.lstsq(N, dd - 1e-3, rcond=None)[0] if False else None
    # an interior point by linear programming (float), only to start the enumeration
    from scipy.optimize import linprog
    nr = np.linalg.norm(N, axis=1); lp = linprog(np.r_[np.zeros(3), -1], A_ub=np.hstack([N, nr[:, None]]), b_ub=dd, bounds=[(None, None)] * 3 + [(0, None)])
    X = HalfspaceIntersection(np.hstack([N, -dd[:, None]]), lp.x[:3]).intersections
    X = X[np.unique(np.round(X, 8), axis=0, return_index=True)[1]]
    C = []
    for x in X:
        tight = [i for i in range(len(H)) if abs(N[i] @ x - dd[i]) < 1e-7 * max(1, nr[i])]
        for tri in itertools.combinations(tight, 3):
            if abs(np.linalg.det(N[list(tri)])) > 1e-9: break
        C.append(solve3([list(H[i][0]) for i in tri], [H[i][1] for i in tri]))
    C = list(dict.fromkeys(C))
    T = [[(dot(n, c) - d).sign() for (n, d) in H] for c in C]
    assert all(t <= 0 for row in T for t in row)
    faces = []
    for i in range(len(H)):
        f = [j for j in range(len(C)) if T[j][i] == 0]
        if len(f) < 3: continue
        pts = np.array([fv(C[j]) for j in f])
        if np.linalg.matrix_rank(pts - pts[0], tol=1e-9) < 2: continue
        c = pts.mean(0); B = np.linalg.svd(pts - c)[2][:2]; o = [f[k] for k in np.argsort(np.arctan2((pts - c) @ B[1], (pts - c) @ B[0]))]
        if any(set(o) == set(g) for g, _ in faces): continue          # same face from a repeated plane
        faces.append((o, i))
    edges = Counter(frozenset(e) for o, _ in faces for e in zip(o, o[1:] + o[:1]))
    assert all(m == 2 for m in edges.values()) and len(C) - len(edges) + len(faces) == 2
    return C, faces

def volume(C, faces):
    """Exact volume: fan from the corner average over each face."""
    n = len(C); g = tuple(sum((c[k] for c in C), Q5(0)) / n for k in range(3)); V = Q5(0)
    for o, _ in faces:
        for a, b in zip(o[1:-1], o[2:]):
            v = det3v(sub(C[o[0]], g), sub(C[a], g), sub(C[b], g)); V = V + (v if v.sign() >= 0 else -v)
    return V / 6

def solid(S):
    """Exact half-spaces of the next-step solid built on corners S (faces v.x <= v.v) are not needed here; we need S's own hull."""
    from scipy.spatial import ConvexHull
    h = ConvexHull(np.array([fv(v) for v in S])); H = []; seen = set()
    for e in h.equations:
        idx = [j for j in range(len(S)) if abs(np.array(fv(S[j])) @ e[:3] + e[3]) < 1e-9]
        if frozenset(idx) in seen: continue                                  # the same face from another hull triangle
        seen.add(frozenset(idx))
        for a_, b_, c_ in itertools.combinations(idx, 3):                    # three corners not in a line
            n = cross(sub(S[b_], S[a_]), sub(S[c_], S[a_]))
            if any(x != Q5(0) for x in n): break
        d = dot(n, S[idx[0]])
        if any((dot(n, v) - d).sign() > 0 for v in S): n, d = tuple(-x for x in n), -d   # orient: the solid on the inner side
        assert all((dot(n, v) - d).sign() <= 0 for v in S) and all((dot(n, S[j]) - d) == Q5(0) for j in idx)
        H.append((n, d))
    return H

def rotations():
    """The 60 exact rotations of the icosahedral group in the standard frame."""
    h = Fr(1, 2); ip = PHI - 1
    R = ((Q5(h), -PHI / 2, ip / 2), (PHI / 2, ip / 2, Q5(-h)), (ip / 2, Q5(h), PHI / 2))
    P = ((Q5(0), Q5(1), Q5(0)), (Q5(0), Q5(0), Q5(1)), (Q5(1), Q5(0), Q5(0)))
    mul = lambda A, B: tuple(tuple(sum((A[i][k] * B[k][j] for k in range(3)), Q5(0)) for j in range(3)) for i in range(3))
    I3 = tuple(tuple(Q5(1 if i == j else 0) for j in range(3)) for i in range(3)); G = {I3}; fr = [I3]
    while fr:
        nw = []
        for g in fr:
            for s in (R, P):
                m = mul(s, g)
                if m not in G: G.add(m); nw.append(m)
        fr = nw
    assert len(G) == 60, len(G)
    return list(G)
app = lambda M, v: tuple(sum((M[i][k] * v[k] for k in range(3)), Q5(0)) for i in range(3))

def shell(Sin, Sout, G, label):
    Hin, Hout = solid(Sin), solid(Sout)
    for M in G[:5]: assert {app(M, v) for v in Sin} == set(Sin)                      # frame: the group fixes the solids
    Cin, Fin = polytope(Hin); Cout, Fout = polytope(Hout); gap = volume(Cout, Fout) - volume(Cin, Fin)
    pieces, kinds = [], Counter(); total = Q5(0); vols = {}
    for o, i in Fin:
        F = [Cin[j] for j in o]; n, d = Hin[i]
        H = list(Hout) + [(tuple(-x for x in n), -d)]
        for a, b in zip(F, F[1:] + F[:1]):
            m = cross(a, b); m = m if dot(m, F[0] if dot(m, F[0]).sign() != 0 else F[2]).sign() < 0 or True else m
            # wall through the centre and edge ab, oriented so the face's other corners are inside
            other = [c for c in F if c not in (a, b)][0]
            if dot(m, other).sign() > 0: m = tuple(-x for x in m)
            H.append((m, Q5(0)))
        C, Fc = polytope(H); v = volume(C, Fc); total = total + v
        key = f'on {len(F)}-gon'; vols.setdefault(key, set()).add(v); kinds[key] += 1; pieces.append((key, frozenset(F)))
    # one orbit per kind: images of one face of each kind give all faces of that kind
    orbit = {}
    for key in kinds:
        F0 = next(F for k, F in pieces if k == key); imgs = {frozenset(app(M, v) for v in F0) for M in G}
        orbit[key] = imgs == {F for k, F in pieces if k == key}
    out = {'shell': label, 'pieces': dict(kinds), 'exact_volumes': {k: [repr(x) for x in v] for k, v in vols.items()},
           'one_volume_per_kind': all(len(v) == 1 for v in vols.values()), 'one_symmetry_orbit_per_kind': orbit,
           'sum_equals_gap_exactly': (total - gap) == Q5(0), 'gap': repr(gap)}
    print(json.dumps(out), flush=True); return out

if __name__ == '__main__':
    from exact_cycle import Q5 as _
    exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'exact_cycle.py')).read().split("if __name__ == '__main__':")[1]
         .split("    log = {")[0].replace('\n    ', '\n'))                         # the exact ID of radius phi
    G = rotations()
    S = [ID];
    for _k in range(4): S.append(step(S[-1])[0])
    res = {'mark': 'DICTO Universal PiTet (UP), exact shell pieces, 2026-10-19', 'shells': []}
    for a, b, nm in zip(S, S[1:], ['ID -> RT', 'RT -> golden truncated icosahedron', 'golden truncated icosahedron -> Q', 'Q -> ID x 10/phi^4']):
        res['shells'].append(shell(a, b, G, nm))
    # the finer stage-3 cut of ID -> RT: 12 + 20 pyramids + 60 valley tetrahedra
    ID_, RT_ = S[0], S[1]; R5 = [v for v in RT_ if len([w for w in ID_ if (dot(v, w) - dot(w, w)).sign() == 0]) == 5]
    Hin = solid(ID_); Cin, Fin = polytope(Hin); Hout = solid(RT_); Cout, Fout = polytope(Hout)
    gap = volume(Cout, Fout) - volume(Cin, Fin); parts = []
    for o, i in Fin:                                                            # pyramid on each ID face to the RT corner above it
        n, d = Hin[i]; apex = max(RT_, key=lambda v: (dot(v, n) / Q5(1)).f() - 0)
        parts.append(([Cin[j] for j in o] + [apex]))
    Eid = {frozenset(e) for o, _ in Fin for e in zip(o, o[1:] + o[:1])}
    for e in Eid:                                                               # valley tetrahedron on each ID edge
        a, b = [Cin[j] for j in e]; m = tuple(x + y for x, y in zip(a, b))
        ups = sorted(RT_, key=lambda v: -(fv(v) @ fv(m)) / np.linalg.norm(fv(v)))[:2]; parts.append([a, b] + ups)
    tv = Q5(0)
    for P in parts:
        from scipy.spatial import ConvexHull
        hc = ConvexHull(np.array([fv(v) for v in P])); Hp = []
        for s in hc.simplices:
            n = cross(sub(P[s[1]], P[s[0]]), sub(P[s[2]], P[s[0]])); d = dot(n, P[s[0]])
            if any((dot(n, q) - d).sign() > 0 for q in P): n, d = tuple(-x for x in n), -d
            Hp.append((n, d))
        C, Fc = polytope(Hp); tv = tv + volume(C, Fc)
        assert all((dot(n, c) - d).sign() <= 0 for c in C for n, d in Hout)                       # inside the RT
    res['stage3_fine_cut'] = {'pieces': len(parts), 'sum_equals_gap_exactly': (tv - gap) == Q5(0)}
    print(res['stage3_fine_cut'])
    json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'exact_shells.json'), 'w'), indent=1)
