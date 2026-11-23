"""uzly.py — узлы калькуляторов из вентилей: окошки, таблица, полусумматор, сумматор, слово.

Двоичный — привычные схемы: перенос = И, сумма = исключающее ИЛИ, быстрый сумматор Когге — Стоуна,
умножитель Бо — Вули (дополнительный код) со сжатием Уоллеса.
Троичный — наш базис: окошки и «таблица» из книги (В.4); перенос полусумматора — согласие (В.1);
перенос по слову — тройка «какой перенос уйдёт при −1, 0, 1» и её применение окошками-порогами; знак — даром.
"""
from shema import DVOICHNYJ, TROICHNYJ, NASTROJKA, ne, i_, ili

TRITY = (-1, 0, 1)


# --- окошки и таблица (книга, В.4) ----------------------------------------------------------

# okna: {значение: окошко}; у трита — ворота(x), ворота(¬x), ¬ворота(x) ∧ ¬ворота(¬x); у бита — x и ¬x
def okna(s, x):
    if s.baza == DVOICHNYJ:
        rez = {1: x, 0: ne(s, x)}
    else:
        v1, vm = s.ventil('ворота', x), s.ventil('ворота', ne(s, x))
        rez = {1: v1, -1: vm, 0: i_(s, ne(s, v1), ne(s, vm))}
    return rez


# proizvedenie: И окошек клетки (слева направо — общие начала не повторяются)
def proizvedenie(s, okna_vhodov, kletka):
    rez = okna_vhodov[0][kletka[0]]
    for ok, z in zip(okna_vhodov[1:], kletka[1:]):
        rez = i_(s, rez, ok[z])
    return rez


# ili_mnogo: ИЛИ списка (деревом — глубина меньше); пусто → «нет»
def ili_mnogo(s, spisok):
    spisok = list(spisok) or [s.konst(0 if s.baza == DVOICHNYJ else -1)]
    while len(spisok) > 1:
        spisok = [ili(s, *spisok[i:i + 2]) if i + 1 < len(spisok) else spisok[i] for i in range(0, len(spisok), 2)]
    return spisok[0]


# po_tablice: рецепт книги: клетки с ответом 1 — ИЛИ окошек; с ответом 0 — то же, ∧ 0; всё через ИЛИ
def po_tablice(s, vhody, tablica):
    ok = [okna(s, x) for x in vhody]
    da = ili_mnogo(s, [proizvedenie(s, ok, k) for k, v in tablica.items() if v == 1])
    rez = da
    if s.baza == TROICHNYJ:
        nol = ili_mnogo(s, [proizvedenie(s, ok, k) for k, v in tablica.items() if v == 0])
        rez = ili(s, da, i_(s, nol, s.konst(0)))
    return rez


# --- сложение цифр --------------------------------------------------------------------------

# cifra_summy: младшая цифра суммы трит + трит (−2 → 1, 2 → −1); таблица 9 клеток
def cifra_summy(a, b):
    return (a + b + 1) % 3 - 1


# soglasie: согласие(x, y) = (x ∧ y) ∨ ((x ∨ y) ∧ 0) — перенос троичного полусумматора
def soglasie(s, x, y):
    return ili(s, i_(s, x, y), i_(s, ili(s, x, y), s.konst(0)))


# TABLICY: действия двух тритов, нужные калькулятору (вектор задаёт действие)
TABLICY = {
    'сумма': cifra_summy,
    'перенос': lambda a, b: max(min(a, b), min(max(a, b), 0)),
    'произведение': lambda a, b: a * b,
    'перенос при −1': lambda a, b: perenos_tritov(a, b, -1),
    'перенос при 1': lambda a, b: perenos_tritov(a, b, 1),
}

# SLOVA: как строить действие в схеме; по умолчанию — рецепт книги «по таблице»; luchshie.py ставит короче
SLOVA = {imya: (lambda f: lambda s, x, y: po_tablice(s, [x, y], {(a, b): f(a, b) for a in TRITY for b in TRITY}))(f)
         for imya, f in TABLICY.items()}
SLOVA['перенос'] = lambda s, x, y: soglasie(s, x, y)
# сложение переносов полусумматоров: оба сразу 1 (или −1) не бывают — эти клетки «всё равно», в таблицу не идут
SLOVA['переносы'] = lambda s, x, y: po_tablice(s, [x, y], {(a, b): a + b for a in TRITY for b in TRITY
                                                         if not a == b != 0})


# cifra_sdvigom: цифра суммы = a, сдвинутое по кругу b раз (окошки b выбирают a, сдвиг(a), сдвиг(сдвиг(a)))
def cifra_sdvigom(s, a, b):
    ok, c1 = okna(s, b), s.ventil('цикл', a)
    c2 = s.ventil('цикл', c1)
    return ili(s, ili(s, i_(s, ok[1], c1), i_(s, ok[0], a)), i_(s, ok[-1], c2))


