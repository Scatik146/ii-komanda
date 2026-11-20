"""Проверка шага Б части 2: Б.1 — 33 закона части 1 на тритах; Б.2 — где и как ломаются ★;
Б.3 — что от ★ остаётся.
Каждый закон — на всех наборах: 3 для одной буквы, 9 для двух, 27 для трёх.
Бит 1 → 1, бит 0 (ложь) → −1; НЕ = −x, И = min, ИЛИ = max,
x → y = ¬x ∨ y, x ≡ y = (x → y) ∧ (y → x).
Запуск: python3 proverka_B2.py chast-2-trit/B-zakony.md
        python3 proverka_B2.py --tablica   (таблица держащихся законов для текста)
        python3 proverka_B2.py --tablica-b2   (таблица Б.2: где ломается каждый ★)
        python3 proverka_B2.py --tablica-b3   (таблица Б.3: что остаётся от каждого ★)"""
import sys
from itertools import product
from pathlib import Path

ZDES = Path(__file__).parent
TRITY = (-1, 0, 1)
BITY = (-1, 1)


# ne: НЕ меняет знак
def ne(x):
    otvet = -x
    return otvet


# i_: И берёт меньшее
def i_(x, y):
    otvet = min(x, y)
    return otvet


# ili: ИЛИ берёт большее
def ili(x, y):
    otvet = max(x, y)
    return otvet


# sl: стрелка «если x, то y» = ¬x ∨ y (договор, как в части 1)
def sl(x, y):
    otvet = ili(ne(x), y)
    return otvet


# ekv: x ≡ y = (x → y) ∧ (y → x) (договор)
def ekv(x, y):
    otvet = i_(sl(x, y), sl(y, x))
    return otvet


