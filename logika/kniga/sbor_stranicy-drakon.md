# ДРАКОН-лист: сборка страницы книги (sbor_stranicy.py)

## Действия

```дракон
название: Сборка страницы
ввод: imya
ishodnik = ZDES / imya
stil = prochitat(kniga.css)
md = prochitat(ishodnik)
stranica = sobrat(md, stil)
put = zapisat(ishodnik, stranica)
вывод: put
```

## Данные

```конспект
тема: Раздел книги -> страница сайта
chast-1-bit/A-osnova.md -> stranicy/A-osnova.html: Markdown в HTML
stranicy/kniga.css -> stranicy/A-osnova.html: оформление встроено
```

## Тест

- пример: ввод chast-1-bit/A-osnova.md → вывод stranicy/A-osnova.html с заголовком «Часть 1. Бит. Шаг А. Основа», 1 таблицей и 4 списками
- контрпример: ввод chast-1-bit/A-osnova.md → в странице есть `style="`

## Пополнение словаря

- prochitat — нижний — текст файла — read_text
- zagolovok — нижний — первая строка «# …» без решётки — splitlines, lstrip
- telo — нижний — Markdown → HTML с таблицами — markdown
- sobrat — средний — страница целиком — zagolovok, telo, SHABLON
- zapisat — нижний — сохранить страницу в stranicy/ — write_text
- glavnoe — верхний — раздел → страница — prochitat, sobrat, zapisat
