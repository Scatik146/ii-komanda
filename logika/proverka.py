# Проверка таблиц функций «Логики очень осторожного человека» (Марьям, 19.11.2026)
# Запуск: python3 proverka.py — проверяет свойства и печатает таблицы.
# Значения: -1 нет / 0 не знаю / 1 да. Четвёртое значение «нет» (атома нет вовсе) — None.

from functools import reduce

V = [-1, 0, 1]
NET = None

# --- слой 1: функции значений ---

# ne: Ф0 «не» — переворачивает да и нет, «не знаю» оставляет
def ne(x):
    return -x

# i: Ф1 «и» — один ноль держит цепочку, одна ложь её рвёт
def i(x, y):
    return min(x, y)

# ili: Ф1а «или»
def ili(x, y):
    return max(x, y)

# osn: Ф2 основание (запись DeepSeek)
def osn(x, b):
    return ili(i(x, b), i(ne(b), 0))

# osn_old: Ф2, прежняя запись Марьям — для сверки
def osn_old(x, b):
    return ili(i(x, ili(b, 0)), i(ne(b), 0))

# soglasie: Ф3 согласие — одинаково → это значение, разное → 0
def soglasie(x, y):
    return ili(i(x, y), i(ili(x, y), 0))

# zapret: Ф6 запрет — «если r, то нужна o»; 1 = нарушено
def zapret(r, o):
    return i(r, ne(o))

# prov: Ф7 проверено по статусу и экспертизе (ОЧ-03)
def prov(stat, eksp):
    if stat == -1:
        otvet = -1
    elif eksp == 0:
        otvet = 0
    else:
        otvet = 1 if stat >= eksp else -1
    return otvet

# prov_srok: Ф7 со сроком — до срока и при неизвестном сроке 0 (это Ф2); без срока как раньше
def prov_srok(stat, eksp, srok=None):
    return prov(stat, eksp) if srok is None else osn(prov(stat, eksp), srok)

# srabot: Ф9 срабатывает — посылка «нет» правило не запускает (ОЧ-13)
def srabot(p):
    return -1 if p is NET else M(p)

# ekspertiza: ОЧ-19 — при «не знаю» берётся вердикт независимого эксперта
def ekspertiza(x, verdikt, nezav):
    return x if x != 0 else osn(verdikt, nezav)

# --- слой 2: вывод (значения «есть пример» приходят из Пролога: 1 найдено, -1 полный список, 0 не определено) ---

# sleduet: Ф12 следование Axy = Vx·V′xy′·Vy (Брусенцов)
def sleduet(vx, kontr, vy):
    return i(vx, i(ne(kontr), vy))

# dlya_vseh: Ф13 «для всех» — ни одного контрпримера (∀x = V′x′)
def dlya_vseh(kontr):
    return ne(kontr)

# sushchestvuet: Ф14 «существует» — есть пример (Mx = Vx)
def sushchestvuet(primer):
    return primer

# ne_dokazano: Ф15 tnot — «не» над выведенным; «не определено» остаётся 0
def ne_dokazano(p):
    return ne(p)

# ravnosilno: Ф16 равносильно — следует в обе стороны
def ravnosilno(sl_xy, sl_yx):
    return i(sl_xy, sl_yx)

# --- слой 3: действия (пишут только в журнал решений, ОЧ-17) ---

# L: Ф4 ворота «необходимо» — только «да» → делать
def L(x):
    return 1 if x == 1 else -1

# M: Ф5 «возможно» — не «нет» → можно
def M(x):
    return -1 if x == -1 else 1

# Q: Ф11 «не знаю ли?» = случайность Q Брусенцова (Qx = Mx·Mx′)
def Q(x):
    return i(M(x), M(ne(x)))

# vosst: Ф8 восстановимо — можно, если обратимо или автор решил (ОЧ-Б8)
def vosst(obr, resh):
    return ili(obr, L(resh))

# J: характеристическая функция значения v (Россер — Тюркетт)
def J(v):
    return lambda x: 1 if x == v else -1

# --- слой 4: время ---

# budet: Т8 неотвратимо будет — согласие по закрытому списку вариантов (пирсовское F Прайора)
def budet(vetki):
    return reduce(soglasie, vetki)

# dolya: Т10 доля — сколько раз «да» из скольких
def dolya(sluchai):
    return sum(1 for x in sluchai if x == 1), len(sluchai)

# --- служебные слова проверки ---

# tab2: таблица функции двух переменных (строки x, столбцы y)
def tab2(f):
    return [[f(x, y) for y in V] for x in V]

# tab1: таблица функции одной переменной
def tab1(f):
    return [f(x) for x in V]

# ne_huzhe: «a не меньше знает, чем b»: 0 ≤ всё, ±1 — только себе
def ne_huzhe(a, b):
    return a == 0 or a == b

