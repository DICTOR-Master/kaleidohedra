# DICTO 2026-10-18 octet study -- STEP 27b: is the expanded tetrahedron piece (step 27) chiral? Its partner at the T- sites is its point
# reflection; they are the same piece exactly when some rotation takes the piece onto its reflection (search the cube's 24 turns, then
# any rotation via vertex triples). -> adds to data/step27-expanded.json
import json, itertools, numpy as np, os
H = os.path.dirname(os.path.abspath(__file__)); p = os.path.join(H, '..', 'data', 'step27-expanded.json'); d = json.load(open(p))
A = np.unique(np.round(np.array(d['mesh']['v']), 6), axis=0); B = -A
def match(X, Y, tol=1e-5): return all(np.min(np.linalg.norm(Y - x, axis=1)) < tol for x in X)
turns = [np.array(Pm) * np.array(s)[:, None] for Pm in itertools.permutations(np.eye(3)) for s in itertools.product((1, -1), repeat=3)]
turns = [M for M in turns if np.linalg.det(M) > 0]
cube_turn = any(match(A @ M.T, B) for M in turns)
d['chirality'] = dict(corners=len(A), same_as_mirror_by_a_cube_turn=cube_turn, verdict='same piece' if cube_turn else 'left and right (no cube turn maps it to its mirror image)')
json.dump(d, open(p, 'w')); print(d['chirality'])
