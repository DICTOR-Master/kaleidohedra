# Assemble the catalogue of the two-placement Aequi: merge the classified dice (dice.json) with the 80-digit refinement
# (exact.jsonl); per-die JSON, the full table (CSV and Markdown), counts by group and m, and the controls:
#  (1) the pilot's 7 sets that mix the placements (study 2026-11-19-aequi-three-families, run1.log; its D12 = (0, ±1, ±φ)
#      cyclic is D12p here, its I12 and RT24 are placement A's) must reappear with the same depths to 9 digits;
#  (2) sets using one placement only are not searched again (counts equal to the earlier study's 57 Th and 153 T sets),
#      and no die found here is congruent to any of the 4553 Aequi of study 2026-11-19-aequi-complete.
# usage: make_table.py dice.json exact.jsonl pilot_run1.log old_exact.jsonl.gz classes.json outdir
import json, sys, os, re, csv, gzip, itertools
import numpy as np
from collections import Counter, defaultdict
from mpmath import mp, mpf
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from groups import DIRS, DFAM, FAMS, show, dperm, QT
mp.dps = 70
dice = json.load(open(sys.argv[1])); E = {}
for L in open(sys.argv[2]):
    r = json.loads(L); E[r['sid']] = r
out = sys.argv[6]; os.makedirs(os.path.join(out, 'dice'), exist_ok=True)
def fmt_dir(j):
    v = DIRS[j]; phi = (1 + 5 ** .5) / 2
    vals = {0: '0', 1: '1', phi: 'φ', 1 / phi: '1/φ'}
    sc = {'C6': 1, 'O8': 3 ** .5, 'RD12': 2 ** .5, 'D12': (phi ** 2 + 1) ** .5, 'I12': (phi ** 2 + phi ** -2) ** .5, 'RT24': 2}[DFAM[j].rstrip('p')]
    s = []
    for c in v * sc:
        for x, t in vals.items():
            if abs(abs(c) - x) < 1e-9: s.append(('-' if c < -1e-9 else '') + t); break
    return '(' + ', '.join(s) + ')'
A = [d for d in dice['dice'] if d['centroid_at_origin'] and not d['face_transitive']]
FT = [d for d in dice['dice'] if d['face_transitive']]
assert all(d['sid'] in E and E[d['sid']]['exact_ok'] for d in A)
# the refined record must agree with the double-precision classification (group, corners, orbit count)
mism = [d['sid'] for d in A if E[d['sid']]['sym_group'] != d['group'] or E[d['sid']]['corners'] != d['corners'] or len(E[d['sid']]['face_orbits']) != d['m']]
seen = defaultdict(list)
for d in A: seen[(d['group'], tuple(d['orbit_labels']))].append(d)
rows = []
for d in A:
    e = E[d['sid']]; same = seen[(d['group'], tuple(d['orbit_labels']))]
    cut = list(itertools.accumulate([0] + d['sizes']))
    reps = [fmt_dir(max(d['idx'][cut[k]:cut[k + 1]], key=lambda j: tuple(DIRS[j]))) for k in range(d['m'])]
    labs = [show(x) for x in d['orbit_labels']]
    lab = d['group'] + ': ' + ' + '.join(labs)
    if len(same) > 1: lab += ' (%d)' % (sorted(x['sid'] for x in same).index(d['sid']) + 1)
    faces = []
    for k in range(d['m']):
        c = Counter(e['sides'][j] for j in range(cut[k], cut[k + 1]))
        faces.append(' & '.join('%d×%d-gon' % (n, s) for s, n in sorted(c.items())))
    rec = dict(label=lab, sid=d['sid'], group=d['group'], symmetry_order=d['sym_order'], m=d['m'], N=d['N'],
               orbits=labs, orbit_sizes=d['sizes'], orbit_representatives=reps, faces_by_orbit=faces,
               corners=e['corners'], hands='two hands' if d['chiral'] else 'one (mirror-symmetric)',
               depths_60_digits=e['depths60'], depths_12=[mp.nstr(mpf(x), 13) for x in e['depths60']],
               residual_solid_angle=e['res_omega'], residual_incidence=e['res_inc'],
               face_directions=d['idx'], found_under=[(f['group_searched'], f['m_searched']) for f in d['found_under']])
    rows.append(rec)
    fn = re.sub(r'[^A-Za-z0-9]+', '-', lab.replace('′', 'p')).strip('-')
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
open(os.path.join(out, 'table.md'), 'w').write('# All two-placement Aequi found (full table)\n\nLabel = group + orbit set; the number is the row index in data/aequi.json. D12′, I12′, RT24′ are the second icosahedron placement (D12′ = (0, ±1, ±φ) cyclic). A label X+Y/k is an orbit of k directions taken from both X and Y (for example D12+D12′/24 under Oh). Depths are the plane distances from the centre, first orbit at 1.\n\n' + md(rows))
cnt = Counter((r['group'], r['m']) for r in rows); groups = sorted({g for g, m in cnt}, key=lambda g: (-max(r['symmetry_order'] for r in rows if r['group'] == g), g))
ms = sorted({m for g, m in cnt})
L = ['| group | order | ' + ' | '.join('m=%d' % m for m in ms) + ' | total |', '|---|---|' + '---|' * (len(ms) + 1)]
for g in groups:
    o = next(r['symmetry_order'] for r in rows if r['group'] == g)
    L.append('| %s | %d | ' % (g, o) + ' | '.join(str(cnt.get((g, m), '')) for m in ms) + ' | %d |' % sum(cnt.get((g, m), 0) for m in ms))
