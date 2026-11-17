#!/usr/bin/env python3
"""ii.py — сборка урока командой ИИ-помощников (алгоритм v9).

Устройство — ii-komanda/ii-py/USTROJSTVO.md. Один файл, только стандартная библиотека.
Скрипт работает с папкой урока на диске и ничего не знает про GitHub.
Ключи: переменные окружения → файл из II_ENV → ~/.ii-komanda.env → tools/.env.
Значения ключей не выводятся никогда.
"""
import argparse
import base64
import datetime
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

VERSIYA = "0.2.7 (17.11.2026)"
TOOLS = Path(__file__).resolve().parent
KOREN = TOOLS.parent
PROMPTY = KOREN / "algoritm" / "prompty"
PREDEL_PO_UMOLCHANIYU = 40
VERDIKTY = ("ПРИНЯТЬ", "ВЕРНУТЬ", "УЧИТЕЛЮ")
KODY = ("kanva", "shpargalka", "prilozhenie", "prezentaciya", "pechatnye", "vizual", "tehkarta")
ROL_ARTEFAKTA = {"kanva": "kanva", "prilozhenie": "prilozhenie", "prezentaciya": "kontent",
                 "pechatnye": "kontent", "shpargalka": "kontent", "tehkarta": "kontent", "vizual": "vizual"}
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


# рассуждение: убирает из ответа блок <think>…</think> (DeepSeek, Qwen рассуждают по умолчанию)
def ubrat_rassuzhdenie(tekst):
    bez_bloka = re.sub(r"<think>.*?</think>", "", tekst, flags=re.S)
    return bez_bloka.strip()


# обрезка: объясняет, почему ответ обрезан — съело ли лимит рассуждение
def prichina_obrezki(soobshchenie, tekst):
    prichina = "ответ обрезан (finish_reason: length)"
    if soobshchenie.get("reasoning_content") and not tekst:
        prichina = "рассуждение съело лимит max_tokens, результата нет (увеличить max_tokens в modeli.json)"
    return prichina


def razobrat_otvet(dannye, ozhidaem=None):
    """Текст и токены из ответа /chat/completions; Nerabochij — если ответ не годится."""
    try:
        vybor = dannye["choices"][0]
        tekst = ubrat_rassuzhdenie(vybor["message"].get("content") or "")
    except (KeyError, IndexError, TypeError, AttributeError):
        raise Nerabochij("нет choices[0].message в ответе")
    if vybor.get("finish_reason") == "length":
        raise Nerabochij(prichina_obrezki(vybor["message"], tekst))
    if not tekst.strip():
        raise Nerabochij("пустой ответ")
    if any(o in tekst[:300].lower() for o in OTKAZY):
        raise Nerabochij("отказ модели")
    if ozhidaem and not ozhidaem(tekst):
        raise Nerabochij("нет ожидаемого блока")
    tokeny = (dannye.get("usage") or {}).get("total_tokens", "")
    return tekst, tokeny


# тело ошибки: первые 200 знаков ответа поставщика — чтобы видеть, что не так в запросе
def telo_oshibki(e):
    kusok = ""
    try:
        kusok = e.read().decode("utf-8", "replace")[:200]
    except Exception:
        kusok = ""
    if kusok:
        kusok = ": " + kusok.replace("\n", " ")
    return kusok


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
        return "ошибка поставщика (HTTP %d)%s" % (e.code, telo_oshibki(e))
    if isinstance(e, (urllib.error.URLError, TimeoutError, OSError)):
        return "ошибка сети (%s)" % getattr(e, "reason", e)
    return "ошибка: %s" % e


# ручная модель: работает через учителя (GLM), по API не вызывается
def vruchnuyu(m):
    return m.get("vid") == "vruchnuyu"


# лимит токенов: свой у модели (рассуждающей нужно больше), иначе — переданный
def limit_tokenov(m, max_tokens):
    limit = max_tokens
    if limit is None:
        limit = m.get("max_tokens", 8000)
    return limit


