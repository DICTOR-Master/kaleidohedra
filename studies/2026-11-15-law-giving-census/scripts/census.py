#!/usr/bin/env python3
"""LAW-GIVING CENSUS over the Wythoff universe (15 Nov 2026).

Universe: for each reflection group G in {A3, B3, H3, A4, B4, D4, F4, H4}, every one-parameter family of Wythoff polytopes
P(c) = conv(G v), v = sum c_j w_j, whose edge-length pattern c has every entry in {0, 1, t} (at least one 1, one t), t > 0,
taken up to t <-> 1/t and diagram automorphisms; plus the stations (patterns in {0, 1}: the uniform polytopes).
On an open family the combinatorial type, the dihedral angles and the facet normals are constant, so every battery quantity is an
exact algebraic function of t:
  corner tones T_k(t) = (1/|G|) sum_g P_k(<v, g v>/<v, v>) / P_k(1)  (O(d)-invariant; T_k = 0 iff the corners are silent in degree k)
  Mahler product M(t) = vol(P) vol(P polar)  (= canonical form at the centre x vol / d!)
  isoperimetric quotient V^(d-1)/A^d
  Dehn invariant (3D): 1 (x) X + t (x) Y with X, Y in the Q-span of the dihedral angles mod pi.
Geometric involutions of a family: sigma(p) = swap(p) for a diagram automorphism sigma gives t -> 1/t with P(1/t) ~ P(t)
(fixed point t = 1); no other similarity can exist (edge lengths are {2, 2t}). Forced laws at t = 1: evenness (every
scale-invariant quantity is critical) and extra symmetry (tones killed by the larger group).
Usage: census.py GROUP [workers] [--pilot]  -> data/census-GROUP.json, log lines (PROGRESS, ok/FAIL, FINAL ok/FAIL)
"""
import sys, os, json, time, itertools, math
from fractions import Fraction as Fr
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exact as X
from exact import K, E, kk, positive_roots
import groups as GR
from flint import fmpq, fmpq_poly, arb

FAILS = []; CHECKS = [0]
def check(cond, msg):
    CHECKS[0] += 1
    print(('ok   ' if cond else 'FAIL ') + msg, flush=True)
    if not cond: FAILS.append(msg)

# ---------- zonal polynomials (Legendre for S^2, Chebyshev U for S^3) ----------
def zonal(k, d):
    if d == 3: return fmpq_poly.legendre_p(k)
    x = fmpq_poly([0, 1]); U0, U1 = fmpq_poly([1]), fmpq_poly([0, 2])
    if k == 0: return U0
    for _ in range(k - 1): U0, U1 = U1, 2*x*U1 - U0
    return U1

# ---------- patterns ----------
def swap(p): return tuple({0: 0, 1: 2, 2: 1}[x] for x in p)
def act(s, p):
    q = [None]*len(p)
    for i in range(len(p)): q[s[i]] = p[i]
    return tuple(q)

def families(gd):
    r = gd['r']; auts = [tuple(range(r))] + [tuple(s) for s in gd['aut']]
    seen = set(); fams = []
    for p in itertools.product((0, 1, 2), repeat=r):
        if 1 not in p or 2 not in p or p in seen: continue
        orb = set()
        for s in auts:
            q = act(s, p); orb.add(q); orb.add(swap(q))
        seen |= orb
        inv = [s for s in auts[1:] if act(s, p) == swap(p)]
        sym = [s for s in auts[1:] if act(s, p) == p]
        fams.append({'p': p, 'raw_patterns': len(orb), 'inv': inv, 'sym': sym})
    return fams

def stations(gd):
    r = gd['r']; auts = [tuple(range(r))] + [tuple(s) for s in gd['aut']]
    seen = set(); out = []
    for p in itertools.product((0, 1), repeat=r):
        if 1 not in p or p in seen: continue
        orb = {act(s, p) for s in auts}; seen |= orb; out.append({'p': p, 'sym': [s for s in auts[1:] if act(s, p) == p]})
    return out

