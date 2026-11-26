#!/usr/bin/env python3
# derevo.py — дерево задач, шаг 2: факты derevo.pl → derevo.json, у каждого узла трит «проверено».
# Правится только derevo.pl; JSON собирается отсюда и руками не правится (листок Е.8 № 28).
# Запуск из корня ii-komanda:
#   gh repo list Scatik146 --json name,pushedAt,isArchived --limit 200 > /tmp/repos.json
#   python3 -I komanda/derevo/derevo.py /tmp/repos.json [komanda/derevo/derevo.pl]
# Сам в сеть не ходит; пишет только derevo.json (№ 23).
# Код выхода — итог по дереву встроенным min: 0 — да, 1 — нет, 2 — не знаю (или нет входа).
import datetime
import json
import os
import re
import sys

sys.path.insert(0, 'yadro-trit')
import trit  # noqa: E402

# === Данные ===
DA, NOL, NET = trit.ДА, trit.НЕ_ЗНАЮ, trit.НЕТ
FAKTY = 'komanda/derevo/derevo.pl'
VYHOD = 'komanda/derevo/derevo.json'
VLADELEC = 'Scatik146'
SVEZHIJ = 14   # дней: пуш свежее — у замороженного это спор (№ 9)
STARYJ = 60    # дней: пуша нет дольше — у живого это «устарело?» (№ 37)
ZHIV = {'работает_у_нас': DA, 'в_работе': DA, 'заморожено': NET, 'завершено': NET, 'идея': NOL}
ARITY = {'статус': 1, 'узел': 3, 'название': 2, 'остановились': 2, 'не_закрыто': 2,
         'источник': 2, 'пометка': 2, 'опирается': 2}
SPISKI = {'не_закрыто': 'ne_zakryto', 'пометка': 'pometki', 'опирается': 'opiraetsya'}
ODNO = {'название': 'nazvanie', 'остановились': 'ostanovilis'}
ARG_RE = re.compile(r"\s*(?:'((?:[^']|'')*)'|(\w+)\('((?:[^']|'')*)'\)|(\w+))\s*")
MUTANTY = ('есть_ли', 'согласие')
PO_IMENI = {imya: t for t, imya in trit.ИМЕНА.items()}
# образец узла в JSON:
# {'id': 'ii_py', 'roditel': 'ii_komanda', 'status': 'заморожено', 'nazvanie': '…', 'ostanovilis': '…',
#  'ne_zakryto': ['…'], 'istochniki': [{'vid': 'github', 'put': 'Scatik146/…'}], 'pometki': [],
#  'opiraetsya': ['…'], 'provereno': {'trit': 'не_знаю', 'pochemu': ['№ 46: …']}}


# === 1. Чтение фактов ===
# chitat: текст файла; нет файла — пустая строка
def chitat(put):
    tekst = ''
    if put and os.path.isfile(put):
        with open(put, encoding='utf-8') as f:
            tekst = f.read()
    return tekst


# znachenie: аргумент из совпадения — текст в кавычках, источник (вид, путь) или атом
def znachenie(m):
    z = m.group(4)
    if m.group(1) is not None:
        z = m.group(1).replace("''", "'")
    elif m.group(2):
        z = (m.group(2), m.group(3).replace("''", "'"))
    return z


# argumenty: аргументы от poz до «)» в конце строки; разбор не удался — None
def argumenty(stroka, poz):
    spisok, celyj, m = [], False, ARG_RE.match(stroka, poz)
    while m is not None:
        spisok.append(znachenie(m))
        konec, poz = stroka[m.end():m.end() + 1], m.end() + 1
        m = ARG_RE.match(stroka, poz) if konec == ',' else None
        celyj = konec == ')' and poz == len(stroka)
    return spisok if celyj else None


# pustaya: строка без факта — пустая, комментарий или директива
def pustaya(stroka):
    s = stroka.strip()
    return s == '' or s.startswith('%') or s.startswith(':-')


