"""Periodic label maps -> neighbour graphs -> frames for the shared event logger (2D and 3D).

CREDIT: periodic_label, graph, torus_euler, match and to_tiling are copied UNCHANGED from the Sun stream's
studies/2026-11-15-sun-granulation/scripts/tiles.py (15 Nov 2026), so that the two streams build tilings the same way.
Watershed: scikit-image (van der Walt et al. 2014, PeerJ 2:e453; BSD licence). Added here: periodic fragment clean-up (each label
one connected piece, 2D and 3D), the 3D contact graph, and a periodic marker watershed for the bubble toy.

2D rules (from the Sun stream): two cells touch when they share a pixel edge (4-adjacency, periodic). Junctions: 2 x 2 pixel blocks
whose four internal edges separate at least three distinct pairs of cells. Boundary segments per pair = (junction blocks where the
pair ends) / 2; a touching pair that ends at no junction is a closed loop (an island cell). Torus Euler: V - E + F = 0.
3D rule (added): two cells touch when they share a voxel face (6-adjacency, periodic). No edges or corners are built, so the
logger's 3D Euler check does not run on these frames (stated in the README)."""
import numpy as np
from scipy import ndimage as ndi
from skimage.segmentation import watershed
from skimage.measure import label as cclabel
from collections import defaultdict


