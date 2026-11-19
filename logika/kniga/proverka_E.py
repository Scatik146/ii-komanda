# proverka_E.py — проверка всех примеров шага Е «Схемы»
# запуск: python3 proverka_E.py
from itertools import product


# ne: элемент НЕ
def ne(a):
    otvet = 1 - a
    return otvet


# i: элемент И
def i(a, b):
    otvet = a & b
    return otvet


# ili: элемент ИЛИ
def ili(a, b):
    otvet = a | b
    return otvet


# xor: элемент исключающее ИЛИ
def xor(a, b):
    otvet = a ^ b
    return otvet


# nabory: все наборы из n битов по порядку таблицы истинности
def nabory(n):
    otvet = list(product((0, 1), repeat=n))
    return otvet


# shema_E1: (x ∧ y) ∨ ¬z — три элемента
def shema_E1(x, y, z):
    otvet = ili(i(x, y), ne(z))
    return otvet


# elementy_E1: ¬x ∧ ¬y = ¬(x ∨ y): три элемента против двух
def elementy_E1():
    otvet = all(i(ne(x), ne(y)) == ne(ili(x, y)) for x, y in nabory(2))
    return otvet


# polusummator: сумма и перенос двух битов
def polusummator(a, b):
    otvet = (xor(a, b), i(a, b))
    return otvet


# summator: сумма и перенос трёх битов — по Ерёмину и Полякову: p = A ⊕ B, g = A ∧ B
def summator(a, b, c):
    p = xor(a, b)
    g = i(a, b)
    otvet = (xor(c, p), ili(g, i(c, p)))
    return otvet


# polusummator_veren: S + 2·P = a + b; контрпример S = a ∨ b ломается на 1, 1
def polusummator_veren():
    verno = all(s + 2 * p == a + b for a, b in nabory(2) for s, p in [polusummator(a, b)])
    otvet = verno and ili(1, 1) != polusummator(1, 1)[0]
    return otvet


# summator_veren: S = (A+B+C) mod 2, P = (A+B+C) div 2; P = большинство; контрпример P = A∧B∧C
def summator_veren():
    po_statje = all(summator(a, b, c) == ((a + b + c) % 2, (a + b + c) // 2) for a, b, c in nabory(3))
    bolsh = all(summator(a, b, c)[1] == int(a + b + c >= 2) for a, b, c in nabory(3))
    kontr = summator(1, 1, 0)[1] == 1 and i(i(1, 1), 0) == 0
    otvet = po_statje and bolsh and kontr
    return otvet


# bity: число → список из n битов, младший первым
def bity(chislo, n):
    otvet = [(chislo >> k) & 1 for k in range(n)]
    return otvet


# slozhit: n-разрядное сложение цепочкой сумматоров; возвращает число с последним переносом
def slozhit(x, y, n):
    perenos = 0
    otvet = 0
    for k, (a, b) in enumerate(zip(bity(x, n), bity(y, n))):
        s, perenos = summator(a, b, perenos)
        otvet = otvet + (s << k)
    otvet = otvet + (perenos << n)
    return otvet


# cepochka_E3: 6 + 7 = 13 и все пары 4-разрядных; без переноса 0110 ⊕ 0111 = 0001
def cepochka_E3():
    primer = slozhit(6, 7, 4) == 13
    vse = all(slozhit(x, y, 4) == x + y for x in range(16) for y in range(16))
    bez_perenosa = (6 ^ 7) == 1
    otvet = primer and vse and bez_perenosa
    return otvet


# STOLBCY: порядок столбцов карты Карно для (y, z) — соседи отличаются одним битом
STOLBCY = [(0, 0), (0, 1), (1, 1), (1, 0)]


# karta: карта Карно трёх переменных — строки x = 0, 1
def karta(f):
    otvet = [[f(x, y, z) for y, z in STOLBCY] for x in (0, 1)]
    return otvet


# sosedi_E4: соседние столбцы (и края) отличаются ровно одним битом; в двоичном порядке 01 и 10 — двумя
def sosedi_E4():
    raznica = lambda u, v: sum(p != q for p, q in zip(u, v))
    karno = all(raznica(STOLBCY[k], STOLBCY[(k + 1) % 4]) == 1 for k in range(4))
    dvoichnyj = raznica((0, 1), (1, 0)) == 2
    otvet = karno and dvoichnyj
    return otvet


# bolshinstvo: 1, если единиц хотя бы две из трёх
def bolshinstvo(x, y, z):
    otvet = int(x + y + z >= 2)
    return otvet


# ne_z_funkciya: единицы в столбцах 00 и 10 — склейка через край
def ne_z_funkciya(x, y, z):
    otvet = int((x, y, z) in [(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 0)])
    return otvet


# minimizaciya_E4: карты примеров, ответы xy ∨ xz ∨ yz и ¬z; контрпримеры «группа из трёх» и «двоичный порядок»
def minimizaciya_E4():
    karty = karta(bolshinstvo) == [[0, 0, 1, 0], [0, 1, 1, 1]] and karta(ne_z_funkciya) == [[1, 0, 0, 1], [1, 0, 0, 1]]
    otvety = all(bolshinstvo(*n) == ((n[0] & n[1]) | (n[0] & n[2]) | (n[1] & n[2])) for n in nabory(3))
    otvety = otvety and all(ne_z_funkciya(*n) == 1 - n[2] for n in nabory(3))
    troika = bolshinstvo(1, 0, 0) == 0
    dvoichnyj = ne_z_funkciya(0, 0, 1) == 0 and int((0, 0, 1)[0] == 0) == 1
    otvet = karty and otvety and troika and dvoichnyj
    return otvet


# f_dvoichnyj: единицы на 001 и 010 — в двоичном порядке столбцы стоят рядом
def f_dvoichnyj(x, y, z):
    otvet = int((x, y, z) in [(0, 0, 1), (0, 1, 0)])
    return otvet


# kontr_dvoichnyj_E4: «склейка» 001 и 010 в ¬x ломается на 000
def kontr_dvoichnyj_E4():
    otvet = f_dvoichnyj(0, 0, 0) == 0 and ne(0) == 1
    return otvet


# proverki: все проверки шага Е — имя и результат
def proverki():
    otvet = {
        "Е.1 схема и элементы": shema_E1(1, 1, 1) == 1 and shema_E1(0, 1, 1) == 0 and elementy_E1(),
        "Е.2 полусумматор": polusummator_veren(),
        "Е.3 сумматор по статье": summator_veren(),
        "Е.3 цепочка 4 разряда": cepochka_E3(),
        "Е.4 соседи на карте": sosedi_E4(),
        "Е.4 минимизация": minimizaciya_E4(),
        "Е.4 контрпример двоичный порядок": kontr_dvoichnyj_E4(),
    }
    return otvet


# glavnoe: запустить проверки и напечатать итог
def glavnoe():
    itogi = proverki()
    for imya, verno in itogi.items():
        print(imya, "ок" if verno else "ОШИБКА")
    print("проверок:", len(itogi), "ошибок:", sum(not v for v in itogi.values()))
    return None


glavnoe()
