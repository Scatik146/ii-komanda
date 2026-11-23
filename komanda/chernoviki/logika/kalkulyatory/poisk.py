"""poisk.py — самая короткая запись действия двух тритов в базисе {И, НЕ, ворота, 0} (перебором).

Действие двух букв — вектор из 9 клеток (x, y ∈ −1, 0, 1). Перебор «по цене»: цена — число вентилей в записи
(запись — дерево, общие куски не считаются общими, поэтому в схеме бывает и дешевле).
Сначала все записи цены 0 (x, y, 0, −1, 1 — провода), потом из записей цены k — записи цены k + 1:
НЕ и ворота над одной, И над двумя с суммой цен k.
"""
import itertools

T = (-1, 0, 1)
KLETKI = [(x, y) for x in T for y in T]


# vektor_nachalnyh: провода: x, y и числа
def vektor_nachalnyh():
    rez = {tuple(x for x, _ in KLETKI): 'x', tuple(y for _, y in KLETKI): 'y'}
    for c in T:
        rez[(c,) * 9] = str(c)
    return rez


# sosedi_odnoj: из записи — НЕ и ворота
def sosedi_odnoj(v, z):
    return [(tuple(-a for a in v), ('НЕ', z)), (tuple(1 if a == 1 else -1 for a in v), ('ворота', z))]


# novye_cenoj: все новые векторы цены k (по уже известным ценам 0..k−1)
def novye_cenoj(po_cene, izvestno, k):
    novye = {}
    kandidaty = [p for v, z in po_cene[k - 1].items() for p in sosedi_odnoj(v, z)]
    for c1 in range(k):
        for (v1, z1), (v2, z2) in itertools.product(po_cene[c1].items(), po_cene[k - 1 - c1].items()):
            kandidaty.append((tuple(min(a, b) for a, b in zip(v1, v2)), ('И', z1, z2)))
    for v, z in kandidaty:
        if v not in izvestno and v not in novye:
            novye[v] = z
    return novye


# najti: самые короткие записи для нужных векторов (до цены potolok); {вектор: (цена, запись)}
def najti(nuzhnye, potolok):
    po_cene, izvestno = [vektor_nachalnyh()], set(vektor_nachalnyh())
    k = 0
    while any(v not in izvestno for v in nuzhnye) and k < potolok:
        k += 1
        po_cene.append(novye_cenoj(po_cene, izvestno, k))
        izvestno |= set(po_cene[k])
    otvet = {}
    for c, sloj in enumerate(po_cene):
        otvet.update({v: (c, sloj[v]) for v in nuzhnye if v in sloj and v not in otvet})
    return otvet


# zapis: запись дерева строкой
def zapis(z):
    return z if isinstance(z, str) else f"{z[0]}({', '.join(zapis(a) for a in z[1:])})"


# postroit: запись → узел схемы (x, y — узлы входов)
def postroit(s, z, x, y):
    if isinstance(z, str):
        rez = {'x': x, 'y': y}.get(z)
        rez = s.konst(int(z)) if rez is None else rez
    else:
        argi = [postroit(s, a, x, y) for a in z[1:]]
        rez = s.ventil(z[0], *argi)
    return rez


# vektor_dejstviya: вектор функции двух тритов
def vektor_dejstviya(f):
    return tuple(f(x, y) for x, y in KLETKI)


# podhodit: вектор совпадает с нужным во всех клетках, где нужное задано (None — «всё равно»)
def podhodit(v, nuzhnyj):
    return all(n is None or a == n for a, n in zip(v, nuzhnyj))


# najti_s_propuskami: самая короткая запись, совпадающая с нужным, где оно задано → (цена, запись) или None
def najti_s_propuskami(nuzhnyj, potolok):
    po_cene, izvestno = [vektor_nachalnyh()], set(vektor_nachalnyh())
    najdeno = next(((0, z) for v, z in po_cene[0].items() if podhodit(v, nuzhnyj)), None)
    k = 0
    while najdeno is None and k < potolok:
        k += 1
        po_cene.append(novye_cenoj(po_cene, izvestno, k))
        izvestno |= set(po_cene[k])
        najdeno = next(((k, z) for v, z in po_cene[k].items() if podhodit(v, nuzhnyj)), None)
    return najdeno
