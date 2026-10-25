# Atom onions, part C (floats): the app's shells and DICTO's named pieces against the closed-form onion shells of onions_exact.py.
#  C1 frame/scale: app goldenT(x) = signed permutations of (1, s, 0) * phi/2 at every golden stop; app tetPiece/octPiece = closed form.
#  C2 named pieces (Polyhedraverse, DICTO's pieces): Icosaxes = big shell at x = tau; Unborn Axes = small shell at x = tau (= big
#     shell at x = 1/tau); Samson = tet shell at the Delian bond / sqrt2; Delilah = oct shell there / sqrt2 (after centring).
#  C3 app stop values = the exact stops.  Output: ../data/checks/app-checks.txt
import json, itertools, math, numpy as np
d = json.load(open('../data/raw/app-dump.json')); PHI = (1 + 5 ** .5) / 2
checks = []
def check(n, ok, det=''): checks.append(('PASS' if ok else 'FAIL', n, det)); print(('PASS ' if ok else 'FAIL ') + n, det)
def T(sv, L=PHI):
    P = set()
    for p in set(itertools.permutations((1, sv, 0))):
        for g in itertools.product((1, -1), repeat=3): P.add(tuple(round(a * b * L / 2, 12) + 0.0 for a, b in zip(p, g)))
    return np.array(sorted(P))
def same(A, B, tol=1e-9):
    A = np.unique(np.round(np.array(A, float), 9), axis=0); B = np.unique(np.round(np.array(B, float), 9), axis=0)
    if len(A) != len(B): return False
    return all(np.min(np.linalg.norm(B - a, axis=1)) < tol for a in A)
def centred(A): A = np.array(A, float); return A - A.mean(0)
S = {'0': 0, '1/tau': 1 / PHI ** 2, '1': .5, 'tau': 1 / PHI, 'inf': 1}
for k, sv in S.items(): check(f'C1 app goldenT(x = {k}) = signed permutations of (1, s, 0) phi/2, s = {sv:.6f}', same(d['golden'][k], T(sv)))
def tet(t):
    q = np.array([.5] * 3); C = [np.array(c, float) for c in itertools.product((0, 1), repeat=3)]
    even = [c for c in C if sum(c) % 2 == 0]; odd = [c for c in C if sum(c) % 2 == 1]
    if t <= 1 / 3: return [q + 3 * t * (v - q) for v in even]
    a = 1.5 * (1 - t); return even + [o + a * (v - o) for o in odd for v in even if abs(np.linalg.norm(v - o) - 1) < 1e-9]
def octp(t, c=np.array([1., 0, 0])):
    E = [np.array(e, float) for e in np.eye(3)]
    if t >= 1 / 3: a = 1.5 * (1 - t); return [c + g * a * e for e in E for g in (1, -1)]
    out = [c + g * e for e in E for g in (1, -1)]
    for sg in itertools.product((-1, 1), repeat=3):
        q = c + np.array(sg) / 2
        for i in range(3):
            v = c.copy(); v[i] += sg[i]; out.append(q + 3 * t * (v - q))
    return out
for k, v in d['delian'].items():
    t = v['t']
    if v['tet']: check(f'C1 app tetPiece(t = {k}) = closed form', same(v['tet'], tet(t)))
    if v['oct']: check(f'C1 app octPiece(t = {k}) = closed form', same(v['oct'], octp(t)))
P = d['pieces']; tb = d['stops']['octet']['delian']
check('C2 Icosaxes (Polyhedraverse) = golden big shell at x = tau (app units)', same(centred(P['DICTO_ICOSAXES']['vertices']), T(1 / PHI)))
check('C2 Unborn Axes (Polyhedraverse) = golden small shell at x = tau = big shell at x = 1/tau', same(centred(P['DICTO_UNBORN_AXES']['vertices']), T(1 / PHI ** 2)))
check('C2 Samson (Polyhedraverse) = Delian tet shell at the Delian bond, / sqrt2', same(centred(P['DICTO_SAMSON']['vertices']), centred(tet(tb)) / 2 ** .5))
check('C2 Delilah (Polyhedraverse) = Delian oct shell at the Delian bond, / sqrt2', same(centred(P['DICTO_DELILAH']['vertices']), centred(octp(tb)) / 2 ** .5))
ex = {'rd': 0, 'equilateralRd': (2 * 6 ** .5 - 3) / 15, 'octet': 1 / 3, 'half': 1 - 6 ** (1 / 3) / 3, 'delian': 1 - (2 / 3) * 2 ** (-1 / 3), 'equilateralCube': 5 / 3 - (2 / 3) * 2 ** .5, 'cube': 1}
check('C3 app OCTET_FAMILY_STOPS = exact stop values', all(abs(d['stops']['octet'][k] - v) < 1e-12 for k, v in ex.items()))
gs = {s['key']: s['v'] for s in d['stops']['golden']}
check('C3 app GOLDEN_STOPS = 0, 1, tau, inf (inf is null in JSON)', gs['zero'] == 0 and gs['kelvin'] == 1 and abs(gs['tau'] - PHI) < 1e-15 and gs['inf'] is None, json.dumps(gs))
with open('../data/checks/app-checks.txt', 'w') as f:
    for c in checks: f.write('  '.join(c) + '\n')
    f.write(f"{sum(c[0] == 'PASS' for c in checks)} PASS, {sum(c[0] == 'FAIL' for c in checks)} FAIL\n")
print(f"{sum(c[0] == 'PASS' for c in checks)} PASS, {sum(c[0] == 'FAIL' for c in checks)} FAIL")
