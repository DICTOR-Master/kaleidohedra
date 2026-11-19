# Assemble the catalogue: merge the classified dice (dice.json) with the 80-digit refinement (exact.jsonl); per-die JSON,
# the full table (CSV and Markdown), counts by group and m, and the controls (Equanimity's twelve, D191, the pilot).
# usage: make_table.py dice.json exact.jsonl pilot_run1.log outdir
import json, sys, os, re, csv, itertools
from collections import Counter, defaultdict
from mpmath import mp, mpf
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from groups import DIRS, DFAM
mp.dps = 70
dice = json.load(open(sys.argv[1])); E = {}
for L in open(sys.argv[2]):
    r = json.loads(L); E[r['sid']] = r
out = sys.argv[4]; os.makedirs(os.path.join(out, 'dice'), exist_ok=True)
FAMS = ['C6', 'O8', 'RD12', 'D12', 'I12', 'RT24']
BIG = ['Ih', 'I', 'Oh', 'O', 'Td', 'Th', 'T']
def fmt_dir(j):
    v = DIRS[j]; phi = (1 + 5 ** .5) / 2
    vals = {0: '0', 1: '1', phi: 'φ', 1 / phi: '1/φ'}
    sc = {'C6': 1, 'O8': 3 ** .5, 'RD12': 2 ** .5, 'D12': (phi ** 2 + 1) ** .5, 'I12': (phi ** 2 + phi ** -2) ** .5, 'RT24': 2}[DFAM[j]]
    s = []
    for c in v * sc:
        for x, t in vals.items():
            if abs(abs(c) - x) < 1e-9: s.append(('-' if c < -1e-9 else '') + t); break
    return '(' + ', '.join(s) + ')'
A = [d for d in dice['dice'] if d['centroid_at_origin'] and not d['face_transitive']]
assert all(d['sid'] in E and E[d['sid']]['exact_ok'] for d in A)
# disambiguate equal labels within a group
seen = defaultdict(list)
for d in A: seen[(d['group'], tuple(d['orbit_labels']))].append(d)
rows = []
for d in A:
    e = E[d['sid']]; same = seen[(d['group'], tuple(d['orbit_labels']))]
    cut = list(itertools.accumulate([0] + d['sizes']))
    reps = [fmt_dir(max(d['idx'][cut[k]:cut[k + 1]], key=lambda j: tuple(DIRS[j]))) for k in range(d['m'])]
    lab = d['group'] + ': ' + ' + '.join(d['orbit_labels'])
    if len(same) > 1: lab += ' (%d)' % (sorted(x['sid'] for x in same).index(d['sid']) + 1)
    faces = []
    for k in range(d['m']):
        c = Counter(e['sides'][j] for j in range(cut[k], cut[k + 1]))
        faces.append(' & '.join('%d×%d-gon' % (n, s) for s, n in sorted(c.items())))
    rec = dict(label=lab, sid=d['sid'], group=d['group'], symmetry_order=d['sym_order'], m=d['m'], N=d['N'],
               orbits=d['orbit_labels'], orbit_sizes=d['sizes'], orbit_representatives=reps, faces_by_orbit=faces,
               corners=e['corners'], hands='two hands' if d['chiral'] else 'one (mirror-symmetric)',
               depths_60_digits=e['depths60'], depths_12=[mp.nstr(mpf(x), 13) for x in e['depths60']],
               residual_solid_angle=e['res_omega'], residual_incidence=e['res_inc'],
               face_directions=d['idx'], found_under=[(f['group_searched'], f['m_searched']) for f in d['found_under']])
    rows.append(rec)
    fn = re.sub(r'[^A-Za-z0-9]+', '-', lab).strip('-')
    rec['file'] = 'dice/%04d-%s.json' % (d['sid'], fn)
    json.dump(rec, open(os.path.join(out, rec['file']), 'w'), indent=1, ensure_ascii=False)
