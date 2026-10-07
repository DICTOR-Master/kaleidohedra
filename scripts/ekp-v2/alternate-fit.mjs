import { roofFoldSolids } from '../../src/geometry-extensions/roof-fold.js';
const S = roofFoldSolids();
const dot=(a,b)=>a[0]*b[0]+a[1]*b[1]+a[2]*b[2];
const sub=(a,b)=>[a[0]-b[0],a[1]-b[1],a[2]-b[2]], add=(a,b)=>[a[0]+b[0],a[1]+b[1],a[2]+b[2]];
const scl=(a,s)=>[a[0]*s,a[1]*s,a[2]*s], cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
const len=(a)=>Math.hypot(...a), unit=(a)=>scl(a,1/len(a));
const EPS=1e-7;
function rot(u,t){const c=Math.cos(t),s=Math.sin(t);return v=>add(add(scl(v,c),scl(cross(u,v),s)),scl(u,dot(u,v)*(1-c)));}
const R90=rot([0,0,1],Math.PI/2);
const mod=(n,m)=>((n%m)+m)%m;
const uniq=(P)=>{const m=new Map();for(const p of P)m.set(p.map(c=>{const t=c.toFixed(7);return t==='-0.0000000'?'0.0000000':t;}).join(),p);return [...m.values()];};
// Supporting planes of a convex point set (outward), via triples.
function planesOf(V){
  const ctr=scl(V.reduce(add),1/V.length);
  const seen=new Map();
  for(let i=0;i<V.length;i++)for(let j=i+1;j<V.length;j++)for(let k=j+1;k<V.length;k++){
    let n=cross(sub(V[j],V[i]),sub(V[k],V[i])); const l=len(n); if(l<1e-9)continue; n=scl(n,1/l);
    for(const sg of [1,-1]){const nn=scl(n,sg);const d=dot(nn,V[i]);
      let ok=true; for(const p of V){if(dot(nn,p)-d>EPS){ok=false;break;}}
      if(ok){ if(dot(nn,ctr)-d>EPS) continue; const dup=[...seen.values()].some(q=>dot(q.n,nn)>1-1e-9&&Math.abs(q.d-d)<1e-7); if(!dup) seen.set(seen.size,{n:nn,d}); }
    }
  }
  return [...seen.values()];
}
// Convex hull volume from points: facets identified by their point sets (robust to near-degenerate normals).
function isFlat(P){
  for(let i=0;i<P.length;i++)for(let j=i+1;j<P.length;j++)for(let k=j+1;k<P.length;k++){
    const n=cross(sub(P[j],P[i]),sub(P[k],P[i])); const l=len(n); if(l<1e-6)continue;
    const nn=scl(n,1/l); return P.every(p=>Math.abs(dot(nn,sub(p,P[i])))<1e-6)?true:false;
  }
  return true;
}
function hullVolume(pts){
  const P=uniq(pts); if(P.length<4||isFlat(P))return 0;
  const ctr=scl(P.reduce(add),1/P.length);
  const keys=new Set(); let V=0;
  for(let i=0;i<P.length;i++)for(let j=i+1;j<P.length;j++)for(let k=j+1;k<P.length;k++){
    let n0=cross(sub(P[j],P[i]),sub(P[k],P[i])); const l=len(n0); if(l<1e-9)continue; n0=scl(n0,1/l);
    for(const sg of [1,-1]){
      const n=scl(n0,sg); const d=dot(n,P[i]);
      if(P.some(p=>dot(n,p)-d>EPS))continue;
      if(dot(n,ctr)-d>EPS)continue;
      const on=[];P.forEach((p,idx)=>{if(Math.abs(dot(n,p)-d)<1e-6)on.push(idx);});
      if(on.length<3)continue;
      const key=on.join(','); if(keys.has(key))continue; keys.add(key);
      const pl=on.map(idx=>P[idx]);
      const dd=pl.reduce((s,p)=>s+dot(n,p),0)/pl.length;
      const u=unit(Math.abs(n[0])<0.9?cross(n,[1,0,0]):cross(n,[0,1,0])); const w=cross(n,u);
      const h=convex2d(pl.map(p=>[dot(p,u),dot(p,w)])); let A=0;
      for(let q=0;q<h.length;q++){const a=h[q],b=h[(q+1)%h.length];A+=a[0]*b[1]-a[1]*b[0];} A=Math.abs(A)/2;
      V+=A*dd/3;
    }
  }
  return V;
}
function convex2d(pts){
  const p=[...pts].sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
  const cr=(o,a,b)=>(a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0]);
  const lo=[],up=[];
  for(const q of p){while(lo.length>=2&&cr(lo[lo.length-2],lo[lo.length-1],q)<=1e-12)lo.pop();lo.push(q);}
  for(let i=p.length-1;i>=0;i--){const q=p[i];while(up.length>=2&&cr(up[up.length-2],up[up.length-1],q)<=1e-12)up.pop();up.push(q);}
  return lo.slice(0,-1).concat(up.slice(0,-1));
}
// Convex polytope from vertices and edges: planes, edges.
function poly(V,E){return {V,E,P:planesOf(V)};}
const inside=(Q,x)=>Q.P.every(({n,d})=>dot(n,x)-d<=EPS);
// Exact intersection volume of two convex polytopes.
function interVol(A,B){
  const pts=[];
  for(const v of A.V)if(inside(B,v))pts.push(v);
  for(const v of B.V)if(inside(A,v))pts.push(v);
  for(const [p,q] of A.E)for(const {n,d} of B.P){const sp=dot(n,p)-d,sq=dot(n,q)-d;if(sp*sq>0)continue;const t=sp/(sp-sq);const x=add(p,scl(sub(q,p),t));if(inside(B,x))pts.push(x);}
  for(const [p,q] of B.E)for(const {n,d} of A.P){const sp=dot(n,p)-d,sq=dot(n,q)-d;if(sp*sq>0)continue;const t=sp/(sp-sq);const x=add(p,scl(sub(q,p),t));if(inside(A,x))pts.push(x);}
  return hullVolume(pts);
}
// Dodecahedron and its world placement
const dodVerts=[...new Map(S.dodeca.faces.flat().map(p=>[p.map(c=>c.toFixed(9)).join(),p])).values()];
const dodEdges=S.dodeca.edges;
function dodecaAt(R,T){const f=p=>add(R(p),T);const V=dodVerts.map(f);const idx=new Map(dodVerts.map((p,i)=>[p.map(c=>c.toFixed(9)).join(),i]));const E=dodEdges.map(([p,q])=>[f(p),f(q)]);return poly(V,E);}
const dodVol=(15+7*Math.sqrt(5))/4*Math.pow(2/((1+Math.sqrt(5))/2),3);
// Self-check: dodecahedron with itself, and with a far copy
const D0=dodecaAt(p=>p,[0,0,0]);
// Star pieces: icosahedron + 20 spike tetrahedra (base = icosahedron face, apex = tip)
const icoV=[...new Map(S.ico.faces.flat().map(p=>[p.map(c=>c.toFixed(9)).join(),p])).values()];
const icoEdges=S.ico.edges;
const tipsOfStar=[...new Map(S.star.faces.flat().filter(p=>len(p)>1.2).map(p=>[p.map(c=>c.toFixed(9)).join(),p])).values()];
// Tetrahedra: each ico face with its apex (dodeca vertex 2/phi from its corners)
const icoFaces=S.ico.faces;
const PHI=(1+Math.sqrt(5))/2;
const tetra=icoFaces.map(tri=>{const c=scl(tri.reduce(add),1/3);const dir=unit(c);
  // tip: the star vertex lying along the outward direction of this face, at distance from the face centre
  const tip=tipsOfStar.reduce((best,p)=>dot(unit(p),dir)>dot(unit(best),dir)?p:best);
  return [tri[0],tri[1],tri[2],tip];});
