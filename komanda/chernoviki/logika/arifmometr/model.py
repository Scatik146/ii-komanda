"""model.py — арифмометр без логики: двоичный (32 бита) и троичный симметричный (21 трит) — счёт операций.

Единица — одна операция над словом: сложить, вычесть, сдвинуть на один разряд (влево или вправо).
Флаги знака и нуля после операции и выпавшая при сдвиге вправо цифра — даром (у «Сетуни» знак результата ω —
в таблице команд у каждой операции). Логики нет: ни И, ни ИЛИ над словами, только эти три действия.
Разряды: 32 бита — int32 (±2,1·10⁹); 21 трит симметрично — ±5,2·10⁹, это наименьшее число тритов, покрывающее int32.
Каждый алгоритм выполняется на настоящих числах; ответ сверяется с Python, счётчик — по операциям.
Запуск: python3 model.py
"""
import random

N_BIT, N_TRIT = 32, 21
VYBORKA = 20000
random.seed(23112026)


# Mashina: арифмометр с основанием 2 или 3 (симметричный); считает операции
class Mashina:
    # __init__: основание и пустой счётчик
    def __init__(self, osnovanie):
        self.b, self.ops = osnovanie, 0

    # slozhit: x + y
    def slozhit(self, x, y):
        self.ops += 1
        return x + y

    # vychest: x − y
    def vychest(self, x, y):
        self.ops += 1
        return x - y

    # vlevo: сдвиг на разряд влево (× основание)
    def vlevo(self, x):
        self.ops += 1
        return x * self.b

    # vpravo: сдвиг вправо → (частное, выпавшая цифра); у троичной цифра −1, 0, 1, у двоичной 0, 1
    def vpravo(self, x):
        self.ops += 1
        c = ((x + 1) % 3) - 1 if self.b == 3 else x % 2
        return ((x - c) // self.b, c)


# --- умножение ----------------------------------------------------------------

# Двоичному отрицательный множитель надо сперва сделать положительным, а ответ — обратно (две операции).
# umn_stolbik: «русский крестьянский» = столбик: младшая цифра множителя → прибавить (вычесть) множимое, сдвиги
def umn_stolbik(m, a, b):
    rez, minus = 0, m.b == 2 and b < 0
    b = m.vychest(0, b) if minus else b
    while b != 0:
        b, c = m.vpravo(b)
        rez = m.slozhit(rez, a) if c == 1 else (m.vychest(rez, a) if c == -1 else rez)
        a = m.vlevo(a) if b != 0 else a
    return m.vychest(0, rez) if minus else rez


# booth: двоичный множитель → цифры −1, 0, 1 (перекодировка Бута: на границах серий единиц)
def booth(b):
    cifry, pred = [], 0
    for i in range(N_BIT):
        bit = (b >> i) & 1
        cifry.append(pred - bit)
        pred = bit
    return cifry


# umn_booth: двоичный столбик по цифрам Бута: прибавить, вычесть или пропустить, сдвиг на каждом разряде
def umn_booth(m, a, b):
    rez, cifry = 0, booth(b % (1 << N_BIT))
    while cifry and cifry[-1] == 0:
        cifry.pop()
    m.ops += len(cifry)  # логики нет: чтобы увидеть пару бит, множитель сдвигают вправо — сдвиг на каждый разряд
    for i, c in enumerate(cifry):
        rez = m.slozhit(rez, a) if c == 1 else (m.vychest(rez, a) if c == -1 else rez)
        a = m.vlevo(a) if i < len(cifry) - 1 else a
    return rez


# --- деление: частное и остаток ----------------------------------------------------

# del_vosst: двоичное «с восстановлением»: вычел — если ушёл в минус, прибавил обратно (n ≥ 0, d > 0)
def del_vosst(m, n, d):
    k, s = 0, d
    while s <= n:
        s, k = m.vlevo(s), k + 1
    q, r = 0, n
    for _ in range(k + 1):
        q = m.vlevo(q)
        r = m.vychest(r, s)
        if r < 0:
            r = m.slozhit(r, s)
        else:
            q = m.slozhit(q, 1)
        s, _ = m.vpravo(s) if _ < k else (s, 0)
    return q, r


# del_bez_vosst: двоичное «без восстановления»: знак остатка решает, вычесть или прибавить на следующем шаге
def del_bez_vosst(m, n, d):
    k, s = 0, d
    while s <= n:
        s, k = m.vlevo(s), k + 1
    q, r = 0, n
    for shag in range(k + 1):
        q = m.vlevo(q)
        r = m.vychest(r, s) if r >= 0 else m.slozhit(r, s)
        q = m.slozhit(q, 1) if r >= 0 else q
        s = m.vpravo(s)[0] if shag < k else s
    if r < 0:
        r = m.slozhit(r, d)
    return q, r


# Сравнение «2r против s» — удвоением и одним вычитанием; частное ближайшее, |остаток| ≤ d/2.
# del_troich: троичное симметричное: на шаге — прибавить, вычесть или пропустить сдвинутый делитель
def del_troich(m, n, d):
    k, s = 0, d
    while s <= abs(n):
        s, k = m.vlevo(s), k + 1
    q, r = 0, n
    for shag in range(k + 1):
        q = m.vlevo(q)
        dva_r = m.slozhit(r, r)
        proba = m.vychest(dva_r, s) if r > 0 else m.slozhit(dva_r, s)
        if r > 0 and proba > 0:
            r, q = m.vychest(r, s), m.slozhit(q, 1)
        elif r < 0 and proba < 0:
            r, q = m.slozhit(r, s), m.vychest(q, 1)
        s = m.vpravo(s)[0] if shag < k else s
    return q, r


# v_shkolnyj: симметричный остаток → школьный (0 … d − 1): одна поправка
def v_shkolnyj(m, q, r, d):
    return (m.vychest(q, 1), m.slozhit(r, d)) if r < 0 else (q, r)


# --- степень ----------------------------------------------------------------------

# stepen_2: «квадрат и умножить» по двоичным цифрам показателя (слева направо): число умножений
def stepen_2(e):
    cifry = bin(e)[3:]
    return sum(2 if c == '1' else 1 for c in cifry)


# stepen_3: «куб и умножить» по обычным троичным цифрам 0, 1, 2 (x² готовим заранее, одно умножение)
def stepen_3(e):
    cifry, mul = [], 0
    while e:
        cifry.append(e % 3)
        e //= 3
    cifry.reverse()
    mul = 1 if 2 in cifry else 0
    mul += sum(2 + (1 if c else 0) for c in cifry[1:]) + (1 if cifry[0] == 2 else 0)
    return mul


# --- перевод из десятичной и обратно ----------------------------------------------------

# iz_desyatichnoj: по Горнеру: acc = acc·10 + цифра; ×10 — сдвигами и сложением
def iz_desyatichnoj(m, cifry):
    acc = 0
    for c in cifry:
        if m.b == 2:
            dva = m.vlevo(acc)
            vosem = m.vlevo(m.vlevo(dva))
            acc = m.slozhit(vosem, dva)
        else:
            devyat = m.vlevo(m.vlevo(acc))
            acc = m.slozhit(devyat, acc)
        acc = m.slozhit(acc, c) if c else acc
    return acc


# v_desyatichnuyu_delenie: делим на 10 с остатком, пока не ноль (деление — лучшим для машины способом)
def v_desyatichnuyu_delenie(m, n):
    cifry = []
    while n:
        q, r = del_bez_vosst(m, n, 10) if m.b == 2 else v_shkolnyj(m, *del_troich(m, n, 10), 10)
        cifry.append(r)
        n = q
    return cifry[::-1] or [0]


# cifra_vychitaniem: вычитаю p, пока не ушёл в минус, и одно восстановление → (цифра, остаток)
def cifra_vychitaniem(m, n, p):
    c, n = -1, m.vychest(n, p)
    while n >= 0:
        c, n = c + 1, m.vychest(n, p)
    return (c + 1, m.slozhit(n, p))


# v_desyatichnuyu_vychitanie: с верхнего разряда: цифра за цифрой вычитанием степеней 10
def v_desyatichnuyu_vychitanie(m, n, stepeni):
    cifry = []
    for p in stepeni:
        c, n = cifra_vychitaniem(m, n, p)
        cifry.append(c)
    return cifry[next((i for i, c in enumerate(cifry) if c), len(cifry) - 1):]


# --- прогон ---------------------------------------------------------------------------

# razryadnye_shagi: операции × длина слова — сколько раз работает одноразрядный узел (32 бита или 21 трит)
def razryadnye_shagi(osnovanie, ops):
    return round(ops * (N_BIT if osnovanie == 2 else N_TRIT))


# srednee: средний счёт операций алгоритма на выборке; ответ сверяется
def srednee(osnovanie, algoritm, pary, otvet):
    vsego = 0
    for x, y in pary:
        m = Mashina(osnovanie)
        rez = algoritm(m, x, y)
        assert rez == otvet(x, y), (algoritm.__name__, x, y, rez)
        vsego += m.ops
    return vsego / len(pary)


# progon_dejstvij: умножение и деление на выборках
def progon_dejstvij():
    pol16 = lambda: random.randint(-2**15, 2**15 - 1)
    umn = [(pol16(), pol16()) for _ in range(VYBORKA)]
    dele = [(random.randint(0, 2**31 - 1), random.randint(1, 2**15)) for _ in range(VYBORKA)]
    pro, shk = (lambda x, y: x * y), (lambda n, d: (n // d, n % d))
    tro = lambda m, n, d: v_shkolnyj(m, *del_troich(m, n, d), d)
    print('УМНОЖЕНИЕ (множители 16 бит со знаком, произведение влезает в int32)')
    print('  двоичный столбик = русский крестьянский:', round(srednee(2, umn_stolbik, umn, pro), 1))
    print('  двоичный по Буту (цифры −1, 0, 1):      ', round(srednee(2, umn_booth, umn, pro), 1))
    print('  троичный столбик = «крестьянский на 3»: ', round(srednee(3, umn_stolbik, umn, pro), 1))
    print('ДЕЛЕНИЕ (делимое int32 ≥ 0, делитель 1…2¹⁵), частное и остаток')
    print('  двоичное с восстановлением:   ', round(srednee(2, del_vosst, dele, shk), 1))
    print('  двоичное без восстановления:  ', round(srednee(2, del_bez_vosst, dele, shk), 1))
    print('  троичное (+ перевод в школьный остаток):', round(srednee(3, tro, dele, shk), 1))


# progon_perevoda: перевод из десятичной и обратно, оба основания
def progon_perevoda():
    chisla, st = [random.randint(0, 2**31 - 1) for _ in range(2000)], [10 ** k for k in range(9, -1, -1)]
    for b in (2, 3):
        m1, m2, m3 = Mashina(b), Mashina(b), Mashina(b)
        assert all(iz_desyatichnoj(m1, [int(c) for c in str(n)]) == n for n in chisla)
        assert all(int(''.join(map(str, v_desyatichnuyu_delenie(m2, n)))) == n for n in chisla)
        assert all(int(''.join(map(str, v_desyatichnuyu_vychitanie(m3, n, st)))) == n for n in chisla)
        k = len(chisla)
        print(f'ПЕРЕВОД, основание {b}: из десятичной {m1.ops / k:.1f}; в десятичную делением на 10 {m2.ops / k:.1f}, '
              f'вычитанием степеней 10 {m3.ops / k:.1f}')


# glavnoe: все таблицы
def glavnoe():
    progon_dejstvij()
    ee = [random.randint(1, 2**20) for _ in range(VYBORKA)]
    print('СТЕПЕНЬ x^e, e до 2²⁰: умножений в среднем')
    print('  двоичный «квадрат и умножить»:', round(sum(map(stepen_2, ee)) / len(ee), 2))
    print('  троичный «куб и умножить»:     ', round(sum(map(stepen_3, ee)) / len(ee), 2))
    progon_perevoda()


if __name__ == '__main__':
    glavnoe()
