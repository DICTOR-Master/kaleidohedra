# Dehn atoms (19 Nov 2026): gather the per-atom results (out/atom-*.json) into data/dehn-atoms.json and the table data/dehn-atoms.md,
# and print the counts. A set entry (one D-number, several pieces) is ZERO or NONZERO only if all its pieces agree; else "mixed".
# Usage: collect.py <manifest.json> <out dir> <calibration.log> <data dir>
import json, os, sys, glob, re
MAN, OUT, CAL, DATA = sys.argv[1:5]
man = json.load(open(MAN)); R = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(OUT, 'atom-*.json')))]
assert len(R) == len(man['atoms']), (len(R), len(man['atoms']))
def why(s):
    v = s.get('verdict', '')
    if v == 'ZERO':
        return 'all dihedrals rational multiples of π' if s['independent_mod_pi'] == 0 else \
            ('relation found: lengths cancel on each of %d independent angle classes' % s['independent_mod_pi'] if s['independent_mod_pi'] > 1 else 'relation found: lengths cancel on its one independent angle class')
    if v == 'NONZERO': return '%d independent angle class%s' % (s['independent_mod_pi'], 'es' if s['independent_mod_pi'] > 1 else '')
    return ''
rows = []
for r in R:
    a = man['atoms'][r['index']]
    src = '; '.join(a.get('files', [])) or a.get('note', '') or a.get('key', '')
    if a['source'] == 'cons': src = 'construction `%s`' % a['key'] + (' — ' + a['note'] if a.get('note') else '')
    if a['source'] == 'ident': src = 'identified (%s)' % (a.get('note') or 'studies/2026-10-14-axe-cleo-fuji/nets/pieces.json, the dehn-words rule')
    pieces = [dict(name=s['name'], faces=s.get('faces'), corners=s['corners'], verdict=s.get('verdict'), why=why(s), distinct_dihedrals=s.get('distinct_dihedrals'),
                   independent_mod_pi=s.get('independent_mod_pi'), rational_pi_dihedrals_deg=s.get('rational_pi_dihedrals_deg'), max_coefficient_sum=s.get('max_coefficient_sum'),
                   checks=s['checks'], info=s.get('info')) for s in r['solids']]
    vs = sorted(set(p['verdict'] for p in pieces))
    verdict = r.get('verdict') if not pieces else (vs[0] if len(vs) == 1 else 'mixed')
    rows.append(dict(no=a['no'], name=a['name'], kind=a['kind'], book=a['book'], source=a['source'], source_detail=src, verdict=verdict, pieces=pieces,
                     error=r.get('error'), extra={k: r[k] for k in ('d1_check',) if k in r}))
calib = [l.strip() for l in open(CAL) if l.startswith(('CAL', 'WORD', 'DIE', 'FINAL', 'undecided'))]
dice = [l for l in calib if l.startswith('DIE')]
tally = {}
for x in rows: tally[x['verdict'] if x['verdict'] in ('ZERO', 'NONZERO', 'UNDECIDED', 'mixed') else ('skipped' if 'skipped' in x['verdict'] else x['verdict'])] = tally.get(x['verdict'] if x['verdict'] in ('ZERO', 'NONZERO', 'UNDECIDED', 'mixed') else ('skipped' if 'skipped' in x['verdict'] else x['verdict']), 0) + 1
solids = [p for x in rows for p in x['pieces']]
st = {}
for p in solids: st[p['verdict']] = st.get(p['verdict'], 0) + 1
summary = dict(in_scope_entries=len(rows), entry_tally=tally, solids_computed=len(solids), solid_tally=st, out_of_scope=len(man['out_of_scope']),
               fair_dice=len(dice), dice_zero=[l for l in dice if ' ZERO ' in l])
json.dump(dict(summary=summary, calibration=calib, atoms=rows, out_of_scope=man['out_of_scope']), open(os.path.join(DATA, 'dehn-atoms.json'), 'w'), indent=1, ensure_ascii=False)
# the table
L = ['| No. | Name (as in the catalogue) | Faces | Dehn | Reason (zero) / independent angle classes (nonzero) | Corners from |', '|---|---|---|---|---|---|']
def cell(t): return str(t).replace('|', '\\|')
for x in rows:
    if not x['pieces']:
        L.append('| %s | %s | — | %s | | %s |' % (cell(x['no']), cell(x['name']), x['verdict'], cell(x['source_detail']))); continue
    if len(x['pieces']) == 1:
        p = x['pieces'][0]
        L.append('| %s | %s | %s | %s | %s | %s |' % (cell(x['no']), cell(x['name']), p['faces'], p['verdict'], p['why'], cell(x['source_detail'])))
    else:
        L.append('| %s | %s | | %s | %d pieces, each below | |' % (cell(x['no']), cell(x['name']), x['verdict'], len(x['pieces'])))
        for p, f in zip(x['pieces'], x['source_detail'].split('; ')):
            L.append('| | · %s | %s | %s | %s | %s |' % (cell(p['name']), p['faces'], p['verdict'], p['why'], cell(f)))
for l in dice:
    m = re.match(r'DIE\s+fair die (\S+) \((\d+) faces\)\s+(\S+)\s+dihedrals (\d+) indep (\d+)', l)
    k = int(m.group(5)); L.append('| fair die | %s (%s faces, #111) | %s | %s | %s | studies/2026-11-18-fair-32-die/data/verts-%s.json |' % (
        m.group(1), m.group(2), m.group(2), m.group(3), 'all dihedrals rational multiples of π' if m.group(3) == 'ZERO' and k == 0 else ('%d independent angle class%s' % (k, 'es' if k > 1 else '')), m.group(1)))
open(os.path.join(DATA, 'dehn-atoms.md'), 'w').write('\n'.join(L) + '\n')
print(json.dumps(summary, ensure_ascii=False, indent=1))
for x in rows:
    if x['verdict'] in ('ZERO', 'mixed'): print('%-7s %-60s %s' % (x['no'], x['name'][:60], x['verdict'] if x['verdict'] == 'ZERO' else 'mixed: ' + ', '.join('%s %s' % (p['name'], p['verdict']) for p in x['pieces'])))
