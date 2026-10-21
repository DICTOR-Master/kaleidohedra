# DICTO 2026-10-21, groundwork for #46 "The DICTO Mandala of Shells" (DICTO's idea): every published DICTO shell cycle tested, EXACTLY in
# Q(sqrt5), against the three operations of the Kyushindo series (#43):
#   T  the UP step   T(S) = {x : v.x <= v.v for every corner v}                         (exact_cycle.step)
#   P  the foot-point step: hull of the foot points of S's face planes; used turned out as phi P   (exact_downward.rev)
#   rho  polarity (reciprocation); rho_s = polarity in the sphere of radius^2 s, = s * polar about the unit sphere; rho P = T rho (Lemma 3)
# and scaling. For each pair of successive stations A -> B we test B = c*A, B = c*T(A), B = c*P(A), B = c*polar(A) and B = c*rect(A)
# (edge midpoints) for an exact c in Q(sqrt5) (corner sets compared exactly). Labels: 'scale' (c != 1), 'T' (c = 1), 'phiP' (c = phi),
# 'rho' (B = s*polar(A): polarity in the sphere of radius^2 s; then also B = c*T(A) when A has one corner radius), 'T x c' / 'P x c'
# (a scaled step that is not a polarity), 'other' (none of these; the operation is described in one line from the paper).
# Stations are built exactly from the definitions in the papers (sizes and contacts as stated there), and each construction is checked
# against the paper's own stated numbers (edges, contacts, closures). Then: links between cycles (same orbit, polar twins, sub-sequence,
# scaling), and the missing cell: the DICTO OTT under T, k <= 4.
# usage: python3 mapping.py <studies/2026-10-19-five-fold-octet> <2026-10-20-ott-rays/cut8-exact.json>
import sys, os
FIVE = sys.argv[1]; CUT = os.path.abspath(sys.argv[2]); HERE = os.path.dirname(os.path.abspath(__file__))
NC = os.path.join(HERE, '..', '2026-10-21-new-cycles', 'nc_common.py')
exec(open(NC).read())
from fractions import Fraction as Fr
t00 = time.time()
Z, ONE, H2 = Q5(0), Q5(1), Q5(Fr(1, 2))
R5 = Q5(0, 1)
GG = G                                                     # the 60 rotations of the #39 frame (I of edge 1, ID of radius phi)
# ---------------------------------------------------------------- exact tools
S_ = lambda c, S: [tuple(c * x for x in v) for v in S]
def key(S): return frozenset(S)
_memo = {}
def memo(tag, S, f):
    k = (tag, key(S))
    if k not in _memo: _memo[k] = f(S)
    return _memo[k]
Tc = lambda S: memo('T', S, lambda S: step(list(S))[0])
Pc = lambda S: memo('P', S, lambda S: corners(rev(list(S))))
Rc = lambda S: memo('R', S, lambda S: polar(list(S)))
def edges_of(S):
    C, F = polytope(solid(list(S))); E = set()
    for o, _ in F:
        for a, b in zip(o, o[1:] + o[:1]): E.add(frozenset((C[a], C[b])))
    return [tuple(e) for e in E]
Mc = lambda S: memo('M', S, lambda S: list(dict.fromkeys(tuple((a[i] + b[i]) / 2 for i in range(3)) for a, b in edges_of(S))))
FC = lambda S: memo('F', S, lambda S: polytope(solid(list(S))))
def sim(A, B):
    """exact c > 0 with c*A = B as corner sets, else None"""
    if len(A) != len(B): return None
    b0 = max(B, key=lambda v: dot(v, v).f()); sb = set(B)
    for a in A:
        if all(x == Z for x in cross(a, b0)) and dot(a, b0).sign() > 0:
            i = next(i for i in range(3) if a[i] != Z); c = b0[i] / a[i]
            if {tuple(c * x for x in v) for v in A} == sb: return c
    return None
def nf(S):
    r = max(dot(v, v).f() for v in S) ** .5; k = 0
    while r * PHI.f() ** -k > 1.7: k += 1
    while r * PHI.f() ** -k < 0.6: k -= 1
    for X_ in (S, S_(ONE / pw(k) if k >= 0 else pw(-k), S), S_(Q5(7), S)):
        try: C, F = FC(X_); return len(C), len(F)
        except Exception: pass
    print(f'NOTE face count not reached for a station of {len(S)} corners (float guessing failed at three scales)', flush=True); return len(S), None
def fkinds(S):
    C, F, K = kinds(list(S)); return {str(s): sum(c for k, c in K.items() if k[0] == s) for s in sorted({k[0] for k in K})}, len(K)
def tight(A, B):
    """least c with A inside c*B, exactly (max over corners of A and faces n.x = d of B of n.v/d)"""
    best = None
    for n, d in solid(list(B)):
        for v in A:
            r = dot(n, v) / d
            if best is None or (r - best).sign() > 0: best = r
    return best
def on_faces(A, B):
    H = solid(list(B)); return sum(1 for v in A if any((dot(n, v) - d) == Z for n, d in H))
L = lambda c: c is not None
eqq = lambda a, b: a is not None and b is not None and a == b
def fq(c): return f'{c!r} = {c.f():.6f}' if c is not None else 'none'
def relate(A, B):
    out = {'scale': sim(A, B), 'T': sim(Tc(A), B), 'P': sim(Pc(A), B), 'rho': sim(Rc(A), B)}
    out['rect'] = sim(Mc(A), B) if not any(out.values()) else None
    return out
def label(r):
    if r['scale'] is not None: return 'same' if r['scale'] == ONE else 'scale'
    if eqq(r['T'], ONE): return 'T'
    if eqq(r['P'], PHI): return 'phiP'
    if r['rho'] is not None: return 'rho'
    if eqq(r['P'], ONE): return 'P'
    if r['T'] is not None: return 'T x c'
    if r['P'] is not None: return 'P x c'
    if r['rect'] is not None: return 'rect x c'
    return 'other'
