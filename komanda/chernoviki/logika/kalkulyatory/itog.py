"""itog.py — сводка: два калькулятора, три варианта деталей, действия над десятичными целыми и задача BitNet.

Запуск: python3 itog.py > rezultat.txt   (все узлы и алгоритмы проверяются на числах по ходу)
Варианты: А — строго базис книги; Б — базис + ИЛИ как деталь; В — инженерный: готовые полусумматор и сумматор;
Г — Б + «сдвиг по кругу» (В.4) как деталь, сумматоры собраны из вентилей (сдвиг — 4 транзистора, условие по статье).
Цены деталей В — по статьям (CNTFET, моделирование, подлинники не читаны — это 0): двоичные ПС 14, СМ 28;
троичные ПС 42, СМ 72 транзистора. Время — глубина: вентиль или деталь = 1 (условие: троичная не медленнее).
"""
import math
import random
import shema
import izmerit
import luchshie
from shema import DVOICHNYJ, TROICHNYJ
from uzly import bystryj
from izmerit import shirina, uzel_slozheniya, uzel_umnozheniya, uzel_maca, K
import algoritmy as al

X = 128 * K
DETALI = {DVOICHNYJ: {'ПС+': 14, 'СМ+': 28, 'ПС→': 0, 'СМ→': 0}, TROICHNYJ: {'ПС+': 42, 'СМ+': 72, 'ПС→': 0, 'СМ→': 0}}
for _b, _d in DETALI.items():
    izmerit.TRANZISTORY[_b].update(_d)


# variant: включить вариант деталей
def variant(imya):
    shema.NASTROJKA['ИЛИ у тритов'] = imya in ('Б', 'В', 'Г')
    shema.NASTROJKA['детали'] = imya == 'В'
    shema.NASTROJKA['сдвиг'] = imya == 'Г'
    return imya


# shiriny: (короткое, длинное) слово
def shiriny(b):
    return (shirina(b, -128, 127), shirina(b, -X, X))


# uzly_varianta: {узел: цена} для основания b
def uzly_varianta(b):
    nk, nd = shiriny(b)
    return {'сложение': uzel_slozheniya(b, nd, bystryj), 'умножение': uzel_umnozheniya(b, nd),
            'MAC (хранящий)': uzel_maca(b, nk, nd, False), 'MAC (полный)': uzel_maca(b, nk, nd, True)}


# pechat_uzlov: таблица узлов варианта
def pechat_uzlov(imya):
    variant(imya)
    rez = {b: uzly_varianta(b) for b in (DVOICHNYJ, TROICHNYJ)}
    print(f'\nВАРИАНТ {imya}: узел — двоичный (транзисторы / глубина) | троичный (транзисторы / глубина)')
    for uzel in rez[DVOICHNYJ]:
        d, t = rez[DVOICHNYJ][uzel], rez[TROICHNYJ][uzel]
        print(f"  {uzel:16} {d['транзисторы']:7} / {d['глубина']:4} | {t['транзисторы']:7} / {t['глубина']:4}"
              f"   троичный/двоичный: цена ×{t['транзисторы'] / d['транзисторы']:.2f}, время ×{t['глубина'] / d['глубина']:.2f}")
    return rez


# srednee: средние (сл, умн) действия по выборке; deystvie(sch, x) сам сверяет ответ
def srednee(deystvie, vyborka):
    sch = al.Schet()
    for x in vyborka:
        deystvie(sch, x)
    return (sch.sl / len(vyborka), sch.umn / len(vyborka))


# proverit: assert с понятным сообщением; возвращает значение
def proverit(poluch, nado, chto):
    assert poluch == nado, (chto, poluch, nado)
    return poluch


