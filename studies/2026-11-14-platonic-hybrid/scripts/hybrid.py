# hybrid.py (14 Nov 2026) - DICTO · dictospheres.com
# Tests the "hybrid" construction for the Platonic mixes, proposed in DICTO's working session of 13-14 November 2026
# (handoff 03-session-addendum, section B, B1-B6, marked "derived; to test"), against #47 (Every Mix of the Platonic Solids
# Fills Space, v3) and #106 (One World for the Platonic Solids). Every claim gets CONFIRMED / REFUTED / UNDECIDED.
#   E  exact facts in Q(sqrt5): edges, containments, roof height 1/2, volumes (cap, Admiral Cap, roof R, plate Z), ridges.
#   X  exact covering tests: random points with rational coordinates (denominator QD), every point must lie in exactly one
#      piece (exact sign tests; points on a boundary are counted apart and skipped), each slab tested in its own frame:
#      golden slab (hybrid, edging X/Y), golden slab (hybrid, edging R/Z), the golden 3D tiling (D + I, no edging),
#      one octet layer cut on its triangle planes; negative controls (wrong edgings, skin without caps) must FAIL.
#   S  float test through the whole stack as mixes3.py does (golden slab + cube slab + octet layer, 40 000 points), and the
#      positive control: #47's own mixes3.py run from its file on all 31 mixes.
#   K  connector counts (B5) by construction.
# Usage: hybrid.py pilot|full [workers]   -> PROGRESS lines, FINAL ok / FINAL FAIL
import sys, os, time, random, itertools, json
from fractions import Fraction as F
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import golden as G
from golden import Q5, V, add, sub, mul, dot, PHI, HF, HALF, PHI2, Part
MODE = sys.argv[1] if len(sys.argv) > 1 else 'pilot'; WORKERS = int(sys.argv[2]) if len(sys.argv) > 2 else 4
NPTS = {'pilot': 600, 'full': 60000}[MODE]; NNEG = {'pilot': 300, 'full': 5000}[MODE]
QD = 1000003                                  # prime denominator of the random points
T0 = time.time(); FAILS = []; RESULTS = {}
def prog(f, what): print(f'PROGRESS {f:.2f} {what} ({time.time() - T0:.0f} s)', flush=True)
def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + (': ' + str(detail) if detail != '' else ''), flush=True)
    RESULTS[name] = (bool(ok), str(detail))
    if not ok: FAILS.append(name)

