# The infinite core as one picture (DICTO): each zoom (one turn, phi^3 closer) framed inside the centre of the previous one.
from PIL import Image, ImageDraw
R = 'renders/polar-turns-'
ims = [Image.open(R + s + '.png').convert('RGB') for s in ('cut2', 'cut3', 'cut4', 'cut5')]
def nest(level, size):
    im = ims[level].resize((size, size), Image.LANCZOS)
    if level + 1 < len(ims):
        k = int(size * 0.40); inner = nest(level + 1, k); o = (size - k) // 2
        im.paste(inner, (o, o)); d = ImageDraw.Draw(im); w = max(2, size // 220)
        d.rectangle([o - w, o - w, o + k + w - 1, o + k + w - 1], outline=(212, 160, 23), width=w)
    return im
out = nest(0, 1600); out.save(R + 'nested.png'); out.convert('RGB').save(R + 'nested.jpg', quality=90); print(out.size)
