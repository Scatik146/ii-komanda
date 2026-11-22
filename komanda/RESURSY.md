# Наши ресурсы — что есть в репозиториях Scatik146 и что брать в уроки

Составлено 23.11.2026 (Claude, проход по всем 11 репозиториям). Читает тот, кто делает экспертизу и собирает артефакты урока (Claude или кто вместо него). Алиса файлы не читает — она переносит раздел 9 шапки урока (форма teacher-workpad `instrumenty/shapka-uroka/`) в «Итог для Claude».

Как пользоваться: в шапке урока отмечены ресурсы → по этому списку найти файлы → прочитать нужное (кусками, через grep) → взять в урок. Новый ресурс — строкой сюда и галочкой в `teacher-workpad/instrumenty/shapka-uroka/dannye.js`, раздел 9.

## Для урока: что брать

| Ресурс | Что даёт уроку | Где лежит | Как подключать |
|---|---|---|---|
| Конспект ДРАКОН-ГРАФ | главные мысли урока для тетради: понятия, правила, сравнения, разбор формул | teacher-workpad `lib/drakon-graf/`; язык — drakon-graf `docs/graf/шпаргалка_ученика.md`, `справочник_учителя.md`; генератор с печатью — https://scatik146.github.io/drakon-graf/generator/; для нейросетей — https://scatik146.github.io/drakon-graf/llms.txt | навык `graficheskij-konspekt`; teacher-workpad `CLAUDE.md`, раздел ДРАКОН-ГРАФ |
| Дракон-схемы | алгоритм, порядок действий, «что делать, если…»; ученик собирает схему сам; код по схеме (Python, КуМир в стиле ОГЭ, C, 1С) | teacher-workpad `lib/drakon-shema/`, `lib/drakonwidget/`, `lib/drakongen/`; текстовая запись — drakon-graf `docs/drakon/текстовая_запись.md` | навык `drakon-shema`; проверка `tools/drakon-shema.mjs` |
| ДРАКОН-лист | код + схема + данные + тест одной страницей; лист в тетрадь | образец — ii-komanda `pravila/primery/drakon-list-evklid.md`; уроки: teacher-workpad `1-klass/iiib-11-cvet/drakon-list.md` | навык `tri-stilya-koda`; проверка `tools/drakon-list.mjs` |
| Двоичная логика (бит) | бит, законы, Жегалкин, схемы, базисы; примеры и проверки на Python, Prolog, Forth | ii-komanda `logika/kniga/chast-1-bit/` (A–P), `logika/dvoichnaya.md`, `logika/istoriya-binarnosti.md`, `logika/dvoich.*`, `primery-dvoich.json` | читать главы по букве (A — основа) |
| Троичная логика (трит) | трит, законы, время, действия, правила, следование; «неизвестное — не да и не нет» | ii-komanda `logika/kniga/chast-2-trit/`, `logika/svod.md`, `logika/och-*`; Брусенцов (Сетунь) — `forto-prolog/brusentsov.md`, `brusentsov-tablicy.md` | читать главы по букве; сводка — `svod.md` |
| Словарь проверенных фактов | факты с истинностью по мирам (реальность, книга, учебный урок); кандидаты 9000–9999 | ii-komanda `slovar/` (README) | брать только атомы со значением 1; кандидатов — не детям |
| Форт и Пролог в браузере | стенды для уроков программирования и логики | drakon-graf `site/experiments/forth/`, `site/experiments/prolog/` | Prolog детям не преподаётся (решение 15.11) |
| Python в браузере (Skulpt) | запуск Python на странице урока без сервера, вывод последнего выражения как в IDLE | Scatik146/skulpt (форк), ветка `zhivoj-konspekt`; сборка — артефакт CI `skulpt-dist` | для «Живого конспекта»; в уроки — после проверки на ноутбуке |
| КуМир | исполнители (Робот, Чертёжник), задания ОГЭ | Scatik146/qumir (форк, страховка); работа — qumir.dev; разбор — drakon-graf `docs/research/10_КуМир_Qumir.md` | код по дракон-схеме — кнопка «Код» |
| Чертёжник на Python | исполнитель «Чертёжник» для Python | Scatik146/drawman (2017, README «Чертежник на Пайтоне») | не проверялся, сначала посмотреть код |
| Древние письменности | финикийское письмо, анбур (древнепермское), глаголица — шрифты без интернета | teacher-workpad `lib/fonts/` (README); уроки: `7-klass/inf-11-alfavity-i-yazyki/`, `2-klass/iiib-11-sozdat-tekstovyj-dokument/` | `@font-face` по относительному пути |
| Коми-пермяцкий календарь | анбур, коми-пермяцкие слова и имена, части суток, цвета, духи, солнце и луна, расчёты; сайт-часы офлайн | komi-perm-game-calendar `docs/` (anbur, slovar, slova-kalendarya, imena, cveta, sutki, grammatika, istochniki), `data/*.json`, `engine/*.js`; сайт https://scatik146.github.io/komi-perm-game-calendar/ | слова — только проверенные по словарям (Баталова и Кривощёкова-Гантман 1985, Лыткин 1952); новое — согласовать с автором |
| Готовые уроки и механики | что уже есть: игры, пульты, Говорун (голос + текст), «врата», пары «за пультом / штурман», печать A4 | teacher-workpad `RAZRABOTANO.md`, `lessons.js`, папки `*-klass/`; черновые — `plan/` | брать механику и код, не копировать урок целиком |
| Поурочное планирование и программы | место урока в курсе, что до и после | teacher-workpad `plan/*.md` (ИИИБ 1–4, 5–9, 10–11; ИНФ 7–9, 10–11; Труд 5–9; РПЗ 10; прог. 5–7), `rabochie-programmy/` (ИИИБ 1–4) | для полей «место в блоке», «до», «после» |
| Курс информатики 10 класса | задания, теория, решения (Python, GitHub Codespaces) | Scatik146/info10-class (закрытый): `start_lesson/`, `lesson_01/` | закрытый — не публиковать на сайт |
| Меню экранов и шрифты | Ctrl+Alt+M в каждом приложении; Nunito, Pangolin, Caveat, PT Serif/Mono | teacher-workpad `lib/menu-ekranov/`, `lib/fonts/`, `lib/drakon-graf/fonts/` | обязательны по правилам сайта |

