# Test print (DICTO 2026-10-29): one c-slab and one h-slab, consecutive layers 0 (c) and 1 (h) of the stacking ABAC, at λ = 1/10,
# each a patch of its layer tile (balls -N..N), joined into one solid (manifold3d union of the exact convex pieces, each grown by
# 0.1% about its centre so touching faces fuse), then cut by one vertical hexagonal prism (circumradius R ball spacings), the same
# for both slabs, so the two bricks have straight sides and mate exactly.
# Scale S mm per ball spacing. Outputs STL files and a preview picture (closed and apart). Checks: watertight, volume = sum of pieces.
import sys, numpy as np, trimesh, manifold3d as mf
from fractions import Fraction as Fr
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from tiles import tile
from stackings import POS
lam = Fr(sys.argv[1]) if len(sys.argv) > 1 else Fr(1, 10); N = 5; R = 2.6; S = 15.0; D = (2 / 3) ** 0.5
word = 'ABAC'
def cart(p): return np.array([float(p[0]) + float(p[1]) / 2, float(p[1]) * 3 ** 0.5 / 2, float(p[2]) * D]) * S
out = {}
for L, t in ((0, 'c'), (1, 'h')):
    P, _ = tile(word, L, lam); b = POS[word[L]]; parts = []; vol = 0
    for i in range(-N, N + 1):
        for j in range(-N, N + 1):
            for k, up, s, pts, J in P:
                X = np.array([cart((p[0] + b[0] + i, p[1] + b[1] + j, p[2] + L)) for p in pts]); c0 = X.mean(0)
                if np.hypot(*c0[:2]) > (R + 1.5) * S: continue
                h = trimesh.convex.convex_hull(c0 + (X - c0) * 1.001)
                vol += h.volume; parts.append(mf.Manifold(mf.Mesh(vert_properties=np.asarray(h.vertices, np.float32), tri_verts=np.asarray(h.faces, np.uint32))))
    U = mf.Manifold.batch_boolean(parts, mf.OpType.Add)
    hexp = mf.Manifold.extrude(mf.CrossSection.circle(R * S, 6), 200.0).translate((0, 0, -100.0))
    U = U ^ hexp
    B = sorted(U.decompose(), key=lambda q: -q.volume())
    print(f'{t}-slab bodies after cut: {[round(q.volume(), 1) for q in B]}, genus {B[0].genus()}')
    U = B[0]; m = U.to_mesh()                         # keep the brick; slivers cut off at the rim are dropped (listed above)
    T = trimesh.Trimesh(m.vert_properties[:, :3], m.tri_verts, process=False)   # manifold3d output as is (merging near-equal float32 corners pinches it)
    print(f'{t}-slab: {len(parts)} pieces, watertight {T.is_watertight}, bodies {len(T.split())}, volume {T.volume:.1f} mm³ (cut from {vol:.1f}), '
          f'size {np.round(T.extents, 1)} mm')
    T.export(f'../print/dicto-two-tiles-{t}-slab-lam{str(lam).replace("/", "_")}.stl'); out[t] = T
fig = plt.figure(figsize=(12, 6), facecolor='white')
for c, gap in enumerate((0, 25)):
    ax = fig.add_subplot(1, 2, c + 1, projection='3d'); ax.set_proj_type('ortho')
    for t, col in (('c', '#d9a521'), ('h', '#3f7fc4')):
        T = out[t]; V = T.vertices + [0, 0, gap if t == 'h' else 0]
        sh = 0.45 + 0.55 * np.clip(T.face_normals @ np.array([0.3, -0.5, 0.8]) / np.linalg.norm([0.3, -0.5, 0.8]), 0, 1)
        rgb = np.array(matplotlib.colors.to_rgb(col)); fc = np.clip(rgb[None] * sh[:, None], 0, 1)
        ax.add_collection3d(Poly3DCollection(V[T.faces], facecolors=fc, edgecolors='none'))
    A = np.vstack([out['c'].vertices, out['h'].vertices + [0, 0, gap]]); m = A.mean(0); r = (A.max(0) - A.min(0)).max() / 2
    ax.set_xlim(m[0]-r, m[0]+r); ax.set_ylim(m[1]-r, m[1]+r); ax.set_zlim(m[2]-r, m[2]+r); ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=12, azim=-60); ax.set_axis_off(); ax.set_title('stacked' if not gap else 'apart')
fig.suptitle(f'Two Tiles test print: c-slab (gold) under h-slab (blue), hexagonal bricks, side {R * S:g} mm, λ = {lam}, {S:g} mm per ball spacing', fontsize=11)
fig.text(0.98, 0.01, 'DICTO · dictospheres.com', ha='right', fontsize=8, color='#777')
plt.savefig('../print/test-print-preview.png', dpi=120)
