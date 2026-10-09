// Polyhedraverse inside the joined app (step D2, DICTO 2026-10-09): its own 3D world, the portrait
// gallery's shapes from krp-core (src/polyhedra). Choose a shape in DICTO (families, then shapes);
// an empty world shows its outline in the app's colour, tap it to place it; then tap attach (D3):
// tap a face, then a shape. The shape browser comes with D4 (PLAN-POLYHEDRAVERSE.md).
// Saved in Polyhedraverse's own form (krp-core assembly: nodes with a shape and a transform), so a
// build moves between this world and the old site by Export/Import.
import * as THREE from 'three';
import { POLYHEDRA, isFaceEligibleForAttach } from '../krp-core/src/polyhedra/index.js';
import { facesCongruent } from '../krp-core/src/polyhedra/core.js';
import { faceAttachOptions } from '../krp-core/src/assembly/faceAttach.js';
import { rankFaceAttachOptions } from '../krp-core/src/assembly/faceRegistration.js';
import { familyIds } from '../krp-core/src/polyhedra/families.js';
import { mountWireframePreview } from './wireframe-preview.js';
import { polyShapeEdges } from './poly-shapes.js';
import { familiesFor } from '../krp-core/src/polyhedra/families.js';
import { FAMILY_COLORS } from '../krp-core/src/assembly/pieceColors.js';
import { getSettings, onSettingsChange } from './settings.js';
import { storageKey, theme } from './site.js';
import { t } from './i18n.js';
import { polyShapeName } from './poly-shapes.js';

export { polyShapeEdges, polyShapeName } from './poly-shapes.js';

const STORAGE_KEY = storageKey('poly-world');
const EDGE_COLOR = 0x0b1220;
const DEFAULT_SHAPE = 'DODECAHEDRON';
const lang = () => getSettings().language;

