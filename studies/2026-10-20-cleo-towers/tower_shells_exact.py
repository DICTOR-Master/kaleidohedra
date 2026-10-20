# DICTO 2026-10-20: Cleo Towers (DICTO's idea): round the CLEO sphere (the icosidodecahedron, cut into 20 Cleo and 12 pentagonal pockets),
# shells of towers "as tall as possible", in a Fibonacci rhythm of beats. A beat is one step of the Universal PiTet rule (#38),
# T(S) = {x : v.x <= v.v for every corner v of S}: the tallest spires on every face with every old corner still on the new surface.
# Shells fuse 1, 1, 2, 3, 5 beats: ID -> RT | RT -> GTI | GTI -> (FPD) -> ID c | ID c -> (RT c, GTI c) -> FPD c | FPD c -> ... -> ID c^3,
# c = 10/phi^4. Each shell is cut into towers, one over each face of its inner solid (the cone from the centre over the face, cut by the
# outer solid): exact corners, volumes, one shape per kind (one symmetry orbit), sum = shell exactly. Uses exact_cycle.py and
# exact_shells.py of studies/2026-10-19-five-fold-octet (#38).   usage: python3 tower_shells_exact.py <studies/2026-10-19-five-fold-octet>
import sys, os, json, itertools
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
import numpy as np
from exact_cycle import Q5, Fr, PHI, dot, fv, step
import exact_shells as X
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open('exact_cycle.py').read().split("if __name__ == '__main__':")[1].split("    log = {")[0].replace('\n    ', '\n'))   # ID of radius phi
G = X.rotations()
S = [ID]
for _ in range(4): S.append(step(S[-1])[0])
c = Q5(10) / (PHI * PHI * PHI * PHI)
ok = lambda cond, m: print(('PASS ' if cond else 'FAIL ') + m, flush=True) or cond
ok(set(S[4]) == {tuple(c * x for x in v) for v in S[0]}, 'one turn of four beats returns the icosidodecahedron exactly 10/phi^4 larger')
for k in range(5, 13): S.append([tuple(c * x for x in v) for v in S[k - 4]])          # later turns: exact scaled copies
names = ['ID', 'RT', 'GTI', 'FPD'] * 4
lab = lambda k: names[k] + ('' if k < 4 else f' c^{k // 4}' if k // 4 > 1 else ' c')
beats = [1, 1, 2, 3, 5]; edges = [0]
for b in beats: edges.append(edges[-1] + b)
res = {'mark': 'DICTO Cleo Towers, exact, 2026-10-20 · DICTO · dictospheres.com', 'beats': beats, 'shells': []}
for k, (a, b) in enumerate(zip(edges, edges[1:])):
    out = X.shell(S[a], S[b], G, f'shell {k + 1}: {lab(a)} -> {lab(b)} ({b - a} beat{"s" if b - a > 1 else ""})')
    res['shells'].append(out)
    ok(out['sum_equals_gap_exactly'] and out['one_volume_per_kind'] and all(out['one_symmetry_orbit_per_kind'].values()),
       f"shell {k + 1} ({b - a} beats, {lab(a)} -> {lab(b)}): towers {out['pieces']}, each kind one shape, adding up to the shell exactly")
res['boundaries_float'] = {lab(k): [fv(v) if not hasattr(fv(v), 'tolist') else fv(v).tolist() for v in S[k]] for k in edges}   # for the figures only
json.dump(res, open(os.path.join(HERE, 'tower-shells-exact.json'), 'w'), indent=1, default=lambda o: o.tolist() if hasattr(o, 'tolist') else float(o))
