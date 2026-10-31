# Splash Rules II, approximants, part 1: the Fibonacci chain and its periodic approximants (exact).
# Run on dicto-big-brother: ~/geom/bin/python sturm.py out/
# Letters: 0 = L (long tile), 1 = S (short tile); alpha = share of S. Mechanical word s_n = floor((n+1)a + r) - floor(n a + r).
# For a = p/q (gcd 1) the word has period q (a Christoffel conjugate); r = 1/(2q) is generic (no point n a + r is an integer).
# Everything is a Fraction or an element of Q(sqrt 5) (qf.QF); no floats in any test.
import sys, os, json, math, itertools, random
from fractions import Fraction as Fr
from qf import QF, fl, frac

OUT = sys.argv[1] if len(sys.argv) > 1 else 'out'; os.makedirs(OUT, exist_ok=True)
QMAX = 60; GMAX = 9
PHI = QF(Fr(1, 2), Fr(1, 2), 5); ASTAR = QF(Fr(3, 2), Fr(-1, 2), 5)   # 1/phi^2 = (3 - sqrt5)/2
assert ASTAR * PHI * PHI == 1
log = open(os.path.join(OUT, 'sturm.log'), 'w')
def say(*a):
    s = ' '.join(str(x) for x in a); print(s); log.write(s + '\n'); log.flush()

def word(p, q):
    a, r = Fr(p, q), Fr(1, 2 * q)
    return tuple(math.floor((n + 1) * a + r) - math.floor(n * a + r) for n in range(q))

def factor_counts(w, g):
    q = len(w); c = {}
    for n in range(q):
        f = tuple(w[(n + k) % q] for k in range(g)); c[f] = c.get(f, 0) + 1
    return c

def intervals(a, g):
    """acceptance intervals of the factors of length g at slope a (Fraction or QF): {factor: length}"""
    pts = sorted(set([frac(-k * a) for k in range(g + 1)] + [frac(a * 0)]))
    one = a * 0 + 1
    pts = pts + [one]
    res = {}
    for i in range(len(pts) - 1):
        lo, hi = pts[i], pts[i + 1]
        if hi == lo: continue
        x = (lo + hi) * Fr(1, 2)
        f = tuple(fl(x + (k + 1) * a) - fl(x + k * a) for k in range(g))
        res[f] = res.get(f, 0) + (hi - lo)
    return res

def balanced(w):
    q = len(w)
    for g in range(1, q + 1):
        s = {sum(w[(n + k) % q] for k in range(g)) for n in range(q)}
        if max(s) - min(s) > 1: return False
    return True

def farey(n):
    return sorted({Fr(p, q) for q in range(1, n + 1) for p in range(0, q + 1)})

def lw(f): return ''.join('LS'[x] for x in f)

# ---- 1. the approximants: all p/q, q <= QMAX
fracs = sorted({Fr(p, q) for q in range(2, QMAX + 1) for p in range(1, q) if math.gcd(p, q) == 1})
say('approximants p/q, 2 <= q <=', QMAX, ':', len(fracs))
data = {}
nbad = 0
for a in fracs:
    p, q = a.numerator, a.denominator; w = word(p, q)
    assert sum(w) == p
    assert balanced(w), a
    rec = {}
    for g in range(1, GMAX + 1):
        c = factor_counts(w, g)
        assert len(c) == min(g + 1, q), (a, g, len(c))       # factor complexity of a Christoffel class
        iv = intervals(a, g)
        for f, n in c.items():
            if Fr(n, q) != iv.get(f, 0): nbad += 1
        assert set(iv) == set(c), (a, g)
        assert len(set(c.values())) <= 3                     # three distance theorem: <= 3 frequencies
        rec[g] = {lw(f): Fr(n, q) for f, n in c.items()}
    data[a] = rec
say('checks: balanced, complexity min(g+1, q), interval lengths = exact frequencies (mismatches:', nbad, '), <= 3 values: all', len(fracs))