def cvec(p):
    t = E.t(); return [E.const(0) if x == 0 else (E.const(1) if x == 1 else t) for x in p]

# ---------- group precomputation ----------
class Grp:
    def __init__(s, name):
        s.gd = GR.group_data(name); gd = s.gd; s.name = name
        s.r, s.d, s.n = gd['r'], gd['r'], gd['n']
        t0 = time.time(); s.els = GR.elements(gd)
        s.M = [[[GR.dot(gd['W'][i], g[j]) for j in range(s.r)] for i in range(s.r)] for g in s.els]
        s.Gw = gd['Gw']; s.detGw = GR.det(s.Gw)
        print(f'group {name}: order {len(s.els)}, field Q(sqrt{gd["D"]}), ambient {s.n}, built in {time.time()-t0:.1f} s', flush=True)

# ---------- tones ----------
def tone_polys(g, p, kmax):
    r = g.r; O = [i for i in range(r) if p[i] == 1]; T = [i for i in range(r) if p[i] == 2]
    cnt = Counter()
    for M in g.M:
        s0 = sum((M[i][j] for i in O for j in O), K(0)); s1 = sum((M[i][j] + M[j][i] for i in O for j in T), K(0))
        s2 = sum((M[i][j] for i in T for j in T), K(0))
        cnt[(s0.key(), s1.key(), s2.key())] += 1
    def kfrom(k): return K(fmpq(k[0], k[1]), fmpq(k[2], k[3]))
    t = E.t(); mom = [E.const(0) for _ in range(kmax + 1)]
    for key, c in cnt.items():
        s = E.const(kfrom(key[0])) + E.const(kfrom(key[1]))*t + E.const(kfrom(key[2]))*t*t
        pw = E.const(1)
        for j in range(kmax + 1):
            mom[j] = mom[j] + E.const(c)*pw; pw = pw*s
    c = cvec(p); nrm = E.const(0)
    for i in range(r):
        for j in range(r): nrm = nrm + c[i]*c[j]*E.const(g.Gw[i][j])
    out = {}
    npow = [E.const(1)]
    for _ in range(kmax): npow.append(npow[-1]*nrm)
    for k in range(1, kmax + 1):
        Pk = zonal(k, g.d); co = list(Pk.coeffs())
        N = E.const(0)
        for j, a in enumerate(co):
            if a != 0: N = N + E.const(K(a))*mom[j]*npow[k - j]
        out[k] = {'N': N, 'den': (len(g.els)*Pk(1), k)}   # T_k = N / (|G| P_k(1) n^k)
    return out, nrm, len(cnt)

def tone_value(N, nrm, k, scale, t):
    return N.ev(t) / (kk(K(scale)) * (nrm.ev(t))**1 if False else kk(K(scale)) * kpow(nrm.ev(t), k))
def kpow(x, k):
    r = K(1)
    for _ in range(k): r = r*x
    return r

# ---------- volumes ----------
def pdet(Mx):
    """determinant of a small matrix of E entries (Leibniz)"""
    n = len(Mx); tot = E.const(0)
    for perm in itertools.permutations(range(n)):
        sg = 1
        for i in range(n):
            for j in range(i+1, n):
                if perm[i] > perm[j]: sg = -sg
        term = E.const(sg)
        for i in range(n):
            term = term*Mx[i][perm[i]]
            if term.iszero(): break
        tot = tot + term
    return tot

def vertices_S(g, p):
    """y_S (omega coordinates, E entries) for every subset S (bitmask)"""
    r = g.r; c = cvec(p)
    Gc = [sum((E.const(g.Gw[i][j])*c[j] for j in range(r)), E.const(0)) for i in range(r)]
    Y = {}
    for mask in range(1 << r):
        S = [i for i in range(r) if mask >> i & 1]; y = [E.const(0)]*r
        if S:
            sub = [[g.Gw[i][j] for j in S] for i in S]; inv = GR.mat_inv(sub)
            for a, i in enumerate(S):
                y[i] = sum((E.const(inv[a][b])*Gc[S[b]] for b in range(len(S))), E.const(0))
        Y[mask] = y
    return Y, Gc

