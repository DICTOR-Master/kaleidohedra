# DICTO 2026-10-20: number audit of the OG polytypes paper against the exact study output (polytype-exact.json) and exact arithmetic.
#   python3 audit.py <studies/2026-10-20-og-polytypes>
import sys, os, json, re
from fractions import Fraction as F
D = json.load(open(os.path.join(sys.argv[1], 'polytype-exact.json')))
txt = re.sub(r'<[^>]+>', ' ', open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'paper.src.html')).read())
S5 = 5 ** .5; bad = 0
def q(s): a, b = s.split('|'); return F(a), F(b)
def mul(x, y): return (x[0] * y[0] + 5 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])
def inv(x): n = x[0] ** 2 - 5 * x[1] ** 2; return (x[0] / n, -x[1] / n)
def chk(cond, msg):
    global bad; print(('PASS ' if cond else 'FAIL ') + msg); bad += (not cond)
def intext(s): return s in txt
cell = (F(32, 27), F(16, 27))
share = lambda name: mul(q(D['solids'][name]['volume']), inv(cell))
for name, want, shown in [('OG', (F(1025, 114), F(-145, 38)), '1025/114 − 145√5/38 ≈ 45.89%'), ('OTT', (F(176, 3), F(-26)), '176/3 − 26√5 ≈ 52.89%'),
                          ('DBT', (F(493, 6), F(-73, 2)), '493/6 − 73√5/2 ≈ 55.02%'), ('RT (golden envelope)', (F(90), F(-40)), '90 − 40√5 = 10/φ⁶ ≈ 55.73%')]:
    s = share(name); chk(s == want and intext(shown), f'{name} share {s} in text as "{shown}"')
chk(abs(90 - 40 * S5 - 10 / ((1 + S5) / 2) ** 6) < 1e-12, '90 - 40 sqrt5 = 10/phi^6')
ov = D['overlap']['RT (golden envelope)']
diff = (q(D['solids']['RT (golden envelope)']['volume'])[0] - q(D['solids']['DBT']['volume'])[0], q(D['solids']['RT (golden envelope)']['volume'])[1] - q(D['solids']['DBT']['volume'])[1])
chk(all(ov[w]['largest_overlap_volume'] == f'{diff[0]}|{diff[1]}' for w in ('ch', 'hc', 'hh')) and ov['cc']['overlap_free'] and intext('(−88 + 40√5)/81 ≈ 0.017811'),
    f'envelope overlap at h = envelope - DBT = {diff}; none at cc')
chk(all(D['overlap']['DBT'][w]['overlap_free'] for w in ('cc', 'ch', 'hc', 'hh')), 'DBT overlap-free for cc, ch, hc, hh')
for nm, v in D['solids'].items():
    chk(v['centre_symmetric'] and v['three_fold_111'] and v['mirror_image_equals_60deg_turn'] and not v['mirror_perp_111_is_a_symmetry'], f'{nm}: twin rule premises and conclusion')
chk(D['solids']['OG']['inside_its_octahedron'] and D['solids']['OTT']['inside_its_octahedron'] and not D['solids']['DBT']['inside_its_octahedron'] and D['solids']['DBT']['inside_its_layer']
    and not D['solids']['RT (golden envelope)']['inside_its_layer'], 'Table 1 octahedron / layer columns')
chk(D['solids']['OG']['pyritohedral_rotations'] and D['solids']['OTT']['pyritohedral_rotations'] and not D['solids']['DBT']['pyritohedral_rotations'], 'all four axes: OG, OTT yes; DBT one axis')
rows = {'3C (octet)': ('c', 'ABC', '0'), '2H (gyrated octet)': ('h', 'AB', '1'), '4H': ('hc', 'ABCB', '1/2'), '6H': ('hcc', 'ABCACB', '1/3'), '9R': ('hhc', 'ABACACBCB', '2/3'), '15R': ('hcchc', 'ABCACBCABACABCB', '2/5')}
for nm, (w, seq, f) in rows.items():
    p = D['polytypes'][nm]; fh = F(f)
    chk(p['jagodzinski'] == w and p['share_h'] == f and seq.startswith(p['abc'][:len(seq)][:7]) and intext(seq),
        f'{nm}: word {w}, packing {seq}, f = {f}; pieces caps {8 - 2 * fh}, twin {fh}, tets {2 - 2 * fh}, bip {fh}')
    want = {'caps': 8 - 2 * fh, 'twin caps': fh, 'tetrahedra': 2 - 2 * fh, 'bipyramids': fh}
    chk(all(F(p['pieces_per_cell'][k]) == v for k, v in want.items()), f'{nm}: piece counts match the study')
fb = D['polytypes']['Fibonacci (aperiodic)']['pieces_per_cell']
chk(fb['caps'] == '5|1' and fb['twin caps'] == '3/2|-1/2' and fb['tetrahedra'] == '-1|1' and fb['bipyramids'] == '3/2|-1/2', 'Fibonacci: 5 + sqrt5, (3 - sqrt5)/2, sqrt5 - 1, (3 - sqrt5)/2')
chk(intext('2584 of the first 6765'), 'Fibonacci counts in text')
w = 'c'
for _ in range(20): w = ''.join('ch' if x == 'c' else 'c' for x in w)
pos = [i for i, x in enumerate(w) if x == 'h']
chk('hh' not in w and 'ccc' not in w and set(b - a for a, b in zip(pos, pos[1:])) == {2, 3} and w.startswith('chcchchcchcch'), 'Fibonacci word: no hh, no ccc, h planes 2 or 3 apart; first letters as printed')
chk(intext('(277 − 79√5)/1539') and intext('(16 + 8√5)/81'), 'cap and tetrahedron volumes as in #37a')
print('ALL PASS' if bad == 0 else f'{bad} FAIL')
