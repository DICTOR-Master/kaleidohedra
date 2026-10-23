# Special positions in the octet family (DICTO 10-23: find special positions first, then name).
import numpy as np, itertools
exec(open('octet1.py').read().split('ts=[')[0])
def edges(V):
    h=ConvexHull(V); N=[]
    for e in h.equations:
        if not any(np.dot(e[:3],q[:3])>1-1e-7 for q in N): N.append(e)
    E=set()
    for a,b in itertools.combinations(range(len(V)),2):
        if sum(1 for q in N if abs(V[a]@q[:3]+q[3])<1e-7 and abs(V[b]@q[:3]+q[3])<1e-7)>=2: E.add(round(float(np.linalg.norm(V[a]-V[b])),6))
    return sorted(E)
sp={'equilateral rhombic-dodecahedron piece  t = 1/(3+2√6)':1/(3+2*6**.5),
    'equilateral cube piece                  t = 1 − 2(√2−1)/3':1-2*(2**.5-1)/3,
    'equal piece volumes (Delian a = 1/∛2)    t = 1 − (2/3)·2^(−1/3)':1-(2/3)*2**(-1/3),
    'tetrahedra and octahedra fill half each  t = 1 − (2/3)(3/4)^(1/3)':1-(2/3)*(3/4)**(1/3)}
for name,t in sp.items():
    A=cell('T',Tc[0],t); B=cell('O',O[0],t)
    print('%s = %.6f'%(name,t))
    for k,V in (('tetra piece',A),('octa piece',B)):
        n,f,fk,vol=describe(V); print('    %-11s %2d corners, faces %s, volume %.6f, edge lengths %s'%(k,n,fk,vol,edges(V)))
