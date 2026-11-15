#!/usr/bin/env python3
"""Systematic exact search for the golden-A4 mechanism in other polytopes.
For P in {600-cell, 24-cell, 120-cell, E8 roots} and K in a list of reflection subgroups of Aut(P) (found as root subsystems, first
realisation of each type) and their rotation subgroups K+, collect every distinct K-orbit O in P. For each O:
  * tones T_k(O), k <= KMAX, exact in Q(sqrt5) (Gegenbauer C_k^{(d-2)/2} of the cosines);
  * S = Stab(O) in Aut(P) (enumerated: H4 14400, W(F4) 1152; for E8 only the listed K, see note), h_k(S) = dim of S-invariant harmonics
    of degree k (Molien over S); a zero with h_k(S) > 0 is GENUINE (not forced by the symmetry of O itself, the census's (X));
  * block contents F_j(O) = sum_{x,y in O} b_j(<x,y>) for the blocks of P (600-cell: the 9 characters of 2I; 24-cell: the 5 real
    characters of 2T; E8: harmonic degrees 0..4, its 5 eigenspaces); identity T_k = sum_j m_kj F_j checked exactly; a vanishing block is
    NONTRIVIAL if some other S-orbit (K-orbit for E8) has F_j != 0, and its rank r_j = number of independent invariant functions in it.
Orbits with >= 2 genuine zeros are listed with the vanishing nontrivial blocks that explain them.
usage: systematic.py WHICH KMAX   (WHICH = 600, 24, 120, E8, all)"""
import sys, itertools, numpy as np
from fractions import Fraction as Fr
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from q5 import Q5, PHI, dot, gegenbauer
WHICH = sys.argv[1] if len(sys.argv) > 1 else 'all'
KMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 20
FAILS = []
def check(ok, what):
    print(('  ok   ' if ok else '  FAIL ') + what, flush=True)
    if not ok: FAILS.append(what)
R5 = Q5(0, 1); IPHI = PHI - 1; half = Fr(1, 2)
def even_perms(n): return [p for p in itertools.permutations(range(n)) if sum(p[i] > p[j] for i in range(n) for j in range(i+1, n)) % 2 == 0]
def signs(v):
    out = set()
    for s in itertools.product((1, -1), repeat=len(v)):
        out.add(tuple(Q5(x)*t if not isinstance(x, Q5) else x*t for x, t in zip(v, s)))
    return out
def allperms(v, ev=False):
    out = set(); idx = even_perms(len(v)) if ev else list(itertools.permutations(range(len(v))))
    for w in signs(v):
        for p in idx: out.add(tuple(w[p[i]] for i in range(len(v))))
    return out
def P600():
    S = allperms([Q5(1), Q5(0), Q5(0), Q5(0)]) | allperms([Q5(half)]*4) | allperms([PHI*half, Q5(half), IPHI*half, Q5(0)], ev=True)
    return sorted(S, key=lambda v: tuple((x.a, x.b) for x in v))
def P600odd():
    odd = lambda n: [p for p in itertools.permutations(range(n)) if p not in set(even_perms(n))]
    base = [PHI*half, Q5(half), IPHI*half, Q5(0)]; S = set()
    for w in signs(base):
        for p in odd(4): S.add(tuple(w[p[i]] for i in range(4)))
    S |= allperms([Q5(1), Q5(0), Q5(0), Q5(0)]) | allperms([Q5(half)]*4)
    return sorted(S, key=lambda v: tuple((x.a, x.b) for x in v))
def roots_for(pts, cands):
    st = set(pts)
    for R in cands:
        if all(reflect(x, r) in st for r in R[:40] for x in pts): return R
    raise RuntimeError('no root system preserves the point set')
def P24(): return sorted(allperms([Q5(1), Q5(1), Q5(0), Q5(0)]), key=lambda v: tuple((x.a, x.b) for x in v))
def F4roots(): return sorted(set(P24()) | allperms([Q5(1), Q5(0), Q5(0), Q5(0)]) | allperms([Q5(half)]*4), key=lambda v: tuple((x.a, x.b) for x in v))
def P120():
    p2 = PHI*PHI; ip2 = IPHI*IPHI; o = Q5(1); z = Q5(0)
    S = (allperms([z, z, Q5(2), Q5(2)]) | allperms([o, o, o, R5]) | allperms([ip2, PHI, PHI, PHI]) | allperms([IPHI, IPHI, IPHI, p2])
         | allperms([z, ip2, o, p2], ev=True) | allperms([z, IPHI, PHI, R5], ev=True) | allperms([IPHI, o, PHI, Q5(2)], ev=True))
    return sorted(S, key=lambda v: tuple((x.a, x.b) for x in v))