def show(r): return ', '.join(f'{k} c = {fq(v)}' for k, v in r.items() if v is not None) or 'no exact T / P / rho / scale / rect relation'
# ---------------------------------------------------------------- exact solids, #39 frame (I of edge 1, corners (0, +-1/2, +-phi/2) cyclic)
I1 = list(I); ID1 = list(ID)                                   # ID: edge 1, radius phi (= 2 x the edge midpoints of I)
CI_, FI_ = polytope(solid(I1)); triI = [[CI_[j] for j in o] for o, _ in FI_]
Dc = [cent(t) for t in triI]                                   # face centres of I(1): a dodecahedron of edge phi/3
ED_I = [(a, b) for a in I1 for b in I1 if a != b and dot(sub(a, b), sub(a, b)) == ONE]
TI1 = list(dict.fromkeys(tuple(2 * a[i] + b[i] for i in range(3)) for a, b in ED_I))   # truncated icosahedron of edge 1 (I(3) cut at thirds)
Iso = lambda a: S_(a, I1); Dod = lambda a: S_(Q5(3) * a / PHI, Dc); IDo = lambda a: S_(a, ID1); TIo = lambda a: S_(a, TI1)
def e2(S): return sorted({dot(sub(a, b), sub(a, b)) for a, b in edges_of(S)}, key=lambda q: q.f())
ok(symmetric(I1, GG) and symmetric(Dc, GG) and symmetric(TI1, GG), 'frame: I, its face centres (D) and TI fixed by the 60 rotations of the #39 frame')
ok(e2(Iso(1)) == [ONE] and e2(Dod(1)) == [ONE] and e2(IDo(1)) == [ONE] and e2(TIo(1)) == [ONE] and len(TI1) == 60,
   'exact unit edges: I(1), D(1) = (3/phi) x face centres of I(1), ID(1) = sums of I(1) edge ends, TI(1) = 2a+b over I(1) edges (60 corners)')
ST = {}                                                        # station id -> dict
def station(sid, S, name, paper, cycle, star=None):
    S = list(dict.fromkeys(S)); ST[sid] = {'S': S, 'name': name, 'paper': paper, 'cycle': cycle, 'star': star}; return S
CYC = {}                                                       # cycle -> list of station ids, inside to outside (or in the paper's order)
EDGE_NOTE = {}                                                 # (a, b) -> one-line description of a non-T/P/rho step, from the paper
# ---------------------------------------------------------------- #22 Chain of Karma: I(1/phi) < D(1) < I(phi^2) < D(phi^3)
P22 = '#22 Chain of Karma (10.5281/zenodo.23310541)'
CYC['#22'] = [station('22.I', Iso(ONE / PHI), 'I', P22, '#22'), station('22.D', Dod(ONE), 'D', P22, '#22'),
              station('22.I2', Iso(PHI * PHI), 'I', P22, '#22'), station('22.D3', Dod(pw(3)), 'D', P22, '#22')] and ['22.I', '22.D', '22.I2', '22.D3']
EDGE_NOTE[('22.I', '22.D')] = 'face-on placement: 12 pentagonal pyramids point-down on D faces, apices on I corners (+30 AXE, 20 CLEO)'
EDGE_NOTE[('22.D', '22.I2')] = 'Lotus seed: 12 I(1) on the corners cut by D faces (J2 in, J11 out) + 30 AXE + 20 FUJI'
EDGE_NOTE[('22.I2', '22.D3')] = 'the first decomposition again, phi^3 larger'
inr = lambda S: min((d / dot(n, n) * d for n, d in solid(S)), key=lambda q: q.f())         # squared inradius
# the paper's numbers: D inradius 1.113516 - J2 height 0.525731 = I(1/phi) circumradius 0.587785 (squared radii exact)
ok(all(dot(v, v) == (PHI * PHI + 1) / (4 * PHI * PHI) for v in Iso(ONE / PHI)) and abs(inr(Dod(ONE)).f() ** .5 - 1.113516) < 1e-6,
   '#22: I(1/phi) circumradius^2 = (phi^2+1)/(4 phi^2) (0.587785); D(1) inradius 1.113516 as stated')
# ---------------------------------------------------------------- #23 Spheres of Dharma: I(1/phi) < ID(phi/2) < D(1) < TI(1/phi) < [H] < RT < I(phi^2)
P23 = '#23 Spheres of Dharma (10.5281/zenodo.23310833)'
I_D, ID_D, D_D, TI_D, I2_D = Iso(ONE / PHI), IDo(PHI / 2), Dod(ONE), TIo(ONE / PHI), Iso(PHI * PHI)
cRT = tight(TI_D, RT); RT_D = S_(cRT, RT)                      # RT = T(ID) shape, at the size holding the cage's 60 corners on its faces
ok(on_faces(TI_D, RT_D) == 60 and on_faces(D_D, TI_D) == 20 and set(e2(RT_D)) == {Q5(Fr(45, 4), Fr(-18, 4))},
   f'#23: TI(1/phi) has all 60 corners on the faces of RT; D(1) corners on TI faces (20, the hexagon centres); RT edge^2 = (45 - 18 sqrt5)/4 exactly, as stated (RT = {fq(cRT)} x T(ID(1)))')
HECA = polar(OG)                                               # the DICTO Hecatodihedron (#28), up to scale
hr = {}
for v in HECA: hr.setdefault(dot(v, v), []).append(v)
cH = next(c for c in (sim(sub60, TI_D) for sub60 in hr.values() if len(sub60) == 60) if c is not None); H_D = S_(cH, HECA)
ok(set(TI_D) <= set(H_D) and on_faces(TI_D, H_D) == 60 and len(H_D) == 80, '#23: the Hecatodihedron stage H = c x polar(OG) holds the TI(1/phi) as 60 of its 80 corners (TI on the faces of H)')
ok(all(inside(a, b)[0] for a, b in [(I_D, ID_D), (ID_D, D_D), (D_D, TI_D), (TI_D, H_D), (H_D, RT_D), (RT_D, I2_D)]), '#23: the seven stations nest exactly, I(1/phi) < ID < D < TI < H < RT < I(phi^2)')
CYC['#23'] = []
for sid, S, nm in [('23.I', I_D, 'I'), ('23.ID', ID_D, 'ID'), ('23.D', D_D, 'D'), ('23.TI', TI_D, 'TI'), ('23.H', H_D, 'H'), ('23.RT', RT_D, 'RT'), ('23.I3', I2_D, 'I')]:
    station(sid, S, nm, P23, '#23'); CYC['#23'].append(sid)
