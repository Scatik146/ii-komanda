# сбор подключаемого листа правил очень осторожного человека
# Марьям, 23.11.2026. Одно знание — одно место (ОЧ-10): лист не пишется руками,
# он собирается из свода (svod-fp.md ← sbor_svoda.py) и кандидатов (pravila-ostorozhnogo.md, Б2).
# Запуск: python3 logika/sobrat_podklyuchenie.py  → пишет pravila/OCHEN-OSTOROZHNYJ.md

import re
from pathlib import Path

KOREN = Path(__file__).resolve().parent.parent
SVOD = KOREN / "logika" / "svod-fp.md"
KANDIDATY = KOREN / "forto-prolog" / "pravila-ostorozhnogo.md"
VYHOD = KOREN / "pravila" / "OCHEN-OSTOROZHNYJ.md"

SHAPKA = """<!-- Собрано программой logika/sobrat_podklyuchenie.py — руками не править.
     Править: свод — logika/sbor_svoda.py, кандидатов — forto-prolog/pravila-ostorozhnogo.md (Б2). -->
# Правила очень осторожного человека — подключаемый лист

**Главный принцип (учитель):** неизвестное не превращается ни в «да», ни в «нет». Наружу и к ученикам проходит только то, что и верно, и проверено.

**Как подключать.** В промт, задание или навык — одна строка:
> Работай по правилам очень осторожного человека: https://github.com/Scatik146/ii-komanda/blob/main/pravila/OCHEN-OSTOROZHNYJ.md

Помощнику без доступа к ссылкам (Алиса) вставлять этот лист текстом целиком.

**Как применять — три шага:**
1. У каждого утверждения два трита: правда ли (1 / 0 / −1) и проверено ли (1 / 0 / −1).
2. Не знаешь — так и говори: «пока не знаю, проверю». Основание для «да» — проверка, пример, подлинник, решение автора.
3. Выдавать, сдавать, публиковать — только «и там, и там 1». Чтобы остановить, хватит сомнения.

Подробно, с примерами и формулами — `logika/svod.md`; атомами — `logika/svod-fp.md`.
"""


# pravila: пары (номер, афоризм) из заголовков свода «### ОЧ-01 · …»
def pravila(tekst, priznak):
    shablon = r"^### (" + priznak + r"[-\d]*\d) · (.+)$"
    return re.findall(shablon, tekst, flags=re.M)


# razdel: текст раздела от заголовка «## начало…» до следующего «## »
def razdel(tekst, nachalo):
    chast = tekst.split("\n## " + nachalo, 1)
    if len(chast) < 2:
        raise SystemExit("нет раздела: " + nachalo)
    return chast[1].split("\n## ", 1)[0]


# kandidaty: пары (номер, афоризм) из таблицы раздела Б2
def kandidaty(tekst):
    stroki = razdel(tekst, "Б2.").splitlines()
    para = []
    for s in stroki:
        kletki = [k.strip() for k in s.strip().strip("|").split("|")]
        if len(kletki) >= 3 and re.fullmatch(r"ОЧ-\d+", kletki[0]):
            para.append((kletki[0], kletki[2]))
    return para


# spisok: строки списка «- **номер.** афоризм»
def spisok(pary):
    return "\n".join(f"- **{n}.** {a}" for n, a in pary)


# sobrat: весь лист из трёх списков
def sobrat():
    svod = SVOD.read_text(encoding="utf-8")
    kand = KANDIDATY.read_text(encoding="utf-8")
    och, murfi, novye = pravila(svod, "ОЧ"), pravila(svod, "Б"), kandidaty(kand)
    if not och or not murfi or not novye:
        raise SystemExit("пустой список — свод или кандидаты не прочитаны")
    return (SHAPKA
            + "\n## Действующие правила\n\n" + spisok(och)
            + "\n\n## Законы Мерфи глазами осторожного\n\n" + spisok(murfi)
            + "\n\n## Кандидаты (0 — ждут решения автора, задание 045)\n\n" + spisok(novye)
            + "\n\nКандидат — не правило: применять как подсказку, ссылаться — с пометкой «кандидат».\n")


# zapisat: собрать и положить лист, сказать сколько правил
def zapisat():
    tekst = sobrat()
    VYHOD.write_text(tekst, encoding="utf-8")
    print(VYHOD.relative_to(KOREN), "—", tekst.count("\n- **"), "строк правил")


zapisat()
