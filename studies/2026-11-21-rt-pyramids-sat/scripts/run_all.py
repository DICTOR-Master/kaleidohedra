#!/usr/bin/env python3
"""Watched job rt-sat: controls, the exact class-O edge-to-edge check, and the RT torus SAT runs.
Prints PROGRESS <done/total> after each instance, a heartbeat every 10 min, RESULT lines, and FINAL ok only if every control
gives its known answer and every instance ends (SAT / UNSAT / UNDECIDED at its time cap)."""
import sys, os, json, time, subprocess, multiprocessing as mp
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); PY = sys.executable
WORKERS = int(sys.argv[1]) if len(sys.argv) > 1 else 10; TCAP = int(sys.argv[2]) if len(sys.argv) > 2 else 3600
PILOT = len(sys.argv) > 3 and sys.argv[3] == 'pilot'
def lat(*v): return ';'.join(','.join(map(str, x)) for x in v)
C = []   # (name, kind, lattice, R2, expect)
C += [('C6-2Z3', 'C6', lat((2, 0, 0), (0, 2, 0), (0, 0, 2)), 0, 'SAT'), ('C6-4Z3', 'C6', lat((4, 0, 0), (0, 4, 0), (0, 0, 4)), 0, 'SAT'),
      ('RD-fcc', 'RD', lat((2, 2, 0), (2, 0, 2), (0, 2, 2)), 0, 'SAT'), ('RD-4Z3', 'RD', lat((4, 0, 0), (0, 4, 0), (0, 0, 4)), 0, 'SAT'),
      ('TET-fcc', 'TET', lat((2, 2, 0), (2, 0, 2), (0, 2, 2)), 0, 'UNSAT'), ('TET-2Z3', 'TET', lat((2, 0, 0), (0, 2, 0), (0, 0, 2)), 0, 'UNSAT'),
      ('TET-4Z3', 'TET', lat((4, 0, 0), (0, 4, 0), (0, 0, 4)), 0, 'UNSAT'),
      ('GR-2x-R0', 'GR', lat((4, 0, 0, 0, 0, 0), (0, 0, 4, 0, 0, 0), (0, 0, 0, 0, 4, 0)), 0, 'SAT'),
      ('GR-2x-R8', 'GR', lat((4, 0, 0, 0, 0, 0), (0, 0, 4, 0, 0, 0), (0, 0, 0, 0, 4, 0)), 8, 'SAT')]
cube4phi = lat((0, 0, 0, 0, 2, 2), (0, 0, 2, 2, 0, 0), (2, 2, 0, 0, 0, 0))
RT = [(f'RT-cube4phi-R2_{r}', 'RT', cube4phi, r, None) for r in ((2, 4, 8) if PILOT else (2, 4, 6, 8, 10, 12, 14, 16, 18, 20))]
if not PILOT:
    L = json.load(open(os.path.join(ROOT, 'data', 'rt_lattices_n8_N30.json')))
    for idx, o in enumerate(L):
        for r in (4, 8, 12):
            RT.append((f'RT-lat{idx:02d}-N{o["N"]}-R2_{r}', 'RT', lat(*o['basis']), r, None))
DFS = [('E2E-RT', 'RT', 60, 'dies'), ('E2E-C6', 'C6', 60, 'alive')]
EXP = [] if PILOT else [('FRAMES1-e2e-float', 1), ('FRAMES2-e2e-float', 2)]
def run_exp(job):
    name, level = job; log = os.path.join(ROOT, 'logs', f'{name}.log')
    with open(log, 'w') as f:
        try:
            subprocess.run([PY, os.path.join(HERE, 'explore_frames_dfs.py'), '60', '2000000', str(level)], stdout=f, stderr=subprocess.STDOUT, timeout=TCAP)
        except subprocess.TimeoutExpired: pass
    last = [l for l in open(log) if l.startswith('{')]
    return name, None, {'verdict': (('alive (60-piece patch)' if "'some_branch_reaches_max': True" in last[-1] else 'dies') if last else 'UNDECIDED (time cap)')}
