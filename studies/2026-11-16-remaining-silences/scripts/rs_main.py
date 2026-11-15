#!/usr/bin/env python3
"""Remaining silences (16 Nov 2026): explain the zeros the hidden-zeros census left OPEN.
Cases (from ../../2026-11-15-hidden-zeros-h4/data/census-*.json, OPEN with at least one rational condition):
  600-cell, degree 8: 30/60-point unions of [C3 x C5], [C5 x C5], [C3 x C10], [C5 x C5].2 orbits (8 sets = 4 mirror pairs);
  120-cell, degree 8: 240-point union of two [C5 x 2T] orbits (2 sets);
  E8 roots, degree 4: 120-root unions with stabiliser 576 or 144 (4 sets).
Tests per case, all exact in Q(sqrt5) unless marked:
  (a) FULL symmetry group Sym(S) in O(n) (Gram automorphisms, own stabiliser-chain search, independent of the census code) and the
      dimension of Sym(S)-invariant harmonics (float fixed-space rank of the generators on polynomials, rounded, checked integral);
  (c) restricted linkage: on the stabiliser-invariant rational weightings V, the exact kernels K_j = N_j cap V for j <= 20, and which
      degrees j satisfy K_j subset K_k (the zero in degree j forces the open zero k);
  (b1) Hopf rings (600-cell, 120-cell): S is invariant under left (or right) multiplication by a cyclic group C_n, n >= 5; then every
      degree-2l harmonic content (l <= 4) of S factors through the Hopf map x -> xbar p x (p the axis of C_n), so T_2l(S) = 0 iff the
      Hopf image multiset M on S^2 is silent in degree l. Checked exactly (ratio T_2l(S)|S|^2 / tone_l(M) constant) on the cases and on
      random C_n-invariant sets; M is then described (axes / tetrahedral orbits, exact values of the invariant);
  (b2) bizonal swap pairs (E8): S = shell + sum over 24-cells C of (C in shell 2 - C in shell 1); C and its shell-2 copy span orthogonal
      complementary 4-spaces, the 24-cell is a 5-design in its own space, and the only O(4)xO(4)-invariant degree-4 harmonic
      5s^2 - 5s + 1 takes the same value at s = 0 and s = 1. Every term checked silent exactly.
Controls: random unions (not silent, not explained); known explained census sets (Hopf criterion must reproduce their zeros);
symmetry-group search on whole polytopes (orders 14400, 1152, 696729600)."""
import sys, os, json, time, itertools
import numpy as np
from fractions import Fraction as F
from flint import fmpq_mat, fmpq
HERE = os.path.dirname(os.path.abspath(__file__))
HZ = os.path.join(HERE, '..', '..', '2026-11-15-hidden-zeros-h4')
sys.path.insert(0, os.path.join(HZ, 'scripts'))
from hz_core import *
from hz_universes import *
PILOT = '--pilot' in sys.argv
OUT = os.path.join(HERE, '..', 'data'); os.makedirs(OUT, exist_ok=True)
def log(*a): print(*a, flush=True)
T0 = time.time()
CHECKS = []
def check(name, ok):
    CHECKS.append((name, bool(ok))); log(f'CHECK {"ok  " if ok else "FAIL"} {name}')
RES = {}

# ------------------------------------------------------------------ Q(sqrt5) helpers (pairs a + b*phi of Fractions)
def qinv(x):
    a, b = F(x[0]), F(x[1]); n = a * a + a * b - b * b        # norm of a + b phi
    return ((a + b) / n, -b / n)
def qdiv(x, y): return qm(x, qinv(y))
def qz(x): return x[0] == 0 and x[1] == 0
def zmul(x, y):  # quaternion product, coordinates as pairs of ints/Fractions
    def m(u, v): return qm(u, v)
    x0, x1, x2, x3 = x; y0, y1, y2, y3 = y
    s = lambda *t: (sum(p[0] for p in t), sum(p[1] for p in t))
    n = lambda p: (-p[0], -p[1])
    return (s(m(x0, y0), n(m(x1, y1)), n(m(x2, y2)), n(m(x3, y3))),
            s(m(x0, y1), m(x1, y0), m(x2, y3), n(m(x3, y2))),
            s(m(x0, y2), n(m(x1, y3)), m(x2, y0), m(x3, y1)),
            s(m(x0, y3), m(x1, y2), n(m(x2, y1)), m(x3, y0)))
def zconj(x): return (x[0],) + tuple((-c[0], -c[1]) for c in x[1:])
def zdot(u, v):
    a = (F(0), F(0))
    for p, q in zip(u, v): a = qa(a, qm(p, q))
    return a
def pt(X, i): return tuple((F(int(X[i, c, 0])), F(int(X[i, c, 1]))) for c in range(X.shape[1]))

