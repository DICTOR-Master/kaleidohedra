# Shared accuracy checks for the geometry studies (DICTO's request, 2026-10-16, after the polar Dharma slips). Each check raises on
# failure, so a study script stops instead of printing a wrong table. Use:
#     sys.path.insert(0, '/home/dicto/kaleidohedra/studies/_lib'); import geomcheck as gc
# Rules (see the study README "Accuracy rules"):
#   1 frame      every generated solid must share the chain's symmetry axes            gc.frame(V, axes) / gc.orient(V, axes)
#   2 orders     test both nestings of a pair; polar reversal swaps a dual pair's order gc.both_orders(f, X, Y)
#   3 known      check each formula on a case with a known answer before using it       gc.known(label, got, want)
#   4 kinds      count piece kinds by symmetry orbit and volume, not float face counts  gc.kinds(pieces, group)
#   5 exact      a claim stands only once the exact remainder is 0                       gc.exact_zero(label, remainder)
#   6 labels     every reported number says exact or float, faithful or adjusted        gc.tag(text, exact=..., variant=...)
import itertools
import numpy as np

PHI = (1 + 5 ** .5) / 2

def rotation(axis, angle):
    a = np.asarray(axis, float); a = a / np.linalg.norm(a); K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + np.sin(angle) * K + (1 - np.cos(angle)) * K @ K

def icosa_axes(ico):
    """The chain's axes from its icosahedron corners: 5-fold (6 lines), 3-fold (face centres, 10 lines), 2-fold (edge midpoints)."""
    I = np.asarray(ico, float); I = I / np.linalg.norm(I, axis=1)[:, None]
    d = np.linalg.norm(I[:, None] - I[None], axis=2); e = np.min(d[d > 1e-9])
    edges = [(i, j) for i, j in itertools.combinations(range(12), 2) if abs(d[i, j] - e) < 1e-9]
    tri = [t for t in itertools.combinations(range(12), 3) if all(abs(d[a, b] - e) < 1e-9 for a, b in itertools.combinations(t, 2))]
    unit = lambda v: v / np.linalg.norm(v)
    return {'5': I, '3': np.array([unit(I[list(t)].sum(0)) for t in tri]), '2': np.array([unit(I[i] + I[j]) for i, j in edges])}

def group(axes):
    """The 60 rotations of the icosahedral group generated from the chain's own axes."""
    gens = [rotation(axes['5'][0], 2 * np.pi / 5), rotation(axes['3'][0], 2 * np.pi / 3)]
    G = [np.eye(3)]; frontier = [np.eye(3)]
    while frontier:
        new = []
        for g in frontier:
            for h in gens:
                m = h @ g
                if not any(np.allclose(m, x, atol=1e-9) for x in G): G.append(m); new.append(m)
        frontier = new
    assert len(G) == 60, f'icosahedral rotation group has {len(G)} elements, expected 60'
    return G

def _invariant(V, R, tol):
    V = np.asarray(V, float); W = V @ R.T; s = np.linalg.norm(V, axis=1).max()
    return all(np.min(np.linalg.norm(V - w, axis=1)) < tol * s for w in W)

def frame(V, axes, name='solid', tol=1e-9):
    """Rule 1: V must be invariant under a 5-fold turn and a 3-fold turn about the chain's axes (same golden frame)."""
    for k, n in (('5', 5), ('3', 3)):
        if not _invariant(V, rotation(axes[k][0], 2 * np.pi / n), tol):
            raise AssertionError(f'{name}: not in the chain frame ({k}-fold turn fails); textbook coordinates may be in the mirror golden frame')
    return V

def orient(V, axes, name='solid'):
    """Rule 1: return V with coordinates permuted into the chain frame (tries the two golden frames), checked."""
    V = np.asarray(V, float)
    for p in ([0, 1, 2], [1, 0, 2]):
        try: return frame(V[:, p], axes, name)
        except AssertionError: pass
    raise AssertionError(f'{name}: no coordinate order puts it in the chain frame')

def both_orders(f, X, Y, names=('X', 'Y')):
    """Rule 2: run f(inner, outer) both ways; returns {('X','Y'): ..., ('Y','X'): ...}."""
    return {(names[0], names[1]): f(X, Y), (names[1], names[0]): f(Y, X)}

def known(label, got, want, tol=1e-6):
    """Rule 3: a formula must reproduce a known case before its results are used."""
    if abs(got - want) > tol * max(1, abs(want)):
        raise AssertionError(f'known case failed: {label}: got {got!r}, want {want!r}')
    return got

def corners(V, tol=1e-7):
    """The true corners of a convex piece: float hulls carry near-duplicate points and points lying on edges; keep a point only
    where at least three independent face planes meet."""
    from scipy.spatial import ConvexHull
    V = np.asarray(V, float); h = ConvexHull(V); pl = []
    for e in h.equations:
        if not any(np.allclose(e, q, atol=tol) for q in pl): pl.append(e)
    pl = np.array(pl); keep = []
    for i in h.vertices:
        on = pl[np.abs(pl[:, :3] @ V[i] + pl[:, 3]) < tol * 10]
        if len(on) >= 3 and np.linalg.matrix_rank(on[:, :3], tol=1e-6) == 3 and not any(np.linalg.norm(V[i] - V[j]) < tol * 100 for j in keep): keep.append(i)
    return V[keep]

def kinds(pieces, G, vol_tol=1e-9):
    """Rule 4: count piece kinds as orbits under the group G (rotations; mirror images join by volume). Pieces are corner arrays.
    Two pieces are the same kind when a rotation maps one's corner set onto the other's, or (mirror) they have equal volume and
    mirrored corner sets. Returns a list of (count, representative index)."""
    from scipy.spatial import ConvexHull
    P = [corners(p) for p in pieces]; vol = [ConvexHull(p).volume for p in P]
    def same(a, b):
        if abs(vol[a] - vol[b]) > vol_tol * max(1, vol[a]) or len(P[a]) != len(P[b]): return False
        for R in G:
            for M in (R, -R):                             # -R covers mirror images (the full group Ih = I x {±1})
                W = P[a] @ M.T
                if all(np.min(np.linalg.norm(P[b] - w, axis=1)) < 1e-6 for w in W): return True
        return False
    out = []
    for i in range(len(P)):
        for k in out:
            if same(k[1], i): k[0] += 1; break
        else: out.append([1, i])
    return [tuple(k) for k in out]

def exact_zero(label, remainder):
    """Rule 5: an exact remainder (a Q(sqrt5) value with .a, .b, or a Fraction/int) must be exactly 0."""
    z = (remainder.a == 0 and remainder.b == 0) if hasattr(remainder, 'a') else remainder == 0
    if not z: raise AssertionError(f'exact check failed: {label}: remainder {remainder!r}')
    return True

def tag(text, exact, variant='faithful'):
    """Rule 6: label every reported line."""
    return f'[{"exact" if exact else "float"}, {variant}] {text}'
