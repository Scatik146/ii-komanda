"""pokupatel.py — П.4, вторая проверка: «чип с ошибкой уйдёт к покупателю».

Завод проверяет каждый чип: подаёт T случайных наборов и сравнивает выходы с эталоном — ответами программы-модели.
Все наборы подать нельзя (у настоящих чипов их больше, чем секунд во Вселенной), поэтому T мало.
Если в проверке есть неизвестное (вход, который проверка не задаёт: незаписанный регистр), эталон считается тремя способами:
  1 — биты: X → 0, сравниваются все биты;
  2, 3 — наша логика (два провода / триты): сравниваются только биты, где эталон уверен;
  точно — перебор X: сравниваются только биты, известные на деле.
Чип проходит, если ни один сравниваемый бит не разошёлся.
Меры: брак прошёл (ушёл к покупателю) — доля дефектных чипов; годных выброшено — доля исправных;
вред прошедшего брака — у скольких наборов чип покупателя даёт неверный ответ; прогонов эталона на один набор проверок.
Дефект — один сломанный вентиль: «что попало» (случайный бит на каждом наборе) или «залип» (всегда 0 или всегда 1).
Чип, который ни на одном наборе не отличается от исправного, дефектным не считается.
Запуск: python3 -I pokupatel.py > rezultat-pokupatel.txt
"""
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import proverka_x as px   # noqa: E402

SPOSOBY = ('точно', '1: биты, X → 0', '2: наша, два провода', '3: наша, триты')
POVEDENIYA = ('что попало', 'залип')
POVTOROV = 20                         # сколько разных наборов проверок (новые T наборов каждый раз)


# vyborka: T случайных наборов из всех (без повторов) → {узел: массив}
def vyborka(vse, T, gen):
    dlina = len(next(iter(vse.values())))
    nomera = gen.choice(dlina, size=T, replace=False)
    return {u: v[nomera] for u, v in vse.items()}


# etalon: ответы эталона (1, 0, −1 — «не сравнивать») по способу; (ответы выходов, прогонов)
def etalon(sh, zn, neizv, sposob):
    s, vy = sh['схема'], sh['выходы']
    rez = px.tochno(s, zn, vy, [neizv])
    if sposob.startswith('1'):
        rez = (px.progon(s, zn, vy, 'бит', {u: 0 for u in neizv}), 1)
    if sposob.startswith('2'):
        rez = px.nash(s, zn, vy, [neizv], 'провода')
    if sposob.startswith('3'):
        rez = px.nash(s, zn, vy, [neizv], 'трит')
    return rez


# na_dele: настоящие входы чипа: неизвестные входы на деле — случайные биты
def na_dele(zn, neizv, gen):
    rez = dict(zn)
    for u in neizv:
        rez[u] = gen.integers(0, 2, len(zn[u]))
    return rez


# povedenie_bity: что выдаёт сломанный вентиль на каждом наборе
def povedenie_bity(povedenie, dlina, gen):
    bity = gen.integers(0, 2, dlina)
    if povedenie == 'залип':
        bity = np.full(dlina, gen.integers(0, 2))
    return bity


# vyhod_chipa: выходы чипа на наборах: исправного (g = None) или со сломанным вентилем g
def vyhod_chipa(sh, zn, g, povedenie, gen):
    rez = px.progon(sh['схема'], zn, sh['выходы'], 'бит', {})
    if g is not None:
        rez = px.progon_s_massivom(sh, zn, g, povedenie_bity(povedenie, len(next(iter(zn.values()))), gen))
    return rez


# prohodit: чип проходит проверку: где эталон уверен, выход совпал
def prohodit(et, vyh):
    return all(np.all((e < 0) | (e == v)) for e, v in zip(et, vyh))


# vred: доля всех наборов, где чип со сломанным g даёт неверный ответ (входы известны — так у покупателя)
def vred(sh, vse, g, povedenie, gen):
    hor = vyhod_chipa(sh, vse, None, povedenie, gen)
    plo = vyhod_chipa(sh, vse, g, povedenie, gen)
    raznyh = np.any(np.array(hor) != np.array(plo), axis=0)
    return float(np.mean(raznyh))


