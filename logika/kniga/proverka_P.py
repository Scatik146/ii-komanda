# proverka_P.py — проверка таблицы «Кто за кем» приложения «Для любопытных»
# запуск: python3 proverka_P.py
# Каждое имя и каждый год строки стоят в разделе из столбца «Где у нас»; годы идут по порядку.
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


# osnova: основа фамилии без падежного окончания
def osnova(imya):
    familiya = imya.split()[-1]
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


# pervyj_god: первый год строки; без цифр (до н. э.) — самый ранний
def pervyj_god(stroka):
    vse = gody(stroka[0])
    otvet = int(vse[0]) if vse else -1
    return otvet


# proverit: печать расхождений, число ошибок
def proverit():
    stroki = stroki_tablicy(PRILOZHENIE.read_text(encoding="utf-8"))
    oshibki = 0
    for s in stroki:
        net = oshibki_stroki(s)
        if net:
            print("нет в", s[3], ":", s[1], net)
            oshibki += 1
    poryadok = [pervyj_god(s) for s in stroki]
    if poryadok != sorted(poryadok):
        print("годы не по порядку")
        oshibki += 1
    lyudi = len({osnova(s[1]) for s in stroki})
    print("строк", len(stroki), "людей", lyudi, "ошибок", oshibki)
    return oshibki


if __name__ == "__main__":
    raise SystemExit(1 if proverit() else 0)
