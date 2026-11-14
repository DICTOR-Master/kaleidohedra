#!/usr/bin/env python3
"""Forced fixed points (14 Nov 2026), task 2(iii): the cuboctahedron with square pyramids on two ADJACENT squares.
Extends the octet-aligned periodic exact-cover search of studies/2026-11-14-chat-handoff (which found none up to index 24)
to index 48, with all 48 orientations of the cube group (so mirrors and point inversion are included).

Reused code, executed from its files, not retyped:
  studies/2026-11-04-tetra-sweep/scripts/tile_octet.py   hnf() (sublattices of index N), solve() (exact cover, Knuth's algorithm X)
  studies/2026-11-14-chat-handoff/scripts/handoff_tests.py   piece_cells(), act(), orients(), torus_cover() (the octet-cell model)
Parallel: the sublattices of each index are split into chunks over a process pool (torus_cover runs on each chunk unchanged; only
the generator hnf it calls is replaced by the chunk). Every cover found is re-verified cell by cell inside torus_cover.
Controls: rhombohedron (1 O + 2 T) tiles at N = 1 (positive); the opposite pair tiles at N = 4 (positive); the cuboctahedron alone
has no cover at N = 16 (negative, it does not tile alone).
Usage: adjacent_cover.py [--pilot] [workers]. Output: PROGRESS lines, data/adjacent-cover(-pilot).json, last line FINAL ok / FINAL FAIL.
"""
import sys, os, json, time, itertools
import numpy as np
from multiprocessing import Pool

here = os.path.dirname(os.path.abspath(__file__)); STUD = os.path.join(here, '..', '..')
PILOT = '--pilot' in sys.argv
args = [a for a in sys.argv[1:] if not a.startswith('--')]
WORKERS = int(args[0]) if args else 4
DATA = os.path.join(here, '..', 'data')
T0 = time.time()

_tile = open(os.path.join(STUD, '2026-11-04-tetra-sweep', 'scripts', 'tile_octet.py')).read()
TO = {}; exec(_tile[:_tile.index("if __name__ == '__main__':")], TO)
_h = open(os.path.join(STUD, '2026-11-14-chat-handoff', 'scripts', 'handoff_tests.py')).read()
NS = {'np': np, 'itertools': itertools, 'TO': TO, 'time': time}
exec(_h[_h.index('SIG = list(itertools.product'):_h.index("OUT['lead8_cover'] = {}")], NS)
HNF_ALL = TO['hnf']

def chunk_job(job):
    """job = (name, ks, N, chunk, nchunks): run torus_cover on one slice of the index-N sublattices"""
    name, ks, N, k, n = job
    full = list(HNF_ALL(N))
    TO['hnf'] = lambda NN, part=full[k::n]: iter(part)
    cells = NS['RHOMB'] if ks == 'RHOMB' else NS['piece_cells'](ks)
    t = time.time(); r = NS['torus_cover'](cells, N, 'all'); TO['hnf'] = HNF_ALL
    r['chunk'] = k; r['sec'] = round(time.time() - t, 1)
    return r

def run(pool, name, ks, N):
    n = WORKERS * 4
    jobs = [(name, ks, N, k, n) for k in range(n)]
    found = None; tried = 0; t = time.time()
    for r in pool.imap_unordered(chunk_job, jobs):
        tried += r['tori_tried']
        if r['found'] and found is None: found = r
    total = sum(1 for _ in HNF_ALL(N))
    ok_count = tried == total
    print(f'      {name} N={N}: {"FOUND" if found else "none"} (tori {tried} of {total}, {round(time.time() - t, 1)} s)', flush=True)
    return {'N': N, 'found': bool(found), 'tori_tried': tried, 'tori_total': total, 'all_tori_searched': ok_count or bool(found),
            'witness': found, 'sec': round(time.time() - t, 1)}

if __name__ == '__main__':
    OUT = {'controls': {}, 'adjacent': []}; CH = []
    def check(ok, what):
        CH.append((bool(ok), what)); print(('ok   ' if ok else 'FAIL ') + what, flush=True)
    with Pool(WORKERS) as pool:
        r = run(pool, 'CONTROL rhombohedron', 'RHOMB', 1); OUT['controls']['rhombohedron N=1'] = r
        check(r['found'], 'CONTROL rhombohedron (1 O + 2 T) tiles at N = 1 (positive)')
        r = run(pool, 'CONTROL opposite pair', ['+x', '-x'], 4); OUT['controls']['opposite N=4'] = r
        check(r['found'], 'CONTROL CO + 2 pyramids on OPPOSITE squares tiles at N = 4 (positive)')
        if not PILOT:
            r = run(pool, 'CONTROL cuboctahedron alone', [], 16); OUT['controls']['CO alone N=16'] = r
            check(not r['found'] and r['all_tori_searched'], 'CONTROL cuboctahedron alone: no cover at N = 16 (negative)')
        NS_ = list(range(4, (16 if PILOT else 48) + 1, 4))
        for i, N in enumerate(NS_):
            print(f'PROGRESS {i / len(NS_):.2f} adjacent pair, index {N}', flush=True)
            r = run(pool, 'CO + 2 pyramids ADJACENT', ['+x', '+y'], N); OUT['adjacent'].append(r)
            check(r['all_tori_searched'], f'adjacent pair, index {N}: every sublattice searched ({r["tori_tried"]})')
            json.dump(OUT, open(os.path.join(DATA, 'adjacent-cover-pilot.json' if PILOT else 'adjacent-cover.json'), 'w'), indent=1, default=str)
            if r['found']:
                print(f'RESULT the adjacent pair TILES (octet-aligned, periodic, index {N})', flush=True); break
    found = [r['N'] for r in OUT['adjacent'] if r['found']]
    OUT['verdict'] = (f'TILES at index {found[0]}' if found else f'no octet-aligned periodic cover up to index {OUT["adjacent"][-1]["N"]}')
    OUT['checks'] = CH; OUT['seconds'] = round(time.time() - T0, 1)
    json.dump(OUT, open(os.path.join(DATA, 'adjacent-cover-pilot.json' if PILOT else 'adjacent-cover.json'), 'w'), indent=1, default=str)
    print('VERDICT adjacent pair:', OUT['verdict'])
    print(f'{sum(c[0] for c in CH)}/{len(CH)} checks ok, {OUT["seconds"]} s')
    print('PROGRESS 1.00 done')
    print('FINAL ok' if all(c[0] for c in CH) else 'FINAL FAIL')
