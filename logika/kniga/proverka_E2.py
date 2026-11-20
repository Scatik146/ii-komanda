# proverka_E2.py — проверка примеров Е.2 «Не знаю» (часть 2)
# запуск: python3 logika/kniga/proverka_E2.py
# Значения: -1 нет, 0 не знаю, 1 да. «Отсутствует» - не трит.

# Данные.
TRITY = (-1, 0, 1)
OTSUTSTVUET = 2            # атома нет вовсе - не трит и не «нет» (ОЧ-13)


# ne: меняет знак
def ne(x):
    otvet = -x
    return otvet


# osnovanie: есть основание (b = 1) - значение x; нет - 0 (ОЧ-01, Б2, Б7)
def osnovanie(x, b):
    otvet = 0
    if b == 1:
        otvet = x
    return otvet


# srabatyvaet: правило по отсутствующему атому не запускается (ОЧ-13)
def srabatyvaet(x):
    otvet = 1
    if x == OTSUTSTVUET:
        otvet = -1
    return otvet


# est_li: нашёл - 1; не нашёл, а список полный - -1; иначе 0 (ОЧ-25, Б3)
def est_li(proverennye, iskomoe, polnyj):
    otvet = 0
    if polnyj and iskomoe not in proverennye:
        otvet = -1
    if iskomoe in proverennye:
        otvet = 1
    return otvet


# vorota: наружу только 1
def vorota(x):
    otvet = 1 if x == 1 else -1
    return otvet


# ne_znayu_li: 1, если x = 0
def ne_znayu_li(x):
    otvet = 1 if x == 0 else -1
    return otvet


# dejstvie: да - делаю, нет - не делаю, не знаю - ищу (ОЧ-26)
def dejstvie(x):
    otvet = "ищу"
    if vorota(x) == 1:
        otvet = "делаю"
    if vorota(ne(x)) == 1:
        otvet = "не делаю"
    return otvet


# otvet_ucheniku: 0 - «пока не знаю, проверю» (ОЧ-32)
def otvet_ucheniku(x):
    otvet = "пока не знаю, проверю"
    if x == 1:
        otvet = "да"
    if x == -1:
        otvet = "нет"
    return otvet


# soglasie: одинаково - значение, разное - 0 (ОЧ-15, Б6)
def soglasie(x, y):
    otvet = 0
    if x == y:
        otvet = x
    return otvet


# spor: согласие всех голосов и подпись «сколько из скольких»
def spor(golosa):
    itog = golosa[0]
    for g in golosa[1:]:
        itog = soglasie(itog, g)
    za = sum(1 for g in golosa if g == 1)
    otvet = (itog, str(za) + " из " + str(len(golosa)))
    return otvet


# visokosnyj_naivno: «очевидно, каждый четвёртый» - с ошибкой
def visokosnyj_naivno(god):
    otvet = god % 4 == 0
    return otvet


# visokosnyj: по григорианскому календарю
def visokosnyj(god):
    otvet = (god % 4 == 0 and god % 100 != 0) or god % 400 == 0
    return otvet


# 1. ОЧ-01: ноль сам не становится ни «да», ни «нет»
for x in TRITY:
    assert osnovanie(x, 1) == x
    assert osnovanie(x, 0) == 0
    assert osnovanie(x, -1) == 0
assert osnovanie(1, 0) == 0                       # «всем понятно?» - тишина: основания нет
for x in TRITY:                                   # сказано «не знаю» - при любом основании 0
    assert osnovanie(0, x) == 0

# 2. Б2: «очевидно» - 0, покажи пример
OCHEVIDNO = 0.1 + 0.2 == 0.3                      # «очевидно, 0,1 + 0,2 = 0,3»
assert OCHEVIDNO is False                         # компьютер: нет (двоичные дроби)
assert osnovanie(1, 0) == 0                       # «очевидно» без примера - 0
assert osnovanie(-1, 1) == -1                     # показали пример - контрпример найден

# 3. ОЧ-13: чего нет - того нет
assert OTSUTSTVUET not in TRITY
assert srabatyvaet(OTSUTSTVUET) == -1             # контрольной не было - оценку не ставим
for x in TRITY:
    assert srabatyvaet(x) == 1                    # даже 0 и -1 - это ответы

