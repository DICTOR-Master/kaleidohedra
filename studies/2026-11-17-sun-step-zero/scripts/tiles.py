"""Periodic cell tilings from images, neighbour graphs, overlap matching across frames, and frames for the shared event logger.

Segmentation that TILES: the cells are the basins of a marker watershed on the (smoothed) image, bright cells and dark lanes as
boundaries; every pixel belongs to one cell. Markers (the threshold h is what is varied): either the connected regions above
mean + h * std ('thr': one marker per connected granule, so the dark lanes are the boundaries), or the regional maxima of
prominence at least h ('hmax', h-maxima). Periodic in x and y: the image and its markers are padded periodically with the SAME marker labels in every copy, the
watershed is run on the padded image (scikit-image, van der Walt et al. 2014, PeerJ 2:e453; BSD licence), and the centre is
kept, so a cell crossing the box edge keeps one label. (Tiling 3 x 3 gives the same result; a 96-pixel periodic pad is enough.)

Neighbour graph: two cells touch when they share a pixel edge (4-adjacency, periodic). Junctions: 2 x 2 pixel blocks whose four
internal edges separate at least three distinct pairs of cells. Boundary segments per pair = (junction blocks where the pair
ends) / 2; a touching pair that ends at no junction is a closed loop (a cell inside another). Torus Euler: V - E + F = 0.

Matching: new cell j takes old label i when i is j's largest-overlap parent and j is i's largest-overlap heir (mutual best);
otherwise j gets a fresh label. Lineage (area shares) is recorded for newcomers and for vanished cells, in the logger's format."""
import numpy as np
from scipy import ndimage as ndi
from skimage.segmentation import watershed
from skimage.morphology import h_maxima
from collections import defaultdict


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


def segment(img, sigma, h, pad=96, method='hmax', amin=4):
    """img: 2D field, bright = cell interior. Returns periodic label map (1..n). The image is padded periodically by `pad` pixels
    (more than the largest cell radius), markers carry the same label in the pad as in the box, and the centre is kept.
    Markers: method 'hmax' = regional maxima of prominence >= h (field units); method 'thr' = connected regions where the field
    exceeds mean + h * std (granules = connected bright/upflow regions; components under amin pixels dropped)."""
    f = ndi.gaussian_filter(img.astype(np.float64), sigma, mode='wrap') if sigma > 0 else img.astype(np.float64)
    N0, N1 = f.shape
    t = np.pad(f, pad, mode='wrap')
    if method == 'hmax':
        hm = h_maxima(t, h)[pad:pad + N0, pad:pad + N1].astype(bool)
    else:
        hm = f > f.mean() + h * f.std()
    mk = periodic_label(hm)                   # 0 = background, 1..m markers (periodic components)
    if method != 'hmax' and amin > 1:
        sz = np.bincount(mk.ravel()); small = sz < amin; small[0] = False
        mk[small[mk]] = 0
    lab = watershed(-t, np.pad(mk, pad, mode='wrap'), connectivity=1)[pad:pad + N0, pad:pad + N1]
    u, inv = np.unique(lab, return_inverse=True)
    return (inv.reshape(lab.shape) + 1).astype(np.int32)


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


def cell_stats(lab, G):
    """Per-cell side number n (distinct neighbours), area; Aboav m(n), Lewis A(n)."""
    nb = defaultdict(set)
    for a, b in G['contacts']: nb[a].add(b); nb[b].add(a)
    ids, area = np.unique(lab, return_counts=True)
    A = dict(zip(ids.tolist(), area.tolist()))
    n = {c: len(nb[c]) for c in A}
    m = {c: (np.mean([n[x] for x in nb[c]]) if nb[c] else 0.0) for c in A}
    return n, A, m


def periodic_voronoi_counts(pts, L):
    """Side numbers of the periodic Voronoi tiling of points pts (N x 2) in an L x L box (Delaunay of the 3 x 3 copies)."""
    from scipy.spatial import Delaunay
    N = len(pts)
    P = np.concatenate([pts + L * np.array([i, j]) for i in (-1, 0, 1) for j in (-1, 0, 1)])
    tri = Delaunay(P)
    ind, nbr = tri.vertex_neighbor_vertices
    centre = 4 * N
    nb = {}
    for k in range(N):
        v = centre + k
        nb[k] = {int(x) % N for x in nbr[ind[v]:ind[v + 1]]} - {k}
    return nb
