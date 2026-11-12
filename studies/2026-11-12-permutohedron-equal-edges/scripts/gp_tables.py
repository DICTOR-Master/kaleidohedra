"""Tables from the members-*.json of gp_analyse: exact cyclic corner configurations for the regular-faced members (to settle
ortho/gyro and antiprism names), refined classes, the stretches of Platonic and Archimedean solids, the new atoms, and summary.

Usage: gp_tables.py DATADIR   (writes DATADIR/solids-{A3,B3}.md, DATADIR/solids-H3.csv, DATADIR/tables.json; prints a summary)
"""
import sys, os, json, itertools, collections
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(__file__))
from coxeter import QF, Fan, dot, vsub, vkey, rank

DATA = sys.argv[1]
checks = []


def chk(n, ok):
    checks.append((n, bool(ok)))
    print(f'CHECK {"ok  " if ok else "FAIL"} {n}', flush=True)


def build(F, bits):
    V = [None] * len(F.W)
    V[0] = (QF(0),) * 3
    st = [0]
    while st:
        c = st.pop()
        for i in range(3):
            d = F.nb[c][i]
            w = F.wallidx[(min(c, d), max(c, d))]
            r = F.walls[w][3] if F.walls[w][0] == c else tuple(-x for x in F.walls[w][3])
            if V[d] is None:
                V[d] = vsub(V[c], r) if bits >> w & 1 else V[c]
                st.append(d)
    pts = {}
    for v in V:
        pts[vkey(v)] = v
    return list(pts.values())


def cyclic_configs(F, P):
    faces = []
    for r in F.rays:
        h = max(dot(v, r) for v in P)
        S = [k for k, v in enumerate(P) if dot(v, r) == h]
        if len(S) >= 3 and rank([vsub(P[k], P[S[0]]) for k in S[1:]]) == 2:
            faces.append(set(S))
    edges = set()
    for a, b in itertools.combinations(range(len(faces)), 2):
        s = faces[a] & faces[b]
        if len(s) == 2:
            edges.add((a, b, tuple(sorted(s))))
    out = collections.Counter()
    for v in range(len(P)):
        fs = [i for i, f in enumerate(faces) if v in f]
        nb = {i: [] for i in fs}
        for a, b, e in edges:
            if v in e and a in nb and b in nb:
                nb[a].append(b)
                nb[b].append(a)
        cyc = [fs[0]]
        while len(cyc) < len(fs):
            cyc.append([x for x in nb[cyc[-1]] if x not in cyc][0])
        seq = [len(faces[i]) for i in cyc]
        rots = [tuple(seq[k:] + seq[:k]) for k in range(len(seq))]
        rots += [tuple(reversed(r)) for r in rots]
        out['.'.join(map(str, min(rots)))] += 1
    return dict(out)


