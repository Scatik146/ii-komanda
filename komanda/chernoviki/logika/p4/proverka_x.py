"""proverka_x.py — П.4: проверка схем с неизвестным (X): три способа и точный ответ.

Задача. Схема собрана из И, ИЛИ, НЕ (сумматор → умножитель → кусок строки слоя). В ней есть неизвестное:
  А — неизвестно значение входа (один бит или целое слово);
  Б — сломан один вентиль, и неизвестно какой; что он выдаёт — тоже неизвестно (модель неисправности X);
  В — оба сразу: неизвестный вход и неизвестно кто сдох.
Вопрос к каждому выходу: «какой здесь будет бит?» Ответы: 0, 1 или «не знаю».
Способы:
  1 — двузначная на битах: X подменяют числом (0 или 1) — один прогон, ответ всегда уверенный;
  2 — наша логика на битах «двумя проводами»: 1 = (1, 0), 0 = (0, 1), не знаю = (0, 0);
  3 — наша логика на тритах: бит 0 → −1, 1 → 1, не знаю → 0; И = меньшее, ИЛИ = большее, НЕ = −x.
Точный ответ — перебор всех значений X (2 прогона на каждое неизвестное, 2^k на k неизвестных).
Меры (по всем выходным битам всех случаев): ложное «да» — уверенный ответ там, где на деле может быть и 0, и 1
(X-оптимизм); лишнее «не знаю» — «не знаю» там, где бит на деле известен (X-пессимизм); прогоны; цена (транзисторы).
Запуск: python3 -I proverka_x.py > rezultat-x.txt
"""
import os
import sys
import itertools
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'kalkulyatory'))
import shema                          # noqa: E402
from shema import Shema, DVOICHNYJ   # noqa: E402
from uzly import summator, volna     # noqa: E402
from umnozhenie import umnozhitel, chislo  # noqa: E402

VENTILI = ('И', 'ИЛИ', 'НЕ')
# TRANZISTORY: цена вентиля в каждой записи (два провода и трит — как в kalkulyatory/dvuhprovodnaya.py)
TRANZISTORY = {'бит': {'И': 6, 'ИЛИ': 6, 'НЕ': 2}, 'провода': {'И': 12, 'ИЛИ': 12, 'НЕ': 0},
               'трит': {'И': 6, 'ИЛИ': 6, 'НЕ': 2}}
X = 'X'                                 # отметка «значение неизвестно» в словаре мест


# --- три записи значений: действие вентиля ---------------------------------------------------

# bit_ventil: вентиль над битами 0/1
def bit_ventil(vid, a):
    assert vid in VENTILI, vid
    if vid == 'НЕ':
        rez = 1 - a[0]
    if vid == 'И':
        rez = a[0] & a[1]
    if vid == 'ИЛИ':
        rez = a[0] | a[1]
    return rez


# trit_ventil: вентиль над тритами −1/0/1 (наша логика)
def trit_ventil(vid, a):
    if vid == 'НЕ':
        rez = -a[0]
    if vid == 'И':
        rez = np.minimum(a[0], a[1])
    if vid == 'ИЛИ':
        rez = np.maximum(a[0], a[1])
    return rez


# provoda_ventil: вентиль над парами проводов (p, n)
def provoda_ventil(vid, a):
    if vid == 'НЕ':
        rez = (a[0][1], a[0][0])
    if vid == 'И':
        rez = (a[0][0] & a[1][0], a[0][1] | a[1][1])
    if vid == 'ИЛИ':
        rez = (a[0][0] | a[1][0], a[0][1] & a[1][1])
    return rez


# --- запись входа и неизвестного в каждой записи ---------------------------------------------

# iz_bita: бит-массив → значение записи
def iz_bita(zapis, b):
    rez = b
    if zapis == 'трит':
        rez = 2 * b - 1
    if zapis == 'провода':
        rez = (b, 1 - b)
    return rez


