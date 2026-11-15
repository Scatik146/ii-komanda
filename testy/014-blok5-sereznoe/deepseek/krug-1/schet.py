# Данные: {"knigi": [{"id", "nazvanie", "avtor"}], "chitateli": [{"id", "imya"}], "vydachi": [{"id", "kniga", "chitatel"}]}
# id_chitatelya: id читателя по имени или None
def id_chitatelya(dannye, imya):
    naydennyy = None
    for chitatel in dannye["chitateli"]:
        if chitatel["imya"] == imya:
            naydennyy = chitatel["id"]
    return naydennyy
# est_li_kniga: есть ли книга с таким id в списке книг
def est_li_kniga(knigi, id_knigi):
    est = False
    for kniga in knigi:
        if kniga["id"] == id_knigi:
            est = True
    return est
# vydachi_chitatelya: выдачи читателя с этим id
def vydachi_chitatelya(dannye, id_chit):
    vybor = []
    for vydacha in dannye["vydachi"]:
        if vydacha["chitatel"] == id_chit:
            vybor.append(vydacha)
    return vybor
# schet_po_vydacham: сколько выдач указывают на существующую книгу
def schet_po_vydacham(vydachi, knigi):
    schet = 0
    for vydacha in vydachi:
        if est_li_kniga(knigi, vydacha["kniga"]):
            schet += 1
    return schet
# skolko_knig: сколько книг взял читатель с этим именем
def skolko_knig(dannye, imya):
    id_chit = id_chitatelya(dannye, imya)
    schet = 0
    if id_chit is not None:
        schet = schet_po_vydacham(vydachi_chitatelya(dannye, id_chit), dannye["knigi"])
    return schet
