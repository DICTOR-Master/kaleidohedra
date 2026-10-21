# DICTO 2026-10-21, Fable referee's study question for #43: what does each symmetry axis pierce on each solid of the OG's downward
# family (= the turned-out sequence, scaled), and does the word repeat? EXACT: the axis leaves a convex solid with this symmetry
# through a corner (a corner on the axis), a face (a face plane square to the axis: its exit point is fixed by the axis turn, so the
# face is turned onto itself) or the inside of an edge (only possible on a 2-fold axis). Tests: cross(v, a) = 0 for corners,
# cross(n, a) = 0 for face normals, in Q(sqrt5). Prediction (referee): 2-fold word OG..TQHD = corner, edge, edge, face, corner, so
# period 4 -> ribbons (edge stations) again at down 5, 6.   usage: python3 axis_words.py <studies/2026-10-19-five-fold-octet>
import sys, os, json, pickle
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
HERE = os.path.dirname(os.path.abspath(__file__))
src = open('exact_downward.py').read(); exec(src.split("log = {")[0].replace("os.path.dirname(os.path.abspath(__file__))", repr(os.getcwd())))
from exact_shells import cross
D = pickle.load(open(os.path.join(HERE, 'golden-long-solids.pkl'), 'rb'))
z = Q5(0); one = Q5(1)
AX = {'5-fold': (z, one, PHI), '3-fold': (one, one, one), '2-fold': (z, z, one)}
zero = lambda u: all(x == z for x in u)
names = ['OG', 'TPH', 'TQH', 'TQP', 'TQHD'] + [f'down {k}' for k in range(5, 13)]
out = {}
for k, S in enumerate(D):
    H = solid(S); row = {}
    for nm, a in AX.items():
        c = any(zero(cross(v, a)) and dot(v, a).sign() > 0 for v in S)
        f = any(zero(cross(n, a)) and dot(n, a).sign() > 0 for n, d in H)
        row[nm] = 'corner' if c else 'face' if f else 'edge'
    out[names[k]] = row; print(f'{names[k]:8s} {len(S):4d} corners  ' + '  '.join(f'{a}: {row[a]:6s}' for a in AX), flush=True)
w2 = [out[n]['2-fold'] for n in out]
print('2-fold word:', ' '.join(w2)); print('period 4 holds over all built:', all(w2[i] == w2[i + 4] for i in range(len(w2) - 4)))
for a in ('3-fold', '5-fold'):
    w = [out[n][a] for n in out]; print(f'{a} word:', ' '.join(w), '| period 2:', all(w[i] == w[i + 2] for i in range(len(w) - 2)))
json.dump(out, open(os.path.join(HERE, 'axis-words.json'), 'w'), indent=1)
