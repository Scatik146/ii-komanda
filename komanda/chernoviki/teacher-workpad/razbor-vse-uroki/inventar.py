"""inventar.py — опись уроков teacher-workpad: файлы, приёмы, имена функций (по-фортовски)."""
import json, re, sys
from pathlib import Path
from collections import defaultdict

KOREN = Path(sys.argv[1])
PRIEMY = {
    'хранение': r'localStorage', 'меню Ctrl+Alt+M': r'menu-ekranov|MenuEkranov', 'голос': r'speechSynthesis',
    'перетаскивание': r'dragstart|draggable|pointerdown|touchstart', 'холст': r'getContext\(', 'таймер': r'setInterval',
    'печать': r'window\.print|@media print', 'буфер обмена': r'clipboard|execCommand\(.copy',
    'звук': r'AudioContext|new Audio', 'дракон-схема': r'DrakonShema', 'конспект ДРАКОН-ГРАФ': r'Konspekt\.draw',
    'lib/slova': r'lib/slova', 'камера/микрофон': r'getUserMedia', 'клавиатура': r"keydown",
    'случайность': r'Math\.random', 'svg': r'<svg|createElementNS', 'файлы': r'FileReader|showOpenFilePicker|download=',
}

# imena: имена функций в JS-тексте
def imena(tekst):
    spisok = set(re.findall(r'function\s+([A-Za-z_$][\w$]*)\s*\(', tekst))
    spisok |= set(re.findall(r'(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:function|\([^)]*\)\s*=>|[a-zA-Z_$]\w*\s*=>)', tekst))
    return spisok

# kod_uroka: весь JS и HTML урока одной строкой (без lib)
def kod_uroka(papka):
    chasti = [p.read_text(encoding='utf-8', errors='ignore') for p in papka.rglob('*') if p.suffix in ('.js', '.html', '.css')]
    return '\n'.join(chasti)

# opis_uroka: одна папка → опись
def opis_uroka(papka):
    kod = kod_uroka(papka)
    js = '\n'.join(p.read_text(encoding='utf-8', errors='ignore') for p in papka.rglob('*.js')) + '\n' + \
         '\n'.join(re.findall(r'<script[^>]*>(.*?)</script>', kod, re.S))
    fajly = sorted(str(p.relative_to(papka)) for p in papka.rglob('*') if p.is_file())
    opis = {'papka': str(papka.relative_to(KOREN)), 'fajlov': len(fajly), 'strok': kod.count('\n'),
            'fajly': fajly[:30], 'priemy': [k for k, r in PRIEMY.items() if re.search(r, kod)], 'imena': sorted(imena(js))}
    return opis

uroki = [opis_uroka(p) for p in sorted(KOREN.glob('*/*/')) if re.match(r'(\d+-klass|obshchie)$', p.parent.name)]
gde = defaultdict(list)
for u in uroki:
    for i in u['imena']: gde[i].append(u['papka'])
obshchie = {i: g for i, g in gde.items() if len(g) >= 3}
json.dump({'uroki': uroki, 'obshchie': obshchie}, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1)
print('уроков', len(uroki), 'имён', len(gde), 'в ≥3 уроках', len(obshchie))
pr = defaultdict(int)
for u in uroki:
    for p in u['priemy']: pr[p] += 1
print(sorted(pr.items(), key=lambda x: -x[1]))
for i, g in sorted(obshchie.items(), key=lambda x: -len(x[1]))[:60]: print(len(g), i)
