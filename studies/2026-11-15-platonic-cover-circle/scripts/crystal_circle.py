# The Platonic Solids, series front cover, circle design (DICTO, 15 Nov 2026: "just the five solids plain in a circle in DICTO order,
# Dodecahedron at the top"; then: the five at EQUAL VOLUME, and TRANSLUCENT as deep crystal). The five Platonic solids, plain (no
# settings), evenly on a circle 72 degrees apart: Dodecahedron at the top, then clockwise Icosahedron, Cube, Tetrahedron, Octahedron,
# in their element colours (DICTO square, 10-22), all of the same volume. Each turned to a recognisable view.
# Path-traced in Blender Cycles (CPU). Crystal = the material of the ring design (studies/2026-11-15-platonic-cover/scripts/ring_scene.py):
# refractive glass (IOR 1.45), tinted, with a volume absorption in the element colour (deeper colour where thicker); small bevels give
# bright facet edges; light reaching a solid through its body comes from a banded light box, so back facets and edges show inside it.
# Orthographic camera; the camera sees only the cover ground (20, 15, 11).
# Run: blender -b -P crystal_circle.py -- OUT.png WIDTH HEIGHT SAMPLES     (the 2400 x 2200 picture block; lettering by compose.py)
import bpy, bmesh, sys, math, itertools
from mathutils import Vector, Matrix
argv = sys.argv[sys.argv.index('--') + 1:]
OUT, RW, RH, SAMPLES = argv[0], int(argv[1]), int(argv[2]), int(argv[3])
PHI = (1 + 5 ** 0.5) / 2; R2, R5 = 2 ** 0.5, 5 ** 0.5
FAIL = []
def X(name, ok, detail=''):
    print(('X PASS ' if ok else 'X FAIL ') + name + (f': {detail}' if detail != '' else ''), flush=True)
    if not ok: FAIL.append(name)
# ------------------------------------------------------------------ the five solids at edge 1 (standard coordinates, scaled)
cyc = lambda a, b, c: [(a, b, c), (c, a, b), (b, c, a)]
def signs(v): return sorted({tuple(x * t for x, t in zip(v, s)) for s in itertools.product((1, -1), repeat=3)})
CUBE8 = signs((1, 1, 1))
SOLIDS = {
    'D': [tuple(x * PHI / 2 for x in v) for v in CUBE8 + [w for c in cyc(0, 1 / PHI, PHI) for w in signs(c)]],
    'I': [tuple(x / 2 for x in w) for c in cyc(0, 1, PHI) for w in signs(c)],
    'C': [tuple(x / 2 for x in v) for v in CUBE8],
    'T': [tuple(x / (2 * R2) for x in v) for v in CUBE8 if v[0] * v[1] * v[2] > 0],
    'O': [tuple(x / R2 for x in w) for c in cyc(1, 0, 0) for w in signs(c)],
}
ORDER = 'DICTO'
NV, NF, NE = {'D': 20, 'I': 12, 'C': 8, 'T': 4, 'O': 6}, {'D': 12, 'I': 20, 'C': 6, 'T': 4, 'O': 8}, {'D': 30, 'I': 30, 'C': 12, 'T': 6, 'O': 12}
COL = {'D': (138, 92, 196), 'I': (58, 112, 205), 'C': (72, 142, 72), 'T': (205, 62, 40), 'O': (232, 200, 82)}   # element colours
# exact volumes at edge 1
VOL1 = {'D': (15 + 7 * R5) / 4, 'I': 5 * (3 + R5) / 12, 'C': 1.0, 'T': 1 / (6 * R2), 'O': R2 / 3}
# EQUAL VOLUME (DICTO 15 Nov): edge of each = (V / VOL1)^(1/3); V = the common volume in cover units (1 unit = 100 px)
VCOMMON = 36.0
EDGE = {k: (VCOMMON / VOL1[k]) ** (1 / 3) for k in ORDER}
print('edges at equal volume (cube edge = 1): ' + ', '.join(f'{k} {EDGE[k] / EDGE["C"]:.6f}' for k in ORDER), flush=True)
lin = lambda c: tuple(((x / 255 + 0.055) / 1.055) ** 2.4 if x / 255 > 0.04045 else x / 255 / 12.92 for x in c)
# ------------------------------------------------------------------ poses (as the opaque draft: x right, y up, z toward the viewer)
def rot(ax, deg): return Matrix.Rotation(math.radians(deg), 3, Vector(ax).normalized())
def align(a, b): return Vector(a).normalized().rotation_difference(Vector(b).normalized()).to_matrix()
Rx = lambda d: rot((1, 0, 0), d); Ry = lambda d: rot((0, 1, 0), d); Rz = lambda d: rot((0, 0, 1), d)
def upright(A, p):
    q = A @ Vector(p); return Rz(90 - math.degrees(math.atan2(q.y, q.x))) @ A
