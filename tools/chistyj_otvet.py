# chistyj_otvet.py: ответ модели без следов копирования из чата — печатает испорченные строки
#   python tools/chistyj_otvet.py otvet-glm.md      код выхода 0 — чисто, 1 — следы есть
# Код по-фортовски (ii-komanda pravila/KOD-PO-FORTOVSKI.md); ДРАКОН-лист — test-zapusk-list.md.
import sys

# Данные. Следы копирования (в 009 у GLM): пробел-сущность и экранированная скобка.
SLEDY = ('&#x20;', '\\[')


# isporchena: в строке есть след копирования
def isporchena(stroka):
    return any(sled in stroka for sled in SLEDY)


# nomera_isporchennyh: номера испорченных строк файла (с 1)
def nomera_isporchennyh(put):
    with open(put, encoding='utf-8') as f:
        stroki = f.read().split('\n')
    return [i + 1 for i, s in enumerate(stroki) if isporchena(s)]


# proverit: напечатать итог; 0 — чисто, 1 — испорчено
def proverit(put):
    nomera = nomera_isporchennyh(put)
    if nomera:
        print('Следы копирования (&#x20; или \\[) в строках:', ', '.join(map(str, nomera[:20])))
    else:
        print('Ответ чистый:', put)
    return 1 if nomera else 0


if __name__ == '__main__':
    sys.exit(proverit(sys.argv[1]))
