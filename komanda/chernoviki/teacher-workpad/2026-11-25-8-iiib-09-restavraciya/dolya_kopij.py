"""dolya_kopij.py — какая доля клеток новой картинки совпадает с исходной клеткой (копия), при увеличении 4×4 → 8×8 и 4×4 → 7×7."""
from fractions import Fraction as F


# koordinaty: новая клетка i → позиция в старой сетке при способе sposob
def koordinaty(i, n_old, n_new, sposob):
    if sposob == 'centry':
        x = (F(2 * i + 1, 2) * n_old / n_new) - F(1, 2)
    elif sposob == 'ugly':
        x = F(i * (n_old - 1), n_new - 1)
    else:
        x = F(i * n_old // n_new)
    return x


# vid_kletki: позиция по двум осям → «копия», «из 2 соседей», «из 4 соседей»
def vid_kletki(x, y):
    celyh = (x.denominator == 1) + (y.denominator == 1)
    return {2: 'копия', 1: 'из 2 соседей', 0: 'из 4 соседей'}[celyh]


# podschet: размеры и способ → {вид: число клеток}
def podschet(n_old, n_new, sposob):
    schet = {}
    for i in range(n_new):
        for j in range(n_new):
            v = vid_kletki(koordinaty(i, n_old, n_new, sposob), koordinaty(j, n_old, n_new, sposob))
            schet[v] = schet.get(v, 0) + 1
    return schet


for n_new, sposob in [(8, 'sosed'), (8, 'centry'), (8, 'ugly'), (7, 'ugly')]:
    print(f'4×4 → {n_new}×{n_new}, {sposob}:', podschet(4, n_new, sposob))
