#!/usr/bin/env python3
"""Roadmap step 2: jargon -> everyday-picture glossary for dictospheres.com page copy.
Counts in the last column are measured from the live index.html (local copy) at build time."""
import re, html, datetime
SITE = '~/dictospheres/index.html'
s = open(SITE).read()
s = re.sub(r'<script.*?</script>|<style.*?</style>', '', s, flags=re.S)
T = re.sub(r'<[^>]+>', ' ', s)
def n(pat): return len(re.findall(pat, T))

# (term, count regex, everyday picture, what it means)
G = [
("1. Shapes", [
 ("polyhedron", r"polyhedr", "A cut gemstone; a die.", "A solid bounded by flat faces, straight edges and corners. Plural: polyhedra."),
 ("face · edge · corner (vertex)", r"vertex|vertices", "A box: six faces, twelve edges, eight corners.", "Say corner; keep vertex in brackets the first time on a page."),
 ("Platonic solids", r"Platonic", "The five dice in a role-playing set (d12, d20, d6, d4, d8).", "The only five solids whose faces are all the same regular polygon, meeting the same way at every corner. Listed in D·I·C·T·O order below."),
 ("dodecahedron", r"[Dd]odecahedr", "The 12-sided die.", "12 pentagons, three at each corner."),
 ("icosahedron", r"[Ii]cosahedr", "The 20-sided die; the shell of many viruses.", "20 triangles, five at each corner."),
 ("cube", r"\bcubes?\b", "A sugar cube; the ordinary die.", "6 squares, three at each corner."),
 ("tetrahedron", r"[Tt]etrahedr", "The original Tetra Pak milk carton; a pyramid on a triangle.", "4 triangles, three at each corner; the simplest solid."),
 ("octahedron", r"[Oo]ctahedr", "Two pyramids glued base to base; many natural diamond crystals.", "8 triangles, four at each corner."),
 ("Archimedean / Catalan solids", r"Archimedean|Catalan", "A football is Archimedean.", "Archimedean: faces of two or more regular kinds, every corner alike (13 of them). Catalan: their duals (see dual)."),
 ("truncated", r"[Tt]runcat", "Slicing the corners off a cheese cube; the football is a truncated icosahedron.", "Corners cut off flat, so each corner becomes a new small face."),
 ("rhombic dodecahedron", r"rhombic dodecahedr", "Garnet crystals; the three-diamond floor of a bee's cell is part of one.", "12 identical diamond-shaped faces; fills space with copies of itself."),
 ("cuboctahedron", r"[Cc]uboctahedr", "Halfway between a cube and an octahedron: cut a cube's corners to the edge midpoints.", "8 triangles and 6 squares; the shape around one orange in a tight stack."),
 ("stellation", r"[Ss]tellat", "A Christmas star ornament.", "Extend the faces of a solid outward until they meet again; the result is a star."),
 ("deltahedron", r"[Dd]eltahedr", "A solid you could build only from identical triangle tiles.", "Every face an equilateral triangle."),
 ("antiprism", r"[Aa]ntiprism", "A drum with zigzag lacing between top and bottom.", "Two equal polygons, one turned, joined by a band of triangles."),
 ("convex", r"[Cc]onvex", "A ball, not a banana: a rubber band stretched round it touches everywhere.", "No dents or hollows."),
 ("dual", r"\bdual", "Swap the roles: a dot on each face, then join the dots.", "Faces become corners and corners become faces. Cube ↔ octahedron, dodecahedron ↔ icosahedron; the tetrahedron is its own dual."),
 ("dihedral angle", r"[Dd]ihedral", "How far a book is opened.", "The angle between two faces along their shared edge."),
 ("congruent", r"[Cc]ongruent", "Two biscuits from the same cutter.", "Same shape and size; one can be moved onto the other exactly."),
 ("symmetry", r"[Ss]ymmetr", "Turn a snowflake by a sixth of a turn: it looks unchanged.", "A turn or mirror that leaves the object looking the same."),
 ("net", r"\bnets?\b", "A flattened cereal box.", "The flat cut-out that folds up into the solid. (In crystal papers a net can also mean a network of bonds; say network there.)"),
]),
("2. Filling space", [
 ("tile · tiling · tessellation", r"[Tt]il(e|ing)|[Tt]essellat", "A bathroom floor.", "Covering a flat floor with shapes, with no gaps and no overlaps."),
 ("space-filling", r"[Ss]pace-fill", "Packing a car boot so perfectly that no air is left between the boxes.", "Copies of a solid that fill all of space with no gaps and no overlaps: tiling, one dimension up."),
 ("honeycomb", r"[Hh]oneycomb", "The bees' comb, but with any solid as the cell.", "In geometry, a space-filling arrangement of solids."),
 ("cell", r"\bcells?\b", "A room in a building; a cell of the comb.", "One solid piece of a space-filling, or one 3D piece of the surface of a 4D shape."),
 ("lattice", r"[Ll]attice", "Streetlights on a perfect grid of streets, going on for ever, in three directions.", "Points repeated by the same steps in every direction; every point sees the same view."),
 ("octet", r"[Oo]ctet", "A space-frame roof or climbing frame of triangles (Buckminster Fuller's octet truss).", "Tetrahedra and octahedra together, two tetrahedra to each octahedron, filling space."),
 ("stacking · close-packed layers", r"[Ss]tack", "Oranges on a market stall: each new layer sits in the dips of the one below.", "Each layer can sit in one of three positions, A, B or C; the order of the letters is the stacking."),
 ("c and h layers · hexagonality", r"[Hh]exagonality", "Knitting Crystals (#83): linking yarns run straight on at a c layer and turn back at an h layer.", "A layer is h when the layers on both sides of it match (…ABA…), c when they differ (…ABC…). Hexagonality is the share of h layers: ABAB… 100%, ABCABC… 0%."),
 ("FCC · hcp", r"\bFCC\b|\bfcc\b|\bhcp\b", "The two classic ways greengrocers stack oranges.", "ABCABC… (face-centred cubic) and ABAB… (hexagonal close-packed). Same tightness, different order."),
 ("polytype", r"[Pp]olytype", "The same paving slabs laid in a different repeating order.", "Crystals made of the same layers stacked in different orders, as in silicon carbide (3C, 4H, 6H…)."),
 ("Dehn invariant", r"Dehn", "The cut-and-rebuild test: can this solid be sawn up and reassembled as a cube?", "A number attached to a solid. Two solids of equal volume can be cut into each other only if their Dehn invariants match; a regular tetrahedron cannot become a cube (Dehn 1900)."),
 ("shell · cluster", r"[Ss]hells?\b|[Cc]luster", "Russian dolls; the layers of an onion.", "A group of solids around a centre (cluster), or one complete layer around it (shell)."),
]),
("3. Crystals and nature", [
 ("crystal", r"[Cc]rystal", "Grains of table salt are tiny cubes.", "Atoms arranged in a pattern that repeats in every direction."),
 ("Kagome", r"[Kk]agome", "The kagome weave of a Japanese bamboo basket: triangles and hexagons.", "A pattern of triangles that touch only at their corners, with hexagonal holes between them."),
 ("pyrochlore", r"[Pp]yrochlore", "A climbing frame of pyramids touching only at their tips.", "Kagome's 3D cousin: tetrahedra joined corner to corner. Named after a mineral that turns green in a flame (Greek pyr, fire; chloros, green)."),
 ("spin ice", r"[Ss]pin ice", "Tiny compass needles at every corner, two pointing in and two out at each pyramid.", "Magnets on a pyrochlore network that obey the same two-in, two-out rule as hydrogen in water ice."),
 ("perovskite", r"[Pp]erovskite", "The crystal family behind the newest solar cells.", "A large family of crystals with one shared layout of atoms."),
 ("icosahedral", r"[Ii]cosahedral", "Shaped like the 20-sided die: virus shells, footballs.", "Having the symmetry of the icosahedron, including five-fold turns."),
 ("quasicrystal · aperiodic", r"[Qq]uasicrystal|[Aa]periodic", "Islamic girih tilework: strict rules, yet the pattern never repeats.", "Ordered by a rule, but never repeating by shifting. Found in real alloys (Shechtman, Nobel Prize 2011)."),
 ("Penrose tiling", r"Penrose", "Two diamond-shaped tiles that cover a floor without the pattern ever repeating.", "The best-known aperiodic tiling (Roger Penrose, 1974)."),
 ("approximant", r"[Aa]pproximant", "As 22/7 comes close to π.", "A repeating crystal that comes very close to a quasicrystal."),
 ("Frank–Kasper phases", r"Frank", "Metal alloys packed from near-tetrahedral pieces.", "Crystals in which every gap between atoms is close to a tetrahedron."),
 ("golden ratio φ", r"φ|[Gg]olden ratio", "In a five-pointed star, every line is cut in this ratio.", "About 1.618: the diagonal of a regular pentagon divided by its side. It runs through every shape with five-fold symmetry."),
 ("Fibonacci", r"Fibonacci", "Spirals on a pinecone: often 8 one way, 13 the other.", "1, 1, 2, 3, 5, 8, 13…: each number the sum of the two before; neighbours divide to about φ."),
 ("entropy", r"[Ee]ntropy", "How many ways a deck of cards can be shuffled.", "A measure of how many arrangements fit the same rules."),
]),
("4. Mirrors and higher dimensions", [
 ("mirror · kaleidoscope", r"[Mm]irror|[Kk]aleidoscop", "A kaleidoscope with three mirrors meeting at a point.", "Three mirrors at the right angles turn one small triangle into a whole solid; a dot placed inside it gives all the Platonic and Archimedean solids (Wythoff's construction)."),
 ("four-dimensional", r"[Ff]our-dimensional|\b4D\b", "Shadow puppets: a 3D hand casts a flat shadow; a 4D shape casts a 3D shadow we can build.", "Having a fourth direction at right angles to all three we know."),
 ("polytope", r"[Pp]olytope", "The word that covers polygon, polyhedron and their cousins in any dimension.", "A flat-sided shape in any number of dimensions."),
 ("24-cell · 120-cell · 600-cell", r"\b(24|120|600)-cell", "The 4D cousins of the Platonic solids.", "4D shapes whose surface is made of 24 octahedra, 120 dodecahedra or 600 tetrahedra."),
 ("projection", r"[Pp]rojection", "A shadow on a wall.", "Flattening a shape onto fewer dimensions."),
 ("E8", r"\bE8\b", "The tightest way to stack balls, in eight dimensions.", "An 8-dimensional lattice; Maryna Viazovska proved in 2016 that it packs spheres most tightly."),
 ("Kepler", r"Kepler", "The astronomer who also drew these solids (1596, 1619) and guessed the orange stack is the tightest.", "Johannes Kepler; many solids on the site first appear in his drawings."),
]),
("5. Words of the papers", [
 ("theorem · proved", r"[Tt]heorem|\bproved\b|\bProved\b", "Not 'it worked every time we tried', but 'it cannot fail'.", "A statement shown true in every case by reasoning. Say what was proved, then the word."),
 ("checked by computer", r"exact counts|by computer", "Every case counted, one by one.", "Verified exactly for a stated range; keep the range in the sentence."),
 ("conjecture", r"[Cc]onjecture", "A good guess that nobody has yet proved or broken.", "A statement believed true but not proved."),
 ("non-backtracking walk", r"non-backtracking", "A tourist who never goes straight back down the street just walked.", "A walk along a network that never reverses its last step."),
 ("DOI", r"\bDOI\b", "A permanent library address, like the ISBN of a book.", "Digital Object Identifier: a link to the paper that never breaks. Best placed after the description, not before it."),
 ("Zenodo", r"Zenodo", "CERN's free public library for research.", "Where every DICTO paper and book is archived for good."),
]),
]

