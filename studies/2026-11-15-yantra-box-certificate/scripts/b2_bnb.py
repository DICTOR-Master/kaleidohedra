"""Step 2: branch and bound (generator).  Covers the box of polys-<name>.json by bisection; a leaf is closed when one test holds on it:
  ('F', k):   the k-th equation polynomial has a fixed sign on the box (so the box holds no solution of F~ = 0);
  ('T', name): an admissibility test fails on the whole box (N and D of opposite fixed signs, so q < 0);
  ('K', 0):   the box lies inside the Krawczyk box (step 3 proves exactly one solution there).
Enclosure used everywhere (generator, exact checker, Lean): all box coordinates are >= 0, so p = p+ - p- with p+, p- having nonnegative
coefficients, and on [l, h]:  p+(l) - p-(h) <= p <= p+(h) - p-(l)  (monotone split; Moore's natural extension for this form).
The generator works in floating point with a relative safety margin; every leaf is re-checked in exact rational arithmetic by b4_check.py
(and independently by b5_arb.py), so floating point only chooses the boxes.
Usage: b2_bnb.py polys.json out.json [maxdepth] [kbox.json]
Prints PROGRESS per level; FINAL ok iff no open box is left (open boxes are written to out.json either way)."""
import json, sys, time, os
import numpy as np
T0 = time.time(); say = lambda *a: print(f'[{time.time() - T0:7.1f} s]', *a, flush=True)
src, dst = sys.argv[1], sys.argv[2]
MAXD = int(sys.argv[3]) if len(sys.argv) > 3 else 60
KB = json.load(open(sys.argv[4])) if len(sys.argv) > 4 and sys.argv[4] != '-' else None
MAXOPEN = int(os.environ.get('MAXOPEN', '4000000'))
data = json.load(open(src))
from fractions import Fraction as Fq
box0 = [[Fq(x) for x in iv] for iv in data['box']]
def mk(p):
    E = np.array([e for e, c in p], dtype=np.int64).reshape(-1, 3); C = np.array([float(int(c)) for e, c in p])
    return E, C
polys = []                                           # (kind, name, list of (E, C)) ; for tests two polys N, D
for k, p in data['F'].items(): polys.append(('F', k, [mk(p)]))
order = sorted(data['tests'].items(), key=lambda kv: len(kv[1]['N']) + len(kv[1]['D']))
if os.environ.get('NOTESTS'): order = []           # negative control: equations only
for k, nd in order:
    if len(nd['N']) == 1 and len(nd['D']) == 1:
        # constant-sign tests (e.g. w1 > 0 is u*tau/(...) with only positive factors): never fail, skip
        cN = int(nd['N'][0][1]); cD = int(nd['D'][0][1])
        if all(x == 0 for x in nd['N'][0][0]) and all(x == 0 for x in nd['D'][0][0]) and (cN > 0) == (cD > 0): continue
    polys.append(('T', k, [mk(nd['N']), mk(nd['D'])]))
maxdeg = max(int(E.max()) if E.size else 0 for _, _, L in polys for E, C in L)
say('tests in use:', [(kd, nm) for kd, nm, _ in polys])
REL = 1e-12
def enclose(E, C, lo, hi):
    """lo, hi: (n, 3) float arrays >= 0.  returns (n,) lower and upper bounds (float, with safety margin), via the monotone split."""
    n = lo.shape[0]
    if E.shape[0] == 0: return np.zeros(n), np.zeros(n)
    plo = np.ones((n, len(C))); phi = np.ones((n, len(C)))
    for j in range(3):
        e = E[:, j]
        if e.max() == 0: continue
        Lp = lo[:, j:j + 1] ** e[None, :]; Hp = hi[:, j:j + 1] ** e[None, :]
        plo *= Lp; phi *= Hp
    pos = C > 0
    Cp = np.where(pos, C, 0.0); Cn = np.where(pos, 0.0, -C)
    low = plo @ Cp - phi @ Cn; up = phi @ Cp - plo @ Cn
    mag = phi @ np.abs(C)
    return low - REL * mag - 1e-300, up + REL * mag + 1e-300
