# сбор подключаемого листа правил очень осторожного человека
# Марьям, 23.11.2026. Одно знание — одно место (строка 28 листка): лист руками не пишется,
# он собирается из листка Е.8 книги (последняя версия правил) и кандидатов (komanda/zadaniya/045/kandidaty.md); logika/ только читает.
# Запуск: python3 tools/sobrat-och-list.py  → пишет pravila/OCHEN-OSTOROZHNYJ.md

import re
from pathlib import Path

KOREN = Path(__file__).resolve().parent.parent
KNIGA = KOREN / "logika" / "kniga" / "chast-2-trit" / "E-pravila.md"
KANDIDATY = KOREN / "komanda" / "zadaniya" / "045" / "kandidaty.md"
VYHOD = KOREN / "pravila" / "OCHEN-OSTOROZHNYJ.md"
VSEGO = 46          # столько строк в листке Е.8; изменилось — проверить сборку

SHAPKA = """<!-- Собрано программой tools/sobrat-och-list.py — руками не править.
     Источники: листок Е.8 книги (logika/kniga/chast-2-trit/E-pravila.md) и komanda/zadaniya/045/kandidaty.md. -->
# Правила очень осторожного человека — подключаемый лист

**Главный принцип (учитель):** неизвестное не превращается ни в «да», ни в «нет». Наружу и к ученикам проходит только то, что и верно, и проверено.

**Как подключать.** В промт, задание или навык — одна строка:
> Работай по правилам очень осторожного человека: https://github.com/Scatik146/ii-komanda/blob/main/pravila/OCHEN-OSTOROZHNYJ.md

Помощнику без доступа к ссылкам (Алиса) вставлять этот лист текстом целиком.

**Как применять — три шага:**
1. У каждого утверждения два трита: правда ли (1 / 0 / −1) и проверено ли (1 / 0 / −1).
2. Не знаешь — так и говори: «пока не знаю, проверю». Основание для «да» — проверка, пример, подлинник, решение автора.
3. Выдавать, сдавать, публиковать — только «и там, и там 1». Чтобы остановить, хватит сомнения.

Правила с формулами, примерами и контрпримерами — книга, часть 2, шаг Е: `logika/kniga/chast-2-trit/E-pravila.md`.
"""


# razdel: текст от заголовка «## начало…» до следующего «## »
def razdel(tekst, nachalo):
    chast = tekst.split("\n## " + nachalo, 1)
    if len(chast) < 2:
        raise SystemExit("нет раздела: " + nachalo)
    return chast[1].split("\n## ", 1)[0]


# listok: строки листка Е.8 — между первой и второй чертой «---», без вступления
def listok(kniga):
    chasti = razdel(kniga, "Е.8.").split("\n---\n")
    if len(chasti) < 3:
        raise SystemExit("в листке Е.8 не найдены черты «---»")
    return chasti[1].strip()


# chislo_pravil: сколько нумерованных строк в листке
def chislo_pravil(tekst):
    return len(re.findall(r"^\d+\. ", tekst, flags=re.M))


# kandidaty: строки «- **ОЧ-NN** (группа). афоризм» из таблиц файла кандидатов
def kandidaty(tekst):
    stroki = []
    for s in tekst.splitlines():
        kletki = [k.strip() for k in s.strip().strip("|").split("|")]
        if len(kletki) >= 3 and re.fullmatch(r"ОЧ-\d+", kletki[0]):
            stroki.append(f"- **{kletki[0]}** ({kletki[2]}). {kletki[1]}")
    return stroki


# sobrat: весь лист — шапка, листок, кандидаты
def sobrat():
    tekst = listok(KNIGA.read_text(encoding="utf-8"))
    if chislo_pravil(tekst) != VSEGO:
        raise SystemExit(f"в листке {chislo_pravil(tekst)} правил, ждали {VSEGO} — проверить")
    kand = kandidaty(KANDIDATY.read_text(encoding="utf-8"))
    if not kand:
        raise SystemExit("кандидаты не прочитаны")
    return (SHAPKA
            + "\n## Листок: действующие правила (книга, Е.8)\n\n" + tekst
            + "\n\n## Кандидаты (0 — ждут решения автора, задание 045)\n\n" + "\n".join(kand)
            + "\n\nКандидат — не правило: применять как подсказку, ссылаться — с пометкой «кандидат».\n")


# zapisat: собрать и положить лист, сказать, сколько в нём правил и кандидатов
def zapisat():
    tekst = sobrat()
    VYHOD.write_text(tekst, encoding="utf-8")
    print(VYHOD.relative_to(KOREN), "—", VSEGO, "правил,", tekst.count("\n- **ОЧ-"), "кандидата")


zapisat()
