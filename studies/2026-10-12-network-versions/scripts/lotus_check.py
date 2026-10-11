# Check of network_screen.py's "every form has a Lotus seed" (2026-10-12): volumes, and pairwise overlap of all corner copies
# (separating-axis test with face normals and the cross products of real edges).
import itertools, numpy as np
from scipy.spatial import ConvexHull
exec(open('network_screen.py').read().split('def sat_overlap')[0])
def edges(V):
    H = ConvexHull(V); E = set()
    for s in H.simplices:
        for a, b in itertools.combinations(s, 2):
            n1 = [i for i, t in enumerate(H.simplices) if a in t and b in t]
            if len(n1) == 2 and np.linalg.norm(H.equations[n1[0]][:3] - H.equations[n1[1]][:3]) > 1e-6: E.add((min(a, b), max(a, b)))
    return [V[a] - V[b] for a, b in E]
def overlap(A, B):
    axes = list(ConvexHull(A).equations[:, :3]) + list(ConvexHull(B).equations[:, :3])
    for u in edges(A):
        for v in edges(B):
            w = np.cross(u, v)
            if np.linalg.norm(w) > 1e-9: axes.append(w / np.linalg.norm(w))
    for ax in axes:
        a, b = A @ ax, B @ ax
        if a.max() <= b.min() + 1e-7 or b.max() <= a.min() + 1e-7: return False
    return True
for X in FORMS:
    Xv = ref[X]; v = ConvexHull(Xv).volume
    copies = []
    for y in Xv:
        j = np.argmax(Xv @ (y / np.linalg.norm(y))); copies.append(Xv + (y * PHI ** 2 - Xv[j]))
    room = v * PHI ** 6 - v / PHI ** 3
    pairs = sum(overlap(copies[0], c) for c in copies[1:])
    print(f'{X}: {len(Xv)} corner copies need {len(Xv) * v:.3f}, room {room:.3f} -> {"fits" if len(Xv) * v <= room + 1e-9 else "TOO MUCH VOLUME"}; '
          f'copy 0 overlaps {pairs} other copies')
