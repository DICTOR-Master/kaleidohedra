# Exact check (Q(sqrt5), fractions) of the data of part U: the 30 two-fold directions of the icosahedral group,
# their Gram table, and the two golden rhombohedra as parallelepipeds on three five-fold axes.
exec(open('q5.py').read())
g=Q(-1,1); G=Q(1,1); two=Q(2); z=Q(0); phi=Q(Fr(1,2),Fr(1,2))
N=[[Q(4),z,z],[Q(-4),z,z],[z,Q(4),z],[z,Q(-4),z],[z,z,Q(4)],[z,z,Q(-4)]]
base=[g,G,two]
for c in range(3):
    v=[base[(r-c)%3] for r in range(3)]
    for s in itertools.product([1,-1],repeat=3):
        N.append([v[r]*s[r] for r in range(3)])
assert len(N)==30 and len(set(tuple(v) for v in N))==30
ok={Q(0),Q(8),Q(-8),Q(16),Q(-16),Q(4,4),Q(4,-4),Q(-4,4),Q(-4,-4)}
for i in range(30):
    assert dot(N[i],N[i])==Q(16)
    for j in range(30): assert dot(N[i],N[j]) in ok,(i,j)
print("rtZ")
for v in N: print("  ![" + ", ".join(f"({x.a}, {x.b})" for x in v)+"],")
# five-fold axes (icosahedron corners), and every cross product of two of them is a multiple of a two-fold direction
F=[[z,Q(1),phi],[z,Q(-1),phi],[Q(1),phi,z],[Q(-1),phi,z],[phi,z,Q(1)],[phi,z,Q(-1)]]
def para(a,b):
    return cross(a,b)==[Q(0)]*3
def idx(n):
    for i,v in enumerate(N):
        if para(n,v) and dot(n,v).sign()>0: return i
for a,b in itertools.combinations(range(6),2):
    assert idx(cross(F[a],F[b])) is not None
print("every cross product of two five-fold axes is along a two-fold direction: ok")
def rhombo(name,u,v,w):
    print(name, "edges", u, v, w, "dots", dot(u,v), dot(v,w), dot(w,u), "len2", dot(u,u))
    out=[]
    for (a,b,c) in [(u,v,w),(v,w,u),(w,u,v)]:
        n=cross(b,c)  # normal to face spanned by b,c, n.a = det
        if dot(n,a).sign()<0: n=[-x for x in n]
        i=idx(n); j=idx([-x for x in n])
        d=dot(N[i],a)
        print("  face pair: +", i, N[i], "d =", d, d.lean(), "  -", j, "dot with other two", dot(N[i],b), dot(N[i],c))
        out.append((i,j,d))
    D=det(N[out[0][0]],N[out[1][0]],N[out[2][0]])
    print("  det of the three normals", D, D.lean())
    return out
rhombo("prolate (acute)", F[0],F[1],F[4])
rhombo("oblate (obtuse)", F[0],F[1],F[2])
# which kind: the product of the three edge dot products is > 0 for the prolate, < 0 for the oblate
for name,(a,b,c) in [("prolate",(0,1,4)),("oblate",(0,1,2))]:
    p=dot(F[a],F[b])*dot(F[b],F[c])*dot(F[c],F[a]); print(name,"product of edge dots",p,p.sign())
