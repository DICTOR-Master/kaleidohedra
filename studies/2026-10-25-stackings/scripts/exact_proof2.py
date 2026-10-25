# Closing the proof of the rule of halves (DICTO 2026-10-25: "honest checks and thorough proofs first").
# (1) LOCALITY, exact: on every stretch of every one of the 16 windows, every corner of every central cell lies within squared
#     distance 1/2 of its site (metric exact; squared distance of an affine path is convex in λ, so the stretch ends suffice).
#     Hand argument (in the paper): a site of a gap three or more gaps away is at least 2.5 layer spacings (2.5·√(2/3)) away in height,
#     and |w_p − w_q| ≤ 11/24, so its bisector plane is at distance ≥ (25/6 − 11/24)/(5·√(2/3)) from p, whose square is 23763/28800 > 1/2:
#     it cannot meet the cell. Hence any stacking with the same six layers round the gap has the same cells (convexity argument).
# (2) OCTAHEDRAL HALVES along whole stretches: each stretch is split where a corner crosses the site's mid-plane; on each piece of
#     stretch, under the symmetry g found by exact_stretch.py's search, the corner functions on each side AND the section points
#     (edge ∩ mid-plane, rational functions of λ, sympy) must coincide with the pure half's.
exec(open('exact_stretch.py').read().split('REFN = ')[0])
import sympy as sp
REFN = {'c': 3, 'h': 2}; L = sp.Symbol('lam')
def corner_at(f, lam): return tuple(f[r][0] + f[r][1] * lam for r in range(3))
def gq(G3, a, b):    # squared distance in the window's metric, with z in layer spacings → convert: metric z-entry is (2/3)n² per cell height n
    return None
rad_ok = rad_bad = 0; half_ok = half_bad = 0; fails = []
def d2_layer(v):     # squared length of (x, y in hex basis, z in layer spacings): hex part x² + xy + y², z part (2/3) z²
    x, y, z = v; return x * x + x * y + y * y + Fr(2, 3) * z * z
def section(F, E, lam_sym):
    pts = set()
    for a, b in E:
        za = F[a][2][0] + F[a][2][1] * lam_sym; zb = F[b][2][0] + F[b][2][1] * lam_sym
        t = sp.cancel(-za / (zb - za))
        pts.add(tuple(sp.cancel(sp.Integer(0) + (F[a][r][0] + F[a][r][1] * lam_sym) + t * ((F[b][r][0] + F[b][r][1] * lam_sym) - (F[a][r][0] + F[a][r][1] * lam_sym))) for r in range(3)))
    return pts
def crossing_edges(F, E, lam):
    out = []
    for a, b in E:
        za = F[a][2][0] + F[a][2][1] * lam; zb = F[b][2][0] + F[b][2][1] * lam
        if za * zb < 0: out.append((a, b))
    return out
for hc in itertools.product('hc', repeat=4):
    hc = ''.join(hc); word = word_for(hc); net, spec = build(word); n = len(word); T = layer_types(word)
    for lo, hi in STRETCH:
        g0 = 2
        for j in range(3):
            i = 3 * g0 + j; k, p = spec['motif'][i]; mid = (lo + hi) / 2
            c = cell(net, i, mid)
            if c is None: continue
            F = funcs(c, spec, i, n)
            # (1) locality radius at both stretch ends
            r = max(d2_layer(corner_at(f, lam)) for f in F for lam in (lo, hi))
            if r <= Fr(1, 2): rad_ok += 1
            else: rad_bad += 1; fails.append(f'RADIUS {hc} ({lo},{hi}) site {i}: {r}')
            if k != 'oct': continue
            # (2) split the stretch where a corner crosses z = 0
            cuts = sorted({-f[2][0] / f[2][1] for f in F if f[2][1] != 0 and lo < -f[2][0] / f[2][1] < hi})
            pieces = [lo] + cuts + [hi]
            E = edges(c)
            for a, b in zip(pieces, pieces[1:]):
                lam_s = (a + b) / 2
                for sgn, t in ((1, T[(g0 + 1) % n]), (-1, T[g0 % n])):
                    rn, rs = REF[t]; found = False
                    for i2, (k2, p2) in enumerate(rs['motif']):
                        if k2 != 'oct': continue
                        c2 = cell(rn, i2, lam_s)
                        if c2 is None: continue
                        F2 = funcs(c2, rs, i2, REFN[t]); E2 = edges(c2)
                        S2 = section(F2, crossing_edges(F2, E2, lam_s), L)
                        for g in OPS:
                            G = [apply(g, f) for f in F]
                            if side(G, sgn, lam_s) != side(F2, sgn, lam_s) or side(G, 0, lam_s) != side(F2, 0, lam_s): continue
                            if section(G, crossing_edges(G, E, lam_s), L) == S2: found = True; break
                        if found: break
                    half_ok += found; half_bad += (not found)
                    if not found: fails.append(f'HALF {hc} ({word}) ({a},{b}) site {i} side {sgn}')
    print(f'window {hc}: radius {rad_ok} ok / {rad_bad} bad; halves {half_ok} ok / {half_bad} bad', flush=True)
print('\n'.join(fails[:30])); print(f'TOTAL radius {rad_ok} ok, {rad_bad} bad; halves {half_ok} ok, {half_bad} bad')