# ================= E: exact facts =================
def d2(u, v): w = sub(u, v); return dot(w, w)
def exact_facts():
    DOD, ICO, OCT, CUBE = G.DOD, G.ICO, G.OCT, G.CUBE
    e = [(a, b) for a, b in itertools.combinations(DOD, 2) if d2(a, b) == 1]
    check('E1 dodecahedron: 20 corners, 30 edges of length exactly 1, min distance 1',
          len(DOD) == 20 and len(e) == 30 and all(d2(a, b) >= 1 for a, b in itertools.combinations(DOD, 2)), f'{len(e)} edges')
    vD = G.volume(DOD); vC = PHI * PHI * PHI; vR = G.volume(G.ROOFS[(2, 1)])
    check('E2 roof R: volume (7 + 3 sqrt5)/24, cube + 6 roofs = dodecahedron', vR == Q5(F(7, 24), F(3, 24)) and vC + 6 * vR == vD, vR)
    top = G.ROOFS[(2, 1)]; hz = max(v[2] for v in top) - HF
    ridge = [v for v in top if v[2] == PHI2 / 2]
    check('B4(b) roof height exactly 1/2 (phi^2/2 - phi/2), ridge of length 1 along y, base = the whole face',
          hz == HALF and len(ridge) == 2 and d2(*ridge) == 1 and ridge[0][0] == 0 and ridge[1][0] == 0
          and sorted(float(v[2]) for v in top)[:4] == [float(HF)] * 4, hz)
    ei = [(a, b) for a, b in itertools.combinations(ICO, 2) if d2(a, b) == 1]
    check('E3 icosahedron (Pacioli): 12 corners, 30 edges of length exactly 1', len(ICO) == 12 and len(ei) == 30)
    # corners on the octahedron's edges, golden section
    gs = True
    for p in ICO:
        on = [(a, b) for a, b in itertools.combinations(OCT, 2) if dot(a, b) == 0          # an edge: two non-opposite corners
              and G.iszero(G.cross(sub(p, a), sub(b, a))) and dot(sub(p, a), sub(p, b)) < 0]
        if len(on) != 1: gs = False; continue
        a, b = on[0]; r = d2(p, a) / d2(p, b)
        if not (r == PHI2 or r == 1 / PHI2): gs = False
    check('E4 every icosahedron corner lies on one octahedron edge, dividing it in the golden ratio', gs)
    mids = [mul(HALF, add(*[v for v in G.RIDGE if v[ax] == s * PHI2 / 2])) for ax in range(3) for s in (1, -1)]
    check('E5 octahedron corners = the 6 roof-ridge midpoints of the dodecahedron', sorted(map(repr, mids)) == sorted(map(repr, OCT)))
    PD = G.planes_from_vertices(DOD)
    check('E6 octahedron inside the dodecahedron; icosahedron inside the octahedron and inside Euclid\'s cube (|x_i| <= phi/2)',
          all(dot(n, v) <= c for n, c in PD for v in OCT)
          and all(dot(n, v) <= c for n, c in G.planes_from_vertices(OCT) for v in ICO)
          and all(abs(float(x)) <= float(HF) + 1e-15 and (x <= HF and -x <= HF) for v in ICO for x in v))
    vI, vO = G.volume(ICO), G.volume(OCT)
    A = G.admiral_caps(); vA = [G.volume(t[0]) + G.volume(t[1]) for t in A]
    check('E7 Admiral Caps: 6 pieces of 2 tetrahedra, each of volume phi/12; icosahedron + 6 A = octahedron (exact)',
          all(x == PHI / 12 for x in vA) and vI + sum(vA, Q5()) == vO, vA[0])
    caps = G.caps8(); vc = [G.volume(vs) for s, vs in caps]
    # congruence: cap(s) = (sign change s) applied to cap(+++)
    c0 = caps[0][1]; cong = all(sorted(map(repr, vs)) == sorted(map(repr, [tuple(x * k for x, k in zip(v, s)) for v in c0])) for s, vs in caps)
    check('E8 caps: 8 convex caps, each (27 + 13 sqrt5)/96, images of one cap under the sign changes (symmetries of the cell); '
          'icosahedron + 6 A + 8 caps = dodecahedron (exact volumes)',
          all(x == Q5(F(27, 96), F(13, 96)) for x in vc) and cong and vI + sum(vA, Q5()) + sum(vc, Q5()) == vD, vc[0])
    vZ = PHI * PHI / 2 - vR
    check('B4(c) plate Z = box phi x phi x 1/2 minus R: volume phi^2/2 - (7 + 3 sqrt5)/24 = (11 + 3 sqrt5)/24',
          vZ == Q5(F(11, 24), F(3, 24)), vZ)
    vS = vC - 6 * vR
    check('E9 Dogstar S = cube - 6 roofs = phi/2 (#47 Table 1)', vS == PHI / 2, vS)
    return dict(vD=vD, vR=vR, vZ=vZ, vI=vI, vO=vO, vA=vA[0], vcap=vc[0], vS=vS)

# ================= pieces of the golden slab =================
def cellc(i, j, k=0): return V(i * PHI, j * PHI, k * PHI + HF)      # centre of the cube (i, j, k); middle layer z in [0, phi]
def is_cell(i, j, k=0): return (i + j + k) % 2 == 0
def kind_of(i, j, k=0):
    """mixed cells: dodecahedron D or skinned icosahedron I by a fixed hash (both occur in every window)"""
    return 'D' if (i * 7 + j * 13 + k * 5 + (i * j) % 3) % 3 else 'I'
