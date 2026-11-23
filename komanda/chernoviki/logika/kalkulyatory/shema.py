"""shema.py — схема из вентилей базиса: строим, считаем вентили и глубину, проверяем на числах.

Два базиса (книга: часть 1 — {И, ИЛИ, НЕ}; часть 2, В.4 — основной базис тритов {И, НЕ, ворота, 0}):
  двоичный: И, ИЛИ, НЕ над 0/1;
  троичный: И (меньшее), НЕ (−x), ворота (1 → 1, иначе −1) над −1/0/1; число 0 — деталь базиса.
ИЛИ у троичного — не деталь, а слово второго уровня: x ∨ y = ¬(¬x ∧ ¬y), три вентиля.
Числа-константы проводами (даром) — у обоих; одинаковые вентили не повторяются; ¬¬x = x; константы сворачиваются.
Цена — число вентилей (по видам); время — глубина: самый длинный путь от входа до выхода в вентилях.
"""
import numpy as np

DVOICHNYJ, TROICHNYJ = 2, 3
# NASTROJKA: вариант «ИЛИ у тритов — тоже деталь» (железу Т-КМОП всё равно, И или ИЛИ); по умолчанию — строго базис
NASTROJKA = {'ИЛИ у тритов': False, 'детали': False}
# «детали» — инженерный вариант: полусумматор (ПС) и сумматор (СМ) — готовые чёрные ящики, выход «+» — цифра, «→» — перенос


# Shema: вентили по порядку создания; у каждого — вид, входы, глубина
class Shema:
    # __init__: пустая схема нужного базиса
    def __init__(self, baza):
        self.baza, self.uzly, self.klyuchi, self.vhody = baza, [], {}, []

    # novyj: новый узел (вид, аргументы, глубина) → номер
    def novyj(self, vid, argi, glubina):
        self.uzly.append((vid, argi, glubina))
        return len(self.uzly) - 1

    # vhod: входной провод
    def vhod(self):
        n = self.novyj('вход', (), 0)
        self.vhody.append(n)
        return n

    # konst: число-провод (даром)
    def konst(self, c):
        klyuch = ('конст', c)
        if klyuch not in self.klyuchi:
            self.klyuchi[klyuch] = self.novyj('конст', (c,), 0)
        return self.klyuchi[klyuch]

    # znachenie_konst: число, если узел — константа, иначе None
    def znachenie_konst(self, n):
        vid, argi, _ = self.uzly[n]
        return argi[0] if vid == 'конст' else None

    # ventil: вентиль вида vid над входами (с повтором, ¬¬ и свёрткой констант)
    def ventil(self, vid, *argi):
        argi = tuple(sorted(argi)) if vid in ('И', 'ИЛИ') or vid[:2] in ('ПС', 'СМ') else argi
        uproshche = uprostit(self, vid, argi)
        if uproshche is None and (vid, argi) not in self.klyuchi:
            glubina = 1 + max(self.uzly[a][2] for a in argi)
            self.klyuchi[(vid, argi)] = self.novyj(vid, argi, glubina)
        return uproshche if uproshche is not None else self.klyuchi[(vid, argi)]


# DEJSTVIE: что делает вентиль над массивами чисел
DEJSTVIE = {
    (DVOICHNYJ, 'И'): lambda a, b: a & b, (DVOICHNYJ, 'ИЛИ'): lambda a, b: a | b,
    (DVOICHNYJ, 'НЕ'): lambda a: 1 - a,
    (TROICHNYJ, 'И'): np.minimum, (TROICHNYJ, 'НЕ'): lambda a: -a,
    (TROICHNYJ, 'ворота'): lambda a: np.where(a == 1, 1, -1), (TROICHNYJ, 'ИЛИ'): np.maximum,
    (DVOICHNYJ, 'ПС+'): lambda a, b: a ^ b, (DVOICHNYJ, 'ПС→'): lambda a, b: a & b,
    (DVOICHNYJ, 'СМ+'): lambda a, b, c: a ^ b ^ c, (DVOICHNYJ, 'СМ→'): lambda a, b, c: (a + b + c) // 2,
    (TROICHNYJ, 'ПС+'): lambda a, b: (a + b + 1) % 3 - 1, (TROICHNYJ, 'ПС→'): lambda a, b: (a + b - ((a + b + 1) % 3 - 1)) // 3,
    (TROICHNYJ, 'СМ+'): lambda a, b, c: (a + b + c + 1) % 3 - 1,
    (TROICHNYJ, 'СМ→'): lambda a, b, c: (a + b + c - ((a + b + c + 1) % 3 - 1)) // 3,
}


