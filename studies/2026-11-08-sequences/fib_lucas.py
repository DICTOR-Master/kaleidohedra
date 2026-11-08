"""Which exact volumes in DICTO's dataset (v8) are a rational multiple of a power of the golden ratio?
phi^n = (L_n + F_n sqrt5)/2 (Lucas, Fibonacci). A volume a + b sqrt5 (a, b rational, b != 0) equals q * phi^n exactly
iff a/b = L_n/F_n (n > 0) or a/b = -L_n/F_n (phi^-n = (-1)^n (L_n - F_n sqrt5)/2). Also pairs of solids from one paper whose
volume RATIO is +-phi^n. Exact arithmetic with Fractions; no floats decide anything."""
import json, glob, os, re, sys
from fractions import Fraction as Fr
import sympy
DS = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/k-mathdata/studies/2026-10-22-math-data-dicto-solids/solids')
F = [0, 1]; L = [2, 1]
for _ in range(80): F.append(F[-1] + F[-2]); L.append(L[-1] + L[-2])
def ab(expr):
    e = sympy.nsimplify(sympy.sympify(expr)) if False else sympy.expand(sympy.sympify(expr))
    a = b = Fr(0)
    for t, c in e.as_coefficients_dict().items():
        c = Fr(int(sympy.Rational(c).p), int(sympy.Rational(c).q))
        if t == 1: a += c
        elif t == sympy.sqrt(5): b += c
        else: return None
    return a, b
def phi_power(a, b):
    """return (q, n) with a + b sqrt5 = q phi^n, q rational, or None"""
    if b == 0: return (a, 0) if a else None
    r = a / b
    for n in range(1, 80):
        if r == Fr(L[n], F[n]): return (2 * b / F[n], n)
        if r == Fr(-L[n], F[n]): return (2 * b * (-1) ** (n + 1) / F[n], -n)
    return None
def mul(x, y): return (x[0] * y[0] + 5 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])
def check(a, b, q, n):   # verify q*phi^n == a + b sqrt5 exactly
    p = (Fr(1, 2), Fr(1, 2)); inv = (Fr(-1, 2), Fr(1, 2))  # phi, 1/phi = (sqrt5-1)/2
    v = (Fr(1), Fr(0)); base = p if n >= 0 else inv
    for _ in range(abs(n)): v = mul(v, base)
    return (q * v[0], q * v[1]) == (a, b)
rows = []; vols = {}
for f in sorted(glob.glob(os.path.join(DS, '*.json'))):
    if 'unit-volume' in f: continue
    j = json.load(open(f))
    if j['field'] not in ('Q(sqrt(5))', 'Q'): continue
    v = j['volume']['exact'] if isinstance(j['volume'], dict) else j['volume']
    r = ab(v)
    if r is None: continue
    vols[j['name']] = (r, j.get('paper', ''))
    pp = phi_power(*r)
    if pp and pp[1] != 0:
        q, n = pp
        assert check(r[0], r[1], q, n), j['name']
        rows.append((j['name'], j.get('paper', ''), str(q), n))
print('SOLIDS whose volume is a rational multiple of phi^n (n != 0):', len(rows), 'of', len(vols))
for name, paper, q, n in sorted(rows, key=lambda x: (str(x[1]), x[0])):
    Ln, Fn = L[abs(n)], F[abs(n)]
    print(f'  {name} ({paper}): volume = {q} * phi^{n}   [phi^{abs(n)} = (L{abs(n)} + F{abs(n)} sqrt5)/2 = ({Ln} + {Fn} sqrt5)/2]')
# pairs within one paper with ratio +-phi^n
print('PAIRS in one paper whose volume ratio is a power of phi:')
names = sorted(vols); seen = 0
for i, x in enumerate(names):
    for y in names[i + 1:]:
        (a1, b1), p1 = vols[x]; (a2, b2), p2 = vols[y]
        if not p1 or p1 != p2: continue
        # ratio (a1 + b1 s)/(a2 + b2 s) = (a1 + b1 s)(a2 - b2 s)/(a2^2 - 5 b2^2)
        den = a2 * a2 - 5 * b2 * b2
        if den == 0: continue
        ra, rb = (a1 * a2 - 5 * b1 * b2) / den, (b1 * a2 - a1 * b2) / den
        pp = phi_power(ra, rb)
        if pp and pp[0] in (1, -1) and pp[1] != 0:
            assert check(ra, rb, pp[0], pp[1]); seen += 1
            print(f'  {p1}: {x} / {y} = {"" if pp[0] == 1 else "-"}phi^{pp[1]}')
print('pairs:', seen)
verified = all(check(*vols[n][0], Fr(q), k) for n, _, q, k in rows)
print('FINAL ok' if verified and len(vols) > 0 else 'FINAL FAIL: a phi-power identity did not re-multiply')
