# EXACT check of the inner UP, all the way in (DICTO 2026-10-19: "firm up all the way in"), in Q(sqrt5), standard frame:
# icosahedron of edge 1 with corners (0, +-1/2, +-phi/2) cyclic; the ID of radius phi (exact_cycle.py) is in the same frame.
#   (the ID here is twice the icosahedron's edge midpoints, radius phi, in the same frame)
#   stage 1  the Cleo star: 20 Cleo-Icos + 20 spikes + 12 inward pyramids + 30 valley tetrahedra fill D' (cf. progenitors step 9-10)
#   stage 2  D' -> ID: every D' corner is an ID triangle centre; 12 twisted frusta = the cone pieces over D''s faces; sum = gap
#   OG       the OG at this size: corners = 30 ID corners + 60 = (2c - v) in each ID triangle (c its centre) + 12 apexes on the kite
#            planes; matched to the study's OG data; ID -> OG (12) and OG -> RT (20 hexagonal Cleos, 12 caps, 120 tetrahedra)
#   stage 3  the fine cut (12 + 20 pyramids + 60 valley tetrahedra)
#   Vajra    inward pyramid + frustum + outward pyramid = their hull, exactly
# Each set of pieces: exact volumes, sum = the gap exactly, every piece inside the outer solid and outside the inner one, and no
# two pieces overlap: for every pair a face plane of one has the other wholly on its far side (exact). Together with the volume
# sum this proves the pieces fill the gap with no overlap and no hole.
import itertools, json, os
from collections import Counter
import numpy as np
from exact_cycle import Q5, Fr, PHI, dot, step
from exact_shells import polytope, volume, solid, cross, sub

def hullH(P):
    P = list(dict.fromkeys(P)); H = solid(P); C, F = polytope(H); return {'H': H, 'C': C, 'F': F, 'V': volume(C, F)}
def piece(P, minus=None):
    p = hullH(P); p['minus'] = minus                                       # minus: a convex part removed (a dimple)
    if minus is not None: p['V'] = p['V'] - minus['V']
    return p
def inside(c, H, strict=False): return all(((dot(n, c) - d).sign() < 0) if strict else ((dot(n, c) - d).sign() <= 0) for n, d in H)
def separated(A, B):
    for X, Y in ((A, B), (B, A)):
        for n, d in X['H']:
            if all((dot(n, c) - d).sign() >= 0 for c in Y['C']): return True
    return False
def check(name, pieces, inner, outer, log):
    gap = outer['V'] - (inner['V'] if inner else Q5(0)); tot = sum((p['V'] for p in pieces), Q5(0))
    ins = all(inside(c, outer['H']) for p in pieces for c in p['C'])
    # outside the inner solid: every piece has a face plane of the inner solid with the piece on its far side
    out = inner is None or all(any(all((dot(n, c) - d).sign() >= 0 for c in p['C']) for n, d in inner['H']) or p['minus'] is not None for p in pieces)
    fc = [np.array([x.f() for x in c]) for p in pieces for c in p['C']]
    cen = [np.mean([[x.f() for x in c] for c in p['C']], axis=0) for p in pieces]
    rad = [max(np.linalg.norm(np.array([x.f() for x in c]) - m) for c in p['C']) for p, m in zip(pieces, cen)]
    bad = 0; pairs = 0
    for i, j in itertools.combinations(range(len(pieces)), 2):
        if np.linalg.norm(cen[i] - cen[j]) > rad[i] + rad[j] + 1e-6: continue          # far apart: cannot overlap
        pairs += 1
        if pieces[i]['minus'] is not None or pieces[j]['minus'] is not None:
            A, B = (pieces[i], pieces[j]) if pieces[i]['minus'] is None else (pieces[j], pieces[i])
            if B['minus'] is not None and A['minus'] is None and separated(A, B): continue
            if B['minus'] is not None and A['minus'] is None and all(inside(c, B['minus']['H']) for c in A['C']): continue   # A sits in the dimple
            if A['minus'] is not None and B['minus'] is not None and separated(A, B): continue
            bad += 1; continue
        if not separated(pieces[i], pieces[j]): bad += 1
    log[name] = {'pieces': len(pieces), 'sum_equals_gap': (tot - gap) == Q5(0), 'all_inside_outer': ins, 'all_outside_inner': out,
                 'close_pairs_tested': pairs, 'pairs_not_separated': bad, 'gap': repr(gap)}
    print(name, log[name], flush=True)

