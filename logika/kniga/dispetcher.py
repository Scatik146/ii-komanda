# dispetcher.py — диспетчер проверок части 2: Python, Пролог, Форт
# Пролог проверяет аналитически, Форт - векторами и счётом, Python раздаёт и сводит итог.
# запуск: python3 logika/kniga/dispetcher.py <путь к клону drakon-graf>
import subprocess
import sys
from pathlib import Path

# Данные.
ZDES = Path(__file__).parent
PYTHON = [("proverka_A2.py", "chast-2-trit/A-osnova.md"), ("proverka_B2.py", "chast-2-trit/B-zakony.md"),
          ("proverka_V.py", "chast-2-trit/V-dejstviya.md"), ("proverka_G2.py", None), ("proverka_D1.py", None),
          ("proverka_D2.py", None), ("proverka_D3.py", None), ("proverka_E1.py", None), ("proverka_E2.py", None),
          ("proverka_E3.py", None), ("proverka_E4.py", None), ("proverka_E5.py", None)]
PROLOG_LIB = "site/experiments/prolog/lib"
FORT_LIB = "site/experiments/forth/lib/index.js"


# zapusk: выполнить команду в папке книги; (прошло ли, последняя строка вывода)
def zapusk(komanda):
    r = subprocess.run(komanda, cwd=ZDES, capture_output=True, text=True)
    stroki = (r.stdout + r.stderr).strip().splitlines() or ["(пусто)"]
    otvet = (r.returncode == 0, stroki[-1])
    return otvet


# komandy: что запускать - (имя, команда)
def komandy(drakon):
    spisok = [(f, [sys.executable, f] + ([a] if a else [])) for f, a in PYTHON]
    spisok.append(("Пролог", ["node", "prolog/zapusk.cjs", str(Path(drakon) / PROLOG_LIB)]))
    spisok.append(("Форт", ["node", "fort/zapusk.cjs", str(Path(drakon) / FORT_LIB)]))
    return spisok


# glavnoe: всё запустить, напечатать итог, код выхода - 0, если всё прошло
def glavnoe(drakon):
    plohih = 0
    for imya, komanda in komandy(drakon):
        proshlo, posled = zapusk(komanda)
        plohih += 0 if proshlo else 1
        print(("да   " if proshlo else "НЕТ  ") + imya + ": " + posled)
    print("Диспетчер: всё прошло" if plohih == 0 else f"Диспетчер: не прошло {plohih}")
    return 0 if plohih == 0 else 1


if __name__ == "__main__":
    sys.exit(glavnoe(sys.argv[1] if len(sys.argv) > 1 else "../../../drakon-graf"))
