#!/usr/bin/env python3
"""PILOT (question a): the 40 sporadic rational tetrahedra of Chentouf-Sun, arXiv:2312.01654, Thm 1.2.
Data: the 40 angle 6-tuples (alpha12, alpha34, alpha13, alpha24, alpha14, alpha23)/pi, as listed in the list L of Y. Sun's criteria.py
(github.com/KimiSun18/TetrahedraUROP @ d30c9ab, 2022; facts from the paper, typed in here, no code copied).
Steps (all ours unless credited):
 1. geometry from dihedral angles (Gram matrix of outward normals; faces tangent to the unit sphere), 60 digits; angles re-measured as a check;
 2. Dehn invariant via #100's numerical screen (Dehn 1901; Debrunner 1980: tilers have Dehn zero) -- a CONTROL: every rational tetrahedron
    must give zero, so Dehn cannot decide this question;
 3. match against the known tilers: Sommerville 1923 (Proc. Edinburgh Math. Soc. 41, figs 7-10) and Goldberg 1974 (JCTA 16) three families
    (first family = Sommerville's equilateral-prism thirds; second and third = its halves through the 2-fold axis, Goldberg, JCTA 17 (1974) p. 375),
    Edmonds 2007 (Sommerville (xi), p/q = sqrt(2/3), sqrt(3/2)); congruence = equal edge 6-tuples under the 24 relabelings, mirror included;
 4. non-face-to-face obstruction: Chentouf-Sun Prop. 2.3 (pi-combinations of dihedral angles), exact rationals;
 5. face-to-face obstruction: Bongiovanni-Diaz-Kakkar-Sothanaphan 2019 (Geom. Dedicata; arXiv:1709.04139) Prop. 4.3, edge-length graphs:
    from every node of every d-edge-length graph a closed walk whose labels' angles sum to 2pi must exist; exact rationals on angles,
    edge-length ties at 1e-40 (numerical; ties to be confirmed exactly in the full run);
 6. Chentouf-Sun Cor. 2.13 LP (float, recomputed) for the record.
Prints PROGRESS k/40 and a FINAL line."""
import sys, json, itertools, math, time
from fractions import Fraction as Fr
import mpmath as mp
import numpy as np
mp.mp.dps = 60
t0 = time.time()
DEHN_DIR = sys.argv[1] if len(sys.argv) > 1 else '.'; OUT = sys.argv[2] if len(sys.argv) > 2 else 'tetra-pilot.json'
RAW = [  # (a12, a34, a13, a24, a14, a23) as (num, den)
 [(1,4),(1,3),(1,3),(1,4),(1,2),(2,3)], [(5,24),(3,8),(1,3),(1,4),(13,24),(5,8)], [(1,4),(1,2),(1,2),(1,3),(1,3),(1,2)],
 [(7,24),(11,24),(13,24),(7,24),(1,3),(1,2)], [(1,5),(1,5),(1,3),(1,5),(2,3),(2,3)], [(1,5),(1,5),(4,15),(4,15),(3,5),(11,15)],
 [(1,5),(1,5),(1,3),(1,3),(3,5),(3,5)], [(1,3),(1,3),(3,5),(1,3),(2,5),(2,5)], [(4,15),(8,15),(1,3),(1,3),(7,15),(7,15)],
 [(1,7),(3,7),(1,3),(1,3),(4,7),(4,7)], [(2,7),(2,7),(1,3),(1,3),(3,7),(5,7)], [(1,5),(2,5),(1,2),(1,3),(1,3),(2,3)],
 [(2,15),(7,15),(1,2),(1,3),(2,5),(3,5)], [(2,15),(7,15),(31,60),(19,60),(5,12),(7,12)], [(1,5),(2,5),(7,12),(1,4),(5,12),(7,12)],
 [(13,60),(23,60),(7,12),(1,4),(2,5),(3,5)], [(1,5),(3,5),(1,3),(1,3),(1,2),(1,2)], [(3,10),(7,10),(1,3),(1,3),(2,5),(2,5)],
 [(1,5),(1,5),(2,5),(1,3),(1,2),(2,3)], [(1,6),(7,30),(11,30),(11,30),(1,2),(2,3)], [(1,5),(1,5),(9,20),(17,60),(11,20),(37,60)],
 [(1,5),(1,3),(1,2),(1,3),(2,5),(3,5)], [(1,6),(11,30),(1,2),(1,3),(13,30),(17,30)], [(1,6),(11,30),(29,60),(7,20),(5,12),(7,12)],
 [(1,5),(1,3),(1,3),(1,5),(1,2),(4,5)], [(7,60),(5,12),(1,3),(1,5),(7,12),(43,60)], [(1,5),(2,5),(2,5),(1,5),(1,2),(2,3)],
 [(1,5),(2,5),(1,3),(1,3),(1,2),(3,5)], [(7,30),(13,30),(3,10),(3,10),(1,2),(3,5)], [(1,4),(7,20),(1,3),(1,3),(9,20),(13,20)],
 [(1,5),(1,2),(3,5),(1,5),(1,3),(2,3)], [(1,5),(1,2),(17,30),(7,30),(3,10),(7,10)], [(3,20),(11,20),(17,30),(7,30),(7,20),(13,20)],
 [(1,5),(1,2),(1,2),(1,3),(2,5),(1,2)], [(1,5),(1,2),(7,15),(11,30),(11,30),(8,15)], [(4,15),(13,30),(17,30),(4,15),(2,5),(1,2)],
 [(4,15),(13,30),(3,5),(3,10),(11,30),(7,15)], [(4,15),(17,30),(2,5),(3,10),(11,30),(8,15)], [(3,10),(2,5),(3,5),(3,10),(1,3),(1,2)],
 [(1,3),(2,5),(2,5),(1,3),(1,2),(2,5)]]
