# The stops of the 20-corner sinking: windows close (genus 11 -> sealed shell), hollow fills (one solid, genus 0). Then four render states.
exec(open('twenty.py').read().split('lo, hi = 0.5')[0])
def U_at(d): return mf.Manifold.batch_boolean(pieces(d), mf.OpType.Add)
def bisect(test, lo, hi):   # test true at lo, false at hi
    for _ in range(40):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if test(m) else (lo, m)
    return (lo + hi) / 2
touch = 2.267283
win = bisect(lambda d: U_at(d).genus() == 11, 1.48, 1.36)      # open at 1.48, shut at 1.36
# hollow: the cavity is the second part; it vanishes when the union is one part of genus 0
fill = bisect(lambda d: not (len(U_at(d).decompose()) == 1 and U_at(d).genus() == 0), win - 1e-4, 0.2)
for name, d in [('windows close', win), ('hollow fills', fill)]:
    U = U_at(d - 1e-6); print(f'{name}: d = {d:.6f} ({d / touch:.4f} of touch); just inside: genus {U.genus()}, parts {len(U.decompose())}, volume {U.volume():.4f}')
for k, d in enumerate([touch, (touch + win) / 2, win - 0.002, fill - 0.002]):
    U = U_at(d); T = U.to_mesh(); t = trimesh.Trimesh(T.vert_properties[:, :3], T.tri_verts); t.merge_vertices(); t.export(f'S{k}-union.obj')
    print(f'S{k} d={d:.4f}: genus {U.genus()}, parts {len(U.decompose())}, volume {U.volume():.4f}, flat faces {len(t.facets) + len(t.faces) - sum(len(x) for x in t.facets)}')
