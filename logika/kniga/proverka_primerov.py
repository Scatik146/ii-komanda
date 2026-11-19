"""Проверка примеров книги: каждое равенство «A = B = C» из таблиц раздела
верно на всех наборах значений букв.
Запуск: python3 proverka_primerov.py chast-1-bit/B-zakony.md"""
import sys
from itertools import product
from pathlib import Path

# очередь действий (А.1): чем больше число, тем раньше выполняется
STUPEN = {"≡": 1, "→": 2, "∨": 3, "⊕": 3, "∧": 4}
DEJSTVIE = {
    "≡": lambda x, y: int(x == y),
    "→": lambda x, y: int((not x) or y),
    "∨": lambda x, y: x | y,
    "⊕": lambda x, y: x ^ y,
    "∧": lambda x, y: x & y,
}


# leksemy: строка формулы → список знаков и букв
def leksemy(formula):
    spisok = [z for z in formula if not z.isspace()]
    return spisok


# operand: буква, константа, ¬… или скобка; возвращает (значение, позиция)
def operand(zn, poz, nabor):
    z = zn[poz]
    if z == "¬":
        znach, poz = operand(zn, poz + 1, nabor)
        otvet = (1 - znach, poz)
    elif z == "(":
        znach, poz = vyrazhenie(zn, poz + 1, nabor, 0)
        otvet = (znach, poz + 1)
    elif z in "01":
        otvet = (int(z), poz + 1)
    else:
        otvet = (nabor[z], poz + 1)
    return otvet


# vyrazhenie: разбор с учётом ступеней; стрелку считаем справа налево
def vyrazhenie(zn, poz, nabor, nizhe):
    levoe, poz = operand(zn, poz, nabor)
    while poz < len(zn) and zn[poz] in STUPEN and STUPEN[zn[poz]] > nizhe:
        znak = zn[poz]
        porog = STUPEN[znak] - 1 if znak == "→" else STUPEN[znak]
        pravoe, poz = vyrazhenie(zn, poz + 1, nabor, porog)
        levoe = DEJSTVIE[znak](levoe, pravoe)
    return levoe, poz


# vektor: значения формулы на всех наборах букв
def vektor(formula, bukvy):
    zn = leksemy(formula)
    nabory = [dict(zip(bukvy, n)) for n in product((0, 1), repeat=len(bukvy))]
    znacheniya = tuple(vyrazhenie(zn, 0, n, 0)[0] for n in nabory)
    return znacheniya


# ravenstvo_verno: все части «A = B = C» дают один вектор
def ravenstvo_verno(stroka):
    chasti = [c.replace("★", "").strip() for c in stroka.split(" = ")]
    bukvy = sorted({z for z in stroka if z.isalpha() and z.islower()})
    vektory = {vektor(c, bukvy) for c in chasti}
    return len(vektory) == 1


# ravenstva: последние ячейки строк таблиц, где есть « = »
def ravenstva(tekst):
    stroki = [s for s in tekst.splitlines() if s.startswith("| ") and " = " in s]
    spisok = [[ya.strip() for ya in s.strip("|").split("|")] for s in stroki]
    vse = [ya for yachejki in spisok for ya in (yachejki[0], yachejki[-1])]
    return vse


# glavnoe: проверить все равенства раздела
def glavnoe(imya):
    vse = ravenstva(Path(imya).read_text(encoding="utf-8"))
    oshibki = [r for r in vse if not ravenstvo_verno(r)]
    for r in oshibki:
        print("НЕВЕРНО:", r)
    print(f"проверено равенств: {len(vse)}, неверных: {len(oshibki)}")
    return len(oshibki)


if __name__ == "__main__":
    sys.exit(1 if glavnoe(sys.argv[1]) else 0)
