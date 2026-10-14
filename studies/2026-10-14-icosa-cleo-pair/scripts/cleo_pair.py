"""Icosahedral Cleo + one partner fill space (DICTO question, 2026-10-14).
Construction: the prolate (acute) golden rhombohedron spanned by the three
vectors u,v,w from the icosahedron centre to one face = Cleo + A + Cleo',
A = trigonal antiprism. Checks: volumes, dihedrals, congruence, face-to-face
lattice tiling (Monte Carlo cover count, face matching, edge and vertex
closure), Dehn bookkeeping, rhombic triacontahedron = 20 rhombohedra."""
import numpy as np, itertools, json, sys
from scipy.spatial import ConvexHull
rng = np.random.default_rng(20261014)
phi = (1+5**.5)/2
V = []
for a in (1,-1):
    for b in (phi,-phi):
        V += [(0,a,b),(a,b,0),(b,0,a)]
V = np.array(V)/5**.5                      # icosahedron, edge 2/sqrt5
E = 2/5**.5
# a face: three mutually adjacent vertices
for i,j,k in itertools.combinations(range(12),3):
    if all(abs(np.linalg.norm(V[p]-V[q])-E)<1e-9 for p,q in ((i,j),(j,k),(i,k))):
        u,v,w = V[i],V[j],V[k]; break
R = np.linalg.norm(u)
out = {"edge_base": E, "side_edge_R": R,
       "cos_uv": float(u@v/R**2), "1/sqrt5": 5**-.5}

def poly(P):
    P = np.array(P,float); h = ConvexHull(P)
    # merge coplanar facets
    planes = []
    for eq in h.equations:
        if not any(np.allclose(eq,p,atol=1e-9) for p in planes): planes.append(eq)
    faces = []
    for eq in planes:
        idx = [i for i in range(len(P)) if abs(P[i]@eq[:3]+eq[3])<1e-9]
        faces.append((eq, idx))
    return dict(P=P, vol=h.volume, faces=faces)

def edges_dihedrals(T):
    P,F = T["P"],T["faces"]; res = []
    for (e1,i1),(e2,i2) in itertools.combinations(F,2):
        s = sorted(set(i1)&set(i2))
        if len(s)==2:
            ang = np.pi-np.arccos(np.clip(e1[:3]@e2[:3],-1,1))
            res.append((s, float(np.linalg.norm(P[s[0]]-P[s[1]])), float(ang)))
    return res

def solid_angle(T, vi):
    ed = [d for d in edges_dihedrals(T) if vi in d[0]]
    return sum(a for *_,a in ed) - (len(ed)-2)*np.pi

def signature(T):
    return sorted((round(l,9), round(np.degrees(a),6)) for _,l,a in edges_dihedrals(T))

o = np.zeros(3); s = u+v+w
C  = poly([o,u,v,w]); C2 = poly([s,s-u,s-v,s-w]); A = poly([u,v,w,u+v,v+w,w+u])
Rh = poly([o,u,v,w,u+v,v+w,w+u,s])
ico = poly(V)
out["vol"] = dict(cleo=C["vol"], cleo2=C2["vol"], A=A["vol"], rhombohedron=Rh["vol"],
                  ico_over_20=ico["vol"]/20, A_over_cleo=A["vol"]/C["vol"],
                  rh_over_cleo=Rh["vol"]/C["vol"])
for name,T in (("cleo",C),("cleo_far",C2),("A",A),("rhombohedron",Rh)):
    out[name+"_edges_len_deg"] = sorted(set(signature(T)))
    out[name+"_nfaces_nverts"] = (len(T["faces"]), len(T["P"]))
out["cleo_far_congruent_to_cleo"] = signature(C)==signature(C2)
out["A_face_sizes"] = sorted(len(i) for _,i in A["faces"])
out["A_vertices"] = A["P"].tolist()
out["u_v_w"] = [u.tolist(), v.tolist(), w.tolist()]
out["cleo_apex_solid_angle_x20_over_4pi"] = solid_angle(C,0)*20/(4*np.pi)
th = np.arccos(-5**.5/3)
out["theta_ico_deg"] = np.degrees(th)
out["A_cap_edge_dihedral_plus_half_theta_deg"] = None
for _,l,a in edges_dihedrals(A):
    if abs(l-E)<1e-9: out["A_cap_edge_dihedral_plus_half_theta_deg"] = np.degrees(a+th/2)
# Dehn bookkeeping: angles written as q*pi + m*(theta/2)
def dehn(T):
    tot = 0.0  # coefficient of (edge length) tensor (theta/2), lengths are E only
    rest = []
    for _,l,a in edges_dihedrals(T):
        for m in (1,-1,0):
            q = (a - m*th/2)/np.pi
            if abs(q*60-round(q*60))<1e-9: break
        else: rest.append(a)
        if m: assert abs(l-E)<1e-9; tot += m
    return tot, rest
out["dehn_coeff_of_E_x_halftheta"] = dict(cleo=dehn(C)[0], A=dehn(A)[0], rhombohedron=dehn(Rh)[0])