# ZAKONY: (группа, закон на тритах, название, ★, букв, левая часть, правая часть)
# «0» части 1 записан как −1: это ложь, а не «не знаю»
ZAKONY = [
    (1, "x ∧ 1 = x", "", False, 1, lambda x: i_(x, 1), lambda x: x),
    (1, "x ∧ −1 = −1", "", False, 1, lambda x: i_(x, -1), lambda x: -1),
    (1, "x ∨ −1 = x", "", False, 1, lambda x: ili(x, -1), lambda x: x),
    (1, "x ∨ 1 = 1", "", False, 1, lambda x: ili(x, 1), lambda x: 1),
    (2, "x ∧ x = x", "идемпотентность для И", False, 1, lambda x: i_(x, x), lambda x: x),
    (2, "x ∨ x = x", "идемпотентность для ИЛИ", False, 1, lambda x: ili(x, x), lambda x: x),
    (2, "¬¬x = x", "двойное отрицание", False, 1, lambda x: ne(ne(x)), lambda x: x),
    (2, "x ∨ ¬x = 1", "исключённого третьего", True, 1, lambda x: ili(x, ne(x)), lambda x: 1),
    (2, "x ∧ ¬x = −1", "противоречия", True, 1, lambda x: i_(x, ne(x)), lambda x: -1),
    (3, "x ∧ y = y ∧ x", "переместительный для И", False, 2,
     lambda x, y: i_(x, y), lambda x, y: i_(y, x)),
    (3, "x ∨ y = y ∨ x", "переместительный для ИЛИ", False, 2,
     lambda x, y: ili(x, y), lambda x, y: ili(y, x)),
    (3, "(x ∧ y) ∧ z = x ∧ (y ∧ z)", "сочетательный для И", False, 3,
     lambda x, y, z: i_(i_(x, y), z), lambda x, y, z: i_(x, i_(y, z))),
    (3, "(x ∨ y) ∨ z = x ∨ (y ∨ z)", "сочетательный для ИЛИ", False, 3,
     lambda x, y, z: ili(ili(x, y), z), lambda x, y, z: ili(x, ili(y, z))),
    (4, "x ∧ (y ∨ z) = (x ∧ y) ∨ (x ∧ z)", "распределительный И относительно ИЛИ", False, 3,
     lambda x, y, z: i_(x, ili(y, z)), lambda x, y, z: ili(i_(x, y), i_(x, z))),
    (4, "x ∨ (y ∧ z) = (x ∨ y) ∧ (x ∨ z)", "распределительный ИЛИ относительно И", False, 3,
     lambda x, y, z: ili(x, i_(y, z)), lambda x, y, z: i_(ili(x, y), ili(x, z))),
    (5, "¬(x ∧ y) = ¬x ∨ ¬y", "де Моргана для И", False, 2,
     lambda x, y: ne(i_(x, y)), lambda x, y: ili(ne(x), ne(y))),
    (5, "¬(x ∨ y) = ¬x ∧ ¬y", "де Моргана для ИЛИ", False, 2,
     lambda x, y: ne(ili(x, y)), lambda x, y: i_(ne(x), ne(y))),
    (6, "x ∧ (x ∨ y) = x", "поглощение для И", False, 2,
     lambda x, y: i_(x, ili(x, y)), lambda x, y: x),
    (6, "x ∨ (x ∧ y) = x", "поглощение для ИЛИ", False, 2,
     lambda x, y: ili(x, i_(x, y)), lambda x, y: x),
    (6, "(x ∧ y) ∨ (x ∧ ¬y) = x", "склеивание для ИЛИ", True, 2,
     lambda x, y: ili(i_(x, y), i_(x, ne(y))), lambda x, y: x),
    (6, "(x ∨ y) ∧ (x ∨ ¬y) = x", "склеивание для И", True, 2,
     lambda x, y: i_(ili(x, y), ili(x, ne(y))), lambda x, y: x),
    (6, "x ∨ (¬x ∧ y) = x ∨ y", "Блейка - Порецкого для ИЛИ", True, 2,
     lambda x, y: ili(x, i_(ne(x), y)), lambda x, y: ili(x, y)),
    (6, "x ∧ (¬x ∨ y) = x ∧ y", "Блейка - Порецкого для И", True, 2,
     lambda x, y: i_(x, ili(ne(x), y)), lambda x, y: i_(x, y)),
    (7, "x → y = ¬x ∨ y", "импликация через ИЛИ", False, 2,
     lambda x, y: sl(x, y), lambda x, y: ili(ne(x), y)),
    (7, "x → y = ¬y → ¬x", "контрапозиция", False, 2,
     lambda x, y: sl(x, y), lambda x, y: sl(ne(y), ne(x))),
    (7, "¬(x → y) = x ∧ ¬y", "отрицание импликации", False, 2,
     lambda x, y: ne(sl(x, y)), lambda x, y: i_(x, ne(y))),
    (7, "1 → x = x", "из единицы", False, 1, lambda x: sl(1, x), lambda x: x),
    (7, "−1 → x = 1", "из нуля (из лжи)", False, 1, lambda x: sl(-1, x), lambda x: 1),
    (7, "x → x = 1", "из себя", True, 1, lambda x: sl(x, x), lambda x: 1),
    (7, "(x ∧ y) → z = x → (y → z)", "экспортация", False, 3,
     lambda x, y, z: sl(i_(x, y), z), lambda x, y, z: sl(x, sl(y, z))),
    (7, "(x ∧ (x → y)) → y = 1", "модус поненс", True, 2,
     lambda x, y: sl(i_(x, sl(x, y)), y), lambda x, y: 1),
    (7, "x ≡ y = (x → y) ∧ (y → x)", "эквивалентность через стрелки", False, 2,
     lambda x, y: ekv(x, y), lambda x, y: i_(sl(x, y), sl(y, x))),
    (7, "x ≡ y = (x ∧ y) ∨ (¬x ∧ ¬y)", "эквивалентность через И, ИЛИ, НЕ", False, 2,
     lambda x, y: ekv(x, y), lambda x, y: ili(i_(x, y), i_(ne(x), ne(y)))),
]


# kontrprimer: первый набор, где части не совпали, или None
def kontrprimer(zakon, znacheniya):
    _, _, _, _, bukv, levaya, pravaya = zakon
    plohie = [n for n in product(znacheniya, repeat=bukv) if levaya(*n) != pravaya(*n)]
    otvet = plohie[0] if plohie else None
    return otvet


