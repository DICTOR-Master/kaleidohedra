#!/usr/bin/env python3
"""Q1 and Q2. For each central solid X in {A, B, C} (fixed at the identity) and each solid Y in {A, B, C}:
all placements g.Y + t (g one of the 120 symmetries, t in Z^6) that share at least one whole face with X (same rhombus, opposite
outward sides) and do not overlap X (exact). Face-to-face contact forces t in Z^6, and for a given g and a given face of X there is
exactly one face of g.Y on the same pair with the opposite side, so this list is complete.
Then the face coronas: sets of such neighbours, pairwise non-overlapping (exact), covering each of the 30 faces of X exactly once
(exact cover, SAT with pysat; all solutions enumerated). Every face-to-face tiling contains one around each tile.
Usage: neighbours.py <k10 dir> <inchbald json> <out json> <max solutions per centre> <centres, e.g. C> <neighbour types, e.g. ABC>"""
import sys, time, json
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from mixlib import *
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
t0 = time.time()
K10, INCH, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
MAXSOL = int(sys.argv[4]); CENTRES = sys.argv[5]; NTYPES = sys.argv[6]
sol = load_solids(K10, INCH)
NAMES = 'ABC'
EF = np.array([[zfloat(c) for c in e] for e in G.E])
for nm in NAMES:
    s = sol[nm]
    pts = np.array([np.array(v, float) @ EF for f in s['faces'] for v in corners(f, 6)])
    s['ctr6'] = None; s['ctr'] = pts.mean(0); s['R'] = np.linalg.norm(pts - s['ctr'], axis=1).max()
    s['neg'] = [c for c, sg in s['cells'] if sg < 0]
    s['clean'] = [sg > 0 and not any(G.relation(c[0], c[1], k[0], k[1]) == 'cross' for k in s['neg']) for c, sg in s['cells']]
PR = G.pairs
Dx = np.array([[G.D[(x, y, i)][0] for (x, y) in PR] for i in range(n)], dtype=np.int64)
Dy = np.array([[G.D[(x, y, i)][1] for (x, y) in PR] for i in range(n)], dtype=np.int64)
def sign_arr(x, y):
    a, b = 2*x + y, y
    s = np.where((a >= 0) & (b >= 0), np.where((a == 0) & (b == 0), 0, 1), 0)
    s = np.where((a <= 0) & (b <= 0) & ~((a == 0) & (b == 0)), -1, s)
    mixed = ((a > 0) & (b < 0)) | ((a < 0) & (b > 0))
    return np.where(mixed, np.where(a*a > 5*b*b, np.sign(a), np.sign(b)), s)
def intervals(cells):
    P = np.array([c[0] for c in cells], dtype=np.int64); bx, by = P @ Dx, P @ Dy
    lox, loy, hix, hiy = bx.copy(), by.copy(), bx.copy(), by.copy()
    for ci, c in enumerate(cells):
        for dd in c[1]:
            vx, vy = Dx[dd], Dy[dd]; pos = sign_arr(vx, vy) > 0
            hix[ci] += np.where(pos, vx, 0); hiy[ci] += np.where(pos, vy, 0)
            lox[ci] += np.where(pos, 0, vx); loy[ci] += np.where(pos, 0, vy)
    return lox, loy, hix, hiy
def cross_matrix(c1, c2):
    """exact: cross[i, j] = True iff cell i of c1 and cell j of c2 meet in their interiors (separating axis on the 15 normals)"""
    lox, loy, hix, hiy = intervals(c1); lx2, ly2, hx2, hy2 = intervals(c2)
    g1 = sign_arr(lx2[None] - hix[:, None], ly2[None] - hiy[:, None])
    g2 = sign_arr(lox[:, None] - hx2[None], loy[:, None] - hy2[None])
    return ~((g1 >= 0) | (g2 >= 0)).any(axis=2)
stats = {'exact_volume_calls': 0}
def overlap_placed(n1, cells1, n2, cells2):
    """exact overlap of two placed solids (cells already placed); n1, n2 their names (for the clean-cell witness)"""
    cm = cross_matrix([c for c, _ in cells1], [c for c, _ in cells2])
    s1 = np.array([s for _, s in cells1]); s2 = np.array([s for _, s in cells2])
    pos = cm & (s1[:, None] > 0) & (s2[None, :] > 0)
    if not pos.any(): return False               # negative cells only remove volume: no overlap
    cl1 = np.array(sol[n1]['clean']); cl2 = np.array(sol[n2]['clean'])
    if (pos & cl1[:, None] & cl2[None, :]).any(): return True   # two cells lying wholly inside the solids meet in interiors
    stats['exact_volume_calls'] += 1
    v = overlap_volume(cells1, cells2); assert v.sign() >= 0
    return v.sign() > 0

