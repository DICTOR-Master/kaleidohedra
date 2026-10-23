# Pictures: the keyed golden pair of the Lotus Jewel network (Jewel + AXE pyramids = big truncated octahedron with 8 dents;
# dodecahedron + AXE pyramids = small truncated octahedron with 8 Tricap keys), and the two fitted together.
import os
exec(open('axesplit4.py').read().split('R1,R2=')[0])
exec(open('jewelsplit1.py').read().split('VD=ConvexHull')[0].split("exec(open('axesplit2.py')")[1].split('\n',1)[1])
COL.update({'dodecahedron':(230,180,60)})
T=1/phi; R1,R2=rot(0.6,0.45),rot(0.6+np.pi,-0.45)
Pi,_=piece(T,ico,np.zeros(3)); Pu,_=piece(T,H-uc,uc)
big=[{'name':'Lotus Jewel','V':JV}]+[{'name':'pyr','V':Q} for Q in Pi[1:]]
small=[{'name':'dodecahedron','V':D}]+[{'name':'pyr','V':Q} for Q in Pu[1:]]
sheet('Lotus Jewel network, golden split: big keyed piece','Lotus Jewel + 12 AXE pyramids (t = 1/φ) = big truncated octahedron with 8 Tricap-shaped dents · volume √5 exactly',
      [(big,R1,'Lotus Jewel (core) + AXE pyramids'),(big,R2,'other side'),(big,rot(np.pi/4,np.arctan(1/2**.5)),'looking into a dent (3-fold axis)')],
      [('Lotus Jewel','Lotus Jewel'),('pyr','AXE pyramids')],'04-keyed-big-Jewel.png')
sheet('Lotus Jewel network, golden split: small keyed piece','dodecahedron + 12 AXE pyramids (t = 1/φ) = small truncated octahedron with 8 Tricap keys · volume 2 exactly',
      [(small,R1,'dodecahedron (core) + AXE pyramids'),(small,R2,'other side'),(small,rot(np.pi/4,np.arctan(1/2**.5)),'a key on the 3-fold axis')],
      [('dodecahedron','dodecahedron'),('pyr','AXE pyramids')],'05-keyed-small-dodecahedron.png')
pair=[{'name':'big','V':P['V']} for P in big]+[{'name':'small','V':P['V']} for P in small]
sheet('Lotus Jewel network, golden split: the keyed pair','each Tricap key of a small piece sits in a dent of a big one · √5 + 2 = φ³ per cell · every Tricap may go either way (mixed keys also fill)',
      [(pair,rot(0.3,0.3),'big + small, key in dent'),(pair,rot(2.2,0.2),'other side'),(pair,rot(np.pi/4,np.arctan(1/2**.5)),'along the key axis')],
      [('big','big keyed (√5)'),('small','small keyed (2)')],'06-keyed-pair.png')
print(sorted(os.listdir(OUT)))
