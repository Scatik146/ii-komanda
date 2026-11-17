#!/usr/bin/env python3
"""avto.py — проверки артефакта без моделей (ii.py 0.3, шаги 2–3 плана 17.11).

1. Стиль: нет inline style=, у функции JS не больше одного return, цвета CSS — только в :root.
2. Решения: правила урока из avtoproverki.md (есть / нет / в данных) и Ctrl+Alt+M у приложения.
3. Прогон в браузере без окна (Edge / Chrome / Chromium): ошибки консоли и снимок каждого экрана.

Только стандартная библиотека. Вызывается из ii.py: `ii.py avto <урок> [код]`, `ii.py progon <урок> [код]`.
"""
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

HTML_KODY = ("prilozhenie", "prezentaciya", "shpargalka", "pechatnye")
FAJL = {"prilozhenie": "artefakty/prilozhenie.html", "prezentaciya": "artefakty/prezentaciya.html",
        "shpargalka": "artefakty/shpargalka.html", "pechatnye": "artefakty/pechatnye.html"}
SHABLON_PRAVIL = """# Автопроверки урока (без моделей)

Правило — строка «- вид: текст» под заголовком артефакта (## prilozhenie) или ## все.
Виды: есть — текст должен быть в файле; нет — текста быть не должно;
в данных — текст хотя бы раз в коде скриптов (данные заданий). Регистр не важен.

## все
- нет: диктуют
- нет: микрофон

## prilozhenie
- есть: Новая пара
"""


# ---------- стиль ----------

# стили-в-строке: сколько атрибутов style= в разметке и коде
def stili_v_stroke(html):
    chislo = len(re.findall(r"""\bstyle\s*=\s*["']""", html, flags=re.I))
    oshibki = []
    if chislo:
        oshibki.append("inline style= — %d раз (стили только в <style>)" % chislo)
    return oshibki


# блоки-стилей: текст всех <style>…</style>
def bloki_stilej(html):
    return "\n".join(re.findall(r"<style\b[^>]*>(.*?)</style>", html, flags=re.S | re.I))


# без-root: CSS без блоков :root { … }
def bez_root(css):
    return re.sub(r":root\s*\{[^}]*\}", "", css)


# цвета-вне-root: значения цвета (#abc, rgb(, hsl() в объявлениях вне :root
def cveta_vne_root(html):
    css = bez_root(bloki_stilej(html))
    najdeno = re.findall(r":[^;{}]*?(#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\()", css)
    oshibki = []
    if najdeno:
        oshibki.append("цвета вне :root — %d раз (пример: %s); цвета — переменными в :root" % (len(najdeno), najdeno[0]))
    return oshibki


# ---------- return: функции и их тела ----------

# пропустить-строку: индекс после закрывающей кавычки строки, начатой в i
def propustit_stroku(kod, i):
    kavychka = kod[i]
    i += 1
    while i < len(kod) and kod[i] != kavychka:
        if kod[i] == "\\":
            i += 1
        i += 1
    return i + 1


# пропустить-комментарий: индекс после комментария // или /* */, начатого в i
def propustit_kommentarij(kod, i):
    konec = "\n" if kod.startswith("//", i) else "*/"
    j = kod.find(konec, i + 2)
    sdvig = len(konec)
    if j < 0:
        j, sdvig = len(kod), 0
    return j + sdvig


# очистить-код: строки и комментарии заменены пробелами той же длины (позиции не сдвигаются)
def ochistit_kod(kod):
    chasti, i = [], 0
    while i < len(kod):
        j = i + 1
        if kod[i] in "'\"`":
            j = propustit_stroku(kod, i)
        elif kod.startswith(("//", "/*"), i):
            j = propustit_kommentarij(kod, i)
        kusok = kod[i:j]
        if j - i > 1:
            kusok = re.sub(r"[^\n]", " ", kusok)
        chasti.append(kusok)
        i = j
    return "".join(chasti)


# парная-скобка: индекс «}», закрывающей «{» в позиции i (или конец кода)
def parnaya_skobka(kod, i):
    glubina, j = 0, i
    while j < len(kod):
        glubina += {"{": 1, "}": -1}.get(kod[j], 0)
        if glubina == 0:
            break
        j += 1
    return j


# начала-функций: (имя, позиция «{» тела) для function и стрелок с телом
def nachala_funkcij(kod):
    shablon = r"function\s*\*?\s*([\w$]*)\s*\([^)]*\)\s*\{|([\w$]+)\s*=\s*(?:async\s*)?\([^)]*\)\s*=>\s*\{|([\w$]+)\s*=>\s*\{"
    nachala = []
    for mt in re.finditer(shablon, kod):
        imya = mt.group(1) or mt.group(2) or mt.group(3) or "(без имени)"
        nachala.append((imya, mt.end() - 1))
    return nachala


