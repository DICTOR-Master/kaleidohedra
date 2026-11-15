#!/usr/bin/env python3
"""Exact surfaces of golden rhombi on the six 5-fold axes of the icosahedron (library for k10_search.py and gnomon.py).

A surface is a dict {(p, a, b): s}: the rhombus p + [0,1]e_a + [0,1]e_b (p in Z^n, a < b) with outward normal s (e_a x e_b), s = +-1.
Everything is exact: numbers a + b*phi in Z[phi] are integer pairs (x, y); signs are decided by integer tests. The model and the tests
follow the earlier pilot (studies/2026-11-15-backyard-open-problems/scripts/zone_pilot.py); new here: surface flips at 3-valent
corners with an exact embedding test, the face-pair vectors lambda_ab, and the exact lattice test."""
import itertools
from fractions import Fraction

# ---------- Z[phi] ----------
def zadd(u, v): return (u[0] + v[0], u[1] + v[1])
def zsub(u, v): return (u[0] - v[0], u[1] - v[1])
def zmul(u, v): return (u[0]*v[0] + u[1]*v[1], u[0]*v[1] + u[1]*v[0] + u[1]*v[1])
def zneg(u): return (-u[0], -u[1])
def zsign(u):
    """exact sign of x + y*phi = (2x + y + y*sqrt5)/2"""
    x, y = u; a, b = 2*x + y, y
    if a >= 0 and b >= 0: return 0 if a == 0 and b == 0 else 1
    if a <= 0 and b <= 0: return -1
    return (1 if a > 0 else -1) if a*a > 5*b*b else (1 if b > 0 else -1)
def zfloat(u): return u[0] + u[1]*(1 + 5**0.5)/2
def zconj(u):
    """Galois twin (Double Vision): phi -> 1 - phi = -1/phi, so x + y phi -> (x + y) - y phi"""
    return (u[0] + u[1], -u[1])

O, I, P, M = (0, 0), (1, 0), (0, 1), (0, -1)
AX6 = [(I, P, O), ((-1, 0), P, O), (O, I, P), (O, (-1, 0), P), (P, O, I), (M, O, I)]   # (1,phi,0),(-1,phi,0),(0,1,phi),(0,-1,phi),(phi,0,1),(-phi,0,1)

def det3(u, v, w):
    t1 = zmul(u[0], zsub(zmul(v[1], w[2]), zmul(v[2], w[1])))
    t2 = zmul(u[1], zsub(zmul(v[0], w[2]), zmul(v[2], w[0])))
    t3 = zmul(u[2], zsub(zmul(v[0], w[1]), zmul(v[1], w[0])))
    return zadd(zsub(t1, t2), t3)

class Geo:
    def __init__(self, n, twin=False):
        self.n = n
        ax = AX6[:n]
        if twin: ax = [tuple(zconj(c) for c in e) for e in ax]
        self.E = ax
        self.D = {(i, j, k): det3(ax[i], ax[j], ax[k]) for i in range(n) for j in range(n) for k in range(n)}
        self.pairs = list(itertools.combinations(range(n), 2))
        self.k = 2*(n - 1)
    # projections on the normal n_xy = e_x cross e_y: e_c . n_xy = det(e_x, e_y, e_c)
    def proj(self, p, xy):
        x, y = xy; acc = O
        for i, c in enumerate(p):
            if c: acc = zadd(acc, zmul((c, 0), self.D[(x, y, i)]))
        return acc
    def interval(self, p, dirs, xy):
        """projection interval of p + sum [0,1] e_d (d in dirs) on n_xy"""
        b = self.proj(p, xy); lo, hi = b, b
        for d in dirs:
            v = self.D[(xy[0], xy[1], d)]
            if zsign(v) > 0: hi = zadd(hi, v)
            else: lo = zadd(lo, v)
        return lo, hi
    def relation(self, p1, d1, p2, d2):
        """'apart' (strictly separated), 'touch' (closed sets meet, interiors of the 3D one do not), 'cross' (meet in the interior)"""
        weak = False
        for xy in self.pairs:
            a0, a1 = self.interval(p1, d1, xy); b0, b1 = self.interval(p2, d2, xy)
            g1, g2 = zsign(zsub(b0, a1)), zsign(zsub(a0, b1))
            if g1 > 0 or g2 > 0: return 'apart'
            if g1 == 0 or g2 == 0: weak = True
        return 'touch' if weak else 'cross'

def unit(n, a): v = [0]*n; v[a] = 1; return tuple(v)
def vadd(p, q): return tuple(x + y for x, y in zip(p, q))
def vsub(p, q): return tuple(x - y for x, y in zip(p, q))

