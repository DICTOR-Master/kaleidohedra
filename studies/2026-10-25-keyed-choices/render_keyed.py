# Blender render of the two valid keyed pairs (DICTO 2026-10-25): Samson + Delilah (A), Goliath + David (B); each piece shown whole
# and cut in half (so the sockets show), gold big piece, blue small piece. Run: blender -b -P render_keyed.py
import bpy, bmesh, math, os
from mathutils import Vector
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene; sc.render.engine='CYCLES'; sc.cycles.samples=64; sc.render.resolution_x=2400; sc.render.resolution_y=1300
sc.world=bpy.data.worlds.new('w'); sc.world.use_nodes=True; sc.world.node_tree.nodes['Background'].inputs[0].default_value=(0.06,0.07,0.09,1)
def mat(name,col):
    m=bpy.data.materials.new(name); m.use_nodes=True; b=m.node_tree.nodes['Principled BSDF']; b.inputs['Base Color'].default_value=(*col,1); b.inputs['Roughness'].default_value=0.45; return m
gold=mat('gold',(0.85,0.62,0.22)); blue=mat('blue',(0.30,0.45,0.85))
def load(fn,loc,m,cut=False,scale=1.0):
    bpy.ops.wm.obj_import(filepath=os.path.abspath(fn)); o=bpy.context.selected_objects[0]
    o.data.materials.append(m); o.location=loc; o.scale=(scale,)*3
    if cut:
        bpy.context.view_layer.objects.active=o; bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.bisect(plane_co=o.matrix_world.inverted()@Vector(loc)+Vector((0,0,0)),plane_no=(0,1,0),clear_outer=True,use_fill=True)
        bpy.ops.object.mode_set(mode='OBJECT')
    return o
row=[('Samson',gold,2.2),('Delilah',blue,2.2),('Goliath',gold,1.25),('David',blue,1.25)]
x=-6.6
for lab,m,s in row:
    for fn,z in ((f'keyed-{lab}.obj',1.9),(f'keyed-{lab}-half.obj',-1.9)):
        if os.path.exists(fn):
            bpy.ops.wm.obj_import(filepath=os.path.abspath(fn)); o=bpy.context.selected_objects[0]
            o.data.materials.clear(); o.data.materials.append(m); o.scale=(s,)*3; o.location=(x,0,z)
            # whole: three-quarter view; half: the cut face (plane y = centre, kept side y < centre) turned toward the camera, tilted 25°
            o.rotation_euler=(math.radians(-25), 0, math.radians(20)) if fn.endswith('half.obj') else (math.radians(-60), 0, math.radians(25))
            if fn.endswith('half.obj'):
                cutm=mat('cut_'+lab,tuple(min(1,c*1.35+0.12) for c in m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value[:3]))
                o.data.materials.append(cutm); me=o.data
                for p in me.polygons:
                    if abs(p.normal.y-1)<1e-3 or abs(p.normal.y+1)<1e-3: p.material_index=1
    nm=bpy.data.curves.new('n'+lab,'FONT'); nm.body='DICTO '+lab+'-K'; nm.align_x='CENTER'; no=bpy.data.objects.new('n'+lab,nm); sc.collection.objects.link(no)
    no.location=(x,-2,-4.3); no.rotation_euler=(math.radians(84),0,0); no.scale=(0.42,)*3; no.data.materials.append(mat('lab'+lab,(0.92,0.92,0.95)))
    x+=4.4
cam=bpy.data.objects.new('cam',bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); cam.location=(0,-19.5,1.2); cam.rotation_euler=(math.radians(84),0,0); sc.camera=cam; cam.data.lens=40
for loc,e in (((-10,-12,14),900),((12,-10,8),500),((0,10,10),300)):
    l=bpy.data.objects.new('l',bpy.data.lights.new('l','AREA')); l.data.energy=e; l.data.size=8; l.location=loc; sc.collection.objects.link(l)
    l.rotation_euler=(Vector((0,0,0))-Vector(loc)).to_track_quat('-Z','Y').to_euler()
t=bpy.data.curves.new('t','FONT'); t.body='DICTO'; to=bpy.data.objects.new('t',t); sc.collection.objects.link(to); to.location=(7.2,-3,-5.2); to.rotation_euler=(math.radians(84),0,0); to.scale=(0.38,)*3; to.data.materials.append(mat('mark',(0.72,0.59,0.18)))
sc.render.filepath=os.path.abspath('keyed-pairs.png'); bpy.ops.render.render(write_still=True)
