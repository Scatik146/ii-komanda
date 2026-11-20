# proverka_D_vremya.py — проверка шага Д «Время»: перебор вариантов против Клини
# Основа — задание 038 (DeepSeek), переписано по-фортовски (Марьям, 20.11).
# запуск: python3 logika/kniga/proverka_D_vremya.py
from itertools import product

# Данные.
NET, NE_ZNAYU, DA = -1, 0, 1
ZNACHENIYA = (NET, NE_ZNAYU, DA)
BOJ = (DA, NET)                                  # варианты завтра: бой будет / не будет
PLANY = ("план 1", "план 2", "план 3")           # три плана урока
# формула: кортеж-дерево ("p",), ("НЕ", f), ("И", f, g), ("ИЛИ", f, g)
P = ("p",)
NP = ("НЕ", P)
ILI = ("ИЛИ", P, NP)
I_ = ("И", P, NP)


# znachenie: считает формулу при данном p по правилам Клини
def znachenie(f, p):
    op = f[0]
    if op == "НЕ":
        otvet = -znachenie(f[1], p)
    elif op == "И":
        otvet = min(znachenie(f[1], p), znachenie(f[2], p))
    elif op == "ИЛИ":
        otvet = max(znachenie(f[1], p), znachenie(f[2], p))
    else:
        otvet = p
    return otvet


# svesti: все 1 -> 1, все -1 -> -1, иначе (и пустой список) 0
def svesti(otvety):
    otvet = NE_ZNAYU
    if otvety and all(x == DA for x in otvety):
        otvet = DA
    if otvety and all(x == NET for x in otvety):
        otvet = NET
    return otvet


# po_variantam: формула целиком в каждом варианте, потом сверка
def po_variantam(f, varianty):
    otvet = svesti([znachenie(f, v) for v in varianty])
    return otvet


# neotvratimo: сверка по вариантам, но только если список полный
def neotvratimo(otvety, polnyj):
    otvet = NE_ZNAYU
    if polnyj:
        otvet = svesti(otvety)
    return otvet


# mozhet_byt: хоть в одном 1 -> 1; во всех -1 и список полный -> -1; иначе 0
# (учитель 20.11, 22:10: «нет» - только по полному списку, как ОЧ-25)
def mozhet_byt(otvety, polnyj):
    otvet = NE_ZNAYU
    if polnyj:
        otvet = svesti(otvety)
    if any(x == DA for x in otvety):
        otvet = DA
    return otvet


# tablica: значения формулы при p = -1, 0, 1 (по ней склеиваем одинаковые)
def tablica(f):
    otvet = tuple(znachenie(f, x) for x in ZNACHENIYA)
    return otvet


# sloj: формулы на шаг глубже из данного списка
def sloj(spisok):
    novye = [("НЕ", f) for f in spisok]
    for op, f, g in product(("И", "ИЛИ"), spisok, spisok):
        novye.append((op, f, g))
    return novye


# raznye_funkcii: формулы глубины <= 2, по одной на каждую таблицу
def raznye_funkcii():
    vse = [P]
    vse = vse + sloj(vse)
    vse = vse + sloj(vse)
    po_tablice = {}
    for f in vse:
        po_tablice.setdefault(tablica(f), f)
    otvet = list(po_tablice.values())
    return otvet


# rashozhdeniya: где перебор и Клини при p = 0 отвечают по-разному
def rashozhdeniya():
    otvet = []
    for f in raznye_funkcii():
        perebor = po_variantam(f, BOJ)
        klini = znachenie(f, NE_ZNAYU)
        if perebor != klini:
            otvet.append((tablica(f), perebor, klini))
    return otvet


# морское сражение
assert po_variantam(ILI, BOJ) == DA and po_variantam(I_, BOJ) == NET
assert po_variantam(P, BOJ) == NE_ZNAYU
assert znachenie(ILI, NE_ZNAYU) == NE_ZNAYU and znachenie(I_, NE_ZNAYU) == NE_ZNAYU

# неотвратимо: «пароль» во всех трёх планах; список полный / неполный
assert neotvratimo([DA for _ in PLANY], True) == DA
assert neotvratimo([DA for _ in PLANY], False) == NE_ZNAYU
assert neotvratimo([NET for _ in PLANY], True) == NET
assert neotvratimo([NET for _ in PLANY], False) == NE_ZNAYU

# может быть: «двухфакторная» в одном плане из трёх
assert mozhet_byt([DA, NET, NET], True) == DA
assert mozhet_byt([DA, NET, NET], False) == DA
assert mozhet_byt([NET, NET, NET], True) == NET
assert mozhet_byt([NET, NET, NET], False) == NE_ZNAYU
assert mozhet_byt([NE_ZNAYU, NET, NET], True) == NE_ZNAYU
assert mozhet_byt([], True) == NE_ZNAYU

# перебор функций глубины <= 2: расхождений два, это p ИЛИ НЕ p и p И НЕ p
RAZ = rashozhdeniya()
assert sorted(RAZ) == [((NET, NE_ZNAYU, NET), NET, NE_ZNAYU), ((DA, NE_ZNAYU, DA), DA, NE_ZNAYU)]

print("Д: все проверки прошли")
print("Расхождения перебора и Клини (таблица при p = -1, 0, 1; перебор; Клини):")
for t, perebor, klini in RAZ:
    print("  ", t, perebor, klini)