if __name__ == '__main__':
    log = {'mark': 'DICTO Universal PiTet (UP), exact inner stages, 2026-10-19'}
    h, z = Q5(Fr(1, 2)), Q5(0)
    I = [v for a, b in ((h, PHI / 2),) for v in [(z, sa * a, sb * b) for sa in (1, -1) for sb in (1, -1)] +
         [(sb * b, z, sa * a) for sa in (1, -1) for sb in (1, -1)] + [(sa * a, sb * b, z) for sa in (1, -1) for sb in (1, -1)]]
    Ih = hullH(I); assert len(Ih['F']) == 20
    tri = [[I_ for I_ in [Ih['C'][j] for j in o]] for o, _ in Ih['F']]
    cent = lambda P: tuple(sum((p[k] for p in P), Q5(0)) / len(P) for k in range(3))
    tips = [tuple(2 * x for x in cent(t)) for t in tri]                                  # spike tips = D' corners
    Dp = hullH(tips); assert len(Dp['C']) == 20 and len(Dp['F']) == 12
    O3 = (z, z, z)
    cleo = [piece(t + [O3]) for t in tri]; spikes = [piece(t + [tp]) for t, tp in zip(tri, tips)]
    pyr = []
    for o, i in Dp['F']:
        n, d = Dp['H'][i]; base = [Dp['C'][j] for j in o]; apex = max(I, key=lambda v: dot(n, v).f()); pyr.append(piece(base + [apex]))
    val = []
    for a, b in {frozenset((p, q)) for t in tri for p, q in itertools.combinations(t, 2)}:
        two = [tp for t, tp in zip(tri, tips) if a in t and b in t]; val.append(piece([a, b] + two))
    log['stage1_counts'] = {'cleo': len(cleo), 'spikes': len(spikes), 'pyramids': len(pyr), 'valleys': len(val)}
    check('stage 1: Cleo star fills D\'', cleo + spikes + pyr + val, None, Dp, log)
    # stage 2
    # the ID in the icosahedron's own frame: twice its edge midpoints (radius phi). exact_cycle.py starts from the mirror frame;
    # the cycle is the same in either.
    ID = list({tuple(x + y for x, y in zip(p, q)) for t in tri for p, q in itertools.combinations(t, 2)})
    assert len(ID) == 30 and all(dot(v, v) == PHI * PHI for v in ID)
    IDh = hullH(ID); T3 = [[IDh['C'][j] for j in o] for o, _ in IDh['F'] if len(o) == 3]
    log['stage2_Dcorners_are_ID_triangle_centres'] = {cent(t) for t in T3} == set(tips)
    print('D\' corners = ID triangle centres:', log['stage2_Dcorners_are_ID_triangle_centres'])
    fr = []
    for o, i in Dp['F']:
        n, d = Dp['H'][i]; base = [Dp['C'][j] for j in o]
        top = sorted(ID, key=lambda v: -dot(n, v).f())[:5]; fr.append(piece(base + top))
    check('stage 2: D\' -> ID, 12 twisted frusta', fr, Dp, IDh, log)
    log['frustum_volume'] = repr(fr[0]['V']); log['frusta_one_volume'] = len({p['V'] for p in fr}) == 1
    # stage 3 fine cut and the RT
    RT = step(ID)[0]; RTh = hullH(RT)
    A5 = [v for v in RT if len([w for w in ID if (dot(v, w) - dot(w, w)).sign() == 0]) == 5]
    A3 = [v for v in RT if v not in A5]
    fine = []
    for o, i in IDh['F']:
        F = [IDh['C'][j] for j in o]; n, d = IDh['H'][i]; fine.append(piece(F + [max(A5 if len(F) == 5 else A3, key=lambda v: dot(n, v).f())]))
    for o, i in IDh['F']:
        F = [IDh['C'][j] for j in o]
    Eid = {frozenset(e) for o, _ in IDh['F'] for e in zip([IDh['C'][j] for j in o], [IDh['C'][j] for j in o[1:] + o[:1]])}
    for e in Eid:
        a, b = list(e); m = tuple(x + y for x, y in zip(a, b))
        fine.append(piece([a, b, max(A5, key=lambda v: dot(v, m).f() / np.linalg.norm([x.f() for x in v])), max(A3, key=lambda v: dot(v, m).f() / np.linalg.norm([x.f() for x in v]))]))
    check('stage 3: ID -> RT fine cut (pyramids + valley tetrahedra)', fine, IDh, RTh, log)
    # the five-sided Vajra on one 5-fold axis
    ax = A5[0]; tipI = max(I, key=lambda v: dot(v, ax).f() / np.linalg.norm([x.f() for x in v]))
    ip = next(p for p in pyr if tipI in p['C'])                                            # Cleo star inward pyramid, tip at I corner
    f5 = max(fr, key=lambda p: sum(dot(c, ax).f() for c in p['C']))                       # the twisted frustum on that axis
    o5 = next(p for p in fine if ax in p['C'] and len(p['C']) == 6)                       # outward pyramid, tip at the RT corner
    log['vajra5_parts'] = [repr(ip['V']), repr(f5['V']), repr(o5['V'])]
    V = hullH(ip['C'] + f5['C'] + o5['C'])
    log['vajra5_union_is_convex_exactly'] = (V['V'] - ip['V'] - f5['V'] - o5['V']) == Q5(0); log['vajra5_volume'] = repr(V['V'])
    print('five-sided Vajra = its hull exactly:', log['vajra5_union_is_convex_exactly'], V['V'])
    # the OG at this size
    X = []
    for t in T3:
        c = cent(t); X += [tuple(2 * c[k] - v[k] for k in range(3)) for v in t]
    X = list(dict.fromkeys(X)); assert len(X) == 60
    apex = []
    for a5 in A5:                                                          # apex on the 5-fold axis, on the kite plane (x, c, x')
        cs = sorted(ID, key=lambda v: -dot(v, a5).f())[:5]; xs = sorted(X, key=lambda v: -dot(v, a5).f())[:5]
        c0 = cs[0]; x2 = sorted(xs, key=lambda v: sum((v[k] - c0[k]).f() ** 2 for k in range(3)))[:2]
        n = cross(sub(x2[0], c0), sub(x2[1], c0)); t_ = dot(n, c0) / dot(n, a5); apex.append(tuple(t_ * x for x in a5))
    OG = ID + X + apex; OGh = hullH(OG)
    log['og'] = {'corners': len(OGh['C']), 'faces': dict(Counter(len(o) for o, _ in OGh['F']))}
    of = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ocd-vertices.json')))
    of = np.array(of); R = np.linalg.norm(of, axis=1); fx = of[np.abs(R - R.max()) < 1e-7] / R.max()
    u = np.array([[x.f() for x in v] for v in A5]); u /= np.linalg.norm(u, axis=1)[:, None]
    a, b = fx[0], fx[np.argsort(np.linalg.norm(fx - fx[0], axis=1))[1]]; xx = u[0]; yy = u[np.argsort(np.linalg.norm(u - xx, axis=1))[1]]
    M = np.array([xx, yy, np.cross(xx, yy)]).T @ np.linalg.inv(np.array([a, b, np.cross(a, b)]).T)
    ofa = of @ M.T * (3 * ((1 + 5 ** .5) / 2) / 2); E = np.array([[x.f() for x in c] for c in OGh['C']])
    dev = max(np.min(np.linalg.norm(E - p, axis=1)) for p in ofa); log['og']['max_distance_to_study_OG_data'] = float(dev)
    print('OG', log['og'], flush=True)
    low = []
    for a5 in A5:
        cs = sorted(ID, key=lambda v: -dot(v, a5).f())[:5]; xs = sorted(X, key=lambda v: -dot(v, a5).f())[:5]
        ap = max(apex, key=lambda v: dot(v, a5).f()); low.append(piece(cs + xs + [ap]))
    check('ID -> OG, 12 pieces', low, IDh, OGh, log)
    hexc = []
    for o, i in OGh['F']:
        if len(o) != 6: continue
        n, d = OGh['H'][i]; hexc.append(piece([OGh['C'][j] for j in o] + [max(A3, key=lambda v: dot(n, v).f())]))
    caps = []
    for a5, L in zip(A5, low):
        cs = sorted(ID, key=lambda v: -dot(v, a5).f())[:5]; xs = sorted(X, key=lambda v: -dot(v, a5).f())[:5]
        caps.append(piece(cs + xs + [a5], minus=L))
    tets = []
    for x in X:
        a5 = max(A5, key=lambda v: dot(v, x).f() / np.linalg.norm([q.f() for q in v])); a3 = max(A3, key=lambda v: dot(v, x).f() / np.linalg.norm([q.f() for q in v]))
        for c in sorted(ID, key=lambda v: sum((v[k] - x[k]).f() ** 2 for k in range(3)))[:2]: tets.append(piece([c, x, a5, a3]))
    check('OG -> RT: 20 hexagonal Cleos + 12 dimpled caps + 120 tetrahedra', hexc + caps + tets, OGh, RTh, log)
    log['hexagonal_cleo_volume'] = repr(hexc[0]['V']); log['cap_volume'] = repr(caps[0]['V']); log['tet_volume'] = repr(tets[0]['V'])
    log['cap_plus_low_is_convex'] = (caps[0]['V'] + low[0]['V'] - hullH(caps[0]['C'])['V']) == Q5(0)
    json.dump(log, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'exact_inner.json'), 'w'), indent=1, default=str)
    print(json.dumps({k: v for k, v in log.items() if not isinstance(v, dict)}, default=str, indent=1))
