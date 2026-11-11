#!/usr/bin/env python3
"""Photo-style render of the knitted HexOct rhombic dodecahedron cushion (n = 2 chart, m = 8), 2 November 2026.

Two stages, one file:
  prep   (python3 rd_knit_render.py prep OUTDIR): uses rd.py (faces, frame, classify, chart_face) to build
         the stuffed cushion mesh, the per-face stitch colour grids (same majority rule as the chart), and a
         stockinette colour + height texture atlas (one tile per face, stitch rows along each face's knitting frame);
         prints the checks (grid of face F0 == chart n = 2; all faces' grids; seam colour comparison).
  render (blender -b -P rd_knit_render.py -- OUTDIR VIEW SAMPLES RES): Cycles scene, one view per call.
  sheet  (python3 rd_knit_render.py sheet OUTDIR OUT.png): the two views side by side + the DICTO mark.

Real size: gauge 22 sts / 10 cm fixes the cubic unit (stitch width = sqrt(6)/12 units = 10/22 cm), so 1 unit = 2.227 cm,
rows 27.2 / 10 cm, face edge 15.4 cm, the cushion 35.6 cm between opposite 4-valent corners (before stuffing).
Shape: each face pushed out along its normal by A (4s(1-s))^al (4t(1-t))^al (s, t = edge coordinates; zero on the
seams), corners softened by a soft-min of the radius with a cap sphere, bottom face flattened on the floor
(all position-only functions, so the two sides of every seam stay joined).
Stitches: stockinette V's, two legs per stitch (round yarn cross-section, ply twist, legs dipping at the top where the
loop goes behind the next stitch), small hand-knit jitter, fibre noise; height faded to 0 over half a row at the seams.
"""
import sys, os, math, json

ASP = None  # stitch width / row height (physical), set in prep


