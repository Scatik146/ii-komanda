#!/usr/bin/env python3
# revizor.py — ревизор навыков и памяти Claude на троичном ядре yadro-trit (этап 4).
# Ничего не удаляет и не меняет: читает копии и пишет отчёт komanda/revizor/otchet-<дата>.md.
# Запуск из корня ii-komanda: python3 -I tools/revizor.py [клон memory_maryam_ai] [папка установленных навыков]
# Код выхода: 0 — да (самопроверка и пробы-мутанты прошли), 1 — нет, 2 — не знаю (нет входа).
# Итог самопроверки — встроенным min, а не словом ядра: проверяемое не судит само себя (урок 25.11).
import datetime
import glob
import json
import os
import re
import sys

sys.path.insert(0, 'yadro-trit')
import trit  # noqa: E402

# === Данные ===
DA, NOL, NET = trit.ДА, trit.НЕ_ЗНАЮ, trit.НЕТ
VIDIMOST = 'komanda/revizor/vidimost.json'
OTCHET = 'komanda/revizor/otchet-{}.md'
NAVYKI_SESSII = '/root/.claude/skills/synced/*'
PUT_RE = re.compile(r'[\w.\-]+(?:/[\w.\-]+)+\.(?:md|py|cjs|mjs|js|json|pl|html|sh|ps1|bat|txt|css)\b')
ZAGLUSHKI = ('NNN', 'XXX', 'имя', 'дата')
CHUZHIE = ('teacher-workpad', 'drakon-graf', 'zhivoj-konspekt', 'komi-perm', 'info10')
MARKERY = ('пока', 'сейчас', 'дальше', 'скоро', 'possibly', 'currently', 'not yet', 'will likely', 'thinking of', 'for now')
VERSIYA_RE = re.compile(r'\bv(\d+)\.(\d+)(?:-([А-ЯA-Z]))?')
SROK_RE = re.compile(r'(?:до|before)\s*≈?\s*(\d{1,2})\.(\d{1,2})(?:\.(\d{4}))?')
SROK_EN_RE = re.compile(r'before\s+(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+(\d{4})')
MESYACY = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
GRUPPY = {'запись': r'^(?:за|до|пере|на)?пис|^(?:за|до|пере|на)?пиш|^обнов|^правит|^поправ|^меня|^измен',
          'удаление': r'^удал|^убра|^стере',
          'чтение': r'^(?:про|пере)?чит|^откры'}
OTRICANIE = ('не', 'нельзя', 'без', 'никогда')
OKONCHANIYA = ('ть', 'ти', 'ут', 'ют', 'ат', 'ят', 'ет', 'ит')
CITATA_RE = re.compile(r'«[^»]*»|"[^"]*"')
MUTANTY = ('есть_ли', 'согласие', 'основание', 'или_всех', 'и', 'или')


# === 1. Чтение входа ===
# chitat: текст файла; нет файла — пустая строка
def chitat(put):
    tekst = ''
    if put and os.path.isfile(put):
        with open(put, encoding='utf-8', errors='replace') as f:
            tekst = f.read()
    return tekst


# istochnik: запись об источнике — вид, имя, путь, текст
def istochnik(vid, imya, put):
    return {'vid': vid, 'imya': imya, 'put': put, 'tekst': chitat(put)}


# shapka: поля шапки «---» (name, description, aliases)
def shapka(tekst):
    m = re.match(r'---\n(.*?)\n---', tekst, re.S)
    blok = m.group(1).split('\n') if m else []
    pary = [s.partition(':') for s in blok]
    return {k.strip(): v.strip().strip('"') for k, _, v in pary}


# ustanovlennye: установленные навыки сессии — имя → путь SKILL.md
def ustanovlennye(papka):
    puti = sorted(glob.glob(os.path.join(papka, '*', 'SKILL.md')))
    return {os.path.basename(os.path.dirname(p)): p for p in puti}