CAPS = None
def cell_pieces(c, kind, nocaps=False):
    global CAPS
    if kind == 'D': return [('D', [Part(G.shift(G.DOD, c))], [])]
    if CAPS is None: CAPS = G.caps8()
    out = [('I', [Part(G.shift(G.ICO, c))], [])]
    out += [('A', [Part(G.shift(t, c)) for t in a], []) for a in G.admiral_caps()]
    if not nocaps: out += [('cap', [Part(G.shift(vs, c))], []) for s, vs in CAPS]
    return out
def roof_at(c, ax, s): return G.shift(G.ROOFS[(ax, s)], c)
def box(lo, hi): return [V(*p) for p in itertools.product(*[(lo[i], hi[i]) for i in range(3)])]
def golden_slab(edging, R=3, kinds='mixed', neg=None):
    """edging 'XY' (#47 Lemma 5: outer layers of cubes of edge phi, X / Y), 'RZ' (B4: roof R + plate Z), or '3D' (the whole
    golden tiling, cells on i+j+k even, no edging). neg = None or the name of a deliberate fault (negative control)."""
    if isinstance(kinds, str): kinds = {'mixed': kind_of, 'I': lambda *a: 'I', 'D': lambda *a: 'D'}[kinds]
    P = []; ks = range(-1, 2) if edging == '3D' else [0]
    for i, j, k in itertools.product(range(-R, R + 1), range(-R, R + 1), ks):
        c = cellc(i, j, k)
        if is_cell(i, j, k):
            P += cell_pieces(c, kinds(i, j, k), nocaps=(neg == 'skin-without-caps'))
        else:                                  # Dogstar: cube minus the roofs poking in from the 6 neighbour positions
            negs = []
            for ax in range(3):
                for s in (1, -1):
                    d = [0, 0, 0]; d[ax] = s; n = add(c, mul(PHI, V(*d)))
                    negs.append(Part(roof_at(n, ax, -s)))     # the neighbour's roof on the shared face
            P.append(('S', [Part(G.shift(G.CUBE, c))], negs))
        if edging == 'XY':
            for s in (1, -1):                  # outer cube above (s=1) / below (s=-1)
                oc = add(c, V(0, 0, s * PHI))
                if is_cell(i, j):
                    if neg == 'X-Y-swapped': P.append(('Y', [Part(G.shift(G.CUBE, oc)), Part(roof_at(oc, 2, -s))], []))
                    else: P.append(('X', [Part(G.shift(G.CUBE, oc))], [Part(roof_at(c, 2, s))]))
                else:
                    if neg == 'X-Y-swapped': P.append(('X', [Part(G.shift(G.CUBE, oc))], [Part(roof_at(c, 2, s))]))
                    else: P.append(('Y', [Part(G.shift(G.CUBE, oc)), Part(roof_at(oc, 2, -s))], []))
        if edging == 'RZ':
            for s in (1, -1):
                zb = (PHI if s == 1 else -HALF); zt = (PHI + HALF if s == 1 else Q5(0))
                bx = box(V(c[0] - HF, c[1] - HF, zb), V(c[0] + HF, c[1] + HF, zt))
                if is_cell(i, j):              # column over a cell: one Z, hollow towards the cell, over its roof
                    rf = roof_at(c, 2, s)
                    if neg == 'Z-turned':      # the plate's hollow turned a quarter turn: ridge across the cell's ridge
                        rf = G.shift([G.rot_z90(sub(v, c)) for v in rf], c)
                    P.append(('Z', [Part(bx)], [Part(rf)]))
                else:                          # column over a Dogstar: R in its hollow, then Z + R (a full plate)
                    oc = add(c, V(0, 0, s * PHI))
                    if neg != 'no-R-in-hollow' or s == -1:
                        P.append(('R', [Part(roof_at(oc, 2, -s))], []))
                    r2 = G.shift(roof_at(oc, 2, -s), V(0, 0, s * HALF))   # same roof, one plate higher: base on the plate's far face
                    P.append(('Z', [Part(bx)], [Part(r2)]))
                    P.append(('R', [Part(r2)], []))
    return P
def slab_range(edging):
    if edging == 'XY': return -PHI, 2 * PHI
    if edging == 'RZ': return -HALF, PHI + HALF
    return HALF - PHI, 2 * PHI - HALF        # '3D': inside the three layers built, clear of the roofs of cells not built
