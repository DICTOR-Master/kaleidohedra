# render_jewels.py (15 Nov 2026) - DICTO · dictospheres.com
# The jewellery figures of the Platonic book's chapter "Filigree": DICTO's image of gold filigree holding stones of different shapes
# close together. Two materials only: stones (Platonic solids, element colours) and one gold (every connector, every band).
# Core designs (the connector kit as filigree) and their variations (pierced bands, closed loops, satellite stones; DICTO 15 Nov).
# Every piece comes from exact coordinates: the golden cell, Admiral Caps, caps, Dogstars, R and Z from the checked builders of
# study 2026-11-14-platonic-hybrid (golden.py, hybrid.py); octet pieces from integer coordinates (corners at the even points of
# Z^3 scaled to edge 1 or to edge phi^2/sqrt2). Exact checks (integers / Q(sqrt5)) run first: X lines; counts: COUNT lines.
# Usage: render_jewels.py <outdir> [width_px]  -> PROGRESS lines, X / COUNT lines, FINAL ok / FINAL FAIL
import sys, os, itertools, numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
OUTD = sys.argv[1]; W = int(sys.argv[2]) if len(sys.argv) > 2 else 2400
from jewels_lib import *                                # renderer, G (golden), H (hybrid), Part, V, PHI, HF ...
os.makedirs(OUTD, exist_ok=True)
FAIL = []
def X(name, ok, detail=''):
    print(('X PASS ' if ok else 'X FAIL ') + name + (f': {detail}' if detail != '' else ''), flush=True)
    if not ok: FAIL.append(name)
def C(name, pieces, want):
    got = count(pieces); print('COUNT', name, got, flush=True)
    if got != want: FAIL.append('count ' + name)
O3 = V(0, 0, 0)
upper_cap = lambda p, zc: p[0] == 'cap' and np.mean([float(v[2]) for q in p[1] for v in q.verts]) > zc

# ================= exact octet ring (integers) =================
# octet: corners at points of Z^3 with even coordinate sum; octahedra centred at the odd points (corners c +- e_i); tetrahedra:
# in every unit cube a + [0,1]^3 the four even corners. Layer between the triangle planes x+y+z = 0 and x+y+z = 2.
E3 = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
def octa(c): return frozenset(tuple(c[k] + s * e[k] for k in range(3)) for e in E3 for s in (1, -1))
def tetra(a): return frozenset(tuple(a[k] + d[k] for k in range(3)) for d in itertools.product((0, 1), repeat=3) if (sum(a) + sum(d)) % 2 == 0)
O0c = (1, 0, 0); O0 = octa(O0c)
cand = [('O', octa(c)) for c in itertools.product(range(-2, 5), repeat=3) if sum(c) % 2] + \
       [('T', tetra(a)) for a in itertools.product(range(-2, 5), repeat=3)]
inlayer = lambda vs: all(0 <= sum(v) <= 2 for v in vs)
ring = [(k, vs) for k, vs in cand if vs != O0 and inlayer(vs) and len(vs & O0) >= 2]
ring = list(dict.fromkeys(ring))
nT = sum(1 for k, _ in ring if k == 'T'); nO = sum(1 for k, _ in ring if k == 'O')
adj = {i: [j for j in range(len(ring)) if j != i and len(ring[i][1] & ring[j][1]) == 3] for i in range(len(ring))}
cyc = [0]; prev = None
while True:
    nxt = [j for j in adj[cyc[-1]] if j != prev]
    if not nxt: break
    prev, n = cyc[-1], nxt[0]
    if n == 0: break
    cyc.append(n)
X('octet ring: the pieces of the layer that share an edge with the missing octahedron are 6 tetrahedra and 6 octahedra',
  nT == 6 and nO == 6, f'T {nT}, O {nO}')
X('octet ring: each shares a whole triangle face with exactly two others, and they close up in one cycle of 12, '
  'tetrahedra and octahedra alternating', all(len(a) == 2 for a in adj.values()) and len(cyc) == 12
  and all(ring[cyc[i]][0] != ring[cyc[(i + 1) % 12]][0] for i in range(12)))
X('octet ring: the hole (the missing octahedron) has one face on each of the two planes, so it runs right through the band',
  sorted(sum(v) for v in O0) == [0, 0, 0, 2, 2, 2])
X('octet ring: every piece lies in the layer between the two planes', all(inlayer(vs) for _, vs in ring))
# satellites of the octet band: on the top face (plane x+y+z = 2) of each ring octahedron, the octet's tetrahedron above it
sats = []
for k, vs in ring:
    if k != 'O': continue
    top = frozenset(v for v in vs if sum(v) == 2)
    t = [tv for kk, tv in cand if kk == 'T' and top < tv and max(sum(v) for v in tv) == 4]
    sats.append(t[0] if len(t) == 1 else None)
