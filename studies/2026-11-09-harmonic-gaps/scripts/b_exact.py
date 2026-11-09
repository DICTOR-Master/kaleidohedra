# DICTO 2026-11-09 harmonic-gaps study, part B exact (Q(sqrt5)): #42's open point "what fills between the great star and the Sunstar".
# DICTO proposed solving these by 3D waves (harmonics); b_harmonic.py is the harmonic half, b_explore.py the float survey behind the
# candidates tested here. Frame and constructions copied from studies/2026-10-20-sunstar/sunstar_exact.py (cells of edge 2).
#   B1 the 63 stellation cells of CORE = DOD/phi^3 (their union is the great star GSD, corners = DOD's);
#   B2 the small Sunstar (CORE + 6 Dogstars of the 1/phi^3 lattice) inside the big Dogstar? and GSD - big Dogstar = 6 wedges + 12 spikes;
#   B3 each stellation cell: exact volume inside the small Sunstar -> the gap, cell by cell, by orbit;
#   B4 candidate fillers: whole pieces of the 1/phi^3 lattice (dodecahedra, Dogstars) -> exact fraction of each orbit inside GSD;
#       whole stellation cells -> exact fractions; the big Dogstar -> exact.
import sys, os, json, itertools, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from fractions import Fraction as Fr
from q5 import *
from exactpoly import planes_of, intersect, volume
DATA = os.path.join(HERE, '..', 'data'); log = {'mark': 'DICTO harmonic gaps, part B exact, 2026-11-09 · ' + MARK}; fails = []
def ok(c, m):
    print(('PASS ' if c else 'FAIL ') + m, flush=True); log.setdefault('checks', []).append(('PASS ' if c else 'FAIL ') + m)
    if not c: fails.append(m)
    return c
t0 = time.time()
P = PHI; IP = qs(P, ONE)
V3 = lambda a, b, c: [x if isinstance(x, tuple) else qr(Fr(x)) for x in (a, b, c)]
def cap(*pp):
    C = intersect([pl for pls in pp for pl in pls]); return volume(C) if C else Z
def vsum(xs):
    t = Z
    for x in xs: t = qa(t, x)
    return t
C8 = [V3(*s) for s in itertools.product((1, -1), repeat=3)]
RID = [r for a in (1, -1) for b in (1, -1) for r in ([Z, qm(qr(a), IP), qm(qr(b), P)], [qm(qr(a), IP), qm(qr(b), P), Z], [qm(qr(b), P), Z, qm(qr(a), IP)])]
DOD = C8 + RID
def roof(c_nb, c_q, s=ONE):
    ax = next(i for i in range(3) if c_nb[i] != c_q[i]); sg = 1 if qf(c_q[ax]) > qf(c_nb[ax]) else -1
    sq = [p for p in C8 if p[ax] == qr(sg)]; rd = [p for p in RID if p[ax] == qm(qr(sg), P)]
    return [vadd(c_nb, vmul(p, s)) for p in sq + rd]
cube = lambda c, s=ONE: [vadd(c, vmul(p, s)) for p in C8]
O = V3(0, 0, 0); E = [V3(*[d * (i == k) for i in range(3)]) for k in range(3) for d in (1, -1)]
nbs = lambda c, s=ONE: [vadd(c, vmul(e, qm(qr(2), s))) for e in E]
PLc = {}
def dogstar_meet(cell_planes, c=O, s=ONE):
    k = (tuple(map(tuple, c)), s)
    if k not in PLc: PLc[k] = (planes_of(cube(c, s)), [planes_of(roof(n, c, s)) for n in nbs(c, s)])
    cu, rf = PLc[k]; v = cap(cell_planes, cu)
    if v == Z: return Z
    for r in rf: v = qs(v, cap(cell_planes, r))
    return v