def enclose_slope(E, C, lo, hi):
    """slope form (Krawczyk and Neumaier 1985): p(x) = p(m) + (x-m) A + (y-m_y) B + (z-m_z) C, m the midpoint,
    x^a - m^a = (x - m) S_a(x, m), S_a = sum_k x^k m^(a-1-k) >= 0 increasing in x; A, B, C bounded by the monotone split."""
    n = lo.shape[0]
    if E.shape[0] == 0: return np.zeros(n), np.zeros(n)
    m = (lo + hi) / 2; r = (hi - lo) / 2
    K = int(E.max()) + 1
    mp = np.ones((n, 3, K)); 
    for k in range(1, K): mp[:, :, k] = mp[:, :, k - 1] * m
    def Spow(x):                                   # S_k(x, m) for k = 0..K-1, shape (n, 3, K); S_0 = 0, S_k = x S_{k-1} + m^(k-1)
        S = np.zeros((n, 3, K))
        for k in range(1, K): S[:, :, k] = x * S[:, :, k - 1] + mp[:, :, k - 1]
        return S
    Sl = Spow(lo); Sh = Spow(hi)
    pl = np.ones((n, 3, K)); ph = np.ones((n, 3, K))
    for k in range(1, K): pl[:, :, k] = pl[:, :, k - 1] * lo; ph[:, :, k] = ph[:, :, k - 1] * hi
    a, b, e = E[:, 0], E[:, 1], E[:, 2]
    pos = C > 0; Cp = np.where(pos, C, 0.0); Cn = np.where(pos, 0.0, -C)
    pm = mp[:, 0, a] * mp[:, 1, b] * mp[:, 2, e]
    val = pm @ C
    # A: S_a(x) y^b z^e ; B: m_x^a S_b(y) z^e ; C: m_x^a m_y^b S_e(z)
    Ah = Sh[:, 0, a] * ph[:, 1, b] * ph[:, 2, e]; Al = Sl[:, 0, a] * pl[:, 1, b] * pl[:, 2, e]
    Bh = mp[:, 0, a] * Sh[:, 1, b] * ph[:, 2, e]; Bl = mp[:, 0, a] * Sl[:, 1, b] * pl[:, 2, e]
    Ch = mp[:, 0, a] * mp[:, 1, b] * Sh[:, 2, e]; Cl = mp[:, 0, a] * mp[:, 1, b] * Sl[:, 2, e]
    rad = 0
    for Xh, Xl, j in ((Ah, Al, 0), (Bh, Bl, 1), (Ch, Cl, 2)):
        up = Xh @ Cp - Xl @ Cn; lw = Xl @ Cp - Xh @ Cn
        rad = rad + r[:, j] * np.maximum(np.abs(up), np.abs(lw))
    mag = (ph[:, 0, a] * ph[:, 1, b] * ph[:, 2, e]) @ np.abs(C)
    return val - rad - REL * mag - 1e-300, val + rad + REL * mag + 1e-300
if os.environ.get('ENCL', 'slope') == 'slope': enclose = enclose_slope
def sign_fixed(E, C, lo, hi):
    l, u = enclose(E, C, lo, hi)
    return np.where(l > 0, 1, np.where(u < 0, -1, 0))
HOLES = (KB or {}).get('holes', [])                   # [{'name':..., 'box': [[a, b], ...]}]: covered elsewhere (charts, Krawczyk box)
def inside_holes(lo, hi):
    out = np.full(lo.shape[0], -1)
    for h, H in enumerate(HOLES):
        kl = np.array([float(Fq(a)) for a, b in H['box']]); kh = np.array([float(Fq(b)) for a, b in H['box']])
        m = np.all((lo >= kl) & (hi <= kh), axis=1) & (out < 0)       # dyadic endpoints: exact in floating point
        out[m] = h
    return out