def E8():
    S = set()
    for i, j in itertools.combinations(range(8), 2):
        for a, b in itertools.product((1, -1), repeat=2):
            v = [Q5(0)]*8; v[i] = Q5(a); v[j] = Q5(b); S.add(tuple(v))
    for s in itertools.product((1, -1), repeat=8):
        if s.count(-1) % 2 == 0: S.add(tuple(Q5(Fr(t, 2)) for t in s))
    return sorted(S, key=lambda v: tuple((x.a, x.b) for x in v))
# Coxeter types
def comp(t):
    k, n = t[0], int(t[1:]) if t[1:].isdigit() else None
    if t == 'F4': return [[0, 3, 0, 0], [3, 0, 4, 0], [0, 4, 0, 3], [0, 0, 3, 0]], [2, 6, 8, 12]
    if t == 'H3': return [[0, 5, 0], [5, 0, 3], [0, 3, 0]], [2, 6, 10]
    if t == 'H4': return [[0, 5, 0, 0], [5, 0, 3, 0], [0, 3, 0, 3], [0, 0, 3, 0]], [2, 12, 20, 30]
    if t == 'I5': return [[0, 5], [5, 0]], [2, 5]
    M = [[0]*n for _ in range(n)]
    def b(i, j, m): M[i][j] = M[j][i] = m
    if k == 'A':
        for i in range(n-1): b(i, i+1, 3)
        return M, list(range(2, n+2))
    if k == 'B':
        for i in range(n-1): b(i, i+1, 3 if i < n-2 else 4)
        return M, [2*i for i in range(1, n+1)]
    if k == 'D':
        for i in range(n-2): b(i, i+1, 3)
        b(n-3, n-1, 3); return M, sorted([2*i for i in range(1, n)] + [n])
    if k == 'E':
        for i in range(n-2): b(i, i+1, 3)
        b(2, n-1, 3); return M, {6: [2, 5, 6, 8, 9, 12], 7: [2, 6, 8, 10, 12, 14, 18], 8: [2, 8, 12, 14, 18, 20, 24, 30]}[n]
    raise ValueError(t)
def cox(types):
    blocks = [comp(t) for t in types]; n = sum(len(b[0]) for b in blocks); M = [[2]*n for _ in range(n)]; off = 0; degs = []
    for B, d in blocks:
        for i in range(len(B)):
            for j in range(len(B)):
                if i != j: M[off+i][off+j] = B[i][j] if B[i][j] else 2
        off += len(B); degs += d
    return M, degs
COS2 = {3: Q5(Fr(1, 4)), 4: Q5(Fr(1, 2)), 5: PHI*PHI/4}
def find_simple(roots, types):
    M, degs = cox(types); n = len(M); R = roots; nr = [dot(r, r) for r in R]
    D = [[dot(R[i], R[j]) for j in range(len(R))] for i in range(len(R))]
    def ok(i, j, m):
        d = D[i][j]
        if m == 2: return d.iszero()
        return d.sign() < 0 and d*d == COS2[m]*nr[i]*nr[j]
    sol = []
    def bt(k):
        if k == n: return True
        for c in range(len(R)):
            if c in sol: continue
            if all(ok(sol[i], c, M[i][k]) for i in range(k)):
                sol.append(c)
                if bt(k+1): return True
                sol.pop()
        return False
    return ([R[i] for i in sol], degs) if bt(0) else (None, degs)
def reflect(x, r):
    c = dot(x, r)*2/dot(r, r); return tuple(a - c*b for a, b in zip(x, r))
def perm_of(f, pts, index): return np.array([index[f(x)] for x in pts], dtype=np.int32)
def closure_group(gens, maxn=20000):
    n = len(gens[0]); idt = np.arange(n, dtype=np.int32); seen = {idt.tobytes(): idt}; fr = [idt]
    while fr:
        nf = []
        for g in fr:
            for s in gens:
                h = s[g]; key = h.tobytes()
                if key not in seen:
                    seen[key] = h; nf.append(h)
                    if len(seen) > maxn: raise RuntimeError('group too large')
        fr = nf
    return np.array(list(seen.values()), dtype=np.int32)