EDGE_NOTE.update({('23.I', '23.ID'): 'loose nest (12 pentagonal pyramids + 20 twisted triangular frusta)', ('23.ID', '23.D'): 'D = ID + 20 triangular corner pyramids (ID is D rectified)',
                  ('23.D', '23.TI'): 'cage wraps D, D corners on hexagon centres (12 twisted frusta + 30 t1)', ('23.TI', '23.H'): 'a Shield (low pyramid) on each hexagon',
                  ('23.H', '23.RT'): 'caps close to the RT (TI corners on RT faces)', ('23.RT', '23.I3'): 'loose nest: 30 edge + 20 face pieces'})
# ---------------------------------------------------------------- #32 Inverted Shells = polar (unit sphere, Dharma frame) of the seven #23 stations, reversed
P32 = '#32 Inverted Shells (10.5281/zenodo.23405029)'
CYC['#32'] = []
NM32 = {'23.I3': 'D', '23.RT': 'ID', '23.H': 'OG', '23.TI': 'PD', '23.D': 'I', '23.ID': 'RT', '23.I': 'D'}
for s in reversed(CYC['#23']):
    sid = '32.' + s[3:]; station(sid, Rc(ST[s]['S']), NM32[s], P32, '#32'); CYC['#32'].append(sid)
c32 = sim(ST['32.I3']['S'], ST['32.I']['S'])
ok(c32 == pw(3) and sim(ST['32.H']['S'], OG) is not None and all(inside(ST[a]['S'], ST[b]['S'])[0] for a, b in zip(CYC['#32'], CYC['#32'][1:])),
   f'#32: polar of #23 reversed nests exactly, D < ID < OG < PD < I < RT < D*phi^3 (closure c = {fq(c32)} = phi^3), its third station is the OG exactly up to scale')
for a, b in zip(CYC['#32'], CYC['#32'][1:]): EDGE_NOTE[(a, b)] = 'the polar of a #23 layer (cones over faces of the inner solid)'
# ---------------------------------------------------------------- #33 Double Vision: #23 and rho_s(#23) in one space, s = phi^2/4 (ends) or 3 phi^2/4 (middle)
P33 = '#33 Double Vision (10.5281/zenodo.23407106)'
sE, sM = PHI * PHI / 4, 3 * PHI * PHI / 4
ok(set(S_(sE, Rc(I_D))) == set(D_D) and set(S_(sE, Rc(D_D))) == set(I_D), '#33 ends setting rho^2 = phi^2/4: rho maps I(1/phi) <-> D(1) exactly (the two cycles share I and D)')
ok(set(S_(sM, Rc(ID_D))) == set(RT_D) and set(S_(sM, Rc(RT_D))) == set(ID_D), '#33 middle setting rho^2 = 3 phi^2/4: rho maps ID <-> RT exactly (the two cycles share ID and RT)')
ok(sM / sE == Q5(3), '#33: the two settings differ by exactly 3 (not a power of phi), so no sphere gives both')
for setting, s in [('ends', sE), ('middle', sM)]:
    CYC[f'#33 {setting}'] = []
    U = [(ST[x]['S'], ST[x]['name'], 'Dharma') for x in CYC['#23']] + [(S_(s * pw(3 * k), Rc(ST[x]['S'])), ST[x]['name'] + '*', 'polar') for x in CYC['#23'] for k in (0, 1)]
    seen = {}
    for S, nm, src in U:
        kk = key(S)
        if kk in seen: seen[kk][2].append(src); continue
        seen[kk] = [S, nm, [src]]
    rad = lambda S: max(dot(v, v).f() for v in S)
    lo, hi = rad(I_D) * 0.999, rad(I2_D) * 1.001
    order = sorted([v for v in seen.values() if lo <= rad(v[0]) <= hi], key=lambda v: (rad(v[0]), len(v[0])))
    for j, (S, nm, src) in enumerate(order):
        sid = f'33{setting[0]}.{j}'; nm2 = {'I*': 'D', 'ID*': 'RT', 'D*': 'I', 'TI*': 'PD', 'H*': 'OG', 'RT*': 'ID'}.get(nm, nm)
        station(sid, S, nm2 + (' (shared)' if len(src) > 1 else ''), P33, f'#33 {setting}'); CYC[f'#33 {setting}'].append(sid)
    ok(True, f"#33 {setting}: the union between I(1/phi) and I(phi^2) has {len(order)} distinct stations, shared: {[ST[x]['name'] for x in CYC[f'#33 {setting}'] if 'shared' in ST[x]['name']]}")
# ---------------------------------------------------------------- #34 Progenitors: I < ID < O < rTI < TI < H < jtI < RT < I phi^3 (Dharma sizes)
P34 = '#34 Progenitors (10.5281/zenodo.23413184)'
O_34 = S_(sM, Rc(H_D))                                         # O at 3 phi^2/4: the middle-setting polar of H
rTI = Mc(TI_D)
jtI0 = Rc(rTI); cj = tight(H_D, jtI0); jtI = S_(cj, jtI0)
ok(on_faces(ID_D, O_34) == 30 and len(rTI) == 90 and on_faces(H_D, jtI) == 80 and on_faces(jtI, RT_D) == 80 and len(jtI) == 92,
   '#34 contacts as stated: 30 ID corners on O faces; rTI = edge midpoints of TI (90); 80 H corners on jtI faces; 80 jtI corners on RT faces; jtI 92 corners')