def corners(f, n):
    p, a, b = f; ea, eb = unit(n, a), unit(n, b)
    return (p, vadd(p, ea), vadd(p, eb), vadd(vadd(p, ea), eb))
def edges_of(f, n):
    p, a, b = f; ea, eb = unit(n, a), unit(n, b)
    return ((p, a), (p, b), (vadd(p, eb), a), (vadd(p, ea), b))

def zonotope(G):
    """surface of the zonotope sum [0,1] e_i: for each pair two faces"""
    S = {}
    for a, b in G.pairs:
        plus = [0]*G.n; minus = [0]*G.n
        for c in range(G.n):
            if c in (a, b): continue
            sg = zsign(G.D[(a, b, c)])
            if sg > 0: plus[c] = 1
            else: minus[c] = 1
        S[(tuple(plus), a, b)] = 1; S[(tuple(minus), a, b)] = -1
    return S

def from_cells(G, cells):
    """surface of a union of non-overlapping cells (p, (i,j,k)) (the pilot's representation)"""
    cnt = {}
    for p, t in cells:
        p = tuple(p); i, j, k = t
        for (a, b), o in (((i, j), k), ((i, k), j), ((j, k), i)):
            so = zsign(G.D[(a, b, o)])
            cnt.setdefault((p, a, b), []).append(-so)                  # low side in o: outward is -e_o
            cnt.setdefault((vadd(p, unit(G.n, o)), a, b), []).append(so)
    return {f: v[0] for f, v in cnt.items() if len(v) == 1}

def canon_t(S):
    m = tuple(min(f[0][i] for f in S) for i in range(len(next(iter(S))[0])))
    return frozenset(((vsub(f[0], m), f[1], f[2]), s) for f, s in S.items())

def analyse(G, S):
    """combinatorial checks: closed 2-manifold sphere, zones. Returns dict or None (with reason)."""
    n = G.n; F = len(S); E = {}; V = {}
    for f in S:
        for e in edges_of(f, n): E.setdefault(e, []).append(f)
        for v in corners(f, n): V.setdefault(v, []).append(f)
    if any(len(x) != 2 for x in E.values()): return None, 'edge not in exactly 2 faces'
    # vertex links: faces at v linked through edges at v must form one cycle
    for v, fs in V.items():
        adj = {f: [] for f in fs}
        for f in fs:
            for e in edges_of(f, n):
                q, d = e
                if q == v or vadd(q, unit(n, d)) == v:
                    for g in E[e]:
                        if g != f: adj[f].append(g)
        if any(len(x) != 2 for x in adj.values()): return None, 'vertex link not a cycle'
        seen = {fs[0]}; st = [fs[0]]
        while st:
            f = st.pop()
            for g in adj[f]:
                if g not in seen: seen.add(g); st.append(g)
        if len(seen) != len(fs): return None, 'pinched vertex'
    chi = len(V) - len(E) + F
    # connectivity
    f0 = next(iter(S)); seen = {f0}; st = [f0]
    while st:
        f = st.pop()
        for e in edges_of(f, n):
            for g in E[e]:
                if g not in seen: seen.add(g); st.append(g)
    if len(seen) != F: return None, 'not connected'
    if chi != 2: return None, f'chi {chi}'
    zones = []
    for d in range(n):
        fs = [f for f in S if d in (f[1], f[2])]; seen = set()
        for f0 in fs:
            if f0 in seen: continue
            comp = [f0]; seen.add(f0); st = [f0]
            while st:
                f = st.pop(); p, a, b = f; o = b if a == d else a
                for q in (p, vadd(p, unit(n, o))):
                    for g in E.get((q, d), []):
                        if g not in seen: seen.add(g); comp.append(g); st.append(g)
            zones.append((d, len(comp)))
    coplanar_adjacent = 0
    for e, (f, g) in E.items():
        if (f[1], f[2]) == (g[1], g[2]): coplanar_adjacent += 1
    perpair = {}
    for f in S: perpair.setdefault((f[1], f[2]), []).append(f)
    return {'F': F, 'V': len(V), 'E': len(E), 'chi': chi, 'zones': zones, 'coplanar_adjacent': coplanar_adjacent,
            'perpair': perpair, 'Vmap': V}, 'ok'

def in_class(G, info):
    """class C(n): one zone per direction, every zone k faces, every pair of directions exactly 2 faces"""
    z = info['zones']
    return len(z) == G.n and all(c == G.k for _, c in z) and sorted(d for d, _ in z) == list(range(G.n)) and \
        all(len(info['perpair'].get(pr, [])) == 2 for pr in G.pairs)

