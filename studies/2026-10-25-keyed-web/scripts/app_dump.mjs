// Dump the app's keyed network (k-mix src/app/world-octet.js goldenPieces(size, { pattern: 'allKeyed' }), as the DICTONIC keyed
// view uses it) as floats for the cross-check. node --import ../../2026-10-25-web-of-bonds/scripts/reg.mjs app_dump.mjs > ../data/app-keyed.json
import { goldenPieces } from '/home/dicto/k-mix/src/app/world-octet.js';
const P = goldenPieces(2, { pattern: 'allKeyed' });
console.log(JSON.stringify(P.map(([role, V, F, n, e]) => ({ role, V, F, n, anchor: e?.anchor }))));