def esign(e):
    """sign of E-poly e on t > 0 (constant there by construction): evaluate at t = 1, confirm at t = 1/3 and 3"""
    s = [e.ev(x).sign() for x in (fmpq(1), fmpq(1, 3), fmpq(3))]
    assert len(set(s)) == 1, f'sign varies {s}'
    return s[0]

def volume_area(g, p):
    r = g.r; Y, Gc = vertices_S(g, p)
    V = E.const(0); A = {j: E.const(0) for j in range(r)}
    for perm in itertools.permutations(range(r)):
        masks = []; m = 0
        for i in perm: m |= 1 << i; masks.append(m)
        dt = pdet([Y[mm] for mm in masks])
        if not dt.iszero(): V = V + E.const(esign(dt))*dt
        j = perm[0]; base = Y[masks[0]]
        rows = [[E.const(1) if i == j else E.const(0) for i in range(r)]] + [[Y[mm][i] - base[i] for i in range(r)] for mm in masks[1:]]
        da = pdet(rows)
        if not da.iszero(): A[j] = A[j] + E.const(esign(da))*da
    L = E.const(1)
    for i in range(r): L = L*Gc[i]
    return V, A, L, Gc

# ---------- IQ critical points (rationalised) ----------
def iq_critical(g, V, A):
    """critical points of V^(d-1)/A^d with A = sum_j A_j / sqrt(Gw_jj): roots of sum_j [(d-1)V'A_j - d V A_j'] / sqrt(Gw_jj)"""
    import sympy as sp
    d = g.d; t = sp.Symbol('t'); s = sp.Symbol('s')
    groups_ = defaultdict(lambda: E.const(0))
    for j, Aj in A.items():
        if Aj.iszero(): continue
        Rj = E.const((d - 1))*V.deriv()*Aj - E.const(d)*V*Aj.deriv()
        groups_[g.Gw[j][j].key()] = groups_[g.Gw[j][j].key()] + Rj
    keys = [k for k, v in groups_.items() if not v.iszero()]
    if not keys: return None, []
    def e2sp(e):
        return sum(sp.Rational(int(c.p), int(c.q))*t**i for i, c in enumerate(e.A.coeffs())) + s*sum(sp.Rational(int(c.p), int(c.q))*t**i for i, c in enumerate(e.B.coeffs()))
    ys = sp.symbols(f'y0:{len(keys)}')
    F = 0
    for a, kq in enumerate(keys):
        term = e2sp(groups_[kq])
        for b in range(len(keys)):
            if b != a: term = term*ys[b]
        F += term
    F = sp.expand(F); Fr_ = F
    gk = [sp.Rational(k[0], k[1]) + s*sp.Rational(k[2], k[3]) for k in keys]
    for a in range(len(keys)):
        F = sp.resultant(sp.Poly(F, ys[a]), sp.Poly(ys[a]**2 - gk[a], ys[a])).as_expr() if F.has(ys[a]) else F
        F = sp.expand(F)
    if F.has(s): F = sp.expand(sp.resultant(sp.Poly(F, s), sp.Poly(s**2 - g.gd['D'], s)).as_expr())
    P = sp.Poly(F, t)
    if P.is_zero: return 'identically', []
    fq = fmpq_poly([fmpq(int(sp.Rational(c).p), int(sp.Rational(c).q)) for c in reversed(P.all_coeffs())])
    # numeric evaluator of the genuine branch F(t) with true positive radicals, all sign branches for certification
    import itertools as it
    from flint import arb as Arb
    Dsq = Arb(g.gd['D']).sqrt()
    def branch(x, signs, sD):
        tot = Arb(0)
        for a, kq in enumerate(keys):
            e = groups_[kq]; val = X.pev(e.A, x) + sD*X.pev(e.B, x)
            gval = Arb(fmpq(kq[0], kq[1])) + sD*Arb(fmpq(kq[2], kq[3]))
            tot += val / (signs[a]*gval.sqrt())
        return tot
    roots = []
    c, facs = fq.factor()
    for f, m in facs:
        if f.degree() < 1: continue
        for xr, _ in f.complex_roots():
            if not xr.imag.is_zero(): continue
            x = xr.real
            if not (x > 0): continue
            main = branch(x, [1]*len(keys), Dsq)
            m_ = len(keys)
            others = [branch(x, sg, sd) for sg in it.product((1, -1), repeat=m_) for sd in (Dsq, -Dsq)
                      if not ((all(q == 1 for q in sg) or all(q == -1 for q in sg)) and sd is Dsq)]
            if not main.contains(0): continue
            gen = all(not o.contains(0) for o in others)
            roots.append({'minpoly': [str(q) for q in f.coeffs()], 'deg': f.degree(), 'value': x.mid().str(30, radius=False), 'genuine': gen if gen else None, 'x': x})
    return 'ok', roots