# ================= octet layer on triangle planes (frame scaled by sqrt2: corners = integer points of even sum) =========
def octet_layer(R=4):
    P = []; rng = range(-R, R + 1)
    for x, y, z in itertools.product(rng, rng, rng):
        if (x + y + z) % 2 and x + y + z == 1:      # octahedra between the planes x+y+z = 0 and 2
            c = (x, y, z); vs = [V(*[c[i] + (d if i == a else 0) for i in range(3)]) for a in range(3) for d in (1, -1)]
            P.append(('O', [Part(vs)], []))
        even = [V(x + i, y + j, z + k) for i in (0, 1) for j in (0, 1) for k in (0, 1) if (x + i + y + j + z + k) % 2 == 0]
        sums = sorted(int(sum(float(t) for t in v)) for v in even)
        if sums[0] >= 0 and sums[-1] <= 2: P.append(('T', [Part(even)], []))
    return P

# ================= exact covering test (parallel over point chunks) =================
JOB = {}
def member(piece, Pi, fp):
    lab, pos, negs = piece; hit = None
    for p in pos:
        t = p.test(Pi, QD, fp)
        if t is None: return None
        if t: hit = True; break
    if not hit: return 0
    for p in negs:
        t = p.test(Pi, QD, fp)
        if t is None: return None
        if t: return 0
    return 1
