#!/usr/bin/env python3
"""paper.src.html -> paper.html: inserts the full catalogue table (Appendix A), read from the exact catalogue of study 2026-11-24-vacuus-resonus-catalogue (data/vacuus-resonus-catalogue.csv).
No computation beyond reading and counting the CSV rows."""
import csv, math, os, sys, html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CSV = os.path.join(ROOT, '..', '..', 'studies', '2026-11-24-vacuus-resonus-catalogue', 'data', 'vacuus-resonus-catalogue.csv')
rows = list(csv.DictReader(open(CSV)))
assert len(rows) == 163, len(rows)

FAM = {'Platonic': 'Platonic', 'Archimedean': 'Archimedean', 'Catalan': 'Catalan',
       'prism': 'prism family', 'antiprism': 'prism family', 'bipyramid': 'prism family', 'trapezohedron': 'prism family',
       'Johnson': 'Johnson'}
counts = {}
for r in rows:
    counts[FAM[r['family']]] = counts.get(FAM[r['family']], 0) + 1
assert counts == {'Platonic': 5, 'Archimedean': 13, 'Catalan': 13, 'prism family': 40, 'Johnson': 92}, counts

# ---------- Appendix A: the full table ----------
def yn(x): return 'yes' if x == 'True' else 'no'
def kind(k): return {'heart': 'H', 'inherited heart': 'IH', 'non-heart': 'N'}[k]
th = ('<tr><th>polyhedron</th><th>V/E/F</th><th>c.s.</th><th>mir.</th>'
      '<th>Vacuus plates (f+s+1)</th><th>kind</th><th>on mir.</th><th>sphere V/E/R</th><th>s.</th>'
      '<th>Resonus planes (2+1)</th><th>on mir.</th><th>sphere V/E/R</th><th>s.</th>'
      '<th>R∩V</th><th>V∩R*</th><th>R∩V*</th></tr>')
GROUP = {'Platonic': 'Platonic', 'Archimedean': 'Archimedean', 'Catalan': 'Catalan', 'prism': 'prisms', 'antiprism': 'antiprisms',
         'bipyramid': 'bipyramids', 'trapezohedron': 'trapezohedra', 'Johnson': 'Johnson polyhedra (corner centroid)'}
trs = []; last = None
for r in rows:
    if r['family'] != last:
        last = r['family']; trs.append(f'<tr class="grp"><td colspan="16">{GROUP[last]}</td></tr>')
    trs.append('<tr>' + ''.join(f'<td>{html.escape(c)}</td>' for c in [
        r['solid'], f"{r['V']}/{r['E']}/{r['F']}", yn(r['centrally_symmetric']), r['mirrors'],
        f"{r['vacuus_plates']} ({r['vacuus_full']}+{r['vacuus_shared']}+{r['vacuus_single']})", kind(r['vacuus_kind']),
        r['vacuus_on_mirrors'], r['vacuus_sphere'], 'y' if r['vacuus_simplicial'] == 'True' else 'n',
        f"{r['resonus_planes']} ({r['resonus_two_faces']}+{r['resonus_one_face']})", r['resonus_on_mirrors'],
        r['resonus_sphere'], 'y' if r['resonus_simplicial'] == 'True' else 'n', r['both'],
        r['vacuus_meets_polar_resonus'], r['resonus_meets_polar_vacuus']]) + '</tr>')
table = '<table class="cat">' + th + '\n'.join(trs) + '</table>'

src = open(os.path.join(ROOT, 'paper.src.html')).read()
assert '__CATTABLE__' in src
out = src.replace('__CATTABLE__', table)
open(os.path.join(ROOT, 'paper.html'), 'w').write(out)
print('paper.html written:', len(rows), 'rows;', counts)
