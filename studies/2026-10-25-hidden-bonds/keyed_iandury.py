# Keyed Ian Dury pair (DICTO 2026-10-25, "proceed"): at the gyrated octet's stop lam = 5/24 the tet-hole piece is DICTO Ian Dury
# (16 corners) and the oct-hole piece the 60° rhombohedron (known), bonded only to Ian Durys across its six rhombi. Keyed exactly as
# Sonsam/Lahdeli (keyed_gyrated.py, same caps and checks, removed keys pushed 1e-4 past the face), both directions, A and B, K = 0.8.
# Valid keyings (one component each, genus 0, total volume conserved) are exported as OBJ (whole + half) and listed in
# keyed_iandury.json for render_keyed_iandury.py.
import os, json
os.environ.setdefault('K', '0.8')
src = open('keyed_gyrated.py').read().replace('LAM = 0.003266957', 'LAM = 5 / 24').split('fig = plt.figure')[0]
exec(src)
import trimesh
valid = []
tot0 = 4 * ConvexHull(Vt).volume + 2 * ConvexHull(Vo).volume
for (d, o), (tp, op) in res.items():
    comps = [len(tp.decompose()), len(op.decompose())]
    vt, vo = tp.volume(), op.volume()
    ok = comps == [1, 1] and tp.genus() == 0 and op.genus() == 0 and abs(4 * vt + 2 * vo - tot0) < 5e-4
    say(f"CHECK {d} {o}: components {comps}, genus {tp.genus()}/{op.genus()}, Ian Dury {vt:.6f}, rhombohedron {vo:.6f}, valid {ok}")
    if not ok: continue
    tag = {'tet->oct': 'TO', 'oct->tet': 'OT'}[d] + o
    for nm, m in (('tet', tp), ('oct', op)):
        mesh = m.to_mesh(); V = np.array(mesh.vert_properties)[:, :3]; c = V.mean(0)
        trimesh.Trimesh(V - c, np.array(mesh.tri_verts)).export(f'ki-{tag}-{nm}.obj')
        half = m.trim_by_plane([0, 1, 0], float(c[1])).to_mesh()
        trimesh.Trimesh(np.array(half.vert_properties)[:, :3] - c, np.array(half.tri_verts)).export(f'ki-{tag}-{nm}-half.obj')
    valid.append(dict(tag=tag, direction=d, option=o, iandury=round(vt, 6), rhombohedron=round(vo, 6)))
json.dump(valid, open('keyed_iandury.json', 'w'), indent=1)
open('keyed_iandury.txt', 'w').write('\n'.join(out) + '\n')
print(json.dumps(valid, indent=1))