today = datetime.date(2026, 11, 8).strftime('%-d %B %Y')
rows = []
for head, items in G:
    rows.append(f'<h2>{html.escape(head)}</h2><table class="g"><tr><th>Term</th><th>Everyday picture</th><th>What it means</th><th>On the site</th></tr>')
    for term, pat, pic, mean in items:
        rows.append(f'<tr><td><b>{html.escape(term)}</b></td><td>{html.escape(pic)}</td><td>{html.escape(mean)}</td><td class="n">{n(pat)}</td></tr>')
    rows.append('</table>')
total = sum(len(i) for _, i in G)

out = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Everyday Words for the Geometry</title><link rel="stylesheet" href="../paper.css">
<style>table.g{{border-collapse:collapse;font-size:8.6pt;width:100%;margin:2mm 0 4mm}} table.g td,table.g th{{border-bottom:1px solid #ccc;padding:1.1mm 1.4mm;text-align:left;vertical-align:top}} table.g th{{font-size:8pt;color:#6b5a2e}} table.g td:first-child{{width:21%}} table.g td:nth-child(2){{width:30%}} td.n{{text-align:right;width:7%;color:#6b5a2e}} table.g tr{{page-break-inside:avoid}} li{{margin:1mm 0}}</style></head><body>
<img class="watermark" src="../dicto-logo.png" alt=""><img class="logo" src="../dicto-logo.png" alt="DICTO">
<h1>Everyday Words for the Geometry<br><span style="font-size:0.72em;font-weight:normal">A glossary for dictospheres.com page copy (roadmap step 2)</span></h1>
<div class="meta"><b>DICTO</b> · dictospheres.com · {today} · {total} entries; counts measured from the live page text. Compiled by Claude (Anthropic) for DICTO.</div>
<div class="status">Working document for DICTO, not for publication. Every picture is for DICTO to keep, change or strike. Next: the "Start Here" page draft (step 3), which will use these pictures.</div>
<h2>How to use it</h2>
<ul>
<li><b>Pair, don't replace.</b> The real word stays; the picture comes first and the word follows: "packing a car boot with no gaps left: space-filling". The mathematics keeps its name, and the newcomer gets a way in.</li>
<li><b>Once per page.</b> Give the picture the first time a word appears on a page or card, then use the word alone.</li>
<li><b>Lead with the object.</b> A card opens with what you can hold or see (the piece, the stack, the fabric), then the result, then the paper number and DOI.</li>
<li><b>Last column:</b> how many times the word (or its family) appears on the page today, so the most frequent words get their pictures first.</li>
</ul>
{''.join(rows)}
<h2>Notes</h2>
<ul>
<li><b>Knitting.</b> The roadmap's "row-by-row patterns used in sweaters" is decoration, a pattern knitted into a fabric. Knitting Crystals (#83) is structural: the knitted sheets are the close-packed layers, and the linking yarns run straight on at a c layer and turn back at an h layer, so the fabric is the crystal. The glossary uses DICTO's version only.</li>
<li><b>Platonic order.</b> The five solids are always listed Dodeca, Icosa, Cube, Tetra, Octa: D·I·C·T·O.</li>
<li><b>Facts checked:</b> Tetra Pak's first carton (1952) was a tetrahedron; virus shells and the football are icosahedral and truncated icosahedral; garnet grows as rhombic dodecahedra; a bee cell's floor is three rhombi; kagome is the Japanese basket weave (kago, basket; me, eye); pyrochlore turns green in a flame; Dehn 1900 (Hilbert's third problem); Shechtman, Nobel Prize in Chemistry 2011; Viazovska, E8, 2016; Penrose tiling 1974; Kepler, Mysterium Cosmographicum 1596 and Harmonices Mundi 1619.</li>
</ul>
</body></html>'''
open('~/k-research/papers/site-glossary/paper.html', 'w').write(out)
print(total, 'entries')
