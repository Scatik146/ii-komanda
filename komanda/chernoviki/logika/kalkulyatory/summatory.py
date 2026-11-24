"""summatory.py — как устроены сумматоры: двоичный и троичный, разряд и слово; проверка гипотезы учителя.

Гипотеза учителя 24.11 (вес 0, проверяем, а не доказываем): «двоичный сумматор будет выигрывать».
Ищем и пример, и контрпример: по каким мерам, при каких деталях и ширинах двоичный выигрывает, а где — нет.
Меры: транзисторы, время (глубина в задержках детали), провода (цифры слова), цена на бит диапазона.
Варианты деталей — как в itog.py: А — строго базис книги; Б — + ИЛИ; Г — Б + «сдвиг по кругу»;
В — готовые полусумматор и сумматор (цены из статей, вес 0). Двоичный в А, Б, Г — один и тот же, из вентилей.
Каждый сумматор проверяется на числах (izmerit.uzel_slozheniya: 3000 случайных пар).
Запуск: python3 summatory.py > rezultat-summatory.txt
"""
import math
import random
import itog
import luchshie
import izmerit
from shema import Shema, DVOICHNYJ, TROICHNYJ
from uzly import volna, bystryj, polusummator, summator, slozhit_karty
from izmerit import shirina, uzel_slozheniya, cena_uzla

VARIANTY = ('А', 'Б', 'Г', 'В')
BITY = (8, 16, 21, 32, 48)          # ширины двоичного слова; троичное — наименьшее, вмещающее тот же диапазон
VIDY = {'волна': volna, 'быстрый': bystryj}


# razryad: (транзисторы, глубина) полусумматора и полного сумматора одного разряда
def razryad(variant, b):
    itog.variant(variant)
    s = Shema(b)
    a, x, c = s.vhod(), s.vhod(), s.vhod()
    pol = cena_uzla(s, list(polusummator(s, a, x)))
    pln = cena_uzla(s, list(summator(s, a, x, c)))
    return ((pol['транзисторы'], pol['глубина']), (pln['транзисторы'], pln['глубина']))


# trity_dlya: сколько тритов вмещают диапазон n-битного слова (дополнительный код)
def trity_dlya(n):
    return shirina(TROICHNYJ, -2 ** (n - 1), 2 ** (n - 1) - 1)


# slovo: (транзисторы, глубина) сумматора слова; проверка на числах — внутри uzel_slozheniya
def slovo(variant, b, n, vid):
    itog.variant(variant)
    r = uzel_slozheniya(b, n, VIDY[vid])
    return (r['транзисторы'], r['глубина'])


# yachejka_karty: (транзисторы, глубина) одной склейки карт переноса: пара у битов, тройка у тритов
def yachejka_karty(variant, b):
    itog.variant(variant)
    s = Shema(b)
    dlina = 2 if b == DVOICHNYJ else 3
    g, f = [s.vhod() for _ in range(dlina)], [s.vhod() for _ in range(dlina)]
    r = cena_uzla(s, list(slozhit_karty(s, g, f)))
    return (r['транзисторы'], r['глубина'])