def odin_vyzov(kt, imya, tekst, ozhidaem=None, max_tokens=None):
    m = kt.modeli["modeli"][imya]
    if vruchnuyu(m):
        raise Nerabochij("модель вручную через учителя, не по API")
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
            "max_tokens": limit_tokenov(m, max_tokens), "temperature": 0.3}
    telo.update(m.get("telo_dop", {}))
    try:
        dannye = http_post(m["adres"].rstrip("/") + "/chat/completions", zagolovki, telo, m.get("tajmaut", 300))
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
                if str(e).startswith(("нет ключа", "модель выключена", "модель вручную")):
                    break  # повтор не поможет
    raise Nerabochij("; ".join(prichiny))


# ---------- шаг 3: klyuchi ----------

# проба: сколько токенов дать на пробный вызов (рассуждающей модели — с запасом)
def tokenov_dlya_proby(m):
    tokenov = 20
    if m.get("rassuzhdenie"):
        tokenov = 2000
    return tokenov


def komanda_klyuchi(arg):
    modeli = zagruzit_modeli(arg.modeli)
    znach, otkuda = najti_klyuchi(imena_peremennyh(modeli))
    print("Переменные (значения не показываются):")
    for imya in imena_peremennyh(modeli):
        print("  %-18s %s" % (imya, ("есть — " + otkuda[imya]) if imya in znach else "нет"))
    kt = Kontekst(modeli, znach, predel=len(modeli["modeli"]) * 2, bez_seti=arg.bez_seti)
    print("\n| модель | что | итог |\n|---|---|---|")
    for imya, m in modeli["modeli"].items():
        if vruchnuyu(m):
            print("| %s | — | вручную через учителя (ekspertiza) |" % imya)
            continue
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
            otvet, tokeny = odin_vyzov(kt, imya, "Ответь одним словом: работает", max_tokens=tokenov_dlya_proby(m))
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


def prochitat_prompt_iz(put):
    """prochitat_prompt_iz: текст файла после шапки «---…---»."""
    chasti = re.split(r"^---\s*$", put.read_text(encoding="utf-8"), maxsplit=2, flags=re.M)
    return chasti[-1].strip() + "\n"


def podstavit(tekst, urok, dop=None):
    """Заменяет {{ИМЯ}}. Не найдено или пусто — Oshibka, а не пустая строка."""
    dop = dop or {}

    def zamena(mt):
        imya = mt.group(1)
        if imya in dop:
            znach = dop[imya]
        elif imya == "STILI":
            # стили: три стиля кода команды — навык tri-stilya-koda без шапки (решение учителя 17.11)
            znach = prochitat_prompt_iz(KOREN / "rezerv" / "navyki" / "tri-stilya-koda" / "SKILL.md")
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


PROVERKA_OKRUZHENIYA = ("prilozhenie", "prezentaciya")


# заказы артефакта: имена картинок из artefakty/<код>-kartinki.md (или из самого файла, как в 0.1)
def zakazy_artefakta(urok, kod):
    p = urok / "artefakty" / (kod + "-kartinki.md")
    if not p.exists():
        p = urok / FAJL_ARTEFAKTA[kod]
    zakazy = zakazy_kartinok(p.read_text(encoding="utf-8"))
    if not zakazy:
        zakazy = None
    return zakazy


# окружение артефакта: проверяет тонкий файл и пишет отчёт proverka/<код>-okruzhenie.md
def okruzhenie_artefakta(urok, kod):
    p = urok / FAJL_ARTEFAKTA[kod]
    oshibki = proverit_okruzhenie(p.read_text(encoding="utf-8"), p.name, tonkij=True, kartinki=zakazy_artefakta(urok, kod))
    spisok = "\n".join("- " + o for o in oshibki) or "нарушений нет"
    otchet = urok / "proverka" / (kod + "-okruzhenie.md")
    otchet.parent.mkdir(parents=True, exist_ok=True)
    otchet.write_text("# Окружение: %s\n\n%s\n" % (p.name, spisok), encoding="utf-8")
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


