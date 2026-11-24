"""smeshannyj_umnozhitel.py — умножитель смешанной машины (основание 2, цифры −1, 0, 1) из вентилей базиса книги.

Вход и выход — обычные двоичные числа (дополнительный код, n = 21 бит, как двоичный умножитель в rezultat.txt):
  1) вход даром: биты 0 / 1 — уже цифры; минус веса старшего бита дополнительного кода — знаком произведений;
  2) частичные произведения — И (на {0, 1} меньшее = двоичное И) и НЕ (−x) для знака: двоичное внутри нашего;
  3) строки складываются попарно деревом сумматоров без цепочки переносов (smeshannyj_summator);
  4) вывод: плюсы и минусы — воротами (ответ только −1 или 1: биты внутри тритов), затем P − M = P + ¬M + 1
     обычным двоичным быстрым сумматором (Склански), собранным из И, ИЛИ, НЕ на −1 и 1 (углы таблиц книги, А.1).
Проверка: случайные множители, ответ = x · y. Варианты А и Б (ИЛИ как деталь). Запуск: python3 smeshannyj_umnozhitel.py
"""
import random
import numpy as np
import shema
from shema import Shema, TROICHNYJ, vychislit, ne, i_, ili
from uzly import po_tablice
from izmerit import cena_uzla
from smeshannyj_summator import razryad, tablica_tw, tablica_cifry

N = 21
PROB = 2000
random.seed(24112026)


# slozhit_sd: x + y без цепочки переносов, длина слова L (лишний старший перенос отбрасываем: счёт по модулю 2^L)
def slozhit_sd(s, x, y):
    tab_t, tab_w, tab_c = tablica_tw(0), tablica_tw(1), tablica_cifry()
    nol, d = s.konst(0), len(x)
    t, w = [nol], []
    for i in range(d):
        xn, yn = (x[i - 1], y[i - 1]) if i > 0 else (nol, nol)
        ti, wi = razryad(s, x[i], y[i], xn, yn, tab_t, tab_w)
        t.append(ti)
        w.append(wi)
    return [po_tablice(s, [w[i], t[i]], tab_c) for i in range(d)]


# cifra_proizv: a_i · b_j, когда на входе биты 0 / 1: И (меньшее) на {0, 1} — это двоичное И; у старшего бита вес
# с минусом — знак произведения НЕ (−x), если ровно один из двух разрядов старший (как Бо — Вули, но без поправок)
def cifra_proizv(s, x, y, minus):
    rez = i_(s, x, y)
    if minus:
        rez = ne(s, rez)
    return rez


# stroki: частичные произведения: строка j — a_i · b_j со сдвигом j, длина 2n
def stroki(s, a, b):
    nol, rez, n = s.konst(0), [], len(a)
    for j in range(n):
        st = [nol] * (2 * n)
        for i in range(n):
            st[i + j] = cifra_proizv(s, a[i], b[j], (i == n - 1) != (j == n - 1))
        rez.append(st)
    return rez


# derevo: строки попарно складываются, пока не останется одна
def derevo(s, spisok):
    while len(spisok) > 1:
        nov = [slozhit_sd(s, spisok[k], spisok[k + 1]) for k in range(0, len(spisok) - 1, 2)]
        if len(spisok) % 2 == 1:
            nov.append(spisok[-1])
        spisok = nov
    return spisok[0]


# xor_bit: a ⊕ b на битах −1 / 1: (a ∨ b) ∧ ¬(a ∧ b)
def xor_bit(s, a, b):
    return i_(s, ili(s, a, b), ne(s, i_(s, a, b)))


# sklanski: двоичный быстрый сумматор на битах −1 / 1 с входным переносом 1 → биты суммы (по модулю 2^L)
def sklanski(s, a, b):
    g = [i_(s, x, y) for x, y in zip(a, b)]
    p = [xor_bit(s, x, y) for x, y in zip(a, b)]
    g[0] = ili(s, g[0], p[0])
    G, P, shag = list(g), list(p), 1
    while shag < len(a):
        for i in range(len(a)):
            if (i // shag) % 2 == 1:
                lo = (i // shag) * shag - 1
                G[i] = ili(s, G[i], i_(s, P[i], G[lo]))
                P[i] = i_(s, P[i], P[lo])
        shag *= 2
    vhod = [s.konst(1)] + G[:-1]
    return [xor_bit(s, p[i], vhod[i]) for i in range(len(a))]


# v_dvoichnoe: цифры → биты: P + ¬M + 1; плюсы и минусы — ворота (биты внутри тритов)
def v_dvoichnoe(s, cifry):
    plus = [s.ventil('ворота', c) for c in cifry]
    ne_minus = [ne(s, s.ventil('ворота', ne(s, c))) for c in cifry]
    return sklanski(s, plus, ne_minus)


# umnozhitel: a × b → 2n битов (−1 / 1)
def umnozhitel(s, a, b):
    return v_dvoichnoe(s, derevo(s, stroki(s, a, b)))


# vhod_cifry: числа → биты n-битного дополнительного кода 0 / 1 (минус старшего веса — в знаке произведений)
def vhod_cifry(chisla):
    rez, x = [], np.array(chisla) % (2 ** N)
    for i in range(N):
        rez.append((x >> i) & 1)
    return rez


# chislo_bitov: биты −1 / 1 (2n) → число дополнительного кода
def chislo_bitov(bity):
    b = [(np.array(v) + 1) // 2 for v in bity]
    u = sum(b[i].astype(object) * 2 ** i for i in range(len(b)))
    return np.where(b[-1] == 1, u - 2 ** len(b), u)


# izmerit: строит, проверяет на числах, цена
def izmerit():
    s = Shema(TROICHNYJ)
    a, b = [s.vhod() for _ in range(N)], [s.vhod() for _ in range(N)]
    vyh = umnozhitel(s, a, b)
    m = 2 ** (N - 1)
    x = [random.randint(-m, m - 1) for _ in range(PROB)]
    y = [random.randint(-m, m - 1) for _ in range(PROB)]
    zn = {**dict(zip(a, vhod_cifry(x))), **dict(zip(b, vhod_cifry(y)))}
    otvet = chislo_bitov(vychislit(s, zn, vyh))
    assert np.all(otvet == np.array(x, dtype=object) * np.array(y, dtype=object)), 'произведение неверно'
    return cena_uzla(s, vyh)


# glavnoe: варианты А и Б
def glavnoe():
    for imya in ('А', 'Б'):
        shema.NASTROJKA['ИЛИ у тритов'] = imya == 'Б'
        c = izmerit()
        print(f'ВАРИАНТ {imya}: смешанный умножитель {N}×{N} → {2 * N} бит: транзисторы {c["транзисторы"]}, '
              f'глубина {c["глубина"]}, вентили {c["вентили"]}; проверено на {PROB} парах')


if __name__ == '__main__':
    glavnoe()
