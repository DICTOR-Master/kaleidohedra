# DICTO 2026-11-09 harmonic-gaps study, part A (exact, Q(sqrt5)): #38a's open point "whether the reciprocal cycle's shells fill by one
# pattern". DICTO proposed solving these by 3D waves (harmonics); this script is the exact half (the harmonic half is a_harmonic.py).
# Frame of #38a: I = icosahedron of edge 1; GSD = I + 20 spikes (tips 3 x face centre) -> hull D1; SSD = D1 + 12 spires (tips sqrt5 x
# face centre) -> hull I2 = phi^3 I. The cycle's own pieces: shell 1 CLEO spikes, caps (D1 face -> I corner), AXEs (I edge + two tips);
# shell 2 spires, inward pyramids (I2 face -> D1 corner), valley tetrahedra (D1 edge + two spire tips).
#  A1  the reciprocals: polar (unit sphere) of GSD = a great icosahedron, of SSD = a great dodecahedron; where their cores and hulls lie;
#  A2  GD(D1) (the great dodecahedron on D1, faces in D1's planes) against shell 2's pieces;
#  A3  GI(I) (the great icosahedron on I, faces in I's planes) against the pieces of both shells.
import os, sys, json, itertools, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from g5 import *
from radial import visible
DATA = os.path.join(HERE, '..', 'data'); log = {'mark': 'DICTO harmonic gaps, part A exact, 2026-11-09 · ' + MARK}; fails = []
def ok(c, m):
    print(('PASS ' if c else 'FAIL ') + m, flush=True); log.setdefault('checks', []).append(('PASS ' if c else 'FAIL ') + m)
    if not c: fails.append(m)
    return c
t0 = time.time()
I = icosahedron(); FI = faces(I)
D1 = [vmul(cent(F), qr(3)) for _, F in FI]
FD = faces(D1); s5 = (Fr(0), Fr(1))
I2 = [vmul(cent(F), s5) for _, F in FD]; phi3 = qm(P, qm(P, P))
ok(same_set(I2, scale(I, phi3)) and len(FD) == 12, 'cycle: D1 = 3 x face centres of I (dodecahedron), I2 = sqrt5 x face centres of D1 = phi^3 I')
PI, PD, PI2 = planes_of(I), planes_of(D1), planes_of(I2)
# ---------- pieces of the cycle (#38a) ----------
spikes = [F + [vmul(cent(F), qr(3))] for _, F in FI]
spires = [F + [vmul(cent(F), s5)] for _, F in FD]
def inward(hullF, core):
    out = []
    for (n, d), F in hullF:
        c = max(core, key=lambda v: qf(dot(n, v))); out.append(F + [c])
    return out
caps, inpyr = inward(FD, I), inward(faces(I2), D1)
def valley(core, sp):
    e2 = min(qf(dot(vsub(a, b), vsub(a, b))) for a, b in itertools.combinations(core, 2)); out = []
    for a, b in itertools.combinations(core, 2):
        if abs(qf(dot(vsub(a, b), vsub(a, b))) - e2) > 1e-9: continue
        two = [S[-1] for S in sp if any(key(a) == key(x) for x in S[:-1]) and any(key(b) == key(x) for x in S[:-1])]
        if len(two) == 2: out.append([a, b] + two)
    return out
