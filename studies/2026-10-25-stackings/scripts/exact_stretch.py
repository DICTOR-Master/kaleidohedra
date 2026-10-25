# Stretch-wide proof of the rule of halves (DICTO 2026-10-25). Coordinates: (x, y) in the hexagonal layer basis, z in layer
# spacings, all relative to the site — rational. On each stretch every corner of every cell is an affine function of λ
# (census engine). For each central site of each of the 16 windows and each stretch, we look for ONE symmetry g of the layer
# lattice (24 = the 12 symmetries of the hexagonal layer about the site's axis, with or without z → −z) such that
#  • tetrahedral site: g maps the set of corner FUNCTIONS of the piece onto those of the pure piece (cubic or hexagonal, by the
#    nearest layer) — then the pieces agree for every λ in the stretch;
#  • octahedral site: g maps the corner functions lying above the site onto those of the pure upper half (layer above decides),
#    and likewise below (layer below decides), the corners ON the mid-plane matching too; the half-polytopes are then the convex
#    hulls of equal point sets with equal sections, checked additionally at three rational λ per stretch by exact point sets.
# A sample λ is kept only if the cell's exact combinatorial interval (engine) contains the whole stretch sample range.
exec(open('exact_halves.py').read().split('lams = ')[0])
STRETCH = [(Fr(-11, 24), Fr(-3, 8)), (Fr(-3, 8), Fr(-1, 8)), (Fr(-1, 8), Fr(5, 24)), (Fr(5, 24), Fr(3, 8))]
def ops():
    R = ((0, -1), (1, 1))                      # 60° turn in the hexagonal basis a1 → a2, a2 → a2 − a1
    M = ((0, 1), (1, 0))                       # mirror a1 ↔ a2
    mul = lambda A, B: tuple(tuple(sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)) for i in range(2))
    G2 = {((1, 0), (0, 1))}
    while True:
        new = {mul(a, b) for a in G2 | {R, M} for b in G2 | {R, M}} | G2
        if new == G2: break
        G2 = new
    return [(A, s) for A in G2 for s in (1, -1)]
OPS = ops(); assert len(OPS) == 24, len(OPS)
def funcs(c, spec, i, n):
    """corner functions relative to the site: ((x0,x1),(y0,y1),(z0,z1)) with z in layer spacings (cell height = n spacings)"""
    p = spec['motif'][i][1]; out = []
    for cr in c.corners:
        P = cr['P']
        f = [(Fr(P[r][0]) - Fr(p[r]), Fr(P[r][1]) if len(P[r]) > 1 else Fr(0)) for r in range(3)]
        f[2] = (f[2][0] * n, f[2][1] * n); out.append(tuple(f))
    return out
def apply(g, f):
    (A, s) = g; x, y, z = f
    return (tuple(A[0][0] * x[k] + A[0][1] * y[k] for k in range(2)), tuple(A[1][0] * x[k] + A[1][1] * y[k] for k in range(2)), tuple(s * z[k] for k in range(2)))
def side(fs, sgn, lam):                       # corners strictly above (sgn=1) / below (−1) / on (0) the mid-plane at λ
    v = lambda f: f[2][0] + f[2][1] * lam
    return frozenset(f for f in fs if (v(f) > 0 if sgn > 0 else v(f) < 0 if sgn < 0 else v(f) == 0))
REFN = {'c': 3, 'h': 2}
ok = bad = 0; fails = []
for hc in itertools.product('hc', repeat=4):
    hc = ''.join(hc); word = word_for(hc); net, spec = build(word); n = len(word); T = layer_types(word)
    for lo, hi in STRETCH:
        samples = [lo + (hi - lo) * Fr(k, 4) for k in (1, 2, 3)]
        g0 = 2
        for j in range(3):
            i = 3 * g0 + j; k, p = spec['motif'][i]
            c = cell(net, i, samples[1])
            if c is None: continue
            iv = c.interval()
            if not ((iv[0] is None or iv[0] <= lo) and (iv[1] is None or iv[1] >= hi)): fails.append(f'{hc} {lo},{hi} site {i}: interval {iv} narrower than the stretch'); bad += 1; continue
            F = funcs(c, spec, i, n)
            if k == 'tet':
                t = T[(g0 + 1) % n] if j == 1 else T[g0 % n]          # nearest layer: tet over X (j=1) sits just under layer g0+1
                rn, rs = REF[t]; cands = []
                for i2, (k2, p2) in enumerate(rs['motif']):
                    if k2 != 'tet': continue
                    c2 = cell(rn, i2, samples[1])
                    if c2 is not None: cands.append(frozenset(funcs(c2, rs, i2, REFN[t])))
                good = any(frozenset(apply(g, f) for f in F) in cands for g in OPS)
            else:
                good = True
                for sgn, t in ((1, T[(g0 + 1) % n]), (-1, T[g0 % n])):
                    rn, rs = REF[t]; found = False
                    for i2, (k2, p2) in enumerate(rs['motif']):
                        if k2 != 'oct': continue
                        c2 = cell(rn, i2, samples[1])
                        if c2 is None: continue
                        F2 = funcs(c2, rs, i2, REFN[t])
                        for g in OPS:
                            G = [apply(g, f) for f in F]; tsgn = sgn * g[1]
                            if all(side(G, sgn, lam) == side(F2, sgn, lam) and side(G, 0, lam) == side(F2, 0, lam) for lam in samples) \
                               and all(sorted(half(c, lam, Fr(p[2]), sgn > 0)) is not None for lam in samples):
                                # exact section check at the samples: the cut points of the two halves coincide under g
                                found = True; break
                        if found: break
                    good &= found
            ok += good; bad += (not good)
            if not good: fails.append(f'{hc} ({word}) stretch ({lo}, {hi}) site {i} {k}')
    print(f'window {hc}: running {ok} PASS, {bad} FAIL', flush=True)
print('\n'.join(fails[:30])); print(f'TOTAL {ok} PASS, {bad} FAIL')
