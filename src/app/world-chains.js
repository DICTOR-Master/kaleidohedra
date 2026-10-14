// Multi-shell chains: a 3D+ world (DICTO 2026-10-13) with DICTO's three published nestings, one at a time: the Chain of Karma (#22,
// doi:10.5281/zenodo.23310541), Spheres of Dharma (#23, doi:10.5281/zenodo.23310833) and the Bodhi Seed (#24,
// doi:10.5281/zenodo.23311353). Each has its views, a slider that pulls the pieces apart and a Crystal switch that makes the
// shells see-through. Geometry: seeds-data.js, built by scripts/build-seeds-data.py from the checked study data.
// Words in all 7 languages (i18n chains.*); DICTO's names stay untranslated.
import * as THREE from 'three';
import CHAINS_DATA from './seeds-data.js';
import MOVIE from './movie-names.js';
import { ROOF_FOLD_WORLD_SCALE as WS } from '../krp-core/src/geometry-extensions/roof-fold.js';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { addPanelMinimiser } from './panel-minimiser.js';
import { storageKey } from './site.js';

const CHAINS_KINDS = ['karma', 'dharma', 'bodhi'];
// Colours as in the papers' figures. Hexagonal caps of the fullerene layer gold (DICTO 2026-10-12).
export const ROLE = { ico: 0x5fd38a, cap: 0x5fd38a, lcap: 0x5fd38a, lj11: 0x5fd38a, npyr5: 0x5fd38a, core: 0xffc857, nfru3: 0xffc857, nfru5: 0xffc857,
  axe: 0x4dd0e1, laxe: 0x4dd0e1, nt1: 0x4dd0e1, nedge: 0x4dd0e1, fuji: 0xc792ea, cleo: 0xc792ea, lfuji: 0xc792ea, lcleo: 0xc792ea, npyr3: 0xc792ea,
  nface: 0xc792ea, ncap: 0xc792ea, nwedge: 0xdfe6f0, outer: 0x9fd8ff, copy: 0x5fd38a, centre: 0xffc857, B1: 0xffc857, B4: 0x4dd0e1,
  B5L: 0xc792ea, B5R: 0xf08fc0, B2: 0x4dd0e1, B3: 0xc792ea,
  // DICTO Dodeca
  dodeca: 0xffc857, j63: 0x5fd38a, pyr5: 0xffc857, tet: 0x5fd38a, ipyr5: 0xffc857, itet: 0x5fd38a, icleo: 0xc792ea, fpyr5: 0xb39ddb, ccleo: 0xffc857, col: 0x9575cd, tx: 0x4dd0e1, ty: 0x2e8b9a, bipyr: 0x9575cd, wedge: 0x4dd0e1, needle: 0xc792ea, star: 0xc792ea, unit: 0xffc857,
  // The 13s (the neighbours' copies in RD 13's blocks view, N, are dimmer)
  j11: 0x5fd38a, hasu: 0x5fd38a, idd: 0xffc857, vajra: 0xc792ea, rdCentre: 0xffc857, rd: 0x9fb4c8, rdA: 0x5fd38a, rdB: 0x4dd0e1,
  rdCentreN: 0x8a7440, rdAN: 0x3f7a57, rdBN: 0x33808a,
  toCentre: 0xffc857, toByHex: 0x4dd0e1, toBySquare: 0xc792ea, toCentreN: 0x8a7440, toByHexN: 0x33808a, toBySquareN: 0x6f5a8a,
  hexCentre: 0xffc857, hexByHex: 0x4dd0e1, hexByRhombus: 0x5fd38a, hexCentreN: 0x8a7440, hexByHexN: 0x33808a, hexByRhombusN: 0x3f7a57,
  // DICTO Icosahedral Octet
  admiral: 0x4dd0e1, icoSmall: 0xffc857, weirdstone: 0xc792ea, tadpole: 0xf08fc0, tet: 0xc792ea, frog: 0xf08fc0, pyroUp: 0xffc857,
  pyroDown: 0xc792ea, octGlass: 0x9fd8ff, tetGlass: 0x9fd8ff, lotusJewel: 0x5fd38a, voidDodeca: 0xffc857 };
