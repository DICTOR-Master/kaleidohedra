# DICTO 2026-10-25: the SHAPES of what each step of the twelve-station golden cycle adds (study for paper #54).
# Classical gnomon (Euclid, Elements II Def. 2; Heron, Definitions): the figure which, added to a figure, makes the whole SIMILAR to the original.
# Exact in Q(√5). Stations from stations-exact.json (dump_stations.py, the published constructions of #34/#35).
# Pieces: a convex layer A ⊂ B is cut as in Inverted Shells / Vajrayana (#35 §3): one piece per face f of A, B ∩ (cone over f from the centre)
# outside f's plane; faces of A lying in a face plane of B give no piece. Step I → Cleo star: the 20 spikes (Cleo-Icos). Step Cleo star → D′:
# DICTO's 12 inward pentagonal pyramids + 30 valley tetrahedra (#35 Table 2). Every corner is solved exactly from three exact planes and checked
# against every half-space; every volume is an exact sum of determinants; similarity is an exact test on all squared corner distances.
# -> gnomon-shapes.txt, pieces.json
import json, itertools, sys, os
from collections import Counter
import numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
from scipy.optimize import linprog
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qs import Q, F, PHI, qsqrt, phi_form, pretty
HERE = os.path.dirname(os.path.abspath(__file__))
raw = json.load(open(os.path.join(HERE, 'stations-exact.json')))
ST = {k: [tuple(Q(F(a), F(b)) for a, b in v) for v in V] for k, V in raw.items()}
fl = lambda V: np.array([[x.f() for x in v] for v in V])
sub = lambda p, q: tuple(p[i] - q[i] for i in range(3))
dot = lambda p, q: p[0] * q[0] + p[1] * q[1] + p[2] * q[2]
cross = lambda u, w: (u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0])
det3 = lambda a, b, c: dot(a, cross(b, c))
checks = []
def check(name, ok): checks.append((name, bool(ok))); return ok

def faces(V):
    """faces of the convex hull of exact points V: list of (vertex indices in cyclic order, n, d) with n·x ≤ d outward; corners = used indices"""
    P = fl(V); h = ConvexHull(P); groups = {}
    for s, eq in zip(h.simplices, h.equations):
        key = tuple(np.round(eq / np.linalg.norm(eq[:3]), 6)); groups.setdefault(key, set()).update(s)
    out = []; cen = tuple(sum((v[i] for v in V), Q(0)) / len(V) for i in range(3))
    for key, idx in groups.items():
        idx = list(idx)
        for a, b, c in itertools.combinations(idx, 3):
            n = cross(sub(V[b], V[a]), sub(V[c], V[a]))
            if any(x != 0 for x in n): break
        d = dot(n, V[a])
        if dot(n, cen) > d: n = tuple(-x for x in n); d = -d
        assert all(dot(n, V[i]) == d for i in idx) and all(dot(n, v) <= d for v in V)
        nf = np.array([x.f() for x in n]); c0 = P[idx].mean(0); e1 = P[idx[0]] - c0; e1 /= np.linalg.norm(e1); e2 = np.cross(nf / np.linalg.norm(nf), e1)
        idx.sort(key=lambda i: np.arctan2((P[i] - c0) @ e2, (P[i] - c0) @ e1))
        out.append((idx, n, d))
    return out

def corners(V):
    used = sorted({i for f, _, _ in faces(V) for i in f})
    return [V[i] for i in used]

def volume(V, F_=None):
    """exact volume of the convex hull of V (sum of origin determinants over fan triangles of each face, oriented outward)"""
    tot = Q(0)
    for idx, n, d in (F_ or faces(V)):
        for i in range(1, len(idx) - 1):
            t = det3(V[idx[0]], V[idx[i]], V[idx[i + 1]])
            # orientation from the cyclic order: (v1 - v0) × (v2 - v0) must point along n
            if dot(cross(sub(V[idx[i]], V[idx[0]]), sub(V[idx[i + 1]], V[idx[0]])), n) < 0: t = -t
            tot = tot + t
    return tot / 6

