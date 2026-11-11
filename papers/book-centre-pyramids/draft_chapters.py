# First drafts of the unwritten chapters of "The Centre Pyramids: from Plato to Kepler" (DICTO), written by the local
# workhorse on compute-host (token-free). DRAFTS ONLY: Claude checks every fact, name and number before use.
# Usage: python3 draft_chapters.py   (writes drafts/ch<N>-<name>.html and drafts/LOG.txt)
import json, re, pathlib, urllib.request, time
H = pathlib.Path(__file__).parent; D = H / 'drafts'
def txt(p, n): s = open(p).read(); s = re.sub(r'<[^>]+>', ' ', s); return re.sub(r'\s+', ' ', s)[:n]
P87 = txt(H.parent / 'dicto-vacuus/paper.src.html', 14000); P44 = txt(H.parent / '2026-10-21-aristotles-pyramid/paper.src.html', 9000)
RULES = ('You draft one chapter of a geometry book by the artist DICTO, "The Centre Pyramids: from Plato to Kepler". Output HTML only '
 '(<h2> chapter title, <h3> sections, <p>, <ol>/<ul>). Rules: use ONLY facts given below; never invent numbers, dates, quotes or '
 'references; mark every historical statement you are not given verbatim with [CHECK]. Write "DICTO proposed" for his ideas, '
 'never "DICTO asked"; "we" for joint work. List the five Platonic solids in DICTO order: dodecahedron, icosahedron, cube, '
 'tetrahedron, octahedron. Never use the words "book", "in plain words", "simply put", "in short". Start with a 3-sentence opening '
 'in everyday words for a reader with no mathematics, then the chapter. About 900 words. Mark places for figures as <p class="fig">[FIGURE: what it shows]</p>.')
FACTS6 = ('DICTO built a cube from his PET-bottle system B1NR and saw it is six pyramids meeting at the centre. Before #87 he built the '
 'octahedron Vacuus from corrugated cardboard in four pieces slotted together without glue: square A with one slot from a corner to '
 'the centre, square B with three slots, and square C cut in two along a diagonal, each half with one slot; he laid the pieces out as '
 'three squares. He also made a sphere of slotted circles. Slot-together works exactly for the solids whose fins close into whole '
 'discs through the centre: octahedron (3 squares), cuboctahedron (4 hexagons), icosidodecahedron (6 decagons); for the cube, rhombic '
 'dodecahedron, icosahedron and dodecahedron the fins meet only at the centre. In metal (aluminium, stainless, corten plate) the four '
 'octahedron pieces slide together with no welds or bolts; standing on three corners its own weight holds it; each half of C carries '
 'two drop-in tabs through slots in A. Squares of 0.9 m edge give a piece 1.27 m across that fits a small car. Origami: open-pyramid '
 'fan nets, double walls, two-half-tab rule, fold the cube first. The cube Vacuus in metal needs 8 weld seams from 4 bent strips. '
 'App: a lens in Polyhedraverse shows any solid as Pyramids, Exploded, Star, Sheets and Struts.')
FACTS5 = ('DICTO proposed dissecting the rhombic dodecahedron into the central pyramids of its cube: 12 congruent square pyramids, six '
 'forming the cube at its centre and six standing on the cube\'s faces. So the rhombic dodecahedron has exactly twice the cube\'s volume. '
 'This matches Proposition 2 of #87 read backwards (the cube\'s Star, its centre pyramids turned out, is the rhombic dodecahedron). '
 'Kepler described the rhombic dodecahedron in 1611 [CHECK where and how]. The rhombic dodecahedron fills space. DICTO also proposed '
 'reconstructing: rhombic dodecahedron to two cubes to a 1x1x2 brick. DICTO also proposed halving: the cube splits into two truncated '
 'octahedra (a central one plus eight corner eighths). The Delian problem is only a historical side remark, not DICTO\'s aim.')
JOBS = [('ch1-plato', 'Chapter 1. Plato: the five solids and their centres. Plato\'s Timaeus [CHECK]: the elements as solids, fire as the pyramid. '
         'DICTO\'s artist name D-I-C-T-O is the initials of the five solids. Each solid has a centre O; joining O to each face gives its centre pyramids.', P87[:7000]),
        ('ch3-euclid', 'Chapter 3. Euclid: the third of a prism. Euclid Elements XII.7 [CHECK]: a pyramid is one third of a prism on the same base and '
         'height; Elements XIII builds the five solids in a sphere around a centre [CHECK]. Then the Star law of #87 (Proposition 2: volume exactly twice, '
         'dihedral angle 2 delta at each old edge, Star surface = reflected Vacuus; cube Star = rhombic dodecahedron; in DICTO order the dodecahedron and '
         'icosahedron fold inward, the cube lies flat, the tetrahedron keeps convex edges, the octahedron folds inward).', P87[6000:14000]),
        ('ch5-kepler', 'Chapter 5. Kepler: twelve pyramids in the rhombic dodecahedron. ' + FACTS5, P44[:5000]),
        ('ch6-dicto', 'Chapter 6. DICTO: building the centre pyramids. ' + FACTS6, P87[:4000])]
key = (pathlib.Path.home() / '.config/dicto/llama-key').read_text().strip(); log = open(D / 'LOG.txt', 'a')
for name, brief, src in JOBS:
    t0 = time.time()
    body = json.dumps({'messages': [{'role': 'system', 'content': RULES}, {'role': 'user', 'content': brief + '\n\nSOURCE TEXT (for facts):\n' + src}],
                       'max_tokens': 2600, 'temperature': 0.3, 'chat_template_kwargs': {'enable_thinking': False}}).encode()
    r = urllib.request.Request('http://compute-host:8081/v1/chat/completions', data=body,
                               headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + key})
    try:
        out = json.load(urllib.request.urlopen(r, timeout=1800))['choices'][0]['message']['content']
        (D / f'{name}.html').write_text(out); log.write(f'{name} ok {time.time() - t0:.0f}s {len(out.split())} words\n')
    except Exception as e: log.write(f'{name} FAILED {e}\n')
    log.flush()
log.write('ALL DONE\n')