# ---- tiling patch: lattice Z u+Z v+Z w, each cell = C + A + C'
N = 4
tiles = []
for n in itertools.product(range(-N,N+1),repeat=3):
    t = n[0]*u+n[1]*v+n[2]*w
    for kind,T in (("C",C),("A",A),("C'",C2)):
        tiles.append((kind, T["P"]+t, [(eq[:3], eq[3]-eq[:3]@t, idx) for eq,idx in T["faces"]], T))
# Monte Carlo cover count in a ball of radius 1.5 (well inside patch)
pts = rng.uniform(-1.5,1.5,(200000,3)); pts = pts[np.linalg.norm(pts,axis=1)<1.5]
cnt = np.zeros(len(pts),int)
for kind,P,F,T in tiles:
    if np.linalg.norm(P.mean(0))>3.5: continue
    inside = np.ones(len(pts),bool)
    for nrm,d,_ in F: inside &= pts@nrm+d < 1e-12
    cnt += inside
out["montecarlo_points"] = int(len(pts)); out["cover_count_hist"] = np.bincount(cnt).tolist()
# face-to-face: collect faces (as vertex coordinate sets) of tiles near origin
def key(X): return tuple(sorted(tuple(np.round(x,7)) for x in X))
faces = {}
near = [t for t in tiles if np.linalg.norm(t[1].mean(0))<4.0]
for ti,(kind,P,F,T) in enumerate(near):
    for nrm,d,idx in F: faces.setdefault(key(P[idx]),[]).append(ti)
deep = [k for k in faces if np.linalg.norm(np.mean(k,axis=0))<2.0]
out["faces_checked"] = len(deep)
out["faces_shared_by_exactly_2"] = sum(len(faces[k])==2 for k in deep)
out["face_kinds"] = {}
for k in deep:
    if len(faces[k])==2:
        kk = "+".join(sorted(near[i][0] for i in faces[k])); out["face_kinds"][kk]=out["face_kinds"].get(kk,0)+1
# edge closure and vertex closure
edgesum, vsum = {}, {}
for kind,P,F,T in near:
    for (i,j),l,a in edges_dihedrals(T):
        edgesum[key(P[[i,j]])] = edgesum.get(key(P[[i,j]]),0)+a
    for vi in range(len(P)):
        kv = tuple(np.round(P[vi],7)); vsum[kv] = vsum.get(kv,0)+solid_angle(T,vi)
de = [abs(val-2*np.pi) for k,val in edgesum.items() if np.linalg.norm(np.mean(k,axis=0))<2.0]
dv = [abs(val-4*np.pi) for k,val in vsum.items() if np.linalg.norm(k)<2.0]
out["edges_checked"]=len(de); out["max_edge_angle_sum_error"]=max(de)
out["vertices_checked"]=len(dv); out["max_vertex_solid_angle_error"]=max(dv)
# ---- rhombic triacontahedron: 20 rhombohedra round the centre (one per ico face)
faces20 = [f for f in itertools.combinations(range(12),3)
           if all(abs(np.linalg.norm(V[p]-V[q])-E)<1e-9 for p,q in itertools.combinations(f,2))]
allp = []; rhs = []
for f in faces20:
    a,b,c = V[list(f)]
    Q = [o,a,b,c,a+b,b+c,c+a,a+b+c]; allp += Q; rhs.append(poly(Q))
hull = ConvexHull(np.array(allp))
out["RT_hull_volume"] = hull.volume; out["20_rhombohedra_volume"] = 20*Rh["vol"]
pts = rng.uniform(-2,2,(200000,3)); c2 = np.zeros(len(pts),int)
for T in rhs:
    ins = np.ones(len(pts),bool)
    for eq,_ in T["faces"]: ins &= pts@eq[:3]+eq[3] < 1e-12
    c2 += ins
inh = np.all(pts@hull.equations[:,:3].T+hull.equations[:,3]<1e-12,axis=1)
out["RT_check_hist_inside_hull"] = np.bincount(c2[inh]).tolist()
out["RT_check_points_outside_hull_covered"] = int((c2[~inh]>0).sum())
hv = np.unique(np.round(hull.points[hull.vertices],7),axis=0)
out["RT_hull_nvertices"] = len(hv); out["RT_hull_nfaces_merged"] = len(poly(hv)["faces"])
# ---- variant: parallelepiped at a BASE corner of Cleo (corner u, edges v-u, w-u, -u)
a1,a2,a3 = v-u, w-u, -u; q = u
Pb = [q,q+a1,q+a2,q+a3,q+a1+a2,q+a2+a3,q+a1+a3,q+a1+a2+a3]
Cb2 = poly([Pb[7],Pb[7]-a1,Pb[7]-a2,Pb[7]-a3])
Ab = poly([q+a1,q+a2,q+a3,q+a1+a2,q+a2+a3,q+a1+a3])
out["variant_base_corner"] = dict(far_corner_congruent_to_cleo=signature(Cb2)==signature(C),
    middle_volume_over_cleo=Ab["vol"]/C["vol"], middle_congruent_to_A=signature(Ab)==signature(A),
    middle_edges_len_deg=sorted(set(signature(Ab))))
json.dump(out, sys.stdout, indent=1, default=float)
