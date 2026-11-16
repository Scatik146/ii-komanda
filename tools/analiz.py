#!/usr/bin/env python3
"""analiz.py — кандидаты в словари: проверка цитат, разметка другой моделью, очередь учителю.

    python tools/analiz.py citaty <папка>                       проверить кандидатов, моделей не звать
    python tools/analiz.py citaty <папка> --fajl <путь> --privatnyj      то же для приватного файла
    python tools/analiz.py razmetka <папка>                     проверить → отдать разметчику → очередь
    python tools/analiz.py razmetka <папка> --podstavit ответ.md --model glm     ответ разметчика из файла
    python tools/analiz.py razmetka <папка> --bez-seti          только собрать запрос

<папка> — папка урока (или любая папка с сырьём). От неё считаются пути в поле «файл».
    <папка>/analiz/kandidaty.md              кандидаты от извлекателя, блоки ```кандидат
    <папка>/analiz/razmetka-zapros.md        что ушло разметчику
    <папка>/analiz/razmetka-otvet.md         что он ответил, блоки ```разметка
    <папка>/analiz/kandidaty-razmechennye.md кандидаты с разметкой
    <папка>/analiz/ochered-uchitelyu.md      вопросы учителю (только то, что ИИ не разметил сам)
    <папка>/analiz/otchet.md                 сколько кандидатов, что отброшено и почему

Правила — komanda/srez-1/postanovka.md. Извлекает одна модель, размечает другая; скрипт — третий:
цитата, повторы, допустимые значения, очередь. Нижние слова (ключи, модели, вызов) взяты из ii.py.
Приватные кандидаты разметчику не отправляются: скрипт умеет только проверить их цитаты.
"""
import argparse
import collections
import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ii  # noqa: E402  — словарь проверенных слов: ключи, модели, вызов

KOREN = ii.KOREN
PROMPT = KOREN / "prompty" / "analiz" / "razmetka.md"

# Данные.
#   kandidat: {"номер", "словарь", "тип", "запись", "цитата", "файл", "_privatnyj": bool}
#   razmetka: {"номер", "истинность", "доступ", "в уроке", "источник", "очередь", "почему"}
#   gotovyj:  кандидат + разметка + {"разметил": модель, "пометки": [строки]}
#   oshibka:  (код, номер, текст)
KLYUCHI_KANDIDATA = ("номер", "словарь", "тип", "запись", "цитата", "файл")
KLYUCHI_RAZMETKI = ("истинность", "доступ", "в уроке", "источник", "очередь", "почему")
DOPUSTIMO = {
    "словарь": ("реальность", "учитель", "методика", "тема", "урок"),
    "тип": ("факт", "оценка", "решение", "норма", "правило", "наблюдение", "утверждение", "сборка"),
    "истинность": ("1", "0", "-1", "—"),
    "доступ": ("публичное", "обезличенное", "приватное"),
    "в уроке": ("да", "нет"),
    "очередь": ("нет", "противоречие", "двусмысленность", "без источника", "второй случай"),
}
# Кто автор какого файла папки урока (страж не автор: разметка автором источника — с пометкой).
AVTORY = {"deepseek": ("kanva.md", "artefakty/"), "alisa": ("chaty/alisa.md", "so-analiz.md"),
          "glm": ("chaty/glm.md", "ekspertiza.md")}
KONTEKST = ("zayavka.md", "resheniya.md", "kanva.md")  # что разметчик видит из урока
NET_ISTOCHNIKA = ("", "нет", "—", "-")
PREDEL_OBYCHNYJ, PREDEL_VSEGO = 10, 40  # вопросов учителю за урок: обычно; с критичными


# ---------- нижний слой: блоки, цитата ----------

# bloki: все блоки ```имя … ``` текста — список словарей «ключ → значение»
def bloki(tekst, imya):
    spisok, tekushchij = [], None
    for stroka in tekst.splitlines():
        s = stroka.strip()
        if tekushchij is None and s.startswith("```") and s.strip("`").strip().lower() == imya:
            tekushchij = {}
        elif tekushchij is not None and s.startswith("```"):
            spisok.append(tekushchij)
            tekushchij = None
        elif tekushchij is not None and ":" in s:
            klyuch, _, znachenie = s.partition(":")
            tekushchij[klyuch.strip().lower()] = znachenie.strip()
    return spisok


# blok_tekstom: словарь → блок ```имя с полями в заданном порядке
def blok_tekstom(imya, slovar, klyuchi):
    stroki = ["```" + imya] + ["%s: %s" % (p, slovar.get(p, "")) for p in klyuchi] + ["```"]
    return "\n".join(stroki)


