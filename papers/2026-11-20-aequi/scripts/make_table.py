# Writes Table 3 of "Fair Dice — The Aequi" (the 149 rows of the main catalogue) into ../paper.html between the
# markers <!--CATALOGUE--> and <!--/CATALOGUE-->, straight from the catalogue study's data/catalogue.csv.
# Usage: STUDIES=<folder holding the studies> python3 make_table.py
import csv, os, re, html
S = os.environ.get('STUDIES', '../../../studies')
rows = list(csv.DictReader(open(os.path.join(S, '2026-11-20-aequi-catalogue/data/catalogue.csv'), encoding='utf-8')))
assert len(rows) == 149
NAMES = {'Ih': 'Ih, full icosahedral symmetry', 'Oh': 'Oh, full cube symmetry', 'Td': 'Td, full tetrahedral symmetry',
         'Th': 'Th, pyritohedral symmetry', 'T': 'T, tetrahedral rotations only (each die in two hands)'}
def faces(s):   # "20×6-gon; 12×5-gon" -> "20×6, 12×5"
    return ', '.join(p.strip().replace('-gon', '') for p in s.split(';'))
out, cur = [], None
for r in rows:
    if r['group'] != cur:
        cur = r['group']; k = sum(1 for x in rows if x['group'] == cur)
        out.append(f'<tr class="hd"><td colspan="6"><b>{html.escape(NAMES[cur])}</b>: {k} dice</td></tr>')
    name = r['name'].split(',')[0].replace('Aequus ', '')
    out.append(f'<tr><td class="n">{r["group"]} {r["number"]}</td><td>{html.escape(name)}</td><td class="n">{r["m"]}</td>'
               f'<td class="n">{r["N"]}</td><td>{html.escape(faces(r["faces"]))}</td><td>{r["D"]}</td></tr>')
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'paper.html')
h = open(P, encoding='utf-8').read()
new = '<!--CATALOGUE-->\n' + '\n'.join(out) + '\n<!--/CATALOGUE-->'
h2, n = re.subn(r'<!--CATALOGUE-->.*?<!--/CATALOGUE-->', lambda m: new, h, flags=re.S)
assert n == 1, 'markers not found'
open(P, 'w', encoding='utf-8').write(h2)
print(f'Table 3: {len(rows)} rows written; FINAL ok')
