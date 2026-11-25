# After collect.py: compare every Aequus found here with every catalogued Aequus and keep the new ones for certification.
# Catalogued: the 1232 (149 frame-group dice of study 2026-11-19-aequi-complete + 1083 of 2026-11-20-aequi-two-placements),
# the 4404 of study 2026-11-19-aequi-complete (certified in 2026-11-24-aequi-certify-4404; same dice folder), and the
# 9490 of study 2026-11-24-aequi-certify-extend (catalogue-2; the 9556 found there, 66 of them repeats among themselves).
# Congruence invariant (as post2a.py of the extension study): scale-free sorted plane distances from the centroid and sorted
# corner distances (volume 1). Different invariants => not congruent (sound); equal to 1e-6 => counted as a repeat.
# A repeat also needs the same full group and corner count, and the same Gram signature of catalogue-2 (common.py).
# Mirror images have equal invariants, so a chiral die and its mirror image count once.
# usage: post.py collected.json     (writes data/counts.md, data/dice-new.json, data/aequi.json, data/repeats.json)
import json, sys, os, glob, gzip, importlib.util, numpy as np
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from groups import DIRS
from exact import combinatorics, centroid
ST = os.path.normpath(os.path.join(HERE, '..', '..'))
spec = importlib.util.spec_from_file_location('groups_ext', os.path.join(ST, '2026-11-24-aequi-certify-extend', 'scripts', 'groups.py'))
gx = importlib.util.module_from_spec(spec); spec.loader.exec_module(gx); XDIRS = gx.DIRS   # 122 directions of the two placements
def sig(Nrm, sizes, dep):
    D = np.repeat(np.asarray(dep, float), sizes); V, inc, trip, faces = combinatorics(Nrm, D); cen, vol = centroid(V, faces, Nrm, D)
    s = vol ** (1 / 3); return np.r_[np.sort((D - Nrm @ cen) / s), np.sort(np.linalg.norm(V - cen, axis=1) / s)]
old = defaultdict(list); n_old = Counter()
for study in ['2026-11-19-aequi-complete', '2026-11-20-aequi-two-placements']:
    for f in glob.glob(os.path.join(ST, study, 'data', 'dice', '*.json')):
        d = json.load(open(f)); src = '1232' if (study.startswith('2026-11-20') or d['group'] in {'Ih', 'Oh', 'Td', 'Th', 'T', 'O', 'I'}) else '4404'
        n_old[src] += 1
        old[d['N']].append((src, study + ':' + os.path.basename(f), sig(XDIRS[d['face_directions']], d['orbit_sizes'], [float(x) for x in d['depths_60_digits']]), d['group'], d['corners'], XDIRS[d['face_directions']], np.repeat([float(x) for x in d['depths_60_digits']], d['orbit_sizes'])))
for b in ['2a', '2caps', '2caps2', '2caps3']:
    for i, d in enumerate(json.load(gzip.open(os.path.join(ST, '2026-11-24-aequi-certify-extend', 'data', 'aequi%s.json.gz' % b)))['new']):
        n_old['9490 (9556 with repeats)'] += 1
        old[d['N']].append(('9490', 'ext-%s:%d' % (b, i), sig(XDIRS[d['idx']], d['sizes'], d['depths']), d['group'], d['corners'], XDIRS[d['idx']], np.repeat(d['depths'], d['sizes'])))
print('catalogued dice loaded:', dict(n_old), flush=True)
col = json.load(open(sys.argv[1])); dice = col['dice']
aeq = [d for d in dice if d['centroid_at_origin'] and not d['face_transitive']]
new, rep, twins = [], [], []
# second invariant (study 2026-11-24-aequi-catalogue-2, common.py sig): Gram matrix of the normals with depth levels
import hashlib
def gsig(U, d, Q=1e4):     # copied from study 2026-11-24-aequi-catalogue-2, common.py sig (statistics bookkeeping dropped)
    U = np.asarray(U, float); U = U / np.linalg.norm(U, axis=1)[:, None]; d = np.asarray(d, float); d = d / d.min()
    G = U @ U.T; ds = np.sort(d); cut = np.diff(ds) > 1e-7
    lev_s = np.r_[0, np.cumsum(cut)]; lev = lev_s[np.searchsorted(ds, d - 5e-8)]
    gi = np.rint(G * Q).astype(np.int64); R = np.sort(gi * 1000 + lev[None, :], axis=1)
    R = np.c_[lev, R]; R = R[np.lexsort(R.T[::-1])]
    return hashlib.sha1(R.tobytes()).hexdigest() + ':%d' % len(d), ds