# функции: список {imya, nachalo, konec} по очищенному коду
def funkcii(kod):
    spisok = []
    for imya, skobka in nachala_funkcij(kod):
        spisok.append({"imya": imya, "nachalo": skobka, "konec": parnaya_skobka(kod, skobka)})
    return spisok


# хозяин: самая внутренняя функция, в теле которой стоит позиция
def hozyain(spisok, poziciya):
    luchshaya = None
    for f in spisok:
        if f["nachalo"] < poziciya < f["konec"]:
            if luchshaya is None or f["nachalo"] > luchshaya["nachalo"]:
                luchshaya = f
    return luchshaya


# возвраты-по-функциям: имя → число return (вложенные функции считаются отдельно)
def vozvraty_po_funkciyam(kod):
    chisty = ochistit_kod(kod)
    spisok = funkcii(chisty)
    schet = {}
    for mt in re.finditer(r"\breturn\b", chisty):
        f = hozyain(spisok, mt.start())
        if f is not None:
            klyuch = "%s@%d" % (f["imya"], f["nachalo"])
            schet[klyuch] = schet.get(klyuch, 0) + 1
    return schet


# лишние-возвраты: функции, где return больше одного
def lishnie_vozvraty(html):
    kod = "\n".join(re.findall(r"<script\b[^>]*>(.*?)</script>", html, flags=re.S | re.I))
    lishnie = [k.split("@")[0] for k, n in vozvraty_po_funkciyam(kod).items() if n > 1]
    oshibki = []
    if lishnie:
        oshibki.append("больше одного return — %d функций: %s" % (len(lishnie), ", ".join(lishnie[:8])))
    return oshibki


# стиль: все проверки стиля одного HTML
def proverit_stil(html):
    return stili_v_stroke(html) + cveta_vne_root(html) + lishnie_vozvraty(html)


# ---------- решения: правила урока ----------

# правила: {раздел: [(вид, текст)]} из avtoproverki.md урока
def prochitat_pravila(urok):
    put = Path(urok) / "avtoproverki.md"
    pravila, razdel = {}, None
    if put.exists():
        for stroka in put.read_text(encoding="utf-8").splitlines():
            zagolovok = re.match(r"##\s+(\S+)", stroka)
            pravilo = re.match(r"-\s*(есть|нет|в данных)\s*:\s*(.+)", stroka.strip())
            if zagolovok:
                razdel = zagolovok.group(1)
            elif pravilo and razdel:
                pravila.setdefault(razdel, []).append((pravilo.group(1), pravilo.group(2).strip()))
    return pravila


# правила-артефакта: общие + свои
def pravila_artefakta(pravila, kod):
    return pravila.get("все", []) + pravila.get(kod, [])


# одно-правило: нарушение строкой или None
def odno_pravilo(html, vid, tekst):
    nizhnij, cel = html.lower(), tekst.lower()
    skripty = "\n".join(re.findall(r"<script\b[^>]*>(.*?)</script>", nizhnij, flags=re.S))
    narushenie = None
    if vid == "есть" and cel not in nizhnij:
        narushenie = "нет обязательного: «%s»" % tekst
    elif vid == "нет" and cel in nizhnij:
        narushenie = "есть запрещённое: «%s»" % tekst
    elif vid == "в данных" and cel not in skripty:
        narushenie = "в данных ни разу: «%s»" % tekst
    return narushenie


# ctrl-alt-m: есть ли обработчик быстрого перехода по экранам
def est_ctrl_alt_m(html):
    kod = html.replace(" ", "")
    return "ctrlKey" in kod and "altKey" in kod and re.search(r"""["'](m|M|KeyM|ь|Ь)["']""", kod) is not None


# решения: нарушения правил урока для одного артефакта
def proverit_resheniya(html, kod, pravila):
    oshibki = []
    for vid, tekst in pravila_artefakta(pravila, kod):
        narushenie = odno_pravilo(html, vid, tekst)
        if narushenie:
            oshibki.append(narushenie)
    if kod == "prilozhenie" and not est_ctrl_alt_m(html):
        oshibki.append("нет быстрого перехода по экранам Ctrl+Alt+M")
    return oshibki


# ---------- отчёт автопроверок ----------

# автопроверка: стиль + решения одного артефакта → (нарушения стиля, нарушения решений)
def avtoproverka(urok, kod, pravila):
    html = (Path(urok) / FAJL[kod]).read_text(encoding="utf-8")
    return proverit_stil(html), proverit_resheniya(html, kod, pravila)


