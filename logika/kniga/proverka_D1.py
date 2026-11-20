# proverka_D1.py — проверка примеров Д.1 «Морское сражение всерьёз» (часть 2)
# запуск: python3 logika/kniga/proverka_D1.py
# Значения: -1 нет, 0 не знаю, 1 да. НЕ x = -x, И = min, ИЛИ = max (Клини).
from itertools import product

# Данные.
# вариант: словарь «имя -> бит», например {"p": 1}
# формула: кортеж-дерево: ("p",), ("НЕ", f), ("И", f, g), ("ИЛИ", f, g)
SRAZHENIE = [{"p": 1}, {"p": -1}]                       # будет / не будет
NE_ZNAYU = {"p": 0}                                      # таблица: про p не знаю
UROK = [{"k": 1, "s": -1}, {"k": -1, "s": 1}]            # контрольная / самостоятельная
UROK_I_KINO = UROK + [{"k": -1, "s": -1}]                # забыли вариант «кино»
BOJ_I_DOZHD = [{"p": a, "d": b} for a, b in product((1, -1), repeat=2)]


# znachenie: считает формулу на одном наборе значений (min/max/минус)
def znachenie(f, nabor):
    op = f[0]
    if op == "НЕ":
        otvet = -znachenie(f[1], nabor)
    elif op == "И":
        otvet = min(znachenie(f[1], nabor), znachenie(f[2], nabor))
    elif op == "ИЛИ":
        otvet = max(znachenie(f[1], nabor), znachenie(f[2], nabor))
    else:
        otvet = nabor[op]
    return otvet


# svesti: из ответов по вариантам делает трит: все 1 -> 1, все -1 -> -1, иначе 0
def svesti(otvety):
    otvet = 0
    if all(x == 1 for x in otvety):
        otvet = 1
    if all(x == -1 for x in otvety):
        otvet = -1
    return otvet


# po_variantam: считает формулу целиком в каждом варианте, потом сверяет
def po_variantam(f, varianty):
    otvety = [znachenie(f, v) for v in varianty]
    otvet = svesti(otvety)
    return otvet


# formuly: все формулы от p из НЕ, И, ИЛИ глубины не больше glubina
def formuly(glubina):
    spisok = [("p",)]
    for _ in range(glubina):
        novye = [("НЕ", f) for f in spisok]
        novye += [(op, f, g) for op in ("И", "ИЛИ") for f in spisok for g in spisok]
        spisok = list(dict.fromkeys(spisok + novye))
    return spisok


# rashozhdeniya: формулы, где таблица (p = 0) и перебор вариантов отвечают по-разному
def rashozhdeniya(spisok):
    raznye = []
    for f in spisok:
        t = znachenie(f, NE_ZNAYU)
        v = po_variantam(f, SRAZHENIE)
        if t != v:
            raznye.append((f, t, v))
    return raznye


P = ("p",)
NP = ("НЕ", P)
ILI = ("ИЛИ", P, NP)
I_ = ("И", P, NP)

# Д.1: сражение по вариантам - целое знает, части нет
assert po_variantam(ILI, SRAZHENIE) == 1
assert po_variantam(I_, SRAZHENIE) == -1
assert po_variantam(P, SRAZHENIE) == 0 and po_variantam(NP, SRAZHENIE) == 0
# Д.1: таблица Клини при p = 0 - «не знаю» в обоих случаях
assert znachenie(ILI, NE_ZNAYU) == 0 and znachenie(I_, NE_ZNAYU) == 0

# Д.1: урок - «пишем по дробям» = к ИЛИ с
DROBI = ("ИЛИ", ("k",), ("s",))
assert po_variantam(DROBI, UROK) == 1
assert znachenie(DROBI, {"k": 0, "s": 0}) == 0
assert po_variantam(("k",), UROK) == 0
# контрпример: забыли вариант «кино» - уверенность пропала
assert po_variantam(DROBI, UROK_I_KINO) == 0

# контрпример: два разных события - перебор и таблица согласны
BOJ_ILI_DOZHD = ("ИЛИ", ("p",), ("d",))
assert len(BOJ_I_DOZHD) == 4
assert po_variantam(BOJ_ILI_DOZHD, BOJ_I_DOZHD) == 0 == znachenie(BOJ_ILI_DOZHD, {"p": 0, "d": 0})

# цена: n неизвестных - 2^n вариантов
assert len(list(product((1, -1), repeat=10))) == 1024

# перебор формул: таблица не врёт, только недоговаривает
VSE = formuly(2)
RAZ = rashozhdeniya(VSE)
assert all(t == 0 and v != 0 for f, t, v in RAZ)          # таблица 0, перебор знает
assert all("НЕ" in str(f) for f, t, v in RAZ)               # везде есть и p, и НЕ p
assert any(f == ILI for f, t, v in RAZ)
# по сути расхождений два: p ИЛИ НЕ p и p И НЕ p (сверено с 038, DeepSeek)
TABLICY = {tuple(znachenie(f, {"p": x}) for x in (-1, 0, 1)) for f, t, v in RAZ}
assert TABLICY == {(1, 0, 1), (-1, 0, -1)} and any(f == I_ for f, t, v in RAZ)
print("формул глубины <= 2:", len(VSE), "расхождений:", len(RAZ))
for f, t, v in RAZ[:6]:
    print("  ", f, "таблица", t, "перебор", v)
print("Д.1: все проверки прошли")
