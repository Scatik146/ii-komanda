"""proverka_043.py — независимая проверка таблиц кусков 10–11 задания 043 перебором всех 9 клеток."""
T = (-1, 0, 1)

# ne: отрицание трита
def ne(x):
    return -x

# i_: И — минимум
def i_(a, b):
    return min(a, b)

# ili: ИЛИ — максимум
def ili(a, b):
    return max(a, b)

# vorota: пропускают только 1
def vorota(x):
    return 1 if x == 1 else -1

# osnovanie: (x ∧ b) ∨ (¬b ∧ 0) — по книге, стр. 288
def osnovanie(x, b):
    return ili(i_(x, b), i_(ne(b), 0))

# oba: оба точно = ворота(a) ∧ ворота(b)
def oba(a, b):
    return i_(vorota(a), vorota(b))

# hot: хоть одно точно = ворота(a) ∨ ворота(b)
def hot(a, b):
    return ili(vorota(a), vorota(b))

# kletki: все 9 пар в порядке a = −1, 0, 1; b = −1, 0, 1
def kletki():
    return [(a, b) for a in T for b in T]

proverki = {
    'вектор «оба точно» как в куске 10 (−1×8, 1)': [oba(a, b) for a, b in kletki()] == [-1] * 8 + [1],
    '«хоть одно точно»: единиц 5': sum(1 for a, b in kletki() if hot(a, b) == 1) == 5,
    'правила 17, 27, 30: ворота(a ∧ b) = оба точно(a, b)': all(vorota(i_(a, b)) == oba(a, b) for a, b in kletki()),
    'правило 18: ворота(основание(x, пр)) = оба точно(x, пр)': all(vorota(osnovanie(a, b)) == oba(a, b) for a, b in kletki()),
    'правило 39: ворота(a) ∧ ворота(b) = оба точно': all(i_(vorota(a), vorota(b)) == oba(a, b) for a, b in kletki()),
    'правила 23, 42, 43: ворота(a) ∨ ворота(b) = хоть одно точно': all(ili(vorota(a), vorota(b)) == hot(a, b) for a, b in kletki()),
}
for imya, da in proverki.items():
    print(('да  ' if da else 'НЕТ ') + imya)
print('вектор «хоть одно точно»:', [hot(a, b) for a, b in kletki()])