// The 12-neighbour space-fillers' 13s (DICTO 2026-10-13): centre gold, the twelve cyan, the neighbouring blocks' copies dimmer.
Object.assign(ROLE, { jewelCentre: 0xffc857, jewelCell: 0x4dd0e1, stella: 0xc792ea });
for (const k of ['skewedRd13', 'bainRd13', 'bilinski13']) Object.assign(ROLE, { [`${k}Centre`]: 0xffc857, [`${k}Cell`]: 0x4dd0e1, [`${k}CentreN`]: 0x8a7440, [`${k}CellN`]: 0x33808a });
// Crystal: which roles turn see-through (the shells), per chain.
const CHAINS_GLASS = { karma: new Set(['ico']), dharma: new Set(['core', 'lj11']), bodhi: new Set(['copy']) };
// Always see-through: an outer form, and the octet's cells round the pyrochlore view's tetrahedra.
const ALWAYS_GLASS = new Set(['outer', 'octGlass', 'tetGlass']);
const EDGE_COLOR = 0x0b1220;
const lang = () => getSettings().language;

const centreOf = (P) => P.reduce((a, p) => a.map((c, i) => c + p[i] / P.length), [0, 0, 0]);

/** The build-movie order of a view's pieces (DICTO 2026-10-14): rings (one kind of piece at one distance) in the order of `named`
 *  (movie-names.js), else by distance; each ring from the top of a five-fold axis down, then round it. { seq, rank, ends }. */
export function filmOrder(list, named = []) {
  const all = list.flatMap((p) => p[1]), c0 = centreOf(all);
  const cen = list.map(([, V]) => centreOf(V).map((c, i) => c - c0[i]));
  const dist = cen.map((c) => Math.hypot(...c));
  const key = (n) => `${list[n][0]}@${dist[n].toFixed(2)}`;
  const ringIndex = new Map(named.map((r, i) => [r.ring, i]));
  const rings = new Map();
  list.forEach((_, n) => { const k = key(n); if (!rings.has(k)) rings.set(k, []); rings.get(k).push(n); });
  const order = [...rings.keys()].sort((a, b) => (ringIndex.get(a) ?? 1e9) - (ringIndex.get(b) ?? 1e9) || Math.min(...rings.get(a).map((n) => dist[n])) - Math.min(...rings.get(b).map((n) => dist[n])));
  // a five-fold axis: the centre piece's corner farthest from its middle (the icosahedron: any corner; the triacontahedron: a five-fold one)
  const c = dist.indexOf(Math.min(...dist)), Vc = list[c][1], mc = centreOf(Vc);
  const far = Vc.reduce((b, v) => (Math.hypot(...v.map((x, i) => x - mc[i])) > Math.hypot(...b.map((x, i) => x - mc[i])) ? v : b));
  const ax = far.map((x, i) => x - mc[i]); const al = Math.hypot(...ax); const a = ax.map((x) => x / al);
  const r1 = Math.abs(a[0]) < 0.9 ? [1, 0, 0] : [0, 1, 0];
  const u = [a[1] * r1[2] - a[2] * r1[1], a[2] * r1[0] - a[0] * r1[2], a[0] * r1[1] - a[1] * r1[0]]; const ul = Math.hypot(...u);
  const e1 = u.map((x) => x / ul), e2 = [a[1] * e1[2] - a[2] * e1[1], a[2] * e1[0] - a[0] * e1[2], a[0] * e1[1] - a[1] * e1[0]];
  const dot = (p, q) => p[0] * q[0] + p[1] * q[1] + p[2] * q[2];
  const polar = (n) => (dist[n] < 1e-9 ? 0 : Math.round(Math.acos(Math.max(-1, Math.min(1, dot(cen[n], a) / dist[n]))) * 1800 / Math.PI));
  const seq = [], ends = [];
  order.forEach((k, ri) => {
    seq.push(...rings.get(k).sort((p, q) => polar(p) - polar(q) || Math.atan2(dot(cen[p], e2), dot(cen[p], e1)) - Math.atan2(dot(cen[q], e2), dot(cen[q], e1))));
    ends.push({ at: seq.length, name: named[ringIndex.get(k) ?? -1]?.name ?? null });
  });
  const rank = new Map(seq.map((n, i) => [n, i]));
  const f = { seq, rank, ends };
  return f;
}

