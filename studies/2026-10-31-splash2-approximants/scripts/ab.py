# Splash Rules II, approximants, part 2: the Ammann-Beenker tiling and its periodic approximants (exact).
# Run on dicto-big-brother: ~/geom/bin/python ab.py out/  (multiprocessing, 22 workers)
# Z^4, physical star e_k = (cos k pi/4, sin k pi/4), internal eps_k = (cos 3k pi/4, sin 3k pi/4). Approximant planes E' are
# rational 2-planes with all six Pluecker coordinates positive (same orientation as E, so the AB rhombs and squares fit).
# Tile {i,j} (i<j): square if j - i = 2, 45-degree rhomb otherwise. Vertex star: the set of the 8 edge directions
# d = k (+e_k), d = k + 4 (-e_k), classified up to the dihedral group of the octagon.
import sys, os, json, random, math, itertools
from fractions import Fraction as Fr
from multiprocessing import Pool
from qf import QF
from zono import int_kernel, minors2, zonogon, area, arrangement, lattice_points

OUT = sys.argv[1] if len(sys.argv) > 1 else 'out'; os.makedirs(OUT, exist_ok=True)
PAIRS = [(i, j) for i in range(4) for j in range(i + 1, 4)]

def canon(star):
    b = tuple(star); best = None
    for r in range(8):
        for s in (1, -1):
            t = tuple(b[(s * d + r) % 8] for d in range(8))
            if best is None or t < best: best = t
    return ''.join('1' if x else '0' for x in best)

def star_of(y, V, gens):
    return tuple((y[0] + g[0], y[1] + g[1]) in V for g in gens) + tuple((y[0] - g[0], y[1] - g[1]) in V for g in gens)

# ---------- the quasicrystal: exact areas in Q(sqrt 2)
def ab_limit():
    s = QF(0, Fr(1, 2), 2)                      # sqrt2/2
    one, zero = QF(1, 0, 2), QF(0, 0, 2)
    eps = [(one, zero), (-s, s), (zero, -one), (s, s)]
    W = zonogon(eps); A = area(W)
    cells = arrangement(W, eps)
    fr = {}
    for P, st in cells:
        c = canon(st); fr[c] = fr.get(c, zero) + area(P) / A
    tot = zero
    for v in fr.values(): tot = tot + v
    assert tot == 1
    return A, fr

# ---------- one rational plane
def plane_stats(job):
    name, u, v, gammas = job
    N = int_kernel([u, v]); assert len(N) == 2
    Lam = int_kernel(N); assert len(Lam) == 2
    p = minors2(Lam[0], Lam[1])
    if any(x < 0 for x in p.values()): p = {k: -x for k, x in p.items()}
    if any(x <= 0 for x in p.values()): return {'name': name, 'ok': False, 'why': 'pluecker sign'}
    gens = [(Fr(N[0][k]), Fr(N[1][k])) for k in range(4)]
    W = zonogon(gens); A = area(W)
    assert A == sum(p.values())
    res = {'name': name, 'ok': True, 'u': u, 'v': v, 'Lam': Lam, 'K': N, 'pl': {f'{i}{j}': p[(i, j)] for i, j in PAIRS}, 'N': int(A)}
    # offset average: arrangement cell areas
    cells = arrangement(W, gens); avg = {}
    for P, st in cells:
        c = canon(st); avg[c] = avg.get(c, 0) + area(P)
    res['avg'] = {c: str(x) for c, x in avg.items()}
    runs = []
    for gam in gammas:
        try:
            pts = lattice_points(W, gam)
        except ValueError:
            continue
        V = set(pts); assert len(V) == A
        ig = [(int(g[0]), int(g[1])) for g in gens]
        cnt = {}; tiles = {f'{i}{j}': 0 for i, j in PAIRS}; edges = {}; cls = {}
        for y in pts:
            c = canon(star_of(y, V, ig)); cls[y] = c; cnt[c] = cnt.get(c, 0) + 1
        for y in pts:
            for i, j in PAIRS:
                gi, gj = ig[i], ig[j]
                if (y[0] + gi[0], y[1] + gi[1]) in V and (y[0] + gj[0], y[1] + gj[1]) in V and (y[0] + gi[0] + gj[0], y[1] + gi[1] + gj[1]) in V:
                    tiles[f'{i}{j}'] += 1
            for k in range(4):
                z = (y[0] + ig[k][0], y[1] + ig[k][1])
                if z in V:
                    key = '|'.join(sorted((cls[y], cls[z]))); edges[key] = edges.get(key, 0) + 1
        runs.append({'gamma': [str(g) for g in gam], 'stars': cnt, 'tiles': tiles, 'edges': edges})
    res['runs'] = runs
    return res

def rnd_gamma(rng):
    return (Fr(rng.randrange(1, 10 ** 9), 10 ** 9 + 7), Fr(rng.randrange(1, 10 ** 9), 10 ** 9 + 9))

if __name__ == '__main__':
    rng = random.Random(20261031)
    A, lim = ab_limit()
    print('AB limit: window area', A, '; vertex stars', len(lim))
    for c, f in sorted(lim.items(), key=lambda x: -float(x[1])): print('  ', c, c.count('1'), 'edges', f, float(f))
    jobs = []
    # square approximants: t = a/b, plane rows (b, a, 0, -a), (0, a, b, a)
    ts = sorted({Fr(a, b) for b in range(1, 25) for a in range(1, b + 1) if Fr(1, 2) <= Fr(a, b) <= 1})
    conv = [Fr(1, 2), Fr(3, 4), Fr(7, 10), Fr(17, 24), Fr(41, 58), Fr(2, 3), Fr(5, 7), Fr(12, 17), Fr(29, 41), Fr(99, 140), Fr(70, 99)]
    for t in sorted(set(ts) | set(conv)):
        a, b = t.numerator, t.denominator
        jobs.append((f't={t}', [b, a, 0, -a], [0, a, b, a], [rnd_gamma(rng) for _ in range(3)]))
    # general planes near E: u ~ M (1, s, 0, -s), v ~ M (0, s, 1, s), integer noise
    s = math.sqrt(2) / 2; k = 0
    while k < 240:
        M = rng.choice([3, 4, 5, 6, 7, 8, 10, 12, 14]); e = max(1, M // 3)
        u = [round(M * x) + rng.randint(-e, e) for x in (1, s, 0, -s)]
        v = [round(M * x) + rng.randint(-e, e) for x in (0, s, 1, s)]
        p = minors2(u, v)
        if any(x <= 0 for x in p.values()): continue
        jobs.append((f'r{k}', u, v, [rnd_gamma(rng) for _ in range(3)])); k += 1
    with Pool(22) as pool:
        res = pool.map(plane_stats, jobs, chunksize=1)
    ok = [r for r in res if r['ok']]
    print('planes', len(res), 'ok', len(ok))
    json.dump({'limit': {'area': repr(A), 'freq': {c: {'a': str(f.a), 'b': str(f.b)} for c, f in lim.items()}}, 'planes': res},
              open(os.path.join(OUT, 'ab.json'), 'w'))
    print('written')