# dejstviya: {действие: (сл, умн)} для основания b — каждый ответ сверяется с Python
def dejstviya(b, vyb, delit):
    obr, obr100 = al.podobrat_obratnoe(b, X, 10), al.podobrat_obratnoe(b, X, 100, (
        lambda x: (x + 50) // 100) if b == TROICHNYJ else None)
    return {**dejstviya_slova(b, vyb, obr), **dejstviya_chisla(b, vyb, delit, obr100)}


# dejstviya_slova: ввод, вывод, сложение, умножение, степень
def dejstviya_slova(b, vyb, obr):
    return {
        'ввод из десятичной': srednee(lambda s, x: proverit(al.vvod(b, s, str(x)), x, 'ввод'), vyb),
        'вывод в десятичную': srednee(lambda s, x: proverit(al.vyvod(b, s, x, obr), str(x), 'вывод'), vyb),
        'сложение, вычитание': (1, 0),
        'умножение': (0, 1),
        'степень x^e, e = 2…20': (0, sum(al.stepen(b, e) for e in range(2, 21)) / 19),
    }


# dejstviya_chisla: деление, корень, округления
def dejstviya_chisla(b, vyb, delit, obr100):
    nd = shiriny(b)[1]
    koren, delenie = (al.koren_2, al.delenie_2) if b == DVOICHNYJ else (al.koren_3, al.delenie_3)
    return {
        'деление с остатком': srednee(lambda s, x: proverit(delenie(s, x, delit[x], nd), divmod(x, delit[x]), 'дел'),
                                      [abs(x) for x in vyb]),
        'корень (целая часть)': srednee(lambda s, x: proverit(koren(s, x, nd), math.isqrt(x), 'корень'),
                                        [abs(x) for x in vyb]),
        'округление до основание^4': srednee(lambda s, x: proverit(al.okrugl_stepen(b, s, x, 4),
                                                             (x + (8 if b == 2 else 40)) // b ** 4, 'окр'), vyb),
        'округление до сотен': srednee(lambda s, x: proverit(al.okrugl_10(b, s, x, 2, obr100), (x + 50) // 100 * 100,
                                                            'окр10'), [abs(x) for x in vyb]),
    }


# pechat_dejstvij: время действий (в задержках) по узлам варианта
def pechat_dejstvij(uzly_po_baze, vyb, delit):
    print('\nДЕЙСТВИЯ НАД ДЕСЯТИЧНЫМИ ЦЕЛЫМИ (|x| ≤ 128·K): сложений / умножений → время в задержках')
    sch = {b: dejstviya(b, vyb, delit) for b in (DVOICHNYJ, TROICHNYJ)}
    for d in sch[DVOICHNYJ]:
        stroka = []
        for b in (DVOICHNYJ, TROICHNYJ):
            sl, um = sch[b][d]
            t = sl * uzly_po_baze[b]['сложение']['глубина'] + um * uzly_po_baze[b]['умножение']['глубина']
            stroka.append((sl, um, t))
        (s2, u2, t2), (s3, u3, t3) = stroka
        print(f'  {d:24} {s2:5.1f}/{u2:4.1f} → {t2:6.0f} | {s3:5.1f}/{u3:4.1f} → {t3:6.0f}   ×{t3 / t2 if t2 else 0:.2f}')
    return sch


# zadacha: скалярное произведение длины K (веса −1/0/1, активации int8) + перевод суммы обратно (умножить, округлить)
def zadacha(imya, u):
    print(f'\nЗАДАЧА, вариант {imya}: строка слоя BitNet, K = {K}: время (задержки) | MAC: транзисторы | работа на транзистор')
    itogi = {}
    for b in (DVOICHNYJ, TROICHNYJ):
        mac, sl, um = u[b]['MAC (хранящий)'], u[b]['сложение'], u[b]['умножение']
        okr = sl['глубина'] if b == DVOICHNYJ else 0
        t = K * mac['глубина'] + sl['глубина'] + um['глубина'] + okr
        itogi[b] = (t, mac['транзисторы'], 1 / (mac['глубина'] * mac['транзисторы']))
        print(f"  {'двоичный' if b == 2 else 'троичный'}: {t:7} | {mac['транзисторы']:6} | {itogi[b][2] * 1e6:8.1f} (×10⁻⁶)")
    print(f'  троичный/двоичный: время ×{itogi[3][0] / itogi[2][0]:.2f}, MAC ×{itogi[3][1] / itogi[2][1]:.2f}, '
          f'работа на транзистор ×{itogi[3][2] / itogi[2][2]:.2f}')
    return itogi


# pamyat: хранение весов и активаций в «двоичных ячейках»; трит = k ячеек (k = 1,0…1,4 — прогноз для Т-КМОП)
def pamyat():
    print('\nПАМЯТЬ на один вес и одну активацию (в двоичных ячейках; трит Т-КМОП = 1,0…1,4 ячейки — прогноз)')
    print('  вес:       двоичный 2 бита (1,6 — пять весов в байте, нужна распаковка) | троичный 1 трит = 1,0…1,4')
    print('  активация: двоичный 8 бит | троичный 6 тритов = 6,0…8,4')
    print('  модель на 2·10⁹ весов: двоичный 0,40…0,50 ГБ | троичный 0,25…0,35 ГБ')
    return None


# glavnoe: всё по порядку
def glavnoe():
    random.seed(23112026)
    for r in luchshie.nastroit(12):
        print('  слово', r)
    print('ШИРИНЫ: двоичный', shiriny(DVOICHNYJ), 'троичный', shiriny(TROICHNYJ), f'(K = {K}, |сумма| ≤ {X})')
    uzly = {v: pechat_uzlov(v) for v in ('А', 'Б', 'В')}
    vyb = [random.randint(-X, X) for _ in range(400)]
    delit = {abs(x): random.randint(1, 1000) for x in vyb}
    for v in ('А', 'В'):
        print(f'\n(время действий — по узлам варианта {v})')
        pechat_dejstvij(uzly[v], vyb, delit)
    for v in ('А', 'Б', 'В'):
        zadacha(v, uzly[v])
    pamyat()


if __name__ == '__main__':
    glavnoe()
