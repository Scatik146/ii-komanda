# migraciya: перенос docs/komanda из drakon-graf и teacher-workpad в ii-komanda
# Комната 2026-11-15-migraciya (реплики 1б, 6). Правила — tools/migraciya-pravila.json.
# Запуск из папки ii-komanda (соседние репозитории — рядом):
#   python tools/migraciya.py --opis   — опись: komanda/migraciya/opis.md, ничего больше не меняет
# Код по-фортовски: над каждым словом строка «слово: что делает».
import json
import re
import sys
from pathlib import Path

# Данные. Образец ссылки:
#   {"fajl": "README.md", "stroka": 12, "repo": "drakon-graf", "put": "BRIFING.md", "tekst": "drakon-graf/docs/komanda/BRIFING.md"}
KOREN = Path(__file__).resolve().parent.parent.parent
PRAVILA = Path(__file__).resolve().parent / "migraciya-pravila.json"
OPIS = Path(__file__).resolve().parent.parent / "komanda" / "migraciya" / "opis.md"
STAROE = "docs/komanda"
# ссылка: необязательная приставка (raw, github, имя репозитория), затем docs/komanda и путь
SSYLKA = re.compile(
    r"((?:raw\.githubusercontent\.com/Scatik146/|github\.com/Scatik146/)?"
    r"(?:[A-Za-z_-]+)/(?:(?:blob|tree)/main/|main/)?)?docs/komanda(/[A-Za-zА-Яа-яЁё0-9_./-]*)?"
)
TEKSTOVYE = {".md", ".txt", ".py", ".js", ".mjs", ".cjs", ".json", ".bat", ".html", ".yml", ".fs", ""}


# prochitat_pravila: правила миграции из json
def prochitat_pravila():
    return json.loads(PRAVILA.read_text(encoding="utf-8"))


# pravilo_dlya: самое длинное правило, чей префикс подходит к пути
def pravilo_dlya(spisok, put):
    luchshee = None
    for p in spisok:
        if put.startswith(p["iz"]) and (luchshee is None or len(p["iz"]) > len(luchshee["iz"])):
            luchshee = p
    return luchshee


# novyj_put: новый путь файла по правилу: в ii-komanda, «репозиторий:путь» (v_repo) или "" — остаётся
def novyj_put(pravilo, put):
    otvet = ""
    if pravilo["dejstvie"] != "ostaetsya":
        otvet = pravilo["v"] + put[len(pravilo["iz"]):]
    return otvet


# fajly_repo: все текстовые файлы репозитория (относительные пути, без .git)
def fajly_repo(repo):
    papka = KOREN / repo
    spisok = []
    for f in sorted(papka.rglob("*")):
        if f.is_file() and ".git" not in f.parts and f.suffix in TEKSTOVYE:
            spisok.append(f.relative_to(papka).as_posix())
    return spisok


# fajly_komandy: файлы docs/komanda репозитория (пути внутри docs/komanda)
def fajly_komandy(repo):
    papka = KOREN / repo / STAROE
    return [f.relative_to(papka).as_posix() for f in sorted(papka.rglob("*")) if f.is_file()]


# repo_po_pristavke: имя репозитория из приставки ссылки ("" — приставки нет)
def repo_po_pristavke(pristavka, repozitorii):
    otvet = ""
    for r in repozitorii:
        if pristavka and (r + "/") in pristavka:
            otvet = r
    return otvet


# repo_sleva: последнее имя репозитория в строке левее ссылки ("" — нет)
def repo_sleva(stroka, nachalo, repozitorii):
    otvet = ""
    luchshee = -1
    for r in repozitorii:
        mesto = stroka.rfind(r, 0, nachalo)
        if mesto > luchshee:
            luchshee = mesto
            otvet = r
    return otvet


# papka_puti: путь, по которому искать: файл целиком или его папка, если файла нет («NNN-…»)
def papka_puti(put, est):
    otvet = put
    vse = est["drakon-graf"] + est["teacher-workpad"]
    if put and not put.endswith("/") and put not in vse and "/" in put:
        otvet = put.rsplit("/", 1)[0] + "/"
    return otvet


# chej_put: в каком репозитории лежит docs/komanda/<put> ("?" — неясно, "нет" — нигде)
def chej_put(put, svoj, est):
    put = papka_puti(put, est)
    gde = [r for r in ("drakon-graf", "teacher-workpad") if put in est[r]]
    otvet = "нет"
    if put == "" or put.endswith("/"):
        gde = [r for r in ("drakon-graf", "teacher-workpad") if any(f.startswith(put) for f in est[r])]
    if svoj in gde:
        otvet = svoj
    elif len(gde) == 1:
        otvet = gde[0]
    elif len(gde) == 2:
        otvet = "?"
    return otvet


# po_podskazke: неясную ссылку решить по подсказке для папки файла
def po_podskazke(kuda, fajl, podskazki):
    otvet = kuda
    for papka, repo in podskazki.items():
        if kuda == "?" and fajl.startswith(papka):
            otvet = repo
    return otvet


