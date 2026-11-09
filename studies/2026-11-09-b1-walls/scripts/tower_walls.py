# B1 / #86: the tower move over whole stretches (Hopscotch walls).
# On each chamber of the weight walk (between stops of the pure stacking's walk) every corner of every power cell is affine in λ,
# every facet plane has a fixed normal and an offset affine in λ (engine of #53/#57). The combinatorial type of the shifted tile
# (pieces, face contacts of positive area, merged surface, edge multiplicities) is fixed by the signs of all 4-plane determinants
# of the tile's planes, each linear in λ, and by the coincidences of parallel planes. So it is constant on every open interval
# between consecutive roots. We list all roots in each chamber (the walls) and run the exact check of #86 (dense.check) at every
# wall and at one interior point of every hop. Usage: python tower_walls.py <c|h> -> data/tower_walls_<t>.json
import sys, os, itertools, json, time
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import tiles as TL
from engine import Cell
import exactfaces as E
import dense

def full_pieces(word, L, lam):
    """as tiles.tile, but return per piece (kind, site_local, full cell corners local, cut z or None)"""
    net, spec = TL.build(word); n = len(word); m = spec['motif']
    ball = (*TL.POS[word[L]], Fr(L))
    def loc(p): return (p[0] - ball[0], p[1] - ball[1], p[2] * n - ball[2])
    g0, g1 = (L - 1) % n, L % n
    want = [(3 * g0, 'oct', True), (3 * g0 + 1, 'tet', None), (3 * g1 + 2, 'tet', None), (3 * g1, 'oct', False)]
    out = []
    for i, k, up in want:
        c = Cell(net, i, (lam,), Fr(12))
        if c.empty: continue
        X = TL.corners(c, lam); site = m[i][1]
        sh = round((site[2] * n - L) / n) * n
        X = [(x[0], x[1], x[2] - Fr(sh, n)) for x in X]; site = (site[0], site[1], site[2] - Fr(sh, n))
        sl = loc(site)
        out.append((k, sl, [loc(p) for p in X], sl[2] if k == 'oct' else None))
    return out

def norm_plane(n, c):
    m, sg = E.prim(n)
    # n = sg*g*m for a positive scalar g; plane n.x = c  <=>  m.x = c / (sg*g)
    j = [i for i in range(3) if n[i]][0]; g = Fr(n[j]) / (sg * m[j])
    return m, Fr(c) / (sg * g)

def planes_at(word, L, lam, shift_rule):
    P = full_pieces(word, L, lam); out = []
    for k, sl, X, zc in P:
        t = shift_rule(sl)
        for n, c, pts in E.facets(X):
            out.append(norm_plane(n, c + n[0] * t[0] + n[1] * t[1]))
        if zc is not None: out.append(((0, 0, 1), zc))
    return len(P), sorted(set(out))

def det3(a, b, c): return E.dot(a, E.cross(b, c))

def walls(word, L, a, b, shift_rule):
    S = [a + (b - a) * Fr(k, 6) for k in range(1, 6)]
    data = [planes_at(word, L, s, shift_rule) for s in S]
    npieces = {d[0] for d in data}; assert len(npieces) == 1, 'piece count changes inside a chamber'
    normals = [sorted(n for n, c in d[1]) for d in data]
    assert all(x == normals[0] for x in normals), 'facet normals change inside a chamber'
    # affine offsets: pair planes by position in the sorted list (same normals, sorted by (n, c): parallel planes keep order
    # only if they do not cross; check by fitting through samples 0 and 4 and testing 1..3)
    PL = []
    for idx in range(len(data[0][1])):
        n = data[0][1][idx][0]; c0 = data[0][1][idx][1]; c4 = data[4][1][idx][1]
        beta = (c4 - c0) / (S[4] - S[0]); alpha = c0 - beta * S[0]
        for q in (1, 2, 3):
            assert data[q][1][idx] == (n, alpha + beta * S[q]), 'offset not affine'
        PL.append((n, alpha, beta))
    R = set(); N = len(PL)
    # parallel coincidences
    for i, j in itertools.combinations(range(N), 2):
        if PL[i][0] == PL[j][0] and PL[i][2] != PL[j][2]:
            r = (PL[j][1] - PL[i][1]) / (PL[i][2] - PL[j][2]); R.add(r)
    T3 = {}
    for tri in itertools.combinations(range(N), 3): T3[tri] = det3(*(PL[k][0] for k in tri))
    for quad in itertools.combinations(range(N), 4):
        D0 = D1 = 0
        for pos, k in enumerate(quad):
            M = T3[tuple(x for x in quad if x != k)]
            if M == 0: continue
            sgn = -1 if pos % 2 else 1        # det [[n, -c]] expanded on the last column: sum (-1)^pos * c * minor
            D0 += sgn * M * PL[k][1]; D1 += sgn * M * PL[k][2]
        if D1 != 0: R.add(-D0 / D1)
    inside = sorted(r for r in R if a < r < b)
    return npieces.pop(), N, inside

if __name__ == '__main__':
    t = sys.argv[1]; t0 = time.time()
    if t == 'c':
        word, L = 'ABC', 1; stops = [Fr(-11, 24), Fr(-3, 8), Fr(-1, 8), Fr(3, 8)]
        rule = lambda sl: (0, 1) if sl[0] < 0 else (0, 0)
    else:
        word, L = 'AB', 0; stops = [Fr(-11, 24), Fr(-1, 8), Fr(5, 24), Fr(3, 8)]
        rule = lambda sl: (0, 0)
    res = dict(tile=t, word=word, stops=[str(s) for s in stops], chambers=[]); allok = True; npts = 0
    for a, b in zip(stops, stops[1:]):
        npc, N, W = walls(word, L, a, b, rule)
        pts = [a] + W + [b]; checks = []
        for x, y in zip(pts, pts[1:]):
            for lam, kind in ((x, 'wall'), ((x + y) / 2, 'hop')):
                r = dense.check(lam, t); ok = r['connected'] and r['manifold']; allok &= ok; npts += 1
                checks.append(dict(lam=str(lam), kind=kind, ok=ok, faces=r['faces'], pieces=r['pieces'], neck=r['neck']))
        r = dense.check(b, t); ok = r['connected'] and r['manifold']; allok &= ok; npts += 1
        checks.append(dict(lam=str(b), kind='wall', ok=ok, faces=r['faces'], pieces=r['pieces'], neck=r['neck']))
        ch = dict(a=str(a), b=str(b), pieces=npc, planes=N, walls=[str(w) for w in W], checks=checks)
        res['chambers'].append(ch)
        print(f'chamber [{a}, {b}]: {npc} pieces, {N} planes, {len(W)} interior walls {[str(w) for w in W]}; '
              f'checks ok {sum(c["ok"] for c in checks)}/{len(checks)}; faces {sorted({c["faces"] for c in checks})}', flush=True)
    res['all_ok'] = allok; res['points'] = npts
    json.dump(res, open(os.path.join(HERE, f'tower_walls_{t}.json'), 'w'), indent=1)
    print(f'{npts} exact checks, {time.time() - t0:.0f} s')
    print('FINAL ok' if allok else 'FINAL FAIL: a wall or hop point fails the one-solid check')