# komandnye: имена навыков команды — есть копия в rezerv/navyki или в memory_maryam_ai/navyki
def komandnye(mem):
    imena = {os.path.basename(p) for p in glob.glob('rezerv/navyki/*')}
    imena |= {os.path.basename(p) for p in glob.glob(os.path.join(mem, 'navyki', '*'))}
    return imena


# fajly_pamyati: файлы копии памяти в папке — пути .md, кроме служебных
def fajly_pamyati(mem, papka, vid):
    puti = glob.glob(os.path.join(mem, 'pamyat', papka, '**', '*.md'), recursive=True)
    return sorted(p for p in puti if os.path.basename(p) not in vid['ne_pamyat'])


# sobrat_istochniki: навыки команды (установленные), память (общая и проекта), копии CLAUDE.md
def sobrat_istochniki(mem, ust, vid):
    komanda = komandnye(mem)
    spisok = [istochnik('навык', n, p) for n, p in sorted(ust.items()) if n in komanda]
    for papka in vid['papki_pamyati']:
        spisok += [istochnik('память', os.path.relpath(p, mem), p) for p in fajly_pamyati(mem, papka, vid)]
    spisok += [istochnik('правила', os.path.basename(p), p) for p in sorted(glob.glob('pravila/проекты/*.md'))]
    return spisok


# stroki: строки источника с номерами — (источник, номер, строка)
def stroki(ist):
    return [(ist, n, s) for n, s in enumerate(ist['tekst'].split('\n'), 1)]


# vse_stroki: строки всех источников подряд
def vse_stroki(spisok):
    return [x for ist in spisok for x in stroki(ist)]


# mesto: «источник:строка» для отчёта
def mesto(ist, n):
    return '{}:{}'.format(ist['imya'], n)


# nahodka: запись отчёта — что, где, байт, трит, предложение
def nahodka(chto, gde, bajt, t, pred):
    return {'chto': chto, 'gde': gde, 'bajt': bajt, 'trit': t, 'pred': pred}


# === 2. Проверка 1: мёртвые ссылки ===
# norm_put: путь без приставки нашего репозитория (ii-komanda/, memory_maryam_ai/)
def norm_put(put):
    return re.sub(r'^(?:Scatik146/)?(?:ii-komanda|memory_maryam_ai)/', '', put)


# najden: трит — нашёлся ли путь хоть в одном корне: ii-komanda, клон памяти, папка источника
def najden(put, ist, mem):
    korni = ['.', mem, os.path.dirname(ist['put'])]
    est = any(os.path.exists(os.path.join(k, put)) for k in korni)
    return DA if est else NET


# polnyj: трит — полон ли список: путь явно наш или строка называет только наш репозиторий (не приставкой пути)
def polnyj(put, s):
    yavnyj = norm_put(put) != put
    nash = re.search(r'(?:ii-komanda|memory_maryam_ai)(?!/)', s) is not None and not any(c in s for c in CHUZHIE)
    return DA if yavnyj or nash else NET


# ssylka: одна ссылка — есть_ли(нашёл, полный): «нет» только при полном списке
def ssylka(ist, n, s, put, mem):
    t = trit.есть_ли(najden(norm_put(put), ist, mem), polnyj(put, s))
    pred = {NET: 'исправить путь или убрать ссылку', NOL: 'проверить в своём репозитории (здесь не подключён)'}
    return nahodka(put, mesto(ist, n), len(s.encode()), t, pred.get(t, ''))


# puti_stroki: пути в строке, кроме заглушек вида NNN, <имя>
def puti_stroki(s):
    return [p for p in PUT_RE.findall(s) if not any(z in p for z in ZAGLUSHKI)]


# ssylki: проверка 1 — ссылки, у которых трит не «да»
def ssylki(spisok, mem):
    vse = [ssylka(ist, n, s, p, mem) for ist, n, s in vse_stroki(spisok) for p in puti_stroki(s)]
    return [x for x in vse if x['trit'] != DA]


# === 3. Проверка 2: повторы ===
# norm_stroka: строка без разметки и пометок — для сравнения
def norm_stroka(s):
    t = re.sub(r'\[stated\]|\[observed\]|\[inferred\]|[`*_>#|]', ' ', s.lower())
    return ' '.join(re.findall(r'\w+', t))


