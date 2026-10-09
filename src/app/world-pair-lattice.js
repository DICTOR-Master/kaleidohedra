// Pair lattices (direct requests, 2026-10-08): 3D+ worlds of two pieces that fill space together
// in a checkerboard on the cubic cells, one piece on the even cells and the other on the odd (the
// face-centred cubic lattice with two pieces per point). Tap a face to add the piece across it;
// long-press to remove. Views show both pieces or either alone. The Shear either moves the cell
// centres and keeps every piece exact (copies), or bends the whole packing (solid). The five-fold
// toggle overlays each even piece's five-fold axes (and, where given, more lines per piece).
// Each world is a config: the Stella–Jewel Lattice (world-stella-jewel.js) and the Sunstar
// Lattice (world-sunstar.js). Geometry in krp-core/src/geometry-extensions/roof-fold.js, checked in
// scripts/verify-roof-fold.mjs.
import * as THREE from 'three';
import { KAGOME_HULLS, KAGOME_HULL_IDS, kagomeHullSolids } from '../krp-core/src/polyhedra/kagomeHulls.js';
import { ROOF_FOLD_WORLD_SCALE as WS, DJ_NEIGHBOURS, fiveFoldAxes } from '../krp-core/src/geometry-extensions/roof-fold.js';
import { t } from './i18n.js';
import { getSettings, onSettingsChange } from './settings.js';
import { addPanelMinimiser } from './panel-minimiser.js';
import { theme, storageKey } from './site.js';

const EDGE_COLOR = 0x0b1220;
const GHOST_COLOR = () => theme().accentHex; // read when drawing: follows the app whose space you're in
// "Tap here first": the theme's contrast colour (cyan against Kaleidohedra's orange, amber against
// Rhombiverse's cyan), read when drawing so it follows the app whose space you're in.
const firstColour = () => theme().contrastHex;
const AXIS_COLOR = 0xffffff;
const lang = () => getSettings().language;
const key = (s) => s.join(',');
const isEven = (s) => (((s[0] + s[1] + s[2]) % 2) + 2) % 2 === 0;

/**
 * config: { storageKey, panelId, minimiser, strings (key prefix), modes [{ id, even, odd, grouped, nested }],
 * nestedFaces (drawn inside every even piece in a nested mode, the even piece then see-through),
 * chainLayers [{ faces, opacity }] (drawn inside every even piece in a chain mode, innermost last),
 * group(evenSite) -> the odd sites that come with an even piece in a grouped mode,
 * evenFaces / oddFaces ([polygon, colour] in cell units), insideEven / insideOdd (p in cell units,
 * centred on the cell), overlay(s) -> { faint, bright } extra line segments per even piece (optional),
 * brightColor, holePrompt (true: a tap toward a hidden piece explains; false: it adds the nearest
 * shown piece instead, as corner-sharing pieces need) }.
 */
