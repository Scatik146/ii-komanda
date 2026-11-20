"""Проверка шага В части 2: В.1 — согласие.
Согласие: одинаково — это значение, разное — 0.
Проверяет таблицу текста, примеры и контрпримеры, порядок, троих, x и ¬x,
НЕ насквозь, формулу с 0 и то, что без 0 согласие не собрать.
Запуск: python3 proverka_V.py chast-2-trit/V-dejstviya.md"""
import sys
from itertools import product
from pathlib import Path

TRITY = (-1, 0, 1)
BITY = (-1, 1)


# ne: НЕ меняет знак
def ne(x):
    otvet = -x
    return otvet


# i_: И берёт меньшее
def i_(x, y):
    otvet = min(x, y)
    return otvet


# ili: ИЛИ берёт большее
def ili(x, y):
    otvet = max(x, y)
    return otvet


# soglasie: одинаково — это значение, разное — 0
def soglasie(x, y):
    otvet = x if x == y else 0
    return otvet


# formula_s_nulem: (x ∧ y) ∨ ((x ∨ y) ∧ 0)
def formula_s_nulem(x, y):
    otvet = ili(i_(x, y), i_(ili(x, y), 0))
    return otvet


# troe: свести двоих, потом с третьим
def troe(x, y, z):
    otvet = soglasie(soglasie(x, y), z)
    return otvet


# chislo: ячейка таблицы «**−1**» → −1
def chislo(yachejka):
    chistaya = yachejka.replace("*", "").replace("−", "-").strip()
    otvet = int(chistaya)
    return otvet


# stroki_tablicy: строка Markdown «| a | b |» → список ячеек
def stroki_tablicy(stroka):
    yachejki = [y.strip() for y in stroka.strip().strip("|").split("|")]
    return yachejki


# razdel: текст раздела от заголовка до следующего «## »
def razdel(tekst, nachalo):
    chast = tekst.split(nachalo, 1)[1] if nachalo in tekst else ""
    konec = chast.find("\n## ")
    otvet = chast if konec < 0 else chast[:konec]
    return otvet


# tablicy: все таблицы раздела — списки строк из ячеек, без строки «|---|»
def tablicy(tekst):
    vse, tekushchaya = [], []
    for stroka in tekst.splitlines() + [""]:
        if stroka.startswith("|"):
            tekushchaya.append(stroki_tablicy(stroka))
        elif tekushchaya:
            vse.append([s for s in tekushchaya if not s[0].startswith("-")])
            tekushchaya = []
    return vse


# sverit_stroku: одна строка таблицы согласия совпадает с soglasie
def sverit_stroku(shapka, stroka):
    x = chislo(stroka[0])
    oshibki = [f"согласие({x}, {chislo(y)}) в книге {z}"
               for y, z in zip(shapka[1:], stroka[1:]) if soglasie(x, chislo(y)) != chislo(z)]
    return oshibki


# sverit_tablicu: таблица «согласие» 3 × 3 совпадает с soglasie; (сверено, ошибки)
def sverit_tablicu(tekst):
    nuzhnye = [t for t in tablicy(razdel(tekst, "## В.1")) if t[0][0] == "согласие"]
    oshibki = [o for t in nuzhnye for stroka in t[1:] for o in sverit_stroku(t[0], stroka)]
    otvet = (len(nuzhnye), oshibki)
    return otvet