# 4. ОЧ-25: не нашёл - не знаю; «нет» - по контрпримеру или полному списку
KLASS = 25
BEZ_TETRADI = set()                               # проверены все 25 - без тетради никого
assert est_li(BEZ_TETRADI, "кто-то", True) == -1  # полный список - честное «нет»
assert est_li(set(), "ключи", False) == 0         # в куртке нет - про квартиру «не знаю»
assert est_li({"ключи"}, "ключи", False) == 1

# 5. Б3: «не нашли» не значит «нет» - тесты високосного года
TESTY = (2020, 2023, 2024)
oshibki = {g for g in TESTY if visokosnyj_naivno(g) != visokosnyj(g)}
assert len(oshibki) == 0                          # три теста - ошибок не нашли
assert est_li(oshibki, "ошибка", False) == 0      # «ошибки есть?» - 0: годов бесконечно, список не полный
oshibki = {g for g in TESTY + (1900,) if visokosnyj_naivno(g) != visokosnyj(g)}
assert oshibki == {1900}                          # 1900 - не високосный: ошибка найдена
assert est_li({"ошибка"} if oshibki else set(), "ошибка", False) == 1

# 6. ОЧ-26: на всё три ответа, ровно один
for x in TRITY:
    vorot = [vorota(x), ne_znayu_li(x), vorota(ne(x))]
    assert vorot.count(1) == 1
assert [dejstvie(x) for x in TRITY] == ["не делаю", "ищу", "делаю"]

# 7. ОЧ-32 и Б7: говорю как есть; пересказ - 0
assert [otvet_ucheniku(x) for x in TRITY] == ["нет", "пока не знаю, проверю", "да"]
for x in TRITY:
    assert osnovanie(x, 0) == 0                   # пересказ: что бы ни сказал - 0
    assert osnovanie(x, 1) == x                   # подлинник: что сказано
assert otvet_ucheniku(osnovanie(1, 0)) == "пока не знаю, проверю"

# 8. ОЧ-15 и Б6: двое спорят - 0, кто и почему - в подпись
TABLICA = [soglasie(x, y) for x in TRITY for y in TRITY]
assert TABLICA == [-1, 0, 0, 0, 0, 0, 0, 0, 1]
assert soglasie(1, -1) == 0                       # часы на стене и в телефоне разошлись
assert spor([1, 1, 1, -1]) == (0, "3 из 4")       # три словаря «да», один «нет» - большинства нет
assert spor([1, 1, 1, 1]) == (1, "4 из 4")
assert soglasie(0, 1) == 0                        # «не знаю» и «да» - всё ещё не знаю

# 9. Формулы через НЕ, И (меньшее), ИЛИ (большее) - совпадают с действиями на всех входах
I_ = min
ILI = max
for x in TRITY:
    for b in TRITY:
        assert ILI(I_(x, b), I_(ne(b), 0)) == osnovanie(x, b)                 # основание
        assert ILI(I_(x, b), I_(ILI(x, b), 0)) == soglasie(x, b)              # согласие
EST_TABLICA = []
for nashel in (-1, 1):
    for polnyj in (-1, 1):
        formula = ILI(nashel, I_(ne(polnyj), 0))                             # есть ли
        po_pravilu = est_li({"x"} if nashel == 1 else set(), "x", polnyj == 1)
        assert formula == po_pravilu
        EST_TABLICA.append(formula)
assert EST_TABLICA == [0, -1, 1, 1]
print("есть ли вектором:", EST_TABLICA, "| 0.1 + 0.2 =", 0.1 + 0.2)

# 10. Формулы из готовых слов (по-фортовски: собрали - пользуемся)
assert [vorota(x) for x in TRITY] == [-1, -1, 1]              # делаю
assert [ne_znayu_li(x) for x in TRITY] == [-1, 1, -1]         # ищу
assert [vorota(ne(x)) for x in TRITY] == [1, -1, -1]          # не делаю
assert [srabatyvaet(x) for x in TRITY + (OTSUTSTVUET,)] == [1, 1, 1, -1]
for x in TRITY:
    assert ILI(I_(x, -1), I_(ne(-1), 0)) == 0                 # пересказ: подлинник = -1 -> 0
assert ILI(I_(-1, 1), I_(ne(1), 0)) == -1                     # «очевидно» с примером: -1

print("согласие вектором:", TABLICA)
print("0.1 + 0.2 == 0.3:", OCHEVIDNO, "| 1900 по-простому:", visokosnyj_naivno(1900), "на деле:", visokosnyj(1900))
print("спор 3 «да» и 1 «нет»:", spor([1, 1, 1, -1]))
print("Е.2: все проверки прошли")
