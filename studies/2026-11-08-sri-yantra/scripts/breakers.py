"""Figure "The condition breakers" for #103 (DICTO 15 Nov 2026: "maybe the yantra diagrams could be used to construct the nearby
inadmissible condition breakers"). Each breaker is drawn by overlay.py's plate() (the same plate as every overlay figure of the paper:
same circle of diameter 1000 px, line weights, fonts, colours and layout): the breaker dotted in its colour over the true yantra in
solid grey (the DICTO Yantra, Theorem 9, for the DICTO Yantra conditions; Kulaichev's yantra, Theorem 10, for Kulaichev's), with only
red marks added for what breaks. Coordinates and defect sizes come from ../data/breakers.json (breakers_certify.py: certified balls);
every number in a note is read from there and the script stops if a note is not borne out by the data.
The six plates are set at one common scale (one diameter = the same length in every panel) in two rows.
usage: python3 breakers.py <out.png>      (prints the checks and a FINAL line)"""
import json, math, os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
import overlay
from overlay import plate, font, BOLD, FONT, INK, BG, RED

HERE = os.path.dirname(os.path.abspath(__file__)); DAT = os.path.join(HERE, '..', 'data')
E = json.load(open(os.path.join(DAT, 'breakers.json')))
F = lambda k: {kk: float(x) for kk, x in E[k]['measures'].items()}


def coords(k):
    g = lambda d: {int(i): float(x) for i, x in d.items()}
    return lambda: (g(E[k]['b']), g(E[k]['w']), g(E[k]['apex']))


def red_tri(i, k, width=5):
    """t_i of breaker k redrawn solid red"""
    b, w, a = coords(k)()
    def f(dr, X, Yd, s):
        L, R_, A = (X(-w[i]), Yd(b[i])), (X(w[i]), Yd(b[i])), (X(0), Yd(a[i]))
        dr.line([L, R_], fill=RED, width=width * s); dr.line([L, A], fill=RED, width=width * s); dr.line([R_, A], fill=RED, width=width * s)
    return f


def ring(x, d, r, width=4):
    def f(dr, X, Yd, s):
        R_ = r * 1000 * s; dr.ellipse([X(x) - R_, Yd(d) - R_, X(x) + R_, Yd(d) + R_], outline=RED, width=width * s)
    return f


def dot(x, d, r=7):
    def f(dr, X, Yd, s):
        dr.ellipse([X(x) - r * s, Yd(d) - r * s, X(x) + r * s, Yd(d) + r * s], fill=RED)
    return f


def cross(x, d, r=12, width=4):
    def f(dr, X, Yd, s):
        dr.line([X(x) - r * s, Yd(d) - r * s, X(x) + r * s, Yd(d) + r * s], fill=RED, width=width * s)
        dr.line([X(x) - r * s, Yd(d) + r * s, X(x) + r * s, Yd(d) - r * s], fill=RED, width=width * s)
    return f


def circ(d, r, width=4):
    def f(dr, X, Yd, s):
        dr.ellipse([X(-r), Yd(d - r), X(r), Yd(d + r)], outline=RED, width=width * s)
    return f


def seq(*fs):
    def f(dr, X, Yd, s):
        for g in fs: g(dr, X, Yd, s)
    return f


def bindu_tri(k, width=5):
    """the bindu triangle (t1's legs down to t5's base) outlined in red"""
    b, w, a = coords(k)()
    hw = w[1] * (a[1] - b[5]) / (a[1] - b[1])
    def f(dr, X, Yd, s):
        P = [(X(-hw), Yd(b[5])), (X(hw), Yd(b[5])), (X(0), Yd(a[1]))]
        dr.line(P + [P[0]], fill=RED, width=width * s, joint='curve')
    return f


ok = True
def need(c, why):
    global ok
    if not c: ok = False; print('NOTE NOT TRUE:', why)


