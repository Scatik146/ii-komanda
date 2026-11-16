# migraciya: перенос docs/komanda из drakon-graf и teacher-workpad в ii-komanda
# Комната 2026-11-15-migraciya (реплики 1б, 6). Правила — tools/migraciya-pravila.json.
# Запуск из папки ii-komanda (соседние репозитории — рядом):
#   python tools/migraciya.py          — проба: komanda/migraciya/proba.md, ничего больше не меняет
#   python tools/migraciya.py --opis   — опись: komanda/migraciya/opis.md, ничего больше не меняет
#   python tools/migraciya.py --sdelat — по-настоящему: файлы по плану пробы и коммит в каждом репозитории (без push)
#   python tools/migraciya.py --proverit — после --sdelat: старых путей в живой части нет, ссылки перенесённого целы
# Код по-фортовски: над каждым словом строка «слово: что делает».
import json
import posixpath
import re
import subprocess
import sys
from fnmatch import fnmatch
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
PROBA = OPIS.parent / "proba.md"
SDELANO = OPIS.parent / "sdelano.json"
SVOJ_SLED = "komanda/migraciya/"
REPOZITORII = ("ii-komanda", "drakon-graf", "teacher-workpad", "memory_maryam_ai")
GITHUB = "https://github.com/Scatik146/"
# код: в нём ссылку «репозиторий/путь» не напишешь — только путь внутри своего репозитория
KOD = {".py", ".js", ".mjs", ".cjs", ".bat", ".json", ".yml", ".fs"}
# комментарий по синтаксису файла; у json комментария нет — строки «перенесено» там не будет
KOMMENTARIJ = {".md": "<!-- {} -->", ".html": "<!-- {} -->", ".txt": "{}", ".py": "# {}", ".yml": "# {}",
               "": "# {}", ".js": "// {}", ".mjs": "// {}", ".cjs": "// {}", ".bat": "rem {}", ".fs": "\\ {}"}
# указатель в коде не молчит: запущенный по старому пути — падает с адресом
UKAZATEL_KODA = {".py": 'import sys\nsys.exit("переехало → {}")\n',
                 ".js": 'console.error("переехало → {}");\nprocess.exit(1);\n',
                 ".bat": "@echo переехало → {}\n@exit /b 1\n"}
UKAZATEL_KODA[".mjs"] = UKAZATEL_KODA[".cjs"] = UKAZATEL_KODA[".js"]
# имя репозитория прямо перед ссылкой: «drakon-graf `docs/komanda/…`»
SLOVO_SLEVA = re.compile(r"(drakon-graf|teacher-workpad)( `?)$")
# относительная ссылка Markdown: [текст](путь)
MD_SSYLKA = re.compile(r"\]\(([^)\s]+)\)")


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


# novyj_put: новый путь файла по правилу: в ii-komanda, «репозиторий:путь» (v_repo) или "" — остаётся;
#   imya_fajla — другое имя на новом месте («{imya}/SKILL.md»)
def novyj_put(pravilo, put):
    otvet = ""
    ostatok = put[len(pravilo["iz"]):]
    if ostatok and "imya_fajla" in pravilo:
        ostatok = pravilo["imya_fajla"].format(imya=Path(ostatok).stem)
    if pravilo["dejstvie"] != "ostaetsya":
        otvet = pravilo["v"] + ostatok
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


# razobrat: одна найденная ссылка: чей docs/komanda и какой путь внутри
def razobrat(m, stroka, nomer, repo, fajl, pravila, est):
    put = (m.group(2) or "/")[1:].rstrip(".")
    kuda = (repo_po_pristavke(m.group(1), pravila["repozitorii"])
            or repo_sleva(stroka, m.start(), ("drakon-graf", "teacher-workpad"))
            or chej_put(put, repo, est))
    kuda = po_podskazke(kuda, fajl, pravila["podskazki"])
    return {"fajl": fajl, "stroka": nomer, "repo": kuda, "put": put, "tekst": m.group(0)}


