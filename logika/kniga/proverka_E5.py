# proverka_E5.py — проверка примеров Е.5 «Хозяйство» (часть 2)
# запуск: python3 logika/kniga/proverka_E5.py
# Значения: -1 нет, 0 не знаю, 1 да.

# Данные.
TRITY = (-1, 0, 1)
CHAT = {"контрольная в 214": 1}                         # объявление в чате, забыли поправить
SAJT = {"контрольная в 214": -1}                        # расписание на сайте, перенесли в 305
POROG = 5                                               # разных пустых запросов - решено заранее


# Слова нижнего уровня.
def ne(x):
    otvet = -x
    return otvet


def i_(x, y):
    otvet = min(x, y)
    return otvet


def ili(x, y):                                          # ИЛИ = ¬(¬x ∧ ¬y)
    otvet = ne(i_(ne(x), ne(y)))
    return otvet


def vorota(x):                                          # пропускают только 1
    otvet = 1 if x == 1 else -1
    return otvet


def ne_znayu(x):                                        # не знаю?(x) = ¬ворота(x) ∧ ¬ворота(¬x)
    otvet = i_(ne(vorota(x)), ne(vorota(ne(x))))
    return otvet


def soglasie(x, y):                                     # одинаково - значение, разное - 0
    otvet = x if x == y else 0
    return otvet


def osnovanie(x, b):                                    # (x ∧ b) ∨ (¬b ∧ 0)
    otvet = ili(i_(x, b), i_(ne(b), 0))
    return otvet


def vektor1(f):
    otvet = [f(x) for x in TRITY]
    return otvet


def vektor2(f):
    otvet = [f(x, y) for x in TRITY for y in TRITY]
    return otvet


# Слова Е.5.
def hranit(ch, s):                                      # ОЧ-09: ворота(ч ∧ с)
    otvet = vorota(i_(ch, s))
    return otvet


def najdu(p, z):                                        # ОЧ-11: ¬п ∨ з
    otvet = ili(ne(p), z)
    return otvet


def menyat_na_meste(r):                                 # ОЧ-18: ворота(¬р)
    otvet = vorota(ne(r))
    return otvet


def zamenit(s, o):                                      # ОЧ-18: ворота(с ∧ о)
    otvet = vorota(i_(s, o))
    return otvet


def vnesti(r, s):                                       # Б4: основание(р, с)
    otvet = osnovanie(r, s)
    return otvet


def sobirat(e):                                         # ОЧ-21
    otvet = vorota(e)
    return otvet


def s_nulya(e):
    otvet = vorota(ne(e))
    return otvet


def iskat(e):
    otvet = ne_znayu(e)
    return otvet


def est_li_gde_to(najdeno, pustyh, porog=POROG):         # ОЧ-22: усталости среди входов нет
    otvet = 0
    if pustyh >= porog:
        otvet = -1
    if najdeno:
        otvet = 1
    return otvet


def pridumyvat(najdeno, pustyh, porog=POROG):
    otvet = vorota(ne(est_li_gde_to(najdeno, pustyh, porog)))
    return otvet


# Проверки.
# 1. ОЧ-09: хранить - только если точно часто и точно есть сброс
assert vektor2(hranit) == [-1, -1, -1, -1, -1, -1, -1, -1, 1]
assert hranit(1, 1) == 1                                # таблица умножения - в голове
assert hranit(-1, 1) == -1                              # средний балл - считаю, когда нужен
assert hranit(0, 1) == -1                               # контрпример: «на всякий случай» - нет

# 2. ОЧ-10: два места - согласие
assert vektor2(soglasie) == [-1, 0, 0, 0, 0, 0, 0, 0, 1]
assert soglasie(CHAT["контрольная в 214"], SAJT["контрольная в 214"]) == 0
assert SAJT["контрольная в 214"] == -1                  # одно место - точный ответ

# 3. ОЧ-11: найду(п, з) = ¬п ∨ з
assert vektor2(najdu) == [1, 1, 1, 0, 0, 1, -1, 0, 1]
assert najdu(1, 1) == 1                                 # учебники в библиотеке, листок на шкафу
assert najdu(1, -1) == -1                               # контрпример: переложил без записки

# 4. ОЧ-18: менять на месте - только сломанное; заменить - сверено и откат готов
assert vektor1(menyat_na_meste) == [1, -1, -1]
assert menyat_na_meste(0) == -1                         # «загляну на минутку» - нет
assert vektor2(zamenit) == [-1, -1, -1, -1, -1, -1, -1, -1, 1]
assert zamenit(1, 0) == -1                              # «откат, наверное, есть» - нет

# 5. Б4: решение без сверки - 0
assert vektor2(vnesti) == [0, 0, -1, 0, 0, 0, 0, 0, 1]
assert vnesti(1, 1) == 1
assert vnesti(1, 0) == 0                                # контрпример: внести без сверки

# 6. ОЧ-21: ровно одно из трёх
assert vektor1(sobirat) == [-1, -1, 1]
assert vektor1(s_nulya) == [1, -1, -1]
assert vektor1(iskat) == [-1, 1, -1]
for e in TRITY:
    assert [sobirat(e), s_nulya(e), iskat(e)].count(1) == 1

# 7. ОЧ-22: придумывать - только после порога пустых запросов
assert pridumyvat(False, 0) == -1                       # не искал - не придумывай
assert pridumyvat(False, 1) == -1                       # один пустой - спроси по-другому
assert pridumyvat(False, POROG) == 1                    # порог - придумываю, пометка «наше»
assert pridumyvat(True, POROG + 3) == -1                # нашлось - собираю
assert est_li_gde_to(False, 2) == 0                     # вечер, устал - всё равно 0

print("найду вектором:", vektor2(najdu))
print("Е.5: все проверки прошли")
