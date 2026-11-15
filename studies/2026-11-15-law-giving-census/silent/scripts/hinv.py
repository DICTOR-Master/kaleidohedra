#!/usr/bin/env python3
"""Invariant harmonics of the Wythoff groups, exact, in orbit-space coordinates (law-giving census, silent coincidences).

Seed v = sum c_j w_j (c_j = <v, alpha_j>, unit roots).  Basic invariants u_1 = |v|^2, u_i = S_{d_i}(v) = sum_{w in Omega_i} <w, v>^{d_i},
power sums over a G-orbit Omega_i of some fundamental weight w_j; the choice is checked by a nonzero Jacobian (algebraic independence),
and since their degrees are the basic degrees, they generate the invariant ring (Chevalley: Hilbert series prod 1/(1 - t^d_i)).
In c coordinates <grad f, grad g> = sum G_ij d_i f d_j g and Laplacian = sum G_ij d_i d_j (G = Gram matrix of the simple roots).
The metric g_ij = <grad u_i, grad u_j> and L_i = Laplacian u_i are invariants, found EXACTLY in the u-monomial basis by evaluation at
rational seeds (the monomials of weighted degree m are a basis of the degree-m invariants; the evaluation system is solved with extra rows
as a consistency check). The Laplacian then acts on polynomials in u, and the invariant harmonics of degree k are its kernel on the
weighted-degree-k monomials. Their dimension is checked against N(k) - N(k-2).
Key fact used downstream: T_k(v) = 0 (corners silent in degree k) iff every invariant harmonic of degree k vanishes at v.
Usage: hinv.py GROUP KMAX -> data/hinv-GROUP.json
"""
import sys, os, json, itertools, random, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'scripts'))
import exact as X
from exact import K
import groups as GR
from flint import fmpq

DEG = {'A3': [2, 3, 4], 'B3': [2, 4, 6], 'H3': [2, 6, 10], 'A4': [2, 3, 4, 5], 'B4': [2, 4, 6, 8], 'D4': [2, 4, 4, 6],
       'F4': [2, 6, 8, 12], 'H4': [2, 12, 20, 30]}

def orbit(gd, v):
    R = gd['R']; seen = {GR.vkey(v): v}; fr = [v]
    while fr:
        nf = []
        for p in fr:
            for a in R:
                q = GR.refl(p, a); k = GR.vkey(q)
                if k not in seen: seen[k] = q; nf.append(q)
        fr = nf
    return list(seen.values())

def kpow(x, k):
    r = K(1)
    for _ in range(k): r = r*x
    return r

