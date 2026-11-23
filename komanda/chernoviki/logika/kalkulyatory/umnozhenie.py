"""umnozhenie.py — умножитель и MAC (умножить и прибавить) для двух калькуляторов; числа ↔ цифры.

Двоичный: дополнительный код, частичные произведения Бо — Вули (знак — поправками и двумя единицами).
Троичный: симметричный код, частичное произведение — произведение тритов, знак даром.
Сжатие столбцов — Уоллес (сумматоры 3 → 2), в конце — быстрый сумматор.
MAC задачи (BitNet b1.58): вес −1, 0, 1, активация — короткое слово, сумма — длинное.
"""
import numpy as np
from shema import DVOICHNYJ, ne, i_
from uzly import summator, polusummator, bystryj


# --- числа и цифры (для проверки) ---------------------------------------------------------

# cifry: число → цифры младшими вперёд (n штук): двоичный — дополнительный код, троичный — симметричный
def cifry(baza, chislo, n):
    rez, x = [], np.array(chislo)
    for _ in range(n):
        c = x % 2 if baza == DVOICHNYJ else (x + 1) % 3 - 1
        rez.append(c)
        x = (x - c) // baza
    return rez


# chislo: цифры → число (двоичный: старший бит — со знаком минус)
def chislo(baza, cf):
    rez = sum(c * baza ** i for i, c in enumerate(cf))
    return rez - (cf[-1] * 2 ** len(cf) if baza == DVOICHNYJ else 0)


# --- умножение ------------------------------------------------------------------------------

# chastichnye: столбцы частичных произведений n × n (вес столбца = основание^номер)
def chastichnye(s, a, b, cifra_proizv):
    n = len(a)
    stolby = [[] for _ in range(2 * n)]
    for i in range(n):
        for j in range(n):
            pp = cifra_proizv(s, a[i], b[j])
            pp = ne(s, pp) if s.baza == DVOICHNYJ and (i == n - 1) != (j == n - 1) else pp
            stolby[i + j].append(pp)
    if s.baza == DVOICHNYJ:
        stolby[n].append(s.konst(1))
        stolby[2 * n - 1].append(s.konst(1))
    return stolby


# shag_uollesa: каждый столбец тройками — в сумматор (сумма — сюда, перенос — в следующий)
def shag_uollesa(s, stolby):
    novye = [[] for _ in stolby]
    for k, st in enumerate(stolby):
        i = 0
        while len(st) - i >= 3:
            cifra, p = summator(s, *st[i:i + 3])
            novye[k].append(cifra)
            novye[k + 1].append(p) if k + 1 < len(novye) else None
            i += 3
        novye[k] += st[i:]
    return novye


# szhat: пока в столбце больше двух цифр — шаг Уоллеса; потом две строки → быстрый сумматор
def szhat(s, stolby):
    while max(len(st) for st in stolby) > 2:
        stolby = shag_uollesa(s, stolby)
    nol = s.konst(0)
    a = [st[0] if st else nol for st in stolby]
    b = [st[1] if len(st) > 1 else nol for st in stolby]
    return bystryj(s, a, b)


# umnozhitel: a × b (n цифр каждое) → 2n цифр
def umnozhitel(s, a, b, cifra_proizv):
    return szhat(s, chastichnye(s, a, b, cifra_proizv))


# --- MAC задачи -----------------------------------------------------------------------------

# term_bitnet: вклад w·x цифрами длинного слова; двоичный вес — (не ноль z, минус m): (x ⊕ m) ∧ z, перенос m ∧ z
def term_bitnet(s, x, ves, dlina, cifra_proizv):
    if s.baza == DVOICHNYJ:
        z, m = ves
        t = [i_(s, polusummator(s, c, m)[0], z) for c in x]
        rez = (t + [t[-1]] * (dlina - len(t)), i_(s, m, z))
    else:
        t = [cifra_proizv(s, c, ves) for c in x]
        rez = (t + [s.konst(0)] * (dlina - len(t)), None)
    return rez


# mac_polnyj: сумма := сумма + w·x (быстрым сумматором; задержка одного шага)
def mac_polnyj(s, summa, x, ves, cifra_proizv):
    t, vhodnoj = term_bitnet(s, x, ves, len(summa), cifra_proizv)
    return bystryj(s, summa, t, vhodnoj)


# mac_sohranyayushchij: сумма держится двумя строками (s, c): шаг — строка сумматоров 3 → 2, без переноса по слову
def mac_sohranyayushchij(s, stroka_s, stroka_c, x, ves, cifra_proizv):
    t, vhodnoj = term_bitnet(s, x, ves, len(stroka_s), cifra_proizv)
    pary = [summator(s, a, b, c) for a, b, c in zip(stroka_s, stroka_c, t)]
    nizhnij = vhodnoj if vhodnoj is not None else s.konst(0)
    return ([p[0] for p in pary], [nizhnij] + [p[1] for p in pary[:-1]])
