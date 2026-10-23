# Golden split in the Lotus Jewel network: AXE coned at t (default 1/φ), pyramids to the Jewel side (on icosahedron faces) and to the
# dodecahedron side (on Unborn faces, which are dodecahedron faces). Big keyed piece = Lotus Jewel + 12 pyramids (= big truncated
# octahedron minus 8 Tricaps), small keyed piece = dodecahedron + 12 pyramids (= small truncated octahedron + 8 Tricaps).
import numpy as np, itertools, json, sys
exec(open('axesplit2.py').read().split('T=1/phi')[0])
exec(open('fuse3.py').read().split('VOL={')[0].split("exec(open('fuse1.py')")[0])
src1=open('fuse1.py').read().split('def pieces')[0]; exec(src1)
J=json.load(open('/home/dicto/k-mix/studies/2026-10-10-icosa-networks-3/data/clawed-icosahedron-unit.json')); JV=np.array(J['vertices']); JVOL=J['volume']
VD=ConvexHull(D).volume; VT=sum(ConvexHull(t).volume for t in TR)
print('Jewel %.6f (√5 − ... check: ico − 8 Tricaps = %.6f)  dodeca %.6f  8 Tricaps %.6f'%(JVOL,vol(ico)-VT,VD,VT))
for t in ([float(x) for x in sys.argv[1:]] or [1/phi]):
    Pi,_=piece(t,ico,np.zeros(3)); Pu,_=piece(t,H-uc,uc)
    pyr_i=sum(abs(np.linalg.det(Q[:3]-Q[3]))/6 for Q in Pi[1:]); pyr_u=sum(abs(np.linalg.det(Q[:3]-Q[3]))/6 for Q in Pu[1:])
    big=JVOL+pyr_i; small=VD+pyr_u
    hb=vol(np.vstack([JV]+Pi[1:])); hs=vol(np.vstack([D]+Pu[1:]))
    print('t=%.4f  big keyed (Jewel+12): vol %.6f fill of hull %.2f%%  |  small keyed (dodeca+12): vol %.6f fill of hull %.2f%%  | sum %.6f (φ³ %.6f)'%(t,big,100*big/hb,small,100*small/hs,big+small,phi**3))
