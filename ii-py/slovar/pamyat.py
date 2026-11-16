# Псевдопамять словаря «Форто-Пролог».
# Адрес слова — номер по порядку первого появления при сборке:
# сначала части, потом целое; повторно встреченное слово адрес не получает.
# Как sys.modules в Python: модуль загружается при первом import и дальше переиспользуется.
# Адреса не хранятся в карточках; выгрузка пересобирается при каждом запуске.
# Запуск: python3 pamyat.py <папка-словаря> <корень> [<корень> ...]
import os
import sys

NACHALO = "```атом"
KONEC = "```"


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


# prochitat: карточка из файла — номер, имя, тип, состав
def prochitat(put):
    with open(put, encoding="utf-8") as f:
        blok = stroki_bloka(f.read())
    ident = pole(blok, "id")
    kartochka = {
        "номер": int(ident.split("-")[0]),
        "id": ident,
        "тип": pole(blok, "тип"),
        "состав": nomera_sostava(pole(blok, "состав")),
    }
    return kartochka


# slovar: все карточки папки по номерам
def slovar(papka):
    vse = {}
    for imya in sorted(os.listdir(papka)):
        if imya[:4].isdigit() and imya.endswith(".md"):
            kartochka = prochitat(os.path.join(papka, imya))
            vse[kartochka["номер"]] = kartochka
    return vse


# razmestit: разместить слово и его части; части раньше целого
def razmestit(nomer, vse, pamyat, put):
    if nomer not in pamyat and nomer not in put and nomer in vse:
        for chast in vse[nomer]["состав"]:
            razmestit(chast, vse, pamyat, put + [nomer])
        pamyat[nomer] = len(pamyat) + 1
    return pamyat


# razdat: раздать адреса, обходя корни по порядку
def razdat(korni, vse):
    pamyat = {}
    for koren in korni:
        razmestit(koren, vse, pamyat, [])
    return pamyat


# vygruzit: таблица памяти в Markdown
def vygruzit(pamyat, vse, korni):
    stroki = [
        "# Псевдопамять словаря (выгрузка)",
        "",
        "Строит `ii-py/slovar/pamyat.py`; руками не править. Корни обхода: " + ", ".join(map(str, korni)) + ".",
        "",
        "| Адрес | Атом | Тип |",
        "|---|---|---|",
    ]
    for nomer, adres in pamyat.items():
        stroki.append(f"| {adres} | {vse[nomer]['id']} | {vse[nomer]['тип']} |")
    vne = [vse[n]["id"] for n in vse if n not in pamyat]
    stroki += ["", "Не вошли в сборку: " + (", ".join(vne) if vne else "нет") + "."]
    return "\n".join(stroki) + "\n"


# zapusk: верхнее — прочитать словарь, раздать адреса, напечатать выгрузку
def zapusk(argumenty):
    papka = argumenty[0]
    korni = [int(k) for k in argumenty[1:]]
    vse = slovar(papka)
    tekst = vygruzit(razdat(korni, vse), vse, korni)
    print(tekst, end="")
    return 0


if __name__ == "__main__":
    sys.exit(zapusk(sys.argv[1:]))
