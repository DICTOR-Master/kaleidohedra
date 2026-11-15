"""Where do the swaps go at a coarser step? For the main rule, list the swaps counted at step 1 that are not counted at a coarser
step s, and classify each by what the logger sees at step s in the interval that contains it: a cell of the swap vanishes or appears
in that interval (the swap falls together with a death / merge / birth / split: side-shedding just before a cell vanishes is the
foam case), or nothing else happens there (a genuine cancellation within the step).
Usage: python diag_lost_swaps.py FRAMES(.jsonl or .jsonl.gz) W P STEP [by_segment] -> prints a table and DIAG_OK"""
import sys, os, json, gzip
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scripts'))
import eventlog as EL, pairing as PR
path, W, P, s = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4])
byseg = len(sys.argv) > 5 and sys.argv[5] == 'by_segment'
op = gzip.open if path.endswith('.gz') else open
fr = [EL.Tiling.from_json(l) for l in op(path, 'rt') if l.strip()]
print('PROGRESS 0.2 frames read', flush=True)
ev1, s1 = PR.pair_census(fr, W, P, by_segment=byseg, keep_events=True)
print('PROGRESS 0.6 step 1 done', flush=True)
frs = fr[::s]
evs, ss = PR.pair_census(frs, W, P, by_segment=byseg, keep_events=True)
key = lambda e: (tuple(map(str, e['lost'])), tuple(map(str, e['gained'])))
have = Counter(key(e) for e in evs)
miss = []
for e in ev1:
    if have[key(e)]: have[key(e)] -= 1
    else: miss.append(e)
ts = [F.t for F in frs]; inc = ts[-1] >= ts[0]
why = Counter()
for e in miss:
    t = e['t']
    i = max(j for j in range(len(ts) - 1) if (ts[j] < t if inc else ts[j] > t)) if (ts[0] < t if inc else ts[0] > t) else 0
    A, B = frs[i], frs[min(i + 1, len(frs) - 1)]
    cells = {str(x) for x in e['lost']} | {str(x) for x in e['gained']}
    gone = cells & {str(x) for x in A.cells - B.cells}; new = cells & {str(x) for x in B.cells - A.cells}
    if gone: why['a cell of the swap vanishes in that interval'] += 1
    elif new: why['a cell of the swap appears in that interval'] += 1
    else:
        near = [x for x in EL.classify(A, B, 0.9, byseg) if cells & set(x['cells']) and x['net'] != 0]
        why['a neighbouring cell vanishes or appears there' if near else 'no cell change nearby (cancelled within the step)'] += 1
print(f'step 1: {s1["swaps"]} swaps; step {s}: {ss["swaps"]}; step-1 swaps not found at step {s}: {len(miss)}')
for k, v in why.most_common(): print(f'  {v:5d}  {k}')
print(f'paired at step 1: {s1["swaps_paired"]}, direct {s1["swaps_direct"]}, cancelled swaps {s1["swaps_cancelled_flicker"]}, '
      f'cancelled halves {s1["halves_cancelled_flicker"]}')
print('DIAG_OK')