def run_tsat(job):
    name, kind, la, r2, exp = job
    log = os.path.join(ROOT, 'logs', f'{name}.log'); out = os.path.join(ROOT, 'data', name)
    with open(log, 'w') as f:
        p = subprocess.run([PY, os.path.join(HERE, 'tsat.py'), kind, la, str(r2), str(TCAP), out], stdout=f, stderr=subprocess.STDOUT)
    try: res = json.load(open(out + '.json'))
    except Exception: res = {'verdict': f'CRASH (exit {p.returncode}, see logs/{name}.log)'}
    return name, exp, res
def run_dfs(job):
    name, kind, mx, exp = job
    log = os.path.join(ROOT, 'logs', f'{name}.log')
    with open(log, 'w') as f:
        p = subprocess.run([PY, os.path.join(HERE, 'classO_e2e.py'), kind, str(mx)], stdout=f, stderr=subprocess.STDOUT)
    try:
        res = json.load(open(os.path.join(ROOT, 'data', f'classO-e2e-{kind}-{mx}.json')))
        res['verdict'] = 'alive' if res['reached_max'] else 'dies'
    except Exception: res = {'verdict': f'CRASH (exit {p.returncode})'}
    return name, exp, res
if __name__ == '__main__':
    os.makedirs(os.path.join(ROOT, 'logs'), exist_ok=True)
    t0 = time.time(); pool = mp.Pool(WORKERS)
    jobs = [pool.apply_async(run_dfs, (j,)) for j in DFS] + [pool.apply_async(run_exp, (j,)) for j in EXP] + [pool.apply_async(run_tsat, (j,)) for j in C + RT]
    total = len(jobs); done = set(); summary = []; last_hb = time.time(); ctrl_ok = True
    print(f'rt-sat: {total} instances ({len(DFS)} edge-to-edge checks, {len(C)} SAT controls, {len(RT)} RT tori), {WORKERS} workers, cap {TCAP} s each', flush=True)
    while len(done) < total:
        for i, j in enumerate(jobs):
            if i in done or not j.ready(): continue
            done.add(i); name, exp, res = j.get(); v = res.get('verdict')
            good = exp is None or (v is not None and v.startswith(exp))
            if exp is not None and not good: ctrl_ok = False
            if v is None or v.startswith('CRASH'): ctrl_ok = False
            row = {'name': name, 'expected': exp, 'verdict': v, **{k: res.get(k) for k in ('N', 'classes', 'placements', 'samples', 'rounds', 'seconds', 'nodes', 'deepest_patch')}}
            summary.append(row)
            print(f'RESULT {name}: {v}' + (f' (expected {exp}: {"ok" if good else "MISMATCH"})' if exp else '') +
                  f" N={res.get('N')} classes={res.get('classes')} placements={res.get('placements')} t={res.get('seconds')}s", flush=True)
            print(f'PROGRESS {len(done)/total:.3f} {len(done)}/{total} instances done ({time.time() - t0:.0f} s)', flush=True)
        if time.time() - last_hb > 600:
            print(f'HEARTBEAT {time.time() - t0:.0f} s, {len(done)}/{total} done', flush=True); last_hb = time.time()
        time.sleep(5)
    pool.close(); pool.join()
    json.dump(summary, open(os.path.join(ROOT, 'data', 'summary-pilot.json' if PILOT else 'summary.json'), 'w'), indent=1)
    rt = [s for s in summary if s['name'].startswith('RT')]
    print('RT verdicts:', {v: sum(1 for s in rt if s['verdict'] == v) for v in sorted({s['verdict'] for s in rt})}, flush=True)
    print('FINAL ok' if ctrl_ok else 'FINAL FAIL (a control gave the wrong answer or an instance crashed)', flush=True)
