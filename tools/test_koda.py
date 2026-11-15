#!/usr/bin/env python3
"""test_koda.py — задание по коду отдаём модели через Яндекс, ответ проверяем командами.

    python tools/test_koda.py <задание.md> --model alisa      (или deepseek)
    python tools/test_koda.py <задание.md> --model alisa --podstavit ответ1.md ответ2.md   (без сети)

Круг: модель отвечает → файлы ответа раскладываются по папке → запускаются проверки задания.
Есть ошибки — второй круг: модель получает текст ошибок и присылает всё заново. Кругов — два.
Ручные проверки (строки «руками:») скрипт задаёт учителю один раз, по последнему кругу.
Итог — testy/<задание>/<модель>/itog.md. Нижние слова (ключи, модели, вызов) взяты из ii.py.

Задание — Markdown. Скрипт читает в нём два раздела:
    ## Сдать файлы          имена файлов в `обратных кавычках`
    ## Проверки командой    строки «- авто: <команда>» и «- руками: <что сделать и что ждём>»
В командах: {otvet} — папка с файлами ответа, {tw} — teacher-workpad, {dg} — drakon-graf.
Внимание: проверки запускают код, написанный моделью, на этом компьютере.
"""
import argparse
import datetime
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ii  # noqa: E402  — словарь проверенных слов: ключи, модели, вызов

KOREN = ii.KOREN
NAVYK = "docs/komanda/TRI-STILYA-ODNIM-TEKSTOM.md"
KRUGOV = 2
OGRADA = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")
IMYA_FAJLA = re.compile(r"[A-Za-zА-Яа-яЁё0-9_-]+\.[A-Za-z0-9]+")

# Данные.
#   proverka: {"vid": "авто" | "руками", "tekst": строка задания}
#   itog:     {"vid", "tekst", "proshla": True | False | None (не проверялась), "vyvod": строка}
#   krug:     {"nomer", "model", "tokeny", "fajly": [имена], "itogi": [itog]}


# раздел: текст раздела задания по началу его заголовка («Сдать файлы»)
def razdel(zadanie, nazvanie):
    m = re.search(r"^##\s*" + re.escape(nazvanie) + r"[^\n]*\n(.*?)(?=^##\s|\Z)", zadanie, re.S | re.M)
    return m.group(1) if m else ""


# файлыЗадания: имена файлов, которые модель должна сдать
def fajly_zadaniya(zadanie):
    return re.findall(r"`([^`\s]+\.[A-Za-z0-9]+)`", razdel(zadanie, "Сдать файлы"))


# проверкиЗадания: список проверок из раздела «Проверки командой»
def proverki_zadaniya(zadanie):
    spisok = []
    for stroka in razdel(zadanie, "Проверки командой").splitlines():
        m = re.match(r"\s*-\s*(авто|руками)\s*:\s*(.+)$", stroka)
        if m:
            spisok.append({"vid": m.group(1), "tekst": m.group(2).strip()})
    return spisok


# конецОграды: номер строки, закрывающей ограду, или длина списка (ограда не закрыта)
def konec_ogrady(stroki, nachalo):
    znak = OGRADA.match(stroki[nachalo]).group(1)
    konec = len(stroki)
    for j in range(nachalo + 1, len(stroki)):
        s = stroki[j].strip()
        if konec == len(stroki) and s.startswith(znak) and set(s) == {znak[0]}:
            konec = j
    return konec


# имяПередОградой: имя файла из ближайшей непустой строки над оградой («» — имени нет)
def imya_pered_ogradoj(stroki, nachalo, nuzhnye):
    imya = ""
    j = nachalo - 1
    while j >= 0 and not stroki[j].strip():
        j -= 1
    if j >= 0:
        najdeny = [n for n in IMYA_FAJLA.findall(stroki[j]) if n in nuzhnye]
        imya = najdeny[0] if najdeny else ""
    return imya


