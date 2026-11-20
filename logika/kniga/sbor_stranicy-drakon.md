# ДРАКОН-лист: сборка страницы книги (sbor_stranicy.py)

## Действия

```дракон
название: Сборка страницы
ввод: imya
ishodnik = ZDES / imya
stil = prochitat(kniga.css)
md = prochitat(ishodnik)
md = ssylki(md, ishodnik)
stranica = sobrat(md, stil)
put = zapisat(ishodnik, stranica)
вывод: put
```

## Данные

```конспект
тема: Раздел книги -> страница сайта
chast-1-bit/A-osnova.md -> stranicy/A-osnova.html: Markdown в HTML
stranicy/kniga.css -> stranicy/A-osnova.html: оформление встроено
chast-2-trit/A-osnova.md -> stranicy/chast-2-trit/A-osnova.html: своя папка, имена частей не сталкиваются
dejstvuyushchie-lica.md -> stranicy/dejstvuyushchie-lica.html: заголовки с якорями как на GitHub
```

## Тест

- пример: ввод chast-1-bit/A-osnova.md → вывод stranicy/A-osnova.html с заголовком «Часть 1. Бит. Шаг А. Основа», 1 таблицей и 4 списками
- контрпример: ввод chast-1-bit/A-osnova.md → в странице есть `style="`
- пример: ввод chast-2-trit/A-osnova.md → вывод stranicy/chast-2-trit/A-osnova.html, страница части 1 stranicy/A-osnova.html не тронута

- пример: в B-zakony.html ссылка `dejstvuyushchie-lica.html#5-огастес-де-морган`, в chast-2-trit/A-osnova.html — `../dejstvuyushchie-lica.html#1-аристотель`; все 38 ссылок попадают в существующие id
- контрпример: ссылка `../dejstvuyushchie-lica.md#…` в готовой странице не остаётся

## Пополнение словаря

- prochitat — нижний — текст файла — read_text
- zagolovok — нижний — первая строка «# …» без решётки — splitlines, lstrip
- metka — нижний — якорь заголовка как на GitHub — re.sub, lower
- telo — нижний — Markdown → HTML с таблицами и якорями — markdown, toc, metka
- ssylki — нижний — ссылки на сводки: .md → .html, путь от папки — papka, replace
- sobrat — средний — страница целиком — zagolovok, telo, SHABLON
- papka — нижний — часть 1 в stranicy/, другие в stranicy/<часть>/ — mkdir
- zapisat — нижний — сохранить страницу в свою папку — papka, write_text
- glavnoe — верхний — раздел → страница — prochitat, sobrat, zapisat
