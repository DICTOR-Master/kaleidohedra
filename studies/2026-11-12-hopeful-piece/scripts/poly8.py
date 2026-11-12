# poly8.py, 13 Nov 2026 (aim 3, lead 1 of the hopeful-piece hunt): every free unkeyed poly-RD of n cells, kill test on fcc tori
# whose index is a multiple of n, up to KMAX pieces per period (index <= KMAX * n), then the ball of radius RMAX for survivors.
# Same kill test as hunt.py (P family) with a faster torus step: sites are reduced to a torus by integer Hermite-normal-form
# arithmetic (no floats), and placements are x + image for every torus site x (every translate once; hunt.py also looped over the
# anchor cell, which gives the same set). Ball step: hunt.py's poly_sat, unchanged.
# usage: poly8.py gen NMAX out.json                          (free polyforms of NMAX cells, canonical under the 48 symmetries)
#        poly8.py run pieces.json KMIN KMAX RMAX SHARD/NSHARDS out.json
#        poly8.py ctl NMAX KMAX                             (control: n <= NMAX through this code; prints counts to compare with hp-main)
import sys, os, json, time
here = os.path.dirname(os.path.abspath(__file__))
_argv = sys.argv; sys.argv = ['hunt.py', 'none']
exec(open(os.path.join(here, 'hunt.py')).read().split('# ---------------------------------------------------------------- modes')[0])
sys.argv = _argv
B3INV2 = np.array([[1, 1, -1], [1, -1, 1], [-1, 1, 1]])            # 2 * inv(B3): lattice coords c = x @ B3INV2 / 2
def to_c(X):
    X = np.asarray(X); Y = X @ B3INV2; assert (Y % 2 == 0).all(); return Y // 2
class Torus:
    def __init__(self, M):
        (a, _, _), (b, d, _), (c, e, f) = M; self.M = np.array(M); self.a, self.d, self.f = a, d, f; self.N = a * d * f
        g = np.array([(i, j, k) for k in range(f) for j in range(d) for i in range(a)]); self.sites = g   # canonical coords, index = i + a(j + d k)
    def red(self, C):                                               # C (..., 3) lattice coords -> site index
        C = C.copy(); M = self.M
        k = np.floor_divide(C[..., 2], self.f); C -= k[..., None] * M[2]
        k = np.floor_divide(C[..., 1], self.d); C -= k[..., None] * M[1]
        k = np.floor_divide(C[..., 0], self.a); C -= k[..., None] * M[0]
        return C[..., 0] + self.a * (C[..., 1] + self.d * C[..., 2])
def images_c(P):
    out = {norm([app(OH[g], c) for c in P]) for g in range(48)}
    return [to_c(np.array(I)) for I in sorted(out)]
def torus_fill(IMG, T):
    """exact cover of the torus by translates x + I (every site x, every image I); True = a periodic filling exists"""
    pl = set()
    for I in IMG:
        cells = T.red(T.sites[:, None, :] + I[None, :, :])          # (N, n)
        for row in cells:
            if len(set(row.tolist())) == len(row): pl.add(tuple(sorted(row.tolist())))
    pl = sorted(pl); cover = [[] for _ in range(T.N)]
    for p, cells in enumerate(pl):
        for cc in cells: cover[cc].append(p + 1)
    if any(not c for c in cover): return False
    s = Cadical153(); top = len(pl)
    for lits in cover:
        s.add_clause(lits)
        if len(lits) > 1:
            enc = CardEnc.atmost(lits, 1, top_id=top, encoding=EncType.seqcounter); top = max(top, enc.nv)
            for cl in enc.clauses: s.add_clause(cl)
    r = s.solve(); s.delete(); return r
TOR = {}
def tor_list(n, kmin, kmax):
    key = (n, kmin, kmax)
    if key not in TOR:
        reps, _ = torus_orbits(n * kmax, list(range(48)), n); TOR[key] = [(N, Torus(M)) for N, M, c in reps if N >= n * kmin]
    return TOR[key]