# kand: кандидат повтора — (источник, номер, строка, норма, слова длиннее трёх букв)
def kand(ist, n, s):
    t = norm_stroka(s)
    return (ist, n, s, t, {w for w in t.split() if len(w) > 3})


# shodstvo: трит повтора — одинаково — да; похоже (Жаккар ≥ 0.75, общих слов ≥ 6) — не знаю; иначе — нет
def shodstvo(a, b):
    obshchie = len(a[4] & b[4])
    t = NET
    if obshchie >= 6 and obshchie / len(a[4] | b[4]) >= 0.75:
        t = NOL
    if a[3] == b[3]:
        t = DA
    return t


# ne_tochno: причина, по которой источник «не знаю» (открытый навык, не виден из проекта); нет — пусто
def ne_tochno(ist, vid):
    prichiny = [v for k, v in vid['ne_tochno'].items() if ist['put'].endswith(k)]
    return '; '.join(prichiny)


# povtor: запись о повторе; у ненадёжного источника трит — основание(t, нет) = не знаю
def povtor(a, b, t, vid):
    prichina = (ne_tochno(a[0], vid) + ' ' + ne_tochno(b[0], vid)).strip()
    t = trit.основание(t, NET if prichina else DA)
    pred = 'оставить в одном месте, в другом — ссылку' if t == DA else 'показать учителю: ' + (prichina or 'похоже, сверить')
    return nahodka(a[2].strip()[:120], mesto(a[0], a[1]) + ' = ' + mesto(b[0], b[1]), len(b[2].encode()), t, pred)


# povtory: проверка 2 — повтор строк (от 40 знаков) между разными файлами
def povtory(spisok, vid):
    k = [kand(i, n, s) for i, n, s in vse_stroki(spisok)]
    k = [x for x in k if len(x[3]) >= 40]
    pary = ((a, b) for j, a in enumerate(k) for b in k[j + 1:] if a[0]['put'] != b[0]['put'])
    ocenki = ((a, b, shodstvo(a, b)) for a, b in pary)
    return [povtor(a, b, t, vid) for a, b, t in ocenki if t != NET]


# === 4. Проверка 3: противоречия ===
# gruppa: группа действия по корню глагола (неопределённая форма и «пишут», «обновляет»)
def gruppa(w):
    naideno = ''
    for imya, koren in GRUPPY.items():
        if w.endswith(OKONCHANIYA) and re.search(koren, w):
            naideno = imya
    return naideno


# znaki: {группа действия: множество знаков} — «не писать» даёт нет, «обновить» — да
def znaki(s):
    slova_s = re.findall(r'[а-яё]+', s.lower())
    zn = {}
    for i, w in enumerate(slova_s):
        if gruppa(w):
            zn.setdefault(gruppa(w), set()).add(NET if i > 0 and slova_s[i - 1] in OTRICANIE else DA)
    return zn


# polyarnosti: {группа: знак}; оба знака в одной строке — оговорка («обновить, но в брифинге не писать»), группа не берётся
def polyarnosti(s):
    return {g: min(z) for g, z in znaki(s).items() if len(z) == 1}


# obekty: предметы строки — пути и латинские заглавные слова (SOSTOYANIE)
def obekty(s):
    return set(PUT_RE.findall(s)) | set(re.findall(r'\b[A-Z][A-Z_\-]{4,}\b', s))


# protivorechie: по каждому общему действию — согласие ядра; «не знаю» — кандидат для учителя
def protivorechie(a, b):
    predmet = ', '.join(sorted(a[3] & b[3]))
    obshchie = sorted(set(a[4]) & set(b[4]))
    spornye = [g for g in obshchie if trit.согласие(a[4][g], b[4][g]) == NOL]
    gde = mesto(a[0], a[1]) + ' / ' + mesto(b[0], b[1])
    return [nahodka(predmet + ': ' + g, gde, len(a[2].encode()) + len(b[2].encode()), NOL, 'показать учителю: что верно') for g in spornye]