# neizvestnoe: «не знаю» в записи (для битов — подмена числом podmena)
def neizvestnoe(zapis, dlina, podmena):
    rez = np.full(dlina, podmena)
    if zapis == 'трит':
        rez = np.zeros(dlina, dtype=int)
    if zapis == 'провода':
        rez = (np.zeros(dlina, dtype=int), np.zeros(dlina, dtype=int))
    return rez


DEJSTVIE = {'бит': bit_ventil, 'трит': trit_ventil, 'провода': provoda_ventil}


# --- прогон схемы ----------------------------------------------------------------------------

# progon: значения выходов; mesta — {узел: X или 0/1} (X — «не знаю» записи, число — подмена)
def progon(s, vhody, vyhody, zapis, mesta, podmena=0):
    dlina = len(next(iter(vhody.values())))
    zn = {}
    for n, (vid, argi, _) in enumerate(s.uzly):
        if vid == 'вход':
            zn[n] = iz_bita(zapis, vhody[n])
        elif vid == 'конст':
            zn[n] = iz_bita(zapis, np.full(dlina, argi[0]))
        else:
            zn[n] = DEJSTVIE[zapis](vid, [zn[a] for a in argi])
        if n in mesta:
            zn[n] = zamena(zapis, dlina, mesta[n], podmena)
    return [zn[v] for v in vyhody]


# zamena: что стоит в месте неизвестного: «не знаю» записи или заданный бит
def zamena(zapis, dlina, chto, podmena):
    rez = neizvestnoe(zapis, dlina, podmena)
    if chto != X:
        rez = iz_bita(zapis, np.full(dlina, chto))
    return rez


# v_otvet: значение записи → ответ по битам: 1, 0 или −1 («не знаю»)
def v_otvet(zapis, v):
    rez = v
    if zapis == 'трит':
        rez = (v + 1) // 2 - (v == 0)
    if zapis == 'провода':
        rez = v[0] - (1 - v[0] - v[1])
    return rez


# --- ответы трёх способов и точный ------------------------------------------------------------

# sovpadayut: склейка ответов прогонов: где все одинаковы — этот бит, иначе −1
def sovpadayut(otvety):
    rez = otvety[0].copy()
    for o in otvety[1:]:
        rez = np.where(rez == o, rez, -1)
    return rez


# tochno: точный ответ: перебор значений неизвестных в каждой из возможностей; (ответы выходов, прогоны)
def tochno(s, vhody, vyhody, vozmozhnosti):
    progony = []
    for mesta in vozmozhnosti:
        for znach in itertools.product((0, 1), repeat=len(mesta)):
            progony.append(progon(s, vhody, vyhody, 'бит', dict(zip(mesta, znach))))
    rez = [sovpadayut([p[k] for p in progony]) for k in range(len(vyhody))]
    return (rez, len(progony))


# nash: наша логика: по прогону на возможность (X во всех её местах), склейка; (ответы, прогоны)
def nash(s, vhody, vyhody, vozmozhnosti, zapis):
    progony = []
    for mesta in vozmozhnosti:
        p = progon(s, vhody, vyhody, zapis, {m: X for m in mesta})
        progony.append([v_otvet(zapis, v) for v in p])
    rez = [sovpadayut([p[k] for p in progony]) for k in range(len(vyhody))]
    return (rez, len(progony))


# dvuznachnyj: способ 1: один прогон, X подменён числом (вход — 0; сломанный вентиль — как исправный)
def dvuznachnyj(s, vhody, vyhody, vozmozhnosti):
    mesta = {m: 0 for m in vozmozhnosti[0] if s.uzly[m][0] == 'вход'}
    return (progon(s, vhody, vyhody, 'бит', mesta), 1)


# srazu: наша логика одним прогоном: X сразу во всех местах всех возможностей
def srazu(s, vhody, vyhody, vozmozhnosti, zapis):
    mesta = {m: X for v in vozmozhnosti for m in v}
    p = progon(s, vhody, vyhody, zapis, mesta)
    return ([v_otvet(zapis, v) for v in p], 1)


