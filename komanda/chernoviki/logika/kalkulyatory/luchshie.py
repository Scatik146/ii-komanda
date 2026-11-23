"""luchshie.py — для каждого действия двух тритов берём запись короче: «по таблице» (книга) или найденную перебором.

Сравниваем в отдельной схеме: меньше вентилей; при равенстве — меньше глубина. Итог — отчёт строками.
"""
import uzly
from shema import Shema, TROICHNYJ, podschet, vychislit
from poisk import najti, zapis, postroit, vektor_dejstviya, KLETKI
import numpy as np


# cena: (вентилей, глубина) построителя действия в чистой схеме; заодно проверка по 9 клеткам
def cena(postroitel, f):
    s = Shema(TROICHNYJ)
    x, y = s.vhod(), s.vhod()
    v = postroitel(s, x, y)
    xs, ys = np.array([k[0] for k in KLETKI]), np.array([k[1] for k in KLETKI])
    assert list(vychislit(s, {x: xs, y: ys}, [v])[0]) == [f(a, b) for a, b in KLETKI]
    vidy, glubina = podschet(s, [v])
    return (sum(vidy.values()), glubina)


# nastroit: подставить в uzly.SLOVA записи короче; отчёт [(имя, было, стало, запись)]
def nastroit(potolok):
    vektory = {imya: vektor_dejstviya(f) for imya, f in uzly.TABLICY.items()}
    najdeno = najti(list(vektory.values()), potolok)
    otchet = []
    for imya, f in uzly.TABLICY.items():
        bylo = cena(uzly.SLOVA[imya], f)
        stalo, z = bylo, None
        if vektory[imya] in najdeno:
            z = najdeno[vektory[imya]][1]
            kandidat = (lambda z: lambda s, x, y: postroit(s, z, x, y))(z)
            stalo = min(bylo, cena(kandidat, f))
            uzly.SLOVA[imya] = kandidat if stalo < bylo else uzly.SLOVA[imya]
        otchet.append((imya, bylo, stalo, zapis(z) if z and stalo < bylo else 'по таблице / согласие'))
    return otchet