# файлыИзОтвета: {имя: текст} — блоки кода ответа, над которыми стоит имя нужного файла
def fajly_iz_otveta(otvet, nuzhnye):
    stroki, fajly, i = otvet.splitlines(), {}, 0
    while i < len(stroki):
        if OGRADA.match(stroki[i]):
            konec = konec_ogrady(stroki, i)
            imya = imya_pered_ogradoj(stroki, i, nuzhnye)
            if imya:
                fajly[imya] = "\n".join(stroki[i + 1:konec]) + "\n"
            i = konec
        i += 1
    return fajly


# разложить: записать файлы ответа в папку круга
def razlozhit(fajly, papka):
    papka.mkdir(parents=True, exist_ok=True)
    for imya, tekst in fajly.items():
        (papka / Path(imya).name).write_text(tekst, encoding="utf-8")


# команда: подставить в строку проверки папки ответа и репозиториев
def komanda(tekst, puti):
    for klyuch, put in puti.items():
        tekst = tekst.replace("{" + klyuch + "}", str(put))
    return tekst


# запуститьАвто: выполнить одну команду проверки; прошла — код выхода 0
def zapustit_avto(proverka, puti):
    try:
        r = subprocess.run(komanda(proverka["tekst"], puti), shell=True, capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=120)
        proshla, vyvod = r.returncode == 0, (r.stdout + r.stderr).strip()
    except subprocess.TimeoutExpired:
        proshla, vyvod = False, "команда не завершилась за 120 с"
    return {"vid": "авто", "tekst": proverka["tekst"], "proshla": proshla, "vyvod": vyvod[-1500:]}


# нетФайлов: итоги-ошибки за файлы, которых модель не сдала
def net_fajlov(nuzhnye, fajly):
    propushcheny = [n for n in nuzhnye if n not in fajly]
    return [{"vid": "авто", "tekst": "сдан файл " + n, "proshla": False,
             "vyvod": "в ответе нет блока кода с именем файла " + n + " над ним"} for n in propushcheny]


# проверитьАвто: итоги всех автоматических проверок круга
def proverit_avto(zadanie, fajly, puti):
    itogi = net_fajlov(fajly_zadaniya(zadanie), fajly)
    for proverka in proverki_zadaniya(zadanie):
        if proverka["vid"] == "авто":
            itogi.append(zapustit_avto(proverka, puti))
    return itogi


# спроситьУчителя: одна ручная проверка — учитель делает и отвечает «да» или «нет»
def sprosit_uchitelya(proverka, puti):
    print("\nРУКАМИ:", komanda(proverka["tekst"], puti))
    otvet = input("Получилось? (да / нет / пропустить): ").strip().lower()
    proshla = {"да": True, "нет": False}.get(otvet)
    vyvod = input("Что увидел (одной строкой, можно пусто): ").strip() if proshla is not None else "пропущено"
    return {"vid": "руками", "tekst": proverka["tekst"], "proshla": proshla, "vyvod": vyvod}


# проверитьРуками: ручные проверки задания; bez_ruk — только записать, что не проверялись
def proverit_rukami(zadanie, puti, bez_ruk):
    itogi = []
    for proverka in proverki_zadaniya(zadanie):
        if proverka["vid"] == "руками" and bez_ruk:
            itogi.append({"vid": "руками", "tekst": proverka["tekst"], "proshla": None, "vyvod": "не проверялось"})
        elif proverka["vid"] == "руками":
            itogi.append(sprosit_uchitelya(proverka, puti))
    return itogi


# промптЗадания: навык «одним текстом» и текст задания
def prompt_zadaniya(zadanie, tw):
    navyk = (tw / NAVYK).read_text(encoding="utf-8")
    return ("НАВЫК КОМАНДЫ (прочитай целиком):\n\n" + navyk + "\n\n=== ЗАДАНИЕ ===\n\n" + zadanie
            + "\n\nКаждый файл — целиком, в своём блоке кода; строкой выше — имя файла. "
              "Файл .md, внутри которого есть блоки ```, оберни в ограду из четырёх обратных кавычек.")


