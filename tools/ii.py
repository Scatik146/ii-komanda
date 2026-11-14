#!/usr/bin/env python3
"""ii.py — сборка урока командой ИИ-помощников (алгоритм v9).

Устройство — ii-komanda/ii-py/USTROJSTVO.md. Один файл, только стандартная библиотека.
Скрипт работает с папкой урока на диске и ничего не знает про GitHub.
Ключи: переменные окружения → файл из II_ENV → ~/.ii-komanda.env → tools/.env.
Значения ключей не выводятся никогда.
"""
import argparse
import datetime
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

VERSIYA = "0.1 (14.11.2026)"
TOOLS = Path(__file__).resolve().parent
KOREN = TOOLS.parent
PROMPTY = KOREN / "algoritm" / "prompty"
PREDEL_PO_UMOLCHANIYU = 40
VERDIKTY = ("ПРИНЯТЬ", "ВЕРНУТЬ", "УЧИТЕЛЮ")
KODY = ("kanva", "shpargalka", "prilozhenie", "prezentaciya", "pechatnye", "vizual", "tehkarta")
ROL_ARTEFAKTA = {"kanva": "kanva", "prilozhenie": "prilozhenie", "prezentaciya": "kontent",
                 "pechatnye": "kontent", "shpargalka": "kontent", "tehkarta": "kontent", "vizual": "strazh"}
FAJL_ARTEFAKTA = {"kanva": "kanva.md", "shpargalka": "artefakty/shpargalka.html",
                  "prilozhenie": "artefakty/prilozhenie.html", "prezentaciya": "artefakty/prezentaciya.html",
                  "pechatnye": "artefakty/pechatnye.html", "tehkarta": "artefakty/tehkarta.md",
                  "vizual": "assets/vizual.md"}
DA = {"да", "+", "✓", "✔", "x", "х", "v", "всегда", "есть", "нужно"}


class Oshibka(Exception):
    """Остановка с понятной причиной (печатается учителю, без трассировки)."""


class Nerabochij(Exception):
    """Ответ модели нерабочий: пусто, отказ, обрезан, нет ожидаемого блока, сеть."""


# ---------- шаг 1: ключи и modeli.json ----------

def chitat_env(put):
    znacheniya = {}
    try:
        tekst = Path(put).read_text(encoding="utf-8-sig")
    except OSError:
        return znacheniya
    for stroka in tekst.splitlines():
        stroka = stroka.strip()
        if not stroka or stroka.startswith("#") or "=" not in stroka:
            continue
        imya, _, znach = stroka.partition("=")
        znach = znach.strip().strip('"').strip("'")
        if znach:
            znacheniya[imya.strip()] = znach
    return znacheniya


def najti_klyuchi(imena):
    """Ищет значения по порядку: окружение → II_ENV → ~/.ii-komanda.env → tools/.env.
    Возвращает {имя: значение} и {имя: откуда} (откуда — для экрана, без значения)."""
    istochniki = []
    if os.environ.get("II_ENV"):
        istochniki.append(Path(os.environ["II_ENV"]))
    istochniki.append(Path.home() / ".ii-komanda.env")
    istochniki.append(TOOLS / ".env")
    fajly = [(p, chitat_env(p)) for p in istochniki]
    znach, otkuda = {}, {}
    for imya in imena:
        if os.environ.get(imya):
            znach[imya], otkuda[imya] = os.environ[imya], "окружение"
            continue
        for p, d in fajly:
            if imya in d:
                znach[imya], otkuda[imya] = d[imya], str(p)
                break
    return znach, otkuda