# uchest: записать один дефектный и один исправный чип в счёт способа
def uchest(m, et, chip, hor, vr):
    proshel = prohodit(et, chip)
    m['брак'] += 1
    m['брак прошёл'] += proshel
    m['вред'] += vr * proshel
    m['годных'] += 1
    m['выброшено'] += not prohodit(et, hor)
    return m


# novyj_schet: пустой счёт способа
def novyj_schet(progony):
    return {'брак': 0, 'брак прошёл': 0, 'вред': 0.0, 'годных': 0, 'выброшено': 0, 'прогонов': progony}


# zavod: одна партия на одном наборе проверок: все дефекты (вентиль × поведение) и столько же исправных
def zavod(sh, vse, T, neizv, vredy, gen, itog):
    zn = vyborka(vse, T, gen)
    etalony = {sp: etalon(sh, zn, neizv, sp) for sp in SPOSOBY}
    for (g, pov), vr in vredy.items():
        chip = vyhod_chipa(sh, na_dele(zn, neizv, gen), g, pov, gen)
        hor = vyhod_chipa(sh, na_dele(zn, neizv, gen), None, pov, gen)
        for sp, (et, progony) in etalony.items():
            uchest(itog.setdefault(sp, novyj_schet(progony)), et, chip, hor, vr)
    return itog


# vredy_defektov: вред каждого дефекта; невидимые (вред 0) — не брак
def vredy_defektov(sh, vse, gen):
    vse_vredy = {(g, pov): vred(sh, vse, g, pov, gen) for g in px.ventili(sh) for pov in POVEDENIYA}
    return {k: v for k, v in vse_vredy.items() if v > 0}


# opyt: все партии: по способам — доли пропущенного брака, выброшенных годных, вред
def opyt(sh, T, neizv, semya=2411):
    gen = np.random.default_rng(semya)
    vse = px.vse_nabory(sh['входы'])
    vredy = vredy_defektov(sh, vse, gen)
    itog = {}
    for _ in range(POVTOROV):
        zavod(sh, vse, T, neizv, vredy, gen, itog)
    return itog


# pechat_opyta: строки таблицы одного опыта
def pechat_opyta(sh, T, neizv, nazvanie):
    itog = opyt(sh, T, neizv)
    print(f'  {nazvanie}, проверка T = {T} наборов:')
    for sp, m in itog.items():
        vred_sr = '   —  '
        if m['брак прошёл'] > 0:
            vred_sr = f"{m['вред'] / m['брак прошёл'] * 100:5.1f} %"
        print(f'    {sp:22} брак прошёл {m["брак прошёл"]:5} из {m["брак"]} ({m["брак прошёл"] / m["брак"] * 100:5.1f} %) | '
              f'годных выброшено {m["выброшено"]:5} из {m["годных"]} ({m["выброшено"] / m["годных"] * 100:5.1f} %) | '
              f'вред прошедшего: неверных ответов {vred_sr} | прогонов эталона {m["прогонов"]}')
    return itog


# pechat_shemy: опыты одной схемы: без X, X во входе b0, X во всём слове b; две длины проверки
def pechat_shemy(sh, dliny):
    b = sh['входы'][1]
    print(f'\n{sh["имя"]}: вентилей {len(px.ventili(sh))}, наборов {len(next(iter(px.vse_nabory(sh["входы"]).values())))}')
    for T in dliny:
        pechat_opyta(sh, T, [], 'без неизвестного')
        pechat_opyta(sh, T, [b[0]], 'неизвестен вход b0')
        pechat_opyta(sh, T, list(b), f'неизвестно слово b ({len(b)} бит)')
    return None


# pechat_perebora: сколько прогонов эталона нужно перебору при k неизвестных
def pechat_perebora():
    print('\nПЕРЕБОР: прогонов эталона при k неизвестных — 2^k; наша логика — 1')
    for k in (1, 4, 10, 20, 40, 100):
        print(f'  k = {k:3}: 2^k = {2 ** k:.3g}')
    return None


# glavnoe: умножитель 4×4 и строка слоя; рост перебора
def glavnoe():
    pechat_shemy(px.shema_umnozhitelya(4), (8, 32))
    pechat_shemy(px.shema_stroki(3), (16, 64))
    pechat_perebora()
    return None


if __name__ == '__main__':
    glavnoe()
