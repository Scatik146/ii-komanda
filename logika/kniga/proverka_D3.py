# proverka_D3.py — проверка примеров Д.3 «Почти неотвратимо: Вальд» (часть 2)
# запуск: python3 logika/kniga/proverka_D3.py
# Решение после броска: 1 - взять, -1 - не брать, 0 - смотреть дальше.
from fractions import Fraction as F

# Данные.
# автор задал: хороший попадает 8 из 10, слабый - 3 из 10; ошибка - 5 из 100
HOROSHIJ = F(8, 10)
SLABYJ = F(3, 10)
OSHIBKA = F(5, 100)
VERH = (1 - OSHIBKA) / OSHIBKA          # 19: взять, когда счёт не меньше
NIZ = OSHIBKA / (1 - OSHIBKA)           # 1/19: не брать, когда счёт не больше
ZA_POPADANIE = HOROSHIJ / SLABYJ        # 8/3
ZA_PROMAH = (1 - HOROSHIJ) / (1 - SLABYJ)  # 2/7
DLINA = 40                              # дальше не считаем: остаток печатаем


# schet: во сколько раз «хороший» объясняет броски лучше, чем «слабый»
def schet(popal, promahnulsya):
    otvet = ZA_POPADANIE ** popal * ZA_PROMAH ** promahnulsya
    return otvet


# reshenie: трит Вальда по счёту
def reshenie(s):
    otvet = 0
    if s >= VERH:
        otvet = 1
    if s <= NIZ:
        otvet = -1
    return otvet


# po_broskam: решения после каждого броска серии (1 - попал, 0 - мимо)
def po_broskam(seriya):
    otvet = []
    popal = 0
    for i, b in enumerate(seriya):
        popal = popal + b
        otvet.append(reshenie(schet(popal, i + 1 - popal)))
    return otvet


# kartochka: после n бросков - сколько попаданий хватит «взять» и сколько мало «не брать»
def kartochka(n):
    vzyat = None
    ne_brat = None
    for h in range(n + 1):
        r = reshenie(schet(h, n - h))
        if r == 1 and vzyat is None:
            vzyat = h
        if r == -1:
            ne_brat = h
    return (vzyat, ne_brat)


# brosok: все, кто ещё «смотрим», бросают n-й раз; решённые уходят в итог
def brosok(zhdut, n, p, itog):
    dalshe = {}
    for popal, ver in zhdut.items():
        for b, vb in ((1, p), (0, 1 - p)):
            r = reshenie(schet(popal + b, n - popal - b))
            if r == 0:
                dalshe[popal + b] = dalshe.get(popal + b, 0) + ver * vb
            else:
                itog[r] = itog[r] + ver * vb
                itog["broski"] = itog["broski"] + ver * vb * n
    return dalshe


# igra: точно - с какой вероятностью игрока с меткостью p возьмут, не возьмут; среднее число бросков
def igra(p):
    zhdut = {0: F(1)}
    itog = {1: F(0), -1: F(0), "broski": F(0)}
    for n in range(1, DLINA + 1):
        zhdut = brosok(zhdut, n, p, itog)
    itog[0] = sum(zhdut.values())
    return itog


# Пример: три промаха подряд - «не брать» ровно на третьем
assert po_broskam([0, 0, 0]) == [0, 0, -1]
# Контрпример: три попадания подряд - ещё «смотрим»; на четвёртом - «взять»
assert po_broskam([1, 1, 1]) == [0, 0, 0]
assert po_broskam([1, 1, 1, 1]) == [0, 0, 0, 1]
assert schet(3, 0) == F(512, 27) and schet(3, 0) < 19   # 18,96 - почти 19, но не 19
assert schet(0, 3) == F(8, 343) and schet(0, 3) < F(1, 19)  # 1/42,9
# вперемешку: попал, мимо, попал, мимо... - долго «смотрим»
assert po_broskam([1, 0] * 3) == [0] * 6

# Карточка тренера
KART = {n: kartochka(n) for n in range(1, 11)}
assert KART[3] == (None, 0) and KART[4] == (4, 0) and KART[10] == (7, 4)

# Карточка-таблица из книги: строка - бросил, столбец - попал
SETKA = {n: [reshenie(schet(h, n - h)) for h in range(n + 1)] for n in range(1, 7)}
assert SETKA == {1: [0, 0], 2: [0, 0, 0], 3: [-1, 0, 0, 0], 4: [-1, 0, 0, 0, 1],
                 5: [-1, -1, 0, 0, 0, 1], 6: [-1, -1, -1, 0, 0, 1, 1]}

# Ошибки и число бросков - точно, по дробям
HOR = igra(HOROSHIJ)
SLAB = igra(SLABYJ)
SRED = igra(F(55, 100))
assert HOR[-1] < OSHIBKA and SLAB[1] < OSHIBKA      # обещанные 5 из 100 соблюдены
assert HOR[0] < F(1, 1000) and SLAB[0] < F(1, 1000)  # к 40-му броску почти все решены
assert 6 < HOR["broski"] < 7 and 5 < SLAB["broski"] < 6    # в среднем 6-7 бросков
# Контрпример: средний игрок (5,5 из 10) - его нет в списке автора, а метод всё равно решает
assert F(2, 5) < SRED[1] < F(1, 2) < SRED[-1] < F(3, 5)   # почти монетка


# binom: вероятность ровно h попаданий из n при меткости p
def binom(n, h, p):
    c = 1
    for i in range(h):
        c = c * (n - i) // (i + 1)
    otvet = c * p ** h * (1 - p) ** (n - h)
    return otvet


# zaranee: самый короткий план «n бросков, взять при k и больше» с теми же ошибками
def zaranee():
    otvet = None
    n = 0
    while otvet is None:
        n = n + 1
        for k in range(n + 1):
            vzyali_slabogo = sum(binom(n, h, SLABYJ) for h in range(k, n + 1))
            ne_vzyali_horoshego = sum(binom(n, h, HOROSHIJ) for h in range(k))
            if otvet is None and vzyali_slabogo <= OSHIBKA and ne_vzyali_horoshego <= OSHIBKA:
                otvet = (n, k)
    return otvet


ZAR = zaranee()
assert ZAR == (10, 6)   # заранее нужно 10 бросков; у Вальда в среднем 6-7


def pr(x):
    return f"{float(x) * 100:.1f} из 100"

print("карточка тренера (бросков: взять, если попаданий не меньше / не брать, если не больше):")
for n, (v, nb) in KART.items():
    print(f"   {n:2}: взять {v if v is not None else '-'}, не брать {nb if nb is not None else '-'}")
print("три попадания: счёт", schet(3, 0), "=", round(float(schet(3, 0)), 2), "; три промаха:", schet(0, 3))
for imya, t in (("хороший 8/10", HOR), ("слабый 3/10", SLAB), ("средний 5,5/10", SRED)):
    print(f"   {imya}: взяли {pr(t[1])}, не взяли {pr(t[-1])}, не решено к 40-му {float(t[0]):.1e}, бросков в среднем {float(t['broski']):.2f}")
print("план заранее: бросков", ZAR[0], ", взять при попаданиях от", ZAR[1])
print("Д.3: все проверки прошли")
