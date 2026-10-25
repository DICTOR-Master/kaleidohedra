# Atom onions: Blender (Cycles, CPU) render of the scenes written by geom.py. Run headless:
#   blender -b -P blender_render.py -- <scene.json> <out.png> <proj.json> [px]
# Translucent shells (Principled BSDF alpha), opaque pastel cut bands, rings/edges as tubes; orthographic camera along the scene's
# cam_dir; transparent film (compose.py lays it on white). proj.json: the label anchors projected to pixel coordinates.
import bpy, json, sys, math
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
argv = sys.argv[sys.argv.index("--") + 1:]
scene_path, out_png, proj_path = argv[:3]; PX = int(argv[3]) if len(argv) > 3 else 1500
S = json.load(open(scene_path))
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 160; sc.cycles.use_denoising = True
sc.cycles.max_bounces = 64; sc.cycles.transparent_max_bounces = 128; sc.cycles.transmission_bounces = 8
sc.render.threads_mode = "FIXED"; sc.render.threads = 16
sc.render.resolution_x = sc.render.resolution_y = PX; sc.render.film_transparent = True
sc.view_settings.view_transform = "Standard"; sc.view_settings.look = "None"
world = bpy.data.worlds.new("w"); sc.world = world; world.use_nodes = True
bg = world.node_tree.nodes["Background"]; bg.inputs[0].default_value = (1, 1, 1, 1); bg.inputs[1].default_value = 0.75

mats = {}
def material(col, alpha, rough, emit=0.0):
    key = (tuple(round(c, 4) for c in col), round(alpha, 3), rough, emit)
    if key in mats: return mats[key]
    m = bpy.data.materials.new("m%d" % len(mats)); m.use_nodes = True
    p = m.node_tree.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = (*col, 1); p.inputs["Alpha"].default_value = alpha; p.inputs["Roughness"].default_value = rough
    if emit:  # flat colour (cut bands): emission only, so the band shows its exact colour
        p.inputs["Base Color"].default_value = (0, 0, 0, 1) if emit >= 1 else (*col, 1)
        p.inputs["Emission Color"].default_value = (*col, 1); p.inputs["Emission Strength"].default_value = emit
    mats[key] = m; return m

for o in S["objs"]:
    if o["type"] == "mesh":
        me = bpy.data.meshes.new(o["name"]); me.from_pydata(o["V"], [], o["F"]); me.validate(); me.update()
        ob = bpy.data.objects.new(o["name"], me); sc.collection.objects.link(ob)
        emit = 1.0 if o["kind"] == "band" else 0.0
        ob.data.materials.append(material(o["col"], o["alpha"], o["rough"], emit))
        for poly in me.polygons: poly.use_smooth = False
    elif o["type"] == "tubes":
        cu = bpy.data.curves.new(o["name"], "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = o["r"]; cu.bevel_resolution = 3; cu.use_fill_caps = True
        for line in o["lines"]:
            sp = cu.splines.new("POLY"); sp.points.add(len(line) - 1)
            for k, p in enumerate(line): sp.points[k].co = (*p, 1)
        ob = bpy.data.objects.new(o["name"], cu); sc.collection.objects.link(ob)
        ob.data.materials.append(material(o["col"], 1.0, 0.45, 0.15))
    elif o["type"] == "sphere":
        bpy.ops.mesh.primitive_uv_sphere_add(radius=o["r"], location=o["c"], segments=32, ring_count=16)
        ob = bpy.context.active_object; ob.data.materials.append(material(o["col"], 1.0, 0.4))
        bpy.ops.object.shade_smooth()

tgt = Vector(S["target"]); d = Vector(S["cam_dir"]).normalized(); size = S["size"]
cam_data = bpy.data.cameras.new("cam"); cam_data.type = "ORTHO"; cam_data.ortho_scale = size * float(S.get("zoom", 2.55))
cam = bpy.data.objects.new("cam", cam_data); sc.collection.objects.link(cam); sc.camera = cam
cam.location = tgt + d * size * 10; cam_data.clip_end = size * 40
cam.rotation_euler = (tgt - cam.location).to_track_quat("-Z", "Y").to_euler()
for name, dirv, en, ang in [("key", (-0.4, 0.3, 1.0), 2.6, 0.35), ("fill", (1.0, -0.6, 0.3), 0.9, 0.6)]:
    L = bpy.data.lights.new(name, "SUN"); L.energy = en; L.angle = ang
    ob = bpy.data.objects.new(name, L); sc.collection.objects.link(ob)
    ob.rotation_euler = Vector(dirv).normalized().to_track_quat("Z", "Y").to_euler()
bpy.context.view_layer.update()
proj = []
for a in S["anchors"]:
    v = world_to_camera_view(sc, cam, Vector(a["p"]))
    proj.append({"key": a["key"], "x": v.x * PX, "y": (1 - v.y) * PX})
json.dump({"px": PX, "anchors": proj, "centre": [(lambda v: [v.x * PX, (1 - v.y) * PX])(world_to_camera_view(sc, cam, tgt))]}, open(proj_path, "w"))
sc.render.filepath = out_png; bpy.ops.render.render(write_still=True)