/** A world of nested shells (Multi-shell chains, DICTO Dodeca): data { kind: { views: { view: [[role, vertices, faces]] } } },
 *  words under '<prefix>.<kind>.<view>' and '<prefix>.note.<kind>'. */
export function createLayeredWorld({ scene, fitView = () => {}, name, data: DATA, kinds: KINDS, glassRoles: GLASS, prefix, defaultParts, centreGold = false, byFace = false, movie = null }) {
  const STORAGE_KEY = storageKey(name);
  const group = new THREE.Group();
  group.visible = false;
  scene.add(group);
  // size: for views that grow (a function of the size, DICTO Icosahedral Octet), how far out the network goes.
  const view = { kind: KINDS[0], part: { ...defaultParts }, apart: 0.3, shells: 1, crystal: false, size: 2, byFace: false };
  try {
    const d = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null');
    if (KINDS.includes(d?.kind)) view.kind = d.kind;
    for (const k of KINDS) if (DATA[k].views[d?.part?.[k]]) view.part[k] = d.part[k];
    if (Number.isFinite(d?.apart)) view.apart = Math.max(0, Math.min(1.2, d.apart));
    if (Number.isFinite(d?.shells)) view.shells = Math.max(0, Math.min(1, d.shells));
    view.crystal = d?.crystal === true;
    view.byFace = byFace && d?.byFace === true;
    if (Number.isInteger(d?.size)) view.size = Math.max(1, Math.min(4, d.size));
  } catch { /* corrupt or blocked storage: defaults */ }
  const save = () => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(view)); } catch { /* best-effort */ } };
  let active = false;
  let skeleton = false, opacity = 1; // the app's view modes: Solid, Translucent, Skeleton
  const solid = new THREE.MeshStandardMaterial({ vertexColors: true, side: THREE.DoubleSide, flatShading: true, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
  const glass = new THREE.MeshStandardMaterial({ vertexColors: true, side: THREE.DoubleSide, flatShading: true, transparent: true, opacity: 0.22, depthWrite: false });
  function clearGroup() {
    for (const child of [...group.children]) { group.remove(child); child.geometry.dispose(); if (child.isLineSegments) child.material.dispose(); }
  }
  // A view is a list of pieces, or a function of the size that builds one (cached per size).
  const grown = new Map();
  const growing = () => typeof DATA[view.kind].views[view.part[view.kind]] === 'function';
  const maxSize = () => DATA[view.kind].maxSize ?? 3;
  function viewList() {
    const v = DATA[view.kind].views[view.part[view.kind]];
    if (typeof v !== 'function') return v;
    const size = Math.min(view.size, maxSize()), key = `${view.kind}.${view.part[view.kind]}.${size}`;
    if (!grown.has(key)) grown.set(key, v(size));
    return grown.get(key);
  }
  // Pull apart by face (DICTO 2026-10-13: see the solids the many pieces form): each piece moves along the outward normal of
  // its outermost face, as far as that face's plane is from the middle, so all the pieces under one face of a shell's solid
  // lift off together as one tile. A piece whose outermost faces tie (under an edge or a corner) moves along their average.
  const faceMoves = new WeakMap();
  function faceMove(V, F, c0) {
    const P = V.map((p) => p.map((c, i) => c - c0[i])), pc = centreOf(P);
    const planes = F.map((f) => {
      const [a, b, c] = [P[f[0]], P[f[1]], P[f[2]]];
      const u = b.map((x, i) => x - a[i]), v = c.map((x, i) => x - a[i]);
      let n = [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]];
      const l = Math.hypot(...n) || 1; n = n.map((x) => x / l);
      if (n.reduce((s, x, i) => s + x * (a[i] - pc[i]), 0) < 0) n = n.map((x) => -x);
      return { n, d: n.reduce((s, x, i) => s + x * a[i], 0) };
    });
    const dmax = Math.max(...planes.map((q) => q.d));
    const sum = planes.filter((q) => q.d > dmax - 1e-6 * Math.max(1, dmax)).reduce((s, q) => s.map((x, i) => x + q.n[i]), [0, 0, 0]);
    const l = Math.hypot(...sum) || 1;
    return sum.map((x) => (x / l) * dmax);
  }
  // The build movie (DICTO 2026-10-14): the view built one piece at a time, ring by ring (rings: one kind of piece at one distance,
  // in the order of movie-names.js, else by distance), each ring from the top of a five-fold axis down, then round it. film: how
  // many pieces show (null: the movie is off and the view shows whole). The newest piece is orange.
  let film = null, playing = null;
  const films = new WeakMap();
  function filmOf(list) {
    if (films.has(list)) return films.get(list);
    const f = filmOrder(list, movie?.[view.kind]?.[view.part[view.kind]] ?? []);
    films.set(list, f);
    return f;
  }
  let radius = 1;
  function draw() {
    clearGroup();
    if (!active) return;
    const list = viewList();
    const all = list.flatMap((p) => p[1]);
    const c0 = centreOf(all);
    radius = Math.max(...all.map((p) => Math.hypot(...p.map((c, i) => c - c0[i]))));
    const buf = { solid: { pos: [], col: [], line: [] }, glass: { pos: [], col: [], line: [] } };
    const colour = new THREE.Color();
    // Shells (DICTO 2026-10-13): pieces grouped by the distance of their centres from the middle; the Top shell slider steps
    // through them, the chosen shell uppermost and every shell outside it lifted away (shown as crystal when Crystal is on).
    const dist = list.map(([, V]) => Math.hypot(...centreOf(V).map((c, i) => c - c0[i])));
    const levels = [...dist].sort((a, b) => a - b).reduce((acc, d) => (acc.length && d - acc[acc.length - 1] < radius * 0.06 ? acc : [...acc, d]), []);
    const shellOf = (d) => levels.reduce((best, l, i) => (Math.abs(l - d) < Math.abs(levels[best] - d) ? i : best), 0);
    // centreGold (the 13s, DICTO 2026-10-13: "the central 13th should always be gold"): the piece nearest the middle is gold, and
    // no other piece is (gold roles turn orange); blocks views keep each block's own centre role (gold, its copies dimmer).
    const GOLD = 0xffc857, ORANGE = 0xff9a52, DIM_GOLD = 0x8a7440;
    const centreIndex = centreGold ? dist.indexOf(Math.min(...dist)) : -1;
    const isCentreRole = (r) => /Centre(N)?$/.test(r) || /^(rdCentre|hexCentre|toCentre)/.test(r);
    const fm = film === null ? null : filmOf(list);
    list.forEach(([role, V, F], n) => {
      if (fm && fm.rank.get(n) >= film) return;
      const sh = shellOf(dist[n]); const top = Math.round(view.shells * (levels.length - 1));
      if (!fm && sh > top && !ALWAYS_GLASS.has(role) && !view.crystal) return;
      const see = ALWAYS_GLASS.has(role) || (view.crystal && (GLASS[view.kind]?.has(role) || sh > top));
      const b = see ? buf.glass : buf.solid;
      // Pulled apart: each piece moves out along the line from the centre through its own centre; see-through shells stay put.
      // By face: along the outward normal of the piece's outermost face instead (faceMove).
      let off = [0, 0, 0];
      if (!see && view.byFace) {
        if (!faceMoves.has(V)) faceMoves.set(V, faceMove(V, F, c0));
        off = faceMoves.get(V).map((c) => c * view.apart);
      } else if (!see) off = centreOf(V).map((c, i) => (c - c0[i]) * view.apart);
      const P = V.map((p) => p.map((c, i) => (c - c0[i] + off[i]) * WS));
      let hex = role === 'ncap' && V.length === 7 ? 0xffc857 : (ROLE[role] ?? 0xb8c4bd);
      if (centreGold) hex = n === centreIndex || (isCentreRole(role) && hex !== DIM_GOLD) ? GOLD : (hex === GOLD ? ORANGE : hex);
      if (fm && fm.rank.get(n) === film - 1) hex = ORANGE; // the newest piece of the movie
      colour.setHex(hex);
      for (const f of F) {
        for (let i = 1; i + 1 < f.length; i++) for (const k of [f[0], f[i], f[i + 1]]) { b.pos.push(...P[k]); b.col.push(colour.r, colour.g, colour.b); }
        f.forEach((k, i) => b.line.push(...P[k], ...P[f[(i + 1) % f.length]]));
      }
    });
    solid.transparent = opacity < 1; solid.opacity = opacity; solid.depthWrite = opacity >= 1; solid.needsUpdate = true;
    for (const [key, mat] of [['solid', solid], ['glass', glass]]) {
      const b = buf[key];
      if (!b.line.length) continue;
      const g = new THREE.BufferGeometry();
      g.setAttribute('position', new THREE.Float32BufferAttribute(b.pos, 3));
      g.setAttribute('color', new THREE.Float32BufferAttribute(b.col, 3));
      g.computeVertexNormals();
      const lg = new THREE.BufferGeometry();
      lg.setAttribute('position', new THREE.Float32BufferAttribute(b.line, 3));
      if (!skeleton) group.add(new THREE.Mesh(g, mat));
      group.add(new THREE.LineSegments(lg, new THREE.LineBasicMaterial(key === 'glass' ? { color: 0x9fa8c0, transparent: true, opacity: 0.55 } : { color: skeleton ? 0xcfe3ff : EDGE_COLOR })));
    }
    renderPanel();
  }
  const fit = () => fitView([0, 0, 0], radius * (1 + view.apart) * WS * 1.1);
  // A shape's own starting view (DATA[kind].viewDir), used when the shape is opened.
  const fitStart = () => fitView([0, 0, 0], radius * (1 + view.apart) * WS * 1.1, DATA[view.kind].viewDir ?? null);

  // ---- panel ----
  const panel = document.createElement('div');
  panel.id = `world${name}-panel`;
  panel.className = 'qc-panel';
  panel.innerHTML = `
    <div class="w4d-row"><label class="hull-pick"><span class="ch-view-label"></span> <select class="hull-select" data-select="part"></select></label></div>
    <div class="w4d-row ch-size-row"><label class="hull-pick"><span class="ch-size-label"></span> <input type="range" class="st-slider" min="1" max="3" step="1"></label></div>
    <div class="w4d-row ch-apart-row"><label class="hull-pick"><span class="ch-apart-label"></span> <input type="range" class="st-slider" min="0" max="1200" step="1"></label></div>
    <div class="w4d-row ch-shells-row"><label class="hull-pick"><span class="ch-shells-label"></span> <input type="range" class="st-slider" min="0" max="1000" step="1"></label></div>
    <div class="w4d-row ch-film-row"><label class="hull-pick"><span class="ch-film-label"></span> <input type="range" class="st-slider" min="0" max="1" step="1"></label></div>
    <div class="w4d-row st-note ch-film-note" aria-live="polite"></div>
    <div class="w4d-row w4d-options"><button type="button" data-chains-play></button><button type="button" data-chains-byface></button><button type="button" data-chains-crystal></button></div>
    <div class="w4d-row st-note"></div>`;
  document.body.appendChild(panel);
  addPanelMinimiser(panel, name);
  const partSelect = panel.querySelector('[data-select="part"]');
  const apartInput = panel.querySelector('.ch-apart-row input');
  const crystalBtn = panel.querySelector('[data-chains-crystal]');
  const byFaceBtn = panel.querySelector('[data-chains-byface]');
  byFaceBtn.hidden = !byFace;
  const shellsInput = panel.querySelector('.ch-shells-row input');
  const sizeInput = panel.querySelector('.ch-size-row input');
  const filmRow = panel.querySelector('.ch-film-row'), filmInput = filmRow.querySelector('input'), filmNote = panel.querySelector('.ch-film-note');
  const playBtn = panel.querySelector('[data-chains-play]');
  filmRow.hidden = playBtn.hidden = filmNote.hidden = !movie;
  // DICTO's piece names stay as they are; the classical pieces are translated.
  const PIECE = { axe: 'AXE', laxe: 'AXE', cleo: 'CLEO', lcleo: 'CLEO', fuji: 'FUJI', lfuji: 'FUJI', nfru3: 'Vajra (twist)', npyr5: 'Stupa', npyr3: 'Cleo-low',
    nfru5: 'Monkey Staff', nt1: 't1', nwedge: 'Vajra-blade', nedge: 'Sevenfold-blade', nface: 'Cleo-low 2', B1: 'Vajra (fine)', B2: 'Chatra', B3: 'Mudra',
    B4: 'Crown Jewel', B5L: 'Diadem L', B5R: 'Diadem R', lj11: 'J11', icleo: 'Cleo-Ico', fpyr5: 'Aetos', ccleo: 'Cleo-Ico', col: 'Kion', tx: 'Sphen', ty: 'Sphenion', bipyr: 'Atraktos' };  // names by DICTO 2026-10-15
  const pieceName = (role, V, L) => (role === 'ncap' && V.length === 7 ? 'Shield' : PIECE[role]
    ?? t({ ico: 'solid.icosahedron', core: 'solid.icosahedron', cap: 'piece.cap', ncap: 'piece.cap', lcap: 'piece.cap', centre: 'solid.rhombicTriacontahedron', copy: 'solid.rhombicTriacontahedron' }[role] ?? role, L));
  const solidName = (k, L) => (k === 'hecatodihedron' ? 'DICTO Truncated-Icosahedral Hecatodihedron' : t(`solid.${k}`, L));
  function renderFilm() {
    if (!movie || !active) return;
    const L = lang(), list = viewList(), fm = filmOf(list), n = film ?? fm.seq.length;
    filmInput.max = String(fm.seq.length); filmInput.value = String(n);
    panel.querySelector('.ch-film-label').textContent = t('chains.film.label', L);
    playBtn.textContent = playing ? `⏸ ${t('chains.film.pause', L)}` : `▶ ${t('chains.film.play', L)}`;
    if (film === null) { filmNote.textContent = ''; return; }
    const [role, V] = n ? list[fm.seq[n - 1]] : [null, []];
    const done = fm.ends.find((e) => e.at === n && e.name);
    filmNote.textContent = n ? `${t('chains.film.piece', L, { n, total: fm.seq.length, piece: pieceName(role, V, L) })}${done ? ` · ${solidName(done.name, L)}` : ''}` : '';
  }
  const stopFilm = () => { if (playing) { clearInterval(playing); playing = null; } };
  const setFilm = (n) => { film = n; draw(); renderFilm(); };
  filmInput.addEventListener('input', () => { stopFilm(); setFilm(Number(filmInput.value)); });
  playBtn.addEventListener('click', () => {
    if (playing) { stopFilm(); renderFilm(); return; }
    const fm = filmOf(viewList()), total = fm.seq.length;
    let n = film === null || film >= total ? 0 : film;
    const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
    // one piece at a time, quick enough that a large view takes about half a minute; with reduced motion, a ring at a time
    const step = reduce ? null : Math.max(1, Math.round(total / 300));
    playing = setInterval(() => {
      n = reduce ? (fm.ends.find((e) => e.at > n)?.at ?? total) : Math.min(total, n + step);
      setFilm(n);
      if (n >= total) { stopFilm(); renderFilm(); }
    }, reduce ? 900 : 100);
    renderFilm();
  });
  function renderPanel() {
    panel.classList.toggle('visible', active);
    if (!active) return;
    const L = lang();
    panel.querySelector('.ch-view-label').textContent = t('icosa.view', L);
    partSelect.innerHTML = Object.keys(DATA[view.kind].views)
      .map((v) => `<option value="${v}"${v === view.part[view.kind] ? ' selected' : ''}>${t(`${prefix}.${view.kind}.${v}`, L)}</option>`).join('');
    panel.querySelector('.ch-size-row').hidden = !growing();
    panel.querySelector('.ch-size-label').textContent = t('chains.size', L);
    sizeInput.max = String(maxSize()); sizeInput.value = String(Math.min(view.size, maxSize()));
    panel.querySelector('.ch-apart-label').textContent = t('icosa.apart', L);
    apartInput.value = String(Math.round(view.apart * 1000));
    panel.querySelector('.ch-shells-label').textContent = t('chains.shells', L);
    shellsInput.value = String(Math.round(view.shells * 1000));
    crystalBtn.textContent = t(view.crystal ? 'chains.crystal.on' : 'chains.crystal.off', L);
    byFaceBtn.textContent = t(view.byFace ? 'chains.byFace.on' : 'chains.byFace.off', L);
    byFaceBtn.classList.toggle('active', view.byFace);
    panel.querySelector('.st-note:not(.ch-film-note)').textContent = t(`${prefix}.note.${view.kind}`, L);
    renderFilm();
  }
  partSelect.addEventListener('change', () => { if (!DATA[view.kind].views[partSelect.value]) return; view.part[view.kind] = partSelect.value; stopFilm(); film = null; save(); draw(); fit(); renderFilm(); });
  apartInput.addEventListener('input', () => { view.apart = Number(apartInput.value) / 1000; save(); draw(); });
  apartInput.addEventListener('change', fit);
  shellsInput.addEventListener('input', () => { view.shells = Number(shellsInput.value) / 1000; save(); draw(); });
  shellsInput.addEventListener('change', fit);
  sizeInput.addEventListener('input', () => { view.size = Number(sizeInput.value); save(); draw(); fit(); });
  crystalBtn.addEventListener('click', () => { view.crystal = !view.crystal; save(); draw(); });
  byFaceBtn.addEventListener('click', () => { view.byFace = !view.byFace; save(); renderPanel(); draw(); });
  let shownLang = lang();
  onSettingsChange((st) => { if (st.language !== shownLang) { shownLang = st.language; if (active) renderPanel(); } });

  return {
    group,
    meshes: () => [],
    handleTap: () => false,
    /** Which of the world's shapes to show (the menu entries); anything else keeps the current one. */
    setChain(kind) {
      if (!KINDS.includes(kind) || kind === view.kind) return;
      view.kind = kind; save();
      stopFilm(); film = null;
      if (active) { draw(); fitStart(); renderFilm(); }
    },
    setActive(on) {
      if (on === active) return;
      active = on;
      group.visible = on;
      if (!on) { panel.classList.remove('visible'); stopFilm(); film = null; }
      draw();
      if (on) fitStart();
    },
    /** Back to each shape's first view (leaving the world, DICTO 2026-10-13). */
    resetView() {
      Object.assign(view, { part: { ...defaultParts }, apart: 0.3, shells: 1, crystal: false, size: 2, byFace: false }); save();
      if (active) { draw(); fit(); }
    },
    setSkeleton(on) { if (on !== skeleton) { skeleton = on; if (active) draw(); } },
    setTranslucent(o) { if (o !== opacity) { opacity = o; if (active) draw(); } },
    setLatticeView() {},
    shearChanged() {},
    get isEmpty() { return true; },
    clear() {},
  };
}

export function createChainsWorld({ scene, fitView }) {
  return createLayeredWorld({ scene, fitView, name: 'chains', data: CHAINS_DATA, kinds: CHAINS_KINDS, glassRoles: CHAINS_GLASS, prefix: 'chains', byFace: true, movie: MOVIE,
    defaultParts: { karma: 'lotus', dharma: 'cycle', bodhi: 'seed' } });
}

/** Points whose convex hull previews a chain in the DICTO menu (its first view's outline). */
export function chainPreviewPoints(kind) {
  const views = CHAINS_DATA[kind]?.views;
  return views ? Object.values(views)[0].flatMap((p) => p[1]) : [];
}
