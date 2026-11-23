"""skelet.py — скелет урока: заголовок, экраны (h1–h3), кнопки — чтобы увидеть механику без чтения кода."""
import re, sys, html
from pathlib import Path
KOREN = Path(sys.argv[1])

# chistyj: текст без тегов и лишних пробелов
def chistyj(t):
    t = html.unescape(re.sub(r'<[^>]+>', '', t))
    return re.sub(r'\s+', ' ', t).strip()

# skelet: один html → строка «title | h: … | b: …»
def skelet(p):
    t = p.read_text(encoding='utf-8', errors='ignore')
    title = chistyj(''.join(re.findall(r'<title>(.*?)</title>', t, re.S)[:1]))
    h = [chistyj(x) for x in re.findall(r'<h[1-3][^>]*>(.*?)</h[1-3]>', t, re.S)]
    b = [chistyj(x) for x in re.findall(r'<button[^>]*>(.*?)</button>', t, re.S)]
    h = [x for x in dict.fromkeys(h) if x][:14]
    b = [x for x in dict.fromkeys(b) if x and len(x) < 40][:12]
    return f"{p.name}: «{title}» | экраны: {' / '.join(h)} | кнопки: {' · '.join(b)}"[:600]

for papka in sorted(KOREN.glob('*/*/')):
    if not re.match(r'(\d+-klass|obshchie)$', papka.parent.name): continue
    print('##', papka.relative_to(KOREN))
    for p in sorted(papka.glob('*.html'))[:4]:
        print(' ', skelet(p))
