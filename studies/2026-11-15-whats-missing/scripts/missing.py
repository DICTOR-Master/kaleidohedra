#!/usr/bin/env python3
"""What's missing (15 Nov 2026; DICTO approved 15 Nov): hidden swaps behind the 17 laws with no swap, known involutions not yet used
(Schuetzenberger evacuation, the longest element w0, Gale and Alexander duality, chirality), and the periodic points of the hops.

A finding QUALIFIES only if a law is FORCED at a fixed point of a GEOMETRIC involution (parity, symmetry + concavity, extra symmetry),
proved exactly, with the controls passing (sqrt3 on the cube-octahedron line, Kelvin at 3/2) and a random point failing.

Exact arithmetic decides every check: Python Fractions for the rational polytopes (slices of permutohedra, simplices), sympy for
radicals (sqrt2, sqrt3, sqrt5) and DomainMatrix over Q(sqrt d) for ranks. Floats only order corners round a face.
Reused code, executed from its files, not retyped:
  studies/2026-11-14-forced-fixed-points/scripts/forced.py : its header (reused-code block: polytope engine of the swaps study,
      exact Dehn of the chat-handoff study, harmonic_invariants) and its CONTROL section, run unchanged
  studies/2026-11-13-platonic-fans-law/scripts/fans_law.py : recog_solid() (exact recognition of registry corners)
Referee fixes (15 Nov, REFEREE-fable.md): facets counted once in rat_measure (all P5/P6 slice volumes recomputed, concavity of
volume^(1/k) checked exactly); statements proved by argument are printed as 'arg' and are not counted as checks; Gale stability and
cube-type restriction checked; #91 uniform member and tone; #100 one angle unit; odd plain hunts; Reverse Bob Minimus from the CCCBR extract.
Usage: missing.py [--pilot] [--workers N]. Output: PROGRESS lines, ok/FAIL/FIND lines, data/missing(-pilot).json, last line FINAL ok|FAIL.
"""
import sys, os, json, time, itertools, math, random
from fractions import Fraction as Fr
from multiprocessing import Pool
import numpy as np
import sympy as sp

here = os.path.dirname(os.path.abspath(__file__)); STUD = os.path.join(here, '..', '..')
PILOT = '--pilot' in sys.argv
WORKERS = int(sys.argv[sys.argv.index('--workers') + 1]) if '--workers' in sys.argv else 4
DATA = os.path.join(here, '..', 'data'); os.makedirs(DATA, exist_ok=True)
T0 = time.time(); T_START = T0

# ---------------- reused: forced.py header (helpers) ----------------
_f = open(os.path.join(STUD, '2026-11-14-forced-fixed-points', 'scripts', 'forced.py')).read()
_argv = sys.argv; sys.argv = sys.argv[:1]
exec(_f[_f.index('# ---------------- reused code'):_f.index('# C. CONTROLS')], globals())
sys.argv = _argv
NSTEP = 12
x, y, z = sp.symbols('x y z')
phi = (1 + sp.sqrt(5)) / 2
s5 = sp.sqrt(5)

# =====================================================================================================================
# 0. CONTROLS: forced.py's control section, run unchanged (sqrt3 qualifies, 3/2 qualifies, 8/5 fails)
# =====================================================================================================================
exec(_f[_f.index("progress(0, 'controls"):_f.index('# A. THE SILENT')], globals())

# ---------------- exact rational polytopes (dimension 2 or 3): A x <= b, Fractions ----------------
def rat_vertices(A, b, d):
    V = []
    m = len(A)
    for idx in itertools.combinations(range(m), d):
        M = [list(A[i]) for i in idx]; r = [b[i] for i in idx]
        # Gaussian elimination in Fractions
        M = [row[:] + [rr] for row, rr in zip(M, r)]
        ok = True
        for c in range(d):
            p = next((k for k in range(c, d) if M[k][c] != 0), None)
            if p is None: ok = False; break
            M[c], M[p] = M[p], M[c]
            for k in range(d):
                if k != c and M[k][c] != 0:
                    f = M[k][c] / M[c][c]; M[k] = [u - f * w for u, w in zip(M[k], M[c])]
        if not ok: continue
        v = tuple(M[k][d] / M[k][k] for k in range(d))
        if all(sum(A[i][j] * v[j] for j in range(d)) <= b[i] for i in range(m)): V.append(v)
    return sorted(set(V))

def rat_measure(A, b, d, info=None):
    """exact area (d = 2) or volume (d = 3). REFEREE FIX (15 Nov): perm_planes can list one plane twice (two subsets giving the same
    inequality on a slice); each facet is now counted ONCE, keyed by its exact vertex set (>= 3 corners of a supporting plane span a
    facet, so two rows with the same vertex set are the same facet). info (dict) receives rows, facets and duplicates skipped."""
    V = rat_vertices(A, b, d)
    if info is not None: info.update(rows=len(A), facets=0, duplicates=0)
    if len(V) <= d: return Fr(0), V
    if d == 2:
        cx = sum(float(v[0]) for v in V) / len(V); cy = sum(float(v[1]) for v in V) / len(V)
        P = sorted(V, key=lambda v: math.atan2(float(v[1]) - cy, float(v[0]) - cx))
        return abs(sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P)))) / 2, V
    vol = Fr(0); seen = set()
    for n, bb in zip(A, b):
        on = [v for v in V if sum(n[j] * v[j] for j in range(3)) == bb]
        if len(on) < 3: continue
        key = frozenset(on)
        if key in seen:
            if info is not None: info['duplicates'] += 1
            continue
        seen.add(key)
        if info is not None: info['facets'] += 1
        c = [sum(float(v[j]) for v in on) / len(on) for j in range(3)]
        nf = [float(t) for t in n]; u = [float(on[0][j]) - c[j] for j in range(3)]
        w = [nf[1] * u[2] - nf[2] * u[1], nf[2] * u[0] - nf[0] * u[2], nf[0] * u[1] - nf[1] * u[0]]
        def ang(v):
            dd = [float(v[j]) - c[j] for j in range(3)]
            return math.atan2(sum(dd[j] * w[j] for j in range(3)), sum(dd[j] * u[j] for j in range(3)))
        on.sort(key=ang)
        S = [Fr(0)] * 3
        for i in range(len(on)):
            p, q = on[i], on[(i + 1) % len(on)]
            S = [S[0] + p[1] * q[2] - p[2] * q[1], S[1] + p[2] * q[0] - p[0] * q[2], S[2] + p[0] * q[1] - p[1] * q[0]]
        nn = sum(t * t for t in n)
        vol += bb * abs(sum(n[j] * S[j] for j in range(3))) / (6 * nn)
    return vol, V

def perm_planes(n, param):
    """permutohedron of 1..n: sum_{i in S} x_i >= C(|S|+1, 2). param(t) -> list of (coeff vector over the free variables, constant) giving
    each x_i as affine form. Returns A, b with A u <= b."""
    A, b = [], []
    for k in range(1, n):
        for S in itertools.combinations(range(n), k):
            co = [Fr(0)] * len(param[0][0]); cst = Fr(0)
            for i in S:
                co = [c + e for c, e in zip(co, param[i][0])]; cst += param[i][1]
            # co.u + cst >= k(k+1)/2  ->  -co.u <= cst - k(k+1)/2
            A.append([-c for c in co]); b.append(cst - Fr(k * (k + 1), 2))
    return A, b

def slice_job(job):
    kind, w = job
    if kind == 'P6':
        w1, w2, w3 = w
        m = Fr(7, 2)
        E = [[Fr(1), 0, 0], [0, Fr(1), 0], [0, 0, Fr(1)], [0, 0, Fr(-1)], [0, Fr(-1), 0], [Fr(-1), 0, 0]]
        W = [w1, w2, w3, w3, w2, w1]
        param = [([Fr(t) for t in E[i]], m + W[i]) for i in range(6)]
        A, b = perm_planes(6, param); info = {}; vol, V = rat_measure(A, b, 3, info); return job, (vol, V, info)
    if kind == 'P5':
        t = w
        param = [([Fr(1), 0, 0], Fr(0)), ([0, Fr(1), 0], Fr(0)), ([0, 0, Fr(1)], Fr(0)), ([Fr(-1), Fr(-1), Fr(-1)], Fr(12) - t), ([0, 0, 0], Fr(3) + t)]
        A, b = perm_planes(5, param); info = {}; vol, V = rat_measure(A, b, 3, info); return job, (vol, V, info)
    raise ValueError(kind)

OUT['P1'] = {}; OUT['P2'] = {}; OUT['P3'] = {}
def tab(part, row, **kw): OUT[part][row] = kw
# REFEREE FIX (15 Nov): statements proved by argument, not computed, are no longer check(True, ...); they are listed apart as ARGUED
ARGUED = []
def argued(what):
    ARGUED.append(what); print('arg  ' + what, flush=True)