# protivorechiya: проверка 3 — один предмет, одно действие, разные знаки в разных файлах
def protivorechiya(spisok):
    k = [(i, n, s, obekty(s), polyarnosti(s)) for i, n, s in vse_stroki(spisok)]
    k = [x for x in k if x[3] and x[4]]
    pary = [(a, b) for j, a in enumerate(k) for b in k[j + 1:] if a[0]['put'] != b[0]['put'] and a[3] & b[3]]
    return [x for a, b in pary for x in protivorechie(a, b)]


# === 5. Проверка 4: устаревшее ===
# data_ili_segodnya: дата из чисел; неверная дата — сегодня (прошедшей не считается)
def data_ili_segodnya(d, m, g, segodnya):
    data = segodnya
    try:
        data = datetime.date(int(g or segodnya.year), int(m), int(d))
    except ValueError:
        data = segodnya
    return data


# sroki: даты сроков в строке — «до дд.мм[.гггг]» и «before 23 Dec 2026»
def sroki(s, segodnya):
    ru = [data_ili_segodnya(d, m, g, segodnya) for d, m, g in SROK_RE.findall(s)]
    en = [data_ili_segodnya(d, MESYACY.index(m) + 1, g, segodnya) for d, m, g in SROK_EN_RE.findall(s)]
    return ru + en


# srok_proshel: трит — срок в строке уже прошёл; срока нет — нет
def srok_proshel(s, segodnya):
    proshel = any(d < segodnya for d in sroki(s, segodnya))
    return DA if proshel else NET


# marker: трит — вне цитат в строке «пока», «сейчас», «possibly» и т. п.: может устареть — не знаю
def marker(s):
    niz = CITATA_RE.sub(' ', s.lower())
    est = not s.lstrip().startswith('>') and any(re.search(r'(?<!\w)' + re.escape(m) + r'(?!\w)', niz) for m in MARKERY)
    return NOL if est else NET


# versii_zhurnala: последняя версия по старшему номеру — из журнала komanda/README.md, по порядку строк
def versii_zhurnala():
    poslednyaya = {}
    for v in VERSIYA_RE.findall(chitat('komanda/README.md')):
        poslednyaya[v[0]] = v
    return poslednyaya


# sravnit_versiyu: да — в журнале позже другая версия того же номера; нет — та же; журнал молчит — не знаю
def sravnit_versiyu(v, p):
    t = NOL
    if p is not None:
        t = NET if p == v else DA
    return t


# versiya: трит строки по версиям: хоть одна старше журнала — да
def versiya(s, posl):
    ocenki = [sravnit_versiyu(v, posl.get(v[0])) for v in VERSIYA_RE.findall(s)]
    return trit.или_всех(ocenki)


# ustarelo_stroka: трит строки — большее из: срок прошёл, версия старше, слово-маркер
def ustarelo_stroka(s, segodnya, posl):
    return trit.или_всех([srok_proshel(s, segodnya), versiya(s, posl), marker(s)])


# ustareloe: проверка 4 — устаревшее; да — устарело, не знаю — проверить
def ustareloe(spisok, segodnya):
    posl = versii_zhurnala()
    vse = [(i, n, s, ustarelo_stroka(s, segodnya, posl)) for i, n, s in vse_stroki(spisok)]
    pred = {DA: 'убрать или обновить', NOL: 'проверить: ещё верно?'}
    return [nahodka(s.strip()[:120], mesto(i, n), len(s.encode()), t, pred[t]) for i, n, s, t in vse if t != NET]


# === 6. Проверка 5: копии навыков ===
# zapis_kopii: сверка одной копии с установленным навыком; установленного нет — не знаю
def zapis_kopii(n, p, ust_t):
    kopiya = chitat(p)
    t = NOL
    if ust_t is not None:
        t = NET if kopiya == ust_t else DA
    pred = {DA: 'сверить, что новее: копия или установленный', NOL: 'навык не установлен в этой сессии'}
    return nahodka(n, p, len(kopiya.encode()) - len((ust_t or '').encode()), t, pred.get(t, 'совпадает'))


