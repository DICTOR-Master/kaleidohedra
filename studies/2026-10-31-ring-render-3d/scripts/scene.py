# Blender (Cycles) scene for the ring renders: imports the ring OBJ (ringmesh.py), places it on a procedural wood table,
# camera and light from a JSON spec, renders a PNG.
# Usage (dicto-big-brother): blender -b -P scene.py -- spec.json
# spec keys: obj, out, res [w,h], samples, M_obj (4x4 object->world, table = plane z=0), cam (4x4 Blender matrix_world),
#   lens_mm (36 mm sensor width), light {az, el, dist, size, power, color}, world {color, strength},
#   ring {color, rough, sss, sss_scale}, wood {scale, c1, c2, c3, rough, rot}, exposure
import bpy, sys, json, math
from mathutils import Matrix, Vector

S = json.load(open(sys.argv[sys.argv.index('--') + 1]))
g = lambda k, d: S.get(k, d)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = g('samples', 128)
sc.cycles.use_denoising = True
try: sc.cycles.denoiser = 'OPENIMAGEDENOISE'
except Exception: pass
sc.cycles.sample_clamp_indirect = g('clamp', 2.0); sc.cycles.blur_glossy = 1.0
sc.cycles.max_bounces = 12; sc.cycles.transmission_bounces = 12; sc.cycles.diffuse_bounces = 4
sc.render.resolution_x, sc.render.resolution_y = g('res', [756, 1008]); sc.render.resolution_percentage = 100
sc.render.film_transparent = False
sc.view_settings.view_transform = g('view', 'AgX')
try: sc.view_settings.look = g('look', 'None')
except Exception as ex: print('look not set', ex)
sc.view_settings.exposure = g('exposure', 0.0)
sc.render.image_settings.file_format = 'PNG'

def principled(name, **kw):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    for k, v in kw.items(): b.inputs[k].default_value = v
    return m, b

R = g('ring', {})
ring_mat, _ = principled('PET', **{'Base Color': (*R.get('color', [0.80, 0.82, 0.85]), 1), 'Roughness': R.get('rough', 0.5),
                                   'Subsurface Weight': R.get('sss', 0.6), 'Subsurface Radius': (1.0, 0.9, 0.75),
                                   'Subsurface Scale': R.get('sss_scale', 0.0015), 'IOR': 1.5})
tie_mat, _ = principled('Nylon', **{'Base Color': (0.92, 0.92, 0.88, 1), 'Roughness': 0.35, 'Transmission Weight': 0.45,
                                    'IOR': 1.53, 'Subsurface Weight': 0.35, 'Subsurface Scale': 0.001})

bpy.ops.wm.obj_import(filepath=S['obj'], forward_axis='Y', up_axis='Z')
M = Matrix(S['M_obj'])
for ob in list(bpy.context.selected_objects):
    ob.matrix_world = M @ ob.matrix_world
    ob.data.materials.clear(); ob.data.materials.append(ring_mat if ob.name.startswith('Rings') else tie_mat)
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.select_all(action='DESELECT'); ob.select_set(True)
    bpy.ops.object.shade_smooth_by_angle(angle=math.radians(35))

# wood table
W = g('wood', {})
bpy.ops.mesh.primitive_plane_add(size=3, location=(0, 0, 0)); tb = bpy.context.object
wm = bpy.data.materials.new('Wood'); wm.use_nodes = True; nt = wm.node_tree; N = nt.nodes; Lk = nt.links
bs = N['Principled BSDF']; bs.inputs['Roughness'].default_value = W.get('rough', 0.42)
tc = N.new('ShaderNodeTexCoord'); rot = math.radians(W.get('rot', 20)); sc_ = W.get('scale', 6.0)
def streaks(sx, sy, det, nscale):
    mp = N.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (sx, sy, 1)
    mp.inputs['Rotation'].default_value = (0, 0, rot); Lk.new(tc.outputs['Object'], mp.inputs['Vector'])
    nz = N.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = nscale; nz.inputs['Detail'].default_value = det
    nz.inputs['Roughness'].default_value = 0.6; Lk.new(mp.outputs['Vector'], nz.inputs['Vector']); return nz
