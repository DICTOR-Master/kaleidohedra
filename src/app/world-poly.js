// Polyhedraverse inside the joined app (step D2, DICTO 2026-10-09): its own 3D world, the portrait
// gallery's shapes from krp-core (src/polyhedra). Choose a shape in DICTO (families, then shapes);
// an empty world shows its outline in the app's colour, tap it to place it; then tap attach (D3):
// tap a face or a corner, then a shape; 4D Prism, Transform to… and the Golden helper in the strip.
// The shape browser comes with D4 (PLAN-POLYHEDRAVERSE.md).
// Saved in Polyhedraverse's own form (krp-core assembly: nodes with a shape and a transform), so a
// build moves between this world and the old site by Export/Import.
import * as THREE from 'three';
import { POLYHEDRA, isFaceEligibleForAttach, HEXA_PARTS, DODECA13_PARTS, KITS13 } from '../krp-core/src/polyhedra/index.js';
import { facesCongruent } from '../krp-core/src/polyhedra/core.js';
import { faceAttachOptions } from '../krp-core/src/assembly/faceAttach.js';
import { rankFaceAttachOptions, isConvex, convexOverlap } from '../krp-core/src/assembly/faceRegistration.js';
import { familyIds } from '../krp-core/src/polyhedra/families.js';
import { describeAssembly } from '../krp-core/src/assembly/assemblyNaming.js';
import { goldenStatus, isGoldenBuild, withNextSafePiece } from '../krp-core/src/assembly/goldenHelper.js';
import { GOLDEN_BUILDS, withNextRecipePiece } from '../krp-core/src/assembly/goldenBuilds.js';
import { matchRewriteVertices, REWRITE_TARGET } from '../krp-core/src/polyhedra/rewrite.js';
import { buildWallPrism, duoprismBuildDepth } from '../krp-core/src/polyhedra/duoprism.js';
import { FOURD_CAPABLE_IDS } from '../krp-core/src/polyhedra/fourD.js';
import { pairPartners } from '../krp-core/src/polyhedra/families.js';
import { buildRcpComplex, rcpTargetOptions, buildSyntheticCellSpec, maxShell } from '../krp-core/src/polyhedra/rcpBuild.js';
import { FOUR_D_SHAPE_PARAMS } from '../krp-core/src/polyhedra/radialProjection.js';
import { buildFaceConnectors } from '../krp-core/src/polyhedra/core.js';
import { mountWireframePreview } from './wireframe-preview.js';
import { addPanelMinimiser } from './panel-minimiser.js';
import { favourites, isFavourite, toggleFavourite, recent, remember as rememberShape, adopt, onPrefsChange } from './poly-prefs.js';
import { polyShapeEdges } from './poly-shapes.js';
import { familiesFor } from '../krp-core/src/polyhedra/families.js';
import { FAMILY_COLORS } from '../krp-core/src/assembly/pieceColors.js';
import { getSettings, onSettingsChange } from './settings.js';
import { SITE, storageKey, theme } from './site.js';
import { migrateLegacyAssembly, ASSEMBLY_STORAGE_KEY } from '../krp-core/src/assembly/assembly.js';
import { solidsOverlap, placedSolid, insideSolid } from '../krp-core/src/assembly/overlap.js';
import { hintSlots, hasHints as buildHasHints } from '../krp-core/src/assembly/hints.js';
import { bestFits } from '../krp-core/src/assembly/bestFits.js';
import { kitSlots, kitFrame, kitIcosahedron, goldenRectangles } from '../krp-core/src/assembly/kitHints.js';
import { t } from './i18n.js';
import { polyShapeName } from './poly-shapes.js';
import { softActive, softState, onSoftChange, puffedFor, finishMaterial, applyFinish, seamMaterial, seamLines } from './soft-finish.js';
import { createStarStep } from './star-step.js';
import { RULES as STAR_RULES, solidOf as starSolidOf } from './star-step-geometry.js';

export { polyShapeEdges, polyShapeName } from './poly-shapes.js';

const STORAGE_KEY = storageKey('poly-world');
const EDGE_COLOR = 0x0b1220;
const DEFAULT_SHAPE = 'DODECAHEDRON';
const lang = () => getSettings().language;
// Parts views of DICTO's families (krp-core HEXA_PARTS, DODECA13_PARTS): which of a shape's views each
// choice shows. The menu lists only the choices the shapes in the build have.
const PART_VIEWS = ['solid', 'jewels', 'piecesA', 'piecesB', 'pieces', 'units', 'stars'];
const ALL_PARTS = { ...HEXA_PARTS, ...DODECA13_PARTS };
const PART_PICK = {
  DICTO_DODECA13: { pieces: 'pieces', units: 'units', stars: 'stars' },
  DICTO_HEXA: { jewels: 'jewels', piecesA: 'cubesAndRoofs', piecesB: 'wholeAndTrimmed' },
  DICTO_HEXA_KEY: { jewels: 'stellasAndRoofs', piecesA: 'stellasAndRoofs', piecesB: 'stellasAndRoofs' },
  DICTO_HEXA_RHOMBO_CLUSTER: { jewels: 'jewels', piecesA: 'hexas', piecesB: 'hexas' },
  DICTO_HEXA_DIAMOND_CLUSTER: { jewels: 'jewels', piecesA: 'hexas', piecesB: 'hexas' },
};
// The Dodeca-13's gap pieces (DICTO): wedges cyan, needles purple.
const PART_COLOURS = { dodeca: 0xffc857, centre: 0xffe27a, unit: 0xd9a520, wedge: 0x4dd0e1, needle: 0xc792ea, star: 0x4dd0e1, jewel: 0xd9a520, shared: 0xffe27a, trimmed: 0x8f5bd8, cube: 0x9aa4b8, roof: 0xb8892a, stella: 0x8f5bd8, hexa: 0xd9a520, key: 0x8f5bd8 };