# задание исполнителю: раздел «## Задание» из промпта кода — страж видит, что требовалось
def zadanie_ispolnitelyu(kod):
    tekst = prochitat_prompt(kod)
    nachalo = tekst.find("## Задание")
    razdel = "(раздела «Задание» в промпте нет)"
    if nachalo >= 0:
        konec = tekst.find("\n## ", nachalo + 1)
        if konec < 0:
            konec = len(tekst)
        razdel = tekst[nachalo:konec].strip()
    return razdel


# уточнить вердикт: ВЕРНУТЬ без «критично» в ответе — это ПРИНЯТЬ (возврат только за критичное)
def utochnit_verdikt(otvet, verdikt):
    itog = verdikt
    if verdikt == "ВЕРНУТЬ" and "критично" not in otvet.lower():
        itog = "ПРИНЯТЬ"
    return itog


def strazh(kt, kod, rezultat, avtor=None, krug=1):
    urok = kt.urok
    dop = {"KOD": kod, "REZULTAT": rezultat, "ZADANIE_ISPOLNITELYU": zadanie_ispolnitelyu(kod)}
    tekst = podstavit(prochitat_prompt("strazh"), urok, dop)
    if kt.bez_seti:
        sohranit_zapros(urok, kod + "-strazh", tekst)
        return None
    otvet, model, _ = vyzov(kt, "strazh", tekst, "strazh " + kod, krug, ozhidaem=najti_verdikt, krome=avtor)
    v = utochnit_verdikt(otvet, najti_verdikt(otvet))
    if v != najti_verdikt(otvet):
        otvet = "ПРИНЯТЬ — скрипт: «критично» в таблице нет, ВЕРНУТЬ стража заменён на ПРИНЯТЬ (решение учителя 15.11)\n\n" + otvet
    (urok / "proverka" / (kod + "-strazh.md")).write_text(otvet, encoding="utf-8")
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
        if kod in PROVERKA_OKRUZHENIYA:
            oshibki = okruzhenie_artefakta(urok, kod)
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
        elif stroka_pozhelanij(urok, kod, v):
            itog.append(stroka_pozhelanij(urok, kod, v))
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


PAKET_GLM = "ekspertiza-dlya-glm.md"


# пакет GLM: собирает промпт экспертизы в файл — учитель копирует его в чат GLM целиком
def podgotovit_paket_glm(urok):
    tekst = podstavit(prochitat_prompt("ekspertiza"), urok)
    p = urok / "proverka" / PAKET_GLM
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(tekst, encoding="utf-8")
    return p


# ответ GLM: переносит ответ из файла учителя в ekspertiza.md
def prinyat_otvet_glm(urok, put):
    tekst = Path(put).read_text(encoding="utf-8-sig").strip()
    if not tekst:
        raise Oshibka("файл с ответом GLM пустой: %s" % put)
    (urok / "ekspertiza.md").write_text(tekst + "\n", encoding="utf-8")
    return urok / "ekspertiza.md"


# ответ есть: в ekspertiza.md лежит настоящий ответ, не пусто и не «нерабочий»
def otvet_glm_est(urok):
    p = urok / "ekspertiza.md"
    est = False
    if p.exists():
        tekst = p.read_text(encoding="utf-8").strip()
        est = bool(tekst) and not tekst.startswith("ОТВЕТ НЕРАБОЧИЙ")
    return est


# подсказка: что сделать учителю с пакетом GLM
def podskazka_glm(paket, urok):
    print("Пакет для GLM:", paket)
    print("1) Открыть файл, скопировать всё в чат GLM.")
    print("2) Ответ GLM сохранить в файл (например ответ-glm.md).")
    print("3) Запустить: ii.py ekspertiza %s --otvet ответ-glm.md" % urok)


def komanda_ekspertiza(arg):
    kt = sozdat_kontekst(arg)
    if arg.otvet:
        print("Ответ GLM принят →", prinyat_otvet_glm(kt.urok, arg.otvet))
    if not otvet_glm_est(kt.urok):
        podskazka_glm(podgotovit_paket_glm(kt.urok), kt.urok)
        kt.zhurnal("ekspertiza", "glm (вручную)", 1, "пакет собран, ждём ответ учителя")
        return 0
    shag_promptom(kt, "so-analiz", "so_analiz", kt.urok / "so-analiz.md")
    if not kt.bez_seti:
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