# ------------------------------------------------------------------ exact kernels on a subspace spanned by orbit indicators
def cross_tables(U, orbs, kmax):
    """C[k][i][j] = sum_{x in O_i, y in O_j} G_k(cos) as (a, b) Fraction pairs"""
    d = len(orbs); C = [[[None] * d for _ in range(d)] for _ in range(kmax + 1)]
    for i in range(d):
        for j in range(i, d):
            cnt = np.bincount(U.IM[np.ix_(orbs[i], orbs[j])].ravel(), minlength=U.ncos)
            for k in range(kmax + 1):
                a = sum((int(n) * g[0] for n, g in zip(cnt, U.G[k]) if n), F(0)); b = sum((int(n) * g[1] for n, g in zip(cnt, U.G[k]) if n), F(0))
                C[k][i][j] = C[k][j][i] = (a, b)
    return C
def kernel_rows(Ck):
    """rational kernel of the d x d matrix with Q(sqrt5) entries (rows of A and B stacked); returns fmpq_mat basis as columns"""
    d = len(Ck)
    M = fmpq_mat(2 * d, d, [fmpq(Ck[i][j][0].numerator, Ck[i][j][0].denominator) for i in range(d) for j in range(d)] +
                 [fmpq(Ck[i][j][1].numerator, Ck[i][j][1].denominator) for i in range(d) for j in range(d)])
    rref, rk = M.rref()
    # nullspace from rref
    piv = []; r = 0
    for c in range(d):
        if r < rk and rref[r, c] != 0: piv.append(c); r += 1
    free = [c for c in range(d) if c not in piv]
    basis = []
    for f in free:
        v = [fmpq(0)] * d; v[f] = fmpq(1)
        for ri, pc in enumerate(piv): v[pc] = -rref[ri, f]
        basis.append(v)
    return basis
def subset(Kj, Kk):
    """is span(Kj) inside span(Kk)? (lists of rational vectors)"""
    if not Kj: return True
    if not Kk: return False
    d = len(Kj[0])
    A = fmpq_mat(len(Kk), d, [x for v in Kk for x in v]); B = fmpq_mat(len(Kk) + len(Kj), d, [x for v in Kk + Kj for x in v])
    return A.rank() == B.rank()

# ------------------------------------------------------------------ (a) full symmetry group: stabiliser chain over Gram automorphisms
def aut_chain(IM, Xf, budget=20_000_000):
    n = len(IM); basis = span_basis(Xf); r = len(basis)
    nv = int(IM.max()) + 1; diag = IM[0, 0]
    def enc(M):
        k = np.zeros(M.shape[0], dtype=np.int64)
        for c in range(M.shape[1]): k = k * nv + M[:, c]
        return k
    ref = enc(IM[:, basis])
    if len(np.unique(ref)) != n: raise RuntimeError('basis signatures not unique')
    ondiag = np.nonzero(IM.diagonal() == diag)[0]
    calls = [0]
    def extend(ys):
        i = len(ys); calls[0] += 1
        if calls[0] > budget: raise RuntimeError('search budget exceeded')
        if i == r:
            sig = enc(IM[:, ys]); o = np.argsort(sig); ss = sig[o]; pos = np.searchsorted(ss, ref)
            if (pos < n).all() and (ss[np.minimum(pos, n - 1)] == ref).all(): return o[pos]
            return None
        cand = ondiag
        for j, y in enumerate(ys): cand = cand[IM[cand, y] == IM[basis[i], basis[j]]]
        for c in cand:
            if c in ys: continue
            g = extend(ys + [int(c)])
            if g is not None: return g
        return None
    gens = []; order = 1; orbits = []
    for i in range(r):
        pre = basis[:i]
        cand = ondiag
        for j in range(i): cand = cand[IM[cand, basis[j]] == IM[basis[i], basis[j]]]
        orbit = {basis[i]}; lg = []
        for t in cand:
            t = int(t)
            if t in orbit: continue
            g = extend(pre + [t])
            if g is not None:
                lg.append(g)
                fr = list(orbit)
                while fr:
                    nf = []
                    for x in fr:
                        for h in lg:
                            y = int(h[x])
                            if y not in orbit: orbit.add(y); nf.append(y)
                    fr = nf
        orbits.append(len(orbit)); order *= len(orbit); gens += lg
    return order, gens, basis, orbits

