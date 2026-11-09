"""03: systematic scan of Escher stepped-hexagon pieces (free parameters).

Family C3 (three-fold, the seat symmetry): top = even plates (c0,u0,w0), odd plates (c1,u1,w1), every plate CLIMBS
ccw at the rim (w > u: DICTO's 'each plate sloping up into the next'); climbs r = w-u in 1..RMAX; risers wherever the
next plate starts lower or higher; rise per turn S = 3(r0+r1).  Heights are free up to a common shift
(min(u0,u1) = 0); centres 0..CMAX.  Bottoms: every MIXED reassembly of the tops of the 3 lower cells (uniform ones
are periodic by Theorem A) and the 6 C2-turned tops (the screw turned end over end).
Family C1 (one helical ramp, DICTO's single staircase): rim climbs r_k in {1,2,3} with S = sum in {6,12,18},
one riser at D_0, plate centres at the mean of their rim ends + e (e in -2..4); bottoms: every reassembly (lean 1/2,
turns 0..5 of each lower cell) and C2 turned tops.
Each piece: battery() proper motions; mirror copies only for pieces that pass (no point adding freedom to a
piece that already fails).  usage: 03_scan.py FAMILY SHARD NSHARDS [SAMPLE]
"""
import sys, time, json, random, itertools
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from multiprocessing import Pool
from escher import *

FAM, SH, NS = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
SAMPLE = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
RMAX, CMAX = 4, 12


def tops_c3():
    for u0 in range(0, 10):
        for u1 in range(0, 10):
            if min(u0, u1) != 0:
                continue
            for r0 in range(1, RMAX + 1):
                for r1 in range(1, RMAX + 1):
                    for c0 in range(CMAX + 1):
                        for c1 in range(CMAX + 1):
                            yield ('C3', (c0, u0, u0 + r0, c1, u1, u1 + r1)), c3_top(c0, u0, u0 + r0, c1, u1, u1 + r1)


def tops_c1():
    for rs in itertools.product((1, 2, 3), repeat=6):
        if sum(rs) not in (6, 12, 18):
            continue
        h = [0]
        for r in rs:
            h.append(h[-1] + r)
        for e in range(-2, 5):
            tr = [((h[s] + h[s + 1]) // 2 + e + 6, h[s], h[s + 1]) for s in range(6)]
            # the leading corner of plate 5 is D_0 itself (value h[6]); riser of -S there
            yield ('C1', (rs, e)), top_from(tr)


def work(item):
    tag, top = item
    out = []
    for b, info in bottoms_for(top, c3=(tag[0] == 'C3')).items():
        if info[3] == 'uniform':
            continue
        P = (top, b)
        if not valid(P) or thickness_sum(P) != 216:
            continue
        r = battery([P])
        rec = {'tag': tag, 'bottom': [str(x) for x in info], 'verdict': r['verdict'],
               'patch': r.get('patch_words'), 'pw': r.get('periodic_words'), 'states': r.get('states')}
        if r['verdict'] in ('CANDIDATE',) or r['verdict'].startswith('PERIODIC'):
            rm = battery([P], mirrors=True)
            rec['mirrors'] = rm['verdict']
            rec['mirror_pw'] = rm.get('periodic_words')
        out.append(rec)
    return out


if __name__ == '__main__':
    t0 = time.time()
    gen = tops_c3() if FAM == 'C3' else tops_c1()
    rnd = random.Random(11)
    items = [it for n, it in enumerate(gen) if n % NS == SH and rnd.random() < SAMPLE]
    print(f'{FAM} shard {SH}/{NS}: {len(items)} tops', flush=True)
    cnt = {}
    wordsets = {}
    cands = []
    nrec = 0
    with Pool(22) as pool:
        for k, recs in enumerate(pool.imap_unordered(work, items, chunksize=20)):
            for r in recs:
                nrec += 1
                kk = r['bottom'][0] + ' ' + r['verdict'] + (' mirrors:' + r['mirrors'] if 'mirrors' in r else '')
                cnt[kk] = cnt.get(kk, 0) + 1
                if r['verdict'].startswith('PERIODIC'):
                    key = (r['verdict'], ','.join(r['pw']))
                    wordsets[key] = wordsets.get(key, 0) + 1
                if r['verdict'] == 'CANDIDATE':
                    cands.append(r)
            if k % 2000 == 0:
                print(f'  heartbeat {k}/{len(items)} tops, {nrec} pieces, {time.time()-t0:.0f}s, {cnt}', flush=True)
    print(f'pieces tested (valid, volume ok, non-uniform bottom): {nrec}')
    print('verdicts:', cnt)
    print('periodic word sets (verdict, c/h words of length 4 realised by periodic tilings): count')
    for k, v in sorted(wordsets.items(), key=lambda x: -x[1]):
        print(f'   {k[0]:11s} {v:7d}  {k[1]}')
    print(f'candidates: {len(cands)}')
    for c in cands[:50]:
        print('   CAND', json.dumps(c))
    json.dump({'counts': cnt, 'wordsets': {f'{a}|{b}': v for (a, b), v in wordsets.items()}, 'candidates': cands},
              open(f'data/03_scan_{FAM}_{SH}of{NS}{"_pilot" if SAMPLE < 1 else ""}.json', 'w'), indent=1)
    print(f'time {time.time()-t0:.0f}s')
    print('FINAL ok' if nrec > 0 else 'FINAL FAIL: nothing tested')
