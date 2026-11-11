"""Atlas of the Chains (DICTO 11 Nov: "finding all of these would shed light on lots of other minor rules and theorems unifying them
all"). For every chain group (A3, B3, H3, A4, B4, F4, H4) and every seed of zeros and ones: the Wythoff polytope, its f-vector, cells
by type, whether it is simple, the Mirror Law split of its codimension-2 faces (on / off the mirrors, by face size and the types of the
two cells), and for simple 4-polytopes one generic sweep: the h-vector (corners by number of downward edges) and the swaps by the
types of the cells that let go and that meet (the balance law's ledger).  usage: atlas.py GROUPS (comma list)  -> atlas_<groups>.json
Controls: known f-vectors (cuboctahedron, 24-cell, 600-cell, 120-cell, bitruncated 600-cell) must come out."""
import sys, itertools, json, time
import numpy as np
from collections import Counter
from scipy.spatial import cKDTree
want = sys.argv[1].split(',') if len(sys.argv) > 1 else ['A3', 'B3', 'H3', 'A4', 'B4', 'F4']
sys.argv = ['x', '--no-h4']
exec(open('mirror_law.py').read().split('groups = [')[0])     # unit, A4, B4, F4, H4, A3, B3d, H3d, chain_any, roots_of, basis_reduce
GR = {'A3': basis_reduce(A3), 'B3': B3d, 'H3': H3d, 'A4': A4, 'B4': B4, 'F4': F4, 'H4': H4}
def group(R):
    n = len(R); G = [np.eye(n)]; gens = [np.eye(n) - 2 * np.outer(r, r) for r in R]; seen = {tuple(np.round(np.eye(n), 6).ravel())}; fr = list(G)
    while fr:
        nf = []
        for g in fr:
            for s in gens:
                h = s @ g; k = tuple(np.round(h, 6).ravel())
                if k not in seen: seen.add(k); G.append(h); nf.append(h)
        fr = nf
    return np.array(G)
def dedupe(Y, tol=1e-6):
    t = cKDTree(Y); keep = np.ones(len(Y), bool)
    for i, j in sorted(t.query_pairs(tol)):
        if keep[i] and keep[j]: keep[j] = False
    # second pass: anything still within tol of a kept point is a duplicate chain; re-run until stable
    Z = Y[keep]; t2 = cKDTree(Z)
    assert len(t2.query_pairs(tol)) == 0
    return Z