# szhat: текст с одним пробелом вместо любых пробелов и переводов строк
def szhat(tekst):
    return " ".join(tekst.split())


# fajl_kandidata: путь к файлу кандидата внутри папки; None — файла нет или он вне папки
def fajl_kandidata(papka, k):
    put = (papka / k.get("файл", "")).resolve()
    najden = None
    if put.is_file() and papka.resolve() in put.parents:
        najden = put
    return najden


# citata_est: цитата кандидата буквально стоит в его файле (пробелы и переводы строк не в счёт)
def citata_est(papka, k):
    put = fajl_kandidata(papka, k)
    est = False
    if put is not None and k.get("цитата"):
        est = szhat(k["цитата"]) in szhat(put.read_text(encoding="utf-8"))
    return est


# iz_fajla: кандидаты одного файла; у каждого отметка, приватный ли файл
def iz_fajla(put, privatnyj=False):
    spisok = []
    if put.is_file():
        spisok = [dict(k, _privatnyj=privatnyj) for k in bloki(put.read_text(encoding="utf-8"), "кандидат")]
    return spisok


# ---------- проверки кандидата: слово возвращает текст ошибки или пустую строку ----------

# net_polya: каких обязательных полей нет
def net_polya(k, okr):
    pustye = [p for p in KLYUCHI_KANDIDATA if not k.get(p)]
    tekst = ""
    if pustye:
        tekst = "нет поля: " + ", ".join(pustye)
    return tekst


# nomer_povtoren: номер встречается у кандидатов больше одного раза
def nomer_povtoren(k, okr):
    tekst = ""
    if k.get("номер") and okr["nomera"][k["номер"]] > 1:
        tekst = "номер повторяется"
    return tekst


# plohie_znacheniya: значения полей не из списка допустимых (проверяются только заполненные поля)
def plohie_znacheniya(k, polya):
    plohie = ["%s: «%s»" % (p, k[p]) for p in polya if k.get(p) and k[p] not in DOPUSTIMO[p]]
    tekst = ""
    if plohie:
        tekst = "недопустимое значение — " + "; ".join(plohie)
    return tekst


# plohoj_slovar_ili_tip: словарь или тип кандидата не из списка
def plohoj_slovar_ili_tip(k, okr):
    return plohie_znacheniya(k, ("словарь", "тип"))


# net_fajla: файла из поля «файл» нет в папке
def net_fajla(k, okr):
    tekst = ""
    if k.get("файл") and fajl_kandidata(okr["papka"], k) is None:
        tekst = "файла нет в папке: " + k["файл"]
    return tekst


# net_citaty: файл есть, а цитаты в нём нет — признак выдумки или пересказа
def net_citaty(k, okr):
    tekst = ""
    if k.get("цитата") and fajl_kandidata(okr["papka"], k) is not None and not citata_est(okr["papka"], k):
        tekst = "цитаты нет в файле " + k["файл"]
    return tekst


# nablyudenie_v_otkrytom: наблюдение за учителем лежит в открытом файле
def nablyudenie_v_otkrytom(k, okr):
    tekst = ""
    if k.get("тип") == "наблюдение" and not k.get("_privatnyj"):
        tekst = "наблюдение — только в приватный файл (memory_maryam_ai)"
    return tekst


# Проверки — данные: (код, слово). Порядок — порядок сообщений.
PROVERKI = (("Ц01", net_polya), ("Ц02", nomer_povtoren), ("Ц03", plohoj_slovar_ili_tip),
            ("Ц04", net_fajla), ("Ц05", net_citaty), ("Ц06", nablyudenie_v_otkrytom))


# oshibki_odnogo: ошибки одного кандидата по таблице PROVERKI
def oshibki_odnogo(k, okr):
    najdeno = []
    for kod, slovo in PROVERKI:
        tekst = slovo(k, okr)
        if tekst:
            najdeno.append((kod, k.get("номер", "?"), tekst))
    return najdeno


# proverit_kandidatov: ошибки всех кандидатов
def proverit_kandidatov(spisok, papka):
    okr = {"papka": papka, "nomera": collections.Counter(k.get("номер", "") for k in spisok)}
    oshibki = []
    for k in spisok:
        oshibki.extend(oshibki_odnogo(k, okr))
    return oshibki


# bez_oshibok: кандидаты, к которым нет ни одной ошибки, — только они идут разметчику
def bez_oshibok(spisok, oshibki):
    plohie = {nomer for _, nomer, _ in oshibki}
    return [k for k in spisok if k.get("номер", "?") not in plohie]


