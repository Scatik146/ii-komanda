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


# вектор каждого действия и константы (НЕ — от первой буквы)
VEKTORY = {d: primenit(d, X, Y) for d in DEJSTVIYA}
VEKTORY.update({"0": NOL, "1": EDINICA})

# классы Поста на векторе 00, 01, 10, 11
KLASSY = {
    "T0": lambda v: v[0] == 0,
    "T1": lambda v: v[3] == 1,
    "S": lambda v: all(v[i] == 1 - v[3 - i] for i in range(4)),
    "M": lambda v: v[0] <= v[1] <= v[3] and v[0] <= v[2] <= v[3],
    "L": lambda v: v[0] ^ v[1] ^ v[2] ^ v[3] == 0,
}


# v_klasse: действие или константа лежит в классе
def v_klasse(imya, klass):
    da = KLASSY[klass](VEKTORY[imya])
    return da


# post: набор не лежит целиком ни в одном классе (теорема Поста)
def post(nabor):
    da = all(any(not v_klasse(d, k) for d in nabor) for k in KLASSY)
    return da


# polnyj_nabor: замыкание набора, где цифры — константы
def polnyj_nabor(nabor):
    dejstviya = "".join(d for d in nabor if d in DEJSTVIYA)
    konstanty = tuple(VEKTORY[d] for d in nabor if d in "01")
    da = polnyj(dejstviya, konstanty)
    return da


# teorema_sovpadaet: для всех 1023 наборов Пост = прямая сборка
def teorema_sovpadaet():
    imena = list(VEKTORY)
    nabory = [[d for d, vzyat in zip(imena, maska) if vzyat]
              for maska in product((0, 1), repeat=len(imena)) if any(maska)]
    rashozhdeniya = [n for n in nabory if post(n) != polnyj_nabor(n)]
    return len(nabory), rashozhdeniya


if __name__ == "__main__":
    for nabor, k in [("¬∧∨", ()), ("¬∧", ()), ("¬∨", ()), ("∧∨", ()), ("¬", ()),
                     ("|", ()), ("↓", ()), ("→¬", ()), ("→", (NOL,)), ("→", ()),
                     ("∧⊕", (EDINICA,)), ("∧⊕", ()), ("⊕≡¬", ())]:
        print(nabor, "+".join("0" if c == NOL else "1" for c in k), len(zamykanie(nabor, k)), polnyj(nabor, k), bazis(nabor, k))
    for d in VEKTORY:
        print(d, "".join("+" if v_klasse(d, k) else "−" for k in KLASSY))
    vsego, rashozhdeniya = teorema_sovpadaet()
    print(f"теорема Поста: наборов {vsego}, расхождений {len(rashozhdeniya)}")
    sys.exit(1 if rashozhdeniya else 0)