def zagruzit_modeli(put=None):
    put = Path(put) if put else TOOLS / "modeli.json"
    try:
        dannye = json.loads(put.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise Oshibka("не читается %s: %s" % (put, e))
    for rol, spisok in dannye.get("roli", {}).items():
        for m in spisok:
            if m not in dannye.get("modeli", {}):
                raise Oshibka("в modeli.json роль %s ссылается на неизвестную модель %s" % (rol, m))
    return dannye


def imena_peremennyh(modeli):
    imena = set()
    for m in modeli["modeli"].values():
        if m.get("klyuch"):
            imena.add(m["klyuch"])
        for s in [m.get("adres", ""), m.get("model", "")] + list(m.get("zagolovki", {}).values()):
            imena.update(re.findall(r"\{([A-Z_]+)\}", s))
    return sorted(imena)


def raskryt(s, znach):
    def zamena(mt):
        if mt.group(1) not in znach:
            raise Oshibka("нет значения %s (нужно для %s)" % (mt.group(1), s))
        return znach[mt.group(1)]
    return re.sub(r"\{([A-Z_]+)\}", zamena, s)


# ---------- шаг 2: вызов модели, нерабочий ответ, повтор и замена, журнал ----------

class Kontekst:
    """Общее на одну команду: модели, ключи, урок, счётчик вызовов, режим без сети."""

    def __init__(self, modeli, klyuchi, urok=None, predel=PREDEL_PO_UMOLCHANIYU, bez_seti=False):
        self.modeli, self.klyuchi, self.urok = modeli, klyuchi, urok
        self.predel, self.vyzovov, self.bez_seti = predel, 0, bez_seti
        self.pometki = []  # для itog.md

    def zhurnal(self, shag, model, krug, verdikt, tokeny=""):
        stroka = "| %s | %s | %s | %s | %s | %s |" % (
            datetime.datetime.now().strftime("%d.%m %H:%M:%S"), shag, model, krug, verdikt, tokeny)
        if self.urok is None:
            print("журнал:", stroka)
            return
        put = self.urok / "proverka" / "zhurnal.md"
        put.parent.mkdir(parents=True, exist_ok=True)
        if not put.exists():
            put.write_text("# Журнал ii.py\n\n| время | шаг | модель | круг | вердикт | токены |\n|---|---|---|---|---|---|\n",
                           encoding="utf-8")
        with put.open("a", encoding="utf-8") as f:
            f.write(stroka + "\n")


def http_post(adres, zagolovki, telo, tajmaut=300):
    """Отдельная функция — её подменяют тесты."""
    zapros = urllib.request.Request(adres, data=json.dumps(telo).encode("utf-8"), method="POST")
    for k, v in zagolovki.items():
        zapros.add_header(k, v)
    with urllib.request.urlopen(zapros, timeout=tajmaut) as otvet:
        return json.loads(otvet.read().decode("utf-8"))


OTKAZY = ("я не могу помочь", "не могу выполнить", "i can't help", "i cannot help", "i'm sorry, but")


def razobrat_otvet(dannye, ozhidaem=None):
    """Текст и токены из ответа /chat/completions; Nerabochij — если ответ не годится."""
    try:
        vybor = dannye["choices"][0]
        tekst = vybor["message"].get("content") or ""
    except (KeyError, IndexError, TypeError, AttributeError):
        raise Nerabochij("нет choices[0].message в ответе")
    if vybor.get("finish_reason") == "length":
        raise Nerabochij("ответ обрезан (finish_reason: length)")
    if not tekst.strip():
        raise Nerabochij("пустой ответ")
    if any(o in tekst[:300].lower() for o in OTKAZY):
        raise Nerabochij("отказ модели")
    if ozhidaem and not ozhidaem(tekst):
        raise Nerabochij("нет ожидаемого блока")
    tokeny = (dannye.get("usage") or {}).get("total_tokens", "")
    return tekst, tokeny


def prichina_http(e):
    if isinstance(e, urllib.error.HTTPError):
        if e.code in (401, 403):
            return "ключ не принят (HTTP %d)" % e.code
        if e.code == 402:
            return "нет денег (HTTP 402)"
        if e.code == 429:
            return "лимит или нет денег (HTTP 429)"
        if e.code == 404:
            return "нет такой модели или адреса (HTTP 404)"
        return "ошибка поставщика (HTTP %d)" % e.code
    if isinstance(e, (urllib.error.URLError, TimeoutError, OSError)):
        return "ошибка сети (%s)" % getattr(e, "reason", e)
    return "ошибка: %s" % e


def odin_vyzov(kt, imya, tekst, ozhidaem=None, max_tokens=8000):
    m = kt.modeli["modeli"][imya]
    if m.get("vid") == "anthropic" or m.get("vklyuchen") is False:
        raise Nerabochij("модель выключена в modeli.json")
    if m.get("klyuch") not in kt.klyuchi:
        raise Nerabochij("нет ключа %s" % m.get("klyuch"))
    if kt.vyzovov >= kt.predel:
        raise Oshibka("достигнут предел вызовов (%d) — остановка, чтобы не тратить деньги" % kt.predel)
    kt.vyzovov += 1
    zagolovki = {"Content-Type": "application/json", "Authorization": "Bearer " + kt.klyuchi[m["klyuch"]]}
    for k, v in m.get("zagolovki", {}).items():
        zagolovki[k] = raskryt(v, kt.klyuchi)
    telo = {"model": raskryt(m["model"], kt.klyuchi), "messages": [{"role": "user", "content": tekst}],
            "max_tokens": max_tokens, "temperature": 0.3}
    try:
        dannye = http_post(m["adres"].rstrip("/") + "/chat/completions", zagolovki, telo)
    except Exception as e:  # сеть, HTTP, неразборчивый JSON
        raise Nerabochij(prichina_http(e))
    return razobrat_otvet(dannye, ozhidaem)


def vyzov(kt, rol, tekst, shag, krug=1, ozhidaem=None, krome=None):
    """Роль → первая работающая модель списка: один повтор той же моделью, затем следующая.
    krome — модель, которой нельзя (страж не автор). Возвращает (текст, модель, токены)."""
    spisok = kt.modeli["roli"].get(rol)
    if not spisok:
        raise Oshibka("в modeli.json нет роли %s" % rol)
    kandidaty = [m for m in spisok if m != krome] or list(spisok)
    if krome and kandidaty == list(spisok) and krome in spisok:
        kt.pometki.append("%s: страж = автор (%s), проверка слабая" % (shag, krome))
    prichiny = []
    for imya in kandidaty:
        for popytka in (1, 2):
            try:
                otvet, tokeny = odin_vyzov(kt, imya, tekst, ozhidaem)
                kt.zhurnal(shag, imya, krug, "ответ", tokeny)
                return otvet, imya, tokeny
            except Nerabochij as e:
                kt.zhurnal(shag, imya, krug, "НЕРАБОЧИЙ: %s" % e)
                prichiny.append("%s: %s" % (imya, e))
                if str(e).startswith(("нет ключа", "модель выключена")):
                    break  # повтор не поможет
    raise Nerabochij("; ".join(prichiny))


# ---------- шаг 3: klyuchi ----------

def komanda_klyuchi(arg):
    modeli = zagruzit_modeli(arg.modeli)
    znach, otkuda = najti_klyuchi(imena_peremennyh(modeli))
    print("Переменные (значения не показываются):")
    for imya in imena_peremennyh(modeli):
        print("  %-18s %s" % (imya, ("есть — " + otkuda[imya]) if imya in znach else "нет"))
    kt = Kontekst(modeli, znach, predel=len(modeli["modeli"]) * 2, bez_seti=arg.bez_seti)
    print("\n| модель | что | итог |\n|---|---|---|")
    for imya, m in modeli["modeli"].items():
        if m.get("vid") == "anthropic" or m.get("vklyuchen") is False:
            print("| %s | — | выключена |" % imya)
            continue
        if m.get("klyuch") not in znach:
            print("| %s | %s | нет ключа |" % (imya, m.get("model")))
            continue
        if arg.bez_seti:
            print("| %s | %s | ключ есть, проверка без сети не делалась |" % (imya, m.get("model")))
            continue
        try:
            otvet, tokeny = odin_vyzov(kt, imya, "Ответь одним словом: работает", max_tokens=20)
            print("| %s | %s | работает (%s ток.) |" % (imya, m.get("model"), tokeny))
        except (Nerabochij, Oshibka) as e:
            print("| %s | %s | %s |" % (imya, m.get("model"), e))
    if not arg.bez_seti and "YANDEX_API_KEY" in znach:
        spisok_modelej_yandeksa(znach)
    return 0


def spisok_modelej_yandeksa(znach):
    """Открытые модели в Yandex AI Studio — для запасного пути «всё через Яндекс»."""
    try:
        zapros = urllib.request.Request("https://ai.api.cloud.yandex.net/v1/models")
        zapros.add_header("Authorization", "Bearer " + znach["YANDEX_API_KEY"])
        if "YANDEX_FOLDER_ID" in znach:
            zapros.add_header("OpenAI-Project", znach["YANDEX_FOLDER_ID"])
        with urllib.request.urlopen(zapros, timeout=30) as o:
            dannye = json.loads(o.read().decode("utf-8"))
        imena = [d.get("id", "") for d in dannye.get("data", [])]
        print("\nМодели Яндекса (для modeli.json, запасной путь):\n  " + "\n  ".join(imena or ["список пуст"]))
    except Exception as e:
        print("\nСписок моделей Яндекса не получен:", prichina_http(e))


# ---------- шаг 4: папка урока, подстановки, набор; novyj, status ----------

SHABLON_ZAYAVKI = """# Заявка на урок

- Предмет, класс, группа (сколько учеников, особенности):
- Дата, время начала урока, длительность:
- Тема и место в модуле (что было до, что будет после):
- Условия кабинета (техника у учеников, проектор, печать, интернет):
- Что обязательно должно быть на уроке:
- Чего быть не должно:

## Набор артефактов (в последнем столбце — «да» у нужного)

| Код | Артефакт | В наборе |
|---|---|---|
| `kanva` | Канва урока | всегда |
| `shpargalka` | Шпаргалка учителя на урок | всегда |
| `prilozhenie` | Приложение (один HTML-файл) | |
| `prezentaciya` | Презентация (HTML) | |
| `pechatnye` | Печатные листы, бланки | |
| `vizual` | Картинки (сколько, в каком стиле) | |
| `tehkarta` | Технологическая карта | |
"""

SHABLON_RESHENIJ = """# Решения автора

Меняет только учитель. Вставляется дословно в каждый промпт.

## ИДЕЯ И МЕХАНИКА

## ЦЕЛИ И ПЛАНИРУЕМЫЕ РЕЗУЛЬТАТЫ

## РЕШЕНИЯ

## ОГРАНИЧЕНИЯ ГРУППЫ

## НЕ ДЕЛАТЬ

## ТЕРМИНЫ

## ДАЛЬШЕ
"""

FAJLY_PODSTANOVOK = {"ZAYAVKA": "zayavka.md", "RESHENIYA": "resheniya.md", "KANVA": "kanva.md",
                     "EKSPERTIZA": "ekspertiza.md", "SO_ANALIZ": "so-analiz.md"}


def put_uroka(tekst, dolzhen_byt=True):
    p = Path(tekst).expanduser().resolve()
    if dolzhen_byt and not (p / "zayavka.md").exists():
        raise Oshibka("в %s нет zayavka.md — это не папка урока (создать: ii.py novyj <папка>)" % p)
    return p


def prochitat_prompt(kod):
    """Текст промпта после строки «---» (шапка — для людей, в модель не идёт)."""
    put = PROMPTY / (kod + ".md")
    try:
        tekst = put.read_text(encoding="utf-8")
    except OSError:
        raise Oshibka("нет промпта %s" % put)
    chasti = re.split(r"^---\s*$", tekst, maxsplit=1, flags=re.M)
    return (chasti[1] if len(chasti) == 2 else tekst).strip() + "\n"


def podstavit(tekst, urok, dop=None):
    """Заменяет {{ИМЯ}}. Не найдено или пусто — Oshibka, а не пустая строка."""
    dop = dop or {}

    def zamena(mt):
        imya = mt.group(1)
        if imya in dop:
            znach = dop[imya]
        elif imya == "SHABLON_TEHKARTY":
            p = urok / "shablon-tehkarty.md"
            znach = p.read_text(encoding="utf-8") if p.exists() else "(шаблона школы нет)"
        elif imya in FAJLY_PODSTANOVOK:
            p = urok / FAJLY_PODSTANOVOK[imya]
            if not p.exists():
                raise Oshibka("подстановка {{%s}}: нет файла %s" % (imya, p))
            znach = p.read_text(encoding="utf-8")
            if imya == "ZAYAVKA" and znach.strip() == SHABLON_ZAYAVKI.strip():
                raise Oshibka("zayavka.md не заполнена")
            if imya == "RESHENIYA" and znach.strip() == SHABLON_RESHENIJ.strip():
                raise Oshibka("resheniya.md не заполнены")
        else:
            raise Oshibka("неизвестная подстановка {{%s}}" % imya)
        if not str(znach).strip():
            raise Oshibka("подстановка {{%s}} пустая" % imya)
        if str(znach).startswith("ОТВЕТ НЕРАБОЧИЙ"):
            raise Oshibka("подстановка {{%s}}: в файле нерабочий ответ — сначала переделать" % imya)
        return str(znach).strip()

    return re.sub(r"\{\{([A-Z_]+)\}\}", zamena, tekst)


def nabor_iz_zayavki(urok):
    """Набор артефактов: строка «Набор: …» или отметки в таблице заявки. kanva и shpargalka — всегда."""
    tekst = (urok / "zayavka.md").read_text(encoding="utf-8")
    nabor = []
    mt = re.search(r"^\s*(?:[-*]\s*)?(?:Набор|Ветка урока)\s*:\s*(.+)$", tekst, flags=re.M | re.I)
    if mt:
        nabor = [k for k in re.findall(r"[a-z]+", mt.group(1)) if k in KODY]
    else:
        for stroka in tekst.splitlines():
            yachejki = [y.strip() for y in stroka.strip().strip("|").split("|")]
            if len(yachejki) >= 3:
                kod = yachejki[0].strip("`* ")
                if kod in KODY and yachejki[-1].strip("*` ").lower() in DA:
                    nabor.append(kod)
    for k in ("shpargalka", "kanva"):
        if k not in nabor:
            nabor.insert(0, k)
    return [k for k in KODY if k in nabor]


def komanda_novyj(arg):
    urok = put_uroka(arg.urok, dolzhen_byt=False)
    if (urok / "zayavka.md").exists():
        raise Oshibka("%s уже есть — не перезаписываю" % (urok / "zayavka.md"))
    for papka in ("artefakty", "assets", "vydacha", "proverka"):
        (urok / papka).mkdir(parents=True, exist_ok=True)
    (urok / "zayavka.md").write_text(SHABLON_ZAYAVKI, encoding="utf-8")
    (urok / "resheniya.md").write_text(SHABLON_RESHENIJ, encoding="utf-8")
    print("Создана папка урока:", urok, "\nЗаполнить zayavka.md и resheniya.md, затем: ii.py ekspertiza", urok)
    return 0


def verdikt_iz_fajla(p):
    if not p.exists():
        return None
    return najti_verdikt(p.read_text(encoding="utf-8"))


def komanda_status(arg):
    urok = put_uroka(arg.urok)
    print("Урок:", urok)
    print("Набор:", ", ".join(nabor_iz_zayavki(urok)))
    for imya in ("zayavka.md", "resheniya.md", "ekspertiza.md", "so-analiz.md"):
        p = urok / imya
        sost = "нет" if not p.exists() else ("НЕРАБОЧИЙ" if p.read_text(encoding="utf-8").startswith("ОТВЕТ НЕРАБОЧИЙ") else "есть")
        print("  %-16s %s" % (imya, sost))
    for kod in nabor_iz_zayavki(urok):
        p = urok / FAJL_ARTEFAKTA[kod]
        v = verdikt_iz_fajla(urok / "proverka" / (kod + "-strazh.md"))
        print("  %-16s %-5s страж: %s" % (kod, "есть" if p.exists() else "нет", v or "—"))
    zapr = sorted((urok / "proverka").glob("*-zapros.md")) if (urok / "proverka").exists() else []
    if zapr:
        print("Собранные запросы:", ", ".join(z.name for z in zapr))
    return 0


# ---------- шаг 5: проверка окружения ----------

ZAGLUSHKI = ("TODO", "пример текста", "Lorem", "lorem ipsum", "здесь будет", "…</", ">…<", "...</")
NOVOE_ES = [(r"\?\.[A-Za-z_$\[(]", "?. (новее ES2018)"), (r"\?\?=?", "?? (новее ES2018)"),
            (r"(?<![\w$])#[A-Za-z_]\w*\s*[=;(]", "#поле класса (новее ES2018)"),
            (r"\.replaceAll\(", "replaceAll (новее ES2018)"), (r"\.at\(", ".at( (новее ES2018)")]


def skripty_iz_html(html):
    return "\n".join(re.findall(r"<script\b[^>]*>(.*?)</script>", html, flags=re.S | re.I))


def proverit_okruzhenie(html, imya_fajla, tonkij=True, kartinki=None):
    """Список нарушений (пустой — всё хорошо). tonkij: файл из artefakty/, ссылки на assets/ можно."""
    oshibki = []
    if not re.fullmatch(r"[a-z0-9_.-]+", imya_fajla):
        oshibki.append("имя файла не латиницей: %s" % imya_fajla)
    for mt in re.finditer(r"https?://|//cdn", html, flags=re.I):
        kusok = html[max(0, mt.start() - 30):mt.start() + 40].replace("\n", " ")
        if "xmlns" in kusok or "www.w3.org" in kusok:
            continue  # пространства имён SVG — не ссылки наружу
        oshibki.append("ссылка наружу: …%s…" % kusok.strip())
    for mt in re.finditer(r"""(?:src|href)\s*=\s*["']([^"'#][^"']*)["']""", html, flags=re.I):
        ssylka = mt.group(1)
        if ssylka.startswith(("data:", "javascript:", "mailto:")):
            continue
        if tonkij and re.fullmatch(r"assets/[a-z0-9_.-]+\.jpg", ssylka):
            if kartinki is not None and Path(ssylka).name not in kartinki:
                oshibki.append("картинка %s не заказана в блоке «КАРТИНКИ»" % ssylka)
            continue
        if not ssylka.startswith(("http", "//")):  # http уже учтены выше
            oshibki.append("внешний файл: %s" % ssylka)
    if re.search(r"@import|\bfetch\s*\(|<link\b[^>]*stylesheet", html, flags=re.I):
        oshibki.append("подключение извне (@import / fetch / link stylesheet)")
    for z in ZAGLUSHKI:
        if z.lower() in html.lower():
            oshibki.append("заглушка: «%s»" % z)
    kod = skripty_iz_html(html)
    for shablon, chto in NOVOE_ES:
        if re.search(shablon, kod):
            oshibki.append(chto)
    if not tonkij and "assets/" in html:
        oshibki.append("в выдаче осталась ссылка на assets/")
    return oshibki


def zakazy_kartinok(tekst):
    """Имена файлов из блока «КАРТИНКИ» в конце ответа исполнителя."""
    mt = re.search(r"КАРТИНКИ\s*:?(.*)$", tekst, flags=re.S)
    return set(re.findall(r"[a-z0-9_-]+\.jpg", mt.group(1))) if mt else set()


# ---------- шаг 6: страж и круги; proverka ----------

def najti_verdikt(tekst):
    """Первая строка, где после разметки стоит ПРИНЯТЬ / ВЕРНУТЬ / УЧИТЕЛЮ."""
    for stroka in tekst.splitlines():
        chistaya = re.sub(r"^[\s>*#`\d.)-]*(?:Вердикт\s*:?\s*)?[*`\s]*", "", stroka, flags=re.I)
        for v in VERDIKTY:
            if chistaya.startswith(v):
                return v
    return None


def strazh(kt, kod, rezultat, avtor=None, krug=1):
    urok = kt.urok
    tekst = podstavit(prochitat_prompt("strazh"), urok, {"KOD": kod, "REZULTAT": rezultat})
    if kt.bez_seti:
        sohranit_zapros(urok, kod + "-strazh", tekst)
        return None
    otvet, model, _ = vyzov(kt, "strazh", tekst, "strazh " + kod, krug, ozhidaem=najti_verdikt, krome=avtor)
    (urok / "proverka" / (kod + "-strazh.md")).write_text(otvet, encoding="utf-8")
    v = najti_verdikt(otvet)
    kt.zhurnal("strazh " + kod, model, krug, v)
    return v


def sohranit_zapros(urok, imya, tekst):
    p = urok / "proverka" / (imya + "-zapros.md")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(tekst, encoding="utf-8")
    print("Без сети: собранный промпт —", p)
    return p


def napisat_itog(kt, stroki):
    p = kt.urok / "proverka" / "itog.md"
    vse = ["# Итог для учителя (СТОП 3) — %s" % datetime.datetime.now().strftime("%d.%m.%Y %H:%M"), ""]
    vse += ["- " + s for s in stroki + kt.pometki] or ["- замечаний нет"]
    p.write_text("\n".join(vse) + "\n", encoding="utf-8")
    print("Итог —", p)


def komanda_proverka(arg):
    kt = sozdat_kontekst(arg)
    urok = kt.urok
    kody = [arg.kod] if arg.kod else nabor_iz_zayavki(urok)
    itog = []
    for kod in kody:
        p = urok / FAJL_ARTEFAKTA[kod]
        if not p.exists():
            itog.append("%s: файла %s нет" % (kod, p.relative_to(urok)))
            continue
        rezultat = p.read_text(encoding="utf-8")
        if kod in ("prilozhenie", "prezentaciya"):
            oshibki = proverit_okruzhenie(rezultat, p.name, tonkij=True, kartinki=zakazy_kartinok(rezultat) or None)
            (urok / "proverka" / (kod + "-okruzhenie.md")).write_text(
                "# Окружение: %s\n\n" % p.name + ("\n".join("- " + o for o in oshibki) or "нарушений нет") + "\n",
                encoding="utf-8")
            if oshibki:
                kt.zhurnal("okruzhenie " + kod, "скрипт", 1, "ВЕРНУТЬ")
                itog.append("%s: окружение — ВЕРНУТЬ (%d нарушений, proverka/%s-okruzhenie.md)" % (kod, len(oshibki), kod))
                continue
        try:
            v = strazh(kt, kod, rezultat)
        except Nerabochij as e:
            itog.append("%s: страж не ответил — %s" % (kod, e))
            continue
        if v is None:
            itog.append("%s: прогон без сети — запрос стража собран, вердикта нет" % kod)
        elif v != "ПРИНЯТЬ":
            itog.append("%s: страж — %s (proverka/%s-strazh.md)" % (kod, v, kod))
    napisat_itog(kt, itog)
    return 0


# ---------- шаг 7 (часть): ekspertiza, zapros ----------

def sozdat_kontekst(arg, urok=True):
    modeli = zagruzit_modeli(arg.modeli)
    znach, _ = najti_klyuchi(imena_peremennyh(modeli))
    return Kontekst(modeli, znach, put_uroka(arg.urok) if urok else None,
                    predel=arg.predel, bez_seti=arg.bez_seti)


def shag_promptom(kt, kod, rol, vyhod, dop=None):
    """Один шаг: промпт + подстановки → модель → файл. Без сети — только собранный промпт."""
    tekst = podstavit(prochitat_prompt(kod), kt.urok, dop)
    if kt.bez_seti:
        sohranit_zapros(kt.urok, kod, tekst)
        kt.zhurnal(kod, "—", 1, "без сети: запрос собран, модель не вызывалась")
        return None
    (kt.urok / "proverka").mkdir(exist_ok=True)
    (kt.urok / "proverka" / (kod + "-zapros.md")).write_text(tekst, encoding="utf-8")
    try:
        otvet, model, _ = vyzov(kt, rol, tekst, kod)
    except Nerabochij as e:
        vyhod.write_text("ОТВЕТ НЕРАБОЧИЙ: %s\n" % e, encoding="utf-8")
        raise Oshibka("%s: ни одна модель не дала рабочего ответа — %s (файл %s)" % (kod, e, vyhod.name))
    vyhod.write_text(otvet, encoding="utf-8")
    print("%s: готово (%s) → %s" % (kod, model, vyhod))
    return model


def komanda_ekspertiza(arg):
    kt = sozdat_kontekst(arg)
    shag_promptom(kt, "ekspertiza", "ekspertiza", kt.urok / "ekspertiza.md")
    if kt.bez_seti:
        print("Со-анализ не собран: ему нужен ответ экспертизы ({{EKSPERTIZA}}), а без сети его нет.")
        return 0
    shag_promptom(kt, "so-analiz", "so_analiz", kt.urok / "so-analiz.md")
    print("СТОП 2: прочитать so-analiz.md, принять / отклонить замечания, поправить resheniya.md.")
    return 0


def komanda_zapros(arg):
    kt = sozdat_kontekst(arg, urok=False)
    tekst = Path(arg.prompt).read_text(encoding="utf-8")
    if kt.bez_seti:
        print("Без сети: запрос не отправлен (%d знаков)." % len(tekst))
        return 0
    otvet, model, tokeny = vyzov(kt, arg.rol, tekst, "zapros")
    Path(arg.vyhod).write_text(otvet, encoding="utf-8")
    print("Готово (%s, %s ток.) → %s" % (model, tokeny, arg.vyhod))
    return 0


def ne_sdelano(arg):
    raise Oshibka("команда %s ещё не написана (план USTROJSTVO.md § 8, шаги 7–8 — следующий чат)" % arg.komanda)


# ---------- разбор команд ----------

def razbor(argv=None):
    p = argparse.ArgumentParser(prog="ii.py", description="Сборка урока командой ИИ (v9). Версия " + VERSIYA)
    obshchie = argparse.ArgumentParser(add_help=False)
    obshchie.add_argument("--bez-seti", action="store_true", help="не вызывать модели: собранный промпт — в proverka/<шаг>-zapros.md")
    obshchie.add_argument("--modeli", help="другой modeli.json")
    obshchie.add_argument("--predel", type=int, default=PREDEL_PO_UMOLCHANIYU, help="предел вызовов (40)")
    k = p.add_subparsers(dest="komanda", required=True)
    k.add_parser("klyuchi", parents=[obshchie], help="проверить ключи и модели").set_defaults(f=komanda_klyuchi)
    for imya, f, pomoshch in (("novyj", komanda_novyj, "создать папку урока"),
                              ("ekspertiza", komanda_ekspertiza, "шаг 3: экспертиза → со-анализ"),
                              ("status", komanda_status, "где урок")):
        s = k.add_parser(imya, parents=[obshchie], help=pomoshch)
        s.add_argument("urok", help="путь к папке урока")
        s.set_defaults(f=f)
    s = k.add_parser("proverka", parents=[obshchie], help="окружение + страж")
    s.add_argument("urok")
    s.add_argument("kod", nargs="?", choices=KODY)
    s.set_defaults(f=komanda_proverka)
    s = k.add_parser("zapros", parents=[obshchie], help="один промпт в одну роль")
    s.add_argument("--rol", required=True)
    s.add_argument("--prompt", required=True)
    s.add_argument("--vyhod", required=True)
    s.set_defaults(f=komanda_zapros, urok=None)
    for imya in ("sborka", "vernut", "kartinki", "vydacha"):
        s = k.add_parser(imya, parents=[obshchie], help="(ещё не написана)")
        s.add_argument("ostalnoe", nargs="*")
        s.set_defaults(f=ne_sdelano)
    return p.parse_args(argv)


def main(argv=None):
    for potok in (sys.stdout, sys.stderr):
        try:
            potok.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    arg = razbor(argv)
    try:
        return arg.f(arg)
    except Oshibka as e:
        print("ОСТАНОВКА:", e, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
