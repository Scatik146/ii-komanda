# proverka_D.py — проверка всех примеров шага Д «Жегалкин»
# запуск: python3 proverka_D.py
from itertools import product


# xor: исключающее ИЛИ на битах
def xor(p, q):
    otvet = int(p != q)
    return otvet


# impl: импликация на битах
def impl(p, q):
    otvet = int((not p) or q)
    return otvet


# bolshinstvo: 1, если единиц хотя бы две из трёх
def bolshinstvo(x, y, z):
    otvet = int(x + y + z >= 2)
    return otvet


# nabory: все наборы из n битов по порядку таблицы истинности
def nabory(n):
    otvet = list(product((0, 1), repeat=n))
    return otvet


# ZAKONY_D1: закон ⊕ → (левая часть, правая часть) на трёх битах
ZAKONY_D1 = {
    "x ⊕ 0 = x": (lambda x, y, z: xor(x, 0), lambda x, y, z: x),
    "x ⊕ 1 = ¬x": (lambda x, y, z: xor(x, 1), lambda x, y, z: 1 - x),
    "x ⊕ x = 0": (lambda x, y, z: xor(x, x), lambda x, y, z: 0),
    "x ⊕ y = y ⊕ x": (lambda x, y, z: xor(x, y), lambda x, y, z: xor(y, x)),
    "(x ⊕ y) ⊕ z = x ⊕ (y ⊕ z)": (lambda x, y, z: xor(xor(x, y), z), lambda x, y, z: xor(x, xor(y, z))),
    "x ∧ (y ⊕ z) = (x ∧ y) ⊕ (x ∧ z)": (lambda x, y, z: x & xor(y, z), lambda x, y, z: xor(x & y, x & z)),
    "x ⊕ y = ¬(x ≡ y)": (lambda x, y, z: xor(x, y), lambda x, y, z: 1 - int(x == y)),
    "x ⊕ y = (x ∧ ¬y) ∨ (¬x ∧ y)": (lambda x, y, z: xor(x, y), lambda x, y, z: (x & (1 - y)) | ((1 - x) & y)),
    "(a ⊕ k) ⊕ k = a": (lambda x, y, z: xor(xor(x, y), y), lambda x, y, z: x),
}


# zakony_D1: все законы Д.1 верны на всех восьми наборах
def zakony_D1():
    otvet = all(l(*n) == r(*n) for l, r in ZAKONY_D1.values() for n in nabory(3))
    return otvet


# kontr_D1: ИЛИ не раскрывается над ⊕ (x = 1, y = 0, z = 0); x ⊕ x ≠ x ∨ x; цепочка — чётность
def kontr_D1():
    ili = (1 | xor(0, 0)) == 1 and xor(1 | 0, 1 | 0) == 0
    sam = xor(1, 1) == 0 and (1 | 1) == 1
    cepochka = xor(xor(xor(xor(1, 1), 1), 0), 1) == 0
    otvet = ili and sam and cepochka
    return otvet


# znachenie_polinoma: многочлен (список одночленов) на наборе; одночлен — кортеж номеров букв
def znachenie_polinoma(odnochleny, nabor):
    otvet = 0
    for chlen in odnochleny:
        otvet = xor(otvet, int(all(nabor[i] for i in chlen)))
    return otvet


# koefficienty: метод неопределённых коэффициентов — наборы по числу единиц, коэффициент = f ⊕ сумма уже найденных
def koefficienty(f, n):
    odnochleny = []
    for nabor in sorted(nabory(n), key=sum):
        chlen = tuple(i for i in range(n) if nabor[i])
        if xor(f(*nabor), znachenie_polinoma(odnochleny, nabor)):
            odnochleny.append(chlen)
    otvet = sorted(odnochleny, key=lambda c: (len(c), c))
    return otvet


# treugolnik: строки треугольника из вектора значений, каждая — ⊕ соседей
def treugolnik(vektor):
    stroki = [list(vektor)]
    while len(stroki[-1]) > 1:
        verh = stroki[-1]
        stroki.append([xor(verh[i], verh[i + 1]) for i in range(len(verh) - 1)])
    otvet = stroki
    return otvet


# po_treugolniku: многочлен по левому краю треугольника
def po_treugolniku(f, n):
    vektor = [f(*nab) for nab in nabory(n)]
    kraj = [stroka[0] for stroka in treugolnik(vektor)]
    chleny = [tuple(i for i in range(n) if nab[i]) for nab, k in zip(nabory(n), kraj) if k]
    otvet = sorted(chleny, key=lambda c: (len(c), c))
    return otvet


# paskal: тот же треугольник с обычным + вместо ⊕ (контрпример)
def paskal(vektor):
    stroki = [list(vektor)]
    while len(stroki[-1]) > 1:
        verh = stroki[-1]
        stroki.append([verh[i] + verh[i + 1] for i in range(len(verh) - 1)])
    otvet = stroki
    return otvet