# derzhitsya: закон верен на всех наборах
def derzhitsya(zakon, znacheniya):
    otvet = kontrprimer(zakon, znacheniya) is None
    return otvet


# PRIMERY: что утверждает текст Б.1 — (что, получилось, должно быть)
PRIMERY = [
    ("де Морган: ¬(1 ∧ 0) = 0", ne(i_(1, 0)), 0),
    ("де Морган: ¬1 ∨ ¬0 = 0", ili(ne(1), ne(0)), 0),
    ("поглощение: 0 ∨ (0 ∧ 1) = 0", ili(0, i_(0, 1)), 0),
    ("распределительный: 0 ∧ (−1 ∨ 1) = 0", i_(0, ili(-1, 1)), 0),
    ("распределительный: (0 ∧ −1) ∨ (0 ∧ 1) = 0", ili(i_(0, -1), i_(0, 1)), 0),
    ("контрапозиция: 1 → 0 = 0", sl(1, 0), 0),
    ("контрапозиция: ¬0 → ¬1 = 0", sl(ne(0), ne(1)), 0),
    ("забыли перевод: −1 ∧ 0 = −1", i_(-1, 0), -1),
    ("★ уже на пороге: 0 ∨ ¬0 = 0", ili(0, ne(0)), 0),
]
# LOMAETSYA: контрпримеры текста — должно НЕ совпасть
LOMAETSYA = [
    ("x ∧ 0 = 0 с тритом 0 при x = −1", i_(-1, 0), 0),
    ("x ∨ ¬x = 1 при x = 0", ili(0, ne(0)), 1),
]


# proverit_primery: (ошибок, строки отчёта)
def proverit_primery():
    oshibki, otchet = 0, []
    for chto, vyshlo, nado in PRIMERY:
        if vyshlo != nado:
            oshibki += 1
            otchet.append(f"ОШИБКА пример: {chto} → {vyshlo}")
    for chto, vyshlo, nado in LOMAETSYA:
        if vyshlo == nado:
            oshibki += 1
            otchet.append(f"ОШИБКА контрпример совпал: {chto}")
    return oshibki, otchet


# proverit_zakony: (ошибок, строки отчёта) — ★ ломаются, остальные держатся, на битах все
def proverit_zakony():
    oshibki, otchet = 0, []
    for zakon in ZAKONY:
        if not derzhitsya(zakon, BITY):
            oshibki += 1
            otchet.append(f"ОШИБКА на битах не держится: {zakon[1]}")
        if derzhitsya(zakon, TRITY) == zakon[3]:
            oshibki += 1
            otchet.append(f"ОШИБКА ★ не совпала: {zakon[1]} {kontrprimer(zakon, TRITY)}")
    return oshibki, otchet


# zvezdy_chasti_1: названия законов со ★ из таблиц Б.1 части 1
def zvezdy_chasti_1():
    tekst = (ZDES / "chast-1-bit" / "B-zakony.md").read_text(encoding="utf-8")
    b1 = tekst.split("## Б.2", 1)[0]
    imena = []
    for stroka in b1.splitlines():
        yachejki = [y.strip() for y in stroka.strip("|").split("|")]
        if stroka.startswith("|") and "★" in yachejki[0]:
            imena.append(yachejki[1])
    return imena


# sverit_zvezdy: ★ у нас = ★ в части 1
def sverit_zvezdy():
    nashi = sorted(z[2] for z in ZAKONY if z[3])
    ih = sorted(zvezdy_chasti_1())
    oshibki = 0 if nashi == ih else 1
    otchet = [] if oshibki == 0 else [f"ОШИБКА ★: у нас {nashi}, в части 1 {ih}"]
    return oshibki, otchet


# stroki_tablicy_teksta: законы из таблиц раздела Б.1 текста (первая ячейка)
def stroki_tablicy_teksta(put):
    tekst = put.read_text(encoding="utf-8")
    b1 = tekst.split("## Б.1", 1)[1].split("\n## ", 1)[0]
    zakony = []
    for stroka in b1.splitlines():
        yachejki = [y.strip() for y in stroka.strip("|").split("|")]
        if stroka.startswith("|") and "=" in yachejki[0]:
            zakony.append(yachejki[0])
    return zakony