# PRIMERY: что утверждает текст В.1 — (что, получилось, должно быть)
PRIMERY = [
    ("каток: оба работал", soglasie(1, 1), 1),
    ("каток: спор", soglasie(1, -1), 0),
    ("И на споре: 1 ∧ −1 = −1", i_(1, -1), -1),
    ("ИЛИ на споре: 1 ∨ −1 = 1", ili(1, -1), 1),
    ("один не подтвердил: согласие(1, 0) = 0", soglasie(1, 0), 0),
    ("электричка: 7:40 ×3 и 7:45", soglasie(troe(1, 1, 1), -1), 0),
    ("сам с собой: x = 1", soglasie(1, ne(1)), 0),
    ("сам с собой: x = −1", soglasie(-1, ne(-1)), 0),
    ("сам с собой: x = 0", soglasie(0, ne(0)), 0),
    ("формула на споре", formula_s_nulem(1, -1), 0),
    ("формула по шагам: 1 ∧ −1", i_(1, -1), -1),
    ("формула по шагам: 1 ∧ 0", i_(ili(1, -1), 0), 0),
]
# LOMAETSYA: контрпримеры текста — И, ИЛИ и голосование НЕ дают согласие
LOMAETSYA = [
    ("И вместо согласия на споре", i_(1, -1), soglasie(1, -1)),
    ("ИЛИ вместо согласия на споре", ili(1, -1), soglasie(1, -1)),
    ("голосование 3 из 4 вместо согласия", 1, soglasie(troe(1, 1, 1), -1)),
]


# sverit_primery: примеры совпадают, контрпримеры — нет
def sverit_primery():
    oshibki = [f"пример: {chto} → {vyshlo}, нужно {nado}"
               for chto, vyshlo, nado in PRIMERY if vyshlo != nado]
    oshibki += [f"контрпример совпал: {chto}"
                for chto, odno, drugoe in LOMAETSYA if odno == drugoe]
    return oshibki


# svojstva_dvoih: порядок, НЕ насквозь, формула с 0 — на 9 наборах
def svojstva_dvoih():
    oshibki = []
    for x, y in product(TRITY, repeat=2):
        if soglasie(x, y) != soglasie(y, x):
            oshibki.append(f"порядок важен на ({x}, {y})")
        if ne(soglasie(x, y)) != soglasie(ne(x), ne(y)):
            oshibki.append(f"НЕ не проходит на ({x}, {y})")
        if formula_s_nulem(x, y) != soglasie(x, y):
            oshibki.append(f"формула с 0 не сошлась на ({x}, {y})")
    return oshibki


# svojstva_troih: общее значение или 0, в любом порядке — на 27 наборах
def svojstva_troih():
    oshibki = []
    for x, y, z in product(TRITY, repeat=3):
        obshchee = x if x == y == z else 0
        poryadki = {troe(x, y, z), troe(y, z, x), troe(z, x, y), soglasie(x, soglasie(y, z))}
        if poryadki != {obshchee}:
            oshibki.append(f"трое ({x}, {y}, {z}): {poryadki}, нужно {obshchee}")
    return oshibki


# svojstva: все свойства и x с ¬x
def svojstva():
    oshibki = svojstva_dvoih() + svojstva_troih()
    oshibki += [f"согласие({x}, ¬{x}) не 0" for x in TRITY if soglasie(x, ne(x)) != 0]
    return oshibki


# bez_nulya: И, ИЛИ, НЕ не выводят из {−1, 1}, а согласие(1, −1) = 0
def bez_nulya():
    vyhody = {ne(x) for x in BITY}
    vyhody |= {d(x, y) for x, y in product(BITY, repeat=2) for d in (i_, ili)}
    oshibki = [] if vyhody <= set(BITY) else [f"И, ИЛИ, НЕ на битах дали {vyhody}"]
    oshibki += [] if soglasie(1, -1) == 0 else ["согласие(1, −1) не 0"]
    return oshibki


# proverit: вся проверка и итог
def proverit(put):
    tekst = Path(put).read_text(encoding="utf-8")
    svereno, oshibki = sverit_tablicu(tekst)
    if svereno != 1:
        oshibki.append(f"таблиц согласия найдено {svereno}, нужна 1")
    oshibki += sverit_primery() + svojstva() + bez_nulya()
    print(f"В.1 — таблиц: {svereno}, примеров: {len(PRIMERY)}, "
          f"контрпримеров: {len(LOMAETSYA)}, свойства: 9 + 27 наборов, без 0 — нельзя")
    print("\n".join(oshibki) if oshibki else "Всё верно.")
    kod = 1 if oshibki else 0
    return kod


if __name__ == "__main__":
    sys.exit(proverit(sys.argv[1] if len(sys.argv) > 1 else "chast-2-trit/V-dejstviya.md"))