# stroki_oshibok: ошибки строками «код номер: текст»
def stroki_oshibok(oshibki):
    return ["%s %s: %s" % o for o in oshibki]


# ---------- запрос разметчику и его ответ ----------

# kontekst_uroka: заявка, «Решения автора» и канва, если они есть, — чтобы разметчик видел, что вошло в урок
def kontekst_uroka(papka):
    chasti = []
    for imya in KONTEKST:
        if (papka / imya).is_file():
            chasti.append("=== %s ===\n%s" % (imya, (papka / imya).read_text(encoding="utf-8")))
    if not chasti:
        chasti = ["(файлов урока в папке нет: в поле «в уроке» ставь «нет»)"]
    return "\n\n".join(chasti)


# zapros_razmetki: промпт разметчика + контекст урока + кандидаты
def zapros_razmetki(papka, spisok):
    kandidaty = "\n\n".join(blok_tekstom("кандидат", k, KLYUCHI_KANDIDATA) for k in spisok)
    prompt = PROMPT.read_text(encoding="utf-8")
    return prompt.replace("{{KONTEKST}}", kontekst_uroka(papka)).replace("{{KANDIDATY}}", kandidaty)


# otvet_razmetchika: текст ответа — из подставного файла, иначе от модели через слова ii.py
def otvet_razmetchika(arg, tekst):
    if arg.podstavit:
        otvet = Path(arg.podstavit).read_text(encoding="utf-8")
    else:
        modeli = ii.zagruzit_modeli(arg.modeli)
        znach, _ = ii.najti_klyuchi(ii.imena_peremennyh(modeli))
        try:
            otvet, _ = ii.odin_vyzov(ii.Kontekst(modeli, znach, predel=1), arg.model, tekst)
        except ii.Nerabochij as e:
            raise ii.Oshibka("разметчик %s не ответил: %s" % (arg.model, e))
    return otvet


# ---------- слияние: кандидат + разметка, пометки, принудительные правила ----------

# privesti: разметка с выровненными значениями (регистр, дефис вместо тире у истинности)
def privesti(r):
    chistaya = {p: r.get(p, "").strip() for p in KLYUCHI_RAZMETKI}
    for p in ("доступ", "в уроке", "очередь"):
        chistaya[p] = chistaya[p].lower()
    if chistaya["истинность"] in ("-", "–"):
        chistaya["истинность"] = "—"
    return chistaya


# avtor_istochnika: разметчик сам написал файл, из которого цитата
def avtor_istochnika(k, model):
    fajl = k.get("файл", "")
    return any(fajl == f or fajl.startswith(f) for f in AVTORY.get(model, ()))


# net_istochnika: у утверждения по теме источник не назван
def net_istochnika(g):
    return g.get("словарь") == "тема" and g.get("источник", "").strip().lower() in NET_ISTOCHNIKA


# pometki_razmetki: что скрипт заметил в разметке одного кандидата
def pometki_razmetki(g, model):
    pometki = []
    if plohie_znacheniya(g, ("истинность", "доступ", "в уроке", "очередь")):
        pometki.append(plohie_znacheniya(g, ("истинность", "доступ", "в уроке", "очередь")))
    if avtor_istochnika(g, model):
        pometki.append("размечено автором источника")
    if g.get("доступ") == "приватное":
        pometki.append("разметчик считает приватным — убрать из открытого файла")
    return pometki


# dovesti: принудительные правила — без источника истинность 0; спорное — в очередь
def dovesti(g):
    if net_istochnika(g) and g.get("истинность") == "1":
        g["истинность"] = "0"
        g["пометки"].append("истинность снижена до 0: нет источника")
    if net_istochnika(g) and g.get("в уроке") == "да":
        g["очередь"] = "без источника"
    if g.get("доступ") == "приватное" and g.get("очередь", "нет") == "нет":
        g["очередь"] = "противоречие"
    return g


# razmetit_odnogo: кандидат + его разметка → готовый; разметки нет — пометка «не размечен»
def razmetit_odnogo(k, r, model):
    g = dict(k, разметил=model, пометки=["не размечен"])
    if r is not None:
        g.update(privesti(r))
        g["пометки"] = pometki_razmetki(g, model)
        g = dovesti(g)
    return g


# slit: все кандидаты с разметкой по номеру
def slit(spisok, razmetki, model):
    po_nomeru = {r.get("номер", ""): r for r in razmetki}
    return [razmetit_odnogo(k, po_nomeru.get(k["номер"]), model) for k in spisok]


# lishnie_razmetki: номера разметок, для которых нет кандидата
def lishnie_razmetki(spisok, razmetki):
    nomera = {k["номер"] for k in spisok}
    return [r.get("номер", "?") for r in razmetki if r.get("номер", "") not in nomera]