assert len(RAW) == 40
ORDER = [(0,1),(2,3),(0,2),(1,3),(0,3),(1,2)]          # edge order 12,34,13,24,14,23 (0-based vertices)
EIDX = {e: i for i, e in enumerate(ORDER)}
def eid(a, b): return EIDX[(min(a, b), max(a, b))]
def opp(e): return tuple(sorted(set(range(4)) - set(e)))

def tet_from_angles(ang):   # ang: 6 Fractions (units of pi) in ORDER
    G = mp.matrix(4, 4)
    for i in range(4): G[i, i] = 1
    for i, j in itertools.combinations(range(4), 2):     # faces i, j meet along the edge joining the other two vertices
        th = ang[eid(*opp((i, j)))]; G[i, j] = G[j, i] = -mp.cos(mp.pi*th.numerator/th.denominator)
    E, Q = mp.eigsy(G)
    idx = sorted(range(4), key=lambda k: -E[k])[:3]
    if min(E[k] for k in idx) <= mp.mpf(10)**-30: raise ValueError('Gram rank')
    N = [mp.matrix([Q[r, k]*mp.sqrt(E[k]) for k in idx]) for r in range(4)]   # outward normals n_r with n_r.n_s = G_rs
    V = []
    for v in range(4):
        F = [f for f in range(4) if f != v]
        A = mp.matrix([[N[f][c] for c in range(3)] for f in F]); V.append(mp.lu_solve(A, mp.matrix([1, 1, 1])))
    return V
def vol(V):
    a, b, c = [V[k] - V[0] for k in (1, 2, 3)]
    return abs(a[0]*(b[1]*c[2]-b[2]*c[1]) - a[1]*(b[0]*c[2]-b[2]*c[0]) + a[2]*(b[0]*c[1]-b[1]*c[0]))/6
def norm(v): return mp.sqrt(sum(x*x for x in v))
def lengths(V):
    s = vol(V)**(mp.mpf(1)/3)
    return [norm(V[a] - V[b])/s for a, b in ORDER]
def cross(a, b): return mp.matrix([a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]])
def dihedrals(V):   # interior dihedral angle at each edge, in units of pi
    out = []
    for a, b in ORDER:
        c, d = opp((a, b)); e = V[b] - V[a]
        u = V[c] - V[a]; w = V[d] - V[a]
        pu = u - e*(sum(u[k]*e[k] for k in range(3))/sum(x*x for x in e)); pw = w - e*(sum(w[k]*e[k] for k in range(3))/sum(x*x for x in e))
        out.append(mp.acos(sum(pu[k]*pw[k] for k in range(3))/(norm(pu)*norm(pw)))/mp.pi)
    return out
