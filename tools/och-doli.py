"""och-doli.py — доли применения правил очень осторожного человека по журналу испытания.

Вход:  komanda/zadaniya/045/ispytanie.md — таблица: когда | момент | правило | что было | итог
       итог начинается со знака: + помогло, − применила — не помогло, ! нужно было, но не применила,
       = ничего не изменило, ? не хватило правила.
Выход: таблица «правило → применений, +, −, =, ?, доля помогло» и правила листка, которые не применялись.
Запуск из корня ii-komanda: python3 -I tools/och-doli.py [--md файл]
Доли — счёт программы, а не вывод: при малом числе случаев это 0 (Л40).
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

ZHURNAL = Path('komanda/zadaniya/045/ispytanie.md')
LISTOK_STROK = 46


# stroki_tablicy: строки журнала, у которых пять ячеек и первая — дата
def stroki_tablicy(tekst):
    stroki = [s for s in tekst.splitlines() if re.match(r'\|\s*\d{2}\.\d{2}', s)]
    return [[y.strip() for y in s.strip().strip('|').split('|')] for s in stroki]


# metki: метки правил в ячейке «правило»: Л12, К36 → ОЧ-36, ОЧ-01, ОЧ-Б2
def metki(yachejka):
    najdeno = re.findall(r'Л\d+|К\d+|ОЧ-[А-ЯA-Z]?\d+', yachejka)
    return [('ОЧ-' + m[1:]) if m.startswith('К') else m for m in najdeno]


# znak_itoga: первый знак итога (+, −, =, ?); звёздочки и пробелы пропускаются
def znak_itoga(yachejka):
    najdeno = re.search(r'[+−=?!]', yachejka)
    return najdeno.group(0) if najdeno else '?'


# poschitat: метка → счётчики по знакам
def poschitat(stroki):
    schet = defaultdict(lambda: defaultdict(int))
    for s in stroki:
        znak = znak_itoga(s[4])
        for m in metki(s[2]):
            schet[m][znak] += 1
    return schet


# dolya: доля «помогло» дробью «a из n»
def dolya(s):
    vsego = sum(s.values())
    return f"{s['+']} из {vsego}"


# tablica: Markdown-таблица счёта, по убыванию числа применений
def tablica(schet):
    stroki = ['| правило | случаев | + | − | ! пропуск | = | ? | помогло |', '|---|---|---|---|---|---|---|---|']
    for m, s in sorted(schet.items(), key=lambda x: (-sum(x[1].values()), x[0])):
        stroki.append(f"| {m} | {sum(s.values())} | {s['+']} | {s['−']} | {s['!']} | {s['=']} | {s['?']} | {dolya(s)} |")
    return '\n'.join(stroki)


# ne_primenyalis: строки листка, ни разу не попавшие в журнал
def ne_primenyalis(schet):
    bylo = {int(m[1:]) for m in schet if m.startswith('Л')}
    return [n for n in range(1, LISTOK_STROK + 1) if n not in bylo]


# glavnoe: посчитать и показать
def glavnoe():
    stroki = stroki_tablicy(ZHURNAL.read_text(encoding='utf-8'))
    schet = poschitat(stroki)
    tekst = (f"Случаев в журнале: {len(stroki)}.\n\n" + tablica(schet) +
             "\n\nСтроки листка, которые ещё не применялись: " + ', '.join(f'Л{n}' for n in ne_primenyalis(schet)) +
             '.\n\nМетки ОЧ-01, ОЧ-Б2 и подобные — номера старого свода; их место в листке сверить (одно знание — одно место).\n')
    print(tekst)
    if '--md' in sys.argv:
        Path(sys.argv[sys.argv.index('--md') + 1]).write_text(tekst, encoding='utf-8')


glavnoe()
