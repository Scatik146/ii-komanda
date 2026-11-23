"""slovar-iz-koda.py — слова JS-кода «по-фортовски» → кандидаты словаря Форто-Пролога.

Слово — функция с комментарием над ней «// имя: что делает». Состав слова —
слова той же папки и общего кода, имя которых стоит в теле (вызов или передача;
совпадение с именем переменной даёт лишнюю связь — состав надо смотреть глазами). Слой: нижний — ни из чего не собрано;
верхний — собрано и никем не вызывается; иначе средний.

    python3 tools/slovar-iz-koda.py <клон teacher-workpad> <коммит> <папка> [<папка> …]
        --nomer 9158                     первый свободный номер кандидата
        --obshchie lib/slova             папки общего кода: их копии в уроках не дают новых атомов
        --ne-kopii 'папка/файл.js:имя'   копия с тем же именем, но другим действием (омоним)
        --vyhod slovar/0001-realnost/kandidaty   куда писать атомы
        --spisok файл.md                 таблица всех слов (номер, слово, папка, слой, что делает)
        --proba                          ничего не писать, только напечатать таблицу

Описание берётся из строки над словом: это пересказ автора кода, тело не проверено
(ОЧ-Б7) — поэтому «проверено: нет», статус «черновик». Код по-фортовски.
"""
import argparse
import re
import sys
from pathlib import Path

SLOVO = re.compile(r"^// ?([\w$]+): ?(.+)\n((?://[^\n]*\n)*)function\s+\1\s*\(([^)]*)\)\s*\{\n(.*?)\n\}", re.M | re.S)
DANNYE = ("tekst.js", "dannye.js", "test.cjs")
DATA = "2026-11-23"


# fajly_papki: JS-файлы папки с кодом (без файлов данных и тестов)
def fajly_papki(koren, papka):
    put = Path(koren) / papka
    fajly = sorted(f for f in put.glob("*.js") if f.name not in DANNYE)
    return fajly


# slova_fajla: слова одного файла — имя, что делает, параметры, тело
def slova_fajla(koren, fajl):
    tekst = fajl.read_text(encoding="utf-8")
    otn = str(fajl.relative_to(koren))
    spisok = [{"imya": m.group(1), "chto": m.group(2).strip(), "param": m.group(4).strip(),
               "telo": m.group(5), "fajl": otn, "papka": str(Path(otn).parent)} for m in SLOVO.finditer(tekst)]
    return spisok


# vse_slova: слова всех папок по порядку
def vse_slova(koren, papki):
    spisok = []
    for papka in papki:
        for fajl in fajly_papki(koren, papka):
            spisok.extend(slova_fajla(koren, fajl))
    return spisok


# upominaet: имя слова стоит в теле как имя (вызов или передача), а не как ключ или свойство
def upominaet(imya, telo):
    shablon = r"(?<![\w.$'\"])" + re.escape(imya) + r"(?![\w$'\"])(?!\s*:)"
    return re.search(shablon, telo) is not None


# vyzyvaet: имена слов своей папки и общего кода, которые упомянуты в теле
def vyzyvaet(slovo, imena_papki):
    est = [i for i in sorted(imena_papki) if i != slovo["imya"] and upominaet(i, slovo["telo"])]
    return est


# kopiya_obshchego: слово урока — копия слова общего кода (то же имя, не объявлено омонимом)
def kopiya_obshchego(slovo, obshchie_imena, ne_kopii, obshchie_papki):
    svoe = slovo["papka"] in obshchie_papki
    omonim = slovo["fajl"] + ":" + slovo["imya"] in ne_kopii
    return not svoe and not omonim and slovo["imya"] in obshchie_imena


# razdelit: атомы (свои слова) и копии общих слов
def razdelit(slova, obshchie_papki, ne_kopii):
    obshchie_imena = {s["imya"] for s in slova if s["papka"] in obshchie_papki}
    atomy = [s for s in slova if not kopiya_obshchego(s, obshchie_imena, ne_kopii, obshchie_papki)]
    kopii = [s for s in slova if kopiya_obshchego(s, obshchie_imena, ne_kopii, obshchie_papki)]
    return atomy, kopii


# slug: имя для id — латиница строчными через дефис
def slug(tekst):
    s = re.sub(r"([a-z])([A-Z])", r"\1-\2", tekst)
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s


# imya_uroka: короткое имя папки для id (последняя часть пути без номера урока)
def imya_uroka(papka):
    chast = Path(papka).name
    return slug(re.sub(r"^[a-z]+-\d+-", "", chast))


# pronumerovat: номер и id каждому атому; ключ — (папка, файл, имя)
def pronumerovat(atomy, nachalo):
    for i, s in enumerate(atomy):
        s["nomer"] = nachalo + i
        s["id"] = "%d-%s-%s" % (s["nomer"], slug(s["imya"]), imya_uroka(s["papka"]))
    return atomy


# najti_nomer: номер слова имени imya для вызова из папки papka (своя папка, иначе общий код)
def najti_nomer(imya, papka, atomy, obshchie_papki):
    svoi = [a["nomer"] for a in atomy if a["imya"] == imya and a["papka"] == papka]
    obshchie = [a["nomer"] for a in atomy if a["imya"] == imya and a["papka"] in obshchie_papki]
    vse = svoi + obshchie
    return vse[0] if vse else None


