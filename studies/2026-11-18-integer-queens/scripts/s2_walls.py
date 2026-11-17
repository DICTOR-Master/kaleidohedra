#!/usr/bin/env python3
"""Integer Queens, part 2: walls and Vacuus, as in #110 section 2 (18 Nov 2026).
Hosts: 4_21 (E8 roots) and 2_31 (E7 roots); also 2_41 and 3_21.
 - Host facets: the host is one W(E)-orbit, so its normal fan coarsens the Coxeter fan and every facet normal is a W-image
   of a fundamental weight.  Each fundamental weight is tested exactly; its W-orbit (exact BFS) gives the facets of that kind.
 - Walls W(H) = mirror hyperplanes (root lines) + cross walls (facet-normal lines that are not root lines).
S-orbit hulls: by the rearrangement inequality the face of perms(a) maximising c is fixed by the ordered partition of
coordinates into level sets of c.  Facets and ridges = ordered partitions into 2 or 3 blocks with face dimension n-1, n-2.
Plates: span of each ridge; normal found by float SVD, then recovered as an integer vector and checked EXACTLY
(integer dot product zero on every ridge corner, sum zero).  Ranks: exact lower bound on chosen rows (Fractions).
Usage: s2_walls.py out.json 7|8  (runs the 3D controls and the E7 or E8 part)"""
import sys, os, json, time, math, itertools; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qlib import *
from collections import Counter
import scipy.linalg as sl
OUT = sys.argv[1]; PART = int(sys.argv[2]); C = Checks(); t0 = time.time(); out = {}

def rank_lb(V, want):
    """exact: True if the affine rank of rows V is >= want (rows chosen by pivoted QR, rank confirmed in Fractions)"""
    V = np.asarray(V, dtype=np.int64); D = V[1:] - V[0]
    if len(D) < want: return False
    _, _, piv = sl.qr(D.T.astype(float), pivoting=True, mode='economic')
    return int_rank(D[piv[:want]].tolist()) == want

def plate_normals(X, ridges):
    """exact plate normal line keys for a list of ridges (index arrays)"""
    d = X.shape[1]; res = [None] * len(ridges)
    groups = {}
    for i, r in enumerate(ridges): groups.setdefault(len(r), []).append(i)
    for k, ids in groups.items():
        R = np.array([ridges[i] for i in ids]); V = X[R]                       # (c, k, d)
        A = np.concatenate([V.astype(float), np.ones((len(ids), 1, d))], axis=1)
        _, s, Vh = np.linalg.svd(A, full_matrices=True)
        assert np.all(s[:, d - 2] > 1e-8), 'plate span too small'
        nv = Vh[:, -1, :]; nv = nv / nv[np.arange(len(ids)), np.abs(nv).argmax(1)][:, None]
        Lm = np.zeros(len(ids), dtype=np.int64); todo = np.ones(len(ids), bool)
        for L in range(1, 20001):
            w = nv[todo] * L; ok = np.all(np.abs(w - np.round(w)) < 1e-6, axis=1)
            t = np.nonzero(todo)[0][ok]; Lm[t] = L; todo[t] = False
            if not todo.any(): break
        assert not todo.any(), 'rational recovery failed'
        N = np.round(nv * Lm[:, None]).astype(np.int64)
        assert np.all(np.einsum('ckd,cd->ck', V, N) == 0) and np.all(N.sum(1) == 0) and np.all(np.abs(N).sum(1) > 0), 'exact check'
        for j, i in enumerate(ids): res[i] = line_key(N[j])
    return res