def same_plane(p1, p2):
    (n1, d1), (n2, d2) = p1, p2
    return all(n1[i] * d2 == n2[i] * d1 for i in range(3)) and (d1 * d2).sign() > 0

def solve3(planes):
    (n1, d1), (n2, d2), (n3, d3) = planes; D = det3(n1, n2, n3)
    if D == 0: return None
    c23, c31, c12 = cross(n2, n3), cross(n3, n1), cross(n1, n2)
    return tuple((d1 * c23[i] + d2 * c31[i] + d3 * c12[i]) / D for i in range(3))

def polytope(H):
    """exact corners of {x : n·x ≤ d for (n, d) in H} (bounded), or [] if it has no interior"""
    A = np.array([[x.f() for x in n] for n, d in H]); b = np.array([d.f() for n, d in H]); nr = np.linalg.norm(A, axis=1)
    res = linprog(np.r_[np.zeros(3), -1], A_ub=np.c_[A, nr], b_ub=b, bounds=[(None, None)] * 3 + [(0, None)])
    if not res.success or res.x[3] < 1e-9: return []
    hs = HalfspaceIntersection(np.c_[A, -b], res.x[:3]); out = []
    for v in hs.intersections:
        act = [k for k in range(len(H)) if abs(A[k] @ v - b[k]) / nr[k] < 1e-7]
        x = None
        for t in itertools.combinations(act, 3):
            x = solve3([H[k] for k in t])
            if x is not None: break
        assert x is not None and all(dot(n, x) <= d for n, d in H), 'corner not exact'
        if x not in out: out.append(x)
    return out

def cone_pieces(A, B):
    FA, FB = faces(A), faces(B); HB = [(n, d) for _, n, d in FB]; pcs = []
    for idx, n, d in FA:
        if any(same_plane((n, d), p) for p in HB): pcs.append(None); continue
        cen = tuple(sum((A[i][k] for i in idx), Q(0)) / len(idx) for k in range(3)); H = list(HB) + [(tuple(-x for x in n), -d)]
        for i in range(len(idx)):
            w = cross(A[idx[i]], A[idx[(i + 1) % len(idx)]])
            if dot(w, cen) > 0: w = tuple(-x for x in w)
            H.append((w, Q(0)))
        V = polytope(H); pcs.append(V if V else None)
    return FA, pcs

def sqd(V): return [[dot(sub(p, q), sub(p, q)) for q in V] for p in V]

def similar(P, R, want_all=False, maxmaps=200000):
    """exact similarity P → R (all squared distances scale by one k²): (k², [mappings]) or None"""
    if len(P) != len(R): return None
    DP, DR = sqd(P), sqd(R); n = len(P)
    mP = max((x for r in DP for x in r), key=lambda q: q.f()); mR = max((x for r in DR for x in r), key=lambda q: q.f()); k2 = mR / mP
    rowP = [Counter((x * k2) for x in r) for r in DP]; rowR = [Counter(r) for r in DR]
    if Counter(x * k2 for r in DP for x in r) != Counter(x for r in DR for x in r): return None
    cand = [[j for j in range(n) if rowR[j] == rowP[i]] for i in range(n)]
    if any(not c for c in cand): return None
    maps = []; m = [None] * n; used = [False] * n
    def bt(i):
        if len(maps) >= (maxmaps if want_all else 1): return
        if i == n: maps.append(list(m)); return
        for j in cand[i]:
            if used[j]: continue
            if all(DR[j][m[t]] == DP[i][t] * k2 for t in range(i)):
                m[i] = j; used[j] = True; bt(i + 1); used[j] = False
    bt(0)
    return (k2, maps) if maps else None

def handed(P, R, mp):
    for a, b, c, e in itertools.combinations(range(len(P)), 4):
        s1 = det3(sub(P[b], P[a]), sub(P[c], P[a]), sub(P[e], P[a])).sign()
        if s1: return s1 == det3(sub(R[mp[b]], R[mp[a]]), sub(R[mp[c]], R[mp[a]]), sub(R[mp[e]], R[mp[a]])).sign()

