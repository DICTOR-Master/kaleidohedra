import numpy as np, time, sys
SIGN=float(sys.argv[1]) if len(sys.argv)>1 else -1.0  # -1: lattice y = -(z x x) maps A-B-C onto the cubic orientation used below (checked: +1 gives the twin)
from mech import *
# frame element rigid-body check
kl=frame_local(1,AREA,I2,I2,GS,J); n=np.array([0.3,0.5,0.81]); n/=np.linalg.norm(n); T=np.kron(np.eye(4),rot(n)); K=T.T@kl@T
w=np.array([0.2,-0.4,0.7]); x=n; q=np.concatenate([np.zeros(3),w,np.cross(w,x),w]); print('rigid rotation residual',np.abs(K@q).max())
t=time.time(); lat=build(PERIODIC_WORDS['3C'],zper=True); M=Model(lat,'pin','full',VOIGT); C=periodic_C(M); print('rho',M.rho,'theory',6*np.sqrt(2)*np.pi*R**2, time.time()-t)
# rotate to cubic axes: stacking axis z = [111]; in-sheet x along a nearest-neighbour bond = [1-10]/sqrt2
ex=np.array([1,-1,0])/np.sqrt(2); ez=np.array([1,1,1])/np.sqrt(3); ey=np.cross(ez,ex)*SIGN; Q=np.array([ex,ey,ez]) # rows: lattice axes in cubic coords
def voigt_to_tensor(C):
    idx=[(0,0),(1,1),(2,2),(1,2),(0,2),(0,1)]; T=np.zeros((3,3,3,3))
    for I,(i,j) in enumerate(idx):
        for Jn,(k,l) in enumerate(idx):
            for a,b in {(i,j),(j,i)}:
                for c,d in {(k,l),(l,k)}: T[a,b,c,d]=C[I,Jn]
    return T
Tt=voigt_to_tensor(C); Tc=np.einsum('ia,jb,kc,ld,ijkl->abcd',Q,Q,Q,Q,Tt)
C11,C12,C44=Tc[0,0,0,0],Tc[0,0,1,1],Tc[1,2,1,2]; E100=(C11-C12)*(C11+2*C12)/(C11+C12)
print('cubic C11 C12 C44',C11,C12,C44,'E100',E100,'rho/9',M.rho/9,'ratio',E100/(M.rho/9))
print(engineering(C))
