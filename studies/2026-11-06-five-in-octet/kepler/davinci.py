"""DICTO's geode / da Vinci plate style (11-06: "that's the look but more shells shaded in perhaps, and the others in same style").
Parchment with a soft vignette; sepia skeleton lines (near heavy, hidden faint dashed); shells as tinted glass (back faces faint, front
faces shaded), the core solid; construction marks; italic caption and a faint DICTO mark. Views down symmetry axes."""
import math, numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.spatial import ConvexHull
PARCH = (240, 230, 208); SEPIA = (91, 58, 30)
def look(dirv, upv):
    z = np.array(dirv, float); z /= np.linalg.norm(z); u = np.array(upv, float); u = u - (u @ z) * z; u /= np.linalg.norm(u)
    return np.array([np.cross(u, z), u, z])
class Plate:
    def __init__(self, R, W=2600, scale=1.0, centre=(0, 0, 0), cy=0.48):
        self.R, self.W, self.sc, self.c, self.cy = R, W, scale, np.array(centre, float), cy
        y, x = np.mgrid[0:W, 0:W]; vig = 1 - 0.40 * (np.hypot(x - W / 2, y - W / 2) / W) ** 2
        self.img = Image.fromarray(np.clip(np.array(Image.new('RGB', (W, W), PARCH)) * vig[..., None], 0, 255).astype(np.uint8))
        self.d = ImageDraw.Draw(self.img, 'RGBA'); self.view = R.T @ np.array([0, 0, 1.0])
        self.light = R.T @ np.array([-0.4, 0.6, 0.7]); self.light /= np.linalg.norm(self.light)
    def P(self, p): q = self.R @ (np.asarray(p) - self.c); return (self.W / 2 + q[0] * self.sc, self.W * self.cy - q[1] * self.sc)
    def z(self, p): return (self.R @ (np.asarray(p) - self.c))[2]
    @staticmethod
    def faces(V):
        h = ConvexHull(V); F = {}
        for eq, sp in zip(h.equations, h.simplices): F.setdefault(tuple(np.round(eq, 6)), set()).update(sp)
        out = []
        for k, idx in F.items():
            idx = list(idx); n = np.array(k[:3]); c = V[idx].mean(0); u = V[idx[0]] - c; w = np.cross(n, u)
            out.append((n, sorted(idx, key=lambda i: math.atan2((V[i] - c) @ w, (V[i] - c) @ u))))
        return out
    def dashed(self, p, q, col, w, dash=14):
        L = math.dist(p, q); n = max(1, int(L / dash))
        for k in range(0, n, 2):
            a = k / n; b = min(1, (k + 1) / n)
            self.d.line([(p[0] + (q[0] - p[0]) * a, p[1] + (q[1] - p[1]) * a), (p[0] + (q[0] - p[0]) * b, p[1] + (q[1] - p[1]) * b)], fill=col, width=w)
    def skeleton(self, V, w=5, alpha=220, hidden=True):
        E = {}
        for n, idx in self.faces(V):
            for a, b in zip(idx, idx[1:] + idx[:1]): E.setdefault(tuple(sorted((a, b))), []).append(n)
        for (a, b), ns in E.items():
            vis = any(n @ self.view > 0 for n in ns)
            if vis: self.d.line([self.P(V[a]), self.P(V[b])], fill=SEPIA + (alpha,), width=w)
            elif hidden: self.dashed(self.P(V[a]), self.P(V[b]), SEPIA + (int(alpha * 0.35),), max(2, w // 2))
    def glass(self, V, rgb, a_front=70, a_back=25, edge=150, w=3, which='both'):
        fs = sorted(self.faces(V), key=lambda f: self.z(V[f[1]].mean(0)))
        for n, idx in fs:
            front = n @ self.view > 0
            if (which == 'back' and front) or (which == 'front' and not front): continue
            b = 0.6 + 0.4 * max(0, n @ self.light) if front else 0.8
            pts = [self.P(V[i]) for i in idx]
            self.d.polygon(pts, fill=tuple(int(c * b) for c in rgb) + ((a_front if front else a_back),))
            if front: self.d.line(pts + [pts[0]], fill=SEPIA + (edge,), width=w)
    def solid(self, V, rgb, w=3):
        for n, idx in sorted(self.faces(V), key=lambda f: self.z(V[f[1]].mean(0))):
            if n @ self.view <= 0: continue
            b = 0.55 + 0.45 * max(0, n @ self.light); pts = [self.P(V[i]) for i in idx]
            self.d.polygon(pts, fill=tuple(int(c * b) for c in rgb) + (255,)); self.d.line(pts + [pts[0]], fill=SEPIA + (230,), width=w)
    def ring(self, p, r=13, col=SEPIA): q = self.P(p); self.d.ellipse([q[0] - r, q[1] - r, q[0] + r, q[1] + r], outline=col + (230,), width=4)
    def cross(self, p, r=15, col=(150, 40, 30)):
        q = self.P(p); self.d.line([(q[0] - r, q[1] - r), (q[0] + r, q[1] + r)], fill=col + (235,), width=4); self.d.line([(q[0] - r, q[1] + r), (q[0] + r, q[1] - r)], fill=col + (235,), width=4)
    def save(self, out, caption):
        img = self.img.resize((self.W // 2, self.W // 2), Image.LANCZOS); d = ImageDraw.Draw(img)
        try: F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf', 26)
        except Exception: F = None
        d.text((self.W // 4, self.W // 2 - 52), caption, fill=SEPIA, font=F, anchor='mm')
        try:
            logo = Image.open('/home/dicto/k-research/papers/dicto-logo.png').convert('RGBA').resize((70, 70)); logo.putalpha(logo.split()[3].point(lambda a: int(a * 0.5)))
            img.paste(logo, (self.W // 2 - 100, self.W // 2 - 100), logo)
        except Exception: pass
        img.save(out)