# --- меры -------------------------------------------------------------------------------------

# mery: счёт по всем выходным битам: верные «да», ложные «да», верные и лишние «не знаю», ошибки
def mery(pravda, otvet):
    m = {'верное да': 0, 'ложное да': 0, 'верное не знаю': 0, 'лишнее не знаю': 0, 'ошибка': 0}
    for t, r in zip(pravda, otvet):
        m['верное да'] += int(np.sum((r >= 0) & (t >= 0) & (r == t)))
        m['ошибка'] += int(np.sum((r >= 0) & (t >= 0) & (r != t)))
        m['ложное да'] += int(np.sum((r >= 0) & (t < 0)))
        m['верное не знаю'] += int(np.sum((r < 0) & (t < 0)))
        m['лишнее не знаю'] += int(np.sum((r < 0) & (t >= 0)))
    return m


# slozhit_mery: сумма двух счётов
def slozhit_mery(a, b):
    return {k: a.get(k, 0) + b[k] for k in b}


# --- схемы: сумматор → умножитель → кусок строки слоя ----------------------------------------

# Obrazec: схема для опыта — {'имя', 'схема', 'входы': [[узлы операнда]], 'выходы': [узлы], 'проверка': f(числа, выход)}

# chistyj_bazis: схемы строятся из И, ИЛИ, НЕ — без готовых деталей (настройку могли оставить другие программы)
def chistyj_bazis():
    for k in shema.NASTROJKA:
        shema.NASTROJKA[k] = False
    return shema.NASTROJKA


# vse_nabory: все наборы битов входов → {узел: массив}
def vse_nabory(vhody):
    uzly = [u for op in vhody for u in op]
    nabory = np.array(list(itertools.product((0, 1), repeat=len(uzly))))
    return {u: nabory[:, k] for k, u in enumerate(uzly)}


# operand: число операнда (дополнительный код) из значений его битов
def operand(zn, bity):
    return chislo(DVOICHNYJ, [zn[b] for b in bity])


# shema_summatora: полный сумматор одного разряда: a + b + c = сумма + 2·перенос
def shema_summatora():
    chistyj_bazis()
    s = Shema(DVOICHNYJ)
    a, b, c = s.vhod(), s.vhod(), s.vhod()
    vyh = list(summator(s, a, b, c))
    proverka = (lambda zn, v: np.all(v[0] + 2 * v[1] == zn[a] + zn[b] + zn[c]))
    return {'имя': 'сумматор разряда', 'схема': s, 'входы': [[a], [b], [c]], 'выходы': vyh, 'проверка': proverka}


# shema_umnozhitelya: умножитель n × n бит со знаком → 2n бит
def shema_umnozhitelya(n):
    chistyj_bazis()
    s = Shema(DVOICHNYJ)
    a, b = [s.vhod() for _ in range(n)], [s.vhod() for _ in range(n)]
    vyh = umnozhitel(s, a, b, lambda s_, x, y: s_.ventil('И', x, y))
    proverka = (lambda zn, v: np.all(chislo(DVOICHNYJ, v) == operand(zn, a) * operand(zn, b)))
    return {'имя': f'умножитель {n}×{n}', 'схема': s, 'входы': [a, b], 'выходы': vyh, 'проверка': proverka}


# shema_stroki: кусок строки слоя: a·b + c·d (по n бит со знаком), сумма волной
def shema_stroki(n):
    chistyj_bazis()
    s = Shema(DVOICHNYJ)
    a, b, c, d = ([s.vhod() for _ in range(n)] for _ in range(4))
    p1 = umnozhitel(s, a, b, lambda s_, x, y: s_.ventil('И', x, y))
    p2 = umnozhitel(s, c, d, lambda s_, x, y: s_.ventil('И', x, y))
    vyh = volna(s, p1 + [p1[-1]], p2 + [p2[-1]])
    proverka = (lambda zn, v: np.all(chislo(DVOICHNYJ, v) ==
                                     operand(zn, a) * operand(zn, b) + operand(zn, c) * operand(zn, d)))
    return {'имя': f'строка слоя: a·b + c·d, {n} бит', 'схема': s, 'входы': [a, b, c, d], 'выходы': vyh,
            'проверка': proverka}


