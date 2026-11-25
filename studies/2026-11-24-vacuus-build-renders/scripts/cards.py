"""DICTO's three-planes card models, both forms (25 Nov 2026), in the same look as the cardboard octahedron of builds.py:
solid tan cards, crisp edges, the crease where two cards meet. Exact geometry from DICTO's templates (three_planes_models.pdf):
  octahedral (diagonal) form: the square in the plane x_k = 0 with its corners on the two axes of that plane (corners = octahedron corners);
  cubic (axial) form: the square in the plane x_k = 0 with its sides parallel to the axes (corners (+-1, +-1) = midpoints of cube edges,
  the cube's middle square, i.e. its Resonus plane slice).
Both: any two cards meet along a whole axis segment. Pull-apart: each card moved along its own normal (as builds.py).
Usage: python cards.py <out.html>   (frames by shots.mjs; p0 octahedral whole, p1 pulled, p2 cubic whole, p3 pulled)."""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../2026-11-21-scutoid-stand-in/renders/scripts"))
import render3d

TAN, TAN_EDGE, TAN_CREASE = '#c9a77c', '#6b4e2e', '#7d5f3c'
E3 = np.eye(3)

def card(k, form):
    i, j = [m for m in range(3) if m != k]
    if form == 'octa':
        return [E3[i], E3[j], -E3[i], -E3[j]]
    return [E3[i] + E3[j], -E3[i] + E3[j], -E3[i] - E3[j], E3[i] - E3[j]]

for form, side, nOct in (('octa', 2 ** 0.5, True), ('cube', 2.0, False)):
    for k in range(3):
        Q = card(k, form)
        assert all(abs(p[k]) < 1e-12 for p in Q)
        assert all(abs(np.linalg.norm(Q[m] - Q[(m + 1) % 4]) - side) < 1e-12 for m in range(4))
        if form == 'cube':     # sides parallel to the axes: the cube's middle square (Resonus slice of the cube [-1,1]^3)
            assert all(sum(abs(Q[m] - Q[(m + 1) % 4]) > 1e-12) == 1 for m in range(4))
        else:                  # corners on the axes: the octahedron's corners
            assert all(sum(abs(p) > 1e-12) == 1 for p in Q)

def cards_part(ks, form, shift=lambda k: np.zeros(3)):
    V, T, C, U = [], [], [], []
    def vid(p):
        p = list(np.round(np.array(p, float), 6))
        if p not in V: V.append(p)
        return V.index(p)
    for k in ks:
        ids = [vid(p + shift(k)) for p in card(k, form)]
        T += [[ids[0], ids[1], ids[2]], [ids[0], ids[2], ids[3]]]; C += [TAN, TAN]
        U += [[ids[m], ids[(m + 1) % 4], TAN_EDGE, None] for m in range(4)]
    if len(ks) == 3 and not shift(0).any():          # creases: the whole axis segment common to two cards
        for k in range(3): U.append([vid(E3[k]), vid(-E3[k]), TAN_CREASE, None])
    return {'v': V, 't': T, 'c': C, 'a': 1, 'tubes': U, 'rad': 0.0042, 'balls': []}

def pulled(form, pull):
    sh = lambda k: E3[k] * pull * (1 if k != 1 else -1)
    m = sum(sh(k) for k in range(3)) / 3
    return [cards_part([k], form, lambda k: sh(k) - m) for k in range(3)]

VO = [0.85, 0.62, 1.25]
scenes = [
    {'E': 1.30, 'dir': VO, 'parts': [cards_part([0, 1, 2], 'octa')]},
    {'E': 2.30, 'dir': VO, 'parts': pulled('octa', 1.8)},
    {'E': 1.75, 'dir': VO, 'parts': [cards_part([0, 1, 2], 'cube')]},
    {'E': 3.00, 'dir': VO, 'parts': pulled('cube', 2.4)},
]
render3d.write(sys.argv[1], scenes)
print('FINAL ok cards: octahedral and cubic forms, 3 cards each, exact')
