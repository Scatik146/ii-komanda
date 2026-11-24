"""otvety_urok9.py — урок 9 (8 кл.): исходник 4×4, сосед 4×4→8×8, середины 4×4→7×7, обратная задача, сумма минут."""
ISHODNIK = [[8, 8, 4, 0], [8, 4, 0, 0], [4, 0, 0, 4], [0, 0, 4, 8]]


# sosed: картинка, k → увеличенная в k раз копированием родителя
def sosed(kartinka, k):
    n = len(kartinka) * k
    return [[kartinka[i // k][j // k] for j in range(n)] for i in range(n)]


# os: новая координата → список старых (одна — копия, две — середина)
def os_(i):
    return [i // 2] if i % 2 == 0 else [i // 2, i // 2 + 1]


# serediny: картинка n×n → (2n−1)×(2n−1), середины — средние соседей
def serediny(kartinka):
    n = 2 * len(kartinka) - 1
    rez = []
    for i in range(n):
        stroka = []
        for j in range(n):
            vals = [kartinka[a][b] for a in os_(i) for b in os_(j)]
            stroka.append(sum(vals) / len(vals))
        rez.append(stroka)
    return rez


# doli: n → (копий, среднее 2, среднее 4) для середин
def doli(n):
    return (n * n, 2 * n * (n - 1), (n - 1) ** 2)


print('сосед 8×8:')
[print(' '.join(map(str, r))) for r in sosed(ISHODNIK, 2)]
s = serediny(ISHODNIK)
print('середины 7×7 (все целые:', all(v == int(v) for r in s for v in r), '):')
[print(' '.join(str(int(v)) for v in r)) for r in s]
print('доли n=4,5,10:', doli(4), doli(5), doli(10), 'сумма n=5:', sum(doli(5)))
print('копий сосед 5×5→10×10:', 100)
m = [2, 9, 3, 4, 9, 4, 4, 4, 1]
print('минуты:', m, 'сумма', sum(m), 'нарастающим:', [sum(m[:i + 1]) for i in range(len(m))])
