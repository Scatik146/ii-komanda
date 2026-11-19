# Двоичная логика — эталон и таблицы (Марьям, 19.11.2026)
# Запуск: python3 dvoich.py — проверяет всё перебором и пишет:
#   dvoichnaya.md (таблицы), primery-dvoich.json (примеры для Форта и Пролога), dvoich-bazisy.pl (базисы).
# Порядок строк таблицы истинности: x — старший разряд; вектор f(0,0) f(0,1) f(1,0) f(1,1); номер — вектор как двоичное число.

import json
from pathlib import Path

ZDES = Path(__file__).parent

IMENA = ["константа 0", "конъюнкция (И)", "запрет по y", "первая переменная x", "запрет по x",
         "вторая переменная y", "исключающее ИЛИ", "дизъюнкция (ИЛИ)", "стрелка Пирса (ИЛИ-НЕ)",
         "эквивалентность", "не y", "обратная импликация", "не x", "импликация", "штрих Шеффера (И-НЕ)", "константа 1"]
OBOZ = ["0", "x∧y, x&y, x·y, xy", "x∧¬y, x↛y", "x", "¬x∧y, x↚y", "y", "x⊕y, x≢y", "x∨y, x+y (в схемах)",
        "x↓y", "x≡y, x↔y, x~y", "¬y, ȳ", "x←y, y→x", "¬x, x̄", "x→y, x⊃y", "x|y", "1"]
ARIF = ["0", "xy", "x(1−y)", "x", "(1−x)y", "y", "x+y−2xy", "x+y−xy", "(1−x)(1−y)", "1−x−y+2xy",
        "1−y", "1−y+xy", "1−x", "1−x+xy", "1−xy", "1"]
SRAVN = ["—", "min(x,y)", "x > y", "—", "x < y", "—", "x ≠ y", "max(x,y)", "max(x,y) = 0", "x = y",
         "—", "x ≥ y", "—", "x ≤ y", "min(x,y) = 0", "—"]


# --- векторы ---

# vektor: биты вектора функции из её номера (n переменных)
def vektor(nomer, n=2):
    dlina = 2 ** n
    return [(nomer >> (dlina - 1 - k)) & 1 for k in range(dlina)]

# nomer_iz: номер из списка битов вектора
def nomer_iz(bity):
    return int("".join(map(str, bity)), 2)

# peremennaya: вектор i-й переменной из n (i = 0 — x, старший разряд строки)
def peremennaya(i, n):
    return nomer_iz([(k >> (n - 1 - i)) & 1 for k in range(2 ** n)])

# shirina: маска из 2^n единиц
def shirina(n):
    return 2 ** (2 ** n) - 1

# f_na_vektorah: функция f_номер, применённая поразрядно к векторам X и Y (ширина n переменных)
def f_na_vektorah(nomer, X, Y, n):
    m = shirina(n)
    nx, ny = ~X & m, ~Y & m
    termy = [(nx & ny, 3), (nx & Y, 2), (X & ny, 1), (X & Y, 0)]
    return sum(t for t, i in termy if (nomer >> i) & 1) & m


# --- полином Жегалкина ---

# treugolnik: треугольник Паскаля по модулю 2 — строки
def treugolnik(bity):
    stroki = [list(bity)]
    while len(stroki[-1]) > 1:
        r = stroki[-1]
        stroki.append([r[i] ^ r[i + 1] for i in range(len(r) - 1)])
    return stroki

# zheg_treug: коэффициенты Жегалкина — левая сторона треугольника
def zheg_treug(bity):
    return [s[0] for s in treugolnik(bity)]

# zheg_bystro: те же коэффициенты сдвигами — маски равны векторам переменных
def zheg_bystro(v, n):
    for i in range(n):
        v ^= (v >> (2 ** (n - 1 - i))) & peremennaya(i, n)
    return v