L.append('| all | | ' + ' | '.join(str(sum(cnt.get((g, m), 0) for g in groups)) for m in ms) + ' | %d |' % len(rows))
open(os.path.join(out, 'counts.md'), 'w').write('\n'.join(L) + '\n')
print('\n'.join(L))
log = []; ok = not mism
log.append('refined vs double-precision classification (group, corners, orbits): %d mismatches -> %s' % (len(mism), 'PASS' if not mism else 'FAIL %s' % mism))
# (1) pilot
qp = dperm(QT)
fullmap = {}
for r in rows:
    e = E[r['sid']]; dep = np.repeat([mpf(x) for x in e['depths60']], r['orbit_sizes'])
    fullmap[frozenset(r['face_directions'])] = (r, dict(zip(r['face_directions'], dep)))
PIL = {'C6': 'C6', 'O8': 'O8', 'RD12': 'RD12', 'D12': 'D12p', 'I12': 'I12', 'RT24': 'RT24'}
npil = 0
for line in open(sys.argv[3]):
    mm = re.match(r'(\S+)\s+N=\s*(\d+)\s+fair solutions: \[\'\(([\d.]+), ([\d.]+)\)\'\]', line)
    if not mm: continue
    fams = mm.group(1).split('+')
    if not ('D12' in fams and ('I12' in fams or 'RT24' in fams)): continue   # the 13 one-placement sets were checked in the earlier study
    npil += 1; x1, x2 = float(mm.group(3)), float(mm.group(4))
    parts = [[j for j in range(len(DIRS)) if DFAM[j] == PIL[f]] for f in fams]
    best = None
    for turned in (False, True):
        P = [[qp[j] for j in p] for p in parts] if turned else parts
        hit = fullmap.get(frozenset(j for p in P for j in p))
        if hit is None: continue
        r, dm = hit; dd = [dm[p[0]] for p in P]
        assert all(abs(dm[j] - dd[i]) < mpf(10) ** -40 for i, p in enumerate(P) for j in p)
        best = (r, (dd[1] / dd[0], dd[2] / dd[0]), turned)
    good = best is not None and abs(best[1][0] - mpf(mm.group(3))) < mpf('1e-9') and abs(best[1][1] - mpf(mm.group(4))) < mpf('1e-9')
    ok &= good
    log.append('pilot %-15s N=%s (%.9f, %.9f) here %s -> %s' % (mm.group(1), mm.group(2), x1, x2,
               '(%s, %s)%s' % (mp.nstr(best[1][0], 12), mp.nstr(best[1][1], 12), ' [as its quarter-turned image]' if best[2] else '') if best else 'not found',
               ('PASS: %s' % best[0]['label']) if good else 'FAIL'))
ok &= npil == 7
# (2a) one-placement sets excluded
cls = json.load(open(sys.argv[5]))
one = {c['name']: sum(v['one_placement'] for v in c['counts'].values()) for c in cls}
both = {c['name']: sum(v['both_bounded'] for v in c['counts'].values()) for c in cls}
srch = Counter()
for s in dice['status']: srch[s['group']] += s['searched']
good = one == {'Th': 57, 'T': 153} and all(srch[g] == both[g] for g in both)
ok &= good
log.append('one-placement sets: Th %d, T %d (= the sets searched in study 2026-11-19-aequi-complete: 57, 153), excluded; searched here: Th %d, T %d (= both-placement sets %d, %d) -> %s'
           % (one['Th'], one['T'], srch['Th'], srch['T'], both['Th'], both['T'], 'PASS' if good else 'FAIL'))
# (2b) no die congruent to a die of the earlier study
def sig(verts, cen, vol, nrm, D):
    s = vol ** (1 / 3); V = np.array(verts)
    return np.r_[np.sort((D - nrm @ cen) / s), np.sort(np.linalg.norm(V - cen, axis=1) / s)]
old = defaultdict(list); nold = 0
for Lr in gzip.open(sys.argv[4], 'rt'):
    e = json.loads(Lr); nold += 1
    D = np.repeat([float(x) for x in e['depths60']], e['sizes']); nrm = DIRS[e['idx']]
    old[(len(e['idx']), e['corners'])].append(sig(e['verts'], np.array(e['centroid']), e['volume'], nrm, D))
same = []
for r in rows:
    e = E[r['sid']]; D = np.repeat([float(x) for x in e['depths60']], r['orbit_sizes']); nrm = DIRS[r['face_directions']]
    s = sig(e['verts'], np.array(e['centroid']), e['volume'], nrm, D)
    if any(len(t) == len(s) and np.abs(t - s).max() < 1e-6 for t in old[(r['N'], r['corners'])]): same.append(r['label'])
good = nold == 4553 and not same; ok &= good
log.append('congruence with the %d Aequi of study 2026-11-19-aequi-complete: %d of %d dice here congruent to one there -> %s' % (nold, len(same), len(rows), 'PASS' if good else 'FAIL %s' % same))
h = Counter()
for s in dice['status']:
    for n, c in s['sols_hist'].items(): h[n] += c
log.append('fair dice per searched set (double precision, in the search box): %s' % dict(sorted(h.items())))
log.append('face-transitive solids met (excluded, one orbit): %s' % ', '.join(sorted({'%s %s N=%d' % (d['group'], show(d['orbit_labels'][0]), d['N']) for d in FT})))
log.append('CONTROLS ' + ('ALL PASS' if ok else 'SOME FAIL'))
open(os.path.join(out, 'controls.log'), 'w').write('\n'.join(log) + '\n')
print('\n'.join(log)); print('rows', len(rows)); print('FINAL ok' if ok else 'FINAL FAIL')