ARCH_ANTI = {}
names_fix = []
tables = {}
for name in ['A3', 'B3', 'H3']:
    F = Fan(name)
    M = json.load(open(os.path.join(DATA, f'members-{name}.json')))
    byid = {m['id']: m for m in M}
    sol = [m for m in M if m['dim'] == 3]
    for m in sol:
        if not m['regular_faced']:
            continue
        P = build(F, int(m['bits'], 16))
        cc = cyclic_configs(F, P)
        m['corner_cycles'] = cc
        cnt = {int(k): v for k, v in m['ngon_counts'].items()}
        nm = m['name']
        if cnt == {3: 8, 4: 2, 5: 4}:
            nm = 'J91 bilunabirotunda'
        elif cnt == {3: 13, 4: 3, 5: 3, 6: 1}:
            nm = 'J92 triangular hebesphenorotunda'
        elif len(cnt) == 2 and 3 in cnt and m['corner_profiles'] == 1 and cnt[3] == 2 * [k for k in cnt if k != 3][0] and cnt[[k for k in cnt if k != 3][0]] == 2:
            nm = f'{[k for k in cnt if k != 3][0]}-gonal antiprism'
        elif nm.startswith('J28/J29'):
            nm = 'J28 square orthobicupola' if '3.3.4.4' in cc else 'J29 square gyrobicupola'
        elif nm.startswith('J30/J31'):
            nm = 'J30 pentagonal orthobicupola' if '3.3.4.4' in cc else 'J31 pentagonal gyrobicupola'
        elif nm.startswith('J32/J33'):
            # Johnson J32 (ortho) has 10 corners 3.4.3.5 (cyclic) on the decagon; J33 (gyro) has 3.3.4.5 there
            nm = 'J32 pentagonal orthocupolarotunda' if '3.4.3.5' in cc else 'J33 pentagonal gyrocupolarotunda'
        elif nm.startswith('J76'):
            nm = 'J76 diminished rhombicosidodecahedron' if set(cc) <= {'3.4.5.4', '4.5.10'} else nm
        elif nm.startswith('J80/J81'):
            if set(cc) <= {'3.4.5.4', '4.5.10'}:
                nm = 'J80 parabidiminished rhombicosidodecahedron' if m['orbit'] * 20 == 120 else 'J81 metabidiminished rhombicosidodecahedron'
        if nm != m['name']:
            names_fix.append((name, m['id'], m['name'], nm, cc))
        m['name'] = nm
        m['label'] = nm
    for m in M:
        if m['dim'] == 3 and m['regular_faced']:
            m['class'] = 'regular-faced (known: ' + m['name'] + ')'
    platarch = {'tetrahedron', 'cube', 'octahedron', 'dodecahedron', 'icosahedron', 'cuboctahedron', 'truncated tetrahedron',
                'truncated octahedron', 'truncated cube', 'rhombicuboctahedron', 'truncated cuboctahedron', 'icosidodecahedron',
                'truncated icosahedron', 'truncated dodecahedron', 'rhombicosidodecahedron', 'truncated icosidodecahedron'}
    for m in sol:
        parts = [byid[a] for a in m['atoms_in']]
        core = byid[m['core']]
        if m['regular_faced']:
            k = 'regular-faced'
        elif m['core_dim'] == 0:
            k = 'zonohedron'
        elif m['segments']:
            k = 'stretch of a Platonic/Archimedean solid' if core.get('name') in platarch else '#49 stretch (segment summand)'
        elif any(p['dim'] == 2 and p['polygon'] == 3 for p in parts) or any(p.get('name') == 'tetrahedron' for p in parts):
            k = '#49 cap (triangle or tetrahedron summand)'
        elif any(p['dim'] == 2 for p in parts):
            k = 'pentagon cap (regular pentagon summand)'
        elif m['atom']:
            k = 'new atom (indecomposable, not regular-faced)'
        else:
            k = 'sum of atoms (no segment, polygon or tetrahedron summand)'
        m['kind'] = k
    kinds = collections.Counter(m['kind'] for m in sol)
    atoms = [m for m in M if m['atom']]
    stretches = [m for m in sol if m['kind'] == 'stretch of a Platonic/Archimedean solid']
    tables[name] = dict(solid_orbits=len(sol), distinct_solids=len({m['invariant'] for m in sol}), kinds=dict(kinds),
                        atoms_by_dim=dict(collections.Counter(m['dim'] for m in atoms)),
                        regular_faced=sorted((m['name'], m['id']) for m in sol if m['regular_faced']),
                        stretches=[dict(id=m['id'], core=byid[m['core']]['name'], segments=m['segments'], V=m['V'], E=m['E'], F=m['F'],
                                        faces=m['face_kinds']) for m in stretches],
                        new_atoms=[dict(id=m['id'], V=m['V'], E=m['E'], F=m['F'], faces=m['face_kinds'], orbit=m['orbit'])
                                   for m in sol if m['kind'].startswith('new atom')])
    # tables
    cols = ['id', 'orbit', 'V', 'E', 'F', 'faces', 'kind', 'built from']
    def row(m):
        dec = ' + '.join(byid[a]['label'] if byid[a]['dim'] != 3 or byid[a].get('name') else f"{name}-{a}" for a in m['atoms_in'])
        nm = m['name'] if m['regular_faced'] else ''
        fk = ', '.join(f'{v} {k}' for k, v in m['face_kinds'].items())
        return [f'{name}-{m["id"]}', str(m['orbit']), str(m['V']), str(m['E']), str(m['F']), fk, m['kind'] + (f' = {nm}' if nm else '') +
                (f' (same solid as {name}-{m["same_solid_as"]}, turned)' if 'same_solid_as' in m else ''), dec]
    if name in ('A3', 'B3'):
        with open(os.path.join(DATA, f'solids-{name}.md'), 'w') as f:
            f.write(f'# Equal-edged members of the {name} permutohedron deformation cone (one per orbit)\n\n')
            f.write('Faces: "n-gon a/b" = equal-edged n-gon with angles a and b degrees. Built from = one exact split into atoms.\n\n')
            f.write('| ' + ' | '.join(cols) + ' |\n|' + '---|' * len(cols) + '\n')
            for m in sol:
                f.write('| ' + ' | '.join(row(m)) + ' |\n')
    with open(os.path.join(DATA, f'solids-{name}.csv'), 'w') as f:
        f.write(';'.join(cols) + '\n')
        for m in sol:
            f.write(';'.join(row(m)) + '\n')
    json.dump(M, open(os.path.join(DATA, f'members-{name}.json'), 'w'), indent=0)
    print(name, json.dumps({k: v for k, v in tables[name].items() if k not in ('new_atoms',)})[:3000], flush=True)
    print(name, 'new atoms', len(tables[name]['new_atoms']), flush=True)

for x in names_fix:
    print('NAME', x)
want = {'J91 bilunabirotunda', 'J92 triangular hebesphenorotunda', '5-gonal antiprism', 'J28 square orthobicupola',
        'J31 pentagonal gyrobicupola'}
found = {n for t in tables.values() for n, _ in t['regular_faced']}
chk('named checks resolved (J28/J29, J30/J31, J32/J33, J80/J81 by cyclic corners; no unresolved names)',
    not any('/' in n or 'not in the table' in n or '(or' in n for n in found))
json.dump(dict(tables=tables, checks=checks), open(os.path.join(DATA, 'tables.json'), 'w'), indent=1)
bad = [n for n, ok in checks if not ok]
print('tables checks', len(checks) - len(bad), '/', len(checks))
sys.exit(1 if bad else 0)