# ---------- очередь учителю ----------

# kritichnyj: утверждение по теме вошло в урок без источника — уйдёт к ученикам непроверенным
def kritichnyj(g):
    return g.get("очередь") == "без источника" and g.get("в уроке") == "да"


# ochered: кого показать учителю сейчас и кто ждёт: критичные — до 40, остальные — пока вопросов не больше 10
def ochered(gotovye):
    kritichnye = [g for g in gotovye if kritichnyj(g)]
    prochie = [g for g in gotovye if g.get("очередь", "нет") != "нет" and not kritichnyj(g)]
    mest = max(0, PREDEL_OBYCHNYJ - len(kritichnye[:PREDEL_VSEGO]))
    sejchas = kritichnye[:PREDEL_VSEGO] + prochie[:mest]
    zhdut = kritichnye[PREDEL_VSEGO:] + prochie[mest:]
    return sejchas, zhdut


# vopros_tekstom: один вопрос очереди — запись, цитата, причина и место для ответа
def vopros_tekstom(nomer, g):
    kritichno = ""
    if kritichnyj(g):
        kritichno = " — КРИТИЧНО: уйдёт к ученикам"
    stroki = ["## %d. %s — %s%s" % (nomer, g["номер"], g["очередь"], kritichno),
              "запись: " + g["запись"], "цитата: «%s» (%s)" % (g["цитата"], g["файл"]),
              "почему: " + g.get("почему", ""), "ответ: "]
    return "\n".join(stroki)


# tekst_ocheredi: файл очереди целиком
def tekst_ocheredi(papka, sejchas, zhdut):
    shapka = ["# Очередь учителю: %s" % papka.name, "",
              "Здесь только то, что ИИ не смог разметить сам. Вопросов: %d." % len(sejchas),
              "Ответ пишите после слова «ответ:» — «да», «нет» или свою правку. Потом сохраните файл.", ""]
    if zhdut:
        shapka.insert(3, "Ждут следующего раза: " + ", ".join(g["номер"] for g in zhdut) + ".")
    voprosy = [vopros_tekstom(i + 1, g) for i, g in enumerate(sejchas)]
    return "\n".join(shapka) + "\n" + "\n\n".join(voprosy) + "\n"


# ---------- запись итогов ----------

# zapisat: текст → <папка>/analiz/<имя>
def zapisat(papka, imya, tekst):
    put = papka / "analiz" / imya
    put.parent.mkdir(parents=True, exist_ok=True)
    put.write_text(tekst, encoding="utf-8")
    return put


# gotovyj_tekstom: готовый кандидат блоком; пометки — одной строкой
def gotovyj_tekstom(g):
    slovar = dict(g, пометки="; ".join(g["пометки"]) or "нет")
    return blok_tekstom("кандидат", slovar, KLYUCHI_KANDIDATA + KLYUCHI_RAZMETKI + ("разметил", "пометки"))


# tekst_otcheta: сколько кандидатов, что отброшено, что заметил скрипт
def tekst_otcheta(arg, gotovye, oshibki, lishnie, sejchas):
    s_pometkami = ["%s: %s" % (g["номер"], "; ".join(g["пометки"])) for g in gotovye if g["пометки"]]
    stroki = ["# Отчёт анализатора: %s" % Path(arg.papka).name, "",
              "Когда: %s · Разметил: %s" % (datetime.datetime.now().strftime("%d.%m.%Y %H:%M"), arg.model),
              "Размечено кандидатов: %d · Отброшено проверкой: %d · Вопросов учителю: %d"
              % (len(gotovye), len({o[1] for o in oshibki}), len(sejchas)), "",
              "## Отброшено (к разметчику не пошло)"] + (stroki_oshibok(oshibki) or ["нет"])
    stroki += ["", "## Пометки скрипта"] + (s_pometkami or ["нет"])
    stroki += ["", "## Разметка без кандидата"] + (lishnie or ["нет"])
    return "\n".join(stroki) + "\n"


# zapisat_itogi: размеченные кандидаты, очередь и отчёт — в файлы; возвращает (сейчас, ждут)
def zapisat_itogi(arg, gotovye, oshibki, lishnie):
    papka = Path(arg.papka)
    sejchas, zhdut = ochered(gotovye)
    zapisat(papka, "kandidaty-razmechennye.md", "\n\n".join(gotovyj_tekstom(g) for g in gotovye) + "\n")
    zapisat(papka, "ochered-uchitelyu.md", tekst_ocheredi(papka, sejchas, zhdut))
    zapisat(papka, "otchet.md", tekst_otcheta(arg, gotovye, oshibki, lishnie, sejchas))
    return sejchas, zhdut