# odnochlen: одночлен по номеру строки k (какие переменные входят)
def odnochlen(k, n, imena="xyz"):
    vhod = [imena[i] for i in range(n) if (k >> (n - 1 - i)) & 1]
    return "".join(vhod) or "1"

# zheg_tekst: полином Жегалкина словами — 1, потом одночлены по длине и алфавиту
def zheg_tekst(koef, n):
    chleny = sorted((odnochlen(k, n) for k, c in enumerate(koef) if c), key=lambda m: (m != "1", len(m), m))
    return " ⊕ ".join(chleny) or "0"


# --- СДНФ и СКНФ ---

# literal: переменная или её отрицание по биту строки
def literal(imya, bit, dlya_dnf):
    return imya if bit == dlya_dnf else "¬" + imya

# sdnf: по вектору — дизъюнкция конъюнкций строк, где 1
def sdnf(bity, n, imena="xyz"):
    st = []
    for k, b in enumerate(bity):
        if b:
            st.append("(" + "∧".join(literal(imena[i], (k >> (n - 1 - i)) & 1, 1) for i in range(n)) + ")")
    return " ∨ ".join(st) or "0"

# sknf: по вектору — конъюнкция дизъюнкций строк, где 0
def sknf(bity, n, imena="xyz"):
    st = []
    for k, b in enumerate(bity):
        if not b:
            st.append("(" + "∨".join(literal(imena[i], (k >> (n - 1 - i)) & 1, 0) for i in range(n)) + ")")
    return " ∧ ".join(st) or "1"


# --- формулы: дерево (операция, аргументы) и две алгебры ---

class Bit:
    ne = staticmethod(lambda a: 1 - a); i = staticmethod(min); ili = staticmethod(max)
    impl = staticmethod(lambda a, b: max(1 - a, b)); ekv = staticmethod(lambda a, b: int(a == b))
    xor = staticmethod(lambda a, b: a ^ b); sheff = staticmethod(lambda a, b: 1 - min(a, b))
    pirs = staticmethod(lambda a, b: 1 - max(a, b)); DA, NET, ZNACH = 1, 0, (0, 1)

class Trit:
    ne = staticmethod(lambda a: -a); i = staticmethod(min); ili = staticmethod(max)
    impl = staticmethod(lambda a, b: max(-a, b)); ekv = staticmethod(lambda a, b: min(max(-a, b), max(-b, a)))
    xor = staticmethod(lambda a, b: -min(max(-a, b), max(-b, a))); sheff = staticmethod(lambda a, b: -min(a, b))
    pirs = staticmethod(lambda a, b: -max(a, b)); DA, NET, ZNACH = 1, -1, (-1, 0, 1)

ZNAK = {"ne": "¬", "i": "∧", "ili": "∨", "impl": "→", "ekv": "≡", "xor": "⊕", "sheff": "|", "pirs": "↓"}

# schitat: значение формулы-дерева в алгебре A при наборе nabor
def schitat(f, A, nabor):
    if f[0] == "var":
        otvet = nabor[f[1]]
    elif f[0] == "const":
        otvet = A.DA if f[1] else A.NET
    else:
        otvet = getattr(A, f[0])(*[schitat(g, A, nabor) for g in f[1:]])
    return otvet

# tekst: формула-дерево знаками
def tekst(f):
    if f[0] == "var":
        otvet = f[1]
    elif f[0] == "const":
        otvet = str(f[1])
    elif f[0] == "ne":
        otvet = "¬" + tekst(f[1])
    else:
        otvet = "(" + tekst(f[1]) + ZNAK[f[0]] + tekst(f[2]) + ")"
    return otvet

# vektor_formuly: вектор формулы на битах (переменные x, y[, z])
def vektor_formuly(f, n):
    imena = "xyz"[:n]
    return [schitat(f, Bit, {imena[i]: (k >> (n - 1 - i)) & 1 for i in range(n)}) for k in range(2 ** n)]


# --- базисы: кратчайшие формулы поиском ---

X, Y = ("var", "x"), ("var", "y")

