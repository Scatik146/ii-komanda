# proverka_E3.py — проверка примеров Е.3 «Проверено и ворота» (часть 2)
# запуск: python3 logika/kniga/proverka_E3.py
# Значения: -1 нет, 0 не знаю, 1 да. Слова собраны из базиса {И, НЕ, ворота, 0}.

# Данные.
TRITY = (-1, 0, 1)


# Слова нижнего уровня.
def ne(x):
    otvet = -x
    return otvet


def i_(x, y):
    otvet = min(x, y)
    return otvet


def vorota(x):
    otvet = 1 if x == 1 else -1
    return otvet


def ili(x, y):                                     # ИЛИ = ¬(¬x ∧ ¬y)
    otvet = ne(i_(ne(x), ne(y)))
    return otvet


def ne_znayu_li(x):                                # не знаю? = ¬ворота(x) ∧ ¬ворота(¬x)
    otvet = i_(ne(vorota(x)), ne(vorota(ne(x))))
    return otvet


def vozmozhno(x):                                  # возможно = ¬ворота(¬x)
    otvet = ne(vorota(ne(x)))
    return otvet


def osnovanie(x, b):                               # (x ∧ b) ∨ (¬b ∧ 0)
    otvet = ili(i_(x, b), i_(ne(b), 0))
    return otvet


# vektor1, vektor2: все ответы действия, строка за строкой
def vektor1(f):
    otvet = [f(x) for x in TRITY]
    return otvet


def vektor2(f):
    otvet = [f(x, y) for x in TRITY for y in TRITY]
    return otvet


# Слова Е.3.
def odnim_tritom(pravda, provereno):               # контрпример к ОЧ-02: проверка выброшена
    otvet = pravda
    return otvet


def provereno(r, s):                               # ОЧ-03: р ∧ основание(р, с)
    otvet = i_(r, osnovanie(r, s))
    return otvet


def provereno_po_pravilu(r, s):                    # ОЧ-03 словами
    otvet = 0
    if r == -1:
        otvet = -1
    if r == 1 and s == 1:
        otvet = 1
    return otvet


def nesti(n, g):                                   # ОЧ-06: ворота(н) ∧ возможно(г)
    otvet = i_(vorota(n), vozmozhno(g))
    return otvet


def trevoga(n, ch):                                # Б5: ворота(н) ∧ ¬ворота(ч); 1 - ошибка
    otvet = i_(vorota(n), ne(vorota(ch)))
    return otvet


def ekspertiza(x, v, z):                           # ОЧ-19 формулой
    n = ne_znayu_li(x)
    otvet = ili(i_(n, osnovanie(v, z)), i_(ne(n), x))
    return otvet


def ekspertiza_po_pravilu(x, v, z):                # ОЧ-19 словами
    otvet = x
    if x == 0 and z == 1:
        otvet = v
    return otvet


def urok(chasti):                                  # ОЧ-04: И по всем частям
    otvet = 1
    for x in chasti:
        otvet = i_(otvet, x)
    return otvet


def naruzhu(p, pr):                                # ОЧ-05
    otvet = vorota(i_(p, pr))
    return otvet


def propustit(x, pr):                              # Б1: основание - только программа
    otvet = vorota(osnovanie(x, pr))
    return otvet


def vklyuchit(z):                                  # ОЧ-12
    otvet = vorota(z)
    return otvet


def procherk(o):                                   # ОЧ-16
    otvet = vorota(ne(o))
    return otvet


def usomnitsya(x, s):                              # ОЧ-31: основание(x, ¬с)
    otvet = osnovanie(x, ne(s))
    return otvet


def mozhno(o, r):                                  # Б8: ворота(о) ∨ ворота(р)
    otvet = ili(vorota(o), vorota(r))
    return otvet


# 0. Слова собраны верно
assert vektor1(vozmozhno) == [-1, 1, 1]
assert vektor1(ne_znayu_li) == [-1, 1, -1]
assert vektor2(osnovanie) == [0, 0, -1, 0, 0, 0, 0, 0, 1]

# 1. ОЧ-02: пар 9; одним тритом «да, проверено» и «да, не проверял» совпадают
PARY = [(p, pr) for p in TRITY for pr in TRITY]
assert len(PARY) == 9
assert vektor2(odnim_tritom) == [-1, -1, -1, 0, 0, 0, 1, 1, 1]
assert odnim_tritom(1, 1) == odnim_tritom(1, -1)