# ---- 2. Farey cells: every window-g frequency is a straight line in alpha on each cell of the Farey sequence of order g
law = {}
for g in range(1, GMAX + 1):
    F = farey(g); cells = list(zip(F, F[1:]))
    words = sorted({f for a in fracs for f in data[a][g]})
    gl = {}
    for (lo, hi) in cells:
        pts = [a for a in fracs if lo <= a <= hi]
        assert len(pts) >= 3, (g, lo, hi)
        a0, a1 = pts[0], pts[-1]
        for f in words:
            y0, y1 = data[a0][g].get(f, 0), data[a1][g].get(f, 0)
            B = (y1 - y0) / (a1 - a0); A = y0 - B * a0
            for a in pts: assert data[a][g].get(f, 0) == A + B * a, (g, lo, hi, f, a)
            gl.setdefault(f, []).append((lo, hi, A, B))
    # globally linear words?
    glin = [f for f in words if len({(A, B) for (_, _, A, B) in gl[f]}) == 1]
    # kink set: Farey points where some word changes slope
    kinks = sorted({hi for f in words for (x, y) in zip(gl[f], gl[f][1:]) if (x[2], x[3]) != (y[2], y[3]) for hi in [x[1]]})
    law[g] = {'words': words, 'pieces': gl, 'global_lines': glin, 'kinks': kinks, 'cells': len(cells)}
    say(f'g={g}: {len(words)} factors over all slopes; Farey cells {len(cells)}; lines on every cell: yes; globally linear: {glin}; kinks at {[str(k) for k in kinks]}')
    assert set(kinks) == {x for x in F if 0 < x < 1 and x.denominator <= g}

# ---- 3. kink vectors (generalised Swap defects): slope right minus slope left, per factor, at each Farey point
kinkvec = {}
for g in (2, 3, 4):
    words = law[g]['words']
    for x in law[g]['kinks']:
        v = {}
        for f in words:
            L = [B for (lo, hi, A, B) in law[g]['pieces'][f] if hi == x][0]
            R = [B for (lo, hi, A, B) in law[g]['pieces'][f] if lo == x][0]
            if R - L: v[f] = R - L
        kinkvec[(g, x)] = v
        say(f'kink g={g} at {x}:', ', '.join(f'{f} {"+" if d > 0 else ""}{d}' for f, d in sorted(v.items())))

# Swap defect: window-2 count F with values F(LL), F(LS), F(SL), F(SS): kink at 1/2 = 2*Delta
v = kinkvec[(2, Fr(1, 2))]
assert v == {'LL': 2, 'LS': -2, 'SL': -2, 'SS': 2}
say('window 2: kink at 1/2 = 2(F(LL) + F(SS) - F(LS) - F(SL)) = twice the Swap defect')

# ---- 4. the quasicrystal: alpha* = 1/phi^2, exact frequencies in Q(sqrt5); its Farey cell; convergents on the same line
fib = [1, 1]
while fib[-1] < 400: fib.append(fib[-1] + fib[-2])
conv = [Fr(fib[n - 2], fib[n]) for n in range(2, len(fib)) if fib[n] <= 400]
say('convergents F(n-2)/F(n):', [str(c) for c in conv])
limit = {}
for g in range(1, GMAX + 1):
    iv = intervals(ASTAR, g)
    F = farey(g); cell = [(lo, hi) for lo, hi in zip(F, F[1:]) if QF(lo, 0, 5) < ASTAR < QF(hi, 0, 5)][0]
    rows = {}
    for f, L in iv.items():
        f = lw(f)
        A, B = [(A, B) for (lo, hi, A, B) in law[g]['pieces'][f] if (lo, hi) == cell][0]
        assert QF(A, 0, 5) + B * ASTAR == L                       # the limit sits on the cell's line
        rows[f] = (L, A, B)
    assert len(iv) == g + 1 and len({v[0] for v in rows.values()}) <= 3
    on = [c for c in conv if cell[0] <= c <= cell[1]]
    first = min(c.denominator for c in on)
    # all convergents with denominator >= first lie on the cell; none with smaller denominator except endpoints
    assert all(cell[0] <= c <= cell[1] for c in conv if c.denominator >= first)
    limit[g] = {'cell': cell, 'rows': rows, 'first_conv_on_line': first}
    say(f'g={g}: limit cell [{cell[0]}, {cell[1]}]; convergents on the limit line from q = {first}; frequencies:',
        '; '.join(f'{f} {L}  (= {A} + {B}a)' for f, (L, A, B) in sorted(rows.items())))

