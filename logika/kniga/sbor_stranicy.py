"""Сборка страницы сайта из раздела книги: Markdown → один HTML-файл.
Запуск: python3 sbor_stranicy.py chast-1-bit/A-osnova.md
Результат: stranicy/<имя>.html, оформление встроено из stranicy/kniga.css."""
import re
import sys
from pathlib import Path
import markdown

ZDES = Path(__file__).parent
SHABLON = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{zagolovok}</title>
<style>
{stil}</style>
</head>
<body>
<main>
{telo}
</main>
</body>
</html>
"""


# prochitat: текст файла
def prochitat(put):
    tekst = put.read_text(encoding="utf-8")
    return tekst


# zagolovok: первая строка «# …» без решётки
def zagolovok(md):
    pervaja = md.splitlines()[0]
    imya = pervaja.lstrip("# ").strip()
    return imya


# metka: якорь заголовка как на GitHub — «### 5. Огастес де Морган» → 5-огастес-де-морган
def metka(tekst, razdel):
    slovo = re.sub(r"[^\w\- ]", "", tekst.strip().lower())
    return slovo.replace(" ", razdel)


# telo: Markdown → HTML с таблицами и якорями заголовков
def telo(md):
    toc = {"toc": {"slugify": metka}}
    html = markdown.markdown(md, extensions=["tables", "attr_list", "toc"], extension_configs=toc)
    return html


# ssylki: ссылки на «Действующих лиц» — с .md на .html, путь от папки страницы
def ssylki(md, ishodnik):
    kuda = "dejstvuyushchie-lica.html#"
    if papka(ishodnik) != ZDES / "stranicy":
        kuda = "../" + kuda
    md = md.replace("../dejstvuyushchie-lica.md#", kuda)
    return md


# sobrat: страница целиком
def sobrat(md, stil):
    stranica = SHABLON.format(zagolovok=zagolovok(md), stil=stil, telo=telo(md))
    return stranica


# papka: часть 1 и общие файлы — прямо в stranicy/, другие части — в stranicy/<часть>/
def papka(ishodnik):
    chast = ishodnik.parent.name
    kuda = ZDES / "stranicy"
    if chast not in ("chast-1-bit", ZDES.name):
        kuda = kuda / chast
    kuda.mkdir(exist_ok=True)
    return kuda


# zapisat: сохранить страницу в свою папку
def zapisat(ishodnik, stranica):
    put = papka(ishodnik) / (ishodnik.stem + ".html")
    put.write_text(stranica, encoding="utf-8")
    return put


# glavnoe: раздел → страница
def glavnoe(imya):
    ishodnik = ZDES / imya
    stil = prochitat(ZDES / "stranicy" / "kniga.css")
    md = ssylki(prochitat(ishodnik), ishodnik)
    put = zapisat(ishodnik, sobrat(md, stil))
    print(put)
    return put


if __name__ == "__main__":
    glavnoe(sys.argv[1])
