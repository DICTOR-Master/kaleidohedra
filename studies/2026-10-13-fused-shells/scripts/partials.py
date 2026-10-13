# Partial rings (DICTO 2026-10-13: "include the partial rings too"; PLAN-FUSED-SHELLS.md steps 2-3). For every whole-ring stage S
# (stages.json) and every ring R not in S that touches it:
#   symmetric partials: one orbit of R under a large subgroup of the structure's rotations (T, D5, D3, D2), touching S;
#   hemispheres: the pieces of R on one side of a plane through the centre, across a 5-, 3- or 2-fold axis;
#   caps: the pieces of R within 45 degrees of a 5-, 3- or 2-fold axis.
# Each stage is the set of its pieces; stages that are rotations of one another are kept once. Output: partials.json (piece index
# sets per view, with how each was made). Facts come after (stage_facts.py --partials).
import os, sys, json, itertools
import numpy as np
from scipy.spatial import ConvexHull
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fuse import DATA
from stages import faces_of, touch

HERE = os.path.dirname(os.path.abspath(__file__))
u = lambda v: np.asarray(v, float) / np.linalg.norm(v)


def rotations(P):
    """All rotations mapping the point set P (centred) to itself."""
    P = np.asarray(P, float)
    r = np.linalg.norm(P, axis=1)
    a = P[0]
    b = next(p for p in P[1:] if np.linalg.norm(np.cross(a, p)) > 1e-3 and abs(np.linalg.norm(p) - np.linalg.norm(a)) < 1e-4)
    ang = np.dot(u(a), u(b))
    out = []
    for a2 in P:
        if abs(np.linalg.norm(a2) - np.linalg.norm(a)) > 1e-4: continue
        for b2 in P:
            if abs(np.linalg.norm(b2) - np.linalg.norm(b)) > 1e-4 or abs(np.dot(u(a2), u(b2)) - ang) > 1e-4: continue
            M1 = np.column_stack([u(a), u(np.cross(a, b)), u(np.cross(a, np.cross(a, b)))])
            M2 = np.column_stack([u(a2), u(np.cross(a2, b2)), u(np.cross(a2, np.cross(a2, b2)))])
            R = M2 @ M1.T
            if np.linalg.det(R) < 0: continue
            img = P @ R.T
            if all(np.min(np.linalg.norm(P - q, axis=1)) < 1e-4 for q in img) and not any(np.allclose(R, S, atol=1e-4) for S in out): out.append(R)
    return out


def axes_of(G):
    """The rotation axes of G by order (5, 3, 2): unit vectors, one per axis line."""
    out = {5: [], 3: [], 2: []}
    for R in G:
        tr = np.trace(R)
        if abs(tr - 3) < 1e-6: continue
        w, v = np.linalg.eig(R)
        ax = u(np.real(v[:, np.argmin(np.abs(w - 1))]))
        ang = np.arccos(np.clip((tr - 1) / 2, -1, 1))
        k = 5 if min(abs(ang - 2 * np.pi / 5), abs(ang - 4 * np.pi / 5)) < 1e-3 else 3 if abs(ang - 2 * np.pi / 3) < 1e-3 else 2 if abs(ang - np.pi) < 1e-3 else None
        if k and not any(abs(abs(np.dot(ax, x)) - 1) < 1e-4 for x in out[k]): out[k].append(ax)
    return out


def subgroups(G, axes):
    """One representative each of T, D5, D3, D2 (as lists of rotations)."""
    line_fixed = lambda R, a: abs(abs(np.dot(R @ a, a)) - 1) < 1e-4
    D = {f'D{k}': [R for R in G if line_fixed(R, axes[k][0])] for k in (5, 3)}
    a2 = axes[2][0]
    perp = [b for b in axes[2] if abs(np.dot(a2, b)) < 1e-4]
    trio = [a2, perp[0], u(np.cross(a2, perp[0]))]
    D['D2'] = [R for R in G if all(line_fixed(R, t) for t in trio)]
    D['T'] = [R for R in G if all(any(abs(abs(np.dot(R @ t, s)) - 1) < 1e-4 for s in trio) for t in trio)]
    return D


