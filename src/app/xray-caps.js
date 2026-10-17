// X-ray solid infill (DICTO 2026-10-17: "crystal infill on the Cleo-Icosa and other spikes, as it gives a confusing perspective in X-ray
// otherwise", then "just solid infill of the same colour may be better"; every world with X-ray). Wherever the X-ray plane cuts a solid
// piece, you see into it; its inside is drawn flat in the piece's own colour, so through the cut it reads as a solid face of that colour (a
// gold spike cuts gold, a cyan core cyan) instead of a hollow skin. DICTO then: translucent and crystal pieces get the same infill at
// their own see-through strength, and so does any world's own cut (Vajrayana's wedge); station and helper shells stay hollow (a world
// marks their material userData.hollow).
// How: every solid the plane clips gets a companion drawn with its back faces only, unlit, in its own colour (per instance and per vertex
// colours kept), pulled a hair towards the camera so it wins over the piece's own back faces. Instanced pieces share their instance
// matrices and colours, so a lattice of thousands costs one extra draw per mesh.
import * as THREE from 'three';

export function createXrayCaps({ scene, plane }) {
  const group = new THREE.Group(); group.name = 'xray-caps'; group.userData.noIcoScan = true; scene.add(group);
  const pairs = new Map(); // source mesh -> companion
  const mats = new Map(); // source material -> its infill material
  // anything cut (the X-ray plane or a world's own planes) that is not marked hollow
  const solid = (m) => !m.userData.hollow && [].concat(m.material).every((x) => x && x.clippingPlanes?.length && !x.userData?.hollow && x.visible !== false && x.colorWrite !== false && x.opacity > 0.01);
  function infill(src) {
    let f = mats.get(src);
    if (!f) {
      f = new THREE.MeshBasicMaterial({ side: THREE.BackSide, vertexColors: !!src.vertexColors,
        color: src.color ? src.color.clone() : new THREE.Color(0xcccccc), polygonOffset: true, polygonOffsetFactor: -1, polygonOffsetUnits: -1 });
      mats.set(src, f);
    }
    if (src.color && !f.color.equals(src.color)) f.color.copy(src.color);
    // the same cut and the same see-through strength as the piece
    const see = src.transparent && src.opacity < 1;
    if (f.clippingPlanes !== src.clippingPlanes || f.clipIntersection !== src.clipIntersection || f.transparent !== see) {
      f.clippingPlanes = src.clippingPlanes; f.clipIntersection = src.clipIntersection; f.transparent = see; f.depthWrite = !see; f.needsUpdate = true;
    }
    f.opacity = see ? src.opacity : 1;
    return f;
  }
  function companion(src) {
    const material = Array.isArray(src.material) ? src.material.map(infill) : infill(src.material);
    let c;
    if (src.isInstancedMesh) { c = new THREE.InstancedMesh(src.geometry, material, src.count); c.instanceMatrix = src.instanceMatrix; c.instanceColor = src.instanceColor; }
    else c = new THREE.Mesh(src.geometry, material);
    c.matrixAutoUpdate = false; c.frustumCulled = false; c.userData.noIcoScan = true; c.raycast = () => {};
    group.add(c); return c;
  }
  return {
    /** Called each frame before rendering; returns how many cut solids are filled. */
    update() {
      const seen = new Set();
      scene.traverseVisible((o) => {
        if (!o.isMesh || o.userData.noIcoScan || o.parent === group || !solid(o)) return;
        seen.add(o);
        let c = pairs.get(o);
        if (!c) { c = companion(o); pairs.set(o, c); }
        c.matrix.copy(o.matrixWorld); c.matrixWorld.copy(o.matrixWorld);
        if (c.geometry !== o.geometry) c.geometry = o.geometry;
        if (o.isInstancedMesh) { c.count = o.count; c.instanceMatrix = o.instanceMatrix; c.instanceColor = o.instanceColor; }
        for (const m of [].concat(o.material)) infill(m);
      });
      for (const [o, c] of pairs) if (!seen.has(o)) { group.remove(c); pairs.delete(o); }
      return pairs.size;
    },
  };
}