const icoPiece=poly(icoV,icoEdges.map(([p,q])=>[p,q]));
const tetraPieces=tetra.map(V=>poly(V,[[V[0],V[1]],[V[1],V[2]],[V[2],V[0]],[V[0],V[3]],[V[1],V[3]],[V[2],V[3]]]));
// ---- v2: identical contents in every cube (six solids), odd cubes rotated 90 deg about z ----
const OCTV = [[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]];
const octE = []; for (let a = 0; a < 6; a++) for (let b = a + 1; b < 6; b++) if (Math.abs(len(sub(OCTV[a], OCTV[b])) - Math.SQRT2) < 1e-9) octE.push([OCTV[a], OCTV[b]]);
const T1V = [[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]], T2V = [[-1,-1,-1],[-1,1,1],[1,-1,1],[1,1,-1]];
const baseDod = poly(dodVerts, dodEdges), baseIco = poly(icoV, icoEdges), baseOct = poly(OCTV, octE);
const tetE = V => { const E = []; for (let a = 0; a < 4; a++) for (let b = a + 1; b < 4; b++) E.push([V[a], V[b]]); return E; };
const FACE = [[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]];
const FCC = []; for (const a of [-1,0,1]) for (const b of [-1,0,1]) for (const c of [-1,0,1]) if ((a+b+c) % 2 === 0 && (a||b||c)) FCC.push([a,b,c]);
const bsph = P => { const c = scl(P.V.reduce(add), 1 / P.V.length); return { c, r: Math.max(...P.V.map(v => len(sub(v, c)))) }; };
const baseT1 = poly(T1V, tetE(T1V)), baseT2 = poly(T2V, tetE(T2V));
const check = interVol(baseT1, baseT2);
const spikes = tetra.map(V => poly(V, tetE(V)));
// Signed convex pieces per solid (indicator = sum of s_i * 1_{P_i})
const pieces = (name, R, T) => {
  const f = p => add(R(p), T);
  const W = P => poly(P.V.map(f), P.E.map(([p, q]) => [f(p), f(q)]));
  switch (name) {
    case 'cube': return [[W(baseCube), 1]];
    case 'dodecahedron': return [[W(baseDod), 1]];
    case 'icosahedron': return [[W(baseIco), 1]];
    case 'star': return [[W(baseIco), 1], ...spikes.map(P => [W(P), 1])];
    case 'octahedron': return [[W(baseOct), 1]];
    case 'stella': return [[W(baseT1), 1], [W(baseT2), 1], [W(baseOct), -1]];
  }
};
const NAMES = ['cube', 'dodecahedron', 'icosahedron', 'star', 'octahedron', 'stella'];
const baseCube = poly(S.cube.faces.flat().filter((p, i, a) => a.findIndex(q => len(sub(q, p)) < 1e-9) === i), (() => { const V = S.cube.faces.flat().filter((p, i, a) => a.findIndex(q => len(sub(q, p)) < 1e-9) === i); const E = []; for (let a = 0; a < V.length; a++) for (let b = a + 1; b < V.length; b++) if (Math.abs(len(sub(V[a], V[b])) - 2) < 1e-9) E.push([V[a], V[b]]); return E; })());
const rotOf = c => (((c[0] + c[1] + c[2]) % 2) + 2) % 2 === 1 ? R90 : (p => p);
const cellPieces = (c) => { const R = rotOf(c), T = c.map(x => 2 * x); const out = {}; for (const n of NAMES) out[n] = pieces(n, R, T); return out; };
function overlapSolids(A, B) { // A, B: lists of [poly, sign]; exact via signed pieces
  let v = 0;
  for (const [P, s] of A) { const bp = bsph(P); for (const [Q, t] of B) { const bq = bsph(Q); if (len(sub(bp.c, bq.c)) > bp.r + bq.r + 1e-9) continue; v += s * t * interVol(P, Q); } }
  return v;
}
// Matrix of overlaps: solid X in cell a, solid Y in cell b
function matrix(a, b) { const A = cellPieces(a), B = cellPieces(b); return NAMES.map(X => NAMES.map(Y => overlapSolids(A[X], B[Y]))); }
const addM = (A, B) => A.map((r, i) => r.map((x, j) => x + B[i][j]));
const zero = () => NAMES.map(() => NAMES.map(() => 0));
const total = (M) => M.reduce((s, r) => s + r.reduce((a, b) => a + b, 0), 0);
const t0 = Date.now();
// Per-direction matrices for the three configurations
const faceM = FACE.map(d => matrix([0,0,0], d));
const fccEM = FCC.map(d => matrix([0,0,0], d));
const fccOM = FCC.map(d => matrix([1,0,0], [1 + d[0], d[1], d[2]]));
console.log('computed in', ((Date.now() - t0) / 1000).toFixed(1), 's');
console.log('face totals per direction (+x,-x,+y,-y,+z,-z):', faceM.map(total).map(x => x.toFixed(5)).join(' '));
console.log('fcc even per direction:', fccEM.map(total).map(x => x.toFixed(5)).join(' '));
console.log('fcc odd per direction:', fccOM.map(total).map(x => x.toFixed(5)).join(' '));
// Per-lattice-cube densities: 3 face pairs, 3 even-even FCC pairs, 3 odd-odd FCC pairs per cube (averaged over directions)
const avg = (Ms) => Ms.reduce((s, M) => addM(s, M), zero()).map(r => r.map(x => x / Ms.length));
const dens = (avgM, pairsPerCube) => avgM.map(r => r.map(x => x * pairsPerCube));
const densTotal = addM(addM(dens(avg(faceM), 3), dens(avg(fccEM), 3)), dens(avg(fccOM), 3));
console.log('per lattice cube (volume 8), total overlap:', total(densTotal).toFixed(4));
console.log('per-type-pair density per lattice cube:');
NAMES.forEach((X, i) => console.log('  ' + X.padEnd(12), densTotal[i].map(x => x.toFixed(4).padStart(8)).join(' ')), '  (columns:', NAMES.join(', ') + ')');
// Alternate fit: the pieces used in even and odd cubes, with the odd cubes turned 90 degrees about z.
// Exact overlap for every neighbour class: face (even-odd), edge-neighbour (same parity, FCC), corner.
const turnOf = c => (((c[0] + c[1] + c[2]) % 2) + 2) % 2 === 1 ? R90 : (p => p);
const at = (c) => { const R = turnOf(c), Tc = c.map(x => 2 * x); return p => add(R(p), Tc); };
const pieceSet = (kind, c) => {
  const f = at(c);
  if (kind === 'star') return [poly(icoV.map(f), icoEdges.map(([p, q]) => [f(p), f(q)])), ...tetra.map(V => { const W = V.map(f); return poly(W, tetE(W)); })].map(P => ({ P, s: 1 }));
  if (kind === 'ico') return [{ P: poly(icoV.map(f), icoEdges.map(([p, q]) => [f(p), f(q)])), s: 1 }];
  if (kind === 'dodeca') return [{ P: poly(dodVerts.map(f), dodEdges.map(([p, q]) => [f(p), f(q)])), s: 1 }];
  if (kind === 'stella') { const T = (Q) => poly(Q.V.map(f), Q.E.map(([p, q]) => [f(p), f(q)])); return [{ P: T(baseT1), s: 1 }, { P: T(baseT2), s: 1 }, { P: T(baseOct), s: -1 }]; }
};
const overlap = (A, B) => { let v = 0; for (const x of A) { const bx = bsph(x.P); for (const y of B) { const by = bsph(y.P); if (len(sub(bx.c, by.c)) > bx.r + by.r + 1e-9) continue; v += x.s * y.s * interVol(x.P, y.P); } } return v; };
const CORNER = []; for (const a of [-1,1]) for (const b of [-1,1]) for (const c of [-1,1]) CORNER.push([a,b,c]);
for (const [label, evenKind, oddKind] of [['star (even) with icosahedron (odd)', 'star', 'ico'], ['dodecahedron (even) with icosahedron (odd)', 'dodeca', 'ico']]) {
  const cls = {
    face: FACE.map(d => overlap(pieceSet(evenKind, [0,0,0]), pieceSet(oddKind, d))),
    corner: CORNER.map(d => overlap(pieceSet(evenKind, [0,0,0]), pieceSet(oddKind, d))),
    edgeEven: FCC.map(d => overlap(pieceSet(evenKind, [0,0,0]), pieceSet(evenKind, d))),
    edgeOdd: FCC.map(d => overlap(pieceSet('ico', [1,0,0]), pieceSet('ico', [1 + d[0], d[1], d[2]]))),
  };
  console.log(`== ${label}`);
  for (const [k, v] of Object.entries(cls)) console.log(`   ${k.padEnd(9)} largest overlap ${Math.max(...v.map(Math.abs)).toExponential(2)} over ${v.length} directions`);
}
// A star surrounded by icosahedra on all sides: the star at the origin with an icosahedron in every neighbour cube.
// Faces (odd, turned) and corners (odd, turned) are above; edge neighbours (even, unturned) are checked here.
{
  const edgeIco = FCC.map(d => overlap(pieceSet('star', [0,0,0]), pieceSet('ico', d)));
  console.log(`== star with icosahedra at the 12 edge neighbours (even, unturned)`);
  console.log(`   largest overlap ${Math.max(...edgeIco.map(Math.abs)).toExponential(2)} over ${edgeIco.length} directions`);
}

// Stella octangula alternating with the dodecahedron, the same checks as the star with the icosahedron.
for (const [label, evenKind, oddKind] of [['stella (even) with dodecahedron (odd, turned)', 'stella', 'dodeca'], ['dodecahedron (even) with stella (odd, turned)', 'dodeca', 'stella']]) {
  const cls = {
    face: FACE.map(d => overlap(pieceSet(evenKind, [0,0,0]), pieceSet(oddKind, d))),
    corner: CORNER.map(d => overlap(pieceSet(evenKind, [0,0,0]), pieceSet(oddKind, d))),
    edgeEven: FCC.map(d => overlap(pieceSet(evenKind, [0,0,0]), pieceSet(evenKind, d))),
  };
  console.log(`== ${label}`);
  for (const [k, v] of Object.entries(cls)) console.log(`   ${k.padEnd(9)} largest overlap ${Math.max(...v.map(Math.abs)).toExponential(2)} over ${v.length} directions`);
}
