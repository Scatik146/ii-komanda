# proverka_P2.py — проверка приложения части 2 «Для любопытных: как считает „Сетунь“»
# запуск: python3 proverka_P2.py
# Цифры троичной симметричной записи: 1, 0, −1 (в тексте: +, 0, −). Разряды справа налево: 1, 3, 9, 27, …
# Проверяет каждое число и каждое правило, которое стоит в приложении, на всех числах от −400 до 400.
import sys

ZNAKI = {1: '+', 0: '0', -1: '−'}
OBRATNO = {'+': 1, '0': 0, '−': -1}
DIAPAZON = range(-400, 401)


# cifry: число → цифры от старшей к младшей (каждая −1, 0 или 1)
def cifry(n):
    otvet = []
    while n != 0:
        ostatok = ((n + 1) % 3) - 1
        otvet.insert(0, ostatok)
        n = (n - ostatok) // 3
    return otvet or [0]


# zapis: число → строка из +, 0, −
def zapis(n):
    otvet = ''.join(ZNAKI[c] for c in cifry(n))
    return otvet


# chislo: строка из +, 0, − → число
def chislo(s):
    otvet = 0
    for znak in s:
        otvet = otvet * 3 + OBRATNO[znak]
    return otvet


# perevernut: каждую цифру — на противоположную (+ ↔ −, 0 остаётся)
def perevernut(s):
    otvet = ''.join(ZNAKI[-OBRATNO[z]] for z in s)
    return otvet


# otbrosit: отбросить k младших цифр и вернуть то, что осталось, в прежнем масштабе
def otbrosit(n, k):
    s = zapis(n)
    otvet = chislo(s[:-k]) * 3 ** k if len(s) > k else 0
    return otvet


# blizhajshee: ближайшее к n число, кратное 3^k
def blizhajshee(n, k):
    shag = 3 ** k
    otvet = min((m for m in range(n - shag, n + shag + 1) if m % shag == 0), key=lambda m: abs(m - n))
    return otvet


# slozhit_cifry: сумма двух цифр и переноса → (цифра, перенос)
def slozhit_cifry(a, b, p):
    s = a + b + p
    otvet = (s - 3, 1) if s > 1 else ((s + 3, -1) if s < -1 else (s, 0))
    return otvet


# slozhit: сложение столбиком по цифрам (как в приложении), без перевода в десятичное
def slozhit(x, y):
    a, b = cifry(x)[::-1], cifry(y)[::-1]
    dlina, p, otvet = max(len(a), len(b)), 0, []
    for i in range(dlina):
        c, p = slozhit_cifry(a[i] if i < len(a) else 0, b[i] if i < len(b) else 0, p)
        otvet.append(c)
    otvet = chislo(''.join(ZNAKI[c] for c in ([p] if p else []) + otvet[::-1]))
    return otvet


# znak: знак числа — первая не нулевая цифра записи
def znak(s):
    nenul = [z for z in s if z != '0']
    otvet = OBRATNO[nenul[0]] if nenul else 0
    return otvet


# proverki_chisel: числа и таблица из текста приложения
def proverki_chisel():
    otvet = [
        ('+−− = 5, −++ = −5, +00 = 9, ++ = 4, +−−− = 14', [zapis(5), zapis(-5), zapis(9), zapis(4), zapis(14)] == ['+−−', '−++', '+00', '++', '+−−−']),
        ('таблица −4…4 в приложении', [zapis(n) for n in range(-4, 5)] == ['−−', '−0', '−+', '−', '0', '+', '+−', '+0', '++']),
        ('запись и обратно — то же число', all(chislo(zapis(n)) == n for n in DIAPAZON)),
        ('5 + 4 = 9: +−− и ++ дают +00', zapis(slozhit(5, 4)) == '+00'),
        ('4 + 4 = 8: ++ и ++ дают +0−', zapis(slozhit(4, 4)) == '+0−'),
        ('14: без одной цифры 15, без двух 18', (otbrosit(14, 1), otbrosit(14, 2)) == (15, 18)),
    ]
    return otvet


# sravnenie_po_cifram: сравнение записей одной длины слева направо при порядке − < 0 < +
def sravnenie_po_cifram(a, b):
    klyuch = str.maketrans('−0+', 'abc')
    otvet = zapis(a).rjust(7, '0').translate(klyuch) < zapis(b).rjust(7, '0').translate(klyuch)
    return otvet


# proverki_pravil: правила приложения на всех числах диапазона
def proverki_pravil():
    sravnit = lambda a, b: (a > b) - (a < b)
    otvet = [
        ('смена знака = переворот всех цифр', all(zapis(-n) == perevernut(zapis(n)) for n in DIAPAZON)),
        ('знак числа = старшая цифра (отдельного разряда знака нет)', all(znak(zapis(n)) == sravnit(n, 0) for n in DIAPAZON)),
        ('сложение по цифрам с переносом', all(slozhit(x, y) == x + y for x in range(-60, 61) for y in range(-60, 61))),
        ('+ и + = 2: пишем −, переносим +', slozhit_cifry(1, 1, 0) == (-1, 1)),
        ('отбросить младшие цифры = ближайшее кратное (k = 1, 2, 3)',
         all(otbrosit(n, k) == blizhajshee(n, k) for n in DIAPAZON for k in (1, 2, 3))),
        ('сравнение записей одной длины — по цифрам слева, − < 0 < +',
         all(sravnenie_po_cifram(a, b) == (a < b) for a in range(-100, 101) for b in range(-100, 101))),
    ]
    return otvet


# glavnoe: напечатать итог; хоть одна ошибка — код выхода 1
def glavnoe():
    rezultat = proverki_chisel() + proverki_pravil()
    for imya, da in rezultat:
        print(('да  ' if da else 'НЕТ ') + imya)
    oshibok = sum(1 for _, da in rezultat if not da)
    print(f"П.1 части 2: проверок {len(rezultat)}, ошибок {oshibok}")
    sys.exit(1 if oshibok else 0)


glavnoe()