def inv_harm_dims(mats, kmax, seed=0):
    """dims of invariant harmonics of degree k <= kmax for the group generated by mats (n x n float, orthogonal), via fixed spaces
    of the generators on polynomials of degree d (monomial basis, least squares), harm(k) = poly(k) - poly(k - 2)."""
    n = mats[0].shape[0]; rng = np.random.default_rng(seed)
    polyinv = []
    for d in range(kmax + 1):
        mons = [e for e in itertools.product(range(d + 1), repeat=n) if sum(e) == d]
        E = np.array(mons)
        P = rng.normal(size=(3 * len(mons) + 10, n)); P /= np.linalg.norm(P, axis=1)[:, None]
        V = np.prod(P[:, None, :] ** E[None, :, :], axis=2)
        Q, R = np.linalg.qr(V)
        rows = []
        for g in mats:
            Vg = np.prod((P @ g.T)[:, None, :] ** E[None, :, :], axis=2)
            Cg = np.linalg.solve(R, Q.T @ Vg)            # V Cg = Vg
            rows.append(Cg - np.eye(len(mons)))
        Mtot = np.vstack(rows) if rows else np.zeros((1, len(mons)))
        s = np.linalg.svd(Mtot, compute_uv=False)
        tol = 1e-7 * max(1.0, s.max())
        polyinv.append(int((s < tol).sum()) + max(0, len(mons) - len(s)))
    return [polyinv[k] - (polyinv[k - 2] if k >= 2 else 0) for k in range(kmax + 1)]

def sym_analysis(U, S, kmax):
    S = np.array(sorted(S))
    IM = U.IM[np.ix_(S, S)]
    order, gens, basis, orbs = aut_chain(IM, U.Xf[S])
    if order <= 200000:
        idn = np.arange(len(S), dtype=np.int32); seen = {idn.tobytes(): idn}; fr = [idn]
        G = [np.asarray(g, dtype=np.int32) for g in gens]
        while fr:
            nf = []
            for p in fr:
                for g in G:
                    q = g[p]; kb = q.tobytes()
                    if kb not in seen: seen[kb] = q; nf.append(q)
            fr = nf
        assert len(seen) == order, (len(seen), order)
        mats = float_mats(U.Xf[S], np.array(list(seen.values())), basis)
        dims = harm_dims(mats, kmax, len(basis)); how = 'Molien over all elements'
    else:
        mats = float_mats(U.Xf[S], np.array(gens), basis)
        dims = inv_harm_dims(list(mats), min(kmax, 4)); how = 'fixed space of generators on polynomials'
    split = None
    if U.dim == 8 and gens:
        Zb = U.Xf[S][basis]                                   # r x 8, r = 8
        if len(basis) == 8:
            Zi = np.linalg.inv(Zb)
            blocks = [np.abs((Zi @ U.Xf[S][np.asarray(g)[basis]]).T[:4, 4:]).max() for g in gens]
            split = bool(max(blocks) < 1e-9)
    SPLIT[0] = split
    return order, orbs, dims, len(basis), how
SPLIT = [None]

# ------------------------------------------------------------------ setup
X, A, lab, Lp, Rp, St, sig = h4_ambient()
U6 = u600(X)
Y, lift = cell120_from(X, A)
U12 = Universe('120-cell', Y, 4, to_float(Y))
P8, ipB, Yf = e8_from(X)
U8 = Universe('E8 roots', P8, 8, Yf, ipfun=ipB)
Xf6 = to_float(X) / 2
ki = {tuple(np.round(v, 9)): i for i, v in enumerate(Xf6)}
ONE = ki[(1.0, 0.0, 0.0, 0.0)]; MONE = ki[(-1.0, 0.0, 0.0, 0.0)]
log(f'PROGRESS 0.02 universes built ({time.time()-T0:.0f}s)')

def census(u): return json.load(open(os.path.join(HZ, 'data', f'census-{u}.json')))
C6, C12, C8 = census('U600'), census('U120'), census('E8')
cases = []
for s in C6['sets']:
    if 8 in s['OPEN']: cases.append(('600-cell', U6, A.P, s))
for s in C12['sets']:
    if 8 in s['OPEN'] and s.get('conditions', 0) >= 1: cases.append(('120-cell', U12, lift, s))
for s in C8['sets']:
    if 4 in s['OPEN'] and s['stab_order'] in (576, 144): cases.append(('E8', U8, np.hstack([A.P, A.P + 120]).astype(np.int32), s))
log(f'cases: {[(c[0], c[3]["size"], c[3]["stab_order"]) for c in cases]}')
check('case list = 8 + 2 + 4 sets', [c[0] for c in cases].count('600-cell') == 8 and [c[0] for c in cases].count('120-cell') == 2 and [c[0] for c in cases].count('E8') == 4)
if PILOT: cases = [cases[0], next(c for c in cases if c[0] == '120-cell'), next(c for c in cases if c[0] == 'E8')]

def open_degree(c): return 8 if c[0] != 'E8' else 4

# ------------------------------------------------------------------ (a) controls: whole polytopes
log('== (a) controls: symmetry-group search on whole polytopes')
o6, _, _, _ = aut_chain(U6.IM, U6.Xf); check(f'600-cell symmetry order {o6} = 14400', o6 == 14400)
rat = np.nonzero((X[..., 1] == 0).all(1))[0]
o24, _, _, _ = aut_chain(U6.IM[np.ix_(rat, rat)], U6.Xf[rat]); check(f'24-cell symmetry order {o24} = 1152', o24 == 1152)
if not PILOT:
    o8, _, _, _ = aut_chain(U8.IM, U8.Xf, budget=20_000_000); check(f'E8 roots symmetry order {o8} = 696729600', o8 == 696729600)
