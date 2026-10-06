"""Runs discover.py's two-way search with the bottom-up pass spread over all cores."""
import sys, json, time
from multiprocessing import Pool
import discover as D
from enumerate_lib import canon

def job(args):
    typ, starts, seed = args
    keep = {typ: D.PARAMS[typ]}
    saved = D.PARAMS
    D.PARAMS = keep
    try:
        return [S for S in D.flatten(D.bottom_up(starts, seed))]
    finally:
        D.PARAMS = saved

if __name__ == '__main__':
    starts = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    t = time.time()
    with Pool() as pool:
        bu_async = pool.map_async(job, [(typ, starts, 1000 * k + i) for k, typ in enumerate(D.PARAMS) for i in range(4)])
        td = D.top_down()
        print('top-down', len(D.flatten(td)), round(time.time() - t), 's', flush=True)
        bu_sets = [S for part in bu_async.get() for S in part]
    print('bottom-up raw', len(bu_sets), round(time.time() - t), 's', flush=True)
    td_list = D.flatten(td)
    td_keys = {canon(S): S for S in td_list}
    bu_keys = {}
    for S in bu_sets: bu_keys.setdefault(canon(S), S)
    recs = []
    for k, S in td_keys.items():
        r = D.record(S); r['found_bottom_up'] = k in bu_keys; recs.append(r)
    recs.sort(key=lambda r: (r['directions'], r['type'], r['line_angles'], r['volume']))
    extra = [D.record(S) for k, S in bu_keys.items() if k not in td_keys]
    json.dump({'special_angles': [round(s, 4) for s in D.SPECIAL], 'targets': recs, 'bottom_up_only': extra}, open('data/geometry-targets.json', 'w'), indent=1)
    from collections import Counter
    c_all = Counter(r['type'] for r in recs); c_bu = Counter(r['type'] for r in recs if r['found_bottom_up'])
    for typ in D.PARAMS: print(f'{typ}: {c_all[typ]} top-down, {c_bu[typ]} also bottom-up')
    print('bottom-up shapes NOT in top-down:', len(extra))
