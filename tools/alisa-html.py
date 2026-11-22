# alisa-html.py — промт Алисы (Markdown) → HTML-страница с частями для вставки в чат.
#   python3 tools/alisa-html.py algoritm/alisa-v7-3-ruchnaya.md выход.html "[7]" "[12]"
# Аргументы после выхода — разделы, с которых начинается часть 2, часть 3, …
# Части: первая строка «ЧАСТЬ k из N. Ответь одним словом «принято».», последняя — «…начинай.»
import html
import sys

SHAPKA = """<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8"><title>{zagolovok}</title>
<style>
body{{font-family:system-ui,sans-serif;background:#f6f4ef;color:#222;max-width:900px;margin:2em auto;padding:0 1em;line-height:1.45}}
h1{{font-size:1.4em}} h2{{font-size:1.05em;margin-top:1.6em}} small{{color:#777;font-weight:normal}}
textarea{{width:100%;height:9em;font:13px/1.35 monospace;border:1px solid #ccc;border-radius:6px;padding:.5em;box-sizing:border-box}}
button{{background:#2f6f5e;color:#fff;border:0;border-radius:6px;padding:.5em 1em;font-size:1em;cursor:pointer;margin-bottom:.4em}}
button.ok{{background:#888}}
</style></head><body>
<h1>{zagolovok}</h1>
<ol>
<li>Откройте Алису в новом чате, режим «Эксперт».</li>
<li>«Копировать часть 1» → вставить в чат (Ctrl+V) → отправить. Алиса ответит «принято».</li>
<li>Так же остальные части по порядку. На последнюю Алиса начнёт работу: спросит, доступен ли Claude, и задаст вопросы по шапке урока.</li>
<li>Если Claude доступен: на СТОП 2 Алиса выдаст пакет — его вставляете в новый чат Claude.</li>
</ol>
"""
KONEC = """<script>
function kop(k,b){var t=document.getElementById('t'+k);t.select();
try{navigator.clipboard.writeText(t.value).then(ok,function(){document.execCommand('copy');ok()})}catch(e){document.execCommand('copy');ok()}
function ok(){b.textContent='Скопировано — часть '+k;b.className='ok'}}
</script></body></html>"""


# razrezat: текст промта → куски, каждый следующий начинается строкой с нужным разделом
def razrezat(tekst, granicy):
    kuski = []
    ostatok = tekst
    for metka in granicy:
        mesto = ostatok.index('\n' + metka + ' ')
        kuski.append(ostatok[:mesto].strip('\n'))
        ostatok = ostatok[mesto + 1:]
    kuski.append(ostatok.strip('\n'))
    return kuski


# podpisat: к куску — первая строка «ЧАСТЬ k из N …»
def podpisat(kusok, k, n):
    pros = 'Ответь одним словом «принято».'
    if k == n:
        pros = 'Это последняя часть: начинай.'
    chast = 'ЧАСТЬ {} из {}. {}\n\n{}'.format(k, n, pros, kusok)
    return chast


# sekciya: HTML-блок одной части с кнопкой копирования
def sekciya(chast, k, n):
    blok = ('<section><h2>Часть {k} из {n} <small>{z} знаков</small></h2>\n'
            '<button onclick="kop({k},this)">Копировать часть {k}</button>\n'
            '<textarea id="t{k}" readonly>{t}</textarea></section>\n').format(
        k=k, n=n, z=len(chast), t=html.escape(chast, quote=False))
    return blok


# stranica: вся страница из частей
def stranica(tekst, granicy, zagolovok):
    kuski = razrezat(tekst, granicy)
    n = len(kuski)
    telo = ''.join(sekciya(podpisat(kusok, i + 1, n), i + 1, n) for i, kusok in enumerate(kuski))
    vsyo = SHAPKA.format(zagolovok=zagolovok) + telo + KONEC
    return vsyo


# glavnoe: прочитать промт, записать страницу, напечатать размеры частей
def glavnoe(argumenty):
    vhod, vyhod, granicy = argumenty[0], argumenty[1], argumenty[2:]
    tekst = open(vhod, encoding='utf-8').read()
    zagolovok = tekst.split('\n', 1)[0].strip('= ').split(' —')[0].replace('ПРОМТ АЛИСА', 'Алиса') + ' — промт для нового урока'
    open(vyhod, 'w', encoding='utf-8').write(stranica(tekst, granicy, zagolovok))
    for i, kusok in enumerate(razrezat(tekst, granicy)):
        print('часть', i + 1, '—', len(kusok), 'знаков')


if __name__ == '__main__':
    glavnoe(sys.argv[1:])