coarse = streaks(sc_ * 0.15, sc_ * 4.0, 4, 1.0)          # broad grain bands along the board
fine = streaks(sc_ * 0.4, sc_ * 25.0, 8, 1.0)            # fine fibres
blot = streaks(sc_ * 0.5, sc_ * 0.5, 3, 2.0)             # soft colour patches
m1 = N.new('ShaderNodeMath'); m1.operation = 'MULTIPLY_ADD'; m1.inputs[1].default_value = 0.5
Lk.new(fine.outputs['Fac'], m1.inputs[0]); Lk.new(coarse.outputs['Fac'], m1.inputs[2])
m2 = N.new('ShaderNodeMath'); m2.operation = 'MULTIPLY_ADD'; m2.inputs[1].default_value = 0.35
Lk.new(blot.outputs['Fac'], m2.inputs[0]); Lk.new(m1.outputs[0], m2.inputs[2])
m3 = N.new('ShaderNodeMapRange'); m3.inputs['From Min'].default_value = 0.55; m3.inputs['From Max'].default_value = 1.35
Lk.new(m2.outputs[0], m3.inputs['Value'])
cr = N.new('ShaderNodeValToRGB'); e = cr.color_ramp.elements
e[0].position = 0.15; e[0].color = (*W.get('c1', [0.30, 0.15, 0.05]), 1)
e[1].position = 0.9; e[1].color = (*W.get('c3', [0.55, 0.32, 0.12]), 1)
mid = e.new(0.55); mid.color = (*W.get('c2', [0.44, 0.24, 0.08]), 1)
Lk.new(m3.outputs['Result'], cr.inputs['Fac']); Lk.new(cr.outputs['Color'], bs.inputs['Base Color'])
bump = N.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.05; bump.inputs['Distance'].default_value = 0.0005
Lk.new(fine.outputs['Fac'], bump.inputs['Height']); Lk.new(bump.outputs['Normal'], bs.inputs['Normal'])
tb.data.materials.append(wm)

# camera
cam = bpy.data.cameras.new('Cam'); cam.lens = S['lens_mm']; cam.sensor_width = 36; cam.sensor_fit = 'HORIZONTAL'
cam.clip_start = 0.005; co = bpy.data.objects.new('Cam', cam); sc.collection.objects.link(co); sc.camera = co
co.matrix_world = Matrix(S['cam'])

# key light (window) + world fill
Lt = g('light', {})
ld = bpy.data.lights.new('Key', 'AREA'); ld.shape = 'DISK'; ld.size = Lt.get('size', 0.5); ld.energy = Lt.get('power', 60)
ld.color = Lt.get('color', [1.0, 0.86, 0.68])
lo = bpy.data.objects.new('Key', ld); sc.collection.objects.link(lo)
az, el, dist = math.radians(Lt.get('az', 135)), math.radians(Lt.get('el', 40)), Lt.get('dist', 1.5)
pos = Vector((math.cos(el) * math.cos(az), math.cos(el) * math.sin(az), math.sin(el))) * dist
lo.location = pos; lo.rotation_euler = (-pos).to_track_quat('-Z', 'Y').to_euler()
Wd = g('world', {})
wo = bpy.data.worlds.new('W'); wo.use_nodes = True; sc.world = wo
bg = wo.node_tree.nodes['Background']; bg.inputs['Color'].default_value = (*Wd.get('color', [1.0, 0.9, 0.78]), 1)
bg.inputs['Strength'].default_value = Wd.get('strength', 0.35)

sc.render.filepath = S['out']
bpy.ops.render.render(write_still=True)
print('RENDERED', S['out'])
