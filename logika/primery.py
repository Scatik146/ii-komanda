# Общие примеры для Форта и Пролога: перебор всех тритов по эталону (Марьям, 19.11.2026)
# Запуск: python3 primery.py — пишет primery.json рядом. Эталон — слова proverka.py.
# Одно место знания (ОЧ-10): Форт и Пролог сверяются с одним и тем же файлом.

import json
import runpy
from itertools import product
from pathlib import Path

E = runpy.run_path(str(Path(__file__).with_name("proverka.py")))
V, ne, i, ili, L, M, Q = E["V"], E["ne"], E["i"], E["ili"], E["L"], E["M"], E["Q"]


# po_spisku: нашли — 1; не нашли по полному списку — −1; иначе 0
def po_spisku(est, polnyj):
    return ili(est, i(ne(polnyj), 0))


# k_sroku: до срока 0, после — факт (Т3)
def k_sroku(sdelano, srok):
    return po_spisku(sdelano, srok)


# SLOVA: (имя на Форте, имя на Прологе, число входов, эталон)
SLOVA = [
    ("не", "не", 1, ne), ("и", "и", 2, i), ("или", "или", 2, ili),
    ("согласие", "согласие", 2, E["soglasie"]), ("основание", "основание", 2, E["osn"]),
    ("ворота", "ворота", 1, L), ("возможно", "возможно", 1, M), ("не-знаю?", "не_знаю", 1, Q),
    ("запрет", "запрет", 2, E["zapret"]), ("проверено", "проверено", 2, E["prov"]),
    ("пров-к-сроку", "пров_к_сроку", 2, E["osn"]),
    ("экспертиза", "экспертиза", 3, E["ekspertiza"]), ("ошибка-сказки?", "ошибка_сказки", 2, E["zapret"]),
    ("спор", "спор", 2, E["soglasie"]), ("по-списку", "по_списку", 2, po_spisku),
    ("следует", "следует", 3, E["sleduet"]), ("для-всех", "для_всех", 1, ne),
    ("не-доказано", "не_доказано", 1, ne), ("равносильно", "равносильно", 2, i),
    ("восстановимо", "восстановимо", 2, E["vosst"]), ("наружу?", "наружу", 2, lambda a, b: L(i(a, b))),
    ("на-экспертизу?", "на_экспертизу", 2, lambda e, s: i(L(e), M(s))),
    ("включить?", "включить", 1, L), ("прочерк?", "прочерк", 1, lambda x: L(ne(x))),
    ("собирать?", "собирать", 1, L), ("с-нуля?", "с_нуля", 1, lambda x: L(ne(x))),
    ("придумывать?", "придумывать", 1, lambda x: L(ne(x))), ("искать?", "искать", 1, Q),
    ("параллельно?", "параллельно", 2, lambda a, b: i(L(a), L(b))),
    ("заменить?", "заменить", 2, lambda a, b: L(i(a, b))),
    ("без-чужих-глаз?", "без_чужих_глаз", 2, lambda e, c: i(L(e), ne(L(c)))),
    ("было", "было", 2, po_spisku), ("всегда-было", "всегда_было", 2, lambda n, p: ne(po_spisku(n, p))),
    ("к-сроку", "к_сроку", 2, k_sroku), ("пока-цело", "пока_цело", 1, lambda n: -1 if n == 1 else 0),
    ("годно", "годно", 2, E["osn"]), ("после", "после", 1, L), ("прогноз-сейчас", "прогноз_сейчас", 1, lambda p: 0),
    ("неотвратимо", "неотвратимо", 4, lambda a, b, c, p: E["osn"](E["budet"]([a, b, c]), p)),
    ("может-быть", "может_быть", 3, lambda a, b, c: max(a, b, c)),
    ("под-рукой?", "под_рукой", 3, lambda a, b, c: L(max(a, b, c))),
    ("обещать?", "обещать", 2, lambda a, b: ili(L(a), L(b))), ("хватит?", "хватит", 2, lambda a, b: ili(L(a), L(b))),
    ("готовиться?", "готовиться", 1, L), ("ещё-не-поздно?", "ещё_не_поздно", 1, Q),
    ("усомниться", "усомниться", 2, lambda x, c: E["osn"](x, ne(c))),
]


# sluchai_slova: все наборы тритов для одного слова и ответ эталона
def sluchai_slova(fort, prolog, n, etalon):
    st = []
    for vhod in product(V, repeat=n):
        st.append({"fort": fort, "prolog": prolog, "vhod": list(vhod), "zhdem": etalon(*vhod)})
    return st


# sobrat: все случаи всех слов → primery.json
def sobrat():
    vse = [s for slovo in SLOVA for s in sluchai_slova(*slovo)]
    put = Path(__file__).with_name("primery.json")
    put.write_text(json.dumps(vse, ensure_ascii=False, indent=0), encoding="utf-8")
    print(len(SLOVA), "слов,", len(vse), "случаев →", put.name)
    return len(vse)


if __name__ == "__main__":
    sobrat()