# ---------- шаг 7: sborka (0.2 — последовательно, по шагам v9), vernut ----------
# Данные:
#   nabor   — список кодов из заявки, например ["kanva", "shpargalka", "prilozhenie"]
#   otvet   — текст модели; для HTML-кодов: HTML (можно в ```html … ```) + блок «КАРТИНКИ»
#   verdikt — "ПРИНЯТЬ" | "ВЕРНУТЬ" | "УЧИТЕЛЮ" | "НЕРАБОЧИЙ"
#   itog    — список строк для proverka/itog.md

HTML_KODY = ("shpargalka", "prilozhenie", "prezentaciya", "pechatnye")
VOLNA_2 = ("shpargalka", "prilozhenie", "prezentaciya", "pechatnye")
VOLNA_3 = ("vizual", "tehkarta")


# круги: сколько кругов стража положено артефакту (канва — 2, остальные — 3)
def krugov(kod):
    chislo = 3
    if kod == "kanva":
        chislo = 2
    return chislo


# шаги сборки: порядок v9 — канва, волна 2, волна 3; только то, что в наборе
def shagi_sborki(nabor):
    poryadok = ("kanva",) + VOLNA_2 + VOLNA_3
    return [kod for kod in poryadok if kod in nabor]


# вырезать HTML: из ```html … ``` или от <!DOCTYPE / <html до </html>; нет — None
def vyrezat_html(otvet):
    html = None
    blok = re.search(r"```html\s*\n(.*?)```", otvet, flags=re.S | re.I)
    if blok:
        html = blok.group(1).strip()
    else:
        celyj = re.search(r"(<!DOCTYPE html.*?</html>|<html.*?</html>)", otvet, flags=re.S | re.I)
        if celyj:
            html = celyj.group(1).strip()
    return html


# блок картинок: текст от слова «КАРТИНКИ» до конца ответа; нет — пусто
def blok_kartinok(otvet):
    blok = ""
    mesto = otvet.rfind("КАРТИНКИ")
    if mesto >= 0:
        blok = otvet[mesto:].strip()
    return blok


# ожидаемое: какой ответ годится для кода (HTML-кодам нужен HTML, стражу — вердикт)
def ozhidaemoe(kod):
    proverka = None
    if kod in HTML_KODY:
        proverka = vyrezat_html
    return proverka


# записать артефакт: основной файл + для HTML — artefakty/<код>-kartinki.md
def zapisat_artefakt(urok, kod, otvet):
    p = urok / FAJL_ARTEFAKTA[kod]
    p.parent.mkdir(parents=True, exist_ok=True)
    if kod in HTML_KODY:
        p.write_text(vyrezat_html(otvet) + "\n", encoding="utf-8")
        kartinki = blok_kartinok(otvet) or "КАРТИНКИ: нет"
        (urok / "artefakty" / (kod + "-kartinki.md")).write_text(kartinki + "\n", encoding="utf-8")
    else:
        p.write_text(otvet.strip() + "\n", encoding="utf-8")
    return p


# все заказы: блоки «КАРТИНКИ» артефактов волны 2 — для {{KARTINKI}}
def vse_zakazy(urok):
    bloki = []
    for kod in VOLNA_2:
        p = urok / "artefakty" / (kod + "-kartinki.md")
        if p.exists():
            bloki.append("%s:\n%s" % (kod, p.read_text(encoding="utf-8").strip()))
    return "\n\n".join(bloki)


# основа промпта: промпт кода с подстановками (vizual получает заказы картинок)
def osnova_prompta(urok, kod):
    dop = {}
    if kod == "vizual":
        dop["KARTINKI"] = vse_zakazy(urok) or "нет"
    return podstavit(prochitat_prompt(kod), urok, dop)


# текст круга: основа + прошлый результат + что исправить
def tekst_kruga(osnova, proshlyj, pravki):
    return (osnova + "\n\n## Прошлый результат\n\n" + proshlyj.strip() +
            "\n\n## Что исправить\n\n" + pravki.strip() +
            "\n\nИсправь и дай результат целиком, в том же формате.\n")