# sverit_tekst: в таблице Б.1 ровно держащиеся законы
def sverit_tekst(put):
    v_tekste = sorted(stroki_tablicy_teksta(put))
    nado = sorted(z[1] for z in ZAKONY if not z[3])
    oshibki = 0 if v_tekste == nado else 1
    lishnie = set(v_tekste) - set(nado)
    netu = set(nado) - set(v_tekste)
    otchet = [] if oshibki == 0 else [f"ОШИБКА таблица текста: лишние {lishnie}, нет {netu}"]
    return oshibki, otchet


# tablica: держащиеся законы по группам — строки Markdown для текста
def tablica():
    stroki = ["| Закон на тритах | Название |", "|---|---|"]
    for z in ZAKONY:
        if not z[3]:
            stroki.append(f"| {z[1]} | {z[2] or 'с константой'} |")
    return "\n".join(stroki)


# itog: сводка по законам
def itog():
    derzh = sum(1 for z in ZAKONY if derzhitsya(z, TRITY))
    stroka = f"законов {len(ZAKONY)}, на тритах держатся {derzh}, ★ ломаются {len(ZAKONY) - derzh}"
    return stroka


# pechat_zvezd: где ломается каждый ★ — первый набор
def pechat_zvezd():
    for z in ZAKONY:
        if z[3]:
            print(f"★ {z[1]}: ломается на {kontrprimer(z, TRITY)}")


# ---- Б.2. Что ломается ----

# vse_polomki: все наборы, где части не совпали — (набор, слева, справа)
def vse_polomki(zakon):
    _, _, _, _, bukv, levaya, pravaya = zakon
    nabory = product(TRITY, repeat=bukv)
    otvet = [(n, levaya(*n), pravaya(*n)) for n in nabory if levaya(*n) != pravaya(*n)]
    return otvet


# trit: трит строкой, минус — настоящий
def trit(t):
    otvet = "−1" if t == -1 else str(t)
    return otvet


# nabor_slovami: (1, 0) → «x = 1, y = 0»
def nabor_slovami(nabor):
    otvet = ", ".join(f"{b} = {trit(t)}" for b, t in zip("xyz", nabor))
    return otvet


# PRIMERY_B2: что утверждает текст Б.2 — (что, получилось, должно быть)
PRIMERY_B2 = [
    ("противоречия: 0 ∧ ¬0 = 0", i_(0, ne(0)), 0),
    ("склеивание: (1 ∧ 0) ∨ (1 ∧ ¬0) = 0", ili(i_(1, 0), i_(1, ne(0))), 0),
    ("Блейк - Порецкий: 0 ∨ (¬0 ∧ 1) = 0", ili(0, i_(ne(0), 1)), 0),
    ("Блейк - Порецкий справа: 0 ∨ 1 = 1", ili(0, 1), 1),
    ("модус поненс: 1 → 0 = 0", sl(1, 0), 0),
    ("модус поненс: 1 ∧ 0 = 0", i_(1, 0), 0),
    ("модус поненс: 0 → 0 = 0", sl(0, 0), 0),
    ("x → x при x = 0 — это 0 ∨ 0", sl(0, 0), ili(ne(0), 0)),
    ("починка: 0 ∨ ¬0 — это то же 0 ∨ 0", ili(0, ne(0)), ili(0, 0)),
] + [
    (f"модус поненс = ¬x ∨ (x ∧ ¬y) ∨ y при {n}",
     sl(i_(n[0], sl(n[0], n[1])), n[1]), ili(ili(ne(n[0]), i_(n[0], ne(n[1]))), n[1]))
    for n in product(TRITY, repeat=2)
]
# NABOROV_B2: (всего наборов у ★, из них ломаются) — числа из текста
NABOROV_B2 = (54, 10)