def describe(V):
    FV = faces(V); fc = Counter(len(f) for f, _, _ in FV); n = len(V)
    E = sorted({dot(sub(V[f[i]], V[f[(i + 1) % len(f)]]), sub(V[f[i]], V[f[(i + 1) % len(f)]])) for f, _, _ in FV for i in range(len(f))}, key=lambda q: q.f())
    big = max(len(f) for f, _, _ in FV); kind = ''
    if n == 4: kind = 'tetrahedron'
    elif any(len(f) == n - 1 for f, _, _ in FV) and fc[3] >= n - 1: kind = f'{n - 1}-gonal pyramid'
    elif n == 5 and fc == Counter({3: 6}): kind = 'triangular bipyramid (6 triangles)'
    big2 = [f for f in FV if len(f[0]) == big]
    if not kind and len(big2) == 2 and len(big2[0][0]) + len(big2[1][0]) == n and cross(big2[0][1], big2[1][1]) == (0, 0, 0):
        (f1, n1, _), (f2, _, _) = big2
        nb = [[j for j in f2 if any((i in f and j in f and abs(f.index(i) - f.index(j)) in (1, len(f) - 1)) for f, _, _ in FV)] for i in f1]
        if all(len(x) == 1 for x in nb):
            T = [sub(V[nb[k][0]], V[f1[k]]) for k in range(len(f1))]
            if all(t == T[0] for t in T): kind = f'{big}-gonal prism' + (' (right)' if cross(T[0], n1) == (0, 0, 0) else ' (oblique)')
            else: kind = f'two parallel {big}-gons joined by {n - 2 and fc[4]} quadrilaterals (not translates)'
    big2 = [f for f in FV if len(f[0]) == big]
    if not kind and len(big2) == 2 and len(big2[0][0]) + len(big2[1][0]) == n and cross(big2[0][1], big2[1][1]) == (0, 0, 0):
        (f1, n1, _), (f2, _, _) = big2; P1 = [V[i] for i in f1]
        # match each corner of the first face to its neighbour (by an edge) on the second
        nb = [[j for j in f2 if any((i in f and j in f and abs(f.index(i) - f.index(j)) in (1, len(f) - 1)) for f, _, _ in FV)] for i in f1]
        if all(len(x) == 1 for x in nb):
            T = [sub(V[nb[k][0]], V[f1[k]]) for k in range(len(f1))]
            if all(t == T[0] for t in T): kind = f'{big}-gonal prism' + (' (right)' if cross(T[0], n1) == (0, 0, 0) else ' (oblique)')
            else: kind = f'{big}-gonal frustum-like solid (two parallel {big}-gons, not translates)'
    return dict(corners=n, faces=dict(sorted(fc.items())), shape=kind, edges2=E, F=FV)

def ratio_txt(k2):
    k = qsqrt(k2)
    if k is not None: return f'k = {k!r}' + (f' = {phi_form(k)}' if phi_form(k) and phi_form(k) != str(k.a) else '')
    return f'k² = {k2!r}' + (f' = {phi_form(k2)}' if phi_form(k2) else '') + ' (k not in Q(√5))'

# ---------------------------------------------------------------- stations
names = ['I', 'Cleo star', 'D′', 'ID', 'OG', 'rTI', 'TI', 'H', 'jtI', 'RT', 'M', 'I·φ³']
I = ST['I']; FI = faces(I); tips = ST['Cleo star tips']
STV = {nm: (corners(ST[nm]) if nm != 'Cleo star' else I + tips) for nm in names}
for nm in names:
    if nm != 'Cleo star': check(f'{nm}: all stored points are corners ({len(ST[nm])})', len(STV[nm]) == len(ST[nm]))