# ---------- Dehn (3D) ----------
def dehn_family(g, p, A):
    import mpmath as mp
    mp.mp.dps = 60
    r = g.r; gd = g.gd; W = gd['W']; R = gd['R']
    c1 = [K(0) if x == 0 else K(1) for x in p]   # t = 1
    v = tuple(sum((c1[i]*W[i][m] for i in range(r)), K(0)) for m in range(g.n))
    facet_types = [k for k in range(r) if not A[k].iszero()]
    def apply(gel, x_w):   # gel = (g w_1..g w_r), x given in omega coords (K)
        return tuple(sum((x_w[i]*gel[i][m] for i in range(r)), K(0)) for m in range(g.n))
    normals = []
    for k in facet_types:
        hk = GR.dot(v, W[k]); seen = set()
        for gel in g.els:
            u = gel[k]; key = GR.vkey(u)
            if key in seen: continue
            seen.add(key); normals.append((k, u, hk))
    classes = []
    for j in range(r):
        if p[j] == 0: continue
        w = GR.refl(v, R[j]); mid = tuple((a + b)*K(Fr(1, 2)) for a, b in zip(v, w))
        inc = [(k, u) for (k, u, hk) in normals if GR.dot(v, u) == hk and GR.dot(w, u) == hk]
        assert len(inc) == 2, (p, j, len(inc))
        (k1, u1), (k2, u2) = inc
        uu = GR.dot(u1, u2); c2 = (uu*uu) / (GR.dot(u1, u1)*GR.dot(u2, u2))
        cosv = -mp.sqrt(mp.mpf(float(c2.a)) + mp.mpf(float(c2.b))*mp.sqrt(gd['D'])) * (1 if uu.sign() > 0 else -1)
        # exact rational parts: rebuild with mpmath rationals
        a_ = mp.mpf(int(c2.a.p))/int(c2.a.q); b_ = mp.mpf(int(c2.b.p))/int(c2.b.q)
        cosv = -mp.sqrt(a_ + b_*mp.sqrt(gd['D'])) * (1 if uu.sign() > 0 else (-1 if uu.sign() < 0 else 0))
        theta = mp.acos(cosv)
        # edge count = orbit size of the edge midpoint
        mid_w = [GR.dot(mid, R[i]) for i in range(r)]   # coordinates <mid, alpha_i> -> omega coords
        orb = {GR.vkey(apply(gel, mid_w)) for gel in g.els}
        classes.append({'node': j, 'len': 'one' if p[j] == 1 else 't', 'count': len(orb), 'cos2': repr(c2), 'cos2_exact': c2, 'cos_sign': -uu.sign(),
                        'theta_deg': float(theta*180/mp.pi), 'theta': theta, 'faces': (k1, k2)})
    return classes

def angle_basis(thetas):
    """Q-relations among the angles and pi by PSLQ (60 digits search, checked at 200 digits)"""
    import mpmath as mp
    out = []
    for th in thetas:
        mp.mp.dps = 60
        rel = mp.pslq([th, mp.pi], maxcoeff=10**6, maxsteps=10**6)
        out.append(rel)
    return out

