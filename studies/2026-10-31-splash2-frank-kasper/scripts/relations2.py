import sys, json
import sympy as sp
D = json.load(open(sys.argv[1]))
FK = [r for r in D['structures'] if r['ok']]
Zs = (12, 14, 15, 16)
names = [f'x{z}' for z in Zs] + [f'nb{a}_{b}' for a in Zs for b in Zs if a <= b] + [f's{z}' for z in Zs] + ['one']
def row(r):
    C = r['census']; N = C['N']; g = lambda k: sp.Rational(C.get(k, 0), N)
    return [g(f'N{z}') for z in Zs] + [g(f'nb_{a}_{b}') for a in Zs for b in Zs if a <= b] + [g(f'shell6_Z{z}') for z in Zs] + [1]
for label, rows in (('all', FK), ('physical', [r for r in FK if r['kind'] == 'cif'])):
    M = sp.Matrix([row(r) for r in rows]); ns = M.nullspace()
    print('==', label, len(rows), 'cols', len(names), 'rank', M.rank())
    # reduce: express relations in reduced row echelon form of the nullspace basis
    B = sp.Matrix.hstack(*ns).T.rref()[0]
    for k in range(B.rows):
        v = B.row(k); den = sp.ilcm(*[sp.fraction(x)[1] for x in v]); v = v * den
        print('   0 =', ' + '.join(f'({v[i]}){names[i]}' for i in range(len(names)) if v[i] != 0))

# ---- separate identities (true for every TCP structure) from the extra relations ----
idx = {n: i for i, n in enumerate(names)}
def vec(d):
    v = [0] * len(names)
    for k, c in d.items(): v[idx[k]] += c
    return v
Zv = {12: 12, 14: 14, 15: 15, 16: 16}
ids = [vec({'x12': 1, 'x14': 1, 'x15': 1, 'x16': 1, 'one': -1})]
for a in Zs:
    d = {f'nb{a}_{a}': 1, f'x{a}': -Zv[a]}
    for b in Zs:
        if b != a: d[f'nb{min(a, b)}_{max(a, b)}'] = d.get(f'nb{min(a, b)}_{max(a, b)}', 0) + 1
    ids.append(vec(d))
ids.append(vec({'s12': 1, 's14': 1, 's15': 1, 's16': 1, 'x14': -6, 'x15': -9, 'x16': -12}))
YK = vec({'x12': -6, 'x14': 2, 'x15': 7, 'x16': 12})
I = sp.Matrix(ids); print('identities rank', I.rank(), ' + YK rank', sp.Matrix(ids + [YK]).rank())
M = sp.Matrix([row(r) for r in FK]); ns = M.nullspace()
for v in [sp.Matrix(x).T for x in ids + [YK]]:
    assert (M * v.T).is_zero_matrix, 'identity fails!'
N = sp.Matrix.hstack(*ns).T
print('nullspace dim', N.rows, ' extra beyond identities+YK:', sp.Matrix.vstack(N, sp.Matrix(ids + [YK])).rank() - sp.Matrix(ids + [YK]).rank() + (N.rows - sp.Matrix.vstack(N, sp.Matrix(ids + [YK])).rank()))
# extra relations in a readable basis: reduce nullspace modulo the identity span, prefer relations without x and s
A = sp.Matrix.vstack(sp.Matrix(ids + [YK]), N)
R = A.T.columnspace()