rows.sort(key=lambda r: r['sid'])
json.dump(rows, open(os.path.join(out, 'aequi.json'), 'w'), indent=1, ensure_ascii=False)
with open(os.path.join(out, 'table.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['label', 'group', 'm', 'orbits', 'orbit representatives', 'N', 'faces by orbit', 'corners', 'depths (12 digits)', 'hands'])
    for r in rows: w.writerow([r['label'], r['group'], r['m'], ' + '.join(r['orbits']), ' ; '.join(r['orbit_representatives']), r['N'],
                               ' | '.join(r['faces_by_orbit']), r['corners'], ' ; '.join(r['depths_12']), r['hands']])
def md(rs):
    L = ['| row | group | orbits (representative direction) | N | faces by orbit | corners | depths (first orbit = 1) | hands |', '|---|---|---|---|---|---|---|---|']
    for r in rs:
        L.append('| %d | %s | %s | %d | %s | %d | %s | %s |' % (r['sid'], r['group'], ' + '.join('%s %s' % (o, p) for o, p in zip(r['orbits'], r['orbit_representatives'])),
                 r['N'], '; '.join(r['faces_by_orbit']), r['corners'], ', '.join(r['depths_12']), 'two' if r['hands'] == 'two hands' else 'one'))
    return '\n'.join(L) + '\n'
open(os.path.join(out, 'table.md'), 'w').write('# All Aequi found (full table)\n\nLabel = group + orbit set; the number is the row index in data/aequi.json. Orbit names: family / number of faces when the orbit is part of a family; a+b marks orbits mixing two families (e.g. C6+RT24/10). Depths are the plane distances from the centre, first orbit at 1.\n\n' + md(rows))
open(os.path.join(out, 'table-frame-groups.md'), 'w').write(md([r for r in rows if r['group'] in BIG or r['group'] in ('D3h', 'D5h', 'D6h', 'D8h', 'D10h')]))
# counts by group and m
cnt = Counter((r['group'], r['m']) for r in rows); groups = sorted({g for g, m in cnt}, key=lambda g: (-max(r['symmetry_order'] for r in rows if r['group'] == g), g))
ms = sorted({m for g, m in cnt})
L = ['| group | order | ' + ' | '.join('m=%d' % m for m in ms) + ' | total |', '|---|---|' + '---|' * (len(ms) + 1)]
for g in groups:
    o = next(r['symmetry_order'] for r in rows if r['group'] == g)
    L.append('| %s | %d | ' % (g, o) + ' | '.join(str(cnt.get((g, m), '')) for m in ms) + ' | %d |' % sum(cnt.get((g, m), 0) for m in ms))
L.append('| all | | ' + ' | '.join(str(sum(cnt.get((g, m), 0) for g in groups)) for m in ms) + ' | %d |' % len(rows))
open(os.path.join(out, 'counts.md'), 'w').write('\n'.join(L) + '\n')
print('\n'.join(L))
# controls
log = []
def find(group, labs):
    c = [r for r in rows if r['group'] == group and sorted(r['orbits']) == sorted(labs)]
    assert len(c) == 1, (group, labs, len(c)); return c[0]
EQ = [(10, 'Td', 'O8/4', 'C6', '1.0659165951'), (14, 'Oh', 'C6', 'O8', '1.0141631690'), (16, 'Td', 'O8/4', 'RD12', '1.0692105364'),
      (16, 'T', 'O8/4', 'D12', '1.0603736500'), (18, 'Oh', 'C6', 'RD12', '1.0312505091'), (18, 'Th', 'C6', 'D12', '1.0384442830'),
      (20, 'Oh', 'O8', 'RD12', '1.0370247603'), (20, 'Th', 'O8', 'D12', '1.0265315223'), (24, 'Th', 'RD12', 'D12', '0.9991525381'),
      (32, 'Ih', 'D12', 'O8+I12/20', '1.0043619497'), (42, 'Ih', 'D12', 'C6+RT24/30', '1.0072683224'), (50, 'Ih', 'O8+I12/20', 'C6+RT24/30', '1.0155843036')]
ok = True
for N, g, a, b, mu in EQ:
    r = find(g, [a, b]); da = mpf(r['depths_60_digits'][r['orbits'].index(a)]); db = mpf(r['depths_60_digits'][r['orbits'].index(b)])
    v = mp.nstr(db / da, 15); good = abs(db / da - mpf(mu)) < mpf('6e-11') and r['N'] == N
    ok &= good; log.append('Equanimity N=%d %s %s ∩ %s: μ_f here %s, published %s, hands: %s -> %s' % (N, g, a, b, v, mu, r['hands'], 'PASS' if good else 'FAIL'))
r = find('Th', ['O8', 'RD12', 'I12']); drd = mpf(r['depths_60_digits'][r['orbits'].index('RD12')])
m1 = mpf(r['depths_60_digits'][r['orbits'].index('O8')]) / drd; m2 = mpf(r['depths_60_digits'][r['orbits'].index('I12')]) / drd
p1, p2 = '1.0027592509652673651138588224943292169120', '1.0106639425964276013947211797925550524897'
good = abs(m1 - mpf(p1)) < mpf(10) ** -39 and abs(m2 - mpf(p2)) < mpf(10) ** -39; ok &= good
log.append('D191 (Th: O8 + RD12 + I12, RD at 1): m1 = %s, m2 = %s; study 2026-11-19-aequus-rd-ico: %s, %s (40 digits) -> %s' % (mp.nstr(m1, 41), mp.nstr(m2, 41), p1, p2, 'PASS' if good else 'FAIL'))
# pilot (scripts/three_fam.py): its D12 = (0, ±1, ±φ) cyclic is the OTHER icosahedron placement; sets mixing it with I12/RT24 are cross-frame
for line in open(sys.argv[3]):
    mm = re.match(r'(\S+)\s+N=\s*(\d+)\s+fair solutions: \[\'\(([\d.]+), ([\d.]+)\)\'\]', line)
    if not mm: continue
    fams = mm.group(1).split('+'); x1, x2 = float(mm.group(3)), float(mm.group(4))
    cross = 'D12' in fams and ('I12' in fams or 'RT24' in fams)
    if cross:
        log.append('pilot %-16s cross-frame set (pilot D12 from the other icosahedron placement): not in this definition, not compared' % mm.group(1)); continue
    labs = fams
    cand = [r for r in rows if sorted(r['orbits']) == sorted(labs)]
    if not cand:
        # the die may have more symmetry than Th; find by orbit union
        cand = [r for r in rows if r['group'] in ('Oh', 'Ih', 'Th') and r['N'] == int(mm.group(2))]
    best = None
    for r in cand:
        try: dd = [mpf(r['depths_60_digits'][r['orbits'].index(f)]) for f in fams]
        except ValueError: continue
        v = (float(dd[1] / dd[0]), float(dd[2] / dd[0]))
        if abs(v[0] - x1) < 2e-9 and abs(v[1] - x2) < 2e-9: best = (r, v)
    if best is None and set(fams) == {'C6', 'O8', 'RD12'}:
        r = find('Oh', ['C6', 'O8', 'RD12']); dd = [mpf(r['depths_60_digits'][r['orbits'].index(f)]) for f in fams]; v = (float(dd[1] / dd[0]), float(dd[2] / dd[0]))
        if abs(v[0] - x1) < 2e-9 and abs(v[1] - x2) < 2e-9: best = (r, v)
    good = best is not None; ok &= good
    log.append('pilot %-16s (%.9f, %.9f) -> %s' % (mm.group(1), x1, x2, ('PASS: %s' % best[0]['label']) if good else 'FAIL'))
log.append('CONTROLS ' + ('ALL PASS' if ok else 'SOME FAIL'))
open(os.path.join(out, 'controls.log'), 'w').write('\n'.join(log) + '\n')
print('\n'.join(log)); print('rows', len(rows)); print('FINAL ok' if ok else 'FINAL FAIL')