# ---------- extra (accidental) symmetry ----------
def extra_isometries(g):
    """isometries outside G that can enlarge the symmetry of a G-orbit: B4 -> F4 (reflection in (1,1,1,1)/2), D4 -> B4, F4,
    A3 -> B3 (reflection x1 -> -x1 of the D3 picture), A4 -> -I (point reflection); B3, H3, H4, F4 (beyond the automorphism) none"""
    h = K(Fr(1, 2)); n = g.n
    def reflmap(u): return lambda x: GR.refl(x, u)
    if g.name == 'B4': return {'F4 reflection (1,1,1,1)/2': reflmap((h, h, h, h))}
    if g.name == 'D4': return {'F4 reflection (1,1,1,1)/2': reflmap((h, h, h, h)), 'B4 reflection e4': reflmap((K(0), K(0), K(0), K(1)))}
    if g.name == 'A3': return {'B3 reflection e1': reflmap((K(1), K(0), K(0)))}
    if g.name == 'A4': return {'point reflection -I': lambda x: tuple(-a for a in x)}
    if g.name == 'F4':
        R = g.gd['R']; s = g.gd['aut'][0]; W = g.gd['W']
        def Ls(x):   # alpha_i -> alpha_s(i): x = sum y_i w_i with y_i = <x, alpha_i>; L x = sum y_i w_s(i)
            y = [GR.dot(x, R[i]) for i in range(4)]
            return tuple(sum((y[i]*W[s[i]][m] for i in range(4)), K(0)) for m in range(4))
        return {'F4 diagram reversal (isometry)': Ls}
    return {}

def extra_symmetry(g, p):
    maps = extra_isometries(g); out = {}
    if not maps: return out
    r = g.r; W = g.gd['W']; R = g.gd['R']; c = cvec(p)
    v = [sum((c[i]*E.const(W[i][m]) for i in range(r)), E.const(0)) for m in range(g.n)]
    # apply the isometry to v (linear): evaluate on the basis w_i
    for nm, f in maps.items():
        fw = [f(W[i]) for i in range(r)]
        w = [sum((c[i]*E.const(fw[i][m]) for i in range(r)), E.const(0)) for m in range(g.n)]
        y = [sum((w[m]*E.const(R[i][m]) for m in range(g.n)), E.const(0)) for i in range(r)]   # omega coords of w
        sols = set(); whole = False
        for gel in g.els:
            diff = [sum((y[i]*E.const(gel[i][m]) for i in range(r)), E.const(0)) - v[m] for m in range(g.n)]
            if all(d.iszero() for d in diff): whole = True; break
            # each coordinate a + b t (a, b in K): common positive root
            cand = None; ok = True
            for d in diff:
                if d.iszero(): continue
                co = d.coeffs_k() + [K(0)]*2
                a, b = co[0], co[1]
                if b.iszero(): ok = False; break
                tt = -(a/b)
                if cand is None: cand = tt
                elif cand != tt: ok = False; break
            if ok and cand is not None and cand.sign() > 0: sols.add(repr(cand))
        out[nm] = 'whole family' if whole else sorted(sols)
    return out