for d in aeq:
    sv = sig(DIRS[d['idx']], d['sizes'], d['depths']); hit = None
    kn = gsig(DIRS[d['idx']], np.repeat(d['depths'], d['sizes']))
    for src, name, so, g, c, U, dd in old.get(d['N'], []):
        if len(so) == len(sv) and np.abs(so - sv).max() < 1e-6:
            same = g == d['group'] and c == d['corners']; ko = gsig(U, dd); gram = ko[0] == kn[0] and np.abs(ko[1] - kn[1]).max() < 1e-6
            if same and gram: hit = (src, name); break
            twins.append(dict(group=d['group'], labels=d['orbit_labels'], N=d['N'], other=(src, name, g), same_group_corners=same, gram_signature_equal=gram))
    if hit: rep.append(dict(group=d['group'], m=d['m'], N=d['N'], labels=d['orbit_labels'], same_as=hit))
    else: new.append(d)
print('Aequi found', len(aeq), '| face-transitive', sum(d['face_transitive'] for d in dice), '| centroid off centre', sum(not d['centroid_at_origin'] for d in dice))
print('congruent to a catalogued die:', len(rep), dict(Counter(r['same_as'][0] for r in rep)), '| NEW:', len(new))
for r in rep: print('  repeat', r['group'], ' + '.join(r['labels']), 'N', r['N'], '=', r['same_as'])
def table(L):
    tab = Counter((d['group'], d['m']) for d in L); order = {d['group']: d['sym_order'] for d in L}
    gs = sorted(order, key=lambda g: (-order[g], g)); ms = sorted({m for g, m in tab})
    T = ['| group | order | ' + ' | '.join('m=%d' % m for m in ms) + ' | total |', '|---|---|' + '---|' * (len(ms) + 1)]
    for g in gs: T.append('| %s | %d | ' % (g, order[g]) + ' | '.join(str(tab.get((g, m), '')) for m in ms) + ' | %d |' % sum(tab[(g, m)] for m in ms))
    T.append('| all | | ' + ' | '.join(str(sum(tab[(g, m)] for g in gs)) for m in ms) + ' | %d |' % len(L))
    return '\n'.join(T)
t = table(new); print(t); open('data/counts.md', 'w').write('New Aequi by full group and m\n\n' + t + '\n\nAll Aequi met (new and repeats)\n\n' + table(aeq) + '\n')
recs = [dict(study='2026-11-25-five-cubes', sid=i, file='', label=d['group'] + ': ' + ' + '.join(d['orbit_labels']), group=d['group'], m=d['m'], N=d['N'],
             sizes=d['sizes'], idx=d['idx'], depths=['1.0'] + ['%.17g' % x for x in d['depths'][1:]], corners=d['corners'], refine=True)
        for i, d in enumerate(new)]
json.dump(recs, open('data/dice-new.json', 'w'))
json.dump(dict(new=new), open('data/aequi.json', 'w')); json.dump(rep, open('data/repeats.json', 'w'), indent=1); json.dump(twins, open('data/twins.json', 'w'), indent=1)
print('equal distance invariants but NOT congruent (different group, corners or Gram signature):', len(twins), dict(Counter((t['group'], t['other'][2]) for t in twins)))
for t in twins: print('  twin', t)
print('FINAL ok' if len(aeq) == len(rep) + len(new) and n_old['1232'] == 1232 and n_old['4404'] == 4404 and n_old['9490 (9556 with repeats)'] == 9556 else 'FINAL FAIL')
