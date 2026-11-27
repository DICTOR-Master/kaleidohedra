"""New-shape protocol (papers/new-shape-protocol.md) on the eleven special Vacuus-Solids of the Vacuus-Solids draft, Theorem 1
(27 Nov 2026; DICTO: "2, run the new-shape protocol"). With Claude (Anthropic). SECTOR BUILD (DICTO 27 Nov): one pit (the sector over one
face) is built exactly, then copied to every face by the symmetries of P that carry face 0 there; control: the copied walls equal the
directly built walls (all of them, 1e-9) before anything is measured.
Steps run here (numbers as in the protocol table): 1 identity (exact depth s, field of the coordinates); 2 counts (corners, edges, faces
as maximal flat regions of coplanar walls, Euler characteristic), symmetry order; 6 volume (EXACT, Q(sqrt r)), surface area and
isoperimetric quotient (float); 7 Dehn invariant (dehn.py numerical screen, calibrated: cube and truncated octahedron zero, octahedron
nonzero); 9 tiles alone? (Dehn nonzero -> no, Debrunner 1980 via the Dehn invariant page); 17 field of the corners.
Steps 3 and 19 (known solid, prior art) are answered from the draft's Section 6 and sources, not computed here; the others need shape
types these solids are not (convex, or a line family) and are marked n/a with the reason."""
import os, sys, json, itertools
from fractions import Fraction as Fr
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ST = os.path.join(HERE, '../..')
src = open(os.path.join(ST, '2026-11-25-partial-vacuus/scripts/exact_check.py')).read(); exec(src[:src.index('fails = 0')])
sys.path.insert(0, os.path.join(ST, '2026-11-04-dehn-screen/scripts')); import dehn as DH
def pr(*a): print(*a, flush=True)
def sym_group(Vf):
    """all orthogonal maps permuting the corners (proper and improper), from triples of corners (float, 1e-9)"""
    n = len(Vf); norms = np.linalg.norm(Vf, axis=1); out = []
    a, b, c = 0, None, None
    for j in range(1, n):
        if abs(np.linalg.det(np.array([Vf[0], Vf[j], np.zeros(3)])[:2, :2])) >= 0 and np.linalg.matrix_rank(np.array([Vf[0], Vf[j]])) == 2: b = j; break
    for k in range(1, n):
        if np.linalg.matrix_rank(np.array([Vf[0], Vf[b], Vf[k]])) == 3: c = k; break
    X = np.array([Vf[a], Vf[b], Vf[c]]).T
    for i, j, k in itertools.permutations(range(n), 3):
        if abs(norms[i] - norms[a]) > 1e-9 or abs(norms[j] - norms[b]) > 1e-9 or abs(norms[k] - norms[c]) > 1e-9: continue
        Y = np.array([Vf[i], Vf[j], Vf[k]]).T; M = Y @ np.linalg.inv(X)
        if not np.allclose(M @ M.T, np.eye(3), atol=1e-9): continue
        W = Vf @ M.T
        if all(np.min(np.linalg.norm(Vf - w, axis=1)) < 1e-9 for w in W): out.append(M)
    U = []
    for M in out:
        if not any(np.allclose(M, N, atol=1e-9) for N in U): U.append(M)
    return U
