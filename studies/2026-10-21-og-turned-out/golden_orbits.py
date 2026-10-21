# DICTO 2026-10-21: OG turned out, golden step: the towers of shell 2 (phi TPH -> phi^2 TQH) counted by symmetry orbit, EXACT.
# golden_exact.py tests "one shape per kind" (kind = number of sides); its 120 towers on triangles have two volumes, so that test
# says FAIL. Here the faces of phi TPH are split into orbits of the 60 exact rotations: each orbit's towers are rotated copies of one
# tower (the solids are symmetric, checked in golden_exact.py), so one orbit = one shape. Printed: orbits, sizes, sides, tower volume.
# usage: python3 golden_orbits.py <studies/2026-10-19-five-fold-octet>
import sys, os, json
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
HERE = os.path.dirname(os.path.abspath(__file__))
src = open('exact_downward.py').read(); exec(src.split("log = {")[0].replace("os.path.dirname(os.path.abspath(__file__))", repr(os.getcwd())))
ok = lambda cond, m: print(('PASS ' if cond else 'FAIL ') + m, flush=True) or cond
D = [OG]
for k in range(1, 3): D.append(rev(D[-1]))
B1 = [tuple(PHI * x for x in v) for v in D[1]]; B2 = [tuple(PHI * PHI * x for x in v) for v in D[2]]
Hin, Hout = solid(B1), solid(B2)
Cin, Fin = polytope(Hin); Cout, Fout = polytope(Hout); gap = volume(Cout, Fout) - volume(Cin, Fin)
tow = {}
for o, i in Fin:
    F = [Cin[j] for j in o]; n, d = Hin[i]
    H = list(Hout) + [(tuple(-x for x in n), -d)]
    for a, b in zip(F, F[1:] + F[:1]):
        m = cross(a, b); other = [c for c in F if c not in (a, b)][0]
        if dot(m, other).sign() > 0: m = tuple(-x for x in m)
        H.append((m, Q5(0)))
    C, Fc = polytope(H); tow[frozenset(F)] = (len(F), volume(C, Fc))
left = set(tow); orbits = []
while left:
    F0 = next(iter(left)); orb = {frozenset(app(M, v) for v in F0) for M in G}
    ok(orb <= left, f'orbit of a {len(F0)}-gon lies among the faces'); left -= orb
    vols = {tow[f][1] for f in orb}; orbits.append({'sides': len(F0), 'faces': len(orb), 'volumes': [repr(v) for v in vols], 'volume_float': [v.f() for v in vols]})
total = Q5(0)
for f in tow: total = total + tow[f][1]
orbits.sort(key=lambda o: (o['sides'], o['volume_float'][0]))
ok(all(len(o['volumes']) == 1 for o in orbits), 'one tower volume per orbit')
ok((total - gap) == Q5(0), 'the towers add up to the shell exactly')
ok(len(orbits) == 3 and [(o['sides'], o['faces']) for o in orbits] == [(3, 60), (3, 60), (5, 12)],
   'shell 2: three orbits, 60 + 60 towers on triangles (two shapes, volumes ' + ', '.join(f"{o['volume_float'][0]:.6f}" for o in orbits[:2]) + f") and 12 on pentagons ({orbits[2]['volume_float'][0]:.6f}): 3 shapes")
json.dump({'mark': 'DICTO OG turned out, golden step, shell 2 orbits, exact, 2026-10-21 · DICTO · dictospheres.com', 'gap': repr(gap), 'orbits': orbits},
          open(os.path.join(HERE, 'golden-orbits.json'), 'w'), indent=1)