def face_pair_vectors(G, S, info):
    """lambda_ab = p(+face) - p(-face); None if some pair has two faces with the same outward side (then no tiling by translates)"""
    lam = {}
    for pr in G.pairs:
        f, g = info['perpair'][pr]
        if S[f] == S[g]: return None
        if S[f] < 0: f, g = g, f
        lam[pr] = vsub(f[0], g[0])
    return lam

def int_rank_basis(rows):
    """exact integer row reduction (Euclid on each column): a Z-basis of the lattice spanned by the rows"""
    A = [list(r) for r in rows if any(r)]; basis = []; ncol = len(rows[0]) if rows else 0
    for col in range(ncol):
        while True:
            nz = [r for r in A if r[col] != 0]
            if len(nz) <= 1: break
            nz.sort(key=lambda r: abs(r[col])); piv = nz[0]
            for r in nz[1:]:
                q = r[col]//piv[col]
                for j in range(ncol): r[j] -= q*piv[j]
        nz = [r for r in A if r[col] != 0]
        if nz: basis.append(nz[0]); A = [r for r in A if r is not nz[0] and any(r)]
        else: A = [r for r in A if any(r)]
    return basis

def rank_Q(rows):
    A = [[Fraction(x) for x in r] for r in rows]; rk = 0; ncol = len(A[0]) if A else 0
    for c in range(ncol):
        piv = next((i for i in range(rk, len(A)) if A[i][c] != 0), None)
        if piv is None: continue
        A[rk], A[piv] = A[piv], A[rk]
        for i in range(len(A)):
            if i != rk and A[i][c] != 0:
                f = A[i][c]/A[rk][c]; A[i] = [x - f*y for x, y in zip(A[i], A[rk])]
        rk += 1
    return rk

def volume3(G, S):
    """3 * volume, exact in Z[phi] (divergence theorem; det(e_a, e_a, e_b) = 0 so only the corner p counts)"""
    acc = O
    for (p, a, b), s in S.items():
        t = O
        for i, c in enumerate(p):
            if c: t = zadd(t, zmul((c, 0), G.D[(i, a, b)]))
        acc = zadd(acc, t if s > 0 else zneg(t))
    return acc

def lattice_det(G, B):
    """det of the 3 x 3 real matrix of the lattice basis B (3 rows in Z^n): Cauchy-Binet sum_{ijk} minor_ijk(B) det(e_i,e_j,e_k)"""
    acc = O
    for t in itertools.combinations(range(G.n), 3):
        m = [[B[r][c] for c in t] for r in range(3)]
        mi = (m[0][0]*(m[1][1]*m[2][2] - m[1][2]*m[2][1]) - m[0][1]*(m[1][0]*m[2][2] - m[1][2]*m[2][0])
              + m[0][2]*(m[1][0]*m[2][1] - m[1][1]*m[2][0]))
        if mi: acc = zadd(acc, zmul((mi, 0), G.D[t]))
    return acc

def corner_moves(G, S, info):
    """flips at 3-valent corners whose faces are (a,b), (a,c), (b,c): indent (remove the corner cell) or bulge (add it).
    Yields (kind, newS, cell) after the exact embedding test: no other face meets the open cell, and any face that touches the closed
    cell must share a lattice vertex with it (conservative)."""
    n = G.n
    for v, fs in info['Vmap'].items():
        if len(fs) != 3: continue
        prs = [(f[1], f[2]) for f in fs]; axes = sorted(set(x for pr in prs for x in pr))
        if len(axes) != 3 or len(set(prs)) != 3: continue
        sig = {}
        okk = True
        for f in fs:
            p, a, b = f
            for d, other in ((a, b), (b, a)):
                s_d = 1 if v[d] == p[d] else -1
                if sig.setdefault(d, s_d) != s_d: okk = False
        if not okk: continue
        a, b, c = axes
        q = tuple(v[i] - (1 if (i in sig and sig[i] < 0) else 0) for i in range(n))
        # orientation: is each face's outward normal pointing away from the cell?
        away = []
        for f in fs:
            p, x, y = f; z = [t for t in axes if t not in (x, y)][0]
            into = sig[z]                                # direction from the face into the cell along e_z
            away.append(S[f]*into*zsign(G.D[(x, y, z)]) < 0)
        if all(away): kind = 'indent'
        elif not any(away): kind = 'bulge'
        else: continue
        cellfaces = {}
        for x, y, z in ((a, b, c), (a, c, b), (b, c, a)):
            so = zsign(G.D[(x, y, z)])
            cellfaces[(q, x, y)] = -so; cellfaces[(vadd(q, unit(n, z)), x, y)] = so    # outward from the cell
        if sum(1 for f in fs if f in cellfaces) != 3: continue
        cverts = set()
        for f in cellfaces: cverts.update(corners(f, n))
        bad = False
        for f in S:
            if f in fs: continue
            r = G.relation(f[0], (f[1], f[2]), q, (a, b, c))
            if r == 'cross': bad = True; break
            if r == 'touch' and not (set(corners(f, n)) & cverts): bad = True; break
        if bad: continue
        T = dict(S)
        for f in fs: del T[f]
        for f, so in cellfaces.items():
            if f in fs: continue
            s_new = -so if kind == 'indent' else so
            if f in T:
                if T[f] == -s_new: del T[f]; continue
                bad = True; break
            T[f] = s_new
        if bad: continue
        yield kind, T, (q, (a, b, c))

