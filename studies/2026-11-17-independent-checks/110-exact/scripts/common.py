"""Independent exact toolkit for checking Paper #110 (written from scratch).

Numbers of Q(sqrt5) that occur here lie in Z[phi] (phi = (1+sqrt5)/2) and are
stored as integer pairs (a, b) meaning a + b*phi.  Products, dot products,
determinants and equality tests are exact integer arithmetic.  Signs are
decided exactly (float only for clearly non-small values, exact integer
comparison otherwise).

Coordinates: the paper's sum-zero space of R^5.  A point x of R^5 is stored
as Y = 5x - (sum x)(1,1,1,1,1), which lies in the sum-zero space, is in
Z[phi]^5, and is 5 times the centred point.  Scaling by 5 changes no angle,
no incidence and no hyperplane through the centre.
"""
import itertools, math, sys, time
import numpy as np

PHI = (1 + 5 ** 0.5) / 2
ONE = np.array([1, 0], dtype=np.int64)
ZERO = np.array([0, 0], dtype=np.int64)


# ---------------------------------------------------------------- Z[phi]
def zmul(x, y):
    """(a+b phi)(c+d phi) = ac+bd + (ad+bc+bd) phi ; phi^2 = phi + 1."""
    a, b = x[..., 0], x[..., 1]
    c, d = y[..., 0], y[..., 1]
    return np.stack([a * c + b * d, a * d + b * c + b * d], axis=-1)


def zdot(X, Y):
    """dot product over the coordinate axis (axis -2)."""
    return zmul(X, Y).sum(axis=-2)


def zfloat(x):
    return x[..., 0] + x[..., 1] * PHI


def _sign_int(a, b):
    a, b = int(a), int(b)
    s = 2 * a + b  # 2(a+b phi) = s + b sqrt5
    if b == 0:
        return (s > 0) - (s < 0)
    if s >= 0 and b > 0:
        return 1
    if s <= 0 and b < 0:
        return -1
    if s > 0:  # b < 0
        return 1 if s * s > 5 * b * b else -1
    return 1 if 5 * b * b > s * s else -1  # s < 0, b > 0


def zsign(x):
    """exact sign of a + b phi, elementwise."""
    x = np.asarray(x)
    a, b = x[..., 0], x[..., 1]
    assert np.abs(a).max(initial=0) < 2 ** 50 and np.abs(b).max(initial=0) < 2 ** 50
    v = a + b * PHI
    out = np.sign(v).astype(np.int64)
    small = np.abs(v) < 1e-2
    if small.any():
        for idx in zip(*np.nonzero(small)):
            out[idx] = _sign_int(a[idx], b[idx])
    return out


def zeq(x, y):
    return np.all(x == y, axis=-1)


def zkey(x):
    return (int(x[0]), int(x[1]))


