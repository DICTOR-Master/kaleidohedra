"""Parse the saved pages of the Imperial College 'Database of Ionic Radii'
(http://abulafia.mt.ic.ac.uk/shannon/radius.php?Element=X, fetched 2026-10-25),
a transcription of Shannon, Acta Cryst. A32 (1976) 751-767, into JSON.
Columns: ion, charge, CN, spin, crystal radius CR, ionic radius IR, key (Angstrom)."""
import re, html, json, glob, os, sys
here = os.path.dirname(os.path.abspath(__file__))
raw = os.path.join(here, '..', 'data', 'raw', 'shannon-db')
out = {}
for f in sorted(glob.glob(os.path.join(raw, '*.html'))):
    el = os.path.basename(f)[:-5]
    t = open(f, encoding='latin-1').read()
    t = t[t.find('<h4>Ion</h4>'):t.find('Radii are in Angstrom')]
    rows = re.findall(r'<tr>(.*?)</tr>', t, re.S)
    charge = None; recs = []
    for r in rows:
        cells = [html.unescape(re.sub('<[^>]+>', '', c)).replace('\xa0', '').strip()
                 for c in re.findall(r'<td[^>]*>(.*?)</td>', r, re.S)]
        if len(cells) == 7:
            charge = cells[1]; cells = cells[2:]
        elif len(cells) == 6:   # new charge block without ion cell
            charge = cells[0]; cells = cells[1:]
        if len(cells) != 5: continue
        cn, spin, cr, ir, key = cells
        recs.append(dict(charge=int(charge), CN=cn, spin=spin, CR=cr, IR=ir, key=key))
    out[el] = recs
json.dump(out, open(os.path.join(here, '..', 'data', 'raw', 'shannon.json'), 'w'), indent=1)
for el, recs in out.items():
    print(el, [(r['charge'], r['CN'], r['IR'], r['key']) for r in recs])
