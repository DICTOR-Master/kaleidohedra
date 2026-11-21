"""Control: the floating-point regime map of study 2026-11-09-b1-walls, redone on a 0.01 grid with this study's chain (12 steps).
Usage: python map.py <cube|dodeca> <from> <to>"""
import sys
import fw
kind, a, b = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
n = int(round((b - a) / 0.01)); done = 0
for t in range(n + 1):
    s = round(a + 0.01 * t, 2)
    try:
        cl, cnt, ty = fw.float_closure(kind, s, 12)
        done += 1; print(f'{kind} s={s:.2f} ' + (f'period {cl[1] - cl[0]} entered at step {cl[0]}' if cl else 'NO closure within 12 steps') + f'  corners {cnt}', flush=True)
    except AssertionError as e:
        print(f'{kind} s={s:.2f} floating point degenerate ({e})', flush=True)
print('FINAL ok' if done == n + 1 else f'FINAL FAIL: {n + 1 - done} depths degenerate in floating point')