# kratchajshie: для каждого из 16 векторов — кратчайшая формула в базисе (поиск по числу знаков)
def kratchajshie(unarnye, binarnye):
    po_razmeru = {0: [X, Y]}
    luchshee = {nomer_iz(vektor_formuly(f, 2)): f for f in po_razmeru[0]}
    razmer = 0
    while len(luchshee) < 16:
        razmer += 1
        po_razmeru[razmer] = novye(po_razmeru, razmer, unarnye, binarnye, luchshee)
    return luchshee

# novye: формулы данного размера с новыми векторами
def novye(po_razmeru, razmer, unarnye, binarnye, luchshee):
    kandidaty = [(u, a) for u in unarnye for a in po_razmeru[razmer - 1]]
    kandidaty += [(b, a, c) for b in binarnye for r in range(razmer)
                  for a in po_razmeru[r] for c in po_razmeru[razmer - 1 - r]]
    st = []
    for f in kandidaty:
        v = nomer_iz(vektor_formuly(f, 2))
        if v not in luchshee:
            luchshee[v] = f
            st.append(f)
    return st

# zheg_formula: полином Жегалкина функции номер как формула-дерево (∧, ⊕, 1)
def zheg_formula(nomer):
    koef = zheg_treug(vektor(nomer))
    chleny = [[("const", 1)], [Y], [X], [("i", X, Y)]]
    termy = [chleny[k][0] for k, c in enumerate(koef) if c]
    otvet = termy[0] if termy else ("const", 0)
    for t in termy[1:]:
        otvet = ("xor", otvet, t)
    return otvet


# --- законы: левая и правая часть — формулы-деревья ---

Z = ("var", "z")
K1, K0 = ("const", 1), ("const", 0)

# op: короткая запись узла формулы
def op(imya, *arg):
    return (imya,) + arg

ne, I, ILI, IMPL, EKV, XOR = (lambda a: op("ne", a)), (lambda a, b: op("i", a, b)), (lambda a, b: op("ili", a, b)), \
    (lambda a, b: op("impl", a, b)), (lambda a, b: op("ekv", a, b)), (lambda a, b: op("xor", a, b))
SH, PI = (lambda a, b: op("sheff", a, b)), (lambda a, b: op("pirs", a, b))