CH34 = [('34.I', I_D, 'I'), ('34.ID', ID_D, 'ID'), ('34.O', O_34, 'OG'), ('34.rTI', rTI, 'rTI'), ('34.TI', TI_D, 'TI'), ('34.H', H_D, 'H'), ('34.jtI', jtI, 'jtI'), ('34.RT', RT_D, 'RT'), ('34.I3', I2_D, 'I')]
ok(all(inside(a[1], b[1])[0] for a, b in zip(CH34, CH34[1:])), '#34: the nine stations nest exactly')
CYC['#34'] = [station(s, S, n, P34, '#34') and s for s, S, n in CH34]
EDGE_NOTE.update({('34.I', '34.ID'): 'loose nest', ('34.ID', '34.O'): 'O wraps ID (30 corners on O faces); O = middle-setting polar of H',
                  ('34.O', '34.rTI'): 'loose nest', ('34.rTI', '34.TI'): 'rTI is TI rectified (corners on TI edges)', ('34.TI', '34.H'): 'Shields on the hexagons',
                  ('34.H', '34.jtI'): 'H corners on jtI faces (jtI = dual of rTI)', ('34.jtI', '34.RT'): 'jtI corners on RT faces', ('34.RT', '34.I3'): 'loose nest'})
# ---------------------------------------------------------------- #35 Vajrayana: I < Cleo star < D' < ID < O < rTI < TI < H < jtI < RT < M < I phi^3
P35 = '#35 Vajrayana (10.5281/zenodo.23429911)'
tips = S_(Q5(2), Pc(I_D))                                      # Cleo-Ico spikes as tall as the core cones: tips at 2 x the foot points
Dp = S_(Q5(Fr(2, 3)), D_D)
ok(set(tips) == set(Dp), "#35: the Cleo star's 20 tips (2 x the face foot points of I) are exactly (2/3) x D(1) = D'")
five = [v for v in RT_D if any(all(x == Z for x in cross(v, w)) for w in I_D)]
Mx = corners(five + S_(PHI * PHI, Dc))
mC, mF = nf(Mx)
ok(len(five) == 12 and mC == 32 and mF == 60 and on_faces(RT_D, Mx) >= 12 and on_faces(Mx, I2_D) == 20,
   '#35: M = hull(12 five-fold RT corners, 20 face centres of I(phi^2)): 32 corners, 60 faces, touching RT and I phi^3 (20 corners on its faces)')
CH35 = [('35.I', I_D, 'I'), ('35.star', I_D + tips, 'Cleo star'), ('35.Dp', Dp, 'D')] + [(s.replace('34', '35'), S, n) for s, S, n in CH34[1:8]] + [('35.M', Mx, 'M'), ('35.I3', I2_D, 'I')]
hull_ok = set(corners(I_D + tips)) == set(Dp)
ok(hull_ok and all(inside(a[1], b[1])[0] for a, b in zip(CH35[2:], CH35[3:])) and inside(I_D, Dp)[0], "#35: the hull of the Cleo star is D' exactly; the twelve stations nest exactly")
CYC['#35'] = []
for s, S, n in CH35:
    station(s, S, n, P35, '#35', star=('35.I', 'Dp') if s == '35.star' else None); CYC['#35'].append(s)
EDGE_NOTE.update({('35.I', '35.star'): 'Kleetope: 20 Cleo-Ico spikes raised on the faces (tips at 2x the face distance)', ('35.star', '35.Dp'): "convex hull of the tips (+12 inward pyramids, 30 valley tetrahedra)",
                  ('35.Dp', '35.ID'): 'loose nest', ('35.RT', '35.M'): 'hull of RT five-fold corners and the face centres of I phi^3', ('35.M', '35.I3'): 'M corners on I phi^3 face centres'})
for (a, b), v in list(EDGE_NOTE.items()):
    if a.startswith('34.'): EDGE_NOTE[('35.' + a[3:], '35.' + b[3:])] = v
EDGE_NOTE[('35.ID', '35.O')] = EDGE_NOTE[('34.ID', '34.O')]
# ---------------------------------------------------------------- #38 Universal PiTet: ID -> RT -> GTI -> FPD -> ID x 10/phi^4 (T)
P38 = '#38 Universal PiTet (10.5281/zenodo.23463305)'
lam = Q5(35, -15)
U38 = [ID1]
for _ in range(4): U38.append(Tc(U38[-1]))
ok(set(U38[4]) == set(S_(lam, ID1)) and lam == Q5(10) / pw(4), '#38: T^4(ID) = (10/phi^4) ID exactly, 10/phi^4 = 35 - 15 sqrt5')
CYC['#38'] = [station(f'38.{k}', U38[k], ['ID', 'RT', 'GTI', 'FPD', 'ID'][k], P38, '#38') and f'38.{k}' for k in range(5)]
s38 = Q5(15, -5)
def Tpow(k):
    m, j = divmod(k, 4); c = ONE
    for _ in range(m): c = c * lam
    return S_(c, U38[j])
ok(all(set(S_(s38, Rc(U38[k]))) == set(Tpow(5 - k)) for k in range(5)),
   '#38 (iv): rho in the sphere of radius^2 15 - 5 sqrt5 (the GTI circumsphere) maps T^k(ID) to T^(5-k)(ID) exactly, k = 0..4 (ID <-> c RT, RT <-> c ID, GTI <-> FPD)')
# ---------------------------------------------------------------- #38a Kepler-Poinsot-UP: I(1) -> great stellated dodecahedron -> D1 = D(phi) -> small stellated dodecahedron -> I(phi^3)
P38a = '#38a Kepler-Poinsot-UP (10.5281/zenodo.23464021)'
gsd_tips = S_(Q5(3), Pc(Iso(ONE))); D1 = Dod(PHI)
ssd_tips = S_(R5, Pc(D1)); I3 = Iso(pw(3))
ok(set(gsd_tips) == set(D1) and set(ssd_tips) == set(I3), '#38a: spikes on I(1) to 3x the face distance have tips = D(phi) exactly; spires on D(phi) to sqrt5 x the face distance have tips = I(phi^3) exactly')
CYC['#38a'] = []
for s, S, n, st in [('38a.I', Iso(ONE), 'I', None), ('38a.gsd', Iso(ONE) + gsd_tips, 'great stellated dodecahedron', ('38a.I', '38a.D1')), ('38a.D1', D1, 'D', None),
                    ('38a.ssd', D1 + ssd_tips, 'small stellated dodecahedron', ('38a.D1', '38a.I3')), ('38a.I3', I3, 'I', None)]:
    station(s, S, n, P38a, '#38a', star=st); CYC['#38a'].append(s)