# ------------------------------------------------- canonical directions
def canon_dir(v):
    """Exact projective key of a nonzero vector v in Z[phi]^n (shape (n,2)):
    multiply by the conjugate-type factor that makes the first nonzero
    coordinate rational, divide by the gcd of all integers, make it positive.
    Two vectors get the same key iff they are proportional over Q(sqrt5)."""
    v = [(int(a), int(b)) for a, b in v]
    k = next(i for i, (a, b) in enumerate(v) if a or b)
    a, b = v[k]
    c, d = a + b, -b  # (a+b phi)((a+b) - b phi) = a^2+ab-b^2, rational
    w = [(p * c + q * d, p * d + q * c + q * d) for p, q in v]
    assert w[k][1] == 0 and w[k][0] != 0
    g = 0
    for p, q in w:
        g = math.gcd(g, p, q)
    s = 1 if w[k][0] > 0 else -1
    return tuple((s * p // g, s * q // g) for p, q in w)


def canon_point(v):
    return tuple((int(a), int(b)) for a, b in v)


# ------------------------------------------------- determinants / normals
_PERM4 = []
for p in itertools.permutations(range(4)):
    inv = sum(1 for i in range(4) for j in range(i + 1, 4) if p[i] > p[j])
    _PERM4.append((p, -1 if inv % 2 else 1))


def zdet4(M):
    """M shape (N,4,4,2) -> (N,2) exact determinant."""
    out = np.zeros(M.shape[:-3] + (2,), dtype=np.int64)
    for p, s in _PERM4:
        t = M[..., 0, p[0], :]
        for r in range(1, 4):
            t = zmul(t, M[..., r, p[r], :])
        out += s * t
    return out


def gcross(R):
    """R shape (N,4,5,2): rows r1..r4 in Z[phi]^5. Returns n (N,5,2) with
    n . r_i = 0 for all i (generalised cross product, n_k = (-1)^k det M_k)."""
    cols = list(range(5))
    out = []
    for k in range(5):
        sub = R[..., :, [c for c in cols if c != k], :]
        d = zdet4(sub)
        out.append(d if k % 2 == 0 else -d)
    return np.stack(out, axis=-2)


ONES5 = np.tile(ONE, (5, 1))


def plate_normals(P):
    """P shape (N,3,5,2): three corners of a two-face (non-collinear, plane
    missing the centre).  Normal of the hyperplane through the centre that
    contains them, inside the sum-zero space."""
    N = P.shape[0]
    R = np.concatenate([np.broadcast_to(ONES5, (N, 1, 5, 2)), P], axis=1)
    return gcross(R)


# ------------------------------------------------------------- geometry
def scaled(x):
    """x: list of 5 Z[phi] pairs -> 5x - (sum x) 1."""
    x = np.array(x, dtype=np.int64)
    s = x.sum(axis=0)
    return 5 * x - s[None, :]


def orbit_perms(seed):
    """all distinct permutations of a 5-tuple of Z[phi] pairs."""
    pts = sorted(set(itertools.permutations([tuple(t) for t in seed])))
    return [list(p) for p in pts]


def build_P0():
    """The 600-cell as the five S5-orbits of the paper (scaled, centred).
    Returns coords (120,5,2) and orbit labels."""
    p2 = (1, 1)   # phi^2
    p1 = (0, 1)   # phi
    one, zero = (1, 0), (0, 0)
    orbits = {}
    orbits['A'] = orbit_perms([p2, p2, p2, p1, zero])
    orbits['B'] = orbit_perms([p2, p2, one, one, zero])
    c3 = []
    for i in range(5):
        for j in range(5):
            if i != j:
                v = [zero] * 5
                v[i] = (0, 1)
                v[j] = (0, -1)
                c3.append(v)
    orbits['C3'] = c3
    coords, labels = [], []
    for name in ['A', 'B', 'C3']:
        for x in orbits[name]:
            coords.append(scaled(x))
            labels.append(name)
    for name in ['A', 'B']:
        for x in orbits[name]:
            coords.append(-scaled(x))
            labels.append('-' + name)
    return np.array(coords, dtype=np.int64), np.array(labels)


def gram(X, Y=None):
    if Y is None:
        Y = X
    return zdot(X[:, None, :, :], Y[None, :, :, :])


def value_labels(G):
    """map each Z[phi] entry of G to an integer label (exact)."""
    flat = G.reshape(-1, 2)
    uniq, inv = np.unique(flat, axis=0, return_inverse=True)
    return uniq, inv.reshape(G.shape[:-1])


def cliques(adj, k):
    """all k-cliques (sorted tuples) of a boolean adjacency matrix."""
    n = adj.shape[0]
    out = []
    def rec(cl, cand):
        if len(cl) == k:
            out.append(tuple(cl))
            return
        for v in cand:
            rec(cl + [v], [w for w in cand if w > v and adj[v, w]])
    for v in range(n):
        rec([v], [w for w in range(v + 1, n) if adj[v, w]])
    return out


def reflect_perm(X, r, index):
    """Exact reflection of every point of X (n,5,2) in the hyperplane
    perpendicular to r.  index: dict canon_point -> idx.  Returns the
    permutation (array) or None if some image is not in the set."""
    rr = zdot(r, r)
    c, d = int(rr[0]), int(rr[1])
    conj = np.array([c + d, -d], dtype=np.int64)
    norm = c * c + c * d - d * d
    xr = zdot(X, r[None])                      # (n,2)
    num = 2 * zmul(xr, conj[None])             # 2(x.r)*conj(r.r)
    if np.any(num % norm):
        return None
    coef = num // norm                         # = 2(x.r)/(r.r) in Z[phi]
    Y = X - zmul(coef[:, None, :], r[None])
    perm = []
    for y in Y:
        j = index.get(canon_point(y))
        if j is None:
            return None
        perm.append(j)
    return np.array(perm)


def close_group(gens):
    """all products of permutation generators (BFS). returns array."""
    n = len(gens[0])
    idp = tuple(range(n))
    seen = {idp}
    frontier = [np.arange(n)]
    elems = [np.arange(n)]
    while frontier:
        nf = []
        for g in frontier:
            for s in gens:
                h = s[g]
                t = tuple(h)
                if t not in seen:
                    seen.add(t)
                    nf.append(h)
                    elems.append(h)
        frontier = nf
    return np.array(elems)


# ---------------------------------------------------------- facets etc.
def facets_exact(X, chunk=20000):
    """Exact facet enumeration of conv(X) for a full-dimensional point set
    X (n,5,2) in the sum-zero space: every 4-subset spanning an affine
    hyperplane is tested as a supporting hyperplane in exact arithmetic.
    Returns sorted list of facets (tuples of point indices)."""
    n = len(X)
    combs = np.array(list(itertools.combinations(range(n), 4)))
    found = set()
    for s in range(0, len(combs), chunk):
        C = combs[s:s + chunk]
        P = X[C]                                   # (m,4,5,2)
        D = P[:, 1:] - P[:, :1]
        R = np.concatenate([np.broadcast_to(ONES5, (len(C), 1, 5, 2)), D], axis=1)
        nrm = gcross(R)                            # (m,5,2)
        nz = np.any(nrm != 0, axis=(1, 2))
        C, P, nrm = C[nz], P[nz], nrm[nz]
        h = zdot(nrm, P[:, 0])                     # (m,2)
        vals = zdot(nrm[:, None], X[None]) - h[:, None]   # (m,n,2)
        sg = zsign(vals)
        pos = (sg > 0).any(1)
        neg = (sg < 0).any(1)
        ok = ~(pos & neg)
        for row in np.nonzero(ok)[0]:
            found.add(tuple(np.nonzero(sg[row] == 0)[0]))
    return sorted(found)


def face_lattice(X):
    """facets, ridges (2-faces), edges, with exact checks of closure."""
    F = facets_exact(X)
    Fs = [set(f) for f in F]
    ridges = set()
    for i in range(len(F)):
        for j in range(i + 1, len(F)):
            I = Fs[i] & Fs[j]
            if len(I) >= 3:
                ridges.add(tuple(sorted(I)))
    ridges = sorted(ridges)
    # each ridge in exactly two facets (closed boundary certificate)
    for r in ridges:
        assert sum(1 for f in Fs if set(r) <= f) == 2
    n = len(X)
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            fc = [f for f in Fs if i in f and j in f]
            if fc and set.intersection(*fc) == {i, j}:
                edges.append((i, j))
    f = (n, len(edges), len(ridges), len(F))
    assert f[0] - f[1] + f[2] - f[3] == 0, f   # Euler, 4D
    return F, ridges, edges


class Log:
    def __init__(self, path):
        self.f = open(path, 'w')
        self.t0 = time.time()
        self.fails = []

    def __call__(self, *a):
        s = ' '.join(str(x) for x in a)
        print(s, flush=True)
        self.f.write(s + '\n')
        self.f.flush()

    def check(self, name, got, want):
        ok = got == want
        self(f"[{'MATCH' if ok else 'MISMATCH'}] {name}: got {got}, paper {want}")
        if not ok:
            self.fails.append(name)
        return ok

    def final(self):
        self(f"runtime {time.time() - self.t0:.1f} s")
        if self.fails:
            self('FINAL FAIL ' + '; '.join(self.fails))
        else:
            self('FINAL ok')
        self.f.close()


def load_base():
    d = np.load('cache/base.npz')
    return {k: d[k] for k in d.files}


def wall_sets(P, Q):
    mir = {canon_dir(p) for p in P}
    crs = {canon_dir(q) for q in Q}
    return mir, crs


def plate_keys(X, ridges):
    """exact plate key of each ridge (first three corners suffice)."""
    T = np.array([r[:3] for r in ridges])
    nr = plate_normals(X[T])
    return [canon_dir(v) for v in nr]
