"""och_slovar.py — словарь правил очень осторожного человека: 46 строк листка и кандидаты — атомами.

Одно знание — одно место: словарь собирается из источников и руками не правится.
  правила, формулы, векторы, слова — книга logika/kniga/chast-2-trit/E-pravila.md (шаги Е.2–Е.8);
  кандидаты и решения по ним        — komanda/zadaniya/045/kandidaty.md;
  случаи и доли                     — komanda/zadaniya/045/ispytanie.md (счёт — tools/och_doli.py).
Запуск из корня ii-komanda: python3 -I tools/och_slovar.py  → pravila/OCH-SLOVAR.md
"""
import re
from pathlib import Path

import och_doli

KNIGA = Path('logika/kniga/chast-2-trit/E-pravila.md')
VYHOD = Path('pravila/OCH-SLOVAR.md')
GRUPPY = ['Е.2', 'Е.3', 'Е.4', 'Е.5', 'Е.6', 'Е.7']
T = (-1, 0, 1)


# Слова нижнего уровня — по книге (Е.2, стр. 255–262; Е.3): базис И, НЕ, ворота, 0.
# vorota: пропускают только 1
def vorota(x):
    return 1 if x == 1 else -1


# podtverdit: подтвердить(A, y) = A ∨ (y ∧ 0)
def podtverdit(a, y):
    return max(a, min(y, 0))


# osnovanie: основание(x, b) = (x ∧ b) ∨ (¬b ∧ 0)
def osnovanie(x, b):
    return max(min(x, b), min(-b, 0))


# soglasie: согласие(x, y) = (x ∧ y) ∨ ((x ∨ y) ∧ 0)
def soglasie(x, y):
    return max(min(x, y), min(max(x, y), 0))


# vektor: вектор слова перебором значений (одна переменная — 3, две — 9 клеток)
def vektor(slovo, mest):
    vhody = [(x,) for x in T] if mest == 1 else [(a, b) for a in T for b in T]
    return tuple(slovo(*v) for v in vhody)


SLOVA = {  # слово таблицы Е.8 → (функция, число входов)
    'ворота': (vorota, 1), 'ворота(¬x)': (lambda x: vorota(-x), 1),
    'не знаю?': (lambda x: min(-vorota(x), -vorota(-x)), 1), 'возможно': (lambda x: -vorota(-x), 1),
    'основание': (osnovanie, 2), 'оба точно': (lambda a, b: min(vorota(a), vorota(b)), 2),
    'хоть одно точно': (lambda a, b: max(vorota(a), vorota(b)), 2), 'согласие': (soglasie, 2),
    'есть ли': (lambda n, p: podtverdit(n, -p), 2), 'подтвердить': (podtverdit, 2),
}


# vektor_po_slovam: вектор правила по его словам; у набора и способа записи своего вектора нет
def vektor_po_slovam(slova):
    chasti = [f'{s} {vektor(*SLOVA[s])}' for s in slova if s in SLOVA]
    svoego_net = [s for s in slova if s not in SLOVA]
    tekst = '; '.join(chasti) + ('; ' if chasti and svoego_net else '')
    return tekst + (f'своего нет ({", ".join(svoego_net)})' if svoego_net else '')




# razdely: текст книги → {«Е.2»: (название, текст раздела)}
def razdely(tekst):
    chasti = re.split(r'^## (Е\.\d+)\. (.+)$', tekst, flags=re.M)
    return {chasti[i]: (chasti[i + 1], chasti[i + 2]) for i in range(1, len(chasti) - 2, 3)}


# pravila_razdela: раздел → [(заголовок правила, текст до следующего правила)]
def pravila_razdela(tekst):
    chasti = re.split(r'^\*\*Правило \d+\. (.+?)\*\*$', tekst, flags=re.M)
    return [(chasti[i], chasti[i + 1]) for i in range(1, len(chasti) - 1, 2)]


# pervoe: первая находка шаблона в тексте или «—»
def pervoe(shablon, tekst):
    najdeno = re.search(shablon, tekst, flags=re.M)
    return najdeno.group(1).strip() if najdeno else '—'


