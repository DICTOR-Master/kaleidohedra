"""Small painter's-algorithm renderer for convex solids (orthographic), house look of DICTO's papers.
Used by fig_*.py (paper #100, 2026-11-07-dehn-tilers). Run on compute-host with python3."""
import numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
from matplotlib.patches import Polygon
from matplotlib.colors import to_rgb

GOLD, VIOLET, BLUE = '#d9a520', '#7b4fa8', '#3f7fc4'
INK = '#2b2b33'
MARK = 'DICTO · dictospheres.com'


def mark(fig, color='#8a7a55'):
    fig.text(0.992, 0.008, MARK, ha='right', va='bottom', fontsize=7.5, color=color, family='DejaVu Sans', alpha=.9)


def hull_from_halfspaces(A, b, interior=None):
    """Polytope {x : A x <= b}; returns its corners."""
    A = np.asarray(A, float); b = np.asarray(b, float)
    if interior is None: interior = np.zeros(A.shape[1])
    hs = HalfspaceIntersection(np.hstack([A, -b[:, None]]), np.asarray(interior, float))
    P = np.unique(np.round(hs.intersections, 10), axis=0)
    return P[ConvexHull(P).vertices]


def faces(P):
    """Faces of conv(P) as (ordered corner array, outward unit normal)."""
    P = np.asarray(P, float); H = ConvexHull(P); out = {}
    for s, eq in zip(H.simplices, H.equations):
        key = tuple(np.round(eq, 7)); out.setdefault(key, set()).update(s.tolist())
    res = []
    for key, idx in out.items():
        n = np.array(key[:3]); n /= np.linalg.norm(n)
        Q = P[sorted(idx)]; c = Q.mean(0)
        u = Q[0] - c; u /= np.linalg.norm(u); v = np.cross(n, u)
        ang = np.arctan2((Q - c) @ v, (Q - c) @ u)
        res.append((Q[np.argsort(ang)], n))
    return res


def view(az=35, el=22):
    """Rotation: world -> view (x right, y up, z towards the viewer)."""
    a, e = np.radians(az), np.radians(el)
    Rz = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])
    # look along -y' after turning; put world z up
    M = np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]], float)  # world (x,y,z) -> (x, z, -y): y away from viewer
    Rx = np.array([[1, 0, 0], [0, np.cos(e), -np.sin(e)], [0, np.sin(e), np.cos(e)]])
    return Rx @ M @ Rz


LIGHT = np.array([-0.45, 0.65, 0.62]); LIGHT /= np.linalg.norm(LIGHT)


def shade(color, n_view, lo=0.62, hi=1.0):
    c = np.array(to_rgb(color)); k = max(0.0, float(n_view @ LIGHT))
    f = lo + (hi - lo) * k
    spec = max(0.0, float(n_view @ (LIGHT + np.array([0, 0, 1])) / np.linalg.norm(LIGHT + np.array([0, 0, 1])))) ** 24
    return np.clip(c * f + spec * 0.18, 0, 1)


class Solid:
    def __init__(self, P, color=GOLD, alpha=1.0, edge=INK, lw=0.8, glass=False, ealpha=1.0, zbias=0.0):
        self.P = np.asarray(P, float); self.F = faces(self.P); self.color = color; self.alpha = alpha
        self.edge = edge; self.lw = lw; self.glass = glass; self.ealpha = ealpha; self.zbias = zbias


def draw(ax, solids, R, offset=(0, 0)):
    """Draw solids: every face sorted by depth (glass back faces drawn, opaque back faces culled)."""
    items = []
    for s in solids:
        for Q, n in s.F:
            nv = R @ n; Qv = Q @ R.T
            front = nv[2] > 1e-9
            if not s.glass and not front: continue
            depth = Qv[:, 2].mean() + s.zbias + (0.0 if front else -1e-3)
            items.append((depth, Qv, nv, s, front))
    items.sort(key=lambda t: t[0])
    for depth, Qv, nv, s, front in items:
        fc = shade(s.color, nv if front else -nv)
        a = s.alpha if front else s.alpha * 0.7
        ax.add_patch(Polygon(Qv[:, :2] + offset, closed=True, facecolor=(*fc, a), edgecolor='none', zorder=depth))
        ea = s.ealpha * (1.0 if front else 0.45)
        ax.add_patch(Polygon(Qv[:, :2] + offset, closed=True, facecolor='none', edgecolor=(*to_rgb(s.edge), ea),
                             lw=s.lw * (1.0 if front else 0.6), joinstyle='round', zorder=depth + 1e-6,
                             linestyle='-' if front else (0, (2, 2))))


def wire(ax, P, R, color=INK, lw=0.8, alpha=1.0, offset=(0, 0), z=1e9, hidden_dash=True):
    """Edges of conv(P); hidden edges dashed."""
    F = faces(P); edges = {}
    for Q, n in F:
        front = (R @ n)[2] > 1e-9
        for i in range(len(Q)):
            a, b = Q[i], Q[(i + 1) % len(Q)]
            key = tuple(sorted([tuple(np.round(a, 7)), tuple(np.round(b, 7))]))
            edges.setdefault(key, []).append(front)
    for (a, b), fr in edges.items():
        A = np.array([a, b]) @ R.T
        vis = any(fr)
        ax.plot(A[:, 0] + offset[0], A[:, 1] + offset[1], color=color, lw=lw if vis else lw * 0.6,
                alpha=alpha if vis else alpha * 0.5, ls='-' if vis or not hidden_dash else (0, (3, 2.5)),
                zorder=z, solid_capstyle='round')


def face_grid(ax, solid, R, families, levels, color, lw=0.35, alpha=0.6, offset=(0, 0)):
    """Lines where the planes n·x = level (n in families) meet the visible faces of an opaque solid."""
    for Q, n in solid.F:
        nv = R @ n
        if nv[2] <= 1e-9: continue
        depth = (Q @ R.T)[:, 2].mean() + solid.zbias
        for m in families:
            m = np.asarray(m, float)
            if abs(abs(m @ n) / np.linalg.norm(m) - 1) < 1e-6: continue
            h = Q @ m
            for L in levels:
                if L <= h.min() + 1e-9 or L >= h.max() - 1e-9: continue
                pts = []
                for i in range(len(Q)):
                    a, b = h[i] - L, h[(i + 1) % len(Q)] - L
                    if a * b < 0: pts.append(Q[i] + (Q[(i + 1) % len(Q)] - Q[i]) * a / (a - b))
                if len(pts) == 2:
                    A = np.array(pts) @ R.T
                    ax.plot(A[:, 0] + offset[0], A[:, 1] + offset[1], color=color, lw=lw, alpha=alpha,
                            zorder=depth + 5e-7, solid_capstyle='round')


def look(d, up=(0, 0, 1)):
    """Rotation world -> view with the viewer in direction d (from the object), 'up' kept vertical."""
    z = np.asarray(d, float); z /= np.linalg.norm(z)
    x = np.cross(up, z); x /= np.linalg.norm(x); y = np.cross(z, x)
    return np.array([x, y, z])