# fakt: строка → (имя, аргументы); не факт схемы — None
def fakt(stroka):
    otvet = None
    m = re.match(r'\s*(\w+)\(', stroka)
    hvost = re.search(r"\)\.\s*(%[^']*)?$", stroka)
    if m and hvost and m.group(1) in ARITY:
        args = argumenty(stroka[:hvost.start() + 1], m.end())
        otvet = (m.group(1), args) if args and len(args) == ARITY[m.group(1)] else None
    return otvet


# fakty: текст derevo.pl → список фактов и номера строк, которые не разобраны
def fakty(tekst):
    spisok, plohie = [], []
    for nomer, stroka in enumerate(tekst.split('\n'), 1):
        f = None if pustaya(stroka) else fakt(stroka)
        if f:
            spisok.append(f)
        elif not pustaya(stroka):
            plohie.append(nomer)
    return spisok, plohie


# === 2. Узлы ===
# pustoj_uzel: узел без свойств — из факта узел/3
def pustoj_uzel(args):
    return {'id': args[0], 'roditel': args[1], 'status': args[2], 'nazvanie': '', 'ostanovilis': '',
            'ne_zakryto': [], 'istochniki': [], 'pometki': [], 'opiraetsya': []}


# svojstvo: положить одно свойство в узел
def svojstvo(uzel, imya, znach):
    if imya in SPISKI:
        uzel[SPISKI[imya]].append(znach)
    elif imya in ODNO:
        uzel[ODNO[imya]] = znach
    else:
        uzel['istochniki'].append({'vid': znach[0], 'put': znach[1]})


# uzly: факты → узлы по порядку и свойства без узла (ошибка входа)
def uzly(spisok):
    vse = {a[0]: pustoj_uzel(a) for i, a in spisok if i == 'узел'}
    bez_uzla = []
    for imya, a in spisok:
        if imya in ('узел', 'статус'):
            continue
        if a[0] in vse:
            svojstvo(vse[a[0]], imya, a[1])
        else:
            bez_uzla.append(imya + '(' + a[0] + ')')
    return vse, bez_uzla


# === 3. Репозитории ===
# zapis_repo: запись gh (name, pushedAt, isArchived) или REST (pushed_at, archived) → (имя, дата, архив)
def zapis_repo(r):
    kogda = r.get('pushedAt') or r.get('pushed_at') or ''
    data = datetime.date.fromisoformat(kogda[:10]) if kogda else None
    return r['name'], {'data': data, 'arhiv': bool(r.get('isArchived') or r.get('archived'))}


# spisok_repo: разобранный текст — список записей с именем; иначе None
def spisok_repo(tekst):
    try:
        dannye = json.loads(tekst)
    except ValueError:
        dannye = None
    celyj = isinstance(dannye, list) and all(isinstance(r, dict) and 'name' in r for r in dannye)
    return dannye if celyj else None


# repozitorii: текст списка репозиториев → имя → запись; нет или испорчен — None («не знаю», № 5)
def repozitorii(tekst):
    dannye = spisok_repo(tekst)
    otvet = None if dannye is None else dict(zapis_repo(r) for r in dannye)
    return otvet


# === 4. Трит «проверено» ===
# zhiv_repo: живёт ли репозиторий — мерка зависит от того, что говорит статус
def zhiv_repo(status, zapis, segodnya):
    dnej = (segodnya - zapis['data']).days if zapis['data'] else 10 ** 6
    porog = STARYJ if ZHIV[status] == DA else SVEZHIJ - 1
    otvet = DA if dnej <= porog and not zapis['arhiv'] else NET
    return otvet


# soglasno: согласие(статус, жизнь репозитория) — разное даёт 0, одинаковое — «да»
def soglasno(status, zapis, segodnya):
    s = trit.согласие(ZHIV[status], zhiv_repo(status, zapis, segodnya))
    return DA if s != NOL else NOL


# prichina_spora: почему статус и репозиторий не согласны
def prichina_spora(status, zapis, segodnya):
    dnej = (segodnya - zapis['data']).days if zapis['data'] else '?'
    otvet = '№ 9: статус «{}», а пуш {} дн. назад'.format(status, dnej)
    if ZHIV[status] == DA:
        otvet = '№ 37: статус «{}», а пушей нет {} дн.{}'.format(status, dnej, ' (архив)' if zapis['arhiv'] else '')
    if ZHIV[status] == NOL:
        otvet = '№ 46: статус «{}» — с репозиторием не сверяется'.format(status)
    return otvet