def vacuus(X, ridges, walls, central):
    """ridges: list of sorted index tuples.  walls: dict name -> set of line keys.  #110 sheets and kinds."""
    keys = plate_normals(X, [np.array(r) for r in ridges])
    plates = {}
    for r, k in zip(ridges, keys): plates.setdefault(k, []).append(r)
    per = Counter(len(v) for v in plates.values())
    if central:
        neg = as_perm(X, -X); rs = set(ridges)
        full = sum(1 for v in plates.values() if all(tuple(sorted(neg[i] for i in r)) in v for r in v))
        assert full == len(plates)      # Lemma 1 of #110
    else: full = 0
    single = per.get(1, 0)
    kind = 'heart' if full == len(plates) else 'non-heart' if single == len(plates) else 'inherited heart'
    hit = Counter(); cls = Counter()
    for k, v in plates.items():
        w = next((nm for nm, s in walls.items() if k in s), 'none'); hit[w] += 1
        sc = max(tuple(sorted(k, reverse=True)), tuple(sorted([-x for x in k], reverse=True)))
        cls[(w, len(v), sc)] += 1
    inw = len(plates) - hit['none']
    verdict = 'hidden' if hit['none'] == 0 else 'not hidden' if inw == 0 else 'partly hidden'
    return dict(ridges=len(ridges), plates=len(plates), ridges_per_plate=dict(sorted(per.items())), kind=kind,
                walls=dict(hit), plates_on_walls=inw, verdict=verdict,
                classes=[dict(wall=w, ridges_on_plate=r, normal_class=list(c), plates=m) for (w, r, c), m in sorted(cls.items())]), plates

# ---------------- S-orbit hulls ----------------
def orbit_hull(seed):
    X = orbit(seed); d = len(seed); n = d - 1; a = np.array(seed)
    labs, dims = [], []
    for nb in (2, 3):
        for lab in itertools.product(range(nb), repeat=d):
            if len(set(lab)) < nb: continue
            sizes = [lab.count(j) for j in range(nb)]; pos = 0; dim = 0
            for j in range(nb):
                ch = a[pos:pos + sizes[j]]; pos += sizes[j]
                dim += (sizes[j] - 1) if ch.max() != ch.min() else 0
            if dim in (n - 1, n - 2): labs.append(lab); dims.append(dim)
    L = np.array(labs); Cm = (L.max(1, keepdims=True) - L)                  # higher weight for earlier block
    vals = X @ Cm.T; M = vals == vals.max(0)
    faces = {}
    for j in range(len(labs)):
        key = M[:, j].tobytes()
        if key in faces: assert faces[key][0] == dims[j], 'same face, two dimensions'
        else: faces[key] = (dims[j], tuple(np.nonzero(M[:, j])[0]))
    facets = [v for dm, v in faces.values() if dm == n - 1]; ridges = [v for dm, v in faces.values() if dm == n - 2]
    return X, facets, ridges

def check_ridges(X, facets, ridges, n, label):
    ok_rank = all(rank_lb(X[list(f)], n - 1) for f in facets) and all(rank_lb(X[list(r)], n - 2) for r in ridges)
    F = np.zeros((len(facets), len(X)), np.float32); R = np.zeros((len(ridges), len(X)), np.float32)
    for i, f in enumerate(facets): F[i, list(f)] = 1
    for i, r in enumerate(ridges): R[i, list(r)] = 1
    outside = R @ (1 - F).T; cnt = (outside == 0).sum(1)
    C(ok_rank and np.all(cnt == 2), f'{label}: {len(facets)} facets (affine rank {n-1}, exact) and {len(ridges)} ridges (rank {n-2}, exact), every ridge in exactly 2 facets')

# ---------------- host machinery ----------------
def host_facets(H, S, fw, n):
    kinds = []; normals = []; masks = []
    for w in fw:
        assert all(x.q == 1 for x in w), 'weight not integral in scaled coordinates'
        W = np.array([int(x) for x in w], dtype=np.int64); v = H @ W; h = v.max(); face = np.nonzero(v == h)[0]
        if rank_lb(H[face], n - 1):
            O = weyl_orbit(W, S); vals = H @ O.T; Mk = vals == vals.max(0)
            assert np.all(vals.max(0) == h)
            kinds.append(dict(corners=len(face), count=len(O))); normals.append(O); masks.append(Mk)
    return kinds, np.concatenate(normals), np.concatenate(masks, axis=1)

def host_ridges(H, Fm, n):
    """ridges of the host from its facet incidence (columns of Fm), by pairwise intersection (exact rank)"""
    Fi = Fm.T.astype(np.float32); inter = Fi @ Fi.T
    ii, jj = np.nonzero(np.triu(inter >= n - 1, 1)); ridges = set()
    for i, j in zip(ii, jj):
        c = tuple(np.nonzero(Fm[:, i] & Fm[:, j])[0])
        if c not in ridges and rank_lb(H[list(c)], n - 2): ridges.add(c)
    return sorted(ridges)

