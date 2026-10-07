// Euclid–Kepler–Pacioli Cell Network: a 3D world of its own on the Euclid–Kepler–Pacioli cell (DISCOVERIES.md #8,
// geometry in geometry-extensions/roof-fold.js). Sites are a simple cubic
// lattice of period phi^2 (icosahedron edge 1). Seven pieces, one at a time,
// several per site: cube, dodecahedron, icosahedron, great stellated dodecahedron (the star),
// octahedron, stella octangula and Pacioli's golden rectangles. Tap a
// solid to add the chosen one at that site, or across the face when it's
// already there; long-press removes. The View picker redraws the same build
// as alternating patterns (site colourings, each with its own space group),
// in X-ray (inner solids through outer ones) or as the exact merged surface
// of the dodecahedra. Lives outside the shear
// group: shearing would break the icosahedra.
import * as THREE from 'three';
import { ekpWindowsSolid, neighbourStellas, stretchedDodeca, PHI, ROOF_FOLD_KINDS, ROOF_FOLD_COLOURS, ROOF_FOLD_WORLD_SCALE as WS, roofFoldSolids, mergedDodecaSurface, mergedDodecaEdges, ROOF_FOLD_PATTERNS, siteParity, turnPoint } from '../geometry-extensions/roof-fold.js';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { addPanelMinimiser } from './panel-minimiser.js';

const STORAGE_KEY = 'kaleidohedra-roof-fold-world';
const VIEWS = ['built', 'starIco', 'dodecaStar', 'checker', 'merged'];
// Studies of the cell (DICTO, 2026-10-08): shapes shown on their own, building paused.
const STUDIES = ['off', 'windows', 'windowsStellas', 'stretch'];
const STRETCH_MAX = 2.6;
const STRETCH_SNAPS = [2 / PHI, 2]; // one edge (squares), the lattice spacing
const KIND_COLOR = ROOF_FOLD_COLOURS;
const PARITY_COLOR = [0xffc857, 0x7cc4ff];
const OCTANT_COLOR = [0xffc857, 0x7cc4ff, 0xff7a59, 0x5fd38a, 0xc792ea, 0x4dd0e1, 0xf06292, 0xe8eef7];
const PATTERNS = Object.keys(ROOF_FOLD_PATTERNS);
const VERTICES = ['off', 'cube', 'all'];
const ALTERNATING = ['starIco', 'dodecaStar', 'checker'];
// X-ray: inside to outside, the same wrap order as the Piece list. The innermost kind in the
// build stays solid; each one further out fades more.
const NESTING = ROOF_FOLD_KINDS;
const xrayOpacity = (rank) => (rank === 0 ? 1 : Math.max(0.14, 0.5 - 0.08 * (rank - 1)));
const FIRST_COLOR = 0x00e5ff;
const GHOST_COLOR = 0x9de0ff;
const EDGE_COLOR = 0x0b1220;
const NODE_COLOR = 0xe8eef7;
const ODD_SHADE = 0.62;
const lang = () => getSettings().language;
const siteKey = (s) => s.join();
const solidKey = (s, kind) => `${s.join()},${kind}`;
const DIRECTIONS = [];
for (const x of [-1, 0, 1]) for (const y of [-1, 0, 1]) for (const z of [-1, 0, 1]) if (x || y || z) DIRECTIONS.push([x, y, z]);

