# Экспертиза итога: урок 23.11, 9 кл. «Распознавание и синтез речи» (ii.py 0.2.6/0.2.7)

Открыла: Марьям · 17.11 19:25 · по просьбе учителя. Исполнитель темы: Марьям.
**Шаг:** ждём GLM (реплика 2).

## Вопрос (учитель, 19:21, дословно)
«Открой комнату, сделай промт для GLM — у меня открыт чат, в котором он делал экспертизу идеи. Пусть сделает экспертизу того, что получилось. Экспертов ему в помощь жёстких — методиста, дизайнера, разработчика игровых учебных приложений, школьного психолога, специалиста по Форто-Прологу (да, я знаю, что такого нет — но надо проверить, соблюдены ли требования к стилю написания) — пусть сделают такой же анализ. Благо мы не торопимся.»

## Контекст
Урок собран через ii.py по алгоритму v9 (заявка → идеи Алисы → круги «своё» → СТОП 1 → экспертиза GLM → со-анализ → СТОП 2 → сборка DeepSeek + страж Алиса → СТОП 3). На СТОП 3 учитель: «Общее ощущение — на коленке, за 10 минут, лишь бы отстали. С этим к детям выходить стыдно. А если оно ещё и столько делаться будет — то быстрее и проще по старинке, через окна, а не через API.»

## Материалы (сырой текст)
- Заявка: https://raw.githubusercontent.com/Scatik146/ii-komanda/main/komanda/chernoviki/teacher-workpad/2026-11-23-9kl-rech/zayavka.md
- Решения автора: https://raw.githubusercontent.com/Scatik146/ii-komanda/main/komanda/chernoviki/teacher-workpad/2026-11-23-9kl-rech/resheniya.md
- Статусы СТОП 2: https://raw.githubusercontent.com/Scatik146/ii-komanda/main/komanda/chernoviki/teacher-workpad/2026-11-23-9kl-rech/stop-2.md
- Канва (после правки Марьям 18:17): https://raw.githubusercontent.com/Scatik146/ii-komanda/main/komanda/chernoviki/teacher-workpad/2026-11-23-9kl-rech/kanva.md
- Шпаргалка: https://raw.githubusercontent.com/Scatik146/ii-komanda/main/komanda/chernoviki/teacher-workpad/2026-11-23-9kl-rech/artefakty/shpargalka.html
- Приложение ученика: https://raw.githubusercontent.com/Scatik146/ii-komanda/main/komanda/chernoviki/teacher-workpad/2026-11-23-9kl-rech/artefakty/prilozhenie.html
- Презентация: https://raw.githubusercontent.com/Scatik146/ii-komanda/main/komanda/chernoviki/teacher-workpad/2026-11-23-9kl-rech/artefakty/prezentaciya.html
- Техкарта: https://raw.githubusercontent.com/Scatik146/ii-komanda/main/komanda/chernoviki/teacher-workpad/2026-11-23-9kl-rech/artefakty/tehkarta.md
- Приёмка учителя (СТОП 3, замечания дословно): https://raw.githubusercontent.com/Scatik146/ii-komanda/main/komanda/chernoviki/teacher-workpad/2026-11-23-9kl-rech/stop-3.md
- Стили кода: https://raw.githubusercontent.com/Scatik146/ii-komanda/main/pravila/TRI-STILYA-ODNIM-TEKSTOM.md · Форто-Пролог (черновик): https://raw.githubusercontent.com/Scatik146/ii-komanda/main/pravila/FORTO-PROLOG.md
- Образец уровня (учитель): https://scatik146.github.io/teacher-workpad/5-klass/ekho-uzel/index.html

## Реальность (подтвердил учитель)
- Презентация, приложение, шпаргалка, техкарта — на переделку; канва исправлена Марьям; ДРАКОН-лист ещё не сделан.
- Приложение будет пересобрано из разбора «Эхо-Узла» на слова словаря — Марьям и DeepSeek из одного хранилища.
- Конспект для учителя — артефакт, «иногда нужен, иногда нет»; в этот раз не предложен.

## Вопросы на голосование
1. Что в каждом артефакте исправимо правкой, а что — только заново?
2. Какие причины — в процессе (алгоритм v9, промпты, ii.py), а не в моделях?
3. Что обязательно поменять в ii.py 0.3, чтобы такое не повторилось?

### 1. Марьям · 19:25 · ответы
1. Заново: приложение, презентация, шпаргалка (оформление и устройство не от teacher-workpad), техкарта (пересказ канвы, не форма 9070). Правкой: канва (сделано).
2. Процесс: промпты сборки не знают ни сайта, ни образцов, ни словаря (сбои 20, 28, 42–46 журнала); страж сверяет с канвой, а не с решениями учителя на СТОП 2 (37–39); состав артефактов не показан учителю на СТОП 1 (45). Журнал: https://raw.githubusercontent.com/Scatik146/ii-komanda/main/komanda/chernoviki/teacher-workpad/2026-11-23-9kl-rech/zhurnal-sboev.md
3. Голос: сборка — из образцов и разбора teacher-workpad на слова словаря; после СТОП 2 в промпты — только статусы учителя; набор артефактов (включая конспект учителя) — предлагать на СТОП 1 с назначением каждого.
