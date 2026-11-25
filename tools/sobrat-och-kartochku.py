"""sobrat-och-kartochku: карточка ОЧ на каждый ответ — § 3, 10, 11 рабочей формы (учитель 25.11 02:55: «Берем А-Д»).

Запуск (из корня ii-komanda):  python3 tools/sobrat-och-kartochku.py
Читает komanda/vstavka/claude/03-pravila-och-rabochie.md, пишет komanda/vstavka/claude/03-och-kartochka.md.
Зачем: рабочая форма целиком (~17 тыс. знаков) перечитывалась бы на каждом запросе сессии; карточка — то,
что нужно в каждом ответе. Форма целиком — на воротах (§ 7) и после паузы. Одно знание — одно место (Л28):
карточку руками не править, пересобирать после правки формы.
Код по-фортовски: маленькие слова.
"""
import pathlib
import re

FORMA = pathlib.Path('komanda/vstavka/claude/03-pravila-och-rabochie.md')
KARTOCHKA = pathlib.Path('komanda/vstavka/claude/03-och-kartochka.md')
RAZDELY = ['3', '10', '11']
SHAPKA = ('# Карточка ОЧ — на каждый ответ\n\n'
          '**Собрано программой** `tools/sobrat-och-kartochku.py` из `03-pravila-och-rabochie.md` (§ 3, 10, 11); '
          'руками не править. Рабочая форма целиком — на воротах (публикация, каталог, «готово», экспертиза) '
          'и после паузы больше получаса. Расходится с формой — верна форма; с листком Е.8 — верен листок.\n\n')


# razdely: текст формы → словарь «номер раздела → текст раздела с заголовком»
def razdely(tekst):
    kuski = re.split(r'(?m)^(?=## \d+\. )', tekst)
    return {re.match(r'## (\d+)\.', k).group(1): k.rstrip() + '\n' for k in kuski if re.match(r'## \d+\. ', k)}


# sobrat: шапка и нужные разделы по порядку
def sobrat(tekst):
    vse = razdely(tekst)
    return SHAPKA + '\n---\n\n'.join(vse[n] for n in RAZDELY)


if __name__ == '__main__':
    KARTOCHKA.write_text(sobrat(FORMA.read_text(encoding='utf-8')), encoding='utf-8')
    print(f'{KARTOCHKA}: {len(KARTOCHKA.read_text(encoding="utf-8"))} знаков (форма — {len(FORMA.read_text(encoding="utf-8"))})')