def judge8(P, kmin, kmax, rmax):
    n = len(P); IMG = images_c(P)
    for N, T in tor_list(n, kmin, kmax):
        if torus_fill(IMG, T): return f'killed {N}'
    for R in range(1, rmax + 1):
        bx = ball_xyz(R)
        if not poly_sat(P, bx, bx, lambda y: y): return f'untileable R{R}'
    return 'SURVIVOR'
def gen(nmax):
    lv = {1: {((0, 0, 0),)}}
    for n in range(2, nmax + 1):
        nxt = set(); t = time.time()
        for i, P in enumerate(lv[n - 1]):
            Ps = set(P)
            for c in P:
                for d in NB:
                    y = tuple(a + b for a, b in zip(c, d))
                    if y not in Ps: nxt.add(free_canon(list(P) + [y]))
            if n == nmax and i % 500 == 0: print(f'PROGRESS {0.9 * i / len(lv[n - 1]):.3f} gen n={n} {i}/{len(lv[n - 1])}', flush=True)
        lv[n] = nxt
    return lv
mode = sys.argv[1]
if mode == 'gen':
    NMAX, OUT = int(sys.argv[2]), sys.argv[3]; lv = gen(NMAX)
    log('free poly-RDs by size:', {n: len(v) for n, v in lv.items()})
    json.dump(sorted(lv[NMAX]), open(OUT, 'w')); print('FINAL ok', flush=True)
elif mode == 'ctl':
    NMAX, KMAX = int(sys.argv[2]), int(sys.argv[3]); lv = polyforms(NMAX); cnt = {}
    for n in range(1, NMAX + 1):
        for P in sorted(lv[n]):
            v = judge8(P, 1, KMAX if n > 1 else 1, 2); cnt[f'{n}|{v}'] = cnt.get(f'{n}|{v}', 0) + 1
        print(f'PROGRESS {n / NMAX:.3f} ctl n={n}', flush=True)
    log('CTL', json.dumps(dict(sorted(cnt.items()))))
    hp = {'1|killed 1': 1, '2|killed 2': 1, '3|killed 3': 4, '4|killed 4': 19, '4|killed 8': 1, '5|killed 5': 103, '5|killed 10': 28,
          '6|killed 6': 928, '6|killed 12': 281, '6|killed 24': 2}     # hp-main summary (n <= 6, cap min(24, 8n))
    ok = all(cnt.get(k) == v for k, v in hp.items() if int(k.split('|')[0]) <= NMAX) and sum(cnt.values()) == sum(v for k, v in hp.items() if int(k.split('|')[0]) <= NMAX)
    print('FINAL ok' if ok else 'FINAL FAIL: control differs from hp-main', flush=True)
elif mode == 'run':
    PJ, KMIN, KMAX, RMAX, SH, OUT = sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6], sys.argv[7]
    k_sh, n_sh = map(int, SH.split('/')); allP = [tuple(map(tuple, P)) for P in json.load(open(PJ))]; mine = allP[k_sh::n_sh]
    res = []; cnt = {}; step = max(1, len(mine) // 200)
    log(f'{len(allP)} pieces, this shard {len(mine)}; tori index {KMIN}n..{KMAX}n (multiples of n), balls to R{RMAX}')
    for i, P in enumerate(mine):
        v = judge8(P, KMIN, KMAX, RMAX); cnt[v] = cnt.get(v, 0) + 1
        if v == 'SURVIVOR': res.append(list(P)); log('SURVIVOR poly', P)
        if (i + 1) % step == 0 or i + 1 == len(mine): print(f'PROGRESS {(i + 1) / len(mine):.3f} shard {SH} {i + 1}/{len(mine)} {json.dumps(cnt)}', flush=True)
    json.dump(dict(kmin=KMIN, kmax=KMAX, rmax=RMAX, shard=SH, pieces=len(mine), counts=cnt, survivors=res), open(OUT, 'w'))
    log('COUNTS', SH, json.dumps(cnt)); print('FINAL ok', flush=True)