# zamechaniya_polomki: ошибки одной поломки — без 0 или не «молчит»
def zamechaniya_polomki(zakon, nabor, sleva, sprava):
    otchet = []
    if 0 not in nabor:
        otchet.append(f"ОШИБКА Б.2 ломается без 0: {zakon[1]} {nabor}")
    if sleva != 0 or sprava == 0:
        otchet.append(f"ОШИБКА Б.2 не «молчит»: {zakon[1]} {nabor} {sleva} {sprava}")
    return otchet


# proverit_polomki: строки ошибок — в каждой поломке есть 0; слева «не знаю», справа знание
def proverit_polomki():
    otchet = [s for z in ZAKONY for n, l, p in vse_polomki(z) for s in zamechaniya_polomki(z, n, l, p)]
    return otchet


# proverit_chisla_b2: строки ошибок — сколько наборов у ★ и сколько ломается
def proverit_chisla_b2():
    zvezdy = [z for z in ZAKONY if z[3]]
    vsego = sum(3 ** z[4] for z in zvezdy)
    lomaetsya = sum(len(vse_polomki(z)) for z in zvezdy)
    otchet = [] if (vsego, lomaetsya) == NABOROV_B2 else [f"ОШИБКА Б.2 наборов: {vsego}, ломается {lomaetsya}"]
    return otchet


# proverit_b2: (ошибок, строки отчёта) — поломки, примеры, числа раздела Б.2
def proverit_b2():
    primery = [f"ОШИБКА пример Б.2: {c} → {v}" for c, v, n in PRIMERY_B2 if v != n]
    otchet = proverit_polomki() + primery + proverit_chisla_b2()
    return len(otchet), otchet


# tablica_b2: где ломается каждый ★ — строки Markdown для текста
def tablica_b2():
    stroki = ["| Закон | Название | Где ломается | Слева | Должно быть |", "|---|---|---|---|---|"]
    for z in ZAKONY:
        polomki = vse_polomki(z)
        if z[3]:
            gde = "; ".join(nabor_slovami(n) for n, _, _ in polomki)
            stroki.append(f"| {z[1]} | {z[2]} | {gde} | {trit(polomki[0][1])} | {trit(polomki[0][2])} |")
    return "\n".join(stroki)


# sverit_tekst_b2: таблица раздела Б.2 текста = tablica_b2()
def sverit_tekst_b2(put):
    tekst = put.read_text(encoding="utf-8")
    razdel = tekst.split("## Б.2", 1)[1].split("\n## ", 1)[0] if "## Б.2" in tekst else ""
    v_tekste = [s for s in razdel.splitlines() if s.startswith("|")]
    nado = tablica_b2().splitlines()
    oshibki = 0 if v_tekste == nado else 1
    otchet = [] if oshibki == 0 else ["ОШИБКА таблица Б.2 в тексте не совпала с программой"]
    return oshibki, otchet


# ---- Б.3. Что остаётся ----

# PARY: у каждого ★ — буквы, которые стоят рядом со своим отрицанием (номера: x = 0, y = 1)
PARY = {
    "исключённого третьего": (0,),
    "противоречия": (0,),
    "склеивание для ИЛИ": (1,),
    "склеивание для И": (1,),
    "Блейка - Порецкого для ИЛИ": (0,),
    "Блейка - Порецкого для И": (0,),
    "из себя": (0,),
    "модус поненс": (0, 1),
}
# NE_BYVAET: правая часть-константа → что остаётся от закона
NE_BYVAET = {1: "никогда не ложь", -1: "никогда не правда"}


# konstanta: правая часть — одно число на всех наборах, иначе None
def konstanta(zakon):
    _, _, _, _, bukv, _, pravaya = zakon
    vse = {pravaya(*n) for n in product(TRITY, repeat=bukv)}
    otvet = min(vse) if len(vse) == 1 else None
    return otvet


# znacheniya_levoj: все значения левой части на тритах
def znacheniya_levoj(zakon):
    _, _, _, _, bukv, levaya, _ = zakon
    otvet = {levaya(*n) for n in product(TRITY, repeat=bukv)}
    return otvet


# derzhitsya_pri: закон верен, когда буквы izvestnye — да или нет, остальные — любые триты
def derzhitsya_pri(zakon, izvestnye):
    _, _, _, _, bukv, levaya, pravaya = zakon
    nabory = [n for n in product(TRITY, repeat=bukv) if all(n[k] in BITY for k in izvestnye)]
    otvet = all(levaya(*n) == pravaya(*n) for n in nabory)
    return otvet


