#!/usr/bin/env python3
"""General Dehn screen (Concordance 6.1 Dehn column, OG / golden-nest row). Input: corners + ordered faces (any orientation; fixed to outward by signed volume).
Dehn(P) = Σ_e L_e ⊗ θ_e in R ⊗_Q R/Qπ, θ_e interior dihedral (works for non-convex). Lengths identified in Q(√2, √5) (basis 1, √2, √5, √10, via PSLQ);
component b: S_b = Σ c_b(L_e) θ_e; Dehn = 0 iff every S_b ∈ Qπ (basis elements Q-independent). Rationality of S_b/π tested by continued fractions (denominator <= 2520, tol 1e-8).
This is a numerical screen: a 'zero' must be confirmed exactly; a 'nonzero' is robust only if the S_b/π residue is far above the tolerance."""
import sys, json, math, itertools, numpy as np
from fractions import Fraction
import mpmath as mp
BASIS = [1.0, math.sqrt(2), math.sqrt(5), math.sqrt(10)]
def identify(x):
    r = mp.pslq([mp.mpf(x)] + [mp.mpf(b) for b in BASIS], maxcoeff=10**6, maxsteps=10**5, tol=mp.mpf(10)**-11)
    if r is None or r[0] == 0: return None
    return [Fraction(-c, r[0]) for c in r[1:]]
def dehn(Vx, F, name='', extra_rows=None, rows_only=False):
    V = np.asarray(Vx, float)
    vol = sum(np.dot(V[f[0]], np.cross(V[f[i]], V[f[i+1]])) for f in F for i in range(1, len(f) - 1))/6
    if vol < 0: F = [f[::-1] for f in F]
    def normal(f):
        n = np.zeros(3)
        for i in range(len(f)): n += np.cross(V[f[i]], V[f[(i+1) % len(f)]])
        return n/np.linalg.norm(n)
    N = [normal(f) for f in F]; E = {}
    for fi, f in enumerate(F):
        for i in range(len(f)):
            a, b = f[i], f[(i+1) % len(f)]; E.setdefault((a, b), fi)
    rows = []
    for (a, b), f1 in E.items():
        if a > b: continue
        f2 = E.get((b, a))
        if f2 is None: raise ValueError('open edge')
        n1, n2 = N[f1], N[f2]; L = np.linalg.norm(V[b] - V[a]); e = (V[b] - V[a])/L
        ang = math.atan2(np.dot(np.cross(n1, n2), e), np.dot(n1, n2))   # signed turn between outward normals about the edge
        theta = math.pi - ang   # interior dihedral; ang>0 convex (theta<pi) with this orientation convention, checked on the cube
        if abs(ang) < 1e-9: continue    # flat edge (coplanar faces) contributes nothing
        rows.append((L, theta))
    if extra_rows: rows = rows + extra_rows
    if rows_only: return rows
    # distinct angles; integer relations among them and pi (PSLQ, small coefficients) -> reduce to a basis beta_j independent mod Q*pi
    angs = []
    for L, th in rows:
        if not any(abs(th - a) < 1e-8 for a in angs): angs.append(th)
    mp.mp.dps = 30
    # express each angle as rational multiple of pi + integer combination of basis angles: greedy basis build
    basis = []; coef = {}   # coef[i] = (dict basis_index -> Fraction)
    for i, a in enumerate(angs):
        vec = [mp.mpf(a)] + [mp.mpf(angs[b]) for b in basis] + [mp.pi]
        r = mp.pslq(vec, maxcoeff=int(sys.argv[3]) if len(sys.argv) > 3 else 200, maxsteps=10**5, tol=mp.mpf(10)**-int(sys.argv[2] if len(sys.argv) > 2 else 10))
        if r is not None and r[0] != 0:
            coef[i] = {b: Fraction(-r[1 + j], r[0]) for j, b in enumerate(basis)}
        else:
            basis.append(i); coef[i] = {i: Fraction(1)}
    X = {b: 0.0 for b in basis}; scale = max(L for L, _ in rows)
    for L, th in rows:
        i = next(k for k, a in enumerate(angs) if abs(th - a) < 1e-8)
        for b, c in coef[i].items(): X[b] += float(c)*L
    resid = {f'{math.degrees(angs[b]):.6f}deg': X[b]/scale for b in basis}
    zero = all(abs(v) < 1e-9 for v in resid.values())
    rational = [f'{math.degrees(a):.4f}' for i, a in enumerate(angs) if not coef[i]]
    return {'name': name, 'edges': len(rows), 'distinct_angles': len(angs), 'basis_angles': len(basis), 'rational_pi_angles_deg': rational,
            'coefficient_sums_over_maxL': resid, 'dehn_zero': bool(zero)}