# ventili: номера вентилей, от которых зависят выходы (кандидаты «кто сдох»)
def ventili(sh):
    s, nuzhny, stek = sh['схема'], set(), list(sh['выходы'])
    while stek:
        n = stek.pop()
        if n not in nuzhny:
            nuzhny.add(n)
            stek += [a for a in s.uzly[n][1] if s.uzly[n][0] != 'конст']
    return sorted(n for n in nuzhny if s.uzly[n][0] in VENTILI)


# cena_shemy: транзисторы схемы в записи
def cena_shemy(sh, zapis):
    s = sh['схема']
    return sum(TRANZISTORY[zapis][s.uzly[n][0]] for n in ventili(sh))


# proverit_shemu: исправная схема даёт верные числа на всех наборах (замок: иначе остановка)
def proverit_shemu(sh):
    zn = vse_nabory(sh['входы'])
    v = progon(sh['схема'], zn, sh['выходы'], 'бит', {})
    assert sh['проверка'](zn, v), sh['имя']
    return len(next(iter(zn.values())))


# --- случаи: что неизвестно ---------------------------------------------------------------------
# случай — список возможностей; возможность — список мест (узлов), где значение неизвестно

# sluchai_vhod: А — неизвестен один входной бит (по очереди каждый)
def sluchai_vhod(sh):
    return [[[u]] for op in sh['входы'] for u in op]


# sluchai_slovo: А — неизвестно целое слово (второй операнд)
def sluchai_slovo(sh):
    return [[list(sh['входы'][1])]]


# sluchai_kto: Б — сломан один вентиль, неизвестно какой (одна задача, G возможностей)
def sluchai_kto(sh):
    return [[[g] for g in ventili(sh)]]


# sluchai_oba: В — неизвестен входной бит и неизвестно, кто сдох
def sluchai_oba(sh):
    vse = ventili(sh)
    return [[[u, g] for g in vse] for op in sh['входы'] for u in op]


# sluchai_izvestnyj: подозреваемый вентиль известен (по очереди каждый) — для «куда уходит X»
def sluchai_izvestnyj(sh):
    return [[[g]] for g in ventili(sh)]


# --- опыт ---------------------------------------------------------------------------------------

# sposoby: ответы и прогоны всех способов на одном случае
def sposoby(sh, zn, sluchaj):
    s, vy = sh['схема'], sh['выходы']
    rez = {'точно': tochno(s, zn, vy, sluchaj), '1: биты, X → число': dvuznachnyj(s, zn, vy, sluchaj),
           '2: наша, два провода': nash(s, zn, vy, sluchaj, 'провода'),
           '3: наша, триты': nash(s, zn, vy, sluchaj, 'трит'),
           '3: триты, все X сразу': srazu(s, zn, vy, sluchaj, 'трит')}
    assert all(np.all(a == b) for a, b in zip(rez['2: наша, два провода'][0], rez['3: наша, триты'][0]))
    return rez


# opyt: сумма мер и прогонов по всем случаям задачи
def opyt(sh, sluchai):
    zn, itog = vse_nabory(sh['входы']), {}
    for sluchaj in sluchai:
        rez = sposoby(sh, zn, sluchaj)
        for imya, (otvet, progony) in rez.items():
            m = mery(rez['точно'][0], otvet)
            m['прогонов'] = progony
            itog[imya] = slozhit_mery(itog.get(imya, {}), m)
    return itog


# kuda_X: известный подозреваемый: доля (вентиль, набор), где X дошёл до выхода, и среднее неизвестных битов
def kuda_X(sh):
    zn, doshel, bitov, vsego = vse_nabory(sh['входы']), 0, 0, 0
    for sluchaj in sluchai_izvestnyj(sh):
        pravda = np.array(tochno(sh['схема'], zn, sh['выходы'], sluchaj)[0])
        neizv = np.sum(pravda < 0, axis=0)
        doshel += int(np.sum(neizv > 0))
        bitov += int(np.sum(neizv))
        vsego += len(neizv)
    return (doshel / vsego, bitov / vsego, len(sh['выходы']))


