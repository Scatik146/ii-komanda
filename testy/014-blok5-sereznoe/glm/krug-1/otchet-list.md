# ДРАКОН-лист: отчёт по читателям
## Действия
```дракон
название: отчёт по читателям
ввод: dannye
r = []
i = 0
пока: i < dannye.chitateli.length
  c = dannye.chitateli[i]
  spisok = spisok_knig_chitatelya(dannye, c.id)
  вопрос: spisok.length == 0
    да: s = c.imya + ": ничего не взял"
    нет:
      s = c.imya + ": " + spisok.join(", ")
      вопрос: spisok.length >= POROG_MNOGO
        да: s = s + " (много)"
        нет: s = s
  r.push(s)
  i = i + 1
вывод: r
```
## Данные
```конспект
тема: Данные отчёта
knigi -> id, nazvanie, avtor
chitateli -> id, imya
vydachi -> id, kniga, chitatel
pole kniga -> ссылка на knigi.id
pole chitatel -> ссылка на chitateli.id
порог много -> 2
```
## Тест
- пример: Тимур (книги 1 и 3) → «Тимур: Карта сети, Тайна пароля (много)»
- пример: читатель без книг → «Олег: ничего не взял»
- контрпример: Вера (1 книга) → «Вера: Робот и ветер (много)»
- контрпример: Тимур → «Тимур: Тайна пароля, Карта сети» (без сортировки)
