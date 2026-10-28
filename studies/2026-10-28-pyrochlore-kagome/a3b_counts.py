# Step C (DICTO 10-28): kagome magnets Mn3X are ordered A3B close-packed layers (A on a kagome net in each layer, B on the 2x2
# sublattice), the same layers as AX3 in hexagonal perovskites. Stacking: L1_2 = 3C (Mn3Ir, Mn3Pt), D0_19 = 2H (Mn3Sn, Mn3Ge),
# D0_24 = 4H (TiNi3 type), 9R, 6H. Exact counts per A atom from coordinates, for any stacking:
#  - A neighbours and B neighbours (nearest);  - A-A-A nearest-neighbour triangles, split into basal (in the layer) and tilted;
#  - tilted kagome planes: A atoms whose tilted triangles share corners only (kagome) - counted as triangles in tilted planes.
import itertools, numpy as np
a1=np.array([1,0,0.]); a2=np.array([.5,3**.5/2,0]); SH={'A':0,'B':1,'C':2}; N=4; dz=np.sqrt(2/3)
def layer(letter,off,k):
    return [(i*a1+j*a2+SH[letter]*(a1+a2)/3+np.array([0,0,k*dz]),'B' if (i%2,j%2)==off else 'A') for i in range(N) for j in range(N)]
def wrap(d,cell):
    f=d@np.linalg.inv(cell); f-=np.round(f); return f@cell
def analyse(seq):
    seq=seq*(-(-6//len(seq))); n=len(seq); cell=np.array([a1*N,a2*N,[0,0,n*dz]]); O=[(0,0),(1,0),(0,1),(1,1)]
    def ok(at):      # no B-B nearest neighbours
        P=np.array([p for p,_ in at]); T=[t for _,t in at]
        D=np.linalg.norm(wrap(P[:,None]-P[None],cell),axis=2)
        return all(not(T[i]=='B' and T[j]=='B' and abs(D[i,j]-1)<1e-6) for i in range(len(T)) for j in range(i+1,len(T))),P,T,D
    def dfs(offs):
        if len(offs)==n:
            g,P,T,D=ok([x for k in range(n) for x in layer(seq[k],offs[k],k)]); return (P,T,D) if g else None
        for o in O:
            at=[x for k in range(len(offs)+1) for x in layer(seq[k],(offs+[o])[k],k)]
            # partial check only between consecutive layers
            g=ok(at)[0] if len(offs)+1<n else True
            if g:
                r=dfs(offs+[o])
                if r: return r
    P,T,D=dfs([(0,0)])
    A=[i for i in range(len(T)) if T[i]=='A']; nn=lambda i:[j for j in range(len(T)) if abs(D[i,j]-1)<1e-6]
    nA=np.mean([sum(T[j]=='A' for j in nn(i)) for i in A]); nB=np.mean([sum(T[j]=='B' for j in nn(i)) for i in A])
    # bow-ties: two coplanar A3 triangles sharing only atom i (kagome), by plane orientation (basal or tilted)
    bow_b=bow_t=0
    for i in A:
        tris=[]
        for j,k in itertools.combinations([x for x in nn(i) if T[x]=='A'],2):
            if abs(D[j,k]-1)<1e-6:
                u,v=wrap(P[j]-P[i],cell),wrap(P[k]-P[i],cell); nrm=np.cross(u,v); nrm/=np.linalg.norm(nrm); tris.append((nrm,{j,k}))
        for (n1,s1),(n2,s2) in itertools.combinations(tris,2):
            if not(s1&s2) and abs(abs(n1@n2)-1)<1e-6:
                if abs(abs(n1[2])-1)<1e-6: bow_b+=1
                else: bow_t+=1
    # holes: tetrahedra and octahedra of nearest neighbours, by composition; all-A octahedra per A atom
    allP=range(len(T)); oct6=0; tetA4=0
    for i in A:
        for j,k,l in itertools.combinations(nn(i),3):
            if abs(D[j,k]-1)<1e-6 and abs(D[j,l]-1)<1e-6 and abs(D[k,l]-1)<1e-6 and i<min(j,k,l) and all(T[x]=='A' for x in (j,k,l)): tetA4+=1
    # octahedra: centre = midpoint of an opposite pair at distance sqrt2 with 4 common neighbours
    seen=set()
    for i in range(len(T)):
        for j in range(len(T)):
            if j>i and abs(D[i,j]-np.sqrt(2))<1e-6:
                c=set(nn(i))&set(nn(j))
                if len(c)==4:
                    key=frozenset(c|{i,j})
                    if key not in seen:
                        seen.add(key); oct6+= all(T[x]=='A' for x in key)
    h=sum(seq[i-1]==seq[(i+1)%n] for i in range(n))/n
    return h,bow_b/len(A),bow_t/len(A),tetA4/len(A),oct6/len(A)
for name,seq in [('3C  L1_2  (Mn3Ir, Mn3Pt)','ABC'),('2H  D0_19 (Mn3Sn, Mn3Ge)','AB'),('4H  D0_24 (TiNi3 type)','ABAC'),('6H','ABCACB'),('9R','ABABCBCAC')]:
    h,bb,bt,t4,o6=analyse(seq)
    print(f'{name:26s} h = {h:.3f}  per A atom: kagome bow-ties basal {bb:.3f}, tilted {bt:.3f} (1-h = {1-h:.3f});  all-A tetrahedra {t4:.3f};  all-A octahedra {o6:.3f}')
