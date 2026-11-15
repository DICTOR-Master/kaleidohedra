# The Platonic Solids, series front cover, second design (DICTO 15 Nov 2026: "a ring with the Japanese character in the middle and
# crystal deep translucent colours"). One gold finger ring = the series' ring (The Five Orders of Space follows Musashi's five rings;
# this book's ring is Wind), the character 風 set in the middle of the hoop, and the five Platonic solids as translucent crystal stones
# on the band in D·I·C·T·O order, all at edge 1, in their element colours (DICTO square, 10-22).
# Path-traced in Blender Cycles (CPU): metallic gold = Principled BSDF metallic 1 with real reflections of a studio environment and
# soft-box lights; crystal = refractive glass (IOR 1.45) with a volume absorption in the element colour, so colour deepens with thickness.
# Run: blender -b -P ring_scene.py -- OUT.png WIDTH HEIGHT SAMPLES      (the picture block of the cover; lettering by compose.py)
import bpy, bmesh, sys, math, itertools
from mathutils import Vector, Matrix
argv = sys.argv[sys.argv.index('--') + 1:]
OUT, RW, RH, SAMPLES = argv[0], int(argv[1]), int(argv[2]), int(argv[3])
PHI = (1 + 5 ** 0.5) / 2
FAIL = []
def X(name, ok, detail=''):
    print(('X PASS ' if ok else 'X FAIL ') + name + (f': {detail}' if detail != '' else ''), flush=True)
    if not ok: FAIL.append(name)
# ------------------------------------------------------------------ the five solids at edge 1 (standard coordinates, scaled)
cyc = lambda a, b, c: [(a, b, c), (c, a, b), (b, c, a)]
def signs(v):
    out = set()
    for s in itertools.product((1, -1), repeat=3): out.add(tuple(x * t for x, t in zip(v, s)))
    return sorted(out)
CUBE8 = signs((1, 1, 1))
SOLIDS = {
    'D': [tuple(x * PHI / 2 for x in v) for v in CUBE8 + [w for c in cyc(0, 1 / PHI, PHI) for w in signs(c)]],
    'I': [tuple(x / 2 for x in w) for c in cyc(0, 1, PHI) for w in signs(c)],
    'C': [tuple(x / 2 for x in v) for v in CUBE8],
    'T': [tuple(x / (2 * 2 ** 0.5) for x in v) for v in CUBE8 if v[0] * v[1] * v[2] > 0],
    'O': [tuple(x / 2 ** 0.5 for x in w) for c in cyc(1, 0, 0) for w in signs(c)],
}
NE = {'D': 30, 'I': 30, 'C': 12, 'T': 6, 'O': 12}
NV, NF = {'D': 20, 'I': 12, 'C': 8, 'T': 4, 'O': 6}, {'D': 12, 'I': 20, 'C': 6, 'T': 4, 'O': 8}
COL = {'D': (138, 92, 196), 'I': (58, 112, 205), 'C': (72, 142, 72), 'T': (205, 62, 40), 'O': (232, 200, 82)}   # element colours
lin = lambda c: tuple(((x / 255 + 0.055) / 1.055) ** 2.4 if x / 255 > 0.04045 else x / 255 / 12.92 for x in c)
# ------------------------------------------------------------------ scene
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
def hull_mesh(name, pts):
    """Convex hull of pts as one polygon per face (coplanar triangles dissolved)."""
    bm = bmesh.new(); [bm.verts.new(p) for p in pts]; bm.verts.ensure_lookup_table()
    bmesh.ops.convex_hull(bm, input=bm.verts[:])
    bmesh.ops.dissolve_limit(bm, angle_limit=math.radians(0.5), verts=bm.verts[:], edges=bm.edges[:])
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); return me
def checks_solid(k, me):
    vs = [v.co for v in me.vertices]; es = [(me.vertices[a].co - me.vertices[b].co).length for a, b in (e.vertices for e in me.edges)]
    X(f'{k}: {len(vs)} corners, {len(me.polygons)} faces, {len(es)} edges', len(vs) == NV[k] and len(me.polygons) == NF[k] and len(es) == NE[k])
    X(f'{k}: every mesh edge = 1 (single precision)', max(abs(e - 1) for e in es) < 1e-6, f'{min(es):.9f}..{max(es):.9f}')
    P = SOLIDS[k]; d = [math.dist(a, b) for a, b in itertools.combinations(P, 2)]   # double precision on the coordinates
    X(f'{k}: shortest corner distance = 1 exactly in doubles, attained {NE[k]} times', abs(min(d) - 1) < 1e-12 and sum(abs(x - 1) < 1e-12 for x in d) == NE[k], f'{min(d):.15f}')