s3 = qd(ONE, qm(P, qm(P, P)))
CORE = [vmul(p, s3) for p in DOD]; CP = planes_of(CORE)
BOX = [(V3(*[d * (i == k) for i in range(3)]), qr(10)) for k in range(3) for d in (1, -1)]
cells = []
for sig in itertools.product((1, -1), repeat=12):
    pl = [(n, d) if g == 1 else ([qn(x) for x in n], qn(d)) for (n, d), g in zip(CP, sig)]
    C = intersect(pl + BOX)
    if not C or any(any(abs(qf(x)) > 9.99 for x in p) for p in C): continue
    v = volume(C)
    if sgn(v) > 0: cells.append({'layer': sig.count(-1), 'planes': pl, 'corners': C, 'vol': v})
ok(len(cells) == 63, f'B1: 63 stellation cells of CORE ({time.time() - t0:.0f} s)')
for c in cells:
    m = dogstar_meet(c['planes']); c['bigdog'] = 1 if m == c['vol'] else (0 if m == Z else None)
GV = vsum(c['vol'] for c in cells); s = s3; s_3 = qm(s, qm(s, s))
dodv = volume(DOD); dogv = qs(qr(16), dodv)
ok(vsum(c['vol'] for c in cells if c['bigdog']) == dogv, 'the big Dogstar is 45 of the 63 cells (as #42)')
small = [vmul(e, qm(qr(2), s)) for e in E]
# ---------- B2 ----------
inbig = [vsum(dogstar_meet(c['planes'], sd, s) for c in cells if c['bigdog']) for sd in small]
fb = [qd(m, qm(dogv, s_3)) for m in inbig]; log['small_dogstar_in_big_dogstar'] = qs_(fb[0])
ok(len({qs_(x) for x in fb}) == 1 and fb[0] != ONE, f'B2: the small Sunstar is NOT inside the big Dogstar: each small Dogstar has only {qs_(fb[0])} = {qf(fb[0]):.6f} of its volume there; the rest reaches into the 6 axis wedges and 12 outer spikes')
rest = [c for c in cells if not c['bigdog']]
lay_rest = sorted(c['layer'] for c in rest)
ok(lay_rest == [2] * 6 + [3] * 12, 'GSD - big Dogstar = the 6 axis wedges + 12 spikes (whole stellation cells)')
SunV = qa(qm(dodv, s_3), qm(qr(6), qm(dogv, s_3))); gapV = qs(GV, SunV)
log['volumes_cells_edge2'] = {'GSD': qs_(GV), 'big_Dogstar': qs_(dogv), 'small_Sunstar': qs_(SunV), 'gap': qs_(gapV), 'gap_minus_rest': qs_(qs(dogv, SunV))}
print(f'   GSD {qs_(GV)} = {qf(GV):.6f}; big Dogstar {qf(dogv):.6f}; small Sunstar {qs_(SunV)} = {qf(SunV):.6f}; gap {qs_(gapV)} = {qf(gapV):.6f} '
      f'({qf(gapV) / qf(GV):.4f} of GSD); in units of the small cell (edge 2/phi^3): GSD {qf(GV) / qf(qm(qr(8), s_3)):.4f}', flush=True)
# ---------- B3: cell by cell ----------
def sun_meet(c):
    v = cap(c['planes'], planes_of(CORE))
    return qa(v, vsum(dogstar_meet(c['planes'], sd, s) for sd in small))
for c in cells:
    m = sun_meet(c); c['sun'] = m; c['gapfrac'] = qd(qs(c['vol'], m), c['vol'])
orb = {}
for c in cells:
    k = (c['layer'], c['bigdog'], qs_(c['gapfrac'])); orb.setdefault(k, []).append(c)
print('   stellation cells of CORE, by kind: (layer, in big Dogstar, part in the gap) -> count, cell volume, gap part volume each', flush=True)
B3 = []
for (L, bd, fr), cs in sorted(orb.items()):
    gv = qs(cs[0]['vol'], cs[0]['sun'])
    print(f'     layer {L} {"Dogstar" if bd else "outside"}  gap fraction {fr} = {qf(cs[0]["gapfrac"]):.6f}   x{len(cs)}  cell {qs_(cs[0]["vol"])}  gap part {qs_(gv)}', flush=True)
    B3.append({'layer': L, 'in_big_dogstar': bool(bd), 'count': len(cs), 'gap_fraction': fr, 'cell_vol': qs_(cs[0]['vol']), 'gap_part': qs_(gv)})