A5 = align((0, 1, PHI), (0, 0, 1))
POSE = {
    'D': Rx(16) @ Ry(-14) @ A5,                       # a pentagon face toward the viewer, tipped to show its ring
    'I': Rx(12) @ Ry(10) @ upright(A5, (0, -1, PHI)),  # a corner toward the viewer: the five-triangle cap, one point up
    'C': Rx(24) @ Ry(-33),                            # three faces: front, side and top (not square-on)
    'T': Rx(16) @ Ry(15) @ align((1, 1, 1), (0, 1, 0)),  # apex up, standing on a face, two side faces seen
    'O': Rx(14) @ Ry(22),                             # a corner up: the double pyramid
}
TOB = Matrix(((1, 0, 0), (0, 0, -1), (0, 1, 0)))     # (x right, y up, z to viewer) -> Blender (x right, z up, -y to viewer)
# ------------------------------------------------------------------ layout: circle, D at the top, clockwise D I C T O (picture pixels)
W, H, CX, CY, RC = 2400, 2200, 1200, 1125, 720
CEN = {}
for i, k in enumerate(ORDER):
    th = math.radians(90 - 72 * i); CEN[k] = (CX + RC * math.cos(th), CY - RC * math.sin(th))
X('D at the top of the circle', abs(CEN['D'][0] - CX) < 1e-9 and CEN['D'][1] < CY)
X('clockwise D I C T O', CEN['I'][0] > CX > CEN['O'][0] and CEN['C'][1] > CY and CEN['C'][0] > CX and CEN['T'][0] < CX)
gaps = [math.dist(CEN[ORDER[i]], CEN[ORDER[(i + 1) % 5]]) for i in range(5)]
X('evenly spaced, 72 degrees', max(gaps) - min(gaps) < 1e-9, f'{min(gaps):.1f} px between centres')
# ------------------------------------------------------------------ scene
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
def hull_mesh(name, pts):
    bm = bmesh.new(); [bm.verts.new(p) for p in pts]; bm.verts.ensure_lookup_table()
    bmesh.ops.convex_hull(bm, input=bm.verts[:])
    bmesh.ops.dissolve_limit(bm, angle_limit=math.radians(0.5), verts=bm.verts[:], edges=bm.edges[:])
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); return me
def crystal_mat(k):
    m = bpy.data.materials.new('crystal' + k); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    c = lin(COL[k]); tint = tuple(0.15 + 0.85 * x for x in c)
    b.inputs['Base Color'].default_value = (*tint, 1); b.inputs['Metallic'].default_value = 0.0
    b.inputs['Roughness'].default_value = 0.0; b.inputs['IOR'].default_value = 1.45; b.inputs['Transmission Weight'].default_value = 1.0
    cs = tuple(0.92 * x / max(c) for x in c)   # the element colour at full strength: its own hue passes, the others are absorbed
    va = nt.nodes.new('ShaderNodeVolumeAbsorption'); va.inputs['Color'].default_value = (*cs, 1); va.inputs['Density'].default_value = DENS[k]
    nt.links.new(va.outputs[0], nt.nodes['Material Output'].inputs['Volume']); return m
