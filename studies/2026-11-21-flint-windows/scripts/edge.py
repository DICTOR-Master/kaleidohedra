"""One window edge of the chain of T, exactly.  Usage: python edge.py <cube|dodeca> <a> <b> <N> <label>
1. bisect (floating point, N steps) between depths a and b on the closure pattern (j, k) to width 1e-10;
2. carry the type of the low side to the high side in arb balls: the slacks whose certified sign flips there are the wall;
3. find that slack's root s* by the secant method in arb, precision ramped to 6000 bits;
4. integer relation (FLINT LLL) for s* over Q (and over Q(sqrt5) for the dodecahedron), factor (FLINT), isolate the real
   roots of the factor (FLINT certified root isolation), pick the one whose ball meets s*;
5. EXACT CHECK in the number field K = Q[x]/(f): solve the chain at s = x along the type and test that the wall slack is
   exactly zero, and that every tight incidence of the type is exactly zero at x as well.
Output: data/edge-<label>.json and a log ending FINAL ok."""
import sys, json, time
from flint import fmpq, fmpz, arb, fmpq_poly, fmpz_poly, ctx
import fw

kind, a, b, N, label = sys.argv[1], fmpq(*map(int, sys.argv[2].split("/"))), fmpq(*map(int, sys.argv[3].split("/"))), int(sys.argv[4]), sys.argv[5]
t0 = time.time()
def log(*x): print(f'[{time.time() - t0:6.1f}s]', *x, flush=True)

def pattern(s):
    for nudge in (0, 1e-13, -1e-13):
        try:
            cl, cnt, ty = fw.float_closure(kind, float(s) + nudge, N); return cl, cnt, ty
        except AssertionError: pass
    return 'degenerate', None, None
pa, ca, _ = pattern(a); pb, cb, _ = pattern(b)
log(f'START {kind} edge {label}: at {a} closure {pa} counts {ca}; at {b} closure {pb} counts {cb}')
assert pa != pb and 'degenerate' not in (pa, pb), 'no clean change of regime between a and b'
lo, hi = a, b
while hi - lo > fmpq(1, 10 ** 8):
    for m in ((lo + hi) / 2, (2 * lo + hi) / 3, (lo + 2 * hi) / 3):
        p = pattern(m)[0]
        if p != 'degenerate': break
    if p == 'degenerate': log(f'float chain degenerate inside [{float(lo):.10f}, {float(hi):.10f}]: bisection stops here'); break
    if p == pa: lo = m
    elif p == pb: hi = m
    else: log(f'third pattern {p} at {float(m)}'); hi = m
log(f'bisected: edge in [{float(lo):.12f}, {float(hi):.12f}]')

def failing(ty, s, steps, prec=512):
    """free (non-tight) slacks of the carried type that are not certified negative at depth s, first failing step only."""
    ctx.prec = prec
    tv = fw.transport(kind, 'arb', arb(s), ty, steps)
    for kk, (pl, V) in enumerate(tv):
        bad = [(kk, jj, ii) for jj, (tri, T) in enumerate(ty[kk]) for ii in range(len(pl)) if ii not in set(T) and not (fw.slack(pl, V[jj], ii) < 0)]
        if bad: return bad
    return []

def side_type(side_s, other_s, steps):
    """a type read inside this side's regime and certified (arb) valid at a point ss2 within 1e-6 of the bracket end; returns (type, ss2).
    (floating point counts a slack below 1e-10 as tight, so the bisected end can sit just past the true wall)"""
    sgn = 1 if float(side_s) > float(other_s) else -1
    for back in (0, 1e-10, 1e-9, 1e-8, 1e-7, 1e-6):
        ss2 = side_s + sgn * fmpq(int(round(back * 10 ** 12)), 10 ** 12)
        for off in (1e-6, 1e-5, 1e-4, 1e-3, 1e-2):
            away = fmpq(int(round((float(ss2) + sgn * off) * 10 ** 9)), 10 ** 9)
            p, cnt, _ = pattern(away)
            if p == 'degenerate': continue
            _, _, ty = fw.float_closure(kind, float(away), steps)
            if not failing(ty, ss2, steps, 512):
                log(f'type of this side read at {float(away):.9f} (closure {p}); carried in arb, valid at {float(ss2):.13f}')
                return ty, ss2
    return None, None

def locate(ty, x_ok, x_bad, steps):
    for it in range(90):
        m = (x_ok + x_bad) / 2
        if failing(ty, m, steps): x_bad = m
        else: x_ok = m
    return x_ok, x_bad, failing(ty, x_bad, steps)

found_wall = None
SIDES = [('low', (lo, hi, pa[1] if pa else 6)), ('high', (hi, lo, pb[1] if pb else 6))]
if not pa: SIDES.reverse()          # the closing side first: the open side's walls crowd towards the edge
for side, (ss, oo, steps) in SIDES:
    ty, ss = side_type(ss, oo, steps)
    if ty is None: log(f'{side} side: no clean type near the edge'); continue
    if not failing(ty, oo, steps): log(f'{side} side: its type stays valid across the bracket'); continue
    x_ok, x_bad, bad = locate(ty, ss, oo, steps)
    found_wall = (side, ty, steps, x_ok, x_bad, bad); break
