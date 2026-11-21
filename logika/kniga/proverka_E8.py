# proverka_E8.py — проверка листка Е.8 «Листок на стену» (часть 2)
# запуск: python3 logika/kniga/proverka_E8.py
# Листок сверяется с самим шагом Е: те же группы, столько же правил, по порядку.
import re
from pathlib import Path

# Данные.
KNIGA = Path(__file__).parent / "chast-2-trit" / "E-pravila.md"
S_PRAVILAMI = ("Е.2", "Е.3", "Е.4", "Е.5", "Е.6", "Е.7")    # подразделы, где есть правила
VSEGO = 46
DLINA = 70                                               # знаков в строке листа А4


# razdely: текст шага Е по подразделам - {номер: (название, текст)}
def razdely(tekst):
    chasti = re.split(r"^## (Е\.\d)\. (.+)$", tekst, flags=re.M)
    otvet = {chasti[i]: (chasti[i + 1].strip(), chasti[i + 2]) for i in range(1, len(chasti), 3)}
    return otvet


# pravil: сколько правил в подразделе
def pravil(tekst):
    otvet = len(re.findall(r"^\*\*Правило \d+\. ", tekst, flags=re.M))
    return otvet


# listok: группы листка - [(название, [(номер, строка)])]
def listok(tekst):
    blok = tekst.split("**Все правила проверены. К сожалению, на авторе.**", 1)[1].split("\n---", 1)[0]
    gruppy = []
    for stroka in blok.splitlines():
        zagolovok = re.fullmatch(r"\*\*([^*]+)\*\*", stroka.strip())
        punkt = re.fullmatch(r"(\d+)\. (.+)", stroka.strip())
        if zagolovok and not stroka.startswith("**Если"):
            gruppy.append((zagolovok.group(1), []))
        elif punkt:
            gruppy[-1][1].append((int(punkt.group(1)), punkt.group(2)))
    otvet = gruppy
    return otvet


# Проверки.
tekst = KNIGA.read_text(encoding="utf-8")
r = razdely(tekst)
gruppy = listok(r["Е.8"][1])

# 1. Группы - те же подразделы, в том же порядке
assert [g for g, _ in gruppy] == [r[n][0] for n in S_PRAVILAMI]

# 2. В каждой группе - столько строк, сколько правил в подразделе
for (g, stroki), n in zip(gruppy, S_PRAVILAMI):
    assert len(stroki) == pravil(r[n][1]), g

# 3. Всего 46, номера подряд
nomera = [nom for _, stroki in gruppy for nom, _ in stroki]
assert nomera == list(range(1, VSEGO + 1))

# 4. Строка помещается в строку листа
for _, stroki in gruppy:
    for nom, s in stroki:
        assert len(s) <= DLINA, (nom, len(s))

# 5. В подразделах без правил правил нет (Е.0, Е.1, Е.8)
for n in ("Е.0", "Е.1", "Е.8"):
    assert pravil(r[n][1]) == 0

print("групп:", len(gruppy), "строк:", len(nomera), "самая длинная:",
      max(len(s) for _, st in gruppy for _, s in st))
print("Е.8: все проверки прошли")
