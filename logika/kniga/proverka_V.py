"""Проверка шага В части 2: В.1 — согласие, В.2 — основание.
Основание: основание есть (b = 1) — x, иначе 0.
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


# osnovanie: есть основание (b = 1) — x, нет или не знаем — 0
def osnovanie(x, b):
    otvet = x if b == 1 else 0
    return otvet


# formula_osnovaniya: (x ∧ b) ∨ (0 ∧ ¬b)
def formula_osnovaniya(x, b):
    otvet = ili(i_(x, b), i_(0, ne(b)))
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


# sverit_stroku_osn: одна строка таблицы основания «**x = 1** | …» против osnovanie
def sverit_stroku_osn(shapka, stroka):
    x = chislo(stroka[0].replace("x =", ""))
    oshibki = [f"основание({x}, {chislo(b.replace('b =', ''))}) в книге {z}"
               for b, z in zip(shapka[1:], stroka[1:])
               if osnovanie(x, chislo(b.replace("b =", ""))) != chislo(z)]
    return oshibki


# sverit_tablicu_osn: таблица «основание» В.2; (сверено, ошибки)
def sverit_tablicu_osn(tekst):
    nuzhnye = [t for t in tablicy(razdel(tekst, "## В.2")) if t[0][0] == "основание"]
    oshibki = [o for t in nuzhnye for stroka in t[1:] for o in sverit_stroku_osn(t[0], stroka)]
    otvet = (len(nuzhnye), oshibki)
    return otvet


# PRIMERY_OSN: что утверждает текст В.2
PRIMERY_OSN = [
    ("сайт видели: основание(1, 1)", osnovanie(1, 1), 1),
    ("слышал от кого-то: основание(1, 0)", osnovanie(1, 0), 0),
    ("журнал: основание(−1, 1)", osnovanie(-1, 1), -1),
    ("соседка без основания: основание(−1, 0)", osnovanie(-1, 0), 0),
    ("И на соседке: −1 ∧ 0", i_(-1, 0), -1),
    ("нечем доказать: основание(1, −1)", osnovanie(1, -1), 0),
    ("два подряд: основание(основание(1, 1), 0)", osnovanie(osnovanie(1, 1), 0), 0),
    ("формула на соседе", formula_osnovaniya(1, -1), 0),
    ("формула по шагам: 1 ∧ −1", i_(1, -1), -1),
    ("формула по шагам: 0 ∧ ¬(−1)", i_(0, ne(-1)), 0),
]
# LOMAETSYA_OSN: И и «нет основания — неправда» НЕ дают основание
LOMAETSYA_OSN = [
    ("И вместо основания у соседки", i_(-1, 0), osnovanie(-1, 0)),
    ("«нет основания — неправда»", -1, osnovanie(1, -1)),
    ("порядок не важен", osnovanie(-1, 1), osnovanie(1, -1)),
]


# sverit_primery_osn: примеры В.2 совпадают, контрпримеры — нет
def sverit_primery_osn():
    oshibki = [f"пример В.2: {chto} → {vyshlo}, нужно {nado}"
               for chto, vyshlo, nado in PRIMERY_OSN if vyshlo != nado]
    oshibki += [f"контрпример В.2 совпал: {chto}"
                for chto, odno, drugoe in LOMAETSYA_OSN if odno == drugoe]
    return oshibki


# svojstva_osn_dvoih: x или 0, НЕ насквозь, формула с 0 — на 9 наборах
def svojstva_osn_dvoih():
    oshibki = []
    for x, b in product(TRITY, repeat=2):
        if osnovanie(x, b) not in (x, 0):
            oshibki.append(f"основание({x}, {b}) — не x и не 0")
        if ne(osnovanie(x, b)) != osnovanie(ne(x), b):
            oshibki.append(f"НЕ не проходит через основание на ({x}, {b})")
        if formula_osnovaniya(x, b) != osnovanie(x, b):
            oshibki.append(f"формула основания не сошлась на ({x}, {b})")
    return oshibki


# svojstva_osn_troih: два основания подряд = основание(x, a ∧ b), порядок оснований не важен
def svojstva_osn_troih():
    oshibki = []
    for x, a, b in product(TRITY, repeat=3):
        podryad = osnovanie(osnovanie(x, a), b)
        if {podryad, osnovanie(osnovanie(x, b), a)} != {osnovanie(x, i_(a, b))}:
            oshibki.append(f"два основания ({x}, {a}, {b}): {podryad}")
    return oshibki


# bez_nulya_osn: на битах основание(1, −1) = 0 — И, ИЛИ, НЕ так не могут
def bez_nulya_osn():
    oshibki = [] if osnovanie(1, -1) == 0 else ["основание(1, −1) не 0"]
    return oshibki


# proverit_V1: всё о согласии; (сверено таблиц, ошибки)
def proverit_V1(tekst):
    svereno, oshibki = sverit_tablicu(tekst)
    if svereno != 1:
        oshibki.append(f"таблиц согласия найдено {svereno}, нужна 1")
    oshibki += sverit_primery() + svojstva() + bez_nulya()
    otvet = (svereno, oshibki)
    return otvet


# proverit_V2: всё об основании; (сверено таблиц, ошибки)
def proverit_V2(tekst):
    svereno, oshibki = sverit_tablicu_osn(tekst)
    if svereno != 1:
        oshibki.append(f"таблиц основания найдено {svereno}, нужна 1")
    oshibki += sverit_primery_osn() + svojstva_osn_dvoih() + svojstva_osn_troih() + bez_nulya_osn()
    otvet = (svereno, oshibki)
    return otvet


# proverit: вся проверка и итог
def proverit(put):
    tekst = Path(put).read_text(encoding="utf-8")
    svereno, oshibki = proverit_V1(tekst)
    svereno_osn, oshibki_osn = proverit_V2(tekst)
    print(f"В.1 — таблиц: {svereno}, примеров: {len(PRIMERY)}, "
          f"контрпримеров: {len(LOMAETSYA)}, свойства: 9 + 27 наборов, без 0 — нельзя")
    print(f"В.2 — таблиц: {svereno_osn}, примеров: {len(PRIMERY_OSN)}, "
          f"контрпримеров: {len(LOMAETSYA_OSN)}, свойства: 9 + 27 наборов, без 0 — нельзя")
    oshibki += oshibki_osn
    print("\n".join(oshibki) if oshibki else "Всё верно.")
    kod = 1 if oshibki else 0
    return kod


if __name__ == "__main__":
    sys.exit(proverit(sys.argv[1] if len(sys.argv) > 1 else "chast-2-trit/V-dejstviya.md"))