EDGE_NOTE.update({('38a.I', '38a.gsd'): 'stellation: a pyramid on each face to 3x the face distance (20 CLEO)', ('38a.gsd', '38a.D1'): 'convex hull of the star (+12 caps, 30 AXE)',
                  ('38a.D1', '38a.ssd'): 'stellation: a spire on each face to sqrt5 x the face distance', ('38a.ssd', '38a.I3'): 'convex hull of the star (+20 inward pyramids, 30 valley tetrahedra)'})
# ---------------------------------------------------------------- #39 OG family: T^k(OG) up, P^k(OG) down, k <= 4
P39 = '#39 OG Family both ways (10.5281/zenodo.23488944)'
UP = [OG]; DN = [OG]
for k in range(4): UP.append(Tc(UP[-1])); DN.append(Pc(DN[-1]))
ok([len(x) for x in UP] == [102, 92, 180, 212, 270] and [len(x) for x in DN] == [102, 80, 132, 140, 162], '#39: corner counts OG, KRE, PHE, TPP, DPHP = 102, 92, 180, 212, 270 and TPH, TQH, TQP, TQHD = 80, 132, 140, 162, as published')
ok(all(set(Tc(DN[k + 1])) == set(DN[k]) for k in range(4)), '#39: T undoes P exactly on all four downward steps (T(P(S)) = S)')
CYC['#39 up'] = [station(f'39u.{k}', UP[k], ['OG', 'KRE', 'PHE', 'TPP', 'DPHP'][k], P39, '#39 up') and f'39u.{k}' for k in range(5)]
CYC['#39 down'] = [station(f'39d.{k}', DN[k], ['OG', 'TPH', 'TQH', 'TQP', 'TQHD'][k], P39, '#39 down') and f'39d.{k}' for k in range(5)]
print(f'solids built ({time.time() - t00:.0f} s)', flush=True)
# ---------------------------------------------------------------- #43 Cleo Towers (beats 0 1 2 4 7 12 of T^k ID), Polar Cleo Towers, OG turned out and its polar
P43 = '#43 Kyushindo Cores (10.5281/zenodo.23532013)'
B = [0, 1, 2, 4, 7, 12]
CYC['Cleo Towers'] = [station(f'CT.{b}', Tpow(b), ['ID', 'RT', 'GTI', 'FPD'][b % 4], P43, 'Cleo Towers') and f'CT.{b}' for b in B]
ok(set(Tc(Tpow(11))) == set(Tpow(12)), 'Cleo Towers: T^(4m+j)(ID) = (10/phi^4)^m T^j(ID) exactly (checked at beat 12 = T(beat 11))')
for a, b in zip(B, B[1:]): EDGE_NOTE[(f'CT.{a}', f'CT.{b}')] = f'T^{b - a} (a fused shell of {b - a} beats)'
CYC['Polar Cleo Towers'] = [station(f'PCT.{b}', S_(s38, Rc(Tpow(b))), '', P43, 'Polar Cleo Towers') and f'PCT.{b}' for b in B]
for b in B:
    m = 5 - b; ST[f'PCT.{b}']['name'] = ['ID', 'RT', 'GTI', 'FPD'][m % 4]
ok(all(sim(Tpow(5 - b) if 5 - b >= 0 else Tpow((5 - b) % 4), ST[f'PCT.{b}']['S']) is not None for b in B) and all(set(ST[f'PCT.{b}']['S']) == set(Tpow(5 - b)) for b in B if 5 - b >= 0),
   'Polar Cleo Towers: rho (radius^2 15 - 5 sqrt5) of beat b is beat 5 - b exactly (b <= 5), and of the UP orbit up to scale for b = 7, 12')
