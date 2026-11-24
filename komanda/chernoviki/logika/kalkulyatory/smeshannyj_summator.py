"""smeshannyj_summator.py — сумматор слова смешанной машины (основание 2, цифры −1, 0, 1) из вентилей базиса книги.

Цифра суммы i: бит g = «x_(i−1) + y_(i−1) ≥ 0» (только −1 или 1 — двоичное внутри нашего), затем перенос t и остаток w
по таблице книги (В.4, рецепт «по таблице») от x_i, y_i, g;
цифра = w_i + t_i — таблица двух тритов. Цепочки переносов нет: глубина не зависит от ширины.
Варианты: А — строго {И, НЕ, ворота, 0}; Б — и ИЛИ как деталь. Сравнение — с rezultat.txt (сложение, 21 бит / 13 тритов).
Проверка: случайные записи, ответ = x + y. Цена: транзисторы по izmerit.TRANZISTORY (условие, как в остальных счётах).
Запуск: python3 smeshannyj_summator.py
"""
import random
import numpy as np
import shema
from shema import Shema, TROICHNYJ, vychislit
from uzly import po_tablice, TRITY
from izmerit import cena_uzla

N = 21
PROB = 3000
random.seed(24112026)


# razlozhit: сумма разряда p и знак соседа снизу → (перенос t, остаток w); то же правило, что в smeshannaya.py
def razlozhit(p, snizu_ne_minus):
    t, w = 0, 0
    if p == 2 or p == -2:
        t = p // 2
    elif p != 0 and snizu_ne_minus:
        t, w = (p + 1) // 2, -1
    elif p != 0:
        t, w = (p - 1) // 2, 1
    return t, w


# tablica_tw: {(x, y, g): t или w}, g — бит внутри трита: 1 — снизу «не минус», −1 — «минус»; g = 0 не бывает
def tablica_tw(nomer):
    tab = {}
    for x in TRITY:
        for y in TRITY:
            for g in TRITY:
                tab[(x, y, g)] = razlozhit(x + y, g >= 0)[nomer]
    return tab


# tablica_znaka: {(x_низ, y_низ): g} — 1, если x_низ + y_низ ≥ 0, иначе −1 (ответ — только −1 или 1: двоичное внутри)
def tablica_znaka():
    return {(a, b): (1 if a + b >= 0 else -1) for a in TRITY for b in TRITY}


# tablica_cifry: {(w, t): цифра}; пары, которых не бывает (w + t = ±2), — всё равно трит (по кругу)
def tablica_cifry():
    return {(w, t): (w + t + 1) % 3 - 1 for w in TRITY for t in TRITY}


# razryad: t_(i+1), w_i: сначала бит g по соседу снизу, потом таблицы от (x, y, g)
def razryad(s, x, y, xn, yn, tab_t, tab_w):
    g = po_tablice(s, [xn, yn], tablica_znaka())
    vh = [x, y, g]
    return po_tablice(s, vh, tab_t), po_tablice(s, vh, tab_w)


# summator: слово x + y → N + 1 цифр
def summator(s, x, y):
    tab_t, tab_w, tab_c = tablica_tw(0), tablica_tw(1), tablica_cifry()
    nol = s.konst(0)
    t, w = [nol], []
    for i in range(N):
        xn, yn = (x[i - 1], y[i - 1]) if i > 0 else (nol, nol)
        ti, wi = razryad(s, x[i], y[i], xn, yn, tab_t, tab_w)
        t.append(ti)
        w.append(wi)
    return [po_tablice(s, [w[i], t[i]], tab_c) for i in range(N)] + [t[N]]


# sluchajnye_cifry: PROB записей по N цифр −1, 0, 1 (массив N × PROB)
def sluchajnye_cifry():
    return np.array([[random.choice(TRITY) for _ in range(PROB)] for _ in range(N)])


# chislo: цифры (массив) → числа
def chislo(cifry):
    return sum(cifry[i] * 2 ** i for i in range(len(cifry)))


# izmerit: строит, проверяет на числах, возвращает цену
def izmerit():
    s = Shema(TROICHNYJ)
    x, y = [s.vhod() for _ in range(N)], [s.vhod() for _ in range(N)]
    vyh = summator(s, x, y)
    cx, cy = sluchajnye_cifry(), sluchajnye_cifry()
    zn = {**dict(zip(x, cx)), **dict(zip(y, cy))}
    otvet = np.array(vychislit(s, zn, vyh))
    assert np.all(chislo(otvet) == chislo(cx) + chislo(cy)), 'сумма неверна'
    assert np.all(np.isin(otvet, TRITY)), 'не трит'
    return cena_uzla(s, vyh)


# glavnoe: варианты А и Б
def glavnoe():
    for imya in ('А', 'Б'):
        shema.NASTROJKA['ИЛИ у тритов'] = imya == 'Б'
        c = izmerit()
        print(f'ВАРИАНТ {imya}: смешанный сумматор {N} цифр: транзисторы {c["транзисторы"]}, глубина {c["глубина"]}, '
              f'вентили {c["вентили"]} {c["виды"]}; на разряд {c["транзисторы"] / N:.0f} тр.; проверено на {PROB} парах')


if __name__ == '__main__':
    glavnoe()
