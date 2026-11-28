"""EXACT certificate for DICTO's Hollow-straw transformation, any core and fair die (28 Nov 2026; DICTO: "parallel testing" of
the next Scutoid-Frusta bridging solids). With Claude (Anthropic). Generalises 2026-11-24-aequi-vacuus-scutoids/scripts/
c116_transform_exact.py (the C116 -> Minana #377 certificate) to the core/die/pairing of hs_general.py (floating resin, same seed).
Inputs made exact: the die's planes in Q(sqrt5) with its 15-digit fair-depth stand-ins; the core's planes, turned by the floating
resin and scaled to core size RHO, rounded to rationals (denominator <= 1e9). Certificate (A)-(C) as for C116; (D): the pattern
changes are exactly the needed neighbour changes (to gain: die pairs the core lacks; to lose: core pairs the die lacks), one swap each.
Usage: CORE=GPc_1_1 DIE=90 RHO=0.7 python hs_exact.py. FINAL ok iff (A)-(D) hold."""
import os, sys, json, time
import numpy as np
from scipy.optimize import linear_sum_assignment
from scipy.spatial import HalfspaceIntersection
from scipy.spatial.transform import Rotation
HERE = os.path.dirname(os.path.abspath(__file__)); ST = os.path.join(HERE, '../..')
argv = list(sys.argv); sys.argv = sys.argv[:1]
sys.path.insert(0, os.path.join(ST, '2026-11-24-aequi-vacuus-scutoids/scripts'))
import amber_aequus as A
sys.argv = argv
def pr(*a): print(*a, flush=True)
CORE = os.environ.get('CORE', 'GPc_1_1'); DIE = int(os.environ.get('DIE', '90'))
RHO = float(os.environ.get('RHO', '0.7')); NG = int(os.environ.get('NG', 300)); NST = int(os.environ.get('NST', 200))
def core_planes(name):
    if name == 'C116':
        d = json.load(open(os.path.join(ST, '2026-11-24-aequi-vacuus-scutoids/data/c116/pairing.json'))); P = np.array(d['P']); out = []
        for f in d['faces']:
            X = P[f]; c0 = X.mean(0); n = np.linalg.svd(X - c0)[2][2]; n = n if n @ c0 > 0 else -n; out.append(n / (n @ c0))
        return np.array(out)
    import importlib.util
    g = os.path.join(ST, '2026-11-21-amber-goldberg/scripts')
    old = sys.modules.pop('resin', None)                    # the Goldberg study has its own resin.py (60-digit reals)
    spec_r = importlib.util.spec_from_file_location('resin', os.path.join(g, 'resin.py')); Rm = importlib.util.module_from_spec(spec_r)
    sys.modules['resin'] = Rm; spec_r.loader.exec_module(Rm)
    spec = importlib.util.spec_from_file_location('gsolids', os.path.join(g, 'solids.py')); S = importlib.util.module_from_spec(spec); spec.loader.exec_module(S)
    if old is not None: sys.modules['resin'] = old
    m, n = map(int, name.split('_')[1:3]); pts, ico, T = S.geodesic(m, n)
    if name.startswith('GPc_'): pts = S.canonical(pts, m, n)
    return np.array([[float(x) for x in p] for p in pts])
def poly(Aa):
    P = HalfspaceIntersection(np.hstack([Aa, -np.ones((len(Aa), 1))]), np.zeros(3)).intersections
    sc = np.abs(P).max(); pts = []
    for p in P:
        if not any(np.linalg.norm(p - q) < 1e-9 * sc for q in pts): pts.append(p)
    P = np.array(pts); tight = np.abs(Aa @ P.T - 1) < 1e-8
    faces = [set(np.where(tight[k])[0]) for k in range(len(Aa))]
    pairs = {(k, l) for k in range(len(Aa)) for l in range(k + 1, len(Aa)) if len(faces[k] & faces[l]) >= 2}
    return P, faces, pairs
def float_resin(Nc, Nd, rng):
    best = None
    for s in range(NST):
        R = Rotation.random(random_state=rng).as_matrix()
        if s % 2: R = -R                                   # mirror allowed
        for it in range(40):
            C = (Nc @ R.T) @ Nd.T; r, c = linear_sum_assignment(-C); sig = c
            H = Nc.T @ Nd[sig]; U, _, Vt = np.linalg.svd(H); R2 = (U @ Vt).T
            if np.allclose(R2, R, atol=1e-12): break
            R = R2
        tot = float(((Nc @ R.T) * Nd[sig]).sum(1).sum())
        if best is None or tot > best[0] + 1e-9: best = (tot, R, sig.copy())
    return best

