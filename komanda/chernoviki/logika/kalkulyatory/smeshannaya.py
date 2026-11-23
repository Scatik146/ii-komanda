"""smeshannaya.py — смешанная машина: основание 2 (как у двоичной), цифры — триты −1, 0, 1 (как у нашей).

Задание учителя 24.11 02:57: решить задачу арифмометра как смесь двоичной и троичной логики, где двоичная —
подмножество нашей. Проверяет на числах:
  1) двоичное число (цифры 0, 1) — уже готовое число смешанной машины, переводить не надо;
  2) сложение без цепочки переносов: цифра суммы зависит только от своих разрядов i, i−1, i−2;
  3) обратный перевод в двоичное — одно обычное вычитание (плюсы минус минусы);
  4) шаги арифмометра (model.py) на умножение: двоичная, троичная и смешанная машины на одних числах.
Запуск: python3 smeshannaya.py
"""
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'arifmometr'))
import model  # noqa: E402  арифмометр: Mashina, umn_stolbik, srednee

N = 32
VYBORKA = 20000
random.seed(24112026)


# cifry: число → список цифр −1, 0, 1 по основанию 2 (младшая первой), запись без соседних ненулевых
def cifry(n):
    zapis = []
    while n != 0:
        c = 0
        if n % 2 == 1:
            c = 2 - (n % 4)
        zapis.append(c)
        n = (n - c) // 2
    return zapis


# chislo: список цифр → число
def chislo(zapis):
    s = 0
    for i, c in enumerate(zapis):
        s += c * 2 ** i
    return s


# dvoichnye: число ≥ 0 → его обычные биты 0, 1 (это тоже запись смешанной машины)
def dvoichnye(n):
    zapis = []
    while n > 0:
        zapis.append(n % 2)
        n //= 2
    return zapis


# dopolnit: дополняет запись нулями до длины d
def dopolnit(zapis, d):
    return zapis + [0] * (d - len(zapis))


# razlozhit: сумма разряда p (−2…2) и знак соседа снизу → (перенос наверх t, остаток w)
def razlozhit(p, snizu_ne_minus):
    t, w = 0, 0
    if p == 2 or p == -2:
        t = p // 2
    elif p != 0 and snizu_ne_minus:
        t, w = (p + 1) // 2, -1
    elif p != 0:
        t, w = (p - 1) // 2, 1
    return t, w


# slozhit: сложение без цепочки переносов; каждая цифра — по разрядам i, i−1, i−2
def slozhit(x, y):
    d = max(len(x), len(y)) + 1
    x, y = dopolnit(x, d), dopolnit(y, d)
    p = [x[i] + y[i] for i in range(d)]
    t, w = [0] * (d + 1), [0] * d
    for i in range(d):
        snizu = i == 0 or p[i - 1] >= 0
        t[i + 1], w[i] = razlozhit(p[i], snizu)
    return [w[i] + t[i] for i in range(d)] + [t[d]]


# v_dvoichnoe: запись → (плюсы, минусы) двумя двоичными словами; число = плюсы − минусы
def v_dvoichnoe(zapis):
    plus = chislo([1 if c == 1 else 0 for c in zapis])
    minus = chislo([1 if c == -1 else 0 for c in zapis])
    return plus, minus


# proverit_zapis: перевод туда и обратно и запись битов как запись машины
def proverit_zapis():
    oshibki = 0
    for n in range(-5000, 5001):
        if chislo(cifry(n)) != n:
            oshibki += 1
        if n >= 0 and chislo(dvoichnye(n)) != n:
            oshibki += 1
    return oshibki


# vse_cifry_trity: в записи суммы только −1, 0, 1
def vse_cifry_trity(zapis):
    return all(c in (-1, 0, 1) for c in zapis)


# sluchajnaya_zapis: случайная запись из N цифр −1, 0, 1
def sluchajnaya_zapis():
    return [random.choice((-1, 0, 1)) for _ in range(N)]