# ---------- команды ----------

# kandidaty_papki: кандидаты из файла по умолчанию или из --fajl; нет файла — остановка
def kandidaty_papki(arg):
    put = Path(arg.papka) / "analiz" / "kandidaty.md"
    if getattr(arg, "fajl", None):
        put = Path(arg.fajl)
    if not put.is_file():
        raise ii.Oshibka("нет файла кандидатов: %s" % put)
    return iz_fajla(put, getattr(arg, "privatnyj", False))


# komanda_citaty: проверить кандидатов без моделей; код 1 — есть ошибки
def komanda_citaty(arg):
    spisok = kandidaty_papki(arg)
    oshibki = proverit_kandidatov(spisok, Path(arg.papka))
    for stroka in stroki_oshibok(oshibki):
        print(stroka)
    if not oshibki:
        print("кандидаты в порядке: %d" % len(spisok))
    return int(bool(oshibki))


# razmetit: запрос → ответ разметчика → слияние → файлы; печатает итог одной строкой
def razmetit(arg, godnye, oshibki, tekst):
    otvet = otvet_razmetchika(arg, tekst)
    zapisat(Path(arg.papka), "razmetka-otvet.md", otvet)
    razmetki = bloki(otvet, "разметка")
    gotovye = slit(godnye, razmetki, arg.model)
    sejchas, zhdut = zapisat_itogi(arg, gotovye, oshibki, lishnie_razmetki(godnye, razmetki))
    print("Размечено: %d, отброшено: %d, вопросов учителю: %d, ждут: %d → %s"
          % (len(gotovye), len({o[1] for o in oshibki}), len(sejchas), len(zhdut),
             Path(arg.papka) / "analiz" / "ochered-uchitelyu.md"))
    return 0


# komanda_razmetka: проверка цитат → запрос разметчику → очередь учителю
def komanda_razmetka(arg):
    spisok = kandidaty_papki(arg)
    oshibki = proverit_kandidatov(spisok, Path(arg.papka))
    godnye = bez_oshibok(spisok, oshibki)
    tekst = zapros_razmetki(Path(arg.papka), godnye)
    zapisat(Path(arg.papka), "razmetka-zapros.md", tekst)
    kod = 0
    if arg.bez_seti:
        print("Без сети: запрос собран (%d кандидатов, %d знаков), разметчик не вызван." % (len(godnye), len(tekst)))
    else:
        kod = razmetit(arg, godnye, oshibki, tekst)
    return kod


# razbor_citaty: аргументы команды citaty
def razbor_citaty(k):
    c = k.add_parser("citaty", help="проверить кандидатов без моделей")
    c.add_argument("papka", help="папка урока (от неё считаются пути в поле «файл»)")
    c.add_argument("--fajl", help="другой файл кандидатов (например, приватный)")
    c.add_argument("--privatnyj", action="store_true", help="файл приватный: наблюдения в нём разрешены")
    c.set_defaults(f=komanda_citaty)
    return c


# razbor_razmetka: аргументы команды razmetka
def razbor_razmetka(k):
    r = k.add_parser("razmetka", help="проверка → разметчик → очередь учителю")
    r.add_argument("papka", help="папка урока")
    r.add_argument("--model", default="deepseek", help="кто размечает: имя из modeli.json или glm с --podstavit")
    r.add_argument("--podstavit", help="файл с готовым ответом разметчика (GLM через чат; проба без сети)")
    r.add_argument("--bez-seti", action="store_true", help="только собрать запрос в analiz/razmetka-zapros.md")
    r.add_argument("--modeli", help="другой modeli.json")
    r.set_defaults(f=komanda_razmetka)
    return r


# razbor: аргументы командной строки
def razbor(argv=None):
    p = argparse.ArgumentParser(prog="analiz.py", description="Кандидаты в словари: цитаты, разметка, очередь учителю.")
    k = p.add_subparsers(dest="komanda", required=True)
    razbor_citaty(k)
    razbor_razmetka(k)
    return p.parse_args(argv)


# main: кодировка консоли, команда, остановка с понятным текстом
def main(argv=None):
    for potok in (sys.stdout, sys.stderr):
        try:
            potok.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    arg = razbor(argv)
    try:
        kod = arg.f(arg)
    except ii.Oshibka as e:
        print("ОСТАНОВКА:", e, file=sys.stderr)
        kod = 2
    return kod


if __name__ == "__main__":
    sys.exit(main())
