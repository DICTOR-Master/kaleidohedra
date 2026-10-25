# Blender: fig1 (Sunstar keyed switch point) and fig2 (the octet walk and the twinned walk). Run: blender -b -P render_figs.py -- 1|2
import bpy, math, os, sys
from mathutils import Vector
which = sys.argv[sys.argv.index('--') + 1]
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 64; sc.render.resolution_y = 1100
sc.world = bpy.data.worlds.new('w'); sc.world.use_nodes = True; sc.world.node_tree.nodes['Background'].inputs[0].default_value = (0.06, 0.07, 0.09, 1)
def mat(name, col, alpha=1.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Roughness'].default_value = 0.45; b.inputs['Alpha'].default_value = alpha
    if alpha < 1: m.blend_method = 'BLEND' if hasattr(m, 'blend_method') else None
    return m
def put(fn, m, loc, s, rot=(math.radians(-60), 0, math.radians(25))):
    bpy.ops.wm.obj_import(filepath=os.path.abspath(fn)); o = bpy.context.selected_objects[0]
    o.data.materials.clear(); o.data.materials.append(m); o.scale = (s,) * 3; o.location = loc; o.rotation_euler = rot; return o
def label(txt, x, z=-3.0, s=0.30):
    t = bpy.data.curves.new('n' + txt, 'FONT'); t.body = txt; t.align_x = 'CENTER'; no = bpy.data.objects.new('n' + txt, t); sc.collection.objects.link(no)
    no.location = (x, -2, z); no.rotation_euler = (math.radians(84), 0, 0); no.scale = (s,) * 3; no.data.materials.append(mat('lab' + txt, (0.92, 0.92, 0.95)))
gold = mat('gold', (0.85, 0.62, 0.22)); blue = mat('blue', (0.30, 0.45, 0.85)); purple = mat('purple', (0.55, 0.36, 0.78)); glass = mat('glass', (0.8, 0.85, 0.95), 0.18); red = mat('red', (0.82, 0.30, 0.25))
if which == '1':
    from mathutils import Euler
    R = Euler((math.radians(-60), 0, math.radians(25))).to_matrix()
    put('f1-cube.obj', mat('grey', (0.62, 0.64, 0.70)), (-6.5, 0, -0.4), 1.0)
    for i in range(6):
        off = [0, 0, 0]; off[i // 2] = (-1 if i % 2 == 0 else 1) * 0.45
        put(f'f1-roof{i}.obj', red, Vector((-6.5, 0, -0.4)) + R @ Vector(off), 1.0)
    label('cube + 6 Euclid roofs', -6.5)
    put('f1-dodeca.obj', gold, (-2.2, 0, -0.4), 1.25); label('= dodecahedron  10 + 2√5', -2.2)
    put('f1-cube.obj', glass, (2.2, 0, -0.4), 1.25); put('f1-dogstar.obj', purple, (2.2, 0, -0.4), 1.25); label('cube − 6 roofs', 2.2)
    put('f1-dogstar.obj', purple, (6.5, 0, -0.4), 1.25); label('= Dogstar  4/φ²', 6.5)
    xs = 9.0
else:
    row = [('samson', gold, 'Samson'), ('delilah', blue, 'Delilah'), ('cube', gold, 'cube (3/8)')]
    row2 = [('sonsam', gold, 'Sonsam'), ('lahdeli', blue, 'Lahdeli'), ('iandury', gold, 'Ian Dury (5/24)'), ('rhombo', blue, '60° rhombohedron'), ('blockhead', gold, 'Blockhead (3/8)')]
    for i, (fn, m, lab) in enumerate(row):
        x = -7.2 + i * 3.6; put(f'f2-{fn}.obj', m, (x, 0, 2.3), 3.2); label(lab, x, 0.55, 0.26)
    for i, (fn, m, lab) in enumerate(row2):
        x = -7.2 + i * 3.6; put(f'f2-{fn}.obj', m, (x, 0, -1.9), 3.2); label(lab, x, -3.75, 0.26)
    label('top: octet (cubic stacking)', 6.6, 2.6, 0.3); label('bottom: twinned octet (hexagonal stacking)', 6.6, 1.9, 0.3)
    xs = 9.0
sc.render.resolution_x = 2400
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); cam.location = (0, -21 if which == '1' else -24.5, 1.0 if which == '1' else 2.4); cam.rotation_euler = (math.radians(84), 0, 0); sc.camera = cam; cam.data.lens = 40
for loc, e in (((-10, -12, 14), 900), ((12, -10, 8), 500), ((0, 10, 10), 300)):
    l = bpy.data.objects.new('l', bpy.data.lights.new('l', 'AREA')); l.data.energy = e; l.data.size = 8; l.location = loc; sc.collection.objects.link(l)
    l.rotation_euler = (Vector((0, 0, 0)) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
t = bpy.data.curves.new('t', 'FONT'); t.body = 'DICTO'; to = bpy.data.objects.new('t', t); sc.collection.objects.link(to); to.location = ((6.9 if which == '1' else 7.6), -3, -4.0); to.rotation_euler = (math.radians(84), 0, 0); to.scale = (0.36,) * 3; to.data.materials.append(mat('mark', (0.72, 0.59, 0.18)))
sc.render.filepath = os.path.abspath(f'fig{which}.png'); bpy.ops.render.render(write_still=True)
