// Star step (DICTO's Star Cores papers, #79): Polyhedraverse's ★ Star step for the convex solid on show. Each tap advances one step,
// animated: Star (every face's pyramid from the centre turned outwards as a spike), Halo (the convex hull of the tips as a see-through
// shell round the solid star; for the polar rule the layer between them in its pieces, corner pyramids gold and edge tetrahedra teal),
// Next (the halo becomes the new solid, scaled back to the solid's size, ready for the next star: the star chain). The geometry is
// star-step-geometry.js; this file only draws it, to the render standard (docs/RENDER-STANDARD.md): solid faces with polygon offset,
// crisp screen-space edges ≥ 1.5 px, the halo glass with its outline edges at full opacity.
import * as THREE from 'three';
import { LineSegments2 } from 'three/addons/lines/LineSegments2.js';
import { LineSegmentsGeometry } from 'three/addons/lines/LineSegmentsGeometry.js';
import { LineMaterial } from 'three/addons/lines/LineMaterial.js';
import { RULES, solidOf, starStep, nextSolid } from './star-step-geometry.js';
import { t } from './i18n.js';

export const STAR_PHASES = ['star', 'halo', 'next'];
const DURATION = 600;                 // ms, one step's animation
const SPIKE = 0x8f5bd8, CORNER = 0xd9a520, EDGE_PIECE = 0x4dd0e1;
const EDGE = 0x0b1220, HALO_EDGE = 0xe8eefc;
const HALO_GLASS = 0.26;              // the see-through shell's opacity
const PIECE_SHRINK = 0.82;            // the layer pieces drawn a little in from their own centres, so each reads as a piece
const ease = (u) => u * u * (3 - 2 * u);

/** The phase after n taps: 'solid' before the first, then star, halo, next in turn. */
export const phaseOf = (n) => (n <= 0 ? 'solid' : STAR_PHASES[(n - 1) % 3]);