# est_li: есть ли репозиторий — есть_ли(нашёл, полный); «нет» только по полному списку (№ 4)
def est_li(put, repo):
    chasti = put.split('/')
    polnyj = DA if len(chasti) == 2 and chasti[0] == VLADELEC else NOL
    najden = DA if len(chasti) >= 2 and chasti[1] in repo and polnyj == DA else NET
    return trit.есть_ли(najden, polnyj)


# github: один источник GitHub → (трит, причина)
def github(uzel, put, repo, segodnya):
    t = est_li(put, repo)
    otvet = (t, '№ 5: {} — путь не сверяю, сверяю только репозиторий {}'.format(put, VLADELEC))
    if t == NET:
        otvet = (NET, '№ 4: {} нет в полном списке репозиториев'.format(put))
    if t == DA:
        zapis = repo.get(put.split('/')[1], {'data': None, 'arhiv': False})
        s = soglasno(uzel['status'], zapis, segodnya)
        otvet = (s, '№ 15: {} есть, статус согласен'.format(put) if s == DA else prichina_spora(uzel['status'], zapis, segodnya))
    return otvet


# istochnik: один источник → (трит, причина)
def istochnik(uzel, ist, repo, segodnya):
    otvet = (NOL, '№ 5: {} — не сверяю'.format(ist['vid']))
    if repo is None:
        otvet = (NOL, '№ 5: нет списка репозиториев')
    elif ist['vid'] == 'github':
        otvet = github(uzel, ist['put'], repo, segodnya)
    return otvet


# provereno: трит узла — встроенным min по источникам; без источника — «не знаю» (№ 46)
def provereno(uzel, repo, segodnya):
    itogi = [istochnik(uzel, i, repo, segodnya) for i in uzel['istochniki']]
    itogi = itogi or [(NOL, '№ 46: нет своего источника')]
    return {'trit': trit.ИМЕНА[min(t for t, _ in itogi)], 'pochemu': [p for _, p in itogi]}


# === 5. Сборка JSON ===
# sobrat: всё дерево — узлы с тритом и итог встроенным min
def sobrat(vse, statusy, repo, segodnya):
    for u in vse.values():
        u['provereno'] = provereno(u, repo, segodnya)
    trity = [PO_IMENI[u['provereno']['trit']] for u in vse.values()]
    return {'sobrano': segodnya.isoformat(), 'iz': FAKTY, 'ne_pravit': True,
            'statusy': statusy, 'uzly': list(vse.values()), 'itog': trit.ИМЕНА[min(trity or [NOL])]}


# derevo: текст фактов и список репозиториев → (JSON-словарь или None, ошибки входа)
def derevo(tekst, repo, segodnya):
    spisok, plohie = fakty(tekst)
    vse, bez_uzla = uzly(spisok)
    oshibki = ['строка {}: не факт схемы'.format(n) for n in plohie] + ['нет узла: ' + b for b in bez_uzla]
    statusy = [a[0] for i, a in spisok if i == 'статус']
    otvet = None if oshibki or not vse else sobrat(vse, statusy, repo, segodnya)
    return otvet, oshibki


# === 6. Самопроверка: пример и контрпример ===
PRIMER_PL = """:- encoding(utf8).
статус(работает_у_нас).
узел(a, корень, работает_у_нас).
название(a, 'Живой: it''s ok').
источник(a, github('Scatik146/zhivoj')).    % есть, пуш свежий
узел(b, a, в_работе).
источник(b, github('Scatik146/net-takogo')).
узел(c, a, заморожено).
источник(c, github('Scatik146/zhivoj')).
узел(d, a, идея).
узел(e, a, работает_у_нас).
источник(e, sourcecraft('e')).
узел(f, a, в_работе).
источник(f, github('Scatik146/staryj')).
"""
PRIMER_REPO = '[{"name": "zhivoj", "pushedAt": "2026-11-20T10:00:00Z", "isArchived": false},' \
              ' {"name": "staryj", "pushed_at": "2026-01-01T00:00:00Z", "archived": false}]'