log(f'PROGRESS 0.10 controls (a) done ({time.time()-T0:.0f}s)')

# ------------------------------------------------------------------ per case: (a), (c)
out_cases = []
for ci, (uname, U, Pa, s) in enumerate(cases):
    S = np.array(s['rep']); k0 = open_degree((uname,))
    rec = {'universe': uname, 'size': len(S), 'stab_order': s['stab_order'], 'zeros': s['zeros'], 'open': k0, 'rep': S.tolist()}
    # (a)
    try:
        order, orbs_chain, dims, rk, how = sym_analysis(U, S, k0)
    except RuntimeError as e:
        order, orbs_chain, dims, how = None, [], [None] * (k0 + 1), str(e)
    rec['sym_order'] = order; rec['sym_inv_harm_dims'] = dims
    rec['a_forced'] = dims[k0] == 0; rec['sym_method'] = how
    if uname == 'E8':
        rec['sym_preserves_4plus4_split'] = SPLIT[0]
        rec['a_forced_with_bizonal_root'] = bool(SPLIT[0] and dims[k0] == 1)
        log(f'   Sym(S) preserves the 4+4 Double-Vision split: {SPLIT[0]} -> its only degree-4 invariant is the bizonal h (zero on every root): {rec["a_forced_with_bizonal_root"]}')
    log(f'[{uname} {len(S)} stab {s["stab_order"]}] (a) |Sym(S)| = {order} (chain {orbs_chain}); invariant harmonic dims k<={k0} ({how}): {dims} -> forced: {dims[k0] == 0}')
    if uname != 'E8': check(f'{uname} {len(S)}: |Sym(S)| equals census symmetry order {s["sym_order"]}', order == s['sym_order'])
    # (c)
    inS = np.zeros(U.N, bool); inS[S] = True
    stab = np.nonzero(inS[Pa[:, S]].all(1))[0]
    orbs = orbits_from_gens(Pa[stab], U.N)
    Ct = cross_tables(U, orbs, 20)
    K = [kernel_rows(Ct[k]) for k in range(21)]
    d = len(orbs)
    vis = [d - len(K[k]) for k in range(21)]
    w = [fmpq(1) if inS[o[0]] else fmpq(0) for o in orbs]
    # S in K_k exactly for its zeros
    def inK(Kk, v): return subset([v], Kk) if Kk else all(x == 0 for x in v)
    zs = [k for k in range(1, 21) if inK(K[k], w)]
    check(f'{uname} {len(S)}: exact kernel zeros {zs} = census zeros', zs == s['zeros'])
    forcing = [j for j in range(1, 21) if j != k0 and vis[j] > 0 and subset(K[j], K[k0])]
    others = [j for j in s['zeros'] if j != k0]
    # intersection of the kernels of the other zero degrees, exactly
    rows = []
    for j in others:
        # constraints of degree j: rows of [A;B]
        for i in range(d):
            rows.append([fmpq(Ct[j][i][jj][0].numerator, Ct[j][i][jj][0].denominator) for jj in range(d)])
            rows.append([fmpq(Ct[j][i][jj][1].numerator, Ct[j][i][jj][1].denominator) for jj in range(d)])
    if rows:
        M = fmpq_mat(len(rows), d, [x for r_ in rows for x in r_])
        Mk = fmpq_mat(len(rows) + 2 * d, d, [x for r_ in rows for x in r_] +
                      [fmpq(Ct[k0][i][jj][t].numerator, Ct[k0][i][jj][t].denominator) for t in (0, 1) for i in range(d) for jj in range(d)])
        others_force = M.rank() == Mk.rank()
    else:
        others_force = False
    rec.update({'dimV': d, 'visible_dims': vis, 'forcing_degrees': forcing, 'other_zeros_force_open': others_force})
    log(f'   (c) dim V = {d}; visible dims k=0..20: {vis}; degrees j with K_j in K_{k0}: {forcing}; the other zeros {others} force {k0}: {others_force}')
    out_cases.append(rec)
    log(f'PROGRESS {0.10 + 0.40 * (ci + 1) / len(cases):.3f} case {ci + 1}/{len(cases)} (a),(c) done ({time.time()-T0:.0f}s)')

# ------------------------------------------------------------------ (b1) Hopf rings for 600-cell and 120-cell
log('== (b1) Hopf reduction')
QX = [pt(X, i) for i in range(120)]
QY = [pt(Y, i) for i in range(600)]
def label_side(g):
    l, r, s_ = map(int, lab[g])
    if s_ != 0: return None
    if r in (ONE, MONE): return ('L', l if r == ONE else ki[tuple(np.round(-Xf6[l], 9))])
    if l in (ONE, MONE): return ('R', r if l == ONE else ki[tuple(np.round(-Xf6[r], 9))])
    return None
