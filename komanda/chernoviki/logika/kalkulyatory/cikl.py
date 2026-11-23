"""cikl.py — цифра суммы тритов, если в базис добавить «следующий по кругу» (successor: −1 → 0 → 1 → −1).

Цифра суммы a + b = a, сдвинутое по кругу b раз: окошки b выбирают одно из a, цикл(a), цикл(цикл(a)).
Сравнение: строго базис (А) — 33 вентиля, глубина 13; с ИЛИ (Б) — 24 / 9; с циклом — считает программа.
"""
import itertools
import numpy as np
import shema
from shema import Shema, TROICHNYJ, podschet, vychislit, i_, ili
from uzly import okna, TRITY

from uzly import cifra_sdvigom as cifra_s_ciklom


# proverit: все 9 пар; (вентили по видам, глубина)
def proverit():
    shema.NASTROJKA['ИЛИ у тритов'] = True
    s = Shema(TROICHNYJ)
    a, b = s.vhod(), s.vhod()
    r = cifra_s_ciklom(s, a, b)
    xs, ys = (np.array(v) for v in zip(*itertools.product(TRITY, TRITY)))
    assert np.all(vychislit(s, {a: xs, b: ys}, [r])[0] == (xs + ys + 1) % 3 - 1)
    return podschet(s, [r])


if __name__ == '__main__':
    print(proverit())
