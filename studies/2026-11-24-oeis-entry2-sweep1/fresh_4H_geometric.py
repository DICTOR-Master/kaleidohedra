"""Entry 2, fresh second method: coordination sequences of the 4H (ABAC) tetrahedral network found GEOMETRICALLY.
Atoms get exact integer coordinates (x, y, z): in-plane point (x*a1 + y*a2)/3 on the triangular lattice (a = 1, a1.a2 = 1/2),
height z in units of b/3 (b = bond length = a*sqrt(3/8), ideal tetrahedra). Bilayer k holds a lower atom at z = 4k and an
upper atom at z = 4k + 3, both at in-plane positions x = y = L(k) (mod 3), L = 0, 1, 2 for A, B, C.
72 * squared distance = 8*(dx^2 + dx*dy + dy^2) + 3*dz^2; two atoms are bonded iff this equals 27 (= 72 b^2).
No stacking-orientation rule is used: the bond vectors are all integer solutions of 8Q + 3dz^2 = 27, kept if the end is an atom.
Breadth-first search by shells (bipartite: next shell = neighbours of this shell minus the previous shell)."""
import sys
N = int(sys.argv[1]) if len(sys.argv) > 1 else 100
STACK = 'ABAC'; L = ['ABC'.index(c) for c in STACK]; P = len(STACK)
VEC = [(dx, dy, dz) for dx in range(-4, 5) for dy in range(-4, 5) for dz in range(-4, 5)
       if 8 * (dx * dx + dx * dy + dy * dy) + 3 * dz * dz == 27]
def is_atom(x, y, z):
    k, r = divmod(z, 4)
    if r not in (0, 3): return False
    l = L[k % P]
    return (x - l) % 3 == 0 and (y - l) % 3 == 0
def nbrs(v):
    x, y, z = v
    return [(x + a, y + b, z + c) for a, b, c in VEC if is_atom(x + a, y + b, z + c)]
def cs(v0, n):
    assert is_atom(*v0)
    prev, cur, out = set(), {v0}, [1]
    for _ in range(n):
        nxt = {w for v in cur for w in nbrs(v)} - prev - cur
        prev, cur = cur, nxt; out.append(len(cur))
    return out
# sanity: every atom has 4 bonds
for z in range(0, 16):
    for x in range(3):
        if is_atom(x, x, z): assert len(nbrs((x, x, z))) == 4, (x, z)
sites = {'bilayer1 B (h) lower': (1, 1, 4), 'bilayer1 B (h) upper': (1, 1, 7),
         'bilayer3 C (h) lower': (2, 2, 12), 'bilayer3 C (h) upper': (2, 2, 15),
         'bilayer0 A (c) lower': (0, 0, 0), 'bilayer2 A (c) upper': (0, 0, 11)}
for name, v in sites.items():
    print(name + ':', ','.join(map(str, cs(v, N))))
