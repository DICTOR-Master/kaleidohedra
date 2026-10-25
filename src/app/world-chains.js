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
  dodeca: 0xffc857, j63: 0x5fd38a, pyr5: 0xffc857, tet: 0x5fd38a, ipyr5: 0xffc857, itet: 0x5fd38a, icleo: 0xc792ea, fpyr5: 0xb39ddb, ccleo: 0xffc857, cspike: 0x4dd0e1, gpyr5: 0xc792ea, cvalley: 0x5fd38a, dprime: 0xf3ead6, col: 0x9575cd, tx: 0x4dd0e1, ty: 0x2e8b9a, bipyr: 0x9575cd, wedge: 0x4dd0e1, needle: 0xc792ea, star: 0xc792ea, unit: 0xffc857,
  // The 13s (the neighbours' copies in RD 13's blocks view, N, are dimmer)
  j11: 0x5fd38a, hasu: 0x5fd38a, idd: 0xffc857, vajra: 0xc792ea, rdCentre: 0xffc857, rd: 0x9fb4c8, rdA: 0x5fd38a, rdB: 0x4dd0e1,
  rdCentreN: 0x8a7440, rdAN: 0x3f7a57, rdBN: 0x33808a,
  toCentre: 0xffc857, toByHex: 0x4dd0e1, toBySquare: 0xc792ea, toCentreN: 0x8a7440, toByHexN: 0x33808a, toBySquareN: 0x6f5a8a,
  hexCentre: 0xffc857, hexByHex: 0x4dd0e1, hexByRhombus: 0x5fd38a, hexCentreN: 0x8a7440, hexByHexN: 0x33808a, hexByRhombusN: 0x3f7a57,
  // DICTO Icosahedral Octet
  admiral: 0x4dd0e1, icoSmall: 0xffc857, weirdstone: 0xc792ea, tadpole: 0xf08fc0, tet: 0xc792ea, frog: 0xf08fc0, pyroUp: 0xffc857,
  pyroDown: 0xc792ea, octGlass: 0x9fd8ff, tetGlass: 0x9fd8ff, lotusJewel: 0x5fd38a, voidDodeca: 0xffc857,
  // the AXE gap (DICTO 2026-10-23): Lotus Jewel green, Tricap purple, Unborn gold, AXE cyan (role axe, above)
  unborn: 0xffc857, tricap: 0xc792ea,
  // Mixed blocks: whole icosahedra green, Lotus Jewels dark green, whole dodecahedra gold, Unborns orange, transitions pink, AXE cyan
  mxIco: 0x5fd38a, mxJewel: 0x2e8b57, mxDodeca: 0xffc857, mxUnborn: 0xff9a52, mxTrans: 0xf08fc0,
  // Golden split (DICTO 2026-10-23): the big truncated octahedra green, the small ones orange, as in the study's pictures
  gsBig: 0x56a866, gsSmall: 0xe8913f,
  // DICTONIC's Delian bond (DICTO 2026-10-23): the tetrahedron pieces (Samson) gold, the octahedron pieces (Delilah) purple
  dlTet: 0xffc857, dlOct: 0xc792ea,
  // The Global Web of Bonds (DICTO 2026-10-25): the A kind's pieces gold, the B kind's blue, as in paper #53's figures
  gwA: 0xffc857, gwB: 0x6fa8ff };