def coplanar_overlap(G, S, info):
    """two same-pair faces in one plane with overlapping interiors (exact sign tests on the in-plane coordinates)"""
    for pr, fs in info['perpair'].items():
        for f, g in itertools.combinations(fs, 2):
            d = vsub(g[0], f[0])
            if zsign(G.proj(d, pr)) != 0: continue
            # in-plane coordinates u, v of d in the basis e_a, e_b: use normals n_{b,z}, n_{a,z} for some z with nonzero denominators
            a, b = pr; u = v = None
            for z in range(G.n):
                if z in pr: continue
                den_u = G.D[(b, z, a)]; den_v = G.D[(a, z, b)]
                if zsign(den_u) and zsign(den_v):
                    nu = G.proj(d, (b, z)); nv = G.proj(d, (a, z))
                    u = (nu, den_u); v = (nv, den_v); break
            if u is None: continue
            def lt1(frac):   # |num/den| < 1 exactly
                num, den = frac; sd = zsign(den)
                num = num if sd > 0 else zneg(num); den = den if sd > 0 else zneg(den)
                return zsign(zsub(den, num)) > 0 and zsign(zadd(den, num)) > 0
            if lt1(u) and lt1(v): return True
    return False

# ---------- the icosahedral group as signed permutations of the axes ----------
def signed_perms(G):
    n = G.n; out = []
    for perm in itertools.permutations(range(n)):
        for sg in itertools.product((1, -1), repeat=n):
            ok = True; dets = None
            for t in itertools.combinations(range(n), 3):
                i, j, k = t; s = sg[i]*sg[j]*sg[k]
                img = G.D[(perm[i], perm[j], perm[k])]
                r = zmul((s, 0), img)
                if r == G.D[t]: c = 1
                elif r == zneg(G.D[t]): c = -1
                else: ok = False; break
                if dets is None: dets = c
                elif dets != c: ok = False; break
            if ok: out.append((perm, sg, dets))
    return out

def apply_sym(G, S, sym):
    perm, sg, dt = sym; n = G.n; T = {}
    for (p, a, b), s in S.items():
        q = [0]*n
        for i, c in enumerate(p): q[perm[i]] += sg[i]*c
        a2, b2 = perm[a], perm[b]
        if sg[a] < 0: q[a2] -= 1
        if sg[b] < 0: q[b2] -= 1
        s2 = s*dt*sg[a]*sg[b]*(1 if a2 < b2 else -1)
        if a2 > b2: a2, b2 = b2, a2
        T[(tuple(q), a2, b2)] = s2
    return T

def canon(G, S, syms):
    best = None
    for sym in syms:
        c = tuple(sorted(canon_t(apply_sym(G, S, sym))))
        if best is None or c < best: best = c
    return best

def is_single_cell(G, S):
    if len(S) != 6: return None
    prs = sorted(set((f[1], f[2]) for f in S))
    axes = sorted(set(x for pr in prs for x in pr))
    if len(axes) != 3 or len(prs) != 3: return None
    q = tuple(min(f[0][i] for f in S) for i in range(G.n))
    return (q, tuple(axes))

def shell_decompose(G, S, maxnodes=20000):
    """exact cell decomposition by peeling corner cells (each peel passes the exact embedding test, so the cell lies inside);
    depth-first with backtracking; every intermediate surface must stay a closed 2-manifold sphere. Returns a list of cells or None."""
    nodes = [0]; failed = set()       # memo of sub-solids already known not to peel (turns the search into one visit per sub-solid)
    def rec(S):
        nodes[0] += 1
        if nodes[0] > maxnodes: return None
        c = is_single_cell(G, S)
        if c: return [c]
        key = frozenset(S.items())
        if key in failed: return None
        info, why = analyse(G, S)
        if info is None: failed.add(key); return None
        for kind, T, cell in corner_moves(G, S, info):
            if kind != 'indent': continue
            r = rec(T)
            if r is not None: return [cell] + r
        failed.add(key)
        return None
    return rec(S)