def orbits_from_gens(gens, n):
    par = list(range(n))
    def f(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    for g in gens:
        for i in range(n):
            a, b = f(i), f(int(g[i]))
            if a != b: par[a] = b
    O = {}
    for i in range(n): O.setdefault(f(i), []).append(i)
    return [tuple(sorted(o)) for o in O.values()]
def molien_h(mats, kmax):
    """h_k = dim of invariant harmonics of degree k for the matrix group mats (float, exact after rounding)"""
    ev = np.linalg.eigvals(mats)                       # (|G|, d)
    p = [None] + [np.sum(ev**i, axis=1) for i in range(1, kmax+1)]
    c = [np.ones(len(mats), dtype=complex)]
    for k in range(1, kmax+1): c.append(sum(p[i]*c[k-i] for i in range(1, k+1)) / k)
    m = [float(np.mean(ck).real) for ck in c]
    mi = [round(x) for x in m]
    assert max(abs(a - b) for a, b in zip(m, mi)) < 1e-6
    return [mi[k] - (mi[k-2] if k >= 2 else 0) for k in range(kmax+1)]
def molien_degrees(degs, d, rot, kmax):
    """h_k for a reflection group with invariant degrees degs on R^d (fixed space gives degree-1 invariants); rot: rotation subgroup"""
    ser = [0]*(kmax+1); ser[0] = 1
    for e in degs + [1]*(d - len(degs)):
        for k in range(e, kmax+1): ser[k] += ser[k-e]
    if rot:
        N = sum(e - 1 for e in degs)
        ser = [ser[k] + (ser[k-N] if k >= N else 0) for k in range(kmax+1)]
    return [ser[k] - (ser[k-2] if k >= 2 else 0) for k in range(kmax+1)]
def rank_q5(rows):
    A = [list(r) for r in rows]; rk = 0; ncol = len(A[0]) if A else 0
    for c in range(ncol):
        piv = next((i for i in range(rk, len(A)) if not A[i][c].iszero()), None)
        if piv is None: continue
        A[rk], A[piv] = A[piv], A[rk]; inv = A[rk][c].inv()
        for i in range(len(A)):
            if i != rk and not A[i][c].iszero():
                f = A[i][c]*inv; A[i] = [a - f*b for a, b in zip(A[i], A[rk])]
        rk += 1
    return rk
def U(k, c): return gegenbauer(k, 1, c)[k]
def blocks_2I(V):   # V: cosine values (9)
    ch = {'1': lambda c: U(0, c), '2': lambda c: U(1, c), '3': lambda c: U(2, c), '4s': lambda c: U(3, c), '5': lambda c: U(4, c),
          '6': lambda c: U(5, c), "2'": lambda c: U(1, c.conj()), "3'": lambda c: U(2, c.conj()), '4': lambda c: U(6, c) - U(2, c.conj())}
    return {r: {c: f(c) for c in V} for r, f in ch.items()}
def blocks_2T(V):
    ch = {'1': lambda c: U(0, c), '2': lambda c: U(1, c), '3': lambda c: U(2, c), "2'+2''": lambda c: U(3, c), "1'+1''": lambda c: U(4, c) - U(2, c)}
    return {r: {c: f(c) for c in V} for r, f in ch.items()}
def blocks_E8(V): return {f'deg{j}': {c: gegenbauer(4, 3, c)[j] for c in V} for j in range(5)}
def solve_mult(V, B, d, kmax):
    """P_k = sum_j m_kj b_j on V, exact (square system)"""
    names = list(B); n = len(V)
    if len(names) != n: return None
    lam = Fr(d - 2, 2)
    Mx = [[B[r][c] for r in names] for c in V]
    out = {}
    for k in range(kmax+1):
        rhs = [gegenbauer(k, lam, c)[k] for c in V]
        A = [Mx[i] + [rhs[i]] for i in range(n)]
        for col in range(n):
            piv = next(i for i in range(col, n) if not A[i][col].iszero()); A[col], A[piv] = A[piv], A[col]
            inv = A[col][col].inv(); A[col] = [a*inv for a in A[col]]
            for i in range(n):
                if i != col and not A[i][col].iszero():
                    f = A[i][col]; A[i] = [a - f*b for a, b in zip(A[i], A[col])]
        out[k] = {names[j]: A[j][n] for j in range(n)}
    return out
SUBS = {
 'H4': [['A4'], ['D4'], ['A2', 'A2'], ['I5', 'I5'], ['A3', 'A1'], ['H3', 'A1'], ['A1']*4, ['A2', 'A1', 'A1'], ['I5', 'A2'], ['I5', 'A1', 'A1'],
        ['H3'], ['A3'], ['A2', 'A1'], ['I5', 'A1'], ['H4']],
 'F4': [['B4'], ['D4'], ['A2', 'A2'], ['B3', 'A1'], ['A3', 'A1'], ['A1']*4, ['B2', 'B2'], ['B3'], ['A3'], ['A2', 'A1'], ['F4']],
 'E8': [['A8'], ['D8'], ['E7', 'A1'], ['E6', 'A2'], ['A4', 'A4'], ['D4', 'D4'], ['A2']*4, ['A1']*8, ['D5', 'A3'], ['A7', 'A1'],
        ['D6', 'A1', 'A1'], ['A5', 'A2', 'A1'], ['A3', 'A3', 'A1', 'A1'], ['E7'], ['E6'], ['D4'], ['A4'], ['E8']]}
def run(name, pts, roots, gname, blockfn, enum):
    print(f'=== {name}: {len(pts)} points, Aut = W({gname}), {len(roots)} roots', flush=True)
    d = len(pts[0]); n = len(pts); index = {p: i for i, p in enumerate(pts)}
    n2 = dot(pts[0], pts[0]); check(all(dot(p, p) == n2 for p in pts), f'{name}: all points on one sphere')
    # cosine class matrix
    IP = [tuple((int(4*x.a), int(4*x.b)) for x in p) for p in pts]
    assert all(Q5(Fr(a, 4), Fr(b, 4)) == x for p, q in zip(pts, IP) for x, (a, b) in zip(p, q))
    keys = {}; CI = np.zeros((n, n), dtype=np.int16)
    for i in range(n):
        xi = IP[i]
        for j in range(n):
            xj = IP[j]; a = sum(p[0]*q[0] + 5*p[1]*q[1] for p, q in zip(xi, xj)); b = sum(p[0]*q[1] + p[1]*q[0] for p, q in zip(xi, xj))
            CI[i, j] = keys.setdefault((a, b), len(keys))
    V = [None]*len(keys)
    for (a, b), t in keys.items(): V[t] = Q5(Fr(a, 16), Fr(b, 16)) / n2
    print(f'  {len(V)} cosine values', flush=True)
    lam = Fr(d - 2, 2); GV = [gegenbauer(KMAX, lam, c) for c in V]
    B = blockfn(V) if blockfn else None
    mult = solve_mult(V, B, d, KMAX) if B else None
    if B:
        check(all(m.b == 0 and m.a >= 0 for k in mult for m in mult[k].values()), f'{name}: every degree is a nonnegative combination of the {len(B)} blocks')
    # Aut generators: reflections in all simple roots of the full group
    full, fdeg = find_simple(roots, [gname])
    check(full is not None, f'{name}: simple roots of {gname} found')
    fg = [perm_of(lambda x, r=r: reflect(x, r), pts, index) for r in full]
    G = closure_group(fg) if enum else None
    if enum: print(f'  |Aut| = {len(G)}', flush=True)
    # basis for matrices
    Xf = np.array([[float(c) for c in p] for p in pts]); bidx = []
    for i in range(n):
        if np.linalg.matrix_rank(Xf[bidx + [i]]) == len(bidx) + 1: bidx.append(i)
        if len(bidx) == d: break
    XBinv = np.linalg.inv(Xf[bidx])
    XBTinv = np.linalg.inv(Xf[bidx].T)
    def mats(elems): return Xf[elems[:, bidx]].transpose(0, 2, 1) @ XBTinv
    ORB = {}; GENS = {}
    for types in SUBS[gname]:
        simple, degs = find_simple(roots, types)
        if simple is None: print(f'  {"+".join(types)}: not realised', flush=True); continue
        gens = [perm_of(lambda x, r=r: reflect(x, r), pts, index) for r in simple]
        rgens = [a[b] for a, b in itertools.combinations(gens, 2)] or [np.arange(n, dtype=np.int32)]
        for rot, gg in ((False, gens), (True, rgens)):
            lab = '+'.join(types) + ('(rot)' if rot else '')
            os_ = orbits_from_gens(gg, n); GENS[lab] = gg
            for o in os_: ORB.setdefault(o, []).append((lab, degs, rot))
        print(f'  PROGRESS {name} subgroup {"+".join(types)}: orbit sizes {sorted(len(o) for o in orbits_from_gens(gens, n))}', flush=True)
    print(f'  {len(ORB)} distinct orbits', flush=True)
    rows = []; flagged = []
    def tones(O):
        Oa = np.array(O); cnt = np.bincount(CI[np.ix_(Oa, Oa)].ravel(), minlength=len(V))
        T = [sum((Q5(int(cnt[c]))*GV[c][k] for c in range(len(V)) if cnt[c]), Q5()) for k in range(KMAX+1)]
        return cnt, T
    for oi, (O, labs) in enumerate(sorted(ORB.items(), key=lambda t: (len(t[0]), t[0]))):
        cnt, T = tones(O)
        zeros = [k for k in range(1, KMAX+1) if T[k].iszero()]
        if enum:
            mask = np.zeros(n, bool); mask[list(O)] = True
            S = G[mask[G[:, list(O)]].all(axis=1)]
            h = molien_h(mats(S), KMAX); ssz = len(S)
            seen = np.zeros(n, bool); sorb = []
            for i in range(n):
                if not seen[i]: o = np.unique(S[:, i]); seen[o] = True; sorb.append(tuple(int(t) for t in o))
        else:
            hs = [molien_degrees(dg, d, rot, KMAX) for _, dg, rot in labs]
            h = [min(x[k] for x in hs) for k in range(KMAX+1)]; ssz = None
            # -I is in W(E8): an antipodal orbit has the extra symmetry -I, which kills every odd degree (census kind (X))
            negi = [index[tuple(-c for c in pts[i])] for i in O]
            if set(negi) == set(O): h = [0 if k % 2 else h[k] for k in range(KMAX+1)]; ssz = 'antipodal'
            sorb = orbits_from_gens(GENS[labs[0][0]], n)
        genuine = [k for k in zeros if h[k] > 0]
        rows.append((len(O), labs[0][0], ssz, zeros, genuine))
        if B:
            Fv = {j: sum((Q5(int(cnt[c]))*B[j][V[c]] for c in range(len(V)) if cnt[c]), Q5()) for j in B}
            ident = all(T[k] == sum((mult[k][j]*Fv[j] for j in B), Q5()) for k in range(KMAX+1))
            if not ident: check(False, f'{name}: block identity fails on an orbit of size {len(O)}')
            pred = [k for k in range(1, KMAX+1) if all(mult[k][j].iszero() or Fv[j].iszero() for j in B)]
            if pred != zeros: check(False, f'{name}: block prediction != zeros on an orbit of size {len(O)}')
        if len(genuine) >= 2:
            info = ''
            if B:
                zb = [j for j in B if Fv[j].iszero()]
                nontriv = []
                for j in zb:
                    tot = [sum((Q5(int(c))*B[j][V[t]] for t, c in enumerate(np.bincount(CI[np.ix_(np.array(o1), np.array(o2))].ravel(), minlength=len(V))) if c), Q5()) for o1 in sorb for o2 in sorb] if len(sorb) <= 40 else None
                    if tot is None: nontriv.append((j, '?')); continue
                    rk = rank_q5([tot[a*len(sorb):(a+1)*len(sorb)] for a in range(len(sorb))])
                    if rk > 0: nontriv.append((j, rk))
                info = f' | nontrivial vanishing blocks (rank): {nontriv}'
            flagged.append((len(O), labs[0][0], ssz, zeros, genuine, info))
    print(f'  RESULT {name}: {len(rows)} orbits; with >= 1 genuine zero: {sum(1 for r in rows if r[4])}; with >= 2 genuine zeros: {len(flagged)}', flush=True)
    for r in rows:
        if r[4]: print(f'    size {r[0]:3d}  first group {r[1]:16s}  |Stab| {r[2]}  zeros {r[3]}  genuine {r[4]}', flush=True)
    print(f'  FLAGGED {name} (>= 2 genuine zeros):', flush=True)
    for f in flagged: print(f'    size {f[0]:3d}  {f[1]:16s}  |Stab| {f[2]}  zeros {f[3]}  genuine {f[4]}{f[5]}', flush=True)
    return rows, flagged
SETS = {'600': lambda: run('600-cell', P600(), P600(), 'H4', blocks_2I, True),
        '24': lambda: run('24-cell', P24(), F4roots(), 'F4', blocks_2T, True),
        '120': lambda: run('120-cell', P120(), roots_for(P120(), [P600(), P600odd()]), 'H4', None, True),
        'E8': lambda: run('E8 roots', E8(), E8(), 'E8', blocks_E8, False)}
RES = {}
todo = list(SETS) if WHICH == 'all' else WHICH.split(',')
for i, w in enumerate(todo):
    print(f'PROGRESS {i/len(todo):.2f} {w}', flush=True)
    RES[w] = SETS[w]()
# controls
if '600' in RES:
    fl = RES['600'][1]
    check(any(f[0] == 20 and f[4][:2] == [5, 7] for f in fl), 'control: the census 20-set type (zeros 5, 7 genuine) is re-found in the 600-cell')
    check(not any(f[0] == 30 and f[4] == [5, 7] for f in fl), 'control: no 30-orbit claims the 20-set pattern (wrong-pattern check)')
print(f'PROGRESS 1.00 done', flush=True)
print('FINAL ok' if not FAILS else f'FINAL FAIL ({len(FAILS)}): ' + '; '.join(FAILS), flush=True)
