import cmath, math
phi=(1+5**.5)/2
C=(0,0,1,1,0,1)
def star():
    T=[]
    for j in range(5):
        th=math.radians(72*j); P=cmath.rect(1,th)
        for s in (1,-1): T.append(('D',P,0j,cmath.rect(phi,th+s*math.radians(36))))
    return T
def splitD(P,Q,R,c=C):
    if not c[2]: Q,R=R,Q
    S=Q+(R-Q)/phi
    return [('K',Q,P,S) if c[3] else ('K',Q,S,P), ('D',S,P,R) if c[4] else ('D',S,R,P)]
def deflate(T,c=C):
    out=[]
    for t,X,Y,Z in T:
        if t=='K':
            A,B,Cc=X,Y,Z
            if c[5]: B,Cc=Cc,B
            D=A+(Cc-A)/phi
            out.append(('K',B,Cc,D) if c[0] else ('K',B,D,Cc))
            out+=splitD(*(((D,A,B) if c[1] else (D,B,A))))
        else: out+=splitD(X,Y,Z)
    return out
def key(a,b):
    k=lambda z:(round(z.real,7),round(z.imag,7)); return tuple(sorted([k(a),k(b)]))
