"""shemy_png.py — ДРАКОН-схемы урока картинками для печати: открыть пустую страницу в папке урока, нарисовать схему, снять элемент."""
import pathlib
import sys
from playwright.sync_api import sync_playwright

STRANICA = """<!doctype html><meta charset="utf-8"><body style="margin:0;background:#fff">
<div id="s" style="display:inline-block;width:{w}px"></div>
<script src="../../lib/drakonwidget/drakonwidget.js"></script><script src="../../lib/drakon-shema/drakon-shema.js"></script>
<script src="tekst.js"></script><script>window.d = DrakonShema.pokazat(document.getElementById('s'), T.shemy.{imya}, {{vpisat:false}});</script>"""


# snyat: папка урока, имя схемы, ширина → PNG в kartinki/
def snyat(papka, imya, w):
    vr = pathlib.Path(papka) / f'_vr-{imya}.html'
    vr.write_text(STRANICA.format(w=w, imya=imya), encoding='utf-8')
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/usr/bin/google-chrome')
        s = b.new_page(device_scale_factor=2); s.goto(vr.resolve().as_uri()); s.wait_for_timeout(2500)
        s.locator('#s').screenshot(path=str(pathlib.Path(papka) / 'kartinki' / f'shema-{imya}.png'))
        b.close()
    vr.unlink()
    return imya


for imya, w in [('ekspertiza', 1100), ('serediny', 1100), ('sosed', 1100)]:
    print(snyat(sys.argv[1], imya, w))


# obrezat: PNG → обрезка по тёмным пикселям схемы (линии и текст) с полями 16 px
def obrezat(put):
    from PIL import Image
    im = Image.open(put).convert('RGB')
    maska = im.convert('L').point(lambda v: 255 if v < 150 else 0)
    x0, y0, x1, y1 = maska.getbbox()
    im.crop((max(0, x0 - 16), max(0, y0 - 16), x1 + 16, y1 + 16)).save(put)
    return im.size


for imya in ['ekspertiza', 'serediny', 'sosed']:
    print(obrezat(pathlib.Path(sys.argv[1]) / 'kartinki' / f'shema-{imya}.png'))
