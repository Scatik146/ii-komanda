"""Проверка шага В: что собирается из набора действий и в каких классах Поста он лежит.
Функции двух букв — векторы из 4 бит в порядке строк 00, 01, 10, 11.
Запуск: python3 proverka_bazisov.py"""
import sys
from itertools import product

X, Y = (0, 0, 1, 1), (0, 1, 0, 1)
NOL, EDINICA = (0, 0, 0, 0), (1, 1, 1, 1)

# действия: имя → функция двух бит (НЕ берёт только первый)
DEJSTVIYA = {
    "¬": lambda a, b: 1 - a,
    "∧": lambda a, b: a & b,
    "∨": lambda a, b: a | b,
    "→": lambda a, b: (1 - a) | b,
    "⊕": lambda a, b: a ^ b,
    "≡": lambda a, b: 1 - (a ^ b),
    "|": lambda a, b: 1 - (a & b),
    "↓": lambda a, b: 1 - (a | b),
}


# primenit: действие к двум векторам — новый вектор
def primenit(imya, u, v):
    vektor = tuple(DEJSTVIYA[imya](a, b) for a, b in zip(u, v))
    return vektor


# shag: всё, что получается одним действием из уже собранного
def shag(sobrano, nabor):
    novye = {primenit(d, u, v) for d in nabor for u in sobrano for v in sobrano}
    return sobrano | novye


# zamykanie: собираем, пока появляется новое
def zamykanie(nabor, konstanty=()):
    sobrano = {X, Y, *konstanty}
    sleduyushchee = shag(sobrano, nabor)
    while sleduyushchee != sobrano:
        sobrano, sleduyushchee = sleduyushchee, shag(sleduyushchee, nabor)
    return sobrano


# polnyj: из набора собираются все 16 функций двух букв
def polnyj(nabor, konstanty=()):
    da = len(zamykanie(nabor, konstanty)) == 16
    return da


# bazis: полна, и без любого действия уже не полна (по Алексееву, 2004)
def bazis(nabor, konstanty=()):
    bez_odnogo = [nabor.replace(d, "") for d in nabor]
    da = polnyj(nabor, konstanty) and not any(polnyj(n, konstanty) for n in bez_odnogo)
    return da


if __name__ == "__main__":
    for nabor, k in [("¬∧∨", ()), ("¬∧", ()), ("¬∨", ()), ("∧∨", ()), ("¬", ()),
                     ("|", ()), ("↓", ()), ("→¬", ()), ("→", (NOL,)), ("→", ()),
                     ("∧⊕", (EDINICA,)), ("∧⊕", ()), ("⊕≡¬", ())]:
        print(nabor, "+".join("0" if c == NOL else "1" for c in k), len(zamykanie(nabor, k)), polnyj(nabor, k), bazis(nabor, k))
    sys.exit(0)