def hull_faces(P):
    from scipy.spatial import ConvexHull
    P = np.asarray(P, float); h = ConvexHull(P); fs = {}
    for eq, s in zip(h.equations, h.simplices):
        k = tuple(np.round(eq, 7)); fs.setdefault(k, set()).update(s)
    F = []
    for k, idx in fs.items():
        idx = list(idx); n = np.array(k[:3]); c = P[idx].mean(0); u = P[idx[0]] - c; w = np.cross(n, u)
        F.append(sorted(idx, key=lambda i: math.atan2(np.dot(P[i] - c, w), np.dot(P[i] - c, u))))
    return P, F
if __name__ == '__main__':
    phi = (1 + 5**.5)/2
    def perms(v, even=False):
        out = set()
        for p in itertools.permutations(range(3)):
            sgn = 1
            if even and p not in [(0,1,2),(1,2,0),(2,0,1)]: continue
            for s in itertools.product((1, -1), repeat=3): out.add(tuple(s[i]*v[p[i]] for i in range(3)))
        return list(out)
    CAL = {
     'cube (0)': perms((1, 1, 1)), 'tetrahedron (≠0)': [(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)], 'octahedron (≠0)': perms((1, 0, 0)),
     'rhombic dodecahedron (0)': perms((1, 0, 0)) and perms((2, 0, 0)) + perms((1, 1, 1)), 'truncated octahedron (0)': perms((0, 1, 2)),
     'icosahedron (≠0)': [p for q in [(0, 1, phi)] for p in perms(q, even=True)], 'T(4) minus corners (0)': None,
     'dodecahedron (≠0)': perms((1, 1, 1)) + [p for p in perms((0, 1/phi, phi), even=True)],
    }
    V0 = np.array([(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)], float)
    CAL['T(4) minus corners (0)'] = [V0[i] + (V0[j] - V0[i])/4 for i in range(4) for j in range(4) if i != j]
    CAL['Archimedean truncated tetrahedron (≠0)'] = [V0[i] + (V0[j] - V0[i])/3 for i in range(4) for j in range(4) if i != j]
    ID = perms((phi, 0, 0)) + [p for p in perms((0.5, phi/2, phi**2/2), even=True)]
    from scipy.spatial import HalfspaceIntersection
    H = np.array([[*v, -1.0] for v in np.unique(np.round(ID, 12), axis=0)]); CAL['rhombic triacontahedron (0)'] = HalfspaceIntersection(H, np.zeros(3)).intersections
    out = []
    for nm, P in CAL.items():
        P, F = hull_faces(np.unique(np.round(np.asarray(P, float), 10), axis=0)); r = dehn(P, F, nm); out.append(r)
        print(f"{nm:42s} zero={r['dehn_zero']!s:5s} basis={r['basis_angles']} sums={ {k: round(v, 10) for k, v in r['coefficient_sums_over_maxL'].items()} }")
    if len(sys.argv) > 1:
        d = json.load(open(sys.argv[1]))
        for nm in d['order']:
            s = d['solids'][nm]; P = np.asarray(s['v'], float)
            from scipy.spatial import ConvexHull
            hv = len(ConvexHull(P).vertices); convex = hv == len(P)
            try: r = dehn(P, s['f'], nm)
            except ValueError: P2, F2 = hull_faces(P); r = dehn(P2, F2, nm + ' (hull)') if convex else {'name': nm, 'error': 'open edge, non-convex'}
            r['convex'] = bool(convex); out.append(r)
            print(f"{nm:42s} convex={convex} zero={r.get('dehn_zero')} basis={r.get('basis_angles')} sums={ {k: round(v, 10) for k, v in r.get('coefficient_sums_over_maxL', {}).items()} } {r.get('error','')}")
    json.dump(out, open('data/dehn-screen.json', 'w'), indent=1)
