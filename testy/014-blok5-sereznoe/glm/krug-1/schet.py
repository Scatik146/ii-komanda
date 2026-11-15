# najti_id_chitatelya: ищет id читателя по имени, возвращает None если не найден
def najti_id_chitatelya(dannye, imya):
    for c in dannye["chitateli"]:
        if c["imya"] == imya:
            return c["id"]
    return None
# kniga_sushchestvuet: проверяет, есть ли книга с таким id в списке книг
def kniga_sushchestvuet(dannye, id_knigi):
    for k in dannye["knigi"]:
        if k["id"] == id_knigi:
            return True
    return False
# chislo_vydach: считает выдачи читателя, где книга есть в списке книг
def chislo_vydach(dannye, id_chitatelya):
    n = 0
    for v in dannye["vydachi"]:
        if v["chitatel"] == id_chitatelya and kniga_sushchestvuet(dannye, v["kniga"]):
            n = n + 1
    return n
# skolko_knig: сколько книг взял читатель с этим именем
def skolko_knig(dannye, imya):
    id_chitatelya = najti_id_chitatelya(dannye, imya)
    if id_chitatelya is None:
        return 0
    return chislo_vydach(dannye, id_chitatelya)