# сделать: один вызов исполнителя по роли кода → файл; возвращает модель-автора
def sdelat(kt, kod, tekst, krug):
    otvet, model, _ = vyzov(kt, ROL_ARTEFAKTA[kod], tekst, kod, krug, ozhidaem=ozhidaemoe(kod))
    zapisat_artefakt(kt.urok, kod, otvet)
    return model


# проверить: окружение (без стража при ошибках), затем страж; → (вердикт, правки)
def proverit(kt, kod, avtor, krug):
    if kod in PROVERKA_OKRUZHENIYA:
        oshibki = okruzhenie_artefakta(kt.urok, kod)
        if oshibki:
            kt.zhurnal("okruzhenie " + kod, "скрипт", krug, "ВЕРНУТЬ")
            return "ВЕРНУТЬ", "Проверка окружения:\n" + "\n".join("- " + o for o in oshibki)
    rezultat = (kt.urok / FAJL_ARTEFAKTA[kod]).read_text(encoding="utf-8")
    verdikt = strazh(kt, kod, rezultat, avtor=avtor, krug=krug)
    pravki = (kt.urok / "proverka" / (kod + "-strazh.md")).read_text(encoding="utf-8")
    return verdikt, pravki


# один круг: сделать и проверить; → (вердикт, правки)
def odin_krug(kt, kod, tekst, krug):
    avtor = sdelat(kt, kod, tekst, krug)
    return proverit(kt, kod, avtor, krug)


# круги артефакта: до krugov(kod) раз, пока страж возвращает; proshlyj/pravki — для vernut
def krugi(kt, kod, proshlyj=None, pravki=None):
    osnova = osnova_prompta(kt.urok, kod)
    verdikt, krug = "ВЕРНУТЬ", 0
    while verdikt == "ВЕРНУТЬ" and krug < krugov(kod):
        krug += 1
        tekst = osnova
        if proshlyj is not None:
            tekst = tekst_kruga(osnova, proshlyj, pravki)
        verdikt, pravki = odin_krug(kt, kod, tekst, krug)
        proshlyj = (kt.urok / FAJL_ARTEFAKTA[kod]).read_text(encoding="utf-8")
    return verdikt, krug


# собрать один: круги с перехватом нерабочего ответа; → (вердикт, круг)
def sobrat_odin(kt, kod, proshlyj=None, pravki=None):
    try:
        verdikt, krug = krugi(kt, kod, proshlyj, pravki)
    except Nerabochij as e:
        (kt.urok / FAJL_ARTEFAKTA[kod]).write_text("ОТВЕТ НЕРАБОЧИЙ: %s\n" % e, encoding="utf-8")
        verdikt, krug = "НЕРАБОЧИЙ: %s" % e, 0
    return verdikt, krug


# строка итога: что показать учителю по артефакту (ПРИНЯТЬ — ничего)
def stroka_itoga(kod, verdikt, krug):
    stroka = None
    if verdikt == "ВЕРНУТЬ":
        stroka = "%s: круги исчерпаны (%d) — выбрать: упростить / другой исполнитель / руками (proverka/%s-strazh.md)" % (kod, krug, kod)
    elif verdikt == "УЧИТЕЛЮ":
        stroka = "%s: страж — УЧИТЕЛЮ, нужно решение автора (proverka/%s-strazh.md)" % (kod, kod)
    elif verdikt != "ПРИНЯТЬ":
        stroka = "%s: %s" % (kod, verdikt)
    return stroka


# пожелания: принят, но в таблице стража есть «желательно» — строка учителю на приёмку
def stroka_pozhelanij(urok, kod, verdikt):
    stroka = None
    p = urok / "proverka" / (kod + "-strazh.md")
    if verdikt == "ПРИНЯТЬ" and p.exists() and "желательно" in p.read_text(encoding="utf-8").lower():
        stroka = "%s: принят, есть желательные правки — посмотреть на приёмке (proverka/%s-strazh.md)" % (kod, kod)
    return stroka


