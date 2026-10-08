// Polyhedraverse inside the joined app (step D2, DICTO 2026-10-09): its own 3D world, the portrait
// gallery's shapes from krp-core (src/polyhedra). Choose a shape in DICTO (families, then shapes);
// an empty world shows its outline in the app's colour, tap it to place it. Building on faces and
// vertices comes with D3, the shape browser with D4 (PLAN-POLYHEDRAVERSE.md).
// Saved in Polyhedraverse's own form (krp-core assembly: nodes with a shape and a transform), so a
// build moves between this world and the old site by Export/Import.
import * as THREE from 'three';
import { POLYHEDRA } from '../krp-core/src/polyhedra/index.js';
import { familiesFor } from '../krp-core/src/polyhedra/families.js';
import { FAMILY_COLORS } from '../krp-core/src/assembly/pieceColors.js';
import { getSettings, onSettingsChange } from './settings.js';
import { storageKey, theme } from './site.js';
import { polyShapeName } from './poly-shapes.js';

export { polyShapeEdges, polyShapeName } from './poly-shapes.js';

const STORAGE_KEY = storageKey('poly-world');
const EDGE_COLOR = 0x0b1220;
const DEFAULT_SHAPE = 'DODECAHEDRON';
const lang = () => getSettings().language;

export function createPolyWorld({ scene, colorOf, getMaterial, onChange = () => {}, showHudPrompt = () => {}, fitView = () => {} }) {
  const group = new THREE.Group();
  group.visible = false;
  scene.add(group);

  // ---- state: Polyhedraverse's assembly form ----
  let nodes = []; // { id, shape, transform: { position, quaternion }, material }
  const view = { shape: DEFAULT_SHAPE };
  let active = false, skeleton = false, opacity = 1;
  let nextId = 1;

  const validNode = (n) => n && POLYHEDRA[n.shape] && Array.isArray(n.transform?.position) && n.transform.position.length === 3
    && Array.isArray(n.transform?.quaternion) && n.transform.quaternion.length === 4;
  function setFromJSON(data) {
    nodes = (Array.isArray(data?.nodes) ? data.nodes : []).filter(validNode).map((n) => ({
      id: String(n.id), shape: n.shape, transform: { position: [...n.transform.position], quaternion: [...n.transform.quaternion] },
      ...(typeof n.material === 'string' ? { material: n.material } : {}),
    }));
    nextId = 1 + Math.max(0, ...nodes.map((n) => Number(String(n.id).replace(/\D/g, '')) || 0));
  }
  const toJSON = () => ({ nodes: nodes.map((n) => ({ ...n })), connections: [] });
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
  let faceOwner = []; // triangle index -> node
  function clearGroup() {
    for (const child of [...group.children]) { group.remove(child); child.geometry.dispose(); if (child.isLineSegments) child.material.dispose(); }
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
      for (const f of s.faces) {
        for (let i = 1; i < f.length - 1; i++) {
          for (const k of [f[0], f[i], f[i + 1]]) { pos.push(P[k].x, P[k].y, P[k].z); col.push(c.r, c.g, c.b); }
          record?.push(n);
        }
      }
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
  const outlineNode = () => ({ id: 'outline', shape: view.shape, transform: { position: [0, 0, 0], quaternion: [0, 0, 0, 1] } });
  function rebuild() {
    clearGroup();
    if (!active) return;
    if (nodes.length) {
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
    } else {
      outlineMaterial.color.setHex(theme().strongHex);
      const [mesh, lines] = meshOf([outlineNode()], outlineMaterial, (n, c) => c.setHex(theme().strongHex), theme().strongHex);
      mesh.userData.poly = 'outline';
      group.add(mesh, lines);
      pickTargets.push(mesh);
    }
  }

  // ---- building (D2: the first piece; attaching comes with D3) ----
  function commit() { save(); rebuild(); onChange(); }
  function handleTap(hit, mode) {
    const kind = hit.object.userData.poly;
    if (kind === 'outline') {
      if (mode === 'chisel' || mode === 'paint') return false;
      nodes.push({ ...outlineNode(), id: `n${nextId++}`, material: getMaterial() });
      commit();
      return true;
    }
    if (kind !== 'piece') return false;
    const n = faceOwner[hit.faceIndex];
    if (!n) return false;
    if (mode === 'chisel') { nodes = nodes.filter((x) => x !== n); commit(); return true; }
    if (mode === 'paint') {
      const m = getMaterial();
      if (n.material === m) return false;
      n.material = m; commit(); return true;
    }
    return false;
  }

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
      rebuild();
    },
    setSkeleton(on) { skeleton = on; if (active) rebuild(); },
    setTranslucent(o) { if (o !== opacity) { opacity = o; if (active) rebuild(); } },
    setLatticeView() { /* no lattice here: shapes are placed freely */ },
    refresh() { if (active) rebuild(); },
    /** DICTO's shape list: build with this shape. An empty world shows its outline; a world holding
     *  only one placed shape starts over with the new one (until D3 there is nothing else to keep). */
    startWith(id) {
      if (!POLYHEDRA[id]) return;
      view.shape = id;
      if (nodes.length === 1) nodes = [];
      commit();
      fitView?.(Math.max(...POLYHEDRA[id].vertices.map((v) => Math.hypot(...v))));
      showHudPrompt(polyShapeName(id), 2500);
    },
    get shape() { return view.shape; },
    get isEmpty() { return nodes.length === 0; },
    clear() { nodes = []; commit(); },
    snapshot: toJSON,
    restore(json) { setFromJSON(json); save(); rebuild(); onChange(); },
    toJSON,
  };
}
