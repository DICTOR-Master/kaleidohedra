# Step 23 movie: a slab sweeping up the five-fold axis of the exact radius-10 chorus; vacancies circled. Float readout of exact sites.
import json, subprocess, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt, imageio_ffmpeg
D = json.load(open('data/chorus-exact-r10.json')); K = np.array(D['sites']); S = np.array(D['silenced']); R = D['RAD']
a5, e1, e2 = (np.array(D[k]) for k in ('a5', 'e1', 'e2')); th0 = D['th0']
P = lambda X: (X @ e1, X @ e2, X @ a5)
kx, ky, kz = P(K); sx, sy, sz = P(S); w = ((np.arctan2(ky, kx) - th0) % (2 * np.pi)) // (2 * np.pi / 5)
bg, fg, mute = '#f4f1ea', '#2b2620', '#6d6556'; cols = ['#e07a2e', '#3b8ea5', '#7a5aa6', '#4f9a4a', '#c0455a']
W, H, fps, n = 1080, 1080, 30, 360; half = 0.6
ff = subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}', '-r', str(fps), '-i', '-',
                       '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '/tmp/chorus-boundary.mp4'], stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
fig = plt.figure(figsize=(W / 100, H / 100), dpi=100, facecolor=bg); ax = fig.add_axes((0, 0, 1, 1)); 
for f in range(n):
    zc = -R + 2 * R * (0.5 - 0.5 * np.cos(np.pi * f / (n - 1)))
    ax.clear(); ax.set_facecolor(bg); ax.set_xlim(-R - 1.4, R + 1.4); ax.set_ylim(-R - 0.6, R + 2.2); ax.set_aspect('equal'); ax.axis('off')
    for j in range(5):
        t = th0 + j * 2 * np.pi / 5; ax.plot([0, R * np.cos(t)], [0, R * np.sin(t)], color=mute, lw=.8, ls='--', alpha=.6)
        mk = (np.abs(kz - zc) < half) & (w == j); a = 1 - np.abs(kz[mk] - zc) / half
        ax.scatter(kx[mk], ky[mk], s=90, c=cols[j], alpha=None, lw=0) if mk.any() else None
    ms = np.abs(sz - zc) < half
    ax.scatter(sx[ms], sy[ms], s=170, facecolors='none', edgecolors=fg, lw=2)
    ax.text(.03, .965, 'DICTO Ogdoecontahedron · five-fold chorus, exact to radius 10', transform=ax.transAxes, color=fg, fontsize=17, va='top')
    ax.text(.03, .925, f'slab at height {zc:+.2f} along the five-fold axis · five voices in colour · silent copies circled', transform=ax.transAxes, color=mute, fontsize=12.5, va='top')
    ax.text(.97, .03, 'DICTO · dictospheres.com', transform=ax.transAxes, color=mute, fontsize=12, ha='right')
    fig.canvas.draw(); ff.stdin.write(np.asarray(fig.canvas.buffer_rgba()).tobytes())
ff.stdin.close(); ff.wait(); print('movie done')
