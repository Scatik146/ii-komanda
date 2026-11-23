"""algoritmy.py — действия над десятичными целыми на калькуляторе со встроенной логикой: сколько раз работает сумматор и умножитель.

Счёт «по словам»: сложение (вычитание) слова — 1 «сл», умножение — 1 «умн», сдвиг на постоянное число разрядов,
установка цифры частного или корня, отрицание у тритов — провода и строка НЕ (почти даром, глубина 1).
Каждый алгоритм выполняется на числах и сверяется с Python. Время = сл · T_сл + умн · T_умн (из izmerit.py).
"""
import math
import sys
sys.path.insert(0, '../arifmometr')
from model import stepen_2, stepen_3


# Schet: счётчик сложений и умножений
class Schet:
    # __init__: нули
    def __init__(self):
        self.sl, self.umn = 0, 0

    # slozhit: x + y (вычитание — то же)
    def slozhit(self, x, y):
        self.sl += 1
        return x + y

    # umnozhit: x · y
    def umnozhit(self, x, y):
        self.umn += 1
        return x * y


# okrugl_troich: отбросить k тритов симметричного числа — это и есть округление до ближайшего (даром)
def okrugl_troich(x, k):
    st = 3 ** k
    return (x + (st - 1) // 2) // st


# sdvig_vpravo: двоичный — отбросить k бит (вниз); троичный — отбросить k тритов (к ближайшему)
def sdvig_vpravo(baza, x, k):
    return x >> k if baza == 2 else okrugl_troich(x, k)


# --- деление на 10 умножением на обратное ----------------------------------------------------

# У тритов c = 0 (сдвиг сам округляет) или −(3^k − 1)/2 (тогда сдвиг даёт «вниз», как у битов).
# tochno: сдвиг(x·M + c, k) даёт нужное для всех x (сначала — на каждом 97-м, потом — на всех)
def tochno(baza, M, k, c, nado):
    vse = lambda shag: all(sdvig_vpravo(baza, x * M + c, k) == q for x, q in list(enumerate(nado))[::shag])
    return vse(97) and vse(1)


# podobrat_obratnoe: (M, k, c): cel(x) = сдвиг(x·M + c, k) для всех 0 ≤ x ≤ X; наименьшее k
def podobrat_obratnoe(baza, X, delitel, cel=None):
    cel = cel or (lambda x: x // delitel)
    nado, najdeno, k = [cel(x) for x in range(X + 1)], None, 1
    while najdeno is None:
        M = -(-baza ** k // delitel)
        varianty = (0,) if baza == 2 else (0, -(3 ** k - 1) // 2)
        najdeno = next(((M, k, c) for c in varianty if tochno(baza, M, k, c, nado)), None)
        k += 1
    return najdeno


# na_desyat: (частное, остаток) от деления на 10: умножение, (у тритов — прибавить c), 10q и вычитание
def na_desyat(baza, sch, x, obr):
    M, k, c = obr
    p = sch.umnozhit(x, M)
    p = sch.slozhit(p, c) if c else p
    q = sdvig_vpravo(baza, p, k)
    desyat_q = sch.slozhit(q * 8, q * 2) if baza == 2 else sch.slozhit(q * 9, q)
    return (q, sch.slozhit(x, -desyat_q))


# --- ввод и вывод десятичных ------------------------------------------------------------------

# vvod: строка цифр → число: acc·10 + цифра (три слагаемых: 8acc + 2acc + d или 9acc + acc + d → два сложения)
def vvod(baza, sch, tekst):
    znak, acc = (-1 if tekst[0] == '-' else 1), 0
    for c in tekst.lstrip('-'):
        a, b = (acc * 8, acc * 2) if baza == 2 else (acc * 9, acc)
        acc = sch.slozhit(sch.slozhit(a, b), int(c))
    acc = (sch.slozhit(0, -acc) if baza == 2 else -acc) if znak < 0 else acc
    return acc


# vyvod: число → строка цифр: модуль (двоичному — сложение), потом цифры делением на 10 обратным
def vyvod(baza, sch, x, obr):
    minus = x < 0
    x = (sch.slozhit(0, -x) if baza == 2 else -x) if minus else x
    cifry = []
    while True:
        x, r = na_desyat(baza, sch, x, obr)
        cifry.append(str(r))
        if x == 0:
            break
    return ('-' if minus else '') + ''.join(reversed(cifry))


# --- деление с остатком (школьный остаток 0…d−1, n ≥ 0, d > 0) ---------------------------------------

# delenie_2: двоичное без восстановления: n шагов по одному сложению, в конце поправка
def delenie_2(sch, n, d, shagi):
    r, q = n, 0
    for i in range(shagi - 1, -1, -1):
        r = sch.slozhit(r, -(d << i)) if r >= 0 else sch.slozhit(r, d << i)
        q = q * 2 + (1 if r >= 0 else 0)
    r = sch.slozhit(r, d) if r < 0 else r
    return (q, r)


# delenie_3: троичное симметричное: шаг — 2r, сравнить с s, прибавить или вычесть s (или пропустить)
def delenie_3(sch, n, d, shagi):
    r, q = n, 0
    for i in range(shagi - 1, -1, -1):
        s, q = d * 3 ** i, q * 3
        proba = sch.slozhit(sch.slozhit(r, r), -s if r > 0 else s)
        if r > 0 and proba > 0:
            r, q = sch.slozhit(r, -s), q + 1
        elif r < 0 and proba < 0:
            r, q = sch.slozhit(r, s), q - 1
    if r < 0:
        r, q = sch.slozhit(r, d), sch.slozhit(q, -1)
    return (q, r)


# --- корень (целая часть) ---------------------------------------------------------------------

# koren_2: двоичный «цифра за цифрой»: на шаг одно вычитание (res + bit — разные биты, это провода)
def koren_2(sch, x, bity):
    res, bit = 0, 4 ** ((bity - 1) // 2)
    while bit:
        proba = sch.slozhit(x, -(res + bit))
        x, res = (proba, (res >> 1) + bit) if proba >= 0 else (x, res >> 1)
        bit >>= 2
    return res


# shag_kornya_3: цифра 0, 1, 2 корня в разряде i; rem = x − R², A = 2·R·3^i (R — старшие цифры); потом A для i − 1
def shag_kornya_3(sch, rem, A, i):
    t1 = sch.slozhit(A, 9 ** i)
    p1 = sch.slozhit(rem, -t1)
    p2 = sch.slozhit(p1, -sch.slozhit(A, 3 * 9 ** i)) if p1 >= 0 else -1
    d = 2 if p2 >= 0 else (1 if p1 >= 0 else 0)
    rem = p2 if d == 2 else (p1 if d == 1 else rem)
    A = sch.slozhit(A, 2 * d * 9 ** i) // 3 if i > 0 and d else A // 3
    return (rem, A, d)


# koren_3: троичный «цифра за цифрой» (школьные цифры 0, 1, 2), разряды сверху
def koren_3(sch, x, trity):
    rem, A, koren = x, 0, 0
    for i in range((trity - 1) // 2, -1, -1):
        rem, A, d = shag_kornya_3(sch, rem, A, i)
        koren += d * 3 ** i
    return koren


# --- округление ---------------------------------------------------------------------------------

# okrugl_stepen: до ближайшего кратного основание^k: двоичный — прибавить половину и отбросить; троичный — отбросить
def okrugl_stepen(baza, sch, x, k):
    return (sch.slozhit(x, 1 << (k - 1)) >> k) if baza == 2 else okrugl_troich(x, k)


# okrugl_10: до ближайшего кратного 10^k (x ≥ 0): двоичный — +половина, ×обратное; троичный — сразу ×обратное
def okrugl_10(baza, sch, x, k, obr):
    M, sd, c = obr
    x = sch.slozhit(x, 10 ** k // 2) if baza == 2 else x
    p = sch.umnozhit(x, M)
    p = sch.slozhit(p, c) if c else p
    return sch.umnozhit(sdvig_vpravo(baza, p, sd), 10 ** k)


# stepen: x^e: умножений «квадрат и умножить» (двоичный) или «куб и умножить» (троичный), из model.py
def stepen(baza, e):
    return stepen_2(e) if baza == 2 else stepen_3(e)
