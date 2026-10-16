# The stella cut puffed out (DICTO 2026-10-16: "can't it puff out to fill the skin?"): its 6 golden hexagons face the bcc cell's 6 square
# walls (both square to the cube axes); push those 6 golden planes out onto the square walls, so a copy touches all 14 neighbours face to
# face (8 joint walls + 6 square walls). Exact in Q(√5): corners, faces, volume and share of space. The limit of puffing everything is the
# cell itself (100%, a truncated octahedron, no golden faces). -> data/stella-puff-exact.txt
src = open('scripts/stella_cut_exact.py').read()
exec(src[:src.index("C = polytope(H_K + HEX)")])
from collections import Counter
VOR_sq = [(t, d) for t, d in VOR if dot(t, t) == max((dot(u, u) for u, _ in VOR if any(iszero(cross(u, w)) for w, _ in H_K)), key=lambda x: x.f())] if False else None
# the cell's walls: the 8 joint walls (shortest lattice vectors) and the 6 square walls (next shortest)
L2 = sorted({(dot(t, t).a, dot(t, t).b) for t in LAT}, key=lambda ab: float(ab[0]) + float(ab[1]) * 5 ** .5)
sq2 = Q(*L2[1]); SQ = [t for t in LAT if dot(t, t) == sq2]; assert len(SQ) == 6, len(SQ)
# golden planes parallel to a square wall get the wall's own distance; the rest stay
HK2 = []
for n, d in H_K:
    w = next((t for t in SQ if iszero(cross(n, t)) and dot(n, t).f() > 0), None)
    HK2.append((n, d) if w is None else (n, dot(n, w) / 2))   # n·x ≤ n·(w/2): the wall's plane
moved = sum(1 for (n, d), (n2, d2) in zip(H_K, HK2) if d != d2)
CELL = polytope(VOR); S = polytope(H_K + HEX + VOR); P = polytope(HK2 + HEX + VOR)
vC, vS, vP = pvol(CELL), pvol(S), pvol(P)
fs = lambda X: dict(Counter(len(g[2]) for g in X['F']))
say(f'golden planes moved onto the square walls: {moved}')
say(f'stella cut: {len(S["V"])} corners, faces {fs(S)}, share {(vS / vC)!r} = {(vS / vC).f():.6f}')
say(f'puffed stella cut: {len(P["V"])} corners, faces {fs(P)}, volume {vP!r} = {vP.f():.6f}, share of space {(vP / vC)!r} = {(vP / vC).f():.6f}')
open('data/stella-puff-exact.txt', 'w').write('DICTO · dictospheres.com\n' + '\n'.join(out) + '\n')
