"""Twisted silence (mechanism of the parallel golden-A4 study, Fable 15 Nov 2026, credited there): a twisted class of a finite group
G of unit quaternions is O = {a x0 alpha(a)^-1 : a in G}, x0 in G, alpha an automorphism of G; a union of alpha-twisted classes kills
degree k iff the twisted-character sums vanish on every alpha-stable constituent of V_k = Sym^k(C^2) restricted to G.
Here: enumerate every union of alpha-twisted classes, for every subgroup G of the base group (2I, or 2O for the 24-cell) and every
automorphism alpha, that lies in the universe; match them (up to the universe's symmetry group) with the census sets; and for each
zero compute (numerically) dim Hom_G(V_k o alpha, V_k) and verify the intertwining identity rho(g) S = S rho(alpha(g)), S = sum rho_k(x)."""
import numpy as np, itertools
from math import comb

def qmul(a, b):
    a0, a1, a2, a3 = a; b0, b1, b2, b3 = b
    return np.array([a0*b0-a1*b1-a2*b2-a3*b3, a0*b1+a1*b0+a2*b3-a3*b2, a0*b2-a1*b3+a2*b0+a3*b1, a0*b3+a1*b2-a2*b1+a3*b0])
def qinv(a): return np.array([a[0], -a[1], -a[2], -a[3]])

class QGroup:
    """a finite group of unit quaternions given as a float array; elements indexed, multiplication table"""
    def __init__(self, E):
        self.E = np.array(E); n = len(E)
        self.key = {tuple(np.round(e, 7)): i for i, e in enumerate(self.E)}
        assert len(self.key) == n
        self.mul = np.array([[self.key[tuple(np.round(qmul(self.E[i], self.E[j]), 7))] for j in range(n)] for i in range(n)])
        self.e = self.key[(1.0, 0.0, 0.0, 0.0)]
        self.inv = np.argmax(self.mul == self.e, axis=1)
        self.n = n
    def closure(self, gens):
        S = {self.e}; fr = [self.e]
        while fr:
            nf = []
            for x in fr:
                for g in gens:
                    y = int(self.mul[x, g])
                    if y not in S: S.add(y); nf.append(y)
            fr = nf
        return sorted(S)
    def order(self, x):
        k, y = 1, x
        while y != self.e: y = int(self.mul[y, x]); k += 1
        return k

def subgroups(Q):
    """all subgroups of Q (index lists), from all pairs of generators (every finite subgroup of SU(2) is 2-generated)"""
    seen = {}
    for a in range(Q.n):
        for b in range(a, Q.n):
            S = tuple(Q.closure([a, b]))
            if S not in seen: seen[S] = (a, b)
    return [(list(S), g) for S, g in seen.items()]

def automorphisms(Q, S, gens):
    """all automorphisms of the subgroup S (as dicts on Q-indices), by images of the two generators"""
    Sset = set(S); g1, g2 = gens; o1, o2 = Q.order(g1), Q.order(g2)
    out = []
    for h1 in S:
        if Q.order(h1) != o1: continue
        for h2 in S:
            if Q.order(h2) != o2: continue
            m = {Q.e: Q.e}; fr = [Q.e]; ok = True
            while fr and ok:
                nf = []
                for x in fr:
                    for g, h in ((g1, h1), (g2, h2)):
                        y = int(Q.mul[x, g]); z = int(Q.mul[m[x], h])
                        if y in m:
                            if m[y] != z: ok = False; break
                        else:
                            m[y] = z; nf.append(y)
                    if not ok: break
                fr = nf
            # consistency on every Cayley-graph edge x -> x g already makes m a homomorphism (induction on words)
            if ok and len(m) == len(S) and len(set(m.values())) == len(S):
                out.append(m)
    return out

def twisted_classes(Q, S, alpha):
    cls = []; seen = set()
    for x0 in S:
        if x0 in seen: continue
        O = sorted({int(Q.mul[Q.mul[a, x0], Q.inv[alpha[a]]]) for a in S})
        seen |= set(O); cls.append(O)
    return cls

def su2(q):
    w, x, y, z = q
    return np.array([[w + 1j * x, y + 1j * z], [-y + 1j * z, w - 1j * x]])

_SYMK = {}
def symk_q(q, k):
    key = (tuple(np.round(q, 9)), k)
    if key not in _SYMK: _SYMK[key] = symk(su2(q), k)
    return _SYMK[key]

def symk(M, k):
    """matrix of Sym^k(M) on the monomial basis u^(k-j) v^j"""
    a, b = M[0]; c, d = M[1]
    R = np.zeros((k + 1, k + 1), complex)
    # image of u^(k-j) v^j where u -> a u + c v, v -> b u + d v
    for j in range(k + 1):
        p = np.zeros(k + 1, complex); p[0] = 1
        for _ in range(k - j): p = _mulpoly(p, a, c, k)
        for _ in range(j): p = _mulpoly(p, b, d, k)
        R[:, j] = p
    return R