assert found_wall, 'no wall found from either side'
side, ty, steps, x_ok, x_bad, flips = found_wall
k, j, i = flips[0]
log(f'wall: type of the {side} side fails at {float(x_bad):.15f}: step {k}, {len(flips)} slacks (one orbit expected); corner {j}, plane {i}')

tri_j = ty[k][j][0]
def det4(rows):
    (a, b, c, d) = rows
    return (a[3] * fw.det3(b[:3], c[:3], d[:3]) - b[3] * fw.det3(a[:3], c[:3], d[:3]) + c[3] * fw.det3(a[:3], b[:3], d[:3])
            - d[3] * fw.det3(a[:3], b[:3], c[:3]))
def F(s):
    # the wall as one determinant: the corner's three planes and the plane i meet in one point (no division at step k,
    # so F stays finite where the corner's own triple degenerates)
    tr = fw.transport(kind, 'arb', s, ty, k, last_only=set())
    planes = tr[k][0]
    return det4([tuple(planes[q][0]) + (-planes[q][1],) for q in tri_j + (i,)])
def Fsl(s):
    tr = fw.transport(kind, 'arb', s, ty, k, last_only={j})
    planes, V = tr[k]; return fw.slack(planes, V[j], i)

def secant(Ff, name):
    x0, x1 = arb(x_ok), arb(x_bad); prev = None
    for bits in (128, 512, 2048, 6400):
        ctx.prec = bits
        if prev: x0 = arb(x1.mid()) + arb(2) ** (-(prev - 60))     # a fresh second point at each precision
        prev = bits
        x0, x1 = arb(x0.mid()), arb(x1.mid()); f0, f1 = Ff(x0), Ff(x1)
        for it in range(80):
            if not (f1.is_finite() and f0.is_finite()) or (f1 - f0).mid() == 0: break
            x2 = arb((x1 - f1 * (x1 - x0) / (f1 - f0)).mid())
            if not x2.is_finite(): break
            x0, f0, x1 = x1, f1, x2; f1 = Ff(x1)
            if abs(x1 - x0).mid() < arb(2) ** (-(bits - 40)): break
    d = abs(x1 - x0).mid()
    accb = 6400 if d == 0 else int(-float(d.log()) / 0.6931471805599453) if d.is_finite() else 0
    log(f'secant on the {name}: s* = {x1.mid().str(30)}, root known to about {accb} bits')
    return x1, accb
cands = [secant(F, 'wall determinant'), secant(Fsl, 'corner slack')]
alpha, accb = max(cands, key=lambda c: c[1])
assert min(float(lo), float(hi)) - 1e-12 <= float(alpha.mid()) <= max(float(lo), float(hi)) + 1e-12, 'root outside the bracket'
B = min(6000, accb - 64)
log(f'integer relations searched at {B} bits')

