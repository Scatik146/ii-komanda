```
knigi.json
```
{
  "books": [
    {
      "id": 1,
      "title": "Тайна пароля",
      "author": "А. Ветров"
    },
    {
      "id": 2,
      "title": "Робот и ветер",
      "author": "Н. Лесной"
    },
    {
      "id": 3,
      "title": "Карта сети",
      "author": "И. Морозова"
    }
  ],
  "readers": [
    {
      "id": 101,
      "name": "Тимур"
    },
    {
      "id": 102,
      "name": "Вера"
    }
  ],
  "issues": [
    {
      "id": 1001,
      "book_id": 1,
      "reader_id": 101
    },
    {
      "id": 1002,
      "book_id": 3,
      "reader_id": 101
    },
    {
      "id": 1003,
      "book_id": 2,
      "reader_id": 102
    }
  ]
}
```

```
knigi.html
```
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="knigi.css">
</head>
<body>
  <h1 class="library-title">Школьная библиотека</h1>
  <ul class="books-list">
    <li class="book-item">Тайна пароля (А. Ветров)</li>
    <li class="book-item">Робот и ветер (Н. Лесной)</li>
    <li class="book-item">Карта сети (И. Морозова)</li>
  </ul>
</body>
</html>
```

```
knigi.css
```
:root {
  --primary-color: blue;
  --secondary-color: lightgray;
  --padding-small: 8px;
  --padding-medium: 16px;
}

.library-title {
  color: var(--primary-color);
  padding: var(--padding-medium);
}

.books-list {
  list-style-type: none;
  padding: 0;
}

.book-item {
  background-color: var(--secondary-color);
  padding: var(--padding-small);
  margin-bottom: var(--padding-small);
  border-radius: 4px;
}
```

```
README.md
```
# Школьная библиотека: описание данных

## Файлы проекта

- `knigi.json` — данные о книгах, читателях и выдачах.
- `knigi.html` — страница «Школьная библиотека» со списком книг.
- `knigi.css` — стили для страницы.

Пример записи выдачи в формате Markdown:

````
````markdown
````json
{
  "id": 1001,
  "book_id": 1,
  "reader_id": 101
}
````
````
```

Что говорит `knigi.json`: описывает структуру данных школьной библиотеки — книги, читатели и факты выдачи книг читателям через ссылки по ID.
Что говорит `knigi.html`: представляет страницу «Школьная библиотека» с заголовком и списком книг, стили подключаются извне.
Что говорит `knigi.css`: задаёт визуальное оформление страницы через переменные и правила стилей для классов.

Пополнение словаря отношений:
- `выдача` — книга, читатель — факт выдачи книги читателю — состоит из связи book_id (ссылка на книгу) и reader_id (ссылка на читателя).
- `книга` — id, title, author — запись о книге в библиотеке.
- `читатель` — id, name — запись о читателе библиотеки.
```