# proverka_P.py — проверка таблицы «Кто за кем» приложения «Для любопытных»
# запуск: python3 proverka_P.py
# Каждое имя и каждый год строки стоят в разделе из столбца «Где у нас»; годы идут по порядку.
# Фамилия в таблице — ссылка на биографию П.5; разделы из «Где у нас:» биографии упоминают эту фамилию.
import re
from pathlib import Path

ZDES = Path(__file__).parent / "chast-1-bit"
PRILOZHENIE = ZDES / "P-dlya-lyubopytnyh.md"
FAJLY = {"А": "A-osnova.md", "Б": "B-zakony.md", "В": "V-bazisy.md",
         "Г": "G-matematika.md", "Д": "D-zhegalkin.md", "Е": "E-shemy.md"}


# stroki_tablicy: строки таблицы П.1 как списки ячеек (без шапки и черты)
def stroki_tablicy(tekst):
    vse = [s for s in tekst.splitlines() if s.startswith("| ")]
    yachejki = [[c.strip() for c in s.strip("|").split("|")] for s in vse]
    otvet = yachejki[1:]
    return otvet


# gody: все четырёхзначные годы из ячейки
def gody(yachejka):
    otvet = re.findall(r"\d{4}", yachejka)
    return otvet


# bez_ssylki: текст ссылки «[текст](#id)» без разметки
def bez_ssylki(yachejka):
    otvet = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", yachejka)
    return otvet


# osnova: основа фамилии без падежного окончания
def osnova(imya):
    familiya = bez_ssylki(imya).split()[-1]
    if familiya[-1] in "ьйая":
        familiya = familiya[:-1]
    otvet = familiya[:6]
    return otvet


# kusok_razdela: текст раздела «## Х.n.» до следующего «## »
def kusok_razdela(nomer):
    tekst = (ZDES / FAJLY[nomer[0]]).read_text(encoding="utf-8")
    chasti = re.split(r"\n(?=## )", tekst)
    najdeno = [c for c in chasti if c.startswith("## " + nomer + ".")]
    otvet = najdeno[0] if najdeno else ""
    return otvet


# oshibki_stroki: чего из строки нет в её разделе
def oshibki_stroki(stroka):
    god, kto, _, gde = stroka
    kusok = kusok_razdela(gde)
    nuzhno = [osnova(kto)] + gody(god)
    otvet = [n for n in nuzhno if n not in kusok]
    return otvet


# oshibki_tablicy: печать строк, которых нет в разделах, их число
def oshibki_tablicy(stroki):
    oshibki = 0
    for s in stroki:
        net = oshibki_stroki(s)
        if net:
            print("нет в", s[3], ":", s[1], net)
            oshibki += 1
    return oshibki


# pervyj_god: первый год строки; без цифр (до н. э.) — самый ранний
def pervyj_god(stroka):
    vse = gody(stroka[0])
    otvet = int(vse[0]) if vse else -1
    return otvet


# yakorya: все «{#id}» в тексте
def yakorya(tekst):
    otvet = set(re.findall(r"\{#([\w-]+)\}", tekst))
    return otvet


# bez_biografii: фамилии таблицы, чья ссылка не ведёт к якорю
def bez_biografii(stroki, tekst):
    est = yakorya(tekst)
    ssylki = [(s[1], re.findall(r"\(#([\w-]+)\)", s[1])) for s in stroki]
    otvet = [kto for kto, ids in ssylki if not ids or ids[0] not in est]
    return otvet


# biografii: пары (имя, разделы из строки «Где у нас:») из П.5
def biografii(tekst):
    p5 = tekst.split("## П.5.")[-1]
    chasti = re.split(r"\n### ", p5)[1:]
    otvet = []
    for c in chasti:
        imya = c.split(" {#")[0]
        gde = re.findall(r"Где у нас:.*", c)
        otvet.append((imya, re.findall(r"\[([А-Е]\.\d)\]", gde[0] if gde else "")))
    return otvet


# oshibki_biografij: биографии, чьи разделы не упоминают героя
def oshibki_biografij(tekst):
    otvet = []
    for imya, razdely in biografii(tekst):
        net = [r for r in razdely if osnova(imya) not in kusok_razdela(r)]
        if net or not razdely:
            otvet.append((imya, net))
    return otvet


# oshibki_p5: печать ошибок ссылок и биографий, их число
def oshibki_p5(stroki, tekst):
    oshibki = 0
    for kto in bez_biografii(stroki, tekst):
        print("нет биографии:", kto)
        oshibki += 1
    for imya, net in oshibki_biografij(tekst):
        print("биография", imya, "- в разделах нет героя:", net)
        oshibki += 1
    return oshibki


# proverit: печать расхождений, число ошибок
def proverit():
    tekst = PRILOZHENIE.read_text(encoding="utf-8")
    stroki = stroki_tablicy(tekst)
    oshibki = oshibki_tablicy(stroki)
    poryadok = [pervyj_god(s) for s in stroki]
    if poryadok != sorted(poryadok):
        print("годы не по порядку")
        oshibki += 1
    oshibki += oshibki_p5(stroki, tekst)
    lyudi = len({osnova(s[1]) for s in stroki})
    bio = len(biografii(tekst))
    print("строк", len(stroki), "людей", lyudi, "биографий", bio, "ошибок", oshibki)
    return oshibki


if __name__ == "__main__":
    raise SystemExit(1 if proverit() else 0)
