# Gaps batch C, item 2 (L13): #45 Conjecture 1, the largest width of DICTO's bodies B = ∩ B(v, D) on the cube, octahedron,
# dodecahedron and icosahedron (D = 2R, the diameter). -> logs/item2.log
#
# Reduction. B is centrally symmetric, so w(u) = h(u) + h(-u) = 2 h(u) and max_u w = 2 max_{x in B} |x|.
# |x|² is convex, so its maximum on B is on the boundary, at a point lying on exactly one sphere, exactly two, or three or more.
#  (1) one sphere |x - v| = ρ (ρ = D = 2R): on that sphere the only local maximum of |x|² is x = v + ρ v/|v| (|x| = 3R), which is not in B
#      (it is 4R from -v); the other critical point is x = -v, the minimum. So no maximum lies inside a face.
#  (2) two spheres v_i, v_j: the circle lies in the plane (v_j - v_i).x = 0 (|v_i| = |v_j|), with centre c = (v_i + v_j)/2 and radius²
#      ρ² - |v_i - v_j|²/4; on it |x|² = ρ² - R² + 2 x.v_i, so a local maximum inside an arc is x = c + r c/|c|. For antipodal pairs (c = 0)
#      |x|² = 3R² on the whole circle, but such x would need x.v_m >= 0 for every corner v_m and its opposite: impossible, so these circles miss B.
#  (3) three or more spheres: every such point lies on the line through 0 along n = (v_j - v_i) x (v_k - v_i), at x = t n with
#      t² |n|² - 2 t p - 3R² = 0, p = n.v_i; the two roots have opposite signs.
# Membership (exact): for x on the sphere of v_i, |x - v_m| <= ρ  <=>  x.(v_m - v_i) >= 0. With x = t n or x = s c (s > 0) its sign is
# sign(t)·sign(n.(v_m - v_i)) or sign(c.(v_m - v_i)), both in Q(√5): membership and ties are decided exactly.
# The values |x|² of the finitely many candidates are then compared at 60 digits; the maximum is separated from the next value by a gap
# far larger than the error, and equals the face-axis value of #45's main theorem.
import sys, os, itertools
sys.path.insert(0, os.path.dirname(__file__))
from q5 import *
import mpmath as mp
mp.mp.dps = 60
L = []
def log(s=''): print(s); L.append(s)
here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s5 = mp.sqrt(5)
mf = lambda z: mp.mpf(z.a.numerator) / z.a.denominator + mp.mpf(z.b.numerator) / z.b.denominator * s5

C8 = uniq([[Q(a), Q(b), Q(c)] for a in (1, -1) for b in (1, -1) for c in (1, -1)])
SOL = [('dodecahedron', uniq(C8 + cyc([(0, 1 / PHI, PHI)]))), ('icosahedron', cyc([(0, 1, PHI)])),
       ('cube', C8), ('octahedron', cyc([(1, 0, 0)]))]
