# proverka_E4.py — проверка примеров Е.4 «Миры» (часть 2)
# запуск: python3 logika/kniga/proverka_E4.py
# Значения: -1 нет, 0 не знаю, 1 да; None - «отсутствует» (не трит).

# Данные.
TRITY = (-1, 0, 1)
ZAPISI = (-1, 0, 1, None)
REALNOST = {"контрольная в пятницу": 1, "проектор работает": 1, "Петя решил №5": 0}
PROGNOZ = {"контрольная в пятницу": -1}                 # «если я заболею»
PLAN = {"контрольная в пятницу": 0}                     # черновик плана, опора - Реальность
ZADACHNIK = {"Петя решил №5": 1}                        # не опора Реальности
OPORY = {"Реальность": None, "прогноз": "Реальность", "план": "Реальность", "задачник": None}
MIRY = {"Реальность": REALNOST, "прогноз": PROGNOZ, "план": PLAN, "задачник": ZADACHNIK}


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


def soglasie(x, y):                                     # одинаково - значение, разное - 0
    otvet = x if x == y else 0
    return otvet


def vektor2(f, vhody=TRITY):
    otvet = [f(x, y) for x in vhody for y in vhody]
    return otvet


# Слова Е.4.
def vzyat(svoya, opora):                                # ОЧ-08: своя запись, иначе опора
    otvet = svoya if svoya is not None else opora
    return otvet


def znachenie(vopros, mir):                             # ОЧ-08: поиск по цепи опор
    otvet = None
    while mir is not None and otvet is None:
        otvet = vzyat(MIRY[mir].get(vopros), None)
        mir = OPORY[mir]
    return otvet


def otvet_na(vopros, mir="Реальность"):                 # ОЧ-07: ответ из мира вопроса
    otvet = znachenie(vopros, mir)
    return otvet


def oshibka(r, o):                                      # ОЧ-14: р ∧ ¬о, 1 - ошибка
    otvet = i_(r, ne(o))
    return otvet


def oshibka_po_pravilu(r, o):                           # ОЧ-14 словами
    otvet = -1
    if r == 1 and o == -1:
        otvet = 1
    if (r == 0 and o != 1) or (r == 1 and o == 0):
        otvet = 0
    return otvet


# Проверки.
# 1. ОЧ-07: ответ из мира вопроса
assert otvet_na("контрольная в пятницу") == 1           # Пете - «да»
assert otvet_na("контрольная в пятницу", "прогноз") == -1
assert soglasie(1, -1) == 0                             # контрпример: свели миры - «не знаю»

# 2. ОЧ-08: поиск по цепи опор
assert vektor2(vzyat, ZAPISI) == [-1, -1, -1, -1, 0, 0, 0, 0, 1, 1, 1, 1, -1, 0, 1, None]
assert vzyat(0, 1) == 0                                 # своя 0 не уступает опоре
assert otvet_na("проектор работает", "план") == 1       # записи нет - из Реальности
assert otvet_na("контрольная в пятницу", "план") == 0   # своя 0 остаётся
assert otvet_na("Петя решил №5") == 0                   # задачник не опора
assert ili(REALNOST["Петя решил №5"], ZADACHNIK["Петя решил №5"]) == 1   # контрпример: ИЛИ ошибается
assert otvet_na("кабинет 214", "план") is None          # нигде нет - отсутствует

# 3. ОЧ-14: ошибка сказки
assert vektor2(oshibka) == [-1, -1, -1, 0, 0, -1, 1, 0, -1]
for r in TRITY:
    for o in TRITY:
        assert oshibka(r, o) == oshibka_po_pravilu(r, o)
    assert oshibka(r, 1) == -1                          # с оговоркой - никогда
assert oshibka(1, -1) == 1                              # диаграмма без «условные»

print("ошибка сказки вектором:", vektor2(oshibka))
print("Е.4: все проверки прошли")
