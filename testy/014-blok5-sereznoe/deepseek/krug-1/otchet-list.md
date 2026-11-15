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
