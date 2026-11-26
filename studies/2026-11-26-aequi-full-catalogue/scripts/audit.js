// DICTO · Aequi full catalogue, step 1 (26 Nov 2026): which tick sets of the picker are already one of ours? With Claude (Anthropic).
// DICTO: "cant we just enumerate every possibility so anything selected is one of ours"; "all combis of everything".
// Uses the picker's own code (k-mix aequi/geom.js) and data (dice.json): for every set of 2+ kinds in each group with at most
// 2^22 sets, classify exactly as the picker does: catalogued (under this group), catalogued under a larger group, one kind
// (face-transitive), or NOT CATALOGUED (the picker would say "computed here" or "cannot make a fair die").
// Usage: node audit.js <aequi dir> <out.json>
const fs = require('fs'), path = require('path');
const [DIR, OUT] = process.argv.slice(2);
const G = require(path.resolve(DIR, 'geom.js'));
const data = JSON.parse(fs.readFileSync(path.join(DIR, 'dice.json')));
G.prepare(data);
const res = {};
for (const g of Object.keys(data.groups)) {
  const k = data.groups[g].length; if (k > 22) { res[g] = { orbits: k, skipped: true }; continue; }
  const c = { orbits: k, sets: 0, catalogued: 0, larger: 0, oneKind: 0, missing: 0, missingByM: {} };
  for (let mask = 1; mask < (1 << k); mask++) {
    const t = []; for (let i = 0; i < k; i++) if (mask & (1 << i)) t.push(i);
    if (t.length < 2) continue; c.sets++;
    const r = G.lookup(data, g, t);
    if (r && r.exact) c.catalogued++; else if (r) c.larger++;
    else if (G.singleOrbit(data, g, t)) c.oneKind++;
    else { c.missing++; c.missingByM[t.length] = (c.missingByM[t.length] || 0) + 1; }
  }
  res[g] = c; console.log(g, JSON.stringify(c));
}
fs.writeFileSync(OUT, JSON.stringify(res, null, 1));
const ctrl = res.Ih && res.Ih.catalogued >= 3;   // control: the catalogued Ih dice (m = 2: 3) are found
console.log(ctrl ? 'FINAL ok' : 'FINAL FAIL (control: Ih dice not found)');
