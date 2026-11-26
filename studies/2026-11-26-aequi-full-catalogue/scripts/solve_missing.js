// DICTO · Aequi full catalogue (26 Nov 2026): the not-catalogued sets of the small groups, solved with the picker's own fairSolve.
// With Claude (Anthropic). Usage: node solve_missing.js <aequi dir> <groups,comma> <out.json>
const fs = require('fs'), path = require('path');
const [DIR, GS, OUT] = process.argv.slice(2);
const G = require(path.resolve(DIR, 'geom.js')); const data = JSON.parse(fs.readFileSync(path.join(DIR, 'dice.json'))); G.prepare(data);
const res = {};
for (const g of GS.split(',')) {
  const orbs = data.groups[g], k = orbs.length, c = { fair: 0, notFair: 0, byM: {} };
  for (let mask = 1; mask < (1 << k); mask++) {
    const t = []; for (let i = 0; i < k; i++) if (mask & (1 << i)) t.push(i);
    if (t.length < 2 || G.lookup(data, g, t) || G.singleOrbit(data, g, t)) continue;
    const planes = []; t.forEach((oi, j) => orbs[oi].dirs.forEach(d => planes.push({ n: data.dirs[d], d: 1, k: j })));
    const fsol = G.fairSolve(planes, t.length), key = t.length + (fsol.ok ? ':fair' : ':none');
    fsol.ok ? c.fair++ : c.notFair++; c.byM[key] = (c.byM[key] || 0) + 1;
  }
  res[g] = c; console.log(g, JSON.stringify(c));
}
fs.writeFileSync(OUT, JSON.stringify(res, null, 1)); console.log('FINAL ok');