X('octet band satellites: on each of the 6 octahedra one tetrahedron seated face to face on its top face, apex on the plane '
  'x+y+z = 4, all distinct', len(sats) == 6 and None not in sats and len(set(sats)) == 6)
s1 = 2 ** -0.5                                         # edge 1
def fpoly(vs, k): return np.array(sorted(vs), float) * k
def hull_items(lab, pts, shift=np.zeros(3), edges=True):
    return [(lab, n, poly + shift, edges) for n, o, poly in hull_faces(pts)]
# view basis with the layer normal (1,1,1) as "up"
e3 = np.ones(3) / 3 ** 0.5; e1 = np.array([1, -1, 0]) / 2 ** 0.5; e2 = np.cross(e3, e1); ALIGN = np.array([e1, e2, e3])

# ================= exact claw (icosahedron of edge 1 in its octahedron of edge phi^2/sqrt2) and its satellites =================
h = PHI * PHI / 2
claw = [p for p in H.cell_pieces(O3, 'I') if p[0] in ('I', 'A')]
def tet_on_face(sg):
    """the regular tetrahedron of edge phi^2/sqrt2 standing face to face on the octahedron face in the octant sg: apex h*sg"""
    f = [V(*(h * sg[k] if k == i else 0 for k in range(3))) for i in range(3)]
    return f + [V(*(h * s for s in sg))]
t0 = tet_on_face((1, 1, 1)); d2 = lambda a, b: G.dot(G.sub(a, b), G.sub(a, b))
X('satellite tetrahedron on an octahedron face: all six edges exactly phi^2/sqrt2 (squared phi^4/2), apex (h, h, h)',
  all(d2(a, b) == PHI * PHI * PHI * PHI / 2 for a, b in itertools.combinations(t0, 2)))
# chirality of the earring: the rotations of the claw are those of the pyritohedral group (12); they keep the two tetrahedral
# sets of octahedron faces {+++, +--, -+-, --+} and {-++, +-+, ++-, ---} apart, and the mirror x -> -x exchanges them
rots = [np.array(M) for M in itertools.product(*[[tuple(r) for r in np.vstack([np.eye(3), -np.eye(3)])]] * 3)]
rots = [M for M in rots if abs(abs(np.linalg.det(M)) - 1) < 1e-9 and np.allclose(M @ M.T, np.eye(3))]
ico = np.array([[float(x) for x in v] for v in G.ICO]); keyset = lambda P: set(map(tuple, np.round(P, 9)))
symI = [M for M in rots if np.linalg.det(M) > 0 and keyset(ico @ M.T) == keyset(ico)]
X('claw (octahedron with the icosahedron in Pacioli\'s position): 12 rotations among the 24 of the octahedron keep the icosahedron',
  len(symI) == 12)
setA = keyset(np.array([(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)], float))
X('earrings: those 12 rotations never carry face +++ to face -++, so the earring and its mirror image are a true left and right pair',
  all(tuple(np.round(M @ np.array([1, 1, 1.]), 9)) in setA for M in symI))

# ================= golden-tiling pieces =================
def dogstar(i, j, k=0):
    c = V(i * PHI, j * PHI, k * PHI + HF); negs = []
    for ax in range(3):
        for s in (1, -1):
            d = [0, 0, 0]; d[ax] = s; n = G.add(c, G.mul(PHI, V(*d))); negs.append(Part(H.roof_at(n, ax, -s)))
    return ('S', [Part(G.shift(G.CUBE, c))], negs)
def cell(i, j, kind, k=0): return H.cell_pieces(V(i * PHI, j * PHI, k * PHI + HF), kind)
def golden(spec):
    """spec: {(i, j, k): 'D' | 'I' | 'S'}; cells only where i + j + k is even, Dogstars where odd (Hart's tiling)"""
    out = []
    for (i, j, k), t in spec.items():
        assert ((i + j + k) % 2 == 1) == (t == 'S'), (i, j, k, t)
        out += [dogstar(i, j, k)] if t == 'S' else cell(i, j, t, k)
    return out
def drawn(pieces, zc=None):
    return [p for p in pieces if not (zc is not None and upper_cap(p, zc))]
