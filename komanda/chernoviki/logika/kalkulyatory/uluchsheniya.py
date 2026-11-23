"""uluchsheniya.py — п. 2 приложения: как ускорить действия алгоритмами (вариант В — готовые детали).

Было (itog.py): шаги друг за другом, каждое сложение — целый сумматор.
Стало: (1) три слагаемых — сначала строка сумматоров 3 → 2 (одна деталь глубины), потом один быстрый сумматор;
(2) у тритов в делении и корне все пробы шага считаются сразу (параллельно), выбор — по знаку;
(3) поправку −(3^k − 1)/2 при выводе прибавляет сам умножитель (лишнее слагаемое в его столбцах).
Время — путь в задержках; работа — сколько сумматоров стоит. Ответы алгоритмов те же — проверены в itog.py.
"""
import shema
import izmerit
import itog
from shema import DVOICHNYJ, TROICHNYJ
from uzly import bystryj

FA = 1


# zaderzhki: (T_сложения, T_умножения) варианта В для основания b
def zaderzhki(b):
    itog.variant('В')
    nk, nd = itog.shiriny(b)
    return (izmerit.uzel_slozheniya(b, nd, bystryj)['глубина'], izmerit.uzel_umnozheniya(b, nd)['глубина'])


# shagi: (деление, корень, десятичных цифр) — по ширине длинного слова
def shagi(b):
    nd = itog.shiriny(b)[1]
    return (nd, (nd + 1) // 2, len(str(itog.X)))


# bylo: время действий «было» — из rezultat.txt (вариант В, посчитано и проверено itog.py)
def bylo(b):
    tekst = open('rezultat.txt').read().split('по узлам варианта В')[1].split('ЗАДАЧА')[0]
    rez = {}
    for stroka in tekst.splitlines():
        chasti = stroka.split('→')
        if len(chasti) == 3:
            rez[chasti[0].split('  ')[1].strip()] = float((chasti[1] if b == 2 else chasti[2]).split()[0])
    return rez


# vremena: {действие: (было, стало)} в задержках
def vremena(b, t_sl, t_um):
    dl, kr, cf = shagi(b)
    tri = t_sl + FA
    vybor = 1
    shag_del = t_sl if b == DVOICHNYJ else t_sl + FA + vybor
    shag_kor = t_sl if b == DVOICHNYJ else t_sl + 2 * FA + vybor
    stalo = {'ввод из десятичной': cf * tri, 'вывод в десятичную': cf * (t_um + tri),
             'деление с остатком': dl * shag_del + t_sl, 'корень (целая часть)': kr * shag_kor}
    return {d: (bylo(b)[d], v) for d, v in stalo.items()}


# glavnoe: таблица «было → стало» для обоих оснований
def glavnoe():
    rez = {b: vremena(b, *zaderzhki(b)) for b in (DVOICHNYJ, TROICHNYJ)}
    print('действие: двоичный было → стало | троичный было → стало | троичный/двоичный было → стало')
    for d in rez[DVOICHNYJ]:
        (d0, d1), (t0, t1) = rez[DVOICHNYJ][d], rez[TROICHNYJ][d]
        print(f'  {d:22} {d0:5.0f} → {d1:5} | {t0:5.0f} → {t1:5} | ×{t0 / d0:.2f} → ×{t1 / d1:.2f}')
    return rez


if __name__ == '__main__':
    glavnoe()