# uprostit: ¬¬x = x; x ∧ x = x; все входы — числа → число; иначе None (нужен вентиль)
def uprostit(s, vid, argi):
    konsty = [s.znachenie_konst(a) for a in argi]
    rez = None
    if vid == 'НЕ' and s.uzly[argi[0]][0] == 'НЕ':
        rez = s.uzly[argi[0]][1][0]
    elif vid in ('И', 'ИЛИ') and argi[0] == argi[1]:
        rez = argi[0]
    elif all(k is not None for k in konsty):
        rez = s.konst(int(DEJSTVIE[(s.baza, vid)](*[np.array(k) for k in konsty])))
    elif vid[:2] in ('ПС', 'СМ') and 0 in konsty:
        rez = bez_nulya(s, vid, [a for a, k in zip(argi, konsty) if k != 0])
    return rez if rez is not None else pogloshchenie(s, vid, argi, konsty)


# bez_nulya: деталь, у которой один вход — 0: сумматор → полусумматор; полусумматор → провод (перенос 0)
def bez_nulya(s, vid, ostalnye):
    if vid[:2] == 'СМ':
        rez = s.ventil('ПС' + vid[2:], *ostalnye)
    else:
        rez = ostalnye[0] if vid == 'ПС+' else s.konst(0)
    return rez


# pogloshchenie: И с крайним числом: «нет» поглощает, «да» пропускает (у ИЛИ двоичного наоборот)
def pogloshchenie(s, vid, argi, konsty):
    niz, verh = (0, 1) if s.baza == DVOICHNYJ else (-1, 1)
    rez = None
    for a, k in zip(argi, konsty):
        if vid == 'И' and k in (niz, verh):
            rez = s.konst(niz) if k == niz else argi[1 - argi.index(a)]
        if vid == 'ИЛИ' and k in (niz, verh):
            rez = s.konst(verh) if k == verh else argi[1 - argi.index(a)]
    return rez


# --- слова второго уровня ---------------------------------------------------------------

# ne: НЕ
def ne(s, x):
    return s.ventil('НЕ', x)


# i_: И
def i_(s, x, y):
    return s.ventil('И', x, y)


# ili: ИЛИ — у двоичного вентиль, у троичного ¬(¬x ∧ ¬y) (или вентиль, если так настроено)
def ili(s, x, y):
    detal = s.baza == DVOICHNYJ or NASTROJKA['ИЛИ у тритов']
    return s.ventil('ИЛИ', x, y) if detal else ne(s, i_(s, ne(s, x), ne(s, y)))


# --- счёт и проверка ------------------------------------------------------------------------

# podschet: {вид: сколько}, глубина выходов
def podschet(s, vyhody):
    nuzhny, stek = set(), list(vyhody)
    while stek:
        n = stek.pop()
        if n not in nuzhny:
            nuzhny.add(n)
            stek += [a for a in s.uzly[n][1] if s.uzly[n][0] != 'конст']
    vidy = {}
    for n in nuzhny:
        vid = s.uzly[n][0]
        vidy[vid] = vidy.get(vid, 0) + (vid not in ('вход', 'конст'))
    return ({v: k for v, k in vidy.items() if k}, max(s.uzly[n][2] for n in vyhody))


# vychislit: значения выходов при значениях входов (массивы — много примеров сразу)
def vychislit(s, znacheniya, vyhody):
    zn = dict(znacheniya)
    for n, (vid, argi, _) in enumerate(s.uzly):
        if n not in zn:
            zn[n] = np.full(len(next(iter(znacheniya.values()))), argi[0]) if vid == 'конст' else \
                DEJSTVIE[(s.baza, vid)](*[zn[a] for a in argi])
    return [zn[v] for v in vyhody]
