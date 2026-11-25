# DICTO · Aequi catalogue 2 -> picker data (25 Nov 2026). With Claude (Anthropic).
# Reads app_dice.json (app_build.py: every die rebuilt, fair to 1e-9, full group and orbits as catalogued) and the picker's
# aequi/dice.json + names.json; appends the 9490 dice (s = 'C', no = catalogue number) and their names ("Name #No", Nos. 1233-10725).
# Orbits of Oh / Ih dice reuse the existing orbit entries where the directions agree; other groups get their own orbit lists.
# Usage: python app_data.py <k-mix dir>
import sys, json, csv, os
KM = sys.argv[1]; HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../2026-11-24-aequi-certify-extend/scripts')); from groups import DFAM   # direction family of each of the 122 directions
res = json.load(open(os.path.join(HERE, 'app_dice.json')))
assert all(r['ok'] for r in res) and len(res) == 9490, 'app_dice.json not all ok'
data = json.load(open(os.path.join(KM, 'aequi/dice.json'))); names = json.load(open(os.path.join(KM, 'aequi/names.json')))
assert len(data['dice']) == 1232 and len(names) == 1232
# colour of an orbit: from the existing orbits of the same direction family (first family in the label)
fam_col = {}
for g, orbs in data['groups'].items():
    for o in orbs: fam_col.setdefault(o['lab'].split('/')[0].split('+')[0].rstrip('ab'), o['col'])
def col_of(lab):
    f = lab.split('/')[0].split('+')[0].rstrip('ab').replace('p', '′')
    return fam_col.get(f, fam_col.get(f.rstrip('′'), 'C'))
ORDER = {'Ih': 120, 'Oh': 48, 'D6h': 24, 'D4h': 16, 'D3h': 12, 'D3d': 12, 'D2h': 8, 'D2d': 8, 'D4': 8, 'C4h': 8, 'D3': 6, 'S6': 6,
         'D2': 4, 'C2h': 4, 'S4': 4}
new_groups = sorted({r['group'] for r in res} - set(data['groups']), key=lambda g: -ORDER[g])
for g in new_groups: data['groups'][g] = []
data['listOnly'] = new_groups
READ = {0: ["o", "re", "maru"], 1: ["i", "hi"], 2: ["ni", "fu"], 3: ["mi", "sa"], 4: ["yo", "shi"], 5: ["go", "ko"],
        6: ["mu", "ro"], 7: ["na"], 8: ["ya", "ha"], 9: ["ku"]}   # the approved goroawase rule (study 2026-11-24-aequi-numberings)
def syllables(n):
    out = []
    for ch in str(n):
        rs = READ[int(ch)]; x = rs[0]
        if out and x == out[-1] and len(rs) > 1: x = rs[1]
        out.append(x)
    return out
def shown(n):
    # DICTO 25 Nov: a hyphen after the first two syllables when a name has four or more (2-2, 2-3), e.g. Goko-goko #5555, Io-nanigo #10725
    sy = syllables(n); w = ''.join(sy[:2]) + ('-' + ''.join(sy[2:]) if len(sy) >= 4 else ''.join(sy[2:]))
    return w[0].upper() + w[1:] + ' #' + str(n)
cat = {int(x['No']): x for x in csv.DictReader(open(os.path.join(HERE, 'catalogue.csv')))}
for r in sorted(res, key=lambda r: r['no']):
    g = r['group']; orbs = data['groups'][g]; oi = []
    # labels of the full orbits, matched by (size, depth)
    used = set()
    for o, dpt, sd in zip(r['orbits'], r['depths'], r['sides']):
        fams = {DFAM[d] for d in o}
        cands = [k for k, (L, sz) in enumerate(zip(r['labels'], r['sizes_rec'])) if k not in used and sz == len(o) and set(L.split('/')[0].split('+')) == fams]
        assert cands, (r['no'], fams, r['labels'])
        used.add(cands[0]); lab = r['labels'][cands[0]]
        labp = __import__('re').sub(r'(\d)p\b', '\\1′', lab)   # the picker writes the second placement with a prime
        key = sorted(o)
        j = next((k for k, x in enumerate(orbs) if sorted(x['dirs']) == key), None)
        if j is None:
            orbs.append({'lab': labp, 'plain': labp + ' (' + str(len(o)) + ')', 'col': col_of(lab), 'dirs': key}); j = len(orbs) - 1
        oi.append(j)
    f = ['%d×%s-gon' % (len(o), '/'.join(map(str, sd))) for o, sd in zip(r['orbits'], r['sides'])]
    data['dice'].append({'g': g, 'o': oi, 'd': r['depths'], 'm': r['m'], 'N': r['N'], 'h': r['h'], 'c': r['c'], 'f': f, 's': 'C', 'no': r['no']})
for no in range(1233, 10726):
    x = cat[no]; assert x['name_shown'].startswith(x['name'])
    names.append(x['name'] + ' #' + str(no))
for k in range(len(names)):                   # every name re-derived from its number by the approved rule, then hyphenated
    no = k + 1; plain = names[k].rsplit(' #', 1)[0]
    assert ''.join(syllables(no)).capitalize() == plain, (no, plain)
    names[k] = shown(no)
assert len(names) == 10725 and len(set(n.rsplit(' #', 1)[0].replace('-', '') for n in names)) == 10725
json.dump(data, open(os.path.join(KM, 'aequi/dice.json'), 'w'), separators=(',', ':'))
json.dump(names, open(os.path.join(KM, 'aequi/names.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
print('dice', len(data['dice']), 'names', len(names), 'new groups', new_groups, 'orbits per new group', {g: len(data['groups'][g]) for g in new_groups})
ok = len(data['dice']) == 1232 + 9490 and len(names) == 10725 and all(len(e['o']) == e['m'] for e in data['dice'])
print('FINAL ok' if ok else 'FINAL FAIL (counts)')