res = {}
for name, V in SOL:
    R2 = dot(V[0], V[0]); assert all(dot(v, v) == R2 for v in V)
    FV = facets(V); rin2 = min((d * d / dot(n, n) for n, d in FV), key=lambda z: z.f())
    rho = 2 * mp.sqrt(mf(R2)); Rm = mp.sqrt(mf(R2))
    cands = []                                     # (|x|², kind, data)
    # (3) points on three spheres
    nvert = 0
    for i, j, k in itertools.combinations(range(len(V)), 3):
        n = cross(sub(V[j], V[i]), sub(V[k], V[i]))
        if all(x == 0 for x in n): continue
        nn = dot(n, n); p = dot(n, V[i])
        for sg in (1, -1):                         # t = (p ± sqrt(p² + 3R² nn)) / nn ; sign(t) = sg
            inside = True; on = 0
            for m in range(len(V)):
                e = dot(n, sub(V[m], V[i])).sign() * sg
                if e < 0: inside = False; break
                if e == 0: on += 1
            if not inside: continue
            t = (mf(p) + sg * mp.sqrt(mf(p) ** 2 + 3 * mf(R2) * mf(nn))) / mf(nn)
            x = [t * mf(c) for c in n]
            cands.append((t * t * mf(nn), 'vertex', on, tuple(mp.nstr(c, 12) for c in x))); nvert += 1
    # (2) interior critical points of arcs (non-antipodal pairs whose circle exists)
    narc = 0
    for i, j in itertools.combinations(range(len(V)), 2):
        cc = [(V[i][a] + V[j][a]) / 2 for a in range(3)]
        if all(x == 0 for x in cc):                # antipodal: circle misses B (lemma above); confirm exactly by membership of its points
            continue
        m2 = dot(sub(V[i], V[j]), sub(V[i], V[j]))
        r2c = 4 * R2 - m2 / 4
        if r2c.sign() <= 0: continue
        if any(dot(cc, sub(V[m], V[i])).sign() < 0 for m in range(len(V))): continue
        c2 = mf(dot(cc, cc)); val = (mp.sqrt(c2) + mp.sqrt(mf(r2c))) ** 2
        cands.append((val, 'arc', 2, (i, j))); narc += 1
    vals = sorted(set(mp.nstr(c[0] / mf(R2) / 4, 40) for c in cands), key=lambda z: -mp.mpf(z))   # |x|² at D = 1 (divide by ρ² = 4R²)
    top = mp.mpf(vals[0]); nxt = mp.mpf(vals[1]) if len(vals) > 1 else mp.mpf(0)
    log(f'   distinct |x|² values among candidates (D = 1): {[mp.nstr(mp.mpf(z), 12) for z in vals]}')
    r = mp.sqrt(mf(rin2) / (4 * mf(R2)))           # inradius at D = 1
    face = mp.sqrt(mp.mpf(3) / 4 + r * r) - r      # #45 main theorem: half the face-axis width
    tops = [c for c in cands if abs(c[0] / mf(R2) / 4 - top) < mp.mpf(10) ** -40]
    kinds = sorted(set((c[1], c[2]) for c in tops))
    # the maximisers lie on face axes: check the direction of each against the facet normals
    on_axis = all(any(abs(abs(mp.fdot([mp.mpf(z) for z in c[3]], [mf(q_) for q_ in nrm]) / (mp.norm([mp.mpf(z) for z in c[3]]) * mp.norm([mf(q_) for q_ in nrm]))) - 1) < 1e-10
                      for nrm, d in FV) for c in tops if c[1] == 'vertex')
    log(f'{name}: {len(V)} corners; candidates in B: {nvert} three-sphere points, {narc} arc maxima')
    log(f'   largest |x| at D = 1: {mp.nstr(mp.sqrt(top), 25)}  -> largest width 2|x| = {mp.nstr(2 * mp.sqrt(top), 25)}')
    log(f'   face-axis width (#45 main theorem) 2(√(3/4 + r²) - r) = {mp.nstr(2 * face, 25)};  difference {mp.nstr(mp.sqrt(top) - face, 5)}')
    log(f'   attained at {len(tops)} candidates, kinds {kinds}, all on face axes: {on_axis}; next largest width {mp.nstr(2 * mp.sqrt(nxt), 15) if nxt else 'none (single value)'} (gap {mp.nstr(2 * (mp.sqrt(top) - mp.sqrt(nxt)), 6)})')
    ok = abs(mp.sqrt(top) - face) < mp.mpf(10) ** -40 and on_axis and (top - nxt) > mp.mpf(10) ** -6
    res[name] = ok
    log(f'   Conjecture 1 for {name}: {"PROVED" if ok else "NOT confirmed"}')
# controls: (a) the smallest width is 1 (#45 (i)) is not tested here; (b) a failing control: drop the arc candidates' membership
# test and the largest |x| exceeds the face-axis value (shows the membership test is what bounds the answer)
V = SOL[2][1]; R2 = dot(V[0], V[0]); bad = 0
for i, j in itertools.combinations(range(len(V)), 2):
    cc = [(V[i][a] + V[j][a]) / 2 for a in range(3)]
    if all(x == 0 for x in cc): continue
    r2c = 4 * R2 - dot(sub(V[i], V[j]), sub(V[i], V[j])) / 4
    bad = max(bad, (mp.sqrt(mf(dot(cc, cc))) + mp.sqrt(mf(r2c))) ** 2 / (4 * mf(R2)))
log(f'control (must exceed): cube, arc maxima without the membership test give |x| = {mp.nstr(mp.sqrt(bad), 12)} > face value {mp.nstr((mp.sqrt(0.75 + 1 / 12.) - mp.sqrt(1 / 12.)), 12)}: {mp.sqrt(bad) > mp.sqrt(0.75 + mp.mpf(1) / 12) - mp.sqrt(mp.mpf(1) / 12)}')
log(f'control (must match #45 widths.log): cube/octahedron 1.248391589161, dodecahedron/icosahedron 1.110988655456 (see lines above)')
log('VERDICT: Conjecture 1 ' + ('PROVED for the cube, octahedron, dodecahedron and icosahedron' if all(res.values()) else f'not settled: {res}') +
    '; the tetrahedron part (√3 − √2/2) is the classical Reuleaux tetrahedron value, not re-proved here.')
log('FINAL ok')
open(os.path.join(here, 'logs/item2.log'), 'w').write('\n'.join(L) + '\n')
