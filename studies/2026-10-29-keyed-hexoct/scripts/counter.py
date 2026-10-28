# Keyed HexOct, step 3 (2026-10-29): a keyed layer that counts. Every HexOct tile of one layer touches its four lattice-axis
# neighbours (+-1,0), (0,+-1) through faces of positive area (step 1, contacts.py, every context and weight checked), so keys on
# those four faces (the other faces blank) make the layer a Wang tiling of the square grid (Wang 1961).
# Tile set (4 keyed tiles): a tile holds a bit b; its (0,-1) face reads the bit below, its (+1,0) face takes the carry from the
# right, its (-1,0) face gives the carry to the left, its (0,+1) face shows its bit to the tile above:
#     below = b_old, carry_in = c, bit = b_old xor c, carry_out = b_old and c.
# Boundary: row v=0 is all 0; the right edge feeds carry 1 into every row. Exhaustive backtracking over a W x H window counts
# every filling that obeys all keys: exactly one is expected, and row v must spell the number v in binary.
import itertools, sys
TILES = [dict(below=b, cin=c, bit=b ^ c, cout=b & c) for b in (0, 1) for c in (0, 1)]

def fillings(W, H):
    sols, grid = [], {}
    cells = [(v, u) for v in range(1, H) for u in range(W - 1, -1, -1)]   # row by row, right to left
    def ok(v, u, t):
        below = 0 if v == 1 else grid[(v - 1, u)]['bit']
        cin = 1 if u == W - 1 else grid[(v, u + 1)]['cout']
        return t['below'] == below and t['cin'] == cin
    def go(i):
        if i == len(cells):
            sols.append({k: t['bit'] for k, t in grid.items()}); return
        v, u = cells[i]
        for t in TILES:
            if ok(v, u, t):
                grid[(v, u)] = t; go(i + 1); del grid[(v, u)]
    go(0)
    return sols

if __name__ == '__main__':
    for W, H in ((3, 8), (4, 16), (5, 20)):
        sols = fillings(W, H)
        good = all(int(''.join(str(s[(v, u)]) for u in range(W)), 2) == v % 2 ** W for s in sols for v in range(1, H))
        print(f'window {W} x {H}: {len(sols)} filling(s); rows count 1..{H - 1} in binary: {good}')
        if (W, H) == (4, 16):
            for v in range(H - 1, 0, -1):
                print(f'   row {v:2d}: ' + ''.join(str(sols[0][(v, u)]) for u in range(W)))