# monoton2: монотонность по знанию — 0 на входе не превращается в ±1 сам
def monoton2(f):
    return all(ne_huzhe(f(a, b), f(c, d)) for a in V for b in V for c in V for d in V
               if ne_huzhe(a, c) and ne_huzhe(b, d))

# --- проверки ---

# слой 1
assert tab2(osn) == tab2(osn_old), "две записи основания расходятся"
assert tab2(osn) == [[0, 0, -1], [0, 0, 0], [0, 0, 1]]
assert tab2(soglasie) == [[-1, 0, 0], [0, 0, 0], [0, 0, 1]]
assert all(soglasie(x, x) == x for x in V)                                  # идемпотентна
assert all(soglasie(soglasie(x, y), z) == soglasie(x, soglasie(y, z))
           for x in V for y in V for z in V)                                # ассоциативна
assert tab2(zapret) == [[-1, -1, -1], [0, 0, -1], [1, 0, -1]]               # у GLM была ошибка
assert tab2(prov) == [[-1, -1, -1], [1, 0, -1], [1, 0, 1]]
assert monoton2(i) and monoton2(ili) and monoton2(osn) and monoton2(soglasie) and monoton2(zapret)
assert not monoton2(prov)
# срок: Петя — ручная проверка прогноза, срок не наступил → 0, ворота закрыты
assert prov_srok(1, 1, -1) == 0 and L(i(1, prov_srok(1, 1, -1))) == -1
assert prov_srok(1, 1, 0) == 0                                              # срок неизвестен
assert prov_srok(1, 1, 1) == 1                                              # срок наступил
assert all(prov_srok(s, e) == prov(s, e) for s in V for e in V)             # без срока — как раньше
# ОЧ-19: экспертиза может сказать и «нет»
assert ekspertiza(0, -1, 1) == -1 and ekspertiza(0, 1, 1) == 1
assert ekspertiza(0, 1, 0) == 0 and ekspertiza(0, 1, -1) == 0

# слой 2: контрпример найден → -1; не искали → 0; всё есть, контрпримера нет → 1
assert sleduet(1, 1, 1) == -1 and sleduet(1, 0, 1) == 0 and sleduet(1, -1, 1) == 1
assert sleduet(-1, -1, 1) == -1        # x-вещей нет — следования нет (в K3 было бы 1)
assert monoton2(lambda a, b: sleduet(a, b, 1))

# слой 3
assert tab1(L) == tab1(J(1))                                                # L = J(1)
assert tab1(M) == [max(J(1)(x), J(0)(x)) for x in V]                        # M = J(1) или J(0)
assert tab1(M) != tab1(J(0)) and tab1(M) != tab1(J(1))                      # M — не один J
assert all(M(x) == ne(L(ne(x))) for x in V)                                 # M = ¬L¬
assert tab1(Q) == tab1(J(0)) == [-1, 1, -1]                                 # Q = J(0)
assert all(max(L(x), Q(x), L(ne(x))) == 1 for x in V)                       # да / не знаю / нет — одно
# ОЧ-22: правильно L(¬x); у GLM ¬L(x) давал «придумывай» при «не знаю»
assert [L(ne(x)) for x in V] == [1, -1, -1]
assert [ne(L(x)) for x in V] == [1, 1, -1]

# слой 4: «морской бой будет и не будет» (Крессвелл 2007) — по вариантам −1, поатомно 0
p = [1, -1]
assert budet([i(x, ne(x)) for x in p]) == -1 and i(budet(p), ne(budet(p))) == 0
assert budet([ili(x, ne(x)) for x in p]) == 1 and ili(budet(p), ne(budet(p))) == 0
# поатомный подсчёт грубее, но не ошибается: где он даёт ±1, по вариантам то же
for a in [[x, y] for x in V for y in V]:
    for f in (lambda x: x, ne):
        assert budet([f(x) for x in a]) == f(budet(a)) or f(budet(a)) == 0
# Т10: Петя — 9 пятёрок из 10; «всегда пять» не следует, прогноз σ
petya = [1] * 9 + [-1]
assert dolya(petya) == (9, 10) and budet(petya) == 0
assert sleduet(1, 1, 1) == -1                                               # одна четвёрка — контрпример

if __name__ == "__main__":
    print("Ф2 основание   ", tab2(osn))
    print("Ф3 согласие    ", tab2(soglasie))
    print("Ф4 L           ", tab1(L))
    print("Ф5 M           ", tab1(M))
    print("Ф6 запрет      ", tab2(zapret))
    print("Ф7 проверено   ", tab2(prov))
    print("Ф8 восстановимо", [[vosst(o, r) for r in V] for o in (-1, 1)])
    print("Ф9 срабатывает ", [srabot(x) for x in (NET, -1, 0, 1)])
    print("Ф11 Q          ", tab1(Q))
    print("Ф12 следует (Vx × контрпример), Vy=1", [[sleduet(a, k, 1) for k in V] for a in V])
    print("Все проверки пройдены.")
