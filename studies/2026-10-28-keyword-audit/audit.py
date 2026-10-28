# Keyword and subject audit (DICTO 10-28): for every DICTO Zenodo record (latest version), propose standard specialist keywords and
# MSC 2020 subject codes by topic, matched on the title, description and existing keywords. Output: proposals.json + audit.html.
import json, os, re, urllib.request, html
tok = open(os.path.expanduser('~/.config/zenodo/token')).read().strip()
C = 'deps.json'
if os.path.exists(C): D = json.load(open(C))
else:
    D = json.load(urllib.request.urlopen(urllib.request.Request('https://zenodo.org/api/deposit/depositions?size=100', headers={'Authorization': 'Bearer ' + tok}), timeout=500)); json.dump(D, open(C, 'w'))
TOPICS = [  # (pattern, keywords in priority order, MSC codes); whole words; first matches win, capped per record
 (r'\b(600-cell|120-cell|4-polytope|polytopes?|four-dimensional|fourth dimension)\b', ['regular polytopes', '4-polytopes', 'cross-sections', 'Schlegel diagram'], ['52B11', '51M20']),
 (r'\b(polytyp\w*|stackings?|close-packed|close packing|hexagonality|swap rule|rule of halves)\b', ['polytypism', 'stacking faults', 'close-packed structures', 'hexagonality'], ['52C17', '82D25']),
 (r'\b(power diagram|voronoi|laguerre|weight walk)\b', ['Voronoi tessellation', 'power diagram'], ['52C22']),
 (r'\b(space-filling|space-filler|fills space|honeycomb|tiling|tessellation)\b', ['space-filling polyhedra', 'tilings'], ['52C22']),
 (r'\b(fibonacci|quasicrystal\w*|aperiodic|penrose)\b', ['quasicrystals', 'aperiodic order', 'Fibonacci chain'], ['52C23']),
 (r'\b(golden|icosahedral|icosahedron|dodecahedron)\b', ['golden ratio', 'icosahedral symmetry'], ['52B10']),
 (r'\b(polyhedron|polyhedra|solid|solids)\b', ['polyhedra'], ['52B10']),
 (r'\b(rock salt|zinc blende|laves|silicon carbide|pyrochlore|perovskite|crystal|crystals)\b', ['crystal structures'], ['82D25']),
 (r'\b(sculpture|sculptor|pet bottles?|pet-bottle)\b', ['geometric sculpture', 'mathematics and art'], ['00A66']),
]
out = []
for d in sorted(D, key=lambda x: x['id']):
    if d.get('state') != 'done': continue
    m = d['metadata']; text = (m['title'] + ' ' + re.sub('<[^>]+>', ' ', m.get('description', '')) + ' ' + ' '.join(m.get('keywords', []))).lower()
    have = {k.lower() for k in m.get('keywords', [])}; add, msc = [], set()
    for pat, kws, codes in TOPICS:
        if re.search(pat, text):
            for k in kws:
                if k.lower() not in have and k not in add and len(add) < 6: add.append(k)
            for c_ in codes:
                if len(msc) < 3: msc.add(c_)
    out.append({'id': d['id'], 'concept': d.get('conceptrecid'), 'title': m['title'], 'keywords': m.get('keywords', []), 'add': add, 'msc': sorted(msc)})
json.dump(out, open('proposals.json', 'w'), indent=1, ensure_ascii=False)
rows = ''.join(f"<tr><td>{html.escape(o['title'][:90])}</td><td>{html.escape(', '.join(o['keywords']))}</td><td><b>{html.escape(', '.join(o['add']))}</b></td><td>{', '.join(o['msc'])}</td></tr>" for o in out)
open('audit.html', 'w').write(f'''<!doctype html><html><head><meta charset="utf-8"><title>Keyword audit</title><link rel="stylesheet" href="../../papers/paper.css">
<style>table{{border-collapse:collapse;font-size:7.4pt;width:100%}} td,th{{border-bottom:1px solid #ddd;padding:1mm;vertical-align:top;text-align:left}} b{{color:#8a6a10}}</style></head><body>
<h1>Keyword and subject audit</h1><p class="sub">Every DICTO record on Zenodo: current keywords, proposed additions (gold) and MSC 2020 subject codes</p>
<p>MSC 2020: 52B10 three-dimensional polytopes; 52B11 n-dimensional polytopes; 51M20 polyhedra and polytopes, regular figures; 52C17 packing and covering; 52C22 tilings; 52C23 quasicrystals and aperiodic tilings; 82D25 crystals; 00A66 mathematics and visual arts. Additions are in-place metadata edits (no new versions); your names stay.</p>
<table><tr><th>Record</th><th>Current keywords</th><th>Add</th><th>MSC</th></tr>{rows}</table></body></html>''')
print(len(out), 'records;', sum(len(o['add']) for o in out), 'keywords proposed')