# exact concavity tests for Brunn-Minkowski: f^(1/k) concave at three equally spaced offsets (a, b, c) means 2 b^(1/k) >= a^(1/k) + c^(1/k)
def kth_root_bounds(q, k, digits=40):
    """rational lo <= q^(1/k) <= hi (q >= 0 rational), from an exact integer k-th root"""
    q = Fr(q); S = 10 ** digits; N = (q.numerator * S ** k) // q.denominator
    r = N
    if N > 1:   # integer Newton: floor of N^(1/k)
        r = 1 << ((N.bit_length() + k - 1) // k)
        while True:
            y = ((k - 1) * r + N // r ** (k - 1)) // k
            if y >= r: break
            r = y
    assert r ** k <= N < (r + 1) ** k
    return Fr(r, S), Fr(r + 1, S)
def concave_root(a_, b_, c_, k):
    """exact: 2 b^(1/k) > a^(1/k) + c^(1/k) (certified by rational bounds); k = 2 decided exactly by squaring"""
    a_, b_, c_ = Fr(a_), Fr(b_), Fr(c_)
    if k == 2: s = 4 * b_ - a_ - c_; return s > 0 and s * s > 4 * a_ * c_
    return 2 * kth_root_bounds(b_, k)[0] > kth_root_bounds(a_, k)[1] + kth_root_bounds(c_, k)[1]

# =====================================================================================================================
# PART 1. HIDDEN SWAPS BEHIND THE 17 LAWS WITH NO SWAP
# =====================================================================================================================
progress(1, 'P1: affine laws (#66/#67, #84) and the silent golden station (#94)')
hh, AA_, BB_, cc = sp.symbols('h A B c', real=True)
fa = AA_ + BB_ * hh
check(is0(sp.expand((fa.subs(hh, 1 - hh) - fa.subs(hh, R(1, 2))) + (fa - fa.subs(hh, R(1, 2))))),
      'P1 [#66/#67, #84] every affine law f = A + Bh: f - f(1/2) is ODD under the c<->h swap h -> 1 - h (tautology: true of every affine f)')
check(is0(fa.subs(hh, R(1, 2)) - (fa.subs(hh, 0) + fa.subs(hh, 1)) / 2),
      'P1 [#66/#67] at the fixed share 1/2 the law gives f(1/2) = (f(cc) + f(hh))/2: the Swap Rule itself, nothing new')
check(not is0(sp.diff(fa.subs(hh, cc / hh), hh, 2)) and is0(sp.diff(fa.subs(hh, cc / hh), hh, 2).subs(BB_, 0)),
      'P1 [#66/#67, #84] mu <-> c/mu: f(c/h) is affine in h only when B = 0 (no c keeps a non-constant affine law); likewise every non-affine Moebius map')
tab('P1', '#66/#67 Hexagonality Law', verdict='SWAP FOUND, NOT FORCED', swap='c<->h, h -> 1 - h (and word reversal)', fixed='h = 1/2 (the word chch)',
    reason='every affine law is odd about its own midpoint; at h = 1/2 it returns the Swap Rule mean; no c/mu, Moebius or Galois swap keeps an affine law except trivially')
tab('P1', '#84 Window Law', verdict='SWAP FOUND, NOT FORCED', swap='c<->h and word reversal (invariance)', fixed='palindromic and self-complementary windows: none for complement',
    reason='the law is linear in word shares; both swaps permute the shares; the only odd quantity, F(ch) - F(hc), is the mirror-hexagonality equality, an invariance')

# #94: Q4 on the first stretch of the cube-octahedron line: corners sperm(1, a, 0), a = mu - 1
a = sp.symbols('a', real=True)
H4 = harmonic_invariants(4)[0]
q4 = sp.expand(H4(1, a, 0))
check(is0(q4 - (a ** 4 - 3 * a ** 2 + 1)), 'P1 [#94] normalised H4(1, a, 0) = a^4 - 3a^2 + 1 (#94 Theorem A); zero on the stretch at a = 1/phi, mu = phi', q4)
Q4n = q4 / (1 + a ** 2) ** 2
vals = {'turn mu -> 3/mu: 3/phi': 3 / phi - 1, 'CsCl swap mu -> 3 - mu: 3 - phi': 2 - phi, 'mu -> 2/mu (maps [1,2] to itself): 2/phi': 2 / phi - 1,
        'B3 seed reversal (other stretch)': None}
for k, av in vals.items():
    if av is None: continue
    check(not is0(q4.subs(a, av)), f'P1 [#94] the image of the silent station under {k} is NOT silent (Q4 = {sp.nsimplify(sp.radsimp(q4.subs(a, av)))})')
# the reversal of the B3 seed (1-a, a, 0) -> (0, a, 1-a) leaves the stretch: corners (1, 1, b) with ... silent nowhere on the second stretch
b_ = sp.symbols('b', real=True)
q4b = sp.factor(sp.expand(H4(1, 1, b_)))
check(sp.Poly(sp.numer(sp.together(q4b)), b_).count_roots(0, 1) == 0, 'P1 [#94] the second stretch (corners sperm(1,1,b), 0 < b < 1, the image of the seed reversal) has no Q4 zero: the reversal does not carry the silence', q4b)
# Moebius involutions with Q4n o m = +-Q4n must permute the poles {i, -i} and the zeros {+-phi, +-1/phi}; fixing 1/phi:
mI = lambda t: -1 / t
check(not is0(mI(1 / phi) - 1 / phi), 'P1 [#94] the involution fixing +-i (a -> -1/a) moves 1/phi')
mM = lambda t: (2 - t) / (2 * t + 1)
check(is0(mM(1 / phi) - 1 / phi) and is0(mM(-phi) + phi) and is0(sp.expand(mM(sp.I) + sp.I)),
      'P1 [#94] the only involution fixing 1/phi and swapping i <-> -i is a -> (2 - a)/(2a + 1) (fixed points 1/phi, -phi)')
img = sp.radsimp(mM(phi))
check(not any(is0(img - r) for r in [phi, -phi, 1 / phi, -1 / phi]), f'P1 [#94] it sends phi to {img}, not a zero of Q4: NO Moebius involution preserving Q4 fixes the station')
check(is0(sp.expand(q4.subs(a, 1 / a) * a ** 4 - q4)) and is0(sp.simplify(Q4n.subs(a, 1 / a) - Q4n)),
      'P1 [#94] REFEREE (I): a -> 1/a preserves Q4 exactly (normalised) and is the identity on shapes (sperm(1, a, 0) ~ sperm(1, 1/a, 0); fixed point a = 1, the cuboctahedron): why every unit of norm +-1 is Galois-fixed up to similarity')
# Galois o similarity: sperm(1, a, 0) ~ sperm(1, 1/a, 0) and ~ sperm(1, -a, 0); sigma(1/phi) = -phi gives the same solid: norm -1
nrm = lambda e: sp.radsimp(sp.expand(e * e.subs(s5, -s5)))
check(is0(nrm(1 / phi) + 1) and is0(nrm(1 / phi ** 3) + 1),
      'P1 [#94] HIDDEN GALOIS SWAP: Icosaxes (a = 1/phi) is fixed by Galois conjugation up to similarity (a sigma(a) = -1); so is a = 1/phi^3')
check(not is0(q4.subs(a, 1 / phi ** 3)), f'P1 [#94] ... but a = 1/phi^3 (mu = 1 + 1/phi^3) is not silent: the Galois fixedness does not force Q4 = 0')
ev = [p for p in itertools.permutations(range(3)) if sum(1 for i in range(3) for j in range(i + 1, 3) if p[i] > p[j]) % 2 == 0]
half = set()
for p in ev:
    for sg in itertools.product((1, -1), repeat=2):
        v0 = (sg[0] * 1, sg[1] / phi, 0); half.add(tuple(sp.nsimplify(v0[p.index(i)]) for i in range(3)))
check(len(half) == 12 and is0(sp.radsimp(sum(H4(*v) for v in half))),
      'P1 [#94] the zero is forced by EXTRA SYMMETRY of the halves: the 12 even-permutation corners form a regular icosahedron, H4 sums to 0 on it (a 5-design: Delsarte-Goethals-Seidel 1977)')
tab('P1', '#94 Silent Golden Station', verdict='NONE (swap of the line); forced by extra symmetry instead', swap='turn, CsCl swap, mu -> 2/mu, B3 seed reversal, every Moebius involution: none preserves Q4 and fixes phi; Galois up to similarity fixes it but also fixes the non-silent a = 1/phi^3',
    fixed='-', reason='the 24 corners split into two regular icosahedra (each a 5-design): mechanism 3 on a sub-object, not an involution of the line')

progress(2, 'P1: #91 (all-golden 4D), #100 (Dehn test), #45, #85, #93, #105, #44, family, locality')
# ---- #91: K cap mu K*, tesseract and 16-cell, 2 < mu < 3: corners sperm4(1, 1, mu - 2, 0)
check(is0(phi ** 2 + 2 + 1 / phi ** 2 - 5), 'P1 [#91] the two all-golden points mu = phi^2 and 2 + 1/phi^2 sum to 5: swapped by mu -> 5 - mu')
M4 = sp.Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [1, 1, 1, 1], [1, 1, 1, -1]])
check(M4.det() != 0, 'P1 [#91] (1, 1, a, 0), a = mu - 2, is a corner of K cap mu K* (active: x1 = 1, x2 = 1, x1+x2+x3+-x4 = mu; independent)')
argued('P1 [#91] its B4 seed (edge lengths along the diagram, last node the short root) is (0, 1-a, a, 0); the seed reversal (0, a, 1-a, 0) is a -> 1-a, i.e. mu -> 5 - mu')
# cube-facet cell at x4 = 1: |x'|_1 <= mu - 1 (eps4 = +1 constraint): the 3D cube-octahedron cell at mu3 = mu - 1; mu -> 5 - mu gives mu3 -> 3 - mu3
mu3 = sp.symbols('mu3')
check(is0(((5 - (mu3 + 1)) - 1) - (3 - mu3)), 'P1 [#91] on the 8 cube cells (C-O cell at mu3 = mu - 1) the swap mu -> 5 - mu IS the CsCl site swap mu3 -> 3 - mu3 (geometric there)')
check(is0((phi ** 2 - 1) - phi) and is0((2 + 1 / phi ** 2 - 1) - (3 - phi)), 'P1 [#91] the golden pair: cube cells at mu3 = phi (Icosaxes) and 3 - phi, its CsCl partner')
# tetrahedral cells: slice {sum x = mu, 0 <= x <= 1} of the unit 4-cube, = slice at t = 4 - mu: cut fraction x(t) = (t-1)/t
tt = sp.symbols('t', positive=True)
xc = lambda t: (t - 1) / t
check(is0(xc(R(3, 2)) - R(1, 3)), 'P1 [#91] fixed point mu = 5/2: tetrahedral cell cut at 1/3 = Archimedean truncated tetrahedron; cube cell = Kelvin: S(5/2) = sperm4(1,1,1/2,0) = the BITRUNCATED TESSERACT (uniform, B4 seed (0,1,1,0))')
check(not is0(sp.radsimp(xc(4 - phi ** 2) - xc(4 - 2 - 1 / phi ** 2))), 'P1 [#91] on the 16 tetrahedral cells the swap pairs non-similar truncated tetrahedra (cuts (2-phi)/(3-phi) and 1/phi^2): not a similarity there')
tone = 192 * (sum(t ** 4 for t in (2, 2, 1, 0)) - R(1, 2) * sum(t ** 2 for t in (2, 2, 1, 0)) ** 2)
check(tone != 0, f'P1 [#91] at the fixed point the B4 degree-4 corner tone (sum x^4 - |x|^4/2; here 192 x its value at the scaled corner (2,2,1,0), i.e. each of the 96 corners twice) = {tone} != 0: no tone forced (as palindromic-middles found)')
# REFEREE (A): the fixed point is singled out by a checkable property (the uniform member), and the degree-4 tone has a forced zero only at the 24-cell end
def sp4(v): return {tuple(sg[i] * p_[i] for i in range(4)) for p_ in itertools.permutations(v) for sg in itertools.product((1, -1), repeat=4)}
C12 = sorted(sp4((Fr(1), Fr(1), Fr(1, 2), Fr(0)))); d2q = lambda p_, q_: sum((p_[i] - q_[i]) ** 2 for i in range(4))
m12 = min(d2q(C12[0], q_) for q_ in C12[1:]); deg12 = {sum(1 for q_ in C12 if d2q(p_, q_) == m12) for p_ in C12}
e1_ = sum((u_ - w_) ** 2 for u_, w_ in zip((1, 1, a, 0), (1, a, 1, 0))); e2_ = sum((u_ - w_) ** 2 for u_, w_ in zip((1, 1, a, 0), (1, 1, 0, a)))
check(len(C12) == 96 and m12 == Fr(1, 2) and deg12 == {4} and sp.solve(sp.Eq(e1_, e2_), a) == [R(1, 2)],
      'P1 [#91] the fixed point a = 1/2 is the UNIFORM member: the two edge kinds of sperm4(1, 1, a, 0), squared lengths 2(1 - a)^2 and 2a^2, are equal only at a = 1/2; there all 96 corners (the bitruncated tesseract has 96, not 192) have 4 neighbours at distance^2 1/2 (exact)')
tone_a = sp.expand(sum(t ** 4 for t in (1, 1, a, 0)) - R(1, 2) * sum(t ** 2 for t in (1, 1, a, 0)) ** 2)
check(is0(tone_a - a ** 2 * (a ** 2 - 4) / 2) and is0(96 * tone_a.subs(a, R(1, 2)) + 45) and is0(2 * 16 * 96 * tone_a.subs(a, R(1, 2)) - tone),
      'P1 [#91] on the line the degree-4 tone summed over the 96 corners is 48 a^2 (a^2 - 4): on 0 <= a <= 1 its only zero is a = 0, the 24-cell (forced there by extra symmetry: F4 has no invariant of degree 4), an endpoint, not the fixed point; at a = 1/2 it is -45 (the earlier -1440 counted each corner twice at scale 2)')
