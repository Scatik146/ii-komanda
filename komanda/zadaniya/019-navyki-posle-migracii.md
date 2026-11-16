# Задание 019: навыки после миграции — карточки и копии

**Исполнитель:** Claude (Haiku 5.5) · **Проверяет:** Claude (Opus), сливает учитель

## Цель
16.11 папка команды переехала в ii-komanda (`komanda/`, `pravila/`, `prompty/`, `rezerv/navyki/`). Навыки аккаунта Claude и их копии ещё ведут на старые пути. Нужно предложить учителю карточки навыков с новыми путями, а после того как он их сохранит, привести обе копии к навыкам аккаунта.

## Прочитать
- `komanda/VHOD-UROKI.md`
- `komanda/migraciya/proba.md` — только раздел «Навыки — по карточке» (`grep -n` по заголовку, дальше до конца файла). Колонка `memory_maryam_ai` — цели в полной форме, с `ii-komanda/`: берёшь их.
- текущий SKILL.md каждого навыка аккаунта: brifing, drakon-shema, ekonomnaya-sessiya, graficheskij-konspekt, teacher-workpad-sajt, tri-stilya-koda, komnata
- копии: `ii-komanda/rezerv/navyki/<имя>/SKILL.md` и `memory_maryam_ai/navyki/<имя>/SKILL.md` (сейчас обе папки одинаковые)

## Можно менять
- навыки аккаунта — **только через карточки** `propose_skills` (kind: improvement, правки `edits`); файлы навыков на диске — кэш, их не правят
- `ii-komanda/rezerv/navyki/*/SKILL.md`, `memory_maryam_ai/navyki/*/SKILL.md`
- конец этого файла — раздел «Итог»

## Сделать
1. Подключи репозитории ii-komanda и memory_maryam_ai (`add_repo`, access «push»), склонируй.
2. Для каждого навыка из таблицы сравни его текст в аккаунте с таблицей. Ищи **по тексту, а не по номеру строки**: tri-stilya-koda и komnata в аккаунте менялись, номера строк могли сдвинуться.
3. Карточки, не больше 3 навыков на один вызов `propose_skills`: 2 вызова (3 — если нужна карточка komnata, п. 5):
   - каждая правка — `old_string` → `new_string` по колонке `memory_maryam_ai` таблицы;
   - если перед путём стоит имя репозитория («drakon-graf `docs/komanda/README.md`», «teacher-workpad `docs/komanda/navyki/`»), меняй и имя: «ii-komanda `komanda/README.md`»;
   - путь без имени репозитория (brifing: «`docs/komanda/BRIFING.md`») → с именем: «ii-komanda `komanda/BRIFING.md`».
   - Описание (`description`) навыка не меняй.
4. Два места таблица не решает. Делай так:
   - **tri-stilya-koda, строка «Решение учителя 15.11.2026…»:** «журнал drakon-graf `docs/komanda/README.md` § 4» → «журнал ii-komanda `komanda/README.md` § 4»; «Правила целиком — teacher-workpad `docs/komanda/`» → «Правила целиком — ii-komanda `pravila/`»; «`docs/komanda/TRI-STILYA-ODNIM-TEKSTOM.md`» → «ii-komanda `pravila/TRI-STILYA-ODNIM-TEKSTOM.md`».
   - **teacher-workpad-sajt, пункт 3 (три ссылки в одной строке):** «Для помощников ИИ — `docs/komanda/README.md`» → «Для помощников ИИ — ii-komanda `komanda/VHOD-UROKI.md`»; «копии навыков — `docs/komanda/navyki/`» → «копии навыков — ii-komanda `rezerv/navyki/`»; «`Scatik146/drakon-graf`, `docs/komanda/README.md`» → «`Scatik146/ii-komanda`, `komanda/README.md`».
5. **komnata** в таблице нет, путей `docs/komanda` в ней нет. Карточка нужна, только если в навыке аккаунта старый путь всё же найдётся (`grep -n 'docs/komanda'`).
6. Учителю — одно сообщение: какие карточки показаны, что в каждой меняется (одной строкой на навык). Дальше **жди его «сохранил»**.
7. После «сохранил» перечитай SKILL.md каждого навыка аккаунта (теперь уже новый) и запиши его текст целиком в обе копии: `rezerv/navyki/<имя>/SKILL.md` и `memory_maryam_ai/navyki/<имя>/SKILL.md`. Так обновятся и tri-stilya-koda с komnata: их копии отстали от аккаунта.
8. Коммит в каждом из двух репозиториев: по-русски, `git add` только этих SKILL.md (не `git add -A`), с трейлерами из системного напоминания, потом push.

## Как писать
- Тексты и коммиты — по-русски. Кода в задании нет.
- В новых файлах команды старый путь не писать даже в комментарии: так 16.11 шапка `migraciya.bat` дала «руками 1».

## Нельзя
- Править файлы навыков на диске вместо карточек; трогать `max-class-bot`; менять что-либо в `komanda/`, `pravila/`, `prompty/` (это задание только про навыки); `git add -A`.

## Готово, когда
- `grep -rn 'docs/komanda' rezerv/navyki` (в ii-komanda) и `grep -rn 'docs/komanda' navyki` (в memory_maryam_ai) — пусто
- `diff -r ii-komanda/rezerv/navyki memory_maryam_ai/navyki` — пусто
- каждая копия совпадает с навыком аккаунта (сравни текст после «сохранил»)
- в ответе: вывод обеих команд целиком; список «навык — что изменено»; коммиты двух репозиториев; что в задании было непонятно или читалось двояко
- в разделе «Итог» этого файла — то же коротко, с датой

## Итог

16.11.2026. Карточки навыков показаны и сохранены учителем (шесть навыков; komnata — без карточки, старых путей нет). Копии в `rezerv/navyki` и `memory_maryam_ai/navyki` приведены к тексту навыков аккаунта: `grep docs/komanda` пусто, `diff -r` пусто. Ветка `navyki-posle-migracii` запушена в ii-komanda и memory_maryam_ai, PR не открыт. Открыто: `komanda/VHOD-UROKI.md` устарел (журнал и путь к drakon-graf); в ekonomnaya-sessiya остался `teacher-workpad/CLAUDE.md` (в таблице его не было).