# primery_D2_D3: x → y = 1 ⊕ x ⊕ xy; большинство = xy ⊕ xz ⊕ yz; оба метода совпадают
def primery_D2_D3():
    imp = koefficienty(impl, 2) == [(), (0,), (0, 1)] == po_treugolniku(impl, 2)
    bol = koefficienty(bolshinstvo, 3) == [(0, 1), (0, 2), (1, 2)] == po_treugolniku(bolshinstvo, 3)
    stroki = treugolnik([1, 1, 0, 1]) == [[1, 1, 0, 1], [0, 1, 1], [1, 0], [1]]
    otvet = imp and bol and stroki
    return otvet


# vse_16_D: на всех 16 функциях двух переменных и всех 256 трёх оба метода совпадают и дают ту же функцию
def vse_16_D():
    verno = True
    for n in (2, 3):
        for vektor in product((0, 1), repeat=2 ** n):
            f = lambda *nab, v=vektor, m=n: v[nabory(m).index(nab)]
            poli = koefficienty(f, n)
            verno = verno and poli == po_treugolniku(f, n) and all(znachenie_polinoma(poli, nab) == f(*nab) for nab in nabory(n))
    otvet = verno
    return otvet


# kontr_D2_D3: обычный + даёт −1 в коэффициенте xy и Паскаля вместо треугольника
def kontr_D2_D3():
    koef_xy = 1 - (1 + 1 + 0)
    treug = paskal([1, 1, 0, 1]) == [[1, 1, 0, 1], [2, 1, 1], [3, 2], [5]]
    pravyj = [stroka[-1] for stroka in treugolnik([1, 1, 0, 1])] == [1, 1, 0, 1]
    oshibka = znachenie_polinoma([(), (1,), (0, 1)], (1, 0)) == 1 and impl(1, 0) == 0
    otvet = koef_xy == -1 and treug and pravyj and oshibka
    return otvet


# lineinaya: в многочлене нет произведений двух и более букв
def lineinaya(f, n):
    otvet = all(len(chlen) <= 1 for chlen in koefficienty(f, n))
    return otvet


# lineinost_D4: ≡ линейна (1 ⊕ x ⊕ y), → и ∨ нет; ∨ = x ⊕ y ⊕ xy (Яблонский, пример 12)
def lineinost_D4():
    ekv = lambda x, y: int(x == y)
    ili = lambda x, y: x | y
    ekv_ok = koefficienty(ekv, 2) == [(), (0,), (1,)] and lineinaya(ekv, 2)
    ili_ok = koefficienty(ili, 2) == [(0,), (1,), (0, 1)] and not lineinaya(ili, 2)
    otvet = ekv_ok and ili_ok and not lineinaya(impl, 2)
    return otvet


# summa_D4: сумма трёх битов — A ⊕ B ⊕ C одной строкой; в СДНФ — 4 слагаемых
def summa_D4():
    summa = lambda a, b, c: (a + b + c) % 2
    otvet = koefficienty(summa, 3) == [(0,), (1,), (2,)] and sum(summa(*n) for n in nabory(3)) == 4
    return otvet


# registr: регистр сдвига из 4 ячеек, новый бит = первая ⊕ последняя; выход — первые k битов
def registr(sostoyanie, k):
    yachejki = list(sostoyanie)
    otvet = []
    for _ in range(k):
        otvet.append(yachejki[-1])
        novyj = xor(yachejki[0], yachejki[-1])
        yachejki = [novyj] + yachejki[:-1]
    return otvet


# period: через сколько шагов регистр с отводами (u, v) вернётся в начальное состояние
def period(sostoyanie, u, v):
    yachejki = tuple(sostoyanie)
    shag = 0
    while shag == 0 or yachejki != tuple(sostoyanie):
        yachejki = (xor(yachejki[u], yachejki[v]),) + yachejki[:-1]
        shag = shag + 1
    otvet = shag
    return otvet


# registr_D4: выход 000111101011001, период 15; отводы 2 и 4 — период 6; из 0000 — одни нули
def registr_D4():
    vyhod = "".join(map(str, registr((1, 0, 0, 0), 15))) == "000111101011001"
    periody = period((1, 0, 0, 0), 0, 3) == 15 and period((1, 0, 0, 0), 1, 3) == 6
    zadacha = registr((0, 0, 0, 1), 8) == [1, 0, 0, 0, 1, 1, 1, 1]
    otvet = vyhod and periody and zadacha and registr((0, 0, 0, 0), 20) == [0] * 20
    return otvet

# proverki: все проверки шага Д — имя и результат
def proverki():
    otvet = {
        "Д.1 законы ⊕": zakony_D1(),
        "Д.1 контрпримеры": kontr_D1(),
        "Д.2–Д.3 примеры": primery_D2_D3(),
        "Д.2–Д.3 все функции 2 и 3 переменных": vse_16_D(),
        "Д.2–Д.3 контрпримеры": kontr_D2_D3(),
        "Д.4 линейность": lineinost_D4(),
        "Д.4 сумма одной строкой": summa_D4(),
        "Д.4 регистр сдвига": registr_D4(),
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
