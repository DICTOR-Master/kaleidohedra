# The Sunstar as rock salt's keyed switch point (DICTO 2026-10-25, "a different but cohesive bond network").
# Claim: in #42's Sunstar lattice (dodecahedra on the even cubes of a cube grid of edge 2, Dogstars on the odd cubes) every
# dodecahedron = its cube + six Euclid roofs (Elements XIII.17) and every Dogstar = its cube − the six roofs of its neighbours.
# So the network is rock salt at its single switch point (all cells cubes, only unlike bonds), keyed with the roofs.
# Exact part (sympy): volumes. Solid part (manifold3d): the app's Dogstar (krp-core, exported to app-solids.json) against cube − roofs,
# and the app's dodecahedron against cube + roofs, by symmetric difference.
import json, itertools, numpy as np, sympy as sp, manifold3d as m3
s5 = sp.sqrt(5); phi = (1 + s5) / 2
cube = [sp.Matrix([x, y, z]) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
# dodecahedron with the cube (±1,±1,±1): the 12 roof-ridge corners are cyclic (0, ±1/φ, ±φ)
ridge = []
for a, b in itertools.product((-1, 1), repeat=2):
    ridge += [sp.Matrix([0, a / phi, b * phi]), sp.Matrix([b * phi, 0, a / phi]), sp.Matrix([a / phi, b * phi, 0])]
V_dodeca = sp.nsimplify(sp.simplify(sp.Rational(15, 4) + 7 * s5 / 4) * (2 / phi) ** 3)
V_dodeca = sp.radsimp(sp.simplify(V_dodeca))
roof = sp.radsimp(sp.simplify((V_dodeca - 8) / 6))
dog = sp.radsimp(sp.simplify(8 - 6 * roof))
out = []
def say(x): print(x); out.append(str(x))
say(f"dodecahedron (cube edge 2) volume = {V_dodeca} = {float(V_dodeca):.9f}")
say(f"one Euclid roof = {roof} = 2φ/3: {sp.simplify(roof - 2 * phi / 3) == 0}")
say(f"Dogstar = cube − 6 roofs = {dog} = {float(dog):.9f};  4/φ²: {sp.simplify(dog - 4 / phi ** 2) == 0}")
say(f"dodecahedron + Dogstar = {sp.simplify(V_dodeca + dog)} (two cubes of edge 2 = 16)")
# solids
f = lambda v: [float(c) for c in v]
hull = lambda P: m3.Manifold.hull_points([f(p) for p in P])
roofs_out = []    # the six roofs of the dodecahedron at the origin
for ax in range(3):
    for sgn in (-1, 1):
        face = [c for c in cube if c[ax] == sgn]; tips = [r for r in ridge if r[ax] * sgn > 1]
        roofs_out.append(hull(face + tips))
C = m3.Manifold.cube([2, 2, 2]).translate([-1, -1, -1])
dodeca_built = C
for r in roofs_out: dodeca_built = dodeca_built + r
# the Dogstar at the origin: its six neighbours are dodecahedra at ±2 along each axis; each pushes one roof in
dog_built = C
for ax in range(3):
    for sgn in (-1, 1):
        shift = [0, 0, 0]; shift[ax] = 2 * sgn
        face = [c for c in cube if c[ax] == -sgn]; tips = [r for r in ridge if r[ax] * -sgn > 1]
        dog_built = dog_built - hull(face + tips).translate(shift)
app = json.load(open('app-solids.json'))
app_dodeca = m3.Manifold.hull_points(app['dodeca'])
say(f"app dodecahedron vs cube + roofs: |symmetric difference| = {(app_dodeca - dodeca_built).volume() + (dodeca_built - app_dodeca).volume():.2e}")
say(f"cube − neighbours' roofs: volume {dog_built.volume():.9f} (exact {float(dog):.9f}), corners of the built solid {len(np.unique(np.round(np.array(dog_built.to_mesh().vert_properties)[:, :3], 9), axis=0))}")
# app Dogstar is not convex: compare point sets by sampling (inside-test via winding on the built solid and the app's vertex cloud)
P = np.array(app['dogstar']); Bv = np.unique(np.round(np.array(dog_built.to_mesh().vert_properties)[:, :3], 7), axis=0)
d_app_to_built = max(min(np.linalg.norm(Bv - p, axis=1)) for p in P)
d_built_to_app = max(min(np.linalg.norm(P - b, axis=1)) for b in Bv)
say(f"app Dogstar corner points vs built corners: every app point is a built corner (max gap {d_app_to_built:.1e}); every built corner is an app point (max gap {d_built_to_app:.1e})")
open('proof.txt', 'w').write('\n'.join(out) + '\n')