PERMS = list(itertools.permutations(range(4)))
def relabel(L, p):  # edge tuple of the tetrahedron with vertex i renamed p[i]
    out = [None]*6
    for k, (a, b) in enumerate(ORDER): out[eid(p[a], p[b])] = L[k]
    return out
def congruent(L1, L2, tol=mp.mpf(10)**-35):
    return any(max(abs(x - y) for x, y in zip(relabel(L1, p), L2)) < tol for p in PERMS)

# ---------------- known tilers from coordinates ----------------
def P(*x): return mp.matrix([mp.mpf(t) for t in x])
s1 = [P(1,0,0), P(-1,0,0), P(0,1,1), P(0,-1,1)]                  # Sommerville fig. 7 (No. 1): opposite edges 2, others sqrt3
def refl(x, a, b, c):
    n = cross(b - a, c - a); n = n/norm(n); d = sum((x[k]-a[k])*n[k] for k in range(3)); return x - n*(2*d)
D = P(0,0,0)                                                         # midpoint of the length-2 edge P1P2
s_fig8 = [s1[2], s1[3], s1[0], D]                                    # half of No. 1 by the symmetry plane through the edge P3P4
E = refl(s1[2], s1[0], D, s1[3]); s_fig9 = [s1[2], s1[0], s1[3], E]  # two fig-8 pieces glued on face B D B'
s_fig10 = [s1[0], s1[1], s1[2], P(0,0,mp.mpf(1)/2)]                  # No. 1 coned from its circumcentre
KNOWN = {'Sommerville fig 7 (No. 1)': s1, 'Sommerville fig 8': s_fig8, 'Sommerville fig 9': s_fig9, 'Sommerville fig 10': s_fig10}
def from_lengths(d):   # d in ORDER; place vertices (exact up to precision)
    d12, d34, d13, d24, d14, d23 = d
    A = P(0,0,0); B = P(d12,0,0)
    x = (d12**2 + d13**2 - d23**2)/(2*d12); C = P(x, mp.sqrt(d13**2 - x**2), 0)
    x4 = (d12**2 + d14**2 - d24**2)/(2*d12)
    y4 = (d14**2 - d34**2 + C[0]**2 + C[1]**2 - 2*x4*C[0])/(2*C[1])
    z2 = d14**2 - x4**2 - y4**2
    if z2 <= 0: return None
    return [A, B, C, P(x4, y4, mp.sqrt(z2))]
def goldberg1(a):   # Goldberg's first family, edge lengths as in Bongiovanni et al. 2019 sect. 3: path 1-2-3-4 of unit edges
    r = mp.sqrt(3*a*a + 1)
    return from_lengths([mp.mpf(1), mp.mpf(1), r, r, 3*a, mp.mpf(1)])   # d12, d34, d13, d24, d14, d23
def halves(V):     # cut through the 2-fold axis (midpoints of edges 14 and 23; symmetry 1<->4, 2<->3), containing edge 14 or 23
    M23 = (V[1] + V[2])/2; M14 = (V[0] + V[3])/2
    return [V[0], V[3], V[1], M23], [V[1], V[2], V[0], M14]
def edmonds(r):    # Sommerville (xi): d12 = d23 = d34 = p, d13 = d14 = d24 = q, p/q = r
    return from_lengths([r, r, mp.mpf(1), mp.mpf(1), mp.mpf(1), r])

out = {'tetrahedra': [], 'controls': {}}
# controls: re-measured angles of the known pieces
for nm, V in KNOWN.items():
    out['controls'][nm] = {'angles_over_pi': [mp.nstr(x, 12) for x in dihedrals(V)], 'volume': mp.nstr(vol(V), 15)}
# check the halves really are halves and the reflected union is a tetrahedron
out['controls']['fig9 volume / fig8 volume (expect 2)'] = mp.nstr(vol(s_fig9)/vol(s_fig8), 20)

sys.path.insert(0, DEHN_DIR)
saved = sys.argv[:]; sys.argv = [saved[0], '', '10', '200']
import dehn as DEHN   # #100's screen (2026-11-04-dehn-screen/scripts/dehn.py)

def pi_combos(ang, target):   # nonnegative integer vectors c with sum c_e ang_e = target (all exact)
    res = []
    def rec(k, rem, c):
        if rem == 0: res.append(tuple(c + [0]*(6 - len(c)))); return
        if k == 6: return
        m = 0
        while m*ang[k] <= rem:
            rec(k + 1, rem - m*ang[k], c + [m]); m += 1
    rec(0, target, []); return [r for r in res if any(r)]
