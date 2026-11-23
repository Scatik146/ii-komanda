"""trit_na_bitah.py — трит на битах: симметричная троичная запись двумя двоичными словами (маска плюсов, маска минусов).

Считает, сколько операций двоичной машины (И, ИЛИ, ИСКЛЮЧАЮЩЕЕ ИЛИ, НЕ, сдвиг, проверка на ноль — каждая 1)
уходит на одно троичное сложение слова из 21 трита. Ответ сверяется с обычным сложением.
Запуск: python3 trit_na_bitah.py
"""
import random

N = 21
MASKA = (1 << N) - 1
random.seed(23112026)


# v_maski: число → (маска плюсов, маска минусов)
def v_maski(n):
    p = m = 0
    i = 0
    while n:
        c = ((n + 1) % 3) - 1
        p, m = p | ((c == 1) << i), m | ((c == -1) << i)
        n, i = (n - c) // 3, i + 1
    return p, m


# iz_masok: (плюсы, минусы) → число
def iz_masok(p, m):
    return sum(3 ** i * (((p >> i) & 1) - ((m >> i) & 1)) for i in range(N + 2))


# shag: одно поразрядное сложение без переноса → (цифра, перенос) и число двоичных операций
def shag(ap, an, bp, bn):
    pp, nn = ap & bp, an & bn
    est_n, est_p = an | bn, ap | bp
    dp = ((ap ^ bp) & ~est_n) | nn
    dn = ((an ^ bn) & ~est_p) | pp
    return (dp, dn, pp << 1, nn << 1), 13


# slozhit: троичное сложение масками: шаги, пока перенос не ноль; → (плюсы, минусы, операций)
def slozhit(ap, an, bp, bn):
    ops = 0
    while True:
        (ap, an, bp, bn), k = shag(ap, an, bp, bn)
        ops += k + 1
        if bp == 0 and bn == 0:
            return ap, an, ops


# glavnoe: средняя цена троичного сложения на битах
def glavnoe():
    vsego, gran = 0, (3 ** N - 1) // 2 // 2
    for _ in range(20000):
        x, y = random.randint(-gran, gran), random.randint(-gran, gran)
        p, m, ops = slozhit(*v_maski(x), *v_maski(y))
        assert iz_masok(p, m) == x + y
        vsego += ops
    print(f'троичное сложение 21 трита на двоичной машине: в среднем {vsego / 20000:.1f} двоичных операций '
          f'(против 1 у родного троичного и 1 у двоичного сложения 32 бит)')


glavnoe()