# materials
def gold_mat():
    m = bpy.data.materials.new('gold'); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (1.0, 0.70, 0.28, 1); b.inputs['Metallic'].default_value = 1.0
    b.inputs['Roughness'].default_value = 0.16; return m
def crystal_mat(k):
    m = bpy.data.materials.new('crystal' + k); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    c = lin(COL[k]); tint = tuple(0.15 + 0.85 * x for x in c)
    b.inputs['Base Color'].default_value = (*tint, 1); b.inputs['Metallic'].default_value = 0.0
    b.inputs['Roughness'].default_value = 0.0; b.inputs['IOR'].default_value = 1.45; b.inputs['Transmission Weight'].default_value = 1.0
    va = nt.nodes.new('ShaderNodeVolumeAbsorption'); va.inputs['Color'].default_value = (*c, 1); va.inputs['Density'].default_value = DENS[k]
    nt.links.new(va.outputs[0], nt.nodes['Material Output'].inputs['Volume']); return m
DENS = {'D': 1.1, 'I': 1.4, 'C': 1.4, 'T': 2.2, 'O': 1.7}   # thinner stones a little denser, so all five read as deep colour
GOLD = gold_mat()
def obj(name, me, mat, smooth=False):
    o = bpy.data.objects.new(name, me); sc.collection.objects.link(o); me.materials.append(mat)
    if smooth:
        for p in me.polygons: p.use_smooth = True
    return o
# ------------------------------------------------------------------ the ring (in the x-z plane, axis y towards the viewer)
R_IN, R_OUT, HALFW, NSEG = 2.25, 2.7, 0.55, 384
def profile():
    """Rounded-rectangle band section, domed a little on the outside: points (r, y) round the section."""
    Rc, A, p = (R_IN + R_OUT) / 2, (R_OUT - R_IN) / 2, 0.3
    sg = lambda x: math.copysign(abs(x) ** p, x)
    pts = []
    for i in range(96):
        a = 2 * math.pi * i / 96; c, s_ = math.cos(a), math.sin(a)
        r = Rc + A * sg(c); y = HALFW * sg(s_)
        if c > 0: r -= 0.10 * (y / HALFW) ** 2 * c
        pts.append((r, y))
    return pts