# ssylki_fajla: все ссылки на docs/komanda в одном файле
def ssylki_fajla(repo, fajl, repozitorii, est, podskazki):
    tekst = (KOREN / repo / fajl).read_text(encoding="utf-8", errors="replace")
    najdeno = []
    for nomer, stroka in enumerate(tekst.splitlines(), 1):
        for m in SSYLKA.finditer(stroka):
            put = (m.group(2) or "/")[1:].rstrip(".")
            kuda = (repo_po_pristavke(m.group(1), repozitorii)
                    or repo_sleva(stroka, m.start(), ("drakon-graf", "teacher-workpad"))
                    or chej_put(put, repo, est))
            kuda = po_podskazke(kuda, fajl, podskazki)
            najdeno.append({"fajl": fajl, "stroka": nomer, "repo": kuda, "put": put, "tekst": m.group(0)})
    return najdeno


# klass_fajla: живой файл или история (файлы docs/komanda — по правилу переноса)
def klass_fajla(pravila, repo, fajl):
    if fajl.startswith(STAROE + "/") and repo in pravila["perenos"]:
        p = pravilo_dlya(pravila["perenos"][repo], fajl[len(STAROE) + 1:])
        otvet = p["vnutri"] if p else "?"
    else:
        otvet = pravilo_dlya(pravila["klass"][repo], fajl)["klass"]
    return otvet


# stroki_perenosa: таблица «старый путь → новый путь» для одного репозитория
def stroki_perenosa(pravila, repo):
    stroki = []
    for put in fajly_komandy(repo):
        p = pravilo_dlya(pravila["perenos"][repo], put)
        kuda = novyj_put(p, put) if p else "?"
        stroki.append(f"| `{put}` | `{kuda}` | {p['dejstvie'] if p else '?'} | {p['vnutri'] if p else '?'} |")
    return stroki


# vse_ssylki: ссылки во всех файлах четырёх репозиториев: {(repo, fajl): [ссылки]}
def vse_ssylki(pravila, est):
    po_fajlam = {}
    for repo in pravila["repozitorii"]:
        for fajl in fajly_repo(repo):
            svoj = repo == "ii-komanda" and any(fajl.startswith(n) for n in pravila["ne_chitat"])
            if not svoj and STAROE in (KOREN / repo / fajl).read_text(encoding="utf-8", errors="replace"):
                po_fajlam[(repo, fajl)] = ssylki_fajla(repo, fajl, pravila["repozitorii"], est, pravila["podskazki"])
    return po_fajlam


# stroki_ssylok: таблица файлов со ссылками: класс, сколько ссылок, сколько неясных
def stroki_ssylok(pravila, po_fajlam):
    stroki = []
    for (repo, fajl), ssylki in sorted(po_fajlam.items()):
        neyasno = sum(1 for s in ssylki if s["repo"] in ("?", "нет"))
        stroki.append(f"| {repo} | `{fajl}` | {klass_fajla(pravila, repo, fajl)} | {len(ssylki)} | {neyasno} |")
    return stroki


# stroki_neyasnyh: каждая неясная ссылка в живом файле — строкой
def stroki_neyasnyh(pravila, po_fajlam):
    stroki = []
    for (repo, fajl), ssylki in sorted(po_fajlam.items()):
        if klass_fajla(pravila, repo, fajl) != "istoriya":
            for s in ssylki:
                if s["repo"] in ("?", "нет"):
                    stroki.append(f"- {repo} `{fajl}`:{s['stroka']} — `{s['tekst']}` → {s['repo']}")
    return stroki


# napisat_opis: собрать опись и записать komanda/migraciya/opis.md
def napisat_opis():
    pravila = prochitat_pravila()
    est = {r: fajly_komandy(r) for r in ("drakon-graf", "teacher-workpad")}
    po_fajlam = vse_ssylki(pravila, est)
    chasti = ["# Опись миграции docs/komanda → ii-komanda", "",
              "Создано `tools/migraciya.py --opis`; правила — `tools/migraciya-pravila.json`.", ""]
    for repo in ("drakon-graf", "teacher-workpad"):
        chasti += [f"## Файлы {repo}/docs/komanda ({len(est[repo])})", "",
                   "| старый путь | новый путь в ii-komanda | действие | внутри |", "|---|---|---|---|"]
        chasti += stroki_perenosa(pravila, repo) + [""]
    vsego = sum(len(s) for s in po_fajlam.values())
    chasti += [f"## Ссылки: {vsego} в {len(po_fajlam)} файлах", "",
               "| репозиторий | файл | класс | ссылок | неясных |", "|---|---|---|---|---|"]
    chasti += stroki_ssylok(pravila, po_fajlam) + ["", "## Неясные ссылки в живых файлах", ""]
    chasti += stroki_neyasnyh(pravila, po_fajlam) or ["нет"]
    OPIS.parent.mkdir(parents=True, exist_ok=True)
    OPIS.write_text("\n".join(chasti) + "\n", encoding="utf-8")
    print(f"Опись: {OPIS} — файлов {sum(len(v) for v in est.values())}, ссылок {vsego} в {len(po_fajlam)} файлах")


# glavnoe: разобрать ключ запуска
def glavnoe():
    if "--opis" in sys.argv:
        napisat_opis()
    else:
        print("Пока есть только опись: python tools/migraciya.py --opis")


glavnoe()
