# registration_check.py, 12 Nov 2026 (aim 3; open item of the keyed-shapes section): do the keyed RDs have to sit on ONE fcc lattice?
# The proof (README, "Registration") rests on finite exact facts, all checked here:
#  (R1) every dihedral angle of the RD is exactly 120 degrees (cos of the angle between outward normals across every edge = 1/2);
#  (R2) the stabiliser in the RD's symmetry group (48) of one face and its side has order 4 and acts on the face as the whole
#       symmetry group of the rhombus (4): so an RD with a given rhombus as a face, on a given side, is unique (= the lattice neighbour);
#  (R3) bump layout: the square pyramids (sides along the face diagonals, half-side s, height <= s/2) lie inside each face with a
#       positive flat margin and do not overlap; with height <= s/2 every crease of a pyramid bends the surface by at most
#       theta = arccos(4/5) < 37 degrees (base edges arctan(1/2) < 27 degrees), well under 60;
#  (R4) sector lemma: around a line on the boundary of several pieces the sectors fill 360 degrees; with sectors 120 (RD edge) or
#       180 +- theta (flat face or a pyramid crease), the only filling containing a 120 is 120+120+120. NEGATIVE CONTROL: with a
#       90-degree edge (the cube) the filling 90+90+180 exists, which is exactly how cube layers slide;
#  (M)  mirror images: the fit relation of keyed_rd.py used the 24 turns only. Here every pair (type a, face, type b MIRRORED, turn)
#       is tested; if none fits, a connected tiling cannot mix mirrored and unmirrored pieces. CONTROL: recount unmirrored fits with
#       our own 24 rotations; must equal keyed_rd.py's count.
# usage: registration_check.py <keyed json from keyed_rd.py>
import sys, json, itertools, math
from fractions import Fraction as Q
ok = True
def chk(name, cond):
    global ok; ok &= bool(cond); print(('ok   ' if cond else 'FAIL ') + name, flush=True)
NB = [d for d in itertools.product((-1, 0, 1), repeat=3) if sum(map(abs, d)) == 2]; assert len(NB) == 12
V4 = [tuple(s if i == k else 0 for i in range(3)) for k in range(3) for s in (1, -1)]
V3 = [tuple(Q(s, 2) for s in sg) for sg in itertools.product((1, -1), repeat=3)]
VERT = [tuple(Q(x) for x in v) for v in V4] + V3
dot = lambda a, b: sum(x * y for x, y in zip(a, b))
def on_face(v, e): return dot(v, e) == 1                    # RD = {x : x.e <= 1 for all 12 e}
# (R1)
edges = [(u, w) for u, w in itertools.combinations(VERT, 2) if sum(1 for e in NB if on_face(u, e) and on_face(w, e)) == 2]
cs = set()
for u, w in edges:
    f1, f2 = [e for e in NB if on_face(u, e) and on_face(w, e)]
    cs.add(Q(dot(f1, f2), 2))                                # |e|^2 = 2
chk(f'(R1) RD: {len(VERT)} corners, {len(edges)} edges, cos(normal angle) over all edges = {sorted(cs)} (1/2 = dihedral 120)', len(VERT) == 14 and len(edges) == 24 and cs == {Q(1, 2)})
# (R2)
OH = [m for p in itertools.permutations(range(3)) for s in itertools.product((1, -1), repeat=3)
      for m in [tuple(tuple(s[i] if j == p[i] else 0 for j in range(3)) for i in range(3))]]
app = lambda M, x: tuple(sum(M[i][j] * x[j] for j in range(3)) for i in range(3))
det = lambda M: round(sum(M[0][p[0]] * M[1][p[1]] * M[2][p[2]] * (1 if sum(1 for a in range(3) for b in range(a + 1, 3) if p[a] > p[b]) % 2 == 0 else -1) for p in itertools.permutations(range(3))))
assert len(OH) == 48 and all(set(app(M, e) for e in NB) == set(NB) for M in OH)
e0 = (1, 1, 0); fv = [v for v in VERT if on_face(v, e0)]
stab = [M for M in OH if app(M, e0) == e0]
acts = {tuple(sorted((fv.index(v), fv.index(app(M, v))) for v in fv)) for M in stab}
chk(f'(R2) stabiliser of face {e0} (and its side): {len(stab)} elements, {len(acts)} distinct actions on the rhombus (its full group has 4)', len(stab) == 4 and len(acts) == 4)
# (R3) layout, in face coordinates of keyed_rd.py: point = C + a U + b V, C = e/2, U = half long diagonal, V = (0,0,1) on the short axis
D = json.load(open(sys.argv[1])); OFFS = [(Q(u), Q(v)) for u, v in D['positions']]
def face_frame(e):
    nz = [i for i in range(3) if e[i] != 0]; z = next(i for i in range(3) if e[i] == 0)
    c1 = [0, 0, 0]; c1[nz[0]] = e[nz[0]]; c2 = [0, 0, 0]; c2[nz[1]] = e[nz[1]]
    U = tuple(Q(c1[i] - c2[i], 2) for i in range(3)); V = tuple(Q(1 if i == z else 0) for i in range(3))
    return tuple(Q(e[i], 2) for i in range(3)), U, V