# ---------- main ----------
def analyse_family(g, fam, kmax, do_iq):
    p = fam['p']; res = {'pattern': ''.join('0' if x == 0 else ('1' if x == 1 else 't') for x in p), 'raw_patterns': fam['raw_patterns'],
                         'involution': 't -> 1/t via automorphism ' + str(fam['inv'][0]) if fam['inv'] else None,
                         'pointwise_symmetric': [list(s) for s in fam['sym']]}
    t0 = time.time()
    tones, nrm, ntrip = tone_polys(g, p, kmax)
    res['distinct_pair_forms'] = ntrip
    V, A, L, Gc = volume_area(g, p)
    res['vol_poly_deg'] = V.degree()
    # Mahler critical points: (V/L)' = 0
    mnum = V.deriv()*L - V*L.deriv()
    crossings = []
    res['tones'] = {}
    for k, td in tones.items():
        N = td['N']
        if N.iszero(): res['tones'][k] = 'identically zero'; continue
        rts = positive_roots(N)
        res['tones'][k] = [{kk_: v for kk_, v in r_.items() if kk_ != 'x'} for r_ in rts]
        for r_ in rts: crossings.append(('tone%d' % k, r_))
    if mnum.iszero(): res['mahler'] = 'constant'
    else:
        rts = positive_roots(mnum); res['mahler_critical'] = [{a: b for a, b in r_.items() if a != 'x'} for r_ in rts]
        for r_ in rts: crossings.append(('mahler', r_))
    if do_iq:
        try:
            st, rts = iq_critical(g, V, A)
            res['iq_critical'] = st if st != 'ok' else [{a: b for a, b in r_.items() if a != 'x'} for r_ in rts]
            if st == 'ok':
                for r_ in rts: crossings.append(('iq', r_))
        except Exception as ex:
            res['iq_critical'] = f'error {ex!r}'
    if g.d == 3:
        cl = dehn_family(g, p, A)
        import dehn as DH
        if g.name in ('A3', 'B3'):
            Xq = Fr(0); Yq = Fr(0); allproved = True
            for c_ in cl:
                a2 = c_['cos2_exact']
                dec = DH.beta_decompose(c_['theta'], (str(a2.a), str(a2.b)), c_['cos_sign'], g.gd['D'])
                assert dec is not None, ('angle not in span(pi, beta)', res['pattern'], c_['theta_deg'])
                pq, q, pr = dec; allproved &= pr; c_['angle'] = f'{pq}*pi + {q}*beta'
                if c_['len'] == 'one': Xq += 2*c_['count']*q
                else: Yq += 2*c_['count']*q
            res['dehn'] = {'X_beta': str(Xq), 'Y_beta': str(Yq), 'form': f'1 (x) {Xq} beta + t (x) {Yq} beta', 'angles_proved': allproved}
            if Xq == 0 and Yq == 0: z = 'whole family'
            elif Yq == 0: z = 'none'
            else:
                ts = -Xq/Yq; z = str(ts) if ts > 0 else 'none'
            res['dehn']['zero_at'] = z; res['dehn']['at_t_1_beta'] = str(Xq + Yq)
            check(allproved, f'{g.name} {res["pattern"]}: every dihedral angle proved of the form p pi + q beta')
        else:
            thetas = [c_['theta'] for c_ in cl]
            nb, co = DH.pslq_basis(thetas)
            Xv = [Fr(0)]*nb; Yv = [Fr(0)]*nb
            for c_, v in zip(cl, co):
                for i in range(nb):
                    if c_['len'] == 'one': Xv[i] += 2*c_['count']*v[i]
                    else: Yv[i] += 2*c_['count']*v[i]
            if all(x == 0 for x in Xv + Yv): z = 'whole family'
            elif all(y == 0 for y in Yv): z = 'none'
            else:
                i0 = next(i for i in range(nb) if Yv[i] != 0); ts = -Xv[i0]/Yv[i0]
                z = str(ts) if ts > 0 and all(Xv[i] + ts*Yv[i] == 0 for i in range(nb)) else 'none'
            res['dehn'] = {'basis_size': nb, 'X': [str(x) for x in Xv], 'Y': [str(y) for y in Yv], 'zero_at': z,
                           'strength': 'relations by PSLQ (80 digits); completeness of the relation lattice not proved'}
        res['dehn_classes'] = [{a: b for a, b in c_.items() if a not in ('theta', 'cos2_exact')} for c_ in cl]
        res['_thetas'] = [(c_['len'], c_['count'], c_['theta']) for c_ in cl]
    # f0 (corners) and f_{d-1} (facets): self-duality within the family needs f0 = f_{d-1}
    def orbit_size(y):
        return len({tuple(sum((y[i]*gel[i][m] for i in range(g.r)), K(0)).key() for m in range(g.n)) for gel in g.els})
    c1 = [K(0) if x_ == 0 else K(1) for x_ in p]
    f0 = orbit_size(c1)
    fd = sum(orbit_size([K(1) if i == j else K(0) for i in range(g.r)]) for j in range(g.r) if not A[j].iszero())
    res['f0'] = f0; res['facets'] = fd; res['self_dual_possible'] = (f0 == fd)
    # extra symmetry along the family: t > 0 where an isometry outside G maps the corner set to itself
    res['extra_symmetry'] = extra_symmetry(g, p)
    if g.name in ('A3', 'A4', 'F4'):
        es = list(res['extra_symmetry'].values())[0]
        st = tuple(0 if x == 0 else 1 for x in p); auts = [tuple(s) for s in g.gd['aut']]
        expect = 'whole family' if fam['sym'] else (['1'] if any(act(s, st) == st for s in auts) else [])
        check(es == expect, f'{g.name} {res["pattern"]}: extra symmetry exactly where the seed is automorphism-fixed ({es} vs {expect})')
    # values at the uniform member t = 1 (every family)
    one = fmpq(1)
    res['at_t_1'] = {'tones': {k: (float(td['N'].ev(one) / kpow(nrm.ev(one), k)) / float(kk(K(td['den'][0]))) if not td['N'].iszero() else 0.0) for k, td in tones.items()},
                     'tone_zero_exact': [k for k, td in tones.items() if not td['N'].iszero() and td['N'].ev(one).iszero()]}
    # similarity test: T_k(t) == T_k(1/t) for every k  <=>  P(1/t) similar to P(t) (needed for an involution t -> 1/t)
    def rev(e, deg):
        def rv(P):
            co = list(P.coeffs()) + [fmpq(0)]*(deg + 1 - len(list(P.coeffs())))
            return fmpq_poly(list(reversed(co)))
        return E(rv(e.A), rv(e.B))
    simil = True; diffk = None
    for k, td in tones.items():
        N = td['N']
        if N.iszero(): continue
        lhs = N*(rev(nrm, 2)**k); rhs = rev(N, 2*k)*(nrm**k)
        if not (lhs - rhs).iszero(): simil = False; diffk = k; break
    res['tones_even_under_t_to_1/t'] = simil
    check(simil == bool(fam['inv']), f'{g.name} {res["pattern"]}: tone test says P(1/t) {"~" if simil else "not ~"} P(t) (first differing degree {diffk}); involution from the diagram: {bool(fam["inv"])}')
    # fixed point analysis
    if fam['inv']:
        one = fmpq(1); fp = {}
        for k, td in tones.items():
            N = td['N']
            if N.iszero(): continue
            val = N.ev(one) / kpow(nrm.ev(one), k)
            dnum = (N.deriv()*nrm - E.const(k)*N*nrm.deriv()).ev(one)
            hk = nrm**k; d2 = (N.deriv().deriv()*hk - N*hk.deriv().deriv()).ev(one)
            fp['tone%d' % k] = {'value_times_|G|P_k(1)': repr(val), 'value': float(val)/float(kk(K(td['den'][0]))), 'zero_at_fixed_point': val.iszero(),
                                'derivative_zero': dnum.iszero(), 'second_derivative_sign': d2.sign() if not val.iszero() else 0}
            check(dnum.iszero(), f'{g.name} {res["pattern"]}: tone {k} critical at the fixed point t = 1 (evenness)')
        md = mnum.ev(one); fp['mahler_derivative_zero'] = md.iszero()
        m2 = (V.deriv().deriv()*L - V*L.deriv().deriv()).ev(one)   # sign of M'' at a critical point
        fp['mahler_second_derivative_sign'] = m2.sign()
        check(md.iszero(), f'{g.name} {res["pattern"]}: Mahler product critical at t = 1')
        # second derivative of log M at 1 (sign): numeric via arb at t = 1 +- h
        res['fixed_point'] = fp
    res['_crossings'] = crossings
    res['seconds'] = round(time.time() - t0, 1)
    return res