SK = [S_(pw(k), DN[k]) for k in range(5)]
ok(all(set(S_(PHI, Pc(SK[k]))) == set(SK[k + 1]) for k in range(4)), '#43 OG turned out: S_(k+1) = phi P(S_k) exactly, so S_k = phi^k x (#39 down_k), k <= 4')
CYC['OG turned out'] = [station(f'OGt.{k}', SK[k], ['OG', 'TPH', 'TQH', 'TQP', 'TQHD'][k], P43, 'OG turned out') and f'OGt.{k}' for k in range(5)]
PS = [Rc(SK[k]) for k in range(5)]; HT = [Rc(OG)]
for k in range(4): HT.append(Tc(HT[-1]))
ok(all(set(PS[k]) == set(S_(Q5(1) / pw(k), HT[k])) for k in range(5)), '#43 Corollary 2: polar(S_k) = phi^-k T^k(H) exactly, k <= 4 (H = polar OG)')
CYC['OG turned out, polar'] = [station(f'OGp.{k}', PS[k], ['H', 'T H', 'T^2 H', 'T^3 H', 'T^4 H'][k], P43, 'OG turned out, polar') and f'OGp.{k}' for k in range(5)]
# ---------------------------------------------------------------- the new cycles (2026-10-21-new-cycles; unpublished)
PNC = 'new cycles 2026-10-21 (study, unpublished)'
A = [ID1]
for k in range(7): A.append(S_(PHI, Pc(A[-1])))
ok(all(set(A[k]) == set(S_(pw(k) / lam, U38[4 - k])) for k in range(1, 5)), 'new A, CLEO turned out: S_k = (phi^k / lam) T^(4-k)(ID) exactly for k = 1..4, i.e. #38 run backwards (P undoes T on the UP orbit)')
CYC['CLEO turned out'] = [station(f'A.{k}', A[k], ['ID', 'FPD', 'GTI', 'RT'][k % 4], PNC, 'CLEO turned out') and f'A.{k}' for k in range(5)]
BP = [Rc(OG)]
for k in range(4): BP.append(Pc(BP[-1]))
ok(all(set(BP[k]) == set(Rc(UP[k])) for k in range(5)), 'new B: P^k(H) = polar(T^k OG) exactly, k <= 4 (Lemma 3)')
CYC['polar of OG up'] = [station(f'B.{k}', BP[k], ['H', 'P H', 'P^2 H', 'P^3 H', 'P^4 H'][k], PNC, 'polar of OG up') and f'B.{k}' for k in range(5)]
print(f'#43 and new A, B built ({time.time() - t00:.0f} s)', flush=True)
# ---------------------------------------------------------------- Task 1: successive stations
EDGES = []
for cyc, ids in CYC.items():
    print(f'--- {cyc}', flush=True)
    for a, b in zip(ids, ids[1:]):
        sa, sb = ST[a], ST[b]
        if sa['star'] or sb['star']:
            note = EDGE_NOTE.get((a, b), 'star step'); hull = sb['S'] if sb['star'] is None else None
            if sb['star']:
                base = ST[sb['star'][0]]['S']; extra = [v for v in sb['S'] if v not in set(base)]
                r = relate(base, extra); lab = 'other'
                ok(True, f'{cyc}: {a} -> {b}: other ({note}); the tips alone: {show(r)}')
            else:
                hl = corners(sa['S']); r = {'scale': sim(hl, sb['S'])}; lab = 'other'
                ok(eqq(r['scale'], ONE), f'{cyc}: {a} -> {b}: other ({note}); hull of the star = {sb["name"]} exactly')
            EDGES.append({'from': a, 'to': b, 'cycle': cyc, 'op': lab, 'note': note, 'factors': {k: repr(v) for k, v in r.items() if v is not None}, 'exact': True}); continue
        r = relate(sa['S'], sb['S']); lab = label(r)
        if cyc in ('Cleo Towers', 'Polar Cleo Towers') and lab not in ('T', 'P'):
            n = int(b.split('.')[1]) - int(a.split('.')[1]); X_ = sa['S']
            for _ in range(n): X_ = Tc(X_) if cyc == 'Cleo Towers' else Pc(X_)
            cn = sim(X_, sb['S'])
            if eqq(cn, ONE): lab = ('T^' if cyc == 'Cleo Towers' else 'P^') + str(n); r['T^n' if cyc == 'Cleo Towers' else 'P^n'] = cn
        note = EDGE_NOTE.get((a, b), '') if lab in ('other', 'rect', 'rho', 'T x c', 'P x c', 'scale') else ''
        EDGES.append({'from': a, 'to': b, 'cycle': cyc, 'op': lab, 'note': note, 'factors': {k: repr(v) for k, v in r.items() if v is not None}, 'exact': True})
        ok(True, f'{cyc}: {a} ({sa["name"]}) -> {b} ({sb["name"]}): {lab}; {show(r)}' + (f'  [{note}]' if note else ''))
print(f'task 1 done ({time.time() - t00:.0f} s)', flush=True)
# ---------------------------------------------------------------- Task 2: links between cycles
LINKS = []
def link(a, b, kind, c, msg):
    LINKS.append({'from': a, 'to': b, 'op': kind, 'factor': repr(c) if c is not None else None, 'note': msg})
cls = []                                                       # similarity classes of convex stations
for sid, s in ST.items():
    if s['star']: continue
    for C in cls:
        if sim(ST[C[0]]['S'], s['S']) is not None: C.append(sid); break
    else: cls.append([sid])
CLASS = {sid: i for i, C in enumerate(cls) for sid in C}
for C in cls:
    print(f'class {CLASS[C[0]]}: {ST[C[0]]["name"]}: {len(ST[C[0]]["S"])} corners, stations {C}', flush=True)
DUALCL = {}
for i, C in enumerate(cls):
    for j, D_ in enumerate(cls):
        if j < i: continue
        if sim(Rc(ST[C[0]]['S']), ST[D_[0]]['S']) is not None: DUALCL[i] = j; DUALCL[j] = i
ok(True, 'dual (rho) pairs of classes: ' + ', '.join(f'{ST[cls[i][0]]["name"]} <-> {ST[cls[j][0]]["name"]}' for i, j in DUALCL.items() if i <= j))
def seqsim(X, Y, shift=0):
    """exact: Y[k] = c * X[k + shift] for one c, every k in range"""
    c = None
    for k in range(len(Y)):
        if not 0 <= k + shift < len(X): continue
        ck = sim(ST[X[k + shift]]['S'], ST[Y[k]]['S'])
        if ck is None or (c is not None and ck != c): return None
        c = ck
    return c
