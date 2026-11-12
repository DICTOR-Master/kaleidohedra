# deep3.py (13 Nov 2026): third check of the keyed-RD candidates (no torus to index 64, fill R8): long box tori.
# Every torus of index 65..NMAX whose lattice-coordinate HNF is diagonal (a, d, f; periods a, d, f along the three fcc basis
# vectors), one per O_h orbit, plus the ball R10. These reach periods far longer than index 64 allows along one direction.
# usage: deep3.py <deep2 json files> NMAX SHARD/NSHARDS out.json
import sys, os, json, time
here = os.path.dirname(os.path.abspath(__file__)); J, NMAX, SH, OUT = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
sys.argv = ['hunt.py', 'none']; exec(open(os.path.join(here, 'hunt.py')).read().split('# ---------------------------------------------------------------- modes')[0])
k_sh, n_sh = map(int, SH.split('/'))
S = []
for f in J.split(','): S += [x[0] for x in json.load(open(f)) if 'no torus to 64' in x[-1]]
mine = S[k_sh::n_sh]
seen = {}
for n in range(65, NMAX + 1):
    for a in range(1, n + 1):
        if n % a: continue
        for d in range(1, n // a + 1):
            if (n // a) % d: continue
            f = n // a // d; M = ((a, 0, 0), (0, d, 0), (0, 0, f)); W = np.array(M) @ B3
            key = min(hnf(np.rint((W @ np.array(OH[g]).T) @ B3I).astype(int).tolist()) for g in range(48))
            seen.setdefault(key, (n, M))
TOR = sorted(seen.values()); log(f'{len(S)} candidates, this part {len(mine)}; {len(TOR)} diagonal box tori of index 65..{NMAX} up to O_h')
BALLS[10] = ball(10); out = []
for si, H in enumerate(mine):
    F = fit_table(np.array(H)); st = np.nonzero(arc(F))[0].tolist(); verdict = None
    for i, (n, M) in enumerate(TOR):
        print(f'PROGRESS {(si + i / len(TOR)) / len(mine):.3f} part {SH} candidate {si} torus {i}/{len(TOR)} index {n} {M}', flush=True)
        if sat_fill(F, st, torus_nbr(M).tolist()): verdict = f'killed {n} {M}'; break
    if verdict is None: verdict = f'no box torus 65..{NMAX}; ' + ('fills R10' if sat_fill(F, st, BALLS[10]) else 'untileable R10')
    log(f'candidate {si}: {verdict}'); out.append([H, verdict])
json.dump(out, open(OUT, 'w')); print('FINAL ok', flush=True)
