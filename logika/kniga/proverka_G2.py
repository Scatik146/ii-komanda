# Проверка примеров шага Г (часть 2, «Следование»). Значения: -1 нет, 0 не знаю, 1 да.
imp = lambda x, y: max(-x, y)          # Филон на двух значениях, Клини на трёх
lu = lambda x, y: min(1, 1 - x + y)    # Лукасевич
bl = lambda x, y: max(min(x, y), min(0, -x))   # Брусенцов буквально: xy ∨ σx′, σ = 0
B = (-1, 1); T = (-1, 0, 1)

# Г.1: три правды, одна ложь
assert [imp(x, y) for x in B for y in B] == [1, 1, -1, 1]

# Г.1: неделя «дождь -> зонт», нарушение только в субботу
ned = [(1, 1), (-1, -1), (-1, 1), (1, 1), (-1, -1), (1, -1), (-1, -1)]
assert [i + 1 for i, (d, z) in enumerate(ned) if imp(d, z) == -1] == [6]

# Г.3: пустой класс - стрелка «да», ОЧ-23 (Axy = Vx · нет x без y · Vy) - нет
kl = [(-1, -1)] * 25
assert min(imp(x, y) for x, y in kl) == 1
Vx = any(x == 1 for x, y in kl); kontr = any(x == 1 and y == -1 for x, y in kl); Vy = any(y == 1 for x, y in kl)
assert not (Vx and not kontr and Vy)

# Г.4: Брусенцов буквально при ложном условии - «привходящее» (0)
assert {(x, y): bl(x, y) for x in B for y in B} == {(-1, -1): 0, (-1, 1): 0, (1, -1): -1, (1, 1): 1}
# Г.4: x -> x и единственная клетка спора Клини и Лукасевича
assert [imp(x, x) for x in T] == [1, 0, 1] and [lu(x, x) for x in T] == [1, 1, 1]
assert [(x, y) for x in T for y in T if imp(x, y) != lu(x, y)] == [(0, 0)]
print("Г: все проверки прошли")