ZAKONY = [
    ("И, ИЛИ, НЕ", "переместительный для И", I(X, Y), I(Y, X)),
    ("И, ИЛИ, НЕ", "переместительный для ИЛИ", ILI(X, Y), ILI(Y, X)),
    ("И, ИЛИ, НЕ", "сочетательный для И", I(I(X, Y), Z), I(X, I(Y, Z))),
    ("И, ИЛИ, НЕ", "сочетательный для ИЛИ", ILI(ILI(X, Y), Z), ILI(X, ILI(Y, Z))),
    ("И, ИЛИ, НЕ", "распределительный И относительно ИЛИ", I(X, ILI(Y, Z)), ILI(I(X, Y), I(X, Z))),
    ("И, ИЛИ, НЕ", "распределительный ИЛИ относительно И", ILI(X, I(Y, Z)), I(ILI(X, Y), ILI(X, Z))),
    ("И, ИЛИ, НЕ", "идемпотентность И", I(X, X), X),
    ("И, ИЛИ, НЕ", "идемпотентность ИЛИ", ILI(X, X), X),
    ("И, ИЛИ, НЕ", "двойное отрицание", ne(ne(X)), X),
    ("И, ИЛИ, НЕ", "де Моргана для И", ne(I(X, Y)), ILI(ne(X), ne(Y))),
    ("И, ИЛИ, НЕ", "де Моргана для ИЛИ", ne(ILI(X, Y)), I(ne(X), ne(Y))),
    ("И, ИЛИ, НЕ", "поглощение (И)", I(X, ILI(X, Y)), X),
    ("И, ИЛИ, НЕ", "поглощение (ИЛИ)", ILI(X, I(X, Y)), X),
    ("И, ИЛИ, НЕ", "склеивание (ИЛИ)", ILI(I(X, Y), I(X, ne(Y))), X),
    ("И, ИЛИ, НЕ", "склеивание (И)", I(ILI(X, Y), ILI(X, ne(Y))), X),
    ("И, ИЛИ, НЕ", "исключённого третьего", ILI(X, ne(X)), K1),
    ("И, ИЛИ, НЕ", "противоречия", I(X, ne(X)), K0),
    ("И, ИЛИ, НЕ", "И с единицей", I(X, K1), X),
    ("И, ИЛИ, НЕ", "И с нулём", I(X, K0), K0),
    ("И, ИЛИ, НЕ", "ИЛИ с нулём", ILI(X, K0), X),
    ("И, ИЛИ, НЕ", "ИЛИ с единицей", ILI(X, K1), K1),
    ("И, ИЛИ, НЕ", "Блейка — Порецкого (ИЛИ)", ILI(X, I(ne(X), Y)), ILI(X, Y)),
    ("И, ИЛИ, НЕ", "Блейка — Порецкого (И)", I(X, ILI(ne(X), Y)), I(X, Y)),
    ("импликация", "импликация через ИЛИ", IMPL(X, Y), ILI(ne(X), Y)),
    ("импликация", "контрапозиция", IMPL(X, Y), IMPL(ne(Y), ne(X))),
    ("импликация", "отрицание импликации", ne(IMPL(X, Y)), I(X, ne(Y))),
    ("импликация", "импликация из единицы", IMPL(K1, X), X),
    ("импликация", "импликация из нуля", IMPL(K0, X), K1),
    ("импликация", "x → x", IMPL(X, X), K1),
    ("импликация", "экспортация", IMPL(I(X, Y), Z), IMPL(X, IMPL(Y, Z))),
    ("импликация", "модус поненс как формула", IMPL(I(X, IMPL(X, Y)), Y), K1),
    ("импликация", "эквивалентность через импликации", EKV(X, Y), I(IMPL(X, Y), IMPL(Y, X))),
    ("импликация", "эквивалентность через И, ИЛИ, НЕ", EKV(X, Y), ILI(I(X, Y), I(ne(X), ne(Y)))),
    ("Шеффер, Пирс", "Шеффер — это И-НЕ", SH(X, Y), ne(I(X, Y))),
    ("Шеффер, Пирс", "НЕ через Шеффера", SH(X, X), ne(X)),
    ("Шеффер, Пирс", "Пирс — это ИЛИ-НЕ", PI(X, Y), ne(ILI(X, Y))),
    ("Шеффер, Пирс", "НЕ через Пирса", PI(X, X), ne(X)),
    ("Жегалкин", "исключающее ИЛИ через И, ИЛИ, НЕ", XOR(X, Y), ILI(I(X, ne(Y)), I(ne(X), Y))),
    ("Жегалкин", "исключающее ИЛИ — не эквивалентность", XOR(X, Y), ne(EKV(X, Y))),
    ("Жегалкин", "x ⊕ x = 0", XOR(X, X), K0),
    ("Жегалкин", "x ⊕ 0 = x", XOR(X, K0), X),
    ("Жегалкин", "x ⊕ 1 = ¬x", XOR(X, K1), ne(X)),
    ("Жегалкин", "ИЛИ через Жегалкина", ILI(X, Y), XOR(XOR(X, Y), I(X, Y))),
    ("Жегалкин", "распределительный И относительно ⊕", I(X, XOR(Y, Z)), XOR(I(X, Y), I(X, Z))),
]


# nabory: все наборы значений для x, y, z в алгебре A
def nabory(A):
    return [{"x": a, "y": b, "z": c} for a in A.ZNACH for b in A.ZNACH for c in A.ZNACH]

# kontrprimer: первый набор, где части закона расходятся (или None)
def kontrprimer(levaya, pravaya, A):
    rashod = [(n, schitat(levaya, A, n), schitat(pravaya, A, n)) for n in nabory(A)
              if schitat(levaya, A, n) != schitat(pravaya, A, n)]
    return rashod[0] if rashod else None