# chto_ostaetsya: что остаётся от ★ — строкой для таблицы
def chto_ostaetsya(zakon):
    c = konstanta(zakon)
    po_bukvam = "держится, если известен " + " и ".join("xyz"[k] for k in PARY[zakon[2]])
    otvet = NE_BYVAET[c] if c is not None else po_bukvam
    return otvet


# zamechaniya_pary: ошибки пар — держится при известных буквах пары; без любой из них — нет
def zamechaniya_pary(zakon):
    para = PARY[zakon[2]]
    otchet = [] if derzhitsya_pri(zakon, para) else [f"ОШИБКА Б.3 не держится при известных {para}: {zakon[1]}"]
    lishnie = [k for k in para if derzhitsya_pri(zakon, tuple(b for b in para if b != k))]
    otchet += [f"ОШИБКА Б.3 буква {k} не нужна: {zakon[1]}" for k in lishnie]
    return otchet


# zamechaniya_konstanty: «никогда не ложь» — нет −1; «никогда не правда» — нет 1; но 0 бывает
def zamechaniya_konstanty(zakon):
    c = konstanta(zakon)
    znacheniya = znacheniya_levoj(zakon)
    plohie = c is not None and (-c in znacheniya or 0 not in znacheniya)
    otchet = [f"ОШИБКА Б.3 {zakon[1]}: слева бывает {sorted(znacheniya)}"] if plohie else []
    return otchet


# zamechaniya_rechi: где левая часть сказала «да» или «нет» — она совпала с правой
def zamechaniya_rechi(zakon):
    _, _, _, _, bukv, levaya, pravaya = zakon
    plohie = [n for n in product(TRITY, repeat=bukv) if levaya(*n) in BITY and levaya(*n) != pravaya(*n)]
    otchet = [f"ОШИБКА Б.3 заговорил и соврал: {zakon[1]} {n}" for n in plohie]
    return otchet


# PRIMERY_B3: что утверждает текст Б.3 — (что, получилось, должно быть)
PRIMERY_B3 = [
    ("дождь: 1 ∨ ¬1 = 1", ili(1, ne(1)), 1),
    ("дождь: −1 ∨ ¬(−1) = 1", ili(-1, ne(-1)), 1),
    ("дождь: 0 ∨ ¬0 = 0", ili(0, ne(0)), 0),
    ("посылка: 1 → 1 = 1", sl(1, 1), 1),
    ("посылка: 1 ∧ 1 = 1", i_(1, 1), 1),
    ("посылка: модус поненс при (1, 1) = 1", sl(i_(1, sl(1, 1)), 1), 1),
    ("посылка: 1 → 0 = 0", sl(1, 0), 0),
    ("посылка: 1 ∧ 0 = 0", i_(1, 0), 0),
    ("посылка: 0 → 0 = 0", sl(0, 0), 0),
    ("посылка: модус поненс при (1, 0) = 0", sl(i_(1, sl(1, 0)), 0), 0),
    ("x → x при x = 0 — 0", sl(0, 0), 0),
    ("магазин: 1 ∧ ¬1 = −1", i_(1, ne(1)), -1),
    ("магазин: −1 ∧ ¬(−1) = −1", i_(-1, ne(-1)), -1),
    ("магазин: 0 ∧ ¬0 = 0", i_(0, ne(0)), 0),
    ("концерт: (1 ∧ 1) ∨ (1 ∧ ¬1) = 1", ili(i_(1, 1), i_(1, ne(1))), 1),
    ("концерт: (1 ∧ −1) ∨ (1 ∧ ¬(−1)) = 1", ili(i_(1, -1), i_(1, ne(-1))), 1),
    ("концерт: (0 ∧ 1) ∨ (0 ∧ ¬1) = 0", ili(i_(0, 1), i_(0, ne(1))), 0),
    ("концерт, контрпример: (1 ∧ 0) ∨ (1 ∧ ¬0) = 0", ili(i_(1, 0), i_(1, ne(0))), 0),
    ("ключ: −1 ∨ (¬(−1) ∧ 1) = 1", ili(-1, i_(ne(-1), 1)), 1),
    ("ключ справа: −1 ∨ 1 = 1", ili(-1, 1), 1),
    ("ключ: 1 ∨ (¬1 ∧ 0) = 1", ili(1, i_(ne(1), 0)), 1),
    ("ключ справа: 1 ∨ 0 = 1", ili(1, 0), 1),
    ("ключ, контрпример: 0 ∨ (¬0 ∧ 1) = 0", ili(0, i_(ne(0), 1)), 0),
    ("ключ, контрпример справа: 0 ∨ 1 = 1", ili(0, 1), 1),
] + [
    (f"прибор: x ∨ ¬x при x = {x} — знаем ли x", ili(x, ne(x)), 1 if x in BITY else 0) for x in TRITY
] + [
    (f"де Морган: x ∧ ¬x = ¬(x ∨ ¬x) при x = {x}", i_(x, ne(x)), ne(ili(x, ne(x)))) for x in TRITY
]


