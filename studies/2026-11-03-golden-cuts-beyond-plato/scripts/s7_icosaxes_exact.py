"""Step 7. Exact recheck of #88's claim that Icosaxes is the 120-cell's vertex-first section at phi/2 of the way to the
tip (atlas height 11/8 + 5 sqrt5/8). #88 compared it in floating point (two_checks.py, 10^-15); this redoes it exactly.

Method (all arithmetic exact in Q(sqrt5), q5.Q5 over Fractions; floats only propose the vertex matching):
 1. the section's corners, exactly, in 4D: the 120-cell corners at height h plus the crossing points of the edges that
    pass strictly through the hyperplane (every such point is a corner of the section: faces of P n H are F n H);
 2. two targets, exactly: Icosaxes from DICTO Solids v7 (exact coordinates) and, independently, the octahedron
    |x|+|y|+|z| = 1 cut at x = 1/phi^2 of its edge (#88's Greater Golden Cut Octahedron);
 3. a bijection section -> target found by backtracking on float distances, then verified EXACTLY: one factor lam with
    |f(p) - f(q)|^2 = lam |p - q|^2 for all pairs. A bijection of finite point sets scaling all distances by one factor
    is a similarity (it extends to an isometry of the affine hulls after scaling), so this proves congruence up to scale.
    Also the house invariant (sorted squared distances over their sum) is compared exactly.
usage (compute-host): python3 s7_icosaxes_exact.py -> ../data/s7-icosaxes-exact.json
"""
import sys, os, json, itertools
from fractions import Fraction as Fr
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, '..', 'data')
SC = os.path.expanduser('~/work/studies/2026-10-27-white-queen-polar/scripts')
sys.path.insert(0, SC); cwd = os.getcwd(); os.chdir(SC)
import atlas120 as A
os.chdir(cwd)
Q5, q5str = A.Q5, A.q5str
CHECKS = []
def check(name, ok):
    CHECKS.append({'check': name, 'pass': bool(ok)}); print(('PASS ' if ok else 'FAIL ') + name, flush=True)


def d2(p, q):
    s = Q5(0)
    for a, b in zip(p, q):
        s = s + (a - b) * (a - b)
    return s


def to_q5(s):
    e = sp.nsimplify(sp.sympify(s)); e = sp.expand(e)
    b = e.coeff(sp.sqrt(5)); a = sp.expand(e - b * sp.sqrt(5))
    assert a.is_Rational and b.is_Rational, s
    return Q5(Fr(int(a.p), int(a.q)), Fr(int(b.p), int(b.q)))


# 1. the section, exact
lab = 'vertex-first'; d = A.DIRS[lab][0]; H = [A.dot(p, d) for p in A.R]
tip = max(H, key=float)
h = Q5(Fr(1, 4), Fr(1, 4)) * tip                       # phi/2 of the way from the centre to the tip
check(f'height h = (phi/2) tip = {q5str(h)} (#88: 11/8 + 5/8 sqrt5)', h == Q5(Fr(11, 8), Fr(5, 8)))
on = [p for p, x in zip(A.R, H) if x == h]
cross = []
for a, b in A.E:
    ha, hb = H[a], H[b]
    if ((ha - h) * (hb - h)).sign() < 0:
        t = (h - ha) / (hb - ha); cross.append(tuple(x + t * (y - x) for x, y in zip(A.R[a], A.R[b])))
S = list(dict.fromkeys(on + cross))
check(f'section corners: {len(on)} 120-cell corners on the hyperplane + {len(cross)} edge crossings = {len(S)} distinct points', len(S) == 24)
check('all section points lie on the hyperplane (exact)', all(A.dot(p, d) == h for p in S))

# 2. targets, exact
w = json.load(open(os.path.expanduser('~/work/dataset-v7/solids/dicto-icosaxes.json')))
ICX = [tuple(to_q5(c) for c in v['exact']) for v in w['vertices']]
g2 = Q5(Fr(3, 2), Fr(-1, 2))                            # 1/phi^2 = (3 - sqrt5)/2
OCT = [tuple(Q5(s if i == k else 0) for k in range(3)) for i in range(3) for s in (1, -1)]
OE = [(i, j) for i, j in itertools.combinations(range(6), 2) if d2(OCT[i], OCT[j]) == Q5(2)]
GGCO = [tuple(p + g2 * (q - p) for p, q in zip(OCT[i], OCT[j])) for i, j in OE] + \
       [tuple(q + g2 * (p - q) for p, q in zip(OCT[i], OCT[j])) for i, j in OE]
check(f'targets: Icosaxes (dataset v7) {len(ICX)} corners, octahedron cut at 1/phi^2 {len(GGCO)} corners', len(ICX) == 24 and len(GGCO) == 24)


def match(P, T):
    """Backtracking bijection P -> T preserving float distances up to one scale; returns the index map or None."""
    n = len(P); DP = [[float(d2(P[i], P[j])) for j in range(n)] for i in range(n)]
    DT = [[float(d2(T[i], T[j])) for j in range(n)] for i in range(n)]
    sP = max(max(r) for r in DP); sT = max(max(r) for r in DT); k = sT / sP
    f = [None] * n; used = [False] * n
    def go(i):
        if i == n: return True
        for c in range(n):
            if used[c]: continue
            if all(abs(DT[c][f[j]] - k * DP[i][j]) < 1e-9 * sT for j in range(i)):
                f[i] = c; used[c] = True
                if go(i + 1): return True
                used[c] = False
        return False
    return f if go(0) else None


def invariant(P):
    D = [d2(p, q) for p, q in itertools.combinations(P, 2)]; tot = sum(D, Q5(0))
    return sorted((x / tot for x in D), key=float)


out = {'section': {'polytope': '120-cell', 'direction': lab, 'atlas_height': q5str(h), 'tip': q5str(tip),
                   'h_over_tip': 'phi/2 = 1/4 + sqrt5/4', 'corners_on_layer': len(on), 'edge_crossings': len(cross),
                   'corners_exact_4d': [[q5str(c) for c in p] for p in S]}}
for name, T in (('Icosaxes (DICTO Solids v7, exact)', ICX), ('octahedron cut at x = 1/phi^2 (Greater Golden Cut Octahedron)', GGCO)):
    f = match(S, T)
    check(f'{name}: float matching found', f is not None)
    if f is None:
        out[name] = {'congruent_exact': False}; continue
    lam = d2(T[f[0]], T[f[1]]) / d2(S[0], S[1])
    allpairs = all(d2(T[f[i]], T[f[j]]) == lam * d2(S[i], S[j]) for i, j in itertools.combinations(range(len(S)), 2))
    check(f'{name}: all 276 squared distances equal section x {q5str(lam)} exactly (similarity, exact)', allpairs)
    inv_ok = all(x == y for x, y in zip(invariant(S), invariant(T)))
    check(f'{name}: house invariant (sorted squared distances over their sum) equal exactly', inv_ok)
    out[name] = {'congruent_exact': bool(allpairs and inv_ok), 'scale_squared_target_over_section': q5str(lam),
                 'bijection_section_to_target': f}
ok = all(c['pass'] for c in CHECKS)
out['verdict'] = ('HOLDS: Icosaxes is exactly (in Q(sqrt5)) the 120-cell vertex-first section at phi/2 of the way to the tip'
                  if ok else 'FAILS: see checks')
json.dump({'result': out, 'checks': CHECKS}, open(os.path.join(DATA, 's7-icosaxes-exact.json'), 'w'), indent=1)
print(out['verdict']); print(f'{sum(c["pass"] for c in CHECKS)}/{len(CHECKS)} checks passed')
