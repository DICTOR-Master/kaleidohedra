# DICTO 2026-10-21 ("yes run the 3 beat shell"): the OG turned out, golden step, shell 4 (3 beats, beat 4 -> beat 7), EXACT, from the
# exact downward solids saved by golden_exact_long.py (golden-long-solids.pkl). Beat k = phi^k x D_k. Checks: both boundaries have full
# icosahedral symmetry (all 60 rotations), beat 4 lies inside beat 7, and the shell cut into towers (cone from the centre over each face
# of beat 4, cut by beat 7): one shape per orbit, sum = shell exactly.   usage: python3 shell4_exact.py <studies/2026-10-19-five-fold-octet>
import sys, os, json, time, pickle
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
HERE = os.path.dirname(os.path.abspath(__file__))
src = open('exact_downward.py').read(); exec(src.split("log = {")[0].replace("os.path.dirname(os.path.abspath(__file__))", repr(os.getcwd())))
ok = lambda cond, m: print(('PASS ' if cond else 'FAIL ') + m, flush=True) or cond
def pw(k):
    r = Q5(1)
    for _ in range(k): r = r * PHI
    return r
D = pickle.load(open(os.path.join(HERE, 'golden-long-solids.pkl'), 'rb'))
B4 = [tuple(pw(4) * x for x in v) for v in D[4]]; B7 = [tuple(pw(7) * x for x in v) for v in D[7]]
H7 = solid(B7); B7 = list(dict.fromkeys([v for v in B7 if True]))
for nm, S in (('beat 4', B4), ('beat 7', B7)):
    ok(all({app(M, v) for v in S} == set(S) for M in G), f'{nm}: {len(S)} listed points, symmetric under all {len(G)} rotations')
o, nbad, worst = inside(B4, B7); ok(o, f'beat 4 lies inside beat 7 exactly (corners outside {nbad})')
t = time.time(); out = shell(B4, B7, G, 'beat 4 -> beat 7 (3 beats)')
ok(out['sum_equals_gap_exactly'] and all(out['one_symmetry_orbit_per_kind'].values()),
   f"shell 4 (3 beats): towers {out['pieces']}, shapes per kind {[len(v) for v in out['exact_volumes'].values()]}, sum = shell exactly ({time.time() - t:.0f} s)")
json.dump({'mark': 'DICTO OG turned out, golden step, shell 4 (3 beats), exact, 2026-10-21 · DICTO · dictospheres.com', 'shell': out,
           'boundaries_float': {'beat 4': [[x.f() for x in v] for v in B4], 'beat 7': [[x.f() for x in v] for v in B7]}},
          open(os.path.join(HERE, 'shell4-exact.json'), 'w'), indent=1)