DENS = {'D': 0.42, 'I': 0.50, 'C': 0.60, 'T': 0.80, 'O': 0.55}   # per cover unit, tuned by eye so all five read as deep colour
reach = {}
for k in ORDER:
    s = EDGE[k]; me = hull_mesh(k, [tuple(s * x for x in p) for p in SOLIDS[k]])
    vs = [v.co.copy() for v in me.vertices]; es = [(me.vertices[a].co - me.vertices[b].co).length for a, b in (e.vertices for e in me.edges)]
    X(f'{k}: {len(vs)} corners, {len(me.polygons)} faces, {len(es)} edges', (len(vs), len(me.polygons), len(es)) == (NV[k], NF[k], NE[k]))
    P = SOLIDS[k]; d = [math.dist(a, b) for a, b in itertools.combinations(P, 2)]
    X(f'{k}: edge-1 coordinates exact (shortest corner distance 1 in doubles, attained {NE[k]} times)', abs(min(d) - 1) < 1e-12 and sum(abs(x - 1) < 1e-12 for x in d) == NE[k])
    X(f'{k}: every mesh edge = {s:.6f} (single precision)', max(abs(e - s) for e in es) < 1e-5 * s)
    # volume of the mesh (divergence theorem over its faces) against the common volume
    vol = sum(Vector(me.vertices[p.vertices[0]].co).dot(Vector(me.vertices[p.vertices[i]].co).cross(Vector(me.vertices[p.vertices[i + 1]].co))) / 6
              for p in me.polygons for i in range(1, len(p.vertices) - 1))
    X(f'{k}: volume = {VCOMMON} (mesh, single precision)', abs(abs(vol) - VCOMMON) < 1e-4 * VCOMMON, f'{abs(vol):.5f}')
    me.transform((TOB @ POSE[k]).to_4x4())
    o = bpy.data.objects.new('solid' + k, me); sc.collection.objects.link(o); me.materials.append(crystal_mat(k))
    cx, cy = CEN[k]; o.location = ((cx - W / 2) / 100, 0, (H / 2 - cy) / 100)
    bv = o.modifiers.new('bevel', 'BEVEL'); bv.width = 0.03; bv.segments = 2; bv.limit_method = 'ANGLE'
    reach[k] = max(v.co.length for v in me.vertices) * 100
    px = [(cx + v.co.x * 100, cy - v.co.z * 100) for v in me.vertices]
    X(f'{k}: inside the picture block (circumradius {reach[k]:.0f} px)', all(30 < x < W - 30 and 30 < y < H - 30 for x, y in px))