export function createRoofFoldWorld({ scene, onChange = () => {}, showHudPrompt = () => {}, fitView = () => {}, shear = () => null }) {
  const SOLIDS = roofFoldSolids();
  const storageKey = STORAGE_KEY;
  const group = new THREE.Group();
  group.visible = false;
  scene.add(group);

  // ---- state ----
  const solids = new Map(); // solidKey -> { site: [x, y, z], kind }
  const view = { piece: 'dodeca', mode: 'built', parity: false, vertices: 'off', pattern: 'xyz', xray: false, turnOdd: false, study: 'off', stretch: STRETCH_SNAPS[0], studyShear: 'copies' };
  let active = false;
  let skeleton = false;
  let opacity = 1;
  let latticeView = false;
  let infoOpen = false;

  function setFromJSON(data) {
    solids.clear();
    for (const s of Array.isArray(data?.solids) ? data.solids : []) {
      if (!Array.isArray(s?.site) || s.site.length !== 3 || !s.site.every(Number.isInteger) || !ROOF_FOLD_KINDS.includes(s.kind)) continue;
      solids.set(solidKey(s.site, s.kind), { site: [...s.site], kind: s.kind });
    }
  }
  const toJSON = () => ({ solids: [...solids.values()] });
  try {
    const data = JSON.parse(localStorage.getItem(storageKey) ?? 'null');
    if (data) {
      setFromJSON(data);
      if (ROOF_FOLD_KINDS.includes(data.view?.piece)) view.piece = data.view.piece;
      if (VIEWS.includes(data.view?.mode)) view.mode = data.view.mode;
      view.parity = data.view?.parity === true;
      if (VERTICES.includes(data.view?.vertices)) view.vertices = data.view.vertices;
      if (PATTERNS.includes(data.view?.pattern)) view.pattern = data.view.pattern;
      view.xray = data.view?.xray === true;
      view.turnOdd = data.view?.turnOdd === true;
      if (STUDIES.includes(data.view?.study)) view.study = data.view.study;
      if (['copies', 'solid'].includes(data.view?.studyShear)) view.studyShear = data.view.studyShear;
      if (Number.isFinite(data.view?.stretch)) view.stretch = Math.max(0, Math.min(STRETCH_MAX, data.view.stretch));
    }
  } catch { /* corrupt or blocked storage: start empty */ }
  function save() {
    try { localStorage.setItem(storageKey, JSON.stringify({ version: 1, ...toJSON(), view })); } catch { /* best-effort */ }
  }
  const sites = () => { const m = new Map(); for (const s of solids.values()) m.set(siteKey(s.site), s.site); return [...m.values()]; };

  // ---- what to draw ----
  // Octants has 8 colours, so it's only offered in Checkerboard; the two-solid views fall back to x+y+z.
  const patternName = () => (view.pattern === 'octants' && view.mode !== 'checker' ? 'xyz' : view.pattern);
  const colourIndex = (site) => ROOF_FOLD_PATTERNS[patternName()].of(...site);
  const odd = (site) => colourIndex(site) % 2 === 1;
  const shade = (hex, site) => { const c = new THREE.Color(hex); return view.parity && odd(site) ? c.multiplyScalar(ODD_SHADE) : c; };
  function drawList() {
    const built = [...solids.values()];
    switch (view.mode) {
      case 'starIco': return sites().map((site) => ({ site, kind: odd(site) ? 'ico' : 'star' }));
      case 'dodecaStar': return sites().map((site) => ({ site, kind: odd(site) ? 'star' : 'dodeca' }));
      default: return built;
    }
  }
  const colourOf = (item) => (view.mode === 'checker'
    ? new THREE.Color((patternName() === 'octants' ? OCTANT_COLOR : PARITY_COLOR)[colourIndex(item.site)])
    : shade(KIND_COLOR[item.kind], item.site));

  // ---- drawing ----
  const pieceMaterial = new THREE.MeshStandardMaterial({ vertexColors: true, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
  const ghostMaterial = new THREE.MeshStandardMaterial({ color: GHOST_COLOR, transparent: true, opacity: 0.18, depthWrite: false, side: THREE.DoubleSide });
  const firstMaterial = new THREE.MeshStandardMaterial({ color: FIRST_COLOR, transparent: true, opacity: 0.14, depthWrite: false, side: THREE.DoubleSide });
  const nodeGeometry = new THREE.SphereGeometry(0.07, 12, 8);
  const nodeMaterial = new THREE.MeshStandardMaterial({ color: NODE_COLOR });
  const pickTargets = [];
  function clearGroup() {
    for (const child of [...group.children]) {
      group.remove(child);
      if (child.geometry !== nodeGeometry) child.geometry.dispose();
      if (child.isLineSegments) child.material.dispose();
      if (child.isInstancedMesh) child.dispose();
      if (child.userData.ownMaterial) child.material.dispose();
    }
    pickTargets.length = 0;
  }
  // One mesh for a list of polygons ({ polygon, offset, colour, record }), plus its edge lines.
  function meshOf(polys, edges, material, edgeColor, tag) {
    const pos = [], col = [], line = [];
    const records = [];
    for (const { polygon, offset, colour, record } of polys) {
      const P = polygon.map((p) => p.map((c, a) => c * WS + offset[a]));
      for (let i = 1; i + 1 < P.length; i++) {
        for (const p of [P[0], P[i], P[i + 1]]) { pos.push(...p); col.push(colour.r, colour.g, colour.b); }
        records.push(record);
      }
    }
    for (const { a, b, offset } of edges) line.push(...a.map((c, i) => c * WS + offset[i]), ...b.map((c, i) => c * WS + offset[i]));
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    g.setAttribute('color', new THREE.Float32BufferAttribute(col, 3));
    g.computeVertexNormals();
    const mesh = new THREE.Mesh(g, material);
    mesh.userData.roofFold = tag;
    mesh.userData.records = records;
    const lg = new THREE.BufferGeometry();
    lg.setAttribute('position', new THREE.Float32BufferAttribute(line, 3));
    return [mesh, new THREE.LineSegments(lg, new THREE.LineBasicMaterial({ color: edgeColor }))];
  }
  // The Shear panel moves the lattice, not the pieces: each cell centre goes
  // through the shear (3×3 rows, or null when there is none) and every piece
  // stays a true regular solid.
  const centreCell = (site) => { const A = shear(); const c = site.map((x) => 2 * x); return A ? A.map((row) => row[0] * c[0] + row[1] * c[1] + row[2] * c[2]) : c; };
  const centreOf = (site) => centreCell(site).map((c) => c * WS);
  // Odd sites are turned a quarter about z when the view asks for it, the merged outer surface included.
  const turnedSite = (site) => view.turnOdd && siteParity(...site) === 1;
  const turnFor = (site) => (turnedSite(site) ? turnPoint : (p) => p);
  // Faces of one kind lying in a face plane of another (same outward side): 8 icosahedron faces lie
  // in the octahedron's planes, and the octahedron's in the tetrahedra's. In the opaque view such an
  // inner face is hidden by the outer piece in the same cell, so it isn't drawn (it would flicker).
  const planeKey = (f) => {
    const n = [0, 1, 2].map((k) => { const a = f[0], b = f[1], c = f[2]; const u = [b[0] - a[0], b[1] - a[1], b[2] - a[2]], v = [c[0] - a[0], c[1] - a[1], c[2] - a[2]]; return [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]][k]; });
    const l = Math.hypot(...n);
    return [...n.map((x) => x / l), (n[0] * f[0][0] + n[1] * f[0][1] + n[2] * f[0][2]) / l].map((x) => (Math.round(x * 1e6) / 1e6 + 0).toFixed(6)).join();
  };
  const PLANES = Object.fromEntries(ROOF_FOLD_KINDS.map((k) => [k, SOLIDS[k].faces.map(planeKey)]));
  const PLANE_SETS = Object.fromEntries(ROOF_FOLD_KINDS.map((k) => [k, new Set(PLANES[k])]));
  function solidPolys(items, colourFn, cullCoplanar = false) {
    const polys = [], edges = [];
    const kindsAt = new Map();
    if (cullCoplanar) for (const s of solids.values()) { const k = siteKey(s.site); if (!kindsAt.has(k)) kindsAt.set(k, []); kindsAt.get(k).push(s.kind); }
    for (const item of items) {
      const offset = centreOf(item.site);
      const colour = colourFn(item);
      const turn = turnFor(item.site);
      const outer = cullCoplanar ? (kindsAt.get(siteKey(item.site)) ?? []).filter((k) => NESTING.indexOf(k) > NESTING.indexOf(item.kind)) : [];
      SOLIDS[item.kind].faces.forEach((polygon, i) => {
        if (outer.some((k) => PLANE_SETS[k].has(PLANES[item.kind][i]))) return;
        polys.push({ polygon: polygon.map(turn), offset, colour, record: item });
      });
      for (const [a, b] of SOLIDS[item.kind].edges) edges.push({ a: turn(a), b: turn(b), offset });
    }
    return { polys, edges };
  }
  function mergedPolys() {
    const polys = [], edges = [];
    const sheared = Boolean(shear());
    const surface = mergedDodecaSurface(sites(), turnedSite, centreCell, sheared ? 2 : 1);
    for (const { site, polygon } of surface) {
      const colour = view.mode === 'merged' && view.parity ? shade(KIND_COLOR.dodeca, site) : new THREE.Color(KIND_COLOR.dodeca);
      // Surface pieces are already in cell units, each around its own cell centre.
      polys.push({ polygon, offset: [0, 0, 0], colour, record: { site, kind: 'dodeca' } });
    }
    for (const [a, b] of mergedDodecaEdges(surface, sites(), turnedSite, sheared ? centreCell : null)) edges.push({ a, b, offset: [0, 0, 0] });
    return { polys, edges };
  }
  // Cube vertices of every occupied cell, or every vertex of every drawn solid.
  function nodeMarkers(items) {
    const corners = new Map();
    const put = (p) => corners.set(p.map((c) => c.toFixed(4)).join(), p);
    if (view.vertices === 'cube') {
      for (const s of sites()) for (const dx of [-1, 1]) for (const dy of [-1, 1]) for (const dz of [-1, 1]) { const o = centreOf(s); put([o[0] + dx * WS, o[1] + dy * WS, o[2] + dz * WS]); }
    } else {
      for (const { site, kind } of items) { const turn = turnFor(site); for (const f of SOLIDS[kind].faces) for (const v of f) put(turn(v).map((c, a) => c * WS + centreOf(site)[a])); }
    }
    const mesh = new THREE.InstancedMesh(nodeGeometry, nodeMaterial, Math.max(1, corners.size));
    const m = new THREE.Matrix4();
    [...corners.values()].forEach((p, i) => mesh.setMatrixAt(i, m.makeTranslation(...p)));
    mesh.count = corners.size;
    return mesh;
  }
  function emptyNeighbourSites() {
    const occupied = new Set(sites().map(siteKey));
    const out = new Map();
    for (const s of sites()) for (const d of DIRECTIONS) {
      if (Math.abs(d[0]) + Math.abs(d[1]) + Math.abs(d[2]) !== 1) continue;
      const n = s.map((c, i) => c + d[i]);
      if (!occupied.has(siteKey(n))) out.set(siteKey(n), n);
    }
    return [...out.values()];
  }
  // A study shears both ways (direct request): as copies on a 2 x 2 x 2 block of cells, each
  // placed through the shear and left exact, or as one solid put through the shear itself.
  const STUDY_BLOCK = [0, 1].flatMap((x) => [0, 1].flatMap((y) => [0, 1].map((z) => [x, y, z])));
  const studyCopies = () => view.studyShear === 'copies';
  function studyPlacements() {
    if (!studyCopies()) return [{ offset: [0, 0, 0], map: (p) => { const A = shear(); return A ? A.map((r) => r[0] * p[0] + r[1] * p[1] + r[2] * p[2]) : p; } }];
    const C = STUDY_BLOCK.map(centreOf);
    const mid = [0, 1, 2].map((a) => C.reduce((t, c) => t + c[a], 0) / C.length);
    return C.map((c) => ({ offset: c.map((v, a) => v - mid[a]), map: (p) => p }));
  }
  function drawStudy() {
    const polys = [], edges = [], ghost = [];
    const faces = [];
    if (view.study === 'stretch') {
      for (const f of stretchedDodeca(view.stretch)) faces.push([f, f.length === 5 ? KIND_COLOR.dodeca : f.length === 6 ? KIND_COLOR.star : KIND_COLOR.cube]);
    } else {
      const { rhombi, walls } = ekpWindowsSolid();
      rhombi.forEach((f) => faces.push([f, KIND_COLOR.dodeca]));
      walls.forEach((f) => faces.push([f, KIND_COLOR.stella]));
    }
    // Context, faint: the six stellas round the windows, or the two dodecahedra the stretch joins.
    const context = [];
    if (view.study === 'windowsStellas') for (const tet of neighbourStellas()) for (const f of tet) f.forEach((p, i) => context.push([p, f[(i + 1) % f.length]]));
    if (view.study === 'stretch') for (const dx of [-view.stretch / 2, view.stretch / 2]) for (const [a, b] of SOLIDS.dodeca.edges) context.push([[a[0] + dx, a[1], a[2]], [b[0] + dx, b[1], b[2]]]);
    for (const { offset, map } of studyPlacements()) {
      for (const [f, hex] of faces) {
        const polygon = f.map(map);
        polys.push({ polygon, offset, colour: new THREE.Color(hex), record: null });
        polygon.forEach((p, i) => edges.push({ a: p, b: polygon[(i + 1) % polygon.length], offset }));
      }
      for (const [a, b] of context) ghost.push(...map(a).map((c, i) => c * WS + offset[i]), ...map(b).map((c, i) => c * WS + offset[i]));
    }
    const [mesh, lines] = meshOf(polys, edges, pieceMaterial, EDGE_COLOR, 'study');
    group.add(mesh, lines);
    if (ghost.length) {
      const g = new THREE.BufferGeometry();
      g.setAttribute('position', new THREE.Float32BufferAttribute(ghost, 3));
      group.add(new THREE.LineSegments(g, new THREE.LineBasicMaterial({ color: view.study === 'stretch' ? GHOST_COLOR : KIND_COLOR.stella, transparent: true, opacity: 0.55 })));
    }
  }
  function fitStudy() {
    const r = view.study === 'windowsStellas' ? 3.4 : view.study === 'stretch' ? view.stretch / 2 + 1.8 : 1.8;
    const spread = studyCopies() ? Math.max(...studyPlacements().map(({ offset }) => Math.hypot(...offset))) : 0;
    fitView([0, 0, 0], r * WS + spread);
  }
  function rebuild() {
    renderInfo();
    clearGroup();
    if (!active) return;
    if (view.study !== 'off') { drawStudy(); renderPanel(); return; }
    pieceMaterial.transparent = opacity < 1;
    pieceMaterial.opacity = opacity;
    pieceMaterial.depthWrite = opacity >= 1;
    if (solids.size) {
      const items = view.mode === 'merged' ? sites().map((site) => ({ site, kind: 'dodeca' })) : drawList();
      // X-ray: one mesh per solid kind, each with its own see-through level.
      const layers = view.mode === 'merged' ? [{ ...mergedPolys(), material: pieceMaterial }]
        : view.xray ? NESTING.filter((kind) => items.some((it) => it.kind === kind)).map((kind, rank) => {
          const own = items.filter((it) => it.kind === kind);
          const o = xrayOpacity(rank) * opacity;
          const material = pieceMaterial.clone();
          Object.assign(material, { transparent: o < 1, opacity: o, depthWrite: o >= 1 });
          material.polygonOffsetUnits = 1 + 16 * (NESTING.length - 1 - NESTING.indexOf(kind));
          return { ...solidPolys(own, colourOf), material, order: rank };
        })
        // One mesh per kind, inner kinds pushed back in depth: some share faces exactly (8 icosahedron
        // faces lie in the octahedron's planes), and the outer one should win there.
        : NESTING.filter((kind) => items.some((it) => it.kind === kind)).map((kind) => {
          const material = pieceMaterial.clone();
          material.polygonOffsetUnits = 1 + 16 * (NESTING.length - 1 - NESTING.indexOf(kind));
          return { ...solidPolys(items.filter((it) => it.kind === kind), colourOf, opacity >= 1 && (view.mode === 'built' || view.mode === 'checker')), material };
        });
      for (const { polys, edges, material, order = 0 } of layers) {
        const [mesh, lines] = meshOf(polys, edges, material, EDGE_COLOR, 'piece');
        if (material !== pieceMaterial) mesh.userData.ownMaterial = true;
        mesh.renderOrder = order;
        mesh.visible = !skeleton;
        if (skeleton) lines.material.color.setHex(GHOST_COLOR);
        group.add(mesh, lines);
        pickTargets.push(mesh);
      }
      if (view.vertices !== 'off') group.add(nodeMarkers(items));
      if (latticeView) {
        const ghosts = emptyNeighbourSites().map((site) => ({ site, kind: view.piece }));
        if (ghosts.length) {
          const g = solidPolys(ghosts, () => new THREE.Color(GHOST_COLOR));
          const [gm, gl] = meshOf(g.polys, g.edges, ghostMaterial, GHOST_COLOR, 'ghost');
          group.add(gm, gl);
          pickTargets.push(gm);
        }
      }
    } else {
      const f = solidPolys([{ site: [0, 0, 0], kind: view.piece }], () => new THREE.Color(FIRST_COLOR));
      const [mesh, lines] = meshOf(f.polys, f.edges, firstMaterial, FIRST_COLOR, 'first');
      group.add(mesh, lines);
      pickTargets.push(mesh);
    }
    renderPanel();
  }

  // ---- building ----
  function commit() { save(); rebuild(); onChange(); }
  // Keep the whole build in view (fitView only ever zooms out).
  function fitBuild() {
    const S = sites();
    if (!S.length) { fitView([0, 0, 0], 2.2 * WS); return; }
    const C = S.map(centreOf);
    const c = [0, 1, 2].map((a) => C.reduce((t, o) => t + o[a], 0) / C.length);
    const r = Math.max(...C.map((o) => Math.hypot(...o.map((v, a) => v - c[a])))) + 1.8 * WS;
    fitView(c, r);
  }
  const pieceName = (kind) => t(`roofFold.${kind}`, lang());
  function add(site, kind) {
    const k = solidKey(site, kind);
    if (solids.has(k)) return false;
    solids.set(k, { site: [...site], kind });
    commit();
    fitBuild();
    return true;
  }
  // The neighbouring site whose direction best matches the face's outward normal.
  function siteAcross(site, normal) {
    let best = null, bestDot = -Infinity;
    for (const d of DIRECTIONS) {
      const dd = (d[0] * normal.x + d[1] * normal.y + d[2] * normal.z) / Math.hypot(...d);
      if (dd > bestDot) { bestDot = dd; best = d; }
    }
    return site.map((c, i) => c + best[i]);
  }
  function handleTap(hit, mode) {
    if (view.study !== 'off') return false;
    const tag = hit.object.userData.roofFold;
    const record = hit.object.userData.records?.[hit.faceIndex];
    if (!tag || !record) return false;
    const chisel = mode === 'chisel';
    if (tag === 'first' || tag === 'ghost') return chisel ? false : add(record.site, view.piece);
    if (chisel) {
      // As built, the tapped solid goes; in a redrawn view, everything at that site.
      const asBuilt = view.mode === 'built' || view.mode === 'checker';
      const gone = asBuilt ? [solidKey(record.site, record.kind)] : ROOF_FOLD_KINDS.map((k) => solidKey(record.site, k));
      if (!gone.some((k) => solids.delete(k))) return false;
      commit();
      return true;
    }
    if (!solids.has(solidKey(record.site, view.piece))) {
      add(record.site, view.piece);
      showHudPrompt(t('roofFold.prompt.inside', lang(), { piece: pieceName(view.piece) }), 3000);
      return true;
    }
    const across = siteAcross(record.site, hit.face.normal);
    if (add(across, view.piece)) return true;
    showHudPrompt(t('roofFold.prompt.taken', lang(), { piece: pieceName(view.piece) }), 2500);
    return false;
  }

  // ---- info ----
  const info = document.createElement('div');
  info.id = 'worldrooffold-info';
  info.className = 'qc-info';
  info.setAttribute('aria-live', 'polite');
  document.body.appendChild(info);
  function renderInfo() {
    const show = active && infoOpen;
    info.classList.toggle('visible', show);
    if (!show) return;
    const L = lang();
    const all = [...solids.values()];
    const count = (k) => all.filter((s) => s.kind === k).length;
    const S = sites();
    const even = S.filter((s) => !odd(s)).length;
    const alternating = ALTERNATING.includes(view.mode);
    const row = (k, v) => `<div><span class="w4d-info-k">${k}</span> ${v}</div>`;
    info.innerHTML = [
      row(t('roofFold.info.solids', L), all.length ? ROOF_FOLD_KINDS.filter((k) => count(k)).map((k) => `${t(`roofFold.${k}`, L)} ${count(k)}`).join(', ') : t('hull.info.none', L)),
      all.length ? row(t('roofFold.info.sites', L), t('roofFold.info.siteCounts', L, { n: S.length, even, odd: S.length - even })) : '',
      row(t('roofFold.info.group', L), alternating ? ROOF_FOLD_PATTERNS[patternName()].group : 'Pm-3 (No. 200)'),
    ].join('');
  }

  // ---- panel ----
  const panel = document.createElement('div');
  panel.id = 'worldrooffold-panel';
  panel.className = 'qc-panel';
  panel.innerHTML = `
    <div class="w4d-row"><label class="hull-pick"><span class="rf-study-label"></span> <select class="hull-select" data-select="study"></select></label></div>
    <div class="w4d-row rf-stretch-row"><label class="hull-pick"><span class="rf-stretch-label"></span> <input type="range" class="rf-stretch" min="0" max="${STRETCH_MAX * 1000}" step="1"> <span class="rf-stretch-val"></span></label></div>
    <div class="w4d-row rf-study-note"></div>
    <div class="w4d-row w4d-options rf-study-opts"><button type="button" data-study-shear></button></div>
    <div class="w4d-row rf-build-row"><label class="hull-pick"><span class="rf-piece-label"></span> <select class="hull-select" data-select="piece"></select></label></div>
    <div class="w4d-row rf-build-row"><label class="hull-pick"><span class="rf-view-label"></span> <select class="hull-select" data-select="mode"></select></label></div>
    <div class="w4d-row rf-pattern-row"><label class="hull-pick"><span class="rf-pattern-label"></span> <select class="hull-select" data-select="pattern"></select></label></div>
    <div class="w4d-row w4d-options"></div>`;
  document.body.appendChild(panel);
  addPanelMinimiser(panel, 'roof-fold');
  const pieceSelect = panel.querySelector('[data-select="piece"]');
  const modeSelect = panel.querySelector('[data-select="mode"]');
  const optionsRow = panel.querySelector('.w4d-options');
  const patternRow = panel.querySelector('.rf-pattern-row');
  const patternSelect = panel.querySelector('[data-select="pattern"]');
  const studySelect = panel.querySelector('[data-select="study"]');
  const stretchRow = panel.querySelector('.rf-stretch-row');
  const stretchInput = panel.querySelector('.rf-stretch');
  const stretchVal = panel.querySelector('.rf-stretch-val');
  const studyNote = panel.querySelector('.rf-study-note');
  const studyOpts = panel.querySelector('.rf-study-opts');
  const studyShearBtn = panel.querySelector('[data-study-shear]');
  function renderPanel() {
    panel.classList.toggle('visible', active);
    if (!active) return;
    const L = lang();
    panel.querySelector('.rf-study-label').textContent = t('roofFold.study', L);
    studySelect.innerHTML = STUDIES.map((k) => `<option value="${k}"${k === view.study ? ' selected' : ''}>${t(`roofFold.study.${k}`, L)}</option>`).join('');
    const studying = view.study !== 'off';
    // Nothing unnecessary: a study hides the build controls, the build hides the study's.
    for (const r of panel.querySelectorAll('.rf-build-row')) r.style.display = studying ? 'none' : '';
    optionsRow.style.display = studying ? 'none' : '';
    stretchRow.style.display = view.study === 'stretch' ? '' : 'none';
    panel.querySelector('.rf-stretch-label').textContent = t('roofFold.stretch', L);
    stretchInput.value = String(Math.round(view.stretch * 1000));
    stretchVal.textContent = view.stretch.toFixed(3);
    studyNote.style.display = studying ? '' : 'none';
    studyOpts.style.display = studying ? '' : 'none';
    studyShearBtn.textContent = t(`roofFold.studyShear.${view.studyShear}`, L);
    studyNote.textContent = studying ? t(view.study === 'stretch' ? 'roofFold.study.note.stretch' : 'roofFold.study.note.windows', L) : '';
    if (studying) { patternRow.style.display = 'none'; return; }
    panel.querySelector('.rf-piece-label').textContent = t('hull.piece', L);
    panel.querySelector('.rf-view-label').textContent = t('roofFold.view', L);
    pieceSelect.innerHTML = ROOF_FOLD_KINDS.map((k) => `<option value="${k}"${k === view.piece ? ' selected' : ''}>${t(`roofFold.${k}`, L)}</option>`).join('');
    modeSelect.innerHTML = VIEWS.map((v) => `<option value="${v}"${v === view.mode ? ' selected' : ''}>${t(`roofFold.view.${v}`, L)}</option>`).join('');
    patternRow.style.display = ALTERNATING.includes(view.mode) ? '' : 'none';
    panel.querySelector('.rf-pattern-label').textContent = t('roofFold.pattern', L);
    patternSelect.innerHTML = PATTERNS.filter((p) => p !== 'octants' || view.mode === 'checker')
      .map((p) => `<option value="${p}"${p === patternName() ? ' selected' : ''}>${t(`roofFold.pattern.${p}`, L)}</option>`).join('');
    // Checkerboard colours by the pattern itself; X-ray doesn't apply to the merged surface.
    optionsRow.innerHTML = [
      view.mode === 'checker' ? '' : `<button type="button" data-opt="parity" class="${view.parity ? 'active' : ''}">${t('roofFold.parity', L)}</button>`,
      view.mode === 'merged' ? '' : `<button type="button" data-opt="xray" class="${view.xray ? 'active' : ''}">${t('roofFold.xray', L)}</button>`,
      `<button type="button" data-opt="turnOdd" class="${view.turnOdd ? 'active' : ''}">${t('roofFold.turnOdd', L)}</button>`,
      `<button type="button" data-opt="vertices" class="${view.vertices !== 'off' ? 'active' : ''}">${t('roofFold.vertices', L)}: ${t(`roofFold.vertices.${view.vertices}`, L)}</button>`,
      `<button type="button" data-opt="info" class="${infoOpen ? 'active' : ''}">${t('hyper.info', L)}</button>`,
    ].join('');
  }
  studySelect.addEventListener('change', () => {
    if (!STUDIES.includes(studySelect.value)) return;
    view.study = studySelect.value;
    save();
    rebuild();
    if (view.study !== 'off') fitStudy(); else fitBuild();
  });
  stretchInput.addEventListener('input', () => {
    let v = Number(stretchInput.value) / 1000;
    const snap = STRETCH_SNAPS.find((x) => Math.abs(x - v) < 0.03);
    if (snap !== undefined) v = snap;
    view.stretch = v;
    save();
    rebuild();
  });
  stretchInput.addEventListener('change', fitStudy);
  studyShearBtn.addEventListener('click', () => {
    view.studyShear = studyCopies() ? 'solid' : 'copies';
    save();
    rebuild();
    fitStudy();
  });
  pieceSelect.addEventListener('change', () => {
    if (!ROOF_FOLD_KINDS.includes(pieceSelect.value)) return;
    view.piece = pieceSelect.value;
    save();
    rebuild();
  });
  modeSelect.addEventListener('change', () => {
    if (!VIEWS.includes(modeSelect.value)) return;
    view.mode = modeSelect.value;
    if (view.mode === 'checker' && view.vertices === 'off') view.vertices = 'cube';
    save();
    if (ALTERNATING.includes(view.mode)) showHudPrompt(t('roofFold.prompt.alt', lang()), 4000);
    rebuild();
  });
  patternSelect.addEventListener('change', () => {
    if (!PATTERNS.includes(patternSelect.value)) return;
    view.pattern = patternSelect.value;
    save();
    rebuild();
  });
  optionsRow.addEventListener('click', (ev) => {
    const b = ev.target.closest('button[data-opt]');
    if (!b) return;
    if (b.dataset.opt === 'parity') { view.parity = !view.parity; save(); }
    else if (b.dataset.opt === 'xray') { view.xray = !view.xray; save(); }
    else if (b.dataset.opt === 'turnOdd') { view.turnOdd = !view.turnOdd; save(); }
    else if (b.dataset.opt === 'vertices') { view.vertices = VERTICES[(VERTICES.indexOf(view.vertices) + 1) % VERTICES.length]; save(); }
    else if (b.dataset.opt === 'info') infoOpen = !infoOpen;
    rebuild();
  });
  let shownLang = lang();
  onSettingsChange((st) => { if (st.language !== shownLang) { shownLang = st.language; if (active) rebuild(); } });

  return {
    group,
    meshes: () => pickTargets,
    handleTap,
    setActive(on) {
      if (on === active) return;
      active = on;
      group.visible = on;
      if (!on) { panel.classList.remove('visible'); info.classList.remove('visible'); }
      rebuild();
      if (on) { if (view.study !== 'off') fitStudy(); else fitBuild(); }
    },
    setSkeleton(on) { skeleton = on; if (active) rebuild(); },
    setTranslucent(o) { if (o !== opacity) { opacity = o; if (active) rebuild(); } },
    setLatticeView(on) { latticeView = on; if (active) rebuild(); },
    shearChanged() { if (active) rebuild(); },
    get isEmpty() { return solids.size === 0; },
    clear() { solids.clear(); commit(); },
    snapshot: toJSON,
    restore(json) { setFromJSON(json); save(); rebuild(); onChange(); },
    toJSON,
  };
}