def cs_nonf2f_excluded(ang):
    C = pi_combos(ang, Fr(1))
    if not C: return True, 'no pi-combination'
    if len(C) == 1:
        sup = [k for k in range(6) if C[0][k]]
        if len(sup) == 2 and sorted(ORDER[sup[0]] + ORDER[sup[1]]) == [0, 1, 2, 3]: return True, 'one pi-combination, on opposite edges only'
    return False, f'{len(C)} pi-combination(s)'
def bdks_f2f_excluded(ang, L, tol=mp.mpf(10)**-40):
    cls = []
    for x in L:
        for k, c in enumerate(cls):
            if abs(c - x) < tol: break
        else: cls.append(x); k = len(cls) - 1
    lab = [next(k for k, c in enumerate(cls) if abs(c - x) < tol) for x in L]
    for d in set(lab):
        G = {}   # node -> list of (node, angle)
        for e, (i, j) in enumerate(ORDER):
            if lab[e] != d: continue
            k, l = opp((i, j))
            for (a, b) in ((i, j), (j, i)):
                n1 = (lab[eid(a, k)], lab[eid(b, k)]); n2 = (lab[eid(a, l)], lab[eid(b, l)])
                G.setdefault(n1, []).append((n2, ang[e])); G.setdefault(n2, []).append((n1, ang[e]))
        for start in G:
            seen = {(start, Fr(0))}; frontier = [(start, Fr(0))]; ok = False
            while frontier and not ok:
                nxt = []
                for node, s in frontier:
                    for n2, a in G[node]:
                        t = s + a
                        if t > 2: continue
                        if t == 2 and n2 == start: ok = True; break
                        if (n2, t) not in seen: seen.add((n2, t)); nxt.append((n2, t))
                    if ok: break
                frontier = nxt
            if not ok: return True, f'length class {d}, node {start}: no closed walk with angle sum 2pi'
    return False, f'{len(cls)} distinct edge lengths; every node has a 2pi closed walk'
def cs_lp(ang, L):
    from scipy.optimize import linprog
    C = pi_combos(ang, Fr(1)) + pi_combos(ang, Fr(2))
    Dm = np.array([[c[e]/float(L[e]) for e in range(6)] for c in C])   # rows = combinations
    r = linprog(np.ones(6), A_ub=-Dm, b_ub=np.zeros(len(C)), bounds=[(None, None)]*6, method='highs')
    return float(r.fun) if r.status == 0 else ('unbounded' if r.status == 3 else f'status {r.status}')

# Goldberg families: scan a, refine, compare with each of the 40
def fam_members(a):
    g = goldberg1(a)
    if g is None: return {}
    h1, h2 = halves(g)
    return {'Goldberg 1 (prism third)': g, 'Goldberg half through edge 14': h1, 'Goldberg half through edge 23': h2}
TL = []
for n, raw in enumerate(RAW):
    ang = [Fr(a, b) for a, b in raw]
    V = tet_from_angles(ang); L = lengths(V); back = dihedrals(V)
    err = max(abs(back[k] - mp.mpf(ang[k].numerator)/ang[k].denominator) for k in range(6))
    TL.append((ang, V, L, err))
known_L = {nm: lengths(V) for nm, V in KNOWN.items()}
for r in (mp.sqrt(mp.mpf(2)/3), mp.sqrt(mp.mpf(3)/2)):
    Vx = edmonds(r)
    if Vx: known_L[f'Edmonds (xi) p/q={mp.nstr(r, 8)}'] = lengths(Vx)
# coarse scan of the families in a (float), then refine near every near-hit at 60 digits
PIDX = []
for p in PERMS:
    idx = [None]*6
    for k, (a, b) in enumerate(ORDER): idx[eid(p[a], p[b])] = k
    PIDX.append(idx)
mp.mp.dps = 20
fam_a, fam_nm, fam_L = [], [], []
for k in range(1, 4000):
    a = mp.mpf(k)/4000
    for nm, Vf in fam_members(a).items():
        if vol(Vf) > 0: fam_a.append(a); fam_nm.append(nm); fam_L.append([float(x) for x in lengths(Vf)])
