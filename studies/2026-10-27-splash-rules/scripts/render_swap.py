# Blender (dicto-big-brother): Swap Rule figure. Top row together, bottom row drawn apart at the gap's mid-plane:
# pure cubic tetrahedral piece | mixed piece (cubic layer below, hexagonal above) | pure hexagonal piece. d^2 = 3/4 * 2/3, lam = 1/10.
import bpy, math, os
D = os.path.expanduser('~/kres-tmp/splash/fig')
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 64; sc.render.resolution_x = 2400; sc.render.resolution_y = 1250
sc.world = bpy.data.worlds.new('w'); sc.world.use_nodes = True; sc.world.node_tree.nodes['Background'].inputs[0].default_value = (0.06, 0.07, 0.09, 1)
sc.view_settings.view_transform = 'Standard'
def mat(name, col, em=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Roughness'].default_value = 0.4
    if em: b.inputs['Emission Color'].default_value = (*col, 1); b.inputs['Emission Strength'].default_value = em
    return m
gold = mat('gold', (0.85, 0.62, 0.22)); plat = mat('plat', (0.72, 0.76, 0.82)); white = mat('white', (0.92, 0.92, 0.95), 1.0); dmark = mat('dm', (0.85, 0.62, 0.22), 1.0)
ROT = (math.radians(-12), math.radians(6), math.radians(35)); S = 3.2
def put(fn, m, loc):
    bpy.ops.wm.obj_import(filepath=f'{D}/{fn}.obj', forward_axis='Y', up_axis='Z'); o = bpy.context.selected_objects[0]
    o.data.materials.clear(); o.data.materials.append(m); o.scale = (S,) * 3; o.location = loc; o.rotation_euler = ROT
    bpy.ops.object.shade_flat(); return o
def label(txt, x, z, s=0.26, m=white):
    t = bpy.data.curves.new('n', 'FONT'); t.body = txt; t.align_x = 'CENTER'; o = bpy.data.objects.new('n', t); sc.collection.objects.link(o)
    o.location = (x, -2, z); o.rotation_euler = (math.radians(90), 0, 0); o.scale = (s,) * 3; o.data.materials.append(m)
X = {'c': -5.2, 'm': 0, 'h': 5.2}; ZT, ZB, GAP = 2.2, -1.9, 0.45
put('pure-c', gold, (X['c'], 0, ZT)); put('pure-h', plat, (X['h'], 0, ZT))
put('mixed-bottom', gold, (X['m'], 0, ZT)); put('mixed-top', plat, (X['m'], 0, ZT))
for k, bot, top, mb, mt in (('c', 'pure-c-bottom', 'pure-c-top', gold, gold), ('m', 'mixed-bottom', 'mixed-top', gold, plat), ('h', 'pure-h-bottom', 'pure-h-top', plat, plat)):
    put(bot, mb, (X[k], 0, ZB - GAP)); put(top, mt, (X[k], 0, ZB + GAP))
label('pure cubic piece', X['c'], -4.2); label('mixed piece: cubic layer below, hexagonal above', X['m'], -4.2); label('pure hexagonal piece', X['h'], -4.2)
label('together', 0, 4.3, 0.22); label('drawn apart at the mid-plane', 0, -0.2, 0.22)
label('Swap Rule: bottom = the pure cubic bottom, top = the pure hexagonal top (exact), so mixed + mixed = pure + pure', 0, -5.0, 0.2)
label('DICTO', 8.9, -5.0, 0.35, dmark)
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); cam.location = (0, -24, 0); cam.rotation_euler = (math.radians(90), 0, 0); sc.camera = cam; cam.data.lens = 40
for loc, e in (((-10, -12, 14), 1100), ((12, -10, 8), 600), ((0, 10, 10), 300)):
    l = bpy.data.objects.new('l', bpy.data.lights.new('l', 'AREA')); l.data.energy = e; l.data.size = 8; l.location = loc; sc.collection.objects.link(l)
sc.render.filepath = os.path.expanduser('~/kres-tmp/splash/swap-rule.png'); bpy.ops.render.render(write_still=True)