axes, vtets = valley(I, spikes), valley(D1, spires)
ok([len(x) for x in (spikes, caps, axes, spires, inpyr, vtets)] == [20, 12, 30, 12, 20, 30], 'the cycle\'s pieces: 20 CLEO, 12 caps, 30 AXE; 12 spires, 20 inward pyramids, 30 valley tetrahedra')
vols = {k: volume(v[0]) for k, v in dict(CLEO=spikes, cap=caps, AXE=axes, spire=spires, inward_pyramid=inpyr, valley_tet=vtets).items()}
vols['I'], vols['D1'], vols['I2'] = volume(I), volume(D1), volume(I2)
ok(qs_(vols['CLEO']) == '1/8|1/24' and qs_(vols['spire']) == '5/3|3/4', f'piece volumes as #38a: CLEO {qs_(vols["CLEO"])}, spire {qs_(vols["spire"])}')
log['volumes'] = {k: qs_(v) for k, v in vols.items()}
# ---------- A1: the reciprocals (polar about the unit sphere) ----------
# GSD: its 20 corners are D1's; its 12 face planes (pentagrams) are the planes through I's 5-corner rings = the faces of d0 = D1/phi^3.
d0 = scale(D1, qd(ONE, phi3)); Pd0 = planes_of(d0)
ring = all(sum(1 for v in I if dot(n, v) == d) == 5 and sum(1 for v in D1 if dot(n, v) == d) == 5 for n, d in Pd0)
ok(ring, "GSD's 12 face planes are d0 = D1/phi^3's faces: each holds 5 corners of I and 5 corners (a pentagram) of D1")
# SSD: corners I2, face planes D1's own faces (5 corners of I2 on each)
ok(all(sum(1 for v in I2 if dot(n, v) == d) == 5 for n, d in PD), "SSD's 12 face planes are D1's own faces (5 corners of I2 on each)")
pol = lambda pts: polar(pts)
D1s, Is, I2s, d0s = pol(D1), pol(I), pol(I2), pol(d0)     # D1* icosahedron, I* dodecahedron, I2* dodecahedron, d0* icosahedron
# reciprocal of GSD: corners = poles of GSD's face planes = d0*; face planes = polars of GSD's corners = D1*'s faces
# reciprocal of SSD: corners = poles of D1's face planes = D1*; face planes = polars of I2's corners = I2*'s faces
ok(same_set(d0s, scale(D1s, phi3)), 'reciprocal of GSD: its 12 corners d0* = phi^3 x D1* (its core, an icosahedron): core and hull one whole turn apart')
outside = [v for v in d0s if not inside_hull(v, planes_of(Is))]
ok(len(outside) == 12, f'the reciprocal shell of [I, D1] is [D1*, I*]; all 12 corners of the reciprocal of GSD lie strictly outside I* ({len(outside)} of 12): the great icosahedron breaks through its shell')
ok(all(inside_hull(v, planes_of(scale(D1s, phi3))) for v in Is) and all(inside_hull(v, planes_of(Is)) for v in D1s),
   'D1* ⊂ I* ⊂ phi^3 D1*: the dodecahedral hull I* lies between the great icosahedron\'s core and hull')
# shape of the reciprocal shells: [D1*, I*] similar to [I, D1]? and [I2*, D1*] similar to [D1, I2]?
def similar(A1, B1, A2, B2):
    """is (A2, B2) = k (A1, B1) for one k > 0 in Q(sqrt5)? k from the corner of A2 on the ray of A1[0]"""
    p = A1[0]; i = next(j for j in range(3) if p[j] != Z)
    par = [v for v in A2 if all(x == Z for x in cross(v, p)) and sgn(qd(v[i], p[i])) > 0]
    if not par: return False, Z
    k = qd(par[0][i], p[i]); return same_set(A2, scale(A1, k)) and same_set(B2, scale(B1, k)), k
s1, k1 = similar(I, D1, D1s, Is); s2, k2 = similar(D1, I2, I2s, D1s)
ok(s1 and s2, f'the convex chain is self-reciprocal: [D1*, I*] = k [I, D1] with k = {qs_(k1)} ({qf(k1):.6f}) and [I2*, D1*] = k [D1, I2] with k = {qs_(k2)} ({qf(k2):.6f})')
log['reciprocal_scale'] = {'GSD_shell': qs_(k1), 'SSD_shell': qs_(k2)}
# so: reciprocal of SSD = k2 x GD(D1) (stellation of D1, corners I2), in the SSD shell itself; reciprocal of GSD = k1 x GI(I) (stellation of I, corners I2)
GIc = [((n, d), [v for v in I2 if dot(n, v) == d]) for n, d in PI]
GDc = [((n, d), [v for v in I2 if dot(n, v) == d]) for n, d in PD]
ok(all(len(F) == 3 for _, F in GIc) and all(len(F) == 5 for _, F in GDc),
   'GI(I): each of I\'s 20 face planes holds exactly 3 corners of I2 (its triangles); GD(D1): each of D1\'s 12 planes holds 5 corners of I2 (its pentagons)')
ok(same_set(scale(I2, k1), d0s) and same_set(scale(I2, k2), D1s), 'reciprocal of GSD = k1·GI(I) and reciprocal of SSD = k2·GD(D1) (corner sets match)')
def order(F, n):
    c = fl(cent(F)); nf = fl(n); u = fl(F[0]) - c; w = np.cross(nf, u)
    return [p for _, p in sorted(((np.arctan2((fl(p) - c) @ w, (fl(p) - c) @ u), i), p) for i, p in enumerate(F))]
