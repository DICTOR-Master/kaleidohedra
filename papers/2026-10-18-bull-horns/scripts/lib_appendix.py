# DICTO 2026-10-19: the appendix table (reference-library sources whose full text was searched for the octet paper).
# usage: python3 -I lib_appendix.py <library root> <folder of extracted .txt (pdftotext)>  -> prints <tr> rows, sorted by year
import sys, json, glob, os, html
LIB, TXT = sys.argv[1], sys.argv[2]
meta = {}
for m in glob.glob(f'{LIB}/*/MANIFEST.json'):
    d = json.load(open(m)); items = d if isinstance(d, list) else d.get('entries', d.get('items', []))
    for e in items:
        fn = e.get('file')
        if isinstance(fn, str) and fn: meta[os.path.basename(fn.rstrip('/'))] = e
MANUAL = {'Fedorov-1885-Nachala-ucheniya-o-figurah.pdf': ('1885', 'E. S. Fedorov', 'Elements of the Theory of Figures (Nachala ucheniya o figurah)'),
          'Grunbaum-2010-Bilinski-dodecahedron-v2-3-10.pdf': ('2010', 'B. Grünbaum', 'The Bilinski dodecahedron, and assorted parallelohedra, zonohedra, monohedra, isozonohedra and otherhedra'),
          'Betke-Henk-2000-Densest-lattice-packings-3-polytopes.pdf': ('1999', 'U. Betke, M. Henk', 'Densest lattice packings of 3-polytopes'),
          'kabai-demonstrations_54FacedSpaceFillingPolyhedron.txt': ('2007', 'S. Kabai', '54-Faced Space-Filling Polyhedron (Wolfram Demonstration; description and screenshot)'),
          'kabai-demonstrations_GoldenOctetTruss.txt': ('2007', 'S. Kabai', 'Golden Octet Truss (Wolfram Demonstration; description and screenshot)'),
          'kabai-demonstrations_ARhombicDodecahedronMadeOfRhombicTriacontahedra.txt': ('2008', 'S. Kabai', 'A Rhombic Dodecahedron Made of Rhombic Triacontahedra (Wolfram Demonstration; description and screenshot)'),
          'kabai-demonstrations_RelatingARhombicTriacontahedronAndARhombicDodecahedron.txt': ('2008', 'S. Kabai', 'Relating a Rhombic Triacontahedron and a Rhombic Dodecahedron (Wolfram Demonstration; description and screenshot)'),
          'kabai-demonstrations_ClusterOf14RhombicTriacontahedra.txt': ('2015', 'S. Kabai', 'Cluster of 14 Rhombic Triacontahedra (Wolfram Demonstration; description and screenshot)')}
SKIP = ('README', 'READING-LIST', 'fedorov-ch13-ocr', 'Fedorov-1885-chapter13-English')
rows = []
for t in sorted(glob.glob(f'{TXT}/*.txt')):
    name = os.path.basename(t)[:-4]; base = name.split('_', 1)[-1] if '_' in name else name
    if any(base.startswith(k) for k in SKIP): continue
    if base in MANUAL: rows.append(MANUAL[base]); continue
    e = meta.get(base) or meta.get(base.replace('.txt', '')) or {}
    a = e.get('authors') or ''; a = ', '.join(a) if isinstance(a, list) else a
    title = e.get('title') or base.rsplit('.', 1)[0].replace('-', ' ')
    yr = str(e.get('year') or '')
    rows.append((yr, a, title))
key = lambda r: ((r[1].replace(',', ' ').split() or [''])[0].lower(), r[2].lower().rstrip('.'))
seen = set(); uniq = []
for r in rows:
    if key(r) in seen: continue
    seen.add(key(r)); uniq.append(r)
rows = uniq
rows.sort(key=lambda r: (r[0] or '9999', r[1]))
for yr, a, title in rows: print(f'<tr><td>{html.escape(a)}</td><td>{html.escape(yr)}</td><td>{html.escape(title)}</td></tr>', end='')
print(); print(len(rows), file=sys.stderr)
