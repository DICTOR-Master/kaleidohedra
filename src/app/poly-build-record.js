// Copy build (DICTO 2026-11-11): an exact record of a Polyhedraverse build, to send for research. Each piece with
// its solid, the piece and face it is attached to, its own attached face, its turn as stored (quaternion and
// position), and its corners in world coordinates (full float precision) with its faces, so the build can be
// rebuilt without the app. Pure: no DOM; copyText below is the clipboard part.
import * as THREE from 'three';

const faceList = (f) => (Array.isArray(f) ? f : f.vertices);

/** The record of a build: nodes and connections as world-poly.js keeps them, POLYHEDRA the shape registry,
 *  caption the build's running name. */
export function buildRecord(nodes, connections, POLYHEDRA, caption) {
  const index = new Map(nodes.map((n, i) => [n.id, i]));
  // each piece's own join: the connection that brought it in (nodeA the piece it went on, nodeB the piece itself)
  const joinOf = new Map();
  for (const c of connections) if (!c.orphaned && index.has(c.nodeA) && index.has(c.nodeB) && !joinOf.has(c.nodeB)) joinOf.set(c.nodeB, c);
  const pieces = nodes.map((n, i) => {
    const spec = POLYHEDRA[n.shape];
    const q = new THREE.Quaternion(...n.transform.quaternion), p = new THREE.Vector3(...n.transform.position);
    const c = joinOf.get(n.id);
    const join = !c ? {} : c.kind === 'vertex'
      ? { join: 'corner', parentCorner: c.vertexA, corner: c.vertexB }
      : { join: c.kind ?? 'face', parentFace: c.vertexA, face: c.vertexB };
    return {
      i,
      solid: n.shape,
      name: spec?.name ?? n.shape,
      parent: c ? index.get(c.nodeA) : null,
      ...join,
      turn: { quaternion: [...n.transform.quaternion], position: [...n.transform.position] },
      vertices: (spec?.vertices ?? []).map((v) => new THREE.Vector3(...v).applyQuaternion(q).add(p).toArray()),
      faces: (spec?.faces ?? []).map((f) => [...faceList(f)]),
    };
  });
  return { app: 'Polyhedraverse', version: 1, caption, pieces };
}

/** Whether a build has a piece attached to another (the Copy build button shows only then). */
export const hasAttached = (nodes, connections) => {
  const ids = new Set(nodes.map((n) => n.id));
  return connections.some((c) => !c.orphaned && ids.has(c.nodeA) && ids.has(c.nodeB));
};

/** Copy text to the clipboard: the Clipboard API, else (older iPad Safari) a selected textarea and execCommand('copy').
 *  Resolves true when copied, false when it could not be. */
export async function copyText(text) {
  try {
    if (navigator.clipboard?.writeText) { await navigator.clipboard.writeText(text); return true; }
  } catch { /* fall through to the older way */ }
  const ta = document.createElement('textarea');
  ta.value = text;
  ta.setAttribute('readonly', '');
  ta.style.cssText = 'position:fixed;top:0;left:0;width:1px;height:1px;opacity:0;font-size:16px';
  document.body.appendChild(ta);
  let ok = false;
  try {
    ta.focus();
    ta.select();
    ta.setSelectionRange(0, text.length);
    ok = document.execCommand('copy');
  } catch { ok = false; }
  ta.remove();
  return ok;
}