def _mulpoly(p, s, t, k):
    q = np.zeros(k + 1, complex)
    q[:k + 1] += s * p          # times s*u (keeps v-degree)
    q[1:] += t * p[:-1]         # times t*v (raises v-degree)
    return q

def hom_dim(Q, S, gens, alpha, k):
    """dim Hom_G(V_k o alpha, V_k) = dim {M : rho(g) M = M rho(alpha(g))} (numeric nullspace)"""
    n = k + 1; rows = []
    for g in gens:
        A = symk_q(Q.E[g], k); B = symk_q(Q.E[alpha[g]], k)
        rows.append(np.kron(A, np.eye(n)) - np.kron(np.eye(n), B.T))   # (A M - M B) vec, row-major
    Mtx = np.vstack(rows); sv = np.linalg.svd(Mtx, compute_uv=False)
    return int((sv < 1e-8).sum()) + max(0, n * n - len(sv))

def intertwines(Q, Sel, gens, alpha, k):
    """for a union Sel of alpha-twisted classes: rho(g) S = S rho(alpha(g)) and ||S||^2 (proportional to T_k)"""
    Ssum = sum(symk_q(Q.E[x], k) for x in Sel)
    err = max(np.abs(symk_q(Q.E[g], k) @ Ssum - Ssum @ symk_q(Q.E[alpha[g]], k)).max() for g in gens)
    return err, float(np.abs(Ssum).max())

def build_twisted(universe_pts, base_pts, canon_fn, translate=None, max_union=3, right_translates=False, log=print):
    """Every union of alpha-twisted classes of every subgroup G of the base group (alpha over automorphisms modulo inner ones: an inner
    change of alpha right-translates the classes by an element of G, which is a symmetry of the 600-cell; with right_translates=True
    those translates are added explicitly, for universes whose symmetry group does not contain them). Returns canonical key -> records."""
    Q = QGroup(base_pts)
    ukey = {tuple(np.round(p, 7)): i for i, p in enumerate(universe_pts)}
    subs = subgroups(Q); log(f'twisted: base group order {Q.n}, {len(subs)} subgroups')
    cand = {}
    for S, gens in subs:
        auts = automorphisms(Q, S, gens)
        inner_keys = set(); reps = []
        for al in auts:
            kk = tuple(sorted(al.items()))
            if kk in inner_keys: continue
            reps.append(al)
            for c in S:   # mark the whole inner class of al
                inner_keys.add(tuple(sorted((x, int(Q.mul[Q.mul[c, al[x]], Q.inv[c]])) for x in S)))
        for al in reps:
            inner = all(al[x] == x for x in S) or any(all(al[x] == int(Q.mul[Q.mul[c, x], Q.inv[c]]) for x in S) for c in S)
            cls = twisted_classes(Q, S, al)
            nc = len(cls)
            rng = range(1, min(nc, max_union) + 1) if nc > 9 else range(1, nc + 1)
            trs = S if right_translates else [Q.e]
            for r in rng:
                for comb_ in itertools.combinations(range(nc), r):
                    sel0 = [x for i in comb_ for x in cls[i]]
                    for c in trs:
                        sel = sorted(int(Q.mul[x, c]) for x in sel0)
                        pts = Q.E[sel]
                        if translate is not None: pts = translate(pts)
                        if pts is None: continue
                        idx = [ukey.get(tuple(np.round(p, 7))) for p in pts]
                        if any(i is None for i in idx): continue
                        fs = frozenset(idx)
                        lst = cand.setdefault(fs, [])
                        if len(lst) < 3:
                            alc = al
                            if c != Q.e:   # the translated union is a union of twisted classes for inn(c^-1) o alpha
                                alc = {x: int(Q.mul[Q.mul[Q.inv[c], al[x]], c]) for x in S}
                            lst.append({'G_order': len(S), 'alpha_inner': inner, 'n_classes_used': r,
                                        'class_sizes': sorted(len(cls[i]) for i in comb_), 'Q': Q, 'S': S, 'gens': list(gens), 'alpha': alc, 'sel': sel})
    out = {}
    for fs, lst in cand.items():
        key = canon_fn(np.array(sorted(fs)))
        o = out.setdefault(key, [])
        for t in lst:
            if len(o) < 3: o.append(dict(t, idx=sorted(fs)))
    log(f'twisted: {len(cand)} candidate sets, {len(out)} distinct twisted-class unions in the universe (up to its symmetry group)')
    return out
