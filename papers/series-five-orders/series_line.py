"""The series line of THE FIVE ORDERS OF SPACE, e.g. "Book Two · Earth 地 · The Five Orders of Space",
in the ring's colour (DICTO's element colours, agreed 22 October 2026). Place it under a book's title.

    from series_line import series_line      # sys.path.insert(0, '<papers>/series-five-orders')
    series_line(2)            -> HTML <p> for Book Two (Earth)
    series_line(1, 'II')      -> "Book One, II · Earth 地 · ..." (Quanta of Space II, the DICTOnary)
    python3 series_line.py 7  -> prints the HTML for Book Seven

The swatch carries the exact ring colour; the text uses the same colour, except Wind, whose yellow is
darkened for the text only so that it reads on white paper.
"""
import sys

SERIES = 'The Five Orders of Space'
WORDS = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven']
#        ring,   kanji, swatch,    text colour
RINGS = {'Earth': ('地', '#488e48', '#488e48'),
         'Water': ('水', '#3a70cd', '#3a70cd'),
         'Fire':  ('火', '#cd3e28', '#cd3e28'),
         'Wind':  ('風', '#e8c852', '#a8891f'),
         'Void':  ('空', '#8a5cc4', '#8a5cc4')}
RING_OF = {1: 'Earth', 2: 'Earth', 3: 'Water', 4: 'Water', 5: 'Water', 6: 'Fire', 7: 'Fire',
           8: 'Wind', 9: 'Void', 10: 'Void', 11: 'Void'}


def series_text(book, part=None):
    ring = RING_OF[book]
    head = f'Book {WORDS[book]}' + (f', {part}' if part else '')
    return f'{head} · {ring} {RINGS[ring][0]} · {SERIES}'


def series_line(book, part=None):
    ring = RING_OF[book]
    _, swatch, ink = RINGS[ring]
    return (f'<p class="series-line" style="font:600 10.5pt/1.3 \'Nimbus Sans\',\'Liberation Sans\',\'DejaVu Sans\',sans-serif;'
            f'color:{ink};letter-spacing:0.02em;margin:1mm 0 3mm">'
            f'<span style="display:inline-block;width:3mm;height:3mm;background:{swatch};border:0.6px solid #222;'
            f'margin-right:1.6mm;vertical-align:-0.2mm"></span>{series_text(book, part)}</p>')


if __name__ == '__main__':
    b = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    print(series_line(b, sys.argv[2] if len(sys.argv) > 2 else None))