def host_ridges_structured(H, Fm, n):
    """ridges from simplex facets (all (n-1)-subsets) and orthoplex facets (one corner of each antipodal pair)"""
    cnt = Counter()
    for j in range(Fm.shape[1]):
        f = np.nonzero(Fm[:, j])[0]
        if len(f) == n:
            for c in itertools.combinations(f, n - 1): cnt[tuple(c)] += 1
        elif len(f) == 2 * (n - 1):
            s = H[f].sum(0); pairs = []; used = set()
            for a in range(len(f)):
                if a in used: continue
                b = next(b for b in range(len(f)) if b != a and b not in used and np.all(len(f) * (H[f[a]] + H[f[b]]) == 2 * s))
                used |= {a, b}; pairs.append((f[a], f[b]))
            for ch in itertools.product(*pairs): cnt[tuple(sorted(ch))] += 1
        else: raise ValueError('facet neither simplex nor orthoplex')
    return sorted(cnt), cnt

# ---------------- 3D controls (#110 Figure 1) ----------------
ctl = {}
for nm, seed, exp in [('tetrahedron', (3, -1, -1, -1), (6, 6, 'non-heart')), ('octahedron', (1, 1, -1, -1), (12, 3, 'heart')),
                      ('cuboctahedron', (1, 0, 0, -1), (24, 4, 'heart'))]:
    X, facets, ridges = orbit_hull(seed)
    cs = set(index_of(-X)) == set(index_of(X))
    v, _ = vacuus(X, ridges, {}, cs)
    C((v['ridges'], v['plates'], v['kind']) == exp, f'control 3D {nm}: {v["ridges"]} edges on {v["plates"]} plates, {v["kind"]} (expected {exp})')
    ctl[nm] = v
out['controls_3D'] = ctl

# ---------------- E8 and E7 ----------------
setups = {8: dict(scale=3, host=(18, 3, None), other=(36, 3, None), hostname='4_21', othername='2_41',
                  known={'4_21': {(8, 17280), (14, 2160)}, '2_41': {(8, 17280), (126, 240)}}),
          7: dict(scale=4, host=(32, 4, (0, 2)), other=(24, 4, None), hostname='2_31', othername='3_21',
                  known={'2_31': {(7, 576), (27, 56)}, '3_21': {(7, 576), (12, 126)}})}
