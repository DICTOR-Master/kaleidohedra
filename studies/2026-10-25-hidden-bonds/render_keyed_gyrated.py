# Blender render of the two valid keyed pairs (DICTO 2026-10-25): the gyrated pair keyed three ways (hidden-bonds study); each piece shown whole
# and cut in half (so the sockets show), gold tetrahedral-hole piece, blue octahedral-hole piece. Run: blender -b -P render_keyed.py
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
cols=[('TOA','tet',gold,'1  tet piece'),('TOA','oct',blue,'1  oct piece'),('TOB','tet',gold,'2  tet piece'),('TOB','oct',blue,'2  oct piece'),('OTA','tet',gold,'3  tet piece'),('OTA','oct',blue,'3  oct piece')]
x=-9.0; S=2.3
for tag,nm,m,lab in cols:
    for fn,z in ((f'kg-{tag}-{nm}.obj',1.9),(f'kg-{tag}-{nm}-half.obj',-1.9)):
        bpy.ops.wm.obj_import(filepath=os.path.abspath(fn)); o=bpy.context.selected_objects[0]
        o.data.materials.clear(); o.data.materials.append(m); o.scale=(S,)*3; o.location=(x,0,z)
        o.rotation_euler=(math.radians(-25),0,math.radians(20)) if fn.endswith('half.obj') else (math.radians(-60),0,math.radians(25))
        if fn.endswith('half.obj'):
            cutm=mat('cut_'+tag+nm,tuple(min(1,c*1.35+0.12) for c in m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value[:3]))
            o.data.materials.append(cutm)
            for p in o.data.polygons:
                if abs(p.normal.y-1)<1e-3 or abs(p.normal.y+1)<1e-3: p.material_index=1
    t=bpy.data.curves.new('n'+tag+nm,'FONT'); t.body=lab; t.align_x='CENTER'; no=bpy.data.objects.new('n'+tag+nm,t); sc.collection.objects.link(no)
    no.location=(x,-2,-4.3); no.rotation_euler=(math.radians(84),0,0); no.scale=(0.36,)*3; no.data.materials.append(mat('lab'+tag+nm,(0.92,0.92,0.95)))
    x+=3.6
sc.render.resolution_x=2700
cam=bpy.data.objects.new('cam',bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); cam.location=(0,-25.5,0.6); cam.rotation_euler=(math.radians(84),0,0); sc.camera=cam; cam.data.lens=40
for loc,e in (((-10,-12,14),900),((12,-10,8),500),((0,10,10),300)):
    l=bpy.data.objects.new('l',bpy.data.lights.new('l','AREA')); l.data.energy=e; l.data.size=8; l.location=loc; sc.collection.objects.link(l)
    l.rotation_euler=(Vector((0,0,0))-Vector(loc)).to_track_quat('-Z','Y').to_euler()
t=bpy.data.curves.new('t','FONT'); t.body='DICTO'; to=bpy.data.objects.new('t',t); sc.collection.objects.link(to); to.location=(8.4,-3,-4.9); to.rotation_euler=(math.radians(84),0,0); to.scale=(0.38,)*3; to.data.materials.append(mat('mark',(0.72,0.59,0.18)))
sc.render.filepath=os.path.abspath('keyed-gyrated.png'); bpy.ops.render.render(write_still=True)
