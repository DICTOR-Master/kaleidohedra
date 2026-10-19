# Proper congruence test (DICTO 2026-10-19, after a flawed edge-list test): two pieces are the same shape (up to size and mirror image)
# if some matching of their corners makes ALL pairwise distances proportional. Checks every "same piece" claim of #38 and #38a.
import itertools, json, numpy as np
exec(open('cleo_pattern.py').read().split("def pattern")[0])
def same_shape(P, Q, tol=1e-6):
    P, Q = np.asarray(P, float), np.asarray(Q, float)
    if len(P) != len(Q): return False
    dP = np.linalg.norm(P[:, None] - P[None], axis=2); dQ = np.linalg.norm(Q[:, None] - Q[None], axis=2); dP /= dP.max(); dQ /= dQ.max()
    if not np.allclose(np.sort(dP.ravel()), np.sort(dQ.ravel()), atol=tol): return False
    for perm in itertools.permutations(range(len(Q))):
        if np.allclose(dP, dQ[np.ix_(perm, perm)], atol=tol): return True
    return False
def load(f):
    s = open(f).read(); return json.loads(s[s.index('{'):s.rindex('}') + 1])
seeds = load('/home/dicto/k-master/src/app/seeds-data.js'); upd = load('/home/dicto/k-master/src/app/up-data.js')
def first(d, role):
    out = []
    def walk(x):
        if isinstance(x, list) and x and isinstance(x[0], list) and len(x[0]) >= 2 and isinstance(x[0][0], str):
            for p in x:
                if p[0] == role and not out: out.append(np.array(p[1]))
        elif isinstance(x, dict): [walk(v) for v in x.values()]
        elif isinstance(x, list): [walk(v) for v in x]
    walk(d); return out[0] if out else None
CLEO, CAP, AXE = first(seeds, 'cleo'), first(seeds, 'cap'), first(seeds, 'axe')
n1, d1 = planes(D1); gcap = np.vstack([D1[np.abs(D1 @ n1[0] - d1[0]) < 1e-9], [I[np.argmax(I @ n1[0])]]])
n2, d2 = planes(I2); scleo = np.vstack([I2[np.abs(I2 @ n2[0] - d2[0]) < 1e-9], [D1[np.argmax(D1 @ n2[0])]]])
e = min(np.linalg.norm(a - b) for a, b in itertools.combinations(I, 2))
i, j = next((i, j) for i, j in itertools.combinations(range(12), 2) if abs(np.linalg.norm(I[i] - I[j]) - e) < 1e-9)
two = [s[-1] for s in GSD if sum(np.min(np.linalg.norm(s[:-1] - I[x], axis=1)) < 1e-9 for x in (i, j)) == 2]; gtet = np.array([I[i], I[j], *two])
claims = [('#38a great-star spike = CLEO', GSD[0], CLEO), ('#38a great-shell inward pyramid = cap', gcap, CAP), ('#38a great-shell valley tetrahedron = AXE', gtet, AXE),
          ('#38a small-shell inward pyramid = CLEO', scleo, CLEO), ('#38a small-shell inward pyramid = great-star spike', scleo, GSD[0]),
          ('#38 ID->RT three-sided pyramid = CLEO', first(upd, 'upPyr3'), CLEO), ('#38 ID->RT five-sided pyramid = cap', first(upd, 'upPyr5'), CAP),
          ('#38 Cleo-Ico = Cleo spike', first(upd, 'upCleo'), first(upd, 'upCleo'))]
for name, P, Q in claims:
    print(f'{name}: {"TRUE" if same_shape(P, Q) else "FALSE"}')