PHI = (1 + 5**0.5)/2
def float_intervals(cells):
    lox, loy, hix, hiy = intervals(cells)
    return lox + PHI*loy, hix + PHI*hiy
EPS = 1e-7       # float values here are below 1e3 in size, so float error < 1e-11 << EPS: strict decisions are sound
def conflicts(neigh):
    """exact pairwise overlap among neighbours. Float SAT with margin EPS decides 'clearly apart' / 'clearly crossing' cell
    pairs; every cell pair within EPS of touching is re-decided by the exact test (zsurf relation)."""
    N = len(neigh); K = max(len(m['cells']) for m in neigh)
    LO = np.full((N, K, 15), np.inf); HI = np.full((N, K, 15), -np.inf); SG = np.zeros((N, K), int); CL = np.zeros((N, K), bool)
    for i, m in enumerate(neigh):
        lo, hi = float_intervals([c for c, _ in m['cells']]); k = len(m['cells'])
        LO[i, :k] = lo; HI[i, :k] = hi; SG[i, :k] = [sg for _, sg in m['cells']]; CL[i, :k] = sol[m['Y']]['clean']
    C = np.array([m['c'] for m in neigh]); Rr = np.array([m['R'] for m in neigh])
    out = []; nexact = 0
    for i in range(N - 1):
        js = np.arange(i + 1, N)
        js = js[np.linalg.norm(C[js] - C[i], axis=1) <= Rr[js] + Rr[i] + 1e-6]
        if len(js) == 0: continue
        g1 = LO[js][:, None, :, :] - HI[i][None, :, None, :]      # (J, Ki, Kj, 15)
        g2 = LO[i][None, :, None, :] - HI[js][:, None, :, :]
        apart = ((g1 > EPS) | (g2 > EPS)).any(axis=3)
        cross = ((g1 < -EPS) & (g2 < -EPS)).all(axis=3)
        amb = ~apart & ~cross
        valid = (SG[i][None, :, None] != 0) & (SG[js][:, None, :] != 0)
        apart |= ~valid; cross &= valid; amb &= valid
        for jj, j in enumerate(js):
            a, b = neigh[i], neigh[j]
            cr = cross[jj].copy()
            for ci, cj in np.argwhere(amb[jj]):
                nexact += 1
                ca, cb = a['cells'][ci][0], b['cells'][cj][0]
                if G.relation(ca[0], ca[1], cb[0], cb[1]) == 'cross': cr[ci, cj] = True
            pos = cr & (SG[i][:, None] > 0) & (SG[j][None, :] > 0)
            if not pos.any(): continue
            if (pos & CL[i][:, None] & CL[j][None, :]).any(): out.append((i, j)); continue
            if overlap_placed(a['Y'], a['cells'], b['Y'], b['cells']): out.append((i, j))
    print('   exact re-decisions of near-touching cell pairs:', nexact, flush=True)
    return out
def fpos(p): return np.array(p, float) @ EF

result = {'solids': {nm: {'symmetries': None, 'basis': sol[nm]['basis'], 'cells': [[list(c[0]), list(c[1]), s] for c, s in sol[nm]['cells']]} for nm in NAMES},
          'centres': {}}