export function createPolyWorld({ scene, colorOf, getMaterial, onChange = () => {}, showHudPrompt = () => {}, fitView = () => {}, pickShape = () => {} }) {
  const group = new THREE.Group();
  group.visible = false;
  scene.add(group);

  // ---- state: Polyhedraverse's assembly form ----
  let nodes = []; // { id, shape, transform: { position, quaternion }, material }
  let connections = []; // { nodeA, vertexA, nodeB, vertexB, kind: 'face' } (face indices for a face join)
  // queue: the shapes used lately, newest first (8); pins: the ones always offered (D3b, DICTO's build queue).
  // Favourites (pins) and Recent (the queue) live in poly-prefs.js, shared with DICTO's browser.
  const view = { shape: DEFAULT_SHAPE, parts: 'solid', rcp: null, hints: true, bestFits: false, kit: null, pacioli: false, cells: false };
  let active = false, skeleton = false, opacity = 1;
  let spherical = false, sphereScale = 1;
  let nextId = 1;

  const validNode = (n) => n && POLYHEDRA[n.shape] && Array.isArray(n.transform?.position) && n.transform.position.length === 3
    && Array.isArray(n.transform?.quaternion) && n.transform.quaternion.length === 4;
  function setFromJSON(data) {
    nodes = (Array.isArray(data?.nodes) ? data.nodes : []).filter(validNode).map((n) => ({
      id: String(n.id), shape: n.shape, transform: { position: [...n.transform.position], quaternion: [...n.transform.quaternion] },
      ...(typeof n.material === 'string' ? { material: n.material } : {}),
    }));
    const ids = new Set(nodes.map((n) => n.id));
    connections = (Array.isArray(data?.connections) ? data.connections : []).filter((c) => c && ids.has(String(c.nodeA)) && ids.has(String(c.nodeB)) && Number.isInteger(c.vertexA) && Number.isInteger(c.vertexB))
      .map((c) => ({ nodeA: String(c.nodeA), vertexA: c.vertexA, nodeB: String(c.nodeB), vertexB: c.vertexB, kind: c.kind ?? 'face',
        ...(Array.isArray(c.duoprismExtraFaces) ? { duoprismExtraFaces: c.duoprismExtraFaces.filter(Number.isInteger) } : {}) }));
    nextId = 1 + Math.max(0, ...nodes.map((n) => Number(String(n.id).replace(/\D/g, '')) || 0));
  }
  const toJSON = () => ({ nodes: nodes.map((n) => ({ ...n })), connections: connections.map((c) => ({ ...c })) });
  // The old Polyhedraverse site's build (step D6, DICTO 2026-10-09: "bring it over once"): on
  // polyhedraverse.dictospheres.com, with nothing saved here yet, its 'polyhedraverse:assembly' is converted
  // once and left untouched. Its 4D cells were pieces joined to the root by 'rcp4d' connections; here
  // a root alone grows by a count (view.rcp), so they become that count.
  function fromOldSite() {
    if (SITE !== 'polyhedraverse' || localStorage.getItem(STORAGE_KEY) !== null) return null;
    const old = migrateLegacyAssembly(JSON.parse(localStorage.getItem(ASSEMBLY_STORAGE_KEY) ?? 'null'));
    if (!old || !Array.isArray(old.nodes) || !old.nodes.length) return null;
    const conns = Array.isArray(old.connections) ? old.connections.filter((c) => c && !c.orphaned) : [];
    const cells = new Set(conns.filter((c) => c.kind === 'rcp4d').map((c) => String(c.nodeB)));
    const out = { nodes: old.nodes.filter((n) => !cells.has(String(n.id))), connections: conns.filter((c) => c.kind !== 'rcp4d'), view: { shape: DEFAULT_SHAPE } };
    const root = out.nodes.length === 1 ? out.nodes[0] : null;
    if (root?.rcpPolytope?.target) out.view.rcp = { target: root.rcpPolytope.target, n: 1 + cells.size, open: root.rcpPolytope.view3D !== false, coords: false };
    return out;
  }
  try {
    const data = fromOldSite() ?? JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null');
    if (data) {
      setFromJSON(data);
      if (POLYHEDRA[data.view?.shape]) view.shape = data.view.shape;
      adopt(Array.isArray(data.view?.pins) ? data.view.pins : [], Array.isArray(data.view?.queue) ? data.view.queue : []);
      if (PART_VIEWS.includes(data.view?.parts)) view.parts = data.view.parts;
      if (data.view?.hints === false) view.hints = false;
      view.bestFits = data.view?.bestFits === true;
      view.kit = KITS13[data.view?.kit] ? data.view.kit : null;
      if (data.view?.rcp && typeof data.view.rcp.target === 'string') view.rcp = { target: data.view.rcp.target, n: Math.max(1, data.view.rcp.n | 0), open: data.view.rcp.open !== false, coords: !!data.view.rcp.coords };
      if (data.version === undefined) save(); // the old site's build, now kept here
    }
  } catch { /* corrupt or blocked storage: start empty */ }
  function save() {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify({ version: 1, ...toJSON(), view })); } catch { /* best-effort */ }
  }

  // ---- drawing ----
  const rcpRootMaterial = new THREE.MeshStandardMaterial({ vertexColors: true, flatShading: true, side: THREE.DoubleSide, transparent: true, opacity: 0.18, depthWrite: false });
  // Closed cells nest inside one another (a 4D shadow): see-through, so every shell reads.
  const rcpCellMaterial = new THREE.MeshStandardMaterial({ vertexColors: true, flatShading: true, side: THREE.DoubleSide, transparent: true, opacity: 0.32, depthWrite: false });
  // Not flatShading: meshOf gives flat faces their own normals and curved shapes (the Reuleaux bodies) smooth ones.
  const pieceMaterial = new THREE.MeshStandardMaterial({ vertexColors: true, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
  const hiddenPickMaterial = new THREE.MeshBasicMaterial({ visible: false, side: THREE.DoubleSide });
  const partsMaterial = new THREE.MeshStandardMaterial({ vertexColors: true, flatShading: true, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
  // Each part of each parted node, in the node's place: solid parts for the splits; the overlapping
  // Jewels views see-through, so the overlap reads.
  function partsMeshes(list) {
    const pos = [], col = [], edge = [], c = new THREE.Color();
    let overlapping = false;
    for (const n of list) {
      const which = PART_PICK[n.shape][view.parts];
      const parts = ALL_PARTS[n.shape]?.[which] ?? [];
      if (which === 'jewels' || which === 'stars') overlapping = true; // these views overlap: see-through
      const q = new THREE.Quaternion(...n.transform.quaternion), p = new THREE.Vector3(...n.transform.position);
      // The splits stand a little apart (each part pushed out from the shape's centre) so they read
      // as pieces; the overlapping Jewels stay in place.
      const apart = which === 'jewels' || which === 'stars' ? 0 : 0.12;
      for (const part of parts) {
        c.setHex(PART_COLOURS[part.role] ?? 0xd9a520);
        const mid = part.vertices.reduce((t, v) => t.add(new THREE.Vector3(...v)), new THREE.Vector3()).divideScalar(part.vertices.length).multiplyScalar(apart);
        const P = part.vertices.map((v) => new THREE.Vector3(...v).add(mid).applyQuaternion(q).add(p));
        for (const f of part.faces) {
          for (let i = 1; i + 1 < f.length; i++) for (const k of [f[0], f[i], f[i + 1]]) { pos.push(P[k].x, P[k].y, P[k].z); col.push(c.r, c.g, c.b); }
          f.forEach((a, i) => { const b = f[(i + 1) % f.length]; edge.push(P[a].x, P[a].y, P[a].z, P[b].x, P[b].y, P[b].z); });
        }
      }
    }
    partsMaterial.transparent = overlapping || opacity < 1;
    partsMaterial.opacity = overlapping ? Math.min(opacity, 0.45) : opacity;
    partsMaterial.depthWrite = !partsMaterial.transparent;
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    g.setAttribute('color', new THREE.Float32BufferAttribute(col, 3));
    g.computeVertexNormals();
    const lg = new THREE.BufferGeometry();
    lg.setAttribute('position', new THREE.Float32BufferAttribute(edge, 3));
    const m = new THREE.Mesh(g, partsMaterial);
    m.userData.poly = 'parts';
    m.visible = !skeleton;
    const l = new THREE.LineSegments(lg, new THREE.LineBasicMaterial({ color: skeleton ? theme().accentHex : EDGE_COLOR, transparent: true, opacity: 0.7 }));
    return [m, l];
  }
  const outlineMaterial = new THREE.MeshStandardMaterial({ transparent: true, opacity: 0.16, depthWrite: false, side: THREE.DoubleSide });
  const pickTargets = [];
  let faceOwner = []; // triangle index -> { node, face }
  function clearGroup() {
    for (const child of [...group.children]) {
      group.remove(child);
      if (child.userData.poly === 'sphere') { child.material.dispose(); continue; }
      if (child.userData.poly === 'soft') { child.dispose(); continue; } // its geometry is the shared puffed one
      if (child.userData.poly === 'softSeams') { child.geometry.dispose(); continue; }
      child.geometry.dispose();
      if (child.isLineSegments || child.userData.ownMat) child.material.dispose();
    }
    pickTargets.length = 0;
  }
  const worldPoints = (n) => {
    const q = new THREE.Quaternion(...n.transform.quaternion), p = new THREE.Vector3(...n.transform.position);
    return POLYHEDRA[n.shape].vertices.map((v) => new THREE.Vector3(...v).applyQuaternion(q).add(p));
  };
  // A curved shape (spec.curved: the Reuleaux Platonic Solids, DICTO 2026-10-21, #45) is drawn from its smooth body, each triangle
  // tapping as its patch (face); its lines are the seams between patches (the creases), as in Kaleidohedra's Reuleaux world.
  function curvedAt(n, fn) {
    const g = puffedFor(n.shape, POLYHEDRA[n.shape]), P = g.attributes.position, N = g.attributes.normal, M = matrixOf(n), R = new THREE.Matrix3().getNormalMatrix(M);
    const v = new THREE.Vector3(), w = new THREE.Vector3();
    for (let i = 0; i < P.count; i++) { v.fromBufferAttribute(P, i).applyMatrix4(M); w.fromBufferAttribute(N, i).applyMatrix3(R).normalize(); fn(v, w, g.userData.faceIds[i], i); }
    return g;
  }
  function meshOf(list, material, colour, edgeColor, record) {
    const pos = [], col = [], nrm = [], edge = [];
    const c = new THREE.Color(), e1 = new THREE.Vector3(), e2 = new THREE.Vector3();
    for (const n of list) {
      colour(n, c);
      const P = worldPoints(n), s = POLYHEDRA[n.shape];
      const own = c.clone(), fc = s.faceColours; // DICTO Transitional Shells: each face in its piece's colour, as in the app's views
      if (s.curved) {
        const g = curvedAt(n, (v, w, fi, i) => {
          if (fc) c.setHex(fc[fi]); else c.copy(own);
          pos.push(v.x, v.y, v.z); nrm.push(w.x, w.y, w.z); col.push(c.r, c.g, c.b);
          if (i % 3 === 0) record?.push({ node: n, face: fi });
        });
        const S = g.userData.seams, M = matrixOf(n);
        for (let i = 0; i < S.length; i += 3) { e1.set(S[i], S[i + 1], S[i + 2]).applyMatrix4(M); edge.push(e1.x, e1.y, e1.z); }
        continue;
      }
      s.faces.forEach((f, fi) => {
        if (fc) c.setHex(fc[fi]); else c.copy(own);
        for (let i = 1; i < f.length - 1; i++) {
          e1.subVectors(P[f[i]], P[f[0]]); e2.subVectors(P[f[i + 1]], P[f[0]]); e1.cross(e2).normalize();
          for (const k of [f[0], f[i], f[i + 1]]) { pos.push(P[k].x, P[k].y, P[k].z); col.push(c.r, c.g, c.b); nrm.push(e1.x, e1.y, e1.z); }
          record?.push({ node: n, face: fi });
        }
      });
      for (const [a, b] of s.edges) edge.push(P[a].x, P[a].y, P[a].z, P[b].x, P[b].y, P[b].z);
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    g.setAttribute('color', new THREE.Float32BufferAttribute(col, 3));
    g.setAttribute('normal', new THREE.Float32BufferAttribute(nrm, 3)); // flat faces flat, curved bodies smooth
    const lg = new THREE.BufferGeometry();
    lg.setAttribute('position', new THREE.Float32BufferAttribute(edge, 3));
    return [new THREE.Mesh(g, material), new THREE.LineSegments(lg, new THREE.LineBasicMaterial({ color: edgeColor }))];
  }
  // Spherical (◯), as in the lattice worlds: each shape as a sphere of its own volume, capped at its
  // inradius (so it stays inside the shape), centred on the shape; the slider scales them all.
  const sphereCache = new Map();
  function sphereOf(shape) {
    if (sphereCache.has(shape)) return sphereCache.get(shape);
    const s = POLYHEDRA[shape], V = s.vertices.map((v) => new THREE.Vector3(...v));
    const c = V.reduce((a, v) => a.add(v), new THREE.Vector3()).divideScalar(V.length);
    let vol = 0, ceiling = Infinity;
    for (const f of s.faces) {
      const a = V[f[0]].clone().sub(c);
      for (let i = 1; i < f.length - 1; i++) vol += a.dot(V[f[i]].clone().sub(c).cross(V[f[i + 1]].clone().sub(c))) / 6;
      const n = V[f[1]].clone().sub(V[f[0]]).cross(V[f[2]].clone().sub(V[f[0]])).normalize();
      ceiling = Math.min(ceiling, Math.abs(n.dot(V[f[0]].clone().sub(c))));
    }
    const out = { centre: c, R: Math.min(Math.cbrt((3 * Math.abs(vol)) / (4 * Math.PI)), ceiling) };
    sphereCache.set(shape, out);
    return out;
  }
  const sphereGeometry = new THREE.SphereGeometry(1, 32, 20);
  const outlineNode = () => ({ id: 'outline', shape: view.shape, transform: { position: [0, 0, 0], quaternion: [0, 0, 0, 1] } });
  // ---- ★ Star step (DICTO's Star Cores papers, #79; star-step.js): for the convex solid on show (the build's one piece; the papers'
  // link opens it on any convex shape), each tap one step of the star core treatment: Star, Halo, Next (the halo the new solid). While it runs,
  // its own drawing stands in for the build; Reset (or any change to the build) goes back to the solid.
  const starStep = createStarStep({
    scene,
    fitView: (r) => fitView?.(r),
    look: () => ({ skeleton, opacity }),
    onSettled: () => renderPanel(),
  });
  const starConvex = new Map();
  const starOk = (id) => {
    if (!starConvex.has(id)) { const s = POLYHEDRA[id]; starConvex.set(id, !!s && !s.curved && isConvex(s) && !!starSolidOf(s)); }
    return starConvex.get(id);
  };
  /** The solid the star step works on: the build's one piece; null when there is none or it is not convex. */
  function starTarget() {
    if (!active || spherical || view.rcp || kitOn() || nodes.length !== 1) return null;
    return starOk(nodes[0].shape) ? nodes[0] : null;
  }
  function starStart(n) {
    return starStep.start(POLYHEDRA[n.shape], colorOf(n.shape, n.material, familiesFor(n.shape)[0]), n.transform);
  }
  function starReset() {
    if (!starStep.on) return;
    starStep.reset();
    rebuild(); renderPanel();
  }
  function starRow(L) {
    const on = starStep.on;
    return `<div class="poly-golden poly-star"><button type="button" class="poly-star-go" data-star title="${t('poly.star.title', L)}">${t('poly.star', L)}</button>${on ? `<label>${t('poly.star.rule', L)} <select data-star-rule>${STAR_RULES.map((r) => `<option value="${r}"${r === starStep.rule ? ' selected' : ''}>${t(`poly.star.rule.${r}`, L)}</option>`).join('')}</select></label>${starStep.hasLayer ? `<button type="button" data-star-layer aria-pressed="${starStep.layer}" title="${t('poly.star.layer.title', L)}">${t('poly.star.layer', L)}</button>` : ''}<button type="button" data-star-reset title="${t('poly.star.reset.title', L)}">${t('poly.star.reset', L)}</button>` : ''}</div>${on ? `<div class="poly-star-caption" data-star-caption>${starStep.caption(L)}</div>` : ''}`;
  }
  // ---- what comes next (DICTO 2026-10-09: "more visual clue help what comes next", "visible
  // patterning"): for pieces with a known pattern (krp-core HINT_RULES), the free spots next to the
  // build as faint ghosts in the colour of the piece that goes there, and the faces they touch glowing
  // in that colour, so mating faces match. Tap a ghost, or a glowing face, to place that piece there.
  // Each kind of piece its own colour, so the two of a pair read apart.
  const HINT_COLOURS = {
    DICTO_HEXA: 0xd9a520, DICTO_HEXA_KEY: 0x8f5bd8, DICTO_DODECA13: 0xffc857,
    DRAGON_JEWEL: 0xd9a520, STELLA_OCTANGULA: 0x8f5bd8, SEAMED_DODECAHEDRON: 0xffc857, DOGSTAR: 0x8f5bd8,
    D4: 0xff8a65, D8: 0x4dd0e1, TRUNCATED_TETRAHEDRON: 0xffc857, CUBOCTAHEDRON: 0xffc857, TRUNCATED_CUBE: 0xffc857,
    CUBE: 0xc792ea, PRISM_3: 0x7ae0b8, PRISM_6: 0xffc857, PRISM_8: 0xffc857, DICTO_EDGE_ROOF: 0x4dd0e1, D20: 0x5fd38a,
  };
  let hintCache = { key: '', slots: [], glow: new Map() };
  const kitOn = () => !!(view.kit && KITS13[view.kit]);
  const hasHints = () => kitOn() || buildHasHints(nodes, POLYHEDRA);
  // ---- best fits (DICTO 2026-10-13: "a helper outline, possible placements, and offer best matches only"): for any build, the
  // three places where a piece closes the most faces flush (krp-core bestFits.js), drawn as ghosts in rank colours and listed in
  // the panel with their names. Worked out a moment after each change, so the screen never waits on it.
  const BEST_COLOURS = [0xffc857, 0x4dd0e1, 0xc792ea];
  let bestState = { key: '', slots: [], glow: new Map(), busy: false };
  function bestHints() {
    const key = JSON.stringify([chosen, nodes.map((n) => [n.shape, n.transform])]);
    if (bestState.key !== key && !bestState.busy) {
      bestState = { key, slots: [], glow: new Map(), busy: true };
      setTimeout(() => {
        const last = nodes.at(-1);
        let slots = [];
        try { slots = bestFits(nodes, POLYHEDRA, { near: last?.transform.position, chosen, preferred: queue(), count: 3, maxFaces: 8 }); } catch (err) { console.warn('best fits', err); }
        bestState = { key, slots: slots.map((sl, i) => ({ ...sl, colour: BEST_COLOURS[i] })), glow: glowFor(slots), busy: false };
        if (active && view.bestFits) { rebuild(); renderPanel(); }
      }, 30);
    }
    return bestState;
  }
  // ---- a 13 kit (DICTO 2026-10-13): the kit's plan lined up with the build, its next layer as ghosts, each kind of piece its own
  // colour (krp-core kitHints.js).
  const KIT_COLOURS = [0xffc857, 0xc792ea, 0x4dd0e1, 0xf08fc0, 0x9fb4c8, 0x5fd38a]; // green last: built pieces are green
  let kitCache = { key: '', slots: [], glow: new Map() };
  function kitHints() {
    const key = JSON.stringify([view.kit, nodes.map((n) => [n.shape, n.transform])]);
    if (kitCache.key === key) return kitCache;
    const kit = KITS13[view.kit], kinds = [...new Set(kit.entries.map((e) => e.shape))];
    const slots = kitSlots(nodes, POLYHEDRA, kit, { near: nodes.at(-1)?.transform.position, cap: 12 })
      .map((sl) => ({ ...sl, colour: KIT_COLOURS[kinds.indexOf(sl.shape) % KIT_COLOURS.length] }));
    kitCache = { key, slots, glow: new Map() };
    return kitCache;
  }
  // Pacioli's three golden rectangles (DICTO 2026-10-14) on any kit that fills an icosahedron: corners on its 12 corners, each through
  // the centre with two opposite edges as its short sides; lined up with the build like the kit's outlines.
  const kitIco = () => (kitOn() ? kitIcosahedron(KITS13[view.kit], POLYHEDRA) : null);
  const pacioliOn = () => view.pacioli && !!kitIco();
  const pacioliFill = new THREE.MeshBasicMaterial({ color: 0xffe082, transparent: true, opacity: 0.45, side: THREE.DoubleSide, depthWrite: false });
  const pacioliEdge = new THREE.LineBasicMaterial({ color: 0xffffff }); // fill as EKP's rectangles; white rims stand clear of the gold outlines
  function pacioliMeshes() {
    const W = kitFrame(nodes, POLYHEDRA, KITS13[view.kit]), rects = goldenRectangles(kitIco());
    if (!W || !rects) return [];
    const q = new THREE.Quaternion(...W.q), p = new THREE.Vector3(...W.p);
    return rects.flatMap((r) => {
      const P = r.map((v) => new THREE.Vector3(...v).applyQuaternion(q).add(p));
      const g = new THREE.BufferGeometry().setFromPoints([P[0], P[1], P[2], P[0], P[2], P[3]]);
      const fill = new THREE.Mesh(g, pacioliFill); fill.renderOrder = 2;
      return [fill, new THREE.LineLoop(new THREE.BufferGeometry().setFromPoints(P), pacioliEdge)];
    });
  }
  // The kit's helper cells (DICTO 2026-10-14, Cleo-Icos & Antonius): each golden rhombohedron the pieces fill, as a purple wireframe,
  // lined up with the build like the outlines.
  const kitCells = () => (kitOn() ? KITS13[view.kit].cells ?? null : null);
  const cellsOn = () => view.cells && !!kitCells();
  const CELL_EDGES = [[0, 1], [0, 2], [0, 3], [1, 4], [1, 6], [2, 4], [2, 5], [3, 5], [3, 6], [4, 7], [5, 7], [6, 7]];
  const cellMaterial = new THREE.LineBasicMaterial({ color: 0xc792ea });
  function cellLines() {
    const W = kitFrame(nodes, POLYHEDRA, KITS13[view.kit]);
    const q = W ? new THREE.Quaternion(...W.q) : new THREE.Quaternion(), p = W ? new THREE.Vector3(...W.p) : new THREE.Vector3();
    const pts = kitCells().flatMap((c) => CELL_EDGES.flatMap(([i, j]) => [c[i], c[j]].map((v) => new THREE.Vector3(...v).applyQuaternion(q).add(p))));
    return new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(pts), cellMaterial);
  }
  const kitDone = () => kitOn() && nodes.length >= KITS13[view.kit].entries.length && !kitHints().slots.length;
  // Outlines of a kit on screen: the pieces go see-through and taps go to the outlines (✕ on the kit row hands them back).
  const kitGuiding = () => kitOn() && view.hints && !view.bestFits && kitHints().slots.length > 0;
  function hints() {
    if (view.bestFits) return nodes.length ? bestHints() : { slots: [], glow: new Map() };
    if (kitOn()) return view.hints ? kitHints() : { slots: [], glow: new Map() };
    if (!view.hints || !hasHints()) return { slots: [], glow: new Map() };
    const key = JSON.stringify(nodes.map((n) => [n.shape, n.transform]));
    if (hintCache.key === key) return hintCache;
    const slots = hintSlots(nodes, POLYHEDRA); // round the build's middle, not the last piece (hints.js)
    hintCache = { key, slots, glow: glowFor(slots) };
    return hintCache;
  }
  // A built face glows when the point just outside its middle is inside a slot's piece.
  function glowFor(slots) {
    const glow = new Map();
    slots.forEach((sl, i) => {
      const ghost = placedSolid(POLYHEDRA[sl.shape], sl.position, sl.quaternion);
      for (const id of sl.from) {
        const n = nodes.find((x) => x.id === id);
        if (!n) continue;
        const P = worldPoints(n), spec = POLYHEDRA[n.shape];
        spec.faces.forEach((f, fi) => {
          const c = f.reduce((a, k) => a.add(P[k]), new THREE.Vector3()).divideScalar(f.length);
          const nrm = P[f[1]].clone().sub(P[f[0]]).cross(P[f[2]].clone().sub(P[f[0]])).normalize();
          if (insideSolid(ghost, c.addScaledVector(nrm, 0.02 * edgeLength(spec)).toArray())) glow.set(`${n.id}:${fi}`, i);
        });
      }
    });
    return glow;
  }
  function hintMeshes() {
    const { slots, glow } = hints(), out = [];
    slots.forEach((sl, i) => {
      const spec = POLYHEDRA[sl.shape], col = sl.colour ?? HINT_COLOURS[sl.shape] ?? theme().strongHex;
      const q = new THREE.Quaternion(...sl.quaternion), p = new THREE.Vector3(...sl.position);
      const P = spec.vertices.map((v) => new THREE.Vector3(...v).applyQuaternion(q).add(p));
      const pos = [], edge = [];
      if (spec.curved) curvedAt({ shape: sl.shape, transform: { position: sl.position, quaternion: sl.quaternion } }, (v) => pos.push(v.x, v.y, v.z));
      else for (const f of spec.faces) {
        for (let k = 1; k + 1 < f.length; k++) for (const j of [f[0], f[k], f[k + 1]]) pos.push(P[j].x, P[j].y, P[j].z);
        f.forEach((a, k) => { const b = f[(k + 1) % f.length]; edge.push(P[a].x, P[a].y, P[a].z, P[b].x, P[b].y, P[b].z); });
      }
      const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.computeVertexNormals();
      // A kit's outlines a little stronger: its first layers are small pieces close against the centre.
      const strong = kitOn() && !view.bestFits;
      const m = new THREE.Mesh(g, new THREE.MeshBasicMaterial({ color: col, transparent: true, opacity: strong ? 0.22 : 0.1, depthWrite: false, side: THREE.DoubleSide }));
      m.userData.poly = 'ghost'; m.userData.slot = i; m.userData.ownMat = true;
      // Curved kit pieces (many small faces) outline only their creases, not every mesh edge (DICTO 2026-10-21).
      let lg = new THREE.BufferGeometry(); lg.setAttribute('position', new THREE.Float32BufferAttribute(edge, 3));
      if (spec.faces.length > 200 || spec.curved) { lg.dispose(); lg = new THREE.EdgesGeometry(g, 25); }
      out.push(m, new THREE.LineSegments(lg, new THREE.LineBasicMaterial({ color: col, transparent: true, opacity: strong ? 0.6 : 0.2, depthWrite: false })));
      pickTargets.push(m);
    });
    for (const [k, i] of glow) {
      const [id, fi] = k.split(':'), n = nodes.find((x) => x.id === id);
      if (!n) continue;
      const P = worldPoints(n), f = POLYHEDRA[n.shape].faces[+fi], col = slots[i].colour ?? HINT_COLOURS[slots[i].shape] ?? theme().strongHex;
      const nrm = P[f[1]].clone().sub(P[f[0]]).cross(P[f[2]].clone().sub(P[f[0]])).normalize().multiplyScalar(0.004);
      const pos = softOn() || POLYHEDRA[n.shape].curved ? softFace(n, +fi) : [];
      if (!pos.length) for (let j = 1; j + 1 < f.length; j++) for (const v of [f[0], f[j], f[j + 1]]) { const x = P[v].clone().add(nrm); pos.push(x.x, x.y, x.z); }
      const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
      const m = new THREE.Mesh(g, new THREE.MeshBasicMaterial({ color: col, transparent: true, opacity: 0.55, depthWrite: false, side: THREE.DoubleSide }));
      m.userData.poly = 'glow'; m.userData.ownMat = true;
      out.push(m);
    }
    return out;
  }
  function placeSlot(i) {
    const sl = hints().slots[i];
    if (!sl) return false;
    remember(sl.shape);
    nodes.push({ id: `n${nextId++}`, shape: sl.shape, transform: { position: [...sl.position], quaternion: [...sl.quaternion] }, material: getMaterial() });
    selection = null;
    commit();
    refitIfGrown();
    return true;
  }

  // ---- Soft (DICTO 2026-10-21): each shape's puffed copy, one instanced mesh per shape over the real pieces (which stay,
  // unseen, for taps). Pieces with their own face colours keep them; shapes with many small faces keep their creases.
  const softMat = finishMaterial({ side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
  const softSeamMat = seamMaterial();
  const softOn = () => softActive() && !skeleton && !spherical && !view.rcp;
  function softMeshes(list) {
    const out = [], byShape = new Map();
    for (const n of list) { if (!byShape.has(n.shape)) byShape.set(n.shape, []); byShape.get(n.shape).push(n); }
    if (softMat.userData.finish !== softState().finish) applyFinish(softMat);
    softMat.transparent = pieceMaterial.transparent; softMat.opacity = pieceMaterial.opacity; softMat.depthWrite = pieceMaterial.depthWrite;
    for (const [shape, ns] of byShape) {
      const spec = POLYHEDRA[shape], g = puffedFor(shape, spec);
      const im = new THREE.InstancedMesh(g, softMat, ns.length);
      const M = ns.map(matrixOf);
      ns.forEach((n, i) => { im.setMatrixAt(i, M[i]); im.setColorAt(i, spec.faceColours ? new THREE.Color(0xffffff) : colorOf(n.shape, n.material, familiesFor(n.shape)[0])); });
      im.userData.poly = 'soft'; im.raycast = () => {};
      out.push(im);
      // the seams: the curved face boundaries; a piece of many small faces keeps its own edges
      if (spec.faces.length > 200) {
        const pos = [];
        for (const n of ns) { const P = worldPoints(n); for (const [a, b] of spec.edges) pos.push(P[a].x, P[a].y, P[a].z, P[b].x, P[b].y, P[b].z); }
        const lg = new THREE.BufferGeometry(); lg.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
        const l = new THREE.LineSegments(lg, softSeamMat); l.raycast = () => {}; l.userData.poly = 'softSeams'; out.push(l);
      } else { const l = seamLines(g, M, softSeamMat); l.userData.poly = 'softSeams'; out.push(l); }
    }
    return out;
  }
  // A finish change only re-finishes the soft material (DICTO 2026-10-23: switching finish on a large build froze the app while it was
  // all rebuilt); Soft on/off and the Softness rebuild.
  let softWas = { on: softOn(), soft: softState().soft, amount: softState().amount };
  onSoftChange((st) => {
    const was = softWas;
    softWas = { on: softOn(), soft: st.soft, amount: st.amount };
    if (!active || !nodes.length) return;
    if (was.on && softWas.on && was.soft === st.soft && (was.amount === st.amount || !st.soft)) { applyFinish(softMat); return; }
    rebuild();
  });
  // A face of a piece as drawn in Soft (its cap and welts), or a curved shape's patch, just off the surface: for the tapped face and the glowing ones.
  function softFace(n, fi) {
    const g = puffedFor(n.shape, POLYHEDRA[n.shape]), P = g.attributes.position, N = g.attributes.normal, ids = g.userData.faceIds;
    const M = matrixOf(n), R = new THREE.Matrix3().getNormalMatrix(M), v = new THREE.Vector3(), w = new THREE.Vector3(), out = [];
    const lift = 0.004 * edgeLength(POLYHEDRA[n.shape]);
    for (let i = 0; i < P.count; i++) {
      if (ids[i] !== fi) continue;
      v.fromBufferAttribute(P, i).applyMatrix4(M); w.fromBufferAttribute(N, i).applyMatrix3(R).normalize();
      v.addScaledVector(w, lift); out.push(v.x, v.y, v.z);
    }
    return out;
  }

  function rebuild() {
    clearGroup();
    starStep.setVisible(active);
    if (!active) return;
    if (starStep.on) return; // the star step's own drawing stands in for the build (no tap targets)
    if (nodes.length && spherical) {
      for (const n of nodes) {
        const { centre, R } = sphereOf(n.shape);
        const m = new THREE.MeshStandardMaterial({ color: colorOf(n.shape, n.material, familiesFor(n.shape)[0]), transparent: opacity < 1, opacity, depthWrite: opacity >= 1 });
        const mesh = new THREE.Mesh(sphereGeometry, m);
        mesh.scale.setScalar(Math.max(1e-3, R * sphereScale));
        mesh.position.copy(centre.clone().applyQuaternion(new THREE.Quaternion(...n.transform.quaternion)).add(new THREE.Vector3(...n.transform.position)));
        mesh.userData.poly = 'sphere';
        mesh.userData.node = n;
        mesh.userData.ownMaterial = true;
        group.add(mesh);
        pickTargets.push(mesh);
      }
    } else if (nodes.length) {
      // Building a kit (DICTO 2026-10-13): the built pieces see-through while outlines show, so the next layer reads even when it
      // nestles behind them (Bodhi's Vajras round the centre).
      const see = kitGuiding() ? Math.min(opacity, 0.4) : opacity;
      pieceMaterial.transparent = see < 1;
      pieceMaterial.opacity = see;
      pieceMaterial.depthWrite = see >= 1;
      faceOwner = [];
      const inParts = (n) => view.parts !== 'solid' && PART_PICK[n.shape]?.[view.parts];
      const shown = nodes.filter((n) => !inParts(n)), parted = nodes.filter(inParts);
      const [mesh, lines] = meshOf(nodes, pieceMaterial, (n, c) => c.copy(colorOf(n.shape, n.material, familiesFor(n.shape)[0])), EDGE_COLOR, faceOwner);
      mesh.userData.poly = 'piece';
      mesh.visible = !skeleton;
      const soft = softOn();
      if (soft) {
        // Soft: the puffed copies drawn; the real pieces stay underneath, unseen, for taps.
        mesh.material = hiddenPickMaterial;
        lines.visible = false;
        group.add(...softMeshes(parted.length ? shown : nodes));
      }
      if (parted.length) {
        // Parts drawn in place of their solids; the solids stay underneath, unseen, for taps.
        mesh.material = hiddenPickMaterial;
        lines.visible = false;
        if (shown.length && !soft) { const [m2, l2] = meshOf(shown, pieceMaterial, (n, c) => c.copy(colorOf(n.shape, n.material, familiesFor(n.shape)[0])), EDGE_COLOR); m2.visible = !skeleton; if (skeleton) l2.material.color.setHex(theme().accentHex); group.add(m2, l2); }
        group.add(...partsMeshes(parted));
      }
      if (skeleton) lines.material.color.setHex(theme().accentHex);
      group.add(mesh, lines);
      pickTargets.push(mesh);
      // RCP-C2B cells (D5).
      if (view.rcp && rcpRoot()) {
        // Closed: the inner cells project inside the root (the nearest cell in 4D), so the root goes
        // see-through once any are built; it stays the tap target.
        const cx = rcpComplex();
        if (cx && view.rcp.n > 1 && !(view.rcp.open && builtShell(cx) <= 1)) mesh.material = rcpRootMaterial;
        const rm = rcpMeshes(); if (rm.length) group.add(...rm);
      }
      // What comes next: ghosts and glowing faces.
      if (!spherical) { const hm = hintMeshes(); if (hm.length) group.add(...hm); }
      if (pacioliOn()) group.add(...pacioliMeshes());
      if (cellsOn()) group.add(cellLines());
      // 4D Prism walls: the prism cell joining each face to the far copy, see-through.
      const walls = duoprismWalls();
      if (walls) group.add(...walls);
      // The tapped face, waiting for a shape: a bright overlay just off the surface.
      if (selection && nodes.includes(selection.node)) group.add(selection.corner != null ? cornerDot(selection.node, selection.corner) : faceHighlight(selection.node, selection.face));
    } else {
      outlineMaterial.color.setHex(theme().strongHex);
      const [mesh, lines] = meshOf([outlineNode()], outlineMaterial, (n, c) => c.setHex(theme().strongHex), theme().strongHex);
      mesh.userData.poly = 'outline';
      group.add(mesh, lines);
      pickTargets.push(mesh);
    }
  }

  // ---- building: tap attach (step D3, DICTO 2026-10-09) ----
  // Tap a face, then a shape: it attaches at once, at its best fit, placed automatically (DICTO
  // 2026-10-09: "no arrows, just automatic good placement"). That shape stays chosen, so each face
  // tapped next gets it in one tap, until another is picked (or ✕).
  let selection = null; // { node, face } or { node, corner }: a face or corner waiting for a shape
  let chosen = null; // the shape that stays chosen
  const PARALLELOHEDRA = new Set(familyIds('PARALLELOHEDRA'));
  const matrixOf = (n) => new THREE.Matrix4().compose(new THREE.Vector3(...n.transform.position), new THREE.Quaternion(...n.transform.quaternion), new THREE.Vector3(1, 1, 1));
  const duoFaces = (c) => [c.vertexA, ...(c.duoprismExtraFaces ?? [])];
  const faceTaken = (n, fi) => connections.some((c) => (c.kind === 'face' && ((c.nodeA === n.id && c.vertexA === fi) || (c.nodeB === n.id && c.vertexB === fi)))
    || (c.kind === 'duoprism' && (c.nodeA === n.id || c.nodeB === n.id) && duoFaces(c).includes(fi)));
  const cornerTaken = (n, vi) => connections.some((c) => c.kind === 'vertex' && ((c.nodeA === n.id && c.vertexA === vi) || (c.nodeB === n.id && c.vertexB === vi)));
  // Does shape `id` go on this face or corner? Any shape goes on a free corner.
  const fitsAt = (id, sel) => (sel.corner != null ? !!POLYHEDRA[id] : fits(id, sel.node, sel.face));
  // The faces of a shape that can go on this face (eligible and congruent), [] if none.
  function fittingFaces(id, n, fi) {
    const spec = POLYHEDRA[id], target = POLYHEDRA[n.shape];
    if (!spec) return [];
    const tf = target.faces[fi];
    // A face kept for one partner (faceMates, e.g. the Admiral Cap's two icosahedron faces, DICTO 2026-10-13) takes only that partner.
    if (target.faceMates?.[fi] && !target.faceMates[fi].includes(id)) return [];
    return spec.faces.map((f, k) => k).filter((k) => isFaceEligibleForAttach(spec, k) && (!spec.faceMates?.[k] || spec.faceMates[k].includes(n.shape))
      && spec.faces[k].length === tf.length && facesCongruent(target.vertices, tf, spec.vertices, spec.faces[k]));
  }
  // No merging (DICTO 2026-10-09: attached Hexas went into each other): a concave piece can sit flush
  // on a face and still pass through the rest, so every placement is tested against the whole build
  // (krp-core overlap.js); convex pairs keep the quick test the ranking already does.
  const placedCache = new Map();
  const placedOf = (n) => {
    const k = `${n.id}|${n.shape}|${n.transform.position}|${n.transform.quaternion}`;
    if (!placedCache.has(k)) placedCache.set(k, placedSolid(POLYHEDRA[n.shape], n.transform.position, n.transform.quaternion));
    return placedCache.get(k);
  };
  const clashes = (id, position, quaternion) => {
    const spec = POLYHEDRA[id], mine = placedSolid(spec, position, quaternion), convex = isConvex(spec);
    return nodes.some((x) => !(convex && isConvex(POLYHEDRA[x.shape])) && solidsOverlap(placedOf(x), mine));
  };
  const cleanOptions = (id, n, fi) => {
    const incoming = fittingFaces(id, n, fi);
    return incoming.length ? faceAttachOptions(POLYHEDRA[n.shape], fi, matrixOf(n), POLYHEDRA[id], incoming).filter((o) => !clashes(id, o.position.toArray(), o.quaternion.toArray())) : [];
  };
  // Offered only where at least one turn is clean.
  const fits = (id, n, fi) => fittingFaces(id, n, fi).length > 0 && cleanOptions(id, n, fi).length > 0;
  function faceHighlight(n, fi) {
    const P = worldPoints(n), f = POLYHEDRA[n.shape].faces[fi];
    const c = f.reduce((a, k) => a.add(P[k].clone()), new THREE.Vector3()).divideScalar(f.length);
    const nrm = P[f[1]].clone().sub(P[f[0]]).cross(P[f[2]].clone().sub(P[f[0]])).normalize();
    if (nrm.dot(c.clone().sub(P.reduce((a, v) => a.add(v.clone()), new THREE.Vector3()).divideScalar(P.length))) < 0) nrm.negate();
    const lift = nrm.multiplyScalar(0.004);
    let pos = [];
    if (softOn() || POLYHEDRA[n.shape].curved) pos = softFace(n, fi);
    else for (let i = 1; i < f.length - 1; i++) for (const k of [f[0], f[i], f[i + 1]]) { const q = P[k].clone().add(lift); pos.push(q.x, q.y, q.z); }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    const m = new THREE.Mesh(g, new THREE.MeshBasicMaterial({ color: theme().contrastHex, transparent: true, opacity: 0.75, side: THREE.DoubleSide, depthWrite: false }));
    m.userData.poly = 'highlight';
    return m;
  }
  // The tapped corner, waiting for a shape: a bright dot on it.
  const dotGeometry = new THREE.SphereGeometry(1, 16, 10);
  function cornerDot(n, vi) {
    const P = worldPoints(n), s = POLYHEDRA[n.shape];
    const m = new THREE.Mesh(dotGeometry, new THREE.MeshBasicMaterial({ color: theme().contrastHex, depthTest: false, transparent: true, opacity: 0.9 }));
    m.scale.setScalar(0.12 * edgeLength(s));
    m.position.copy(P[vi]);
    m.renderOrder = 10;
    m.userData.poly = 'highlight';
    return m;
  }
  const edgeLength = (s) => s.edges.reduce((t, [a, b]) => t + Math.hypot(...s.vertices[a].map((x, i) => x - s.vertices[b][i])), 0) / s.edges.length;
  const centreOf = (s) => s.vertices.reduce((a, v) => a.add(new THREE.Vector3(...v)), new THREE.Vector3()).divideScalar(s.vertices.length);
  // Corner attach (D3c): the new shape meets corner vi of node n with one of its own corners (one
  // with as many edges, else its first), pointing straight out, and turns about that line to the
  // best twist found by itself (DICTO: no arrows): no overlap with the build, then the most room.
  function attachCorner(id, n, vi) {
    const spec = POLYHEDRA[id], root = POLYHEDRA[n.shape];
    const deg = (s, v) => s.edges.filter((e) => e.includes(v)).length;
    const vInc = Math.max(0, spec.vertices.findIndex((_, k) => deg(spec, k) === deg(root, vi)));
    const rq = new THREE.Quaternion(...n.transform.quaternion), rp = new THREE.Vector3(...n.transform.position);
    const corner = new THREE.Vector3(...root.vertices[vi]).applyQuaternion(rq).add(rp);
    const out = new THREE.Vector3(...root.vertices[vi]).sub(centreOf(root)).applyQuaternion(rq).normalize();
    const localDir = new THREE.Vector3(...spec.vertices[vInc]).sub(centreOf(spec)).normalize();
    const base = new THREE.Quaternion().setFromUnitVectors(localDir, out.clone().negate());
    const others = nodes.map((x) => ({ spec: POLYHEDRA[x.shape], pts: worldPoints(x) }));
    const allPts = others.flatMap((o) => o.pts);
    const eps = 1e-6 * edgeLength(spec);
    // Every turn about the corner, roomiest first; the first that passes through nothing wins (concave
    // pieces are tested whole, so only as many as needed).
    const turns = [];
    for (let k = 0; k < 120; k++) {
      const q = base.clone().multiply(new THREE.Quaternion().setFromAxisAngle(localDir, (k * Math.PI) / 60));
      const pos = corner.clone().sub(new THREE.Vector3(...spec.vertices[vInc]).applyQuaternion(q));
      const pts = spec.vertices.map((v) => new THREE.Vector3(...v).applyQuaternion(q).add(pos));
      let room = Infinity;
      pts.forEach((p, i) => { if (i !== vInc) for (const r of allPts) room = Math.min(room, p.distanceTo(r)); });
      turns.push({ q, pos, pts, room });
    }
    turns.sort((x, y) => y.room - x.room);
    const allConvex = isConvex(spec) && others.every((o) => isConvex(o.spec));
    const clean = turns.find((tn) => (allConvex ? !others.some((o) => convexOverlap(spec, tn.pts, o.spec, o.pts, eps)) : !clashes(id, tn.pos.toArray(), tn.q.toArray())));
    if (!clean) { showHudPrompt(t('poly.noRoom', lang()), 3000); return false; }
    const best = { score: clean.room, q: clean.q, pos: clean.pos };
    remember(id);
    const node = { id: `n${nextId++}`, shape: id, transform: { position: best.pos.toArray(), quaternion: best.q.toArray() }, material: getMaterial() };
    nodes.push(node);
    connections.push({ nodeA: n.id, vertexA: vi, nodeB: node.id, vertexB: vInc, kind: 'vertex' });
    selection = null;
    commit();
    refitIfGrown();
    return true;
  }
  // 4D Prism (duoprism) attach (D3c): the same shape, same turn, pushed straight out from the tapped
  // face, joined to it by a prism cell. A real duoprism has one far copy, so a second face of the same
  // piece reuses it and gains its own wall.
  const wallMaterial = new THREE.MeshStandardMaterial({ color: 0x8fd3ff, transparent: true, opacity: 0.28, depthWrite: false, side: THREE.DoubleSide });
  function duoprismWalls() {
    const pos = [], edge = [];
    for (const c of connections) {
      if (c.kind !== 'duoprism') continue;
      const a = nodes.find((x) => x.id === c.nodeA), b = nodes.find((x) => x.id === c.nodeB);
      if (!a || !b) continue;
      const P = worldPoints(a), offset = new THREE.Vector3(...b.transform.position).sub(new THREE.Vector3(...a.transform.position)).toArray();
      for (const fi of duoFaces(c)) {
        const f = POLYHEDRA[a.shape].faces[fi];
        if (!f) continue;
        const w = buildWallPrism(f.map((k) => P[k].toArray()), offset);
        for (const face of w.faces.slice(2)) for (let i = 1; i + 1 < face.length; i++) for (const k of [face[0], face[i], face[i + 1]]) pos.push(...w.verts[k]);
        for (const [x, y] of w.edges) edge.push(...w.verts[x], ...w.verts[y]);
      }
    }
    if (!pos.length) return null;
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    g.computeVertexNormals();
    const lg = new THREE.BufferGeometry();
    lg.setAttribute('position', new THREE.Float32BufferAttribute(edge, 3));
    const m = new THREE.Mesh(g, wallMaterial);
    m.userData.poly = 'wall';
    return [m, new THREE.LineSegments(lg, new THREE.LineBasicMaterial({ color: 0x8fd3ff, transparent: true, opacity: 0.6 }))];
  }
  const FOURD = new Set(FOURD_CAPABLE_IDS);
  function duoprism(n, fi) {
    if (!FOURD.has(n.shape) || faceTaken(n, fi)) return false;
    const existing = connections.find((c) => c.kind === 'duoprism' && c.nodeA === n.id);
    if (existing) existing.duoprismExtraFaces = [...(existing.duoprismExtraFaces ?? []), fi];
    else {
      const spec = POLYHEDRA[n.shape], q = new THREE.Quaternion(...n.transform.quaternion);
      const normal = new THREE.Vector3(...buildFaceConnectors(spec)[fi].normal).applyQuaternion(q).normalize();
      const pos = new THREE.Vector3(...n.transform.position).addScaledVector(normal, duoprismBuildDepth(spec, fi));
      const far = { id: `n${nextId++}`, shape: n.shape, transform: { position: pos.toArray(), quaternion: [...n.transform.quaternion] }, material: n.material ?? getMaterial() };
      nodes.push(far);
      connections.push({ nodeA: n.id, vertexA: fi, nodeB: far.id, vertexB: fi, kind: 'duoprism' });
    }
    selection = null;
    commit();
    refitIfGrown();
    return true;
  }
  // Transform to… (D3c): a shape with a partner (the 10- and 12-face deltahedra) becomes it in place,
  // same position and turn; its corner joins move to the nearest matching corners and its face joins
  // let go (the neighbours never move).
  function transform(n) {
    const to = REWRITE_TARGET[n.shape];
    if (!to) return false;
    const mine = connections.filter((c) => c.nodeA === n.id || c.nodeB === n.id);
    const corners = mine.filter((c) => c.kind === 'vertex');
    const old = corners.map((c) => (c.nodeA === n.id ? c.vertexA : c.vertexB));
    const match = matchRewriteVertices(n.shape, to, old);
    connections = connections.filter((c) => !mine.includes(c) || (c.kind === 'vertex' && match[corners.indexOf(c)] !== undefined));
    corners.forEach((c, i) => { if (match[i] === undefined) return; if (c.nodeA === n.id) c.vertexA = match[i]; else c.vertexB = match[i]; });
    n.shape = to;
    selection = null;
    remember(to);
    commit();
    return true;
  }
  const attachAt = (id, sel) => (sel.corner != null ? attachCorner(id, sel.node, sel.corner) : attach(id, sel.node, sel.face));
  // Attach shape `id` on face fi of node n, the best fit first; false if it doesn't fit there.
  function attach(id, n, fi) {
    const spec = POLYHEDRA[id];
    const options = cleanOptions(id, n, fi);
    if (!options.length) { if (fittingFaces(id, n, fi).length) showHudPrompt(t('poly.noRoom', lang()), 3000); return false; }
    const built = nodes.map((x) => ({ spec: POLYHEDRA[x.shape], matrixWorld: matrixOf(x) }));
    const ranked = rankFaceAttachOptions(options, spec, built, nodes.indexOf(n), fi, id === n.shape && PARALLELOHEDRA.has(id));
    const best = ranked[0].option;
    remember(id);
    const node = { id: `n${nextId++}`, shape: id, transform: { position: best.position.toArray(), quaternion: best.quaternion.toArray() }, material: getMaterial() };
    nodes.push(node);
    connections.push({ nodeA: n.id, vertexA: fi, nodeB: node.id, vertexB: best.incomingFaceIndex, kind: 'face' });
    selection = null;
    commit();
    refitIfGrown();
    return true;
  }
  // Keep the build in view as it grows: refit when it reaches well past the last fitted size (not on
  // every tap, which would jump about).
  let fittedRadius = 0;
  function refitIfGrown() {
    // The ghosts of what comes next count too, so they stay in view.
    const ghostR = hints().slots.map((sl) => Math.hypot(...sl.position) + Math.max(...POLYHEDRA[sl.shape].vertices.map((v) => Math.hypot(...v))));
    const r = Math.max(...nodes.flatMap((n) => worldPoints(n).map((v) => v.length())), ...ghostR);
    if (r > fittedRadius * 1.25) { fittedRadius = r; fitView?.(r); }
  }
  function remove(n) {
    nodes = nodes.filter((x) => x !== n);
    connections = connections.filter((c) => c.nodeA !== n.id && c.nodeB !== n.id);
    if (selection?.node === n) selection = null;
    commit();
  }

  function commit() { if (starStep.on) starStep.reset(); save(); rebuild(); onChange(); renderPanel(); renderName(); }
  function handleTap(hit, mode) {
    const kind = hit.object.userData.poly;
    if (kind === 'outline') {
      if (mode === 'chisel' || mode === 'paint') return false;
      nodes.push({ ...outlineNode(), id: `n${nextId++}`, material: getMaterial() });
      commit();
      refitIfGrown();
      return true;
    }
    if (kind === 'ghost') { if (mode === 'chisel' || mode === 'paint') return false; return placeSlot(hit.object.userData.slot); }
    if (kind !== 'piece' && kind !== 'sphere') return false;
    const rec = kind === 'sphere' ? { node: hit.object.userData.node, face: null } : faceOwner[hit.faceIndex];
    const n = rec?.node;
    if (!n) return false;
    if (mode === 'chisel') { remove(n); return true; }
    if (mode === 'paint') {
      const m = getMaterial();
      if (n.material === m) return false;
      n.material = m; commit(); return true;
    }
    if (rec.face == null) return false; // spheres: no faces to attach to
    // A glowing face: the piece that goes there, in its place.
    const glowing = hints().glow.get(`${n.id}:${rec.face}`);
    if (glowing !== undefined) return placeSlot(glowing);
    // A tap within a finger's reach of a corner picks the corner (a dot shows it), anywhere else the face.
    const s = POLYHEDRA[n.shape], P = worldPoints(n);
    let vi = -1, d = Infinity;
    for (const k of s.faces[rec.face]) { const dk = P[k].distanceTo(hit.point); if (dk < d) { d = dk; vi = k; } }
    const sel = d < 0.22 * edgeLength(s) ? { node: n, corner: vi } : { node: n, face: rec.face };
    if (sel.corner != null ? cornerTaken(n, vi) : faceTaken(n, rec.face)) { showHudPrompt(t('poly.taken', lang()), 2000); return false; }
    // The chosen shape goes straight on when it fits; otherwise the face or corner waits for a shape.
    if (chosen && fitsAt(chosen, sel) && attachAt(chosen, sel)) return true;
    selection = sel;
    rebuild();
    renderPanel();
    if (!queue().some((id) => fitsAt(id, sel))) showHudPrompt(t('poly.noFit', lang()), 3000);
    return true;
  }

  // ---- RCP-C2B, 4D build (step D5, from Polyhedraverse): the first piece, if it is a 4D seed (tetrahedron,
  // cube, octahedron, dodecahedron), grows cell by cell into a 4D polytope's 3D shadow (krp-core
  // rcpBuild): shell 1 a cell at a time, then a whole shell per tap; Open shows shell 1 as true copies of
  // the seed on its faces, Closed their real projected positions (locked once shell 2 is built, which is
  // anchored there); RCP-Coordinates marks each cell's own 4D coordinate. Shells in their own colours.
  const rcpRoot = () => (nodes[0] && FOUR_D_SHAPE_PARAMS[nodes[0].shape] ? nodes[0] : null);
  const rcpTargets = (id) => rcpTargetOptions((FOUR_D_SHAPE_PARAMS[id] ?? []).map((o) => o.name));
  const complexCache = new Map();
  function rcpComplex() {
    const root = rcpRoot();
    if (!root || !view.rcp) return null;
    if (!rcpTargets(root.shape).includes(view.rcp.target)) view.rcp.target = rcpTargets(root.shape)[0];
    const k = `${root.shape}|${view.rcp.target}`;
    if (!complexCache.has(k)) complexCache.set(k, buildRcpComplex(root.shape, view.rcp.target));
    return complexCache.get(k);
  }
  // The build order: shell by shell, cell by cell; n cells built (cell 0 is the root itself).
  const rcpOrder = (cx) => [...cx.cells].sort((a, b) => a.shell - b.shell || a.id - b.id);
  const builtShell = (cx) => rcpOrder(cx)[Math.max(0, (view.rcp?.n ?? 1) - 1)]?.shell ?? 0;
  const SHELL_COLOURS = [0x5ee233, 0x22c3e6, 0xffc857, 0xc792ea, 0xff8a65, 0x7ae0b8];
  // Open: a shell-1 cell as a true copy of the seed, flush on the root face it shares, nearest its closed place.
  function openCellPoints(cx, cell) {
    const seed = POLYHEDRA[cx.seedSpecId], R = seed.vertices;
    const shared = cell.vertices3D.map((v) => R.findIndex((r) => Math.hypot(...r.map((x, i) => x - v[i])) < 1e-5)).filter((i) => i >= 0);
    const fi = seed.faces.findIndex((f) => f.every((v) => shared.includes(v)));
    if (fi < 0) return cell.vertices3D;
    const ids = seed.faces.map((_, k) => k).filter((k) => seed.faces[k].length === seed.faces[fi].length);
    const opts = faceAttachOptions(seed, fi, new THREE.Matrix4(), seed, ids);
    const target = cell.vertices3D.reduce((t, v) => t.map((x, i) => x + v[i] / cell.vertices3D.length), [0, 0, 0]);
    let best = null;
    for (const o of opts) {
      const pts = seed.vertices.map((v) => new THREE.Vector3(...v).applyQuaternion(o.quaternion).add(o.position).toArray());
      const c = pts.reduce((t, v) => t.map((x, i) => x + v[i] / pts.length), [0, 0, 0]);
      const d = Math.hypot(...c.map((x, i) => x - target[i]));
      if (!best || d < best.d) best = { d, pts };
    }
    return best ? best.pts : cell.vertices3D;
  }
  function rcpMeshes() {
    const cx = rcpComplex(), root = rcpRoot();
    if (!cx || !root) return [];
    const q = new THREE.Quaternion(...root.transform.quaternion), p0 = new THREE.Vector3(...root.transform.position);
    const at = (v) => new THREE.Vector3(...v).applyQuaternion(q).add(p0);
    const seed = POLYHEDRA[cx.seedSpecId], order = rcpOrder(cx), n = Math.min(view.rcp.n, order.length);
    const open = view.rcp.open && builtShell(cx) <= 1;
    const pos = [], col = [], edge = [], c = new THREE.Color();
    for (const cell of order.slice(1, n)) {
      const pts = open && cell.shell === 1 ? openCellPoints(cx, cell) : cell.vertices3D;
      const spec = buildSyntheticCellSpec(seed, cell.id, pts);
      c.setHex(SHELL_COLOURS[cell.shell % SHELL_COLOURS.length]);
      const P = spec.vertices.map(at);
      for (const f of spec.faces) for (let i = 1; i + 1 < f.length; i++) for (const k of [f[0], f[i], f[i + 1]]) { pos.push(P[k].x, P[k].y, P[k].z); col.push(c.r, c.g, c.b); }
      for (const [a, b] of spec.edges) edge.push(P[a].x, P[a].y, P[a].z, P[b].x, P[b].y, P[b].z);
    }
    const out = [];
    if (pos.length) {
      const g = new THREE.BufferGeometry();
      g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute('color', new THREE.Float32BufferAttribute(col, 3)); g.computeVertexNormals();
      const m = new THREE.Mesh(g, open ? pieceMaterial : rcpCellMaterial); m.userData.poly = 'rcp'; m.visible = !skeleton;
      const lg = new THREE.BufferGeometry(); lg.setAttribute('position', new THREE.Float32BufferAttribute(edge, 3));
      out.push(m, new THREE.LineSegments(lg, new THREE.LineBasicMaterial({ color: skeleton ? theme().accentHex : EDGE_COLOR })));
    }
    if (view.rcp.coords) {
      // Each built cell's own 4D coordinate, projected: a thin line from the centre and a small cross; the
      // next shell's dimmed.
      const nextShell = builtShell(cx) + 1, lines = [], dim = [];
      const r = 0.06 * Math.max(...seed.vertices.map((v) => Math.hypot(...v)));
      for (const cell of order) {
        const built = order.indexOf(cell) < n;
        if (!built && cell.shell !== nextShell) continue;
        const into = built ? lines : dim, cp = at(cell.coordPoint3D), o = at([0, 0, 0]);
        into.push(o.x, o.y, o.z, cp.x, cp.y, cp.z);
        for (const d of [[r, 0, 0], [0, r, 0], [0, 0, r]]) into.push(cp.x - d[0], cp.y - d[1], cp.z - d[2], cp.x + d[0], cp.y + d[1], cp.z + d[2]);
      }
      for (const [list, op] of [[lines, 0.9], [dim, 0.3]]) if (list.length) {
        const lg = new THREE.BufferGeometry(); lg.setAttribute('position', new THREE.Float32BufferAttribute(list, 3));
        out.push(new THREE.LineSegments(lg, new THREE.LineBasicMaterial({ color: 0xc792ea, transparent: true, opacity: op, depthTest: false })));
      }
    }
    return out;
  }
  function rcpRow(L) {
    const root = rcpRoot();
    if (!root || nodes.length !== 1) return '';
    const targets = rcpTargets(root.shape);
    if (!view.rcp) return `<div class="poly-golden"><button type="button" data-rcp-start>${t('poly.rcp.start', L)}</button></div>`;
    const cx = rcpComplex(), order = rcpOrder(cx), n = Math.min(view.rcp.n, order.length), shell = builtShell(cx), top = maxShell(cx);
    const shell1 = order.filter((c) => c.shell === 1).length, done = n >= order.length;
    const next = done ? t('poly.rcp.complete', L) : shell < 1 || (shell === 1 && n - 1 < shell1) ? t('poly.rcp.nextCell', L, { i: n, k: shell1 }) : t('poly.rcp.nextShell', L, { s: shell + 1, m: top });
    const locked = shell >= 2;
    return `<div class="poly-golden"><span>${t('poly.rcp.title', L)}</span>
      <select data-rcp-target aria-label="${t('poly.rcp.target', L)}">${targets.map((x) => `<option value="${x}"${x === view.rcp.target ? ' selected' : ''}>${x}</option>`).join('')}</select>
      <button type="button" data-rcp-next${done ? ' disabled' : ''}>${next}</button>
      <button type="button" data-rcp-back${n <= 1 ? ' disabled' : ''}>${t('poly.rcp.remove', L)}</button>
      <button type="button" data-rcp-open${locked ? ' disabled' : ''} title="${locked ? t('poly.rcp.locked', L) : ''}">${view.rcp.open && !locked ? t('poly.rcp.open', L) : t('poly.rcp.closed', L)}</button>
      <button type="button" data-rcp-coords aria-pressed="${view.rcp.coords}">${t('poly.rcp.coords', L)}</button></div>`;
  }
  function rcpAct(b) {
    const cx = () => rcpComplex();
    if ('rcpStart' in b.dataset) { view.rcp = { target: rcpTargets(rcpRoot().shape)[0], n: 1, open: true, coords: false }; }
    else if ('rcpNext' in b.dataset) {
      const order = rcpOrder(cx()), n = view.rcp.n, shell = builtShell(cx());
      const shell1 = order.filter((c) => c.shell === 1).length;
      if (shell < 1 || (shell === 1 && n - 1 < shell1)) view.rcp.n = n + 1; // shell 1: one cell
      else { const s2 = shell + 1; view.rcp.n = order.filter((c) => c.shell <= s2).length; view.rcp.open = false; } // a whole shell, anchored Closed
    } else if ('rcpBack' in b.dataset) {
      const order = rcpOrder(cx()), shell = builtShell(cx());
      view.rcp.n = shell >= 2 ? order.filter((c) => c.shell < shell).length : Math.max(1, view.rcp.n - 1);
    } else if ('rcpOpen' in b.dataset) view.rcp.open = !view.rcp.open;
    else if ('rcpCoords' in b.dataset) view.rcp.coords = !view.rcp.coords;
    else return false;
    save(); rebuild(); renderPanel();
    return true;
  }

  // ---- the shape strip ----
  // Shapes to offer: the build's own (newest first) and the shape last chosen in DICTO, up to 8.
  function queue() {
    const out = [];
    for (const id of [...favourites(), chosen, ...recent(), ...nodes.map((n) => n.shape).reverse(), view.shape]) if (id && POLYHEDRA[id] && !out.includes(id)) out.push(id);
    return out.slice(0, 8 + favourites().length);
  }
  // Remember a shape used, newest first; saved with the build.
  const remember = rememberShape;
  onPrefsChange(() => { if (active) renderPanel(); });
  const panel = document.createElement('div');
  panel.className = 'qc-panel poly-strip';
  const stripBody = document.createElement('div');
  stripBody.className = 'poly-strip-body';
  panel.appendChild(stripBody);
  document.body.appendChild(panel);
  addPanelMinimiser(panel, 'poly');
  let disposers = [];
  // The Golden helper (D3c), for a build of golden rhombohedra only: how many pieces sit in the true
  // 3D Penrose tiling (a build inside it can always go on), the next piece that keeps it there, and
  // the golden zonohedra built step by step.
  let recipe = GOLDEN_BUILDS[2].axes;
  const golden = () => nodes.length > 0 && isGoldenBuild({ nodes, connections });
  function goldenRow(L) {
    const st = goldenStatus({ nodes, connections });
    if (!st) return '';
    return `<div class="poly-golden"><span>${t('poly.golden.status', L, { n: st.inTiling, total: st.total })}</span>
      <button type="button" data-golden-next>${t('poly.golden.next', L)}</button>
      <select data-golden-recipe aria-label="${t('poly.golden.recipe', L)}">${GOLDEN_BUILDS.map((b) => `<option value="${b.axes}"${b.axes === recipe ? ' selected' : ''}>${b.name}</option>`).join('')}</select>
      <button type="button" data-golden-step>${t('poly.golden.step', L)}</button></div>`;
  }
  function takeAssembly(a) {
    if (!a) return false;
    const mat = getMaterial();
    setFromJSON({ nodes: a.nodes.map((n) => ({ ...n, material: n.material ?? mat })), connections: a.connections });
    selection = null;
    commit();
    refitIfGrown();
    return true;
  }
  function bestRow(L) {
    const st = bestHints();
    if (st.busy) return `<div class="poly-golden poly-best-status">${t('poly.best.finding', L)}</div>`;
    if (!st.slots.length) return `<div class="poly-golden poly-best-status">${t('poly.best.none', L)}</div>`;
    return `<div class="poly-golden poly-best">${st.slots.map((sl, i) => `<button type="button" data-best-pick="${i}" style="border-color:#${sl.colour.toString(16).padStart(6, '0')};color:#${sl.colour.toString(16).padStart(6, '0')}">${polyShapeName(sl.shape).replaceAll('_', ' ')} · ${t(sl.closes === 1 ? 'poly.best.closes1' : 'poly.best.closes', L, { n: sl.closes })}</button>`).join('')}</div>`;
  }
  function renderPanel() {
    disposers.forEach((d) => d()); disposers = [];
    const isGolden = active && !spherical && golden();
    const hasParts = active && !spherical && nodes.some((n) => PART_PICK[n.shape]);
    const hasRcp = active && !spherical && rcpRoot() && nodes.length === 1;
    const hasHintRow = active && !spherical && hasHints();
    const hasBestRow = active && !spherical && nodes.length > 0;
    const hasStar = !!starTarget() || (active && starStep.on);
    const show = active && !spherical && (selection || chosen || isGolden || hasParts || hasRcp || hasHintRow || hasBestRow || hasStar);
    panel.classList.toggle('visible', Boolean(show));
    if (!show) return;
    const L = lang();
    // While the star step runs, its row alone: the build's helpers don't apply to the star.
    if (starStep.on) { stripBody.innerHTML = starRow(L); return; }
    const offer = selection ? queue().filter((id) => fitsAt(id, selection)) : chosen ? [chosen] : [];
    stripBody.innerHTML = `<div class="poly-shapes">${offer.map((id) => { const pinned = isFavourite(id); return `<button type="button" class="poly-shape${id === chosen ? ' chosen' : ''}${pinned ? ' pinned' : ''}" data-shape="${id}" title="${polyShapeName(id).replaceAll('_', ' ')} · ${t(pinned ? 'poly.unpinHint' : 'poly.pinHint', L)}"><canvas></canvas></button>`; }).join('')}
      ${selection ? `<button type="button" class="poly-more" data-more>${t('poly.more', L)}</button>` : ''}
      ${selection && selection.face != null && FOURD.has(selection.node.shape) ? `<button type="button" class="poly-more" data-duoprism>${t('poly.duoprism', L)}</button>` : ''}
      ${selection && REWRITE_TARGET[selection.node.shape] ? `<button type="button" class="poly-more" data-transform>${t('poly.transform', L, { name: polyShapeName(REWRITE_TARGET[selection.node.shape]).replaceAll('_', ' ') })}</button>` : ''}
      ${chosen ? `<button type="button" class="poly-clear" data-clear title="${t('poly.clear', L, { name: polyShapeName(chosen).replaceAll('_', ' ') })}">✕</button>` : ''}</div>${isGolden ? goldenRow(L) : ''}${hasRcp ? rcpRow(L) : ''}${kitOn() ? `<div class="poly-golden poly-kit-row"><span>${t(kitDone() ? 'poly.kit.done' : 'poly.kit', L, { name: KITS13[view.kit].label })}</span>${kitCells() ? `<button type="button" data-cells aria-pressed="${!!view.cells}" title="${t('poly.cells.title', L)}">${t('poly.cells', L)}</button>` : ''}${kitIco() ? `<button type="button" data-pacioli aria-pressed="${!!view.pacioli}" title="${t('poly.pacioli.title', L)}">${t('poly.pacioli', L)}</button>` : ''}<button type="button" data-kit-off title="${t('poly.kit.off', L)}">✕</button></div>` : ''}${hasHintRow || hasBestRow ? `<div class="poly-golden">${hasHintRow ? `<button type="button" data-hints aria-pressed="${view.hints && !view.bestFits}" title="${t('poly.hints.title', L)}">${t('poly.hints', L)}</button>` : ''}${hasBestRow ? `<button type="button" data-best aria-pressed="${view.bestFits}" title="${t('poly.best.title', L)}">${t('poly.best', L)}</button>` : ''}</div>${hasBestRow && view.bestFits ? bestRow(L) : ''}` : ''}${hasParts ? `<label class="poly-golden">${t('poly.parts', L)} <select data-parts>${PART_VIEWS.filter((v) => v === 'solid' || nodes.some((n) => PART_PICK[n.shape]?.[v])).map((v) => `<option value="${v}"${v === view.parts ? ' selected' : ''}>${t(`poly.parts.${v}`, L)}</option>`).join('')}</select></label>` : ''}${hasStar ? starRow(L) : ''}`;
    stripBody.querySelectorAll('.poly-shape canvas').forEach((cv) => disposers.push(mountWireframePreview(cv, polyShapeEdges(cv.parentElement.dataset.shape), 34)));
  }
  panel.addEventListener('change', (e) => {
    if (e.target.matches('[data-golden-recipe]')) recipe = Number(e.target.value);
    if (e.target.matches('[data-star-rule]')) { starStep.setRule(e.target.value); renderPanel(); }
    if (e.target.matches('[data-parts]')) { view.parts = e.target.value; save(); rebuild(); }
    if (e.target.matches('[data-rcp-target]')) { view.rcp.target = e.target.value; view.rcp.n = 1; view.rcp.open = true; save(); rebuild(); renderPanel(); }
  });
  // Long-press a shape in the strip to pin it (always offered) or unpin it.
  let pressTimer = 0, pressed = false;
  panel.addEventListener('pointerdown', (e) => {
    const b = e.target.closest('.poly-shape');
    if (!b) return;
    pressed = false;
    pressTimer = setTimeout(() => {
      pressed = true;
      const id = b.dataset.shape;
      toggleFavourite(id);
      save();
      renderPanel();
    }, 550);
  });
  for (const ev of ['pointerup', 'pointerleave', 'pointercancel']) panel.addEventListener(ev, () => clearTimeout(pressTimer));
  panel.addEventListener('click', (e) => {
    const b = e.target.closest('button');
    if (!b) return;
    if (pressed) { pressed = false; return; } // that was a long-press (pin), not a tap
    if ('clear' in b.dataset) { chosen = null; renderPanel(); return; }
    if ('star' in b.dataset) {
      if (!starStep.on) { const n = starTarget(); if (!n || !starStart(n)) return; selection = null; rebuild(); }
      starStep.advance();
      renderPanel();
      return;
    }
    if ('starReset' in b.dataset) { starReset(); return; }
    if ('starLayer' in b.dataset) { starStep.toggleLayer(); renderPanel(); return; }
    if (rcpAct(b)) return;
    if ('hints' in b.dataset) { if (view.bestFits) { view.bestFits = false; view.hints = true; } else view.hints = !view.hints; save(); rebuild(); renderPanel(); return; }
    if ('cells' in b.dataset) { view.cells = !view.cells; save(); rebuild(); renderPanel(); return; }
    if ('pacioli' in b.dataset) { view.pacioli = !view.pacioli; save(); rebuild(); renderPanel(); return; }
    if ('kitOff' in b.dataset) { view.kit = null; save(); rebuild(); renderPanel(); return; }
    if ('best' in b.dataset) { view.bestFits = !view.bestFits; save(); rebuild(); renderPanel(); return; }
    if ('bestPick' in b.dataset) { placeSlot(Number(b.dataset.bestPick)); return; }
    if ('transform' in b.dataset && selection) { transform(selection.node); return; }
    if ('duoprism' in b.dataset && selection) { duoprism(selection.node, selection.face); return; }
    if ('goldenNext' in b.dataset) { if (!takeAssembly(withNextSafePiece({ nodes, connections }))) showHudPrompt(t('poly.golden.none', lang()), 3000); return; }
    if ('goldenStep' in b.dataset) {
      const r = withNextRecipePiece({ nodes, connections }, recipe);
      if (takeAssembly(r.assembly)) showHudPrompt(t('poly.golden.stepNote', lang(), { name: GOLDEN_BUILDS.find((x) => x.axes === recipe).name, i: r.step, total: r.total }), 2500);
      return;
    }
    if ('more' in b.dataset && selection) {
      const sel = selection;
      pickShape((id) => fitsAt(id, sel), (id) => { chosen = id; attachAt(id, sel); }, { partners: pairPartners(sel.node.shape) });
      return;
    }
    if (b.dataset.shape) {
      const id = b.dataset.shape;
      if (selection) { chosen = id; attachAt(id, selection); }
      else { chosen = chosen === id ? null : id; renderPanel(); }
    }
  });

  // ---- the running build name (D3b): one shortened line under the dimension label; a tap shows it
  // whole. Named builds are recognised (DICTO-Star, Stella Octangula, …), else the pieces listed.
  const nameEl = document.createElement('button');
  nameEl.type = 'button';
  nameEl.id = 'poly-build-name';
  nameEl.hidden = true;
  document.body.appendChild(nameEl);
  nameEl.addEventListener('click', () => nameEl.classList.toggle('open'));
  function renderName() {
    const name = active && nodes.length > 1 ? describeAssembly(nodes, connections) : '';
    nameEl.hidden = !name;
    if (nameEl.textContent !== name) { nameEl.textContent = name; nameEl.classList.remove('open'); }
  }

  let shownLang = lang();
  onSettingsChange((st) => { if (st.language !== shownLang) { shownLang = st.language; renderPanel(); if (active) rebuild(); } });

  return {
    group,
    meshes: () => (kitGuiding() ? pickTargets.filter((m) => m.userData.poly === 'ghost') : pickTargets),
    handleTap,
    setActive(on) {
      if (on === active) return;
      active = on;
      group.visible = on;
      if (!on) selection = null;
      rebuild();
      renderPanel();
      renderName();
    },
    setSkeleton(on) { skeleton = on; if (active) { rebuild(); starStep.redraw(); } },
    /** Soft applies to the pieces as they are: not to Skeleton, Spherical or a 4D cell build (their own drawing). */
    softApplies: () => active && !skeleton && !spherical && !view.rcp,
    setTranslucent(o) { if (o !== opacity) { opacity = o; if (active) { rebuild(); starStep.redraw(); } } },
    setLatticeView() { /* no lattice here: shapes are placed freely */ },
    refresh() { if (active) rebuild(); },
    setSpherical(on, scale = 1) { if (on === spherical && scale === sphereScale) return; spherical = on; sphereScale = scale; const wasStar = starStep.on; if (on) starStep.reset(); if (active) { rebuild(); if (wasStar) renderPanel(); } },
    /** DICTO's shape list: build with this shape. An empty world shows its outline to tap; with a
     *  build, it becomes the chosen shape, going straight onto each face tapped. */
    startWith(id) {
      if (!POLYHEDRA[id]) return;
      view.shape = id;
      remember(id);
      if (nodes.length) { chosen = id; commit(); showHudPrompt(t('poly.chosen', lang(), { name: polyShapeName(id).replaceAll('_', ' ') }), 3000); return; }
      commit();
      fittedRadius = Math.max(...POLYHEDRA[id].vertices.map((v) => Math.hypot(...v)));
      fitView?.(fittedRadius);
      showHudPrompt(polyShapeName(id), 2500);
    },
    // A 13 kit (DICTO 2026-10-13): its centre piece alone, and the kit's outlines showing where the next pieces go. Over an
    // existing build it asks first; Cancel keeps the build and lines the kit up with whatever of it is already there.
    startKit(id) {
      const kit = KITS13[id];
      if (!kit) return;
      view.kit = id; view.hints = true; view.bestFits = false;
      if (!nodes.length || confirm(t('poly.kit.replace', lang()))) {
        const e = kit.entries[0];
        nodes = [{ id: `n${nextId++}`, shape: e.shape, transform: { position: [...e.position], quaternion: [...e.quaternion] }, material: getMaterial() }];
        connections = []; selection = null; chosen = null;
      }
      view.shape = kit.entries[0].shape;
      commit();
      // Framed on the centre and its next layer (the build refits as it grows), not the whole finished kit.
      const reach = (sh, pos) => Math.hypot(...pos) + Math.max(...POLYHEDRA[sh].vertices.map((v) => Math.hypot(...v)));
      fittedRadius = Math.max(...nodes.map((n) => reach(n.shape, n.transform.position)), ...hints().slots.map((sl) => reach(sl.shape, sl.position)));
      fitView?.(fittedRadius);
      showHudPrompt(kit.label, 2500);
    },
    // A 4D polytope's Build (D5): its seed alone, growing into the polytope (RCP-C2B), shell 1 open.
    startPolytope(seed, target) {
      if (!POLYHEDRA[seed]) return;
      if (nodes.length && !confirm(t('polytope.replace', lang()))) return;
      nodes = [{ ...outlineNode(), shape: seed, id: `n${nextId++}`, material: getMaterial() }];
      connections = []; selection = null; chosen = null;
      view.shape = seed;
      view.rcp = { target, n: 1, open: true, coords: false };
      commit();
      fittedRadius = 2.2 * Math.max(...POLYHEDRA[seed].vertices.map((v) => Math.hypot(...v)));
      fitView?.(fittedRadius);
    },
    /** ?open=starstep:<id>[:<k>] (the Star Cores papers' "View in app"): the star step on shape `id`, k steps on (no animation).
     *  The build is left as it is; an empty world shows `id`'s outline once the star step is reset. */
    openStarStep(id, k = 0) {
      if (!active || !starOk(id)) return false;
      const n = nodes.length === 1 && nodes[0].shape === id ? nodes[0] : { ...outlineNode(), shape: id };
      if (!starStart(n)) return false;
      selection = null;
      for (let i = 0; i < k; i++) starStep.advance(true);
      fittedRadius = Math.max(...POLYHEDRA[id].vertices.map((v) => Math.hypot(...v)));
      fitView?.(starStep.reach, true); // framed on what the link shows, nearer as well as farther
      rebuild(); renderPanel();
      return true;
    },
    starProbe: () => starStep.probe(),
    get shape() { return view.shape; },
    get isEmpty() { return nodes.length === 0; },
    clear() { nodes = []; connections = []; selection = null; chosen = null; commit(); },
    snapshot: toJSON,
    restore(json) { starStep.reset(); setFromJSON(json); selection = null; save(); rebuild(); renderPanel(); renderName(); onChange(); },
    toJSON,
  };
}
