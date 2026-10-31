# Frank-Kasper topology engine for Splash Rules II (DICTO 2026-10-31).
# Reads a CIF (COD or AFLOW), expands the space group, builds the periodic Delaunay tetrahedra (dual of the Voronoi cells,
# the Frank-Kasper definition of neighbours) and returns the exact combinatorics: every count is an integer per unit cell.
# Floats are used ONLY to decide which points are neighbours (the Delaunay step); the topology is then checked for
# consistency (closed triangulated coordination shells, Euler characteristic 2, edge folds 5 or 6, Z = 12 + #6-bonds,
# no two 6-bonds adjacent in a shell, empty-sphere margin) and all quantities are integers / Fractions.
import re, itertools
from fractions import Fraction as Fr
from collections import Counter, defaultdict
import numpy as np
from scipy.spatial import Delaunay

def _tok(line):
    return re.findall(r"'[^']*'|\"[^\"]*\"|\S+", line)

def parse_cif(path):
    txt = open(path).read().splitlines()
    vals, loops, i = {}, [], 0
    while i < len(txt):
        l = txt[i].strip()
        if l.lower().startswith('loop_'):
            heads, rows = [], []
            i += 1
            while i < len(txt) and txt[i].strip().startswith('_'):
                heads.append(txt[i].strip().split()[0].lower()); i += 1
            buf = []
            while i < len(txt):
                s = txt[i].strip()
                if not s or s.startswith('#'):
                    i += 1
                    if not s and buf == [] and rows: break
                    continue
                if s.startswith('_') or s.lower().startswith('loop_') or s.lower().startswith('data_'): break
                if s.startswith(';'):
                    i += 1
                    while i < len(txt) and not txt[i].startswith(';'): i += 1
                    i += 1; continue
                buf += _tok(s)
                while len(buf) >= len(heads):
                    rows.append(buf[:len(heads)]); buf = buf[len(heads):]
                i += 1
            loops.append((heads, rows)); continue
        if l.startswith('_'):
            t = _tok(l)
            if len(t) >= 2: vals[t[0].lower()] = t[1]
        i += 1
    num = lambda s: float(re.sub(r'\(.*\)', '', s))
    cell = [num(vals['_cell_length_' + k]) for k in 'abc'] + [num(vals['_cell_angle_' + k]) for k in ('alpha', 'beta', 'gamma')]
    ops, sites = None, []
    for heads, rows in loops:
        for key in ('_symmetry_equiv_pos_as_xyz', '_space_group_symop_operation_xyz'):
            if key in heads:
                ops = [r[heads.index(key)].strip("'\"") for r in rows]
        if '_atom_site_fract_x' in heads:
            ix = [heads.index('_atom_site_fract_' + k) for k in 'xyz']
            il = heads.index('_atom_site_label')
            io = heads.index('_atom_site_occupancy') if '_atom_site_occupancy' in heads else None
            it = heads.index('_atom_site_type_symbol') if '_atom_site_type_symbol' in heads else None
            for r in rows:
                occ = num(r[io]) if io is not None and r[io] not in ('.', '?') else 1.0
                sites.append(dict(label=r[il], el=(r[it] if it is not None else re.sub(r'[^A-Za-z].*', '', r[il])),
                                  frac=[num(r[k]) for k in ix], occ=occ))
    assert ops, 'no symmetry operations in ' + path
    return dict(cell=cell, ops=ops, sites=sites)

def _op(s):
    rows = []
    for part in s.lower().replace(' ', '').split(','):
        coef, const = [0.0, 0.0, 0.0], 0.0
        for sign, term in re.findall(r'([+-]?)([^+-]+)', part):
            sg = -1.0 if sign == '-' else 1.0
            m = re.fullmatch(r'(\d*\.?\d*)\*?([xyz])', term)
            if m:
                coef['xyz'.index(m.group(2))] += sg * (float(m.group(1)) if m.group(1) else 1.0)
            else:
                const += sg * float(Fr(term))
        rows.append((coef, const))
    R = np.array([r[0] for r in rows]); t = np.array([r[1] for r in rows])
    return R, t

def lattice(cell):
    a, b, c, al, be, ga = cell
    al, be, ga = np.radians([al, be, ga])
    A = np.array([a, 0, 0]); B = np.array([b * np.cos(ga), b * np.sin(ga), 0])
    cx = c * np.cos(be); cy = c * (np.cos(al) - np.cos(be) * np.cos(ga)) / np.sin(ga)
    C = np.array([cx, cy, np.sqrt(c * c - cx * cx - cy * cy)])
    return np.array([A, B, C])

def expand(cif, keep=lambda s: True, tol=2e-3):
    ops = [_op(o) for o in cif['ops']]
    pos, lab = [], []
    for s in cif['sites']:
        if not keep(s): continue
        f = np.array(s['frac'])
        for R, t in ops:
            p = (R @ f + t) % 1.0
            dup = False
            for q in pos:
                d = (p - q + 0.5) % 1.0 - 0.5
                if np.max(np.abs(d)) < tol: dup = True; break
            if not dup:
                pos.append(p); lab.append(s['label'])
    return np.array(pos), lab

