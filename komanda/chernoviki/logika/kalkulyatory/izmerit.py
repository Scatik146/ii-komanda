"""izmerit.py — строим узлы обоих калькуляторов нужной ширины, проверяем на числах, считаем цену и время.

Ширины — из задачи (BitNet b1.58: веса −1, 0, 1; активации int8; сумма K произведений):
короткое слово вмещает −128…127, длинное — ±128·K. Наименьшее число цифр, которого хватает, считает программа.
Цена: вентили и транзисторы (условие: вентиль Т-КМОП по транзисторам как двоичный того же вида, ворота — 4).
Время: глубина в вентилях (условие: вентиль троичный не медленнее двоичного — иначе умножить на m).
"""
import random
import numpy as np
from shema import Shema, DVOICHNYJ, TROICHNYJ, podschet, vychislit, i_
from uzly import volna, bystryj, slovo
from umnozhenie import cifry, chislo, umnozhitel, mac_polnyj, mac_sohranyayushchij

K = 4096
TRANZISTORY = {DVOICHNYJ: {'НЕ': 2, 'И': 6, 'ИЛИ': 6}, TROICHNYJ: {'НЕ': 2, 'И': 6, 'ИЛИ': 6, 'ворота': 4, 'цикл': 4}}
PROB = 3000
random.seed(23112026)


# vmeshchaet: n цифр вмещают все числа lo…hi (двоичный — дополнительный код, троичный — симметричный)
def vmeshchaet(baza, n, lo, hi):
    niz, verh = (-2 ** (n - 1), 2 ** (n - 1) - 1) if baza == DVOICHNYJ else (-(3 ** n - 1) // 2, (3 ** n - 1) // 2)
    return niz <= lo and hi <= verh


# shirina: наименьшее число цифр, вмещающее lo…hi
def shirina(baza, lo, hi):
    n = 1
    while not vmeshchaet(baza, n, lo, hi):
        n += 1
    return n


# proizv_cifr: произведение цифр: И у битов, найденная запись у тритов
def proizv_cifr(s, x, y):
    return i_(s, x, y) if s.baza == DVOICHNYJ else slovo(s, 'произведение', x, y)


# cena_uzla: (вентили, транзисторы, глубина) выходов
def cena_uzla(s, vyhody):
    vidy, glubina = podschet(s, vyhody)
    tranz = sum(TRANZISTORY[s.baza][v] * k for v, k in vidy.items())
    return {'вентили': sum(vidy.values()), 'транзисторы': tranz, 'глубина': glubina, 'виды': vidy}


# vhody_slova: n входов-цифр
def vhody_slova(s, n):
    return [s.vhod() for _ in range(n)]


# podat: значения входов слова для массива чисел
def podat(baza, slovo_vh, chisla, n):
    return dict(zip(slovo_vh, cifry(baza, chisla, n)))


# sluchajnye: PROB чисел в −m…m
def sluchajnye(m):
    return np.array([random.randint(-m, m) for _ in range(PROB)])


# po_modulyu: число, как его покажут n цифр (переполнение по кругу)
def po_modulyu(baza, x, n):
    return chislo(baza, cifry(baza, x, n))


# uzel_slozheniya: сумматор n цифр (волна или быстрый), проверка на случайных
def uzel_slozheniya(baza, n, vid):
    s = Shema(baza)
    a, b = vhody_slova(s, n), vhody_slova(s, n)
    rez = vid(s, a, b)
    m = (2 ** (n - 2) - 1 if baza == DVOICHNYJ else (3 ** n - 1) // 4)  # 24.11: было 2^(n−2) — сумма 2^(n−1) переполняла слово
    x, y = sluchajnye(m), sluchajnye(m)
    vyh = vychislit(s, {**podat(baza, a, x, n), **podat(baza, b, y, n)}, rez)
    assert np.all(chislo(baza, vyh) == x + y), (baza, n, vid.__name__)
    return cena_uzla(s, rez)


# uzel_umnozheniya: n × n → 2n цифр, проверка
def uzel_umnozheniya(baza, n):
    s = Shema(baza)
    a, b = vhody_slova(s, n), vhody_slova(s, n)
    rez = umnozhitel(s, a, b, proizv_cifr)
    m = (2 ** (n - 1) - 1 if baza == DVOICHNYJ else (3 ** n - 1) // 2)
    x, y = sluchajnye(m), sluchajnye(m)
    vyh = vychislit(s, {**podat(baza, a, x, n), **podat(baza, b, y, n)}, rez)
    assert np.all(chislo(baza, vyh) == x * y), (baza, n)
    return cena_uzla(s, rez)


# vhody_vesa: вес: два бита (не ноль, минус) или один трит; и их значения для массива весов
def vhody_vesa(s, w):
    if s.baza == DVOICHNYJ:
        z, m = s.vhod(), s.vhod()
        rez = ((z, m), {z: (w != 0).astype(int), m: (w < 0).astype(int)})
    else:
        t = s.vhod()
        rez = (t, {t: w})
    return rez


# dannye_maca: случайные активации, веса −1/0/1 и суммы (|сумма| < 128·(K−1), чтобы шаг не переполнял)
def dannye_maca():
    vesa = np.array([random.choice((-1, 0, 1)) for _ in range(PROB)])
    return (sluchajnye(127), vesa, sluchajnye(128 * (K - 1)))


# shag_maca: схема шага MAC → (схема, выходы, значения входов, что должно выйти)
def shag_maca(baza, nk, nd, polnyj):
    s, (a, w, acc) = Shema(baza), dannye_maca()
    x, sm, sc = vhody_slova(s, nk), vhody_slova(s, nd), vhody_slova(s, nd)
    ves, zn_vesa = vhody_vesa(s, w)
    zn = {**podat(baza, x, a, nk), **podat(baza, sm, acc, nd), **podat(baza, sc, 0 * acc, nd), **zn_vesa}
    rez = mac_polnyj(s, sm, x, ves, proizv_cifr) if polnyj else \
        sum(mac_sohranyayushchij(s, sm, sc, x, ves, proizv_cifr), [])
    return (s, rez, zn, acc + w * a)


# uzel_maca: шаг MAC (полный — быстрым сумматором; хранящий — строкой сумматоров 3 → 2), проверка
def uzel_maca(baza, nk, nd, polnyj):
    s, rez, zn, nado = shag_maca(baza, nk, nd, polnyj)
    vyh = vychislit(s, zn, rez)
    poluch = chislo(baza, vyh) if polnyj else chislo(baza, vyh[:nd]) + chislo(baza, vyh[nd:])
    assert np.all(po_modulyu(baza, poluch, nd) == po_modulyu(baza, nado, nd)), (baza, polnyj)
    return cena_uzla(s, rez)
