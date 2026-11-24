// Aequi picker data from the numberings study (k-research studies/2026-11-24-aequi-numberings):
//   aequi/names.json       the 1232 approved names, in picker order (entry n-1 = "Minana (No.377)" for n = 377)
//   aequi/numberings.json  face numbers for every finished die: { "<n>": { o, s, b } }, each a list with the
//                          number on face i (face i = the i-th plane of planesFor). o = opposites (N + 1), only for
//                          centrally symmetric dice; s = spin-down; b = balanced. Plain (face i gets i + 1) needs no data.
// Later dice are added by running this again on the study folder (a data-only update).
// Usage: node scripts/aequi-data.mjs <study folder>
import { readFile, writeFile, readdir } from 'node:fs/promises';
import path from 'node:path';

const study = process.argv[2];
if (!study) throw new Error('usage: node scripts/aequi-data.mjs <study folder>');
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const dice = JSON.parse(await readFile(path.join(root, 'aequi/dice.json'), 'utf8'));
const D = dice.dice.length;

// names
const rows = (await readFile(path.join(study, 'names.csv'), 'utf8')).trim().split(/\r?\n/).slice(1).map((l) => l.split(','));
if (rows.length !== D) throw new Error(`names.csv has ${rows.length} rows, the picker ${D} dice`);
const names = rows.map((r, i) => {
  if (+r[0] !== i + 1 || r[2] !== `${r[1]} (No.${i + 1})`) throw new Error(`names.csv row ${i + 1}: ${r.join(',')}`);
  return r[2];
});
if (new Set(names.map((s) => s.replace(/ \(no\. \d+\)$/, ''))).size !== D) throw new Error('names not distinct');

// numberings
const isPerm = (a, N) => Array.isArray(a) && a.length === N && new Set(a).size === N && a.every((x) => Number.isInteger(x) && x >= 1 && x <= N);
const out = {};
const files = (await readdir(path.join(study, 'data/dice'))).filter((f) => /^\d{4}\.json$/.test(f)).sort();
let nO = 0, nS = 0, nB = 0;
for (const f of files) {
  const x = JSON.parse(await readFile(path.join(study, 'data/dice', f), 'utf8'));
  const e = dice.dice[x.n - 1];
  const dirs = e.o.flatMap((oi) => dice.groups[e.g][oi].dirs);
  if (x.N !== e.N || x.group !== e.g || JSON.stringify(x.face_direction) !== JSON.stringify(dirs)) throw new Error(`${f}: face order differs from the picker`);
  if (x.name_shown.replace(/\(no\. (\d+)\)/, "(No.$1)") !== names[x.n - 1]) throw new Error(`${f}: name differs from names.csv`);
  const s = x.schemes, r = {};
  if (s.opposite && s.opposite.available && isPerm(s.opposite.numbers, e.N)) {
    const o = s.opposite.numbers;
    // each face and its exactly opposite face carry numbers summing to N + 1
    dirs.forEach((d, i) => {
      const v = dice.dirs[d], j = dirs.findIndex((d2) => dice.dirs[d2].every((c, k) => Math.abs(c + v[k]) < 1e-9));
      if (j < 0 || o[i] + o[j] !== e.N + 1) throw new Error(`${f}: opposites do not sum to N + 1`);
    });
    r.o = o; nO++;
  }
  if (s.spin_down && isPerm(s.spin_down.numbers, e.N)) {
    // consecutive numbers on faces that share a side (and N next to 1 for a cycle)
    const sp = s.spin_down.numbers, at = []; sp.forEach((v, i) => { at[v] = i; });
    const sides = x.face_vertices.map((fv) => new Set(fv.map((a, t) => { const b = fv[(t + 1) % fv.length]; return a < b ? a + '_' + b : b + '_' + a; })));
    const adj = (i, j) => [...sides[i]].some((k) => sides[j].has(k));
    for (let v = 1; v < e.N; v++) if (!adj(at[v], at[v + 1])) throw new Error(`${f}: spin-down ${v}, ${v + 1} not on adjacent faces`);
    if (s.spin_down.kind === 'cycle' && !adj(at[e.N], at[1])) throw new Error(`${f}: spin-down cycle not closed`);
    r.s = sp; nS++;
  }
  if (s.balanced && isPerm(s.balanced.numbers, e.N)) { r.b = s.balanced.numbers; nB++; }
  out[x.n] = r;
}
await writeFile(path.join(root, 'aequi/names.json'), JSON.stringify(names) + '\n');
await writeFile(path.join(root, 'aequi/numberings.json'), JSON.stringify(out) + '\n');
console.log(`names ${names.length}; numbered dice ${files.length}: opposites ${nO}, spin-down ${nS}, balanced ${nB}`);