# ======================================================================= prep
def prep(outdir):
    import numpy as np
    from fractions import Fraction as F
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import rd
    from scipy.ndimage import gaussian_filter
    os.makedirs(outdir, exist_ok=True)
    n, m = 2, 8
    W, R = rd.W_ST, rd.R_ST
    asp = W / R
    UNIT_M = (10 / 22) / W / 100          # metres per cubic unit
    fs = rd.faces(m)
    _, ups = rd.net_and_orientations()
    ch = rd.chart_face(n, ups, fs)
    X0, Y0, TX, TY = -1, -1, 35, 59        # tile window in stitch / row units
    PX = 24                                 # pixels per stitch width
    PY = PX / asp                           # pixels per row (non-integer)
    tw, th = TX * PX, int(round(TY * PY))
    NC, NR = 4, 3
    rng = np.random.default_rng(20261102)
    cols = np.zeros((NR * th, NC * tw, 3), np.float32)
    hts = np.zeros((NR * th, NC * tw), np.float32)
    def lin(hx):
        c = np.array([int(hx[i:i + 2], 16) / 255 for i in (1, 3, 5)], np.float32)
        return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4).astype(np.float32)
    CD, CL = lin(rd.GOLD_D), lin(rd.GOLD_L)
    # world orientation: face (-1,-1,0) down, face F0 = (1,-1,0) towards -y (the camera side)
    Q = np.array([[0, 0, -1], [-1 / math.sqrt(2), 1 / math.sqrt(2), 0], [1 / math.sqrt(2), 1 / math.sqrt(2), 0]])
    A, AL, RCAP, KR = 0.8, 0.6, 7.85, 0.3
    ZF, KF = -m / math.sqrt(2) - 0.35, 0.22
    NG = 256
    checks = {}
    verts, quads, luv = [], [], []
    grids = {}
    for k, f in enumerate(fs):
        Nn = f['N']
        u, r = rd.frame(f, ups[Nn])
        V3 = [np.array([float(x) for x in v]) for v in f['V']]
        co = [(float(np.dot(v, r)), float(np.dot(v, u))) for v in V3]
        xmin = min(c[0] for c in co)
        left = [i for i, c in enumerate(co) if abs(c[0] - xmin) < 1e-9]
        o = min(left, key=lambda i: co[i][1])
        O3 = V3[o]
        R2 = [((c[0] - co[o][0]) / W, (c[1] - co[o][1]) / R) for c in co]
        p3 = lambda x, y: O3 + x * W * r + y * R * u
        # stitch colour grid, chart rule: majority over 4 x 4 sub-points, tie -> dark
        sub = [-3 / 8, -1 / 8, 1 / 8, 3 / 8]
        g = np.zeros((TY, TX), np.int8)    # 1 = dark (tet), 0 = light (oct); index [j - Y0, c - X0]
        for j in range(Y0, Y0 + TY):
            for c in range(X0, X0 + TX):
                v = {'tet': 0, 'oct': 0}
                for a in sub:
                    for b in sub:
                        kk = rd.classify(tuple(p3(c + a, j + b)))
                        if kk: v[kk[0]] += 1
                g[j - Y0, c - X0] = 0 if v['oct'] > v['tet'] else 1
        grids[Nn] = (g, R2, O3, u, r)
        # ---------------- texture tile
        iy, ix = np.mgrid[0:th, 0:tw]
        Xs = X0 + (ix + 0.5) / PX                   # stitch-space x (cell c spans c-0.5..c+0.5)
        Ys = Y0 + (iy + 0.5) / PY
        Xs = Xs - 0.5; Ys = Ys - 0.5               # tile starts at the left/bottom edge of cell (X0, Y0)
        best = np.full(Xs.shape, 0.16, np.float32); own = np.full(Xs.shape, -1, np.int32)
        cc0 = np.floor(Xs + 0.5).astype(int); jj0 = np.floor(Ys + 0.5).astype(int)
        jit = rng.normal(0, 1, (TY + 2, TX + 2, 5)).astype(np.float32)
        for dj in (-1, 0, 1):
            for dc in (-1, 0, 1):
                cc, jj = cc0 + dc, jj0 + dj
                inb = (cc >= X0) & (cc < X0 + TX) & (jj >= Y0) & (jj < Y0 + TY)
                ci, ji = np.clip(cc - X0, 0, TX - 1), np.clip(jj - Y0, 0, TY - 1)
                J = jit[ji, ci]
                px = (Xs - cc) * asp; py = Ys - jj
                for side in (-1, 1):
                    Bx, By = side * (0.07 + 0.02 * J[..., 0]), -0.50 + 0.02 * J[..., 1]
                    Tx, Ty = side * (0.50 + 0.03 * J[..., 2]), 0.66 + 0.02 * J[..., 3]
                    rw0 = 0.285 * (1 + 0.04 * J[..., 4])
                    dx, dy = Tx - Bx, Ty - By; L2 = dx * dx + dy * dy
                    t = np.clip(((px - Bx) * dx + (py - By) * dy) / L2, 0, 1)
                    qx, qy = px - (Bx + t * dx), py - (By + t * dy)
                    d = np.hypot(qx, qy)
                    rw = rw0 * (1 - 0.22 * (2 * t - 1) ** 2)
                    hc = np.sqrt(np.clip(1 - (d / rw) ** 2, 0, 1))
                    sm = lambda a, b, x: np.clip((x - a) / (b - a), 0, 1) ** 2 * (3 - 2 * np.clip((x - a) / (b - a), 0, 1))
                    e = 1 - 0.55 * sm(0.62, 1.0, t) - 0.18 * sm(0.18, 0.0, t)
                    across = (qx * dy - qy * dx) / np.sqrt(L2) / rw
                    ply = 0.5 + 0.5 * np.sin(2 * np.pi * (t * np.sqrt(L2) / 0.27 - side * across * 0.6))
                    h = (0.16 + 0.84 * hc ** 0.8 * e) * (0.9 + 0.1 * ply)
                    h = np.where((hc > 0) & inb, h, 0)
                    upd = h > best
                    best = np.where(upd, h, best)
                    own = np.where(upd, (ji * TX + ci), own)
        fuzz = gaussian_filter(rng.normal(0, 1, Xs.shape), 0.8).astype(np.float32)
        fuzz /= fuzz.std() + 1e-9
        streak = gaussian_filter(rng.normal(0, 1, Xs.shape), (0.6, 2.5)).astype(np.float32)
        streak /= streak.std() + 1e-9
        hgt = np.clip(best + 0.035 * fuzz, 0, 1.2)
        # seam fade: distance to the rhombus boundary (physical, row units)
        P2 = [(x * asp, y) for x, y in R2]
        cx = sum(p[0] for p in P2) / 4; cy = sum(p[1] for p in P2) / 4
        dmin = np.full(Xs.shape, 1e9, np.float32)
        for i in range(4):
            (ax, ay), (bx, by) = P2[i], P2[(i + 1) % 4]
            nx, ny = by - ay, -(bx - ax); ln = math.hypot(nx, ny); nx /= ln; ny /= ln
            if (cx - ax) * nx + (cy - ay) * ny < 0: nx, ny = -nx, -ny
            dmin = np.minimum(dmin, (Xs * asp - ax) * nx + (Ys - ay) * ny)
        fade = np.clip(dmin / 0.5, 0, 1); fade = fade * fade * (3 - 2 * fade)
        hgt = hgt * fade
        # colour stitch by stitch (owner of the visible leg), tint per stitch, cavity + fibre streaks
        gflat = g.ravel()
        dark = np.where(own >= 0, gflat[np.clip(own, 0, None)], 1)
        base = np.where(dark[..., None] == 1, CD, CL)
        ow = np.clip(own, 0, None)
        tint = 1 + 0.025 * jit[ow // TX, ow % TX, 0]
        cav = 0.62 + 0.38 * np.clip(best, 0, 1) ** 0.7
        colr = base * (tint * cav * (1 + 0.045 * streak))[..., None]
        ty, tx = k // NC, k % NC
        cols[ty * th:(ty + 1) * th, tx * tw:(tx + 1) * tw] = colr
        hts[ty * th:(ty + 1) * th, tx * tw:(tx + 1) * tw] = hgt
        # ---------------- mesh of this face
        s, tt = np.meshgrid(np.linspace(0, 1, NG + 1), np.linspace(0, 1, NG + 1), indexing='ij')
        Pp = V3[0][None, None] + s[..., None] * (V3[1] - V3[0]) + tt[..., None] * (V3[3] - V3[0])
        Xp = ((Pp - O3) @ r) / W; Yp = ((Pp - O3) @ u) / R
        Nh = np.array(Nn, float) / math.sqrt(2)
        bul = A * (np.clip(4 * s * (1 - s), 0, 1) ** AL) * (np.clip(4 * tt * (1 - tt), 0, 1) ** AL)
        P = Pp + bul[..., None] * Nh
        rad = np.linalg.norm(P, axis=-1)
        rs = -KR * np.logaddexp(-rad / KR, -RCAP / KR)
        P = P * (rs / rad)[..., None]
        Pw = P @ Q.T
        Pw[..., 2] = ZF + KF * np.logaddexp(0, (Pw[..., 2] - ZF) / KF)
        base_i = sum(len(v) for v in verts)
        verts.append((Pw * UNIT_M).reshape(-1, 3))
        idx = np.arange((NG + 1) ** 2).reshape(NG + 1, NG + 1) + base_i
        a_, b_, c_, d_ = idx[:-1, :-1], idx[1:, :-1], idx[1:, 1:], idx[:-1, 1:]
        qd = np.stack([a_, b_, c_, d_], -1).reshape(-1, 4)
        # orient quads outward
        e1 = Pp[1, 0] - Pp[0, 0]; e2 = Pp[0, 1] - Pp[0, 0]
        if np.dot(np.cross(e1, e2), Nh) < 0: qd = qd[:, ::-1]
        quads.append(qd)
        U = (tx + (Xp - X0 + 0.5) / TX) / NC
        Vv = (ty + (Yp - Y0 + 0.5) / TY * (TY * PY) / th) / NR
        uvv = np.stack([U, Vv], -1).reshape(-1, 2)
        luv.append(uvv[(qd - base_i).ravel()].reshape(-1, 4, 2))
        checks.setdefault('corners', {})[str(Nn)] = [(round(x, 6), round(y, 6)) for x, y in R2]
    # ---------------- checks
    g0, *_ = grids[(1, -1, 0)]
    mism = sum(1 for (j, c), col in ch['grid'].items() if g0[j - Y0, c - X0] != (1 if col == 'D' else 0))
    checks['F0_vs_chart_n2_mismatches'] = mism
    checks['F0_chart_cells'] = len(ch['grid'])
    inside = np.zeros_like(g0, bool)
    for (j, c) in ch['grid']: inside[j - Y0, c - X0] = True
    checks['faces_grid_equal_F0_on_chart_cells'] = {str(N_): int(((gg[0] != g0) & inside).sum()) for N_, gg in grids.items()}
    # seams: stitch colours either side of every shared edge, at 40 points, half a stitch in from the seam
    def stitch_col(Nn, p):
        g, R2, O3, u, r = grids[Nn]
        x, y = np.dot(p - O3, r) / W, np.dot(p - O3, u) / R
        return int(g[int(round(y)) - Y0, int(round(x)) - X0])
    def piece(p):
        kk = rd.classify(tuple(p)); return kk[0] if kk else None
    tot = bad = badp = 0
    for f in fs:
        for g2 in fs:
            if f['N'] >= g2['N']: continue
            sh = [v for v in f['V'] if v in g2['V']]
            if len(sh) != 2: continue
            P0, P1 = [np.array([float(x) for x in v]) for v in sh]
            cf = np.mean([[float(x) for x in v] for v in f['V']], 0); cg = np.mean([[float(x) for x in v] for v in g2['V']], 0)
            for a in np.linspace(0.025, 0.975, 40):
                q = P0 + a * (P1 - P0)
                qf = q + (cf - q) / np.linalg.norm(cf - q) * 0.5 * W
                qg = q + (cg - q) / np.linalg.norm(cg - q) * 0.5 * W
                tot += 1
                bad += stitch_col(f['N'], qf) != stitch_col(g2['N'], qg)
                badp += piece(qf) != piece(qg)
    checks['seam_points'] = tot
    checks['seam_stitch_colour_differs'] = int(bad)
    checks['seam_exact_piece_differs_half_stitch_in'] = int(badp)
    checks['unit_cm'] = UNIT_M * 100
    checks['rows_per_10cm'] = 10 / (R * UNIT_M * 100)
    V = np.concatenate(verts)
    checks['size_cm'] = (np.ptp(V, 0) * 100).round(1).tolist()
    checks['floor_z_m'] = ZF * UNIT_M
    print(json.dumps(checks, indent=1))
    json.dump(checks, open(os.path.join(outdir, 'checks.json'), 'w'), indent=1)
    np.savez(os.path.join(outdir, 'mesh.npz'), V=V.astype(np.float32), Qd=np.concatenate(quads).astype(np.int32),
             UV=np.concatenate(luv).astype(np.float32), zfloor=np.float32(ZF * UNIT_M))
    rgba = np.concatenate([cols, np.ones(cols.shape[:2] + (1,), np.float32)], -1)
    np.save(os.path.join(outdir, 'col.npy'), rgba)
    np.save(os.path.join(outdir, 'hgt.npy'), hts)
    # preview of the F0 tile (sRGB) for checking against the chart
    from PIL import Image
    kf0 = [i for i, f in enumerate(fs) if f['N'] == (1, -1, 0)][0]
    ty, tx = kf0 // NC, kf0 % NC
    t0 = cols[ty * th:(ty + 1) * th, tx * tw:(tx + 1) * tw] * (0.55 + 0.45 * hts[ty * th:(ty + 1) * th, tx * tw:(tx + 1) * tw, None])
    srgb = np.where(t0 <= 0.0031308, 12.92 * t0, 1.055 * np.clip(t0, 0, None) ** (1 / 2.4) - 0.055)
    Image.fromarray((np.clip(srgb, 0, 1)[::-1] * 255).astype(np.uint8)).save(os.path.join(outdir, 'tile-F0.png'))


# ======================================================================= render (inside Blender)
def render(outdir, view, samples, res):
    import bpy, glob
    sys.path += glob.glob(os.path.expanduser('~/pyenv/lib/python3*/site-packages'))   # Blender's system Python has no numpy
    import numpy as np
    from mathutils import Vector
    D = np.load(os.path.join(outdir, 'mesh.npz'))
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = samples
    sc.cycles.use_denoising = True
    try: sc.cycles.denoiser = 'OPENIMAGEDENOISE'
    except Exception: pass
    sc.cycles.max_bounces = 6; sc.cycles.diffuse_bounces = 3; sc.cycles.sample_clamp_indirect = 3.0
    sc.render.resolution_x = sc.render.resolution_y = res; sc.render.resolution_percentage = 100
    sc.view_settings.view_transform = 'Standard'     # AgX desaturated the golds (rendered dark gold ~#bd9448)
    sc.view_settings.exposure = -0.9
    sc.render.image_settings.file_format = 'PNG'
    # mesh
    V, Qd, UV = D['V'], D['Qd'], D['UV']
    me = bpy.data.meshes.new('Cushion')
    me.vertices.add(len(V)); me.vertices.foreach_set('co', V.ravel())
    me.loops.add(Qd.size); me.loops.foreach_set('vertex_index', Qd.ravel())
    me.polygons.add(len(Qd)); me.polygons.foreach_set('loop_start', np.arange(0, Qd.size, 4, dtype=np.int32))
    me.update(calc_edges=True)
    uvl = me.uv_layers.new(name='UV'); uvl.data.foreach_set('uv', UV.ravel())
    me.polygons.foreach_set('use_smooth', np.ones(len(Qd), bool))
    me.validate(); me.update()
    ob = bpy.data.objects.new('Cushion', me); sc.collection.objects.link(ob)
    # textures
    def img(name, arr, noncolor):
        h, w = arr.shape[:2]
        im = bpy.data.images.new(name, w, h, alpha=True, float_buffer=True)
        if arr.ndim == 2: arr = np.repeat(arr[..., None], 4, -1); arr[..., 3] = 1
        im.colorspace_settings.name = 'Non-Color' if noncolor else 'Linear Rec.709'   # before the pixels: a change reloads
        im.pixels.foreach_set(arr.astype(np.float32).ravel())
        im.update()
        px = np.empty(w * h * 4, np.float32); im.pixels.foreach_get(px)
        print('IMAGE', name, w, h, 'mean', float(px[0::4].mean()), float(px[1::4].mean()), im.colorspace_settings.name)
        return im
    col = np.load(os.path.join(outdir, 'col.npy')); hg = np.load(os.path.join(outdir, 'hgt.npy'))
    mat = bpy.data.materials.new('Yarn'); mat.use_nodes = True; nt = mat.node_tree; N = nt.nodes; L = nt.links
    bs = N['Principled BSDF']
    for k, v in {'Roughness': 0.88, 'Sheen Weight': 0.3, 'Sheen Roughness': 0.45, 'Specular IOR Level': 0.25}.items():
        try: bs.inputs[k].default_value = v
        except Exception as ex: print('skip', k, ex)
    try: bs.inputs['Sheen Tint'].default_value = (1.0, 0.95, 0.82, 1)
    except Exception: pass
    tc = N.new('ShaderNodeTexImage'); tc.image = img('col', col, False); tc.interpolation = 'Linear'
    th_ = N.new('ShaderNodeTexImage'); th_.image = img('hgt', hg, True); th_.interpolation = 'Cubic'
    L.new(tc.outputs['Color'], bs.inputs['Base Color'])
    dn = N.new('ShaderNodeDisplacement'); dn.inputs['Midlevel'].default_value = 0.0; dn.inputs['Scale'].default_value = 0.0014
    L.new(th_.outputs['Color'], dn.inputs['Height'])
    L.new(dn.outputs['Displacement'], N['Material Output'].inputs['Displacement'])
    for setter in (lambda: setattr(mat, 'displacement_method', 'BOTH'), lambda: setattr(mat.cycles, 'displacement_method', 'BOTH')):
        try: setter(); print('DISPLACEMENT BOTH set'); break
        except Exception as ex: print('displacement setter failed', ex)
    ob.data.materials.append(mat)
    # floor + world (neutral)
    zf = float(D['zfloor'])
    bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, zf)); fl = bpy.context.object
    fm = bpy.data.materials.new('Floor'); fm.use_nodes = True
    fb = fm.node_tree.nodes['Principled BSDF']; fb.inputs['Base Color'].default_value = (0.42, 0.42, 0.41, 1)
    fb.inputs['Roughness'].default_value = 0.9; fl.data.materials.append(fm)
    wo = bpy.data.worlds.new('W'); wo.use_nodes = True; sc.world = wo
    bg = wo.node_tree.nodes['Background']; bg.inputs['Color'].default_value = (0.42, 0.42, 0.41, 1); bg.inputs['Strength'].default_value = 0.25
    def area(name, az, el, dist, size, power, color=(1, 1, 1)):
        ld = bpy.data.lights.new(name, 'AREA'); ld.shape = 'DISK'; ld.size = size; ld.energy = power; ld.color = color
        lo = bpy.data.objects.new(name, ld); sc.collection.objects.link(lo)
        a, e = math.radians(az), math.radians(el)
        p = Vector((math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e))) * dist
        lo.location = p; lo.rotation_euler = (-p).to_track_quat('-Z', 'Y').to_euler()
    # camera
    az, el = {'front': (-125, 20), 'side': (35, 40)}[view]       # camera azimuth (deg from +x), elevation
    for nm, laz, lel, ds, sz, pw in (('Key', az + 45, 50, 2.0, 1.6, 140), ('Fill', az - 70, 18, 2.2, 2.0, 45),
                                      ('Rim', az + 180, 35, 2.0, 1.2, 80)):
        area(nm, laz, lel, ds, sz, pw, (1.0, 0.97, 0.92) if nm == 'Key' else (0.95, 0.97, 1.0))
    cam = bpy.data.cameras.new('Cam'); cam.lens = 85; cam.sensor_width = 36
    co = bpy.data.objects.new('Cam', cam); sc.collection.objects.link(co); sc.camera = co
    tgt = Vector((0, 0, -0.005)); dist = 1.15
    a, e = math.radians(az), math.radians(el)
    co.location = tgt + Vector((math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e))) * dist
    co.rotation_euler = (tgt - co.location).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = os.path.join(outdir, f'view-{view}.png')
    bpy.ops.render.render(write_still=True)
    print('RENDERED', sc.render.filepath)