allok = True
for X in CENTRES:
    SX = sol[X]['faces']; CX = sol[X]['cells']
    neigh = []; seenF = set()
    for Y in NTYPES:
        imgs = {}
        for gi in range(120):
            F0 = tfaces(sol[Y]['faces'], gi, (0,)*6)
            imgs.setdefault(canon_t(F0), gi)
        for gi in sorted(imgs.values()):
            F0 = tfaces(sol[Y]['faces'], gi, (0,)*6)
            byp = {}
            for f, s in F0.items(): byp.setdefault((f[1], f[2], s), f)
            for f, s in SX.items():
                g = byp[(f[1], f[2], -s)]
                t = tuple(a - b for a, b in zip(f[0], g[0]))
                FY, CY = place(sol, Y, gi, t)
                key = frozenset(FY.items())
                if key in seenF: continue
                seenF.add(key)
                shared = sorted(i for i, (ff, ss) in enumerate(sorted(SX.items())) if FY.get(ff) == -ss)
                if overlap_placed(X, CX, Y, CY): continue
                neigh.append({'Y': Y, 'g': gi, 't': list(t), 'shared': shared, 'faces': FY, 'cells': CY})
    print(X, 'valid face neighbours:', {Y: sum(1 for m in neigh if m['Y'] == Y) for Y in NAMES}, f't={time.time()-t0:.0f}s', flush=True)
    # lattice neighbours (control): Y = X, same orientation, t in the lattice of X
    B = np.array(sol[X]['basis'])
    def in_lattice(t):
        sol_, res, rk, _ = np.linalg.lstsq(B.T.astype(float), np.array(t, float), rcond=None)
        r = np.round(sol_).astype(int); return bool((r @ B == np.array(t)).all())
    for m in neigh:
        m['lattice'] = m['Y'] == X and canon_t(m['faces']) == canon_t(SX) and in_lattice(m['t']) and \
            frozenset(m['faces'].items()) == frozenset(tfaces(SX, IDENT, m['t']).items())
    if MAXSOL == 0:      # neighbour counts only (Q1)
        result['centres'][X] = {'neighbours': [{'Y': m['Y'], 'g': m['g'], 't': m['t'], 'shared': m['shared'], 'lattice': m['lattice']} for m in neigh],
                                'n_neighbours': {Y: sum(1 for m in neigh if m['Y'] == Y) for Y in NTYPES}, 'coronas_complete': True}
        continue
    # pairwise conflicts among neighbours (exact)
    N = len(neigh); ctr = [fpos(m['t']) + 0 for m in neigh]
    for m in neigh:
        P = np.array([fpos(v) for f in m['faces'] for v in corners(f, 6)]); m['c'] = P.mean(0); m['R'] = np.linalg.norm(P - m['c'], axis=1).max()
    conf = conflicts(neigh)
    print(X, 'neighbour pairs in conflict:', len(conf), 'of', N*(N - 1)//2, f't={time.time()-t0:.0f}s', flush=True)
    # SAT exact cover of the 30 faces
    cover = {fi: [i for i, m in enumerate(neigh) if fi in m['shared']] for fi in range(30)}
    clauses = []; top = N
    for fi, lst in cover.items():
        enc = CardEnc.equals(lits=[i + 1 for i in lst], bound=1, top_id=top, encoding=EncType.pairwise)
        clauses += enc.clauses
    for i, j in conf: clauses.append([-(i + 1), -(j + 1)])
    sols = []
    with Cadical153(bootstrap_with=clauses) as S:
        while len(sols) < MAXSOL and S.solve():
            mdl = S.get_model(); chosen = [i for i in range(N) if mdl[i] > 0]
            sols.append(chosen); S.add_clause([-(i + 1) for i in chosen])
        complete = len(sols) < MAXSOL
    kinds = {}
    for ch in sols:
        k = ''.join(sorted(neigh[i]['Y'] for i in ch))
        lat = all(neigh[i]['lattice'] for i in ch)
        kk = (k, lat); kinds[kk] = kinds.get(kk, 0) + 1
    mixed = [ch for ch in sols if any(neigh[i]['Y'] != X for i in ch)]
    print(X, 'face coronas:', len(sols), '(complete enumeration)' if complete else '(CAPPED)', 'mixed:', len(mixed), flush=True)
    for (k, lat), c in sorted(kinds.items(), key=lambda z: -z[1])[:40]:
        print('   ', X, 'neighbour types', k, 'lattice corona' if lat else '', 'count', c)
    result['centres'][X] = {
        'neighbours': [{'Y': m['Y'], 'g': m['g'], 't': m['t'], 'shared': m['shared'], 'lattice': m['lattice']} for m in neigh],
        'n_neighbours': {Y: sum(1 for m in neigh if m['Y'] == Y) for Y in NAMES},
        'conflicts': conf, 'coronas': sols, 'coronas_complete': complete,
        'corona_kinds': [[k, lat, c] for (k, lat), c in kinds.items()], 'n_mixed': len(mixed)}
    nlat = sum(1 for (k, lat), c in kinds.items() if lat)
    if nlat != 1 and X != 'Z': allok = False; print('control: lattice corona not found exactly once for', X)
result['exact_volume_calls'] = stats['exact_volume_calls']
json.dump(result, open(OUT, 'w'))
print('exact volume computations', stats['exact_volume_calls'], f't={time.time()-t0:.0f}s')
print('FINAL ok' if allok and all(result['centres'][X]['coronas_complete'] for X in CENTRES) else 'FINAL FAIL: control or enumeration incomplete')
