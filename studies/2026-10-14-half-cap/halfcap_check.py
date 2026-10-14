# DICTO half-cap study 2026-10-14 (credit: DICTO). Numeric checks for octahedron = 20 Cleo-Icos + 12 half caps,
# dihedral angles, volumes, Dehn-invariant bookkeeping. DICTO · dictospheres.com
import numpy as np, itertools, json, mpmath as mp
phi=(1+5**.5)/2
V=[]
for s1 in(1,-1):
  for s2 in(1,-1):
    V+= [(0,s1/2,s2*phi/2),(s1/2,s2*phi/2,0),(s2*phi/2,0,s1/2)]
V=np.array(V,float)
E=[(i,j) for i,j in itertools.combinations(range(12),2) if abs(np.linalg.norm(V[i]-V[j])-1)<1e-9]
F=[t for t in itertools.combinations(range(12),3) if all(abs(np.linalg.norm(V[a]-V[b])-1)<1e-9 for a,b in itertools.combinations(t,2))]
assert len(E)==30 and len(F)==20
a=phi**2/2; O=np.zeros(3)
cleos=[np.array([O,V[i],V[j],V[k]]) for i,j,k in F]
halves=[]
for ax in range(3):
  for sg in(1,-1):
    T=np.zeros(3);T[ax]=sg*a
    near=[i for i in range(12) if abs(np.linalg.norm(V[i]-T)-2**-.5)<1e-9]  # A,B
    assert len(near)==2; A,B=V[near[0]],V[near[1]]
    CD=[i for i in range(12) if i not in near and abs(np.linalg.norm(V[i]-A)-1)<1e-9 and abs(np.linalg.norm(V[i]-B)-1)<1e-9]
    assert len(CD)==2
    for c in CD: halves.append(np.array([A,B,T,V[c]]))
def vol(t): return abs(np.linalg.det(t[1:]-t[0]))/6
def dih(t,i,j):
  k,l=[m for m in range(4) if m not in(i,j)]; e=t[j]-t[i]; e/=np.linalg.norm(e)
  u=t[k]-t[i]; u-=u.dot(e)*e; w=t[l]-t[i]; w-=w.dot(e)*e
  return np.degrees(np.arccos(u.dot(w)/np.linalg.norm(u)/np.linalg.norm(w)))
H=halves[0]; names='ABTC'
hd={names[i]+names[j]:(round(np.linalg.norm(H[i]-H[j]),6),round(dih(H,i,j),4)) for i,j in itertools.combinations(range(4),2)}
# point-membership test: every sample point of the octahedron lies in exactly one piece
def bary_in(t,P):
  M=np.c_[(t[1:]-t[0]).T]; L=np.linalg.solve(M,(P-t[0]).T).T; L=np.c_[1-L.sum(1),L]; return (L>-1e-12).all(1)
rng=np.random.default_rng(1); P=rng.uniform(-a,a,(400000,3)); P=P[np.abs(P).sum(1)<a]
cnt=sum(bary_in(t,P).astype(int) for t in cleos+halves)
th=np.arccos(-5**.5/3); al=np.arccos(3**-.5)
mp.mp.dps=60
rel=mp.pslq([mp.pi,mp.acos(-mp.sqrt(5)/3),mp.acos(1/mp.sqrt(3))],maxcoeff=10**6,maxsteps=10**6)
out=dict(n_cleo=len(cleos),n_half=len(halves),vol_cleo=vol(cleos[0]),phi2_24=phi**2/24,vol_half=vol(H),phi_24=phi/24,
 vol_sum=sum(map(vol,cleos+halves)),vol_oct=4/3*a**3,all_half_vols_equal=bool(np.ptp([vol(h) for h in halves])<1e-12),
 half_cap_edges_len_dihedral=hd,theta_I_deg=np.degrees(th),alpha_deg=np.degrees(al),
 checks_deg=dict(AB_eq_180_minus_thI_over2=180-np.degrees(th)/2,AC_eq_180_minus_thI=180-np.degrees(th),TC_eq_2alpha=2*np.degrees(al)),
 samples=int(len(P)),covered_exactly_once=int((cnt==1).sum()),uncovered=int((cnt==0).sum()),overlap=int((cnt>1).sum()),
 octet_tet_volume=(phi**2/2**.5)**3/(6*2**.5),five_cleo_three_half=5*phi**2/24+3*phi/24,
 pslq_pi_thetaI_alpha_maxcoeff_1e6=str(rel))
print(json.dumps(out,indent=1)); json.dump(out,open(__file__.replace('.py','.json'),'w'),indent=1)