# текстОшибок: непрошедшие проверки — для второго круга и для отчёта
def tekst_oshibok(itogi):
    plohie = [i for i in itogi if i["proshla"] is False]
    return "\n\n".join("ПРОВЕРКА: %s\nВЫВОД:\n%s" % (i["tekst"], i["vyvod"]) for i in plohie)


# промптИсправления: задание, прошлый ответ и ошибки проверки
def prompt_ispravleniya(osnova, otvet, itogi):
    return (osnova + "\n\n=== ТВОЙ ПРОШЛЫЙ ОТВЕТ ===\n\n" + otvet + "\n\n=== ОШИБКИ ПРОВЕРКИ ===\n\n"
            + tekst_oshibok(itogi) + "\n\nИсправь ошибки и пришли все файлы заново, целиком, в том же виде.")


# ответМодели: текст ответа и число токенов — из сети или из подставного файла
def otvet_modeli(kt, model, tekst, podstavit, nomer):
    if podstavit:
        fajl = podstavit[min(nomer, len(podstavit)) - 1]
        otvet, tokeny = Path(fajl).read_text(encoding="utf-8"), "подставной ответ"
    else:
        otvet, tokeny = ii.odin_vyzov(kt, model, tekst)
    return otvet, tokeny


# круг: вызов модели → разложить файлы → автоматические проверки
def krug(kt, nastrojki, tekst, nomer):
    otvet, tokeny = otvet_modeli(kt, nastrojki["model"], tekst, nastrojki["podstavit"], nomer)
    papka = nastrojki["papka"] / ("krug-%d" % nomer)
    fajly = fajly_iz_otveta(otvet, fajly_zadaniya(nastrojki["zadanie"]))
    razlozhit(fajly, papka)
    (papka / "otvet.md").write_text(otvet, encoding="utf-8")
    itogi = proverit_avto(nastrojki["zadanie"], fajly, dict(nastrojki["puti"], otvet=papka))
    print("круг %d: проверок %d, не прошло %d" % (nomer, len(itogi), sum(i["proshla"] is False for i in itogi)))
    return {"nomer": nomer, "tokeny": tokeny, "fajly": sorted(fajly), "itogi": itogi, "otvet": otvet, "papka": papka}


# круги: первый круг и, если есть ошибки, круги исправления
def krugi(kt, nastrojki):
    osnova = prompt_zadaniya(nastrojki["zadanie"], nastrojki["puti"]["tw"])
    spisok = [krug(kt, nastrojki, osnova, 1)]
    while tekst_oshibok(spisok[-1]["itogi"]) and len(spisok) < KRUGOV:
        proshlyj = spisok[-1]
        tekst = prompt_ispravleniya(osnova, proshlyj["otvet"], proshlyj["itogi"])
        spisok.append(krug(kt, nastrojki, tekst, len(spisok) + 1))
    return spisok


# строкаИтога: одна проверка одной строкой отчёта
def stroka_itoga(i):
    znak = {True: "✓", False: "✗", None: "—"}[i["proshla"]]
    poslednyaya = (i["vyvod"].strip().splitlines() or [""])[-1]
    hvost = " → " + poslednyaya if i["proshla"] else "\n  ```\n  " + i["vyvod"].replace("\n", "\n  ") + "\n  ```"
    return "- %s %s: `%s`%s" % (znak, i["vid"], i["tekst"], hvost)


# счёт: «прошло из всего» по автоматическим проверкам круга
def schet(k):
    avto = [i for i in k["itogi"] if i["vid"] == "авто"]
    return "%d из %d" % (sum(i["proshla"] is True for i in avto), len(avto))