argued('P1 [#91] the B4 diagram has no symmetry, so the seed reversal is not an automorphism of the group: mu -> 5 - mu is a PARAMETER PAIRING, geometric on the cube cells only')
tab('P1', '#91 all-golden 4D solids', verdict='SWAP FOUND (pair), NOT FORCED', swap='mu -> 5 - mu = the B4 seed reversal on the line; on the cube cells it is the CsCl site swap',
    fixed='mu = 5/2, the bitruncated tesseract (cells Kelvin TO + Archimedean truncated tetrahedra)', reason='a parameter pairing, geometric on the cube cells only (the B4 diagram has no symmetry); the two all-golden polytopes are a swapped PAIR; the fixed point is the uniform member; its degree-4 tone is nonzero; the tone 48 a^2 (a^2 - 4) (over the 96 corners) vanishes only at the 24-cell end (a = 0), forced there by F4 symmetry')

# ---- #100: Kelvin's zero is the CsCl parity (control C above); the truncated tetrahedra T cap (-kT): fold k -> 1/k
TV = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
def tcut(k):
    P = [([-v[0], -v[1], -v[2]], 1) for v in TV] + [(list(v), k) for v in TV]
    V, _ = polytope(P); return [tuple(t) for t in V]
DT = {}
for k in ([R(3, 2), R(2)] if PILOT else [R(1), R(3, 2), R(2), R(5, 2), R(2, 3)]):
    DT[k] = exact_dehn(tcut(k), f'T cap -{k}T')['D']; note(f'P1 #100 Dehn of T cap (-{k}T)', f'{DT[k]} (x) beta')
check(is0(DT[R(2)]) and all(is0(sp.expand(DT[k] - 24 * s2 * (k - 2))) for k in DT if k >= 1),
      'P1 [#100] Dehn(T cap -kT) = 24 sqrt2 (k - 2) (x) beta, beta = arctan(1/sqrt2) (cuts sum to 3 - k; zero iff they sum to one edge, k = 2)')
check(set(map(lambda v: tuple(sp.nsimplify(-t / 2) for t in v), tcut(R(2)))) == set(map(lambda v: tuple(sp.nsimplify(t) for t in v), tcut(R(1, 2)))),
      'P1 [#100] the fold k -> 1/k is the similarity x -> -x/k: S(1/2) = -S(2)/2 exactly (same shape: a fold, identity on shapes)')
if R(2, 3) in DT: check(not is0(DT[R(3, 2)]) and (is0(sp.expand(DT[R(2, 3)] - DT[R(3, 2)] * R(2, 3))) or is0(sp.expand(DT[R(2, 3)] + DT[R(3, 2)] * R(2, 3)))), f'P1 [#100] Dehn is EVEN under the fold: D(2/3) = (2/3) D(3/2) = {DT[R(2, 3)]} (homogeneous of degree 1, never odd): parity forces no zero')
if R(1) in DT: check(not is0(DT[R(1)]), f'P1 [#100] at the fold\'s fixed point k = 1 (the octahedron T cap -T) Dehn = {DT[R(1)]} != 0')
# REFEREE (B): one angle unit. The exact routine measures Dehn in beta = arctan(1/sqrt2) = arcsin(1/sqrt3) (arccos(1/3) = 2 beta, arccos(-1/3) = pi - 2 beta,
# arccos(1/sqrt3) = pi/2 - beta). On the cube-octahedron line: Dehn(S(mu)) = -24 sqrt2 (3 - 2 mu) (x) beta = 12 sqrt2 (3 - 2 mu) (x) arccos(-1/3)
check(all(is0(sp.expand(DCO[m_] + 24 * s2 * (3 - 2 * m_))) for m_ in DCO),
      f'P1 [#100] Dehn(cube cap mu octahedron) = -24 sqrt2 (3 - 2 mu) (x) beta, beta = arctan(1/sqrt2), i.e. 12 sqrt2 (3 - 2 mu) (x) arccos(-1/3), on every control point {sorted(map(str, DCO))}: odd under mu -> 3 - mu')
argued('P1 [#100] proof of the forcing: in the cube tiling the cell complementary to cube cap mu-octahedron is a copy of cube cap (3 - mu)-octahedron about the cube corner; one of each fills a period, so D(mu) + D(3 - mu) = 0 and D(3/2) = 0. The swap extends to 0 <= mu <= 3 and pairs the cube (mu = 3) with the empty cell (mu = 0)')
tab('P1', '#100 Dehn test', verdict='SWAP FOUND (Kelvin half), FORCED (already proved, swaps study K4)', swap='CsCl site swap mu -> 3 - mu',
    fixed='mu = 3/2, Kelvin', reason='Dehn = -24 sqrt2 (3 - 2 mu) (x) beta, beta = arctan(1/sqrt2) (= 12 sqrt2 (3 - 2 mu) (x) arccos(-1/3)), odd: the complementary cell in the cube tiling is the (3 - mu) cell, one of each fills a period; the swap pairs the cube (mu = 3) with the empty cell (mu = 0), so the cube zero is not at a fixed point; on T cap (-kT) the only swap is the fold k -> 1/k, under which Dehn is even: no forced zero')

# ---- #45 width
rho = sp.symbols('rho', positive=True)
wd = sp.sqrt(3 + rho ** 2) - rho
check(is0(sp.radsimp(wd.subs(rho, 1 / s3) - (sp.sqrt(30) - s3) / 3)), 'P1 [#45] w(rho) = sqrt(3 + rho^2) - rho with rho = r/R reproduces the cube/octahedron width (sqrt30 - sqrt3)/3')
check(is0(sp.expand(wd * wd.subs(rho, -rho) - 3)), 'P1 [#45] w(rho) w(-rho) = 3 (an algebraic "turn", fixed point rho = 0: a flat solid, no geometry)')
argued('P1 [#45] polar duality: R(P°) = 1/r(P), r(P°) = 1/R(P), so r/R and the width are equal on dual pairs (the paper\'s corollary IS a duality invariance)')
tab('P1', '#45 width theorem', verdict='SWAP FOUND (invariance), NOT FORCED', swap='polar duality D<->I, C<->O', fixed='the tetrahedron (self-dual)',
    reason='the width depends only on r/R, which duality keeps; at the fixed point the formula does not apply (classical Reuleaux tetrahedron)')

# ---- #85 valley rule
sv, al_ = sp.symbols('s alpha', positive=True)
kk = 3
lhs = (1 / sv) ** kk * sp.tan(sp.pi / 2 - al_); rhs = 1 / (sv ** kk * sp.tan(al_))
check(is0(sp.simplify(lhs - rhs)), 'P1 [#85] tan g_k = s^k tan(alpha) is invariant under (s -> 1/s, alpha -> pi/2 - alpha, g -> pi/2 - g): an involution of ONE solid only when alpha = pi/4')
argued('P1 [#85] alpha = pi/4 exactly for the cube (tan alpha = (a/2)/(a/2)); at the fixed point s = 1 (mirrored spikes, t = 2): g = pi/4 forced, delta + 2g = pi: valley faces coplanar (the rhombic dodecahedron, classical)')
tq = sp.symbols('tq')
cr = sp.simplify((tq - 0) * (tq / (tq - 1) - 2) / ((tq - 2) * (tq / (tq - 1) - 0)))
check(is0(cr + 1), 'P1 [#85] t -> t/(t-1) is harmonic conjugation with respect to the centre (t = 0) and the mirror point (t = 2): projective, not a similarity')
tab('P1', '#85 valley rule', verdict='ALGEBRAIC SWAP ONLY (does not qualify)', swap='s -> 1/s with alpha, gamma -> pi/2 - ., only for alpha = pi/4 (the cube)',
    fixed='t = 2 on the cube', reason='the involution is projective harmonic conjugation, not geometric; what it forces (coplanar valleys = the RD) is the formula\'s own value')

# ---- #93 and #105: CsCl swap
def dist2set(P):
    return sorted(sp.nsimplify(sum((p[i] - q[i]) ** 2 for i in range(len(p)))) for p, q in itertools.combinations(P, 2))
def prop(L1, L2):
    r = L2[-1] / L1[-1]; return all(is0(u * r - w) for u, w in zip(L1, L2))
for vals4, mm in [((1, 2, 4, 5), R(4, 3)), ((-5, -1, 1, 5), R(5, 3)), ((1, 2, 3, 4), R(3, 2))]:
    P4 = [tuple(sp.Integer(t) for t in p) for p in set(itertools.permutations(vals4))]
    P3 = [tuple(t) for t in sperms((sp.Integer(1), mm - 1, sp.Integer(0)))]
    check(len(P4) == len(P3) == 24 and prop(dist2set(P4), dist2set(P3)), f'P1 [#105/#93] the permutohedron of {vals4} has the distance pattern of the C-O cell at mu = {mm}')
tab('P1', '#93 one way only', verdict='SWAP FOUND (invariance), NOT FORCED', swap='CsCl site swap mu -> 3 - mu exchanges P_mu and Q_mu',
    fixed='mu = 3/2 (Kelvin)', reason='the law holds at every mu of the walk, so the swap maps it to itself; nothing new happens at 3/2')
tab('P1', '#105 4D Vacuus counts', verdict='SWAP FOUND (pair), NOT AT THE FIXED POINT', swap='CsCl swap: the 1:2 TO (mu = 4/3) <-> the 2:1 TO (5/3)',
    fixed='mu = 3/2 (Kelvin, the permutohedron of 1,2,3,4)', reason='the heart is one member of a swapped pair; the slice counts are integers with no parameter')

# ---- #44 face pyramids
dual = {'D': 'I', 'I': 'D', 'C': 'O', 'O': 'C', 'T': 'T'}
fill = [frozenset('C'), frozenset('TO'), frozenset('CTO')]
img44 = [frozenset(dual[c] for c in s) for s in fill]
check([s in fill for s in img44] == [False, False, True], 'P1 [#44] duality maps the filling sets {C}, {T,O}, {C,T,O} to {O}, {T,C}, {C,T,O}: only the last is a filling set; the law is not duality-invariant')
tab('P1', '#44 face pyramids', verdict='NONE', swap='duality (fails: {C} -> {O}); mirror and Galois act trivially or leave the five', fixed='-', reason='discrete classification; the one natural swap does not preserve it')
for lab, why in [('#47 every mix fills', 'universal over all 31 mixes: every permutation of D,I,C,T,O keeps it; no point is singled out'),
                 ('#106 one world', 'same: universal over the 31 mixes'),
                 ('#77 face-to-face reduction', 'discrete; no parameter'),
                 ('#92 pyramid tilings = stackings', 'c<->h and word reversal permute the tilings (invariance); complement has no fixed word, palindromes carry nothing'),
                 ('#101 held by shape', 'the layer inversion fixes the octahedra (locked) but also the cubes of the upright cube layer, which are free (#101 calibration): no correlation to force'),
                 ('Laves locality theorem', 'the six-layer window is symmetric about the gap (mirror-invariant); nothing at a fixed point')]:
    tab('P1', lab, verdict='NONE', swap='-', fixed='-', reason=why)
# permutohedron family: Loday's facets are the intervals; reversal i -> n+1-i keeps intervals and their sizes
ok = True
for n in range(4, 8):
    I = {frozenset(range(i, j + 1)) for i in range(1, n + 1) for j in range(i, n + 1)}
    ok &= all(frozenset(n + 1 - t for t in S) in I for S in I)
check(ok, 'P1 [Permutohedron Family Thm 1] the reversal i -> n+1-i maps intervals to intervals of the same size (n = 4..7): it fixes Pi and Loday\'s L, hence EVERY member of the line')
tab('P1', 'Permutohedron Family Theorem 1', verdict='NONE', swap='reversal w0 and x -> (n+1) - x fix every member', fixed='the whole line',
    reason='a swap that fixes every point singles none out; the end points are not isometric (Pi tiles, L does not), so no s -> 1 - s is geometric')