# sverka_navyka: по каждой копии навыка (rezerv/navyki, memory_maryam_ai/navyki) — запись сверки
def sverka_navyka(n, put_ust, mem):
    ust_t = chitat(put_ust) if put_ust else None
    puti = ['rezerv/navyki/{}/SKILL.md'.format(n), os.path.join(mem, 'navyki', n, 'SKILL.md')]
    return [zapis_kopii(n, p, ust_t) for p in puti if os.path.isfile(p)]


# kopii: проверка 5 — все копии навыков команды
def kopii(ust, mem):
    return [x for n in sorted(komandnye(mem)) for x in sverka_navyka(n, ust.get(n), mem)]


# === 7. Проверка 6: вес ===
# opisanie_navyka: байты строки списка навыков — имя и описание из шапки
def opisanie_navyka(put):
    p = shapka(chitat(put))
    return len((p.get('name', '') + ': ' + p.get('description', '')).encode())


# opisanie_pamyati: байты строки списка памяти — путь, псевдонимы, описание
def opisanie_pamyati(put_v_pamyati, tekst):
    p = shapka(tekst)
    stroka = '{} [aliases: {}] — {}'.format(put_v_pamyati, p.get('aliases', ''), p.get('description', ''))
    return len(stroka.encode())


# spisok_pamyati: файл копии → путь в живой памяти; общая — по vidimost.json, проект — с приставкой проекта
def spisok_pamyati(vid, mem):
    puti = dict(vid['obshchaya_vidna'])
    koren = os.path.join(mem, 'pamyat', vid['papka_proekta'])
    for p in fajly_pamyati(mem, vid['papka_proekta'], vid):
        puti[os.path.relpath(p, os.path.join(mem, 'pamyat'))] = vid['pristavka_proekta'] + os.path.relpath(p, koren)
    return puti


# ves_kazhdyj: что читается на каждом запросе — описания навыков, строки списка памяти, вставки, карточка ОЧ
def ves_kazhdyj(ust, vid, mem):
    komanda = komandnye(mem)
    v = [(('навык команды: ' if n in komanda else 'навык встроенный: ') + n, opisanie_navyka(p)) for n, p in sorted(ust.items())]
    v += [('память, строка списка: ' + z, opisanie_pamyati(z, chitat(os.path.join(mem, 'pamyat', k)))) for k, z in sorted(spisok_pamyati(vid, mem).items())]
    v += [('вставлено: ' + k, b) for k, b in vid['vnedryaetsya'].items()]
    v += [('карточка ОЧ (с первого чтения в чате)', len(chitat(vid['kartochka_och']).encode()))]
    return v


# ves_po_momentu: что читается по моменту — тела навыков, файлы памяти, копии CLAUDE.md
def ves_po_momentu(spisok):
    return [(i['vid'] + ': ' + i['imya'], len(i['tekst'].encode())) for i in spisok]


# === 8. Самопроверка и пробы-мутанты ===
# proba_ist: источник для самопроверки без файла
def proba_ist(imya):
    return {'vid': 'проба', 'imya': imya, 'put': imya, 'tekst': ''}


# proba_protivorechiya: трит — нашлось ли противоречие в примере 25.11 (brifing против ekonomnaya-sessiya)
def proba_protivorechiya():
    a = (proba_ist('a'), 1, 'SOSTOYANIE не писать', {'SOSTOYANIE'}, polyarnosti('SOSTOYANIE не писать'))
    b = (proba_ist('b'), 1, 'SOSTOYANIE обновить', {'SOSTOYANIE'}, polyarnosti('SOSTOYANIE обновить'))
    return NOL if protivorechie(a, b) else NET


# proba_povtora: трит повтора, где один источник — открытый навык (должно быть «не знаю»)
def proba_povtora():
    vid = {'ne_tochno': {'otkryt.md': 'открытый навык'}}
    s = 'одна и та же строка правила, длинная, для проверки повтора между файлами'
    a, b = kand(proba_ist('otkryt.md'), 1, s), kand(proba_ist('drugoj.md'), 1, s)
    return povtor(a, b, shodstvo(a, b), vid)['trit']


