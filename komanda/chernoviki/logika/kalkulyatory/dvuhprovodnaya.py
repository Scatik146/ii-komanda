"""dvuhprovodnaya.py — наша логика тритов на двоичной машине «двумя проводами» против троичной машины.

Трит на битах: (p, n): 1 → (1, 0), 0 → (0, 0) «не знаю», −1 → (0, 1).
И = (p∧p′, n∨n′); ИЛИ = (p∨p′, n∧n′); НЕ = (n, p) — провода местами, даром; ворота(x) = (p, ¬p).
Считаем вентили и транзисторы слов книги на обеих машинах; проверка — все 9 пар значений.
"""
import itertools
import numpy as np
import shema
from shema import Shema, DVOICHNYJ, TROICHNYJ, podschet, vychislit, ne, i_, ili
from izmerit import TRANZISTORY

T = (-1, 0, 1)


# d_i: И на двух проводах (слова базиса — d_i, d_ili, d_ne, d_vorota)
def d_i(s, x, y):
    return (i_(s, x[0], y[0]), ili(s, x[1], y[1]))


# d_ili: ИЛИ на двух проводах
def d_ili(s, x, y):
    return (ili(s, x[0], y[0]), i_(s, x[1], y[1]))


# d_ne: НЕ — поменять провода
def d_ne(s, x):
    return (x[1], x[0])


# d_vorota: ворота — «да» только из «да»
def d_vorota(s, x):
    return (x[0], ne(s, x[0]))


# d_nol: число 0 — оба провода «нет»
def d_nol(s):
    return (s.konst(0), s.konst(0))


# SLOVA_KNIGI: слова через И, ИЛИ, НЕ, ворота, 0 — одна запись для обеих машин (k — набор действий)
SLOVA_KNIGI = {
    'И': lambda k, x, y: k['И'](x, y),
    'НЕ': lambda k, x, y: k['НЕ'](x),
    'ИЛИ': lambda k, x, y: k['ИЛИ'](x, y),
    'ворота': lambda k, x, y: k['ворота'](x),
    'согласие': lambda k, x, y: k['ИЛИ'](k['И'](x, y), k['И'](k['ИЛИ'](x, y), k['0']())),
    'подтвердить': lambda k, x, y: k['ИЛИ'](x, k['И'](y, k['0']())),
    'оба точно': lambda k, x, y: k['И'](k['ворота'](x), k['ворота'](y)),
    'не знаю?': lambda k, x, y: k['И'](k['НЕ'](k['ворота'](x)), k['НЕ'](k['ворота'](k['НЕ'](x)))),
}


# nabor: действия для машины: троичная — вентили, двоичная — два провода
def nabor(s):
    if s.baza == TROICHNYJ:
        k = {'И': lambda x, y: i_(s, x, y), 'ИЛИ': lambda x, y: ili(s, x, y), 'НЕ': lambda x: ne(s, x),
             'ворота': lambda x: s.ventil('ворота', x), '0': lambda: s.konst(0)}
    else:
        k = {'И': lambda x, y: d_i(s, x, y), 'ИЛИ': lambda x, y: d_ili(s, x, y), 'НЕ': lambda x: d_ne(s, x),
             'ворота': lambda x: d_vorota(s, x), '0': lambda: d_nol(s)}
    return k


# v_provoda: значения трита → (p, n)
def v_provoda(v):
    return ((v == 1).astype(int), (v == -1).astype(int))


# izmerit_slovo: (транзисторы, глубина) слова на машине; проверка по 9 парам
def izmerit_slovo(baza, imya):
    s = Shema(baza)
    xs, ys = (np.array(c) for c in zip(*itertools.product(T, T)))
    x, y = ((s.vhod(), s.vhod()), (s.vhod(), s.vhod())) if baza == DVOICHNYJ else (s.vhod(), s.vhod())
    v = SLOVA_KNIGI[imya](nabor(s), x, y)
    vyh = list(v) if baza == DVOICHNYJ else [v]
    zn = {**dict(zip(x, v_provoda(xs))), **dict(zip(y, v_provoda(ys)))} if baza == DVOICHNYJ else {x: xs, y: ys}
    r = vychislit(s, zn, vyh)
    poluch = r[0] - r[1] if baza == DVOICHNYJ else r[0]
    nado = SLOVA_KNIGI[imya](OBRAZEC, xs, ys)
    assert np.all(poluch == nado), (baza, imya)
    vidy, gl = podschet(s, vyh)
    return (sum(TRANZISTORY[baza][k] * c for k, c in vidy.items()), gl)


# OBRAZEC: те же слова над числами (как в книге)
OBRAZEC = {'И': np.minimum, 'ИЛИ': np.maximum, 'НЕ': lambda x: -x, 'ворота': lambda x: np.where(x == 1, 1, -1),
           '0': lambda: 0}


# glavnoe: таблица слов
def glavnoe():
    shema.NASTROJKA['ИЛИ у тритов'] = True
    print('слово: двоичный «два провода» (транзисторы / глубина) | троичный | двоичный/троичный по транзисторам')
    for imya in SLOVA_KNIGI:
        d, t = izmerit_slovo(DVOICHNYJ, imya), izmerit_slovo(TROICHNYJ, imya)
        print(f'  {imya:12} {d[0]:4} / {d[1]} | {t[0]:4} / {t[1]} | ×{d[0] / t[0] if t[0] else 0:.2f}')
    return None


if __name__ == '__main__':
    glavnoe()