def panels():
    P = []
    # ---- DICTO Yantra conditions (u v = 2/phi^3, (b), (c), (d)); grey: the DICTO Yantra (Theorem 9)
    k = 'D057120'; m = F(k); b, w, a = coords(k)()
    need(E[k]['fails'] == ['b5 < 1/2 (centre below the bindu base)'] and m['b5_minus_half'] > 0 and abs(m['excentre_minus_half']) < 1e-30, k)
    P.append((k, ('The excentre, u = 0.57120', coords(k), (0, 105, 148), True), 'GF1',
              [f"the circle's centre is the EXCENTRE of the bindu triangle (red circle), {m['b5_minus_half']:.4f} above its base, "
               f"outside it; the incentre (x) lies {m['incentre_minus_half']:.4f} below the centre. Every other condition holds"],
              seq(bindu_tri(k), circ(0.5, m['exradius']), dot(0, 0.5), cross(0, 0.5 + m['incentre_minus_half']))))
    k = 'CA0'; m = F(k); b, w, a = coords(k)()
    need(E[k]['fails'] == [] and abs(m['incentre_minus_half'] + 0.058132) < 1e-6, k)
    P.append((k, ('Cleo-Antonius, u = 3 − √5', coords(k), (184, 150, 46), True), 'GF1',
              [f"the undistorted Cleo-Antonius; bindu not centred: its incircle (red) is centred {-m['incentre_minus_half']:.4f} of the diameter above the circle's "
               f"centre (dot); (d) fails, every other condition holds"],
              seq(circ(0.5 + m['incentre_minus_half'], m['inradius']), cross(0, 0.5 + m['incentre_minus_half']), dot(0, 0.5),
                  lambda dr, X, Yd, s, o=m['incentre_minus_half']: dr.line([X(0), Yd(0.5), X(0), Yd(0.5 + o)], fill=RED, width=3 * s))))
    # ---- Kulaichev's conditions ((a) equal great triangles, (b), (c), (d)); grey: Kulaichev's yantra (Theorem 10)
    k = 'Rh345'; m = F(k)
    need(E[k]['fails'] == [] and abs(abs(m['incentre_minus_half']) - 2.36e-5) < 0.01e-5, k)
    P.append((k, ('Rh345, the 3-4-5 rhombus, u = 3/4', coords(k), (160, 82, 45), True), 'KRP',
              [f"bindu off centre by {abs(m['incentre_minus_half']) * 1e5:.2f}·10⁻⁵ of the diameter (ringed; too small to see); "
               "(d) fails, every other condition holds"],
              seq(ring(0, 0.5, 0.03), dot(0, 0.5))))
    inv = ['b4 < b5', 'b6 < b7', 'w5 > 0', 'w6 > 0', 'apex t4 below its base', 'corner t4 inside the disc', 'corner t6 inside the disc']
    for k, lab, col, base in (('D067176', 'u = 0.67176', (85, 107, 47), 'GF1'), ('D088628', 'u = 0.88628', (72, 61, 139), 'GF1'),
                              ('K066866', 'u = 0.66866 (Kulaichev)', (199, 21, 133), 'KRP')):
        m = F(k); b, w, a = coords(k)(); f = E[k]['fails']
        need(f[:7] == inv and m['apex4_minus_b4'] < 0 and m['w5'] < 0 and m['w6'] < 0 and m['corner4_outside'] > 0 and m['corner6_outside'] > 0, k)
        notes = [f"t4 turned over (red): its apex {-m['apex4_minus_b4']:.3f} above its base, which lies at depth {b[4]:.3f}; "
                 f"b4 > b5 by {m['b4_minus_b5']:.3f}, b6 > b7 by {m['b6_minus_b7']:.3f}",
                 f"w5 = −{-m['w5']:.4f}, w6 = −{-m['w6']:.4f} (t5, t6 red); corners of t4, t6 outside the circle (ringed) by "
                 f"{m['corner4_outside']:.3f}, {m['corner6_outside']:.3f}"]
        if 'b5 < 1/2 (centre below the bindu base)' in f:
            need(m['b5_minus_half'] > 0 and abs(m['excentre_minus_half']) < 1e-30, k + ' excentre')
            notes.append(f"the circle's centre is also the excentre of the bindu triangle (b5 > 1/2 by {m['b5_minus_half']:.4f})")
        else:
            need(abs(m['incentre_minus_half']) < 1e-30, k + ' incentre')
        rings = [ring(sx * w[i], b[i], 0.03) for i in (4, 6) for sx in (1, -1)]
        P.append((k, ('t4 turned over, ' + lab, coords(k), col, True), base, notes,
                  seq(red_tri(4, k), red_tri(5, k), red_tri(6, k), *rings)))
    return P


def main(out):
    ims = []
    for k, entry, base, notes, extra in panels():
        im = plate(k, notes, [], None, base=base, entry=entry, extra=extra, ret=True); ims.append(im)
        print('plate', k, im.size, '|', ' | '.join(notes))
    rows = [ims[:3], ims[3:]]
    gap = 30; head = 150
    W = max(sum(i.width for i in r) + gap * (len(r) - 1) for r in rows) + 2 * gap
    Hs = [max(i.height for i in r) for r in rows]
    G = Image.new('RGB', (W, head + sum(Hs) + gap * len(rows)), BG); dr = ImageDraw.Draw(G)
    dr.text((gap, 40), 'The condition breakers', font=font(BOLD, 80), fill=INK)
    dr.text((W - gap, 70), 'DICTO · dictospheres.com', font=font(FONT, 36), fill=(150, 110, 20), anchor='ra')
    y = head
    for r, h in zip(rows, Hs):
        x = (W - (sum(i.width for i in r) + gap * (len(r) - 1))) // 2
        for i in r:
            G.paste(i, (x, y)); x += i.width + gap
        y += h + gap
    G.save(out); print('wrote', out, G.size)
    print('FINAL ok' if ok else 'FINAL FAIL: a note is not true')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'figures', 'condition-breakers.png'))
