"""Figure 1(a) of the Vacuus and Resonus paper (v2), redrawn from DICTO's Template 2 (diagonal form, 25 Nov 2026): his cardboard
octahedron as four pieces, exact geometry: A (plane x = 0) with one slot from its lower corner to the centre; B (plane z = 0) with a slot
from its upper corner to the centre and two short slots from its side corners, 20 mm of the 40 mm to the centre; C1, C2 (plane y = 0)
the third square cut in two along the line where it meets A, each with one 20 mm slot from its cut edge. Pieces 80 mm across (corners
40 mm from the centre = 1), slots 1.5 mm wide. Style of the current Figure 1 (builds.py of study 2026-11-24-vacuus-build-renders): one
cardboard tan, dark edges, same view. Two scenes: assembled, and pulled apart (A, B along their slot line, C1, C2 out along the line
they slide in on). Pieces asserted against the exhaustive search (scheme (a)).  Usage: python fig1a.py <schemes-N4.json> <out.html>"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import renders as R
R.COL = {0: '#c9a77c', 1: '#c9a77c', 2: '#c9a77c'}; R.EDGE = '#6b4e2e'        # TAN and TAN_EDGE of builds.py
sc = R.SCHEMES['a']; VO = [0.85, 0.62, 1.25]
P = [pc for k in range(3) for pc in R.card_pieces(k, sc['half'], sc['centre'], 'octahedron')]
per = [sum(1 for k, _, _ in P if k == j) for j in range(3)]
S = {(r['cut'], tuple(r['half']), r['centre']): r for r in json.load(open(sys.argv[1]))['results']}
r = S[('octahedron', tuple(sc['half']), sc['centre'])]
names = ['XYZ'[k] if per[k] == 1 else R.piece_name(k, cen) for k, _, cen in P]
whole = [R.part(k, polys, np.zeros(3)) for k, polys, _ in P]
pulled = [R.part(k, polys, R.PULL * np.array(sc['pull'][nm], float)) for (k, polys, _), nm in zip(P, names)]
def fit(parts):
    Q = np.vstack([R.render3d.project(np.array(p['v']), VO, 1.0) for p in parts]) / R.render3d.PX * 2 - 1
    return round(float(np.abs(Q).max()) * 1.06, 3)
E1, E2 = fit(whole), fit(pulled)
lab = {'X': 'A', 'Z': 'B', 'Y-x': 'C1', 'Y+x': 'C2'}
labels = [[lab[nm]] + [round(float(v), 1) for v in R.render3d.project(np.array(p['v']).mean(axis=0), VO, E2)[0]] for p, nm in zip(pulled, names)]
R.render3d.write(sys.argv[2], [{'E': E1, 'dir': VO, 'parts': whole}, {'E': E2, 'dir': VO, 'parts': pulled}])
json.dump(labels, open(os.path.splitext(sys.argv[2])[0] + '.labels.json', 'w'))
ok = per == [1, 2, 1] and r['pieces_per_card'] == per and r['outcome'] == 'POSSIBLE' and sorted(names) == ['X', 'Y+x', 'Y-x', 'Z']
print('pieces per card', per, 'search', r['pieces_per_card'], r['outcome'], 'E', E1, E2, 'labels', labels)
print('FINAL ok' if ok else 'FINAL FAIL')
