# DICTO · dictospheres.com — the three.js renderer of the gold-standard figures (paper #43: studies 2026-10-19-five-fold-octet
# family_figs.py), copied unchanged from the Dehn Canon paper (2026-11-19-dehn-canon/scripts), which extended it with a view direction per scene and edges drawn
# as tubes (one colour per edge, an outline tube behind it so dark edges stay visible on the dark ground) with balls at the
# corners. Lights at 0.8 of the Dehn Canon values here, so that the pale silver and cream faces keep their tone (no faces
# washed out to white). Orthographic camera; project() gives the pixel of a 3D point exactly as the camera draws it, for labels.
# 20 Nov (Dehn–Hadwiger 4D, Version 2): a part marked 'top' is drawn in a second pass after the depth buffer is cleared, so
# nothing hides it (a small coloured facet inside a dense wire solid); within each pass solid faces hide what lies behind them.
import json, os
import numpy as np

PX = 1600
HTML = '''<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;background:transparent}canvas{display:block}</style></head><body>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script><script>
const SC = __D__; const PX = __PX__;
const r = new THREE.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true }); r.setPixelRatio(1); r.setSize(PX, PX); r.setClearColor(0x000000, 0); document.body.append(r.domElement);
let scene = null, cam = null;
function tube(a, b, rad, col, back) {
  const A = new THREE.Vector3(...a), B = new THREE.Vector3(...b), d = B.clone().sub(A), L = d.length();
  const m = new THREE.Mesh(new THREE.CylinderGeometry(rad, rad, L, 20, 1, true), new THREE.MeshStandardMaterial({ color: col, roughness: 0.55, metalness: 0.0, side: back ? THREE.BackSide : THREE.FrontSide }));
  m.position.copy(A.clone().add(B).multiplyScalar(0.5)); m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), d.normalize()); return m; }
window.show = (i) => { const s = SC[i]; scene = new THREE.Scene(); const E = s.E; const dir = new THREE.Vector3(...s.dir).normalize();
  scene.add(new THREE.HemisphereLight(0xffffff, 0xb8b0a0, 0.50)); const F = new THREE.DirectionalLight(0xffffff, 0.32); F.position.copy(dir.clone().multiplyScalar(6)); scene.add(F);
  const L = new THREE.DirectionalLight(0xffffff, 0.50); L.position.copy(dir.clone().multiplyScalar(4).add(new THREE.Vector3(-2, 3, 1))); scene.add(L);
  cam = new THREE.OrthographicCamera(-E, E, E, -E, 0.1, 50); cam.up.set(0, 1, 0); cam.position.copy(dir.clone().multiplyScalar(10)); cam.lookAt(0, 0, 0);
  const grp = new THREE.Group(), top = new THREE.Group();
  for (const d of s.parts) { const grp0 = d.top ? top : grp;
    const g = new THREE.BufferGeometry(); const p = new Float32Array(d.t.length * 9), c = new Float32Array(d.t.length * 9); let k = 0;
    d.t.forEach((tr, ti) => { const col = new THREE.Color(d.c[ti]); for (const j of tr) { p[k] = d.v[j][0]; p[k + 1] = d.v[j][1]; p[k + 2] = d.v[j][2]; c[k] = col.r; c[k + 1] = col.g; c[k + 2] = col.b; k += 3; } });
    g.setAttribute('position', new THREE.BufferAttribute(p, 3)); g.setAttribute('color', new THREE.BufferAttribute(c, 3)); g.computeVertexNormals();
    const glass = d.a < 1; const mesh = new THREE.Mesh(g, new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.5, metalness: 0.05, flatShading: true, transparent: glass, opacity: d.a, depthWrite: !glass, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 }));
    if (glass) mesh.renderOrder = 5; grp0.add(mesh);
    for (const e of (d.tubes || [])) {
      grp0.add(tube(d.v[e[0]], d.v[e[1]], d.rad * E, e[2], false));
      if (e[3]) grp0.add(tube(d.v[e[0]], d.v[e[1]], d.rad * E * 1.55, e[3], true));
    }
    for (const b of (d.balls || [])) { const m = new THREE.Mesh(new THREE.SphereGeometry(d.rad * E * 1.25, 20, 14), new THREE.MeshStandardMaterial({ color: b[1], roughness: 0.55 })); m.position.set(...d.v[b[0]]); grp0.add(m); }
  }
  scene.add(grp); scene.add(top); r.autoClear = true; top.visible = false; r.render(scene, cam);
  if (top.children.length) { r.autoClear = false; grp.visible = false; top.visible = true; r.clearDepth(); r.render(scene, cam); grp.visible = true; r.autoClear = true; }
  return SC.length; };
</script></body></html>'''


def basis(dirv):
    z = np.asarray(dirv, float); z = z / np.linalg.norm(z)
    x = np.cross([0, 1, 0], z); x /= np.linalg.norm(x); y = np.cross(z, x)
    return x, y, z


def project(P, dirv, E):
    """Pixel coordinates (in the PX × PX shot) of 3D points, as the orthographic camera of HTML draws them."""
    x, y, _ = basis(dirv); P = np.atleast_2d(P)
    return np.c_[(P @ x / E + 1) / 2 * PX, (1 - P @ y / E) / 2 * PX]


def solid_part(S, col, P=None, alpha=1.0, edge_col='#2b261e', rad=0.006, outline=None, edge_cols=None, ball=None, faces=None):
    """A Solid as a mesh part: faces in col (or a list per face), edges as tubes. P overrides the float corners."""
    V = S.vf() if P is None else P; tris, cols = [], []
    for k, (n, d, o) in enumerate(S.F):
        if faces is not None and k not in faces: continue
        c = col[k] if isinstance(col, list) else col
        for a, b in zip(o[1:-1], o[2:]): tris.append([o[0], a, b]); cols.append(c)
    tubes = []
    for k, e in enumerate(S.E):
        ec = edge_cols[k] if edge_cols else edge_col
        oc = outline[k] if isinstance(outline, list) else outline
        tubes.append([int(e[0]), int(e[1]), ec, oc])
    balls = [[i, ball] for i in range(len(V))] if ball else []
    return {'v': np.round(V, 6).tolist(), 't': tris, 'c': cols, 'a': alpha, 'tubes': tubes, 'rad': rad, 'balls': balls}


def write(path, scenes):
    open(path, 'w').write(HTML.replace('__D__', json.dumps(scenes, separators=(',', ':'))).replace('__PX__', str(PX)))
