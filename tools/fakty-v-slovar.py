"""fakty-v-slovar.py — проверенные цитатой кандидаты-факты (блоки ```кандидат) → атомы `тип: факт`.

    python3 tools/fakty-v-slovar.py <kandidaty.md> <коммит teacher-workpad> --nomer 9393 --metka 044
        --zametka 'Ф-16=текст'     строка истории к факту (можно много раз)
        --citata 'Ф-46=текст'      исправленная дословная цитата (если исполнитель ошибся)
        --vyhod slovar/0001-realnost/kandidaty   --proba

Цитаты проверяет до этого `tools/analiz.py citaty`. Истинность каждого факта — 0 (ОЧ-01:
источник не сверен), проверено — нет. Мир: `реальность` → 0001, `урок` → 0003 (оговорка 0006).
Код по-фортовски.
"""
import argparse
import sys
from pathlib import Path

DATA = "2026-11-23"
MIR = {"реальность": ("0001", "Реальность"), "урок": ("0003", "учебный урок, оговорка 0006")}


# bloki: блоки ```кандидат файла → список словарей полей
def bloki(tekst):
    spisok, tek = [], None
    for stroka in tekst.splitlines():
        s = stroka.strip()
        if tek is None and s == "```кандидат":
            tek = {}
        elif tek is not None and s.startswith("```"):
            spisok.append(tek)
            tek = None
        elif tek is not None and ":" in s:
            k, _, v = s.partition(":")
            tek[k.strip()] = v.strip()
    return spisok


# pary: список 'Ф-NN=текст' → словарь номер → список текстов
def pary(spisok):
    d = {}
    for p in spisok:
        k, _, v = p.partition("=")
        d.setdefault(k.strip(), []).append(v.strip())
    return d


# atom: текст атома-факта
def atom(k, nomer, arg, zametki, citaty):
    mir, imya_mira = MIR[k["словарь"]]
    aid = "%d-fakt-%s-%s" % (nomer, arg.metka, k["номер"].lower().replace("ф-", "f"))
    citata = citaty.get(k["номер"], [k["цитата"]])[0]
    stroki = ["```атом", "id: " + aid, "тип: факт",
              "тема: факт урока, %s, мир %s (%s)" % (str(Path(k["файл"]).parent), mir, imya_mira),
              "описание: " + k["запись"], "назначение: банк фактов: урок берёт проверенный факт, а не ищет заново",
              "вход: нет", "выход: значение", "изменяет: нет",
              "истинность: %s = 0" % mir, "проверено: нет",
              "источник: [О] teacher-workpad@%s %s: «%s»" % (arg.kommit, k["файл"], citata),
              "лицензия: неизвестно", "статус: черновик | %s | Claude" % DATA, "версия: %s | Claude" % DATA,
              "автор: учитель", "критичный: 0", "состав: нет", "история:",
              "- %s | DeepSeek | выписан по заданию %s (%s)" % (DATA, arg.metka, k["номер"]),
              "- %s | Claude | цитата сверена с файлом программой analiz.py citaty; источник факта не сверен — истинность 0" % DATA]
    stroki += ["- %s | Claude | %s" % (DATA, z) for z in zametki.get(k["номер"], [])]
    return aid, "\n".join(stroki + ["```", ""])


# razbor: аргументы командной строки
def razbor():
    r = argparse.ArgumentParser(description="кандидаты-факты → атомы")
    r.add_argument("kandidaty"); r.add_argument("kommit")
    r.add_argument("--nomer", type=int, required=True); r.add_argument("--metka", required=True)
    r.add_argument("--zametka", action="append", default=[]); r.add_argument("--citata", action="append", default=[])
    r.add_argument("--vyhod", default="slovar/0001-realnost/kandidaty"); r.add_argument("--proba", action="store_true")
    return r.parse_args()


# glavnoe: прочитать блоки, проверить номера, записать атомы
def glavnoe():
    arg = razbor()
    spisok = bloki(Path(arg.kandidaty).read_text(encoding="utf-8"))
    zanyato = [n for n in range(arg.nomer, arg.nomer + len(spisok)) if list(Path(arg.vyhod).glob("%d-*" % n))]
    kod = 1 if zanyato else 0
    for i, k in enumerate(spisok if not zanyato else []):
        aid, tekst = atom(k, arg.nomer + i, arg, pary(arg.zametka), pary(arg.citata))
        if not arg.proba:
            (Path(arg.vyhod) / (aid + ".md")).write_text(tekst, encoding="utf-8")
    print("номера заняты: %s" % zanyato if zanyato else "атомов: %d (%d–%d)" % (len(spisok), arg.nomer, arg.nomer + len(spisok) - 1))
    return kod


if __name__ == "__main__":
    sys.exit(glavnoe())