# sostavit: состав и слой каждого атома
def sostavit(atomy, obshchie_papki):
    imena = {}
    for a in atomy + []:
        imena.setdefault(a["papka"], set()).add(a["imya"])
    obshchie = set().union(*[imena.get(p, set()) for p in obshchie_papki]) if obshchie_papki else set()
    for a in atomy:
        nomera = [najti_nomer(i, a["papka"], atomy, obshchie_papki) for i in vyzyvaet(a, imena[a["papka"]] | obshchie)]
        a["sostav"] = sorted({n for n in nomera if n and n != a["nomer"]})
    vyzvannye = {n for a in atomy for n in a["sostav"]}
    for a in atomy:
        a["sloj"] = "нижний" if not a["sostav"] else ("верхний" if a["nomer"] not in vyzvannye else "средний")
    return atomy


# kopii_atoma: строки истории о копиях общего слова в уроках
def kopii_atoma(atom, kopii):
    stroki = ["- %s | Claude | копия в %s — старая, перевести на lib при правке урока" % (DATA, k["fajl"])
              for k in kopii if k["imya"] == atom["imya"]]
    return stroki


# atom_tekstom: файл атома-кандидата в формате словаря
def atom_tekstom(a, kommit, kopii):
    vyhod = "значение" if re.search(r"\breturn\b", a["telo"]) else "—"
    stroki = ["```атом", "id: " + a["id"], "тип: код",
              "тема: код, слой %s, %s" % (a["sloj"], a["papka"]),
              "описание: " + a["chto"], "назначение: —",
              "вход: " + (a["param"] or "нет"), "выход: " + vyhod, "изменяет: —",
              "истинность: —", "проверено: нет",
              "источник: [О] teacher-workpad@%s %s: «// %s: %s»" % (kommit, a["fajl"], a["imya"], a["chto"]),
              "лицензия: неизвестно", "статус: черновик | %s | Claude" % DATA, "версия: %s | Claude" % DATA,
              "автор: Claude по заданию учителя", "критичный: -1",
              "состав: " + (", ".join(str(n) for n in a["sostav"]) or "нет"), "история:",
              "- %s | Claude | создан кандидатом программой tools/slovar-iz-koda.py; описание — строка над словом, тело не проверялось" % DATA]
    stroki += kopii_atoma(a, kopii) + ["```", ""]
    return "\n".join(stroki)


# tablica: Markdown-таблица всех атомов
def tablica(atomy, kopii):
    stroki = ["| № | слово | папка | слой | состав | что делает |", "|---|---|---|---|---|---|"]
    stroki += ["| %d | `%s` | %s | %s | %s | %s |" % (a["nomer"], a["imya"], a["papka"], a["sloj"],
               ", ".join(map(str, a["sostav"])) or "—", a["chto"].replace("|", "/")) for a in atomy]
    stroki += ["", "Копии общих слов в уроках (атомов не дают): %d — %s" % (len(kopii), ", ".join(sorted({k["fajl"] + ":" + k["imya"] for k in kopii})))]
    return "\n".join(stroki) + "\n"


# zapisat: атомы в папку выхода и таблица в файл списка
def zapisat(atomy, kopii, arg):
    papka = Path(arg.vyhod)
    for a in atomy:
        (papka / (a["id"] + ".md")).write_text(atom_tekstom(a, arg.kommit, kopii), encoding="utf-8")
    if arg.spisok:
        Path(arg.spisok).write_text(tablica(atomy, kopii), encoding="utf-8")
    return len(atomy)


# zanyato: номера, уже занятые в папке выхода (защита от повторной выдачи)
def zanyato(papka, atomy):
    est = {int(f.name[:4]) for f in Path(papka).glob("[0-9][0-9][0-9][0-9]-*")}
    return sorted(est & {a["nomer"] for a in atomy})


# razbor: аргументы командной строки
def razbor():
    r = argparse.ArgumentParser(description="слова JS-кода → кандидаты словаря")
    r.add_argument("koren"); r.add_argument("kommit"); r.add_argument("papki", nargs="+")
    r.add_argument("--nomer", type=int, required=True)
    r.add_argument("--obshchie", action="append", default=[])
    r.add_argument("--ne-kopii", action="append", default=[], dest="ne_kopii")
    r.add_argument("--vyhod", default="slovar/0001-realnost/kandidaty")
    r.add_argument("--spisok"); r.add_argument("--proba", action="store_true")
    return r.parse_args()


# glavnoe: разобрать, пронумеровать, проверить номера, записать
def glavnoe():
    arg = razbor()
    slova = vse_slova(arg.koren, arg.obshchie + arg.papki)
    atomy, kopii = razdelit(slova, set(arg.obshchie), set(arg.ne_kopii))
    atomy = sostavit(pronumerovat(atomy, arg.nomer), set(arg.obshchie))
    zanyatye = zanyato(arg.vyhod, atomy)
    kod = 1 if zanyatye else 0
    if zanyatye:
        print("номера заняты:", zanyatye[:10], file=sys.stderr)
    elif arg.proba:
        print(tablica(atomy, kopii))
    else:
        print("записано атомов:", zapisat(atomy, kopii, arg), "копий:", len(kopii))
    return kod


if __name__ == "__main__":
    sys.exit(glavnoe())