# пауза: при --po-shagam ждёт учителя; «q» — остановка
def pauza(kt, kod):
    if getattr(kt, "po_shagam", False):
        otvet = input("Дальше: %s. Enter — делать, q — остановить: " % kod)
        if otvet.strip().lower() == "q":
            raise Oshibka("остановлено учителем перед %s" % kod)


# стоп 2 пройден: со-анализ есть и рабочий — без него канву не собираем
def trebovat_stop_2(urok):
    p = urok / "so-analiz.md"
    if not p.exists() or p.read_text(encoding="utf-8").startswith("ОТВЕТ НЕРАБОЧИЙ"):
        raise Oshibka("нет рабочего so-analiz.md — сначала ii.py ekspertiza и СТОП 2")


# пропустить vizual: в наборе, но ни одного заказа картинок нет
def propustit_vizual(urok, kod):
    return kod == "vizual" and not zakazy_kartinok(vse_zakazy(urok))


# канва принята: файл есть и страж сказал ПРИНЯТЬ (после vernut) — заново не собираем
def kanva_prinyata(urok):
    est = (urok / FAJL_ARTEFAKTA["kanva"]).exists()
    return est and verdikt_iz_fajla(urok / "proverka" / "kanva-strazh.md") == "ПРИНЯТЬ"


# шаг сборки: один код → строка итога или None; канва не принята — Oshibka (дальше нельзя)
def shag_sborki(kt, kod):
    pauza(kt, kod)
    if propustit_vizual(kt.urok, kod):
        return "vizual: заказов картинок нет — пропущен"
    if kod == "kanva" and kanva_prinyata(kt.urok):
        print("kanva: уже принята — беру готовую")
        return None
    verdikt, krug = sobrat_odin(kt, kod)
    print("%s: %s (круг %d)" % (kod, verdikt, krug))
    stroka = stroka_itoga(kod, verdikt, krug) or stroka_pozhelanij(kt.urok, kod, verdikt)
    if kod == "kanva" and verdikt != "ПРИНЯТЬ":
        raise Oshibka("канва не принята — %s" % stroka)
    return stroka


# пройти шаги: все шаги набора; остановка — последней строкой итога
def projti_shagi(kt, nabor):
    itog = []
    try:
        for kod in shagi_sborki(nabor):
            stroka = shag_sborki(kt, kod)
            if stroka:
                itog.append(stroka)
    except Oshibka as e:
        itog.append("ОСТАНОВКА: %s" % e)
    return itog


# сборка без сети: собирает только запрос канвы (дальше нужна готовая канва)
def sborka_bez_seti(kt):
    sohranit_zapros(kt.urok, "kanva", osnova_prompta(kt.urok, "kanva"))
    print("Без сети: дальше канвы не идём — остальным шагам нужна готовая канва.")
    return 0


def komanda_sborka(arg):
    kt = sozdat_kontekst(arg)
    kt.po_shagam = arg.po_shagam
    trebovat_stop_2(kt.urok)
    if kt.bez_seti:
        return sborka_bez_seti(kt)
    itog = projti_shagi(kt, nabor_iz_zayavki(kt.urok))
    napisat_itog(kt, itog)
    print("СТОП 3: приёмка — открыть proverka/itog.md и отмеченные файлы.")
    return 2 if any(s.startswith("ОСТАНОВКА") for s in itog) else 0


# в архив: копия старой версии в proverka/starye/<имя>.<n>
def v_arhiv(urok, kod):
    p = urok / FAJL_ARTEFAKTA[kod]
    arhiv = urok / "proverka" / "starye"
    arhiv.mkdir(parents=True, exist_ok=True)
    nomer = len(list(arhiv.glob(p.name + ".*"))) + 1
    kopiya = arhiv / ("%s.%d" % (p.name, nomer))
    kopiya.write_text(p.read_text(encoding="utf-8"), encoding="utf-8")
    return kopiya