export function createStarStep({ scene, fitView = () => {}, look = () => ({ skeleton: false, opacity: 1 }), onSettled = () => {} }) {
  const root = new THREE.Group();
  const inner = new THREE.Group();
  root.add(inner);
  root.visible = false;
  scene.add(root);
  let st = null;      // { R, solid, rule, n, step, colour, layer }
  let anim = null;    // { from, u, raf }

  const solidMat = new THREE.MeshStandardMaterial({ flatShading: true, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1, roughness: 0.55 });
  const spikeMat = new THREE.MeshStandardMaterial({ color: SPIKE, flatShading: true, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1, roughness: 0.5 });
  const cornerMat = new THREE.MeshStandardMaterial({ color: CORNER, flatShading: true, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1, roughness: 0.45, metalness: 0.15 });
  const edgePieceMat = new THREE.MeshStandardMaterial({ color: EDGE_PIECE, flatShading: true, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1, roughness: 0.5 });
  const haloMat = new THREE.MeshStandardMaterial({ color: 0xcfe0ff, flatShading: true, side: THREE.DoubleSide, transparent: true, opacity: HALO_GLASS, depthWrite: false, roughness: 0.4 });
  const lineMats = [];
  const lineMat = (color, width, opacity = 1) => {
    const m = new LineMaterial({ color, linewidth: width, transparent: opacity < 1, opacity, depthWrite: opacity >= 1 });
    lineMats.push(m);
    return m;
  };

  function clear() {
    for (const c of [...inner.children]) { inner.remove(c); c.geometry.dispose(); }
    lineMats.splice(0).forEach((m) => m.dispose());
  }
  // Triangles (each [a, b, c] of points) as one flat-shaded mesh.
  function mesh(tris, material, order = 0) {
    const pos = new Float32Array(tris.length * 9);
    tris.forEach((tr, i) => tr.forEach((p, k) => pos.set(p, i * 9 + k * 3)));
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    g.computeVertexNormals();
    const m = new THREE.Mesh(g, material);
    m.renderOrder = order;
    inner.add(m);
    return m;
  }
  function lines(segs, color, width, opacity = 1, order = 0) {
    if (!segs.length) return null;
    const g = new LineSegmentsGeometry();
    g.setPositions(segs.flatMap(([a, b]) => [...a, ...b]));
    const l = new LineSegments2(g, lineMat(color, width, opacity));
    l.frustumCulled = false;
    l.renderOrder = order;
    inner.add(l);
    return l;
  }
  const fan = (loop) => loop.slice(1, -1).map((_, i) => [loop[0], loop[i + 1], loop[i + 2]]);
  const loopEdges = (loop) => loop.map((p, i) => [p, loop[(i + 1) % loop.length]]);
  const lerp = (a, b, u) => [a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u];
  const toward = (P, u) => { const c = P.reduce((s, p) => [s[0] + p[0] / P.length, s[1] + p[1] / P.length, s[2] + p[2] / P.length], [0, 0, 0]); return P.map((p) => lerp(c, p, u)); };
  const radius = (P) => Math.max(...P.map((p) => Math.hypot(...p)));

  // The picture at phase `phase`, `u` of the way into it (1 = arrived).
  function draw(phase, u = 1) {
    clear();
    if (!st) return;
    const { skeleton, opacity } = look();
    const see = opacity < 1;
    for (const m of [solidMat, spikeMat]) { m.transparent = see; m.opacity = see ? opacity : 1; m.depthWrite = !see; m.visible = !skeleton; }
    solidMat.color.copy(st.colour);
    const { solid, step } = st;
    const P = solid.vertices;
    const e = ease(u);
    inner.scale.setScalar(1);
    if (phase === 'solid' || (phase === 'next' && u >= 1)) {
      mesh(solid.faces.flatMap((f) => fan(f.map((k) => P[k]))), solidMat);
      lines(solid.edges.map(([a, b]) => [P[a], P[b]]), skeleton ? 0xffffff : EDGE, 2);
      return;
    }
    // The star: the solid and its spikes (growing out of their faces on the way into Star).
    const grow = phase === 'star' ? e : 1;
    const tips = solid.planes.map(({ n, c }, i) => lerp([n[0] * c, n[1] * c, n[2] * c], step.tips[i], grow));
    const fadeStar = phase === 'next' ? 1 - e : 1;
    if (fadeStar > 0.02) {
      mesh(solid.faces.flatMap((f) => fan(f.map((k) => P[k]))), solidMat);
      mesh(solid.faces.flatMap((f, fi) => f.map((k, i) => [P[k], P[f[(i + 1) % f.length]], tips[fi]])), spikeMat);
      const segs = solid.edges.map(([a, b]) => [P[a], P[b]]);
      solid.faces.forEach((f, fi) => f.forEach((k) => segs.push([P[k], tips[fi]])));
      lines(segs, skeleton ? 0xffffff : EDGE, 2, fadeStar < 1 ? fadeStar : 1);
    }
    if (phase === 'star') return;
    // The halo: see-through glass, outline edges at full opacity; on the way into Next it turns solid as it shrinks to size.
    const H = step.halo;
    const glass = phase === 'halo' ? HALO_GLASS * e : HALO_GLASS + (1 - HALO_GLASS) * e;
    haloMat.opacity = glass;
    haloMat.color.copy(phase === 'next' ? new THREE.Color(0xcfe0ff).lerp(st.colour, e) : new THREE.Color(0xcfe0ff));
    haloMat.depthWrite = phase === 'next' && e > 0.95;
    mesh(H.faces.flatMap((f) => fan(f.map((k) => H.vertices[k]))), haloMat, 3);
    lines(H.faces.flatMap((f) => loopEdges(f.map((k) => H.vertices[k]))), HALO_EDGE, 2, phase === 'halo' ? Math.max(0.05, e) : 1, 4);
    if (phase === 'halo' && step.layer && st.layer && !skeleton) {
      const k = PIECE_SHRINK * e;
      const cornerTris = [], edgeTris = [], segs = [];
      for (const { apex, base } of step.layer.corners) {
        const Q = toward([apex, ...base], k), A = Q[0], B = Q.slice(1);
        cornerTris.push(...fan(B), ...B.map((p, i) => [A, p, B[(i + 1) % B.length]]));
        segs.push(...loopEdges(B), ...B.map((p) => [A, p]));
      }
      for (const tet of step.layer.edges) {
        const [a, b, p, q] = toward(tet, k);
        edgeTris.push([a, b, p], [a, b, q], [a, p, q], [b, p, q]);
        segs.push([a, b], [a, p], [a, q], [b, p], [b, q], [p, q]);
      }
      mesh(cornerTris, cornerMat, 1);
      mesh(edgeTris, edgePieceMat, 1);
      lines(segs, EDGE, 1.5, 1, 1);
    }
    if (phase === 'next') inner.scale.setScalar(1 + (st.R / radius(H.vertices) - 1) * e);
  }

  function stopAnim() { if (anim) { cancelAnimationFrame(anim.raf); anim = null; } }
  function animate(phase) {
    stopAnim();
    const t0 = performance.now();
    anim = { raf: 0 };
    const tick = (now) => {
      const u = Math.min(1, (now - t0) / DURATION);
      draw(phase, u);
      if (u < 1) anim.raf = requestAnimationFrame(tick);
      else { anim = null; if (phase === 'next') afterNext(); onSettled(); }
    };
    anim.raf = requestAnimationFrame(tick);
  }
  // Arrived at Next: the halo, scaled back to the solid's size, is the solid now; its star step is ready.
  function afterNext() {
    st.solid = nextSolid(st.step, st.R) ?? st.solid;
    st.step = starStep(st.solid, st.rule);
    draw('next', 1);
  }
  const phase = () => (st ? phaseOf(st.n) : 'solid');

  return {
    root,
    get on() { return !!st; },
    get animating() { return !!anim; },
    /** Start on a shape spec ({ vertices, faces }) in colour `colour`, placed by `transform` ({ position, quaternion }). */
    start(spec, colour, transform) {
      const solid = solidOf(spec);
      if (!solid) return false;
      stopAnim();
      st = { R: solid.R, solid, rule: st?.rule ?? 'polar', n: 0, step: null, colour: new THREE.Color(colour), layer: true };
      st.step = starStep(solid, st.rule);
      // The solid is drawn about its own centre (star-step-geometry centres it), put back where the shape stands.
      const m = [0, 1, 2].map((k) => spec.vertices.reduce((s, v) => s + v[k], 0) / spec.vertices.length);
      const q = new THREE.Quaternion(...(transform?.quaternion ?? [0, 0, 0, 1]));
      root.quaternion.copy(q);
      root.position.set(...(transform?.position ?? [0, 0, 0])).add(new THREE.Vector3(...m).applyQuaternion(q));
      draw('solid');
      return true;
    },
    /** One step on; animated unless `quick`. */
    advance(quick = false) {
      if (!st) return;
      if (anim) { const was = phase(); stopAnim(); if (was === 'next') afterNext(); }
      st.n += 1;
      const p = phase();
      if (p === 'star') fitView(radius(st.step.halo.vertices));
      if (quick) { if (p === 'next') afterNext(); else draw(p); return; }
      animate(p);
    },
    reset() { stopAnim(); st = null; clear(); root.visible = false; },
    setVisible(on) { root.visible = on && !!st; if (root.visible && !anim) draw(phase()); },
    redraw() { if (st && !anim) draw(phase()); },
    setRule(rule) {
      if (!st || !RULES.includes(rule) || rule === st.rule) return;
      if (anim) { const was = phase(); stopAnim(); if (was === 'next') afterNext(); }
      st.rule = rule;
      st.step = starStep(st.solid, rule);
      if (phase() === 'star' || phase() === 'halo') fitView(radius(st.step.halo.vertices));
      draw(phase());
    },
    toggleLayer() { if (st) { st.layer = !st.layer; if (!anim) draw(phase()); } },
    get rule() { return st?.rule ?? 'polar'; },
    get layer() { return !!st?.layer; },
    /** Whether the halo step shows (or could show) layer pieces: the polar rule with the star inside its halo. */
    get hasLayer() { return !!st && phase() === 'halo' && !!st.step.layer; },
    get phase() { return phase(); },
    /** How far the picture reaches from the centre: the halo's radius at Star and Halo, else the solid's. */
    get reach() { if (!st) return 0; const p = phase(); return p === 'star' || p === 'halo' ? radius(st.step.halo.vertices) : st.R; },
    /** The caption: step number, the current solid's corners and faces, and at the halo the layer (polar) or why there is none. */
    caption(L) {
      if (!st) return '';
      const p = phase(), s = st.solid, step = st.step;
      const parts = [t('poly.star.step', L, { n: st.n }), t(`poly.star.phase.${p}`, L), t('poly.star.counts', L, { v: s.vertices.length, f: s.faces.length })];
      if (p === 'halo') {
        if (step.layer) parts.push(t('poly.star.layerCount', L, { v: s.vertices.length, e: s.edges.length }));
        else if (!step.contains) parts.push(t('poly.star.out', L));
      }
      return parts.join(' · ');
    },
    /** For the browser tests (?probe): the state in numbers. */
    probe() {
      if (!st) return null;
      return { n: st.n, phase: phase(), rule: st.rule, corners: st.solid.vertices.length, faces: st.solid.faces.length, edges: st.solid.edges.length,
        haloCorners: st.step.halo.vertices.length, haloFaces: st.step.halo.faces.length, contains: st.step.contains, layer: !!st.step.layer, animating: !!anim };
    },
  };
}
