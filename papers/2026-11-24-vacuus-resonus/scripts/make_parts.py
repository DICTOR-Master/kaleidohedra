#!/usr/bin/env python3
"""paper.src.html -> paper.html: inserts the catalogue figure (inline SVG) and the full catalogue table (Appendix A),
both read from the exact catalogue of study 2026-11-24-vacuus-resonus-catalogue (data/vacuus-resonus-catalogue.csv).
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

# ---------- figure: Vacuus plates against Resonus planes, log scale ----------
W, H = 640, 470
L, R, T, B = 62, 170, 18, 52
lo, hi = 1, 256
def sx(v): return L + (math.log2(v) - math.log2(lo)) / (math.log2(hi) - math.log2(lo)) * (W - L - R)
def sy(v): return H - B - (math.log2(v) - math.log2(lo)) / (math.log2(hi) - math.log2(lo)) * (H - T - B)
# neutral palette (abstract labels): greys and one slate blue; shapes carry the family
STY = {'Platonic': ('#1f2a36', 'square'), 'Archimedean': ('#3d5a73', 'diamond'), 'Catalan': ('#7a8fa3', 'triangle'),
       'prism family': ('#a7a59c', 'circle'), 'Johnson': ('#5f5f5f', 'cross')}
def mark(x, y, fam, simp):
    col, shp = STY[fam]
    fill = col if simp else 'none'
    s = 4.2
    if shp == 'square':
        return f'<rect x="{x-s:.1f}" y="{y-s:.1f}" width="{2*s:.1f}" height="{2*s:.1f}" fill="{fill}" stroke="{col}" stroke-width="1.3"/>'
    if shp == 'diamond':
        return f'<polygon points="{x:.1f},{y-s-1:.1f} {x+s+1:.1f},{y:.1f} {x:.1f},{y+s+1:.1f} {x-s-1:.1f},{y:.1f}" fill="{fill}" stroke="{col}" stroke-width="1.3"/>'
    if shp == 'triangle':
        return f'<polygon points="{x:.1f},{y-s-1:.1f} {x+s+0.6:.1f},{y+s-0.6:.1f} {x-s-0.6:.1f},{y+s-0.6:.1f}" fill="{fill}" stroke="{col}" stroke-width="1.3"/>'
    if shp == 'circle':
        return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{s-0.4:.1f}" fill="{fill}" stroke="{col}" stroke-width="1.2" fill-opacity="0.85"/>'
    return (f'<path d="M{x-s:.1f},{y-s:.1f}L{x+s:.1f},{y+s:.1f}M{x-s:.1f},{y+s:.1f}L{x+s:.1f},{y-s:.1f}" stroke="{col}" '
            f'stroke-width="{2.2 if simp else 1.1}" stroke-opacity="0.8"/>')

parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" '
         'aria-label="Vacuus plates against Resonus planes for the 163 polyhedra of the catalogue" '
         'style="font-family:DejaVu Sans,sans-serif;font-size:11px">']
parts.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff"/>')
for k in range(0, 9):
    v = 2 ** k
    parts.append(f'<line x1="{sx(v):.1f}" y1="{T}" x2="{sx(v):.1f}" y2="{H-B}" stroke="#e6e4de" stroke-width="1"/>')
    parts.append(f'<line x1="{L}" y1="{sy(v):.1f}" x2="{W-R}" y2="{sy(v):.1f}" stroke="#e6e4de" stroke-width="1"/>')
    parts.append(f'<text x="{sx(v):.1f}" y="{H-B+15}" text-anchor="middle" fill="#444">{v}</text>')
    parts.append(f'<text x="{L-6}" y="{sy(v)+4:.1f}" text-anchor="end" fill="#444">{v}</text>')
parts.append(f'<line x1="{sx(lo):.1f}" y1="{sy(lo):.1f}" x2="{sx(hi):.1f}" y2="{sy(hi):.1f}" stroke="#b8962e" stroke-width="1.2" stroke-dasharray="5 4"/>')
parts.append(f'<text x="{sx(150):.1f}" y="{sy(190):.1f}" fill="#8a7020" text-anchor="end">equal counts</text>')
parts.append(f'<rect x="{L}" y="{T}" width="{W-L-R}" height="{H-T-B}" fill="none" stroke="#999"/>')
parts.append(f'<text x="{(L+W-R)/2:.0f}" y="{H-12}" text-anchor="middle" fill="#222">Vacuus: plates through the centre and an edge</text>')
parts.append(f'<text transform="translate(16,{(T+H-B)/2:.0f}) rotate(-90)" text-anchor="middle" fill="#222">Resonus: planes through the centre parallel to a face</text>')
order = ['prism family', 'Johnson', 'Catalan', 'Archimedean', 'Platonic']
for fam in order:
    for r in rows:
        if FAM[r['family']] != fam:
            continue
        v, s = int(r['vacuus_plates']), int(r['resonus_planes'])
        simp = r['resonus_simplicial'] == 'True'
        parts.append(mark(sx(v), sy(s), fam, simp))
# label the two polyhedra whose Vacuus and Resonus are the same set of planes (exact, catalogue Theorem B)
for name, dx, dy, lab in [('rhombic dodecahedron', 8, 16, 'rhombic dodecahedron'), ('rhombic triacontahedron', -8, -10, 'rhombic triacontahedron')]:
    r = next(r for r in rows if r['solid'] == name)
    v, s = int(r['vacuus_plates']), int(r['resonus_planes'])
    assert int(r['both']) == v == s
    anchor = 'start' if dx > 0 else 'end'
    parts.append(f'<circle cx="{sx(v):.1f}" cy="{sy(s):.1f}" r="8" fill="none" stroke="#b8962e" stroke-width="1.4"/>')
    parts.append(f'<text x="{sx(v)+dx:.1f}" y="{sy(s)+dy:.1f}" text-anchor="{anchor}" fill="#8a7020">{lab} (Vacuus = Resonus)</text>')
# legend
lx, ly = W - R + 16, T + 14
parts.append(f'<text x="{lx}" y="{ly}" fill="#222" font-weight="bold">family (rows)</text>')
for i, fam in enumerate(['Platonic', 'Archimedean', 'Catalan', 'prism family', 'Johnson']):
    y = ly + 20 + 19 * i
    parts.append(mark(lx + 6, y - 4, fam, True))
    parts.append(f'<text x="{lx+18}" y="{y}" fill="#222">{fam} ({counts[fam]})</text>')
y = ly + 20 + 19 * 5 + 14
parts.append(f'<text x="{lx}" y="{y}" fill="#222" font-weight="bold">Resonus</text>')
parts.append(mark(lx + 6, y + 16, 'Platonic', True) + f'<text x="{lx+18}" y="{y+20}" fill="#222">simplicial</text>')
parts.append(mark(lx + 6, y + 35, 'Platonic', False) + f'<text x="{lx+18}" y="{y+39}" fill="#222">not simplicial</text>')
parts.append(f'<text x="{W-8}" y="{H-6}" text-anchor="end" fill="#888" font-size="9.5">DICTO · dictospheres.com</text>')
parts.append('</svg>')
svg = '\n'.join(parts)

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
assert '__CATFIG__' in src and '__CATTABLE__' in src
out = src.replace('__CATFIG__', svg).replace('__CATTABLE__', table)
open(os.path.join(ROOT, 'paper.html'), 'w').write(out)
print('paper.html written:', len(rows), 'rows;', counts)