def qorder(i):
    c = Xf6[i][0]
    for n in range(1, 31):
        if abs(c - np.cos(2 * np.pi / n)) < 1e-9: return n
def hopf_side(Pa, S, N):
    inS = np.zeros(N, bool); inS[S] = True
    stab = np.nonzero(inS[Pa[:, S]].all(1))[0]
    best = None
    for g in stab:
        t = label_side(g)
        if t is None: continue
        n = qorder(t[1])
        if n in (5, 10) and (best is None or n > best[2]): best = (t[0], t[1], n)
    return best
def hopf_images(Q, S, side, q):
    p = (( F(0), F(0)),) + QX[q][1:]
    out = []
    for i in S:
        x = Q[i]
        u = zmul(zmul(zconj(x), p), x) if side == 'L' else zmul(zmul(x, p), zconj(x))
        assert qz(u[0])
        out.append(u[1:])
    return out
def s2_tones(M, lmax):
    n2 = zdot(M[0], M[0])
    for u in M: assert zdot(u, u) == n2
    mult = {}
    for u in M: mult[u] = mult.get(u, 0) + 1
    D = list(mult); cnt = {}; inv2 = qinv(n2)
    for u in D:
        for v in D:
            c = qm(zdot(u, v), inv2); cnt[c] = cnt.get(c, 0) + mult[u] * mult[v]
    cs = list(cnt); G = gegen_table(cs, lmax, 3)
    return [(sum(cnt[c] * G[l][i][0] for i, c in enumerate(cs)), sum(cnt[c] * G[l][i][1] for i, c in enumerate(cs))) for l in range(lmax + 1)]
def s4_raw(U, S):
    S = np.asarray(sorted(S)); cnt = np.bincount(U.IM[np.ix_(S, S)].ravel(), minlength=U.ncos)
    return U.tones_counts(cnt)
ratio_seen = {}
def hopf_check(tag, U, Q, Pa, S, lmax=4, record=True):
    hs = hopf_side(Pa, S, U.N)
    if hs is None or hs[2] < 5: return None
    side, q, n = hs
    M = hopf_images(Q, S, side, q)
    tb = s2_tones(M, lmax); ts = s4_raw(U, S)
    ok = True; ratios = []
    for l in range(1, lmax + 1):
        a, b = ts[2 * l], tb[l]
        if qz(b): ok &= qz(a); ratios.append(None)
        else:
            rr = qdiv(a, b); ratios.append(rr)
            key = (U.name, l); ratio_seen.setdefault(key, set()).add(rr)
    return {'side': side, 'n': n, 'M': M, 'base_zero': [l for l in range(1, lmax + 1) if qz(tb[l])], 'S_zero_even': [2 * l for l in range(1, lmax + 1) if qz(ts[2 * l])], 'equiv_ok': ok}

def axis_key(u):
    f = np.array([qf(c) for c in u]); f /= np.linalg.norm(f)
    j = np.argmax(np.abs(f) > 1e-9); f = f if f[j] > 0 else -f
    return tuple(np.round(f, 7))

