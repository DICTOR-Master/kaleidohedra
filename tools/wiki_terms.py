#!/usr/bin/env python3
"""Fetch Wikipedia articles in a target language for standard geometry terms, through the English articles' language links.
Used to build the term lists of DICTO's translated editions (ja 11-07, zh 11-07, fa/ar 11-07). Polite: <= 1 request per 2.5 s.
  python3 wiki_terms.py <lang> <out dir>      e.g.  python3 wiki_terms.py fa ~/kaleidohedra-references/persian-models/wikipedia-fa
Writes one <title>.txt per article found and en-<lang>-titles.json (English title -> title in <lang>, or null)."""
import json, os, sys, time, urllib.request, urllib.parse
lang, out = sys.argv[1], os.path.expanduser(sys.argv[2]); os.makedirs(out, exist_ok=True)
H = {'User-Agent': 'dicto-research/1.0 (geometry book translation)'}
def get(host, **q):
    q.update(format='json'); u = f'https://{host}/w/api.php?' + urllib.parse.urlencode(q)
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=60))
EN = ['Regular polytope', 'Polyhedron', '600-cell', '120-cell', 'Tesseract', 'Tessellation', 'Honeycomb (geometry)', 'Rhombic dodecahedron',
      'Truncated icosahedron', 'Icosidodecahedron', 'Golden ratio', 'Platonic solid', 'Archimedean solid', 'Quasicrystal', 'Girih tiles',
      'Through the Looking-Glass', 'Dual polyhedron', 'Snub dodecahedron', 'Kepler–Poinsot polyhedron', 'Close-packing of equal spheres',
      'Cuboctahedron', 'Truncated octahedron', 'Zonohedron', 'Rhombic triacontahedron', 'Space-filling polyhedron', "Abu al-Wafa' Buzjani",
      'Johnson solid', 'Uniform polytope', 'Stellation', 'Crystal structure', 'Fibonacci word', 'Tetrahedron', 'Octahedron',
      'Icosahedron', 'Regular dodecahedron', 'Cube', 'Pyramid (geometry)', 'Dehn invariant', 'Fullerene', 'Spherical design']
links = {}
for i in range(0, len(EN), 10):
    d = get('en.wikipedia.org', action='query', prop='langlinks', lllang=lang, redirects=1, titles='|'.join(EN[i:i + 10]))
    for p in d['query']['pages'].values():
        ll = p.get('langlinks'); links[p['title']] = ll[0]['*'] if ll else None
    time.sleep(2.5)
n = 0
for en, tr in links.items():
    if not tr: print('none:', en); continue
    time.sleep(2.5)
    try:
        p = list(get(f'{lang}.wikipedia.org', action='query', prop='extracts', explaintext=1, redirects=1, titles=tr)['query']['pages'].values())[0]
    except Exception as e:
        print('fail:', en, e); continue
    t = p.get('extract', '')
    if t: open(os.path.join(out, tr.replace('/', '_') + '.txt'), 'w').write(t); n += 1
    print(en, '->', tr, len(t))
json.dump(links, open(os.path.join(out, f'en-{lang}-titles.json'), 'w'), ensure_ascii=False, indent=1)
print('FINAL ok' if n else 'FINAL FAIL (no article fetched)', n, 'articles')
