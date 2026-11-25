"""Tables for the README from the exhaustive search (25 Nov 2026). Usage: python table.py schemes-N4.json"""
import sys, json
from collections import Counter
S = json.load(open(sys.argv[1])); R = S['results']
SH = {0: (1, 2), 1: (0, 2), 2: (0, 1)}        # axis -> (A, B) cards
NAMED = {'W  three whole cards (every slot stops short of the centre or of the rim)': (['Ai', 'Bi', 'Ai', 'Bi', 'Ai', 'Bi'], 'X'),
         '(a) Y in two, both halves slide in along x': (['Bi', 'Bi', 'A', 'B', 'A', 'A'], 'Z'),
         '(a2) Y in two, one half slides in along z': (['A', 'Bi', 'B', 'Bi', 'A', 'A'], 'Z'),
         '(b) Y in four': (['B', 'B', 'A', 'B', 'A', 'A'], 'Z'),
         '(c) closed central slot in X, Y in two': (['Bi', 'Bi', 'Bi', 'Bi', 'A', 'A'], 'Z')}
def lab(card, v):
    if card != 'Y': return card
    return 'Y(%s%s)' % ('+x' if v[0] > 0 else '-x' if v[0] < 0 else '', '+z' if v[2] > 0 else '-z' if v[2] < 0 else '')
for cut in ('octahedron', 'cube'):
    rs = [r for r in R if r['cut'] == cut]
    print('## %s cut: %d schemes' % (cut, len(rs)))
    C = Counter((tuple(sorted(r['pieces_per_card'])), r['outcome']) for r in rs)
    for sig in sorted({s for s, _ in C}, key=lambda s: (sum(s), s)):
        print('  pieces per card %s (total %d): possible %d, impossible %d' % (sig, sum(sig), C[(sig, 'POSSIBLE')], C[(sig, 'IMPOSSIBLE')]))
    print('  sequential order exists for every possible scheme: %s' % all(r['search'] == 'sequential' for r in rs if r['outcome'] == 'POSSIBLE'))
    pos = [sum(r['pieces_per_card']) for r in rs if r['outcome'] == 'POSSIBLE']
    print('  fewest pieces in a possible scheme: %d' % min(pos))
    # closed central slots: on some axis the inner owner holds both inner halves and the centre, the outer owner is a whole card
    cl = []
    for r in rs:
        for a in range(3):
            h = r['half'][2 * a: 2 * a + 2]
            for inner, outer in (('Ai', 1), ('Bi', 0)):
                ic = 'XYZ'[SH[a][0 if inner == 'Ai' else 1]]; oc = SH[a][outer]
                if h == [inner, inner] and r['centre'] == ic and r['pieces_per_card'][oc] == 1: cl.append(r); break
            else: continue
            break
    print('  closed central slot in a whole card (partner holds the middle through the centre): %d schemes, possible %d' % (len(cl), sum(r['outcome'] == 'POSSIBLE' for r in cl)))
    for nm, (h, c) in NAMED.items():
        r = [x for x in rs if x['half'] == h and x['centre'] == c][0]
        o = '' if r['order'] is None else '; order: ' + ', '.join(lab(p, v) + ('' if d is None else ' along %s' % (tuple(-x for x in d),)) for p, v, d in r['order'])
        print('  %s: pieces per card %s, %s%s' % (nm, r['pieces_per_card'], r['outcome'], o))
want = {'W': 'IMPOSSIBLE', '(a)': 'POSSIBLE', '(a2)': 'POSSIBLE', '(b)': 'POSSIBLE', '(c)': 'IMPOSSIBLE'}
got = {nm.split()[0]: [x for x in R if x['cut'] == cut and x['half'] == h and x['centre'] == c][0]['outcome'] for cut in ('octahedron', 'cube') for nm, (h, c) in NAMED.items()}
print('FINAL ok' if got == want else 'FINAL FAIL: named outcomes %s' % got)
