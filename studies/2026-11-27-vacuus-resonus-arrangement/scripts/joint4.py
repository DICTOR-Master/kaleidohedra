"""Step 1 (27 Nov 2026; DICTO's conjecture, his words: "create intersecting planes of vacuus and resonus to define their
intersectionality and resolve desired outcomes via those planes through trigonometry ... including new combinations or
alternative space-filling solutions"; DICTO "yes to all"). With Claude (Anthropic).
The joint arrangement for n = 4: the permutohedron P4 = conv of the rearrangements of (4,3,2,1), centred, in the 3-space
sum y = 0 (a truncated octahedron). Vacuus planes: through the centre and an edge (ridge, n - 3 = 1); Resonus planes: through
the centre parallel to a facet (normal = indicator of S minus |S|/4). All EXACT (fractions). Output:
 - the distinct planes (expected 15 Vacuus + 7 Resonus, 3 Resonus being Vacuus planes: 19 distinct; #120 Theorem 3, 5);
 - the lines where planes meet, with how many planes pass through each (multiplicity);
 - the angles between planes, as exact cos^2 (rational), grouped;
 - the number of cones (cells) the planes cut space into: 2 + 2 sum over lines (m - 1);
 - an angle basis: every plane-pair angle as a rational combination of pi and a few basic angles (PSLQ, 50 digits: identified,
   not proved; proof = step 2).
Output data/joint4.json."""
import os, json, itertools
from fractions import Fraction as F
import mpmath as mp
mp.mp.dps = 60
HERE = os.path.dirname(os.path.abspath(__file__)); n = 4
V = [tuple(F(x) - F(n + 1, 2) for x in p) for p in itertools.permutations(range(n, 0, -1))]
dot = lambda a, b: sum(x * y for x, y in zip(a, b))
one = (F(1),) * n
def null(rows):   # exact nullspace of rows in Q^n
    M = [list(r) for r in rows]; piv = []; r = 0
    for c in range(n):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]; M[r] = [x / M[r][c] for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0: M[i] = [a - M[i][c] * b for a, b in zip(M[i], M[r])]
        piv.append(c); r += 1
    free = [c for c in range(n) if c not in piv]; out = []
    for f in free:
        v = [F(0)] * n; v[f] = F(1)
        for i, c in enumerate(piv): v[c] = -M[i][f]
        out.append(tuple(v))
    return out
def canon(v):   # primitive integer vector, sign fixed
    from math import gcd
    den = 1
    for x in v: den = den * x.denominator // gcd(den, x.denominator)
    iv = [int(x * den) for x in v]; g = 0
    for x in iv: g = gcd(g, abs(x))
    iv = [x // g for x in iv]; s = next(x for x in iv if x != 0)
    return tuple(x if s > 0 else -x for x in iv)
# edges of P4: vertices differing by swapping two values that differ by 1
def edge(p, q):
    d = [i for i in range(n) if p[i] != q[i]]; return len(d) == 2 and abs(p[d[0]] - p[d[1]]) == 1
E = [(p, q) for p, q in itertools.combinations(V, 2) if edge(p, q)]
vac = {}
for p, q in E:
    (nv,) = null([one, p, q]); vac.setdefault(canon(nv), []).append((p, q))
res = {}
for k in range(1, n):
    for S in itertools.combinations(range(n), k):
        v = tuple(F(1 if i in S else 0) - F(k, n) for i in range(n)); res.setdefault(canon(v), []).append(S)
planes = {}
for v in vac: planes.setdefault(v, set()).add('V')
for v in res: planes.setdefault(v, set()).add('R')
PL = sorted(planes); kind = {v: ''.join(sorted(planes[v])) for v in PL}
print(f'edges {len(E)}; Vacuus planes {len(vac)}; Resonus planes {len(res)}; distinct {len(PL)}; both {sum(1 for v in PL if kind[v] == "RV")}', flush=True)
# lines: direction of the intersection of two planes (inside sum y = 0)
lines = {}
for a, b in itertools.combinations(range(len(PL)), 2):
    (d,) = null([one, PL[a], PL[b]]); lines.setdefault(canon(d), set()).update((a, b))
mult = sorted(len(s) for s in lines.values())
from collections import Counter
print(f'lines {len(lines)}; planes per line: {sorted(Counter(mult).items())}', flush=True)
cells = 2 + 2 * sum(m - 1 for m in mult)
print(f'cells (cones from the centre) {cells}', flush=True)
# angles between planes, exact cos^2 (normals already orthogonal to 1, so plain dot products)
ang = Counter()
for a, b in itertools.combinations(PL, 2):
    a_, b_ = [F(x) for x in a], [F(x) for x in b]
    c2 = dot(a_, b_) ** 2 / (dot(a_, a_) * dot(b_, b_)); ang[c2] += 1
print('plane-pair angles (cos^2 : count):', sorted((str(k), v) for k, v in ang.items()), flush=True)
# angle basis by PSLQ: theta = arccos(sqrt(c2)) in [0, pi/2]
th = {k: mp.acos(mp.sqrt(mp.mpf(k.numerator) / k.denominator)) for k in ang}
basis = []
def rel(x, B):
    r = mp.pslq([x] + [b for _, b in B] + [mp.pi], maxcoeff=10**4, maxsteps=10**6)
    return r if r and r[0] != 0 and abs(sum(c * y for c, y in zip(r, [x] + [b for _, b in B] + [mp.pi]))) < mp.mpf(10) ** -50 else None
expr = {}
for k in sorted(th, key=lambda k: th[k]):
    r = rel(th[k], basis)
    if r is None: basis.append((str(k), th[k])); expr[str(k)] = 'basis'
    else:
        c0 = r[0]; expr[str(k)] = ' + '.join(f'{F(-c, c0)}*{nm}' for c, (nm, _) in zip(r[1:-1], basis) if c) + (f' + {F(-r[-1], c0)}*pi' if r[-1] else '')
print('angle basis (cos^2 of the basic angles):', [nm for nm, _ in basis], flush=True)
for k, e in expr.items(): print(f'   arccos(sqrt({k})) = {e}', flush=True)
json.dump(dict(planes=[dict(normal=list(v), kind=kind[v], edges=len(vac.get(v, [])), facets=[list(S) for S in res.get(v, [])]) for v in PL],
               lines=[dict(direction=list(d), planes=sorted(s)) for d, s in lines.items()], cells=cells,
               angles={str(k): v for k, v in ang.items()}, basis=[nm for nm, _ in basis], expressions=expr),
          open(os.path.join(HERE, '../data/joint4.json'), 'w'), indent=1)
ok = len(vac) == 15 and len(res) == 7 and len(PL) == 19
print('FINAL ok' if ok else 'FINAL FAIL (plane counts disagree with #120)')
