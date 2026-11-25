---
name: "teacher-workpad-sajt"
description: "Публикация уроков, приложений и материалов учителя на сайт teacher-workpad (GitHub Pages): клон, правила, каталог, проверка в браузере, списки, коммит."
---

# Сайт teacher-workpad

Сайт уроков учителя: `Scatik146/teacher-workpad` (GitHub Pages; запасной вариант — школьная сетевая папка без интернета). Всё по-русски: тексты, интерфейсы, коммиты.

## Начало работы
1. `add_repo` (owner `Scatik146`, repo `teacher-workpad`, access `push`), затем `git clone --depth 1 https://github.com/Scatik146/teacher-workpad /home/claude/teacher-workpad`.
2. `CLAUDE.md` репозитория — действующие правила, он главнее этого навыка. После `register_repo_root` он приходит сам: вручную не читать, копию из ii-komanda `pravila/проекты/` тоже не читать (16,5 КБ; каждая копия в истории оплачивается на каждом запросе). Не пришёл — прочитать один раз из клона.
3. Для помощников ИИ — ii-komanda `komanda/VHOD-UROKI.md`; копии навыков — ii-komanda `rezerv/navyki/` (обновляет навык `ekonomnaya-sessiya` в конце сессии). Журнал решений по ДРАКОН-ГРАФ и дракон-схемам — `Scatik146/ii-komanda`, `komanda/README.md`.

## Правила приложений
Одно место — `PRAVILA-PRILOZHENIJ.md` в корне сайта (решение учителя 25.11): читать один раз за сессию перед созданием или правкой приложения. Здесь не дублировать (Л28).

## Каталог и списки
- Урок — объект в `LESSONS` в `lessons.js` (`where:[{s:'iiib'|'inf'|'mat'|'trud', g:класс}]`, title, topic, about, format, path, teacher:[{label, href, kind:'slides'|'print'|'guide'|'tool'}]; `ready:false` — скрыт) и строка в таблице `README.md`.
- После изменений обновить `RAZRABOTANO.md` и `DORABOTKI.md`. В проект Claude «Разработка уроков» (`claude/Разработано teacher-workpad.md`, `claude/Доработки teacher-workpad.md`) записывать их **один раз — в конце задачи** (решение учителя 25.11, экономия лимита): `project_read` обоих, затем `project_write` с `local_path`. Правки между — только в файлах репозитория.

## Проверка перед отправкой
- **Сначала — одна команда проверки урока, один раз после последней правки:** `python3 -I tools/proverka-vsyo.py <папка урока> --kartinka svodka.png` (страницы через `proverka-uroka.py` — слайды, листы PDF, первый экран, консоль; ДРАКОН-листы, схемы, конспекты, стиль кода, тесты ДРАКОН при правке библиотеки, git). Отчёт и код выхода — в ответ учителю; сводную картинку **смотрит учитель** при приёмке, Claude её не открывает (учитель 25.11 03:17, задание 047).
- **Проход приложения путём пользователя — учитель при приёмке** (дешевле человеком, учитель 25.11 02:55): ему — список экранов, действий и что должно получиться. Учителя нет — пройти самой в headless Chrome (`/usr/bin/google-chrome` + Python playwright, file://, 1366×768, все ветки: обычная, ускоренная, ранний финал).
- Синтаксис скрипта: вырезать `<script>` и `node --check`.
- Длины реплик для детей проверять скриптом, если есть лимиты.

## Отправка
```bash
git add -A && git -c user.name="Claude" -c user.email="noreply@anthropic.com" commit -m "…"
git fetch -q origin main && git rebase -q origin/main && git push -q origin HEAD:main
```
В конце сообщения коммита — строки соавторства, которые даёт сессия.