# ssylki_fajla: все ссылки на docs/komanda в одном файле
def ssylki_fajla(repo, fajl, pravila, est):
    tekst = (KOREN / repo / fajl).read_text(encoding="utf-8", errors="replace")
    najdeno = []
    for nomer, stroka in enumerate(tekst.splitlines(), 1):
        najdeno += [razobrat(m, stroka, nomer, repo, fajl, pravila, est) for m in SSYLKA.finditer(stroka)]
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
                po_fajlam[(repo, fajl)] = ssylki_fajla(repo, fajl, pravila, est)
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

# --- Проба: план «что будет сделано» и проверка ссылок после замены. Образец действия:
#   {"vid": "perenos", "repo": "ii-komanda", "put": "komanda/BRIFING.md", "tekst": "…", "otkuda": ("drakon-graf", "docs/komanda/BRIFING.md")}
#   vid: perenos (новый файл), ukazatel (старое место — «переехало → ссылка»), zamena (тот же файл, новые пути)
# Образец заметки о ссылке: {"repo", "fajl", "stroka", "bylo", "stalo"} (stalo "" — руками)


# kommit: короткий хеш последнего коммита репозитория
def kommit(repo):
    r = subprocess.run(["git", "-C", str(KOREN / repo), "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
    return r.stdout.strip() or "?"


# kommentarij: строка в синтаксисе файла ("" — у файла нет комментариев)
def kommentarij(rassh, tekst):
    shablon = KOMMENTARIJ.get(rassh, "")
    return shablon.format(tekst) if shablon else ""


# s_shapkoj: вставить строку первой — или второй, если первая обязана быть первой (#!, кодировка, @echo off)
def s_shapkoj(tekst, shapka):
    stroki = tekst.split("\n")
    mesto_ = 1 if re.match(r"#!|# -\*- coding|@echo off", stroki[0], re.I) else 0
    if shapka:
        stroki.insert(mesto_, shapka)
    return "\n".join(stroki)


# s_zagolovka: номера строк от первого заголовка nachalo до конца
def s_zagolovka(stroki, nachalo):
    pervaya = next((i for i, s in enumerate(stroki) if s.startswith(nachalo)), len(stroki))
    return set(range(pervaya, len(stroki)))


# razdel: номера строк раздела nachalo до следующего заголовка «## »
def razdel(stroki, nachalo):
    nomera = set()
    vnutri = False
    for i, s in enumerate(stroki):
        vnutri = s.startswith(nachalo) if s.startswith("## ") else vnutri
        if vnutri:
            nomera.add(i)
    return nomera


# stroki_istorii: номера строк, которые — история (их не трогаем)
def stroki_istorii(stroki, pravilo):
    nomera = set()
    if pravilo is None or pravilo["vnutri"] not in ("zhivoj", "navyk"):
        nomera = set(range(len(stroki)))
    elif "istoriya_s" in pravilo:
        nomera = s_zagolovka(stroki, pravilo["istoriya_s"])
    elif "istoriya_razdel" in pravilo:
        nomera = razdel(stroki, pravilo["istoriya_razdel"])
    return nomera


# pravilo_fajla: правило файла: перенос (для docs/komanda) или {"vnutri": класс}
def pravilo_fajla(pravila, repo, fajl):
    if fajl.startswith(STAROE + "/") and repo in pravila["perenos"]:
        otvet = pravilo_dlya(pravila["perenos"][repo], fajl[len(STAROE) + 1:])
    else:
        otvet = {"vnutri": pravilo_dlya(pravila["klass"][repo], fajl)["klass"]}
    return otvet


# mesto: (репозиторий, путь) из нового пути правила: «repo:путь» — свой репозиторий, иначе ii-komanda
def mesto(novyj):
    repo, _, put = novyj.rpartition(":")
    return (repo or "ii-komanda", put)


# gde_budet: где окажется файл после переноса (указатель — остаётся на месте)
def gde_budet(pravila, repo, fajl):
    otvet = (repo, fajl)
    p = pravilo_fajla(pravila, repo, fajl)
    if p and p.get("dejstvie") in ("perenos", "v_repo"):
        otvet = mesto(novyj_put(p, fajl[len(STAROE) + 1:]))
    return otvet


# kuda_vedet: куда ведёт ссылка после переноса (None — путь пустой или неясный)
def kuda_vedet(pravila, s):
    otvet = None
    p = pravilo_dlya(pravila["perenos"].get(s["repo"], []), s["put"])
    if p and s["put"]:
        otvet = mesto(novyj_put(p, s["put"]))
    return otvet


# tekst_ssylki: новый текст ссылки ("" — не заменить: в коде путь в чужой репозиторий);
#   vid: {"sleva": имя репозитория перед ссылкой или None, "v_ssylke": цель ссылки Markdown, "kod": файл — код}
def tekst_ssylki(m, s, otkuda, kuda, vid):
    pristavka = m.group(1) or ""
    svoj = repo_po_pristavke(pristavka, REPOZITORII)
    hvost = (m.group(2) or "")[1 + len(s["put"]):]
    novyj = ""
    if svoj:
        novyj = pristavka.replace(svoj + "/", kuda[0] + "/", 1) + kuda[1]
    elif vid["sleva"]:
        novyj = kuda[0] + vid["sleva"].group(2) + kuda[1]
    elif kuda[0] == otkuda[0]:
        novyj = pristavka + kuda[1]
    elif vid["v_ssylke"]:
        novyj = GITHUB + kuda[0] + "/blob/main/" + kuda[1]
    elif not vid["kod"]:
        novyj = pristavka + kuda[0] + "/" + kuda[1]
    return novyj + hvost if novyj else ""


# vid_ssylki: что вокруг ссылки: имя репозитория слева, цель ссылки Markdown, код
def vid_ssylki(k, stroka, m):
    sleva = None if m.group(1) else SLOVO_SLEVA.search(stroka, 0, m.start())
    return {"sleva": sleva, "v_ssylke": stroka[:m.start()].endswith("]("), "kod": Path(k["fajl"]).suffix in KOD}


# zamenit_v_stroke: новые пути в одной строке; каждая ссылка — заметкой
def zamenit_v_stroke(k, stroka, nomer, zametki):
    novaya = stroka
    for m in reversed(list(SSYLKA.finditer(stroka))):
        s = razobrat(m, stroka, nomer, k["repo"], k["fajl"], k["pravila"], k["est"])
        kuda = kuda_vedet(k["pravila"], s)
        vid = vid_ssylki(k, stroka, m)
        tekst = tekst_ssylki(m, s, k["otkuda"], kuda, vid) if kuda else ""
        nachalo = vid["sleva"].start() if vid["sleva"] and tekst else m.start()
        zametki.append({"repo": k["repo"], "fajl": k["fajl"], "stroka": nomer, "bylo": stroka[nachalo:m.end()],
                        "stalo": tekst, "kuda": kuda, "staroe": (s["repo"], STAROE + "/" + s["put"])})
        novaya = novaya[:nachalo] + tekst + novaya[m.end():] if tekst else novaya
    return novaya


# svoi: особые замены или «оставить» из правил, которые относятся к этому файлу
def svoi(k, klyuch):
    return [o for o in k["pravila"].get(klyuch, []) if o["repo"] == k["repo"] and fnmatch(k["fajl"], o["fajl"])]


# osobye_v_stroke: особые замены в строке (пути, которых общий разбор не видит или понял не так)
def osobye_v_stroke(k, stroka, nomer, zametki):
    for o in svoi(k, "osobye"):
        if o["bylo"] in stroka:
            stroka = stroka.replace(o["bylo"], o["stalo"])
            zametki.append({"repo": k["repo"], "fajl": k["fajl"], "stroka": nomer, "bylo": o["bylo"], "stalo": o["stalo"], "osobaya": True})
    return stroka


# zamenit_v_zhivoj: одна строка живой части: «оставить» — как есть; иначе особые замены, потом общий разбор
def zamenit_v_zhivoj(k, stroka, nomer, zametki):
    novaya = stroka
    if not any(o["tekst"] in stroka for o in svoi(k, "ostavit")):
        novaya = zamenit_v_stroke(k, osobye_v_stroke(k, stroka, nomer, zametki), nomer, zametki)
    return novaya


# zamenit_v_fajle: текст файла с новыми путями в живой части (история — как была)
def zamenit_v_fajle(k, tekst, zametki):
    stroki = tekst.split("\n")
    istoriya = stroki_istorii(stroki, pravilo_fajla(k["pravila"], k["repo"], k["fajl"]))
    for i in range(len(stroki)):
        stroki[i] = stroki[i] if i in istoriya else zamenit_v_zhivoj(k, stroki[i], i + 1, zametki)
    return "\n".join(stroki)


# tekst_ukazatelya: «переехало → ссылка» в синтаксисе файла
def tekst_ukazatelya(rassh, kuda):
    adres = GITHUB + kuda[0] + "/blob/main/" + kuda[1]
    imya = kuda[0] + "/" + kuda[1]
    otvet = kommentarij(rassh, "переехало → " + adres) + "\n"
    if rassh == ".md":
        otvet = f"# Переехало\n\n→ [{imya}]({adres})\n\nСтарое место оставлено до брифинга после миграции (окно отката).\n"
    elif rassh == ".html":
        otvet = f'<!DOCTYPE html>\n<meta charset="utf-8">\n<p>Переехало → <a href="{adres}">{imya}</a></p>\n'
    elif rassh == ".json":
        otvet = json.dumps({"pereehalo": adres}, ensure_ascii=False) + "\n"
    elif rassh in UKAZATEL_KODA:
        otvet = UKAZATEL_KODA[rassh].format(adres)
    return otvet


# dejstviya_komandy: перенос и указатель для одного файла docs/komanda
def dejstviya_komandy(k, tekst, zametki):
    p = pravilo_fajla(k["pravila"], k["repo"], k["fajl"])
    rassh = Path(k["fajl"]).suffix
    kuda = mesto(novyj_put(p, k["fajl"][len(STAROE) + 1:]))
    dejstviya = [{"vid": "ukazatel", "repo": k["repo"], "put": k["fajl"], "tekst": tekst_ukazatelya(rassh, kuda), "kuda": kuda}]
    if p["dejstvie"] in ("perenos", "v_repo"):
        # внутри своего репозитория (v_repo) строки нет: история — в git, номера строк не сдвигаются (тест drakon-zapis)
        shapka = kommentarij(rassh, f"перенесено из {k['repo']}@{k['kommit'][k['repo']]} {k['fajl']}") if p["dejstvie"] == "perenos" else ""
        novyj = s_shapkoj(zamenit_v_fajle(k, tekst, zametki), shapka)
        dejstviya.insert(0, {"vid": "perenos", "repo": kuda[0], "put": kuda[1], "tekst": novyj, "otkuda": (k["repo"], k["fajl"])})
    return dejstviya


# dejstviya_fajla: что будет с одним файлом (пусто — ничего)
def dejstviya_fajla(k, zametki):
    tekst = (KOREN / k["repo"] / k["fajl"]).read_text(encoding="utf-8", errors="replace")
    dejstviya = []
    if k["fajl"].startswith(STAROE + "/") and k["repo"] in k["pravila"]["perenos"]:
        dejstviya = dejstviya_komandy(k, tekst, zametki)
    elif pravilo_fajla(k["pravila"], k["repo"], k["fajl"])["vnutri"] == "navyk":
        dlya_kartochki = []
        zamenit_v_fajle(k, tekst, dlya_kartochki)
        zametki += [dict(z, navyk=True) for z in dlya_kartochki]
    else:
        novyj = zamenit_v_fajle(k, tekst, zametki)
        dejstviya = [{"vid": "zamena", "repo": k["repo"], "put": k["fajl"], "tekst": novyj}] if novyj != tekst else []
    return dejstviya


# plan: все действия и заметки по четырём репозиториям
def plan(pravila):
    est = {r: fajly_komandy(r) for r in ("drakon-graf", "teacher-workpad")}
    dejstviya, zametki = [], []
    kommity = {r: kommit(r) for r in REPOZITORII}
    for repo in pravila["repozitorii"]:
        for fajl in fajly_repo(repo):
            svoj = repo == "ii-komanda" and any(fajl.startswith(n) for n in pravila["ne_chitat"])
            k = {"pravila": pravila, "est": est, "repo": repo, "fajl": fajl,
                 "otkuda": gde_budet(pravila, repo, fajl), "kommit": kommity}
            dejstviya += [] if svoj else dejstviya_fajla(k, zametki)
    return dejstviya, zametki


# --- Проверка ссылок после замены


# vse_fajly: все файлы четырёх репозиториев сейчас: {(repo, путь)}
def vse_fajly():
    nabor = set()
    for r in REPOZITORII:
        nabor |= {(r, f.relative_to(KOREN / r).as_posix()) for f in (KOREN / r).rglob("*")
                  if f.is_file() and ".git" not in f.relative_to(KOREN / r).parts}
    return nabor


# est_li: есть ли такой файл или папка
def est_li(nabor, repo, put):
    put = put.rstrip("/")
    return (repo, put) in nabor or any(r == repo and f.startswith(put + "/") for r, f in nabor)


# otnositelnye: относительные ссылки Markdown (без адресов, якорей и путей от корня)
def otnositelnye(tekst):
    ssylki = [a.split("#")[0] for a in MD_SSYLKA.findall(tekst)]
    return [a for a in ssylki if a and not re.match(r"[a-z]+:|/", a)]


# razreshit: (репозиторий, путь) относительной ссылки из файла repo/put
def razreshit(repo, put, ssylka):
    polnyj = posixpath.normpath(posixpath.join(repo, posixpath.dirname(put), ssylka))
    r, _, f = polnyj.partition("/")
    return (r, f)


# bitye_otnositelnye: относительные ссылки живого .md, целые до миграции и битые после
def bitye_otnositelnye(pravila, d, do, posle):
    otkuda = d.get("otkuda", (d["repo"], d["put"]))
    staryj = (KOREN / otkuda[0] / otkuda[1]).read_text(encoding="utf-8", errors="replace")
    byli_bitye = {a for a in otnositelnye(staryj) if not est_li(do, *razreshit(*otkuda, a))}
    return [a for a in otnositelnye(d["tekst"])
            if a not in byli_bitye and not est_li(posle, *razreshit(d["repo"], d["put"], a))]


# proverit_ssylki: битые ссылки после замены: новые пути и относительные в живых .md
def proverit_ssylki(pravila, dejstviya, zametki):
    do = vse_fajly()
    posle = do | {(d["repo"], d["put"]) for d in dejstviya if d["vid"] == "perenos"}
    bitye = [f"- {z['repo']} `{z['fajl']}`:{z['stroka']} — `{z['stalo']}`: нет `{'/'.join(z['kuda'])}`"
             for z in zametki if z["stalo"] and z.get("kuda") and not est_li(posle, *z["kuda"]) and est_li(do, *z["staroe"])]
    for d in dejstviya:
        zhivoj = d["vid"] == "zamena" or pravilo_fajla(pravila, *d["otkuda"])["vnutri"] == "zhivoj" if d["vid"] != "ukazatel" else False
        if zhivoj and d["put"].endswith(".md"):
            bitye += [f"- {d['repo']} `{d['put']}` — `{a}`" for a in bitye_otnositelnye(pravila, d, do, posle)]
    return bitye


# --- Отчёт пробы


# stroki_dejstvij: таблица действий одного вида
def stroki_dejstvij(dejstviya, vid):
    stroki = []
    for d in dejstviya:
        if d["vid"] == vid and vid == "perenos":
            stroki.append(f"| {d['otkuda'][0]} `{d['otkuda'][1]}` | {d['repo']} `{d['put']}` |")
        elif d["vid"] == vid:
            stroki.append(f"| {d['repo']} `{d['put']}` | {'/'.join(d['kuda']) if 'kuda' in d else 'новые пути'} |")
    return stroki


# stroki_zamen: каждая замена — строкой «было → стало» (руками — отдельно; навыки — отдельно)
def stroki_zamen(zametki, ruchnye, navyki=False):
    stroki = []
    for z in zametki:
        if bool(z["stalo"]) != ruchnye and z.get("navyk", False) == navyki:
            stroki.append(f"- {z['repo']} `{z['fajl']}`:{z['stroka']} — `{z['bylo']}`" + ("" if ruchnye else f" → `{z['stalo']}`"))
    return stroki


# lishnie_osobye: особые замены и «оставить», которые ни к чему не подошли (правило устарело?)
def lishnie_osobye(pravila, zametki):
    byli = {(z["repo"], z["bylo"]) for z in zametki if z.get("osobaya")}
    return [f"- особая {o['repo']} `{o['fajl']}`: `{o['bylo']}`" for o in pravila.get("osobye", []) if (o["repo"], o["bylo"]) not in byli]


# napisat_probu: план и проверку — в komanda/migraciya/proba.md; коротко — на экран
def napisat_probu():
    pravila = prochitat_pravila()
    dejstviya, zametki = plan(pravila)
    bitye = proverit_ssylki(pravila, dejstviya, zametki)
    ruchnye = stroki_zamen(zametki, True) + lishnie_osobye(pravila, zametki)
    schet = {v: sum(1 for d in dejstviya if d["vid"] == v) for v in ("perenos", "ukazatel", "zamena")}
    itog = (f"переносов {schet['perenos']}, указателей {schet['ukazatel']}, файлов с заменой путей {schet['zamena']}, "
            f"замен {sum(1 for z in zametki if z['stalo'] and not z.get('navyk'))}, путей в навыках {sum(1 for z in zametki if z.get('navyk'))}, руками {len(ruchnye)}, битых ссылок после замены {len(bitye)}")
    chasti = ["# Проба миграции: что будет сделано", "", "Создано `tools/migraciya.py` (проба, ничего не меняет). " + itog + ".", "",
              "## Битые ссылки после замены", ""] + (bitye or ["нет"]) + ["", "## Руками (не заменено)", ""] + (ruchnye or ["нет"])
    chasti += ["", "## Перенос", "", "| откуда | куда |", "|---|---|"] + stroki_dejstvij(dejstviya, "perenos")
    chasti += ["", "## Указатели и файлы с заменой", "", "| файл | куда |", "|---|---|"]
    chasti += stroki_dejstvij(dejstviya, "ukazatel") + stroki_dejstvij(dejstviya, "zamena")
    chasti += ["", "## Замены путей", ""] + stroki_zamen(zametki, False)
    chasti += ["", "## Навыки — по карточке (скрипт копии не меняет)", ""]
    chasti += stroki_zamen(zametki, False, True) + stroki_zamen(zametki, True, True)
    PROBA.write_text("\n".join(chasti) + "\n", encoding="utf-8")
    print(f"Проба: {PROBA}\n{itog}")


# --- По-настоящему (--sdelat) и проверка после (--proverit). Образец строки sdelano.json:
#   {"vid": "perenos", "repo": "ii-komanda", "put": "komanda/BRIFING.md", "otkuda": ["drakon-graf", "docs/komanda/BRIFING.md"]}


# git: выполнить git в репозитории, вернуть вывод
def git(repo, *kluchi, vvod=None):
    r = subprocess.run(["git", "-C", str(KOREN / repo)] + list(kluchi), input=vvod,
                       capture_output=True, text=True, encoding="utf-8", check=True)
    return r.stdout


# gryaznye: репозитории с незакоммиченными изменениями (свой след миграции — не в счёт)
def gryaznye():
    spisok = []
    for r in REPOZITORII:
        stroki = [s for s in git(r, "status", "--porcelain").splitlines() if SVOJ_SLED not in s]
        spisok += [r] if stroki else []
    return spisok


# uzhe_est: цели переноса, которые уже лежат на месте (миграция уже была?)
def uzhe_est(dejstviya):
    return [d["repo"] + "/" + d["put"] for d in dejstviya if d["vid"] == "perenos" and (KOREN / d["repo"] / d["put"]).exists()]


# konec_strok: конец строк исходного файла — "\r\n", если в нём есть CRLF (.bat), иначе "\n"
def konec_strok(repo, put):
    f = KOREN / repo / put
    return "\r\n" if f.exists() and b"\r\n" in f.read_bytes() else "\n"


# zapisat: одно действие — на диск, с концами строк исходного файла
def zapisat(d, konec):
    f = KOREN / d["repo"] / d["put"]
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_bytes(d["tekst"].replace("\n", konec).encode("utf-8"))


# soobshchenie: текст коммита по-русски для одного репозитория
def soobshchenie(repo, dejstviya, kommity):
    schet = {v: sum(1 for d in dejstviya if d["repo"] == repo and d["vid"] == v) for v in ("perenos", "ukazatel", "zamena")}
    otkuda = ", ".join(f"{r}@{kommity[r]}" for r in ("drakon-graf", "teacher-workpad"))
    zagolovok = {"ii-komanda": "Миграция: docs/komanda из drakon-graf и teacher-workpad — в ii-komanda",
                 "memory_maryam_ai": "Память: пути docs/komanda — на новые места в ii-komanda"}
    return (zagolovok.get(repo, "Миграция: docs/komanda переехало в ii-komanda — указатели и новые пути") + "\n\n"
            + f"Перенесено файлов {schet['perenos']}, указателей {schet['ukazatel']}, файлов с новыми путями {schet['zamena']}.\n"
            + f"Из {otkuda}. Сделано tools/migraciya.py --sdelat (ii-komanda), план — komanda/migraciya/proba.md.\n"
            + "docs/komanda не удалять до брифинга после миграции (окно отката).\n")


# zakommitit: коммит одного репозитория — только свои пути (без git add -A)
def zakommitit(repo, puti, tekst):
    git(repo, "add", "--pathspec-from-file=-", vvod="\n".join(puti) + "\n")
    git(repo, "commit", "-q", "-F", "-", vvod=tekst)
    return git(repo, "rev-parse", "--short", "HEAD").strip()


# mozhno_li: причины не запускать (пусто — можно): грязные репозитории, уже перенесено, проба не чиста
def mozhno_li(pravila, dejstviya, zametki):
    prichiny = [f"не закоммичено: {r}" for r in gryaznye()]
    prichiny += [f"уже есть: {p}" for p in uzhe_est(dejstviya)]
    prichiny += ["битые ссылки после замены — смотри пробу"] if proverit_ssylki(pravila, dejstviya, zametki) else []
    prichiny += ["есть замены «руками» — смотри пробу"] if stroki_zamen(zametki, True) + lishnie_osobye(pravila, zametki) else []
    return prichiny


# sdelat: проба → проверки → запись всех действий → sdelano.json → коммит в каждом репозитории
def sdelat():
    pravila = prochitat_pravila()
    napisat_probu()
    dejstviya, zametki = plan(pravila)
    prichiny = mozhno_li(pravila, dejstviya, zametki)
    kommity = {r: kommit(r) for r in REPOZITORII}
    if prichiny:
        print("Не делаю:\n" + "\n".join("- " + p for p in prichiny))
    else:
        koncy = [konec_strok(*d.get("otkuda", (d["repo"], d["put"]))) for d in dejstviya]
        for d, konec in zip(dejstviya, koncy):
            zapisat(d, konec)
        zapisat_sled(dejstviya)
        for repo in REPOZITORII:
            puti = [d["put"] for d in dejstviya if d["repo"] == repo]
            puti += [SVOJ_SLED + "proba.md", SVOJ_SLED + "sdelano.json"] if repo == "ii-komanda" else []
            print(f"{repo}: {zakommitit(repo, puti, soobshchenie(repo, dejstviya, kommity))}" if puti else f"{repo}: нечего")
        print("Готово. Дальше: python tools/migraciya.py --proverit, потом push в каждом репозитории.")


# zapisat_sled: что сделано — в komanda/migraciya/sdelano.json (для --proverit и отката)
def zapisat_sled(dejstviya):
    sled = [{k: d[k] for k in ("vid", "repo", "put", "otkuda") if k in d} for d in dejstviya]
    SDELANO.write_text(json.dumps(sled, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


# ostalis_starye: старые пути docs/komanda в живой части файла после --sdelat
def ostalis_starye(pravila, d):
    otkuda = tuple(d.get("otkuda", (d["repo"], d["put"])))
    k = {"pravila": pravila, "repo": otkuda[0], "fajl": otkuda[1]}
    stroki = (KOREN / d["repo"] / d["put"]).read_text(encoding="utf-8").split("\n")
    istoriya = stroki_istorii(stroki, pravilo_fajla(pravila, *otkuda))
    ostavit = [o["tekst"] for o in svoi(k, "ostavit")]
    return [f"- {d['repo']} `{d['put']}`:{i + 1} — `{s.strip()[:80]}`" for i, s in enumerate(stroki)
            if i not in istoriya and STAROE in s and "перенесено из " not in s and not any(o in s for o in ostavit)]


# proverit_posle: после --sdelat: файлы на месте, старых путей в живой части нет, относительные ссылки .md целы
def proverit_posle():
    pravila = prochitat_pravila()
    sled = json.loads(SDELANO.read_text(encoding="utf-8"))
    nabor = vse_fajly()
    net = [f"- нет файла: {d['repo']}/{d['put']}" for d in sled if (d["repo"], d["put"]) not in nabor]
    starye, bitye = [], []
    for d in sled:
        if d["vid"] != "ukazatel" and (d["repo"], d["put"]) in nabor:
            starye += ostalis_starye(pravila, d)
            bitye += [f"- {d['repo']} `{d['put']}` — `{a}`" for a in bitye_posle(pravila, d, nabor)]
    print(f"Проверка после --sdelat: файлов {len(sled)}, нет на месте {len(net)}, старых путей {len(starye)}, битых ссылок {len(bitye)}")
    print("\n".join(net + starye + bitye) or "Всё цело.")


# bitye_posle: битые относительные ссылки перенесённого или изменённого живого .md (на диске сейчас)
def bitye_posle(pravila, d, nabor):
    otkuda = tuple(d.get("otkuda", (d["repo"], d["put"])))
    zhivoj = d["vid"] == "zamena" or pravilo_fajla(pravila, *otkuda)["vnutri"] == "zhivoj"
    tekst = (KOREN / d["repo"] / d["put"]).read_text(encoding="utf-8") if zhivoj and d["put"].endswith(".md") else ""
    return [a for a in otnositelnye(tekst) if not est_li(nabor, *razreshit(d["repo"], d["put"], a))]


# glavnoe: разобрать ключ запуска
def glavnoe():
    if "--opis" in sys.argv:
        napisat_opis()
    elif "--sdelat" in sys.argv:
        sdelat()
    elif "--proverit" in sys.argv and not SDELANO.exists():
        print("Нет komanda/migraciya/sdelano.json — сначала python tools/migraciya.py --sdelat")
    elif "--proverit" in sys.argv:
        proverit_posle()
    else:
        napisat_probu()


glavnoe()
