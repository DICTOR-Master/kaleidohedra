# Which OG is the mirror twin? Test (exactly) whether the OG reflected in an octahedron face is the OG turned 90 degrees about a cube axis
# (the other of the two icosahedral settings in a cubic frame), up to the shift to the neighbouring octahedron.
exec(open('check.py').read().split("# the angle across the joint")[0])
c2 = tuple(2 * Rv / nn * n[k] for k in range(3))                        # the twin octahedron's centre
Mc = {tuple(v[k] - c2[k] for k in range(3)) for v in M}                  # the twin OG, moved back to the origin
z = Q5(0)
rots = {'90 about x': lambda v: (v[0], -v[2], v[1]), '90 about y': lambda v: (v[2], v[1], -v[0]), '90 about z': lambda v: (-v[1], v[0], v[2]),
        'identity': lambda v: v}
for name, f in rots.items(): print(f'twin = OG turned {name}:', Mc == {f(v) for v in V})
print('twin = OG inverted through the centre:', Mc == {tuple(-x for x in v) for v in V})
# reflection in a plane at right angles to a 3-fold axis = inversion x half-turn about that axis; the OG has inversion and a 3-fold turn,
# so the twin should be the OG turned 60 degrees about the shared 3-fold axis (1,1,1) - an exact rational rotation
F3 = lambda a, b: Q5(Fr(a, b))
R60 = ((F3(2, 3), F3(-1, 3), F3(2, 3)), (F3(2, 3), F3(2, 3), F3(-1, 3)), (F3(-1, 3), F3(2, 3), F3(2, 3)))
rot = lambda M_, v: tuple(sum((M_[i][k] * v[k] for k in range(3)), Q5(0)) for i in range(3))
print('R60 is a rotation about (1,1,1):', rot(R60, (Q5(1), Q5(1), Q5(1))) == (Q5(1), Q5(1), Q5(1)))
print('twin = OG turned 60 degrees about the joint axis (1,1,1):', Mc == {rot(R60, v) for v in V})