c = seqsim(CYC['#22'][:3], [CYC['#23'][0], CYC['#23'][2], CYC['#23'][6]])
ok(eqq(c, ONE), '#22 and #23 share their I(1/phi), D(1) and I(phi^2) exactly (the hinge of #23 section 5)'); link('#22', '#23', 'same', c, 'shared stations I(1/phi), D(1), I(phi^2): the hinge')
ok(all(set(Rc(ST[a]['S'])) == set(ST[b]['S']) for a, b in zip(CYC['#23'], reversed(CYC['#32']))), '#32 = rho(#23) station by station, order reversed (unit sphere, Dharma frame)'); link('#23', '#32', 'rho', ONE, 'polar twins, unit sphere, nesting reversed')
link('#23', '#33', 'rho', sE, '#33 ends = #23 + rho_s(#23), s = phi^2/4 (shares I, D)'); link('#23', '#33', 'rho', sM, '#33 middle = #23 + rho_s(#23), s = 3 phi^2/4 (shares ID, RT)')
link('#32', '#33', 'scale', sE, '#33 polar half = #32 scaled by s')
ok(set(O_34) == set(S_(sM, ST['32.H']['S'])), "#34's O is #32's OG station scaled by 3 phi^2/4 exactly, i.e. the middle-setting polar of #23's H (#33 middle)"); link('#33 middle', '#34', 'rho', sM, "O = rho_s(H), s = 3 phi^2/4: #34 takes #33 middle's OG station into #23")
k34 = [s for s in CYC['#34'] if s in ('34.I', '34.ID', '34.TI', '34.H', '34.RT', '34.I3')]
ok(all(set(ST[s]['S']) == set(ST['23.' + s[3:]]['S']) for s in k34), '#34 contains six of the seven #23 stations exactly (all but D); adds O, rTI, jtI'); link('#23', '#34', 'sub-sequence', ONE, '#34 = #23 with D replaced by O, plus rTI (TI rectified) and jtI (its dual)')
ok(all(set(ST['35.' + s[3:]]['S']) == set(ST[s]['S']) for s in CYC['#34']), '#35 contains all nine #34 stations exactly (adds Cleo star, D\', M)'); link('#34', '#35', 'sub-sequence', ONE, "#35 = #34 + Cleo star, D' = (2/3) D, M")
ok(set(Dp) == set(S_(Q5(Fr(2, 3)), ST['22.D']['S'])), "#35's D' = (2/3) x #22's D(1) exactly"); link('#22', '#35', 'scale', Q5(Fr(2, 3)), "D' = (2/3) D(1)")
c = seqsim([CYC['#22'][0], CYC['#22'][1], CYC['#22'][2]], [CYC['#38a'][0], CYC['#38a'][2], CYC['#38a'][4]])
ok(eqq(c, PHI), f'#38a hulls I(1) < D(phi) < I(phi^3) = phi x #22 stations I(1/phi) < D(1) < I(phi^2) exactly (the same orbit, c = {fq(c)})'); link('#22', '#38a', 'scale', c, 'the KP-UP hulls are the Chain of Karma, phi larger; the stars are its stellations')
ok(set(S_(Q5(Fr(3, 2)) * PHI, tips)) == set(gsd_tips) , "the Cleo star (#35, #38) and the great stellated dodecahedron (#38a) are the same Kleetope rule at heights 2 and 3 (tips at 2x and 3x the face foot points; checked: (3/2) phi x Cleo tips = GSD tips)")
link('#35', '#38a', 'other', None, 'Cleo star (tips 2x face distance) vs great stellated dodecahedron (3x): one Kleetope rule, two heights')
c1 = sim(U38[0], ST['23.ID']['S']); c2 = sim(U38[1], ST['23.RT']['S'])
ok(L(c1) and L(c2), f"#38's ID and RT are #23's ID and RT up to scale (ID x {fq(c1)}, RT x {fq(c2)}); #23's RT = {fq(sim(Tc(ST['23.ID']['S']), ST['23.RT']['S']))} x T(#23's ID)")
link('#38', '#23', 'scale', c1, 'ID and RT shared up to scale; GTI and FPD are not Archimedean TI / canonical PD')
ok(sim(U38[2], TI_D) is None and sim(U38[3], ST['32.TI']['S']) is None, "#38's GTI is not similar to #23's TI, and #38's FPD not to #32's PD (exact: different solids)")
ok(all(set(ST[f'CT.{b}']['S']) == set(Tpow(b)) for b in B), 'Cleo Towers = the #38 orbit at beats 0, 1, 2, 4, 7, 12 (a Fibonacci sub-sequence)'); link('#38', 'Cleo Towers', 'sub-sequence', ONE, 'beats 0|1|2|4|7|12 of T^k(ID)')
link('Cleo Towers', 'Polar Cleo Towers', 'rho', s38, 'rho_s, s = 15 - 5 sqrt5: beat b -> beat 5 - b; the same orbit read from the centre (self-polar)')
ok(all(set(ST[f'OGt.{k}']['S']) == set(S_(pw(k), DN[k])) for k in range(5)), 'OG turned out = phi^k x #39 down_k beat by beat'); link('#39 down', 'OG turned out', 'scale', PHI, 'beat k scaled by phi^k')
ok(all(set(ST[f'OGt.{k}']['S']) == set(S_(pw(k), DN[k])) for k in range(5)) and all(set(ST[f'B.{k}']['S']) == set(Rc(UP[k])) for k in range(5)), 'new B = rho(#39 up) station by station')
link('#39 up', 'polar of OG up', 'rho', ONE, 'P^k(H) = polar(T^k OG)'); link('OG turned out', 'OG turned out, polar', 'rho', ONE, 'polar(S_k) = phi^-k T^k(H)')
ok(all(eqq(sim(HT[k], ST[f'OGp.{k}']['S']), ONE / pw(k)) for k in range(5)), "#43's polar of the OG turned out = phi^-k x (the UP family of H) beat by beat; new B is H's DOWN family: H is the hinge (#39 read through rho)")
link('#38', 'CLEO turned out', 'reverse', ONE / lam, 'S_k = (phi^k/lam) T^(4-k) ID: #38 run backwards, phi per beat')
# OG family vs the Dharma: is #32's OG the #39 OG (same solid, scale)?
ok(sim(OG, ST['32.H']['S']) is not None and sim(OG, O_34) is not None, "#39's OG is #32's and #34's OG up to scale (one solid in all three)")
link('#32', '#39 up', 'scale', sim(OG, ST['32.H']['S']), "#32's OG station = c x #39's OG; #39 runs T and P from it")
print(f'task 2 done ({time.time() - t00:.0f} s)', flush=True)
# ---------------------------------------------------------------- the OTT (its own frame, the Cleo Towers ID of exact_cycle.py) : new C and Task 3
q = lambda s: Q5(Fr(s.split('|')[0]), Fr(s.split('|')[1]))
OTT = [tuple(q(x) for x in p) for p in json.load(open(CUT))['V']]
ns = dict(globals()); exec(open('exact_cycle.py').read().split("if __name__ == '__main__':")[1].split("    log = {")[0].replace('\n    ', '\n'), ns); IDc = ns['ID']
GA = X.rotations()
Cc = [OTT]
for k in range(4): Cc.append(S_(PHI, Pc(Cc[-1])))
cC = sim(IDc, Cc[1])
Ac = [IDc]
for k in range(3): Ac.append(S_(PHI, Pc(Ac[-1])))
ok(L(cC) and all(eqq(sim(Ac[k - 1], Cc[k]), cC) for k in range(1, 5)), f'new C, OTT turned out: C_k = {fq(cC)} x A_(k-1) exactly for k = 1..4 (A one beat behind; c = phi (sqrt5 - 1)/3)')
CYC['OTT turned out'] = [station(f'C.{k}', Cc[k], ['OTT', 'ID', 'FPD', 'GTI', 'RT'][k], PNC, 'OTT turned out') and f'C.{k}' for k in range(5)]
link('CLEO turned out', 'OTT turned out', 'scale', cC, 'C_k = c A_(k-1): one beat behind')
r = relate(OTT, Cc[1]); ok(True, f'OTT -> C_1: {label(r)}; {show(r)}')
# Task 3: the OTT under T
TO = [OTT]
for k in range(4):
    t = time.time(); TO.append(Tc(TO[-1])); print(f'built T^{k + 1}(OTT): {len(TO[-1])} corners ({time.time() - t:.0f} s)', flush=True)
