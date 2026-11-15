# The five-cover comparison sheet, built fresh: Space-Fillers, Golden Cycle, Star Cores, Permutohedron Paradigm (exploded),
# Platonic Solids, in a row on the cover ground, each scaled to the same height.   Run: python compare.py OUT.png FRONT1 ... FRONT5
import sys
from PIL import Image
out, fronts = sys.argv[1], sys.argv[2:]; assert len(fronts) == 5
HT, PAD, GROUND = 1100, 24, (20, 15, 11)
ims = [Image.open(f).convert('RGB') for f in fronts]; ims = [im.resize((round(im.width * HT / im.height), HT), Image.LANCZOS) for im in ims]
S = Image.new('RGB', (sum(im.width for im in ims) + PAD * 6, HT + 2 * PAD), (40, 34, 28)); x = PAD
for im in ims: S.paste(im, (x, PAD)); x += im.width + PAD
S.save(out); print('compare sheet saved', out, S.size)
