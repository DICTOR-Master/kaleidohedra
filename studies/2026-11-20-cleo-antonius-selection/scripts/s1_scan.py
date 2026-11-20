"""Step 1 (computed, 50 digits): scan the slope product c = uv over (0, 1).
By #103 Theorem 5 the viewpoint T_beta keeps (b), (c), every count and uv, and maps (u, v) to (lam u, v/lam); so every (b), (c)
yantra with uv = c is the image of one with u = v = sqrt(c) (the rhombus member).  For each c: every admissible (b), (c) member
on the rhombus u = v = sqrt(c) (S from G, t from the degree-10 H1, all real roots), its odd regions (yarr.py), marmas and
sandhis (counts.py rule).  Second, a check of the reduction: at 12 random (u, v) the members and counts equal those of the
rhombus member with the same product.  Writes data/scan-c.json.  usage: python s1_scan.py N"""
import sys, os, json, time, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mpmath as mp
from multiprocessing import Pool
mp.mp.dps = 50
import yfam as Y
N = int(sys.argv[1]) if len(sys.argv) > 1 else 400

def job(args):
    mp.mp.dps = 50
    c, lam = args
    c = mp.mpf(c); u = mp.sqrt(c) * mp.mpf(lam); v = c / u
    rows = []
    for y in Y.members(u, v):
        r = Y.regions(y); m, s = Y.counts_traditional(y); mg = Y.margin(y)
        rows.append(dict(S=mp.nstr(y['S'], 30), t=mp.nstr(y['t'], 30), odd=r['odd'], odd_tri=r['odd_tri'], faces=r['faces'],
                         marma=m, sandhi=s, d=mp.nstr(Y.bindu(y)[0], 8), margin=mp.nstr(mg[0], 6), margin_at=mg[1]))
    return dict(c=str(args[0]), lam=str(lam), members=rows)

if __name__ == '__main__':
    t0 = time.time()
    cs = [mp.nstr(mp.mpf(k) / N, 20) for k in range(1, N)]
    with Pool(22) as pool:
        res = pool.map(job, [(c, 1) for c in cs], chunksize=2)
    print('PROGRESS 0.8 rhombus scan done', f'{time.time()-t0:.0f}s', flush=True)
    rng = random.Random(20261120)
    checks = [(mp.nstr(mp.mpf(rng.uniform(0.05, 0.95)), 20), mp.nstr(mp.mpf(rng.uniform(0.75, 1.3)), 20)) for _ in range(12)]
    with Pool(12) as pool:
        chk = pool.map(job, checks)
        ref = pool.map(job, [(c, 1) for c, _ in checks])
    same = all([(r['odd'], r['marma'], r['sandhi'], r['faces']) for r in a['members']] ==
               [(r['odd'], r['marma'], r['sandhi'], r['faces']) for r in b['members']] for a, b in zip(chk, ref))
    print('reduction check (12 random (u, v) vs rhombus member, same uv): counts and number of members agree:', same)
    for a in chk: print('   ', a['c'][:8], 'lam', a['lam'][:6], [(r['odd'], r['sandhi']) for r in a['members']])
    # summary: runs of equal (number of members, counts)
    prev = None; runs = []
    for r in res:
        key = tuple((m['odd'], m['odd_tri'], m['marma'], m['sandhi'], m['faces']) for m in r['members'])
        if key != prev: runs.append([r['c'], r['c'], key]); prev = key
        else: runs[-1][1] = r['c']
    print('runs of c with the same members and counts (members: odd, odd triangles, marmas, sandhis, all regions):')
    for a, b, k in runs: print(f'   c in [{a[:8]}, {b[:8]}]: {list(k)}')
    json.dump(dict(N=N, scan=res, checks=chk, check_ref=ref, runs=runs), open(os.path.join(Y.ROOT, 'data', 'scan-c.json'), 'w'), indent=0)
    print(f'time {time.time()-t0:.0f}s'); print('FINAL ok' if same else 'FINAL FAIL (reduction check)')
