import { roofFoldSolids } from '../../src/krp-core/src/geometry-extensions/roof-fold.js';
const S = roofFoldSolids();
// --unturned: the identical-cells variation (no turn). Default: odd cubes turned 90 degrees about z.
const UNTURNED = process.argv.includes('--unturned');
console.log(UNTURNED ? 'variation: identical cells, unturned' : 'variation: odd cubes turned 90 degrees about z');
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
// Convex polytope from vertices and edges: planes, edges.
function poly(V,E){return {V,E,P:planesOf(V)};}
// Exact intersection volume of two convex polytopes. Each boundary face of one is clipped to the other, so the
// boundary of A∩B is the part of A's boundary inside B plus the part of B's boundary inside A. A face of B that
// lies in the same plane, with the same outward normal, as a face of A is counted once.
const TOL=1e-9;
function facesOf(Q){
  return Q.P.map(({n,d})=>{
    const on=uniq(Q.V.filter(v=>Math.abs(dot(n,v)-d)<1e-6));
    const c=scl(on.reduce(add),1/on.length);
    const u=unit(Math.abs(n[0])<0.9?cross(n,[1,0,0]):cross(n,[0,1,0])), w=cross(n,u);
    const ang=v=>Math.atan2(dot(sub(v,c),w),dot(sub(v,c),u));
    return {n,d,poly:on.sort((a,b)=>ang(a)-ang(b))};
  }).filter(f=>f.poly.length>=3);
}
function clipPoly(poly,m,e){
  const out=[], s=poly.map(p=>dot(m,p)-e);
  for(let i=0;i<poly.length;i++){
    const j=(i+1)%poly.length, p=poly[i], q=poly[j], sp=s[i], sq=s[j];
    if(sp<=TOL)out.push(p);
    if((sp<-TOL&&sq>TOL)||(sp>TOL&&sq<-TOL))out.push(add(p,scl(sub(q,p),sp/(sp-sq))));
  }
  return out;
}
function polyArea(poly,n){
  let s=[0,0,0];
  for(let i=0;i<poly.length;i++)s=add(s,cross(poly[i],poly[(i+1)%poly.length]));
  return Math.abs(dot(s,n))/2;
}
function interVol(A,B){
  const FA=facesOf(A), FB=facesOf(B);
  let v=0;
  for(const f of FA){
    let poly=f.poly; for(const g of B.P)poly=clipPoly(poly,g.n,g.d);
    if(poly.length>=3)v+=f.d*polyArea(poly,f.n)/3;
  }
  for(const g of FB){
    if(FA.some(f=>dot(f.n,g.n)>1-1e-9&&Math.abs(f.d-g.d)<1e-7))continue;
    let poly=g.poly; for(const f of A.P)poly=clipPoly(poly,f.n,f.d);
    if(poly.length>=3)v+=g.d*polyArea(poly,g.n)/3;
  }
  return v;
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
const tetE = V => { const E = []; for (let a = 0; a < 4; a++) for (let b = a + 1; b < 4; b++) E.push([V[a], V[b]]); return E; };
const T1V = [[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]], T2V = [[-1,-1,-1],[-1,1,1],[1,-1,1],[1,1,-1]];
const baseDod = poly(dodVerts, dodEdges), baseIco = poly(icoV, icoEdges), baseOct = poly(OCTV, octE);
const baseT1 = poly(T1V, tetE(T1V)), baseT2 = poly(T2V, tetE(T2V));
const check = interVol(baseT1, baseT2);
console.log('check: stella T1 cap T2 volume', check.toFixed(6), '(octahedron 4/3 =', (4/3).toFixed(6) + ')');
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
const rotOf = c => !UNTURNED && (((c[0] + c[1] + c[2]) % 2) + 2) % 2 === 1 ? R90 : (p => p);
const cellPieces = (c) => { const R = rotOf(c), T = c.map(x => 2 * x); const out = {}; for (const n of NAMES) out[n] = pieces(n, R, T); return out; };
const bsph = P => { const c = scl(P.V.reduce(add), 1 / P.V.length); return { c, r: Math.max(...P.V.map(v => len(sub(v, c)))) }; };
function overlapSolids(A, B) { // A, B: lists of [poly, sign]; exact via signed pieces
  let v = 0;
  for (const [P, s] of A) { const bp = bsph(P); for (const [Q, t] of B) { const bq = bsph(Q); if (len(sub(bp.c, bq.c)) > bp.r + bq.r + 1e-9) continue; v += s * t * interVol(P, Q); } }
  return v;
}
// Matrix of overlaps: solid X in cell a, solid Y in cell b
function matrix(a, b) { const A = cellPieces(a), B = cellPieces(b); return NAMES.map(X => NAMES.map(Y => overlapSolids(A[X], B[Y]))); }
const FACE = [[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]];
const FCC = []; for (const a of [-1,0,1]) for (const b of [-1,0,1]) for (const c of [-1,0,1]) if ((a+b+c) % 2 === 0 && (a||b||c)) FCC.push([a,b,c]);
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
// Corner neighbours (odd offsets, one step along each axis): the large pieces touch there, so the total should be zero.
const CORNER = []; for (const a of [-1, 1]) for (const b of [-1, 1]) for (const c of [-1, 1]) CORNER.push([a, b, c]);
console.log('corner neighbours, total over the 8 directions:', CORNER.map(d => total(matrix([0,0,0], d))).map(x => x.toFixed(6)).join(' '));
// Monte Carlo check of one pair of pieces: the star with the star across a face (+y), by sampling points.
if (process.argv.includes('--mc')) {
  const inStar = (pieces, x) => pieces.some(([P]) => P.P.every(({ n, d }) => dot(n, x) - d <= 1e-12));
  const A = cellPieces([0,0,0]).star, B = cellPieces([0,1,0]).star, N = 2e7;
  const bbox = pcs => [0,1,2].map(i => [Math.min(...pcs.flatMap(([P]) => P.V.map(v => v[i]))), Math.max(...pcs.flatMap(([P]) => P.V.map(v => v[i])))]);
  const a = bbox(A), b = bbox(B);
  const lo = [0,1,2].map(i => Math.max(a[i][0], b[i][0])), hi = [0,1,2].map(i => Math.min(a[i][1], b[i][1]));
  const box = (hi[0]-lo[0])*(hi[1]-lo[1])*(hi[2]-lo[2]);
  let hit = 0;
  for (let k = 0; k < N; k++) {
    const x = [lo[0]+Math.random()*(hi[0]-lo[0]), lo[1]+Math.random()*(hi[1]-lo[1]), lo[2]+Math.random()*(hi[2]-lo[2])];
    if (inStar(A, x) && inStar(B, x)) hit++;
  }
  const exact = (() => { let s = 0; for (const [P] of A) for (const [Q] of B) s += interVol(P, Q); return s; })();
  console.log(`star with star across a face (+y): exact ${exact.toFixed(5)}; Monte Carlo ${(box*hit/N).toFixed(5)} +/- ${(box*Math.sqrt((hit/N)*(1-hit/N)/N)).toFixed(5)} (${N.toExponential(0)} samples)`);
}
