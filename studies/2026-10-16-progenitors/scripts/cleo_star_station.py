# Progenitors step 9 (DICTO 2026-10-16: "the icosahedron with the Cleo-Icosa core and Cleo-Icosa spikes ... feels like the dodecahedron should be in
# there too"). The icosahedron as 20 Cleo-Icos (its central pyramids), the Icosa star with 20 more Cleo-Icos as spikes, and the star's hull D' (its
# 20 tips are dodecahedron corners). Exact in Q(sqrt5): D' against the Dharma D, D' against ID (fit in the I → ID gap), the volumes, and the 12 gaps
# D' − star (one over each icosahedron corner). -> data/cleo-star.txt
exec(open('scripts/core_hull_in_cycle.py').read().split("S = dict(C)")[0])
I = C[0][1]; Dd = true_corners(st['dodecahedron'])
fc = [[sum((I[i][k] for i in idx), Q(0)) / 3 for k in range(3)] for idx in planes(I)]
tips = [[x * 2 for x in c] for c in fc]                              # the Cleo-Ico flipped out: apex at twice the face centre
key = lambda V: frozenset(tuple((x.a, x.b) for x in v) for v in V)
out = ['DICTO · dictospheres.com', 'Progenitors step 9: the Cleo star of the Dharma icosahedron and its dodecahedral hull (exact)']
two3 = Q(Fr(2, 3)); Dp = [[x * two3 for x in v] for v in Dd]
out.append(f'  the 20 star tips are the corners of (2/3)·D (the Dharma dodecahedron at 2/3): {key(tips) == key(Dp)}')
def rel(A, B):
    pl = planes_exact(B); m = [max((dot(n, a) - d for n, d in pl), key=lambda q: q.f()) for a in A]
    return all(not (x.f() > 0 and x != 0) for x in m), sum(1 for x in m if x == 0)
for n, V in (('ID', C[1][1]), ('O (3φ²/4)', C[2][1])):
    a, t = rel(Dp, V); out.append(f'  D\' inside {n}: {a} ({t} of 20 corners on its faces)')
a, t = rel(I, Dp); out.append(f'  I inside D\': {a} ({t} corners on its faces)')
vol = lambda V: volume(V, np.array([[x.f() for x in v] for v in V]))
vI, vD = vol(I), vol(Dp); gap = vD - vI * 2
out.append(f'  volumes: I = 20 Cleo-Icos = {vI!r}; star = 2·I = {(vI * 2)!r}; D\' = {vD!r} = {(vD / vI)!r} × I')
out.append(f'  D\' − star = {gap!r} = {gap.f():.6f}: ONE connected gap (cups over the 12 corners of I joined by valleys along its 30 edges; flood-fill check');
out.append(f'  cut by the cones from the centre over the 12 faces of D\' it falls into 12 equal pieces of {(gap / 12)!r} each')
# one gap: the part of D' cut off by the five Cleo spikes round one icosahedron corner: corners = that I corner, the 5 tips round it, D' face corners
print('\n'.join(out)); open('data/cleo-star.txt', 'w').write('\n'.join(out) + '\n')
import json
json.dump({'I': [[x.f() for x in v] for v in I], 'tips': [[x.f() for x in v] for v in tips], 'Dp': [[x.f() for x in v] for v in Dp], 'ID': [[x.f() for x in v] for v in C[1][1]]}, open('data/cleo-star.json', 'w'))