# =====================================================================================================================
# PART 2a. SCHUETZENBERGER EVACUATION
# =====================================================================================================================
progress(3, 'P2a: evacuation, RSK, self-evacuating tableaux, domino tableaux')
def rsk(w):
    P, Q = [], []
    for k, v in enumerate(w, 1):
        r = 0
        while True:
            if r == len(P): P.append([v]); Q.append([k]); break
            row = P[r]; j = next((j for j, u in enumerate(row) if u > v), None)
            if j is None: row.append(v); Q[r].append(k); break
            row[j], v = v, row[j]; r += 1
    return P, Q
def evac(T):
    T = [r[:] for r in T]; n = sum(len(r) for r in T); res = [[0] * len(r) for r in T]
    for k in range(n, 0, -1):
        i = j = 0
        while True:
            rt = T[i][j + 1] if j + 1 < len(T[i]) else None
            dn = T[i + 1][j] if i + 1 < len(T) and j < len(T[i + 1]) else None
            if rt is None and dn is None: break
            if dn is None or (rt is not None and rt < dn): T[i][j] = rt; j += 1
            else: T[i][j] = dn; i += 1
        T[i].pop(); res[i][j] = k
        if not T[i]: T.pop(i) if i == len(T) - 1 else None
    return res
NMAX = 6 if PILOT else 7
ok = True; fixedperm = {}
for n in range(1, NMAX + 1):
    cnt = 0
    for w in itertools.permutations(range(1, n + 1)):
        P, Q = rsk(w); wh = tuple(n + 1 - w[n - 1 - i] for i in range(n)); P2, Q2 = rsk(wh)
        ok &= (P2 == evac(P)) and (Q2 == evac(Q))
        cnt += (wh == w)
    fixedperm[n] = cnt