def run(view, stages):
    pieces = DATA[view]
    allP = np.array([p for _, V, _ in pieces for p in V], float); c0 = allP.mean(0)
    P = [np.array(V, float) - c0 for _, V, _ in pieces]
    roles = [r for r, _, _ in pieces]
    cen = np.array([p.mean(0) for p in P])
    ring = [f'{r}@{np.linalg.norm(c):.2f}' for r, c in zip(roles, cen)]
    centre_piece = int(np.argmin(np.linalg.norm(cen, axis=1)))
    G = rotations(P[centre_piece])
    # keep only rotations of the whole structure (piece centres to piece centres of the same role)
    perm = []
    for R in G:
        img = cen @ R.T
        m = [int(np.argmin(np.linalg.norm(cen - q, axis=1))) for q in img]
        if all(np.linalg.norm(cen[j] - img[i]) < 1e-3 and roles[j] == roles[i] for i, j in enumerate(m)): perm.append((R, m))
    G = [R for R, _ in perm]
    axes = axes_of(G)
    H = subgroups(G, axes)
    print(view, 'rotations', len(G), {k: len(v) for k, v in H.items()}, 'axes', {k: len(v) for k, v in axes.items()}, flush=True)
    rings = sorted(set(ring), key=lambda g: np.linalg.norm(cen[ring.index(g)]))
    members = {g: [i for i in range(len(P)) if ring[i] == g] for g in rings}
    # piece-to-piece contacts between rings (box test, then shared face area)
    F = [faces_of(P[i], pieces[i][2]) for i in range(len(P))]
    lo = [p.min(0) for p in P]; hi = [p.max(0) for p in P]
    nbr = {i: set() for i in range(len(P))}
    for i, j in itertools.combinations(range(len(P)), 2):
        if np.any(hi[i] < lo[j] - 1e-6) or np.any(hi[j] < lo[i] - 1e-6): continue
        if touch(F[i], F[j]): nbr[i].add(j); nbr[j].add(i)
    print(view, 'contacts', sum(len(v) for v in nbr.values()) // 2, flush=True)

    def canon(S):
        return min(tuple(sorted(m[i] for i in S)) for _, m in perm)

    def orbits(idx, Hg):
        hm = [m for R, m in perm if any(np.allclose(R, S, atol=1e-4) for S in Hg)]
        left, out = set(idx), []
        while left:
            i = min(left); o = {m[i] for m in hm}; out.append(sorted(o)); left -= o
        return out

    seen, out = set(), []
    def add(S, how):
        k = canon(S)
        if k in seen: return
        seen.add(k); out.append({'pieces': sorted(S), 'how': how})
    for st in stages:
        base = {i for g in st for i in members[g]}
        for g in rings:
            if g in st: continue
            Rm = members[g]
            if not any(nbr[i] & base for i in Rm): continue
            for name, Hg in H.items():
                for o in orbits(Rm, Hg):
                    if len(o) < len(Rm) and any(nbr[i] & base for i in o): add(base | set(o), f"{'+'.join(x.split('@')[0] for x in st)} + {name} part of {g.split('@')[0]}")
            for k, ax in axes.items():
                a = ax[0]
                half = [i for i in Rm if np.dot(cen[i], a) > 1e-6]
                cap = [i for i in Rm if np.dot(u(cen[i]), a) > np.cos(np.radians(45))]
                for nm, part in (('half', half), ('cap', cap)):
                    if part and len(part) < len(Rm) and any(nbr[i] & base for i in part):
                        add(base | set(part), f"{'+'.join(x.split('@')[0] for x in st)} + {nm} of {g.split('@')[0]} ({k}-fold axis)")
    print(view, 'partial stages', len(out), flush=True)
    return out


if __name__ == '__main__':
    st = {R['view']: R['all'] for R in json.load(open(os.path.join(HERE, '..', 'stages.json')))}
    res = {v: run(v, st[v]) for v in DATA}
    json.dump(res, open(os.path.join(HERE, '..', 'partials.json'), 'w'))
