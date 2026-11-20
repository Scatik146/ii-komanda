"""Проверка шага А части 2 (А.1, А.2): таблицы НЕ, И, ИЛИ на тритах,
девять вариантов пары (сказано, верить), ворота наружу,
все примеры с контрпримерами.
Запуск: python3 proverka_A2.py chast-2-trit/A-osnova.md"""
import sys
from itertools import product
from pathlib import Path

TRITY = (-1, 0, 1)

# ne: НЕ переворачивает «да» и «нет», «не знаю» оставляет
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


# bit_v_trit: бит части 1 → трит; бит 0 (ложь) → −1
def bit_v_trit(b):
    otvet = 1 if b == 1 else -1
    return otvet


# PRIMERY: что утверждает текст А.1 — (что, получилось, должно быть)
# «ломается» — должно НЕ совпасть: старая формула части 1 врёт на тритах
PRIMERY = [
    ("¬0 = 0", ne(0), 0),
    ("¬(−1) = 1", ne(-1), 1),
    ("экскурсия: 1 ∧ ¬0 = 0", i_(1, ne(0)), 0),
    ("перенос: −1 ∨ 0 = 0", ili(-1, 0), 0),
    ("1 ∨ 0 = 1", ili(1, 0), 1),
    ("−1 ∧ 0 = −1", i_(-1, 0), -1),
]
LOMAETSYA = [
    ("1 − x при x = 0 даёт 1, а ¬0 = 0", 1 - 0, ne(0)),
    ("1 − x при x = 1 даёт 0, а ¬1 = −1", 1 - 1, ne(1)),
    ("x · y: (−1) · (−1) = 1, а −1 ∧ −1 = −1", (-1) * (-1), i_(-1, -1)),
    ("x · y: 0 · (−1) = 0, а 0 ∧ −1 = −1", 0 * (-1), i_(0, -1)),
    ("x + y − x · y: (−1) + (−1) − 1 = −3, а −1 ∨ −1 = −1",
     -1 + -1 - (-1) * (-1), ili(-1, -1)),
]


# chislo: ячейка таблицы → трит («−1», «**0**»)
def chislo(yachejka):
    chistaya = yachejka.replace("*", "").replace("−", "-").strip()
    return int(chistaya)


# stroki_tablicy: строка Markdown «| a | b |» → список ячеек
def stroki_tablicy(stroka):
    yachejki = [y.strip() for y in stroka.strip().strip("|").split("|")]
    return yachejki


# razdel: текст раздела от «## А.1» до следующего «## »
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


# sverit_ne: таблица «x / ¬x» совпадает с ne
def sverit_ne(t):
    pary = zip(t[0][1:], t[1][1:])
    oshibki = [f"¬{x} в книге {y}" for x, y in pary if ne(chislo(x)) != chislo(y)]
    return oshibki


# sverit_stroku: одна строка таблицы 3 × 3 совпадает с действием
def sverit_stroku(shapka, stroka, dejstvie):
    x = chislo(stroka[0])
    pary = zip(shapka[1:], stroka[1:])
    oshibki = [f"{stroka[0]} {shapka[0]} {y} в книге {z}"
               for y, z in pary if dejstvie(x, chislo(y)) != chislo(z)]
    return oshibki


# sverit_dvuh: таблица 3 × 3 для ∧ или ∨ совпадает с действием
def sverit_dvuh(t):
    dejstvie = i_ if t[0][0] == "∧" else ili
    oshibki = []
    for stroka in t[1:]:
        oshibki += sverit_stroku(t[0], stroka, dejstvie)
    return oshibki


# sverit_tablicy: все таблицы А.1; возвращает (сколько сверено, ошибки)
def sverit_tablicy(tekst):
    svereno, oshibki = 0, []
    for t in tablicy(razdel(tekst, "## А.1")):
        if t[0][0] == "x" and t[1][0] == "¬x":
            oshibki += sverit_ne(t)
            svereno += 1
        elif t[0][0] in ("∧", "∨"):
            oshibki += sverit_dvuh(t)
            svereno += 1
    return svereno, oshibki


# ugly: на битах (−1 и 1) min и max — это старые И и ИЛИ части 1
def ugly():
    oshibki = []
    for a, b in product((0, 1), repeat=2):
        if i_(bit_v_trit(a), bit_v_trit(b)) != bit_v_trit(a & b):
            oshibki.append(f"угол И: {a} {b}")
        if ili(bit_v_trit(a), bit_v_trit(b)) != bit_v_trit(a | b):
            oshibki.append(f"угол ИЛИ: {a} {b}")
    return oshibki


# sverit_primery: примеры совпадают, «ломается» — не совпадает
def sverit_primery():
    oshibki = [f"пример: {c}" for c, est, nado in PRIMERY if est != nado]
    oshibki += [f"не ломается: {c}" for c, est, nado in LOMAETSYA if est == nado]
    return oshibki


# --- А.2: пара (сказано, верить) ---

# vorota: пропускают только 1, всё остальное — −1
def vorota(x):
    otvet = 1 if x == 1 else -1
    return otvet


# vmeste: два трита пары → один, И берёт меньшее
def vmeste(skazano, verit):
    otvet = i_(skazano, verit)
    return otvet


