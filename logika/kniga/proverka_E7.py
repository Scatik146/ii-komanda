# proverka_E7.py — проверка примеров Е.7 «Следует» (часть 2)
# запуск: python3 logika/kniga/proverka_E7.py
# Значения: -1 нет, 0 не знаю, 1 да.
from itertools import product

# Данные.
TRITY = (-1, 0, 1)
BIT = (-1, 1)
KLASS = 25                                               # список класса из журнала
PACHKA = 23                                              # листков согласия в пачке, на всех «согласен»
PROEKT = [(True, True)] * 18 + [(False, True)] * 3 + [(False, False)] * 4   # (вовремя, пять) - по журналу
RANSHE = [False] * 25                                    # сдал на неделю раньше - никто


# Слова нижнего уровня.
def ne(x):
    otvet = -x
    return otvet


def i_(x, y):
    otvet = min(x, y)
    return otvet


def ili(x, y):                                           # ИЛИ = ¬(¬x ∧ ¬y)
    otvet = ne(i_(ne(x), ne(y)))
    return otvet


def soglasie(x, y):                                      # одинаково - значение, разное - 0
    otvet = x if x == y else 0
    return otvet


def osnovanie(x, b):                                     # (x ∧ b) ∨ (¬b ∧ 0)
    otvet = ili(i_(x, b), i_(ne(b), 0))
    return otvet


def est_li(n, p):                                        # н ∨ (¬п ∧ 0)
    otvet = ili(n, i_(ne(p), 0))
    return otvet


def nashel(spisok):                                      # нашлось ли в просмотренном: 1 или -1
    otvet = 1 if any(spisok) else -1
    return otvet


def soglasie_vseh(znacheniya):
    otvet = znacheniya[0]
    for x in znacheniya[1:]:
        otvet = soglasie(otvet, x)
    return otvet


def neotvratimo(znacheniya, polnyj):                     # основание(согласие всех вариантов, полный)
    otvet = osnovanie(soglasie_vseh(znacheniya), polnyj)
    return otvet


def vektor2(f):
    otvet = [f(x, y) for x in TRITY for y in TRITY]
    return otvet


# Слова Е.7.
def dlya_vseh(k, p):                                     # ОЧ-24: к - нашёл ли контрпример
    otvet = ne(est_li(k, p))
    return otvet


def sleduet(vx, k, vy):                                  # ОЧ-23: Брусенцов - три вопроса
    otvet = i_(vx, i_(ne(k), vy))
    return otvet


def strelka(x, y):                                       # для сравнения: ¬x ∨ y у каждого
    otvet = ili(ne(x), y)
    return otvet


def tri_voprosa(lyudi, polnyj):                          # lyudi: (x, y) у каждого; ответы - через «есть ли»
    vx = est_li(nashel([x for x, y in lyudi]), polnyj)
    k = est_li(nashel([x and not y for x, y in lyudi]), polnyj)
    vy = est_li(nashel([y for x, y in lyudi]), polnyj)
    otvet = (vx, k, vy)
    return otvet


# Проверки.
# 1. ОЧ-24: для всех = ¬есть ли
assert vektor2(dlya_vseh) == [0, 0, 1, 0, 0, 0, -1, -1, -1]
assert dlya_vseh(-1, 1) == 1                             # по списку класса у всех галочки
assert dlya_vseh(1, 0) == -1                             # одна фамилия без галочки - сразу −1
pachka = [False] * PACHKA                                # отказов в пачке нет
assert dlya_vseh(nashel(pachka), -1) == 0                # пачка - не список класса: 0
assert dlya_vseh(nashel(pachka), -1) != 1                # контрпример: «пересмотрел всю пачку»
zhurnal = [False] * PACHKA + [True] * (KLASS - PACHKA)   # по журналу: две фамилии без листка
assert len(zhurnal) == KLASS and zhurnal.count(True) == 2
assert dlya_vseh(nashel(zhurnal), 1) == -1

# 2. Мостик: «неотвратимо будет» = «для всех вариантов - да»
spiskov = 0
for dlina in range(1, 5):
    for varianty in product(BIT, repeat=dlina):
        for p in TRITY:
            kontr = nashel([v != 1 for v in varianty])   # контрпример - вариант, где не да
            assert (neotvratimo(list(varianty), p) == 1) == (dlya_vseh(kontr, p) == 1)
            spiskov += 1
assert spiskov == 3 * (2 + 4 + 8 + 16)

# 3. ОЧ-23: следует - 27 наборов
nabory = [sleduet(vx, k, vy) for vx, k, vy in product(TRITY, repeat=3)]
assert len(nabory) == 27
assert (nabory.count(1), nabory.count(-1), nabory.count(0)) == (1, 19, 7)
assert sleduet(1, -1, 1) == 1
assert sleduet(0, 0, -1) == -1                           # пятёрок нет ни у кого - уже ясно

# 4. Проект: по журналу - следует
assert len(PROEKT) == KLASS and sum(1 for x, y in PROEKT if x) == 18
assert tri_voprosa(PROEKT, 1) == (1, -1, 1)
assert sleduet(*tri_voprosa(PROEKT, 1)) == 1

# 5. На неделю раньше: никого - из ничего ничего не следует
ranshe = [(x, y) for x, (_, y) in zip(RANSHE, PROEKT)]   # пятёрки в классе есть, сдавших раньше - нет
assert all(strelka(1 if x else -1, 1 if y else -1) == 1 for x, y in ranshe)   # по каждому: нарушителей нет
assert tri_voprosa(ranshe, 1) == (-1, -1, 1)
assert sleduet(*tri_voprosa(ranshe, 1)) == -1

print("следует: 1 / -1 / 0 -", nabory.count(1), nabory.count(-1), nabory.count(0))
print("мостик: списков проверено", spiskov)
print("Е.7: все проверки прошли")