def coincidences(res):
    cr = res['_crossings']; out = []
    for i in range(len(cr)):
        a, ra = cr[i]
        flags = []
        if ra['deg'] == 1: flags.append('rational ' + ra['value'])
        if ra['deg'] == 1 and abs(float(ra['x'].mid()) - 1) < 1e-20: flags.append('AT t = 1')
        if ra['deg'] == 2:
            c = [fmpq(x) for x in ra['minpoly']]; disc = c[1]*c[1] - 4*c[0]*c[2]
            flags.append(f'quadratic, discriminant {disc}')
        for j in range(i + 1, len(cr)):
            b, rb = cr[j]
            if X.same_algebraic(ra, rb) and a != b: out.append({'what': f'{a} and {b} vanish/critical at the same point', 'value': ra['value'], 'minpoly': ra['minpoly']})
        if flags: out.append({'what': f'{a} at a special number', 'flags': flags, 'value': ra['value']})
    return out

def worker(args):
    name, fi, kmax, do_iq = args
    CHECKS[0] = 0; FAILS.clear()
    g = G_GLOBAL; fam = FAMS[fi]
    r = analyse_family(g, fam, kmax, do_iq)
    r['coincidences'] = coincidences(r)
    r['_crossings'] = [(a, {k: v for k, v in b.items() if k != 'x'}) for a, b in r['_crossings']]
    th = r.pop('_thetas', None)
    if th is not None: r['_thetas'] = [(a, b, str(c)) for a, b, c in th]
    return fi, r, CHECKS[0], list(FAILS)

