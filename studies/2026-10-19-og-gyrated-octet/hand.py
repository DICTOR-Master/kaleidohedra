# EXACT: are the caps left- and right-handed? A cap is the part of the octahedron under one face, outside the OG. The only improper
# symmetries the face's cone allows are the three mirrors through the face's axis and one octahedron corner. If none of them maps the
# OG corners inside the cone onto themselves, the cap has no mirror symmetry: it is chiral.
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'check.py')).read().split("n = (Q5(1), Q5(1), Q5(1))")[0])
Rv = R
# the closed cone over the face x+y+z=R from the centre: x, y, z >= 0 (the face is the triangle on the positive axes)
inside = {v for v in V if all(c.sign() >= 0 for c in v)}
print('OG corners in the cone of face (1,1,1):', len(inside))
mirrors = {'y=z': lambda v: (v[0], v[2], v[1]), 'x=z': lambda v: (v[2], v[1], v[0]), 'x=y': lambda v: (v[1], v[0], v[2])}
for name, f in mirrors.items(): print(f'mirror {name} maps them to themselves:', {f(v) for v in inside} == inside)
turn = lambda v: (v[2], v[0], v[1])
print('the 3-fold turn maps them to themselves:', {turn(v) for v in inside} == inside)
# hands per octahedron: faces reached from (1,1,1) by rotations (even number of minus signs) keep the hand; the others are inverted
print('faces with the same hand as (1,1,1): (1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1); the other four are its mirror images')