# primery: пары (ожидаю, получила) — пример и контрпример каждой проверки
def primery(mem):
    i, den = proba_ist('проба.md'), datetime.date(2026, 11, 25)
    return [(DA, ssylka(i, 1, 'ii-komanda `yadro-trit/trit.py`', 'yadro-trit/trit.py', mem)['trit']),
            (NET, ssylka(i, 1, 'ii-komanda `komanda/net-takogo-fajla.md`', 'komanda/net-takogo-fajla.md', mem)['trit']),
            (NOL, ssylka(i, 1, 'teacher-workpad `lib/net-takogo.md`', 'lib/net-takogo.md', mem)['trit']),
            (NOL, proba_povtora()), (NOL, proba_protivorechiya()),
            (DA, ustarelo_stroka('сдать до 01.01.2020', den, {})),
            (NOL, ustarelo_stroka('possibly a GitHub Pages site', den, {})),
            (NET, ustarelo_stroka('Тело цикла «пока» справа', den, {})),
            (NET, ustarelo_stroka('обычная строка без срока', den, {})),
            (NET, sravnit_versiyu(('7', '5', 'Б'), ('7', '5', 'Б')))]


# samoproverka: да — каждая пара совпала; итог — встроенным min
def samoproverka(mem):
    return min(DA if ozhid == poluchila else NET for ozhid, poluchila in primery(mem))


# proba_mutanta: испортить слово ядра (всегда «да») — самопроверка обязана сказать «нет»; слово вернуть
def proba_mutanta(slovo, mem):
    celoe = getattr(trit, slovo)
    setattr(trit, slovo, lambda *a: DA)
    itog = samoproverka(mem)
    setattr(trit, slovo, celoe)
    return DA if itog != DA else NET


# === 9. Отчёт ===
# yachejka: текст для ячейки таблицы — без «|» и переводов строк
def yachejka(t):
    return str(t).replace('|', '¦').replace('\n', ' ')


# tablica: таблица «трит | что | где | байт | предложение»; сначала «да», потом «не знаю»
def tablica(nahodki):
    ryady = ['| трит | что | где | байт | предложение |', '|---|---|---|---|---|']
    for n in sorted(nahodki, key=lambda x: -x['trit']):
        ryady.append('| ' + ' | '.join(yachejka(x) for x in (trit.ИМЕНА[n['trit']], n['chto'], n['gde'], n['bajt'], n['pred'])) + ' |')
    return '\n'.join(ryady)


# schet: «да N, не знаю N, нет N» по разделу
def schet(nahodki):
    return ', '.join('{} {}'.format(trit.ИМЕНА[t], sum(1 for n in nahodki if n['trit'] == t)) for t in (DA, NOL, NET))


# pometka_vesa: «сократить?» — у своего (не встроенного) больше 300 байт на каждом запросе
def pometka_vesa(c, b):
    return ' — сократить?' if b > 300 and 'встроенный' not in c else ''


# gruppy_vesa: сумма на каждом запросе по группам — до первого двоеточия или скобки
def gruppy_vesa(kazhdyj):
    gr = {}
    for c, b in kazhdyj:
        gr[re.split(r'[:(]', c)[0].strip()] = gr.get(re.split(r'[:(]', c)[0].strip(), 0) + b
    return gr


# razdel_vesa: раздел «вес» — суммы и строки, крупные сверху
def razdel_vesa(kazhdyj, po_momentu, vid):
    s = ['## 6. Вес (байт)', '', '**На каждом запросе: {} байт.**'.format(sum(b for _, b in kazhdyj)), '']
    s += ['- {} — {}{}'.format(c, b, pometka_vesa(c, b)) for c, b in sorted(kazhdyj, key=lambda x: -x[1])]
    s += ['', 'Не видны из проекта (не знаю, читаются ли): ' + ', '.join(vid['obshchaya_ne_vidna']), '']
    s += ['**По моменту: {} байт.**'.format(sum(b for _, b in po_momentu)), '']
    s += ['- {} — {}'.format(c, b) for c, b in sorted(po_momentu, key=lambda x: -x[1])]
    return '\n'.join(s)


