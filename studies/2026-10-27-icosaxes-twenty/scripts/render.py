# Icosahedral Hexa block (DICTO 2026-10-27): exact union of the pieces, closedness, volume, and renders (whole + parts).
import bpy, bmesh, sys, os, math
from mathutils import Vector
D = os.path.dirname(os.path.abspath(__file__))
COL = {'frame': (0.95, 0.72, 0.29), 'lotusJewelAxes': (0.95, 0.72, 0.29), 'keyedOut': (0.95, 0.72, 0.29), 'dodecaxes': (0.55, 0.36, 0.85), 'icosaxes': (0.30, 0.78, 0.35), 'unbornAxes': (0.95, 0.55, 0.15), 'ico': (0.95, 0.72, 0.29), 'lotusJewel': (0.95, 0.72, 0.29), 'voidDodeca': (0.55, 0.36, 0.85), 'axe': (0.25, 0.8, 0.9)}

def clear():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def mat(name, rgb, metal=0.9, rough=0.25, alpha=1.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*rgb, 1); b.inputs['Metallic'].default_value = metal; b.inputs['Roughness'].default_value = rough
    if alpha < 1:
        b.inputs['Alpha'].default_value = alpha; m.blend_method = 'BLEND' if hasattr(m, 'blend_method') else None
    return m

def vol(ob):
    bm = bmesh.new(); bm.from_mesh(ob.data); bm.transform(ob.matrix_world); v = bm.calc_volume(signed=False)
    manifold = all(e.is_manifold for e in bm.edges); bm.free(); return v, manifold

def stage(cam_dist=7.5):
    sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 64; sc.cycles.device = 'CPU'
    sc.render.resolution_x = 1440; sc.render.resolution_y = 1080; sc.render.film_transparent = False
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
    w.node_tree.nodes['Background'].inputs['Color'].default_value = (0.02, 0.02, 0.03, 1); w.node_tree.nodes['Background'].inputs['Strength'].default_value = 1
    for loc, e in (((6, -6, 8), 900), ((-7, -3, 4), 400), ((0, 7, 6), 500)):
        bpy.ops.object.light_add(type='AREA', location=loc); L = bpy.context.object; L.data.energy = e; L.data.size = 5
        L.rotation_euler = (Vector((0, 0, 0)) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    bpy.ops.object.camera_add(location=(cam_dist * 0.62, -cam_dist * 0.78, cam_dist * 0.5)); cam = bpy.context.object
    cam.rotation_euler = (Vector((0, 0, 0)) - cam.location).to_track_quat('-Z', 'Y').to_euler(); cam.data.lens = 50; sc.camera = cam

def load(kind):
    bpy.ops.wm.obj_import(filepath=os.path.join(D, f'{kind}.obj'), forward_axis='Y', up_axis='Z')
    obs = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    c = sum((o.matrix_world @ Vector(v.co) for o in obs for v in o.data.vertices), Vector()) / sum(len(o.data.vertices) for o in obs)
    for o in obs: o.location -= c
    return obs

report = []
for kind in (sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else ['A1', 'A2']):
    total = 0
    if os.path.exists(os.path.join(D, f'{kind}.obj')):
      clear(); stage(); obs = load(kind)
      total = 0
      r = max((o.matrix_world @ Vector(v.co)).length for o in obs for v in o.data.vertices); cam = bpy.context.scene.camera
      cam.location = cam.location.normalized() * r * 3.0; cam.rotation_euler = (-cam.location).to_track_quat('-Z', 'Y').to_euler()
      for o in obs:
          role = o.name.split('_')[0]; o.data.materials.clear(); o.data.materials.append(mat(role, COL.get(role, (0.8, 0.8, 0.8)), 0.85 if role != 'axe' else 0.2, 0.3))
          total += vol(o)[0]
          bpy.context.view_layer.objects.active = o
          o.modifiers.new('wf', 'WIREFRAME').thickness = 0.012; o.modifiers['wf'].use_replace = False
      bpy.context.scene.render.filepath = os.path.join(D, f'{kind}-parts.png'); bpy.ops.render.render(write_still=True)
    if not os.path.exists(os.path.join(D, f'{kind}-union.obj')): continue
    # the joined solid: from measure.py (manifold3d), not Blender's boolean (unreliable on touching faces)
    clear(); stage(); bpy.ops.wm.obj_import(filepath=os.path.join(D, f'{kind}-union.obj'), forward_axis='Y', up_axis='Z')
    base = [o for o in bpy.context.scene.objects if o.type == 'MESH'][0]
    c = sum((Vector(v.co) for v in base.data.vertices), Vector()) / len(base.data.vertices); base.location -= c
    r = max((Vector(v.co) - c).length for v in base.data.vertices); cam = bpy.context.scene.camera   # frame the whole solid
    cam.location = (Vector((0.18, 1, 1.618)).normalized() if kind[0] in 'SL' else cam.location.normalized()) * r * 4.3; cam.rotation_euler = (-cam.location).to_track_quat('-Z', 'Y').to_euler()
    bm = bmesh.new(); bm.from_mesh(base.data)
    bmesh.ops.dissolve_limit(bm, angle_limit=math.radians(0.5), verts=bm.verts, edges=bm.edges); bm.to_mesh(base.data); bm.free()
    v, ok = vol(base)
    report.append(f'{kind}: pieces sum {total:.6f}, union {v:.6f} (overlap {total - v:.6f}), closed {ok}, faces {len(base.data.polygons)}, corners {len(base.data.vertices)}')
    base.data.materials.clear(); base.data.materials.append(mat('gold', COL['icosaxes'] if kind[0] in 'HS' else (0.95, 0.72, 0.29) if kind[0] == 'L' else (0.95, 0.72, 0.29) if kind.startswith('K') else (0.95, 0.72, 0.29), 0.9, 0.25))
    bpy.context.scene.render.filepath = os.path.join(D, f'{kind}-whole.png'); bpy.ops.render.render(write_still=True)
open(os.path.join(D, 'report.txt'), 'w').write('\n'.join(report) + '\n'); print('\n'.join(report))