def compose(panels, cols, path, labels=True, gap=0.0):
    rows = [panels[i:i + cols] for i in range(0, len(panels), cols)]
    cw = W // cols; hs = [max(p.size[1] for p in r) for r in rows]
    im = Image.new('RGB', (W, sum(hs) + int(W * 0.05)), GROUND); y = 0; labs = []
    for r, hh in zip(rows, hs):
        for c, p in enumerate(r):
            im.paste(p, (c * cw + (cw - p.size[0]) // 2, y + (hh - p.size[1]) // 2))
            labs.append((c * cw + int(W * 0.015), y + int(W * 0.01), '(' + 'abcdefgh'[len(labs)] + ')'))
        y += hh
    finish(im, labs if labels and len(panels) > 1 else [], path)
def view(ax0, az, base=np.eye(3)): return rot(0, np.radians(ax0)) @ rot(2, np.radians(az)) @ base

P_ = lambda f: print(f'PROGRESS {f:.2f}', flush=True)
# ---------- 1. ring (core): claw setting on a hoop; full setting with the four upper caps lifted ----------
full = H.cell_pieces(O3, 'I'); C('ring full setting', full, {'I': 1, 'A': 6, 'cap': 8})
Rr = view(-72, -24)
def lift(pc):
    if not upper_cap(pc, 0): return np.zeros(3)
    c = np.mean([[float(x) for x in v] for p in pc[1] for v in p.verts], 0); return np.array([0.45 * np.sign(c[0]), 0.45 * np.sign(c[1]), 1.3])
a = render(items_of(claw) + hoop((0.0, 0.0, -float(h))), Rr, W // 2, Hmax=int(W * 0.62))
b = render(items_of(full, lift), Rr, W // 2, Hmax=int(W * 0.62))
compose([a, b], 2, os.path.join(OUTD, 'ring.png')); P_(0.12)
# ---------- 2. bracelet (core): one grid line D S I S D S I ----------
line = {(i, 0, 0): t for i, t in enumerate('DSISDSI')}
br = golden(line); C('bracelet', br, {'A': 12, 'D': 2, 'I': 2, 'S': 3, 'cap': 16})
Rb = view(-60, -14)
im = render(items_of(drawn(br, float(HF))), Rb, W); compose([im], 1, os.path.join(OUTD, 'bracelet.png')); P_(0.22)
# ---------- 3. brooch (core): 3 x 3 patch of the golden slab with its bottom edging ----------
KIND = {(0, 0): 'D', (2, 0): 'D', (1, 1): 'I', (0, 2): 'D', (2, 2): 'D'}
Pb = H.golden_slab('RZ', R=1, kinds=lambda i, j, k=0: KIND.get((i + 1, j + 1), 'D'))
cz = lambda pc: np.mean([[float(x) for x in v] for p in pc[1] for v in p.verts], 0)
brooch = [pc for pc in Pb if not (pc[0] in ('Z', 'R') and cz(pc)[2] > float(PHI) / 2)]
C('brooch', brooch, {'A': 6, 'D': 4, 'I': 1, 'R': 8, 'S': 4, 'Z': 9, 'cap': 8})
Rc = view(-56, -30)
im = render(items_of(drawn(brooch, float(HF))), Rc, int(W * 0.8)); compose([im], 1, os.path.join(OUTD, 'brooch.png')); P_(0.32)
# ---------- 4. pendant and necklace (core): the icosahedral band (pierced), the golden loop ----------
L = float(h)                                          # octet of edge phi^2/sqrt2: integer point p -> (p - (1,0,0)) * phi^2/2
band = []
for k, vs in ring:
    if k == 'O':
        cI = next(iter(vs)); ctr = tuple(sum(v[i] for v in vs) // 6 for i in range(3))
        c = V(*[(ctr[i] - O0c[i]) * h for i in range(3)])
        band += [p for p in H.cell_pieces(c, 'I') if p[0] in ('I', 'A')]
    else:
        band.append(('gT', [Part([V(*[(v[i] - O0c[i]) * h for i in range(3)]) for v in vs])], []))
C('pendant: icosahedral band', band, {'I': 6, 'A': 36, 'gT': 6})
# necklace: the 16 positions round the edge of a 5 x 5 block of the grid; cells (corners and every other place) alternate D, I
per = [(i, 0) for i in range(4)] + [(4, j) for j in range(4)] + [(i, 4) for i in range(4, 0, -1)] + [(0, j) for j in range(4, 0, -1)]
loop = {}; kk = 0
for (i, j) in per:
    if (i + j) % 2: loop[(i, j, 0)] = 'S'
    else: loop[(i, j, 0)] = 'DI'[kk % 2]; kk += 1
lp = golden(loop); C('necklace: golden loop', lp, {'A': 24, 'D': 4, 'I': 4, 'S': 8, 'cap': 32})
a = render(items_of(band), view(-35, 0, ALIGN), W // 2, Hmax=int(W * 0.5))
b = render(items_of(drawn(lp, float(HF))), view(-40, -20), W // 2, Hmax=int(W * 0.5))
compose([a, b], 2, os.path.join(OUTD, 'band-loop.png')); P_(0.45)
# ---------- 5. earrings: core pair (claws), satellite pair (one tetrahedron each, left and right) ----------
mir = lambda P: [(lab, [Part([V(-v[0], v[1], v[2]) for v in p.verts]) for p in pos], []) for lab, pos, _ in P]
satR = claw + [('T', [Part(t0)], [])]; satL = mir(satR)
C('earring with satellite (one of the pair)', satR, {'I': 1, 'A': 6, 'T': 1})
Re = view(-70, -30)
pairs = []
for P in (claw, mir(claw), satR, satL):
    it = items_of(P) + hoop((0.0, 0.0, float(h) + 0.64), R=0.32, wy=0.12, th=0.05)
    pairs.append(render(it, Re, W // 4, Hmax=int(W * 0.42)))
compose(pairs, 4, os.path.join(OUTD, 'earrings.png')); P_(0.58)
# ---------- 6. variations: stone loop ring, satellite ring (octet band), satellite pendant (stella), satellite necklace ----------
stone_loop = [hull_items(k, fpoly(vs, s1)) for k, vs in ring]
X('stone loop ring: 6 tetrahedra and 6 octahedra of edge 1, whole, face to face', nT == 6 and nO == 6)
gold_band = [hull_items('g' + k, fpoly(vs, s1)) for k, vs in ring] + [hull_items('T', fpoly(t, s1)) for t in sats]
ALT = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]          # one of the two tetrahedral sets of faces
stella = claw + [('T', [Part(tet_on_face(sg))], []) for sg in ALT]
C('satellite pendant (four tetrahedra on alternate faces)', stella, {'I': 1, 'A': 6, 'T': 4})
apex = [V(*(h * s for s in sg)) for sg in ALT]
X('pendant: the octahedron with tetrahedra on four alternate faces is the regular tetrahedron of edge 2 phi^2/sqrt2 '
  '(apexes pairwise at squared distance 2 phi^4; volume of octahedron + 4 tetrahedra = volume of that tetrahedron)',
  all(d2(a, b) == 2 * PHI * PHI * PHI * PHI for a, b in itertools.combinations(apex, 2))
  and G.volume(G.OCT) + 4 * G.volume(t0) == G.volume(apex))
out_of = lambda i, j: (i, -1) if j == 0 else (5, j) if i == 4 else (i, 5) if j == 4 else (-1, j)
loopS = dict(loop); loopS.update({(*out_of(i, j), 0): 'D' for (i, j, k), t in loop.items() if t == 'S'})
lpS = golden(loopS); C('satellite necklace', lpS, {'A': 24, 'D': 12, 'I': 4, 'S': 8, 'cap': 32})
q = W // 2
a = render([x for g in stone_loop for x in g], view(-35, 0, ALIGN), q, Hmax=int(W * 0.42))
b = render([x for g in gold_band for x in g], view(-35, 0, ALIGN), q, Hmax=int(W * 0.42))
c = render(items_of(stella), view(-62, 18), q, Hmax=int(W * 0.42))
d = render(items_of(drawn(lpS, float(HF))), view(-40, -20), q, Hmax=int(W * 0.42))
compose([a, b, c, d], 2, os.path.join(OUTD, 'variations.png')); P_(0.78)
# ---------- 7. satellite bracelet and satellite brooch ----------
lineS = dict(line); lineS.update({(i, s, 0): 'D' for i in (1, 3, 5) for s in (1, -1)})
brS = golden(lineS); C('satellite bracelet', brS, {'A': 12, 'D': 8, 'I': 2, 'S': 3, 'cap': 16})
broochS = brooch + [p for (i, j) in [(0, -1), (-1, 0), (1, 0), (0, 1)] for p in cell(i, j, 'D', 1)]
C('satellite brooch', broochS, {'A': 6, 'D': 8, 'I': 1, 'R': 8, 'S': 4, 'Z': 9, 'cap': 8})
a = render(items_of(drawn(brS, float(HF))), view(-60, -14), W, Hmax=int(W * 0.45))
b = render(items_of(drawn(broochS, float(HF))), Rc, int(W * 0.7), Hmax=int(W * 0.6))
compose([a, b], 1, os.path.join(OUTD, 'satellites.png')); P_(0.95)
allp = full + br + brooch + band + lp + satR + stella + lpS + brS + broochS
X('every drawn piece has faces', all(len(piece_faces(pc)) > 0 for pc in allp))
print('FINAL ok' if not FAIL else 'FINAL FAIL: ' + '; '.join(FAIL))