# formula_pravila: формула правила («x = …», «Формулой: …», строки таблицы) или почему её нет
def formula_pravila(tekst, dejstvie):
    najdeno = pervoe(r'^Формулой: ([^\n]+)$', tekst)
    if najdeno == '—':
        najdeno = pervoe(r'^([а-яё«][^|\n]{0,70}? = [^\n]+)$', tekst)
    if najdeno == '—':
        najdeno = pervoe(r'([а-яё]+\([^)\n]*\) = [^.;\n]+)', tekst)
    stroki_tablicy = re.findall(r'^\| ([а-яё ]+ = [^|]+?) \|', tekst, flags=re.M)
    if najdeno == '—' and stroki_tablicy:
        najdeno = '; '.join(stroki_tablicy) + ' (строки таблицы)'
    if najdeno == '—' and re.match(r'(своего|только набор|выбор по триту)', dejstvie):
        najdeno = 'своей нет: ' + dejstvie.split(' - ')[0].split('. ')[0]
    return najdeno


# vektor_pravila: вектор из текста правила или пометка, где он и почему его нет
def vektor_pravila(tekst, dejstvie):
    najdeno = pervoe(r'(Вектора?м?и?[^:\n]*: [^\n]+?)(?:\.\s|\.$|$)', tekst)
    ssylka = pervoe(r'((?:Таблица и вектор|Формула|Действие)[^\n]{0,15}(?:те же|та же|то же|тот же|- основание)[^\n]{0,80})', tekst)
    nabory = pervoe(r'(Наборов на входе \d+\.[^\n]{0,80})', tekst)
    if najdeno == '—' and re.search(r'^\| [а-яё ]+ = [^|]+ \| [−\d]', tekst, flags=re.M):
        najdeno = 'в таблице правила (строка на каждое действие)'
    for zapas in (ssylka, nabory):
        if najdeno == '—' and zapas != '—':
            najdeno = zapas
    if najdeno == '—' and re.match(r'(своего|выбор по триту)', dejstvie):
        najdeno = 'своего нет: ' + dejstvie.split(' - ')[0].split('. ')[0]
    return najdeno


# atom_knigi: заголовок и текст правила → поля атома
def atom_knigi(nomer, gruppa, zagolovok, tekst):
    dejstvie = pervoe(r'^\*Действие: ([^\n]{0,160})', tekst)
    atom = {'id': f'Л{nomer}', 'gruppa': gruppa, 'pravilo': zagolovok, 'dejstvie': dejstvie,
            'formula': formula_pravila(tekst, dejstvie), 'vektor': vektor_pravila(tekst, dejstvie)}
    return atom


# listok: строки листка Е.8: номер → текст
def listok(tekst):
    return {int(n): s.strip() for n, s in re.findall(r'^(\d+)\. (.+)$', tekst, flags=re.M)}


# slova_listka: таблица Е.8 «слово → правила»: номер правила → [слова]
def slova_listka(tekst):
    slova = {}
    for slovo, nomera in re.findall(r'^\|[^|]*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|$', tekst, flags=re.M):
        for n in re.findall(r'\d+', nomera):
            slova.setdefault(int(n), []).append(slovo.strip())
    return slova


# atomy_knigi: все 46 правил по порядку групп Е.2–Е.7
def atomy_knigi(tekst):
    r = razdely(tekst)
    atomy = []
    for g in GRUPPY:
        nazvanie, telo = r[g]
        for zagolovok, kusok in pravila_razdela(telo):
            atomy.append(atom_knigi(len(atomy) + 1, f'{g} {nazvanie}', zagolovok, kusok))
    return atomy


# kandidaty: строки таблицы кандидатов → атомы
def kandidaty(tekst):
    atomy = []
    for s in tekst.splitlines():
        k = [y.strip() for y in s.strip().strip('|').split('|')]
        if len(k) > 10 and re.fullmatch(r'ОЧ-\d+', k[0]):
            atomy.append({'id': k[0], 'stroka': k[1], 'gruppa': k[2], 'pravilo': k[3], 'formula': k[6],
                          'vektor': k[7], 'tot_zhe': k[8], 'reshenie': k[10]})
    return atomy