def init(name, kw):
    JOB['name'] = name
    if name == 'octet':
        JOB['P'] = octet_layer()
    else:
        JOB['P'] = golden_slab(**kw)
    # bucket pieces by float bbox in a grid for speed
    B = {}
    for pc in JOB['P']:
        lo = [min(p.lo[i] for p in pc[1]) for i in range(3)]; hi = [max(p.hi[i] for p in pc[1]) for i in range(3)]
        for gx in range(int(lo[0] // 1) - 1, int(hi[0] // 1) + 1):
            for gy in range(int(lo[1] // 1) - 1, int(hi[1] // 1) + 1):
                B.setdefault((gx, gy), []).append(pc)
    JOB['B'] = B
def run_points(args):
    name, kw, seed, n = args
    if JOB.get('name') != name or JOB.get('kw') != kw: init(name, kw); JOB['kw'] = kw
    rnd = random.Random(seed); bad = 0; ties = 0; kinds = {}; examples = []
    if name == 'octet':
        lo, hi = (-2, -2, -2), (2, 2, 2)
    else:
        e = kw['edging']; z0, z1 = slab_range(e)
        lo = (-1.6 * float(PHI), -1.6 * float(PHI), float(z0)); hi = (1.6 * float(PHI), 1.6 * float(PHI), float(z1))
    done = 0
    while done < n:
        Pi = tuple(rnd.randint(int(lo[i] * QD) + 1, int(hi[i] * QD) - 1) for i in range(3))
        if name == 'octet':
            s = sum(Pi)
            if not (0 < s < 2 * QD): continue
        else:
            zq = F(Pi[2], QD)
            if not (z0 < Q5(zq) < z1): continue
        fp = tuple(x / QD for x in Pi)
        cand = JOB['B'].get((int(fp[0] // 1), int(fp[1] // 1)), [])
        cnt = 0; labs = []; tie = False
        for pc in cand:
            m = member(pc, Pi, fp)
            if m is None: tie = True; break
            if m: cnt += 1; labs.append(pc[0])
        done += 1
        if tie: ties += 1; continue
        for l in labs: kinds[l] = kinds.get(l, 0) + 1
        if cnt != 1:
            bad += 1
            if len(examples) < 3: examples.append((fp, cnt, labs))
    return bad, ties, kinds, examples
def cover(name, kw, n, pool, expect_ok=True):
    chunks = max(1, min(WORKERS * 2, n // 50)); per = n // chunks
    res = pool.map(run_points, [(name, kw, 1000 + k, per) for k in range(chunks)])
    bad = sum(r[0] for r in res); ties = sum(r[1] for r in res); kinds = {}
    for r in res:
        for k, v in r[2].items(): kinds[k] = kinds.get(k, 0) + v
    ex = [e for r in res for e in r[3]][:2]
    tested = per * chunks - ties
    return bad, ties, tested, dict(sorted(kinds.items())), ex

# ================= S: float stack test (as mixes3.py) =================
def float_stack(n=40000, neg=None):
    import numpy as np
    sys.path.insert(0, STEP1)
    from mixes2 import octet_pieces, RZ
    phi = float(PHI); rng = np.random.default_rng(7)
    golden = golden_slab('RZ', R=3, neg=neg)
    zG = phi * phi                                 # golden slab: z in [0, phi^2] (shifted up by 1/2)
    zC = zG + 1.0; zT = zC + (2 / 3) ** 0.5        # cube slab of thickness 1, then one octet layer on triangle planes
    def fl(part, dz): return [[float(x) for x in v] for v in part.verts], dz
    from scipy.spatial import ConvexHull
    def planes(Vs):
        Vs = np.asarray(Vs, float); h = ConvexHull(Vs); return h.equations[:, :3], -h.equations[:, 3]
    pieces = []   # (label, [pos (n,o)], [neg (n,o)])
    for lab, pos, negs in golden:
        sh = np.array([0, 0, 0.5])
        pieces.append((lab, [planes(np.array([[float(x) for x in v] for v in p.verts]) + sh) for p in pos],
                       [planes(np.array([[float(x) for x in v] for v in p.verts]) + sh) for p in negs]))
    for i, j in itertools.product(range(-4, 4), range(-4, 4)):
        pieces.append(('C', [planes(np.array(list(itertools.product((0, 1), repeat=3)), float) + np.array([i, j, zG]))], []))
    for k, Vs, c in octet_pieces(1.0, 5):
        Vv = np.array(Vs) @ RZ.T; m = Vv[:, 2].mean()
        if 0 < m < (2 / 3) ** 0.5: pieces.append((k, [planes(Vv + np.array([0, 0, zC]))], []))
    X = np.column_stack([rng.uniform(-2, 2, n), rng.uniform(-2, 2, n), rng.uniform(0.001, zT - 0.001, n)])
    cnt = np.zeros(n, int); kinds = set()
    def inside(pl): nrm, o = pl; return np.all(X @ nrm.T < o - 1e-9, axis=1)
    for lab, pos, negs in pieces:
        a = np.zeros(n, bool)
        for pl in pos: a |= inside(pl)
        for pl in negs: a &= ~(np.all(X @ pl[0].T < pl[1] + 1e-9, axis=1))
        if a.any(): kinds.add(lab)
        cnt += a
    bad = int((cnt != 1).sum())
    return bad, sorted(kinds), round(zT, 4)
STEP1 = os.path.normpath(os.path.join(HERE, '..', '..', '2026-10-22-platonic-mix-step1'))
def mixes3_control():
    """#47's own check, run from its file (not retyped): all 31 mixes"""
    sys.path.insert(0, STEP1); cwd = os.getcwd(); os.chdir(STEP1)
    import mixes3
    os.chdir(cwd); out = []
    for r in range(1, 6):
        for m in itertools.combinations('DICTO', r):
            k, bad, ov, top = mixes3.check(set(m), N=40000 if MODE == 'full' else 4000)
            out.append((''.join(m), bad, ov))
    return out

# ================= K: connector counts =================
def connectors(mix, construction):
    """connectors used by one construction for one mix (a set of letters from DICTO)."""
    m = set(mix); out = set(); worlds = 0
    golden = m & {'D', 'I'}; seam = bool(m - {'D', 'I'})
    if construction == 'published':                      # #47 v3 Theorem 1
        if 'D' in m: out |= {'S', 'X', 'Y'}; worlds += 1
        if 'I' in m: out |= {'A', "Q'"}; worlds += 1
        if 'C' in m: worlds += 1
        if m & {'T', 'O'}:
            worlds += 1; out |= {'P'}
            if 'T' not in m: out |= {'Q'}
    else:
        tri = construction in ('triangle', 'hybrid', 'hybrid-RZ')
        hyb = construction in ('hybrid', 'hybrid-RZ')
        if hyb and golden:
            worlds += 1; out |= {'S'}
            if 'I' in m: out |= {'A', 'cap'}
            if seam: out |= ({'R', 'Z'} if construction == 'hybrid-RZ' else {'X', 'Y'})
        else:
            if 'D' in m: out |= {'S', 'X', 'Y'}; worlds += 1
            if 'I' in m: out |= {'A', "Q'"}; worlds += 1
        if 'C' in m: worlds += 1
        if m & {'T', 'O'}:
            worlds += 1
            if not tri: out |= {'P'}
            if 'O' not in m: out |= {'P'}                # an octahedron of the layer cut into two half octahedra
            if 'T' not in m: out |= {'Q'}                # a tetrahedron cut into four face pyramids
    return worlds, sorted(out)

# ================= main =================
if __name__ == '__main__':
    print(f'hybrid.py {MODE}, workers {WORKERS}, exact points per configuration {NPTS} (negative controls {NNEG})', flush=True)
    prog(0.02, 'start')
    vols = exact_facts(); prog(0.10, 'exact facts')
    # B4(a): ridges on the slab face: every cell's top roof and every Dogstar's top hollow, in a 7 x 7 window
    dirs = set()
    for i, j in itertools.product(range(-3, 4), range(-3, 4)):
        c = cellc(i, j)
        rf = roof_at(c, 2, 1) if is_cell(i, j) else roof_at(add(c, V(0, 0, PHI)), 2, -1)
        far = max(v[2] for v in rf) if is_cell(i, j) else min(v[2] for v in rf)   # the ridge: the roof's corners off its base
        rd = [v for v in rf if v[2] == far]
        d = sub(rd[0], rd[1]); dirs.add(tuple(abs(float(x)) for x in d))
    check('B4(a) every roof standing out of the slab face and every roof-shaped hollow has its ridge along the same line '
          '(y), 49 columns', dirs == {(0.0, 1.0, 0.0)}, sorted(dirs))
    prog(0.15, 'ridges')
    with Pool(WORKERS) as pool:
        tests = [
            ('B2 hybrid golden slab, edging X/Y (#47 Lemma 5), cells mixed D and skinned I', 'gold', dict(edging='XY'), True),
            ('B4(d) hybrid golden slab, edging R/Z (partial skins), cells mixed D and skinned I', 'gold', dict(edging='RZ'), True),
            ('B4(d) hybrid golden slab, edging R/Z, all cells skinned icosahedra (mix without D)', 'gold', dict(edging='RZ', kinds='allI'), True),
            ('B5 golden tiling in 3D (no edging), cells mixed D and skinned I', 'gold', dict(edging='3D'), True),
            ('B3 one octet layer between two triangle planes, whole T and O', 'octet', {}, True),
            ('CONTROL+ #47 Lemma 5 slab, dodecahedra only (edging X/Y)', 'gold', dict(edging='XY', kinds='allD'), True),
            ('CONTROL- plate hollow turned a quarter turn', 'gold', dict(edging='RZ', neg='Z-turned'), False),
            ('CONTROL- no R in the Dogstar hollows (top face)', 'gold', dict(edging='RZ', neg='no-R-in-hollow'), False),
            ('CONTROL- X and Y swapped', 'gold', dict(edging='XY', neg='X-Y-swapped'), False),
            ('CONTROL- icosahedron skin without its 8 caps', 'gold', dict(edging='RZ', neg='skin-without-caps'), False),
        ]
        for t, (name, kind, kw, want) in enumerate(tests):
            kw2 = dict(kw)
            n = NPTS if want else NNEG
            if kind == 'gold':
                kk = kw.get('kinds')
                kw2['kinds'] = {'allI': 'I', 'allD': 'D'}.get(kk, 'mixed')
            bad, ties, tested, kinds, ex = cover('octet' if kind == 'octet' else 'gold', kw2, n, pool)
            if want:
                check(name, bad == 0 and tested > 0.99 * n, f'{tested} points, {bad} not covered once, {ties} on a boundary; pieces hit {kinds}')
            else:
                check(name + ' (must fail)', bad > 0, f'{tested} points, {bad} not covered once (detected){"; e.g. " + str(ex[0]) if ex else ""}')
            prog(0.15 + 0.6 * (t + 1) / len(tests), name[:40])
    bad, kinds, top = float_stack()
    check('B4(d)/B5 float stack (as mixes3.py): golden slab R/Z + cube slab + octet layer on triangle planes, 40 000 points',
          bad == 0 and set(kinds) >= {'D', 'I', 'C', 'T', 'O', 'A', 'cap', 'S', 'R', 'Z'} and not set(kinds) & {'P', 'Q', "Q'", 'X', 'Y'},
          f'{bad} not covered once; pieces {kinds}; stack height {top}')
    bad, kinds, top = float_stack(neg='Z-turned')
    check('CONTROL- float stack with the plate hollow turned (must fail)', bad > 0, f'{bad} not covered once')
    prog(0.85, 'float stack')
    m3 = mixes3_control()
    check('CONTROL+ #47 published construction (mixes3.py run from its file): all 31 mixes covered once, no D overlaps',
          all(b == 0 and o == 0 for _, b, o in m3), f'{sum(1 for _, b, o in m3 if b == 0 and o == 0)}/31 mixes pass')
    prog(0.95, 'mixes3 control')
    rows = {}
    for c in ('published', 'triangle', 'hybrid', 'hybrid-RZ'):
        rows[c] = connectors('DICTO', c)
        print(f'K all five, {c}: {rows[c][0]} worlds, connectors {rows[c][1]} ({len(rows[c][1])})')
    check('B5 all five: #47 published 4 worlds, P Q\' A S X Y (6)', rows['published'] == (4, sorted(['P', "Q'", 'A', 'S', 'X', 'Y'])))
    check('B5 all five: octet on triangle planes 4 worlds, Q\' A S X Y (5)', rows['triangle'] == (4, sorted(["Q'", 'A', 'S', 'X', 'Y'])))
    check('B5 all five: hybrid 3 worlds, A cap S X Y (5)', rows['hybrid'] == (3, sorted(['A', 'cap', 'S', 'X', 'Y'])))
    check('B5 all five: hybrid with partial skins 3 worlds, A cap S R Z (5)', rows['hybrid-RZ'] == (3, sorted(['A', 'cap', 'S', 'R', 'Z'])))
    di = connectors('DI', 'hybrid-RZ'); dip = connectors('DI', 'published')
    check('B5 D + I: hybrid 1 world, A cap S (3), against #47 A Q\' S X Y (5)',
          di == (1, sorted(['A', 'cap', 'S'])) and dip[1] == sorted(['A', "Q'", 'S', 'X', 'Y']), f'{di} vs {dip}')
    # every mix: best count over the constructions, and the kit for all 31
    best = {}; kit = set()
    for r in range(1, 6):
        for m in itertools.combinations('DICTO', r):
            opts = {c: connectors(m, c) for c in ('published', 'triangle', 'hybrid', 'hybrid-RZ')}
            c = min(opts, key=lambda c: (len(opts[c][1]), opts[c][0]))
            best[''.join(m)] = (c, opts[c]); kit |= set(connectors(m, 'hybrid-RZ')[1])
            print(f'K {"".join(m):6s}', '  '.join(f'{c}: {len(v[1])} {",".join(v[1]) or "-"}' for c, v in opts.items()))
    print('K kit serving all 31 mixes with the hybrid (partial skins) and triangle-plane octet:', sorted(kit), len(kit))
    json.dump({'results': RESULTS, 'volumes': {k: repr(v) for k, v in vols.items()}, 'best': best, 'kit31': sorted(kit)},
              open(os.path.join(HERE, '..', 'data', f'hybrid-{MODE}.json'), 'w'), indent=1)
    prog(0.99, 'counts')
    print(f'{len(RESULTS) - len(FAILS)}/{len(RESULTS)} checks pass, {time.time() - T0:.0f} s')
    print('FINAL ok' if not FAILS else 'FINAL FAIL: ' + '; '.join(FAILS))