def topology(L, frac, labels=None, reach=None):
    """Periodic Delaunay tetrahedra of the point set frac (fractional, n x 3) in the lattice L (rows = vectors)."""
    n = len(frac)
    if reach is None:
        # enough cell copies to cover ~9 Angstrom around the cell
        cover = 3.0 * (abs(np.linalg.det(L)) / n) ** (1 / 3)      # ~3 neighbour distances
        reach = [1 + int(np.ceil(cover / (abs(np.linalg.det(L)) / np.linalg.norm(np.cross(L[(k + 1) % 3], L[(k + 2) % 3]))))) for k in range(3)]
    shifts = list(itertools.product(*[range(-r, r + 1) for r in reach]))
    pts, ids = [], []
    for s in shifts:
        for i in range(n):
            pts.append((frac[i] + s) @ L); ids.append((i, s))
    pts = np.array(pts)
    D = Delaunay(pts, qhull_options='Qbb Qc Qz Q12')
    tets = set()
    inner = lambda s: all(abs(s[k]) <= reach[k] - 1 for k in range(3))
    margin = np.inf
    for simp in D.simplices:
        vs = [ids[v] for v in simp]
        if not any(v[1] == (0, 0, 0) for v in vs): continue
        if not all(inner(v[1]) for v in vs): continue
        base = min(vs)
        sh = base[1]
        can = tuple(sorted((v[0], tuple(v[1][k] - sh[k] for k in range(3))) for v in vs))
        tets.add(can)
    # empty-sphere margin (smallest relative gap between circumradius and the next point) on the canonical tets
    from scipy.spatial import cKDTree
    tree = cKDTree(pts)
    for t in list(tets)[:4000]:
        P = np.array([(frac[i] + np.array(s)) @ L for i, s in t])
        A = 2 * (P[1:] - P[0]); bb = np.sum(P[1:] ** 2 - P[0] ** 2, axis=1)
        cen = np.linalg.solve(A, bb); r = np.linalg.norm(P[0] - cen)
        d, _ = tree.query(cen, k=6)
        margin = min(margin, (d[4] - r) / r)
    return tets, margin

def analyse(L, frac, labels=None):
    n = len(frac)
    tets, margin = topology(L, frac, labels)
    # incidence at each site of the cell: tets containing (i, shift) translated so that i sits at shift 0
    inc = defaultdict(list)
    for t in tets:
        for (i, s) in t:
            inc[i].append(tuple((j, tuple(u[k] - s[k] for k in range(3))) for (j, u) in t))
    T = len(tets)
    Z, six, shell6, ok, msgs = {}, {}, {}, True, []
    edgefold = {}
    for i in range(n):
        me = (i, (0, 0, 0))
        tri = [tuple(sorted(v for v in t if v != me)) for t in inc[i]]
        nb = sorted({v for tr in tri for v in tr})
        # link graph of the shell
        edges = Counter()
        for tr in tri:
            for a, b in itertools.combinations(tr, 2): edges[(a, b) if a < b else (b, a)] += 1
        if any(c != 2 for c in edges.values()): ok = False; msgs.append(f'site {i}: shell not closed')
        V, E, F = len(nb), len(edges), len(tri)
        if V - E + F != 2: ok = False; msgs.append(f'site {i}: Euler {V - E + F}')
        deg = Counter()
        for (a, b) in edges: deg[a] += 1; deg[b] += 1
        Z[i] = V
        folds = {v: deg[v] for v in nb}     # tetrahedra around bond (i, v) = degree of v in the shell
        bad = [f for f in folds.values() if f not in (5, 6)]
        if bad: ok = False; msgs.append(f'site {i}: bond folds {sorted(Counter(bad).items())}')
        sixv = [v for v in nb if folds[v] == 6]
        six[i] = len(sixv)
        if any(((a, b) if a < b else (b, a)) in edges for a, b in itertools.combinations(sixv, 2)):
            ok = False; msgs.append(f'site {i}: adjacent 6-vertices')
        for v in nb: edgefold[(me, v)] = folds[v]
        # 6-bonds inside the shell (between two neighbours of i)
        shell6[i] = None
    for i in range(n):
        if Z[i] != 12 + six[i]: ok = False; msgs.append(f'site {i}: Z {Z[i]} != 12 + {six[i]}')
    return dict(n=n, T=T, Z=Z, six=six, tets=tets, edgefold=edgefold, ok=ok, msgs=msgs[:12], margin=margin)

def bonds(res):
    """Canonical bond list ((i,(0,0,0)),(j,s)) with i<=j convention, fold."""
    out = {}
    for (a, b), f in res['edgefold'].items():
        i, s = b
        key = (a[0], (0, 0, 0), i, s)
        rkey = (i, (0, 0, 0), a[0], tuple(-x for x in s))
        if rkey in out: continue
        out[key] = f
    return out