# sluchai: строка счёта для атома
def sluchai(schet, m):
    s = schet.get(m)
    return och_doli.dolya(s) + f" помогло; − {s['−']}, ! {s['!']}, ? {s['?']}" if s else 'нет'


# blok_knigi: атом правила листка текстом
def blok_knigi(a, stroka, slova, schet, dubli):
    svoi = [k for k, l in dubli.items() if a['id'] in l]
    stroki = [f"### {a['id']} · {stroka}", '', '```атом', f"id: {a['id']}", 'тип: правило ОЧ',
              f"строка листка: {stroka}", f"правило в книге: {a['pravilo']}", f"группа: {a['gruppa']}",
              f"слово: {', '.join(slova) or 'нет в таблице Е.8'}", f"формула: {a['formula']}",
              f"вектор правила (книга): {a['vektor']}", f"векторы слов (программа): {vektor_po_slovam(slova)}",
              f"действие: {a['dejstvie']}", 'слой: 1 (листок; слои — по долям ≈ 23.12)',
              f"случаи: {sluchai(schet, a['id'])}", f"дубли-кандидаты: {', '.join(svoi) or 'нет'}", '```', '']
    return '\n'.join(stroki)


# blok_kandidata: атом кандидата текстом
def blok_kandidata(a, schet):
    stroki = [f"### {a['id']} · {a['stroka']}", '', '```атом', f"id: {a['id']}", 'тип: кандидат ОЧ',
              f"правило: {a['pravilo']}", f"группа: {a['gruppa']}", f"формула: {a['formula']}",
              f"вектор: {a['vektor']}", f"тот же вектор у: {a['tot_zhe']}", f"решение: {a['reshenie']}",
              f"случаи: {sluchai(schet, a['id'])}", '```', '']
    return '\n'.join(stroki)


SHAPKA = ('# Словарь правил очень осторожного человека\n\n**Собран программой** `tools/och_slovar.py` — руками не править. '
          'Источники: книга (`logika/kniga/chast-2-trit/E-pravila.md`), кандидаты (`komanda/zadaniya/045/kandidaty.md`), '
          'случаи (`komanda/zadaniya/045/ispytanie.md`). Решение учителя 23.11, 22:04–22:11: список правил — словарь, растёт; '
          'у каждого правила и кандидата — формула и вектор; по долям случаев за месяц — порядок и слои. '
          '«Вектор правила» — из книги; если своего вектора нет, сказано почему (так в книге), «—» — в книге не нашлось ни вектора, ни объяснения. «Векторы слов» — программа считает по словам таблицы Е.8; это вектор слова, а не правила: у 7 правил формула составная (слово плюс ещё действие), и векторы различаются — так и должно быть. У набора И, ИЛИ, НЕ и у способа записи своего вектора нет.\n\n## Правила листка (46)\n\n')


# chast_pravil: 46 атомов листка текстом
def chast_pravil(kniga, schet, dubli):
    e8 = razdely(kniga)['Е.8'][1]
    ls, sl = listok(e8), slova_listka(e8)
    return ''.join(blok_knigi(a, ls.get(int(a['id'][1:]), '—'), sl.get(int(a['id'][1:]), []), schet, dubli)
                   for a in atomy_knigi(kniga))


# sobrat: весь словарь одним текстом
def sobrat():
    kniga = KNIGA.read_text(encoding='utf-8')
    tekst_kand = och_doli.KANDIDATY.read_text(encoding='utf-8')
    dubli = och_doli.dubli(tekst_kand)
    schet = och_doli.poschitat(och_doli.stroki_tablicy(och_doli.ZHURNAL.read_text(encoding='utf-8')), dubli)
    kand = ''.join(blok_kandidata(a, schet) for a in kandidaty(tekst_kand))
    return SHAPKA + chast_pravil(kniga, schet, dubli) + '## Кандидаты\n\n' + kand


if __name__ == '__main__':
    VYHOD.write_text(sobrat(), encoding='utf-8')
    print(VYHOD, '— записан')