TASK3 = []
SP = []
for perm in itertools.permutations(range(3)):
    for sg in itertools.product((1, -1), repeat=3): SP.append(tuple(tuple(Q5(sg[i]) if perm[i] == j else Z for j in range(3)) for i in range(3)))
for k in range(5):
    info, C, F, K = describe(TO[k]); ico = symmetric(TO[k], GA); th = sum(1 for M in SP if symmetric(TO[k], [M]))
    row = {'k': k, 'corners': info['corners'], 'faces': info['faces'], 'edges': info['edges'], 'faces_by_sides': info['faces_by_sides'], 'face_kinds': len(K),
           'face_kinds_exact': info['face_kinds_exact'], 'volume': info['volume'], 'volume_float': info['volume_float'], 'corner_radii_float': info['corner_radii_float'],
           'icosahedral': ico, 'signed_permutation_symmetries': th}
    if k:
        o, nb, wx = inside(TO[k - 1], TO[k]); row['holds_previous'] = o; row['previous_corners_outside'] = nb
        row['P_undoes_T'] = set(Pc(TO[k])) == set(TO[k - 1])
        sk = [(j, sim(Cc[j], TO[k])) for j in range(5)]; row['similar_to_OTT_turned_out_beat'] = [(j, repr(c)) for j, c in sk if c is not None]
        sa = [(nm, sim(Sx, TO[k])) for nm, Sx in [('ID', IDc)] + [(f'T^{j} ID', Sx) for j, Sx in enumerate([Tc(IDc), Tc(Tc(IDc)), Tc(Tc(Tc(IDc)))], 1)]]
        row['similar_to_UP_orbit'] = [(nm, repr(c)) for nm, c in sa if c is not None]
    TASK3.append(row)
    ok(True, f"OTT under T, k = {k}: {info['corners']} corners, {info['faces']} faces ({kind_str(K)}), {len(K)} exact face kinds, volume {info['volume_float']:.6f}, radii {info['corner_radii_float'][0]:.4f}..{info['corner_radii_float'][-1]:.4f}, "
            f"icosahedral {ico}, signed-permutation symmetries {th}" + (f"; T^{k - 1} inside T^{k}: {row['holds_previous']} (corners outside {row['previous_corners_outside']}); P(T^{k}) = T^{k - 1}: {row['P_undoes_T']}; similar to the UP orbit: {row['similar_to_UP_orbit'] or 'no'}" if k else ''))
pol = Rc(OTT); r3 = all(set(Rc(TO[k])) == set(corners(Pk)) for k, Pk in [(1, rev(pol))])
ok(r3, 'Lemma 3 check on the OTT: polar(T(OTT)) = P(polar OTT) exactly')
CYC['OTT under T'] = [station(f'OT.{k}', TO[k], 'OTT' if k == 0 else f'T^{k} OTT', 'missing cell (this study)', 'OTT under T') and f'OT.{k}' for k in range(5)]
for a, b in zip(CYC['OTT under T'], CYC['OTT under T'][1:]):
    r = relate(ST[a]['S'], ST[b]['S']); EDGES.append({'from': a, 'to': b, 'cycle': 'OTT under T', 'op': label(r), 'note': '', 'factors': {k: repr(v) for k, v in r.items() if v is not None}, 'exact': True})
for cyc in ['OTT turned out']:
    ids = CYC[cyc]
    for a, b in zip(ids, ids[1:]):
        r = relate(ST[a]['S'], ST[b]['S']); lab = label(r)
        EDGES.append({'from': a, 'to': b, 'cycle': cyc, 'op': lab, 'note': '', 'factors': {k: repr(v) for k, v in r.items() if v is not None}, 'exact': True})
        ok(True, f'{cyc}: {a} -> {b}: {lab}; {show(r)}')
print(f'task 3 done ({time.time() - t00:.0f} s)', flush=True)
# ---------------------------------------------------------------- output
nodes = []
for sid, s in ST.items():
    if s['star']: nc_, nf_ = len(s['S']), None
    else: nc_, nf_ = nf(s['S'])
    nodes.append({'id': sid, 'name': s['name'], 'cycle': s['cycle'], 'source': s['paper'], 'corners': nc_, 'faces': nf_, 'star': bool(s['star']),
                  'class': CLASS.get(sid), 'circumradius_float': max(dot(v, v).f() for v in s['S']) ** .5, 'exact': True})
out = {'mark': 'DICTO Mandala of Shells, exact mapping, 2026-10-21 · DICTO · dictospheres.com (groundwork for #46; DICTO\'s idea)',
       'operations': {'T': 'T(S) = {x : v.x <= v.v, every corner v}', 'phiP': 'phi x hull of the foot points of the face planes', 'rho': 'polarity; factor = radius^2 of the sphere (unit sphere x s)',
                      'scale': 'B = c A', 'T x c': 'B = c T(A), not a polarity', 'P x c': 'B = c P(A), not a polarity', 'rect': 'B = c x edge midpoints of A', 'other': 'none of these exactly (see note)'},
       'frame': '#39 frame (I of edge 1); OTT rows in the exact_cycle.py frame', 'cycles': CYC, 'nodes': nodes, 'edges': EDGES, 'links': LINKS,
       'classes': [{'class': i, 'name': ST[C[0]]['name'], 'corners': len(ST[C[0]]['S']), 'stations': C, 'dual_class': DUALCL.get(i)} for i, C in enumerate(cls)],
       'ott_under_T': TASK3}
json.dump(out, open(os.path.join(HERE, 'mandala-map.json'), 'w'), indent=1)
print(f'done ({time.time() - t00:.0f} s)')
