"""proverka.py — проверка ядра trit.py одной командой (Марьям, 25.11.2026).

Часть А: строки «пример:» и «контрпример:» эталона bazis.pl — на словах Python.
Часть Б: таблицы слов Python против таблиц Пролога (swipl на сервере или swipl-wasm из drakon-graf).
Итог — троичный: меньшее из А и Б встроенным min Python, а не словом «и» ядра:
проверяемое ядро не судит само себя (испорченное «и» = max давало итог «да», проба 25.11).
Пролога нет — Б = «не знаю».
Код выхода: 0 — да, 1 — нет, 2 — не знаю.
Запуск из корня ii-komanda: python3 -I yadro-trit/proverka.py [путь к клону drakon-graf]
"""
import ast
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import trit  # noqa: E402

# Данные.
ZDES = Path(__file__).resolve().parent
ETALON = ZDES.parent / 'logika' / 'kniga' / 'prolog'
FAJLY = ['bazis.pl', 'chast2-B.pl']
SLOVA1 = ['не', 'ворота', 'погасло', 'не_знаю', 'возможно', 'с_нулём']
SLOVA2 = ['и', 'не_и', 'или', 'погасли_оба', 'подтвердить', 'основание', 'согласие', 'есть_ли', 'сл', 'экв']
STROKA = re.compile(r"^(пример|контрпример)\(([^,]+), '([^']*)', ([а-яё_0-9]+)\((.*)\)\)\.\s*$")
KOD_VYHODA = {trit.ДА: 0, trit.НЕТ: 1, trit.НЕ_ЗНАЮ: 2}


# argumenty: строка аргументов Пролога → кортеж Python (атомы — строки)
def argumenty(tekst):
    s = re.sub(r"([а-яёa-z_][а-яёa-z_0-9]*)", r"'\1'", tekst)
    return ast.literal_eval('(' + s + ',)')


# primery: строки пример/контрпример эталона → (вид, шаг, что, слово, аргументы); остальные — None
def primery(put):
    spisok = []
    for stroka in put.read_text(encoding='utf-8').splitlines():
        m = STROKA.match(stroka)
        if m:
            spisok.append((m.group(1), m.group(2), m.group(3), m.group(4), argumenty(m.group(5))))
        elif stroka.startswith(('пример(', 'контрпример(')):
            spisok.append(None)
    return spisok


# vyvoditsya: выводится ли цель на словах Python; слова нет — None
def vyvoditsya(slovo, args):
    otvet = None
    if slovo == 'трит' and len(args) == 1:
        otvet = trit.это_трит(args[0])
    elif slovo in ('вектор1', 'вектор2'):
        otvet = getattr(trit, slovo)(getattr(trit, args[0])) == list(args[1])
    elif hasattr(trit, slovo):
        try:
            otvet = getattr(trit, slovo)(*args[:-1]) == args[-1]
        except TypeError:
            otvet = None
    return otvet


# otvet_primera: трит одного примера: пример выводится, контрпример нет
def otvet_primera(primer):
    otvet = trit.НЕ_ЗНАЮ
    if primer is not None:
        v = vyvoditsya(primer[3], primer[4])
        if v is not None:
            otvet = trit.ДА if v == (primer[0] == 'пример') else trit.НЕТ
    return otvet


# chast_a: трит части А и список плохих
def chast_a():
    spisok = primery(ETALON / 'bazis.pl')
    otvety = [otvet_primera(p) for p in spisok]
    plohie = [(p, o) for p, o in zip(spisok, otvety) if o != trit.ДА]
    print('А, эталон bazis.pl: строк', len(spisok), '| да', otvety.count(trit.ДА),
          '| нет', otvety.count(trit.НЕТ), '| не знаю', otvety.count(trit.НЕ_ЗНАЮ))
    return min(otvety), plohie


# celi: цели Пролога для таблиц всех слов
def celi():
    return [('вектор1', s) for s in SLOVA1] + [('вектор2', s) for s in SLOVA2]


# prolog_swipl: таблицы через swipl на сервере; нет swipl — None
def prolog_swipl():
    tablicy = None
    if shutil.which('swipl'):
        cel = 'forall(member(V-S, %s), (call(V, S, T), format("~w ~w~n", [S, T])))' % \
              '[' + ', '.join("%s-'%s'" % c for c in celi()) + ']'
        r = subprocess.run(['swipl', '-q', '-g', cel, '-t', 'halt'] + [str(ETALON / f) for f in FAJLY],
                           capture_output=True, text=True)
        tablicy = {s: list(ast.literal_eval(t)) for s, t in (x.split(' ', 1) for x in r.stdout.splitlines())}
    return tablicy


# prolog_wasm: таблицы через swipl-wasm из drakon-graf; нет пути — None
def prolog_wasm(drakon):
    tablicy = None
    lib = Path(drakon) / 'site' / 'experiments' / 'prolog' / 'lib'
    if (lib / 'swipl-web.js').exists():
        r = subprocess.run(['node', str(ZDES / 'prolog-vektory.cjs'), str(lib), str(ETALON),
                            json.dumps(FAJLY), json.dumps(celi(), ensure_ascii=False)],
                           capture_output=True, text=True)
        tablicy = json.loads(r.stdout or 'null')
    return tablicy


# sverit: трит части Б — таблицы Python против таблиц Пролога
def sverit(tablicy):
    otvet = trit.НЕ_ЗНАЮ
    if tablicy:
        rashod = [s for v, s in celi() if getattr(trit, v)(getattr(trit, s)) != tablicy.get(s)]
        print('Б, таблицы против Пролога: слов', len(celi()), '| расходятся', len(rashod), rashod or '')
        otvet = trit.НЕТ if rashod else trit.ДА
    else:
        print('Б, таблицы против Пролога: не знаю (нет swipl и не дан путь к drakon-graf)')
    return otvet


# glavnaya: итог проверки ядра
def glavnaya():
    a, plohie = chast_a()
    for p, o in plohie:
        print('  ', trit.трит(o), p if p else '(строка не разобрана)')
    tablicy = prolog_swipl() or (prolog_wasm(sys.argv[1]) if len(sys.argv) > 1 else None)
    itog = min(a, sverit(tablicy))
    print('Итог ядра:', trit.трит(itog))
    return KOD_VYHODA[itog]


if __name__ == '__main__':
    sys.exit(glavnaya())
