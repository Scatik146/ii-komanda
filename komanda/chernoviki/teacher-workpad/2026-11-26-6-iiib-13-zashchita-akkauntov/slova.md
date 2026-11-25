# Пополнение словаря: урок 13 ИИИБ 6 кл. «Защита аккаунтов» (teacher-workpad @ 0e52f17)

`tools/slovar-iz-koda.py --proba` кандидатов урока не нашёл: код — внутри HTML, не в `.js` (25.11). Список составлен руками; кандидаты в `slovar/` не вносила.

**Взято готовым** (`lib/slova/slova.js`): `el`, `sozdat`, `knopkaPechati`, `narisovatKonspekt`. **Колода слайдов** (`skrytye`, `pokazat`, `vpered`, `nazad`, `klavisha`) и `slajdGrafa` — копия из `9-klass/iiib-10-rech/slajdy.html`; тела не менялись, кроме `Slova.el`. Это уже не первый урок с колодой — кандидат в `lib/` (ОЧ-09), сначала сверить тела с «Цветом» и «Вратами» (ОЧ-Б2).

| слово | файл | слой | что делает | из каких слов |
|---|---|---|---|---|
| `znachenie` | slajdy.html | нижний | текст из TEKST по пути «a.b» | — |
| `podstavitTeksty` | slajdy.html | средний | элементы с `data-t` получают текст урока | znachenie |
| `zapolnitSpisok` | slajdy.html | нижний | пункты списка из массива строк | Slova.sozdat |
| `podstavitSpiski` | slajdy.html | средний | элементы с `data-spisok` получают пункты | znachenie, zapolnitSpisok |
| `kadr`, `risovatKadry` | slajdy.html | нижний / средний | кадр комикса; кадры по номерам из `data-kadry` | Slova.sozdat |
| `karta`, `risovatMify` | slajdy.html | нижний / средний | карточка «правда или выдумка» (П-16), ответ по щелчку | Slova.sozdat, Slova.el |
| `stroka`, `tablica`, `pary` | slajdy.html | нижний | строка таблицы; таблица из шапки и строк; строки из двух полей записей | Slova.sozdat, Slova.el |
| `risovatTablicy` | slajdy.html | средний | образец треков, защита, ID, правила пароля | tablica, pary, zapolnitSpisok |
| `vpisat` | slajdy.html | нижний | высокая схема ДРАКОН-ГРАФ вписывается в слайд по высоте | — |
| `risovatGrafSlajdy` | slajdy.html | средний | каждая схема конспекта — на своё место `graf-N` | slajdGrafa |
| `postroit` | slajdy.html | верхний | все тексты, кадры, карточки, таблицы, схемы | podstavitTeksty … risovatGrafSlajdy |
| `kartochkaSleda`, `kartochkaMifa`, `postroitDosye` | dosye.html | нижний / верхний | след досье; миф в `<details>`; страница досье целиком | Slova.sozdat, Slova.el |
| `prostoj`, `strokaTreka`, `risovatTreki` | drakon-list.html | нижний / средний | лист с подсказкой (`#prostoj`); строка карты треков | Slova.sozdat |
| `risovatBatarejku`, `risovatSpiski`, `risovatGraf`, `pechatProstogo`, `risovatList` | drakon-list.html | средний / верхний | батарейка защиты; чек-лист и ДЗ; три схемы; печать листа с подсказкой; лист целиком | Slova.narisovatKonspekt, Slova.knopkaPechati |
| `punktMifa`, `postroitShpargalku` | shpargalka.html | нижний / верхний | ключ к мифу; ключи и сверка | Slova.sozdat, Slova.el |

`podstavitTeksty` + `podstavitSpiski` (`data-t`, `data-spisok`) — способ «тексты из tekst.js в разметку без кода на каждый блок»; при повторе во втором уроке — кандидат в `lib/slova/`.
