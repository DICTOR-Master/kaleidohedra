# First draft of "DICTO-Kepler Golden Truncations" / golden truncated triangles (DICTO 11-02) by the local workhorse on compute-host.
# DRAFT ONLY: Claude checks every statement and number against trunc-exact.md and fet-exact.md before use.
import json, pathlib, urllib.request
H = pathlib.Path(__file__).parent
FACTS = (H / 'trunc-exact.md').read_text() + '\n' + (H / 'fet-exact.md').read_text() + '''
Established today (exact, sympy over Q(sqrt5), from the DICTO Solids dataset v7):
- A truncated triangle = hexagon with all angles 120 deg and sides alternating a, b (Coxeter t{3}); its symmetry is ditrigonal.
- In the dataset (69 solids) every 3-fold hexagonal face is a truncated triangle whose long/short ratio lies in Q(sqrt5): phi in Icosaxes Hexa (56 faces), White Knight (20), Icosaxes (8), Unborn Axes (8); sqrt5 TI Star core (20); 1 + 3 sqrt5/5 GTI (20); phi^4/2 Golden Clasp (8); (1+2sqrt5)/5 Haigha (2); (5+4sqrt5)/11 Hatta (2). No other hexagon in the dataset has 3-fold symmetry.
- GTI and TI Star core are exactly truncated icosahedra (12 regular pentagons + 20 truncated triangles, one plane distance per face kind); Icosaxes and Unborn Axes are exactly truncated octahedra (6 squares + 8 truncated triangles); White Knight follows the truncated icosidodecahedron pattern and Golden Clasp the truncated cuboctahedron pattern, with rectangles in place of squares. Their cutting depths (ratio of plane distances) are golden, not Archimedean: Icosaxes depth^2 = 3/phi^2 (Archimedean truncated octahedron 4/3), Unborn Axes 3 phi^2/5, GTI phi sqrt5/3, Golden Clasp hexagon/octagon depth^2 = 3/phi^2 (same as Icosaxes). White Knight hexagon/decagon depth^2 = 13/3 - 22 sqrt5/15, the Archimedean truncated icosahedron's own value.
- Classical background: Archimedean and Johnson solids have only regular faces, Catalan solids have no hexagons, zonohedra hexagons are centrally symmetric. Kepler (Harmonices Mundi, 1619) described the Archimedean truncations. DICTO's #20 (The FUJI Family: Pyramids on Flat-Ended Triangles) first used the shape.
- Group names (DICTO): DICTO-GTT-Solids (squares + golden truncated triangles, Oh, two edge lengths: Icosaxes, Icosaxes Hexa, Unborn Axes); 'DICTO-Kepler' proposed for the golden truncations.'''
RULES = ('Draft a short geometry paper by the artist DICTO, HTML (<h1>,<h2>,<p>,<table>). Title: "DICTO-Kepler Golden Truncations: Archimedean Patterns '
 'Cut at Golden Depths". Structure: plain 3-sentence opening for non-mathematicians; Main Theorem stated first (from the facts); definitions (truncated '
 'triangle, cutting depth); results table; the two cross-links; classical background; what is DICTO\'s; conclusion. Use ONLY the facts given; never invent '
 'numbers or references; mark any unsupported historical point [CHECK]. State his ideas directly, no running credit ("DICTO proposed", "asked"); "we" for joint work. Platonic solids '
 'in DICTO order (dodecahedron, icosahedron, cube, tetrahedron, octahedron). Never write "flat-ended" (except inside the cited title of #20), "book", '
 '"in plain words", "simply put". Mark figures as <p class="fig">[FIGURE: ...]</p>. About 1500 words.')
key = (pathlib.Path.home() / '.config/dicto/llama-key').read_text().strip()
body = json.dumps({'messages': [{'role': 'system', 'content': RULES}, {'role': 'user', 'content': FACTS}], 'max_tokens': 4000, 'temperature': 0.3,
                   'chat_template_kwargs': {'enable_thinking': False}}).encode()
r = urllib.request.Request('http://compute-host:8081/v1/chat/completions', data=body, headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + key})
out = json.load(urllib.request.urlopen(r, timeout=2400))['choices'][0]['message']['content']
(H / 'drafts' / 'draft-1.html').write_text(out); print('draft written', len(out.split()), 'words')
