# Step 5 (DICTO: "would rotating out of their existing connections change the shape of the shadow entities?"). Exploratory, float.
# A twinned copy: the OCD turned 90 deg about a cube axis (the other golden frame). The turn maps the 8 cube-diagonal joint
# directions onto themselves, so every joint hexagon is still there; but kites and free hexagons turn, so the gaps change.
# Arrangements: (a) one diamond network, B sites twinned; (b) double network, the second network twinned; (c) bcc alternating
# by sublattice parity (A, A' plain; B, B' twinned). Checks: joints stay full hexagon contacts? any collisions? (LP overlap test)
import json, itertools, numpy as np
from scipy.spatial import ConvexHull
from scipy.optimize import linprog
N = json.load(open('data/network.json')); R = json.load(open('data/network-render.json'))
O = np.array(N['ocd']); T = np.array(N['T']); cube = np.array(R['cube'])
def rot(axis, ang):
    a = axis / np.linalg.norm(axis); K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]]); return np.eye(3) + np.sin(ang) * K + (1 - np.cos(ang)) * K @ K
Rt = rot(cube[0], np.pi / 2); Ot = O @ Rt.T
same = lambda X, Y: len(X) == len(Y) and all(np.min(np.linalg.norm(Y - x, axis=1)) < 1e-9 for x in X)
assert not same(O, Ot), 'the 90-degree turn should not be a symmetry'
EQ = {0: ConvexHull(O).equations, 1: ConvexHull(Ot).equations}
def overlap(p, kp, q, kq):
    H = np.vstack([EQ[kp] - np.c_[np.zeros((len(EQ[kp]), 3)), EQ[kp][:, :3] @ p], EQ[kq] - np.c_[np.zeros((len(EQ[kq]), 3)), EQ[kq][:, :3] @ q]])
    nrm = np.linalg.norm(H[:, :3], axis=1)
    r = linprog([0, 0, 0, -1], A_ub=np.c_[H[:, :3], nrm], b_ub=-H[:, 3], bounds=[(None, None)] * 3 + [(0, None)])
    return r.status == 0 and r.x[3] > 1e-7
def hexagon(Vs, n):   # the face of solid Vs whose outward normal is n
    e = ConvexHull(Vs).equations; i = np.argmax(e[:, :3] @ (n / np.linalg.norm(n))); return Vs[np.abs(Vs @ e[i, :3] + e[i, 3]) < 1e-7]
def joint(kp, kq, t):    # hexagon of copy kp at +t direction vs hexagon of copy kq (at t) at -t direction
    A = hexagon(O if kp == 0 else Ot, t); B = hexagon(O if kq == 0 else Ot, -t) + t
    return same(A, B), len(A)
sites = []
for m in itertools.product(range(-2, 3), repeat=4):
    p = sum(k * t for k, t in zip(m, T)); s = sum(m) % 4
    if np.linalg.norm(p) < 2.4 and not any(np.allclose(p, x[0]) for x in sites): sites.append((p, s))
arr = {'(a) one network, B twinned': lambda s: (s in (0, 1)), 'b': None}
cases = {'(a) one network, B sites twinned': ({0: 0, 1: 1}, (0, 1)),
         '(b) double network, second network twinned': ({0: 0, 1: 0, 2: 1, 3: 1}, (0, 1, 2, 3)),
         '(c) bcc alternating: A, A\' plain, B, B\' twinned': ({0: 0, 1: 1, 2: 0, 3: 1}, (0, 1, 2, 3))}
out = []
for name, (orient, used) in cases.items():
    S = [(p, orient[s]) for p, s in sites if s in used]
    coll = 0; full = 0; partial = 0
    for (p, kp), (q, kq) in itertools.combinations(S, 2):
        d = q - p
        if any(np.allclose(d, s * t) for t in T for s in (1, -1)):        # a joint
            ok, nv = joint(kp, kq, d); full += ok; partial += (not ok)
        elif overlap(p, kp, q, kq): coll += 1
    out.append(f'{name}: {len(S)} copies; joints with full hexagon contact {full}, joints mismatched {partial}; collisions elsewhere {coll}')
    print(out[-1], flush=True)
open('data/twin.txt', 'w').write('\n'.join(out) + '\n')
