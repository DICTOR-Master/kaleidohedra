# DICTO 2026-10-20: Figure 4 of #37a V3: each solid with the fill pieces that touch it, pulled apart (from renders/kits-data.json)
# -> renders/clusters.html (one cluster per frame; shots with cover_shots.mjs) -> compose -> figures/clusters.jpg
import os, json, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(H, 'renders', 'kits-data.json')))['kits']
GOLD, G1, G2, TEAL = '#d9a521', '#3f9a5b', '#57b06f', '#2a9d9a'
frames = []
for key, solid_col, fill_col in (('dbt-gyr', '#cf9418', G1), ('cut8-gyr', '#e0ae2c', G2), ('cut8-oct', '#e0ae2c', G1)):
    k = K[key]; parts = [dict(v=k['solid']['v'], t=k['solid']['t'], colour=solid_col, off=[0, 0, 0])]
    for f in k['fills']:
        P = np.array(f['v']); c = P.mean(0); u = c / np.linalg.norm(c)
        parts.append(dict(v=f['v'], t=f['t'], colour=(TEAL if f['hand'] < 0 else fill_col), off=(u * 0.7).round(4).tolist()))
    frames.append(parts)
ext = max(np.linalg.norm(np.array(p['v']) + np.array(p['off']), axis=1).max() for fr in frames for p in fr) * 1.02   # farthest point: no clipping in any view
src = open(os.path.join(H, 'renders', 'lineup.html')).read()
a = src.index('const D = '); b = src.index(';', src.index(', E = ')) + 1
src = src[:a] + f'const D = {json.dumps(frames, separators=(",", ":"))}, E = {ext:.4f};' + src[b:]
old = src[src.index('window.show = (i) =>'):src.index('</script></body>')]
new = '''window.show = (i) => { if (grp) scene.remove(grp); grp = new THREE.Group();
  for (const d of D[i]) { const g = new THREE.BufferGeometry(); const p = new Float32Array(d.t.length * 9); let k = 0;
    for (const tr of d.t) for (const j of tr) { p[k++] = d.v[j][0] + d.off[0]; p[k++] = d.v[j][1] + d.off[1]; p[k++] = d.v[j][2] + d.off[2]; }
    g.setAttribute('position', new THREE.BufferAttribute(p, 3)); g.computeVertexNormals();
    grp.add(new THREE.Mesh(g, new THREE.MeshStandardMaterial({ color: d.colour, roughness: 0.5, metalness: 0.06, flatShading: true })));
    grp.add(new THREE.LineSegments(new THREE.EdgesGeometry(g, 18), new THREE.LineBasicMaterial({ color: 0x2b261e, transparent: true, opacity: 0.4 }))); }
  scene.add(grp); r.render(scene, cam); return D.length; };
'''
src = src.replace(old, new)
open(os.path.join(H, 'renders', 'clusters.html'), 'w').write(src); print('clusters.html', len(frames), 'frames, half-width', round(ext, 3))