vol = {nm: volume(STV[nm]) for nm in names if nm != 'Cleo star'}
spikes = [list(I[i] for i in f) + [tips[k]] for k, (f, n, d) in enumerate(FI)]
check('each Cleo star tip is 2 × the centre of its face of I (spike = Cleo-Ico reflected in the face)',
      all(tips[k] == tuple(2 * sum((I[i][c] for i in f), Q(0)) / 3 for c in range(3)) for k, (f, n, d) in enumerate(FI)))
vol['Cleo star'] = vol['I'] + sum((volume(s) for s in spikes), Q(0))
VI = vol['I']
ref = {'I': Q(F(-5, 12), F(5, 12)), 'Cleo star': Q(F(-5, 6), F(5, 6)), 'D′': Q(F(10, 9), F(14, 27)), 'OG': Q(F(1975, 456), F(895, 456)),
       'rTI': Q(F(-15, 2), F(73, 8)), 'TI': Q(F(-35, 4), F(39, 4)), 'H': Q(F(-365, 4), F(189, 4)), 'jtI': Q(F(-3465, 38), F(900, 19)),
       'RT': Q(-135, F(135, 2)), 'M': Q(F(145, 12), F(65, 12)), 'I·φ³': Q(F(235, 12), F(35, 4)), 'ID': Q(F(175, 48), F(79, 48))}
for nm in names: check(f'volume of {nm} = published value {ref[nm]!r} (#54 Table 1)', vol[nm] == ref[nm])
for a, b in zip(names, names[1:]):
    if b != 'Cleo star' and a != 'Cleo star':
        check(f'{a} ⊂ {b} (every corner of {a} inside every face plane of {b}, exact)', all(dot(n, v) <= d for v in STV[a] for _, n, d in faces(STV[b])))

out = ['DICTO · dictospheres.com', 'Gnomon shapes: what each step of the twelve-station golden cycle adds, exactly (Q(√5))', '']
out.append('1. Stations: corners, faces, exact sizes (R = corner radius, r = inradius = least face distance; squares exact)')
size = {}
for nm in names:
    V = STV[nm]; R2 = max((dot(v, v) for v in V), key=lambda q: q.f())
    if nm == 'Cleo star': r2 = None; nf = 60
    else:
        FV = faces(V); r2 = min((d * d / dot(n, n) for _, n, d in FV), key=lambda q: q.f()); nf = len(FV)
    size[nm] = (R2, r2)
    out.append(f'  {nm:10s} {len(V):3d} corners {nf:3d} faces  R² = {pretty(R2):34s} r² = {pretty(r2) if r2 is not None else "— (not convex)"}')

# ---------------------------------------------------------------- steps and pieces
steps = []   # (from, to, list of (label, kind-name, [V,...]))
def group(pcs):
    kinds = []
    for V in pcs:
        for K in kinds:
            s = similar(K[0], V)
            if s and s[0] == 1: K.append(V); break
        else: kinds.append([V])
    return kinds
cleo_core = [[(Q(0), Q(0), Q(0))] + [I[i] for i in f] for f, n, d in FI]
steps.append(('I', 'Cleo star', [('Cleo-Ico (spike)', spikes)]))
pyr = []; val = []
for k, (f, n, d) in enumerate(faces(tips)):
    ax = tuple(sum((tips[i][c] for i in f), Q(0)) / len(f) for c in range(3))
    below = [v for v in I if cross(v, ax) == (0, 0, 0) and dot(v, ax) > 0]
    pyr.append([tips[i] for i in f] + below)
EI = {(min(a, b), max(a, b)) for f, _, _ in FI for a, b in zip(f, f[1:] + f[:1])}
for a, b in sorted(EI):
    side = [tips[k] for k, (f, n, d) in enumerate(FI) if a in f and b in f]
    val.append([I[a], I[b]] + side)