export function createPairLatticeWorld({ scene, fitView = () => {}, shear = () => null, showHudPrompt = () => {}, onChange = () => {} }, config) {
  const { storageKey: STORAGE_KEY, strings: S_, modes: MODE_LIST } = config;
  const MODES = MODE_LIST.map((m) => m.id);
  const modeOf = () => MODE_LIST.find((m) => m.id === view.mode) ?? MODE_LIST[0];
  const showsSite = (s) => (isEven(s) ? modeOf().even : modeOf().odd);
  const group = new THREE.Group();
  group.visible = false;
  scene.add(group);
  const AXES = fiveFoldAxes();

  // ---- state ----
  const cells = new Map(); // key -> [x, y, z]
  const view = { mode: MODES[0], shear: 'solid', axes: false }; // solid by default: sheared pieces stay face to face (DICTO 2026-10-09)
  let active = false, skeleton = false, opacity = 1, latticeView = false;
  function read(data) {
    cells.clear();
    for (const s of Array.isArray(data?.cells) ? data.cells : []) if (Array.isArray(s) && s.length === 3 && s.every(Number.isInteger)) cells.set(key(s), [...s]);
    if (MODES.includes(data?.view?.mode)) view.mode = data.view.mode;
    if (['copies', 'solid'].includes(data?.view?.shear)) view.shear = data.view.shear;
    view.axes = data?.view?.axes === true;
  }
  try { read(JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null')); } catch { /* corrupt or blocked storage: start empty */ }
  const snapshot = () => ({ version: 1, cells: [...cells.values()], view: { ...view } });
  const save = () => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(snapshot())); } catch { /* best-effort */ } };
  const shown = () => [...cells.values()].filter(showsSite);

  // ---- placement through the shear ----
  const shearMap = (p) => { const A = shear(); return A ? A.map((r) => r[0] * p[0] + r[1] * p[1] + r[2] * p[2]) : p; };
  const shearInv = (p) => {
    const A = shear();
    if (!A) return p;
    const [a, b, c] = A, det = a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0]);
    const inv = [
      [b[1] * c[2] - b[2] * c[1], a[2] * c[1] - a[1] * c[2], a[1] * b[2] - a[2] * b[1]],
      [b[2] * c[0] - b[0] * c[2], a[0] * c[2] - a[2] * c[0], a[2] * b[0] - a[0] * b[2]],
      [b[0] * c[1] - b[1] * c[0], a[1] * c[0] - a[0] * c[1], a[0] * b[1] - a[1] * b[0]],
    ].map((r) => r.map((v) => v / det));
    return inv.map((r) => r[0] * p[0] + r[1] * p[1] + r[2] * p[2]);
  };
  const copies = () => view.shear === 'copies';
  // A cell-unit point of the piece at site s, in world units.
  const toWorld = (s, p) => {
    const c = s.map((x) => 2 * x);
    return (copies() ? shearMap(c).map((v, a) => v + p[a]) : shearMap(p.map((v, a) => v + c[a]))).map((v) => v * WS);
  };
  // A world point back into the frame of the piece at site s (cell units, unsheared).
  const toLocal = (s, w) => {
    const q = w.map((v) => v / WS), c = s.map((x) => 2 * x);
    return copies() ? q.map((v, a) => v - shearMap(c)[a]) : shearInv(q).map((v, a) => v - c[a]);
  };

  // ---- drawing ----
  const pieceMaterial = new THREE.MeshStandardMaterial({ vertexColors: true, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
  const layerMaterials = new Map();
  const layerMaterial = (op) => {
    if (!layerMaterials.has(op)) layerMaterials.set(op, new THREE.MeshStandardMaterial({ vertexColors: true, transparent: true, opacity: op, depthWrite: false, side: THREE.DoubleSide }));
    return layerMaterials.get(op);
  };
  const seeThroughMaterial = new THREE.MeshStandardMaterial({ vertexColors: true, transparent: true, opacity: 0.28, depthWrite: false, side: THREE.DoubleSide });
  const ghostMaterial = new THREE.MeshStandardMaterial({ color: GHOST_COLOR(), transparent: true, opacity: 0.16, depthWrite: false, side: THREE.DoubleSide });
  const firstMaterial = new THREE.MeshStandardMaterial({ color: firstColour(), transparent: true, opacity: 0.16, depthWrite: false, side: THREE.DoubleSide });
  // The solid octahedral clusters' centres burn (DICTO, 2026-10-09: "burn bright like fire at their
  // centres ... a blue eternal flame might work too"): fire, flickering, in the Octahedral clusters
  // view; a steady blue eternal flame in the Octet network view. Additive, so they glow through the
  // see-through pieces round them.
  const glow = (color, opacity) => new THREE.MeshBasicMaterial({ color, transparent: true, opacity, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide });
  const fireMaterial = glow(0xff7a1a, 0.95), fireHalo = glow(0xff5a00, 0.28);
  const eternalMaterial = glow(0x4aa8ff, 0.9), eternalHalo = glow(0x2a6cff, 0.25);
  let flickerRaf = 0;
  const FIRE_LOW = new THREE.Color(0xff4a00), FIRE_HIGH = new THREE.Color(0xffd060);
  function flicker(now) {
    flickerRaf = 0;
    if (!active || modeOf().cluster !== 'octa') return;
    const t = now / 1000;
    // a few incommensurate waves: a fire's irregular flicker, not a pulse
    const k = 0.5 + 0.22 * Math.sin(t * 7.3) + 0.16 * Math.sin(t * 13.1 + 1.7) + 0.12 * Math.sin(t * 3.1 + 0.4);
    fireMaterial.color.copy(FIRE_LOW).lerp(FIRE_HIGH, Math.min(1, Math.max(0, k)));
    fireHalo.opacity = 0.18 + 0.2 * Math.min(1, Math.max(0, k));
    flickerRaf = requestAnimationFrame(flicker);
  }
  const pickTargets = [];
  function clearGroup() {
    for (const child of [...group.children]) {
      group.remove(child);
      child.geometry.dispose();
      if (child.isLineSegments) child.material.dispose();
    }
    pickTargets.length = 0;
  }
  const facesOf = (s) => (isEven(s) ? config.evenFaces : config.oddFaces);
  function meshOf(sitesList, material, tag, colourOverride, edgeColor = EDGE_COLOR, faces = facesOf) {
    const pos = [], col = [], line = [], records = [];
    for (const s of sitesList) for (const [f, hex] of faces(s)) {
      const colour = new THREE.Color(colourOverride ?? hex);
      const P = f.map((p) => toWorld(s, p));
      for (let i = 1; i + 1 < P.length; i++) {
        for (const p of [P[0], P[i], P[i + 1]]) { pos.push(...p); col.push(colour.r, colour.g, colour.b); }
        records.push(s);
      }
      P.forEach((p, i) => line.push(...p, ...P[(i + 1) % P.length]));
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    g.setAttribute('color', new THREE.Float32BufferAttribute(col, 3));
    g.computeVertexNormals();
    const mesh = new THREE.Mesh(g, material);
    mesh.userData.stellaJewel = tag;
    mesh.userData.records = records;
    const lg = new THREE.BufferGeometry();
    lg.setAttribute('position', new THREE.Float32BufferAttribute(line, 3));
    return [mesh, new THREE.LineSegments(lg, new THREE.LineBasicMaterial({ color: edgeColor }))];
  }
  // Empty cells touching the build: across faces (DICTO Jewel <-> stella), and DICTO Jewel to
  // DICTO Jewel across the rhombi; in the jewels-alone view, the rhombus neighbours only.
  function emptyNeighbours() {
    const out = new Map();
    for (const s of shown()) for (const d of DJ_NEIGHBOURS) {
      const n = s.map((c, i) => c + d[i]);
      if (!showsSite(n) || !config.touches(s, d)) continue;
      if (grouped() && !isEven(n)) continue;
      if (!cells.has(key(n))) out.set(key(n), n);
    }
    return [...out.values()];
  }
  function draw() {
    clearGroup();
    if (!active) return;
    // A Kagome hull network draws once its solids are in (loading them redraws).
    if (modeOf().hull && !netOf(modeOf().cluster)) { loadHulls(); return; }
    const S = shown();
    if (!S.length) {
      firstMaterial.color.setHex(firstColour());
      // The first placement: the piece, or in a cluster mode the whole cluster.
      const firstNet = netOf(modeOf().cluster);
      const firstSites = firstNet ? netCells(firstNet, firstAnchor(firstNet)) : clustered() ? clusterOf([0, 0, 0]) : [modeOf().even ? [0, 0, 0] : [1, 0, 0]];
      const [m, l] = meshOf(firstSites, firstMaterial, 'first', firstColour(), firstColour(), firstNet?.allJewels ? () => config.evenFaces : facesOf);
      group.add(m, l);
      pickTargets.push(m);
    } else if (clustered()) {
      drawClusters(modeOf().cluster, S);
    } else {
      pieceMaterial.transparent = opacity < 1;
      pieceMaterial.opacity = opacity;
      pieceMaterial.depthWrite = opacity >= 1;
      // Nested (direct request, 2026-10-08: "Dogstars in every cell"): each even piece see-through,
      // the nested piece solid inside it.
      const nested = modeOf().nested === true || modeOf().chain === true;
      const solidSites = nested ? S.filter((s) => !isEven(s)) : S;
      // A network view (DICTO, 2026-10-09: the octet network): the pieces see-through, the cells
      // the present pieces complete drawn between their centres.
      const network = Boolean(modeOf().network);
      // In a chain view the odd pieces between the cells (DICTO, 2026-10-08: "the macro dogstars seem
      // to be missing between the cells") are see-through, so the chains inside stay visible.
      // Each arrangement its own colour scheme (DICTO 2026-10-09).
      const scheme = modeOf();
      const [m, l] = meshOf(solidSites, modeOf().chain || network ? seeThroughMaterial : pieceMaterial, 'piece', scheme.pieceColour, scheme.edgeColour ?? EDGE_COLOR);
      m.visible = !skeleton;
      if (skeleton) l.material.color.setHex(GHOST_COLOR());
      group.add(m, l);
      pickTargets.push(m);
      if (nested) {
        const evens = S.filter(isEven);
        const [om, ol] = meshOf(evens, seeThroughMaterial, 'piece');
        om.visible = !skeleton;
        om.renderOrder = 2;
        group.add(om, ol);
        pickTargets.push(om);
        // A chain (direct request, 2026-10-08: "add the nested Sunstar chain as a view"): layer
        // inside layer, each see-through but the innermost, drawn outside in.
        const layers = modeOf().chain ? config.chainLayers : [{ faces: config.nestedFaces, opacity: 1 }];
        layers.forEach(({ faces, opacity: op }, i) => {
          const mat = op >= 1 ? pieceMaterial : layerMaterial(op);
          const [nm, nl] = meshOf(evens, mat, 'nested', undefined, EDGE_COLOR, () => faces);
          nm.visible = !skeleton;
          nm.renderOrder = layers.length - i;
          nl.material.transparent = op < 1;
          nl.material.opacity = Math.min(1, op + 0.35);
          group.add(nm, nl);
        });
      }
      if (latticeView) {
        const ghosts = emptyNeighbours();
        if (ghosts.length) {
          const [gm, gl] = meshOf(ghosts, ghostMaterial, 'ghost', GHOST_COLOR(), GHOST_COLOR());
          gl.material.transparent = true;
          gl.material.opacity = 0.4;
          group.add(gm, gl);
          pickTargets.push(gm);
        }
      }
      if (network) group.add(...networkOverlay(S.filter(isEven)));
      if (view.axes) group.add(...fiveFoldOverlay(S.filter(isEven)));
    }
    renderPanel();
  }
  // Clusters as cohesive blocks (DICTO 2026-10-09: "they look like separate balloons ... make all
  // improvements global"): in every cluster arrangement each cluster is drawn whole, as its own solid
  // (krp-core's cluster shape, outlined only where its faces fold, no seams), and the cells between the
  // clusters fill by themselves: the odd pieces (stellas, Dogstars), and in the Kagome network the
  // single even pieces (violet), so a build is solid with no gaps. A tap places the free cluster
  // nearest the tap; the octahedral clusters' blocks stay a little see-through for their fire.
  const BLOCK_COLOURS = { tetra: 0xd9a520, kagome: 0xd9a520, octa: 0x8c5a2b, hexa: 0xd9a520 };
  const SINGLE_VIOLET = 0x8f5bd8;
  const NEAR12 = [[1, 1, 0], [1, -1, 0], [-1, 1, 0], [-1, -1, 0], [1, 0, 1], [1, 0, -1], [-1, 0, 1], [-1, 0, -1], [0, 1, 1], [0, 1, -1], [0, -1, 1], [0, -1, -1]];
  const AXES6 = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]];
  const K = (1 + Math.sqrt(5)) / 4; // krp-core's cluster shapes: cube edge 2 scaled by phi/2
  const blockMaterial = new THREE.MeshStandardMaterial({ vertexColors: true, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
  const glassBlockMaterial = new THREE.MeshStandardMaterial({ vertexColors: true, transparent: true, opacity: 0.55, depthWrite: false, side: THREE.DoubleSide });
  // A cluster shape's feature edges: where its faces fold (seams between faces in one plane left out).
  const featureEdges = new Map();
  function edgesOf(spec) {
    if (featureEdges.has(spec.id)) return featureEdges.get(spec.id);
    const V = spec.vertices, normal = (f) => { const a = V[f[0]], b = V[f[1]], c = V[f[2]]; const u = b.map((x, i) => x - a[i]), v = c.map((x, i) => x - a[i]); const n = [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]; const l = Math.hypot(...n) || 1; return n.map((x) => x / l); };
    const byEdge = new Map();
    spec.faces.forEach((f, fi) => f.forEach((x, i) => { const y = f[(i + 1) % f.length]; const k = x < y ? `${x}-${y}` : `${y}-${x}`; byEdge.set(k, [...(byEdge.get(k) ?? []), fi]); }));
    const out = [];
    for (const [k, fs] of byEdge) {
      const ns = fs.map((fi) => normal(spec.faces[fi]));
      const flat = ns.length === 2 && Math.abs(ns[0][0] * ns[1][0] + ns[0][1] * ns[1][1] + ns[0][2] * ns[1][2]) > 0.9999;
      if (!flat) out.push(k.split('-').map(Number));
    }
    featureEdges.set(spec.id, out);
    return out;
  }
  function clusterFill(kind, evens, centres) {
    const held = new Set([...evens, ...centres].map(key));
    const singles = new Map(), odds = new Map();
    if (kind === 'kagome') for (const e of evens) for (const d of NEAR12) {
      const c = e.map((v, i) => v + d[i]), k = key(c);
      if (held.has(k) || singles.has(k) || config.clusters.kagome(c)) continue;
      if (NEAR12.filter((d2) => held.has(key(c.map((v, i) => v + d2[i])))).length >= 3) singles.set(k, c);
    }
    const solid = new Set([...held, ...singles.keys()]);
    for (const e of [...evens, ...singles.values()]) for (const d of AXES6) {
      const o = e.map((v, i) => v + d[i]), k = key(o);
      if (odds.has(k) || held.has(k)) continue;
      if (AXES6.filter((d2) => solid.has(key(o.map((v, i) => v + d2[i])))).length >= 4) odds.set(k, o);
    }
    return { singles: [...singles.values()], odds: [...odds.values()] };
  }
  function drawClusters(kind, S) {
    const evens = S.filter(isEven);
    // each cluster once, keyed by its first site (the centre, for an octahedral cluster)
    const clusters = new Map();
    const net = netOf(kind);
    if (net) for (const { cells: cl } of heldNet(net, S)) clusters.set(key(cl[0]), cl);
    else for (const e of evens) { const cl = config.clusters[kind](e); if (cl) clusters.set(key(cl[0]), cl); }
    const centres = kind === 'octa' ? [...clusters.values()].map((cl) => cl[0]) : [];
    const spec = net ? net.spec : config.clusterBlocks[kind], edges = edgesOf(spec);
    const colour = new THREE.Color(BLOCK_COLOURS[kind] ?? modeOf().pieceColour ?? 0xd9a520);
    const pos = [], col = [], line = [], records = [];
    for (const cl of clusters.values()) {
      // the cells the solid is centred on: an octahedral cluster's six, a network's even cells
      const a = cl[0], members = kind === 'octa' ? cl.slice(1) : net ? cl.filter(isEven) : cl;
      // the shape is centred on its cells' centre; each corner goes through the shear with the cell it
      // belongs to (the nearest), so with sheared copies every piece sits on its own sheared centre
      const C = members.reduce((t, m) => t.map((v, i) => v + (2 * m[i]) / members.length), [0, 0, 0]);
      const P = spec.vertices.map((v) => {
        const r = v.map((c, i) => c / K + C[i]);
        const m = cl.reduce((best, x) => (Math.hypot(...r.map((c, i) => c - 2 * x[i])) < Math.hypot(...r.map((c, i) => c - 2 * best[i])) ? x : best));
        return toWorld(m, r.map((c, i) => c - 2 * m[i]));
      });
      for (const f of spec.faces) for (let i = 1; i + 1 < f.length; i++) {
        for (const k of [f[0], f[i], f[i + 1]]) { pos.push(...P[k]); col.push(colour.r, colour.g, colour.b); }
        records.push(a);
      }
      for (const [x, y] of edges) line.push(...P[x], ...P[y]);
    }
    // A network's keys (the Hexa-Keys of the checkerboard), each centred on its block, in its colour.
    if (net?.keys) {
      const kc = new THREE.Color(net.keys.colour), kEdges = edgesOf(net.keys.spec);
      for (const g of netKeys(net, S)) {
        const kcells = netCells(net, g), C = kcells.filter(isEven).reduce((t, m, _, l) => t.map((v, i) => v + (2 * m[i]) / l.length), [0, 0, 0]);
        const P = net.keys.spec.vertices.map((v) => {
          const r = v.map((c, i) => c / K + C[i]);
          const m = kcells.reduce((best, x) => (Math.hypot(...r.map((c, i) => c - 2 * x[i])) < Math.hypot(...r.map((c, i) => c - 2 * best[i])) ? x : best));
          return toWorld(m, r.map((c, i) => c - 2 * m[i]));
        });
        for (const f of net.keys.spec.faces) for (let i = 1; i + 1 < f.length; i++) {
          for (const k of [f[0], f[i], f[i + 1]]) { pos.push(...P[k]); col.push(kc.r, kc.g, kc.b); }
          records.push(kcells[0]);
        }
        for (const [x, y] of kEdges) line.push(...P[x], ...P[y]);
      }
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    g.setAttribute('color', new THREE.Float32BufferAttribute(col, 3));
    g.computeVertexNormals();
    const glass = kind === 'octa';
    const mat = glass ? glassBlockMaterial : blockMaterial;
    if (!glass) { mat.transparent = opacity < 1; mat.opacity = opacity; mat.depthWrite = opacity >= 1; }
    const m = new THREE.Mesh(g, mat);
    m.userData.stellaJewel = 'piece';
    m.userData.records = records;
    m.visible = !skeleton;
    const lg = new THREE.BufferGeometry();
    lg.setAttribute('position', new THREE.Float32BufferAttribute(line, 3));
    const l = new THREE.LineSegments(lg, new THREE.LineBasicMaterial({ color: skeleton ? GHOST_COLOR() : EDGE_COLOR }));
    group.add(m, l);
    pickTargets.push(m);
    const { singles, odds } = net ? netFill(net, S) : clusterFill(kind, evens, centres);
    pieceMaterial.transparent = opacity < 1; pieceMaterial.opacity = opacity; pieceMaterial.depthWrite = opacity >= 1;
    if (singles.length) { const [sm, sl] = meshOf(singles, pieceMaterial, 'fill', SINGLE_VIOLET); sm.visible = !skeleton; group.add(sm, sl); pickTargets.push(sm); }
    if (odds.length) { const [om, ol] = meshOf(odds, pieceMaterial, 'fill', null, EDGE_COLOR, () => config.oddFaces); om.visible = !skeleton; group.add(om, ol); pickTargets.push(om); }
    if (centres.length) {
      group.add(...flames(centres, fireMaterial, fireHalo));
      if (!flickerRaf) flickerRaf = requestAnimationFrame(flicker);
    }
  }
  // Networks (DICTO 2026-10-09): clusters on an anchor pattern, sharing single pieces corner to
  // corner, drawn whole as one solid each: the DICTO Hexa diamond network (8 Jewels on a 2 x 2 x 2 block,
  // any parity) and the Kagome hulls of DISCOVERIES #17 (krp-core kagomeHulls.js, solids loaded on
  // demand). A network: { offsets (its cells from its anchor), isAnchor, spec (its solid), singles }.
  // The cells no cluster can cover fill by themselves once surrounded: stellas (or Dogstars), and
  // single Jewels where the network leaves them.
  const BLOCK8 = [0, 1].flatMap((x) => [0, 1].flatMap((y) => [0, 1].map((z) => [x, y, z])));
  const nets = { hexa: config.isHexaAnchor ? { offsets: BLOCK8, isAnchor: config.isHexaAnchor, spec: config.clusterBlocks?.hexa, singles: false, allJewels: true } : null };
  // The Hexa checkerboard (DISCOVERIES #18): Hexas window to window on an FCC pattern (anchors all even,
  // x+y+z = 0 mod 4), never sharing a piece; in every gap a DICTO Hexa-Key (anchors x+y+z = 2 mod 4),
  // filled in by itself once 4 of its 6 Hexas are there. 5 : 3, the Stella-Jewel Lattice one level up.
  const FCC2 = [[2, 2, 0], [2, -2, 0], [-2, 2, 0], [-2, -2, 0], [2, 0, 2], [2, 0, -2], [-2, 0, 2], [-2, 0, -2], [0, 2, 2], [0, 2, -2], [0, -2, 2], [0, -2, -2]];
  const AX2 = [[2, 0, 0], [-2, 0, 0], [0, 2, 0], [0, -2, 0], [0, 0, 2], [0, 0, -2]];
  const evenAll = (a) => a.every((v) => v % 2 === 0), mod4 = (v) => ((v % 4) + 4) % 4;
  if (config.clusterBlocks?.hexaKey) nets.hexaKey = { offsets: BLOCK8, isAnchor: (a) => evenAll(a) && mod4(a[0] + a[1] + a[2]) === 0,
    spec: config.clusterBlocks.hexa, singles: false, fillOdds: false, allJewels: true, neighbours: FCC2,
    keys: { isAnchor: (a) => evenAll(a) && mod4(a[0] + a[1] + a[2]) === 2, around: AX2, needs: 4, spec: config.clusterBlocks.hexaKey, colour: 0x8f5bd8 } };
  // A network's keys present: key anchors with enough held clusters round them.
  function netKeys(net, S) {
    if (!net.keys) return [];
    const held = new Set(heldNet(net, S).map((o) => key(o.a))), out = new Map();
    for (const k of held) {
      const a = k.split(',').map(Number);
      for (const d of net.keys.around) {
        const g = a.map((v, i) => v + d[i]), gk = key(g);
        if (out.has(gk) || !net.keys.isAnchor(g)) continue;
        if (net.keys.around.filter((d2) => held.has(key(g.map((v, i) => v - d2[i])))).length >= net.keys.needs) out.set(gk, g);
      }
    }
    return [...out.values()];
  }
  const netOf = (kind) => nets[kind] ?? null;
  let hullsLoading = null;
  // A Kagome hull's network, once its solids are in (they load the first time one is opened).
  function loadHulls() {
    hullsLoading ??= kagomeHullSolids().then((data) => {
      for (const id of KAGOME_HULL_IDS) {
        const h = data[id], solid = h[config.hullLattice];
        nets[id] = { offsets: [...h.evenCells, ...h.enclosedOddCells, ...h.cornerOddCells], isAnchor: KAGOME_HULLS[id].isAnchor,
          spec: { id: `hull-${id}-${config.hullLattice}`, vertices: solid.vertices.map((v) => v.map((c) => c * K)), faces: solid.faces }, singles: true };
      }
      if (active) draw();
    });
    return hullsLoading;
  }
  // The first cluster: the anchor nearest the origin.
  function firstAnchor(net) {
    for (let r = 0; r <= 4; r++) for (let x = -r; x <= r; x++) for (let y = -r; y <= r; y++) for (let z = -r; z <= r; z++) if (net.isAnchor([x, y, z])) return [x, y, z];
    return [0, 0, 0];
  }
  const netCells = (net, a) => net.offsets.map((d) => a.map((v, i) => v + d[i]));
  const netAnchorsOf = (net, c) => net.offsets.map((d) => c.map((v, i) => v - d[i])).filter(net.isAnchor);
  const netHeld = (net, a) => netCells(net, a).every((x) => cells.has(key(x)));
  function heldNet(net, S) {
    const out = new Map();
    for (const c of S) for (const a of netAnchorsOf(net, c)) if (!out.has(key(a)) && netHeld(net, a)) out.set(key(a), { a, cells: netCells(net, a) });
    return [...out.values()];
  }
  function netFill(net, S) {
    const held = new Set(S.map(key)), singles = new Map(), odds = new Map();
    const free = (c) => !held.has(key(c)) && !netAnchorsOf(net, c).length; // no cluster can cover it
    if (net.singles) for (const c of S) for (const d of NEAR12) {
      const e = c.map((v, i) => v + d[i]), k = key(e);
      if (!isEven(e) || singles.has(k) || !free(e)) continue;
      // a single Jewel once at least half its 12 neighbours are held (in a whole network, all are)
      if (NEAR12.filter((d2) => held.has(key(e.map((v, i) => v + d2[i])))).length >= 6) singles.set(k, e);
    }
    const solid = new Set([...held, ...singles.keys()]);
    if (net.fillOdds !== false) for (const c of [...S, ...singles.values()]) for (const d of AXES6) {
      const o = c.map((v, i) => v + d[i]), k = key(o);
      if (odds.has(k) || singles.has(k) || !free(o)) continue;
      if (AXES6.filter((d2) => solid.has(key(o.map((v, i) => v + d2[i])))).length >= 4) odds.set(k, o);
    }
    return { singles: [...singles.values()], odds: [...odds.values()] };
  }
  // Placement: the free cluster nearest the tap among those beside the tapped piece, preferring ones
  // that join the build (share a piece with it).
  function netPlace(net, site, point) {
    const tap = [point.x, point.y, point.z], seen = new Set(), options = [];
    const R = 4;
    for (let dx = -R; dx <= R; dx++) for (let dy = -R; dy <= R; dy++) for (let dz = -R; dz <= R; dz++) {
      const a = [site[0] + dx, site[1] + dy, site[2] + dz];
      if (!net.isAnchor(a) || seen.has(key(a))) continue;
      seen.add(key(a));
      const cs = netCells(net, a);
      const joins = cs.some((x) => cells.has(key(x))) || (net.neighbours ?? []).some((d) => netHeld(net, a.map((v, i) => v + d[i])));
      if (cs.some((x) => !cells.has(key(x)))) options.push({ a, joins, centre: centreOf(cs.filter(isEven)) });
    }
    // Where a network has neighbours (the checkerboard), the build grows compact: each held neighbour
    // counts as a third of a step nearer, so gaps close round and their keys fill in.
    const step = net.neighbours ? Math.hypot(...centreOf(netCells(net, [0, 0, 0])).map((v, i) => v - centreOf(netCells(net, net.neighbours[0]))[i])) : 0;
    const held = (o) => (net.neighbours ?? []).filter((d) => netHeld(net, o.a.map((v, i) => v + d[i]))).length;
    const dist = (o) => Math.hypot(...o.centre.map((v, i) => v - tap[i])) + (o.joins || !cells.size ? 0 : 1e3) - held(o) * step / 3;
    options.sort((p, q) => dist(p) - dist(q));
    return options.length ? addCells(netCells(net, options[0].a)) : false;
  }
  const centreOf = (list) => list.map((x) => toWorld(x, [0, 0, 0])).reduce((t, p) => t.map((v, i) => v + p[i] / list.length), [0, 0, 0]);
  function addCells(list) {
    const fresh = list.filter((x) => !cells.has(key(x)));
    if (!fresh.length) return false;
    for (const x of fresh) cells.set(key(x), [...x]);
    commit();
    fit();
    return true;
  }
  // Long-press on a cluster: it goes, but pieces another whole cluster shares stay.
  function removeNet(net, s, point) {
    const tap = [point.x, point.y, point.z];
    const mine = netAnchorsOf(net, s).filter((a) => netHeld(net, a));
    if (!mine.length) return false;
    const a = mine.sort((p, q) => Math.hypot(...centreOf(netCells(net, p)).map((v, i) => v - tap[i])) - Math.hypot(...centreOf(netCells(net, q)).map((v, i) => v - tap[i])))[0];
    const keep = new Set(heldNet(net, [...cells.values()]).filter((o) => key(o.a) !== key(a)).flatMap((o) => o.cells.map(key)));
    const gone = netCells(net, a).filter((x) => !keep.has(key(x)) && cells.delete(key(x)));
    if (!gone.length) return false;
    commit();
    return true;
  }
  // Placement: the free cluster nearest the tap among those beside the tapped site.
  function clusterPlace(kind, site, point) {
    const tap = [point.x, point.y, point.z];
    const centre = (cl) => cl.map((x) => toWorld(x, [0, 0, 0])).reduce((t, p) => t.map((v, i) => v + p[i] / cl.length), [0, 0, 0]);
    const seen = new Set(), options = [];
    const consider = (c) => { const cl = config.clusters[kind](c); if (!cl || seen.has(key(cl[0]))) return; seen.add(key(cl[0])); if (cl.some((x) => !cells.has(key(x)))) options.push(cl); };
    const evensNear = isEven(site) ? [site, ...NEAR12.map((d) => site.map((v, i) => v + d[i]))] : AXES6.map((d) => site.map((v, i) => v + d[i]));
    for (const e of evensNear) { consider(e); for (const d of NEAR12) consider(e.map((v, i) => v + d[i])); }
    if (kind === 'kagome' && isEven(site)) config.kagomeNeighbours(site).forEach((cl) => consider(cl[0]));
    options.sort((a, b) => Math.hypot(...centre(a).map((v, i) => v - tap[i])) - Math.hypot(...centre(b).map((v, i) => v - tap[i])));
    return options.length ? addCluster(options[0][0]) : false;
  }
  // A flame: the odd piece at each site, glowing, inside a faint larger halo of itself.
  function flames(sites, core, halo, faces = config.oddFaces, size = 1) {
    const [fm, fl] = meshOf(sites, core, 'piece', core.color.getHex(), EDGE_COLOR, () => faces.map(([f]) => [f.map((p) => p.map((c) => c * size)), 0xffffff]));
    fl.geometry.dispose(); fl.material.dispose(); // a flame has no outline
    fm.renderOrder = 5;
    pickTargets.push(fm);
    const big = () => faces.map(([f]) => [f.map((p) => p.map((c) => c * 1.12 * size)), 0xffffff]);
    const [hm, hl] = meshOf(sites, halo, 'flame', halo.color.getHex(), EDGE_COLOR, big);
    hl.geometry.dispose(); hl.material.dispose();
    hm.renderOrder = 6;
    return [fm, hm];
  }
  // The network's cells (config.networkCells: triangles of piece sites, with a colour) and the
  // edges between neighbouring centres, drawn through the shear like the pieces.
  function networkOverlay(evens) {
    const centre = (s) => toWorld(s, [0, 0, 0]);
    const { triangles, edges } = config.networkCells(evens);
    const pos = [], col = [];
    for (const { sites, colour } of triangles) {
      const c = new THREE.Color(colour);
      for (const s of sites) { pos.push(...centre(s)); col.push(c.r, c.g, c.b); }
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    g.setAttribute('color', new THREE.Float32BufferAttribute(col, 3));
    g.computeVertexNormals();
    const cells = new THREE.Mesh(g, layerMaterial(0.45));
    cells.renderOrder = 3;
    const lg = new THREE.BufferGeometry();
    lg.setAttribute('position', new THREE.Float32BufferAttribute(edges.flatMap(([a, b]) => [...centre(a), ...centre(b)]), 3));
    const lines = new THREE.LineSegments(lg, new THREE.LineBasicMaterial({ color: AXIS_COLOR, transparent: true, opacity: 0.8 }));
    lines.renderOrder = 4;
    // Each octahedral cell's centre piece: a blue eternal flame.
    const eternal = config.networkCells(evens).octaCentres ?? [];
    return [cells, lines, ...(eternal.length ? flames(eternal, eternalMaterial, eternalHalo) : [])];
  }
  // The six five-fold axes through each DICTO Jewel, and on every face the five window
  // positions: faint, with the cube's choice (the window itself) bright.
  function fiveFoldOverlay(jewels) {
    const axis = [], faint = [], bright = [];
    for (const s of jewels) {
      for (const a of AXES) axis.push(...toWorld(s, a.map((c) => -2.1 * c)), ...toWorld(s, a.map((c) => 2.1 * c)));
      for (const [polys, into] of [[config.overlay?.faint ?? [], faint], [config.overlay?.bright ?? [], bright]]) for (const P of polys) P.forEach((p, i) => into.push(...toWorld(s, p), ...toWorld(s, P[(i + 1) % P.length])));
    }
    const lines = (pts, color, op) => {
      const g = new THREE.BufferGeometry();
      g.setAttribute('position', new THREE.Float32BufferAttribute(pts, 3));
      const ls = new THREE.LineSegments(g, new THREE.LineBasicMaterial({ color, transparent: true, opacity: op, depthTest: false }));
      ls.renderOrder = 3;
      return ls;
    };
    return [lines(axis, AXIS_COLOR, 0.7), lines(faint, firstColour(), 0.35), lines(bright, config.brightColor ?? AXIS_COLOR, 1)];
  }
  function fit() {
    const S = shown();
    if (!S.length) { fitView([0, 0, 0], 2.2 * WS); return; }
    const P = S.map((s) => toWorld(s, [0, 0, 0]));
    const c = [0, 1, 2].map((a) => P.reduce((t0, p) => t0 + p[a], 0) / P.length);
    fitView(c, Math.max(...P.map((p) => Math.hypot(...p.map((v, a) => v - c[a])))) + 2 * WS);
  }

  // ---- building ----
  function commit() { save(); draw(); onChange(); }
  function add(s) {
    if (cells.has(key(s))) return false;
    if (!showsSite(s)) return false;
    cells.set(key(s), [...s]);
    commit();
    fit();
    return true;
  }
  // Grouped modes (direct request, 2026-10-08: "the dodecahedron has all stars attached"): an
  // even piece comes with its group (a Sunstar: the dodecahedron with the 6 Dogstars on its faces).
  const grouped = () => modeOf().grouped === true;
  const AXIS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]];
  function addGroup(e) {
    const fresh = [e, ...config.group(e)].filter((x) => !cells.has(key(x)));
    if (!fresh.length) return false;
    for (const x of fresh) cells.set(key(x), [...x]);
    commit();
    fit();
    return true;
  }
  // Cluster modes (DICTO, 2026-10-09: DICTO's clusters of DICTO Jewels): config.clusters[mode.cluster](s)
  // is the whole cluster the site belongs to; a tap adds or removes it whole.
  const clustered = () => Boolean(modeOf().cluster);
  const clusterOf = (s) => config.clusters[modeOf().cluster](s);
  function addCluster(s) {
    const fresh = (clusterOf(s) ?? []).filter((x) => !cells.has(key(x)));
    if (!fresh.length) return false;
    for (const x of fresh) cells.set(key(x), [...x]);
    commit();
    fit();
    return true;
  }
  function removeCluster(s) {
    const gone = (clusterOf(s) ?? [s]).filter((x) => cells.delete(key(x)));
    if (!gone.length) return false;
    commit();
    return true;
  }
  // Remove an even piece's group: its own odd pieces go too, unless another even piece present still has them.
  function removeGroup(e) {
    if (!cells.delete(key(e))) return false;
    for (const o of config.group(e)) {
      const shared = AXIS.some((d) => { const e2 = o.map((c, i) => c + d[i]); return key(e2) !== key(e) && cells.has(key(e2)) && config.group(e2).some((x) => key(x) === key(o)); });
      if (!shared) cells.delete(key(o));
    }
    commit();
    return true;
  }
  // The even piece an odd site belongs with: the present one beside it nearest the tap, else none.
  function evenFor(o, q) {
    let best = null, bestD = Infinity;
    for (const d of AXIS) {
      const e = o.map((c, i) => c + d[i]);
      if (!cells.has(key(e))) continue;
      const dist = q ? Math.hypot(...q.map((v, a) => v - 2 * d[a])) : 0;
      if (dist < bestD) { bestD = dist; best = e; }
    }
    return best;
  }
  // The piece across the tapped face: the neighbour whose piece holds a point just outside it.
  function across(s, hit) {
    const n = hit.face.normal;
    const w = [hit.point.x + n.x * 0.03 * WS, hit.point.y + n.y * 0.03 * WS, hit.point.z + n.z * 0.03 * WS];
    const q = toLocal(s, w);
    for (const d of DJ_NEIGHBOURS) {
      const nb = s.map((c, i) => c + d[i]);
      const p = q.map((v, a) => v - 2 * d[a]);
      if (isEven(nb) ? config.insideEven(p) : config.insideOdd(p)) {
        if (showsSite(nb) || config.holePrompt) return nb;
        break;
      }
    }
    // Pieces that only share corners (or a hidden piece in between): the nearest shown neighbour.
    let best = null, bestD = Infinity;
    for (const d of DJ_NEIGHBOURS) {
      const nb = s.map((c, i) => c + d[i]);
      if (!showsSite(nb) || !config.touches(s, d)) continue;
      const dist = Math.hypot(...q.map((v, a) => v - 2 * d[a]));
      if (dist < bestD) { bestD = dist; best = nb; }
    }
    return best;
  }
  function handleTap(hit, mode) {
    const tag = hit.object.userData.stellaJewel === 'fill' ? 'fill' : hit.object.userData.stellaJewel;
    const s = hit.object.userData.records?.[hit.faceIndex];
    if (!tag || !s || mode === 'paint') return false;
    const chisel = mode === 'chisel';
    if (clustered()) {
      if (tag === 'first' || tag === 'ghost') {
        if (chisel) return false;
        const net = netOf(modeOf().cluster);
        return net ? addCells(netCells(net, firstAnchor(net))) : addCluster(s);
      }
      // Every cluster arrangement (DICTO 2026-10-09: "just automatic good placement"): a tap on a block
      // or a filled piece places the free cluster nearest the tap; a long-press on a block removes it.
      {
        const kind = modeOf().cluster;
        const net = netOf(kind);
        if (chisel) return tag === 'piece' ? (net ? removeNet(net, s, hit.point) : removeCluster(s)) : false;
        if (net) {
          if (netPlace(net, s, hit.point)) return true;
          showHudPrompt(t(`${S_}.prompt.taken`, lang()), 2000);
          return false;
        }
        // On a block, the piece actually tapped: the cluster member nearest the tap.
        const p = [hit.point.x, hit.point.y, hit.point.z];
        const members = tag === 'piece' ? (config.clusters[kind](s) ?? [s]) : [s];
        const at = members.reduce((best, x) => (Math.hypot(...toWorld(x, [0, 0, 0]).map((v, i) => v - p[i])) < Math.hypot(...toWorld(best, [0, 0, 0]).map((v, i) => v - p[i])) ? x : best));
        if (clusterPlace(kind, at, hit.point)) return true;
        showHudPrompt(t(`${S_}.prompt.taken`, lang()), 2000);
        return false;
      }
      if (chisel) return removeCluster(s);
      const nb = across(s, hit);
      if (!nb) return false;
      // Across a face into a hidden piece's cell (a stella's, between clusters): say so.
      // Into a cell no cluster can take (a hidden piece, or one between clusters): say so.
      if (!showsSite(nb)) { showHudPrompt(t(`${S_}.prompt.hole`, lang()), 2500); return false; }
      // In the Kagome network, half the even cells hold single pieces between the clusters.
      if (!clusterOf(nb)) { showHudPrompt(t(modeOf().cluster === 'kagome' ? `${S_}.prompt.single` : `${S_}.prompt.hole`, lang()), 2500); return false; }
      if (addCluster(nb)) return true;
      showHudPrompt(t(`${S_}.prompt.taken`, lang()), 2000);
      return false;
    }
    if (grouped()) {
      if (tag === 'first' || tag === 'ghost') return chisel ? false : addGroup(isEven(s) ? s : evenFor(s) ?? s.map((c, i) => c + (i === 0 ? 1 : 0)));
      if (chisel) {
        const e = isEven(s) ? s : evenFor(s, toLocal(s, [hit.point.x, hit.point.y, hit.point.z]));
        if (e) return removeGroup(e);
        if (!cells.delete(key(s))) return false;
        commit();
        return true;
      }
      const nb = across(s, hit);
      // Through a Dogstar, the Sunstar beyond it: straight on from the tapped dodecahedron.
      const e = !nb ? null : isEven(nb) ? nb : isEven(s) ? nb.map((c, i) => 2 * c - s[i]) : null;
      if (e && addGroup(e)) return true;
      showHudPrompt(t(`${S_}.prompt.taken`, lang()), 2000);
      return false;
    }
    if (tag === 'first' || tag === 'ghost') return chisel ? false : add(s);
    if (chisel) {
      if (!cells.delete(key(s))) return false;
      commit();
      return true;
    }
    const nb = across(s, hit);
    if (!nb) return false;
    if (!showsSite(nb)) { showHudPrompt(t(`${S_}.prompt.hole`, lang()), 2500); return false; }
    if (add(nb)) return true;
    showHudPrompt(t(`${S_}.prompt.taken`, lang()), 2000);
    return false;
  }

  // ---- panel ----
  const panel = document.createElement('div');
  panel.id = config.panelId;
  panel.className = 'qc-panel';
  panel.innerHTML = `
    <div class="w4d-row"><label class="hull-pick"><span class="sj-view-label"></span> <select class="hull-select" data-select="mode"></select></label></div>
    <div class="w4d-row sj-count"></div>
    <div class="w4d-row w4d-options"><button type="button" data-sj="shear"></button><button type="button" data-sj="axes"></button></div>`;
  document.body.appendChild(panel);
  addPanelMinimiser(panel, config.minimiser);
  const modeSelect = panel.querySelector('[data-select="mode"]');
  function renderPanel() {
    panel.classList.toggle('visible', active);
    if (!active) return;
    const L = lang();
    // Arrangements (DICTO 2026-10-09: "separate access for each genuinely different arrangement") are
    // opened from DICTO, each its own entry: in one, the panel names it instead of offering the views.
    const arrangement = modeOf().arrangement === true;
    modeSelect.hidden = arrangement;
    panel.querySelector('.sj-view-label').textContent = arrangement ? t(`${S_}.view.${view.mode}`, L) : t(`${S_}.view`, L);
    modeSelect.innerHTML = MODE_LIST.filter((m) => !m.arrangement).map(({ id: m }) => `<option value="${m}"${m === view.mode ? ' selected' : ''}>${t(`${S_}.view.${m}`, L)}</option>`).join('');
    const all = [...cells.values()];
    const net = netOf(modeOf().cluster);
    panel.querySelector('.sj-count').textContent = net
      ? (() => { const f = netFill(net, all), keys = netKeys(net, all).length * 8, jewels = net.allJewels ? all : all.filter(isEven); return t(`${S_}.count`, L, { even: jewels.length + f.singles.length, odd: all.length - jewels.length + f.odds.length + keys }); })()
      : clustered()
        // the cluster arrangements count what fills in by itself too: single pieces and stellas or Dogstars
        ? (() => { const evens = all.filter(isEven), odd = all.filter((x) => !isEven(x)), f = clusterFill(modeOf().cluster, evens, modeOf().cluster === 'octa' ? odd : []);
          return t(`${S_}.count`, L, { even: evens.length + f.singles.length, odd: odd.length + f.odds.length }); })()
        : t(`${S_}.count`, L, { even: all.filter(isEven).length, odd: all.filter((s) => !isEven(s)).length });
    const shearBtn = panel.querySelector('[data-sj="shear"]');
    shearBtn.textContent = t(`studies.shear.${view.shear}`, L);
    // Only where there is a shear to follow (Kaleidohedra's space): elsewhere it would do nothing.
    shearBtn.hidden = !shear();
    const axesBtn = panel.querySelector('[data-sj="axes"]');
    axesBtn.textContent = t(`${S_}.axes`, L);
    axesBtn.classList.toggle('active', view.axes);
  }
  modeSelect.addEventListener('change', () => {
    if (!MODES.includes(modeSelect.value)) return;
    view.mode = modeSelect.value;
    save(); draw(); fit();
  });
  panel.querySelector('[data-sj="shear"]').addEventListener('click', () => { view.shear = copies() ? 'solid' : 'copies'; save(); draw(); fit(); });
  panel.querySelector('[data-sj="axes"]').addEventListener('click', () => { view.axes = !view.axes; save(); draw(); });
  let shownLang = lang();
  onSettingsChange((st) => { if (st.language !== shownLang) { shownLang = st.language; if (active) renderPanel(); } });

  return {
    group,
    meshes: () => pickTargets,
    handleTap,
    setActive(on) {
      if (on === active) return;
      active = on;
      group.visible = on;
      if (!on) panel.classList.remove('visible');
      draw();
      if (on) { fit(); if (!shown().length) showHudPrompt(t(`${S_}.prompt.start`, lang()), 5000); }
    },
    setSkeleton(on) { skeleton = on; if (active) draw(); },
    setTranslucent(o) { if (o !== opacity) { opacity = o; if (active) draw(); } },
    setLatticeView(on) { latticeView = on; if (active) draw(); },
    shearChanged() { if (active) draw(); },
    /** Open on an arrangement (its own DICTO entry), or, with none, on the plain lattice's views. */
    setArrangement(id) {
      const target = id && MODE_LIST.find((m) => m.id === id && m.arrangement) ? id : (modeOf().arrangement ? MODE_LIST.find((m) => !m.arrangement).id : view.mode);
      if (target === view.mode) return;
      view.mode = target;
      save();
      if (active) { draw(); fit(); }
    },
    get isEmpty() { return cells.size === 0; },
    get mode() { return view.mode; },
    clear() { cells.clear(); commit(); if (active) fit(); },
    snapshot,
    restore(json) { read(json); save(); draw(); },
  };
}