# отчёт-авто: текст proverka/<код>-avto.md
def otchet_avto(kod, stil, resheniya):
    def spisok(oshibki):
        return "\n".join("- " + o for o in oshibki) or "нарушений нет"
    return "# Автопроверки: %s\n\n## Стиль\n\n%s\n\n## Решения\n\n%s\n" % (kod, spisok(stil), spisok(resheniya))


# записать-авто: отчёт в proverka/ → число нарушений
def zapisat_avto(urok, kod, pravila):
    stil, resheniya = avtoproverka(urok, kod, pravila)
    put = Path(urok) / "proverka" / (kod + "-avto.md")
    put.parent.mkdir(parents=True, exist_ok=True)
    put.write_text(otchet_avto(kod, stil, resheniya), encoding="utf-8")
    return len(stil) + len(resheniya)


# ---------- прогон в браузере ----------

KANDIDATY_BRAUZERA = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/mnt/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
    "/mnt/c/Program Files/Microsoft/Edge/Application/msedge.exe",
    "msedge", "microsoft-edge", "google-chrome", "chromium", "chromium-browser", "chrome",
]

# перехватчик: вставляется первым в <head>; копит ошибки, показывает экран из #ii-ekran=N, пишет отчёт в DOM
PEREHVATCHIK = r"""<script>
(function () {
  var oshibki = [];
  window.addEventListener("error", function (e) { oshibki.push("ошибка: " + e.message + " (строка " + e.lineno + ")"); });
  window.addEventListener("unhandledrejection", function (e) { oshibki.push("обещание: " + e.reason); });
  var staryj = console.error;
  console.error = function () { oshibki.push("console.error: " + Array.prototype.join.call(arguments, " ")); staryj.apply(console, arguments); };
  function ekrany() { return document.querySelectorAll(".screen, .ekran, .slide, section"); }
  function pokazat(n) {
    var vse = ekrany(), i;
    for (i = 0; i < vse.length; i++) { vse[i].classList.add("hidden"); vse[i].classList.remove("active"); vse[i].style.display = "none"; }
    if (vse[n]) { vse[n].classList.remove("hidden"); vse[n].classList.add("active"); vse[n].style.display = ""; }
  }
  window.addEventListener("load", function () {
    var mt = location.hash.match(/ii-ekran=(\d+)/);
    if (mt) { pokazat(Number(mt[1])); }
    setTimeout(function () {
      var pre = document.createElement("pre");
      pre.id = "ii-otchet"; pre.hidden = true;
      pre.textContent = JSON.stringify({ oshibki: oshibki, ekranov: ekrany().length });
      document.body.appendChild(pre);
    }, 500);
  });
})();
</script>"""


# это-wsl: скрипт работает внутри WSL (Linux в Windows)
def eto_wsl():
    return "microsoft" in os.uname().release.lower() if hasattr(os, "uname") else False


# есть-браузер: кандидат лежит по пути или находится в PATH
def est_brauzer(kandidat):
    return Path(kandidat).exists() or shutil.which(kandidat) is not None


# найти-браузер: путь к браузеру (II_BRAUZER → список кандидатов) или None
def najti_brauzer():
    najden = os.environ.get("II_BRAUZER")
    for kandidat in KANDIDATY_BRAUZERA:
        if najden is None and est_brauzer(kandidat):
            najden = shutil.which(kandidat) or kandidat
    return najden


# браузер-windows: браузер — .exe Windows, а скрипт в WSL (пути надо переводить)
def brauzer_windows(brauzer):
    return eto_wsl() and brauzer.lower().endswith(".exe")


# путь-для-браузера: путь в том виде, какой понимает браузер
def put_dlya_brauzera(put, brauzer):
    tekst = str(put)
    if brauzer_windows(brauzer):
        tekst = subprocess.run(["wslpath", "-w", tekst], capture_output=True, text=True).stdout.strip()
    return tekst


# адрес-файла: file:/// адрес файла для браузера
def adres_fajla(put, brauzer):
    tekst = put_dlya_brauzera(put, brauzer).replace("\\", "/")
    if not tekst.startswith("/"):
        tekst = "/" + tekst
    return "file://" + tekst


# рабочая-папка: временная папка, видная браузеру (у Edge из WSL — на диске C:)
def rabochaya_papka(brauzer):
    koren = None
    if brauzer_windows(brauzer):
        temp = subprocess.run(["cmd.exe", "/c", "echo %TEMP%"], capture_output=True, text=True).stdout.strip()
        koren = subprocess.run(["wslpath", "-u", temp], capture_output=True, text=True).stdout.strip()
    return Path(tempfile.mkdtemp(prefix="ii-progon-", dir=koren))


