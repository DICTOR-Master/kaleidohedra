// Export the app's dodecahedron and Dogstar (krp-core roof-fold.js, the geometry of #42) as vertex lists for proof.py.
// Usage: node export.mjs <k-mix path>
const { roofFoldSolids, dogstarSolid } = await import(process.argv[2] + '/src/krp-core/src/geometry-extensions/roof-fold.js');
const verts = (faces) => { const m = new Map(); for (const f of faces) for (const p of f) m.set(p.map((c) => c.toFixed(12)).join(','), p); return [...m.values()]; };
const fs = await import('fs');
fs.writeFileSync('app-solids.json', JSON.stringify({ dodeca: verts(roofFoldSolids().dodeca.faces), dogstar: verts(dogstarSolid()) }));
console.log('exported');
// faces too (for the solid-to-solid comparison of the Dogstar)
fs.writeFileSync('app-dogstar-faces.json', JSON.stringify(dogstarSolid()));
