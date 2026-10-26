# Render the stacking columns side by side: network pieces solid (gold from cubic layers, platinum from hexagonal), voids faint glass.
import bpy, os, sys, math
from mathutils import Vector
D = os.path.dirname(os.path.abspath(__file__)); args = sys.argv[sys.argv.index('--') + 1:]; PATCH = '--patch' in args; words = [a for a in args if a != '--patch']
PRE, STEP = ('patch', 4.6) if PATCH else ('col', 2.4)
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.samples = 96; sc.render.resolution_x = 1600; sc.render.resolution_y = 1200
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs['Color'].default_value = (0.02, 0.02, 0.03, 1)
def mat(name, rgb, metal, rough, alpha=1.0, trans=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*rgb, 1); b.inputs['Metallic'].default_value = metal; b.inputs['Roughness'].default_value = rough
    b.inputs['Alpha'].default_value = alpha
    if 'Transmission Weight' in b.inputs: b.inputs['Transmission Weight'].default_value = trans
    return m
M = {'tet_c': mat('tc', (0.95, 0.72, 0.29), 1, 0.22), 'tet_h': mat('th', (0.85, 0.84, 0.82), 1, 0.18),
     'void_c': mat('vc', (0.95, 0.80, 0.55), 0, 0.05, 0.16), 'void_h': mat('vh', (0.85, 0.88, 0.95), 0, 0.05, 0.16)}
x0 = 0; tops = []
for word in words:
    before = set(bpy.data.objects); bpy.ops.wm.obj_import(filepath=os.path.join(D, f'{PRE}_{word}.obj'), forward_axis='Y', up_axis='Z')
    obs = [o for o in bpy.data.objects if o not in before]
    for o in obs:
        role = '_'.join(o.name.split('_')[:2]); o.data.materials.clear(); o.data.materials.append(M[role]); o.location.x += x0
        if role.startswith('void'): o.visible_shadow = False
    tops.append(max(v.co.z for o in obs for v in o.data.vertices)); x0 += STEP
for loc, e in (((6, -9, 9), 1500), ((-6, -6, 5), 600), ((3, 8, 7), 700)):
    bpy.ops.object.light_add(type='AREA', location=loc); L = bpy.context.object; L.data.energy = e; L.data.size = 6
    L.rotation_euler = (Vector((x0 / 2, 0, 1)) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
allv = [o.matrix_world @ v.co for o in bpy.data.objects if o.type == 'MESH' for v in o.data.vertices]   # frame everything
lo = Vector([min(v[i] for v in allv) for i in range(3)]); hi = Vector([max(v[i] for v in allv) for i in range(3)]); c = (lo + hi) / 2
span = max(hi.x - lo.x, (hi.z - lo.z) * 4 / 3); bpy.ops.object.camera_add(location=c + Vector((0, -1, 0.3)).normalized() * span * 2.1)
cam = bpy.context.object; cam.rotation_euler = (c - cam.location).to_track_quat('-Z', 'Y').to_euler(); cam.data.lens = 50; sc.camera = cam
sc.render.filepath = os.path.join(D, f'{PRE}es.png' if PATCH else 'columns.png'); bpy.ops.render.render(write_still=True); print('ok')
