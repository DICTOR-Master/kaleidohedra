"""Item 7: no selection of dual copies covers each pentagon exactly once.
Two independent methods: CP-SAT (equality constraints) and a plain
Algorithm X (Knuth) written here, each on A*, B*, C3* alone and on all
300 dual copies together."""
import json, sys, time
from common import Log
from ortools.sat.python import cp_model

L = Log('logs/s8_exactcover.log')
inst = json.load(open('data/dual_cover_instance.json'))
fams = {'A': inst['A']['sets'], 'B': inst['B']['sets'], 'C3': inst['C3']['sets']}
fams['all'] = fams['A'] + fams['B'] + fams['C3']

def algx(sets, limit=600.0):
    t0 = time.time()
    cov = [[] for _ in range(720)]
    for c, s in enumerate(sets):
        for p in s:
            cov[p].append(c)
    sets = [set(s) for s in sets]
    nodes = [0]
    def rec(uncov, alive):
        nodes[0] += 1
        if time.time() - t0 > limit:
            raise TimeoutError
        if not uncov:
            return True
        best, bc = None, None
        for p in uncov:
            cs = [c for c in cov[p] if c in alive]
            if best is None or len(cs) < len(bc):
                best, bc = p, cs
                if not cs:
                    return False
        for c in bc:
            s = sets[c]
            nalive = {d for d in alive if not (sets[d] & s)}
            if rec(uncov - s, nalive):
                return True
        return False
    found = rec(set(range(720)), set(range(len(sets))))
    return found, nodes[0], time.time() - t0

for name, sets in fams.items():
    n = len(sets)
    m = cp_model.CpModel()
    x = [m.NewBoolVar('') for _ in range(n)]
    cov = [[] for _ in range(720)]
    for c, s in enumerate(sets):
        for p in s:
            cov[p].append(c)
    for p in range(720):
        m.Add(sum(x[c] for c in cov[p]) == 1)
    sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = 100; sv.parameters.num_workers = 24
    st = sv.Solve(m)
    L(f'{name}: {n} copies; CP-SAT exact cover: {sv.StatusName(st)} ({sv.WallTime():.1f} s)')
    try:
        f, nn, t = algx(sets, 60.0)
        L(f'{name}: Algorithm X: exact cover exists = {f} ({nn} nodes, {t:.1f} s, complete search)')
        ok = (not f) and sv.StatusName(st) == 'INFEASIBLE'
    except TimeoutError:
        L(f'{name}: Algorithm X: timeout')
        ok = sv.StatusName(st) == 'INFEASIBLE'
    L.check(f'{name}: no exact cover (proved)', ok, True)
L.final()