def komanda_vernut(arg):
    kt = sozdat_kontekst(arg)
    p = kt.urok / FAJL_ARTEFAKTA[arg.kod]
    if not p.exists():
        raise Oshibka("нет файла %s — возвращать нечего" % p)
    proshlyj = p.read_text(encoding="utf-8")
    print("Старая версия →", v_arhiv(kt.urok, arg.kod))
    verdikt, krug = sobrat_odin(kt, arg.kod, proshlyj, "Замечание учителя: " + arg.chto)
    print("%s: %s (круг %d)" % (arg.kod, verdikt, krug))
    stroka = stroka_itoga(arg.kod, verdikt, krug) or stroka_pozhelanij(kt.urok, arg.kod, verdikt)
    napisat_itog(kt, [s for s in [stroka] if s])
    return 0


# ---------- шаг 8: vydacha — вшить картинки, строгая проверка ----------

IMG_ASSETS = r"""<img\b[^>]*?\bsrc\s*=\s*["']assets/([a-z0-9_.-]+\.jpg)["'][^>]*>"""


# картинка в data: файл JPEG → строка data:image/jpeg;base64,…
def kartinka_v_data(put):
    return "data:image/jpeg;base64," + base64.b64encode(put.read_bytes()).decode("ascii")


# где стоит: строка блока «КАРТИНКИ» с этим именем, иначе «место не указано»
def gde_stoit(blok, imya):
    mesto = "место не указано"
    for stroka in blok.splitlines():
        if imya in stroka:
            mesto = stroka.strip(" -*")
    return mesto


# вшить одну: тег <img> с assets/ → с data:, нет файла — видимая строка «НЕТ КАРТИНКИ»
def vshit_odnu(teg, imya, assets, blok, net):
    put = assets / imya
    if put.exists():
        return teg.replace("assets/" + imya, kartinka_v_data(put))
    net.append("НЕТ КАРТИНКИ: %s, %s" % (imya, gde_stoit(blok, imya)))
    return '<span class="net-kartinki">НЕТ КАРТИНКИ: %s</span>' % imya


# вшить картинки: все <img src="assets/…"> файла; → (html, список «НЕТ КАРТИНКИ»)
def vshit_kartinki(html, assets, blok):
    net = []
    novyj = re.sub(IMG_ASSETS, lambda mt: vshit_odnu(mt.group(0), mt.group(1), assets, blok, net), html, flags=re.I)
    return novyj, net


# блок артефакта: текст artefakty/<код>-kartinki.md или пусто
def blok_artefakta(urok, kod):
    p = urok / "artefakty" / (kod + "-kartinki.md")
    return p.read_text(encoding="utf-8") if p.exists() else ""


# выдать файл: вшить, строго проверить, положить в vydacha/; → строки отчёта
def vydat_fajl(urok, kod):
    p = urok / FAJL_ARTEFAKTA[kod]
    html, net = vshit_kartinki(p.read_text(encoding="utf-8"), urok / "assets", blok_artefakta(urok, kod))
    oshibki = proverit_okruzhenie(html, p.name, tonkij=False)
    otchet = ["%s: %s" % (kod, s) for s in net]
    if oshibki:
        otchet += ["%s: НЕ ВЫДАН — %s" % (kod, o) for o in oshibki]
    else:
        (urok / "vydacha").mkdir(exist_ok=True)
        (urok / "vydacha" / p.name).write_text(html, encoding="utf-8")
        otchet.append("%s: выдан → vydacha/%s" % (kod, p.name))
    return otchet


# не принят: страж по файлу сказал не ПРИНЯТЬ — предупредить
def preduprezhdenie_strazha(urok, kod):
    verdikt = verdikt_iz_fajla(urok / "proverka" / (kod + "-strazh.md"))
    stroki = []
    if verdikt != "ПРИНЯТЬ":
        stroki.append("%s: внимание — вердикт стража %s, выдаю по решению учителя" % (kod, verdikt or "нет"))
    return stroki


def komanda_vydacha(arg):
    urok = put_uroka(arg.urok)
    otchet = []
    for kod in nabor_iz_zayavki(urok):
        if kod in HTML_KODY and (urok / FAJL_ARTEFAKTA[kod]).exists():
            otchet += preduprezhdenie_strazha(urok, kod) + vydat_fajl(urok, kod)
    (urok / "proverka").mkdir(exist_ok=True)
    (urok / "proverka" / "vydacha.md").write_text("# Выдача\n\n" + "\n".join("- " + s for s in otchet) + "\n", encoding="utf-8")
    print("\n".join(otchet) or "выдавать нечего")
    return 2 if any("НЕ ВЫДАН" in s for s in otchet) else 0