# nikogda_ne_lozh: для законов «… = 1»: на тритах левая часть никогда не −1
def nikogda_ne_lozh(levaya, pravaya):
    return pravaya == K1 and all(schitat(levaya, Trit, n) != -1 for n in nabory(Trit))

# nikogda: для законов «… = const» на тритах — левая часть ни разу не даёт противоположного значения
def nikogda(levaya, pravaya):
    protiv = {K1: -1, K0: 1}.get(pravaya)
    return protiv is not None and all(schitat(levaya, Trit, n) != protiv for n in nabory(Trit))

# gruppa_neudachi: почему закон не переходит на триты
def gruppa_neudachi(gruppa, levaya, pravaya):
    if gruppa == "Жегалкин":
        otvet = "держится на 1 ⊕ 1 = 0 (счёт по модулю 2); у тритов свой «Жегалкин» — по модулю 3"
    elif nikogda(levaya, pravaya):
        otvet = "держится на «третьего не дано»; на тритах становится «никогда не " + ("ложь" if pravaya == K1 else "истина") + "»"
    else:
        otvet = "держится на «третьего не дано»: при 0 и x, и ¬x — «не знаю»"
    return otvet


# --- вывод: таблицы Markdown ---

# znachenie_tekst: трит словами для контрпримера
def znachenie_tekst(t):
    return {1: "1", 0: "0", -1: "−1"}[t]