check('12 inward pentagonal pyramids, each apex the corner of I on its face axis', len(pyr) == 12 and all(len(p) == 6 for p in pyr))
check('30 valley tetrahedra, one per edge of I (two ends + the two neighbouring spike tips)', len(val) == 30 and all(len(p) == 4 for p in val))
check('star + 12 inward pyramids + 30 valley tetrahedra = D′ exactly (remainder 0, #35 Table 2)',
      vol['Cleo star'] + sum((volume(p) for p in pyr), Q(0)) + sum((volume(p) for p in val), Q(0)) == vol['D′'])
steps.append(('Cleo star', 'D′', [('inward pentagonal pyramid', pyr), ('valley tetrahedron', val)]))
comp = {}
for a, b in zip(names[2:], names[3:]):
    A, B = STV[a], STV[b]; FA, pcs = cone_pieces(A, B)
    got = [V for V in pcs if V]; vs = sum((volume(V) for V in got), Q(0))
    check(f'{a} → {b}: the {len(got)} cone pieces add up to vol {b} − vol {a} exactly', vs == vol[b] - vol[a])
    # connectivity: neighbouring faces of A whose pieces share a wall with positive area
    par = list(range(len(FA))); fnd = lambda x: x if par[x] == x else fnd(par[x])
    edge_of = {}
    for i, (f, n, d) in enumerate(FA):
        for p, q in zip(f, f[1:] + f[:1]): edge_of.setdefault((min(p, q), max(p, q)), []).append(i)
    for (p, q), fs in edge_of.items():
        if len(fs) == 2 and pcs[fs[0]] and pcs[fs[1]]:
            w = cross(A[p], A[q]); on = [v for v in pcs[fs[0]] if dot(w, v) == 0]
            if len(on) >= 3 and any(cross(sub(y, on[0]), sub(z, on[0])) != (0, 0, 0) for y, z in itertools.combinations(on[1:], 2)):
                par[fnd(fs[0])] = fnd(fs[1])
    comp[(a, b)] = len({fnd(i) for i in range(len(FA)) if pcs[i]})
    labelled = []
    for K in group(got):
        fsz = Counter(len(FA[i][0]) for i in range(len(FA)) if pcs[i] and similar(K[0], pcs[i]) and similar(K[0], pcs[i])[0] == 1)
        labelled.append((f'over {"/".join(f"{s}-gon" for s in fsz)} faces of {a}', K))
    steps.append((a, b, labelled))
check('I → Cleo star: 20 spikes add vol I exactly', sum((volume(s) for s in spikes), Q(0)) == VI)

NAMES = {}   # DICTO's published names, matched exactly below
kinds = [('I (core)', 'Cleo-Ico (core)', cleo_core)]
for a, b, lab in steps:
    for label, pcs in lab: kinds.append((f'{a} → {b}', label, pcs))
check('the 20 core Cleo-Icos of I are congruent', all(similar(cleo_core[0], c) and similar(cleo_core[0], c)[0] == 1 for c in cleo_core))
check('spike Cleo-Ico congruent to core Cleo-Ico (#35 §2)', similar(cleo_core[0], spikes[0]) is not None and similar(cleo_core[0], spikes[0])[0] == 1)
for st_, lab, pcs in kinds:
    check(f'{st_}: {lab}: all {len(pcs)} pieces congruent', all((s := similar(pcs[0], V)) and s[0] == 1 for V in pcs))

out.append('\n2. Steps: what each step adds (pieces; all pieces of a kind congruent; kinds named by DICTO where published)')
rows = []
for si, (a, b, lab) in enumerate(steps, 1):
    g = vol[b] - vol[a]
    out.append(f'  step {si:2d}  {a} → {b}: adds {pretty(g / VI)} × I'
               + (f'; region = {comp[(a, b)]} connected part(s)' if (a, b) in comp else ''))
    for label, pcs in lab:
        D = describe(pcs[0]); v1 = volume(pcs[0])
        out.append(f'      {len(pcs):3d} × {label}: {D["shape"] or "polyhedron"}, {D["corners"]} corners, faces {D["faces"]}, each {pretty(v1 / VI)} × I')
        out.append(f'            squared edges: {", ".join(repr(e) for e in D["edges2"])}')
        rows.append((si, a, b, len(pcs), label, D, v1))