# boxes are integer index triples (level per coordinate) : box = prod [i_j, i_j + 1] * width0_j / 2^d_j
leaves = []                                           # (d0, i0, d1, i1, d2, i2, kind, name)
cur = np.zeros((1, 6), dtype=np.int64)               # d0 i0 d1 i1 d2 i2
W0 = np.array([float(b - a) for a, b in box0]); A0 = np.array([float(a) for a, b in box0])
openleft = []
level = 0
counts = {}
while cur.shape[0]:
    n = cur.shape[0]
    d = cur[:, 0::2].astype(float); i = cur[:, 1::2].astype(float)
    w = W0[None, :] / 2.0 ** d
    lo = A0[None, :] + i * w; hi = lo + w
    closed = np.zeros(n, bool); how = np.full(n, -1)
    hin = inside_holes(lo, hi); kin = hin >= 0; closed |= kin; how[kin] = 10**6 + hin[kin]
    for pi, (kind, name, L) in enumerate(polys):
        idx = np.nonzero(~closed)[0]
        if idx.size == 0: break
        for s in range(0, idx.size, 20000):
            sub = idx[s:s + 20000]
            if kind == 'F':
                sg = sign_fixed(*L[0], lo[sub], hi[sub]); ok = sg != 0
            else:
                sN = sign_fixed(*L[0], lo[sub], hi[sub]); sD = sign_fixed(*L[1], lo[sub], hi[sub]); ok = (sN * sD) == -1
            closed[sub[ok]] = True; how[sub[ok]] = pi
    for j in np.nonzero(closed)[0]:
        h = int(how[j]); kind, name = (('H', HOLES[h - 10**6]['name']) if h >= 10**6 else polys[h][:2])
        leaves.append(list(map(int, cur[j])) + [kind, name]); counts[name] = counts.get(name, 0) + 1
    rest = cur[~closed]
    if rest.shape[0] == 0: break
    # split along the coordinate with the largest normalised width (u, tau width 1; rho by its range / 6)
    d = rest[:, 0::2]
    wn = 1.0 / 2.0 ** d
    j = np.argmax(wn, axis=1)
    too_deep = d.max(axis=1) >= MAXD
    if too_deep.any():
        for r in rest[too_deep]: openleft.append(list(map(int, r)))
        rest = rest[~too_deep]; j = j[~too_deep]
    if rest.shape[0] > MAXOPEN:
        say('open boxes exceed', MAXOPEN, '- stopping'); [openleft.append(list(map(int, r))) for r in rest]; break
    a = rest.copy(); b = rest.copy()
    rows = np.arange(rest.shape[0])
    a[rows, 2 * j] += 1; a[rows, 2 * j + 1] = 2 * rest[rows, 2 * j + 1]
    b[rows, 2 * j] += 1; b[rows, 2 * j + 1] = 2 * rest[rows, 2 * j + 1] + 1
    cur = np.concatenate([a, b])
    level += 1
    if cur.shape[0] == 0: break

    say(f'level {level}: open {cur.shape[0]}, leaves {len(leaves)}, deepest {int(cur[:, 0::2].max())}')
    if level % 12 == 0:
        from collections import Counter
        dd = cur[:, 0::2].astype(float); ii = cur[:, 1::2].astype(float); ww = W0[None, :] / 2.0 ** dd; ll = A0[None, :] + ii * ww
        say('   open clusters:', Counter(tuple(np.round(x / np.array([0.05, 0.05, 0.3])) * np.array([0.05, 0.05, 0.3])) for x in ll).most_common(8))
    print(f'PROGRESS {min(level / MAXD / 3, 0.99):.3f} level {level}', flush=True)
say('leaves:', len(leaves), ' by test:', counts, ' open:', len(openleft))
json.dump({'polys': os.path.basename(src), 'box': data['box'], 'kbox': KB, 'leaves': leaves, 'open': openleft,
           'tests': [(kd, nm) for kd, nm, _ in polys]}, open(dst, 'w'))
if openleft:
    ol = np.array(openleft); d = ol[:, 0::2].astype(float); i = ol[:, 1::2].astype(float); w = W0[None, :] / 2.0 ** d
    lo = A0[None, :] + i * w
    say('open box lower corners (first 30, sorted):')
    for r in sorted(map(tuple, np.round(lo, 6)))[:30]: say('   ', r)
    # cluster summary
    from collections import Counter
    cl = Counter(tuple(np.round(x, 1)) for x in lo)
    say('open clusters (rounded to 0.1):', cl.most_common(20))
print('PROGRESS 1.0 done')
print('FINAL ok' if not openleft else f'FINAL FAIL: {len(openleft)} open boxes')
