# EXACT check that the UP chain is its own polar (DICTO 2026-10-19), in Q(sqrt5): reciprocation about the sphere of radius^2 = 10/phi^2
# (the DICTO GTI's circumsphere) maps each face  n.x = d  of a solid to the corner  (rho^2/d) n,  and swaps GTI <-> FPD, RT <-> ID*k,
# ID <-> RT*k (k = 10/phi^4), exactly. Also: the GTI's corners all lie on that sphere.
import itertools, json, os
from exact_cycle import Q5, Fr, PHI, dot, step
from exact_shells import solid
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'exact_cycle.py')).read().split("if __name__ == '__main__':")[1]
     .split("    log = {")[0].replace('\n    ', '\n'))                         # ID of radius phi
rho2 = Q5(10) / (PHI * PHI)
chain = [ID]
for _ in range(5): chain.append(step(chain[-1])[0])                            # ID RT GTI FPD ID*k RT*k
polar = lambda S: {tuple(x * (rho2 / d) for x in n) for n, d in solid(S)}
res = {'mark': 'DICTO Universal PiTet, exact self-polarity, 2026-10-19', 'rho2': repr(rho2),
       'GTI_corners_on_sphere': all(dot(v, v) == rho2 for v in chain[2])}
for i, j, a, b in [(2, 3, 'GTI', 'FPD'), (1, 4, 'RT', 'ID*k'), (0, 5, 'ID', 'RT*k')]:
    res[f'{a} -> {b}'] = polar(chain[i]) == set(chain[j]); res[f'{b} -> {a}'] = polar(chain[j]) == set(chain[i])
print(json.dumps(res, indent=1))
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'exact_polar.json'), 'w'), indent=1)