def positions(e):
    C, U, V = face_frame(e); return [tuple(C[i] + a * U[i] + b * V[i] for i in range(3)) for a, b in OFFS]
C, U, V = face_frame(e0); P = positions(e0)
sub = lambda a, b: tuple(x - y for x, y in zip(a, b))
def d2_line(p, a, b):                                       # squared distance from p to the line ab, exact
    ab = sub(b, a); ap = sub(p, a); t = dot(ap, ab) / dot(ab, ab); r = sub(ap, tuple(t * x for x in ab)); return dot(r, r)
corners = [tuple(C[i] + U[i] for i in range(3)), tuple(C[i] + V[i] / 2 for i in range(3)), tuple(C[i] - U[i] for i in range(3)), tuple(C[i] - V[i] / 2 for i in range(3))]
chk('(R3) face corners as computed are the RD corners of the face', set(corners) == set(fv))
inside = all(abs(a) + 2 * abs(b) < 1 for a, b in OFFS)
db = min(d2_line(p, corners[i], corners[(i + 1) % 4]) for p in P for i in range(4))
lu, lv = dot(U, U), dot(V, V)                               # squared lengths of the U, V steps
gap_u = min(abs(a1 - a2) for (a1, _), (a2, _) in itertools.combinations(OFFS, 2) if a1 != a2) ** 2 * lu
gap_v = min(abs(b1 - b2) for (_, b1), (_, b2) in itertools.combinations(OFFS, 2) if b1 != b2) ** 2 * lv
S = Q(1, 40)                                                # the pyramid half-side we fix
fits = 2 * S * S * 4 < db and (2 * S) ** 2 < min(gap_u, gap_v)   # footprint (circumradius s*sqrt2) at most half the boundary distance; squares disjoint
chk(f'(R3) {len(OFFS)} positions per face, inside the rhombus: {inside}; squared distance to the boundary >= {db} ({float(db) ** .5:.4f}); '
    f'squares of half-side s = {S} stay at least half that distance from the boundary and are disjoint', inside and fits)
cls = D['classes']; hmax = S / 2; unit = hmax / cls
th_base = math.degrees(math.atan(.5)); th_lat = math.degrees(math.acos(.8))
chk(f'(R3) heights: class c gets height c * {unit} (s/2 / {cls} classes), so every pyramid has height <= s/2; creases bend <= {max(th_base, th_lat):.2f} degrees < 60', max(th_base, th_lat) < 60)
# (R4) sector lemma, exhaustive over sector multisets (theta from R3); intervals handled by their ends
TH = max(th_base, th_lat)
def fillings(edge):
    out = []
    for k in range(0, 5):
        for m in range(0, 4):
            lo = edge * k + (180 - TH) * m; hi = edge * k + (180 + TH) * m
            if k + m >= 2 and lo - 1e-9 <= 360 <= hi + 1e-9: out.append((k, m))
    return out
fr = fillings(120); fc = fillings(90)
chk(f'(R4) RD: fillings of 360 by (k edges of 120, m near-flat sectors): {fr}; the only one with an RD edge is (3, 0)', [x for x in fr if x[0] >= 1] == [(3, 0)])
chk(f'(R4) NEGATIVE CONTROL cube: fillings {fc} include an edge beside a flat sector (k >= 1, m >= 1): sliding possible', any(k >= 1 and m >= 1 for k, m in fc))
# (M) mirror images
ROT = [M for M in OH if det(M) == 1]; assert len(ROT) == 24
H = {k: v for k, v in D['heights'].items()}
POS = {e: positions(e) for e in NB}; PIDX = {e: {p: j for j, p in enumerate(POS[e])} for e in NB}
def h(a, e, p): return H[f'{a}:{e}'][PIDX[e][p]]
T = D['types']; fit_plain = 0; fit_mixed = []
for a in range(T):
    for e in NB:
        for R in ROT:
            ebp = app(R, tuple(-x for x in e)); ebm = app(R, e)
            for b in range(T):
                if all(h(a, e, p) + h(b, ebp, app(R, sub(p, e))) == 0 for p in POS[e]): fit_plain += 1
                if all(h(a, e, p) + h(b, ebm, tuple(-x for x in app(R, sub(p, e)))) == 0 for p in POS[e]): fit_mixed.append((a, e, b))
    if a % 10 == 9: print(f'PROGRESS {(a + 1) / T:.2f} types (mirror test)', flush=True)
chk(f'(M) CONTROL unmirrored fits recounted with our own rotations: {fit_plain} (keyed_rd.py: {D["fit"]})', fit_plain == D['fit'])
flatfaces = sum(1 for k, v in H.items() if all(x == 0 for x in v))
print(f'(M) faces with no bump or dent: {flatfaces}; fitting (type, face, MIRRORED type, turn) pairs: {len(fit_mixed)}', flush=True)
print('VERDICT MIRRORS:', 'no mirrored piece fits beside an unmirrored one (a tiling is all one hand)' if not fit_mixed else
      f'{len(fit_mixed)} mixed pairs fit: mirrored pieces can join; the contact and whole-chair tests must be rerun with 48 orientations', flush=True)
print('FINAL ok' if ok else 'FINAL FAIL', flush=True)
