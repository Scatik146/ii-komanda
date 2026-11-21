# proverka_E6.py — проверка примеров Е.6 «Время» (часть 2)
# запуск: python3 logika/kniga/proverka_E6.py
# Значения: -1 нет, 0 не знаю, 1 да.
from fractions import Fraction
from itertools import product

# Данные.
TRITY = (-1, 0, 1)
BIT = (-1, 1)
GOLOS = {"всего": 25, "ракета": 14, "комета": 6}         # голосование: 20 проголосовали
GOLOS_SPOR = {"всего": 25, "ракета": 11, "комета": 9}    # контрпример: перевес мал
SBYLOS = Fraction(7, 10)                                 # доля сбывшихся прогнозов - по записям


# Слова нижнего уровня.
def ne(x):
    otvet = -x
    return otvet


def i_(x, y):
    otvet = min(x, y)
    return otvet


def ili(x, y):                                           # ИЛИ = ¬(¬x ∧ ¬y)
    otvet = ne(i_(ne(x), ne(y)))
    return otvet


def vorota(x):                                           # пропускают только 1
    otvet = 1 if x == 1 else -1
    return otvet


def ne_znayu(x):                                         # не знаю?(x) = ¬ворота(x) ∧ ¬ворота(¬x)
    otvet = i_(ne(vorota(x)), ne(vorota(ne(x))))
    return otvet


def soglasie(x, y):                                      # одинаково - значение, разное - 0
    otvet = x if x == y else 0
    return otvet


def osnovanie(x, b):                                     # (x ∧ b) ∨ (¬b ∧ 0)
    otvet = ili(i_(x, b), i_(ne(b), 0))
    return otvet


def est_li(n, p):                                        # н ∨ (¬п ∧ 0): нашёл - 1, полный без находки - -1
    otvet = ili(n, i_(ne(p), 0))
    return otvet


def soglasie_vseh(znacheniya):
    otvet = znacheniya[0]
    for x in znacheniya[1:]:
        otvet = soglasie(otvet, x)
    return otvet


def neotvratimo(znacheniya, polnyj):                     # основание(согласие всех вариантов, полный)
    otvet = osnovanie(soglasie_vseh(znacheniya), polnyj)
    return otvet


def vektor1(f):
    otvet = [f(x) for x in TRITY]
    return otvet


def vektor2(f):
    otvet = [f(x, y) for x in TRITY for y in TRITY]
    return otvet


# Слова Е.6.
def bylo(n, p):                                          # Т1: по журналу
    otvet = est_li(n, p)
    return otvet


def vsegda_bylo(n, p):                                   # Т2: н - нашли нарушение
    otvet = ne(est_li(n, p))
    return otvet


def k_sroku(s, p):                                       # Т3: п - прошёл ли срок
    otvet = est_li(s, p)
    return otvet


def poka_celo(n):                                        # Т4: журнал будущего никогда не полный
    otvet = ne(est_li(n, -1))
    return otvet


def godno(x, g):                                         # Т5: устаревшее - 0
    otvet = osnovanie(x, g)
    return otvet


def posle(a):                                            # Т6: второе - только после первого
    otvet = vorota(a)
    return otvet


def prognoz_v_realnosti(pr):                             # Т7: у прогноза основания нет
    otvet = osnovanie(pr, -1)
    return otvet


def zadacha(k, zk, zl):                                  # ОЧ-28: (к ∧ зк) ∨ (¬к ∧ зл)
    otvet = ili(i_(k, zk), i_(ne(k), zl))
    return otvet


def i_tam_i_tam(k):                                      # «и за компьютерами, и на листочках»
    otvet = i_(k, ne(k))
    return otvet


def po_variantam(f):                                     # каждый вариант целиком, потом сверка
    otvet = soglasie_vseh([f(k) for k in BIT])
    return otvet


def varianty_golosov(golos):                             # оставшиеся: за ракету, за комету, не пришёл
    ostalos = golos["всего"] - golos["ракета"] - golos["комета"]
    otvet = []
    for hody in product(("р", "к", "-"), repeat=ostalos):
        r = golos["ракета"] + hody.count("р")
        k = golos["комета"] + hody.count("к")
        otvet.append(1 if r > k else -1)
    return otvet


def hvatit(n, v):                                        # ОЧ-20: ворота(н) ∨ ворота(в)
    otvet = ili(vorota(n), vorota(v))
    return otvet


def obeshchat(n, r):                                     # ОЧ-29: ворота(н) ∨ ворота(р)
    otvet = ili(vorota(n), vorota(r))
    return otvet


def gotovitsya(n):                                       # ОЧ-30
    otvet = vorota(n)
    return otvet


