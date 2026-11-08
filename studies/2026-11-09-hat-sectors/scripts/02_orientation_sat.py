# Task 1b/2: which sets of hat orientations can tile a large hexagonal disc of the kite grid?
# A 3D hat piece made of RD (or TRD) sectors can only reach half of the 12 kite-grid orientations by
# motions that keep the layer's relief (see README).  We test the orientation sets with SAT:
#   ALL12 (control, must be SAT), C6 = rotations only (control, must be UNSAT: hat needs reflections),
#   D3CM = {rot 0,120,240} + reflections in centre-midpoint lines   (RD/fcc layer, proper motions)
#   D3CV = {rot 0,120,240} + reflections in centre-vertex lines     (TRD/hcp layer, any motions)
# Disc: every kite of hexagons with hex distance <= R covered exactly once; placements may stick out
# into a 3-hexagon margin (covered at most once there).
# usage: python -u 02_orientation_sat.py R [sets...]
import sys, time
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from hatgrid import *
from pysat.formula import CNF, IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical153

SETS = {
    'ALL12': LIN,
    'C6': [('r', j) for j in range(6)],
    'D3CM': [('r', 0), ('r', 2), ('r', 4), ('s', 1), ('s', 3), ('s', 5)],
    'D3CV': [('r', 0), ('r', 2), ('r', 4), ('s', 0), ('s', 2), ('s', 4)],
    'D3CM_odd': [('r', 1), ('r', 3), ('r', 5), ('s', 0), ('s', 2), ('s', 4)],
    'D3CV_odd': [('r', 1), ('r', 3), ('r', 5), ('s', 1), ('s', 3), ('s', 5)],
}

def lattice_ij(c):
    a, b = c
    assert (2 * a + b) % 6 == 0 and (b - a) % 6 == 0
    return ((2 * a + b) // 6, (b - a) // 6)

DIRS = [rot((2, 0), k) for k in range(6)]

def transform_kite(g, c, k):
    gc_ = apply(g, c)
    v = apply(g, rot((2, 0), k))
    return lattice_ij(gc_), DIRS.index(v)

def placements(R, lin):
    t, hk = kites_of_hat()
    base = [(lattice_ij(c), k) for c, k in hk]
    out = []
    M = R + 3
    for g in lin:
        gk = [transform_kite(g, centre(*ij), k) for ij, k in base]
        for di in range(-M - 4, M + 5):
            for dj in range(-M - 4, M + 5):
                ks = [((i + di, j + dj), k) for (i, j), k in gk]
                if all(hexdist(*ij) <= M for ij, k in ks) and any(hexdist(*ij) <= R for ij, k in ks):
                    out.append((g, ks))
    return out

def run(R, name):
    t0 = time.time()
    P = placements(R, SETS[name])
    pool = IDPool()
    cov = {}
    for n, (g, ks) in enumerate(P):
        v = pool.id(('p', n))
        for kk in ks:
            cov.setdefault(kk, []).append(v)
    cnf = CNF()
    for kk, vs in cov.items():
        inner = hexdist(*kk[0]) <= R
        if inner:
            cnf.extend(CardEnc.equals(lits=vs, bound=1, vpool=pool, encoding=EncType.seqcounter).clauses if len(vs) > 1 else [[vs[0]]])
        elif len(vs) > 1:
            cnf.extend(CardEnc.atmost(lits=vs, bound=1, vpool=pool, encoding=EncType.seqcounter).clauses)
    # inner kites with no placement at all -> UNSAT immediately
    ninner = sum(1 for i in range(-R, R + 1) for j in range(-R, R + 1) if hexdist(i, j) <= R) * 6
    missing = ninner - sum(1 for kk in cov if hexdist(*kk[0]) <= R)
    with Cadical153(bootstrap_with=cnf.clauses) as s:
        sat = (missing == 0) and s.solve()
        model = s.get_model() if sat else None
    used = None
    if sat:
        ms = set(x for x in model if x > 0)
        chosen = [P[n] for n in range(len(P)) if pool.id(('p', n)) in ms]
        from collections import Counter
        used = Counter(g for g, ks in chosen)
    print(f'R={R} set={name} placements={len(P)} vars={pool.top} clauses={len(cnf.clauses)} -> {"SAT" if sat else "UNSAT"}'
          f' ({time.time()-t0:.1f}s)' + (f' orientations used {dict(used)}' if used else ''), flush=True)
    return sat

if __name__ == '__main__':
    R = int(sys.argv[1])
    names = sys.argv[2:] or list(SETS)
    res = {n: run(R, n) for n in names}
    # controls: ALL12 must tile; for R >= 2 the rotations-only set C6 must fail (the hat needs reflections)
    expect_ok = res.get('ALL12', True) and (R < 2 or not res.get('C6', False))
    print('RESULT', res)
    print('FINAL ok' if expect_ok else 'FINAL FAIL: controls wrong (ALL12 must be SAT, C6 UNSAT)')