DEN = datetime.date(2026, 11, 26)
OZHIDAEM = {'a': DA, 'b': NET, 'c': NOL, 'd': NOL, 'e': NOL, 'f': NOL}


# primery: пары (ожидали, получили) — пример и контрпримеры
def primery():
    d, osh = derevo(PRIMER_PL, repozitorii(PRIMER_REPO), DEN)
    poluchili = {u['id']: PO_IMENI[u['provereno']['trit']] for u in d['uzly']} if d else {}
    pary = [(t, poluchili.get(i)) for i, t in OZHIDAEM.items()]
    pary.append(("Живой: it's ok", d['uzly'][0]['nazvanie'] if d else None))
    pary.append((['строка 2: не факт схемы'], derevo(PRIMER_PL.replace('статус(работает_у_нас).', 'узел(x, y).'), {}, DEN)[1]))
    pary.append((['нет узла: название(z)'], derevo(PRIMER_PL + "название(z, 'нет').\n", {}, DEN)[1]))
    pary.append((NOL, PO_IMENI[derevo(PRIMER_PL, None, DEN)[0]['itog']]))
    pary.append((None, repozitorii('{"message": "403"}')))
    return pary


# samoproverka: да — каждая пара совпала; итог — встроенным min
def samoproverka():
    return min(DA if ozhid == poluchili else NET for ozhid, poluchili in primery())


# proba_mutanta: испортить слово ядра (всегда «да») — самопроверка обязана сказать «нет»; слово вернуть
def proba_mutanta(slovo):
    celoe = getattr(trit, slovo)
    setattr(trit, slovo, lambda *a: DA)
    itog = samoproverka()
    setattr(trit, slovo, celoe)
    return DA if itog != DA else NET


# === 7. Главное ===
# schet: «да N, не знаю N, нет N» по узлам
def schet(d):
    imena = [u['provereno']['trit'] for u in d['uzly']]
    return ', '.join('{} {}'.format(trit.ИМЕНА[t], imena.count(trit.ИМЕНА[t])) for t in (DA, NOL, NET))


# zapisat: JSON в файл — по узлу на блок, русские буквы как есть
def zapisat(d, put):
    with open(put, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
        f.write('\n')


# svodka: короткая сводка в чат — самопроверка, счёт, узлы «нет»
def svodka(sam, d, put):
    s = ['самопроверка и мутанты: ' + trit.ИМЕНА[sam], 'узлов {}: {}; итог: {}'.format(len(d['uzly']), schet(d), d['itog'])]
    s += ['нет — {}: {}'.format(u['id'], '; '.join(u['provereno']['pochemu'])) for u in d['uzly'] if u['provereno']['trit'] == 'нет']
    s += ['записано: ' + put]
    return '\n'.join(s)


# kod_vyhoda: трит → 0 (да), 1 (нет), 2 (не знаю)
def kod_vyhoda(t):
    return {DA: 0, NET: 1, NOL: 2}[t]


# glavnoe: самопроверка → дерево → JSON → сводка; ошибки входа — «не знаю» (2) без записи
def glavnoe(argv):
    sam = min([samoproverka()] + [proba_mutanta(s) for s in MUTANTY])
    repo = repozitorii(chitat(argv[1] if len(argv) > 1 else ''))
    d, oshibki = derevo(chitat(argv[2] if len(argv) > 2 else FAKTY), repo, datetime.date.today())
    kod = 2
    if d and sam == DA:
        zapisat(d, VYHOD)
        print(svodka(sam, d, VYHOD))
        kod = kod_vyhoda(PO_IMENI[d['itog']])
    else:
        print('самопроверка: {}; не знаю: {}'.format(trit.ИМЕНА[sam], '; '.join(oshibki) or 'нет входа'))
    kod = 1 if sam != DA else kod
    return kod


if __name__ == '__main__':
    sys.exit(glavnoe(sys.argv))