# otchet: весь отчёт Markdown
def otchet(razdely, kazhdyj, po_momentu, sam, vid):
    s = ['# Ревизия навыков и памяти — ' + datetime.date.today().isoformat(), '',
         'Программа `tools/revizor.py` ничего не удаляет и навыки не меняет. Трит ядра: да / не знаю / нет.',
         'Самопроверка и пробы-мутанты: **{}**. Снимок видимости памяти: `{}`.'.format(trit.ИМЕНА[sam], VIDIMOST),
         'Не ищется (0): повтор между русским и английским текстом; противоречия — только по словам «не писать / обновить», «удалить», «читать».', '']
    for imya, nahodki in razdely.items():
        s += ['## ' + imya + ' — ' + schet(nahodki), '', tablica(nahodki), '']
    return '\n'.join(s) + '\n' + razdel_vesa(kazhdyj, po_momentu, vid) + '\n'


# svodka: короткая сводка в чат — счёт по разделам, вес, путь отчёта
def svodka(razdely, kazhdyj, po_momentu, sam, put):
    s = ['самопроверка и мутанты: ' + trit.ИМЕНА[sam]]
    s += ['{} — {}'.format(k, schet(v)) for k, v in razdely.items()]
    s += ['вес: на каждом запросе {} байт ({}), по моменту {} байт'.format(sum(b for _, b in kazhdyj), ', '.join('{} {}'.format(k, v) for k, v in gruppy_vesa(kazhdyj).items()), sum(b for _, b in po_momentu))]
    s += ['отчёт: ' + put]
    return '\n'.join(s)


# === 10. Главное ===
# provesti: проверки 1–5 по источникам
def provesti(spisok, ust, vid, mem):
    return {'1. Мёртвые ссылки': ssylki(spisok, mem),
            '2. Повторы': povtory(spisok, vid),
            '3. Противоречия (кандидаты)': protivorechiya(spisok),
            '4. Устаревшее': ustareloe(spisok, datetime.date.today()),
            '5. Копии навыков': kopii(ust, mem)}


# proverit_i_otchitatsya: самопроверка с мутантами → проверки → отчёт в файл → сводка в чат
def proverit_i_otchitatsya(mem, papka):
    sam = min([samoproverka(mem)] + [proba_mutanta(s, mem) for s in MUTANTY])
    vid = json.loads(chitat(VIDIMOST))
    ust = ustanovlennye(papka)
    spisok = sobrat_istochniki(mem, ust, vid)
    razdely, kazhdyj, po_momentu = provesti(spisok, ust, vid, mem), ves_kazhdyj(ust, vid, mem), ves_po_momentu(spisok)
    put = OTCHET.format(datetime.date.today().isoformat())
    with open(put, 'w', encoding='utf-8') as f:
        f.write(otchet(razdely, kazhdyj, po_momentu, sam, vid))
    print(svodka(razdely, kazhdyj, po_momentu, sam, put))
    return 0 if sam == DA else 1


# vhody: клон памяти и папка установленных навыков — из аргументов или по умолчанию
def vhody(argv):
    mem = argv[1] if len(argv) > 1 else '../memory_maryam_ai'
    papki = sorted(glob.glob(NAVYKI_SESSII))
    papka = argv[2] if len(argv) > 2 else (papki[0] if papki else '')
    return mem, papka


# glavnoe: вход есть — проверить и отчитаться (0 / 1); нет — «не знаю» (2)
def glavnoe(argv):
    mem, papka = vhody(argv)
    kod = 2
    if os.path.isfile(VIDIMOST) and os.path.isdir(os.path.join(mem, 'pamyat')) and os.path.isdir(papka):
        kod = proverit_i_otchitatsya(mem, papka)
    else:
        print('не знаю: нет входа (vidimost.json, клон памяти или папка навыков)')
    return kod


if __name__ == '__main__':
    sys.exit(glavnoe(sys.argv))
