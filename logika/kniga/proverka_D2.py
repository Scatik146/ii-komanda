# proverka_D2.py — проверка примеров Д.2 «Неотвратимо и может быть» (часть 2)
# запуск: python3 logika/kniga/proverka_D2.py
# Значения: -1 нет, 0 не знаю, 1 да. В каждом варианте событие решено: 1 или -1.
from itertools import product

# Данные.
# расписание: три варианта, в каждом - что есть в понедельник
RASPISANIE = [
    {"математика": 1, "физкультура": -1, "химия": -1},
    {"математика": 1, "физкультура": 1, "химия": -1},
    {"математика": 1, "физкультура": -1, "химия": -1},
]
PREDMETY = ["математика", "физкультура", "химия"]


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


# stolbec: ответы всех вариантов про один предмет
def stolbec(varianty, predmet):
    otvet = [v[predmet] for v in varianty]
    return otvet


# svod_slov: таблица слов - (что в вариантах, полный?) -> (неотвратимо, может быть)
def svod_slov():
    sluchai = {"во всех да": [1, 1, 1], "расходятся": [1, -1, 1], "во всех нет": [-1, -1, -1]}
    tablica = {}
    for imya, otvety in sluchai.items():
        for polnyj in (True, False):
            tablica[(imya, polnyj)] = (neotvratimo(otvety, polnyj), mozhet_byt(otvety, polnyj))
    return tablica


# Пример: расписание, список полный
OTV = {p: stolbec(RASPISANIE, p) for p in PREDMETY}
assert neotvratimo(OTV["математика"], True) == 1
assert neotvratimo(OTV["физкультура"], True) == 0
assert neotvratimo(OTV["химия"], True) == -1
assert mozhet_byt(OTV["математика"], True) == 1
assert mozhet_byt(OTV["физкультура"], True) == 1
assert mozhet_byt(OTV["химия"], True) == -1

# Контрпример: нужен четвёртый вариант - список неполный
assert neotvratimo(OTV["математика"], False) == 0
assert neotvratimo(OTV["химия"], False) == 0
assert mozhet_byt(OTV["физкультура"], False) == 1      # найденный вариант никуда не делся
assert mozhet_byt(OTV["химия"], False) == 0

# Морское сражение: p - бой; «бой или не бой» во всех вариантах да
BOJ = [1, -1]
assert neotvratimo(BOJ, True) == 0 and mozhet_byt(BOJ, True) == 1
assert neotvratimo([1, 1], True) == 1                   # p ИЛИ НЕ p в обоих вариантах

# Контрпример «почти»: 99 из 100 - всё равно не неотвратимо
assert neotvratimo([1] * 99 + [-1], True) == 0

# Таблица слов
T = svod_slov()
assert T[("во всех да", True)] == (1, 1)
assert T[("расходятся", True)] == (0, 1)
assert T[("во всех нет", True)] == (-1, -1)
assert T[("во всех да", False)] == (0, 1)
assert T[("расходятся", False)] == (0, 1)
assert T[("во всех нет", False)] == (0, 0)

# Свойства - на всех списках до 4 вариантов, полных и нет
VSE = [list(s) for n in range(1, 5) for s in product((1, -1), repeat=n)]
for otvety in VSE:
    for polnyj in (True, False):
        n_ = neotvratimo(otvety, polnyj)
        m_ = mozhet_byt(otvety, polnyj)
        assert n_ <= m_                                  # неотвратимое тем более может быть
        assert (n_ == -1) == (m_ == -1)                  # на «нет» слова сходятся
        if not polnyj:
            assert n_ == 0 and m_ != -1                  # неполный список: у «неотвратимо» - всё, у «может быть» - только «нет»
    # чтобы «неотвратимо» перестало быть 1, хватит одного варианта с «нет»
    if neotvratimo(otvety, True) == 1:
        assert neotvratimo(otvety + [-1], True) == 0
print("списков проверено:", len(VSE) * 2)
for k, v in T.items():
    print("  ", k[0], "полный" if k[1] else "неполный", "-> неотвратимо", v[0], "может быть", v[1])
print("Д.2: все проверки прошли")
