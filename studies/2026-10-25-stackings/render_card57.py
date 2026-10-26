# Blender: #57 dictospheres card. Fang and Chucky in metallic gold (cubic halves) and platinum (hexagonal halves) on a starfield.
# Run beside the h-*.obj files: blender -b -P render_card57.py
import bpy, math, os
from mathutils import Vector
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 160
sc.render.resolution_x, sc.render.resolution_y = 1600, 1200
sc.view_settings.view_transform = 'Standard'

# World: stars + faint nebula for the camera, soft studio grey for reflections (so the metals read)
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; nt = w.node_tree; N, L = nt.nodes, nt.links
for n in list(N): N.remove(n)
out = N.new('ShaderNodeOutputWorld'); tc = N.new('ShaderNodeTexCoord'); lp = N.new('ShaderNodeLightPath')
vor = N.new('ShaderNodeTexVoronoi'); vor.inputs['Scale'].default_value = 260
rmp = N.new('ShaderNodeValToRGB'); rmp.color_ramp.elements[0].position = 0.0; rmp.color_ramp.elements[0].color = (1, 1, 1, 1)
rmp.color_ramp.elements[1].position = 0.08; rmp.color_ramp.elements[1].color = (0, 0, 0, 1)
L.new(tc.outputs['Generated'], vor.inputs['Vector']); L.new(vor.outputs['Distance'], rmp.inputs['Fac'])
dim = N.new('ShaderNodeMath'); dim.operation = 'POWER'; dim.inputs[1].default_value = 6.0  # most stars faint, a few bright
L.new(vor.outputs['Color'], dim.inputs[0])
sep = N.new('ShaderNodeSeparateColor'); L.new(vor.outputs['Color'], sep.inputs[0])
pw = N.new('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = 4.0; L.new(sep.outputs[0], pw.inputs[0])
star = N.new('ShaderNodeMath'); star.operation = 'MULTIPLY'; L.new(rmp.outputs['Color'], star.inputs[0]); L.new(pw.outputs[0], star.inputs[1])
starx = N.new('ShaderNodeMath'); starx.operation = 'MULTIPLY'; starx.inputs[1].default_value = 9.0; L.new(star.outputs[0], starx.inputs[0])
noi = N.new('ShaderNodeTexNoise'); noi.inputs['Scale'].default_value = 1.6; noi.inputs['Detail'].default_value = 8
L.new(tc.outputs['Generated'], noi.inputs['Vector'])
neb = N.new('ShaderNodeValToRGB'); neb.color_ramp.elements[0].position = 0.45; neb.color_ramp.elements[0].color = (0.004, 0.005, 0.014, 1)
neb.color_ramp.elements[1].position = 0.85; neb.color_ramp.elements[1].color = (0.05, 0.03, 0.10, 1)
L.new(noi.outputs['Fac'], neb.inputs['Fac'])
add = N.new('ShaderNodeMix'); add.data_type = 'RGBA'; add.blend_type = 'ADD'; add.inputs['Factor'].default_value = 1.0
L.new(neb.outputs['Color'], add.inputs['A']); L.new(starx.outputs[0], add.inputs['B'])
sky = N.new('ShaderNodeBackground'); L.new(add.outputs['Result'], sky.inputs['Color'])
xyz = N.new('ShaderNodeSeparateXYZ'); L.new(tc.outputs['Generated'], xyz.inputs[0])
grad = N.new('ShaderNodeValToRGB'); E = grad.color_ramp.elements  # bright sky band, dark floor: gives the metals their shine
E[0].position = 0.40; E[0].color = (0.02, 0.02, 0.03, 1); E[1].position = 0.58; E[1].color = (0.75, 0.73, 0.70, 1)
e = E.new(0.50); e.color = (0.12, 0.12, 0.16, 1); e = E.new(0.75); e.color = (0.25, 0.26, 0.32, 1); e = E.new(0.92); e.color = (0.85, 0.86, 0.92, 1)
fz = N.new('ShaderNodeMath'); fz.operation = 'MULTIPLY_ADD'; fz.inputs[1].default_value = 0.5; fz.inputs[2].default_value = 0.5
L.new(xyz.outputs['Z'], fz.inputs[0]); L.new(fz.outputs[0], grad.inputs['Fac'])
studio = N.new('ShaderNodeBackground'); L.new(grad.outputs['Color'], studio.inputs['Color']); studio.inputs['Strength'].default_value = 1.6
mix = N.new('ShaderNodeMixShader'); L.new(lp.outputs['Is Camera Ray'], mix.inputs['Fac'])
L.new(studio.outputs[0], mix.inputs[1]); L.new(sky.outputs[0], mix.inputs[2]); L.new(mix.outputs[0], out.inputs['Surface'])

def mat(name, col, metal=0.0, rough=0.45, emit=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Metallic'].default_value = metal; b.inputs['Roughness'].default_value = rough
    if emit: b.inputs['Emission Color'].default_value = (*col, 1); b.inputs['Emission Strength'].default_value = emit
    return m
def put(fn, m, loc, s, rot):
    bpy.ops.wm.obj_import(filepath=os.path.abspath(fn)); o = bpy.context.selected_objects[0]
    o.data.materials.clear(); o.data.materials.append(m); o.scale = (s,) * 3; o.location = loc; o.rotation_euler = rot
    bpy.ops.object.shade_flat(); return o
def label(txt, x, z, s, col=(0.88, 0.89, 0.93), emit=1.0):
    t = bpy.data.curves.new('n' + txt, 'FONT'); t.body = txt; t.align_x = 'CENTER'; no = bpy.data.objects.new('n' + txt, t); sc.collection.objects.link(no)
    no.location = (x, -2, z); no.rotation_euler = (math.radians(84), 0, 0); no.scale = (s,) * 3; no.data.materials.append(mat('lab' + txt, col, emit=emit))

gold = mat('gold', (1.0, 0.71, 0.29), metal=1.0, rough=0.16)
silver = mat('platinum', (0.70, 0.67, 0.62), metal=1.0, rough=0.20)
rot = (math.radians(-28), math.radians(18), math.radians(52))
for tag, x, S, lab in (('fang', -3.3, 5.0, 'Fang'), ('chucky', 3.3, 2.35, 'Chucky')):
    for nm, m in (('hex-top', silver), ('cubic-bottom', gold)):
        for z, gap in ((1.75, 0.0), (-2.35, 0.45)):
            put(f'h-{tag}-{nm}.obj', m, (x, 0, z + (gap if nm == 'hex-top' else -gap)), S, rot)
    label(lab, x, -4.35, 0.42)
label('platinum: hexagonal top half  ·  gold: cubic bottom half', 0, -5.0, 0.24, (0.75, 0.77, 0.82), 0.7)
label('together', 0, 1.75, 0.26, (0.75, 0.77, 0.82), 0.7); label('drawn apart', 0, -2.35, 0.26, (0.75, 0.77, 0.82), 0.7)

cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); sc.collection.objects.link(cam)
cam.location = (0, -22.5, -1.0); cam.rotation_euler = (math.radians(89), 0, 0); sc.camera = cam; cam.data.lens = 46
for loc, e, col in (((-10, -12, 14), 1400, (1.0, 0.95, 0.88)), ((12, -10, 6), 700, (0.85, 0.9, 1.0)), ((0, 10, 10), 600, (1, 1, 1))):
    l = bpy.data.objects.new('l', bpy.data.lights.new('l', 'AREA')); l.data.energy = e; l.data.size = 8; l.data.color = col; l.location = loc
    sc.collection.objects.link(l); l.rotation_euler = (Vector((0, 0, 0)) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
t = bpy.data.curves.new('t', 'FONT'); t.body = 'DICTO'; to = bpy.data.objects.new('t', t); sc.collection.objects.link(to)
to.location = (6.0, -3, -5.0); to.rotation_euler = (math.radians(84), 0, 0); to.scale = (0.36,) * 3; to.data.materials.append(mat('mark', (0.85, 0.66, 0.2), emit=1.5))
sc.render.filepath = os.path.abspath('card57.png'); bpy.ops.render.render(write_still=True)
