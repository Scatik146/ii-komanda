"""smeshannyj_razryad.py — разряд сумматора без переносов, сокращённый: только действия двух тритов.

Разбор разряда (p = x + y; h — бит «x + y ≥ 0» у разряда снизу, только −1 или 1):
  остаток w = −h, если p нечётно, иначе 0;   перенос t = U(x, y), если h = 1, иначе D(x, y);
  выбор по биту: t = (U ∧ h) ∨ (D ∧ ¬h) — на h = ±1 это ровно «если — то» (двоичное внутри нашего);
  цифра суммы = w + t (бывает только −1, 0, 1).
Записи H, U, D, W — самые короткие перебором (poisk.py, потолок 13); O и цифра суммы короче 14 не нашлись —
по таблице книги (В.4). Каждая запись сверяется по 9 клеткам.
Запуск: python3 smeshannyj_razryad.py — цена разряда и сверка с прежним (smeshannyj_summator.razlozhit).
"""
import numpy as np
from shema import Shema, TROICHNYJ, vychislit, ne, i_, ili, podschet
from uzly import po_tablice, TRITY
from poisk import najti_s_propuskami, postroit, KLETKI

POTOLOK = 13


# vektor: функция двух тритов → вектор 9 клеток (None — всё равно)
def vektor(f):
    return tuple(f(x, y) for x, y in KLETKI)


# DEJSTVIYA: что нужно разряду; функции двух тритов
DEJSTVIYA = {
    'H': lambda x, y: 1 if x + y >= 0 else -1,
    'U': lambda x, y: 1 if x + y >= 1 else (-1 if x + y == -2 else 0),
    'D': lambda x, y: 1 if x + y == 2 else (-1 if x + y <= -1 else 0),
    'O': lambda x, y: 1 if (x + y) % 2 else -1,
    'W': lambda o, h: None if o == 0 or h == 0 else (-h if o == 1 else 0),
    'S': lambda w, t: None if abs(w + t) > 1 else w + t,
}


# polnaya_tablica: для рецепта книги пропуски заполняем: W — 0, S — по кругу
def polnaya_tablica(imya):
    f, tab = DEJSTVIYA[imya], {}
    for a in TRITY:
        for b in TRITY:
            v = f(a, b)
            if v is None:
                v = 0 if imya == 'W' else (a + b + 1) % 3 - 1
            tab[(a, b)] = v
    return tab


# ZAPISI: найденные записи (или None — тогда по таблице)
ZAPISI = {imya: najti_s_propuskami(vektor(f), POTOLOK) for imya, f in DEJSTVIYA.items()}


# dejstvie: узел действия imya над (a, b): найденная запись или рецепт таблицы
def dejstvie(s, imya, a, b):
    z = ZAPISI[imya]
    rez = None
    if z is not None:
        rez = postroit(s, z[1], a, b)
    else:
        rez = po_tablice(s, [a, b], polnaya_tablica(imya))
    return rez


# razryad: (перенос наверх t_(i+1), остаток w_i) по x, y и соседу снизу xn, yn
def razryad(s, x, y, xn, yn, *_):
    h = dejstvie(s, 'H', xn, yn)
    o = dejstvie(s, 'O', x, y)
    w = dejstvie(s, 'W', o, h)
    t = ili(s, i_(s, dejstvie(s, 'U', x, y), h), i_(s, dejstvie(s, 'D', x, y), ne(s, h)))
    return t, w


# cifra: цифра суммы w + t
def cifra(s, w, t):
    return dejstvie(s, 'S', w, t)


# sverit: все 81 набор (x, y, xn, yn) против прежнего разложения; цена разряда
def sverit():
    from smeshannyj_summator import razlozhit
    s = Shema(TROICHNYJ)
    vh = [s.vhod() for _ in range(4)]
    t, w = razryad(s, *vh)
    nabory = [(a, b, c, d) for a in TRITY for b in TRITY for c in TRITY for d in TRITY]
    zn = {vh[k]: np.array([n[k] for n in nabory]) for k in range(4)}
    tv, wv = vychislit(s, zn, [t, w])
    nado = [razlozhit(n[0] + n[1], n[2] + n[3] >= 0) for n in nabory]
    assert list(tv) == [p[0] for p in nado] and list(wv) == [p[1] for p in nado], 'разряд неверен'
    return podschet(s, [t, w])


if __name__ == '__main__':
    for imya, z in ZAPISI.items():
        print(imya, 'перебор: %d вентилей' % z[0] if z else 'по таблице книги')
    print('разряд (t, w): вентили и глубина', sverit())