CAL = {}
for nm, V_ in (('cube', [(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]),
               ('octahedron', [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]),
               ('truncated octahedron', [p for t in itertools.permutations((0, 1, 2)) for p in itertools.product(*[(0,) if v == 0 else (-v, v) for v in t])])):
    Pc, Fc = DH.hull_faces(np.unique(np.array(V_, float), axis=0)); CAL[nm] = DH.dehn(Pc, Fc, nm)['dehn_zero']
cal_ok = CAL == {'cube': True, 'octahedron': False, 'truncated octahedron': True}
pr('calibration (Dehn zero?):', CAL, '-> as expected' if cal_ok else '-> UNEXPECTED')
rows = []
for Pn, Qn, s, r in TWELVE:
    VP = body(Pn, r); FP = faces(VP); Vf = np.array([flt(v) for v in VP])
    tips = [scl(s, scl(d / dot(N, N), N)) for idx, N, d in FP]
    # direct build: wall (tip f, edge u v) for every face
    direct = []
    for fi, (idx, N, d) in enumerate(FP):
        for i, j in zip(idx, idx[1:] + idx[:1]): direct.append(np.array([flt(VP[i]), flt(VP[j]), flt(tips[fi])]))
    # sector build: face 0's pit, copied by the symmetries that carry face 0 to face k
    G = sym_group(Vf); c0 = Vf[FP[0][0]].mean(0)
    sector = [np.array([flt(VP[i]), flt(VP[j]), flt(tips[0])]) for i, j in zip(FP[0][0], FP[0][0][1:] + FP[0][0][:1])]
    copied = []
    for k, (idx, N, d) in enumerate(FP):
        ck = Vf[idx].mean(0); M = next(M for M in G if np.allclose(M @ c0, ck, atol=1e-9))
        copied += [t @ M.T for t in sector]
    key = lambda T: tuple(sorted(tuple(np.round(p, 8)) for p in T))
    sector_ok = sorted(map(key, copied)) == sorted(map(key, direct))
    # the excavated solid: corners of P and the tips; faces = the wall triangles (each pit fully replaces its face)
    V_all = [VP[i] for i in range(len(VP))] + tips; Vfa = np.array([flt(v) for v in V_all]); nV0 = len(VP)
    tris = []
    for fi, (idx, N, d) in enumerate(FP):
        for i, j in zip(idx, idx[1:] + idx[:1]): tris.append([j, i, nV0 + fi])     # oriented with the material outside the pit
    # exact volume: P's volume minus the pits (pyramid on face f with apex tip f)
    def tet(a, b, c, d_): return dot(sub(b, a), cross(sub(c, a), sub(d_, a))) / 6
    o = (VP[0][0] * 0, VP[0][0] * 0, VP[0][0] * 0)
    vol_exact = sum(tet(o, VP[idx[0]], VP[idx[t]], VP[idx[t + 1]]) * (1 if tet(o, VP[idx[0]], VP[idx[t]], VP[idx[t + 1]]).sign() > 0 else -1) for idx, N, d in FP for t in range(1, len(idx) - 1)) \
        - sum(tet(tips[fi], VP[idx[0]], VP[idx[t]], VP[idx[t + 1]]) * (1 if tet(tips[fi], VP[idx[0]], VP[idx[t]], VP[idx[t + 1]]).sign() > 0 else -1) for fi, (idx, N, d) in enumerate(FP) for t in range(1, len(idx) - 1))
    # flat regions: walls in one plane that share an edge merge into one face
    def plane(t):
        n = np.cross(Vfa[t[1]] - Vfa[t[0]], Vfa[t[2]] - Vfa[t[0]]); n /= np.linalg.norm(n); return tuple(np.round(np.append(n, n @ Vfa[t[0]]), 7))
    parent = list(range(len(tris)))
    def find(x):
        while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
        return x
    emap = {}
    for ti, t in enumerate(tris):
        for a, b in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])): emap.setdefault(tuple(sorted((a, b))), []).append(ti)
    for e, L in emap.items():
        if len(L) == 2 and plane(tris[L[0]]) == plane(tris[L[1]]): parent[find(L[0])] = find(L[1])
    nF = len({find(i) for i in range(len(tris))})
    edges_true = sum(1 for e, L in emap.items() if not (len(L) == 2 and plane(tris[L[0]]) == plane(tris[L[1]])))
    used = {v for t in tris for v in t}
    V_true = 0
    for v in used:   # a corner where at least three flat faces meet
        fs = {find(ti) for ti, t in enumerate(tris) if v in t}
        V_true += len(fs) >= 3
    euler = V_true - edges_true + nF
    area = sum(np.linalg.norm(np.cross(Vfa[t[1]] - Vfa[t[0]], Vfa[t[2]] - Vfa[t[0]])) / 2 for t in tris)
    vol = float(vol_exact); iq = 36 * np.pi * vol ** 2 / area ** 3
    try: dz = DH.dehn(Vfa, tris, f'{Pn}/{Qn}')
    except Exception as ex: dz = f'error {ex}'
    row = dict(P=Pn, Q=Qn, s=repr(s), field=f'Q(sqrt{r})', sector_build_matches_direct=bool(sector_ok), symmetry_order=len(G),
               corners=V_true, edges=edges_true, faces=nF, euler=euler, volume_exact=repr(vol_exact), volume=vol, area=float(area), iq=float(iq),
               dehn=dz if not isinstance(dz, dict) else {k: (str(v) if not isinstance(v, (int, float, bool, str)) else v) for k, v in dz.items()})
    rows.append(row)
    pr(f'{Pn:24s} on {Qn:26s} s = {s}: sector build = direct {sector_ok} (group {len(G)}); V E F = {V_true} {edges_true} {nF}, Euler {euler}; '
       f'volume {vol:.6f} (exact {vol_exact}); area {area:.6f}; IQ {iq:.4f}; Dehn screen: {'zero' if isinstance(dz, dict) and dz['dehn_zero'] else ('nonzero' if isinstance(dz, dict) else dz)}')
json.dump(rows, open(os.path.join(HERE, '../data/protocol.json'), 'w'), indent=1, default=str)
pr('FINAL ok' if cal_ok and len(rows) == 11 and all(r['sector_build_matches_direct'] for r in rows) else 'FINAL FAIL')
