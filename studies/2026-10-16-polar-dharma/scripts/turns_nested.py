# The infinite core as one seamless picture (DICTO, 2026-10-16). Orthographic cut views share one centre; view k is phi^3 narrower
# than view k-1, so set into the centre at exactly 1/phi^3 of its width it lines up with the picture around it (the cycle is
# self-similar). The deeper turns come from their own renders, so they stay sharp instead of shrinking to a blur. No frames.
from PIL import Image
phi3 = 4.236067977499790
base = Image.open('renders/core-0.png').convert('RGB'); N = base.size[0]; size = N
for k in (1, 2, 3):
    size = size / phi3; s = int(round(size)); o = (N - s) // 2
    base.paste(Image.open(f'renders/core-{k}.png').convert('RGB').resize((s, s), Image.LANCZOS), (o, o))
base.save('renders/polar-turns-seamless.png'); base.resize((1600, 1600), Image.LANCZOS).save('renders/polar-turns-seamless.jpg', quality=90)
c = N // 2; w = int(N / phi3 * 1.15)                                    # detail: the centre, one turn in
base.crop((c - w // 2, c - w // 2, c + w // 2, c + w // 2)).resize((1200, 1200), Image.LANCZOS).save('renders/polar-turns-seamless-detail.jpg', quality=90)
print('ok', N)
