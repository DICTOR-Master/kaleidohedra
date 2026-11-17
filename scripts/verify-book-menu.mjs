// The world menu by the books (DICTO 2026-11-17): every world action of the app -- the wizard's lists (dimension-wizard.js), the
// Lattice Select stations (lattice-select.js) and the worlds render.js opens (OWN_WORLD_ACTIONS) -- is placed exactly once in the
// menu's books and shelves (book-menu-data.js), and so is every lattice piece. Prints the placement and any world unplaced or
// placed twice; exits 1 if there is one.
import { readFileSync } from 'node:fs';
import { BOOKS, EXTRA_WORLDS, OTHERS_SHELF, TOOLS_SHELF } from '../src/app/book-menu-data.js';
import { K_WORLDS, LATTICES_3D, FAMILIES_1D, LATTICE_FAMILIES_2D } from '../src/app/dimension-wizard.js';
import { LATTICE_BLOCKS } from '../src/app/lattice-select.js';

const base = (a) => a.split(':').slice(0, 2).join(':'); // tool:octetWorld:caps -> tool:octetWorld
const isWorld = (a) => /^tool:\w+(World|Kit)$/.test(base(a)) || base(a) === 'tool:hexoctKit';
const worldOf = (key) => K_WORLDS.find((w) => w.key === key) ?? LATTICES_3D.find((l) => l.key === key);
const DICTO_PIECES = new Set(['tool:pieceType:dictohex']);

// what the menu places, entry by entry: [where, actions]
const placed = [];
for (const b of BOOKS) for (const [key] of b.worlds) {
  const acts = EXTRA_WORLDS[key] ? [EXTRA_WORLDS[key].action] : worldOf(key)?.pieces.map((p) => p.action);
  if (!acts) throw new Error(`Book ${b.id}: no world "${key}"`);
  placed.push([`Book ${b.id} · ${key}`, acts]);
}
for (const s of OTHERS_SHELF) {
  if (s.lat) placed.push([`Others · ${s.id}`, LATTICES_3D.find((l) => l.key === s.lat).pieces.map((p) => p.action).filter((a) => !DICTO_PIECES.has(a))]);
  else if (s.world) placed.push([`Others · ${s.id}`, worldOf(s.world).pieces.map((p) => p.action)]);
}
for (const s of TOOLS_SHELF) {
  if (s.world) placed.push([`Tools · ${s.id}`, worldOf(s.world).pieces.map((p) => p.action)]);
  else if (s.families) placed.push([`Tools · ${s.id}`, s.families.map((id) => [...FAMILIES_1D, ...LATTICE_FAMILIES_2D].find((f) => f.id === id).action)]);
}

// every world and lattice piece the app has
const render = readFileSync(new URL('../src/render.js', import.meta.url), 'utf8');
const own = [...render.match(/const OWN_WORLD_ACTIONS = \{([^}]*)\}/)[1].matchAll(/'(tool:\w+)'/g)].map((m) => m[1]);
const leaves = (st) => st.flatMap((s) => (s.kids ? leaves(s.kids) : [s]));
const sources = {
  'dimension-wizard.js': [...K_WORLDS, ...LATTICES_3D].flatMap((l) => l.pieces.map((p) => p.action)).concat(FAMILIES_1D.map((f) => f.action), LATTICE_FAMILIES_2D.filter((f) => !f.action.startsWith('tool:pieceType:lattice2d')).map((f) => f.action)),
  'lattice-select.js': LATTICE_BLOCKS.flatMap((b) => leaves(b.st)).map((s) => s.action),
  'render.js OWN_WORLD_ACTIONS': own,
};
const want = new Set();
for (const acts of Object.values(sources)) for (const a of acts) want.add(isWorld(a) ? base(a) : a);

// a world counts once per entry that opens it (its pieces are one entry); a lattice piece per action
const count = new Map(), where = new Map();
for (const [w, acts] of placed) for (const k of new Set(acts.map((a) => (isWorld(a) ? base(a) : a)))) {
  count.set(k, (count.get(k) ?? 0) + 1); where.set(k, [...(where.get(k) ?? []), w]);
}
const unplaced = [...want].filter((k) => !count.has(k));
const twice = [...count].filter(([, n]) => n > 1).map(([k]) => `${k}: ${where.get(k).join(' and ')}`);
const extra = [...count.keys()].filter((k) => !want.has(k));
for (const [w, acts] of placed) console.log(`${w.padEnd(34)} ${[...new Set(acts.map((a) => (isWorld(a) ? base(a) : a)))].join(', ')}`);
console.log(`\n${want.size} world actions and lattice pieces in the app (${Object.entries(sources).map(([f, a]) => `${f}: ${new Set(a.map((x) => (isWorld(x) ? base(x) : x))).size}`).join('; ')}).`);
console.log(`Unplaced: ${unplaced.length ? unplaced.join(', ') : 'none'}`);
console.log(`Placed more than once: ${twice.length ? twice.join('; ') : 'none'}`);
console.log(`Placed but not an app action: ${extra.length ? extra.join(', ') : 'none'}`);
process.exit(unplaced.length || twice.length || extra.length ? 1 : 0);
