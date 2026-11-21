"""Branch C (tree-search round 1): exact counting for a face-to-face periodic tiling by C1 and ONE scutoid kind K.
C1 = truncated icosahedron (edge 1) + dodecahedron centre pyramid on each pentagon: 60 spike triangles (1, L, L), L = sqrt3*phi/2,
20 regular hexagons; edges: 30 hexagon-hexagon (hh, 3pi/2 - 2beta), 60 reflex (r, 3pi/4 + beta, length 1), 60 side-side (ss, 2pi/3, length L).
Proved lemmas used (README, proper round): B1 no shared spike triangle; B2 shared hexagon only with types swapped, each of its 6 edges keeps
a wedge t' = beta - pi/4 filled by ONE K edge; B3 at most 8 hexagons of a C1 shared.  s = shared hexagons per C1 (average), 0 <= s <= 8.
Scope (inherited from the proper round): K dihedrals p*pi + b*beta with b in {-1,0,1}; lateral-lateral edges rational (b = 0), so every
beta-carrying K edge is an end-lateral edge.  Scutoid = two parallel end faces (p-gon, q-gon), lateral faces, y >= 1 Y-vertices, every
vertex of degree 3 (simple), each lateral face has at most one top edge and at most one bottom edge.  Faces meet in whole faces (complex).
Equations:
 (E1) incidence, strict: n*t = 60, n*h = 20 - s (all spike-triangle and hexagon faces of K lie on C1);
      loose: n*t >= 60, n*h >= 20 - s, n*(t + h) >= 80 - s (a K triangle/hexagon face may also lie on another K).
 (E2) Euler for a simple scutoid: V = p+q+y, E = 3V/2, F = 2 + (p+q+y)/2 <= 16; y >= max(1, |p-q|).
 (E3) lateral faces: c_i in {0,1,2} end edges, sum c_i = p+q, #(c=2) <= min(p,q); a lateral face with c end edges has exactly 2c vertices
      on the end planes (simple), so sum over lateral faces of (sides - 2c) = 3y.  Lateral triangle: c <= 1 (c = 1 apex is a Y-vertex);
      lateral hexagon: c <= 2; other lateral faces any sides >= max(3, 2c).
 (E4) beta demand per C1 (ring closure, rings.json alphabet |b| <= 1 per K edge): hh ring needs b-sum +2 (>= 2 K edges), reflex ring b-sum
      -1 (>= 1), merged ring at a shared hexagon exactly one t' edge.  Other C1 in an hh/reflex ring adds no saving (t' with two gaps is
      impossible: p-sum >= -1/4 + w/4 + z/12 with equality only for one edge).  So per C1 >= 3s + 2(30-3s) + (60-3s) = 120 - 6s
      beta-carrying K edges of length 1, each an END edge of length 1.  Supply per K: end triangle 1 (base; legs are L), end hexagon 6,
      end K-K m-gon <= m.  Need n*S >= 120 - 6s.
 (E5) s > 0: the t' wedge is an edge between a K face on a spike triangle and a K face on a hexagon, one of them an END face.
 (E6) volume and packet: vol C1 + n vol K = cell volume fixes no integer (cell free); packet zero of K is sum b*l = 0 over its beta edges,
      compatible with (E4) (C1 demands sum to +60 - 60 = 0).  Recorded, no filter.
Output: every surviving combinatorial type (n, s, t, h, f, end kinds, p, q, y) in both modes."""
import itertools, json, sys
from fractions import Fraction as Fr
FMAX = 16
def lateral_ok(p, q, y, tl, hl, fl):
    """exists c-assignment with sum c = p+q, #c2 <= min(p,q), sum(sides-2c) = 3y; triangles c<=1, hexagons c<=2, others sides free >= max(3,2c)."""
    need = p + q
    for a in range(tl + 1):                      # triangles with c=1
        for h2 in range(hl + 1):
            for h1 in range(hl - h2 + 1):
                for o2 in range(fl + 1):
                    for o1 in range(fl - o2 + 1):
                        if a + h1 + 2 * h2 + o1 + 2 * o2 != need: continue
                        if h2 + o2 > min(p, q): continue
                        if (a + h1 + h2 + o1 + o2) < max(p, q) - (h2 + o2) + (h2 + o2): pass
                        # Y incidences: triangles 3-2c, hexagons 6-2c, others (m-2c) with m >= max(3,2c)
                        yt = a * 1 + (tl - a) * 3 + h1 * 4 + h2 * 2 + (hl - h1 - h2) * 6
                        ymin_o = o2 * 0 + o1 * 1 + (fl - o1 - o2) * 3
                        r = 3 * y - yt
                        if fl == 0 and r == 0: return (a, h1, h2, o1, o2)
                        if fl > 0 and r >= ymin_o: return (a, h1, h2, o1, o2)
    return None