cl = [gaps[i] - reach[ORDER[i]] - reach[ORDER[(i + 1) % 5]] for i in range(5)]
X('neighbours clear of each other (centre distance > sum of circumradii)', min(cl) > 40, [round(c) for c in cl])
# ------------------------------------------------------------------ studio (the ring design's, scaled 2.5x): soft boxes + light box
w = bpy.data.worlds.new('studio'); sc.world = w
if w.node_tree is None: w.use_nodes = True
nt = w.node_tree; nd = nt.nodes
bg = nd['Background']; lp = nd.new('ShaderNodeLightPath'); mix = nd.new('ShaderNodeMixShader')
cam_bg = nd.new('ShaderNodeBackground'); cam_bg.inputs['Color'].default_value = (*lin((20, 15, 11)), 1); cam_bg.inputs['Strength'].default_value = 1
tc = nd.new('ShaderNodeTexCoord'); sep = nd.new('ShaderNodeSeparateXYZ'); ramp = nd.new('ShaderNodeValToRGB')
nt.links.new(tc.outputs['Generated'], sep.inputs[0])
ma = nd.new('ShaderNodeMath'); ma.operation = 'MULTIPLY_ADD'; ma.inputs[1].default_value = 0.5; ma.inputs[2].default_value = 0.5
nt.links.new(sep.outputs['Z'], ma.inputs[0]); nt.links.new(ma.outputs[0], ramp.inputs[0])
ramp.color_ramp.elements[0].position = 0.0; ramp.color_ramp.elements[0].color = (0.02, 0.018, 0.016, 1)
ramp.color_ramp.elements[1].position = 0.80; ramp.color_ramp.elements[1].color = (0.30, 0.29, 0.28, 1)
e = ramp.color_ramp.elements.new(0.45); e.color = (0.10, 0.09, 0.08, 1)
e = ramp.color_ramp.elements.new(0.53); e.color = (0.70, 0.64, 0.56, 1)
nt.links.new(ramp.outputs['Color'], bg.inputs['Color']); bg.inputs['Strength'].default_value = 0.9
box = nd.new('ShaderNodeBackground'); box.inputs['Strength'].default_value = 2.2
ramp2 = nd.new('ShaderNodeValToRGB'); nt.links.new(ma.outputs[0], ramp2.inputs[0])
ramp2.color_ramp.elements[0].color = (0.35, 0.33, 0.30, 1); ramp2.color_ramp.elements[1].color = (1.0, 0.98, 0.95, 1)
wav = nd.new('ShaderNodeTexWave'); wav.wave_type = 'BANDS'; wav.bands_direction = 'DIAGONAL'; wav.inputs['Scale'].default_value = 1.1
wav.inputs['Distortion'].default_value = 2.0; wav.inputs['Detail'].default_value = 0.0
nt.links.new(tc.outputs['Generated'], wav.inputs['Vector'])
wr = nd.new('ShaderNodeValToRGB'); nt.links.new(wav.outputs['Fac'], wr.inputs[0])
wr.color_ramp.elements[0].position = 0.35; wr.color_ramp.elements[0].color = (0.12, 0.12, 0.12, 1)
wr.color_ramp.elements[1].position = 0.65; wr.color_ramp.elements[1].color = (1, 1, 1, 1)
mul = nd.new('ShaderNodeMix'); mul.data_type = 'RGBA'; mul.blend_type = 'MULTIPLY'; mul.inputs['Factor'].default_value = 1.0
nt.links.new(ramp2.outputs['Color'], mul.inputs['A']); nt.links.new(wr.outputs['Color'], mul.inputs['B'])
nt.links.new(mul.outputs['Result'], box.inputs['Color'])
gt = nd.new('ShaderNodeMath'); gt.operation = 'GREATER_THAN'; gt.inputs[1].default_value = 0.5
nt.links.new(lp.outputs['Transmission Depth'], gt.inputs[0])
mixb = nd.new('ShaderNodeMixShader'); nt.links.new(gt.outputs[0], mixb.inputs['Fac']); nt.links.new(bg.outputs[0], mixb.inputs[1]); nt.links.new(box.outputs[0], mixb.inputs[2])
nt.links.new(lp.outputs['Is Camera Ray'], mix.inputs['Fac']); nt.links.new(mixb.outputs[0], mix.inputs[1]); nt.links.new(cam_bg.outputs[0], mix.inputs[2])
nt.links.new(mix.outputs[0], nd['World Output'].inputs['Surface'])
S_, E_ = 2.5, 2.5 ** 2
def softbox(name, loc, size, power, sx=None):
    L = bpy.data.lights.new(name, 'AREA'); L.shape = 'RECTANGLE'; L.size = size * S_; L.size_y = (sx or size) * S_; L.energy = power * E_
    o = bpy.data.objects.new(name, L); sc.collection.objects.link(o); o.location = Vector(loc) * S_
    o.rotation_euler = (-o.location).to_track_quat('-Z', 'Y').to_euler(); return o
softbox('key', (-9, -11, 12), 7, 5200, 3)
softbox('rim', (10, 7, 6), 6, 3200, 2.5)
softbox('fill', (6, -14, -3), 8, 1400, 4)
softbox('top', (0, 2, 16), 10, 2200, 2)
softbox('back', (-6, 14, 10), 9, 4500, 5)
cam = bpy.data.cameras.new('cam'); cam.type = 'ORTHO'; cam.ortho_scale = W / 100; cam.sensor_fit = 'HORIZONTAL'
co = bpy.data.objects.new('cam', cam); sc.collection.objects.link(co); sc.camera = co
co.location = (0, -60, 0); co.rotation_euler = (math.radians(90), 0, 0)
sc.render.engine = 'CYCLES'; cy = sc.cycles; cy.device = 'CPU'; cy.samples = SAMPLES; cy.use_denoising = True
cy.max_bounces = 32; cy.glossy_bounces = 16; cy.transmission_bounces = 24; cy.transparent_max_bounces = 16; cy.volume_bounces = 2
cy.diffuse_bounces = 2; cy.caustics_reflective = False; cy.caustics_refractive = False; cy.blur_glossy = 0.5
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = RW, RH, 100
sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'; sc.view_settings.exposure = 0.0
sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGB'; sc.render.filepath = OUT
print('PROGRESS 0.10 scene built', flush=True)
if FAIL: print('FINAL FAIL: ' + '; '.join(FAIL)); sys.exit(1)
bpy.ops.render.render(write_still=True)
print('PROGRESS 0.80 rendered', OUT, flush=True)
