# Refresh the five-cover comparison sheet: the Platonic cover and its back mark replace the fifth column of the existing sheet
# (columns: Space-Fillers, Golden Cycle, Star Cores, Permutohedron Paradigm, Platonic Solids; back marks below).
# Run: python compare.py OLD_SHEET.png FRONT.png BACKMARK.png OUT.png
import sys
import numpy as np
from PIL import Image
old, front, mark, out = sys.argv[1:5]
S = Image.open(old).convert('RGB'); GROUND = (20, 15, 11)
X0, X1, Y0, Y1, MY0, MY1 = 2928, 3635, 20, 1020, 1040, 1220      # the fifth cover slot and its mark slot in the sheet
S.paste(Image.open(front).convert('RGB').resize((X1 - X0, Y1 - Y0), Image.LANCZOS), (X0, Y0))
S.paste(Image.new('RGB', (X1 - X0, MY1 - MY0), GROUND), (X0, MY0))
m = Image.open(mark).convert('RGBA'); k = min(0.88 * (X1 - X0) / m.width, 0.70 * (MY1 - MY0) / m.height)
m = m.resize((int(m.width * k), int(m.height * k)), Image.LANCZOS)
S.paste(m, (X0 + (X1 - X0 - m.width) // 2, MY0 + (MY1 - MY0 - m.height) // 2), m)
S.save(out); print('compare sheet saved', out, S.size)