# slovo: действие двух тритов по имени (вариант «сдвиг — деталь»: сумма и сложение переносов — сдвигом)
def slovo(s, imya, x, y):
    sdvigom = NASTROJKA['сдвиг'] and imya in ('сумма', 'переносы')
    return cifra_sdvigom(s, x, y) if sdvigom else SLOVA[imya](s, x, y)


# polusummator: (сумма, перенос) двух цифр
def polusummator(s, a, b):
    if NASTROJKA['детали']:
        para = (s.ventil('ПС+', a, b), s.ventil('ПС→', a, b))
    elif s.baza == DVOICHNYJ:
        para = (i_(s, ili(s, a, b), ne(s, i_(s, a, b))), i_(s, a, b))
    else:
        para = (slovo(s, 'сумма', a, b), slovo(s, 'перенос', a, b))
    return para


# summator: (сумма, перенос) трёх цифр — два полусумматора; переносы складываются без нового переноса
def summator(s, a, b, c):
    return (s.ventil('СМ+', a, b, c), s.ventil('СМ→', a, b, c)) if NASTROJKA['детали'] else summator_iz_pol(s, a, b, c)


# summator_iz_pol: сумматор из двух полусумматоров
def summator_iz_pol(s, a, b, c):
    s1, p1 = polusummator(s, a, b)
    s2, p2 = polusummator(s, s1, c)
    perenos = ili(s, p1, p2) if s.baza == DVOICHNYJ else slovo(s, 'переносы', p1, p2)
    return (s2, perenos)


# --- сложение слов --------------------------------------------------------------------------

# volna: сумматор «волной»: перенос идёт по разрядам (дёшево, медленно)
def volna(s, a, b, vhodnoj=None):
    c, rez = vhodnoj if vhodnoj is not None else s.konst(0), []
    for x, y in zip(a, b):
        cifra, c = summator(s, x, y, c)
        rez.append(cifra)
    return rez


# perenos_tritov: перенос из разряда a + b + c (c — пришедший снизу)
def perenos_tritov(a, b, c):
    return (a + b + c - cifra_summy(cifra_summy(a, b), c)) // 3


# karta_cifry: двоичный (порождает, пропускает); троичный — тройка: какой перенос уйдёт при c = −1, 0, 1
def karta_cifry(s, x, y):
    if s.baza == DVOICHNYJ:
        rez = (i_(s, x, y), polusummator(s, x, y)[0])
    else:
        rez = (slovo(s, 'перенос при −1', x, y), slovo(s, 'перенос', x, y), slovo(s, 'перенос при 1', x, y))
    return rez


# primenit: монотонная карта g (тройка) к триту u: g(−1) ∨ (g(0) ∧ «u ≥ 0») ∨ (g(1) ∧ «u ≥ 1»)
def primenit(s, g, u):
    ne_menshe_nulya = ne(s, s.ventil('ворота', ne(s, u)))
    return ili(s, g[0], ili(s, i_(s, g[1], ne_menshe_nulya), i_(s, g[2], s.ventil('ворота', u))))


# slozhit_karty: старшая g после младшей f; двоичный — (G ∨ P∧G′, P∧P′), троичный — g(f(c)) для c = −1, 0, 1
def slozhit_karty(s, g, f):
    if s.baza == DVOICHNYJ:
        rez = (ili(s, g[0], i_(s, g[1], f[0])), i_(s, g[1], f[1]))
    else:
        rez = tuple(primenit(s, g, fc) for fc in f)
    return rez


# perenos_iz_karty: перенос дальше, если в самый низ пришёл 0
def perenos_iz_karty(s, karta):
    return karta[0] if s.baza == DVOICHNYJ else karta[1]


# prefiks: карты отрезков 0..i (Когге — Стоун: шаг 1, 2, 4, …)
def prefiks(s, karty):
    shag = 1
    while shag < len(karty):
        karty = [slozhit_karty(s, k, karty[i - shag]) if i >= shag else k for i, k in enumerate(karty)]
        shag *= 2
    return karty


# bystryj: быстрый сумматор: цифра i = (a_i + b_i) по модулю ⊕ перенос из отрезка 0..i−1
def bystryj(s, a, b, vhodnoj=None):
    karty = [karta_cifry(s, x, y) for x, y in zip(a, b)]
    if vhodnoj is not None:
        karty = [(ili(s, karty[0][0], i_(s, karty[0][1], vhodnoj)), karty[0][1])] + karty[1:]
    pref = prefiks(s, karty)
    perenosy = [vhodnoj if vhodnoj is not None else s.konst(0)] + [perenos_iz_karty(s, k) for k in pref[:-1]]
    return [polusummator(s, polusummator(s, x, y)[0], c)[0] for x, y, c in zip(a, b, perenosy)]