# ---------------------------------------------------------------- similarities
out.append('\n3. Similar pieces across the cycle (exact test on all squared corner distances; k = linear ratio later/earlier)')
simpairs = []
for (i, (s1, l1, p1)), (j, (s2, l2, p2)) in itertools.combinations(enumerate(kinds), 2):
    r = similar(p1[0], p2[0], want_all=True)
    if r:
        k2, maps = r; direct = any(handed(p1[0], p2[0], m) for m in maps)
        simpairs.append((i, j, k2, direct))
        out.append(f'  {s1}: {l1}  ~  {s2}: {l2}   {ratio_txt(k2)}  ({"direct" if direct else "mirror only"})')
if not simpairs: out.append('  none')
out.append('\n4. Pieces similar to a station (equal corner counts tested exactly)')
hit = 0
for s1, l1, p1 in kinds:
    for nm in names:
        if len(STV[nm]) == len(p1[0]):
            r = similar(STV[nm], p1[0])
            out.append(f'  {s1}: {l1} vs {nm}: ' + (ratio_txt(r[0]) if r else 'not similar')); hit += 1
if not hit: out.append('  no piece has as many corners as any station')

out.append('\n5. Classical check (Euclid II Def. 2; Heron): is the new whole similar to an earlier station (any turn: stations repeat ×φ³)?')
stsim = {}
for (i, a), (j, b) in itertools.combinations(enumerate(names), 2):
    if len(STV[a]) == len(STV[b]):
        r = similar(STV[a], STV[b]); stsim[(a, b)] = r[0] if r else None
for i, b in enumerate(names[1:], 1):
    hits = [(a, k2) for (a, bb), k2 in stsim.items() if bb == b and k2 is not None]
    same_n = [a for a in names if a != b and len(STV[a]) == len(STV[b])]
    out.append(f'  step {i:2d} → {b:10s}: ' + ('; '.join(f'similar to {a} ({ratio_txt(k2)}): GNOMON in the classical sense' for a, k2 in hits) if hits else
               f'similar to no other station (same corner count only: {", ".join(same_n) or "none"}; tested exactly: not similar)'))
out.append('  step 12 → Cleo star·φ³ (first step of the next turn) is step 1 scaled by φ³, so its new whole is similar to the Cleo star, not to a station of this whole turn other than itself.')
check('I·φ³ is similar to I with linear ratio φ³ (the only similar pair of stations in one turn)',
      [(k, v) for k, v in stsim.items() if v is not None] == [(('I', 'I·φ³'), PHI * PHI * PHI * PHI * PHI * PHI)])

out.append('\n6. Size growth of the whole, step by step (exact squares; k where it lies in Q(√5))')
out.append(f'  {"step":20s} {"V ratio":32s} {"R² ratio":36s} {"r² ratio":36s}')
for a, b in zip(names, names[1:]):
    (Ra, ra), (Rb, rb) = size[a], size[b]
    rr = ratio_txt(rb / ra) if ra is not None and rb is not None else '—'
    out.append(f'  {a + " → " + b:20s} {pretty(vol[b] / vol[a]):32s} {ratio_txt(Rb / Ra):36s} {rr}')

for t, k in checks: out.append(('PASS ' if k else 'FAIL ') + t)
npass = sum(k for _, k in checks); out.append(f'{npass} PASS, {len(checks) - npass} FAIL')
txt = '\n'.join(out); print(txt); open(os.path.join(HERE, 'gnomon-shapes.txt'), 'w').write(txt + '\n')
js = {'stations': {nm: [[x.f() for x in v] for v in STV[nm]] for nm in names},
      'steps': [{'from': a, 'to': b, 'kinds': [{'label': l, 'pieces': [[[x.f() for x in v] for v in V] for V in pcs]} for l, pcs in lab]} for a, b, lab in steps]}
json.dump(js, open(os.path.join(HERE, 'pieces.json'), 'w'), ensure_ascii=False)