# proverit_slozhenie: все пары малых записей и выборка длинных
def proverit_slozhenie():
    oshibki = 0
    pary = [(cifry(a), cifry(b)) for a in range(-200, 201) for b in range(-200, 201)]
    pary += [(sluchajnaya_zapis(), sluchajnaya_zapis()) for _ in range(VYBORKA)]
    pary += [(dvoichnye(random.randrange(2 ** N)), dvoichnye(random.randrange(2 ** N))) for _ in range(VYBORKA)]
    for x, y in pary:
        s = slozhit(x, y)
        if chislo(s) != chislo(x) + chislo(y) or not vse_cifry_trity(s):
            oshibki += 1
    return oshibki, len(pary)


# proverit_vyvod: обратный перевод одним вычитанием
def proverit_vyvod():
    oshibki = 0
    for _ in range(VYBORKA):
        z = sluchajnaya_zapis()
        plus, minus = v_dvoichnoe(z)
        if plus - minus != chislo(z):
            oshibki += 1
    return oshibki


# Smeshannaya: арифмометр с основанием 2, но сдвиг вправо отдаёт цифру −1, 0, 1 (смотрит два младших разряда)
class Smeshannaya(model.Mashina):
    # __init__: основание 2
    def __init__(self):
        super().__init__(2)

    # vpravo: (x − c) / 2 и цифра c записи без соседних ненулевых
    def vpravo(self, x):
        self.ops += 1
        c = 0
        if x % 2 == 1:
            c = 2 - (x % 4)
        return ((x - c) // 2, c)


# umn_smesh: столбик по цифрам −1, 0, 1: прибавить, вычесть или пропустить; знак множителя не трогаем
def umn_smesh(m, a, b):
    rez = 0
    while b != 0:
        b, c = m.vpravo(b)
        if c == 1:
            rez = m.slozhit(rez, a)
        elif c == -1:
            rez = m.vychest(rez, a)
        if b != 0:
            a = m.vlevo(a)
    return rez


# srednee_smesh: средний счёт операций смешанной машины на выборке; ответ сверяется
def srednee_smesh(algoritm, pary, otvet):
    vsego = 0
    for x, y in pary:
        m = Smeshannaya()
        assert algoritm(m, x, y) == otvet(x, y), (x, y)
        vsego += m.ops
    return vsego / len(pary)


# arifmometr_umnozhenie: те же множители, что в model.py, три машины
def arifmometr_umnozhenie():
    random.seed(23112026)
    pary = [(random.randint(-2 ** 15, 2 ** 15 - 1), random.randint(-2 ** 15, 2 ** 15 - 1)) for _ in range(VYBORKA)]
    pro = lambda x, y: x * y  # noqa: E731
    dv = model.srednee(2, model.umn_stolbik, pary, pro)
    tr = model.srednee(3, model.umn_stolbik, pary, pro)
    sm = srednee_smesh(umn_smesh, pary, pro)
    return dv, tr, sm


# glavnoe: все проверки и сводка
def glavnoe():
    o_zap = proverit_zapis()
    o_sl, vsego = proverit_slozhenie()
    o_vyv = proverit_vyvod()
    dv, tr, sm = arifmometr_umnozhenie()
    print("ЗАПИСЬ: число ↔ цифры −1, 0, 1 и биты как запись, n от −5000 до 5000; ошибок:", o_zap)
    print("СЛОЖЕНИЕ без цепочки переносов (разряды i, i−1, i−2): пар", vsego, "; ошибок:", o_sl)
    print("ВЫВОД в двоичное = плюсы − минусы (одно вычитание), выборка", VYBORKA, "; ошибок:", o_vyv)
    print("УМНОЖЕНИЕ, шаги арифмометра (как model.py, 16 бит со знаком): двоичная %.1f, троичная %.1f, смешанная %.1f"
          % (dv, tr, sm))


if __name__ == '__main__':
    glavnoe()