def eshche_ne_pozdno(n):
    otvet = ne_znayu(n)
    return otvet


# Проверки.
# 1. Было и всегда было - по журналу
assert vektor2(bylo) == [0, 0, -1, 0, 0, 0, 1, 1, 1]
assert bylo(1, -1) == 1                                  # нашёл запись - было
assert bylo(-1, 1) == -1                                 # журнал полный, записи нет - не было
assert bylo(-1, -1) == 0                                 # контрпример: «не помню» - не −1
assert vektor2(vsegda_bylo) == [0, 0, 1, 0, 0, 0, -1, -1, -1]
assert vsegda_bylo(1, -1) == -1                          # одно опоздание нашлось - −1
assert vsegda_bylo(-1, 0) == 0                           # контрпример: «не помню, чтобы опаздывал»

# 2. К сроку: то же «есть ли», полнота - прошедший срок
assert vektor2(k_sroku) == vektor2(est_li)
assert k_sroku(-1, -1) == 0                              # среда, не проверил - ещё не «не успел»
assert k_sroku(-1, 1) == -1                              # пятница вечер, не проверил - не успел
assert k_sroku(1, -1) == 1                               # проверил в среду - уже успел
assert k_sroku(0, 1) == 0                                # срок прошёл, сделано ли - не знаю (свод выровнен 21.11)

# 3. Пока цело: «всегда будет» не бывает 1
assert vektor1(poka_celo) == [0, 0, -1]
assert 1 not in vektor1(poka_celo)
for n in TRITY:
    assert poka_celo(n) == vsegda_bylo(n, -1) == i_(ne(n), 0)
assert vsegda_bylo(-1, 1) == 1                           # флешка не подводила - по полному журналу 1
assert poka_celo(-1) == 0                                # «и не подведёт» - 0

# 4. Срок годности: устаревшее - 0, не −1
assert vektor2(godno) == [0, 0, -1, 0, 0, 0, 0, 0, 1]
assert godno(1, -1) == 0                                 # телефон из прошлогодней анкеты
assert godno(1, -1) != -1                                # контрпример: зачеркнуть как неверный

# 5. После
assert vektor1(posle) == [-1, -1, 1]
assert posle(0) == -1                                    # «почти все сдали» - ответы не раздаю

# 6. Прогноз и доля
assert vektor1(prognoz_v_realnosti) == [0, 0, 0]
assert SBYLOS == Fraction(7, 10)                         # доля - факт о прошлом, подпись к прогнозу

# 7. ОЧ-28: сначала каждый вариант целиком
assert zadacha(0, 1, 1) == 0                             # по частям - не знаю
assert po_variantam(lambda k: zadacha(k, 1, 1)) == 1     # по вариантам - решаем в любом случае
assert i_tam_i_tam(0) == 0
assert po_variantam(i_tam_i_tam) == -1

# 8. ОЧ-20: итог не изменится - хватит
assert len(varianty_golosov(GOLOS)) == 3 ** 5
assert neotvratimo(varianty_golosov(GOLOS), 1) == 1      # 14 против 6 + 5 - объявляю
assert neotvratimo(varianty_golosov(GOLOS_SPOR), 1) == 0  # 11 против 9 + 5 - ждём
assert vektor2(hvatit) == [-1, -1, 1, -1, -1, 1, 1, 1, 1]
assert hvatit(1, -1) == 1
assert hvatit(0, 0) == -1                                # «кажется, всё ясно» - не хватит

# 9. ОЧ-29: та же таблица, что у «хватит»
assert vektor2(obeshchat) == vektor2(hvatit)
assert obeshchat(0, 1) == 1                              # «проверю до пятницы» - своё решённое
assert obeshchat(0, 0) == -1                             # контрпример: «получит пять»

# 10. ОЧ-30: неизбежное - готовиться; пока 0 - ещё не поздно
assert vektor1(gotovitsya) == [-1, -1, 1]
assert vektor1(eshche_ne_pozdno) == [-1, 1, -1]
assert neotvratimo([1], 1) == 1                          # интернета до 15:00 не будет - один вариант
assert gotovitsya(1) == 1
assert eshche_ne_pozdno(0) == 1                          # «может, отключат» - скачать на флешку
assert gotovitsya(0) == -1                               # контрпример: тормозит - «всё, сорвано»
for n in TRITY:
    assert [gotovitsya(n), eshche_ne_pozdno(n)].count(1) <= 1

print("было вектором:", vektor2(bylo))
print("голосование:", neotvratimo(varianty_golosov(GOLOS), 1), neotvratimo(varianty_golosov(GOLOS_SPOR), 1))
print("Е.6: все проверки прошли")
