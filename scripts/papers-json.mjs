// Writes data/papers.json for the world menu's paper chips and each book's "Papers in this book" (DICTO 2026-11-21, approved).
// One source of truth each: which papers belong to which WORLD stays in src/app/book-menu-data.js (the menu's own lists, read by
// the app directly; not copied here). This file adds only what the app did not have:
//   papers: number -> short title, full title, concept DOI   (from the Concordance, dicto-concordance/concordance.json "papers";
//           its "doi" is the concept record; checked against each paper folder's zenodo-state.json conceptrecid where one exists)
//   books:  app book id -> paper numbers                       (from the survey map, studies/2026-11-21-survey-map/survey-map.json:
//           a paper is in a book when the book cites it; book folder names mapped to the app's book ids below)
// Usage: node scripts/papers-json.mjs [path to k-research]   (default ~/k-research). Run it and commit data/papers.json.
import { readFileSync, writeFileSync, readdirSync, existsSync } from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';
import { BOOKS, paperNumbers } from '../src/app/book-menu-data.js';

const KR = process.argv[2] || path.join(os.homedir(), 'k-research');
const out = path.join(path.dirname(fileURLToPath(import.meta.url)), '..', 'data', 'papers.json');
const conc = JSON.parse(readFileSync(path.join(KR, 'papers/dicto-concordance/concordance.json'), 'utf8')).papers;
const survey = JSON.parse(readFileSync(path.join(KR, 'studies/2026-11-21-survey-map/survey-map.json'), 'utf8'));

// survey-map book folders -> the app's book ids (BOOKS in book-menu-data.js); a folder with no app book is reported, not guessed
const BOOK_OF = {
  'quanta-of-space': 'One', 'quanta-dictonary': 'One', 'space-fillers': 'Two', bonds: 'Three', 'golden-cycle': 'Four',
  'star-cores': 'Five', 'laws-of-stacking': 'Six', 'permutohedron-paradigm': 'Seven', platonic: 'Eight', 'golden-ladder': 'Nine', queens: 'Ten',
};
const ids = new Set(BOOKS.map((b) => b.id));
for (const v of Object.values(BOOK_OF)) if (!ids.has(v)) throw new Error(`no app book ${v}`);

const num = (n) => { const m = String(n).match(/^(\d+)(.*)$/); return [Number(m[1]), m[2]]; };
const byNum = (a, b) => { const [x, s] = num(a), [y, t] = num(b); return x - y || s.localeCompare(t); };
const bare = (d) => String(d).replace(/^10\.5281\/zenodo\./, '');
// short title: the part before the first colon or dash, when that part is a title on its own (at least two words)
const short = (t) => { const h = t.split(/:\s| — | – /)[0].trim(); return h.split(/\s+/).length >= 2 && h.length < t.length ? h : t; };

// concept ids from the paper folders, to check the Concordance's "doi"
const conceptOfVersion = new Map();
for (const d of readdirSync(path.join(KR, 'papers'))) {
  const f = path.join(KR, 'papers', d, 'zenodo-state.json');
  if (!existsSync(f)) continue;
  try { const z = JSON.parse(readFileSync(f, 'utf8')); if (z.id && z.conceptrecid) conceptOfVersion.set(String(z.id), String(z.conceptrecid)); } catch { /* not a state file */ }
}
const papers = {}, notes = [];
let checked = 0;
for (const n of Object.keys(conc).sort(byNum)) {
  const p = conc[n];
  if (!p.doi) { notes.push(`#${n}: no DOI in the Concordance, left out`); continue; }
  const doi = bare(p.doi);
  for (const [k, v] of Object.entries(p)) {
    if (!/^doi_v\d+$/.test(k) || !v) continue;
    const c = conceptOfVersion.get(bare(v));
    if (c) { checked++; if (c !== doi) notes.push(`#${n}: version ${bare(v)} belongs to concept ${c}, Concordance says ${doi}; folder's concept used`); }
  }
  let concept = doi;
  for (const [k, v] of Object.entries(p)) { const c = /^doi_v\d+$/.test(k) && v && conceptOfVersion.get(bare(v)); if (c) concept = c; }
  papers[n] = { t: short(p.title), title: p.title, doi: `10.5281/zenodo.${concept}` };
}
const books = {}, unmapped = new Set();
for (const p of survey) {
  if (!papers[p.n]) continue;
  for (const f of p.books ?? []) {
    const b = BOOK_OF[f];
    if (!b) { unmapped.add(f); continue; }
    (books[b] ??= new Set()).add(p.n);
  }
}
for (const b of Object.keys(books)) books[b] = [...books[b]].sort(byNum);
if (unmapped.size) notes.push(`survey-map books with no app book (left out): ${[...unmapped].join(', ')}`);
// every paper the menu's worlds name must be here
const missing = BOOKS.flatMap((b) => b.worlds.flatMap(([, s]) => paperNumbers(s))).filter((n) => !papers[n]);
if (missing.length) notes.push(`world papers not in the Concordance: ${missing.join(', ')}`);

writeFileSync(out, JSON.stringify({ source: 'scripts/papers-json.mjs: Concordance (titles, concept DOIs) + survey map (books); world papers stay in src/app/book-menu-data.js', papers, books }) + '\n');
console.log(`papers ${Object.keys(papers).length}; concept ids checked against paper folders ${checked}; books ${Object.entries(books).map(([b, l]) => `${b} ${l.length}`).join(', ')}`);
for (const n of notes) console.log('note: ' + n);
