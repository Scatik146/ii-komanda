# Псевдопамять словаря «Форто-Пролог».
# Вселенная — папка словаря; миры — её подпапки с номером («0001-realnost/…»);
# служебные папки без номера («kandidaty», «sistema»).
# Мир атома — ближайшая папка мира в пути; опора мира — папка мира над ним,
# у корневого мира (папка прямо во вселенной) — он сам.
# Адрес слова — номер по порядку первого появления при сборке:
# опора и части раньше целого; повторно встреченное слово адрес не получает
# (как sys.modules в Python: модуль загружается при первом import).
# Адреса не хранятся в карточках; выгрузка пересобирается при каждом запуске.
# Запуск: python3 pamyat.py <папка-вселенной> <корень> [<корень> ...]
import os
import sys

NACHALO = "```атом"
KONEC = "```"
MIR = "описание мира"


# stroki_bloka: строки блока «атом» из текста карточки
def stroki_bloka(tekst):
    stroki = tekst.split("\n")
    nachalo = stroki.index(NACHALO) + 1
    konec = stroki.index(KONEC, nachalo)
    blok = stroki[nachalo:konec]
    return blok


# pole: значение поля «ключ: значение» или пусто
def pole(blok, klyuch):
    znachenie = ""
    for stroka in blok:
        if stroka.startswith(klyuch + ": "):
            znachenie = stroka[len(klyuch) + 2:].strip()
    return znachenie


# nomera_sostava: список номеров из поля «состав»
def nomera_sostava(zapis):
    nomera = []
    if zapis not in ("", "нет"):
        nomera = [int(chast) for chast in zapis.split(",")]
    return nomera


# nomer_papki: номер мира по имени папки или None для служебной
def nomer_papki(imya):
    nomer = None
    if imya[:4].isdigit() and imya[4:5] == "-":
        nomer = int(imya[:4])
    return nomer


# miry_puti: номера миров по пути от вселенной вглубь
def miry_puti(otnositelnyj):
    chasti = otnositelnyj.split(os.sep) if otnositelnyj != "." else []
    miry = [nomer_papki(c) for c in chasti if nomer_papki(c) is not None]
    return miry


# opora: опора мира по цепочке миров пути; у корня — он сам
def opora(miry):
    nomer = miry[-1]
    if len(miry) > 1:
        nomer = miry[-2]
    return nomer


# prochitat: карточка из файла — номер, тип, мир, связи (опора и состав)
def prochitat(put, miry):
    with open(put, encoding="utf-8") as f:
        blok = stroki_bloka(f.read())
    ident = pole(blok, "id")
    kartochka = {"номер": int(ident.split("-")[0]), "id": ident, "тип": pole(blok, "тип"),
                 "мир": miry[-1] if miry else None, "связи": nomera_sostava(pole(blok, "состав"))}
    if kartochka["тип"] == MIR:
        kartochka["связи"] = [opora(miry)] + kartochka["связи"]
    return kartochka


# kartochki_papki: карточки одной папки по номерам
def kartochki_papki(mesto, miry):
    vse = {}
    for imya in sorted(os.listdir(mesto)):
        if imya[:4].isdigit() and imya.endswith(".md"):
            kartochka = prochitat(os.path.join(mesto, imya), miry)
            vse[kartochka["номер"]] = kartochka
    return vse


# slovar: все карточки вселенной — обход дерева миров
def slovar(vselennaya):
    vse = {}
    for mesto, _, _ in os.walk(vselennaya):
        miry = miry_puti(os.path.relpath(mesto, vselennaya))
        vse.update(kartochki_papki(mesto, miry))
    return vse


# razmestit: разместить слово, его опору и части; они раньше целого
def razmestit(nomer, vse, pamyat, put):
    if nomer not in pamyat and nomer not in put and nomer in vse:
        for chast in vse[nomer]["связи"]:
            razmestit(chast, vse, pamyat, put + [nomer])
        pamyat[nomer] = len(pamyat) + 1
    return pamyat


# razdat: раздать адреса, обходя корни по порядку
def razdat(korni, vse):
    pamyat = {}
    for koren in korni:
        razmestit(koren, vse, pamyat, [])
    return pamyat


# stroka_pamyati: строка таблицы для одного слова
def stroka_pamyati(adres, kartochka):
    mir = f"{kartochka['мир']:04d}" if kartochka["мир"] is not None else "—"
    stroka = f"| {adres} | {kartochka['id']} | {kartochka['тип']} | {mir} |"
    return stroka


# vygruzit: таблица памяти в Markdown
def vygruzit(pamyat, vse, korni):
    stroki = ["# Псевдопамять словаря (выгрузка)", "",
              "Строит `ii-py/slovar/pamyat.py`; руками не править. Корни обхода: " + ", ".join(f"{k:04d}" for k in korni) + ".",
              "", "| Адрес | Атом | Тип | Мир |", "|---|---|---|---|"]
    for nomer, adres in pamyat.items():
        stroki.append(stroka_pamyati(adres, vse[nomer]))
    vne = [vse[n]["id"] for n in vse if n not in pamyat]
    stroki += ["", "Не вошли в сборку: " + (", ".join(vne) if vne else "нет") + "."]
    return "\n".join(stroki) + "\n"


# zapusk: верхнее — прочитать вселенную, раздать адреса, напечатать выгрузку
def zapusk(argumenty):
    vselennaya = argumenty[0]
    korni = [int(k) for k in argumenty[1:]]
    vse = slovar(vselennaya)
    print(vygruzit(razdat(korni, vse), vse, korni), end="")
    return 0


if __name__ == "__main__":
    sys.exit(zapusk(sys.argv[1:]))