# --- поиск виновника: «непонятно, кто сдох» (диагностика по модели неисправности X) ----------

# (поведение: «случайно» — на каждом наборе свой бит, «залип» — один бит; неизвестный вход — случайный бит)
# nablyudenie: что выдал сломанный чип с виновником g
def nablyudenie(sh, zn, g, gen, vhod_x, povedenie):
    dlina = len(next(iter(zn.values())))
    znach = dict(zn)
    if vhod_x is not None:
        znach[vhod_x] = gen.integers(0, 2, dlina)
    bity = gen.integers(0, 2, dlina)
    if povedenie == 'залип':
        bity = np.full(dlina, gen.integers(0, 2))
    return progon_s_massivom(sh, znach, g, bity)


# progon_s_massivom: прогон битов, где выход вентиля g заменён массивом bity
def progon_s_massivom(sh, zn, g, bity):
    s, rez = sh['схема'], {}
    for n, (vid, argi, _) in enumerate(s.uzly):
        if vid == 'вход':
            rez[n] = zn[n]
        elif vid == 'конст':
            rez[n] = np.full(len(bity), argi[0])
        else:
            rez[n] = bit_ventil(vid, [rez[a] for a in argi])
        if n == g:
            rez[n] = bity
    return [rez[v] for v in sh['выходы']]


# ne_protivorechit: ответы (1, 0, −1) не спорят с увиденным: где ответ уверен — совпадает
def ne_protivorechit(otvety, vidno):
    return all(np.all((o < 0) | (o == v)) for o, v in zip(otvety, vidno))


# zalip_obyasnyaet: двузначная: «h залип в 0» или «h залип в 1» объясняет всё увиденное
def zalip_obyasnyaet(sh, zn, vidno, mesta, h):
    obyasnyaet = False
    for z in (0, 1):
        v = progon(sh['схема'], zn, sh['выходы'], 'бит', {**mesta, h: z})
        obyasnyaet = obyasnyaet or ne_protivorechit(v, vidno)
    return obyasnyaet


# podozrevaemye_dva: способ 1 (двузначная): h остаётся, если его «залипание» объясняет всё
def podozrevaemye_dva(sh, zn, vidno, vhod_x):
    ost, mesta = [], {}
    if vhod_x is not None:
        mesta = {vhod_x: 0}
    for h in ventili(sh):
        if zalip_obyasnyaet(sh, zn, vidno, mesta, h):
            ost.append(h)
    return (ost, 2 * len(ventili(sh)))


# podozrevaemye_nash: способы 2 и 3: X в h (и во входе); h остаётся, если уверенные биты не спорят с увиденным
def podozrevaemye_nash(sh, zn, vidno, vhod_x, zapis):
    ost = []
    for h in ventili(sh):
        mesta = {h: X}
        if vhod_x is not None:
            mesta[vhod_x] = X
        v = [v_otvet(zapis, o) for o in progon(sh['схема'], zn, sh['выходы'], zapis, mesta)]
        if ne_protivorechit(v, vidno):
            ost.append(h)
    return (ost, len(ventili(sh)))


# podozrevaemye_tochno: точно: h остаётся, если на каждом наборе какое-то значение h (и входа) объясняет увиденное
def podozrevaemye_tochno(sh, zn, vidno, vhod_x):
    ost, progony = [], 0
    mesta_x = []
    if vhod_x is not None:
        mesta_x = [vhod_x]
    for h in sh.get('кандидаты', ventili(sh)):
        obyasneno = np.zeros(len(vidno[0]), dtype=bool)
        for znach in itertools.product((0, 1), repeat=1 + len(mesta_x)):
            v = progon(sh['схема'], zn, sh['выходы'], 'бит', dict(zip([h] + mesta_x, znach)))
            obyasneno |= np.all(np.array(v) == np.array(vidno), axis=0)
            progony += 1
        if np.all(obyasneno):
            ost.append(h)
    return (ost, progony)