hopf_rec = []
for rec, (uname, U, Pa, s) in zip(out_cases, cases):
    if uname == 'E8': continue
    S = np.array(s['rep']); Q = QX if uname == '600-cell' else QY
    h = hopf_check(uname, U, Q, Pa, S)
    if h is None:
        rec['hopf'] = None; log(f'[{uname} {len(S)}] no left/right cyclic factor of order >= 5'); continue
    axes = {}
    for u in h['M']: k_ = axis_key(u); axes[k_] = axes.get(k_, 0) + 1
    dirs = {}
    for u in h['M']:
        f = np.array([qf(c) for c in u]); f /= np.linalg.norm(f); kk = tuple(np.round(f, 7)); dirs[kk] = dirs.get(kk, 0) + 1
    rec['hopf'] = {'side': h['side'], 'cyclic_order': h['n'], 'base_silent_degrees': h['base_zero'], 'S_even_zeros_le8': h['S_zero_even'],
                   'equivalence_exact': h['equiv_ok'], 'n_directions': len(dirs), 'direction_multiplicities': sorted(dirs.values()),
                   'n_axes': len(axes), 'axis_multiplicities': sorted(axes.values())}
    log(f'[{uname} {len(S)}] Hopf ({h["side"]} C{h["n"]}): base silent in l = {h["base_zero"]}; S silent in even degrees <= 8: {h["S_zero_even"]}; '
        f'exact equivalence: {h["equiv_ok"]}; {len(dirs)} directions, multiplicities {sorted(dirs.values())}; {len(axes)} axes, {sorted(axes.values())}')
    check(f'{uname} {len(S)}: Hopf equivalence T_2l(S)=0 <=> tone_l(M)=0, l<=4', h['equiv_ok'])
    check(f'{uname} {len(S)}: Hopf base silent in l={open_degree((uname,))//2}', open_degree((uname,)) // 2 in h['base_zero'])
    if uname == '120-cell':
        # tetrahedral frame from the order-4 elements on the other side; value of the T-invariant quartic on each direction
        inS = np.zeros(U.N, bool); inS[S] = True
        stab = np.nonzero(inS[Pa[:, S]].all(1))[0]
        other = 'R' if h['side'] == 'L' else 'L'
        o4 = sorted({t[1] for g in stab for t in [label_side(g)] if t and t[0] == other and qorder(t[1]) == 4})
        axes4 = []
        for i in o4:
            v = QX[i][1:]
            if not any(all(qz(qa(a_, b_)) for a_, b_ in zip(v, w_)) or v == w_ for w_ in axes4): axes4.append(v)
        log(f'   tetrahedral frame: {len(axes4)} two-fold axes from {len(o4)} order-4 elements')
        def hT(u):
            nu = zdot(u, u); tot = (F(0), F(0))
            for e in axes4:
                c2 = qdiv(qm(zdot(u, e), zdot(u, e)), qm(nu, zdot(e, e)))
                tot = qa(tot, qm(c2, c2))
            return qs(tot, (F(3, 5), F(0)))
        vals = {}
        for u in h['M']:
            f = np.array([qf(c) for c in u]); f /= np.linalg.norm(f); kk = tuple(np.round(f, 7))
            vals.setdefault(qstr(hT(u)), [0, kk])[0] += 1
        tot = (F(0), F(0))
        for u in h['M']: tot = qa(tot, hT(u))
        rec['hopf']['quartic_values'] = {k_: v[0] for k_, v in vals.items()}
        rec['hopf']['quartic_sum'] = qstr(tot)
        log(f'   T-invariant quartic x^4+y^4+z^4-3/5 on the Hopf image (value: multiplicity): {rec["hopf"]["quartic_values"]}; sum {qstr(tot)}')
        check(f'{uname} {len(S)}: quartic sum over Hopf image = 0 exactly', qz(tot) and len(axes4) == 3)
log(f'PROGRESS 0.60 Hopf on cases done ({time.time()-T0:.0f}s)')

# Hopf controls: random left-C5-invariant sets (unions of left cosets), and every census set with a cyclic factor of order >= 5
log('== (b1) controls')
rng = np.random.default_rng(20261116)
def left_cosets(U, Q, q, N, side='L'):
    # cosets of the left (right) cyclic group generated by icosian q acting on the universe points
    g = int(A.index_of(Lp[q][None])[0])
    P = A.P if U is U6 else lift
    return orbits_from_gens(P[[g]], N), g
o5 = [i for i in range(120) if qorder(i) == 5]
for U, Q, P, name in ((U6, QX, A.P, '600-cell'), (U12, QY, lift, '120-cell')):
    cos_, g = left_cosets(U, Q, o5[0], U.N)
    nrand = 40 if PILOT else 400; nsil = 0; ok = True; nexp = 0
    for t in range(nrand):
        m = rng.integers(2, len(cos_) // 2 + 1)
        pick = rng.choice(len(cos_), m, replace=False)
        S = np.concatenate([cos_[i] for i in pick])
        h = hopf_check(name, U, Q, P, S)
        if h is None: ok = False; break
        ok &= h['equiv_ok']
        if 8 in h['S_zero_even'] or 4 in h['S_zero_even']: nsil += 1
    check(f'{name}: Hopf equivalence on {nrand} random left-C5-invariant sets (silent among them in degree 4 or 8: {nsil})', ok)
    # constructed equal-coverage sets (600-cell): pick cosets so each 5-fold axis gets equal coverage -> must be silent in 4 and 8
    if name == '600-cell':
        byaxis = {}
        for i, c in enumerate(cos_):
            u = hopf_images(Q, c[:1], 'L', o5[0])[0]; byaxis.setdefault(axis_key(u), []).append(i)
        ok2 = True; nb = 0
        for t in range(20 if PILOT else 200):
            m = rng.integers(1, min(len(v) for v in byaxis.values()) + 1)
            pick = [i for v in byaxis.values() for i in rng.choice(v, m, replace=False)]
            S = np.concatenate([cos_[i] for i in pick]); z = U.zeros(S)
            ok2 &= (4 in z and 8 in z); nb += 1
        check(f'600-cell: {nb} constructed equal-axis-coverage left-C5 sets are all silent in degrees 4 and 8 (cosets per axis: {sorted(len(v) for v in byaxis.values())})', ok2)
        rec_axes = {str(k): len(v) for k, v in byaxis.items()}
for key, v in ratio_seen.items():
    check(f'Hopf ratio T_2l(S)|S|^2 / tone_l(M) constant for {key}: {len(v)} value(s)', len(v) == 1)
    log(f'   ratio {key}: {[qstr(x) for x in v]}')
# known explained census sets with a cyclic factor of order >= 5: Hopf must reproduce their even zeros <= 8
nk = 0; okk = True
for name, U, Q, P, Cn in (('600-cell', U6, QX, A.P, C6), ('120-cell', U12, QY, lift, C12)):
    sets_ = [s for s in Cn['sets'] if not s['OPEN'] and any(k in s['zeros'] for k in (4, 8))]
    if PILOT: sets_ = sets_[:15]
    for s in sets_:
        S = np.array(s['rep'] if isinstance(s['rep'], list) else json.loads(s['rep']))
        h = hopf_check(name, U, Q, P, S)
        if h is None: continue
        nk += 1
        okk &= h['equiv_ok'] and set(h['S_zero_even']) == {k for k in s['zeros'] if k in (2, 4, 6, 8)}
check(f'Hopf criterion reproduces the even zeros <= 8 of all {nk} explained census sets with a cyclic factor of order >= 5', okk and nk > 0)
log(f'PROGRESS 0.75 Hopf controls done ({time.time()-T0:.0f}s)')

# ------------------------------------------------------------------ (b2) E8 bizonal swap pairs
log('== (b2) E8 bizonal swap pairs')
# the 25 24-cells inside the 600-cell: left cosets of the five conjugates of 2T
two_t = [i for i in rat]
def qmulf(a, b):
    a0, a1, a2, a3 = a; b0, b1, b2, b3 = b
    return np.array([a0*b0-a1*b1-a2*b2-a3*b3, a0*b1+a1*b0+a2*b3-a3*b2, a0*b2-a1*b3+a2*b0+a3*b1, a0*b3+a1*b2-a2*b1+a3*b0])
def qinvf(a): return np.array([a[0], -a[1], -a[2], -a[3]])
cells24 = set()
for c in range(120):
    conj = [ki[tuple(np.round(qmulf(qmulf(Xf6[c], Xf6[t]), qinvf(Xf6[c])), 9))] for t in two_t]
    for x in range(120):
        cells24.add(tuple(sorted(ki[tuple(np.round(qmulf(Xf6[x], Xf6[t]), 9))] for t in conj)))
cells24 = sorted(cells24)
check(f'24-cells inscribed in the 600-cell: {len(cells24)} = 25', len(cells24) == 25)
G4 = U8.G[4]; G2 = U8.G[2]
def content_zero(U, wvec, k):
    """exact: is the weighting wvec (dict index -> int) silent in degree k?  M_k w = 0 over Q(sqrt5)"""
    idx = list(wvec); wv = np.array([wvec[i] for i in idx])
    for x in range(U.N):
        a = F(0); b = F(0)
        for i, wi in zip(idx, wv):
            g = U.G[k][U.IM[x, i]]; a += int(wi) * g[0]; b += int(wi) * g[1]
        if a != 0 or b != 0: return False
    return True
# general law: for every inscribed 24-cell C, D_C = C(shell 2) - C(shell 1) is silent in degree 4, not in degree 2; C(1) _|_ C(2)
law_ok = True; orth_ok = True
cl = cells24 if not PILOT else cells24[:3]
for C in cl:
    D = {i: -1 for i in C}; D.update({120 + i: 1 for i in C})
    law_ok &= content_zero(U8, D, 4) and not content_zero(U8, D, 2)
    Bs = U8.IM[np.ix_(list(C), [120 + i for i in C])]
    vals = {U8.cos[v] for v in np.unique(Bs)}
    orth_ok &= vals == {(F(0), F(0))}
check(f'every inscribed 24-cell C: C in shell 1 is orthogonal to its copy in shell 2 ({len(cl)} checked)', orth_ok)
check(f'every inscribed 24-cell C: D_C = C(2) - C(1) silent in degree 4, not in degree 2 ({len(cl)} checked)', law_ok)
# negative control: mismatched pairs C(2) - C'(1), C != C', are not silent in degree 4 (they are not orthogonal complements)
neg = 0; negn = 0
for t in range(10 if PILOT else 60):
    i, j = rng.choice(len(cells24), 2, replace=False)
    if set(cells24[i]) & set(cells24[j]): continue
    D = {x: -1 for x in cells24[j]}; D.update({120 + x: 1 for x in cells24[i]})
    negn += 1; neg += content_zero(U8, D, 4)
check(f'negative control: {negn} disjoint mismatched pairs C(2) - C\'(1): silent in degree 4 in {neg}', negn > 0 and neg == 0)
shell_ok = content_zero(U8, {i: 1 for i in range(120)}, 4) and content_zero(U8, {120 + i: 1 for i in range(120)}, 4)
check('both 600-cell shells silent in degree 4 (bizonal root, census RES)', shell_ok)
for rec, (uname, U, Pa, s) in zip(out_cases, cases):
    if uname != 'E8': continue
    S = set(s['rep']); A1 = {i for i in S if i < 120}; A2 = {i - 120 for i in S if i >= 120}
    found = None
    for first, second, sh in ((A1, A2, 2), (A2, A1, 1)):
        # 'second' must be a disjoint union of inscribed 24-cells and 'first' its complement
        if first | second != set(range(120)) or first & second: continue
        fam = [C for C in cells24 if set(C) <= second]
        # exact cover of 'second' by disjoint members of fam
        def cover(rem, chosen):
            if not rem: return chosen
            x = min(rem)
            for C in fam:
                if x in C and set(C) <= rem:
                    r_ = cover(rem - set(C), chosen + [C])
                    if r_: return r_
            return None
        cv = cover(set(second), [])
        if cv: found = (sh, cv); break
    if found:
        sh, cv = found
        # exact identity S = shell(3 - sh) + sum_C (C(sh) - C(3 - sh)) as weightings
        Wt = {}
        base = 0 if sh == 2 else 120
        for i in range(120): Wt[base + i] = Wt.get(base + i, 0) + 1
        for C in cv:
            for i in C:
                Wt[(120 if sh == 2 else 0) + i] = Wt.get((120 if sh == 2 else 0) + i, 0) + 1
                Wt[base + i] = Wt.get(base + i, 0) - 1
        ident = {i for i, v in Wt.items() if v != 0} == S and all(v == 1 for v in Wt.values() if v != 0)
        rec['bizonal'] = {'shell_kept': 1 if sh == 2 else 2, 'n_24cells_swapped': len(cv), 'identity_exact': ident}
        log(f'[E8 {len(S)} stab {s["stab_order"]}] S = shell {1 if sh == 2 else 2} with {len(cv)} inscribed 24-cell(s) swapped to the other shell; identity exact: {ident}')
        check(f'E8 {len(S)} stab {s["stab_order"]}: bizonal swap decomposition exact', ident)
    else:
        rec['bizonal'] = None; log(f'[E8 {len(S)} stab {s["stab_order"]}] no bizonal swap decomposition'); check(f'E8 stab {s["stab_order"]}: bizonal decomposition found', False)
# float check of the formula: the O(4)xO(4)-invariant harmonic h = 5s^2 - 5s + 1 (s = |x_par|^2 on S^7) is harmonic and symmetric
xs = rng.normal(size=(2000, 8)); xs /= np.linalg.norm(xs, axis=1)[:, None]
def hpoly(x): a = (x[:, :4] ** 2).sum(1); b = (x[:, 4:] ** 2).sum(1); return a * a - 3 * a * b + b * b
eps = 1e-4; lap = np.zeros(len(xs))
for c in range(8):
    e = np.zeros(8); e[c] = eps; lap += (hpoly(xs + e) - 2 * hpoly(xs) + hpoly(xs - e)) / eps ** 2
check('bizonal h = |a|^4 - 3|a|^2|b|^2 + |b|^4 is harmonic (finite differences, float) and h(s=0) = h(s=1) = 1', np.abs(lap).max() < 1e-3)
log(f'PROGRESS 0.90 E8 bizonal done ({time.time()-T0:.0f}s)')

# ------------------------------------------------------------------ random-union controls for (c): random unions of stabiliser orbits
log('== (c) control: random unions of orbits of the same stabilisers')
rc_ok = True; rc_n = 0
for rec, (uname, U, Pa, s) in zip(out_cases, cases):
    if uname == 'E8' and PILOT: continue
    S = np.array(s['rep']); inS = np.zeros(U.N, bool); inS[S] = True
    stab = np.nonzero(inS[Pa[:, S]].all(1))[0]; orbs = orbits_from_gens(Pa[stab], U.N)
    for t in range(5):
        pick = [o for o in orbs if rng.random() < 0.5]
        if not pick: continue
        T = np.concatenate(pick); z = U.zeros(T); rc_n += 1
        k0 = open_degree((uname,))
        for j in rec['forcing_degrees']:
            if j in z and k0 not in z: rc_ok = False
check(f'(c) soundness on {rc_n} random unions of stabiliser orbits (a forcing degree zero always brings the open zero)', rc_ok)

summary = {'cases': [{k: v for k, v in r.items() if k != 'rep'} | {'rep': r['rep']} for r in out_cases],
           'hopf_ratios': {f'{k[0]} l={k[1]}': [qstr(x) for x in v] for k, v in ratio_seen.items()},
           'checks': [{'name': n, 'ok': o} for n, o in CHECKS], 'pilot': PILOT}
json.dump(summary, open(os.path.join(OUT, 'remaining-silences' + ('-pilot' if PILOT else '') + '.json'), 'w'), indent=1, default=str)
nf = sum(not o for _, o in CHECKS)
log(f'PROGRESS 1.00 done: {len(CHECKS) - nf}/{len(CHECKS)} checks passed ({time.time()-T0:.0f}s)')
if nf == 0: print('FINAL ok')
else: print(f'FINAL FAIL ({nf} checks failed)')
