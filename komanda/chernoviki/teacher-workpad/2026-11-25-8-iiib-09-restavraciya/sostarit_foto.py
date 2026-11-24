"""sostarit_foto.py — «состарить» картинку: ч/б с желтизной, блёклость, царапины, пятна, сгиб, оторванный угол; плюс мелкая копия.

Вход: путь к картинке, имя, папка. Выход: <имя>-staroe.jpg (768 px), <имя>-melkoe.png (64 px, ч/б), <имя>-podlinnik.jpg (768 px).
"""
import random
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageOps


# sepiya: цветная → ч/б с желтизной и блёклым контрастом
def sepiya(im):
    seroe = ImageOps.autocontrast(im.convert('L'), cutoff=2)
    blekloe = seroe.point(lambda v: int(60 + v * 0.65))
    return ImageOps.colorize(blekloe, black=(52, 38, 24), white=(236, 222, 190))


# carapiny: тонкие светлые линии
def carapiny(im, sl):
    d = ImageDraw.Draw(im)
    for _ in range(14):
        x, y = sl.randint(0, im.width), sl.randint(0, im.height)
        d.line([(x, y), (x + sl.randint(-90, 90), y + sl.randint(80, 320))], fill=(245, 238, 220), width=sl.choice([1, 1, 2]))
    return im


# pyatna: полупрозрачные бурые пятна
def pyatna(im, sl):
    sloj = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(sloj)
    for _ in range(6):
        x, y, r = sl.randint(0, im.width), sl.randint(0, im.height), sl.randint(18, 60)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(110, 80, 40, sl.randint(50, 110)))
    sloj = sloj.filter(ImageFilter.GaussianBlur(6))
    return Image.alpha_composite(im.convert('RGBA'), sloj).convert('RGB')


# sgib: светлая полоса сгиба поперёк кадра
def sgib(im):
    d = ImageDraw.Draw(im)
    y = int(im.height * 0.42)
    d.line([(0, y), (im.width, y + 30)], fill=(240, 232, 210), width=5)
    return im


# ugol: оторванный правый нижний угол — белый рваный треугольник
def ugol(im, sl):
    d = ImageDraw.Draw(im)
    w, h = im.size
    tochki = [(w, int(h * 0.62))]
    for k in range(1, 8):
        tochki.append((w - int(w * 0.3 * k / 8) + sl.randint(-8, 8), int(h * 0.62) + int(h * 0.38 * k / 8) + sl.randint(-8, 8)))
    tochki += [(int(w * 0.68), h), (w, h)]
    d.polygon(tochki, fill=(255, 255, 255))
    return im


# sostarit: путь, имя, папка → три файла
def sostarit(put, imya, papka):
    sl = random.Random(imya)
    podlinnik = Image.open(put).convert('RGB').resize((768, 768))
    staroe = ugol(sgib(pyatna(carapiny(sepiya(podlinnik), sl), sl)), sl).filter(ImageFilter.GaussianBlur(1.2))
    p = Path(papka)
    staroe.save(p / f'{imya}-staroe.jpg', quality=82)
    podlinnik.convert('L').resize((64, 64), Image.BILINEAR).save(p / f'{imya}-melkoe.png')
    podlinnik.save(p / f'{imya}-podlinnik.jpg', quality=85)
    return [f'{imya}-staroe.jpg', f'{imya}-melkoe.png', f'{imya}-podlinnik.jpg']


print(sostarit(sys.argv[1], sys.argv[2], sys.argv[3]))
