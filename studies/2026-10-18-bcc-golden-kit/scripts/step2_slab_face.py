# DICTO 2026-10-18 bcc golden kit -- STEP 2 (picture first): one slab face (the RT golden-rhombus face facing a second neighbour) tiled
# by golden pieces, and the two layers seen side-on. Exact in Q(sqrt5):
#  - the face's edges lie along two five-fold axes u1, u2 and have length 3*phi*e (e = lambda/phi rhombohedron edge) = 3e + 3e/phi;
#  - a layer = the face's parallelogram tiles (sides e, e/phi) pushed along a third five-fold axis w by length L: rhombohedra and golden
#    bricks (parallelepipeds with edges along five-fold axes). Which (w, L) give layer height = half the slab gap?
#  - spill: a layer is an OBLIQUE prism; its top face is shifted sideways by the part of L*w in the face plane. Is there a pair of
#    layers (w1, L1), (w2, L2) whose sideways shifts cancel, so the stack ends exactly on the neighbour's face (no spill at the top)?
# -> data/step2-slab.json (+ 2D coords for draw_step2.py)
import itertools, numpy as np
from exactpoly import *
G = json.load(open(os.path.join(HERE, '..', '..', '2026-10-16-ocd-pyrochlore', 'data', 'gbpc-geom-exact.json')))
RT = [[q(x) for x in v] for v in G['RT']]; LB = [[q(x) for x in v] for v in G['LB']]; AX5 = [[q(x) for x in v] for v in G['AX5']]
second = []
for c in itertools.product(range(-2, 3), repeat=3):
    o = [Z, Z, Z]
    for k, Lv in zip(c, LB): o = vadd(o, vmul(Lv, qr(k)))
    second.append(o)
d2 = sorted({qs_(dot(o, o)) for o in second if dot(o, o) != Z}, key=lambda s: qf(q(s)))[1]
o = [o for o in second if qs_(dot(o, o)) == d2][0]
n, d = [(n, d) for n, d in planes_of(RT) if all(x == Z for x in cross(n, o)) and sgn(dot(n, o)) > 0][0]
FA = [v for v in RT if dot(n, v) == d]
# order the face corners round the rhombus; edges from corner A
A = FA[0]; others = FA[1:]
dd = sorted(others, key=lambda v: qf(dot(vsub(v, A), vsub(v, A))))
B, D_ = dd[0], dd[1]; Cc = dd[2]                                   # A-B and A-D are edges, C opposite
E1, E2 = vsub(B, A), vsub(D_, A)
assert all(x == y for x, y in zip(vadd(A, vadd(E1, E2)), Cc)), 'rhombus'
lam = qm(PHI, qr(Fr(1, 9))); iphi = qinv(PHI); s_e = qm(lam, iphi); s_e2 = qm(s_e, iphi)   # rhombohedron edge = s * |AX5|
def along(E):   # E = k * (some AX5 vector): return (index, k)
    for i, a in enumerate(AX5):
        if all(x == Z for x in cross(E, a)):
            k = next(qd(E[j], a[j]) for j in range(3) if a[j] != Z); return i, k
i1, k1 = along(E1); i2, k2 = along(E2)
three_phi = qm(qr(3), PHI)
edge_identity = dict(edge1_over_e=qs_(qd(k1, s_e)), edge2_over_e=qs_(qd(k2, s_e)), equals_3phi=(qd(k1, s_e) == three_phi or qd(k1, s_e) == qn(three_phi)),
                     three_phi_equals_3_plus_3_over_phi=three_phi == qa(qr(3), qm(qr(3), iphi)))
# out-of-plane edges w (the other four five-fold axes, either sign) with lengths L in {e, e/phi}; height along n
gap_n = qs(dot(o, n), qm(qr(2), d))                                  # gap * |n|
nn = dot(n, n); half = qm(gap_n, qr(Fr(1, 2)))
cands = []
for i, a in enumerate(AX5):
    if i in (i1, i2): continue
    for sg in (1, -1):
        w = vmul(a, qr(sg))
        for Lname, sL in (('e', s_e), ('e/phi', s_e2)):
            h = qm(sL, dot(w, n))                                    # height * |n|
            if sgn(h) <= 0: continue
            shift = vsub(vmul(w, sL), vmul(n, qd(qm(sL, dot(w, n)), nn)))   # sideways shift of the top face (exact vector)
            cands.append(dict(axis=i, sign=sg, L=Lname, height_is_half_gap=h == half, height=qf(h) / qf(nn) ** .5,
                              shift=[qs_(x) for x in shift], shift_len=qf(dot(shift, shift)) ** .5, _shift=shift, _wL=vmul(w, sL)))
half_layers = [c for c in cands if c['height_is_half_gap']]
# rhombohedron or brick? (shape of the layer's e x e tile pushed by w): oblate/prolate by the angle sign
for c in half_layers:
    c['ee_piece'] = 'rhombohedron' if c['L'] == 'e' else 'brick (e, e, e/phi)'