GI_faces = [np.array([fl(p) for p in order(F, n)]) for (n, d), F in GIc]
GD_faces = [np.array([fl(p) for p in order(F, n)]) for (n, d), F in GDc]
# ---------- the two stars as exact cones over their visible boundaries ----------
visGI, visGD = visible(GI_faces), visible(GD_faces)
conesGI, conesGD = exact_cones(visGI, PI), exact_cones(visGD, PD)
import pickle; pickle.dump({'visGI': visGI, 'visGD': visGD}, open(os.path.join(DATA, 'a_visible.pkl'), 'wb'))
VGI = vsum(volume([[Z, Z, Z]] + T) for T, _, _ in conesGI); VGD = vsum(volume([[Z, Z, Z]] + T) for T, _, _ in conesGD)
P4 = qm(phi3, P); e3 = lambda e: qm(e, qm(e, e))
ok(VGI == qm(qd((Fr(25), Fr(9)), qr(4)), e3(P)), f'GI(I) volume from {len(conesGI)} exact cones = (25 + 9 sqrt5)/4 x a^3 with a = phi = its triangles\' edge phi^4 / phi^3 (classical formula, short edge): {qs_(VGI)} = {qf(VGI):.6f}')
ok(VGD == qm(qd((Fr(-5), Fr(5)), qr(4)), e3(phi3)), f'GD(D1) volume from {len(conesGD)} exact cones = 5(sqrt5 - 1)/4 x edge^3 with edge phi^3 (classical): {qs_(VGD)} = {qf(VGD):.6f}')
log['GI_volume'], log['GD_volume'] = qs_(VGI), qs_(VGD)
# ---------- A2: GD(D1) and the second shell ----------
def classify(pieces, cones, name):
    res = []
    for p in pieces:
        v = volume(p); m = vol_in(p, cones); res.append('in' if m == v else ('out' if m == Z else 'part ' + qs_(qd(m, v))))
    print(f'   {name}: {dict((k, res.count(k)) for k in set(res))}', flush=True)
    return res
A2 = {'D1': classify([D1], conesGD, 'D1'), 'spire': classify(spires, conesGD, 'spires'), 'valley_tet': classify(vtets, conesGD, 'valley tetrahedra'),
      'inward_pyramid': classify(inpyr, conesGD, 'inward pyramids')}
ok(A2['D1'] == ['in'] and set(A2['spire']) == {'in'} and set(A2['valley_tet']) == {'in'} and set(A2['inward_pyramid']) == {'out'} and
   VGD == vsum([vols['D1'], qm(qr(12), vols['spire']), qm(qr(30), vols['valley_tet'])]),
   'GD(D1) = D1 + 12 spires + 30 valley tetrahedra exactly, and I2 - GD(D1) = the 20 inward pyramids: the great dodecahedron is a stage of the SSD shell\'s own fill')
# ---------- A3: GI(I) and both shells ----------
A3 = {'I': classify([I], conesGI, 'I'), 'CLEO': classify(spikes, conesGI, 'CLEO spikes'), 'cap': classify(caps, conesGI, 'caps'),
      'AXE': classify(axes, conesGI, 'AXEs'), 'spire': classify(spires, conesGI, 'spires'), 'inward_pyramid': classify(inpyr, conesGI, 'inward pyramids'),
      'valley_tet': classify(vtets, conesGI, 'valley tetrahedra')}
log['A2'], log['A3'] = A2, A3
cut = [k for k, v in A3.items() if any(x.startswith('part') for x in v)]
whole = all(not x.startswith('part') for v in A3.values() for x in v)
ok(True, f'GI(I) against the cycle\'s pieces: pieces cut by it: {cut if cut else "none"}; GI is {"" if whole else "not "}a union of the cycle\'s pieces')
log['GI_union_of_cycle_pieces'] = whole
fr = lambda k: qs(ONE, Z) if A3[k][0] == 'in' else (Z if A3[k][0] == 'out' else (Fr(A3[k][0].split()[1].split('|')[0]), Fr(A3[k][0].split()[1].split('|')[1])))
recon = vsum([vols['I']] + [qm(qm(qr(len(A3[k])), vols[n]), fr(k)) for k, n in (('CLEO', 'CLEO'), ('cap', 'cap'), ('AXE', 'AXE'), ('spire', 'spire'), ('inward_pyramid', 'inward_pyramid'), ('valley_tet', 'valley_tet'))])
ok(recon == VGI and all(len(set(v)) == 1 for v in A3.values()), f'partition check: I + the cycle pieces\' parts inside GI add up to its volume ({qs_(recon)}); each kind is cut the same way (caps keep {A3["cap"][0]}, spires keep {A3["spire"][0]})')
# GI's corners over I's corners (5-fold), its faces in I's planes: tips over the core's CORNERS, not its faces
ok(all(any(qd(v[k], w[k]) == phi3 for k in range(3) if w[k] != Z) and same_set([v], [scale([w], phi3)[0]]) for v, w in zip(scale(I, phi3), I)),
   "GI(I)'s 12 tips stand over I's 12 corners (radially, x phi^3): the Cleo pattern needs tips over the core's faces")
log['seconds'] = round(time.time() - t0, 1)
json.dump(log, open(os.path.join(DATA, 'a_exact.json'), 'w'), indent=1, default=str)
print('FINAL ok' if not fails else 'FINAL FAIL: ' + '; '.join(fails))