# proverit_b3: (ошибок, строки отчёта) — константы, пары, «заговорил — прав», примеры Б.3
def proverit_b3():
    zvezdy = [z for z in ZAKONY if z[3]]
    zakony = [s for z in zvezdy for s in zamechaniya_konstanty(z) + zamechaniya_pary(z) + zamechaniya_rechi(z)]
    primery = [f"ОШИБКА пример Б.3: {c} → {v}" for c, v, n in PRIMERY_B3 if v != n]
    otchet = zakony + primery
    return len(otchet), otchet


# tablica_b3: что остаётся от каждого ★ — строки Markdown для текста
def tablica_b3():
    stroki = ["| Закон | Название | Что остаётся |", "|---|---|---|"]
    stroki += [f"| {z[1]} | {z[2]} | {chto_ostaetsya(z)} |" for z in ZAKONY if z[3]]
    return "\n".join(stroki)


# sverit_tekst_b3: таблица раздела Б.3 текста = tablica_b3()
def sverit_tekst_b3(put):
    tekst = put.read_text(encoding="utf-8")
    razdel = tekst.split("## Б.3", 1)[1].split("\n## ", 1)[0] if "## Б.3" in tekst else ""
    v_tekste = [s for s in razdel.splitlines() if s.startswith("|")]
    oshibki = 0 if v_tekste == tablica_b3().splitlines() else 1
    otchet = [] if oshibki == 0 else ["ОШИБКА таблица Б.3 в тексте не совпала с программой"]
    return oshibki, otchet


# proverit_vse: все проверки, напечатать отчёт, вернуть число ошибок
def proverit_vse(argumenty):
    chasti = [proverit_zakony(), sverit_zvezdy(), proverit_primery(), proverit_b2(), proverit_b3()]
    if argumenty:
        chasti.append(sverit_tekst(ZDES / argumenty[0]))
        chasti.append(sverit_tekst_b2(ZDES / argumenty[0]))
        chasti.append(sverit_tekst_b3(ZDES / argumenty[0]))
    oshibki = sum(o for o, _ in chasti)
    for _, otchet in chasti:
        print("\n".join(otchet)) if otchet else None
    pechat_zvezd()
    print(itog())
    print(f"ошибок: {oshibki}")
    return oshibki


# glavnoe: --tablica / --tablica-b2 / --tablica-b3 печатают таблицу, иначе проверки; код выхода = число ошибок
def glavnoe(argumenty):
    tolko_tablica = bool(argumenty) and argumenty[0].startswith("--tablica")
    print(tablica()) if tolko_tablica and argumenty[0] == "--tablica" else None
    print(tablica_b2()) if tolko_tablica and argumenty[0] == "--tablica-b2" else None
    print(tablica_b3()) if tolko_tablica and argumenty[0] == "--tablica-b3" else None
    oshibki = 0 if tolko_tablica else proverit_vse(argumenty)
    return oshibki


if __name__ == "__main__":
    sys.exit(glavnoe(sys.argv[1:]))