# integer relation (any relation found is only a candidate: the exact check in K below is the proof)
found = None
for d in list(range(1, 25)) + list(range(26, 61, 2)):
    if 8 * (d + 1) > B // 2: break
    v = fw.guess_poly(alpha, d, B)
    p = fmpz_poly(v)
    if p.degree() < 1: continue
    ctx.prec = B + 400
    val = abs(sum((arb(c) * alpha ** e for e, c in enumerate(v)), arb(0)))
    height = max(abs(c) for c in v)
    if val < arb(2) ** (-(B * 4 // 5)) and height.bit_length() * (d + 1) < B // 2:   # a genuine relation is far below LLL's floor
        found = p; log(f'relation at degree {d}: height {height.bit_length()} bits, residual < 2^-{B * 4 // 5}'); break
assert found is not None, f'no integer relation up to the degree reachable at {B} bits'
fac = found.factor()[1]
ctx.prec = 6400
cands = []
for g, m in fac:
    for r, mult in g.complex_roots():
        if abs(float(r.imag.mid())) < 1e-30 and abs(float((r.real - alpha).mid())) < 1e-40: cands.append((g, r))
assert len(cands) == 1, f'expected one factor root at s*, got {len(cands)}'
f, root = cands[0]
log(f'minimal polynomial (degree {f.degree()}): {f}')
ctx.prec = 200
reals = [r for r, mult in f.complex_roots() if r.imag.mid() == 0 or abs(float(r.imag.mid())) < 1e-40]
log(f'real roots of f: {[r.real.mid().str(15) for r in reals]}')

# exact check in K = Q[x]/(f)
fw.NF.f = fmpq_poly(f.coeffs())
q5root = None
if kind == 'dodeca' and f.degree() <= 2:
    c = [fmpq(int(x)) for x in f.coeffs()]
    if f.degree() == 1: q5root = fw.Q5(-c[0] / c[1])
    else:
        disc = c[1] ** 2 - 4 * c[2] * c[0]; w = disc / 5            # roots (-c1 +- sqrt(disc)) / (2 c2); in Q(sqrt5) iff disc/5 is a square
        num, den = w.p, w.q
        rn, rd = fmpz(num).sqrtrem() if num >= 0 else (None, 1), fmpz(den).sqrtrem()
        if rn is not None and rn[1] == 0 and rd[1] == 0:
            t = fmpq(rn[0], rd[0])
            for sg in (1, -1):
                z = fw.Q5(-c[1] / (2 * c[2]), sg * t / (2 * c[2]))
                if abs(float(z) - float(alpha.mid())) < 1e-20: q5root = z
if q5root is not None:
    log(f'the root lies in Q(sqrt5): s* = {q5root.a} + ({q5root.b}) sqrt5; exact check in Q(sqrt5)')
elif kind == 'dodeca':
    if f.degree() == 1:
        fw.NF.SQ5 = None
    sq = None
    if f.degree() % 2 == 0:
        ctx.prec = 6400
        v = fw.guess_poly(alpha, f.degree() // 2, 6000, with_sqrt5=True)
        e = f.degree() // 2 + 1; g0, g1 = fmpq_poly(v[:e]), fmpq_poly(v[e:])
        if not g1.is_zero():
            fw.NF.SQ5 = fw.NF(g0) * 0 - fw.NF(g0) / fw.NF(g1)
            ok5 = (fw.NF.SQ5 * fw.NF.SQ5 - 5).is_zero()
            ctx.prec = 300
            sgn = sum((arb(c) * alpha ** e for e, c in enumerate(fw.NF.SQ5.p.coeffs())), arb(0))
            log(f'sqrt5 relation {v}: square 5 exactly {ok5}, value {sgn.str(10)}')
            if ok5 and sgn > 0: sq = 'sqrt5 = -g0(x)/g1(x) in K, checked: its square is 5 exactly and its value at s* is +2.236...'
            else: fw.NF.SQ5 = None
    assert fw.NF.SQ5 is not None, 'sqrt5 not found in K (the pair arithmetic K(sqrt5) is not built here)'
    log(sq)
X = fw.NF(fmpq_poly([0, 1]))
fld, sval = ('Q5', q5root) if q5root is not None else ('NF', X)
# exact transport step by step; a corner whose triple is exactly dependent at s* is itself an exact wall (corners merge there)
planes = fw.start_planes(kind, fld, sval); early = None; inc_ok = True; ninc = 0
for kk in range(k):
    V = []
    for jj, (tri, T) in enumerate(ty[kk]):
        if fw.det3(*[planes[q][0] for q in tri]).is_zero():
            early = (kk, jj); break
        V.append(fw.solve(planes, tri))
    if early: break
    inc_ok = inc_ok and all(fw.slack(planes, V[jj], ii).is_zero() for jj, (tri, T) in enumerate(ty[kk]) for ii in T)
    ninc += sum(len(T) for _, T in ty[kk])
    planes = [(v, fw.dot(v, v)) for v in V]
if early:
    wall = None; tri_det_zero = True; oth_ok = None
    log(f'EXACT at s*: the triple of corner {early[1]} of step {early[0]} is exactly dependent: s* is a wall of step {early[0]} '
        f'(corners merge there; the sign test first saw it at step {k}); tight incidences of steps 0..{early[0] - 1} exactly zero: {inc_ok} ({ninc})')
    exact_ok = inc_ok
else:
    pl = planes
    wall = det4([tuple(pl[q][0]) + (-pl[q][1],) for q in tri_j + (i,)])
    tri_det_zero = fw.det3(*[pl[q][0] for q in tri_j]).is_zero()
    others = [(kk, jj, ii) for (kk, jj, ii) in flips if (kk, jj, ii) != (k, j, i)]
    oth_ok = all(det4([tuple(pl[q][0]) + (-pl[q][1],) for q in ty[k][jj][0] + (ii,)]).is_zero() for kk, jj, ii in others if kk == k)
    log(f'EXACT in K: wall determinant zero: {wall.is_zero()} (the triple of the corner degenerate there: {tri_det_zero}); '
        f'all {ninc} tight incidences of steps 0..{k - 1} zero: {inc_ok}; the other {len(others)} failing slacks (their determinants) zero too: {oth_ok}')
    exact_ok = wall.is_zero() and inc_ok
iso = (root.real.mid() - root.real.rad(), root.real.mid() + root.real.rad())
res = dict(kind=kind, label=label, bracket=[str(lo), str(hi)], pattern_low=str(pa), pattern_high=str(pb), counts_low=ca, counts_high=cb,
           wall=dict(side=side, step=k, corner=j, plane=i, orbit=len(flips)), s_star=alpha.mid().str(60),
           minpoly=str(f), minpoly_coeffs=[int(c) for c in f.coeffs()], degree=f.degree(),
           isolating_interval=[iso[0].str(40, radius=False), iso[1].str(40, radius=False)],
           exact_wall_zero=(None if wall is None else wall.is_zero()), early_wall=early, triple_degenerate=tri_det_zero, exact_incidences=inc_ok, exact_orbit=oth_ok, sqrt5=(None if kind == 'cube' else 'in K'))
json.dump(res, open(f'edge-{label}.json', 'w'), indent=1)
print('FINAL ok' if exact_ok else 'FINAL FAIL: exact check')