# md_tablica16: таблица 16 функций со всеми записями
def md_tablica16(baz):
    st = ["| № | Вектор | Двоичный номер | Название | Обозначения | Арифметика | Сравнение | Жегалкин | И, ИЛИ, НЕ | Шеффер | Пирс |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for n in range(16):
        v = "".join(map(str, vektor(n)))
        stroka = (f"| f{n} | {v} | {n} = {v}₂ | {IMENA[n]} | {OBOZ[n]} | {ARIF[n]} | {SRAVN[n]} | "
                  f"{zheg_tekst(zheg_treug(vektor(n)), 2)} | {tekst(baz['ion'][n])} | {tekst(baz['sh'][n])} | {tekst(baz['pi'][n])} |")
        st.append(ekran(stroka))
    return st

# ekran: знак Шеффера внутри ячеек таблицы Markdown — с обратной косой
def ekran(stroka):
    yachejki = stroka[2:-2].split(" | ")
    return "| " + " | ".join(y.replace("|", "\\|") for y in yachejki) + " |"

# md_peremennye: векторы переменных и «номера складываются»
def md_peremennye():
    st = ["| Переменных | x | y | z | x И y | x ИЛИ y | x ⊕ y |", "|---|---|---|---|---|---|---|"]
    for n in (2, 3):
        x, y = peremennaya(0, n), peremennaya(1, n)
        z = f"{peremennaya(2, n):08b} ({peremennaya(2, n)})" if n == 3 else "—"
        w = 2 ** n
        st.append(f"| {n} | {x:0{w}b} ({x}) | {y:0{w}b} ({y}) | {z} | {x & y:0{w}b} ({x & y}) | "
                  f"{x | y:0{w}b} ({x | y}) | {x ^ y:0{w}b} ({x ^ y}) |")
    return st

# md_zakony: законы — на битах и на тритах
def md_zakony():
    st = ["| Группа | Закон | Формула | Биты | Триты | Контрпример на тритах | Почему |", "|---|---|---|---|---|---|---|"]
    for gr, imya, l, r in ZAKONY:
        k = kontrprimer(l, r, Trit)
        if k is None:
            trit, kp, pochemu = "работает", "—", "—"
        else:
            nab = ", ".join(f"{v}={znachenie_tekst(k[0][v])}" for v in "xyz" if v in tekst(l) + tekst(r))
            trit, kp, pochemu = "нет", f"{nab}: {znachenie_tekst(k[1])} ≠ {znachenie_tekst(k[2])}", gruppa_neudachi(gr, l, r)
        st.append(ekran(f"| {gr} | {imya} | {tekst(l)} = {tekst(r)} | верен | {trit} | {kp} | {pochemu} |"))
    return st

# md_primer3: пример для трёх переменных — большинство
def md_primer3():
    bity = [1 if (k >> 2) + ((k >> 1) & 1) + (k & 1) >= 2 else 0 for k in range(8)]
    v = "".join(map(str, bity))
    return [f"Функция «большинство» трёх переменных: вектор {v} = {nomer_iz(bity)}.", "",
            f"- СДНФ: {sdnf(bity, 3)}", f"- СКНФ: {sknf(bity, 3)}",
            f"- Жегалкин: {zheg_tekst(zheg_treug(bity), 3)}"]


# --- запись для Форта и Пролога ---

FORT = {"ne": "НЕ", "i": "И", "ili": "ИЛИ", "impl": "ИМПЛ", "ekv": "ЭКВ", "xor": "ИСКЛ", "sheff": "ШЕФФЕР", "pirs": "ПИРС"}
PROLOG = {"ne": "не", "i": "и", "ili": "или", "impl": "импл", "ekv": "экв", "xor": "искл", "sheff": "шеффер", "pirs": "пирс"}

# fort: формула-дерево обратной польской записью для Форта (векторы трёх переменных)
def fort(f):
    if f[0] == "var":
        otvet = f[1].upper()
    elif f[0] == "const":
        otvet = "ВСЕ" if f[1] else "0"
    else:
        otvet = " ".join(fort(g) for g in f[1:]) + " " + FORT[f[0]]
    return otvet

# prolog: формула-дерево термом Пролога
def prolog(f):
    if f[0] in ("var", "const"):
        otvet = str(f[1])
    else:
        otvet = PROLOG[f[0]] + "(" + ", ".join(prolog(g) for g in f[1:]) + ")"
    return otvet


# --- сборка и проверки ---

# bazisy: кратчайшие формулы в трёх базисах и полином Жегалкина
def bazisy():
    baz = {"ion": kratchajshie(["ne"], ["i", "ili"]), "sh": kratchajshie([], ["sheff"]),
           "pi": kratchajshie([], ["pirs"]), "zh": {n: zheg_formula(n) for n in range(16)}}
    for imya, slovar in baz.items():
        assert all(nomer_iz(vektor_formuly(slovar[n], 2)) == n for n in range(16)), imya
    return baz

# proverit_vse: всё, что должно сойтись
def proverit_vse():
    assert all(zheg_treug(vektor(n)) == vektor(zheg_bystro(n, 2)) for n in range(16))
    assert all(zheg_treug(vektor(n, 3)) == vektor(zheg_bystro(n, 3), 3) for n in range(256))
    assert all(zheg_bystro(zheg_bystro(n, 3), 3) == n for n in range(256))          # туда и обратно — то же действие
    assert all(f_na_vektorah(n, 3, 5, 2) == n for n in range(16))                    # f(x, y) на векторах = свой номер
    assert all(f_na_vektorah(n, 15, 51, 3) == nomer_iz([vektor(n)[2 * (k >> 2) + ((k >> 1) & 1)] for k in range(8)])
               for n in range(16))                                                     # z — фиктивная
    assert all(kontrprimer(l, r, Bit) is None for _, _, l, r in ZAKONY)
    return True

# primery_fort: строки Форта и ожидаемый вывод
def primery_fort():
    st = [[f"3 5 {n} f2 .", str(n)] for n in range(16)]
    st += [[f"15 51 {n} f3 .", str(f_na_vektorah(n, 15, 51, 3))] for n in range(16)]
    st += [[f"{n} жегалкин2 .", str(zheg_bystro(n, 2))] for n in range(16)]
    st += [[f"{n} жегалкин3 .", str(zheg_bystro(n, 3))] for n in range(256)]
    st += [[f"закон-{i + 1} .", "-1"] for i in range(len(ZAKONY))]
    return st

# primery_prolog: запросы Пролога и ожидаемый ответ
def primery_prolog(baz):
    st = [[f"вектор2({prolog(baz[b][n])}, V), V == {vektor(n)}", True] for b in ("ion", "sh", "pi", "zh") for n in range(16)]
    st += [[f"функция_формулы({prolog(baz['ion'][n])}, N), N == {n}", True] for n in range(16)]
    st += [[f"закон_верен({i + 1})", True] for i in range(len(ZAKONY))]
    st += [[f"сднф_скнф_обратно({vektor(n)})", True] for n in range(16)]
    st += [[f"жегалкин({vektor(n)}, К), К == {zheg_treug(vektor(n))}", True] for n in range(16)]
    st += [[f"жегалкин({vektor(n, 3)}, К), К == {zheg_treug(vektor(n, 3))}", True] for n in range(0, 256, 17)]
    st += [["упростить(и(импл(x, y), импл(y, x)), Имя), Имя == 'эквивалентность'", True],
           ["упростить(или(x, не(x)), Имя), Имя == 'константа 1'", True]]
    return st

# pisat: все файлы вывода
def pisat(baz):
    zak = [f": закон-{i + 1} ( -- f )  {fort(l)}  {fort(r)} = ;   \\ {imya}" for i, (_, imya, l, r) in enumerate(ZAKONY)]
    (ZDES / "dvoich-zakony.fs").write_text("\\ Законы на векторах трёх переменных — собрано из dvoich.py\n" + "\n".join(zak) + "\n", encoding="utf-8")
    nazv = {"ion": "и_или_не", "sh": "шефферов", "pi": "пирсов", "zh": "жегалкин"}
    fakty = [f"имя_функции({n}, '{IMENA[n]}')." for n in range(16)]
    fakty += [f"базис({n}, {nazv[b]}, {prolog(baz[b][n])})." for b in ("ion", "sh", "pi", "zh") for n in range(16)]
    fakty += [f"закон({i + 1}, '{imya}', {prolog(l)}, {prolog(r)})." for i, (_, imya, l, r) in enumerate(ZAKONY)]
    (ZDES / "dvoich-dannye.pl").write_text("% Базисы и законы — собрано из dvoich.py\n" + "\n".join(fakty) + "\n", encoding="utf-8")
    dannye = {"fort": primery_fort(), "prolog": primery_prolog(baz)}
    (ZDES / "primery-dvoich.json").write_text(json.dumps(dannye, ensure_ascii=False, indent=0), encoding="utf-8")
    return len(dannye["fort"]) + len(dannye["prolog"])

# tekst_md: справочник двоичной логики
def tekst_md(baz):
    st = ["# Двоичная логика — справочник (собран программой dvoich.py, 19.11.2026)", "",
          "Вектор — значения f(0,0) f(0,1) f(1,0) f(1,1); номер — вектор как двоичное число. Все формулы проверены перебором;",
          "формулы в базисах — кратчайшие, найдены поиском.", "", "## 16 функций двух переменных", ""]
    st += md_tablica16(baz) + ["", "## Векторы переменных: номера складываются поразрядно", ""] + md_peremennye()
    st += ["", "## Пример: три переменные", ""] + md_primer3()
    st += ["", "## Законы: на битах и на тритах", "", "На тритах: «не» = −x, «и» = min, «или» = max, импликация K3 = max(−x, y), 1 → 1, 0 → −1 (Р30).", ""]
    return st + md_zakony()

if __name__ == "__main__":
    baz = bazisy()
    proverit_vse()
    (ZDES / "dvoichnaya.md").write_text("\n".join(tekst_md(baz)) + "\n", encoding="utf-8")
    print("примеров для Форта и Пролога:", pisat(baz), "; законов:", len(ZAKONY), "; всё сошлось")