# 2. ОЧ-03: проверено
assert vektor2(provereno) == [-1, -1, -1, 0, 0, 0, 0, 0, 1]
assert vektor2(provereno) == vektor2(provereno_po_pravilu)
assert provereno(-1, 1) == -1                      # билеты в черновике
assert provereno(1, -1) == 0                       # решил, но до пятницы
assert provereno(1, 0) != 1                        # контрпример: «проверено» без срока

# 3. ОЧ-06: нести на экспертизу
assert vektor2(nesti) == [-1, -1, -1, -1, -1, -1, -1, 1, 1]
assert nesti(1, -1) == -1                          # черновик - не носят
assert nesti(1, 0) == 1                            # сам проверил - несу

# 4. Б5: тревога
assert vektor2(trevoga) == [-1, -1, -1, -1, -1, -1, 1, 1, -1]
assert trevoga(1, 0) == 1                          # «не знаю, смотрел ли кто-то» - тревога

# 5. ОЧ-19: экспертиза - все 27 наборов
for x in TRITY:
    for v in TRITY:
        for z in TRITY:
            assert ekspertiza(x, v, z) == ekspertiza_po_pravilu(x, v, z)
assert [ekspertiza(0, v, z) for v in TRITY for z in TRITY] == vektor2(osnovanie)
assert ekspertiza(0, -1, 1) == -1                  # коллега нашёл два ответа
assert ekspertiza(0, 1, -1) == 0                   # друг сказал «да» - остаётся 0
assert ekspertiza(1, -1, 1) == 1                   # ответ уже был - не трогаем

# 6. ОЧ-04: И по частям урока
assert vektor2(i_) == [-1, -1, -1, -1, 0, 0, -1, 0, 1]
assert urok([1, 1, 0, 1, 1]) == 0
assert urok([1, 1, -1, 1, 1]) == -1

# 7. ОЧ-05: наружу - только (1, 1)
assert vektor2(naruzhu) == [-1, -1, -1, -1, -1, -1, -1, -1, 1]
assert [pa for pa in PARY if naruzhu(*pa) == 1] == [(1, 1)]

# 8. Б1: пропустить - та же таблица, что у «наружу»
assert vektor2(propustit) == vektor2(naruzhu)
assert propustit(1, 0) == -1                       # «сам посмотрю» - проверку не запускали

# 9, 10. ОЧ-12, ОЧ-16
assert vektor1(vklyuchit) == [-1, -1, 1]
assert vektor1(procherk) == [1, -1, -1]

# 11. ОЧ-17: ворота склеивают «нет» и «не знаю»
assert vektor1(vorota) == [-1, -1, 1]
assert vorota(0) == vorota(-1)

# 12. ОЧ-31: усомниться
assert vektor2(usomnitsya) == [-1, 0, 0, 0, 0, 0, 1, 0, 0]
for x in TRITY:
    assert vorota(usomnitsya(x, 1)) == -1          # после сомнения ворота закрыты
    assert vorota(usomnitsya(x, 0)) == -1
assert usomnitsya(1, 1) == 0                       # ИИ назвал год - 0 до подлинника

# 13. Б8: можно
assert vektor2(mozhno) == [-1, -1, 1, -1, -1, 1, 1, 1, 1]
assert mozhno(0, 0) == -1                          # «наверное, отменяемо» - не считается

# 14. Два новых слова: оба точно, хоть одно точно (начало Е.3)
def oba_tochno(a, b):                              # ворота(a) ∧ ворота(b)
    otvet = i_(vorota(a), vorota(b))
    return otvet


def hot_odno_tochno(a, b):                         # ворота(a) ∨ ворота(b)
    otvet = ili(vorota(a), vorota(b))
    return otvet


assert vektor2(oba_tochno) == [-1, -1, -1, -1, -1, -1, -1, -1, 1]
assert vektor2(hot_odno_tochno) == [-1, -1, 1, -1, -1, 1, 1, 1, 1]
assert oba_tochno(1, 0) == -1                      # каток работает, про лёд не знаем - не идём
assert hot_odno_tochno(0, 1) == 1                  # прогноз молчит, тучи - беру зонт
assert vektor2(naruzhu) == vektor2(oba_tochno)     # наружу = оба точно
assert vektor2(propustit) == vektor2(oba_tochno)   # пропустить = оба точно
assert vektor2(mozhno) == vektor2(hot_odno_tochno) # можно = хоть одно точно

print("наружу вектором:", vektor2(naruzhu))
print("усомниться вектором:", vektor2(usomnitsya))
print("Е.3: все проверки прошли")