# ---------------- copied unchanged from the Sun stream (see CREDIT) ----------------
def periodic_label(mask):
    lab, n = ndi.label(mask)
    par = np.arange(n + 1)
    def find(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    for a, b in list(zip(lab[:, 0], lab[:, -1])) + list(zip(lab[0, :], lab[-1, :])):
        if a and b:
            ra, rb = find(a), find(b)
            if ra != rb: par[ra] = rb
    roots = np.array([find(a) for a in range(n + 1)])
    u, inv = np.unique(roots, return_inverse=True)
    return inv[lab]


def graph(lab):
    """Contacts with lengths, junctions (cell tuples), segments per pair, loops; periodic."""
    R = np.roll(lab, -1, 1); D = np.roll(lab, -1, 0)
    contacts = defaultdict(int)
    for A, B in ((lab, R), (lab, D)):
        m = A != B
        if not m.any(): continue
        a, b = np.minimum(A[m], B[m]), np.maximum(A[m], B[m])
        up, cnt = np.unique(np.stack([a, b], 1), axis=0, return_counts=True)
        for (x, y), c in zip(up.tolist(), cnt.tolist()): contacts[(x, y)] += c
    a, b, c, d = lab, R, D, np.roll(R, -1, 0)      # block [[a, b], [c, d]]
    e1 = (a, b); e2 = (a, c); e3 = (b, d); e4 = (c, d)
    nd = sum((p != q).astype(np.int8) for p, q in (e1, e2, e3, e4))
    cand = np.argwhere(nd >= 3)
    junctions, ends = [], defaultdict(int)
    for i, j in cand:
        pairs = set()
        for p, q in (e1, e2, e3, e4):
            x, y = int(p[i, j]), int(q[i, j])
            if x != y: pairs.add((min(x, y), max(x, y)))
        if len(pairs) >= 3:
            cells = sorted({v for pr in pairs for v in pr})
            junctions.append((tuple(cells), tuple(sorted(pairs))))
            for pr in pairs: ends[pr] += 1
    segs, loops, odd = {}, 0, 0
    for pr in contacts:
        e = ends.get(pr, 0)
        if e == 0: segs[pr] = 1; loops += 1
        else:
            if e % 2: odd += 1
            segs[pr] = max(1, e // 2)
    return dict(contacts=dict(contacts), junctions=junctions, segs=segs, loops=loops, odd=odd)


def torus_euler(ncells, G):
    V = len(G['junctions']) + G['loops']
    E = sum(G['segs'].values())
    return V - E + ncells


def match(prev, lab, next_id):
    """prev: persistent label map; lab: raw label map. Returns (persistent map, parents, heirs, next_id)."""
    K = np.int64(lab.max() + 1)
    key = prev.astype(np.int64) * K + lab
    u, cnt = np.unique(key, return_counts=True)
    old, new = u // K, u % K
    area_old = dict(zip(*np.unique(prev, return_counts=True)))
    area_new = dict(zip(*np.unique(lab, return_counts=True)))
    best_par, best_heir = {}, {}
    for o, n, c in zip(old, new, cnt):
        if c > best_par.get(n, (0, -1))[1]: best_par[n] = (o, c)
        if c > best_heir.get(o, (0, -1))[1]: best_heir[o] = (n, c)
    mp = {}
    for n, (o, c) in best_par.items():
        if best_heir[o][0] == n: mp[n] = o
    for n in area_new:
        if n not in mp: mp[n] = next_id; next_id += 1
    lut = np.zeros(K, dtype=np.int64)
    for n, v in mp.items(): lut[n] = v
    out = lut[lab]
    kept = set(mp[n] for n in mp if mp[n] in area_old)
    born = {mp[n] for n in area_new if mp[n] not in area_old}
    died = set(area_old) - kept
    parents, heirs = defaultdict(dict), defaultdict(dict)
    for o, n, c in zip(old, new, cnt):
        pn = mp[n]
        if pn in born and c / area_new[n] >= 0.01: parents[pn][o] = c / area_new[n]
        if o in died and c / area_old[o] >= 0.01: heirs[o][pn] = c / area_old[o]
    return out, dict(parents), dict(heirs), next_id


def to_tiling(Tiling, lab, G, t, parents=None, heirs=None):
    cells = [str(c) for c in np.unique(lab)]
    bnd = [[str(a), str(b)] for (a, b), k in G['segs'].items() for _ in range(k)]
    jn = [[str(c) for c in cs] for cs, _ in G['junctions']]
    par = {str(k): {str(a): s for a, s in v.items()} for k, v in (parents or {}).items()}
    hr = {str(k): {str(a): s for a, s in v.items()} for k, v in (heirs or {}).items()}
    return Tiling(cells, bnd, jn, 2, 'torus', t, loops=G['loops'], parents=par, heirs=hr)
# ---------------- end of copied part ----------------


def periodic_components(lab):
    """Connected pieces of equal label (face adjacency), periodic in every axis. Returns piece map 0..n-1."""
    comp = cclabel(lab, background=-1, connectivity=1)       # equal-value regions; labels start at 1 (no background value used)
    n = comp.max() + 1
    par = np.arange(n)
    def find(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    for ax in range(lab.ndim):
        lo = np.take(lab, 0, axis=ax).ravel(); hi = np.take(lab, -1, axis=ax).ravel()
        clo = np.take(comp, 0, axis=ax).ravel(); chi = np.take(comp, -1, axis=ax).ravel()
        m = lo == hi
        for a, b in set(zip(clo[m].tolist(), chi[m].tolist())):
            ra, rb = find(a), find(b)
            if ra != rb: par[ra] = rb
    roots = np.array([find(a) for a in range(n)])
    return np.unique(roots, return_inverse=True)[1][comp]


def clean_fragments(lab, protect=None, max_iter=20):
    """Make every label one connected piece: keep each label's largest piece; the pixels of its other pieces take the most common
    label among their face neighbours (repeated until none is left). Returns (lab, number of pixels reassigned).
    protect: a label (e.g. the liquid of a wet foam) that may lie in several pieces and is left alone."""
    moved = 0
    for _ in range(max_iter):
        pc = periodic_components(lab)
        npc = pc.max() + 1
        size = np.bincount(pc.ravel(), minlength=npc)
        plab = np.zeros(npc, dtype=lab.dtype); plab[pc.ravel()] = lab.ravel()
        best = {}
        for p in np.argsort(size):                      # ascending: the last write per label is the largest piece
            best[int(plab[p])] = int(p)
        bad_piece = np.ones(npc, bool)
        for l, p in best.items(): bad_piece[p] = False
        if protect is not None: bad_piece[plab == protect] = False
        bad = bad_piece[pc]
        if not bad.any(): return lab, moved
        moved += int(bad.sum())
        # majority of good face neighbours
        votes = []
        for ax in range(lab.ndim):
            for s in (1, -1):
                nl = np.roll(lab, s, ax); nb = np.roll(bad, s, ax)
                votes.append(np.where(nb, -1, nl))
        V = np.stack(votes)[:, bad]                       # (2d, nbad)
        new = lab[bad].copy()
        for k in range(V.shape[1]):
            col = V[:, k]; col = col[col >= 0] if protect is None else col[(col >= 0) & (col != protect)]
            if len(col): vals, cnt = np.unique(col, return_counts=True); new[k] = vals[np.argmax(cnt)]
        lab = lab.copy(); lab[bad] = new
    return lab, moved


def graph3(lab):
    """3D contacts (face-sharing voxel pairs, periodic): {(a, b): area in voxel faces}."""
    contacts = defaultdict(int)
    for ax in range(3):
        B = np.roll(lab, -1, ax); m = lab != B
        a, b = np.minimum(lab[m], B[m]), np.maximum(lab[m], B[m])
        up, cnt = np.unique(np.stack([a, b], 1), axis=0, return_counts=True)
        for (x, y), c in zip(up.tolist(), cnt.tolist()): contacts[(x, y)] += c
    return dict(contacts)


def to_tiling3(Tiling, lab, C, t, parents=None, heirs=None):
    cells = [str(c) for c in np.unique(lab)]
    par = {str(k): {str(a): s for a, s in v.items()} for k, v in (parents or {}).items()}
    hr = {str(k): {str(a): s for a, s in v.items()} for k, v in (heirs or {}).items()}
    return Tiling(cells, [[str(a), str(b)] for a, b in C], None, 3, 'torus3', t, parents=par, heirs=hr)


def periodic_marker_watershed(field, markers, pad=48):
    """Watershed of `field` (low = basin) from integer markers (0 = none), periodic in x and y (2D) or x, y, z (3D):
    pad periodically with the same marker labels, flood, keep the centre."""
    t = np.pad(field, pad, mode='wrap'); mk = np.pad(markers, pad, mode='wrap')
    out = watershed(t, mk, connectivity=1)
    sl = tuple(slice(pad, pad + n) for n in field.shape)
    return out[sl]