def ring_mesh():
    pr = profile(); bm = bmesh.new(); rows = []
    for s in range(NSEG):
        th = 2 * math.pi * s / NSEG; rows.append([bm.verts.new((r * math.cos(th), y, r * math.sin(th))) for r, y in pr])
    for s in range(NSEG):
        a, b = rows[s], rows[(s + 1) % NSEG]
        for i in range(len(pr)):
            j = (i + 1) % len(pr); bm.faces.new((a[i], a[j], b[j], b[i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    me = bpy.data.meshes.new('ring'); bm.to_mesh(me); bm.free(); return me
ring = obj('ring', ring_mesh(), GOLD, smooth=True)
sub = ring.modifiers.new('sub', 'SUBSURF'); sub.levels = sub.render_levels = 1
# ------------------------------------------------------------------ stones on the upper arc, D at the left .. O at the right
ANG = {'D': 170, 'I': 130, 'C': 90, 'T': 50, 'O': 10}   # evenly, 40 degrees apart
SEAT_H = 0.16
def place(k):
    me = hull_mesh(k, SOLIDS[k]); checks_solid(k, me)
    # one face down: the face whose normal is nearest -z, turned to exactly -z, then the solid spun a little about its axis
    f = min(me.polygons, key=lambda p: p.normal.z); n = f.normal.copy()
    Rd = n.rotation_difference(Vector((0, 0, -1))).to_matrix().to_4x4()
    me.transform(Rd); me.transform(Matrix.Rotation(math.radians({'D': 18, 'I': 25, 'C': 69, 'T': 15, 'O': 20}[k]), 4, 'Z'))
    zmin = min(v.co.z for v in me.vertices); r_in = -zmin
    flat = [v for v in me.vertices if abs(v.co.z - zmin) < 1e-9]
    foot = max(Vector((v.co.x, v.co.y)).length for v in flat)   # circumradius of the bottom face
    th = math.radians(ANG[k]); radial = Vector((math.cos(th), 0, math.sin(th)))
    base = R_OUT + SEAT_H - 0.02   # the band's crown (y = 0) is at R_OUT
    centre = radial * (base + r_in)
    # local z -> radial; local y -> ring axis y
    M = Matrix(((math.sin(th), 0, math.cos(th)), (0, 1, 0), (-math.cos(th), 0, math.sin(th)))).to_4x4()
    o = obj('stone' + k, me, crystal_mat(k)); o.matrix_world = Matrix.Translation(centre) @ M
    bv = o.modifiers.new('bevel', 'BEVEL'); bv.width = 0.02; bv.segments = 2; bv.limit_method = 'ANGLE'
    # the seat: a small gold collet (truncated cone) from the band to just under the stone's bottom face, and short prongs
    bpy.ops.mesh.primitive_cone_add(vertices=64, radius1=0.30, radius2=min(foot * 0.80, 0.62), depth=SEAT_H + 0.12, location=(0, 0, 0))
    cone = bpy.context.active_object; cone.data.materials.append(GOLD)
    for p in cone.data.polygons: p.use_smooth = True
    cone.matrix_world = Matrix.Translation(radial * (base - (SEAT_H + 0.12) / 2)) @ M
    corners = [v.co.copy() for v in flat]
    for c in corners:   # one prong per corner of the bottom face, reaching a little up the stone's side
        d = Vector((c.x, c.y, 0)).normalized()
        p0 = Vector((d.x * min(foot * 0.80, 0.62), d.y * min(foot * 0.80, 0.62), zmin - 0.02)); p1 = Vector((c.x, c.y, zmin)) + d * 0.035 + Vector((0, 0, 0.12))
        mid = (p0 + p1) / 2; L = (p1 - p0).length
        bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.035, depth=L, location=(0, 0, 0))
        pr = bpy.context.active_object; pr.data.materials.append(GOLD)
        for p in pr.data.polygons: p.use_smooth = True
        R_ = Vector((0, 0, 1)).rotation_difference((p1 - p0).normalized()).to_matrix().to_4x4()
        pr.matrix_world = Matrix.Translation(centre) @ M @ Matrix.Translation(mid) @ R_
    top = (base + r_in) + max(v.co.length for v in me.vertices)
    print(f'stone {k}: inradius {r_in:.4f}, outer reach {top:.3f}, angle {ANG[k]}', flush=True)
    return centre, max(v.co.length for v in me.vertices)
placed = {k: place(k) for k in 'DICTO'}
gaps = [((placed[a][0] - placed[b][0]).length - placed[a][1] - placed[b][1]) for a, b in zip('DICT', 'ICTO')]
X('neighbouring stones clear of each other (centre distance > sum of circumradii)', min(gaps) > 0.05, [round(g, 3) for g in gaps])
# ------------------------------------------------------------------ 風 in the middle of the hoop (in the ring's plane, gold)
cu = bpy.data.curves.new('kanji', 'FONT'); cu.body = '風'
cu.font = bpy.data.fonts.load('/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc')
cu.size = 1.0; cu.extrude = 0.024; cu.bevel_depth = 0.008; cu.bevel_resolution = 3; cu.align_x = 'CENTER'; cu.align_y = 'CENTER'
kj = bpy.data.objects.new('kanji', cu); sc.collection.objects.link(kj); cu.materials.append(GOLD)
kj.rotation_euler = (math.radians(90), 0, 0)   # text plane x-y -> ring plane x-z, facing -y (the viewer)
bpy.context.view_layer.update()
bb = [kj.matrix_world @ Vector(c) for c in kj.bound_box]
KH = 2.95   # the glyph's ink height in the ring's units
sk = KH / (max(v.z for v in bb) - min(v.z for v in bb)); kj.scale = (sk, sk, sk); bpy.context.view_layer.update()
bb = [kj.matrix_world @ Vector(c) for c in kj.bound_box]
cx = sum(v.x for v in bb) / 8; cz = sum(v.z for v in bb) / 8; kj.location = (-cx, 0, -cz)
bpy.context.view_layer.update(); bb = [kj.matrix_world @ Vector(c) for c in kj.bound_box]
reach = max(math.hypot(v.x, v.z) for v in bb)
X('風 inside the hoop (every corner of its box within the inner radius)', reach < R_IN - 0.05, round(reach, 3))
# ------------------------------------------------------------------ studio: soft boxes + gradient environment; camera sees the cover ground
BOX = 2.2
w = bpy.data.worlds.new('studio'); sc.world = w
if w.node_tree is None: w.use_nodes = True
nt = w.node_tree; nd = nt.nodes
bg = nd['Background']; lp = nd.new('ShaderNodeLightPath'); mix = nd.new('ShaderNodeMixShader')
cam_bg = nd.new('ShaderNodeBackground'); cam_bg.inputs['Color'].default_value = (*lin((20, 15, 11)), 1); cam_bg.inputs['Strength'].default_value = 1
tc = nd.new('ShaderNodeTexCoord'); sep = nd.new('ShaderNodeSeparateXYZ'); ramp = nd.new('ShaderNodeValToRGB')
nt.links.new(tc.outputs['Generated'], sep.inputs[0])   # world: the ray direction
ma = nd.new('ShaderNodeMath'); ma.operation = 'MULTIPLY_ADD'; ma.inputs[1].default_value = 0.5; ma.inputs[2].default_value = 0.5
nt.links.new(sep.outputs['Z'], ma.inputs[0]); nt.links.new(ma.outputs[0], ramp.inputs[0])
ramp.color_ramp.elements[0].position = 0.0; ramp.color_ramp.elements[0].color = (0.02, 0.018, 0.016, 1)
ramp.color_ramp.elements[1].position = 0.80; ramp.color_ramp.elements[1].color = (0.30, 0.29, 0.28, 1)
e = ramp.color_ramp.elements.new(0.45); e.color = (0.10, 0.09, 0.08, 1)
e = ramp.color_ramp.elements.new(0.53); e.color = (0.70, 0.64, 0.56, 1)
nt.links.new(ramp.outputs['Color'], bg.inputs['Color']); bg.inputs['Strength'].default_value = 0.9
# light box: rays that have passed into a crystal see a bright warm-white surround (a jeweller's light box), so the stones glow in
# their own colour, deeper where the path through them is longer; reflections (gold, crystal surfaces) see the darker studio.
box = nd.new('ShaderNodeBackground'); box.inputs['Strength'].default_value = BOX
ramp2 = nd.new('ShaderNodeValToRGB'); nt.links.new(ma.outputs[0], ramp2.inputs[0])
ramp2.color_ramp.elements[0].color = (0.35, 0.33, 0.30, 1); ramp2.color_ramp.elements[1].color = (1.0, 0.98, 0.95, 1)
wav = nd.new('ShaderNodeTexWave'); wav.wave_type = 'BANDS'; wav.bands_direction = 'DIAGONAL'; wav.inputs['Scale'].default_value = 1.1
wav.inputs['Distortion'].default_value = 2.0; wav.inputs['Detail'].default_value = 0.0
nt.links.new(tc.outputs['Generated'], wav.inputs['Vector'])   # light and dark panels in the box, so each back facet seen through
wr = nd.new('ShaderNodeValToRGB'); nt.links.new(wav.outputs['Fac'], wr.inputs[0])   # the crystal takes its own brightness
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
def softbox(name, loc, size, power, sx=None):
    L = bpy.data.lights.new(name, 'AREA'); L.shape = 'RECTANGLE'; L.size = size; L.size_y = sx or size; L.energy = power
    o = bpy.data.objects.new(name, L); sc.collection.objects.link(o); o.location = loc
    d = Vector((0, 0, 0)) - Vector(loc); o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler(); return o
softbox('key', (-9, -11, 12), 7, 5200, 3)
softbox('rim', (10, 7, 6), 6, 3200, 2.5)
softbox('fill', (6, -14, -3), 8, 1400, 4)
softbox('top', (0, 2, 16), 10, 2200, 2)
softbox('back', (-6, 14, 10), 9, 4500, 5)   # behind the stones: light through the crystal
# camera: three-quarter view, long lens
cam = bpy.data.cameras.new('cam'); cam.lens = 105; cam.sensor_width = 36
co = bpy.data.objects.new('cam', cam); sc.collection.objects.link(co); sc.camera = co
AZ, EL, DIST = math.radians(24), math.radians(14), 29.0
target = Vector((-0.4, 0, 0.85))
co.location = target + DIST * Vector((math.sin(AZ) * math.cos(EL), -math.cos(AZ) * math.cos(EL), math.sin(EL)))
co.rotation_euler = (target - co.location).to_track_quat('-Z', 'Y').to_euler()
cam.sensor_fit = 'HORIZONTAL'
# render
sc.render.engine = 'CYCLES'; cy = sc.cycles; cy.device = 'CPU'; cy.samples = SAMPLES; cy.use_denoising = True
cy.max_bounces = 32; cy.glossy_bounces = 16; cy.transmission_bounces = 24; cy.transparent_max_bounces = 16; cy.volume_bounces = 2
cy.diffuse_bounces = 2; cy.caustics_reflective = False; cy.caustics_refractive = False; cy.blur_glossy = 0.5
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = RW, RH, 100
sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'; sc.view_settings.exposure = 0.0
sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGB'; sc.render.filepath = OUT
sc.render.threads_mode = 'AUTO'
print('PROGRESS 0.10 scene built', flush=True)
if FAIL: print('FINAL FAIL: ' + '; '.join(FAIL)); sys.exit(1)
bpy.ops.render.render(write_still=True)
print('PROGRESS 0.80 rendered', OUT, flush=True)
