"""mashina_sdvig.py — сколько даёт всей машине «сдвиг по кругу» как деталь (вариант Г).

Сравниваем троичную Г с двоичной А (обе собраны из вентилей — время в задержках вентилей, честно один к одному)
и с двоичной В (готовые сумматоры — так её делают на деле; задержка готового сумматора = 1, это в её пользу).
Действия — по алгоритмам «стало» (uluchsheniya.py), задача — строка слоя BitNet (itog.py). Узлы проверяются на числах.
"""
import shema
import itog
import uluchsheniya as ul
from shema import Shema, DVOICHNYJ, TROICHNYJ
from uzly import summator
from izmerit import cena_uzla


# razryad: (транзисторы, глубина) полного сумматора одного разряда в варианте
def razryad(variant, b):
    itog.variant(variant)
    s = Shema(b)
    a, x, c = s.vhod(), s.vhod(), s.vhod()
    r = cena_uzla(s, list(summator(s, a, x, c)))
    return (r['транзисторы'], r['глубина'])


# mashina: (узлы, времена действий «стало») варианта для основания b
def mashina(variant, b):
    itog.variant(variant)
    u = itog.uzly_varianta(b)
    return (u, ul.vremena(b, u['сложение']['глубина'], u['умножение']['глубина']))


# stroka: строка сравнения двух машин
def stroka(imya, d, t):
    return f'  {imya:24} {d:8} | {t:8} | ×{t / d:.2f}'


# sravnit: троичная Г против двоичной (вариант dv)
def sravnit(dv, tg):
    (ud, vd), (ut, vt) = dv, tg
    print(stroka('сложение: транзисторы', ud['сложение']['транзисторы'], ut['сложение']['транзисторы']))
    print(stroka('сложение: время', ud['сложение']['глубина'], ut['сложение']['глубина']))
    print(stroka('умножение: время', ud['умножение']['глубина'], ut['умножение']['глубина']))
    print(stroka('MAC: транзисторы', ud['MAC (хранящий)']['транзисторы'], ut['MAC (хранящий)']['транзисторы']))
    for d in vd:
        print(stroka(d, vd[d][1], vt[d][1]))
    return None


# glavnoe: разряд в вариантах; машина Г против двоичных А и В; задача
def glavnoe():
    for v in ('А', 'Б', 'Г'):
        print(f'сумматор разряда, вариант {v}: двоичный {razryad(v, DVOICHNYJ)} | троичный {razryad(v, TROICHNYJ)}')
    tg = mashina('Г', TROICHNYJ)
    for dv in ('А', 'В'):
        print(f'\nтроичная Г против двоичной {dv}: двоичная | троичная | троичная/двоичная')
        sravnit(mashina(dv, DVOICHNYJ), tg)
    itog.zadacha('Г против двоичной Г (= А)', {DVOICHNYJ: mashina('А', DVOICHNYJ)[0], TROICHNYJ: tg[0]})
    return None


if __name__ == '__main__':
    glavnoe()
