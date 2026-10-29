# "All the atoms" (Quanta of Space, DICTO 10-29: the book of all the atoms as a chapter of the overview): the catalogue of
# every named shape of DICTO's work from DICTO Solids (dataset v5, index.csv): DICTO's new shapes in D-number order, then
# the known and rediscovered shapes the work uses. A shape with exact geometry in the dataset gets its icon (render_atoms.py).
# Output: atoms-catalogue.html (a block of pages for the book). Usage: atoms.py <index.csv> <icons dir> <out html>
import csv, html, os, re, sys
idx, icons, out = sys.argv[1:4]
rows = list(csv.DictReader(l for l in open(idx, encoding='utf8') if not l.startswith('#')))
e = html.escape
def dnum(r): m = re.match(r'D(\d+)$', r['universal_number']); return int(m.group(1)) if m else None
def icon(r):
    f = r['dataset_file'].replace('solids/', '').replace('.json', '.png') if r['dataset_file'] else ''
    return f if f and os.path.exists(os.path.join(icons, f)) else ''
def where(r):
    p = r['paper'].strip(); doi = re.search(r'10\.5281/zenodo\.\d+', r['dicto_doi'] or '')
    w = p or (r['finding'] and 'finding ' + r['finding']) or ''
    return f'<a href="https://doi.org/{doi.group(0)}">{e(w)}</a>' if doi and w else e(w)
def card(r):
    num = r['universal_number'] or '—'; ic = icon(r)
    note = e(r['prior_art_or_note'] or r['status'])
    # DICTO 10-29: say clearly what "known" means for Alicia Boole Stott's sections: the shape is hers, the exact geometry DICTO's
    w = re.match(r'(W\d+|R\d+):', r['prior_art_or_note'] or '')
    if r['status'].startswith('known') and 'Boole Stott' in (r['prior_art_or_note'] or ''):
        note = ((w.group(1) + '. ') if w else '') + ('Shape first found by Alicia Boole Stott (1900), by construction, drawn as a plan and built as a card model; '
                'its exact geometry (coordinates, volume, symmetry, checked) computed by DICTO in #63.' + (' Named after her by DICTO.' if r['name'] == 'Alicia' else ''))
    pic = f'<img src="figures/atoms/{ic}" alt="{e(r["name"])}">' if ic else '<div class="noicon">no exact model in the dataset</div>'
    return (f'<div class="atom">{pic}<div class="an"><b>{e(num)}</b> {e(r["name"])}</div>'
            f'<div class="am">{e(r["kind"])} · {where(r)}</div><div class="ant">{note}</div></div>')
