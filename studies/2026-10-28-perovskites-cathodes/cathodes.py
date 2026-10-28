# Layered LiCoO2 along charge vs hexagonality h of the oxygen stacking (DICTO 10-28).
# Exact count from the oxygen layer letters: slabs = layer pairs (0,1),(2,3)...; Co sits in each slab, Li in each gap,
# both on the letter missing from their two bounding layers. Octahedra across a layer share a face iff same letter.
def third(a,b): return ({'A','B','C'}-{a,b}).pop()
def analyse(seq):
    n=len(seq); L=lambda i: seq[i%n]
    h=sum(L(i-1)==L(i+1) for i in range(n))/n
    per_gap=[]
    for s in range(0,n,2):                      # gap between layer s+1 and s+2
        co_below=third(L(s),L(s+1)); li=third(L(s+1),L(s+2)); co_above=third(L(s+2),L(s+3))
        per_gap.append((co_below==li)+(co_above==li))
    return h, per_gap
cases=[('O3  LiCoO2',            'ABCABC'),        # Delmas notation: O = octahedral Li, 3 slabs per cell
       ('O1  CoO2',              'AB'),
       ('O2  LiCoO2 (metastable)','ABAC'),
       ('H1-3 Li0.12CoO2',        None)]
# H1-3 built explicitly: alternate O3-type and O1-type gaps (Van der Ven et al. 1998; Motohashi et al. 2009)
def hybrid(k):
    seq=['A','B']
    for i in range(k):
        X,Y=seq[-2],seq[-1]
        if i%2==0: a=third(X,Y); seq+=[a,third(Y,a)]   # O3 gap: next slab continues ABC
        else:      seq+=[X,Y]                            # O1 gap: next slab repeats (hcp across gap)
    return seq[:-2]
cases[3]=('H1-3 Li0.12CoO2', ''.join(hybrid(12)))
for name,seq in cases:
    h,g=analyse(seq)
    print(f'{name:24s} oxygen {seq:24s} h = {h:.3f}  face-sharing Li-Co pairs per gap site: {g}  mean {sum(g)/len(g):.2f} = 2h {2*h:.2f}')
# Motohashi et al., PRB 80, 165114 (2009), Table I (measured): interlayer distance d per CoO2 layer
a,b=4.24,4.81
print(f'law line at h=1/2 between O1 d={a} and O3 (x=0.35) d={b}: {(a+b)/2:.3f} A; measured H1-3 d=4.52 A (c/6={27.13/6:.4f}); off {((a+b)/2-4.52)/4.52*100:+.2f}%')