# odin_poisk: один сломанный чип (виновник g): кого оставил каждый способ; None — поломку не видно
def odin_poisk(sh, zn, g, gen, vhod_x, povedenie):
    vidno = nablyudenie(sh, zn, g, gen, vhod_x, povedenie)
    ispravno = progon(sh['схема'], zn, sh['выходы'], 'бит', {})
    rez = None
    if vhod_x is not None or not all(np.all(a == b) for a, b in zip(vidno, ispravno)):
        rez = {'точно': podozrevaemye_tochno(sh, zn, vidno, vhod_x),
               '1: биты, «залип»': podozrevaemye_dva(sh, zn, vidno, vhod_x),
               '2: наша, два провода': podozrevaemye_nash(sh, zn, vidno, vhod_x, 'провода'),
               '3: наша, триты': podozrevaemye_nash(sh, zn, vidno, vhod_x, 'трит')}
        assert rez['2: наша, два провода'][0] == rez['3: наша, триты'][0]
        assert set(rez['точно'][0]) <= set(rez['3: наша, триты'][0])
        rez['3 + точно: фильтр, потом перебор'] = filtr_i_perebor(sh, zn, vidno, vhod_x, rez['3: наша, триты'])
    return rez


# filtr_i_perebor: сначала наша логика (G прогонов), потом точный перебор только оставшихся
def filtr_i_perebor(sh, zn, vidno, vhod_x, nash_rez):
    ostalis, progony = nash_rez
    uzkij = dict(sh)
    uzkij['кандидаты'] = ostalis
    tochnye, progony2 = podozrevaemye_tochno(uzkij, zn, vidno, vhod_x)
    assert tochnye == podozrevaemye_tochno(sh, zn, vidno, vhod_x)[0]
    return (tochnye, progony + progony2)


# poisk: виновник — каждый shag-й вентиль: потерян ли виновник, сколько подозреваемых, прогоны
def poisk(sh, povedenie, vhod_x=None, shag=1, semya=2411):
    zn, gen, itog = vse_nabory(sh['входы']), np.random.default_rng(semya), {}
    for g in ventili(sh)[::shag]:
        rez = odin_poisk(sh, zn, g, gen, vhod_x, povedenie)
        for imya, (ost, progony) in (rez or {}).items():
            m = itog.setdefault(imya, {'чипов': 0, 'виновник потерян': 0, 'подозреваемых': 0, 'прогонов': 0})
            m['чипов'] += 1
            m['виновник потерян'] += g not in ost
            m['подозреваемых'] += len(ost)
            m['прогонов'] += progony
    return itog


# --- отчёт ---------------------------------------------------------------------------------------

# zapis_sposoba: в какой записи работает способ (для цены прогона)
def zapis_sposoba(imya):
    rez = 'бит'
    if imya.startswith('2'):
        rez = 'провода'
    if imya.startswith('3'):
        rez = 'трит'
    return rez


# pechat_opyta: таблица мер одной задачи
def pechat_opyta(sh, nazvanie, sluchai):
    itog = opyt(sh, sluchai)
    vsego = sum(itog['точно'][k] for k in ('верное да', 'верное не знаю'))
    print(f'  {nazvanie}: выходных битов {vsego}, из них на деле неизвестны {itog["точно"]["верное не знаю"]}')
    for imya, m in itog.items():
        rabota = m['прогонов'] * cena_shemy(sh, zapis_sposoba(imya))
        print(f'    {imya:24} ложных «да» {m["ложное да"]:7} | лишних «не знаю» {m["лишнее не знаю"]:6} | '
              f'ошибок {m["ошибка"]} | прогонов {m["прогонов"]:6} | работа {rabota:9} тр.·прогон')
    return itog