// The 12-neighbour space-fillers' 13s (DICTO 2026-10-13): centre gold, the twelve cyan, the neighbouring blocks' copies dimmer.
Object.assign(ROLE, { jewelCentre: 0xffc857, jewelCell: 0x4dd0e1, stella: 0xc792ea });
for (const k of ['skewedRd13', 'bainRd13', 'bilinski13']) Object.assign(ROLE, { [`${k}Centre`]: 0xffc857, [`${k}Cell`]: 0x4dd0e1, [`${k}CentreN`]: 0x8a7440, [`${k}CellN`]: 0x33808a });
// Crystal: which roles turn see-through (the shells), per chain.
const CHAINS_GLASS = { karma: new Set(['ico']), dharma: new Set(['core', 'lj11']), bodhi: new Set(['copy']) };
// Always see-through: an outer form, and the octet's cells round the pyrochlore view's tetrahedra.
const ALWAYS_GLASS = new Set(['outer', 'octGlass', 'tetGlass']);
const EDGE_COLOR = 0x0b1220;
const SHRINK = 0.996; // see draw(): touching faces a hair apart
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
 *  words under '<prefix>.<kind>.<view>' and '<prefix>.note.<kind>'. hideable: { kind: role }, a kind's pieces that one button shows or
 *  hides (DICTO 2026-10-23: the octet's AXE; shown at first), words '<prefix>.toggle.<role>.on|off'; the button only where the view has them.
 *  A kind with options { patterns, block } (the octet's Mixed blocks, DICTO 2026-10-23) has growing views (size, { pattern, block, swap })
 *  and three more controls, only for it: a pattern menu, a block-size slider (1..block) and a Swap button; words '<prefix>.option.*' and
 *  '<prefix>.pattern.<pattern>'. Options may also say (the octet's Golden split, DICTO 2026-10-23): buttons (the patterns as a row of
 *  buttons, and the view menu hidden), blockPatterns (the patterns the block slider applies to; elsewhere it hides), flips (taps change
 *  single pieces: the kind's tap(tag, opts) gives the new state of the tapped face's tag, kept in opts.flips until a pattern control
 *  changes) and xray (the view is also told whether the X-ray cut is on, opts.xray, and redrawn when it turns). A piece may carry a 5th
 *  item { anchor, tags }: the point it pulls apart from and its shell distance (so the parts of one piece move together), and each
 *  face's tag for taps. links: { kind: [[name, action]] }, buttons that open those pieces where they live (Polyhedraverse), words
 *  '<prefix>.<kind>.links'; names are DICTO's and stay as they are (an entry [label, action, key] takes its words from key instead).
 *  DICTONIC (DICTO 2026-10-23): kindButtons puts the kinds in a row of buttons (words '<prefix>.kind.<kind>'); a kind with param
 *  { start, stops: [{ u, v, key }], value(u), caption(v, L) } has one big slider (0..1000, snapping to its stops; words
 *  '<prefix>.param.<kind>') whose value reaches its views as opts.param, with a caption under it; a kind with xray: true is told of
 *  the X-ray cut as opts.xray; hideRows (['size', 'shells']) hides those sliders. rowWords { size, shells } gives those two sliders
 *  their own words (DICTONIC: Layers, Top layer); a kind's maxSize may be a function (per device). A kind with web(size, o) (DICTONIC,
 *  DICTO 2026-10-25: the web of bonds) gets a Web button: the pieces turn see-through and a gold rod joins the anchors of every two
 *  pieces that share a face, its thickness by the face's area (web gives [[anchorA, anchorB, area]]); a kind with a param also gets
 *  a Loop button that runs its slider end to end and back (words '<prefix>.web.on|off|note', '<prefix>.loop.play|pause'). A web entry may
 *  carry a 4th item, the rod's colour (The Global Web of Bonds: one colour per kind of bond; gold otherwise), and a kind its own
 *  webNote (an i18n key: the 2D networks' bonds are shared edges). */
export function createLayeredWorld({ scene, fitView = () => {}, name, data: DATA, kinds: KINDS, glassRoles: GLASS, prefix, defaultParts, centreGold = false, byFace = false, movie = null, pinnedRoles = new Set(), hideable = {}, links = {}, openAction = () => {}, kindButtons = false, hideRows = [], rowWords = {}, foldNote = false, theorem = null }) {
  const STORAGE_KEY = storageKey(name);
  const group = new THREE.Group();
  group.visible = false;
  scene.add(group);
  // size: for views that grow (a function of the size, DICTO Icosahedral Octet), how far out the network goes.
  const defaultOpts = () => Object.fromEntries(KINDS.filter((k) => DATA[k].options).map((k) => [k, { pattern: DATA[k].options.patterns[0], block: DATA[k].options.startBlock ?? 1, swap: false, ...(DATA[k].options.flips ? { flips: {} } : {}) }]));
  const defaultParam = () => Object.fromEntries(KINDS.filter((k) => DATA[k].param).map((k) => [k, DATA[k].param.start]));
  const view = { kind: KINDS[0], part: { ...defaultParts }, apart: 0.3, shells: 1, crystal: false, size: 2, byFace: false, hidden: false, web: false, opts: defaultOpts(), param: defaultParam() };
  try {
    const d = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null');
    if (KINDS.includes(d?.kind)) view.kind = d.kind;
    for (const k of KINDS) if (DATA[k].views[d?.part?.[k]]) view.part[k] = d.part[k];
    if (Number.isFinite(d?.apart)) view.apart = Math.max(0, Math.min(1.2, d.apart));
    if (Number.isFinite(d?.shells)) view.shells = Math.max(0, Math.min(1, d.shells));
    view.crystal = d?.crystal === true;
    view.byFace = byFace && d?.byFace === true;
    view.hidden = d?.hidden === true;
    view.web = d?.web === true;
    if (Number.isInteger(d?.size)) view.size = Math.max(1, Math.min(6, d.size));
    for (const k of KINDS) if (DATA[k].param && Number.isFinite(d?.param?.[k])) view.param[k] = Math.max(0, Math.min(1000, Math.round(d.param[k])));
    for (const k of KINDS) {
      const o = DATA[k].options, s = d?.opts?.[k];
      if (!o || !s) continue;
      if (o.patterns.includes(s.pattern)) view.opts[k].pattern = s.pattern;
      if (Number.isInteger(s.block)) view.opts[k].block = Math.max(1, Math.min(o.block, s.block));
      view.opts[k].swap = s.swap === true;
      if (o.flips && s?.flips && typeof s.flips === 'object') view.opts[k].flips = Object.fromEntries(Object.entries(s.flips).filter(([, v]) => [0, 1, 2].includes(v)));
    }
  } catch { /* corrupt or blocked storage: defaults */ }
  const save = () => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(view)); } catch { /* best-effort */ } };
  let active = false;
  let skeleton = false, opacity = 1; // the app's view modes: Solid, Translucent, Skeleton
  const solid = new THREE.MeshStandardMaterial({ vertexColors: true, side: THREE.DoubleSide, flatShading: true, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
  const glass = new THREE.MeshStandardMaterial({ vertexColors: true, side: THREE.DoubleSide, flatShading: true, transparent: true, opacity: 0.22, depthWrite: false });
  glass.userData.hollow = true; // glass shells and helpers stay hollow in an X-ray cut (xray-caps.js)
  function clearGroup() {
    for (const child of [...group.children]) { group.remove(child); if (child.isInstancedMesh) child.dispose(); else child.geometry.dispose(); if (child.isLineSegments) child.material.dispose(); }
  }
  // A view is a list of pieces, or a function of the size that builds one (cached per size).
  const grown = new Map();
  const growing = () => typeof DATA[view.kind].views[view.part[view.kind]] === 'function';
  const maxSize = () => { const m = DATA[view.kind].maxSize ?? 3; return typeof m === 'function' ? m() : m; };
  function viewList() {
    const v = DATA[view.kind].views[view.part[view.kind]];
    if (typeof v !== 'function') return v;
    const size = Math.min(view.size, maxSize()), pm = DATA[view.kind].param;
    let o = view.opts[view.kind];
    if (xrayAware() || pm) o = { ...(o ?? {}), ...(xrayAware() ? { xray: xrayOn() } : {}), ...(pm ? { param: paramValue(), paramU: view.param[view.kind] } : {}) };
    const key = `${view.kind}.${view.part[view.kind]}.${size}${o ? `.${JSON.stringify(o)}` : ''}`;
    if (!grown.has(key)) { if (grown.size > 40) grown.clear(); grown.set(key, v(size, o)); }
    return grown.get(key);
  }
  const webAble = () => typeof DATA[view.kind].web === 'function';
  const webOn = () => view.web && webAble();
  function webList() {
    const size = Math.min(view.size, maxSize()), key = `web.${view.kind}.${size}.${view.param[view.kind] ?? ''}`;
    if (!grown.has(key)) { if (grown.size > 40) grown.clear(); grown.set(key, DATA[view.kind].web(size, { param: paramValue() })); }
    return grown.get(key);
  }
  const rodMat = new THREE.MeshStandardMaterial({ color: 0xffffff, metalness: 0.3, roughness: 0.45 });
  const rodGeo = new THREE.CylinderGeometry(1, 1, 1, 8, 1, true);
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
  // the app's X-ray cut (render.js's #section-enable), for kinds whose view shows its parts under it
  const xrayOn = () => !!document.getElementById('section-enable')?.checked;
  const xrayAware = () => !!(DATA[view.kind].options?.xray || DATA[view.kind].xray);
  // the kind's one big slider (DICTONIC): its position u (0..1000) and the value it stands for
  const paramValue = () => DATA[view.kind].param?.value(view.param[view.kind]);
  let looping = null, loopHold = 0;
  const stopLoop = () => { if (looping) { clearInterval(looping); looping = null; } loopHold = 0; };
  function startLoop() {
    const pm = DATA[view.kind].param; if (!pm) return;
    const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches, stops = pm.stops.map((st) => st.u).sort((a, b) => a - b);
    let dir = 1;
    looping = setInterval(() => {
      let u = view.param[view.kind];
      if (reduce) { const next = dir > 0 ? stops.find((x) => x > u) : [...stops].reverse().find((x) => x < u); if (next === undefined) { dir = -dir; return; } u = next; }
      else {
        // the loop holds about two seconds at the kind's decisive points (pm.pauseAt: Kelvin, the octet), so the switch can be seen
        if (loopHold > 0) { loopHold--; if (loopHold > 0) return; draw(); return; }
        const next = u + dir * 8, hit = (pm.pauseAt ?? []).find((p) => (p - u) * (p - next) < 0 || p === next);
        u = hit ?? next;
        if (hit !== undefined) loopHold = 16;
        if (u >= 1000 || u <= 0) { u = Math.max(0, Math.min(1000, u)); dir = -dir; }
      }
      view.param[view.kind] = u; draw();
    }, reduce ? 1500 : 120);
  }
  let solidMesh = null, solidTags = []; // the solid mesh drawn and each of its triangles' tag (taps)
  const hiddenRole = () => (view.hidden ? hideable[view.kind] ?? null : null);
  let drawn = {}; // pieces drawn, by role (the browser tests' probe)
  function draw() {
    drawn = {};
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
    const anchorOf = (p) => p[4]?.anchor ?? centreOf(p[1]);
    const dist = list.map((p) => Math.hypot(...anchorOf(p).map((c, i) => c - c0[i])));
    const levels = [...dist].sort((a, b) => a - b).reduce((acc, d) => (acc.length && d - acc[acc.length - 1] < radius * 0.06 ? acc : [...acc, d]), []);
    const shellOf = (d) => levels.reduce((best, l, i) => (Math.abs(l - d) < Math.abs(levels[best] - d) ? i : best), 0);
    // centreGold (the 13s, DICTO 2026-10-13: "the central 13th should always be gold"): the piece nearest the middle is gold, and
    // no other piece is (gold roles turn orange); blocks views keep each block's own centre role (gold, its copies dimmer).
    const GOLD = 0xffc857, ORANGE = 0xff9a52, DIM_GOLD = 0x8a7440;
    const centreIndex = centreGold ? dist.indexOf(Math.min(...dist)) : -1;
    const isCentreRole = (r) => /Centre(N)?$/.test(r) || /^(rdCentre|hexCentre|toCentre)/.test(r);
    const fm = film === null ? null : filmOf(list);
    solidMesh = null; solidTags = [];
    list.forEach(([role, V, F, , extra], n) => {
      if (fm && fm.rank.get(n) >= film) return;
      if (role === hiddenRole()) return;
      const sh = shellOf(dist[n]); const top = Math.round(view.shells * (levels.length - 1));
      if (!fm && sh > top && !ALWAYS_GLASS.has(role) && !view.crystal) return;
      const see = webOn() || ALWAYS_GLASS.has(role) || (view.crystal && (GLASS[view.kind]?.has(role) || sh > top));
      const b = see ? buf.glass : buf.solid;
      // Pulled apart: each piece moves out along the line from the centre through its own centre; see-through shells stay put.
      // By face: along the outward normal of the piece's outermost face instead (faceMove).
      let off = [0, 0, 0];
      if (!see && view.byFace) {
        if (!faceMoves.has(V)) faceMoves.set(V, faceMove(V, F, c0));
        off = faceMoves.get(V).map((c) => c * view.apart);
      } else if (!see && !pinnedRoles.has(role)) off = (extra?.anchor ?? centreOf(V)).map((c, i) => (c - c0[i]) * view.apart);   // pinned: marks that stay on their corner
      // Each solid piece is drawn 0.4% smaller about its own centre (DICTO 2026-10-15): faces two pieces share then sit a hair apart, so
      // they never fight in depth (the speckles the X-ray cut showed); too small to see in the closed views. Glass shells keep their size.
      const cV = see ? null : centreOf(V);
      const P = V.map((p) => p.map((c, i) => ((cV ? cV[i] + (c - cV[i]) * SHRINK : c) - c0[i] + off[i]) * WS));
      let hex = role === 'ncap' && V.length === 7 ? 0xffc857 : (ROLE[role] ?? 0xb8c4bd);
      if (centreGold) hex = n === centreIndex || (isCentreRole(role) && hex !== DIM_GOLD) ? GOLD : (hex === GOLD ? ORANGE : hex);
      if (fm && fm.rank.get(n) === film - 1) hex = ORANGE; // the newest piece of the movie
      colour.setHex(hex);
      drawn[role] = (drawn[role] ?? 0) + 1;
      F.forEach((f, fi) => {
        for (let i = 1; i + 1 < f.length; i++) {
          for (const k of [f[0], f[i], f[i + 1]]) { b.pos.push(...P[k]); b.col.push(colour.r, colour.g, colour.b); }
          if (b === buf.solid) solidTags.push(extra?.tags?.[fi] ?? null);
        }
        f.forEach((k, i) => b.line.push(...P[k], ...P[f[(i + 1) % f.length]]));
      });
    });
    glass.opacity = webOn() ? 0.1 : 0.22; // the web on: the pieces step back so the rods read
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
      if (!skeleton) { const m = new THREE.Mesh(g, mat); group.add(m); if (key === 'solid') solidMesh = m; }
      group.add(new THREE.LineSegments(lg, new THREE.LineBasicMaterial(key === 'glass' ? { color: 0x9fa8c0, transparent: true, opacity: webOn() ? 0.12 : 0.55 } : { color: skeleton ? 0xcfe3ff : EDGE_COLOR })));
    }
    // The web of bonds: one rod per shared face, between the two pieces' anchors, as thick as the face is large (radius ∝ √area), within
    // the layers shown; the rods move with Pulled apart as the anchors do.
    if (webOn()) {
      const top = Math.round(view.shells * (levels.length - 1)), rods = [];
      const where = (a) => a.map((c, i) => (c - c0[i] + (c - c0[i]) * view.apart) * WS);
      for (const [a, b, area, hex] of webList()) {
        if (area <= 1e-9 || shellOf(Math.hypot(...a.map((c, i) => c - c0[i]))) > top || shellOf(Math.hypot(...b.map((c, i) => c - c0[i]))) > top) continue;
        // outer layers fainter and thinner (DICTO 2026-10-25, after a TV test: the far rods made a tangle), the core's bonds brightest
        const lay = Math.max(shellOf(Math.hypot(...a.map((c, i) => c - c0[i]))), shellOf(Math.hypot(...b.map((c, i) => c - c0[i])))) / Math.max(1, levels.length - 1);
        rods.push([where(a), where(b), DATA[view.kind].webRadius * Math.sqrt(area) * WS * (1 - 0.4 * lay), 1 - 0.65 * lay, hex ?? 0xffc857]);
      }
      const inst = new THREE.InstancedMesh(rodGeo, rodMat, Math.max(1, rods.length));
      const m = new THREE.Matrix4(), q = new THREE.Quaternion(), up = new THREE.Vector3(0, 1, 0);
      const rc = new THREE.Color();
      rods.forEach(([pa, pb, r, bright, hex], i) => {
        const A = new THREE.Vector3(...pa), B = new THREE.Vector3(...pb), d = B.clone().sub(A), len = d.length();
        q.setFromUnitVectors(up, d.normalize());
        m.compose(A.add(B).multiplyScalar(0.5), q, new THREE.Vector3(r, len, r));
        inst.setMatrixAt(i, m);
        inst.setColorAt(i, rc.setHex(hex).multiplyScalar(bright));
      });
      inst.count = rods.length;
      group.add(inst);
      drawn.web = rods.length;
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
    <div class="w4d-row w4d-options ch-kind-buttons">${KINDS.map((k) => `<button type="button" data-chains-kind="${k}"></button>`).join('')}</div>
    <div class="w4d-row ch-param-row"><label class="hull-pick"><span class="ch-param-label"></span> <input type="range" class="st-slider" min="0" max="1000" step="1"></label></div>
    <div class="w4d-row ch-param-caption" aria-live="polite"></div>
    <div class="w4d-row"><label class="hull-pick"><span class="ch-view-label"></span> <select class="hull-select" data-select="part"></select></label></div>
    <div class="w4d-row ch-size-row"><label class="hull-pick"><span class="ch-size-label"></span> <input type="range" class="st-slider" min="1" max="3" step="1"></label></div>
    <div class="w4d-row ch-pattern-row"><label class="hull-pick"><span class="ch-pattern-label"></span> <select class="hull-select" data-select="pattern"></select></label></div>
    <div class="w4d-row w4d-options ch-pattern-buttons"></div>
    <div class="w4d-row ch-block-row"><label class="hull-pick"><span class="ch-block-label"></span> <input type="range" class="st-slider" min="1" max="3" step="1"></label></div>
    <div class="w4d-row ch-apart-row"><label class="hull-pick"><span class="ch-apart-label"></span> <input type="range" class="st-slider" min="0" max="1200" step="1"></label></div>
    <div class="w4d-row ch-shells-row"><label class="hull-pick"><span class="ch-shells-label"></span> <input type="range" class="st-slider" min="0" max="1000" step="1"></label></div>
    <div class="w4d-row ch-film-row"><label class="hull-pick"><span class="ch-film-label"></span> <input type="range" class="st-slider" min="0" max="1" step="1"></label></div>
    <div class="w4d-row st-note ch-film-note" aria-live="polite"></div>
    <div class="w4d-row w4d-options ch-options"><button type="button" data-chains-play></button><button type="button" data-chains-byface></button><button type="button" data-chains-crystal></button><button type="button" data-chains-hide></button><button type="button" data-chains-swap></button><button type="button" data-chains-web></button><button type="button" data-chains-loop></button></div>
    <div class="w4d-row w4d-options ch-links"><span class="ch-links-label hull-pick"></span> </div>
    <div class="w4d-row st-note"></div>`;
  document.body.appendChild(panel);
  addPanelMinimiser(panel, name);
  // theorem (DICTONIC, DICTO 2026-10-25): a statement + live evidence block under the slider's caption (dictonic-theorem.js)
  const thm = theorem ? theorem(panel) : null;
  // foldNote (DICTONIC, DICTO 2026-10-25): the note shows one line; a tap opens or closes it
  const noteEl = panel.querySelector('.st-note:not(.ch-film-note)');
  if (foldNote) { noteEl.classList.add('fold'); noteEl.addEventListener('click', () => noteEl.classList.toggle('open')); }
  const partSelect = panel.querySelector('[data-select="part"]');
  const paramInput = panel.querySelector('.ch-param-row input');
  const apartInput = panel.querySelector('.ch-apart-row input');
  const crystalBtn = panel.querySelector('[data-chains-crystal]');
  const byFaceBtn = panel.querySelector('[data-chains-byface]');
  byFaceBtn.hidden = !byFace;
  const hideBtn = panel.querySelector('[data-chains-hide]');
  const patternSelect = panel.querySelector('[data-select="pattern"]'), blockInput = panel.querySelector('.ch-block-row input');
  const swapBtn = panel.querySelector('[data-chains-swap]');
  const webBtn = panel.querySelector('[data-chains-web]'), loopBtn = panel.querySelector('[data-chains-loop]');
  const shellsInput = panel.querySelector('.ch-shells-row input');
  const sizeInput = panel.querySelector('.ch-size-row input');
  const filmRow = panel.querySelector('.ch-film-row'), filmInput = filmRow.querySelector('input'), filmNote = panel.querySelector('.ch-film-note');
  const playBtn = panel.querySelector('[data-chains-play]');
  filmRow.hidden = playBtn.hidden = filmNote.hidden = !movie;
  // DICTO's piece names stay as they are; the classical pieces are translated.
  const PIECE = { axe: 'AXE', laxe: 'AXE', cleo: 'CLEO', lcleo: 'CLEO', fuji: 'FUJI', lfuji: 'FUJI', nfru3: 'Vajra (twist)', npyr5: 'Stupa', npyr3: 'Cleo-low',
    nfru5: 'Monkey Staff', nt1: 't1', nwedge: 'Vajra-blade', nedge: 'Sevenfold-blade', nface: 'Cleo-low 2', B1: 'Vajra (fine)', B2: 'Chatra', B3: 'Mudra',
    B4: 'Crown Jewel', B5L: 'Diadem L', B5R: 'Diadem R', lj11: 'J11', icleo: 'Cleo-Ico', fpyr5: 'Aetos', ccleo: 'Cleo-Ico', cspike: 'Cleo-Ico', col: 'Kion', tx: 'Sphen', ty: 'Sphenion', bipyr: 'Atraktos', upFrustum: 'Monkey Staff B' };  // names by DICTO 2026-10-15; Monkey Staff B 2026-10-19 (UP)
  const pieceName = (role, V, L) => (role === 'ncap' && V.length === 7 ? 'Shield' : PIECE[role]
    ?? t({ ico: 'solid.icosahedron', core: 'solid.icosahedron', cap: 'piece.cap', ncap: 'piece.cap', lcap: 'piece.cap', gpyr5: 'piece.inwardPyr5', cvalley: 'piece.valleyTet', dprime: 'solid.dodecahedron', centre: 'solid.rhombicTriacontahedron', copy: 'solid.rhombicTriacontahedron' }[role] ?? role, L));
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
    panel.querySelector('.ch-view-label').closest('.w4d-row').hidden = !!DATA[view.kind].options?.buttons || kindButtons;
    const kb = panel.querySelector('.ch-kind-buttons');
    kb.hidden = !kindButtons;
    if (kindButtons) kb.querySelectorAll('[data-chains-kind]').forEach((x) => { x.textContent = t(`${prefix}.kind.${x.dataset.chainsKind}`, L); x.classList.toggle('active', x.dataset.chainsKind === view.kind); });
    const pm = DATA[view.kind].param;
    panel.querySelector('.ch-param-row').hidden = panel.querySelector('.ch-param-caption').hidden = !pm;
    if (pm) {
      panel.querySelector('.ch-param-label').textContent = t(`${prefix}.param.${view.kind}`, L);
      paramInput.value = String(view.param[view.kind]);
      panel.querySelector('.ch-param-caption').textContent = pm.caption(paramValue(), L) + (webOn() ? ` · ${t(DATA[view.kind].webNote ?? `${prefix}.web.note`, L)}` : '');
    }
    panel.querySelector('.ch-view-label').textContent = t('icosa.view', L);
    partSelect.innerHTML = Object.keys(DATA[view.kind].views)
      .map((v) => `<option value="${v}"${v === view.part[view.kind] ? ' selected' : ''}>${t(`${prefix}.${view.kind}.${v}`, L)}</option>`).join('');
    panel.querySelector('.ch-size-row').hidden = !growing() || hideRows.includes('size');
    panel.querySelector('.ch-shells-row').hidden = hideRows.includes('shells');
    panel.querySelector('.ch-size-label').textContent = t(rowWords.size ?? 'chains.size', L);
    sizeInput.max = String(maxSize()); sizeInput.value = String(Math.min(view.size, maxSize()));
    panel.querySelector('.ch-apart-label').textContent = t('icosa.apart', L);
    apartInput.value = String(Math.round(view.apart * 1000));
    panel.querySelector('.ch-shells-label').textContent = t(rowWords.shells ?? 'chains.shells', L);
    webBtn.hidden = !webAble(); loopBtn.hidden = !pm;
    if (webAble()) { webBtn.textContent = t(`${prefix}.web.${view.web ? 'on' : 'off'}`, L); webBtn.classList.toggle('active', view.web); }
    if (pm) { loopBtn.textContent = looping ? `⏸ ${t(`${prefix}.loop.pause`, L)}` : `▶ ${t(`${prefix}.loop.play`, L)}`; loopBtn.classList.toggle('active', !!looping); }
    shellsInput.value = String(Math.round(view.shells * 1000));
    crystalBtn.textContent = t(view.crystal ? 'chains.crystal.on' : 'chains.crystal.off', L);
    byFaceBtn.textContent = t(view.byFace ? 'chains.byFace.on' : 'chains.byFace.off', L);
    byFaceBtn.classList.toggle('active', view.byFace);
    const opt = DATA[view.kind].options, o = view.opts[view.kind], showOpt = !!opt && growing();
    panel.querySelector('.ch-pattern-row').hidden = panel.querySelector('.ch-block-row').hidden = swapBtn.hidden = !showOpt;
    const buttons = panel.querySelector('.ch-pattern-buttons');
    buttons.hidden = !showOpt || !opt.buttons;
    if (showOpt && opt.buttons) {
      panel.querySelector('.ch-pattern-row').hidden = true;
      panel.querySelector('.ch-block-row').hidden = !(opt.blockPatterns ?? opt.patterns).includes(o.pattern);
      buttons.innerHTML = opt.patterns.map((p) => `<button type="button" data-chains-pattern="${p}" class="${p === o.pattern ? 'active' : ''}">${t(`${prefix}.pattern.${p}`, L)}</button>`).join('');
    }
    if (showOpt) {
      panel.querySelector('.ch-pattern-label').textContent = t(`${prefix}.option.pattern`, L);
      patternSelect.innerHTML = opt.patterns.map((p) => `<option value="${p}"${p === o.pattern ? ' selected' : ''}>${t(`${prefix}.pattern.${p}`, L)}</option>`).join('');
      panel.querySelector('.ch-block-label').textContent = t(`${prefix}.option.block`, L);
      blockInput.max = String(opt.block); blockInput.value = String(o.block);
      swapBtn.textContent = t(`${prefix}.option.swap.${o.swap ? 'on' : 'off'}`, L); swapBtn.classList.toggle('active', o.swap);
      if (opt.buttons) swapBtn.textContent = t(`${prefix}.${view.kind}.swap.${o.swap ? 'on' : 'off'}`, L);
      if (opt.buttons) swapBtn.hidden = o.pattern === 'smooth';   // nothing keyed: no way for the keys to point
    }
    const lk = links[view.kind], linkRow = panel.querySelector('.ch-links');
    linkRow.hidden = !lk;
    if (lk) {
      linkRow.querySelector('.ch-links-label').textContent = t(`${prefix}.${view.kind}.links`, L);
      linkRow.querySelectorAll('button').forEach((x) => x.remove());
      for (const [label, action, key] of lk) { const btn = document.createElement('button'); btn.type = 'button'; btn.dataset.chainsLink = action; btn.textContent = key ? t(key, L) : label; linkRow.append(btn); }
    }
    const hr = hideable[view.kind];
    hideBtn.hidden = !hr || !viewList().some((p) => p[0] === hr);
    if (hr) { hideBtn.textContent = t(`${prefix}.toggle.${hr}.${view.hidden ? 'off' : 'on'}`, L); hideBtn.classList.toggle('active', !view.hidden); }
    panel.querySelector('.st-note:not(.ch-film-note)').textContent = t(`${prefix}.note.${view.kind}`, L);
    thm?.update({ kind: view.kind, u: view.param[view.kind] ?? 0, v: pm ? paramValue() : null, L, paused: loopHold > 0 });
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
  hideBtn.addEventListener('click', () => { view.hidden = !view.hidden; save(); draw(); });
  // the web starts at 2 layers (more is a tangle at first sight; the Layers slider still goes higher)
  webBtn.addEventListener('click', () => { view.web = !view.web; if (view.web && view.size > 2) view.size = 2; save(); draw(); fit(); });
  // Loop (DICTO 2026-10-25, "the rhythm of the loop"): the kind's slider runs from one end to the other and back, without end, until
  // paused (or the kind or world changes); with reduced motion it steps from stop to stop instead of sliding.
  loopBtn.addEventListener('click', () => { if (looping) stopLoop(); else startLoop(); renderPanel(); });
  // a pattern control starts the pattern afresh: single pieces tapped (flips) are let go
  const unflip = (o) => { if (o.flips) o.flips = {}; };
  patternSelect.addEventListener('change', () => { const o = view.opts[view.kind]; if (!o || !DATA[view.kind].options.patterns.includes(patternSelect.value)) return; o.pattern = patternSelect.value; unflip(o); save(); draw(); });
  panel.querySelector('.ch-pattern-buttons').addEventListener('click', (e) => {
    const p = e.target.closest('[data-chains-pattern]')?.dataset.chainsPattern, o = view.opts[view.kind];
    if (!p || !o || !DATA[view.kind].options.patterns.includes(p)) return;
    o.pattern = p; unflip(o); save(); draw();
  });
  blockInput.addEventListener('input', () => { const o = view.opts[view.kind]; if (!o) return; o.block = Number(blockInput.value); unflip(o); save(); draw(); });
  swapBtn.addEventListener('click', () => { const o = view.opts[view.kind]; if (!o) return; o.swap = !o.swap; unflip(o); save(); draw(); });
  panel.querySelector('.ch-kind-buttons').addEventListener('click', (e) => {
    const k = e.target.closest('[data-chains-kind]')?.dataset.chainsKind;
    if (!k || k === view.kind) return;
    view.kind = k; save(); stopFilm(); stopLoop(); film = null; draw(); fitStart();
  });
  // the one big slider: it snaps to a stop within 2% of it (no step buttons, DICTO); the picture is framed again when it is let go
  paramInput.addEventListener('input', () => {
    const pm = DATA[view.kind].param; if (!pm) return;
    stopLoop();
    let u = Number(paramInput.value);
    const stop = pm.stops.find((st) => Math.abs(st.u - u) <= 20);
    if (stop) { u = stop.u; paramInput.value = String(u); }
    if (u === view.param[view.kind]) return;
    view.param[view.kind] = u; save(); draw();
  });
  paramInput.addEventListener('change', fit);
  panel.querySelector('.ch-links').addEventListener('click', (e) => { const a = e.target.closest('[data-chains-link]')?.dataset.chainsLink; if (a) openAction(a); });
  // X-ray turned on or off (the ⛶ button; render.js sets the box after its own click handler): kinds that show their parts redraw
  let shownXray = xrayOn();
  document.addEventListener('click', (e) => {
    if (!e.target.closest?.('#xray-toggle')) return;
    setTimeout(() => { if (xrayOn() !== shownXray) { shownXray = xrayOn(); if (active && xrayAware()) draw(); } }, 0);
  });
  let shownLang = lang();
  onSettingsChange((st) => { if (st.language !== shownLang) { shownLang = st.language; if (active) renderPanel(); } });

  return {
    group,
    meshes: () => (DATA[view.kind].tap && solidMesh ? [solidMesh] : []),
    /** A tap on a tagged face (the Golden split's hexagons) steps that one piece: the kind's tap(tag, opts) gives its new state. */
    handleTap(hit, mode) {
      const o = view.opts[view.kind], tap = DATA[view.kind].tap;
      if (mode !== 'build' || !tap || !o?.flips || hit?.object !== solidMesh) return false;
      const tag = solidTags[hit.faceIndex];
      if (!tag) return false;
      o.flips = { ...o.flips, [tag]: tap(tag, o) };
      save(); draw();
      return true;
    },
    /** Open on one of the current shape's views (a link from another world: Vajrayana's Cleo star opens Theaetetus's 'cleostar'). */
    openView(name) {
      if (!DATA[view.kind].views[name]) return;
      view.part[view.kind] = name; stopFilm(); film = null; save();
      if (active) { draw(); fit(); renderFilm(); renderPanel(); }
    },
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
      if (!on) { panel.classList.remove('visible'); stopFilm(); stopLoop(); film = null; }
      draw();
      if (on) fitStart();
    },
    /** Back to each shape's first view (leaving the world, DICTO 2026-10-13). */
    resetView() {
      stopLoop(); Object.assign(view, { part: { ...defaultParts }, apart: 0.3, shells: 1, crystal: false, size: 2, byFace: false, hidden: false, web: false, opts: defaultOpts(), param: defaultParam() }); save();
      if (active) { draw(); fit(); }
    },
    setSkeleton(on) { if (on !== skeleton) { skeleton = on; if (active) draw(); } },
    setTranslucent(o) { if (o !== opacity) { opacity = o; if (active) draw(); } },
    setLatticeView() {},
    shearChanged() {},
    get isEmpty() { return true; },
    clear() {},
    /** For the browser tests (?probe): what is shown, and the pieces drawn by role. */
    probe: () => ({ web: webOn(), looping: !!looping, maxSize: maxSize(), param: DATA[view.kind].param ? { u: view.param[view.kind], value: paramValue() } : null, xray: xrayOn(), flips: view.opts[view.kind]?.flips ? Object.keys(view.opts[view.kind].flips).length : null, kind: view.kind, part: view.part[view.kind], size: Math.min(view.size, maxSize()), crystal: view.crystal, hidden: hiddenRole(), opts: view.opts[view.kind] ? { ...view.opts[view.kind] } : null, drawn: { ...drawn } }),
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
