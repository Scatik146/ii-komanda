# proverka_G.py — проверка всех примеров шага Г «Математика и логика»
# запуск: python3 proverka_G.py
from itertools import product

# данные: сравнение битов → логическая связка (таблица Г.2)
SVYAZKI = {
    "==": (lambda p, q: p == q, lambda p, q: (p and q) or (not p and not q)),
    "!=": (lambda p, q: p != q, lambda p, q: not ((p and q) or (not p and not q))),
    "<=": (lambda p, q: p <= q, lambda p, q: (not p) or q),
    ">=": (lambda p, q: p >= q, lambda p, q: p or (not q)),
    "<": (lambda p, q: p < q, lambda p, q: (not p) and q),
    ">": (lambda p, q: p > q, lambda p, q: p and (not q)),
}


# impl: импликация на битах
def impl(p, q):
    otvet = (not p) or q
    return otvet


# ekv: эквивалентность через И, ИЛИ, НЕ
def ekv(p, q):
    otvet = (p and q) or (not p and not q)
    return otvet


# zadacha_G3: выражение задачи Г.3 как в Python
def zadacha_G3(x, y, z):
    otvet = (((x + y > z) <= (x - z >= -y)) > ((2*z > 2*(x + y)) == (x + y > z))) <= (z - y >= x)
    return otvet


# kontrprimer_G3: то же, но с ошибкой переноса во втором сравнении
def kontrprimer_G3(x, y, z):
    otvet = (((x + y > z) <= (x + y <= z)) > ((2*z > 2*(x + y)) == (x + y > z))) <= (z - y >= x)
    return otvet


# formula_G3: шаг 3 — формула на буквах A, B
def formula_G3(a, b):
    otvet = impl(impl(a, b) and not ekv(not b, a), not a)
    return otvet


# svyazki_verny: каждая строка таблицы Г.2 на всех четырёх парах битов
def svyazki_verny():
    pary = list(product((0, 1), repeat=2))
    otvet = all(bool(s(p, q)) == bool(l(p, q)) for s, l in SVYAZKI.values() for p, q in pary)
    return otvet


# primery_G1: примеры и контрпримеры Г.1
def primery_G1():
    summa = (5 < 7) + (3 < 1) == 1
    polozhit = (3 > 0) + (-1 > 0) + (8 > 0) == 2
    cepochka = ((1 < 3) < 2) is True and (1 < 3 < 2) is False
    otvet = summa and polozhit and cepochka and (20 < 15) == 0
    return otvet


# primer_G2: (x < 10) <= (x < 5) совпадает с «x ≥ 10 или x < 5»
def primer_G2():
    otvet = all(((x < 10) <= (x < 5)) == (x >= 10 or x < 5) for x in range(-50, 51))
    return otvet


# shagi_G3: допустимые A, B (без A=1, B=0) — формула шага 3 равна ¬A
def shagi_G3():
    dopustimye = [(0, 0), (0, 1), (1, 1)]
    otvet = all(bool(formula_G3(a, b)) == (not a) for a, b in dopustimye)
    return otvet


# podschet: сколько троек 0..9 дают истину
def podschet(funkciya):
    r = range(10)
    otvet = sum(bool(funkciya(x, y, z)) for x in r for y in r for z in r)
    return otvet


# otvet_G3: выражение равно [x + y ≤ z] на широком диапазоне
def otvet_G3():
    r = range(-20, 21)
    otvet = all(bool(zadacha_G3(x, y, z)) == (x + y <= z) for x in r for y in r for z in r)
    return otvet


# glavnoe: все проверки шага Г
def glavnoe():
    itogi = {
        "Г.1 примеры": primery_G1(),
        "Г.2 шесть связок": svyazki_verny(),
        "Г.2 пример": primer_G2(),
        "Г.3 шаги на буквах": shagi_G3(),
        "Г.3 = [x + y ≤ z]": otvet_G3(),
        "Г.3 ответ 220": podschet(zadacha_G3) == 220,
        "Г.3 контрпример 1000": podschet(kontrprimer_G3) == 1000,
    }
    for imya, verno in itogi.items():
        print(imya, "ок" if verno else "ОШИБКА")
    print("проверок:", len(itogi), "ошибок:", sum(not v for v in itogi.values()))
    return None


glavnoe()
