# Резервная копия Claude: навыки, память, где лежит работа

Снято 13.11.2026, 21:30 (МСК), чат «Перенос уроков». Обновлять при изменении навыков или памяти (раз в неделю — на брифинге в пятницу).

**Внимание: репозиторий открытый** (решение учителя 13.11) — сюда не класть пароли, ключи API, данные учеников.

## Что здесь

| папка | что | откуда |
|---|---|---|
| `navyki/<имя>/SKILL.md` | 4 навыка учителя: `ekonomnaya-sessiya`, `teacher-workpad-sajt`, `drakon-shema`, `graficheskij-konspekt` | установленные в claude.ai (13.11); в `ekonomnaya-sessiya` исправлен путь к заданиям (`teacher-workpad/docs/komanda/zadaniya/`) |
| `pamyat/obshchaya/` | общая память Claude (вне проектов): профиль, предпочтения, teacher-workpad | память claude.ai, дословно |
| `pamyat/proekt-razrabotka-urokov/` | память проекта «Разработка уроков»: профиль, правила приложений, репозитории drakon-graf, ii-komanda, info10-class | память claude.ai, дословно |
| `pamyat/proekt-zhivoj-konspekt/` | память проекта «Живой конспект»: предпочтения, drakon-graf, ii-komanda, teacher-workpad (профиля у проекта нет) | память claude.ai, дословно (13.11) |

Остальные навыки (docx, pdf, pptx, xlsx, браузер и т. п.) — встроенные Anthropic, их копировать не нужно.

Не вошло (Claude из этого чата не видит): память **других проектов** claude.ai и сами **переписки**. Их сохранить может только учитель: в настройках claude.ai — экспорт данных (Export data; архив приходит на почту).

## Где «рабочая голова» команды (это и есть главное — всё уже в GitHub)

- Состояние и план дня: `drakon-graf/docs/komanda/SOSTOYANIE.md`, `BRIFING.md`, журнал решений — `README.md` (разделы 4–5).
- Правила сайта уроков: `teacher-workpad/CLAUDE.md`; копии навыков: `teacher-workpad/docs/komanda/navyki/`; задания помощникам: `teacher-workpad/docs/komanda/zadaniya/`.
- Списки «Разработано» и «Доработки»: `teacher-workpad/RAZRABOTANO.md`, `DORABOTKI.md` (их копии — документы проекта «Разработка уроков»).
- Перенос уроков (шаги 1–7): `teacher-workpad/chernoviki/OPIS.md`.
- Алгоритмы уроков и план автоматизации: этот репозиторий (`istochniki/uroki/`, `AVTOMATIZACIYA.md`).

## Как поднять всё заново

1. **Навыки.** в настройках claude.ai, раздел навыков (Skills), — загрузить: для каждого навыка папку `navyki/<имя>/` запаковать в zip (внутри — `SKILL.md`). Или в чате: «создай навык из этого файла» и приложить `SKILL.md`.
2. **Проект.** Создать проект «Разработка уроков» (описание: «Информатика, Искусственный интеллект, Информационная безопасность, Труд(технология)»), добавить в него документы из `teacher-workpad/RAZRABOTANO.md` и `DORABOTKI.md` под именами `Разработано teacher-workpad.md`, `Доработки teacher-workpad.md`.
3. **Память.** В чате проекта: «Вот моя память, запиши её» и приложить файлы `pamyat/proekt-razrabotka-urokov/*`; в обычном чате (вне проекта) — так же с `pamyat/obshchaya/*`. Есть встроенный навык `import-memory` — он разложит по местам.
4. **Первый чат.** «Брифинг»: Claude читает `drakon-graf/docs/komanda/SOSTOYANIE.md` и `BRIFING.md` — и работа продолжается с того же места.
5. **Без Claude.** Порядок для других помощников — `drakon-graf/docs/komanda/BEZ_CLAUDE.md`.