import itertools
from fractions import Fraction as Fr
import sympy as sp
from resin import Q
t0 = time.time()
Ac = core_planes(CORE); Nc = Ac / np.linalg.norm(Ac, axis=1)[:, None]
Pc, Fc, Ec = poly(Ac); rc = np.linalg.norm(Pc, axis=1).max(); NF = len(Ac)
S = A.build(f'aequus-{DIE}')
Md = np.array([[float(x) for x in u] for u, c in S['planes']]) / np.array([float(c) for u, c in S['planes']])[:, None]
assert len(Md) == NF, 'face counts differ'
Nd = Md / np.linalg.norm(Md, axis=1)[:, None]; Pd, Fd, Ed = poly(Md); rin = (1 / np.linalg.norm(Md, axis=1)).min()
tot, R, sig = float_resin(Nc, Nd, np.random.default_rng(DIE))
inv = {int(v): k for k, v in enumerate(sig)}
Ed_c = {tuple(sorted((inv[a], inv[b]))) for a, b in Ed}
SWAP = os.environ.get('SWAP') == '1'   # DICTO 28 Nov: the reverse, the fair die as the inner core growing into the core solid
if not SWAP:
    need_set = set(Ed_c - Ec); lose_set = set(Ec - Ed_c)
    scale = rc / (RHO * rin)
    a0 = (Ac @ R.T) * scale
    AK = [[Q(Fr(float(x)).limit_denominator(10 ** 9)) for x in a] for a in a0]
    M = [[x / c for x in u] for u, c in S['planes']]
    Mk = [M[sig[k]] for k in range(NF)]
else:
    # inner: the die turned back by R^T (so its faces meet the core's in the forward pairing), scaled so its
    # circumradius is RHO times the core's inradius; outer: the core solid itself. Plane k = die face sig[k] -> core face k.
    rd = np.linalg.norm(Pd, axis=1).max(); rin_c = (1 / np.linalg.norm(Ac, axis=1)).min()
    a0 = (Md @ R) * (rd / (RHO * rin_c))
    AK = [[Q(Fr(float(x)).limit_denominator(10 ** 9)) for x in a0[sig[k]]] for k in range(NF)]
    Mk = [[Q(Fr(float(x)).limit_denominator(10 ** 9)) for x in Ac[k]] for k in range(NF)]
    Ec, Ed_c = Ed_c, Ec                    # start pattern: the die's; end pattern: the core's
    need_set = set(Ed_c - Ec); lose_set = set(Ec - Ed_c)
    scale = rd / (RHO * rin_c)