ok(vsum(qs(c['vol'], c['sun']) for c in cells) == gapV, 'B3: the cells\' gap parts add up to the gap exactly')
whole_cells = all(c['gapfrac'] in (ONE, Z) for c in cells)
ok(True, f'B3: the gap is {"" if whole_cells else "not "}a union of whole stellation cells of CORE ({sum(1 for c in cells if c["gapfrac"] == ONE)} whole, {sum(1 for c in cells if c["gapfrac"] not in (ONE, Z))} cut)')
log['B3'] = B3
# ---------- B4: whole pieces of the 1/phi^3 lattice ----------
# one cell per orbit of the pyritohedral group T_h (cyclic permutations and sign changes; (2,1,0) and (1,2,0) are different orbits);
# every cell whose piece can reach the great star (its cube, grown by the roof height, comes within GSD's circumradius sqrt3)
def canon(k):
    return min(tuple(sg * x for sg, x in zip(sgs, k[i:] + k[:i])) for i in range(3) for sgs in itertools.product((1, -1), repeat=3))
orbits = {}
for k in itertools.product(range(-5, 6), repeat=3):
    near = sum(max(0.0, abs(x) * 2 * qf(s) - 2 * qf(s)) ** 2 for x in k) ** .5   # distance from O to the cell's piece (cube grown by one cell edge)
    if near < 3 ** .5: orbits.setdefault(canon(k), []).append(k)
reps = sorted(orbits, key=lambda k: sum(x * x for x in k))
B4 = {}
for r in reps:
    c = [qm(qr(2 * x), s) for x in r]; even = sum(r) % 2 == 0
    if even:
        pp = planes_of([vadd(c, vmul(p, s)) for p in DOD]); m = vsum(cap(pp, k['planes']) for k in cells); pv = qm(dodv, s_3)
    else:
        m = vsum(dogstar_meet(k['planes'], c, s) for k in cells); pv = qm(dogv, s_3)
    fr = qd(m, pv); B4[str(r)] = {'piece': 'dodecahedron' if even else 'Dogstar', 'orbit_size': len(orbits[r]), 'fraction_in_GSD': qs_(fr), 'float': qf(fr), 'vol_in': m}
    if m != Z: print(f'     1/phi^3 lattice {"dodecahedron" if even else "Dogstar":12s} at cell {r} (x{len(orbits[r])}): fraction inside GSD {qs_(fr)} = {qf(fr):.6f}', flush=True)
tot = vsum(qm(qr(v['orbit_size']), v['vol_in']) for v in B4.values())
ok(tot == GV, f'B4: the 1/phi^3 lattice pieces\' parts inside GSD, summed over all {len(reps)} orbits ({sum(len(v) for v in orbits.values())} cells), give GSD exactly: the list is complete')
for v in B4.values(): v['vol_in'] = qs_(v['vol_in'])
log['B4'] = B4
whole = [r for r, v in B4.items() if v['fraction_in_GSD'] == '1|0']
ok(set(whole) == {'(0, 0, 0)', '(-1, 0, 0)'} or set(whole) == {'(0, 0, 0)', '(1, 0, 0)'}, f'B4: of the 1/phi^3 lattice only the Sunstar\'s own 7 pieces lie wholly in GSD; every other piece meeting GSD is cut (whole: {whole})')
log['seconds'] = round(time.time() - t0, 1)
json.dump(log, open(os.path.join(DATA, 'b_exact.json'), 'w'), indent=1, default=str)
print('FINAL ok' if not fails else 'FINAL FAIL: ' + '; '.join(fails))
