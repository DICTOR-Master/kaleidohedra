#!/usr/bin/env python3
"""PILOT (question b): Grünbaum 2010 (Bilinski paper, v2/3/10 p. 17): a rhombic monohedral parallelohedron with every zone of exactly k faces, k >= 10.
Model: solids = finite sets of golden rhombohedra p + [0,1]e_i + [0,1]e_j + [0,1]e_k, p in Z^n, on n of the six 5-fold axes of the icosahedron
(any two of these axes span the same golden rhombus, so every such solid is monohedral). Start: the convex zonotope on the n axes
(n = 3 golden rhombohedron, 4 Bilinski dodecahedron, 5 rhombic icosahedron, 6 rhombic triacontahedron), cut into its C(n,3) rhombohedra.
Moves: remove one rhombohedron, or add one that shares a face with the solid and does not overlap it (separating axes: the 15 face normals).
Keep: surfaces that are closed 2-manifolds of Euler characteristic 2 with every zone of exactly k = 2(n-1) faces.
Translation-tiling test (Grünbaum's condition first: faces in translated pairs with opposite outward sides): candidate lattices = Z-spans of
three independent pair translations; accept when the lattice has rank 3 in Z^n (a discrete lattice in R^3), covolume = volume, and no lattice
translate (|lambda| <= diameter) overlaps the solid. Controls: n = 4 depth 0 must find the Bilinski dodecahedron (k = 6) tiling;
n = 5 should find Grünbaum's doubly indented icosahedra D1, D2 (k = 8) within depth 2; n = 6 depth 0 (the triacontahedron) must NOT tile.
Floating point with tolerance 1e-9 (pilot); exact Q(sqrt5) re-check in the full run. Prints PROGRESS and FINAL."""
import sys, itertools, json, time, math
import numpy as np
t0 = time.time()
phi = (1 + 5**0.5)/2
AX = np.array([(1, phi, 0), (-1, phi, 0), (0, 1, phi), (0, -1, phi), (phi, 0, 1), (-phi, 0, 1)], float)
OUT = sys.argv[1] if len(sys.argv) > 1 else 'zone-pilot.json'
DEPTH = {3: 0, 4: 1, 5: 2, 6: 2}
def run(n):
    E = AX[:n]; T = list(itertools.combinations(range(n), 3)); PAIRS = list(itertools.combinations(range(n), 2))
    NRM = {pr: np.cross(E[pr[0]], E[pr[1]]) for pr in PAIRS}; NRM = {k: v/np.linalg.norm(v) for k, v in NRM.items()}
    def pos(p): return np.asarray(p, float) @ E
    def interval(c, nv):
        p, t = c; base = pos(p) @ nv; proj = [E[a] @ nv for a in t]
        return base + sum(min(0, x) for x in proj), base + sum(max(0, x) for x in proj)
    def overlap(c1, c2):
        for nv in NRM.values():
            a0, a1 = interval(c1, nv); b0, b1 = interval(c2, nv)
            if a1 <= b0 + 1e-9 or b1 <= a0 + 1e-9: return False
        return True
    def unit(a): v = [0]*n; v[a] = 1; return tuple(v)
    def add(p, q): return tuple(x + y for x, y in zip(p, q))
    def sub(p, q): return tuple(x - y for x, y in zip(p, q))
    def faces_of(c):
        p, (i, j, k) = c; out = []
        for (a, b), o in (((i, j), k), ((i, k), j), ((j, k), i)):
            out.append(((p, (a, b)), -1, c)); out.append(((add(p, unit(o)), (a, b)), +1, c))   # side relative to the third axis
        return out
    def surface(S):
        cnt = {}
        for c in S:
            for f, side, cc in faces_of(c):
                cnt.setdefault(f, []).append((side, cc))
        return {f: v[0] for f, v in cnt.items() if len(v) == 1}, cnt
    def analyse(S):
        surf, _ = surface(S)
        F = len(surf); edges = {}; verts = set()
        for (p, (a, b)) in surf:
            for (q, d) in ((p, a), (p, b), (add(p, unit(b)), a), (add(p, unit(a)), b)):
                edges.setdefault((q, d), []).append((p, (a, b)))
            for q in (p, add(p, unit(a)), add(p, unit(b)), add(add(p, unit(a)), unit(b))): verts.add(q)
        if any(len(v) != 2 for v in edges.values()): return None
        chi = len(verts) - len(edges) + F
        # zones: per direction d, components of faces containing d linked through d-edges
        zones = []
        for d in range(n):
            fs = [f for f in surf if d in f[1]]; seen = set()
            for f0 in fs:
                if f0 in seen: continue
                comp = [f0]; seen.add(f0); st = [f0]
                while st:
                    f = st.pop(); p, (a, b) = f; o = b if a == d else a
                    for q in (p, add(p, unit(o))):
                        for g in edges.get((q, d), []):
                            if g not in seen: seen.add(g); comp.append(g); st.append(g)
                zones.append(len(comp))
        return {'faces': F, 'chi': chi, 'zones': sorted(zones), 'surf': surf}
    def volume(S): return sum(abs(np.linalg.det(E[list(t)])) for _, t in S)
    def tiles(S, info):
        surf = info['surf']; byp = {}
        for (p, pr), (side, c) in surf.items(): byp.setdefault(pr, []).append((p, side))
        trans = set()
        for pr, L in byp.items():
            for (p, s), (q, s2) in itertools.permutations(L, 2):
                if s == -s2 and s == -1: trans.add(sub(q, p))
        trans = sorted(trans)
        if not trans: return False, 'no translated face pairs'
        Vol = volume(S); P0 = np.array([pos(c[0]) for c in S]); diam = 2*(np.abs(P0).max() + 3*phi*2)
        tried = 0
        for a, b, c in itertools.combinations(trans, 3):
            M = np.array([a, b, c], float)
            if np.linalg.matrix_rank(M) < 3: continue
            span = np.array(trans + [a, b, c], float)
            if np.linalg.matrix_rank(span) > 3: pass   # other translations outside the lattice: allowed, tested below by overlaps
            L3 = M @ E
            if abs(abs(np.linalg.det(L3)) - Vol) > 1e-7: continue
            tried += 1; ok = True
            for co in itertools.product(range(-3, 4), repeat=3):
                if co == (0, 0, 0): continue
                lam = tuple(int(x) for x in np.array(co) @ M)
                if np.linalg.norm(pos(lam)) > diam: continue
                for c1 in S:
                    c1s = (add(c1[0], lam), c1[1])
                    if any(overlap(c1s, c2) for c2 in S): ok = False; break
                if not ok: break
            if ok: return True, f'lattice {a}, {b}, {c}'
            if tried > 200: break
        return False, f'{tried} lattices with covolume = volume tried; all overlap' if tried else 'no lattice with covolume = volume'
    def canon(S):
        m = min(c[0] for c in S); return frozenset((sub(c[0], m), c[1]) for c in S)
    def zonotope_cells(m):   # fine tiling of Z(e_0..e_{m-1}) by induction: Z_m = Z_{m-1} + the e_{m-1} zone over its upper boundary
        if m == 3: return {((0,)*n, (0, 1, 2))}
        cells = zonotope_cells(m - 1); top = m - 1
        for i, j in itertools.combinations(range(top), 2):
            u = np.cross(E[i], E[j]); u = u if u @ E[top] > 0 else -u
            off = [0]*n
            for q in range(top):
                if q not in (i, j) and E[q] @ u > 0: off[q] = 1
            cells.add((tuple(off), (i, j, top)))
        return cells
    start = frozenset(zonotope_cells(n))
    k = 2*(n - 1); res = {'n': n, 'k': k, 'depth': DEPTH[n]}
    info0 = analyse(start)
    res['start_surface'] = None if info0 is None else {'faces': info0['faces'], 'chi': info0['chi'], 'zones': info0['zones']}
    level = {canon(start)}; seen = set(level); found = []; stats = []
    for depth in range(DEPTH[n] + 1):
        good = 0
        for S in level:
            info = analyse(S)
            if info and info['chi'] == 2 and all(z == k for z in info['zones']):
                good += 1; ok, why = tiles(S, info)
                if ok: found.append({'depth': depth, 'cells': len(S), 'faces': info['faces'], 'why': why,
                                     'cells_list': sorted([list(c[0]), list(c[1])] for c in S)})
        stats.append({'depth': depth, 'states': len(level), 'sphere_like_all_zones_k': good, 'tilers_so_far': len(found)})
        print(f'n={n} depth={depth} states={len(level)} good={good} tilers={len(found)} t={time.time()-t0:.0f}s', flush=True)
        if depth == DEPTH[n]: break
        nxt = set()
        for S in level:
            Sl = list(S)
            for c in Sl:
                R = S - {c}
                if R:
                    cr = canon(R)
                    if cr not in seen: seen.add(cr); nxt.add(cr)
            surf, _ = surface(S)
            for (p, pr), (side, c0) in surf.items():
                for o in range(n):
                    if o in pr: continue
                    t = tuple(sorted(pr + (o,)))
                    nv = NRM[pr]; out_dir = side*(E[[x for x in c0[1] if x not in pr][0]] @ nv)
                    q = p if (E[o] @ nv)*out_dir > 0 else sub(p, unit(o))   # the new cell lies on the outer side of the face
                    c = (q, t)
                    if c in S or any(overlap(c, d) for d in Sl): continue
                    cr = canon(S | {c})
                    if cr not in seen: seen.add(cr); nxt.add(cr)
        level = nxt
    res['levels'] = stats; res['tilers'] = found[:20]; res['n_tilers'] = len(found)
    return res
out = {}
for i, n in enumerate((3, 4, 5, 6)):
    out[n] = run(n); print(f'PROGRESS {(i+1)/4:.2f} n={n} done', flush=True)
json.dump(out, open(OUT, 'w'), indent=1)
ctrl = (out[4]['levels'][0]['tilers_so_far'] >= 1, out[6]['levels'][0]['tilers_so_far'] == 0, out[3]['levels'][0]['tilers_so_far'] >= 1)
print('CONTROLS rhombohedron tiles at depth 0:', ctrl[2], '| Bilinski tiles at depth 0:', ctrl[0], '| triacontahedron does not tile:', ctrl[1])
print('RESULT k=8 tilers found (n=5):', out[5]['n_tilers'], '| k=10 tilers found (n=6, depth<=2):', out[6]['n_tilers'], f'| {time.time()-t0:.0f}s')
print('FINAL ok' if all(ctrl) else 'FINAL FAIL: a control failed')