def norm_dir(n): n = n / np.linalg.norm(n); return n if n[np.argmax(np.abs(n))] > 0 else -n
out = {}; BAL = Counter()
for gname in want:
    R, bonds = chain_any(list(GR[gname])); n = len(R); Rm = np.array(R); G = group(R); ROOTS = roots_of(R)
    MIR = np.array([norm_dir(r) for r in ROOTS]); Wt = np.linalg.inv(Rm)
    print(f'{gname}: chain {bonds}, order {len(G)}, mirrors {len(ROOTS) // 2}', flush=True)
    for lab in itertools.product((0, 1), repeat=n):
        if not any(lab): continue
        t0 = time.time(); x = np.linalg.solve(Rm, np.array(lab, float)); P = dedupe(G @ x)
        tree = cKDTree(P); E = [(i, j) for i, j in tree.query_pairs(2 + 1e-6) if np.linalg.norm(P[i] - P[j]) > 2 - 1e-6]
        deg = Counter(); nb = [[] for _ in P]
        for i, j in E: nb[i].append(j); nb[j].append(i)
        degs = Counter(len(b) for b in nb)
        cells = {}                                       # facets, labelled by the node j of their fundamental weight
        for j in range(n):
            D = dedupe(np.array([unit(v) for v in (G @ Wt[:, j])]), 1e-7)
            for d in D:
                hv = P @ d; top = frozenset(np.where(hv > hv.max() - 1e-7)[0])
                if len(top) >= n and np.linalg.matrix_rank(P[list(top)] - P[list(top)].mean(0), tol=1e-7) == n - 1: cells[top] = j + 1
        ctype = Counter(); csize = {}
        for c, j in cells.items(): ctype[j] += 1; csize.setdefault(j, Counter())[len(c)] += 1
        by_v = {}
        for c, j in cells.items():
            for v in c: by_v.setdefault(v, []).append(c)
        faces = {}                                       # codimension-2 faces: two facets sharing an (n-2)-dimensional face
        for v, cs in by_v.items():
            for a, b in itertools.combinations(cs, 2):
                sh = a & b
                if len(sh) >= n - 1 and sh not in faces and np.linalg.matrix_rank(P[list(sh)] - P[list(sh)].mean(0), tol=1e-7) == n - 2:
                    faces[sh] = tuple(sorted((cells[a], cells[b])))
        split = Counter(); offn = []
        for f, tt in faces.items():
            nrm = np.linalg.svd(P[list(f)])[2][-1]; on = np.abs(MIR @ nrm).max() > 1 - 1e-7
            split[('on' if on else 'off', len(f), tt)] += 1
            if not on: offn.append(norm_dir(nrm))
        # second Vacuus: off-mirror central planes carrying >= 3 faces (beyond a face and its opposite)
        res2 = Counter()
        if offn:
            A = np.array(offn); used = np.zeros(len(A), bool)
            for i in range(len(A)):
                if used[i]: continue
                grp = np.where(np.abs(A @ A[i]) > 1 - 1e-7)[0]; used[grp] = True
                if len(grp) >= 3: res2[len(grp)] += 1
        simple = set(degs) == {n}
        rec = {'group': gname, 'chain': bonds, 'seed': lab, 'f': [len(P), len(E), len(faces) if n == 3 else len(faces), len(cells)] if n == 3 else None,
               'corners': len(P), 'edges': len(E), 'codim2_faces': len(faces), 'facets': len(cells), 'facets_by_node': dict(ctype),
               'facet_sizes_by_node': {k: dict(v) for k, v in csize.items()}, 'simple': simple, 'degrees': dict(degs),
               'offmirror_discs': dict(res2), 'mirror_split': {f'{a} {s}-gon/edge between types {t[0]}+{t[1]}': c for (a, s, t), c in sorted(split.items())}}
        if n == 4 and simple:
            allsw = []
            for k in range(3):
                u = unit(np.random.default_rng(7 + k).normal(size=4)); h = P @ u; hvec = Counter(); swaps = Counter()
                for v in range(len(P)):
                    down = [w for w in nb[v] if h[w] < h[v]]; up = [w for w in nb[v] if h[w] > h[v]]; hvec[len(down)] += 1
                    if len(down) != 2: continue
                    pair = lambda e: tuple(sorted(cells[c] for c in by_v[v] if e[0] in c and e[1] in c))
                    swaps[(pair(down), pair(up))] += 1
                allsw.append(swaps)
            same = all(a == allsw[0] for a in allsw)
            rev = all(sw[(X, Y)] == sw[(Y, X)] for sw in allsw for (X, Y) in sw)
            BAL['cases'] += 1; BAL['same'] += same; BAL['rev'] += rev
            if not (same and rev): print('    BALANCE BREAKS', gname, lab, [dict(a) for a in allsw])
            rec['h'] = [hvec[i] for i in range(5)]; rec['swaps'] = {f'{X}->{Y}': c for (X, Y), c in sorted(allsw[0].items())}
            rec['swaps_direction_independent'] = same; rec['swaps_reverse_balanced'] = rev
        out[f'{gname} {lab}'] = rec
        on = sum(c for (a, s, t), c in split.items() if a == 'on'); off = sum(c for (a, s, t), c in split.items() if a == 'off')
        print(f'  {lab}: corners {len(P)} edges {len(E)} codim-2 {len(faces)} facets {len(cells)} {dict(ctype)} simple {simple} | '
              f'on mirrors {on}, off {off}, off-mirror discs {dict(sorted(res2.items()))}' + (f" | h {rec['h']} swaps {rec['swaps']}" if 'h' in rec else '') + f'  ({time.time() - t0:.0f} s)', flush=True)
json.dump(out, open(f"atlas_{'_'.join(want)}.json", 'w'), indent=1, default=str)
# controls
C = {('B3', (0, 1, 0)): (12, 24), ('B3', (0, 1, 1)): (24, 36), ('H3', (0, 1, 0)): (30, 60), ('F4', (1, 0, 0, 0)): (24, 96),
     ('H4', (0, 0, 0, 1)): (120, 720), ('H4', (1, 0, 0, 0)): (600, 1200), ('H4', (0, 1, 1, 0)): (3600, 7200), ('A4', (1, 1, 1, 1)): (120, 240)}
ok = True
for (g, lab), (v, e) in C.items():
    r = out.get(f'{g} {lab}')
    if r is None: continue
    good = r['corners'] == v and r['edges'] == e; ok &= good; print('control', g, lab, r['corners'], r['edges'], 'ok' if good else f'EXPECTED {v} {e}')
print(f"general balance: {BAL['cases']} simple 4-polytopes, direction-independent {BAL['same']}, every swap type balanced by its reverse {BAL['rev']}")
print('FINAL ok' if ok else 'FINAL FAIL')