Dk = [[Mk[k][i] - AK[k][i] for i in range(3)] for k in range(NF)]
pr(f'{"REVERSE: die " + str(DIE) + " -> core " + CORE if SWAP else "core " + CORE + " -> die " + str(DIE)} ({NF} faces), inner size {RHO}: kept {len(Ec & Ed_c)}, to gain {len(need_set)}, to lose {len(lose_set)}')
# ---- polynomials in lam with Q(sqrt5) coefficients: list of Q, low degree first
def padd(p, q): n = max(len(p), len(q)); return [(p[i] if i < len(p) else Q(0)) + (q[i] if i < len(q) else Q(0)) for i in range(n)]
def pneg(p): return [-c for c in p]
def pmul(p, q):
    out = [Q(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q): out[i + j] = out[i + j] + a * b
    return out
def peval(p, lam):
    v = Q(0)
    for c in reversed(p): v = v * Q(lam) + c
    return v
row = lambda k: [[AK[k][i], Dk[k][i]] for i in range(3)]          # a_k(lam) as 3 linear polys
def vcross(u, v): return [padd(pmul(u[1], v[2]), pneg(pmul(u[2], v[1]))), padd(pmul(u[2], v[0]), pneg(pmul(u[0], v[2]))), padd(pmul(u[0], v[1]), pneg(pmul(u[1], v[0])))]
def vdot(u, v): return padd(padd(pmul(u[0], v[0]), pmul(u[1], v[1])), pmul(u[2], v[2]))
lam = sp.Symbol('lam')
def norm_poly(p):    # A^2 - 5 B^2 for p = A + B sqrt5, as a sympy Poly over QQ
    Apol = sp.Poly([sp.Rational(c.a.numerator, c.a.denominator) for c in reversed(p)], lam, domain='QQ')
    Bpol = sp.Poly([sp.Rational(c.b.numerator, c.b.denominator) for c in reversed(p)], lam, domain='QQ')
    return Apol ** 2 - 5 * Bpol ** 2
def roots_in(p, lo, hi):
    """exact sign-change roots of p in the open interval (lo, hi): list of isolating rational intervals (a, b) with sign(p(a)) != sign(p(b))"""
    N = norm_poly(p)
    if N.is_zero: raise ValueError('identically zero polynomial')
    if N.count_roots(sp.Rational(lo.numerator, lo.denominator), sp.Rational(hi.numerator, hi.denominator)) == 0: return []
    out = []
    for (a, b), m in N.intervals(inf=sp.Rational(lo.numerator, lo.denominator), sup=sp.Rational(hi.numerator, hi.denominator)):
        a, b = Fr(int(sp.numer(a)), int(sp.denom(a))), Fr(int(sp.numer(b)), int(sp.denom(b)))
        if a == b:            # rational root of the norm: is it a root of p?
            if peval(p, a).sign() == 0 and lo < a < hi: out.append((a, a))
            continue
        sa, sb = peval(p, a).sign(), peval(p, b).sign()
        if sa != sb and lo < b and a < hi: out.append((max(a, lo), min(b, hi)))
    return out
def refine(p, a, b, w):
    while b - a > w:
        m = (a + b) / 2; sm = peval(p, m).sign()
        if sm == 0: return m, m
        if sm == peval(p, a).sign(): a = m
        else: b = m
    return a, b
# ---- exact state at rational lam: corners (sets of 3 planes) verified exactly
def planes_at(l): return [[AK[k][i] + Dk[k][i] * Q(l) for i in range(3)] for k in range(NF)]
def state(l, guess=None):
    Af = np.array([[float(AK[k][i]) + float(Dk[k][i]) * float(l) for i in range(3)] for k in range(NF)])
    P = HalfspaceIntersection(np.hstack([Af, -np.ones((NF, 1))]), np.zeros(3)).intersections
    labs = set()
    for p in ([] if guess is not None else P):
        t = np.argsort(np.abs(Af @ p - 1))[:3]; labs.add(frozenset(int(i) for i in t))
    if guess is not None: labs = set(guess)   # combinatorial flip from the previous state, verified exactly below
    PL = planes_at(l); ok = True
    from resin import det3
    for L in labs:
        k, a, b = sorted(L); dd = det3(PL[k], PL[a], PL[b])
        if dd.sign() == 0: ok = False; continue
        # x = (r_a x r_b + r_b x r_k + r_k x r_a) / det
        def cr(u, v): return [u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
        Nn = [x + y + z for x, y, z in zip(cr(PL[a], PL[b]), cr(PL[b], PL[k]), cr(PL[k], PL[a]))]
        for c in range(NF):
            if c in L: continue
            if ((sum((PL[c][i] * Nn[i] for i in range(3)), Q(0)) - dd) * Q(dd.sign())).sign() >= 0: ok = False
    # closed sphere: faces as cycles, Euler
    E = {}
    for L1, L2 in itertools.combinations(labs, 2):
        if len(L1 & L2) == 2: E.setdefault(frozenset(L1 & L2), []).append((L1, L2))
    deg = {L: 0 for L in labs}
    for e, lst in E.items():
        for L1, L2 in lst: deg[L1] += 1; deg[L2] += 1
    ok &= all(len(lst) == 1 for lst in E.values()) and all(d == 3 for d in deg.values())
    faces_present = {k for L in labs for k in L}
    ok &= len(faces_present) == NF and len(labs) - len(E) + NF == 2
    pairs = {tuple(sorted(e)) for e in E}
    return labs, pairs, ok
def pairs_of(fl):
    at = {}
    for k, F in enumerate(fl):
        for v in F: at.setdefault(v, set()).add(k)
    return {(a, b) for S_ in at.values() for a in S_ for b in S_ if a < b}
want0 = set(Ec); want1 = set(Ed_c)
# ---- corner polynomials
cache = {}
def corner_polys(L):
    if L in cache: return cache[L]
    k, a, b = sorted(L); rk, ra, rb = row(k), row(a), row(b)
    Nv = [padd(padd(x, y), z) for x, y, z in zip(vcross(ra, rb), vcross(rb, rk), vcross(rk, ra))]
    det = vdot(rk, vcross(ra, rb)); cache[L] = (Nv, det); return Nv, det
lam0 = Fr(0); labs, pairs, ok0 = state(lam0)
pr('(A) lam = 0: corners', len(labs), 'exact and closed:', ok0, '; pattern = the core under the pairing:', pairs == want0)
okA = ok0 and pairs == want0
born = {L: lam0 for L in labs}; events = []; okC = True; okdet = True; step = 0
while True:
    step += 1
    # earliest event after lam0: roots of f_c for every corner and plane, grouped by the 4-plane set
    cands = []
    for L in labs:
        Nv, det = corner_polys(L)
        if roots_in(det, lam0, Fr(1)): okdet = False
        for c in range(NF):
            if c in L: continue
            f = padd(vdot(row(c), Nv), pneg(det))
            for a_, b_ in roots_in(f, lam0, Fr(1)): cands.append((a_, b_, frozenset(L | {c}), f))
    if not cands:
        lam1 = Fr(1); break
    # refine until the earliest group is separated from all others
    w = Fr(1, 10 ** 6)
    while True:
        cands = [(*refine(f, a_, b_, w), F4, f) for a_, b_, F4, f in cands]
        first = min(cands, key=lambda z: z[1]); grp = {z[2] for z in cands if z[0] <= first[1]}
        if len(grp) == 1: break
        w /= 1000
        if w < Fr(1, 10 ** 40): pr('  two different four-plane sets meet at the same lam (to 1e-40):', [sorted(g) for g in grp]); break
    F4 = first[2]; hi = max(z[1] for z in cands if z[2] == F4)
    nxt = min((z[0] for z in cands if z[2] != F4), default=Fr(1))
    lam1 = (hi + nxt) / 2 if nxt < 1 else (hi + 1) / 2
    present = {L for L in labs if L <= F4}
    guess = (labs - present) | ({frozenset(T) for T in itertools.combinations(sorted(F4), 3)} - present)
    labs1, pairs1, ok1 = state(lam1, guess)
    lost, gained = sorted(pairs - pairs1), sorted(pairs1 - pairs)
    sw = len(lost) == 1 and len(gained) == 1 and tuple(gained[0]) in need_set and tuple(lost[0]) in lose_set and set(lost[0]) | set(gained[0]) == set(F4)
    events.append(dict(lam_lo=str(first[0]), lam_hi=str(hi), lam=float(hi), planes=sorted(F4), lost=lost, gained=gained, one_floor_swap=sw, state_ok=ok1))
    pr(f'  event {len(events)}: lam in [{float(first[0]):.12f}, {float(hi):.12f}] planes {sorted(F4)} lost {lost} gained {gained} '
       f'floor swap {sw}; state after exact and closed: {ok1}  ({time.time() - t0:.0f} s)')
    # (C) nesting on the lifetimes of the corners that die here
    for L in labs - labs1:
        Nv, det = corner_polys(L); sdet = peval(det, (born[L] + first[0]) / 2).sign()
        for p in L:
            g = vdot([[Dk[p][i]] for i in range(3)], Nv)
            if roots_in(g, born[L], hi) or (peval(g, (born[L] + first[0]) / 2) * Q(sdet)).sign() >= 0: okC = False; pr('  NOT growing: corner', sorted(L), 'plane', p)
    for L in labs1 - labs: born[L] = hi
    labs, pairs, lam0 = labs1, pairs1, lam1
    if step > max(60, 3 * len(need_set) + 20): pr('too many events'); break
labsE, pairsE, okE = state(Fr(1))
for L in labsE:        # nesting on the lifetimes of the corners alive at the end
    Nv, det = corner_polys(L); sdet = peval(det, (born[L] + 1) / 2).sign()
    for p in L:
        g = vdot([[Dk[p][i]] for i in range(3)], Nv)
        if roots_in(g, born[L], Fr(1)) or (peval(g, (born[L] + 1) / 2) * Q(sdet)).sign() >= 0: okC = False; pr('  NOT growing: corner', sorted(L), 'plane', p)
okAend = okE and pairsE == want1
pr('(A) lam = 1: corners', len(labsE), 'exact and closed:', okE, '; pattern = the die under the pairing:', pairsE == want1)
pr('(B) events:', len(events), '; every state between events exact and closed:', all(e['state_ok'] for e in events), '; no corner degenerates (det):', okdet)
pr('(C) nested (every plane moves outward at every corner over its whole life):', okC)
okD = (len(events) == len(need_set) and all(e['one_floor_swap'] for e in events)
       and {tuple(e['gained'][0]) for e in events} == need_set and {tuple(e['lost'][0]) for e in events} == lose_set)
pr(f'(D) exactly the {len(need_set)} needed neighbour changes, one swap per event:', okD)
json.dump(dict(core=CORE, die=DIE, rho=RHO, scale=str(scale), sigma=[int(x) for x in sig], events=events, A=[okA, okAend], C=okC, D=okD, det=okdet),
          open(os.path.join(HERE, f'../data/exact_{"rev_" if SWAP else ""}{CORE}_{DIE}_rho{RHO}.json'), 'w'))
good = okA and okAend and okC and okD and okdet and all(e['state_ok'] for e in events)
pr('RESULT:', (f"DICTO's Hollow-straw transformation die {DIE} -> {CORE} (reverse) is EXACT (both solids' planes rounded to 1e-9)" if SWAP else f"DICTO's Hollow-straw transformation {CORE} -> die {DIE} is EXACT (core planes rounded to 1e-9; die with its 15-digit depth stand-ins)") if good else 'NOT certified: see above')
pr('FINAL ok' if good else 'FINAL FAIL')