def ne_sdelano(arg):
    raise Oshibka("команда %s ещё не написана (вторая очередь, USTROJSTVO.md § 7)" % arg.komanda)


# ---------- разбор команд ----------

# komanda_analiz: кандидаты урока → разметчик → очередь учителю; работу делает tools/analiz.py
def komanda_analiz(arg):
    import analiz  # здесь, а не наверху: analiz.py сам берёт слова из ii.py
    argumenty = ["razmetka", str(arg.urok), "--model", arg.model]
    if arg.podstavit:
        argumenty += ["--podstavit", arg.podstavit]
    if arg.bez_seti:
        argumenty.append("--bez-seti")
    if arg.modeli:
        argumenty += ["--modeli", arg.modeli]
    return analiz.main(argumenty)


def razbor(argv=None):
    p = argparse.ArgumentParser(prog="ii.py", description="Сборка урока командой ИИ (v9). Версия " + VERSIYA)
    obshchie = argparse.ArgumentParser(add_help=False)
    obshchie.add_argument("--bez-seti", action="store_true", help="не вызывать модели: собранный промпт — в proverka/<шаг>-zapros.md")
    obshchie.add_argument("--modeli", help="другой modeli.json")
    obshchie.add_argument("--predel", type=int, default=PREDEL_PO_UMOLCHANIYU, help="предел вызовов (40)")
    k = p.add_subparsers(dest="komanda", required=True)
    k.add_parser("klyuchi", parents=[obshchie], help="проверить ключи и модели").set_defaults(f=komanda_klyuchi)
    for imya, f, pomoshch in (("novyj", komanda_novyj, "создать папку урока"),
                              ("status", komanda_status, "где урок"),
                              ("vydacha", komanda_vydacha, "вшить картинки из assets/, строгая проверка → vydacha/")):
        s = k.add_parser(imya, parents=[obshchie], help=pomoshch)
        s.add_argument("urok", help="путь к папке урока")
        s.set_defaults(f=f)
    s = k.add_parser("ekspertiza", parents=[obshchie], help="шаг 3: пакет для GLM → ответ GLM → со-анализ")
    s.add_argument("urok")
    s.add_argument("--otvet", help="файл с ответом GLM (скопированным из чата)")
    s.set_defaults(f=komanda_ekspertiza)
    s = k.add_parser("sborka", parents=[obshchie], help="шаги 4–6: канва, артефакты, проверка → СТОП 3")
    s.add_argument("urok")
    s.add_argument("--po-shagam", action="store_true", help="ждать Enter учителя перед каждым артефактом")
    s.set_defaults(f=komanda_sborka)
    s = k.add_parser("vernut", parents=[obshchie], help="вернуть один артефакт с замечанием учителя")
    s.add_argument("urok")
    s.add_argument("kod", choices=KODY)
    s.add_argument("chto", help="что не так (в кавычках)")
    s.set_defaults(f=komanda_vernut)
    s = k.add_parser("proverka", parents=[obshchie], help="окружение + страж")
    s.add_argument("urok")
    s.add_argument("kod", nargs="?", choices=KODY)
    s.set_defaults(f=komanda_proverka)
    s = k.add_parser("analiz", parents=[obshchie], help="после приёмки: кандидаты в словари → разметчик → вопросы учителю")
    s.add_argument("urok")
    s.add_argument("--model", default="deepseek", help="кто размечает (не тот, кто извлекал)")
    s.add_argument("--podstavit", help="ответ разметчика файлом (GLM через чат)")
    s.set_defaults(f=komanda_analiz)
    s = k.add_parser("zapros", parents=[obshchie], help="один промпт в одну роль")
    s.add_argument("--rol", required=True)
    s.add_argument("--prompt", required=True)
    s.add_argument("--vyhod", required=True)
    s.set_defaults(f=komanda_zapros, urok=None)
    s = k.add_parser("kartinki", parents=[obshchie], help="(вторая очередь, ещё не написана)")
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