pairs = []
for a_, b_ in itertools.combinations_with_replacement(range(len(half_layers)), 2):
    sa, sb = half_layers[a_]['_shift'], half_layers[b_]['_shift']
    if all(x == Z for x in vadd(sa, sb)): pairs.append((a_, b_))
# side view: section plane spanned by n and the first half-layer's shift
hl = half_layers[0]; sh = hl['_shift']
nf = np.array([qf(x) for x in n]); nf /= np.linalg.norm(nf); shf = np.array([qf(x) for x in sh]); su = shf / np.linalg.norm(shf)
Af = np.array([qf(x) for x in A]); Pf = lambda v: [float((np.array([qf(x) for x in v]) - Af) @ su), float((np.array([qf(x) for x in v]) - Af) @ nf)]
face_ext = [Pf(v) for v in FA]
# face plane 2D coords for the tiling: basis along E1 and the in-plane perpendicular
e1f = np.array([qf(x) for x in E1]); e2f = np.array([qf(x) for x in E2]); bx = e1f / np.linalg.norm(e1f); by = np.cross(nf, bx)
F2 = lambda vec: [float(vec @ bx), float(vec @ by)]
ef = qf(s_e) * np.linalg.norm([qf(x) for x in AX5[0]])
order = [1, 1, 1, 1 / ((1 + 5 ** .5) / 2)] * 1
seq = [ef] * 3 + [ef / ((1 + 5 ** .5) / 2)] * 3                      # 3 long then 3 short along each edge
tiles = []; cum1 = np.cumsum([0] + seq); cum2 = np.cumsum([0] + seq)
u1h, u2h = e1f / np.linalg.norm(e1f), e2f / np.linalg.norm(e2f)
for i in range(6):
    for j in range(6):
        p0 = cum1[i] * u1h + cum2[j] * u2h
        P = [p0, p0 + seq[i] * u1h, p0 + seq[i] * u1h + seq[j] * u2h, p0 + seq[j] * u2h]
        kind = 'rhombus e' if (i < 3 and j < 3) else ('rhombus e/phi' if (i >= 3 and j >= 3) else 'parallelogram e x e/phi')
        tiles.append(dict(kind=kind, p=[F2(x) for x in P]))
from collections import Counter
counts = dict(Counter(t['kind'] for t in tiles))
# exact check of the tiling's total area: 9 e^2 + 9 e^2/phi^2 + 18 e^2/phi (times sin of the face angle) = (3phi e)^2 (times the same)
area_ok = qa(qa(qr(9), qm(qr(9), qm(iphi, iphi))), qm(qr(18), iphi)) == qm(three_phi, three_phi)
side = dict(face=[Pf(A), Pf(Cc)] if False else None)
out = dict(mark=MARK, step=2, edge_identity=edge_identity, face_angle_deg=float(np.degrees(np.arccos(abs(u1h @ u2h)))),
           e=ef, gap=qf(gap_n) / qf(nn) ** .5, half_layers=[{k: v for k, v in c.items() if not k.startswith('_')} for c in half_layers],
           closing_pairs=[[half_layers[a]['axis'], half_layers[a]['sign'], half_layers[a]['L'], half_layers[b]['axis'], half_layers[b]['sign'], half_layers[b]['L']] for a, b in pairs],
           tiling_counts=counts, tiling_area_exact=area_ok,
           draw=dict(tiles=tiles, face=[F2(np.array([qf(x) for x in v]) - Af) for v in (A, B, Cc, D_)],
                     side_face_extent=[min(p[0] for p in face_ext), max(p[0] for p in face_ext)],
                     side_shift=[float(shf @ su), float(shf @ nf) if False else 0.0], gap=qf(gap_n) / qf(nn) ** .5,
                     layer_h=hl['height'], layers=[{k: v for k, v in half_layers[x].items() if not k.startswith('_')} for x in (pairs[0] if pairs else (0, 0))]))
# side-view shifts of the chosen pair (component along su and along n)
if pairs:
    a, b = pairs[0]; out['draw']['pair_shifts'] = [[float(np.array([qf(x) for x in half_layers[k]['_wL']]) @ su), float(np.array([qf(x) for x in half_layers[k]['_wL']]) @ nf)] for k in (a, b)]
# side views, one per closing pair: plane spanned by the face normal and that pair's sideways shift
sides = []
for a, b in pairs:
    shf_ = np.array([qf(x) for x in half_layers[a]['_shift']]); su_ = shf_ / np.linalg.norm(shf_)
    ext = [float((np.array([qf(x) for x in v]) - Af) @ su_) for v in FA]
    sides.append(dict(L=half_layers[a]['L'], piece_on_e_tiles=half_layers[a]['ee_piece'], shift=float(np.linalg.norm(shf_)),
                      face=[min(ext), max(ext)], h=half_layers[a]['height']))
out['draw']['sides'] = sides
save('step2-slab.json', out)
print(json.dumps({k: v for k, v in out.items() if k != 'draw'}, indent=1))