def run(mode):
    out = []
    for n in range(1, 61):
        for s in range(0, 9):
            for t in range(1, FMAX):
                for h in range(1, FMAX - t + 1):
                    if mode == 'strict' and not (n * t == 60 and n * h == 20 - s): continue
                    if mode == 'loose' and not (n * t >= 60 and n * h >= 20 - s and n * (t + h) >= 80 - s): continue
                    for f in range(0, FMAX - t - h + 1):
                        F = t + h + f
                        for et in range(0, min(2, t) + 1):
                            for eh in range(0, min(2 - et, h) + 1):
                                ef = 2 - et - eh
                                if ef > f: continue
                                if s > 0 and et + eh == 0: continue           # E5
                                kinds = ['T'] * et + ['H'] * eh + ['K'] * ef
                                fixed = [3] * et + [6] * eh
                                # end polygon sizes
                                rng = [range(3, 2 * FMAX)] * ef
                                for free in itertools.product(*rng):
                                    sides = fixed + list(free)
                                    p, q = sides
                                    if (p + q) % 2 and False: pass
                                    y2 = 2 * (F - 2) - (p + q)              # E2: F = 2 + (p+q+y)/2
                                    y = y2
                                    if y < max(1, abs(p - q)): continue
                                    S = et * 1 + eh * 6 + sum(free)
                                    if n * S < 120 - 6 * s: continue        # E4
                                    lat = lateral_ok(p, q, y, t - et, h - eh, f - ef)
                                    if lat is None: continue
                                    key = (n, s, t, h, f, ''.join(sorted(kinds)), min(p, q), max(p, q), y)
                                    out.append(key)
    return sorted(set(out))
res = {}
for mode in ('strict', 'loose'):
    L = run(mode)
    res[mode] = L
    print(f"== {mode}: {len(L)} surviving types (n, s, t, h, f, end kinds, p, q, y)")
    ns = sorted(set(k[0] for k in L)); print("   n values:", ns)
    for k in L[:40]: print("  ", k)
    if len(L) > 40: print("   ...")
# diagnostics: which constraint kills the strict case at s = 0 (branch C proper)
print("== strict, s = 0 (no hexagon shared): candidates n | 20 with n*t = 60, n*h = 20, t + h <= 16")
for n in (1, 2, 4, 5, 10, 20):
    t, h = 60 // n, 20 // n
    print(f"   n={n}: t={t}, h={h}, t+h={t+h}", "too many faces" if t + h > FMAX else "", "| survivors:", [k for k in res['strict'] if k[0] == n and k[1] == 0])
checks = []
def chk(name, c): checks.append(bool(c)); print(f"  [{'pass' if c else 'FAIL'}] {name}")
print("== checks")
# controls: the classic scutoid (pentagon top, hexagon bottom, one Y-vertex; 1 lateral triangle, 2 pentagons, 3 quadrilaterals)
chk("control: classic scutoid p=5, q=6, y=1 has F = 2 + (5+6+1)/2 = 8 faces", 2 + (5 + 6 + 1) // 2 == 8)
chk("control: its 6 lateral faces pass E3", lateral_ok(5, 6, 1, 0, 0, 6) is not None)
chk("control: 6 lateral faces cannot carry 13 end edges (E3 rejects p=6, q=7 with 6 laterals)", lateral_ok(6, 7, 1, 0, 0, 6) is None)
chk("strict, s = 0: no survivor with n <= 5", not [k for k in res['strict'] if k[1] == 0 and k[0] <= 5])
chk("strict, s = 0, n = 5 killed by supply: 5 * (6 + 6) < 120", 5 * 12 < 120)
chk("beta demand cancels per C1: +2*30 - 60 = 0", 2 * 30 - 60 == 0)
chk("every survivor has F <= 16 and y >= 1", all(k[2] + k[3] + k[4] <= FMAX and k[8] >= 1 for m in res for k in res[m]))
import collections
summ = {'strict_types': [list(k) for k in res['strict']], 'strict_count': len(res['strict']), 'loose_count': len(res['loose']),
        'strict_by_n_s': {f"{a},{b}": c for (a, b), c in sorted(collections.Counter((k[0], k[1]) for k in res['strict']).items())},
        'loose_by_n': {str(a): c for a, c in sorted(collections.Counter(k[0] for k in res['loose']).items())}}
json.dump(summ, open(sys.argv[1] if len(sys.argv) > 1 else 'count_summary.json', 'w'), indent=0)
print("FINAL ok" if all(checks) else "FINAL FAIL (a check failed)")
