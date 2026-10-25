# Blender render of the valid keyed Ian Dury pairs (keyed_iandury.json): per keying, DICTO Ian Dury (gold) and the keyed 60°
# rhombohedron (blue), whole on top and cut in half below. Run: blender -b -P render_keyed_iandury.py
import bpy, math, os, json
from mathutils import Vector
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 64; sc.render.resolution_y = 1300
sc.world = bpy.data.worlds.new('w'); sc.world.use_nodes = True; sc.world.node_tree.nodes['Background'].inputs[0].default_value = (0.06, 0.07, 0.09, 1)
def mat(name, col):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Roughness'].default_value = 0.45; return m
gold = mat('gold', (0.85, 0.62, 0.22)); blue = mat('blue', (0.30, 0.45, 0.85))
valid = json.load(open('keyed_iandury.json'))
cols = [(v['tag'], nm, m, f"{i + 1}  {lab}") for i, v in enumerate(valid) for nm, m, lab in (('tet', gold, 'Ian Dury'), ('oct', blue, 'rhombohedron'))]
step = 3.6; x = -step * (len(cols) - 1) / 2; S = 2.3
for tag, nm, m, lab in cols:
    for fn, z in ((f'ki-{tag}-{nm}.obj', 1.9), (f'ki-{tag}-{nm}-half.obj', -1.9)):
        bpy.ops.wm.obj_import(filepath=os.path.abspath(fn)); o = bpy.context.selected_objects[0]
        o.data.materials.clear(); o.data.materials.append(m); o.scale = (S,) * 3; o.location = (x, 0, z)
        o.rotation_euler = (math.radians(-25), 0, math.radians(20)) if fn.endswith('half.obj') else (math.radians(-60), 0, math.radians(25))
        if fn.endswith('half.obj'):
            cutm = mat('cut_' + tag + nm, tuple(min(1, c * 1.35 + 0.12) for c in m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value[:3]))
            o.data.materials.append(cutm)
            for p in o.data.polygons:
                if abs(p.normal.y - 1) < 1e-3 or abs(p.normal.y + 1) < 1e-3: p.material_index = 1
    t = bpy.data.curves.new('n' + tag + nm, 'FONT'); t.body = lab; t.align_x = 'CENTER'; no = bpy.data.objects.new('n' + tag + nm, t); sc.collection.objects.link(no)
    no.location = (x, -2, -4.3); no.rotation_euler = (math.radians(84), 0, 0); no.scale = (0.34,) * 3; no.data.materials.append(mat('lab' + tag + nm, (0.92, 0.92, 0.95)))
    x += step
sc.render.resolution_x = max(1600, int(450 * len(cols)))
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); sc.collection.objects.link(cam)
cam.location = (0, -max(14, 4.3 * len(cols)), 0.6); cam.rotation_euler = (math.radians(84), 0, 0); sc.camera = cam; cam.data.lens = 40
for loc, e in (((-10, -12, 14), 900), ((12, -10, 8), 500), ((0, 10, 10), 300)):
    l = bpy.data.objects.new('l', bpy.data.lights.new('l', 'AREA')); l.data.energy = e; l.data.size = 8; l.location = loc; sc.collection.objects.link(l)
    l.rotation_euler = (Vector((0, 0, 0)) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
t = bpy.data.curves.new('t', 'FONT'); t.body = 'DICTO'; to = bpy.data.objects.new('t', t); sc.collection.objects.link(to)
to.location = (step * (len(cols) - 1) / 2 - 0.6, -3, -4.9); to.rotation_euler = (math.radians(84), 0, 0); to.scale = (0.38,) * 3; to.data.materials.append(mat('mark', (0.72, 0.59, 0.18)))
sc.render.filepath = os.path.abspath('keyed-iandury.png'); bpy.ops.render.render(write_still=True)
