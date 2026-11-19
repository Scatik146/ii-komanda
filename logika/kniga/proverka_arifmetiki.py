"""Проверка Б.3: логика как арифметика на числах 0 и 1.
Каждая пара «логика ↔ арифметика» даёт одно и то же на всех наборах.
Запуск: python3 proverka_arifmetiki.py"""
import sys
from itertools import product

# пары: имя, логика, арифметика (обе — функции от x, y)
PARY = [
    ("НЕ", lambda x, y: int(not x), lambda x, y: 1 - x),
    ("И", lambda x, y: x & y, lambda x, y: x * y),
    ("И = min", lambda x, y: x & y, lambda x, y: min(x, y)),
    ("ИЛИ", lambda x, y: x | y, lambda x, y: x + y - x * y),
    ("ИЛИ = max", lambda x, y: x | y, lambda x, y: max(x, y)),
    ("⊕", lambda x, y: x ^ y, lambda x, y: (x + y) % 2),
    ("→", lambda x, y: int((not x) or y), lambda x, y: 1 - x + x * y),
    ("≡", lambda x, y: int(x == y), lambda x, y: 1 - x - y + 2 * x * y),
    ("x·x = x", lambda x, y: x, lambda x, y: x * x),
    ("x·(1 − x) = 0", lambda x, y: 0, lambda x, y: x * (1 - x)),
    ("x + (1 − x) = 1", lambda x, y: 1, lambda x, y: x + (1 - x)),
    ("де Морган", lambda x, y: 1 - x * y,
     lambda x, y: (1 - x) + (1 - y) - (1 - x) * (1 - y)),
]


# sovpadaet: логика и арифметика равны на всех четырёх наборах
def sovpadaet(para):
    _, logika, arifm = para
    vse = all(logika(x, y) == arifm(x, y) for x, y in product((0, 1), repeat=2))
    return vse


# kontrprimer_slozhenie: «ИЛИ — это просто +» ломается на 1 + 1
def kontrprimer_slozhenie():
    lomaetsya = (1 | 1) != 1 + 1
    return lomaetsya


# glavnoe: все пары и контрпример
def glavnoe():
    oshibki = [p[0] for p in PARY if not sovpadaet(p)]
    if not kontrprimer_slozhenie():
        oshibki.append("контрпример 1 + 1")
    print(f"пар: {len(PARY)}, неверных: {len(oshibki)}", *oshibki)
    return len(oshibki)


if __name__ == "__main__":
    sys.exit(1 if glavnoe() else 0)