export function createPolyWorld({ scene, colorOf, getMaterial, onChange = () => {}, showHudPrompt = () => {}, fitView = () => {}, pickShape = () => {} }) {
  const group = new THREE.Group();
  group.visible = false;
  scene.add(group);

  // ---- state: Polyhedraverse's assembly form ----
  let nodes = []; // { id, shape, transform: { position, quaternion }, material }
  let connections = []; // { nodeA, vertexA, nodeB, vertexB, kind: 'face' } (face indices for a face join)
  const view = { shape: DEFAULT_SHAPE };
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
      .map((c) => ({ nodeA: String(c.nodeA), vertexA: c.vertexA, nodeB: String(c.nodeB), vertexB: c.vertexB, kind: c.kind ?? 'face' }));
    nextId = 1 + Math.max(0, ...nodes.map((n) => Number(String(n.id).replace(/\D/g, '')) || 0));
  }
  const toJSON = () => ({ nodes: nodes.map((n) => ({ ...n })), connections: connections.map((c) => ({ ...c })) });
  try {
    const data = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null');
    if (data) { setFromJSON(data); if (POLYHEDRA[data.view?.shape]) view.shape = data.view.shape; }
  } catch { /* corrupt or blocked storage: start empty */ }
  function save() {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify({ version: 1, ...toJSON(), view })); } catch { /* best-effort */ }
  }

  // ---- drawing ----
  const pieceMaterial = new THREE.MeshStandardMaterial({ vertexColors: true, flatShading: true, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
  const outlineMaterial = new THREE.MeshStandardMaterial({ transparent: true, opacity: 0.16, depthWrite: false, side: THREE.DoubleSide });
  const pickTargets = [];
  let faceOwner = []; // triangle index -> { node, face }
  function clearGroup() {
    for (const child of [...group.children]) {
      group.remove(child);
      if (child.userData.poly === 'sphere') { child.material.dispose(); continue; }
      child.geometry.dispose();
      if (child.isLineSegments) child.material.dispose();
    }
    pickTargets.length = 0;
  }
  const worldPoints = (n) => {
    const q = new THREE.Quaternion(...n.transform.quaternion), p = new THREE.Vector3(...n.transform.position);
    return POLYHEDRA[n.shape].vertices.map((v) => new THREE.Vector3(...v).applyQuaternion(q).add(p));
  };
  function meshOf(list, material, colour, edgeColor, record) {
    const pos = [], col = [], edge = [];
    const c = new THREE.Color();
    for (const n of list) {
      colour(n, c);
      const P = worldPoints(n), s = POLYHEDRA[n.shape];
      s.faces.forEach((f, fi) => {
        for (let i = 1; i < f.length - 1; i++) {
          for (const k of [f[0], f[i], f[i + 1]]) { pos.push(P[k].x, P[k].y, P[k].z); col.push(c.r, c.g, c.b); }
          record?.push({ node: n, face: fi });
        }
      });
      for (const [a, b] of s.edges) edge.push(P[a].x, P[a].y, P[a].z, P[b].x, P[b].y, P[b].z);
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    g.setAttribute('color', new THREE.Float32BufferAttribute(col, 3));
    g.computeVertexNormals();
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
  function rebuild() {
    clearGroup();
    if (!active) return;
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
      pieceMaterial.transparent = opacity < 1;
      pieceMaterial.opacity = opacity;
      pieceMaterial.depthWrite = opacity >= 1;
      faceOwner = [];
      const [mesh, lines] = meshOf(nodes, pieceMaterial, (n, c) => c.copy(colorOf(n.shape, n.material, familiesFor(n.shape)[0])), EDGE_COLOR, faceOwner);
      mesh.userData.poly = 'piece';
      mesh.visible = !skeleton;
      if (skeleton) lines.material.color.setHex(theme().accentHex);
      group.add(mesh, lines);
      pickTargets.push(mesh);
      // The tapped face, waiting for a shape: a bright overlay just off the surface.
      if (selection && nodes.includes(selection.node)) group.add(faceHighlight(selection.node, selection.face));
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
  let selection = null; // { node, face }: a face waiting for a shape
  let chosen = null; // the shape that stays chosen
  const PARALLELOHEDRA = new Set(familyIds('PARALLELOHEDRA'));
  const matrixOf = (n) => new THREE.Matrix4().compose(new THREE.Vector3(...n.transform.position), new THREE.Quaternion(...n.transform.quaternion), new THREE.Vector3(1, 1, 1));
  const faceTaken = (n, fi) => connections.some((c) => (c.nodeA === n.id && c.vertexA === fi) || (c.nodeB === n.id && c.vertexB === fi));
  // The faces of a shape that can go on this face (eligible and congruent), [] if none.
  function fittingFaces(id, n, fi) {
    const spec = POLYHEDRA[id], target = POLYHEDRA[n.shape];
    if (!spec) return [];
    const tf = target.faces[fi];
    return spec.faces.map((f, k) => k).filter((k) => isFaceEligibleForAttach(spec, k) && spec.faces[k].length === tf.length && facesCongruent(target.vertices, tf, spec.vertices, spec.faces[k]));
  }
  const fits = (id, n, fi) => fittingFaces(id, n, fi).length > 0;
  function faceHighlight(n, fi) {
    const P = worldPoints(n), f = POLYHEDRA[n.shape].faces[fi];
    const c = f.reduce((a, k) => a.add(P[k].clone()), new THREE.Vector3()).divideScalar(f.length);
    const nrm = P[f[1]].clone().sub(P[f[0]]).cross(P[f[2]].clone().sub(P[f[0]])).normalize();
    if (nrm.dot(c.clone().sub(P.reduce((a, v) => a.add(v.clone()), new THREE.Vector3()).divideScalar(P.length))) < 0) nrm.negate();
    const lift = nrm.multiplyScalar(0.004);
    const pos = [];
    for (let i = 1; i < f.length - 1; i++) for (const k of [f[0], f[i], f[i + 1]]) { const q = P[k].clone().add(lift); pos.push(q.x, q.y, q.z); }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    const m = new THREE.Mesh(g, new THREE.MeshBasicMaterial({ color: theme().contrastHex, transparent: true, opacity: 0.75, side: THREE.DoubleSide, depthWrite: false }));
    m.userData.poly = 'highlight';
    return m;
  }
  // Attach shape `id` on face fi of node n, the best fit first; false if it doesn't fit there.
  function attach(id, n, fi) {
    const incoming = fittingFaces(id, n, fi);
    if (!incoming.length) return false;
    const spec = POLYHEDRA[id];
    const options = faceAttachOptions(POLYHEDRA[n.shape], fi, matrixOf(n), spec, incoming);
    if (!options.length) return false;
    const built = nodes.map((x) => ({ spec: POLYHEDRA[x.shape], matrixWorld: matrixOf(x) }));
    const ranked = rankFaceAttachOptions(options, spec, built, nodes.indexOf(n), fi, id === n.shape && PARALLELOHEDRA.has(id));
    const best = ranked[0].option;
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
    const r = Math.max(...nodes.flatMap((n) => worldPoints(n).map((v) => v.length())));
    if (r > fittedRadius * 1.25) { fittedRadius = r; fitView?.(r); }
  }
  function remove(n) {
    nodes = nodes.filter((x) => x !== n);
    connections = connections.filter((c) => c.nodeA !== n.id && c.nodeB !== n.id);
    if (selection?.node === n) selection = null;
    commit();
  }

  function commit() { save(); rebuild(); onChange(); renderPanel(); }
  function handleTap(hit, mode) {
    const kind = hit.object.userData.poly;
    if (kind === 'outline') {
      if (mode === 'chisel' || mode === 'paint') return false;
      nodes.push({ ...outlineNode(), id: `n${nextId++}`, material: getMaterial() });
      commit();
      return true;
    }
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
    if (faceTaken(n, rec.face)) { showHudPrompt(t('poly.taken', lang()), 2000); return false; }
    // The chosen shape goes straight on when it fits; otherwise the face waits for a shape.
    if (chosen && attach(chosen, n, rec.face)) return true;
    selection = { node: n, face: rec.face };
    rebuild();
    renderPanel();
    if (!queue().some((id) => fits(id, n, rec.face))) showHudPrompt(t('poly.noFit', lang()), 3000);
    return true;
  }

  // ---- the shape strip ----
  // Shapes to offer: the build's own (newest first) and the shape last chosen in DICTO, up to 8.
  function queue() {
    const out = [];
    for (const id of [chosen, ...nodes.map((n) => n.shape).reverse(), view.shape]) if (id && POLYHEDRA[id] && !out.includes(id)) out.push(id);
    return out.slice(0, 8);
  }
  const panel = document.createElement('div');
  panel.className = 'poly-strip';
  document.body.appendChild(panel);
  let disposers = [];
  function renderPanel() {
    disposers.forEach((d) => d()); disposers = [];
    const show = active && !spherical && (selection || chosen);
    panel.hidden = !show;
    if (!show) return;
    const L = lang();
    const offer = selection ? queue().filter((id) => fits(id, selection.node, selection.face)) : chosen ? [chosen] : [];
    panel.innerHTML = `<div class="poly-shapes">${offer.map((id) => `<button type="button" class="poly-shape${id === chosen ? ' chosen' : ''}" data-shape="${id}" title="${polyShapeName(id).replaceAll('_', ' ')}"><canvas></canvas></button>`).join('')}
      ${selection ? `<button type="button" class="poly-more" data-more>${t('poly.more', L)}</button>` : ''}
      ${chosen ? `<button type="button" class="poly-clear" data-clear title="${t('poly.clear', L, { name: polyShapeName(chosen).replaceAll('_', ' ') })}">✕</button>` : ''}</div>`;
    panel.querySelectorAll('.poly-shape canvas').forEach((cv) => disposers.push(mountWireframePreview(cv, polyShapeEdges(cv.parentElement.dataset.shape), 34)));
  }
  panel.addEventListener('click', (e) => {
    const b = e.target.closest('button');
    if (!b) return;
    if ('clear' in b.dataset) { chosen = null; renderPanel(); return; }
    if ('more' in b.dataset && selection) {
      const sel = selection;
      pickShape((id) => fits(id, sel.node, sel.face), (id) => { chosen = id; attach(id, sel.node, sel.face); });
      return;
    }
    if (b.dataset.shape) {
      const id = b.dataset.shape;
      if (selection) { chosen = id; attach(id, selection.node, selection.face); }
      else { chosen = chosen === id ? null : id; renderPanel(); }
    }
  });

  let shownLang = lang();
  onSettingsChange((st) => { if (st.language !== shownLang) { shownLang = st.language; renderPanel(); if (active) rebuild(); } });

  return {
    group,
    meshes: () => pickTargets,
    handleTap,
    setActive(on) {
      if (on === active) return;
      active = on;
      group.visible = on;
      if (!on) selection = null;
      rebuild();
      renderPanel();
    },
    setSkeleton(on) { skeleton = on; if (active) rebuild(); },
    setTranslucent(o) { if (o !== opacity) { opacity = o; if (active) rebuild(); } },
    setLatticeView() { /* no lattice here: shapes are placed freely */ },
    refresh() { if (active) rebuild(); },
    setSpherical(on, scale = 1) { if (on === spherical && scale === sphereScale) return; spherical = on; sphereScale = scale; if (active) rebuild(); },
    /** DICTO's shape list: build with this shape. An empty world shows its outline to tap; with a
     *  build, it becomes the chosen shape, going straight onto each face tapped. */
    startWith(id) {
      if (!POLYHEDRA[id]) return;
      view.shape = id;
      if (nodes.length) { chosen = id; commit(); showHudPrompt(t('poly.chosen', lang(), { name: polyShapeName(id).replaceAll('_', ' ') }), 3000); return; }
      commit();
      fittedRadius = Math.max(...POLYHEDRA[id].vertices.map((v) => Math.hypot(...v)));
      fitView?.(fittedRadius);
      showHudPrompt(polyShapeName(id), 2500);
    },
    get shape() { return view.shape; },
    get isEmpty() { return nodes.length === 0; },
    clear() { nodes = []; connections = []; selection = null; chosen = null; commit(); },
    snapshot: toJSON,
    restore(json) { setFromJSON(json); selection = null; save(); rebuild(); renderPanel(); onChange(); },
    toJSON,
  };
}