if __name__ == '__main__':
    name = sys.argv[1]; workers = int(sys.argv[2]) if len(sys.argv) > 2 else 1; pilot = '--pilot' in sys.argv
    kmax = int(os.environ.get('KMAX', '12')); do_iq = os.environ.get('IQ', '1') == '1'
    t0 = time.time()
    G_GLOBAL = Grp(name); FAMS = families(G_GLOBAL.gd); ST = stations(G_GLOBAL.gd)
    if pilot: FAMS = FAMS[:int(os.environ.get('PILOT_N', '3'))]
    print(f'{name}: {len(FAMS)} families (raw patterns {sum(f["raw_patterns"] for f in FAMS)}), {len(ST)} stations; kmax {kmax}; IQ {do_iq}', flush=True)
    results = [None]*len(FAMS); allfails = []; nchk = 0
    import multiprocessing as mpc
    ctxm = mpc.get_context('fork')
    tasks = [(name, i, kmax, do_iq) for i in range(len(FAMS))]
    done = 0
    if workers > 1:
        with ctxm.Pool(workers) as pool:
            for fi, r, nc, fl in pool.imap_unordered(worker, tasks):
                results[fi] = r; nchk += nc; allfails += fl; done += 1
                print(f'PROGRESS {done/len(FAMS):.3f} {name} family {r["pattern"]} ({r["seconds"]} s)', flush=True)
    else:
        for tk in tasks:
            CHECKS[0] = 0; FAILS.clear()
            fi, r, nc, fl = worker(tk); results[fi] = r; nchk += nc; allfails += list(fl); done += 1
            print(f'PROGRESS {done/len(FAMS):.3f} {name} family {r["pattern"]} ({r["seconds"]} s)', flush=True)
    out = {'group': name, 'order': G_GLOBAL.gd['order'], 'field_D': G_GLOBAL.gd['D'], 'kmax': kmax, 'families': results,
           'stations': [{'pattern': ''.join(map(str, s['p'])), 'symmetric_under': [list(x) for x in s['sym']]} for s in ST],
           'checks': nchk, 'fails': allfails, 'seconds': round(time.time() - t0, 1)}
    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', f'census-{name}{"-pilot" if pilot else ""}.json')
    json.dump(out, open(fn, 'w'), indent=1, default=str)
    print(f'{name}: {nchk} checks, {len(allfails)} FAIL, {out["seconds"]} s', flush=True)
    print('FINAL ok' if not allfails else 'FINAL FAIL', flush=True)