# phason strain: on the cell, f(p/q) - f(alpha*) = B (p/q - alpha*)
for g in (2, 3, 5):
    for c in conv:
        if c.denominator < limit[g]['first_conv_on_line']: continue
        for f, (L, A, B) in limit[g]['rows'].items():
            cnt = factor_counts(word(c.numerator, c.denominator), g)
            assert QF(Fr(cnt.get(tuple('LS'.index(ch) for ch in f), 0), c.denominator), 0, 5) - L == B * (QF(c, 0, 5) - ASTAR)
say('phason strain: every window-g count of a convergent on the line differs from the limit by B * (p/q - 1/phi^2), exactly')


# convergent F(n-2)/F(n) lies on the limit's window-g line (closed Farey cell of order g) exactly when g < F(n+2)
fibs = [1, 1]
while fibs[-1] < 5000: fibs.append(fibs[-1] + fibs[-2])
for g in range(1, 301):
    lo = max((Fr(math.floor(float(ASTAR) * q), q) for q in range(1, g + 1)))
    hi = min((Fr(math.floor(float(ASTAR) * q) + 1, q) for q in range(1, g + 1)))
    assert QF(lo, 0, 5) < ASTAR < QF(hi, 0, 5)
    for n in range(2, len(fibs) - 2):
        c = Fr(fibs[n - 2], fibs[n])
        assert (lo <= c <= hi) == (g < fibs[n + 2]), (g, c)
say('rule checked for g = 1..300: the approximant F(n-2)/F(n) is on the Fibonacci line of window g iff g < F(n+2)')

# ---- 5. the Window Law plane: all binary necklaces up to length 12 vs the approximants (window 2)
def necklaces(n):
    seen = set(); out = []
    for bits in itertools.product((0, 1), repeat=n):
        rots = [bits[k:] + bits[:k] for k in range(n)]
        m = min(rots)
        if m in seen: continue
        seen.add(m)
        if any(m == m[k:] + m[:k] for k in range(1, n) if n % k == 0): continue   # primitive only
        out.append(m)
    return out
plane = []
for n in range(1, 13):
    for w in necklaces(n):
        h = Fr(sum(w), n); pss = Fr(sum(1 for k in range(n) if w[k] == 1 and w[(k + 1) % n] == 1), n)
        plane.append((h, pss, balanced(w)))
nb = sum(1 for x in plane if x[2])
for h, pss, b in plane:
    assert pss >= max(Fr(0), 2 * h - 1)
    if b: assert pss == max(Fr(0), 2 * h - 1)
lower = [x for x in plane if x[1] == max(Fr(0), 2 * x[0] - 1)]
say(f'necklaces up to 12: {len(plane)} primitive, {nb} balanced (= Christoffel); all balanced on the lower edge p_SS = max(0, 2a - 1); {len(lower)} words on the edge in all')

# ---- write data
def js(x):
    if isinstance(x, Fr): return str(x)
    if isinstance(x, QF): return {'a': str(x.a), 'b': str(x.b), 'sqrt': x.d}
    return x
out = {
    'approximants': {str(a): {g: {f: str(v) for f, v in r.items()} for g, r in rec.items()} for a, rec in data.items()},
    'laws': {g: {'kinks': [str(k) for k in L['kinks']], 'global_lines': L['global_lines'],
                 'pieces': {f: [[str(lo), str(hi), str(A), str(B)] for lo, hi, A, B in ps] for f, ps in L['pieces'].items()}} for g, L in law.items()},
    'kinkvectors': {f'{g}@{x}': {f: str(d) for f, d in v.items()} for (g, x), v in kinkvec.items()},
    'limit': {g: {'cell': [str(c) for c in L['cell']], 'first_conv_on_line': L['first_conv_on_line'],
                  'rows': {f: {'value': js(v[0]), 'A': str(v[1]), 'B': str(v[2])} for f, v in L['rows'].items()}} for g, L in limit.items()},
    'convergents': [str(c) for c in conv],
    'plane': [[str(h), str(p), b] for h, p, b in plane],
}
json.dump(out, open(os.path.join(OUT, 'sturm.json'), 'w'), indent=0)
say('done')
