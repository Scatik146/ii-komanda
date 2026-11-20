"""Сборка страницы сайта из раздела книги: Markdown → один HTML-файл.
Запуск: python3 sbor_stranicy.py chast-1-bit/A-osnova.md
Результат: stranicy/<имя>.html, оформление встроено из stranicy/kniga.css."""
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


# telo: Markdown → HTML с таблицами
def telo(md):
    html = markdown.markdown(md, extensions=["tables", "attr_list"])
    return html


# sobrat: страница целиком
def sobrat(md, stil):
    stranica = SHABLON.format(zagolovok=zagolovok(md), stil=stil, telo=telo(md))
    return stranica


# zapisat: сохранить страницу рядом в stranicy/
def zapisat(ishodnik, stranica):
    put = ZDES / "stranicy" / (ishodnik.stem + ".html")
    put.write_text(stranica, encoding="utf-8")
    return put


# glavnoe: раздел → страница
def glavnoe(imya):
    ishodnik = ZDES / imya
    stil = prochitat(ZDES / "stranicy" / "kniga.css")
    put = zapisat(ishodnik, sobrat(prochitat(ishodnik), stil))
    print(put)
    return put


if __name__ == "__main__":
    glavnoe(sys.argv[1])