new = sorted((r for r in rows if dnum(r)), key=dnum)
newc = [r for r in rows if not dnum(r) and r['status'].startswith('new')]   # DICTO's new clusters, structures, networks: no D-number (D-numbers are for single solids and pieces)
other = [r for r in rows if not dnum(r) and not r['status'].startswith('new')]   # known or rediscovered: at the end of the book
css = '''<style>
.atoms { display: grid; grid-template-columns: repeat(4, 1fr); gap: 3mm 4mm; }
.atom { break-inside: avoid; font: 7.6pt/1.3 "Nimbus Sans", "Liberation Sans", sans-serif; }
.atom img { width: 100%; display: block; border-radius: 2mm; }
.atom .noicon { aspect-ratio: 1; border: 1px dashed #bbb; border-radius: 2mm; color: #999; font-size: 7pt; display: flex; align-items: center; justify-content: center; text-align: center; padding: 2mm; }
.atl { font: 7.4pt/1.3 "Nimbus Sans", "Liberation Sans", sans-serif; width: 100%; } .atl td, .atl th { padding: 1mm 1.5mm; vertical-align: top; } .tl { font-size: 9pt; margin-top: 4mm; text-align: left; caption-side: top; padding-bottom: 2mm; }
.atom .an { margin-top: 1mm; font-size: 8.4pt; } .atom .am { color: #6b5310; } .atom .ant { color: #555; font-size: 7pt; }
</style>'''
with open(out, 'w', encoding='utf8') as f:
    f.write(css)
    f.write('<section class="page catalogue">\n<p class="chapter-mark">Chapter 1 · Atoms · the catalogue</p>\n<h1>All the atoms</h1>\n')
    f.write(f'<p>Every named shape of the work, one quantum of space each: first DICTO\'s new shapes, {len(new)} of them, D1 to D{dnum(new[-1])} (given in order of first publication, never reused); then his {len(newc)} new clusters, structures and networks built from them; the {len(other)} known or rediscovered shapes the work builds with are listed at the end of the book. A shape whose model file is in the dataset <i>DICTO Solids: Exact Geometry</i> is drawn, all in one pose: gold for DICTO\'s new shapes, silver for known ones. Under each: its kind, the paper or finding it comes from (linked to its DICTO DOI), and the status found by the prior-art search.</p>\n')
    # DICTO 10-29: all the pictures first, then the shapes not yet drawn, in tables at the end of the catalogue
    def row(r): return f'<tr><td>{e(r["universal_number"] or "—")}</td><td>{e(r["name"])}</td><td>{e(r["kind"])}</td><td>{where(r)}</td><td>{e((r["prior_art_or_note"] or r["status"])[:140])}</td></tr>'
    def pics(title, rs): f.write(f'<h2>{title}</h2>\n<div class="atoms">\n' + '\n'.join(card(r) for r in rs if icon(r)) + '\n</div>\n')
    pics("DICTO's new atoms", new)
    f.write('<p class="tl">D-numbers are given to single solids and pieces. DICTO\'s new clusters, structures and networks, built from them, follow without numbers.</p>\n')
    pics("DICTO's new clusters, structures and networks", newc)
    f.write('<h2>Not drawn here</h2>\n<p class="tl">Each of these is computed exactly in its paper or finding, but is not yet a model file in the data set.</p>\n')
    for title, rs in (("DICTO's new atoms", new), ("DICTO's new clusters, structures and networks", newc)):
        rest = [r for r in rs if not icon(r)]
        if rest:
            f.write(f'<table class="atl"><caption class="tl">{title}</caption><thead><tr><th>No.</th><th>Shape</th><th>Kind</th><th>From</th><th>Status</th></tr></thead>\n' + '\n'.join(row(r) for r in rest) + '\n</table>\n')
    f.write('</section>\n')
# the known and rediscovered shapes go to the very end of the book (DICTO 10-29), so nothing after the new atoms reads as known
with open(out.replace('.html', '-known.html'), 'w', encoding='utf8') as f:
    f.write('<section class="page catalogue">\n<p class="chapter-mark">The known shapes</p>\n<h1>Known and rediscovered shapes in the work</h1>\n')
    f.write(f'<p>The {len(other)} shapes the work builds with that were made first by others, or rediscovered by DICTO and found in the sources checked; each keeps the number its first maker gave it. Drawn in silver where its exact geometry is in the dataset.</p>\n')
    pics = [r for r in other if icon(r)]; rest = [r for r in other if not icon(r)]
    f.write('<div class="atoms">\n' + '\n'.join(card(r) for r in pics) + '\n</div>\n')
    if rest:
        f.write('<table class="atl"><caption class="tl">Not drawn here: computed in the sources, not yet a model file in the data set</caption><thead><tr><th>No.</th><th>Shape</th><th>Kind</th><th>From</th><th>Status</th></tr></thead>\n')
        f.write('\n'.join(f'<tr><td>{e(r["universal_number"] or "—")}</td><td>{e(r["name"])}</td><td>{e(r["kind"])}</td><td>{where(r)}</td><td>{e((r["prior_art_or_note"] or r["status"])[:140])}</td></tr>' for r in rest) + '\n</table>\n')
    f.write('</section>\n')
print('new', len(new), 'new clusters', len(newc), 'other', len(other), 'with icons', sum(1 for r in rows if icon(r)))