# ---------------------------------------------------------------------------------------------------------------
# Census: every count is an integer per unit cell. Keys are strings so that the JSON is readable.
def census(res):
    n, Z, tets = res['n'], res['Z'], res['tets']
    zc = Counter(Z.values())
    B = bonds(res)
    def zz(i): return Z[i]
    C = Counter()
    C['N'] = n; C['T'] = len(tets)
    for z in (12, 14, 15, 16): C[f'N{z}'] = zc.get(z, 0)
    C['Zsum'] = sum(Z.values())
    for (i, _, j, s), f in B.items():
        a, b = sorted((Z[i], Z[j]))
        C[f'bond{f}_{a}_{b}'] += 1; C[f'bond{f}'] += 1; C['bond'] += 1
    # tetrahedra: number of 6-edges and vertex types
    fold = {}
    for (i, _, j, s), f in B.items():
        fold[(i, (0, 0, 0), j, s)] = f; fold[(j, (0, 0, 0), i, tuple(-x for x in s))] = f
    def ef(u, v):
        (i, si), (j, sj) = u, v
        return fold[(i, (0, 0, 0), j, tuple(sj[k] - si[k] for k in range(3)))]
    triangles = Counter()
    for t in tets:
        j6 = [(u, v) for u, v in itertools.combinations(t, 2) if ef(u, v) == 6]
        typ = ''.join(str(Z[v[0]] - 10) for v in sorted(t, key=lambda v: Z[v[0]]))   # e.g. '2246' = 12,12,14,16
        C[f'tet_j{len(j6)}'] += 1
        if len(j6) == 2:
            C['tet_j2_opposite' if not (set(j6[0]) & set(j6[1])) else 'tet_j2_adjacent'] += 1
        C[f'tet_v{typ}'] += 1
        C[f'tet_v{typ}_j{len(j6)}'] += 1
    # triangles (faces) = 2T ; per-site shell data: 6-bonds inside each shell
    inc = defaultdict(list)
    for t in tets:
        for (i, s) in t:
            inc[i].append([(j, tuple(u[k] - s[k] for k in range(3))) for (j, u) in t if (j, u) != (i, s)])
    for i in range(n):
        sh = set()
        for tri in inc[i]:
            for u, v in itertools.combinations(tri, 2):
                if ef(u, v) == 6: sh.add(tuple(sorted((u, v))))
        C[f'shell6_Z{Z[i]}'] += len(sh)
        # neighbour types of each site type
        for (j, s) in {v for tri in inc[i] for v in tri}:
            C[f'nb_{Z[i]}_{Z[j]}'] += 1
    # rings around 6-bonds: types of the 6 common neighbours (each ring site is joined to both ends by 5-bonds)
    nbr = defaultdict(set)
    for (i, _, j, s), f in B.items():
        nbr[i].add((j, s)); nbr[j].add((i, tuple(-x for x in s)))
    def nb_of(v):
        i, s = v
        return {(j, tuple(u[k] + s[k] for k in range(3))) for (j, u) in nbr[i]}
    for (i, _, j, s), f in B.items():
        if f != 6: continue
        ring = nb_of((i, (0, 0, 0))) & nb_of((j, s))
        assert len(ring) == 6
        a, b = sorted((Z[i], Z[j]))
        rc = Counter(Z[v[0]] for v in ring)
        C[f'ring_{a}_{b}_n12={rc.get(12, 0)}'] += 1
        C[f'ring6_Z12'] += rc.get(12, 0)
    return C

def skeleton(res):
    """Major skeleton = graph of 6-bonds on the non-icosahedral sites. Returns per component: sites, edges and the rank of
    its translation lattice (1 = isolated lines, 2 = layers, 3 = 3D network)."""
    Z = res['Z']; B = bonds(res)
    adj = defaultdict(list)
    for (i, _, j, s), f in B.items():
        if f == 6:
            adj[i].append((j, s)); adj[j].append((i, tuple(-x for x in s)))
    seen, comps = {}, []
    for r in adj:
        if r in seen: continue
        seen[r] = (0, 0, 0); stack = [r]; cyc = []; nodes = [r]
        while stack:
            a = stack.pop()
            for (b, s) in adj[a]:
                pos = tuple(seen[a][k] + s[k] for k in range(3))
                if b not in seen:
                    seen[b] = pos; stack.append(b); nodes.append(b)
                else:
                    d = tuple(pos[k] - seen[b][k] for k in range(3))
                    if any(d): cyc.append(d)
        rank = int(np.linalg.matrix_rank(np.array(cyc))) if cyc else 0
        comps.append(dict(sites=len(nodes), edges=sum(len(adj[a]) for a in nodes) // 2, rank=rank,
                          deg=dict(Counter(len(adj[a]) for a in nodes))))
    return comps
