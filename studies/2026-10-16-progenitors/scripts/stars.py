# Progenitors step 5 (DICTO 2026-10-16): "take an icosahedron and place 20 Cleo-Icos on the outside as a star, and the same with a dodecahedron".
# Each star = the solid with its own central face pyramids flipped outward (a tip on every face at twice the face distance): the Icosa star
# (I + 20 Cleo-Icos) and the Dodeca star (D + 12 central pyramids). Built on the Dharma's I and D (Chain of Karma pair), exact in Q(sqrt5):
# tip radii, hulls, and how each star and its tips sit against the stations, H and O (on the Dharma ID). -> data/stars.txt
exec(open('scripts/o_dharma.py').read().split("out = ['DICTO")[0])
def face_centres(V):
    out = []
    for idx in planes(V):
        c = [sum((V[i][k] for i in idx), Q(0)) / len(idx) for k in range(3)]; out.append(c)
    return out
def star(V):                                   # tips at twice each face centre (apex of the flipped central pyramid)
    return [[x * 2 for x in c] for c in face_centres(V)]
I = C[0][1]; D = true_corners(st['dodecahedron'])
TIi, TId = star(I), star(D)
r2 = lambda v: dot(v, v)
out = ['DICTO · dictospheres.com', 'Progenitors step 5: the Icosa star (I + 20 Cleo-Icos) and the Dodeca star (D + 12 central pyramids), on the Dharma I and D (exact)']
out.append(f'  Icosa star: 20 tips at radius² {r2(TIi[0])!r} = {r2(TIi[0]).f():.6f} (I corners at {r2(I[0])!r} = {r2(I[0]).f():.6f})')
out.append(f'  Dodeca star: 12 tips at radius² {r2(TId[0])!r} = {r2(TId[0]).f():.6f} (D corners at {r2(D[0])!r} = {r2(D[0]).f():.6f})')
S = dict(C); S['D'] = D; S['O·(3φ²/4)'] = S.pop('O')
def where(P, label):
    for n, V in S.items():
        pl = planes_exact(V); vals = [max((dot(nn, p) - d for nn, d in pl), key=lambda q: q.f()) for p in P]
        ins = all(not (v.f() > 1e-15) for v in vals); on = sum(1 for v in vals if v == 0)
        out.append(f'    {label} tips vs {n}: all inside {ins}; {on} on its faces')
    for n, V in S.items():
        if len(V) == len(P): out.append(f'    {label} tips are the corners of {n}: {frozenset(tuple((x.a, x.b) for x in v) for v in V) == frozenset(tuple((x.a, x.b) for x in v) for v in P)}')
where(TIi, 'Icosa star'); where(TId, 'Dodeca star')
both = TIi + TId                                   # the two stars together (I and D as in the Dharma): the hull of all 32 tips
Bf = np.array([[x.f() for x in v] for v in both]); h = ConvexHull(Bf)
out.append(f'  both stars together: hull of the 32 tips has {len(h.vertices)} corners, {len(set(tuple(np.round(e, 7)) for e in h.equations))} face planes; '
           f'tip radii {np.sqrt((Bf ** 2).sum(1)).min():.5f} (I tips) / {np.sqrt((Bf ** 2).sum(1)).max():.5f} (D tips)')
print('\n'.join(out)); open('data/stars.txt', 'w').write('\n'.join(out) + '\n')