## Для команды (не в урок, а для работы над уроком)

| Что | Где |
|---|---|
| Промты Алисы (v7.4-А и -Б), алгоритм уроков v9, исполнитель | ii-komanda `algoritm/` |
| Роли и промты помощников (Алиса, GLM, DeepSeek, Qwen), промт DrakonHub | ii-komanda `prompty/roli/`, `prompty/proekty/`, `prompty/drakonhub-prompt.md` |
| Прежние алгоритмы и шаблоны уроков (сентябрь–октябрь) | ii-komanda `istochniki/uroki/` |
| Три стиля кода, Форто-Пролог | ii-komanda `pravila/`, `forto-prolog/` |
| Проверки | teacher-workpad `tools/` (konspekt, drakon-shema, drakon-list, drakon-kod-test), ii-komanda `tools/` (stil-fort, drakon-list, prolog-zapusk) |
| Разборы ДРАКОНа и ГРАФа: Паронджанов, Гуленков, Венда, Митькин, КуМир, StepInDev, ГРАФ и Prolog | drakon-graf `docs/research/01–12`, `docs/литература.md` |
| ТЗ «Живой конспект» (редактор Markdown с ДРАКОН, ГРАФ, Python, КуМиром) | zhivoj-konspekt (пока только документы) |
| Навык ДРАКОН-ГРАФ для ИИ | drakon-graf `navyk/` |

## Что не ресурс

- Scatik146/memory_maryam_ai (закрытый) — резервная копия навыков и памяти Claude.
- Scatik146/max-class-bot (закрытый) — пустой, файлов нет.
- skulpt и qumir — чужой код (форки); наши изменения — только ветка `zhivoj-konspekt` в skulpt.