# naruzhu: выдавать ли утверждение — ворота от «вместе»
def naruzhu(skazano, verit):
    otvet = vorota(vmeste(skazano, verit))
    return otvet


# PRIMERY_A2: что утверждает текст А.2 — (что, получилось, должно быть)
PRIMERY_A2 = [
    ("учитель записал в журнал (1, 1) → наружу", naruzhu(1, 1), 1),
    ("учитель: «не будет» (−1, 1) → «будет» не наружу", naruzhu(-1, 1), -1),
    ("«контрольной нет»: (¬(−1), 1) → наружу", naruzhu(ne(-1), 1), 1),
    ("соседка: «не будет», не верю: −1 ∧ −1 = −1", vmeste(-1, -1), -1),
    ("учитель: «ещё не решил» (0, 1) → не наружу", naruzhu(0, 1), -1),
]
# LOMAETSYA_A2: короткий путь — должен НЕ совпасть с naruzhu
LOMAETSYA_A2 = [
    ("«верю, значит да»: (−1, 1) по «верить» → 1", vorota(1), naruzhu(-1, 1)),
    ("«сказали, значит да»: (1, 0) по «сказано» → 1", vorota(1), naruzhu(1, 0)),
    ("умножение: (−1) · (−1) = 1", vorota((-1) * (-1)), naruzhu(-1, -1)),
]


# sverit_devyat: таблица девяти вариантов — все пары, «вместе» и «наружу»
def sverit_devyat(t):
    oshibki, pary = [], set()
    for s in t[1:]:
        skazano, verit = chislo(s[0]), chislo(s[1])
        pary.add((skazano, verit))
        if vmeste(skazano, verit) != chislo(s[3]):
            oshibki.append(f"вместе ({s[0]}, {s[1]}) в книге {s[3]}")
        if naruzhu(skazano, verit) != chislo(s[4]):
            oshibki.append(f"наружу ({s[0]}, {s[1]}) в книге {s[4]}")
    if pary != set(product(TRITY, repeat=2)):
        oshibki.append(f"вариантов в таблице {len(pary)}, нужно 9")
    return oshibki


# sverit_vorota: таблица «x / ворота» совпадает с vorota
def sverit_vorota(t):
    pary = zip(t[0][1:], t[1][1:])
    oshibki = [f"ворота({x}) в книге {y}" for x, y in pary
               if vorota(chislo(x)) != chislo(y)]
    return oshibki


# tolko_odin: наружу проходит ровно одна пара — (1, 1)
def tolko_odin():
    prohodyat = [p for p in product(TRITY, repeat=2) if naruzhu(*p) == 1]
    oshibki = [] if prohodyat == [(1, 1)] else [f"наружу проходят {prohodyat}"]
    return oshibki


# dve_stroki: наружу проходят прямо или через НЕ ровно две пары — (−1, 1) и (1, 1)
def dve_stroki():
    prohodyat = [p for p in product(TRITY, repeat=2)
                 if naruzhu(*p) == 1 or naruzhu(ne(p[0]), p[1]) == 1]
    oshibki = [] if prohodyat == [(-1, 1), (1, 1)] else [f"две строки: {prohodyat}"]
    return oshibki


# sverit_A2: таблицы, примеры и контрпримеры А.2; (сколько таблиц, ошибки)
def sverit_A2(tekst):
    svereno, oshibki = 0, []
    for t in tablicy(razdel(tekst, "## А.2")):
        if t[0][0] == "сказано":
            oshibki += sverit_devyat(t)
            svereno += 1
        elif t[0][0] == "x" and t[1][0] == "ворота":
            oshibki += sverit_vorota(t)
            svereno += 1
    oshibki += [f"пример А.2: {c}" for c, est, nado in PRIMERY_A2 if est != nado]
    oshibki += [f"не ломается А.2: {c}" for c, est, nado in LOMAETSYA_A2
                if est == nado]
    if svereno < 2:
        oshibki.append(f"таблиц А.2 найдено {svereno}, нужно 2")
    return svereno, oshibki + tolko_odin() + dve_stroki()


# proverit: верхнее слово — сверить таблицы, примеры и углы, напечатать итог
def proverit(put):
    svereno, oshibki = sverit_tablicy(Path(put).read_text(encoding="utf-8"))
    tekst = Path(put).read_text(encoding="utf-8")
    oshibki += sverit_primery() + ugly()
    if svereno < 3:
        oshibki.append(f"таблиц НЕ, И, ИЛИ найдено {svereno}, нужно 3")
    svereno_A2, oshibki_A2 = sverit_A2(tekst)
    oshibki += oshibki_A2
    print(f"А.1 — таблиц: {svereno}, примеров: {len(PRIMERY)}, "
          f"контрпримеров: {len(LOMAETSYA)}, углов: 4 × 2")
    print(f"А.2 — таблиц: {svereno_A2}, примеров: {len(PRIMERY_A2)}, "
          f"контрпримеров: {len(LOMAETSYA_A2)}, наружу — только (1, 1), с НЕ — две строки")
    print("\n".join(oshibki) if oshibki else "Всё верно.")
    kod = 1 if oshibki else 0
    return kod


if __name__ == "__main__":
    sys.exit(proverit(sys.argv[1] if len(sys.argv) > 1 else "chast-2-trit/A-osnova.md"))
