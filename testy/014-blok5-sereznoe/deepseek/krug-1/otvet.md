Вход → результат (до переделки):

1) Данные: книги 1 «Тайна пароля», 2 «Робот и ветер», 3 «Карта сети»; читатели 1 Тимур, 2 Вера; выдачи: (1,1), (3,1), (2,2).
   Результат: `["Тимур: Карта сети, Тайна пароля (много)", "Вера: Робот и ветер"]`

2) Те же данные + читатель 3 Глеб без выдач.
   Результат: `["Тимур: Карта сети, Тайна пароля (много)", "Вера: Робот и ветер", "Глеб: ничего не взял"]`

knigi-otchet.js
```js
// Данные: { knigi: [{id, nazvanie, avtor}], chitateli: [{id, imya}], vydachi: [{id, kniga, chitatel}] }
const POROG_MNOGO = 2;
// nazvaniya_odnoy_vydachi: названия книг, на которые указывает выдача
function nazvaniya_odnoy_vydachi(vydacha, knigi) {
  const nazvaniya = [];
  for (const kniga of knigi) {
    if (kniga.id == vydacha.kniga) nazvaniya.push(kniga.nazvanie);
  }
  return nazvaniya;
}
// nazvaniya_knig: названия книг по списку выдач, по алфавиту
function nazvaniya_knig(vydachi, knigi) {
  const nazvaniya = [];
  for (const vydacha of vydachi) {
    const chast = nazvaniya_odnoy_vydachi(vydacha, knigi);
    for (const nazvanie of chast) {
      nazvaniya.push(nazvanie);
    }
  }
  nazvaniya.sort();
  return nazvaniya;
}
// knigi_chitatelya: выдачи одного читателя
function knigi_chitatelya(chitatel, dannye) {
  const vybor = [];
  for (const vydacha of dannye.vydachi) {
    if (vydacha.chitatel == chitatel.id) vybor.push(vydacha);
  }
  return vybor;
}
// stroka_net_knig: строка «имя: ничего не взял»
function stroka_net_knig(chitatel) {
  return chitatel.imya + ': ничего не взял';
}
// stroka_est_knigi: строка «имя: книги» с пометкой «много»
function stroka_est_knigi(chitatel, nazvaniya) {
  let stroka = chitatel.imya + ': ' + nazvaniya.join(', ');
  if (nazvaniya.length >= POROG_MNOGO) {
    stroka += ' (много)';
  }
  return stroka;
}
// stroka_chitatelya: строка отчёта про одного читателя
function stroka_chitatelya(chitatel, dannye) {
  const nazvaniya = nazvaniya_knig(knigi_chitatelya(chitatel, dannye), dannye.knigi);
  let stroka;
  if (nazvaniya.length === 0) {
    stroka = stroka_net_knig(chitatel);
  } else {
    stroka = stroka_est_knigi(chitatel, nazvaniya);
  }
  return stroka;
}
// otchet: отчёт по читателям, по строке на читателя
function otchet(dannye) {
  const stroki = [];
  for (const chitatel of dannye.chitateli) {
    stroki.push(stroka_chitatelya(chitatel, dannye));
  }
  return stroki;
}
if (typeof module !== 'undefined') module.exports = { otchet };
```

schet.py
```python
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
```

otchet-list.md
````markdown
# ДРАКОН-лист: отчёт по читателям
## Действия
```дракон
название: Отчёт по читателям
stroki = []
для: for (const chitatel of dannye.chitateli)
  nazvaniya = nazvaniya_knig(knigi_chitatelya(chitatel, dannye), dannye.knigi)
  вопрос: nazvaniya.length == 0
    да:
      stroka = chitatel.imya + ': ничего не взял'
    нет:
      stroka = chitatel.imya + ': ' + nazvaniya.join(', ')
      вопрос: nazvaniya.length >= POROG_MNOGO
        да:
          stroka = stroka + ' (много)'
        нет:
  stroki.push(stroka)
вывод: stroki
```
## Данные
```конспект
тема: Данные отчёта
- книги: id, nazvanie, avtor
- читатели: id, imya
- выдачи: id, kniga, chitatel
- порог «много»: POROG_MNOGO = 2
```
## Тест
- пример: Тимур взял «Тайна пароля» и «Карта сети», Вера — «Робот и ветер» → `["Тимур: Карта сети, Тайна пароля (много)", "Вера: Робот и ветер"]`
- контрпример: тот же вход → `["Тимур: Тайна пароля, Карта сети (много)", "Вера: Робот и ветер"]`
````

Пополнение словаря (JS):
- nazvaniya_odnoy_vydachi — нижний — названия книг, на которые указывает выдача — (нет)
- nazvaniya_knig — средний — названия книг по списку выдач, по алфавиту — nazvaniya_odnoy_vydachi
- knigi_chitatelya — нижний — выдачи одного читателя — (нет)
- stroka_net_knig — нижний — строка «имя: ничего не взял» — (нет)
- stroka_est_knigi — средний — строка «имя: книги» с пометкой «много» — (нет)
- stroka_chitatelya — средний — строка отчёта про одного читателя — nazvaniya_knig, knigi_chitatelya, stroka_net_knig, stroka_est_knigi
- otchet — верхний — отчёт по читателям, по строке на читателя — stroka_chitatelya

Пополнение словаря (Python):
- id_chitatelya — нижний — id читателя по имени или None — (нет)
- est_li_kniga — нижний — есть ли книга с таким id в списке книг — (нет)
- vydachi_chitatelya — нижний — выдачи читателя с этим id — (нет)
- schet_po_vydacham — средний — сколько выдач указывают на существующую книгу — est_li_kniga
- skolko_knig — верхний — сколько книг взял читатель с этим именем — id_chitatelya, vydachi_chitatelya, schet_po_vydacham