"""Part 1 table: the 28 catalogue polyhedra whose Resonus and Vacuus share planes (read from the exact catalogue data)."""
import os, json, csv, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ST = os.path.normpath(os.path.join(HERE, '..', '..'))
D = json.load(open(os.path.join(ST, '2026-11-24-vacuus-resonus-catalogue', 'data', 'catalogue-all.json')))
rows = {r['solid']: r for r in csv.DictReader(open(os.path.join(ST, '2026-11-24-vacuus-resonus-catalogue', 'data', 'vacuus-resonus-catalogue.csv')))}
G = {'cuboctahedron': 'Oh', 'icosidodecahedron': 'Ih', 'truncated octahedron': 'Oh', 'rhombic dodecahedron': 'Oh', 'rhombic triacontahedron': 'Ih',
     '6-gonal prism': 'D6h', '10-gonal prism': 'D10h'}
out = ['| polyhedron | family | symmetry | centrally symmetric | Resonus | Vacuus | shared | of them mirrors | each shared plane: edges in it; side counts of the two parallel faces |', '|---|---|---|---|---|---|---|---|---|']
n = 0
for x in D:
    c = x.get('corner', x)
    if not c['both']: continue
    nm = x['name'].replace('_', ' ').lower(); key = next(k for k in rows if (k.lower() == nm) or (x['family'] == 'Johnson' and k.split()[0] == nm.split()[0].upper()))
    r = rows[key]; n += 1
    kinds = collections.Counter((b['edges'], tuple(b['faces_parallel']), b['mirror']) for b in c['both_info'])
    desc = '; '.join('%d× (%d edge%s, faces %s%s)' % (m, e, 's' if e > 1 else '', '+'.join(map(str, fp)) if len(fp) > 1 else str(fp[0]) + ' alone', ', mirror' if mi else '') for (e, fp, mi), m in sorted(kinds.items()))
    out.append('| %s | %s | %s | %s | %s | %s | **%d** | %d | %s |' % (key, r['family'], x.get('group') or G.get(key, '–'), 'yes' if r['centrally_symmetric'] == 'True' else 'no', r['resonus_planes'], r['vacuus_plates'], c['both'], c['both_on_mirrors'], desc))
assert n == 28, n
open(os.path.join(HERE, '..', 'data', 'table28.md'), 'w').write('\n'.join(out) + '\n')
print('\n'.join(out))
