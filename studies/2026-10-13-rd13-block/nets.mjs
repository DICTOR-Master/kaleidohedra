// DICTO Spheroid-13 RD: printable A4 nets of its pieces (centre, outer A and B, and their mirror images) at thickness 0.15 and 0.35,
// from Polyhedraverse's own net tool (krp-core polyhedra-nets). Run: node studies/2026-10-13-rd13-block/nets.mjs
import fs from 'fs';
import { POLYHEDRA } from '../../src/krp-core/src/polyhedra/index.js';
import { netOf } from '../../src/krp-core/src/polyhedra-nets/unfold.js';
import { printableNetPdf, layoutNet } from '../../src/krp-core/src/polyhedra-nets/printable.js';
const ids = Object.keys(POLYHEDRA).filter((id) => /^KIT13_RD13_RD(CENTRE|A|B)_T(15|35)(_M)?$/.test(id));
// One scale for each thickness's set: the largest at which every piece of that set still fits its A4 sheet.
const nets = Object.fromEntries(ids.map((id) => [id, netOf(POLYHEDRA[id].vertices, POLYHEDRA[id].faces)]));
const setK = {};
for (const id of ids) { if (!nets[id]) continue; const t = id.match(/_T(\d+)/)[1]; setK[t] = Math.min(setK[t] ?? Infinity, layoutNet(nets[id], true).k); }
for (const id of ids) {
  const spec = POLYHEDRA[id], net = nets[id];
  if (!net) { console.log(id, 'NO NET FOUND'); continue; }
  const name = 'DICTO Spheroid-13 RD: ' + spec.name.replace('RD 13 ', '');
  const pdf = printableNetPdf(net, { title: name, tabs: true, credit: 'DICTO Spheroid-13 RD · DICTO · dictospheres.com', k: setK[id.match(/_T(\d+)/)[1]] });
  const out = new URL(`./nets/${id.toLowerCase()}.pdf`, import.meta.url);
  fs.writeFileSync(out, pdf);
  console.log(id.padEnd(26), name, `1 unit = ${(setK[id.match(/_T(\d+)/)[1]] / (72 / 25.4)).toFixed(1)} mm`);
}
