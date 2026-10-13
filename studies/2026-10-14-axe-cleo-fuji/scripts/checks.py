# Checks for the paper on AXE, CLEO and FUJI (DICTO, 2026-10-14). Reads the DICTO Icosa-13 study data (unit: icosahedron
# edge 1) and recomputes every number the paper states. Writes ../CHECKS.json and ../nets/pieces.json (for nets.py).
# DICTO · dictospheres.com
import json, math, os, itertools
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
D = os.path.join(ROOT, '..', '2026-10-10-icosa-13', 'data')
ld = lambda n: json.load(open(os.path.join(D, n + '-unit.json')))
phi = (1 + 5 ** .5) / 2; s5 = 5 ** .5
out, bad = {}, []

def vol(V, F):
    V = np.array(V, float); c = V.mean(0)
    return sum(np.dot(V[f[0]] - c, np.cross(V[f[i]] - c, V[f[i + 1]] - c)) for f in F for i in range(1, len(f) - 1)) / 6

def edges(V, F):
    V = np.array(V, float); E = {tuple(sorted((f[i], f[(i + 1) % len(f)]))) for f in F for i in range(len(f))}
    return sorted(round(float(np.linalg.norm(V[a] - V[b])), 9) for a, b in E)

def normal(V, f):
    V = np.array(V, float); c = V[f].mean(0); n = sum(np.cross(V[f[i]] - c, V[f[(i + 1) % len(f)]] - c) for i in range(len(f)))
    return n / np.linalg.norm(n)

def dihedrals(V, F):
    E = {}
    for fi, f in enumerate(F):
        for i in range(len(f)): E.setdefault(tuple(sorted((f[i], f[(i + 1) % len(f)]))), []).append(fi)
    V = np.array(V, float); res = []
    for (a, b), (f1, f2) in E.items():
        n1, n2 = normal(V, F[f1]), normal(V, F[f2])
        ang = math.pi - math.acos(np.clip(n1 @ n2, -1, 1))
        res.append((round(float(np.linalg.norm(V[a] - V[b])), 6), round(math.degrees(ang), 4)))
    return sorted(set(res))

def check(name, got, want, tol=1e-8):
    ok = bool(abs(got - want) < tol); out[name] = dict(value=round(float(got), 9), exact=round(want, 9), ok=ok)
    if not ok: bad.append(name)

P = {k: ld(f) for k, f in [('AXE', 'ico13-wedge'), ('CLEO', 'ico13-needle'), ('FUJI', 'ico13-hex-pyramid'),
                           ('Triskelion Hex', 'ico13-outer-star'), ('Triskelion', 'ico13-inner-star'),
                           ('Inner Eye', 'ico13-core'), ('small centre', 'ico13-small-centre'), ('Lotus seed', 'ico13-filled')]}
EXACT = {'AXE': 1 / 12, 'CLEO': (s5 - 1) / 24, 'FUJI': (1 + 3 * s5) / 24, 'Triskelion Hex': (7 + 3 * s5) / 24,
         'Triskelion': (5 + s5) / 24, 'Inner Eye': 5 * phi / 2, 'small centre': 5 * (s5 - 1) / 12, 'Lotus seed': (235 + 105 * s5) / 12}
for k, d in P.items():
    check(f'volume {k}', vol(d['vertices'], d['faces']), EXACT[k])
for k in ('AXE', 'CLEO', 'FUJI'):
    out[f'edges {k}'] = edges(P[k]['vertices'], P[k]['faces'])
    out[f'dihedrals {k} (edge length, degrees)'] = dihedrals(P[k]['vertices'], P[k]['faces'])
VI = 5 * (3 + s5) / 12  # icosahedron, edge 1
J2 = (5 + s5) / 24; J11 = VI - J2; DOD = (15 + 7 * s5) / 4
check('Lotus seed = phi^6 icosahedra', EXACT['Lotus seed'], phi ** 6 * VI)
check('113-piece build: 12 I + I(1/phi) + 60 AXE + 20 FUJI + 20 CLEO', 12 * VI + EXACT['small centre'] + 60 / 12 + 20 * EXACT['FUJI'] + 20 * EXACT['CLEO'], EXACT['Lotus seed'])
check('63-piece build: dodecahedron + 12 J11 + 30 AXE + 20 FUJI', DOD + 12 * J11 + 30 / 12 + 20 * EXACT['FUJI'], EXACT['Lotus seed'])
check('dodecahedron = I(1/phi) + 12 J2 + 30 AXE + 20 CLEO', EXACT['small centre'] + 12 * J2 + 30 / 12 + 20 * EXACT['CLEO'], DOD)
check('Inner Eye = I(1/phi) + 30 AXE + 20 CLEO', EXACT['small centre'] + 30 / 12 + 20 * EXACT['CLEO'], EXACT['Inner Eye'])
check('Triskelion = CLEO + 3 AXE = J2 (volume)', EXACT['CLEO'] + 3 / 12, J2)
check('Triskelion Hex = FUJI + 3 AXE', EXACT['FUJI'] + 3 / 12, EXACT['Triskelion Hex'])
# 63-piece data: count, roles, volume sum
parts = ld('ico13-dodeca-j11-parts')['parts']
roles = {}
for p in parts: roles[p['role']] = roles.get(p['role'], 0) + 1
out['63-piece roles'] = roles
check('63-piece data volume sum', sum(vol(p['vertices'], p['faces']) for p in parts), EXACT['Lotus seed'], 1e-6)
# FUJI base: cyclic equiangular hexagon, sides 1 and 1/phi, circumradius^2 = 2/3, height 1/sqrt3
check('FUJI base circumradius^2 (a^2+ab+b^2)/3', (1 + 1 / phi + 1 / phi ** 2) / 3, 2 / 3)
check('FUJI height', math.sqrt(1 - 2 / 3), 1 / math.sqrt(3))
# angles
al = math.degrees(math.acos(s5 / 3))
dihF = [a for _, a in dihedrals(P['FUJI']['vertices'], P['FUJI']['faces'])]
de = min(dihF)
check('two icosahedra round an edge leave 360 - 2*138.19 = 83.62 = 2 alpha', 360 - 2 * math.degrees(math.acos(-s5 / 3)), 2 * al, 1e-9)
check('alpha + 2 delta = dodecahedron dihedral 116.5651', al + 2 * de, math.degrees(math.acos(-1 / s5)), 1e-3)
out['delta (FUJI base angle on short edges), degrees'] = de
# AXE congruent to Mosseri-Sadoc t6/tau: five edges 1, one 1/phi
check('AXE short edge = 1/phi', out['edges AXE'][0], 1 / phi, 1e-8)
check('CLEO base edge = 1/phi', out['edges CLEO'][0], 1 / phi, 1e-8)
out['failures'] = bad
json.dump(out, open(os.path.join(ROOT, 'CHECKS.json'), 'w'), indent=1, ensure_ascii=False)
# pieces for the nets (the 63-piece hand build, plus CLEO)
pick = {}
for p in parts:
    if p['role'] not in pick: pick[p['role']] = p
nets = {r: dict(vertices=p['vertices'], faces=p['faces']) for r, p in pick.items()}
nets['CLEO'] = dict(vertices=P['CLEO']['vertices'], faces=P['CLEO']['faces'])
json.dump(nets, open(os.path.join(ROOT, 'nets', 'pieces.json'), 'w'))
print('roles', roles, 'failures', bad)