# с-перехватчиком: HTML со вставленным перехватчиком ошибок
def s_perehvatchikom(html):
    mt = re.search(r"<head\b[^>]*>", html, flags=re.I)
    mesto = mt.end() if mt else 0
    return html[:mesto] + PEREHVATCHIK + html[mesto:]


# флаги-браузера: общие флаги запуска без окна с отдельным профилем
def flagi_brauzera(brauzer, papka):
    profil = put_dlya_brauzera(papka / "profil", brauzer)
    return ["--headless=new", "--disable-gpu", "--no-first-run", "--hide-scrollbars",
            "--user-data-dir=" + profil, "--window-size=1280,800", "--virtual-time-budget=3000"]


# запустить-браузер: один запуск без окна → stdout (пусто при сбое)
def zapustit_brauzer(brauzer, flagi, adres):
    try:
        rez = subprocess.run([brauzer] + flagi + [adres], capture_output=True, text=True,
                             encoding="utf-8", errors="replace", timeout=90)
        vyvod = rez.stdout
    except (OSError, subprocess.TimeoutExpired) as e:
        vyvod = ""
        print("браузер не запустился: %s" % e)
    return vyvod


# отчёт-из-dom: {oshibki, ekranov} из выведенной страницы
def otchet_iz_dom(dom):
    mt = re.search(r'<pre id="ii-otchet"[^>]*>(.*?)</pre>', dom, flags=re.S)
    otchet = {"oshibki": ["страница не дала отчёт (не загрузилась или упала до load)"], "ekranov": 0}
    if mt:
        tekst = mt.group(1).replace("&quot;", '"').replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
        otchet = json.loads(tekst)
    return otchet


# снимок: снимок одного экрана в файл png → есть ли файл
def snimok(brauzer, flagi, adres, papka, png):
    vremennyj = papka / png.name
    for _ in range(2):  # вторая попытка: прошлый запуск мог ещё держать профиль
        if not vremennyj.exists():
            zapustit_brauzer(brauzer, flagi + ["--screenshot=" + put_dlya_brauzera(vremennyj, brauzer)], adres)
    est = vremennyj.exists()
    if est:
        png.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(vremennyj), str(png))
    return est


# снимки: по снимку на экран (не больше predel) → список имён файлов
def snimki(brauzer, flagi, adres, papka, kuda, kod, ekranov, predel=20):
    imena = []
    for n in range(max(1, min(ekranov, predel))):
        png = kuda / ("%s-%02d.png" % (kod, n + 1))
        if snimok(brauzer, flagi, adres + "#ii-ekran=%d" % n, papka, png):
            imena.append(png.name)
    return imena


# прогон: один артефакт в браузере → {oshibki, ekranov, snimki}
def progon(urok, kod, brauzer):
    papka = rabochaya_papka(brauzer)
    stranica = papka / (kod + ".html")
    stranica.write_text(s_perehvatchikom((Path(urok) / FAJL[kod]).read_text(encoding="utf-8")), encoding="utf-8")
    flagi, adres = flagi_brauzera(brauzer, papka), adres_fajla(stranica, brauzer)
    otchet = otchet_iz_dom(zapustit_brauzer(brauzer, flagi + ["--dump-dom"], adres))
    otchet["snimki"] = snimki(brauzer, flagi, adres, papka, Path(urok) / "proverka" / "progon", kod, otchet["ekranov"])
    shutil.rmtree(papka, ignore_errors=True)
    return otchet


# отчёт-прогона: текст proverka/<код>-progon.md
def otchet_progona(kod, otchet):
    oshibki = "\n".join("- " + o for o in otchet["oshibki"]) or "ошибок нет"
    snimki_ = "\n".join("- progon/" + s for s in otchet["snimki"]) or "снимков нет"
    return "# Прогон в браузере: %s\n\nЭкранов найдено: %d\n\n## Ошибки консоли\n\n%s\n\n## Снимки\n\n%s\n" % (
        kod, otchet["ekranov"], oshibki, snimki_)


# записать-прогон: прогон + отчёт → число ошибок (-1 — снимков нет совсем)
def zapisat_progon(urok, kod, brauzer):
    otchet = progon(urok, kod, brauzer)
    put = Path(urok) / "proverka" / (kod + "-progon.md")
    put.parent.mkdir(parents=True, exist_ok=True)
    put.write_text(otchet_progona(kod, otchet), encoding="utf-8")
    chislo = len(otchet["oshibki"])
    if not otchet["snimki"]:
        chislo = -1
    return chislo