# pechat_poiska: таблица поиска виновника
def pechat_poiska(sh, nazvanie, povedenie, vhod_x, shag):
    itog = poisk(sh, povedenie, vhod_x, shag)
    print(f'  {nazvanie}')
    for imya, m in itog.items():
        rabota = m['прогонов'] * cena_shemy(sh, zapis_sposoba(imya))
        print(f'    {imya:24} чипов {m["чипов"]:4} | виновник потерян {m["виновник потерян"]:4} | '
              f'подозреваемых в среднем {m["подозреваемых"] / m["чипов"]:6.2f} | прогонов {m["прогонов"]:7} | '
              f'работа {rabota:10} тр.·прогон')
    luchshie(sh, itog)
    return itog


# luchshie: точный ответ лучшими способами: перебор на битах, отсев на двух проводах + перебор, отсев на тритах + перебор
def luchshie(sh, itog):
    bit, prov, trit = (cena_shemy(sh, z) for z in ('бит', 'провода', 'трит'))
    otsev = itog['3: наша, триты']['прогонов']
    ostatok = itog['3 + точно: фильтр, потом перебор']['прогонов'] - otsev
    rabota = {'перебор, биты': itog['точно']['прогонов'] * bit, 'отсев, два провода': otsev * prov + ostatok * bit,
              'отсев, триты': otsev * trit + ostatok * bit}
    dvoichnyj = min(rabota['перебор, биты'], rabota['отсев, два провода'])
    porog = (dvoichnyj - ostatok * bit) / otsev / bit
    print(f'    ЛУЧШИЕ (точный ответ): ' + ' | '.join(f'{k} {v}' for k, v in rabota.items()) +
          f' | лучший двоичный / триты ×{dvoichnyj / rabota["отсев, триты"]:.2f}; '
          f'триты выигрывают, пока тритовая схема дороже двоичной не больше чем в {porog:.2f} раза')
    print('    ЦЕНА ТРИТА (тритовая схема дороже двоичной в r раз): ' + ' | '.join(
        f'r = {r}: ×{dvoichnyj / (otsev * r * trit + ostatok * bit):.2f}' for r in (1.0, 1.2, 1.4)))
    return rabota


# pechat_shemy: всё по одной схеме
def pechat_shemy(sh, shag):
    nabory = proverit_shemu(sh)
    doshel, bitov, vyh = kuda_X(sh)
    ceny = {z: cena_shemy(sh, z) for z in TRANZISTORY}
    print(f'\n{sh["имя"]}: вентилей {len(ventili(sh))}, наборов {nabory}, выходов {vyh}; '
          f'транзисторы: биты {ceny["бит"]}, два провода {ceny["провода"]}, триты {ceny["трит"]}')
    print(f'  известный подозреваемый: X дошёл до выхода в {doshel * 100:.1f} % случаев, '
          f'неизвестных битов в среднем {bitov:.2f} из {vyh}')
    pechat_opyta(sh, 'А, неизвестен один входной бит', sluchai_vhod(sh))
    pechat_opyta(sh, 'А, неизвестно слово (второй операнд)', sluchai_slovo(sh))
    pechat_opyta(sh, 'Б, неизвестно, кто сдох (ответ про биты)', sluchai_kto(sh))
    pechat_poiska(sh, 'Б, поиск виновника: сдох и выдаёт что попало', 'случайно', None, shag)
    pechat_poiska(sh, 'Б, поиск виновника: залип в 0 или 1', 'залип', None, shag)
    pechat_poiska(sh, 'В, оба сразу: вход b0 неизвестен и кто-то сдох', 'случайно', sh['входы'][1][0], shag)
    return None


# glavnoe: три ступени: сумматор → умножитель → кусок строки слоя
def glavnoe():
    pechat_shemy(shema_summatora(), 1)
    pechat_shemy(shema_umnozhitelya(4), 1)
    pechat_shemy(shema_stroki(3), 5)
    return None


if __name__ == '__main__':
    glavnoe()
