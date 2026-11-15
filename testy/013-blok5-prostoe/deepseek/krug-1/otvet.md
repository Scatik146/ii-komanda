knigi.json
```json
{
  "knigi": [
    { "id": "k1", "nazvanie": "Тайна пароля", "avtor": "А. Ветров" },
    { "id": "k2", "nazvanie": "Робот и ветер", "avtor": "Н. Лесной" },
    { "id": "k3", "nazvanie": "Карта сети", "avtor": "И. Морозова" }
  ],
  "chitateli": [
    { "id": "ch1", "imya": "Тимур" },
    { "id": "ch2", "imya": "Вера" }
  ],
  "vydachi": [
    { "id": "v1", "kniga_id": "k1", "chitatel_id": "ch1" },
    { "id": "v2", "kniga_id": "k3", "chitatel_id": "ch1" },
    { "id": "v3", "kniga_id": "k2", "chitatel_id": "ch2" }
  ]
}
```
knigi.html
```html
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <title>Школьная библиотека</title>
  <link rel="stylesheet" href="knigi.css">
</head>
<body class="stranitsa">
  <h1>Школьная библиотека</h1>
  <ul class="spisok-knig">
    <li class="kniga">«Тайна пароля» — А. Ветров</li>
    <li class="kniga">«Робот и ветер» — Н. Лесной</li>
    <li class="kniga">«Карта сети» — И. Морозова</li>
  </ul>
</body>
</html>
```
knigi.css
```css
:root {
  --tsvet-fona: #f7f3e8;
  --tsvet-teksta: #2b2b2b;
  --otstup: 12px;
}

.stranitsa {
  background-color: var(--tsvet-fona);
  color: var(--tsvet-teksta);
}

.spisok-knig {
  padding: var(--otstup);
}

.kniga {
  margin-bottom: var(--otstup);
}
```
README.md
`````markdown
# Школьная библиотека

Описание файлов и примера записи выдачи.

## Файлы

- `knigi.json` — данные: книги, читатели, выдачи.
- `knigi.html` — страница «Школьная библиотека» со списком книг.
- `knigi.css` — вид страницы.

## Пример записи выдачи

````markdown
```json
{ "id": "v1", "kniga_id": "k1", "chitatel_id": "ch1" }
```
````
`````

- `knigi.json` — какие книги есть, кто читатели и кто какую книгу взял.
- `knigi.html` — что страница называется «Школьная библиотека» и что на ней список трёх книг.
- `knigi.css` — что цвета и отступы вынесены в переменные, а правила привязаны к классам страницы, списка книг и книги.
- `README.md` — какие файлы есть и как записывается выдача.

Пополнение словаря отношений:
- `книга` — участники: id, название, автор — что значит: книга числится в библиотеке.
- `читатель` — участники: id, имя — что значит: читатель записан в библиотеку.
- `выдача` — участники: id, книга, читатель — что значит: читатель взял книгу.