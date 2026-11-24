"""Task 2 (b), screen at 60 digits: Double Vision's factor 3 (in radius squared; sqrt3 in radius). Does any Aequus with its
Resonus in the 31 planes have two orbits whose depth ratio r gives the factor 3 from phi-steps, i.e. r^2 = 3 phi^k or phi^k / 3
for an integer k (|k| <= 12)?  Depths: 60 digits (study 2026-11-19-aequi-complete) or certified enclosures, radius about 1e-40
(study 2026-11-24-aequi-certify-extend).  A hit is a ratio within 1e-30.  -> data/factor3.json"""
import glob, gzip, json, os, re
from decimal import Decimal as D, getcontext
getcontext().prec = 70
HERE = os.path.dirname(os.path.abspath(__file__)); ST = os.path.join(HERE, '../..')
S5 = D(5).sqrt(); PHI = (1 + S5) / 2; LPHI = PHI.ln(); L3 = D(3).ln()
def fams(label): return label.split('/')[0].split('+')
def frame(orbits):
    F = [f for o in orbits for f in fams(o)]
    if any(f.startswith('RD12') for f in F): return 'cube'
    pr = any(f.endswith('p') for f in F); un = any(f in ('D12', 'I12', 'RT24') for f in F)
    return 'both' if (pr and un) else 'primed31' if pr else '31'
def test(dep, orbits):
    hits = []
    for i in range(len(dep)):
        for j in range(i + 1, len(dep)):
            x = 2 * (dep[i] / dep[j]).ln()
            for sgn in (1, -1):
                y = (x - sgn * L3) / LPHI; k = y.to_integral_value()
                if abs(y - k) < D(10) ** -30 and abs(k) <= 12: hits.append((orbits[i], orbits[j], ('3' if sgn > 0 else '1/3'), int(k)))
    return hits
rows = []; n = 0
for f in sorted(glob.glob(os.path.join(ST, '2026-11-19-aequi-complete/data/dice/*.json'))):
    d = json.load(open(f))
    if frame(d['orbits']) in ('31', 'primed31'):
        n += 1; h = test([D(x) for x in d['depths_60_digits']], d['orbits'])
        if h: rows.append(dict(src='4553', sid=d['sid'], label=d['label'], hits=h))
enc = re.compile(r"\[([-0-9.e]+) \+/- ([0-9.e-]+)\]")
for f in sorted(glob.glob(os.path.join(ST, '2026-11-24-aequi-certify-extend/data/certify*.jsonl.gz'))):
    b = os.path.basename(f)[7:-9]
    for line in gzip.open(f, 'rt'):
        d = json.loads(line)
        if d.get('status') != 'certified': continue
        lab = d['label'].split(': ', 1)[1]; orbits = [o.strip() for o in lab.split(' + ')]
        if frame(orbits) not in ('31', 'primed31'): continue
        t = eval(d['tight']) if isinstance(d['tight'], str) else d['tight']
        dep = [D(1)] + [D(enc.match(s).group(1)) for s in t['enclosure']][:len(orbits) - 1]
        n += 1; h = test(dep, orbits)
        if h: rows.append(dict(src='ext ' + b, sid=d['sid'], label=d['label'], hits=h))
json.dump(dict(n_dice=n, hits=rows), open(os.path.join(HERE, '../data/factor3.json'), 'w'), indent=1)
print('dice', n, 'with a factor-3 ratio:', len(rows))
for r in rows: print(r)
print('FINAL ok' if n == 4039 else 'FINAL FAIL: %d dice' % n)