# ======================================================================= sheet
def sheet(outdir, out):
    from PIL import Image
    a = Image.open(os.path.join(outdir, 'view-front.png')).convert('RGB')
    b = Image.open(os.path.join(outdir, 'view-side.png')).convert('RGB')
    W_, H_ = a.size
    ct = int(H_ * 0.065)                              # crop the darker far floor at the top
    a, b = a.crop((0, ct, W_, H_)), b.crop((0, ct, W_, H_)); H_ -= ct
    S = Image.new('RGB', (2 * W_, H_))
    S.paste(a, (0, 0)); S.paste(b, (W_, 0))
    lg = Image.open(os.path.expanduser(os.environ.get('LOGO', '~/work/dicto-logo.png'))).convert('RGBA')
    sz = int(H_ * 0.075); lg = lg.resize((sz, sz), Image.LANCZOS)
    S.paste(lg, (2 * W_ - sz - int(sz * 0.3), H_ - sz - int(sz * 0.3)), lg)
    S.save(out)
    print('SHEET', out)


if __name__ == '__main__':
    if '--' in sys.argv:
        a = sys.argv[sys.argv.index('--') + 1:]
        render(a[0], a[1], int(a[2]), int(a[3]))
    elif sys.argv[1] == 'prep':
        prep(sys.argv[2])
    elif sys.argv[1] == 'sheet':
        sheet(sys.argv[2], sys.argv[3])