# karta_razryada: какой перенос уйдёт из разряда (x, y) при каждом входящем c — кортеж по c
def karta_razryada(b, x, y):
    vhody = (0, 1) if b == DVOICHNYJ else (-1, 0, 1)
    karta = []
    for c in vhody:
        summa = x + y + c
        cifra = summa % 2 if b == DVOICHNYJ else (summa + 1) % 3 - 1
        karta.append((summa - cifra) // b)
    return tuple(karta)


# karty_vsego: все карты переноса разрядов и их склеек (замыкание): сколько «слов» нужно разряду сказать
def karty_vsego(b):
    cifry = (0, 1) if b == DVOICHNYJ else (-1, 0, 1)
    sdvig = 0 if b == DVOICHNYJ else 1
    karty = {karta_razryada(b, x, y) for x in cifry for y in cifry}
    rastet = True
    while rastet:
        novye = {tuple(g[f[i] + sdvig] for i in range(len(f))) for g in karty for f in karty}
        rastet = not novye <= karty
        karty |= novye
    return sorted(karty)


# ekonomiya: «экономичность основания» b / ln b (цена цифры пропорциональна b — допущение Хейса)
def ekonomiya(b):
    return b / math.log(b)


# pechat_razryadov: таблица разрядов по вариантам
def pechat_razryadov():
    print('РАЗРЯД: полусумматор | полный сумматор (транзисторы / глубина)')
    for v in VARIANTY:
        for b, imya in ((DVOICHNYJ, 'двоичный'), (TROICHNYJ, 'троичный')):
            (p, pg), (f, fg) = razryad(v, b)
            print(f'  {v} {imya:9} {p:4} / {pg:2} | {f:4} / {fg:2}')
    print('СКЛЕЙКА КАРТ ПЕРЕНОСА (одна ячейка быстрого сумматора), вариант Б:',
          'двоичный', yachejka_karty('Б', DVOICHNYJ), '| троичный', yachejka_karty('Б', TROICHNYJ))
    return None


# stroka_slova: строка сравнения слова: двоичный n бит против троичного m тритов
def stroka_slova(v, n, vid):
    m = trity_dlya(n)
    d, t = slovo(v, DVOICHNYJ, n, vid), slovo(v, TROICHNYJ, m, vid)
    na_bit_d, na_bit_t = d[0] / n, t[0] / (m * math.log2(3))
    print(f'  {v} {vid:8} {n:2} бит / {m:2} трит: {d[0]:6} / {d[1]:3} | {t[0]:6} / {t[1]:3} | '
          f'цена ×{t[0] / d[0]:.2f}, время ×{t[1] / d[1]:.2f}, на бит диапазона {na_bit_d:.1f} | {na_bit_t:.1f}')
    return (d, t)


# sluchai: все сочетания (вариант, вид сумматора, ширина)
def sluchai():
    return [(v, vid, n) for v in VARIANTY for vid in VIDY for n in BITY]


# pechat_slov: таблица сумматоров слова; счёт случаев «троичный не хуже» по каждой мере
def pechat_slov():
    print('\nСЛОВО: двоичный | троичный (транзисторы / глубина), тот же диапазон чисел')
    pobedy = {'цена': 0, 'время': 0, 'провода': 0}
    spisok = sluchai()
    for v, vid, n in spisok:
        d, t = stroka_slova(v, n, vid)
        pobedy['цена'] += t[0] <= d[0]
        pobedy['время'] += t[1] <= d[1]
        pobedy['провода'] += trity_dlya(n) <= n
    print(f'  случаев {len(spisok)}; троичный не хуже: по цене {pobedy["цена"]}, по времени {pobedy["время"]}, '
          f'по проводам {pobedy["провода"]}')
    return pobedy


# okupaetsya: слово-ответ: окупается ли разряд при отношении цен r
def okupaetsya(r, porog):
    otvet = 'не окупается'
    if r <= porog:
        otvet = 'окупается'
    return otvet


# pechat_ekonomii: экономичность оснований, клетки таблиц и карты переноса
def pechat_ekonomii():
    for b in (2, 3, 4):
        print(f'  экономичность основания {b}: b/ln b = {ekonomiya(b):.4f}')
    print(f'  троичное «дешевле» двоичного по этой мере на {(1 - ekonomiya(3) / ekonomiya(2)) * 100:.1f} %')
    print(f'  клеток таблицы полного сумматора: двоичный 2³ = 8, троичный 3³ = 27, отношение {27 / 8:.3f}')
    for b, imya in ((DVOICHNYJ, 'двоичный'), (TROICHNYJ, 'троичный')):
        k = karty_vsego(b)
        print(f'  карт переноса ({imya}): {len(k)} — {k}')
    return None


# pechat_poroga: порог окупаемости разряда и сравнение вариантов с ним
def pechat_poroga():
    porog = math.log2(3)
    print(f'\nПОРОГ: трит несёт log2(3) = {porog:.4f} бита; троичный разряд окупается, если дороже двоичного '
          f'не больше чем в {porog:.3f} раза; от готового двоичного 28 тр. это {28 * porog:.1f} тр.')
    pechat_ekonomii()
    for v in VARIANTY:
        d, t = razryad(v, DVOICHNYJ)[1][0], razryad(v, TROICHNYJ)[1][0]
        print(f'  вариант {v}: разряд троичный / двоичный = {t / d:.2f} (порог {porog:.3f}) — {okupaetsya(t / d, porog)}')
    return porog


# chto_esli: волна 21 бит / 14 тритов на готовых сумматорах, если троичный полный сумматор стоит sm транзисторов
def chto_esli():
    print('\nЧТО ЕСЛИ (вариант В, волна 21 бит / 14 тритов): цена троичного полного сумматора → слово')
    bylo = izmerit.TRANZISTORY[TROICHNYJ]['СМ+']
    d = slovo('В', DVOICHNYJ, 21, 'волна')
    for sm in (72, 55, 44, 40):
        izmerit.TRANZISTORY[TROICHNYJ]['СМ+'] = sm
        t = slovo('В', TROICHNYJ, 14, 'волна')
        print(f'  {sm} тр.: двоичный {d[0]} / {d[1]} | троичный {t[0]} / {t[1]}')
    izmerit.TRANZISTORY[TROICHNYJ]['СМ+'] = bylo
    return None


# glavnoe: все таблицы
def glavnoe():
    random.seed(23112026)
    luchshie.nastroit(12)
    pechat_razryadov()
    pechat_slov()
    pechat_poroga()
    chto_esli()
    return None


if __name__ == '__main__':
    glavnoe()
