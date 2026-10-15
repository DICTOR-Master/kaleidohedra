# Movie of the window figure (DICTO: "make a movie of the window figure"). Reads data/fig-window.json (exact plane lattice points,
# drawn in float). 1920x1080, 30 fps, 540 frames (18 s): (1) a view sweeps along the axis and the chain ticks appear for points in
# the canonical strip [0, L); (2) zoom out, the build's silent copies and the centre appear; (3) the strip edge slides down from L to
# t_c (the ring self-clash); (4) the fork at 12.81 is left outside the narrower strip and its tick goes.
import json, subprocess, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt, imageio_ffmpeg
D = json.load(open('data/fig-window.json')); P = np.array(D['points']); S = np.array(D['silent']); tc, L = D['tc'], D['L']; fh, ft = D['fork']
bg, fg, mute, gold, gold2, red, vio = '#f4f1ea', '#2b2620', '#6d6556', '#f3d9a0', '#e9b949', '#c62828', '#7b1fa2'
W, H, fps, n = 1920, 1080, 30, 540
ff = subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}', '-r', str(fps), '-i', '-',
                       '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '/tmp/dicto-chorus-window.mp4'], stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
fig = plt.figure(figsize=(W / 100, H / 100), dpi=100, facecolor=bg); ax = fig.add_axes((0.06, 0.12, 0.9, 0.68))
ease = lambda x: (lambda y: y * y * (3 - 2 * y))(min(1, max(0, x)))
for f in range(n):
    if f < 180:   # sweep
        c = -16 + 32 * ease(f / 170); x0, x1 = c - 10, c + 10; edge = L; reveal = c + 10; showS = 0
        cap = 'Lattice points of the axis plane (exact). Those inside the strip [0, W) project to the Fibonacci chain below.'
    elif f < 270:  # zoom out, build appears
        k = ease((f - 180) / 60); x0, x1 = 6 - 32 * k, 26; x0 = -26 * k + (6) * (1 - k); x1 = 26; edge = L; reveal = 99; showS = ease((f - 200) / 50)
        cap = 'Circled: the copies the radius-10 build silences, exactly the chain points there. Star: the central copy.'
    elif f < 420:  # strip edge slides to t_c
        x0, x1 = -26, 26; k = ease((f - 285) / 110); edge = L + (tc - L) * k; reveal = 99; showS = 1
        cap = f'The ring clashes with itself only below t_c = {tc:.4f}: the narrower window [0, t_c). Canonical W = {L:.4f}.'
    else:          # the fork
        x0, x1 = -26, 26; edge = tc; reveal = 99; showS = 1
        cap = 'Below height 12.81 both windows pick the same points. At 12.81 they first disagree: the fork (diamond).'
    ax.clear(); ax.set_facecolor(bg)
    ax.axhspan(0, L, color=gold, zorder=0); ax.axhspan(0, edge, color=gold2, alpha=0.6, zorder=0)
    ax.axvspan(-10, 10, color='#000', alpha=0.035, zorder=0)
    ax.scatter(P[:, 0], P[:, 1], s=34, c=fg, zorder=2)
    if showS > 0:
        ax.scatter(S[:, 0], S[:, 1], s=260, facecolors='none', edgecolors=red, linewidths=2.2, alpha=showS, zorder=3)
        ax.scatter([0], [0], marker='*', s=520, c=red, alpha=showS, zorder=4)
    inw = P[(P[:, 1] >= -1e-9) & (P[:, 1] < edge) & (P[:, 0] <= reveal)]
    for h in inw[:, 0]: ax.plot([h, h], [-0.44, -0.28], c=fg, lw=2)
    ax.axhline(-0.36, c=fg, lw=1)
    if f >= 270:
        a = 1 if f >= 420 else ease((f - 380) / 40)
        ax.scatter([fh], [ft], marker='D', s=220, facecolors='none', edgecolors=vio, linewidths=2.6, alpha=a, zorder=5)
        if f >= 420 and not (ft < edge):
            ax.plot([fh, fh], [-0.44, -0.28], c=vio, lw=2, ls=':', alpha=0.9)
            ax.annotate('the fork, height 12.81', (fh, ft), (fh + 1.2, 1.75), color=vio, fontsize=17, arrowprops=dict(arrowstyle='-', color=vio, lw=1.5))
    ax.set_xlim(x0, x1); ax.set_ylim(-0.5, 2.2)
    ax.set_xlabel('height along the five-fold axis', fontsize=16, color=fg); ax.set_ylabel('distance from the axis, t', fontsize=16, color=fg)
    ax.tick_params(labelsize=13, colors=fg); [s_.set_color(mute) for s_ in ax.spines.values()]
    ax.text(x0 + 0.3, -0.33, 'chain', fontsize=13, color=fg, va='bottom')
    fig.texts.clear()
    fig.text(0.06, 0.93, 'DICTO Ogdoecontahedron five-fold chorus: the Fibonacci spine', fontsize=28, color=fg, va='top')
    fig.text(0.06, 0.875, cap, fontsize=18, color=mute, va='top')
    fig.text(0.06, 0.04, 'Grey band: heights inside the radius-10 build. Pale strip [0, W): canonical window; darker strip: the current window.', fontsize=14, color=mute)
    fig.text(0.96, 0.04, 'DICTO · dictospheres.com', fontsize=15, color=mute, ha='right')
    fig.canvas.draw(); ff.stdin.write(np.asarray(fig.canvas.buffer_rgba()).tobytes())
ff.stdin.close(); ff.wait(); print('movie done')
