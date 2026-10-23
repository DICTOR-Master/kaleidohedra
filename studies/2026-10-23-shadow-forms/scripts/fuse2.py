# Shadow forms, step 2: clusters round one piece: Unborn + every AXE that shares a face with it; icosahedron + its AXE; Unborn + k Tricaps.
exec(open('fuse1.py').read().split('import sys')[0])
P=pieces('four'); Pi=pieces('icoUnborn')
U=H.copy()
ax_U=[V for n,V in P if n=='AXE' and share_face(U,V)]
for k in range(len(ax_U)+1) if False else [len(ax_U)]:
    M=np.vstack([U]+ax_U); hv=ConvexHull(M).volume; s=ConvexHull(U).volume+len(ax_U)/12
    print('Unborn + %d AXE sharing a face: hull %.6f sum %.6f convex %s'%(len(ax_U),hv,s,abs(hv-s)<1e-7), sig(M) if abs(hv-s)<1e-7 else '')
I0=ico.copy(); ax_I=[V for n,V in Pi if n=='AXE' and share_face(I0,V)]
M=np.vstack([I0]+ax_I); hv=ConvexHull(M).volume; s=ConvexHull(I0).volume+len(ax_I)/12
print('icosahedron + %d AXE sharing a face: hull %.6f sum %.6f convex %s'%(len(ax_I),hv,s,abs(hv-s)<1e-7), sig(M) if abs(hv-s)<1e-7 else '')
# AXE between: how many pieces each AXE touches, by kind
V0=list(axes.values())[0]
print('one AXE touches:', sorted(n for n,V in Pi if n!='AXE' and share_face(V0,V)), '| in the four-kind network:', sorted(n for n,V in P if not (V.shape==V0.shape and np.allclose(V,V0)) and share_face(V0,V)))
for k in range(1,9):
    M=np.vstack([U]+TR[:k]); hv=ConvexHull(M).volume; s=ConvexHull(U).volume+k*(3-5**.5)/24
    print('Unborn + %d Tricaps (first %d corners): convex %s'%(k,k,abs(hv-s)<1e-7))