def wmonos(degs, m):
    """exponent tuples e with sum e_i degs_i = m"""
    out = []
    def rec(i, rem, cur):
        if i == len(degs):
            if rem == 0: out.append(tuple(cur))
            return
        for e in range(rem//degs[i] + 1): rec(i + 1, rem - e*degs[i], cur + [e])
    rec(0, m, []); return out

# ---------- polynomials in u: dict exps -> K ----------
def padd(P, Q, s=K(1)):
    R = dict(P)
    for e, c in Q.items():
        R[e] = R.get(e, K(0)) + s*c
        if R[e].iszero(): del R[e]
    return R
def pmul(P, Q):
    R = {}
    for e1, c1 in P.items():
        for e2, c2 in Q.items():
            e = tuple(a + b for a, b in zip(e1, e2)); R[e] = R.get(e, K(0)) + c1*c2
    return {e: c for e, c in R.items() if not c.iszero()}
def pder(P, i):
    R = {}
    for e, c in P.items():
        if e[i] == 0: continue
        f = list(e); f[i] -= 1; R[tuple(f)] = R.get(tuple(f), K(0)) + c*K(e[i])
    return {e: c for e, c in R.items() if not c.iszero()}
def peval(P, u):
    s = K(0)
    for e, c in P.items():
        t = c
        for ui, ei in zip(u, e): t = t*kpow(ui, ei)
        s = s + t
    return s

def solve_exact(A, B):
    """A: list of rows (m x n, m >= n), B: list of rhs columns (each length m). returns list of solution vectors; asserts rank n + consistency"""
    m, n = len(A), len(A[0]); nb = len(B)
    M = [list(A[i]) + [B[j][i] for j in range(nb)] for i in range(m)]
    piv = []; row = 0
    for col in range(n):
        p = next((r for r in range(row, m) if not M[r][col].iszero()), None)
        assert p is not None, 'singular evaluation system'
        M[row], M[p] = M[p], M[row]; iv = M[row][col].inv(); M[row] = [x*iv for x in M[row]]
        for r in range(m):
            if r != row and not M[r][col].iszero():
                f = M[r][col]; M[r] = [x - f*y for x, y in zip(M[r], M[row])]
        piv.append(col); row += 1
    for r in range(n, m):
        assert all(M[r][n + j].iszero() for j in range(nb)), 'inconsistent fit (target not in the span?)'
    return [[M[i][n + j] for i in range(n)] for j in range(nb)]

def nullspace(A, ncols):
    """exact nullspace of matrix A (rows) over K"""
    M = [list(r) for r in A]; m = len(M); piv = []; row = 0
    for col in range(ncols):
        p = next((r for r in range(row, m) if not M[r][col].iszero()), None)
        if p is None: continue
        M[row], M[p] = M[p], M[row]; iv = M[row][col].inv(); M[row] = [x*iv for x in M[row]]
        for r in range(m):
            if r != row and not M[r][col].iszero():
                f = M[r][col]; M[r] = [x - f*y for x, y in zip(M[r], M[row])]
        piv.append(col); row += 1
        if row == m: break
    free = [c for c in range(ncols) if c not in piv]; basis = []
    for fc in free:
        v = [K(0)]*ncols; v[fc] = K(1)
        for i, pc in enumerate(piv): v[pc] = -M[i][fc]
        basis.append(v)
    return basis

class Setup:
    def __init__(s, name):
        s.name = name; s.gd = gd = GR.group_data(name); s.r = gd['r']; s.degs = DEG[name]; s.D = gd['D']
        s.G = gd['G']; s.Gw = gd['Gw']; W = gd['W']
        orbs = []
        for j in range(s.r):
            O = orbit(gd, W[j]); hat = [[GR.dot(w, W[i]) for i in range(s.r)] for w in O]
            # keep one of each +- pair when -1 is in the group image (even degrees only would need it; keep all, simpler)
            orbs.append((j, len(O), hat))
        orbs.sort(key=lambda t: t[1]); s.orbs = orbs
        # choose an orbit per basic degree (>2) giving a nonzero Jacobian at a random rational point
        rnd = random.Random(1)
        c0 = [K(fmpq(rnd.randint(1, 9), rnd.randint(1, 5))) for _ in range(s.r)]
        best = None
        for choice in itertools.product(range(len(orbs)), repeat=len(s.degs) - 1):
            s.choice = choice
            J = [s.grad(i, c0) for i in range(len(s.degs))]
            if not GR.det(J).iszero(): best = choice; break
        assert best is not None, 'no independent choice of power sums'
        s.choice = best
        s.omega_used = [None] + [(orbs[ch][0], orbs[ch][1]) for ch in best]

    def lin(s, hat, c): return [sum((h[j]*c[j] for j in range(s.r)), K(0)) for h in hat]
    def u(s, c):
        out = [sum((c[i]*c[j]*s.Gw[i][j] for i in range(s.r) for j in range(s.r)), K(0))]
        for i, d in enumerate(s.degs[1:]):
            hat = s.orbs[s.choice[i]][2]; out.append(sum((kpow(L, d) for L in s.lin(hat, c)), K(0)))
        return out
    def grad(s, i, c):
        if i == 0: return [K(2)*sum((s.Gw[a][j]*c[a] for a in range(s.r)), K(0)) for j in range(s.r)]
        d = s.degs[i]; hat = s.orbs[s.choice[i - 1]][2]; Ls = s.lin(hat, c)
        pw = [kpow(L, d - 1) for L in Ls]
        return [K(d)*sum((p*h[j] for p, h in zip(pw, hat)), K(0)) for j in range(s.r)]
    def lap(s, i, c):
        if i == 0: return K(2*s.r)
        d = s.degs[i]; hat = s.orbs[s.choice[i - 1]][2]; Ls = s.lin(hat, c)
        nrm = [sum((h[a]*h[b]*s.G[a][b] for a in range(s.r) for b in range(s.r)), K(0)) for h in hat]
        return K(d*(d - 1))*sum((kpow(L, d - 2)*q for L, q in zip(Ls, nrm)), K(0))
    def metric(s, gi, gj):
        return sum((s.G[a][b]*gi[a]*gj[b] for a in range(s.r) for b in range(s.r)), K(0))

def build(name, kmax):
    t0 = time.time(); S = Setup(name); n = len(S.degs)
    print(f'{name}: basic degrees {S.degs}; power-sum orbits (weight index, size) {S.omega_used[1:]}', flush=True)
    targets = []   # (label, weighted degree)
    for i in range(n):
        for j in range(i, n): targets.append((('g', i, j), S.degs[i] + S.degs[j] - 2))
        targets.append((('L', i), S.degs[i] - 2))
    maxN = max(len(wmonos(S.degs, m)) for _, m in targets)
    rnd = random.Random(7); pts = []
    for _ in range(maxN + 6):
        pts.append([K(fmpq(rnd.randint(-9, 9), rnd.randint(1, 7))) for _ in range(S.r)])
    vals = []
    for c in pts:
        u = S.u(c); gr = [S.grad(i, c) for i in range(n)]
        tv = {}
        for (lab, m) in targets:
            if lab[0] == 'g': tv[lab] = S.metric(gr[lab[1]], gr[lab[2]])
            else: tv[lab] = S.lap(lab[1], c)
        vals.append((u, tv))
    gmet = {}; Lap = {}
    for lab, m in targets:
        mons = wmonos(S.degs, m)
        if not mons: 
            assert all(v[1][lab].iszero() for v in vals); P = {}
        else:
            A = [[peval({e: K(1)}, u) for e in mons] for (u, tv) in vals[:len(mons) + 6]]
            B = [[tv[lab] for (u, tv) in vals[:len(mons) + 6]]]
            sol = solve_exact(A, B)[0]; P = {e: c for e, c in zip(mons, sol) if not c.iszero()}
        if lab[0] == 'g': gmet[(lab[1], lab[2])] = P; gmet[(lab[2], lab[1])] = P
        else: Lap[lab[1]] = P
    print(f'{name}: metric and Laplacians fitted ({time.time()-t0:.1f} s)', flush=True)
    def lap_u(P):
        out = {}
        for i in range(n):
            di = pder(P, i)
            if di: out = padd(out, pmul(di, Lap[i]))
            for j in range(n):
                dij = pder(di, j)
                if dij: out = padd(out, pmul(dij, gmet[(i, j)]))
        return out
    # check: Laplacian of u_1^k = 2k(2k + r - 2) u_1^(k-1)  (|x|^(2k))
    P = {tuple([3] + [0]*(n - 1)): K(1)}; Q = lap_u(P)
    assert Q == {tuple([2] + [0]*(n - 1)): K(6*(6 + S.r - 2))}, Q
    harm = {}
    for k in range(1, kmax + 1):
        mons = wmonos(S.degs, k); lower = wmonos(S.degs, k - 2)
        if not mons: harm[k] = []; continue
        imgs = [lap_u({e: K(1)}) for e in mons]
        rows = [[img.get(f, K(0)) for img in imgs] for f in lower]
        for img in imgs: assert all(f in lower for f in img), 'Laplacian left the degree'
        ns = nullspace(rows, len(mons)) if rows else [[K(1) if i == j else K(0) for i in range(len(mons))] for j in range(len(mons))]
        assert len(ns) == len(mons) - len(lower), (k, len(ns), len(mons), len(lower))
        # normalise: make the coefficient of the highest monomial (last pivot-free) 1
        basis = []
        for v in ns:
            lead = next(c for c in reversed(v) if not c.iszero()); iv = lead.inv()
            basis.append({e: c*iv for e, c in zip(mons, v) if not c.iszero()})
        for h in basis: assert lap_u(h) == {}, 'not harmonic'
        harm[k] = basis
    dims = {k: len(v) for k, v in harm.items()}
    print(f'{name}: harmonic invariant dimensions ' + ' '.join(f'{k}:{d}' for k, d in dims.items() if d), flush=True)
    def ks(c): return [str(c.a), str(c.b)]
    out = {'group': name, 'D': S.D, 'r': S.r, 'degs': S.degs, 'omega': S.omega_used[1:],
           'omega_hat': {str(ch): [[ks(x) for x in h] for h in S.orbs[ch][2]] for ch in set(S.choice)},
           'choice': list(S.choice), 'dims': dims,
           'harm': {k: [[[list(e), ks(c)] for e, c in h.items()] for h in v] for k, v in harm.items()},
           'metric': {f'{i},{j}': [[list(e), ks(c)] for e, c in P.items()] for (i, j), P in gmet.items()},
           'lap': {str(i): [[list(e), ks(c)] for e, c in P.items()] for i, P in Lap.items()},
           'G': [[ks(x) for x in row] for row in S.G], 'Gw': [[ks(x) for x in row] for row in S.Gw],
           'W': [[ks(x) for x in w] for w in S.gd['W']], 'R': [[ks(x) for x in a] for a in S.gd['R']], 'order': S.gd['order'],
           'aut': S.gd['aut'], 'seconds': round(time.time() - t0, 1)}
    fn = os.path.join(HERE, '..', 'data', f'hinv-{name}.json'); json.dump(out, open(fn, 'w'))
    print(f'{name}: written {fn} ({out["seconds"]} s)', flush=True)
    return out

if __name__ == '__main__':
    build(sys.argv[1], int(sys.argv[2]))