# отчёт: itog.md — модель, счёт по кругам, все проверки
def otchet(nastrojki, spisok, ruchnye):
    kt_model = nastrojki["imya_modeli"]
    stroki = ["# Итог: %s — %s" % (nastrojki["imya_zadaniya"], nastrojki["model"]), "",
              "- модель: `%s`" % kt_model, "- когда: " + datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
              "- первый круг: %s; последний круг (%d): %s" % (schet(spisok[0]), spisok[-1]["nomer"], schet(spisok[-1])), ""]
    for k in spisok:
        stroki += ["## Круг %d (токенов: %s; файлы: %s)" % (k["nomer"], k["tokeny"], ", ".join(k["fajly"]) or "нет"), ""]
        stroki += [stroka_itoga(i) for i in k["itogi"]] + [""]
    stroki += ["## Руками (учитель, по последнему кругу)", ""] + [stroka_itoga(i) for i in ruchnye]
    stroki += ["", "## Чтением (лист проверки — заполняет проверяющий)", "", "_не заполнено_", ""]
    (nastrojki["papka"] / "itog.md").write_text("\n".join(stroki), encoding="utf-8")


# настройки: всё, что нужно прогону, из аргументов командной строки
def nastrojki_progona(arg, modeli):
    zadanie = Path(arg.zadanie)
    tw = Path(arg.tw) if arg.tw else KOREN.parent / "teacher-workpad"
    dg = Path(arg.dg) if arg.dg else KOREN.parent / "drakon-graf"
    if not (tw / NAVYK).exists():
        raise ii.Oshibka("не найден навык: %s — склонируйте teacher-workpad рядом или укажите --tw" % (tw / NAVYK))
    if arg.model not in modeli["modeli"]:
        raise ii.Oshibka("нет модели %s в modeli.json" % arg.model)
    return {"zadanie": zadanie.read_text(encoding="utf-8"), "imya_zadaniya": zadanie.stem, "model": arg.model,
            "imya_modeli": modeli["modeli"][arg.model].get("model", "—"), "podstavit": arg.podstavit,
            "papka": KOREN / "testy" / zadanie.stem / arg.model, "puti": {"tw": tw, "dg": dg}}


# прогон: верхнее слово — настройки, круги, ручные проверки, отчёт
def progon(arg):
    modeli = ii.zagruzit_modeli(arg.modeli)
    znach, _ = ii.najti_klyuchi(ii.imena_peremennyh(modeli))
    kt = ii.Kontekst(modeli, znach, predel=KRUGOV)
    nastrojki = nastrojki_progona(arg, modeli)
    spisok = krugi(kt, nastrojki)
    puti = dict(nastrojki["puti"], otvet=spisok[-1]["papka"])
    ruchnye = proverit_rukami(nastrojki["zadanie"], puti, arg.bez_ruk)
    otchet(nastrojki, spisok, ruchnye)
    print("Готово → %s" % (nastrojki["papka"] / "itog.md"))
    return 0


# разбор: аргументы командной строки
def razbor(argv):
    p = argparse.ArgumentParser(description="Задание по коду — модели через Яндекс, ответ — на проверку.")
    p.add_argument("zadanie", help="файл задания (.md)")
    p.add_argument("--model", required=True, help="имя из modeli.json: alisa, deepseek")
    p.add_argument("--podstavit", nargs="+", help="без сети: файлы с готовыми ответами по кругам")
    p.add_argument("--bez-ruk", action="store_true", help="не задавать ручных проверок")
    p.add_argument("--tw", help="папка teacher-workpad (по умолчанию — рядом с ii-komanda)")
    p.add_argument("--dg", help="папка drakon-graf (по умолчанию — рядом с ii-komanda)")
    p.add_argument("--modeli", help="другой modeli.json")
    return p.parse_args(argv)


# кодировка: русские буквы и стрелки в консоли Windows
def kodirovka():
    for potok in (sys.stdout, sys.stderr):
        try:
            potok.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def main(argv=None):
    kodirovka()
    try:
        kod = progon(razbor(argv))
    except (ii.Oshibka, ii.Nerabochij) as e:
        print("ОСТАНОВКА:", e, file=sys.stderr)
        kod = 2
    return kod


if __name__ == "__main__":
    sys.exit(main())
