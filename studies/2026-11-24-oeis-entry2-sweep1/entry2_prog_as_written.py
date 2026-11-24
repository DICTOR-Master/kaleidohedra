def coordseq(stack, k0, u0, N):
    # tetrahedral (SiC-type) net on the periodic stacking `stack` of close-packed bilayers.
    # Atom (k,x,y,u): bilayer k, in-plane point (x*a1+y*a2)/3, u = 0 lower / 1 upper atom.
    p = len(stack); L = ['ABC'.index(c) for c in stack]
    D = [(1,1), (-2,1), (1,-2)]          # the 3 shortest vectors from a point of A to B
    eps = lambda k: 1 if (L[(k+1)%p]-L[k%p]) % 3 == 1 else -1
    def nbrs(v):
        k, x, y, u = v
        if u: e = eps(k);  return [(k,x,y,0)] + [(k+1,x+e*a,y+e*b,0) for a,b in D]
        e = eps(k-1);      return [(k,x,y,1)] + [(k-1,x-e*a,y-e*b,1) for a,b in D]
    v0 = (k0, L[k0], L[k0], u0); seen = {v0}; front = {v0}; out = [1]
    for _ in range(N):
        front = {w for v in front for w in nbrs(v) if w not in seen}
        seen |= front; out.append(len(front))
    return out
import sys; print(coordseq("ABAC", 1, 0, int(sys.argv[1]) if len(sys.argv) > 1 else 57))