fam_L = np.array(fam_L)
mp.mp.dps = 60
def best_match(L):
    Lf_ = np.array([float(x) for x in L]); dist = np.full(len(fam_L), 1e9)
    for idx in PIDX: dist = np.minimum(dist, np.abs(fam_L[:, idx] - Lf_).max(1))
    order = np.argsort(dist)[:6]
    return [(mp.mpf(float(dist[i])), fam_a[i], fam_nm[i]) for i in order]
for n, (ang, V, L, err) in enumerate(TL):
    rec = {'index': n + 1, 'angles_over_pi': [str(a) for a in ang], 'angle_roundtrip_error': mp.nstr(err, 3),
           'edge_lengths_unit_volume': [mp.nstr(x, 15) for x in L]}
    try:
        rows = DEHN.dehn(np.array([[float(c) for c in v] for v in V]), [[0,2,1],[0,1,3],[1,2,3],[0,3,2]], f'T{n+1}')
        rec['dehn_zero_control'] = rows['dehn_zero']
    except Exception as ex: rec['dehn_zero_control'] = f'error {ex}'
    rec['known_match'] = [nm for nm, Lk in known_L.items() if congruent(Lk, L)]
    cand = best_match(L)
    hits = []
    for d, a0, nm in cand:
        if d > mp.mpf('0.01'): continue
        # refine a by secant on the best relabeling distance
        def f(a):
            Vf = fam_members(a).get(nm)
            if Vf is None: return mp.mpf(1)
            Lf = lengths(Vf); return min(max(abs(x - y) for x, y in zip(relabel(Lf, p), L)) for p in PERMS)
        lo, hi = a0 - mp.mpf(1)/4000, a0 + mp.mpf(1)/4000
        for _ in range(200):   # golden-section on a unimodal distance
            m1 = lo + (hi - lo)*0.381966; m2 = hi - (hi - lo)*0.381966
            if f(m1) < f(m2): hi = m2
            else: lo = m1
        dd = f((lo + hi)/2)
        if dd < mp.mpf(10)**-25: hits.append({'family': nm, 'a': mp.nstr((lo + hi)/2, 25), 'distance': mp.nstr(dd, 3)})
    rec['goldberg_family_match'] = hits
    rec['nonf2f_excluded_CS_Prop2_3'] = cs_nonf2f_excluded(ang)
    rec['f2f_excluded_BDKS_Prop4_3'] = bdks_f2f_excluded(ang, L)
    try: rec['CS_LP_min'] = cs_lp(ang, L)
    except Exception as ex: rec['CS_LP_min'] = f'error {ex}'
    if rec['known_match'] or hits: cls = 'KNOWN TILER'
    elif rec['nonf2f_excluded_CS_Prop2_3'][0] and rec['f2f_excluded_BDKS_Prop4_3'][0]: cls = 'NON-TILER (both obstructions)'
    elif rec['f2f_excluded_BDKS_Prop4_3'][0]: cls = 'OPEN: face-to-face excluded, non-face-to-face open'
    elif rec['nonf2f_excluded_CS_Prop2_3'][0]: cls = 'OPEN: only face-to-face possible'
    else: cls = 'OPEN: both kinds possible'
    rec['class'] = cls; out['tetrahedra'].append(rec)
    print(f"T{n+1:02d} {[str(a) for a in ang]} -> {cls} | known={rec['known_match']} gold={[h['family'] for h in hits]} | dehn0={rec['dehn_zero_control']} | LP={rec['CS_LP_min']}", flush=True)
    print(f'PROGRESS {(n+1)/40:.3f} tetrahedron {n+1}/40', flush=True)
from collections import Counter
cnt = Counter(r['class'] for r in out['tetrahedra']); out['summary'] = dict(cnt)
dehn_ok = all(r['dehn_zero_control'] is True for r in out['tetrahedra'])
rt_ok = all(mp.mpf(r['angle_roundtrip_error']) < mp.mpf(10)**-40 for r in out['tetrahedra'])
out['checks'] = {'dehn_zero_all_40 (control)': dehn_ok, 'angle_roundtrip_all_40': rt_ok, 'seconds': round(time.time() - t0, 1)}
json.dump(out, open(OUT, 'w'), indent=1)
print('SUMMARY', dict(cnt), out['checks'])
print('FINAL ok' if (dehn_ok and rt_ok) else 'FINAL FAIL: a control failed')