check(ok, f'P2a Schuetzenberger: RSK(w0 w w0) = (evac P, evac Q) for every permutation, n <= {NMAX}: on orderings evacuation IS w -> w0 w w0 (reverse the row, b -> n+1-b)')
check(all(fixedperm[n] == 2 ** (n // 2) * math.factorial(n // 2) for n in fixedperm), f'P2a fixed orderings = the centrally symmetric ones, 2^k k! (k = floor(n/2)): {fixedperm}')
def partitions(n, mx=None):
    if n == 0: yield (); return
    for p in range(min(n, mx or n), 0, -1):
        for q in partitions(n - p, p): yield (p,) + q
def syts(sh):
    sh = list(sh); n = sum(sh)
    if n == 0: yield []; return
    for i in range(len(sh)):
        if sh[i] > 0 and (i + 1 == len(sh) or sh[i + 1] < sh[i]):
            s2_ = sh[:]; s2_[i] -= 1
            for T in syts(tuple(t for t in s2_ if t)):
                T = [r[:] for r in T]
                while len(T) <= i: T.append([])
                T[i].append(n); yield T
from functools import lru_cache
@lru_cache(None)
def dominoes(sh):
    if sum(sh) == 0: return 1
    sh = list(sh); tot = 0
    for i in range(len(sh)):
        if sh[i] >= 2:
            s2_ = sh[:]; s2_[i] -= 2
            if all(s2_[j] >= s2_[j + 1] for j in range(len(s2_) - 1)): tot += dominoes(tuple(t for t in s2_ if t))
        if i + 1 < len(sh) and sh[i] == sh[i + 1]:
            s2_ = sh[:]; s2_[i] -= 1; s2_[i + 1] -= 1
            if all(s2_[j] >= s2_[j + 1] for j in range(len(s2_) - 1)): tot += dominoes(tuple(t for t in s2_ if t))
    return tot
ok = True; sumsq = {}; rows = {}
for n in range(2, (7 if PILOT else 9)):
    sq = 0
    for sh in partitions(n):
        Ts = list(syts(sh)); se = sum(1 for T in Ts if evac(T) == T); sq += se * se
        if n % 2 == 0: ok &= (se == dominoes(sh)); rows[str(sh)] = [len(Ts), se, dominoes(sh)]
    sumsq[n] = sq
check(ok, 'P2a self-evacuating SYT of shape lambda = domino tableaux of lambda, every lambda with |lambda| even <= 8 (Stanley\'s conjecture, proved by Stembridge 1996; bijection Berenstein-Kirillov 2000; survey Stanley 2009)')
check(all(sumsq[n] == 2 ** (n // 2) * math.factorial(n // 2) for n in sumsq), f'P2a sum over shapes of (self-evacuating)^2 = 2^k k!, the fixed orderings: {sumsq}')
OUT['P2']['evacuation_tableaux_even'] = rows

progress(4, 'P2a: the fixed slice of the permutohedron, its battery, Brunn')
# sigma: x -> (n+1) 1 - w0 x. Fixed corners in u-coordinates u_a = x_a - x_{n+1-a}
for n in range(4, 8):
    k = n // 2; fx = [w for w in itertools.permutations(range(1, n + 1)) if all(w[i] + w[n - 1 - i] == n + 1 for i in range(n))]
    U = {tuple(w[i] - w[n - 1 - i] for i in range(k)) for w in fx}
    exp = {tuple(s * p for s, p in zip(sg, pm)) for pm in itertools.permutations(range(1, 2 * k, 2) if n % 2 == 0 else range(2, 2 * k + 1, 2)) for sg in itertools.product((1, -1), repeat=k)}
    check(U == exp, f'P2a n = {n}: the evacuation-fixed corners are the signed permutations of ({", ".join(map(str, sorted(abs(t) for t in next(iter(U)))))}) in the fixed space (a B{k} permutohedron)')
    if not PILOT or n <= 5:
        rnd = random.Random(n); okk = True
        allp = list(itertools.permutations(range(1, n + 1)))
        for _ in range(30):
            d = [Fr(rnd.randint(-50, 50), rnd.randint(1, 9)) for _ in range(k)]
            L = lambda w: sum(d[i] * (w[i] - w[n - 1 - i]) for i in range(k))
            okk &= max(map(L, allp)) == max(map(L, fx))
        check(okk, f'P2a n = {n}: the projection of the permutohedron to the fixed space has the same support as the fixed corners (30 random directions; not needed: for every convex body and affine involution s preserving it, x -> (x + s x)/2 maps the body onto its fixed slice): fixed slice = projection')
argued('P2a so the 3D fixed slices are the silent-zonohedron line of the forced study at a = 1/2 (n = 6, corners sperm(1/2, 3/2, 5/2)) and a = 1 (n = 7, sperm(1, 2, 3))')
Vz = 4 * (2 * a ** 3 + 12 * a ** 2 + 21 * a + 8); Az = 24 * a ** 2 + (48 + 24 * s2) * a + 12 + 24 * s3
Vpol = 8 / ((a + 2) * (3 * a + 3) * (2 * a + 3)); Mah = Vz * Vpol
HK = {kq: harmonic_invariants(kq) for kq in [4, 6, 8, 12]}
al, ga, de = sp.symbols('alpha gamma delta', positive=True)
p1, p2, p3 = sp.Matrix([al, 0, 0]), sp.Matrix([ga, ga, ga]), sp.Matrix([de, de, 0])
subz = {al: 1 / (a + 2), ga: 1 / (3 * a + 3), de: 1 / (2 * a + 3)}
u1, u2, u3 = sp.symbols('u1 u2 u3')
FK = {}
for kq in [4, 6, 8, 12]:
    for idx, H in enumerate(HK[kq]):
        Xv = p1 * u1 + p2 * u2 + p3 * u3
        pol = sp.Poly(sp.expand(H(*Xv)), u1, u2, u3)
        integ = sum(cf * sp.factorial(e1) * sp.factorial(e2) * sp.factorial(e3) / sp.factorial(e1 + e2 + e3 + 3) for (e1, e2, e3), cf in pol.terms())
        FK[(kq, idx)] = (48 * al * ga * de * integ).subs(subz)
for av, nn_ in [(R(1, 2), 6), (R(1), 7)]:
    v0 = (av, av + 1, av + 2)
    tz = {f'Q{kq}.{i}': sp.nsimplify(H(*v0)) for kq in HK for i, H in enumerate(HK[kq])}
    fz = {f'F{kq}.{i}': sp.nsimplify(sp.simplify(FK[(kq, i)].subs(a, av))) for (kq, i) in FK}
    dM = sp.simplify(sp.diff(Mah, a).subs(a, av)); gI = sp.simplify((2 * sp.diff(Vz, a) * Az - 3 * Vz * sp.diff(Az, a)).subs(a, av))
    check(all(t != 0 for t in tz.values()) and all(t != 0 for t in fz.values()) and dM != 0 and not is0(gI),
          f'P2a battery at the n = {nn_} fixed slice (a = {av}): every corner tone Q4..Q12 and canonical-form tone F4..F12 nonzero, Mahler and roundness not critical (Mahler\' = {dM})')
    OUT['P2'][f'evac_slice_n{nn_}'] = {'a': str(av), 'tones': {k_: str(v_) for k_, v_ in tz.items()}, 'form_tones': {k_: str(v_) for k_, v_ in fz.items()}}
argued('P2a tiling: no member a > 0 fills space in any way (forced study, dihedral-angle proof); Dehn = 0 at every a (a zonotope is a union of parallelepipeds): neither is forced by the swap')
# Brunn: the fixed slice is the largest parallel slice (sigma negates F-perp, slice volume even; Brunn-Minkowski concavity)
# n = 4: Kelvin's cell, slices parallel to the octagon, offset w along (1,-1,-1,1)
def p4_area(w):
    m = Fr(5, 2)
    param = [([Fr(1), Fr(0)], m + w), ([Fr(0), Fr(1)], m - w), ([Fr(0), Fr(-1)], m - w), ([Fr(-1), Fr(0)], m + w)]
    A_, b_ = perm_planes(4, param); return rat_measure(A_, b_, 2)
A4 = {w: p4_area(w) for w in [Fr(0), Fr(1, 4), Fr(-1, 4), Fr(1, 2), Fr(-1, 2)]}
V0 = set(A4[Fr(0)][1]); expo = {(Fr(s1 * p[0], 2), Fr(s2_ * p[1], 2)) for p in [(1, 3), (3, 1)] for s1 in (1, -1) for s2_ in (1, -1)}
check(V0 == expo, 'P2a n = 4: the evacuation-fixed slice of Kelvin\'s cell (the 4-permutohedron) is the octagon sperm(1/2, 3/2) (exact vertex enumeration)')
q4_ = [Fr(-1, 2), Fr(-1, 4), Fr(0), Fr(1, 4), Fr(1, 2)]
check(all(A4[Fr(0)][0] > A4[w][0] and A4[w][0] == A4[-w][0] for w in [Fr(1, 4), Fr(1, 2)]),
      f'P2a [Brunn] n = 4: slice areas even in the offset and largest at the fixed slice: {[(str(w), str(A4[w][0])) for w in sorted(A4)]}')
check(all(concave_root(A4[q4_[i - 1]][0], A4[q4_[i]][0], A4[q4_[i + 1]][0], 2) for i in (1, 2, 3)),
      'P2a [Brunn, concavity] n = 4: area^(1/2) strictly concave at offsets -1/4, 0, 1/4 (exact, by squaring)')
OUT['P2']['brunn_P4_octagon_areas'] = {str(w): str(A4[w][0]) for w in sorted(A4)}
# REFEREE FIX (15 Nov): duplicate planes are now skipped in rat_measure; all P5 and P6 slices recomputed; concavity of volume^(1/3) checked
P6D = [(Fr(1), Fr(-1), Fr(0)), (Fr(1), Fr(0), Fr(-1))]     # the two offset directions tested (w1 + w2 + w3 = 0 keeps the slice in the hyperplane)
s6_ = [Fr(-1, 2), Fr(-1, 4), Fr(0), Fr(1, 4), Fr(1, 2)]
off6 = lambda s, d: tuple(s * t for t in d)
jobs = [('P6', off6(Fr(0), P6D[0]))] + ([] if PILOT else [('P6', off6(s, d)) for d in P6D for s in s6_ if s != 0])
t5_ = [Fr(-1), Fr(-1, 2), Fr(0), Fr(1, 2), Fr(1)]
jobs += [('P5', t) for t in t5_]
import multiprocessing as _mp
with _mp.get_context('fork').Pool(min(WORKERS, len(jobs))) as pool: SL = dict(pool.map(slice_job, jobs))
from scipy.spatial import ConvexHull
hull_ok = all(abs(ConvexHull(np.array([[float(c) for c in v] for v in SL[j][1]])).volume - float(SL[j][0])) < 1e-9 for j in SL)
check(hull_ok, f'P2a/P2b every exact slice volume agrees with an independent floating hull volume (|difference| < 1e-9) on all {len(SL)} slices')
OUT['P2']['slice_facets'] = {f'{j[0]} {j[1] if j[0] == "P5" else tuple(map(str, j[1]))}': SL[j][2] for j in SL}
V6 = set(SL[('P6', (Fr(0), Fr(0), Fr(0)))][1])
exp6 = {tuple(Fr(s * p, 2) for s, p in zip(sg, pm)) for pm in itertools.permutations((1, 3, 5)) for sg in itertools.product((1, -1), repeat=3)}
check(V6 == exp6, 'P2a n = 6: the evacuation-fixed 3D slice of the 6-permutohedron is exactly sperm(1/2, 3/2, 5/2) (48 corners, exact vertex enumeration)')
v6 = {k_[1]: SL[k_][0] for k_ in SL if k_[0] == 'P6'}
z6 = (Fr(0),) * 3
check(v6[z6] == 87 and sp.Rational(87) == Vz.subs(a, R(1, 2)),
      f'P2a n = 6: the fixed slice has volume {v6[z6]} = 4(2a^3 + 12a^2 + 21a + 8) at a = 1/2 (the forced study\'s zonohedron formula, an independent route); the earlier 138 counted duplicate planes twice ({SL[("P6", z6)][2]["duplicates"]} duplicates now skipped)')
if not PILOT:
    check(all(v6[z6] > v6[w] for w in v6 if w != z6) and all(v6[w] == v6[tuple(-t for t in w)] for w in v6),
          f'P2a [Brunn-Minkowski] n = 6: slice volumes even in the offset and largest at the fixed slice: {[(str(tuple(map(str, w))), str(v6[w])) for w in v6]}')
    check(all(concave_root(v6[off6(s6_[i - 1], d)], v6[off6(s6_[i], d)], v6[off6(s6_[i + 1], d)], 3) for d in P6D for i in (1, 2, 3)),
          'P2a [Brunn-Minkowski, concavity] n = 6: volume^(1/3) strictly concave along both offset directions (1,-1,0) and (1,0,-1) at -1/4, 0, 1/4 (exact rational bounds on cube roots)')
    OUT['P2']['brunn_P6_slice_volumes'] = {str(tuple(map(str, w))): str(v6[w]) for w in v6}
v5 = {k_[1]: SL[k_][0] for k_ in SL if k_[0] == 'P5'}
V5 = set(SL[('P5', Fr(0))][1]); exp5 = {p[:3] for p in itertools.permutations((Fr(1), Fr(2), Fr(4), Fr(5)))}
check(V5 == exp5, 'P2b the central slice x5 = 3 of the 4D permutohedron is the DICTO 1:2 Truncated Octahedron, permutohedron of (1,2,4,5) (#105)')
mu_ = R(4, 3); vhand = (R(4, 3) * mu_ ** 3 - 4 * (mu_ - 1) ** 3) * 27 / 2
check(v5[Fr(0)] == Fr(122, 3) and sp.Rational(v5[Fr(0)].numerator, v5[Fr(0)].denominator) == vhand,
      f'P2b its volume in coordinates y1..y3 is {v5[Fr(0)]} = (4mu^3/3 - 4(mu - 1)^3) x 3^3 / 2 at mu = 4/3 (cube cap mu-octahedron, an independent route); the earlier 140/3 counted the six squares twice')
check(v5[Fr(1)] == v5[Fr(-1)] == Fr(205, 6) and v5[Fr(1, 2)] == v5[Fr(-1, 2)] == Fr(1835, 48),
      f'P2b slices x5 = 3 +- 1 (permutohedra of 1,2,3,5 and 1,3,4,5): {v5[Fr(1)]} (earlier 259/6, duplicates); x5 = 3 +- 1/2: {v5[Fr(1, 2)]} (unchanged, no coincident planes)')
check(all(v5[Fr(0)] > v5[t] for t in v5 if t != 0) and all(v5[t] == v5[-t] for t in v5),
      f'P2b [Brunn] it is the largest of its parallel slices x5 = 3 + t (volumes in coordinates y1..y3: {[(str(t), str(v5[t])) for t in sorted(v5)]})')
check(all(concave_root(v5[t5_[i - 1]], v5[t5_[i]], v5[t5_[i + 1]], 3) for i in (1, 2, 3)),
      f'P2b [Brunn, concavity] volume^(1/3) strictly concave at t = -1/2, 0, 1/2 (cube roots {[round(float(v5[t]) ** (1 / 3), 4) for t in t5_]}; exact rational bounds)')
OUT['P2']['brunn_P5_slice_volumes'] = {str(t): str(v5[t]) for t in sorted(v5)}

progress(5, 'P2a: change ringing (Paradigm Ch. 15)')
def sig_row(r): n = len(r); return tuple(n + 1 - r[n - 1 - i] for i in range(n))
def apply(r, swaps):
    r = list(r)
    for i in swaps: r[i], r[i + 1] = r[i + 1], r[i]
    return tuple(r)
def hunt(n, first):
    A_ = list(range(0, n - 1, 2)); B_ = list(range(1, n - 1, 2)); ch = [A_, B_] if first == 0 else [B_, A_]
    r = tuple(range(1, n + 1)); out = [r]
    for k in range(2 * n - 1): r = apply(r, ch[k % 2]); out.append(r)
    return out
ok_even = all(all(sig_row(r) == r for r in hunt(n, 0)) for n in range(4, 11, 2))
ok_odd = all([sig_row(r) for r in hunt(n, 0)] == hunt(n, 1) for n in range(5, 12, 2))
check(ok_even, 'P2a plain hunt on 4, 6, 8, 10 bells: EVERY row is fixed by evacuation (reverse the row, b -> n+1-b)')
check(ok_odd, 'P2a plain hunt on 5, 7, 9, 11 bells: evacuation maps the hunt to the hunt that starts with the other change (the two halves of Paradigm Thm 13.7 swapped)')
# REFEREE (D): for odd n the two hunts are the same 2n rows rung in opposite order; exactly two rows (rounds, back rounds) are fixed
ok_rev = all(hunt(n, 1) == [hunt(n, 0)[0]] + hunt(n, 0)[:0:-1] and sum(1 for r in hunt(n, 0) if sig_row(r) == r) == 2 for n in range(5, 12, 2))
check(ok_rev, 'P2a odd n = 5..11: the other hunt is the same 2n rows rung in the opposite order, so the move maps the plain hunt to itself reversed; exactly 2 of its rows are fixed (rounds and back rounds)')
PN = {'x': [0, 2], '14': [1], '12': [2], '34': [0]}
def method(lead, n_leads):
    r = (1, 2, 3, 4); out = [r]
    for _ in range(n_leads):
        for c in lead: r = apply(r, PN[c]); out.append(r)
    return out
pb = method(['x', '14'] * 3 + ['x', '12'], 3)
check(len(set(pb[:-1])) == 24 and pb[-1] == (1, 2, 3, 4), 'P2a Plain Bob Minimus: 24 rows, an extent')
img_pb = [sig_row(r) for r in pb]; m34 = method(['x', '14'] * 3 + ['x', '34'], 3)
nfix = sum(1 for r in pb[:-1] if sig_row(r) == r)
check(img_pb == m34 and nfix == 8 == sum(1 for r in itertools.permutations(range(1, 5)) if sig_row(r) == r),
      f'P2a evacuation maps Plain Bob Minimus (x14x14x14x12) to x14x14x14x34 (not to itself); {nfix} of its 24 rows are fixed, which says nothing about the method: its rows are all of S4 and 8 = 2^2 2! is the number of centrally symmetric rows')
# REFEREE (D) credit: the image is Reverse Bob Minimus started from its half-lead (CCCBR Methods Library, extract of the change-ringing study)
def expand_pn(pn):
    half, le = pn.split(',') if ',' in pn else (pn, None)
    toks = []; i = 0
    while i < len(half):
        if half[i] in '-x': toks.append('x'); i += 1
        else:
            j = i
            while j < len(half) and half[j] not in '-x.': j += 1
            toks.append(half[i:j]); i = j + (1 if j < len(half) and half[j] == '.' else 0)
    return toks + toks[-2::-1] + [le] if le else toks
CCCBR = {}
for line in open(os.path.join(STUD, '2026-11-12-change-ringing', 'data', 'cccbr-methods-stage3-6.tsv')):
    f_ = line.rstrip('\n').split('\t')
    if len(f_) >= 8 and f_[6] in ('Plain Bob Minimus', 'Reverse Bob Minimus'): CCCBR[f_[6]] = f_[7]
pbx, rbx = expand_pn(CCCBR['Plain Bob Minimus']), expand_pn(CCCBR['Reverse Bob Minimus'])
imgx = ['34' if c == '12' else c for c in pbx]   # the move sends place 1-2 to place 3-4, keeps 1-4 and x
check(pbx == ['x', '14'] * 3 + ['x', '12'] and imgx[4:] + imgx[:4] == rbx,
      f'P2a [credit: the ringers\' reverse] the image x14x14x14x34, started from its half-lead, is {"".join(rbx)} = Reverse Bob Minimus ({CCCBR["Reverse Bob Minimus"]}, CCCBR Methods Library)')
tab('P2', 'evacuation (Schuetzenberger)', fixed='orderings: centrally symmetric rows (2^k k!); tableaux: self-evacuating = domino tableaux; slice: B_k permutohedra sperm(1,3,..) / sperm(1,..,k)',
    forced='Brunn: the fixed slice is the largest parallel slice (classical); nothing else (tones, form, Mahler, roundness nonzero/not critical; tiling no; Dehn 0 for every zonotope)',
    verdict='FORCED LAW = classical (Brunn-Minkowski: the fixed slice has codimension >= 2 for n >= 6; Brunn 1887 for hyperplane slices); the fixed slice is the type-B permutohedron by the standard folding A_{n-1} -> B_k (Steinberg; Stembridge); no new law')

# =====================================================================================================================
# PART 2b. LONGEST ELEMENT w0
# =====================================================================================================================
progress(6, 'P2b: w0 of A3, B3, H3, A4, B4, F4, H4; sweep reversal; Brunn')
def e(n, i): v = [0] * n; v[i] = 1; return v
def sub_(u, v): return [p - q for p, q in zip(u, v)]
G = {
 'A3': [sub_(e(4, i), e(4, i + 1)) for i in range(3)],
 'B3': [sub_(e(3, 0), e(3, 1)), sub_(e(3, 1), e(3, 2)), e(3, 2)],
 'H3': [[2, 0, 0], [-phi, 1, -1 / phi], [0, -2, 0]],
 'A4': [sub_(e(5, i), e(5, i + 1)) for i in range(4)],
 'B4': [sub_(e(4, 0), e(4, 1)), sub_(e(4, 1), e(4, 2)), sub_(e(4, 2), e(4, 3)), e(4, 3)],
 'F4': [sub_(e(4, 1), e(4, 2)), sub_(e(4, 2), e(4, 3)), e(4, 3), [R(1, 2), R(-1, 2), R(-1, 2), R(-1, 2)]],
 'H4': [[2, 0, 0, 0], [-phi, 1, -1 / phi, 0], [0, -2, 0, 0], [0, 1, phi, 1 / phi]]}
NPOS = {'A3': 6, 'B3': 9, 'H3': 15, 'A4': 10, 'B4': 16, 'F4': 24, 'H4': 60}
W0 = {}
_qf = {}; exec(open(os.path.join(STUD, '2026-11-13-platonic-fans-law', 'scripts', 'qf.py')).read(), _qf); QF = _qf['QF']; QF.D = 5
def toQF(t):
    t = sp.radsimp(sp.nsimplify(t)); b = sp.expand(t).coeff(s5); a_ = sp.expand(t - b * s5)
    return QF(Fr(int(a_.p), int(a_.q)), Fr(int(b.p), int(b.q)))
def qdot(u, v): return sum((p * q for p, q in zip(u, v)), QF(0))
for g, roots in G.items():
    rts = [sp.Matrix(r) for r in roots]; d = len(roots[0]); rk = len(roots)
    RQ = [[toQF(t) for t in r] for r in roots]; NQ = [qdot(r, r) for r in RQ]
    def srefl(i, v): c = qdot(v, RQ[i]) * 2 / NQ[i]; return [vi - c * ri for vi, ri in zip(v, RQ[i])]
    cs = sp.symbols(f'c0:{d}'); vv = sp.Matrix(cs)
    eqs = [(vv.T * r)[0] - 1 for r in rts] + ([sum(cs)] if d > rk else [])
    sol = sp.solve(eqs, cs, dict=True)[0]; v = [toQF(t) for t in vv.subs(sol)]
    word = []
    while True:
        i = next((i for i in range(rk) if qdot(v, RQ[i]).sign() > 0), None)
        if i is None: break
        v = srefl(i, v); word.append(i)
    steps = len(word)
    cols = []
    for j in range(d):
        b0 = [QF(1 if k_ == j else 0) for k_ in range(d)]
        for i in word: b0 = srefl(i, b0)
        cols.append([sp.Rational(t.a) + sp.Rational(t.b) * s5 for t in b0])
    Wm = sp.Matrix(cols).T
    W0[g] = Wm
    minus = all(is0(t) for t in (Wm + sp.eye(d)) * sp.Matrix.hstack(*rts))
    flip = all(all(is0(t) for t in (Wm * rts[i] + rts[rk - 1 - i])) for i in range(rk))
    fixdim = d - (Wm - sp.eye(d)).rank() - (d - rk)
    check(steps == NPOS[g] and (minus if g not in ('A3', 'A4') else (flip and not minus)),
          f'P2b {g}: w0 found as a product of {steps} reflections (= number of positive roots); w0 = {"-1" if minus else "-epsilon (diagram flip), not -1"}; fixed subspace dimension {fixdim}')
    OUT['P2'].setdefault('w0', {})[g] = {'length': steps, 'w0_is_minus_1': bool(minus), 'fixed_dim': int(fixdim)}
# sweep ledger of the 4D permutohedron: x -> 6 - x maps a corner with i down-edges at height h to one with 4 - i at height -h
uu = (1, 10, 100, 1000, 10000)
perms5 = list(itertools.permutations(range(1, 6)))
def nb(p):
    out = []
    for k in range(1, 5):
        q = tuple(k + 1 if t == k else k if t == k + 1 else t for t in p); out.append(q)
    return out
H_ = lambda p: sum(a_ * b__ for a_, b__ in zip(uu, p))
idown = {p: sum(1 for q in nb(p) if H_(q) < H_(p)) for p in perms5}
hv = [sum(1 for p in perms5 if idown[p] == i) for i in range(5)]
check(all(idown[tuple(6 - t for t in p)] == 4 - idown[p] for p in perms5) and hv == [1, 26, 66, 26, 1],
      f'P2b 4D permutohedron (A4, palindromic seed, so centrally symmetric): the sweep is a time palindrome, i down-edges at h <-> 4 - i at -h; h-vector {hv} (#104)')
# Brunn on the tetrahedron (A3: w0 = half-turn about the z axis, negates x and y) and its control
TP = [[-t for t in v] for v in TV]
def tet_slice(axis_eq):
    # 2D slice of T = {-v.x <= 1} by a plane; axis_eq: function giving param -> (coeff rows)
    return axis_eq
def area_x(t):   # plane x = t; free (y, z)
    A_ = [[Fr(n_[1]), Fr(n_[2])] for n_ in TP]; b_ = [Fr(1) - Fr(n_[0]) * t for n_ in TP]; return rat_measure(A_, b_, 2)[0]
def area_d(s):   # plane x + y + z = s; free (x, y), z = s - x - y (area in (x, y), a fixed multiple of the true area)
    A_ = [[Fr(n_[0] - n_[2]), Fr(n_[1] - n_[2])] for n_ in TP]; b_ = [Fr(1) - Fr(n_[2]) * s for n_ in TP]; return rat_measure(A_, b_, 2)[0]
ax = {t: area_x(t) for t in [Fr(0), Fr(1, 2), Fr(-1, 2)]}
check(ax[0] > ax[Fr(1, 2)] and ax[Fr(1, 2)] == ax[Fr(-1, 2)], f'P2b [Brunn, FORCED, A3] slices of the tetrahedron across a direction negated by w0: even, largest in the middle (the square): {[(str(t), str(v)) for t, v in ax.items()]}')
adg = {s: area_d(s) for s in [Fr(-1), Fr(0), Fr(1)]}
check(adg[Fr(-1)] > adg[Fr(0)], f'P2b [control, FAILS as required] along a 3-fold axis (no symmetry negates it) the middle slice is not the largest: {[(str(s), str(v)) for s, v in adg.items()]}')
def cell5(t):   # 5-cell {x >= 0, sum = 1}, slice x1 - x5 = t; free (s, x2, x3): x1 = s + t/2, x5 = s - t/2, x4 = 1 - 2s - x2 - x3
    A_ = [[Fr(-1), 0, 0], [Fr(-1), 0, 0], [0, Fr(-1), 0], [0, 0, Fr(-1)], [Fr(2), Fr(1), Fr(1)]]
    b_ = [t / 2, -t / 2, Fr(0), Fr(0), Fr(1)]; return rat_measure(A_, b_, 3)[0]
def cell5c(s):  # control: slice x1 = s; free (x2, x3, x4), x5 = 1 - s - x2 - x3 - x4
    A_ = [[Fr(-1), 0, 0], [0, Fr(-1), 0], [0, 0, Fr(-1)], [Fr(1), Fr(1), Fr(1)]]; b_ = [Fr(0), Fr(0), Fr(0), 1 - s]; return rat_measure(A_, b_, 3)[0]
c5 = {t: cell5(t) for t in [Fr(0), Fr(1, 4), Fr(-1, 4)]}
check(c5[0] > c5[Fr(1, 4)] and c5[Fr(1, 4)] == c5[Fr(-1, 4)], f'P2b [Brunn, FORCED, A4] slices of the 5-cell x1 - x5 = t (negated by w0 = (15)(24)): even, largest at t = 0: {[(str(t), str(v)) for t, v in c5.items()]}')
check(concave_root(ax[Fr(-1, 2)], ax[Fr(0)], ax[Fr(1, 2)], 2) and concave_root(c5[Fr(-1, 4)], c5[Fr(0)], c5[Fr(1, 4)], 3),
      'P2b [Brunn, concavity] tetrahedron area^(1/2) and 5-cell volume^(1/3) strictly concave across the middle slice (exact)')
c5c = {s: cell5c(s) for s in [Fr(0), Fr(1, 5)]}
check(c5c[Fr(0)] > c5c[Fr(1, 5)], 'P2b [control, FAILS as required] slices x1 = s (no symmetry negates e1): the largest is the facet s = 0, not the centroid level 1/5')
tab('P2', 'longest element w0', fixed='the centre (w0 = -1: B3, H3, B4, F4, H4); a line (A3) or plane (A4) for w0 = -epsilon',
    forced='every slice fixed by a symmetry that negates the offset directions is the largest of its parallels (Brunn for hyperplane slices, Brunn-Minkowski in general; central symmetry suffices but is not needed: the tetrahedron and the 5-cell examples use w0), e.g. the 1:2 TO (volume 122/3) in the 4D permutohedron; the sweep ledger of a centrally symmetric Wythoff solid is a time palindrome',
    verdict='FORCED LAW = classical (Brunn; Dehn-Sommerville pairing); no new law')

# =====================================================================================================================
# PART 2c. GALE AND ALEXANDER DUALITY
# =====================================================================================================================
progress(7, 'P2c: Gale self-association (8 corners, hexagonal discs), Alexander duality screen')
from sympy.polys.matrices import DomainMatrix
_fl = open(os.path.join(STUD, '2026-11-13-platonic-fans-law', 'scripts', 'fans_law.py')).read()
_ns = {'math': math, 'Fr': Fr}; exec(_fl[_fl.index('def recog_solid(Vf):'):_fl.index('def edges_of(F):')], _ns)
REG = {r['id']: r for r in json.load(open(os.path.join(STUD, '2026-11-13-platonic-disc-ranking', 'data', 'registry-solids.json')))}
def ld(v): return json.loads(v) if isinstance(v, str) else v
def exact_corners(sid):
    r = _ns['recog_solid'](ld(REG[sid]['V']))
    if r is None: return None, None
    D, _, _, out, _ = r; rt = sp.sqrt(D)
    return D, [tuple(sp.Rational(p[0]) + sp.Rational(p[1]) * rt for p in q) for q in out]
def rank_K(rows, D):
    M = sp.Matrix(rows); K = sp.QQ.algebraic_field(sp.sqrt(D)) if D != 1 else sp.QQ
    return DomainMatrix.from_Matrix(M).convert_to(K).rank()
def quad_rows(P): return [[p[0] ** 2, p[1] ** 2, p[2] ** 2, p[0] * p[1], p[0] * p[2], p[1] * p[2], p[0], p[1], p[2], 1] for p in P]
GALE = {}
# REFEREE (E): "rank <= 7 means self-associated" is a theorem for STABLE sets (Coble; Dolgachev-Ortland; Eisenbud-Popescu 2000, Cor. 7.4):
# 8 points in space, no two equal, no four on a line, no six in a plane. Checked exactly for every set tested.
def stable8(P, D):
    if len({tuple(map(str, p_)) for p_ in P}) < len(P): return False
    for k_, rmax in ((4, 1), (6, 2)):
        for S_ in itertools.combinations(P, k_):
            if rank_K([[S_[j][i] - S_[0][i] for i in range(3)] for j in range(1, k_)], D) <= rmax: return False
    return True
for sid in ['CUBE', 'J26_GYROBIFASTIGIUM', 'TRIAKIS_TETRAHEDRON', 'RHOMBOHEDRON', 'RHOMBIC_PRISM_60', 'LEANING_SQUARE_PRISM',
            'GOLDEN_RHOMBOHEDRON_PROLATE', 'GOLDEN_RHOMBOHEDRON_OBLATE', 'REULEAUX_CUBE'][: (3 if PILOT else 9)]:
    D, P = exact_corners(sid)
    if P is None: note(f'P2c {sid}', 'not recognised exactly'); continue
    rk = rank_K(quad_rows(P), D); GALE[sid] = {'faces': len(ld(REG[sid]['F'])), 'quadric_rank': rk, 'self_associated': rk <= 7, 'stable': stable8(P, D)}
    find(f'P2c Gale: {sid} (8 corners, {len(ld(REG[sid]["F"]))} faces): quadric rank {rk} -> {"SELF-ASSOCIATED (Gale fixed point)" if rk <= 7 else "not self-associated"}')
OUT['P2']['gale_8'] = GALE
check(GALE.get('CUBE', {}).get('self_associated'), 'P2c the cube\'s corners are self-associated: the products of opposite face planes (x^2-1, y^2-1, z^2-1) are a net of quadrics through all 8 (Coble; Eisenbud-Popescu)')
# frustum of the octahedron (a planar-faced hexahedron = projective image of the cube): self-associated, Dehn != 0
FR = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (R(1, 2), 0, R(1, 2)), (-R(1, 2), 0, R(1, 2)), (0, R(1, 2), R(1, 2)), (0, -R(1, 2), R(1, 2))]
check(rank_K(quad_rows(FR), 1) == 7, 'P2c the octahedron frustum (half octahedron cut at half height, 8 corners) is self-associated (rank 7)')
# REFEREE (2): the claim holds for hexahedra of CUBE TYPE only. The other 8-corner hexahedron, a tetrahedron with two corners cut off
# (2 triangles, 2 quadrilaterals, 2 pentagons), is not self-associated
def cut2(s0, s1):
    out = []
    for i, v in enumerate(TV):
        si = {0: s0, 1: s1}.get(i)
        if si is None: out.append(tuple(Fr(t) for t in v)); continue
        out += [tuple(Fr(v[k_]) + si * (w[k_] - v[k_]) for k_ in range(3)) for j, w in enumerate(TV) if j != i]
    return out
CUTS = {}
for s0, s1 in [(Fr(1, 4), Fr(1, 4)), (Fr(1, 4), Fr(1, 8))]:
    P_ = cut2(s0, s1); _, Fc = DS.hull_faces(np.array([[float(t) for t in p_] for p_ in P_]))
    CUTS[f'{s0},{s1}'] = {'corners': len(P_), 'face_sizes': sorted(len(f) for f in Fc), 'quadric_rank': rank_K(quad_rows(P_), 1), 'stable': stable8(P_, 1)}
OUT['P2']['gale_cut_tetrahedra'] = CUTS
check(all(c_['corners'] == 8 and c_['face_sizes'] == [3, 3, 4, 4, 5, 5] and c_['quadric_rank'] == 8 and c_['stable'] for c_ in CUTS.values()),
      f'P2c [Gale, not every hexahedron] two tetrahedra with two corners cut (faces 3,3,4,4,5,5; stable): quadric rank 8, NOT self-associated: {CUTS}')
_, Ffr = DS.hull_faces(np.array([[float(t) for t in p_] for p_ in FR]))
check(all(GALE[k_]['stable'] for k_ in GALE) and stable8(FR, 1) and sorted(len(f) for f in Ffr) == [4] * 6,
      f'P2c every 8-point set tested is STABLE (no two equal, no four on a line, no six in a plane), so the quadric-rank test decides self-association (Eisenbud-Popescu Cor. 7.4); the self-associated hexahedra are all of cube type (frustum faces {sorted(len(f) for f in Ffr)})')
nb_ = sp.Matrix([0, 0, -1]); nl = sp.Matrix([1, 1, 1]); nt = sp.Matrix([0, 0, 1]); nl2 = sp.Matrix([1, -1, 1])
cosang = lambda n1, n2: sp.radsimp(-(n1.T * n2)[0] / sp.sqrt((n1.T * n1)[0] * (n2.T * n2)[0]))
check(is0(cosang(nb_, nl) - 1 / s3) and is0(cosang(nt, nl) + 1 / s3) and is0(cosang(nl, nl2) + R(1, 3)),
      'P2c its dihedral angles: base pi/2 - g/2, top pi/2 + g/2, sides pi - g (cos 1/sqrt3, -1/sqrt3, -1/3; g = arccos(1/3) = 2 beta, beta = arctan(1/sqrt2))')
DF = 4 * s2 * R(-1, 2) + 4 * (s2 / 2) * R(1, 2) + 4 * (s2 / 2) * (-1)
check(not is0(DF), f'P2c so Dehn(frustum) = {sp.simplify(DF)} (x) arccos(1/3) = -6 sqrt2 (x) beta != 0: a Gale fixed point that cannot fill space (Dehn; Debrunner 1980): Gale fixedness forces no tiling')
# hexagonal discs (convex solids: disc planes = central planes cutting no face)
def discs_convex(sid):
    D, P = exact_corners(sid)
    if P is None: return None
    O = [sum(p[i] for p in P) / len(P) for i in range(3)]; Q = [tuple(sp.radsimp(p[i] - O[i]) for i in range(3)) for p in P]
    F = ld(REG[sid]['F']); planes = {}
    for i, j in itertools.combinations(range(len(Q)), 2):
        n = sp.Matrix(Q[i]).cross(sp.Matrix(Q[j])).applyfunc(sp.radsimp)
        if all(is0(t) for t in n): continue
        fl = [float(t) for t in n]; mx = max(range(3), key=lambda t: abs(fl[t])); keyp = tuple(round(fl[t] / fl[mx], 9) for t in range(3))
        if keyp in planes: continue
        sgn = [0 if is0((n.T * sp.Matrix(q))[0]) else (1 if float((n.T * sp.Matrix(q))[0]) > 0 else -1) for q in Q]
        if any(min(sgn[t] for t in f) < 0 < max(sgn[t] for t in f) for f in F): continue
        if any(all(sgn[t] == 0 for t in f) for f in F): continue
        on = [Q[t] for t in range(len(Q)) if sgn[t] == 0]
        if len(on) >= 3: planes[keyp] = (n, on)
    return D, planes
HEX = {}
for sid in ['CUBOCTAHEDRON', 'TETRAKIS_HEXAHEDRON'] + ([] if PILOT else ['J15_ELONGATED_SQUARE_BIPYRAMID', 'J91_BILUNABIROTUNDA']):
    r = discs_convex(sid)
    if r is None: note(f'P2c {sid}', 'not recognised'); continue
    D, planes = r; sizes = {}; onconic = []
    for keyp, (n, on) in planes.items():
        sizes[len(on)] = sizes.get(len(on), 0) + 1
        if len(on) == 6:
            nn_ = [float(t) for t in n]; b1 = sp.Matrix(on[0]); b2 = sp.Matrix(n).cross(b1)
            pts = [((sp.Matrix(p).T * b1)[0], (sp.Matrix(p).T * b2)[0]) for p in on]
            M6 = [[u_ ** 2, u_ * v_, v_ ** 2, u_, v_, 1] for u_, v_ in pts]
            onconic.append(rank_K(M6, D) <= 5)
    HEX[sid] = {'disc_sizes': sizes, 'hexagon_discs_on_a_conic': onconic}
    find(f'P2c {sid}: discs {sizes} (float census agrees: see fans-law); hexagonal discs on a conic (Gale self-associated, Coble): {onconic}')
OUT['P2']['gale_hexagon_discs'] = HEX
check(HEX.get('CUBOCTAHEDRON', {}).get('disc_sizes') == {6: 4} and all(HEX['CUBOCTAHEDRON']['hexagon_discs_on_a_conic']),
      'P2c cuboctahedron: 4 hexagon discs, each on a conic: Gale fixed points; yet its Dehn invariant is 24 sqrt2 (x) beta != 0 (chat-handoff, k = 0): no tiling forced')
# Alexander duality screen: fixed point needs V = F (self-dual), |S| = E/2 disc edges, chi(S) = 1
NC = json.load(open(os.path.join(STUD, '2026-11-13-platonic-fans-law', 'data', 'fans-nonconvex.json')))['rows']
cand = []; vf = 0
for r in NC:
    s = REG[r['id']]; V = ld(s['V']); F = ld(s['F'])
    E = {frozenset((f[i], f[(i + 1) % len(f)])) for f in F for i in range(len(f))}
    on = sum(int(k_) * v_ for k_, v_ in r['float_rule'].items())
    if len(V) == len(F):
        vf += 1
        if 2 * on == len(E): cand.append(r['id'])
check(cand == [], f'P2c Alexander duality S -> (E minus S)* (disc edges to the dual graph): a fixed point needs V = F and |S| = E/2; of the {vf} registry solids with V = F none has |S| = E/2 (gyrobifastigium 4 of 14, bilunabirotunda 12 of 26): NONE')
tab('P2', 'Gale duality', fixed='self-associated in Coble\'s sense (stable sets; Eisenbud-Popescu Cor. 7.4): the corners of every hexahedron of CUBE TYPE with planar faces (opposite-face net); not the tetrahedron with two corners cut (rank 8), the gyrobifastigium or the triakis tetrahedron; hexagonal discs on a conic (cuboctahedron, tetrakis hexahedron, ...)',
    forced='none: the octahedron frustum is self-associated with Dehn -3 sqrt2 (x) arccos(1/3) = -6 sqrt2 (x) beta; the cuboctahedron has Gale-fixed discs and Dehn != 0', verdict='NONE')
tab('P2', 'Alexander duality', fixed='S -> (E minus S)* needs a chosen self-duality of the solid (V = F is only the screen) and half the edges on discs: no registry solid', forced='-', verdict='NONE: no fixed point in the registry (planar duality: Whitney 1932; Alexander 1922 is the homological statement behind chi(S) = 1)')

# =====================================================================================================================
# PART 2d. CHIRALITY
# =====================================================================================================================
progress(8, 'P2d: chirality: Narcissus, Covenant, the twist family, the chiral fives')
Hh = sp.sqrt(R(2, 3))
NAR = [(0, 0, 0), (0, 1 / s3, -Hh / 2), (0, 1 / s3, 0), (R(1, 2), -1 / (2 * s3), -Hh / 2), (R(1, 2), -1 / (2 * s3), 0), (R(1, 2), 1 / (2 * s3), -Hh),
       (R(1, 2), s3 / 2, 0), (1, 0, 0), (1, 1 / s3, -Hh / 2), (1, 1 / s3, 0)]
cN = (R(1, 2), 1 / (2 * s3), 0)
NAR = [tuple(sp.radsimp(sp.sympify(p[i]) - cN[i]) for i in range(3)) for p in NAR]
def rotz(th_c, th_s, p): return (sp.radsimp(th_c * p[0] - th_s * p[1]), sp.radsimp(th_s * p[0] + th_c * p[1]), p[2])
def refl_v(ang, p):   # mirror in the vertical plane at angle ang (cos 2ang, sin 2ang exact)
    c2, s2a = sp.cos(2 * ang), sp.sin(2 * ang); return (sp.radsimp(c2 * p[0] + s2a * p[1]), sp.radsimp(s2a * p[0] - c2 * p[1]), p[2])
def same_set(P, Q):
    if len(P) != len(Q): return False
    return all(any(all(is0(p[i] - q[i]) for i in range(3)) for q in Q) for p in P)
def dedup(P):
    out = []
    for p in P:
        if not any(all(is0(p[i] - q[i]) for i in range(3)) for q in out): out.append(p)
    return out
mir = [k for k in range(6) if same_set([refl_v(sp.pi * k / 6, p) for p in NAR], NAR)]
check(len(mir) == 3, f'P2d Narcissus: exactly 3 vertical mirror planes (at {[30 * k for k in mir]} deg): achiral, a FIXED point of the mirror swap')
flip = [(p[0], p[1], -p[2]) for p in NAR]
def union(cth, sth): return [p for p in NAR] + [rotz(cth, sth, q) for q in flip]
TC = dedup(union(1, 0)); CV = dedup(union(R(1, 2), s3 / 2))
check(len(CV) == 14 and same_set([tuple(-t for t in p) for p in CV], CV), 'P2d Covenant (turned 60 deg): 14 corners, centrally symmetric about the hexagon centre: achiral, a fixed point')
impro = [lambda p, k=k: refl_v(sp.pi * k / 6, p) for k in range(6)] + [lambda p, k=k: (lambda q: (q[0], q[1], -q[2]))(rotz(sp.cos(sp.pi * k / 3), sp.sin(sp.pi * k / 3), p)) for k in range(6)]
tc_ach = [i for i, f in enumerate(impro) if same_set([f(p) for p in TC], TC)]
find(f'P2d twisted cube (straight join): improper symmetries among the 12 axis-preserving candidates: {len(tc_ach)} -> {"achiral" if tc_ach else "chiral"}')
# twist family U(theta) = N cup R_theta(flip N): the mirror maps theta -> -theta; theta = 0 and 60 deg are fixed (3-fold symmetry)
Cs, Ss = sp.symbols('C S', real=True)
def S_l(l, Cv, Sv, deriv=0):
    P = NAR + [rotz(Cs, Ss, q) for q in flip]
    nrm2 = [sp.radsimp(sum(t ** 2 for t in p)) for p in NAR + flip]
    tot = 0
    Pl = sp.legendre(l, sp.Symbol('q'))
    for i in range(len(P)):
        for j in range(len(P)):
            if (i < 10) == (j < 10): continue        # pairs within one half do not depend on theta
            cg = sum(P[i][k_] * P[j][k_] for k_ in range(3)) / sp.sqrt(nrm2[i] * nrm2[j])
            tot += Pl.subs(sp.Symbol('q'), cg)
    if deriv == 1: tot = sp.diff(tot, Cs) * (-Ss) + sp.diff(tot, Ss) * Cs
    if deriv == 2:
        d1 = sp.diff(tot, Cs) * (-Ss) + sp.diff(tot, Ss) * Cs; tot = sp.diff(d1, Cs) * (-Ss) + sp.diff(d1, Ss) * Cs
    return sp.radsimp(sp.expand(tot.subs({Cs: Cv, Ss: Sv})))
PAL = {}
for l in ([4] if PILOT else [4, 6]):
    d0 = S_l(l, 1, 0, 1); d60 = S_l(l, R(1, 2), s3 / 2, 1); dr = S_l(l, R(3, 5), R(4, 5), 1)
    s0 = S_l(l, 1, 0, 2); s60 = S_l(l, R(1, 2), s3 / 2, 2)
    PAL[l] = {'d/dtheta at 0': str(d0), 'at 60': str(d60), 'at random (cos 3/5)': str(sp.nsimplify(dr)), 'second at 0': float(s0), 'second at 60': float(s60)}
    check(is0(d0) and is0(d60) and not is0(dr), f'P2d [mirror evenness, FORCED; the simplest case of Palais 1979] twist family: the degree-{l} corner tone is critical at the straight join and at Covenant (fixed points of theta -> -theta), not at a random twist (cos = 3/5); second derivatives {float(s0):.4f}, {float(s60):.4f}')
OUT['P2']['twist_family'] = PAL
# the chiral fives: the two compounds of five tetrahedra in the dodecahedron
DOD = [p for p in itertools.product((1, -1), repeat=3)] + [q for base in [(0, 1 / phi, phi)] for q in
       [tuple(sg[k_] * base[(k_ + c_) % 3] for k_ in range(3)) for c_ in range(3) for sg in itertools.product((1, -1), repeat=3)]]
DOD = dedup([tuple(sp.radsimp(sp.sympify(t)) for t in p) for p in DOD])
d2 = lambda p, q: sp.radsimp(sum((p[i] - q[i]) ** 2 for i in range(3)))
adj = {(i, j) for i, j in itertools.combinations(range(20), 2) if is0(d2(DOD[i], DOD[j]) - 8)}
tets = [c_ for c_ in itertools.combinations(range(20), 4) if all(pr in adj for pr in itertools.combinations(c_, 2))]
comps = [c_ for c_ in itertools.combinations(tets, 5) if len(set(itertools.chain(*c_))) == 20]
check(len(DOD) == 20 and len(tets) == 10 and len(comps) == 2, 'P2d the dodecahedron holds 10 regular tetrahedra and exactly 2 compounds of five (the chiral fives)')
idx = {tuple(map(str, p)): i for i, p in enumerate(DOD)}
neg = lambda t: frozenset(next(j for j in range(20) if all(is0(DOD[j][k_] + DOD[i][k_]) for k_ in range(3))) for i in t)
L5, R5_ = [set(map(frozenset, c_)) for c_ in comps]
check({neg(t) for t in L5} == R5_, 'P2d the central inversion (improper) maps one five onto the other: they are mirror images, swapped by the chirality swap')
check(all(is0(sum(DOD[i][k_] for i in t)) for t in tets for k_ in range(3)),
      'P2d each tetrahedron is centred at the origin, so its face normals are its negated corners: each five has as face normals all 20 three-fold directions')
argued('P2d so both fives have the SAME 20 face planes and the same core, which is therefore mirror-symmetric: the regular icosahedron (forced by the orbit: the 20 three-fold directions are an achiral set)')
tab('P2', 'chirality', fixed='Narcissus (3 mirrors), Covenant (centre), the common core of the chiral fives (icosahedron); the twisted cube per test',
    forced='every battery quantity is O(3)-invariant, hence even under the mirror: nothing vanishes; in the twist family the mirror acts as theta -> -theta and every DIFFERENTIABLE mirror-invariant quantity is critical at the straight join and at Covenant (an even differentiable function; the simplest case of Palais 1979); hull volume, Mahler volume, roundness or wall area may have a corner there instead; the fives\' common core is forced achiral',
    verdict='FORCED: criticality only, for differentiable quantities; no new law')

# =====================================================================================================================
# PART 3. CYCLES (HOPS): periodic points
# =====================================================================================================================
progress(9, 'P3: periodic points of the hops')
sF = sp.symbols('s')
Mf = sp.Matrix([[0, 1], [1, 1]]); ok = True
for k in range(1, 21):
    Mk = Mf ** k; poly = sp.expand(Mk[1, 0] * sF ** 2 + (Mk[1, 1] - Mk[0, 0]) * sF - Mk[0, 1])
    ok &= is0(sp.expand(poly - Mk[1, 0] * (sF ** 2 + sF - 1)))
check(ok and (Mf ** 2).trace() == 3, 'P3 [#69] Fibonacci hop s -> 1/(1+s): the fixed points of every iterate (k <= 20) are the roots of F_k (s^2 + s - 1): periodic points = the two fixed points 1/phi, -phi; M^2 is hyperbolic (trace 3), so no other period exists')
tab('P3', '#69 Fibonacci hop', periodic='only the fixed points 1/phi (share) and -phi (off the interval)', forced='the share 1/phi^2 at the fixed point (already #69); no reversing swap is geometric', verdict='NONE new')
# DICTO's growth rule T(S) = {x : v.x <= v.v}: on shapes it is polar reciprocation, an involution up to scale
def T_of(V):
    P = [(list(v), sp.radsimp(sum(t * t for t in v))) for v in V]; W, _ = polytope(P); return [tuple(sp.radsimp(t) for t in w) for w in W]
TET = [tuple(sp.Integer(t) for t in v) for v in TV]
CUB = [tuple(sp.Integer(t) for t in v) for v in itertools.product((1, -1), repeat=3)]
T1 = T_of(TET)
check(same_set(T1, [tuple(-3 * t for t in v) for v in TET]), 'P3 [#80] T(tetrahedron) = -3 x tetrahedron: a FIXED point of T on shapes (one step, factor 3 = R/r; two steps 9)')
T2 = T_of(T_of(CUB)); check(same_set(T2, [tuple(3 * t for t in v) for v in CUB]), 'P3 [#80] T(T(cube)) = 3 x cube (gain 3): cube <-> octahedron, period 2')
if not PILOT:
    T2D = T_of(T_of(DOD)); g = 15 - 6 * s5
    check(same_set(T2D, [tuple(sp.radsimp(g * t) for t in v) for v in DOD]), 'P3 [#80] T(T(dodecahedron)) = (15 - 6 sqrt5) x dodecahedron: D <-> I, period 2')
argued('P3 [#80] so on solids whose corners all lie on one sphere about the centre (R the same for every corner), T is polar reciprocation up to the scale R^2; T^2 is a scaled copy only when T(S) is again sphere-inscribed (the Platonic solids; an Archimedean solid goes to a Catalan solid, which is not); the tetrahedron is A fixed point on shapes up to the point reflection (every sphere-inscribed self-polar solid is one), where the law reads gain = 3^2 = 9, the main theorem restated')
tab('P3', '#80 growth rule T', periodic='only on solids with all corners on one sphere about the centre is T a scaled polar; period 2 when the image is again sphere-inscribed (the Platonic solids); the tetrahedron: period 1 up to the point reflection (a fixed point, not the only one: every sphere-inscribed self-polar solid)', forced='gain = (R\'/R)^2 (the main theorem); at the fixed point 3^2 = 9, a restatement', verdict='RECLASSIFIED: a swap modulo scale on sphere-inscribed solids; no new law')
argued('P3 [pentakis 4-cycle] lemma (exact, by orbit sizes 12, 20, 30, 60, 120 of the icosahedral group on directions): an I_h-invariant polytope with 12 facets is a regular dodecahedron, with 20 facets a regular icosahedron (the only orbits of those sizes are the 5-fold and 3-fold axes, one distance each)')
tab('P3', 'pentakis four-step cycle (twin-vacuus)', periodic='every pentakis start (Catalan; pyramid heights h): period 4 on the twin side, D_{k+4} = c D_k with c in Q(sqrt5) (cited, exact there)',
    forced='the twin hulls at k = 0, 2 are a REGULAR dodecahedron and icosahedron for every start: forced by I_h symmetry and the facet counts 12 and 20 (lemma); the counts themselves are observed', verdict='FORCED (classical symmetry lemma) for an observed regularity; no new law')
tab('P3', 'golden cycles x phi^3 (#38a), crossed golden loop, nest by thirds (#99)', periodic='every member, in shape space (I <-> D period 2; icosahedron period 1 in the crossed loop); none as solids (scale != 1)',
    forced='the cycles are polarity (or a fixed nest) composed with a golden or rational scale; no involution of the cycle fixes a member with a new law', verdict='NONE')
tab('P3', 'OG chain', periodic='none: the OG family does not cycle and has no gnomon polynomial (twin-vacuus, og-margin)', forced='-', verdict='NONE')

# =====================================================================================================================
progress(11, 'writing')
nf = sum(1 for c_ in CHECKS if not c_[0])
OUT['checks'] = [[bool(a_), b__, c_] for a_, b__, c_ in CHECKS]; OUT['argued'] = ARGUED; OUT['seconds'] = round(time.time() - T_START)
OUT['counts'] = {'computed_checks': len(CHECKS), 'computed_fail': nf, 'argued_statements': len(ARGUED)}
json.dump(OUT, open(os.path.join(DATA, 'missing-pilot.json' if PILOT else 'missing.json'), 'w'), indent=1, default=str)
print(f'{len(CHECKS)} computed checks, {nf} FAIL; {len(ARGUED)} statements proved by argument (listed as arg, not counted as checks); {time.time() - T_START:.0f} s')
print('FINAL ok' if nf == 0 else 'FINAL FAIL')
