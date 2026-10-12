# Which faces of the kit pieces are perpendicular to a five-fold axis (and so can lie on the ring's floor or top), and which to a
# three-fold axis (the ring's sloping sides)? Shapes listed with side lengths and angles.
import sys, os, itertools, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ring_core as rc
from kit_exact import KIT
PHI = rc.PHI
Ic = KIT['I'] - KIT['I'].mean(0); A5 = Ic / np.linalg.norm(Ic, axis=1)[:, None]
A3 = np.array([-f[:3] for f in rc.planes(Ic)])
def kind(n):
    if np.any(np.abs(np.abs(A5 @ n) - 1) < 1e-9): return '5'
    if np.any(np.abs(np.abs(A3 @ n) - 1) < 1e-9): return '3'
    return '?'
far = np.argmax(np.linalg.norm(KIT['I'] - KIT['I'][0], axis=1)); KIT['AP'] = np.delete(KIT['I'], [0, far], axis=0)
for k in ('AXE', 'CLEO', 'FUJI', 'J2', 't1', 't2', 't3', 't4', 't5', 't6', 'T2', 'I', 'J11', 'AP'):
    V = KIT[k]; out = []
    for e in rc.planes(V):
        idx = np.where(np.abs(V @ e[:3] + e[3]) < 1e-9)[0]; c = V[idx].mean(0); n = e[:3]
        a = V[idx[0]] - c; a /= np.linalg.norm(a); b = np.cross(n, a)
        idx = idx[np.argsort([np.arctan2((V[i] - c) @ b, (V[i] - c) @ a) for i in idx])]
        L = [np.linalg.norm(V[idx[i]] - V[idx[(i + 1) % len(idx)]]) for i in range(len(idx))]
        ang = []
        for i in range(len(idx)):
            p, q, r_ = V[idx[i - 1]], V[idx[i]], V[idx[(i + 1) % len(idx)]]
            ang.append(np.degrees(np.arccos(np.clip(((p - q) @ (r_ - q)) / np.linalg.norm(p - q) / np.linalg.norm(r_ - q), -1, 1))))
        out.append((kind(n), len(idx), tuple(np.round(L, 4)), tuple(np.round(ang, 1))))
    print(f'{k}:')
    for kd, nv, L, ang in sorted(out): print(f'   normal {kd}-fold: {nv}-gon sides {L} angles {ang}')