for n, S in setups.items():
    if n != PART: continue
    d = n + 1; res = out[f'E{n}'] = {}
    def shell(N2, q, resid):
        sd = shell_seeds(d, q, N2)
        if resid: sd = [s for s in sd if s[0] % q in resid]
        return sd
    host_seeds = shell(*S['host']); other_seeds = shell(*S['other'])
    Hh = np.concatenate([orbit(s) for s in host_seeds]); Ho = np.concatenate([orbit(s) for s in other_seeds])
    roots = Hh; Ssimple = simple_roots(roots); C(len(Ssimple) == n, f'E{n}: {len(Ssimple)} simple roots')
    fw = fundamental_weights(Ssimple, d)
    root_lines = {line_key(r) for r in roots}
    S_lines = {line_key(r) for r in roots if np.count_nonzero(r) == 2}
    C(len(root_lines) == {7: 63, 8: 120}[n] and len(S_lines) == n * (n + 1) // 2,
      f'E{n}: {len(root_lines)} mirrors, of which {len(S_lines)} are the S{d} mirrors')
    hosts = {}
    for hn, H in ((S['hostname'], Hh), (S['othername'], Ho)):
        kinds, normals, Fm = host_facets(H, Ssimple, fw, n)
        got = {(k['corners'], k['count']) for k in kinds}
        C(got == S['known'][hn], f'E{n} {hn}: facets {sorted(got)} (corners, count) = Coxeter/Gosset {sorted(S["known"][hn])}')
        lines = {line_key(v) for v in normals}
        hosts[hn] = dict(H=H, Fm=Fm, kinds=kinds, facet_lines=lines)
    hl = hosts[S['hostname']]['facet_lines']; ol = hosts[S['othername']]['facet_lines']
    cross = hl - root_lines
    C(len(hl & root_lines) == 0, f'E{n}: no facet normal of {S["hostname"]} is a root line, so cross walls = {len(cross)} facet-pair lines')
    walls = {f'S{d} mirror': S_lines, f'E{n} mirror (hidden)': root_lines - S_lines, 'cross wall': cross}
    res['walls'] = dict(mirrors=len(root_lines), S_mirrors=len(S_lines), hidden_mirrors=len(root_lines - S_lines), cross_walls=len(cross),
                        total=len(root_lines) + len(cross), other_facet_lines=len(ol), other_cross_equal=(ol - root_lines) == cross,
                        other_facet_lines_in_walls=len(ol & (root_lines | cross)))
    print(f"E{n}: walls of {S['hostname']} = {len(root_lines)} mirrors + {len(cross)} cross walls; {S['othername']} facet lines {len(ol)}, "
          f"of which {len(ol & root_lines)} mirrors, {len(ol & cross)} cross walls of the host")
    # hosts' own Vacuus
    for hn, hd in hosts.items():
        H, Fm = hd['H'], hd['Fm']
        if all(k['corners'] in (n, 2 * (n - 1)) for k in hd['kinds']):
            ridges, cnt = host_ridges_structured(H, Fm, n)
            C(all(v == 2 for v in cnt.values()), f'E{n} {hn}: {len(ridges)} ridges (from simplex and orthoplex facets), each in exactly 2 facets')
        else:
            ridges = host_ridges(H, Fm, n)
            check_ridges(H, [tuple(np.nonzero(Fm[:, j])[0]) for j in range(Fm.shape[1])], ridges, n, f'E{n} {hn}')
        v, _ = vacuus(H, ridges, walls, True); v['facets'] = hd['kinds']; v['corners'] = len(H)
        res[hn] = v; print(f'  {hn}: {v}')
    # S-orbit hulls
    res['orbits'] = []
    ordinary = {8: [(7, 2, 0, 0, 0, 0, 0, -4, -5), (4, 4, 4, -2, -2, -2, -2, -2, -2)], 7: [(5, 2, 0, 0, 0, 0, -3, -4), (3, 3, 3, 3, -3, -3, -3, -3)]}[n]
    for sd in ordinary:
        X, facets, ridges = orbit_hull(sd); cs = set(index_of(-X)) == set(index_of(X))
        v, _ = vacuus(X, ridges, walls, cs)
        exp_hidden = len(set(sd)) == 2      # a scaled hypersimplex is the same shape: must repeat the hidden verdict
        C((v['verdict'] == 'hidden') == exp_hidden and (exp_hidden or v['walls'].get('none', 0) > v['plates'] // 2),
          f'E{n} control orbit {sd} (scale {S["scale"]}): {v["plates"]} plates, {v["walls"]}, {v["verdict"]} (expected '
          f'{"hidden: a scaled copy of a shell orbit" if exp_hidden else "mostly on no wall: ordinary seed"})')
        res.setdefault('controls', []).append(dict(seed=list(sd), **{k: v[k] for k in ('ridges', 'plates', 'kind', 'walls', 'verdict')}))
    for sd in host_seeds + other_seeds:
        X, facets, ridges = orbit_hull(sd)
        lbl = f'E{n} orbit {[str(Fr(x, S["scale"])) for x in sd]} ({len(X)})'
        check_ridges(X, facets, ridges, n, lbl)
        cs = set(index_of(-X)) == set(index_of(X))
        v, plates = vacuus(X, ridges, walls, cs)
        if sd in other_seeds:     # also against the walls of its own shell polytope (2_41 or 3_21)
            ow = {f'S{d} mirror': S_lines, f'E{n} mirror (hidden)': root_lines - S_lines, 'cross wall': ol - root_lines}
            v2, _ = vacuus(X, ridges, ow, cs); v['walls_of_own_shell'] = dict(walls=v2['walls'], verdict=v2['verdict'])
        v.update(seed=[str(Fr(x, S['scale'])) for x in sd], corners=len(X), facets=len(facets), shell=S['hostname'] if sd in host_seeds else S['othername'],
                 facet_sizes=dict(sorted(Counter(len(f) for f in facets).items())))
        res['orbits'].append(v); print(f'  {v}')
    C(all(o['walls'].get(f'E{n} mirror (hidden)', 0) == 0 for o in res['orbits']), f'E{n}: no S-orbit hull has a plate on a hidden E{n} mirror')
json.dump(out, open(OUT, 'w'), indent=1, default=str)
print(f'time {time.time()-t0:.1f}s'); C.final()
