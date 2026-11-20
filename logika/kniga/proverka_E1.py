# proverka_E1.py — проверка примеров Е.1 «Мерфи» (часть 2)
# запуск: python3 logika/kniga/proverka_E1.py
# Значения: -1 нет, 0 не знаю, 1 да. В каждом варианте «пошло не так» решено: 1 или -1.
from fractions import Fraction
from itertools import product

# Данные.
# датчики из байки: 16 штук, каждый можно приклеить двумя способами
DATCHIKOV = 16
SPOSOBY = (1, -1)          # 1 - приклеен верно, -1 - наоборот


# neotvratimo: во всех да и список полный -> 1; во всех нет и полный -> -1; иначе 0
def neotvratimo(otvety, polnyj):
    otvet = 0
    if polnyj and len(otvety) > 0 and all(x == 1 for x in otvety):
        otvet = 1
    if polnyj and len(otvety) > 0 and all(x == -1 for x in otvety):
        otvet = -1
    return otvet


# mozhet_byt: хоть в одном да -> 1; во всех нет и список полный -> -1; иначе 0
def mozhet_byt(otvety, polnyj):
    otvet = 0
    if polnyj and len(otvety) > 0 and all(x == -1 for x in otvety):
        otvet = -1
    if any(x == 1 for x in otvety):
        otvet = 1
    return otvet


# ne_tak: в варианте установки «пошло не так», если хоть один датчик наоборот
def ne_tak(variant):
    otvet = -1
    if any(d == -1 for d in variant):
        otvet = 1
    return otvet


# vse_naoborot: все датчики приклеены наоборот
def vse_naoborot(variant):
    otvet = all(d == -1 for d in variant)
    return otvet


# dolya_vse_naoborot: какая доля вариантов - «все наоборот»
def dolya_vse_naoborot(varianty):
    skolko = sum(1 for v in varianty if vse_naoborot(v))
    otvet = Fraction(skolko, len(varianty))
    return otvet


# zakon_merfi: из «может пойти не так» делает «пойдёт не так»
def zakon_merfi(otvety, polnyj):
    otvet = neotvratimo(otvety, polnyj)
    if mozhet_byt(otvety, polnyj) == 1:
        otvet = 1
    return otvet


# gotovitsya: трит действия - готовиться, пока «не так» не исключено
def gotovitsya(otvety, polnyj):
    otvet = 1
    if mozhet_byt(otvety, polnyj) == -1:
        otvet = -1
    return otvet


# 1. Датчики, если клеить «монеткой»: 2^16 вариантов
MONETKA = list(product(SPOSOBY, repeat=DATCHIKOV))
OTVETY_M = [ne_tak(v) for v in MONETKA]
assert len(MONETKA) == 65536
assert mozhet_byt(OTVETY_M, True) == 1           # может пойти не так - да
assert neotvratimo(OTVETY_M, True) == 0          # неотвратимо - нет такого слова: есть вариант «всё верно»
assert dolya_vse_naoborot(MONETKA) == Fraction(1, 65536)

# 2. Датчики, если клеит один человек с одним убеждением: 2 варианта
ODIN_CHELOVEK = [tuple([s] * DATCHIKOV) for s in SPOSOBY]
assert dolya_vse_naoborot(ODIN_CHELOVEK) == Fraction(1, 2)

# 3. Закон Мерфи как утверждение - на всех полных списках до 4 вариантов
VSE = [list(s) for n in range(1, 5) for s in product((1, -1), repeat=n)]
oshibok = 0
for otvety in VSE:
    if zakon_merfi(otvety, True) != neotvratimo(otvety, True):
        oshibok += 1
assert oshibok == 22                              # 30 списков, из них 22 с расходящимися вариантами
assert zakon_merfi([1, -1], True) == 1 and neotvratimo([1, -1], True) == 0   # контрпример: один удачный день

# 4. Закон Мерфи как правило действия
for otvety in VSE:
    assert gotovitsya(otvety, False) == 1         # список неполный - готовиться всегда
    if gotovitsya(otvety, True) == -1:
        assert all(x == -1 for x in otvety)       # не готовиться - только если во всех вариантах всё так
assert gotovitsya([-1, -1, -1], True) == -1
assert gotovitsya([-1, -1, -1], False) == 1

print("датчики монеткой: вариантов", len(MONETKA), "все наоборот", dolya_vse_naoborot(MONETKA))
print("датчики одним человеком: все наоборот", dolya_vse_naoborot(ODIN_CHELOVEK))
print("закон как утверждение: ошибся на", oshibok, "списках из", len(VSE))
print("Е.1: все проверки прошли")
