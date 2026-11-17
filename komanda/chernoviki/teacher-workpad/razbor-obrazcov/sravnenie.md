# Сравнение ответов DeepSeek и GLM (17.11, шаг 2)

Цитаты (`analiz.py citaty`, teacher-workpad@6b7c339): 118 из 119 на месте. Не прошла DS-през С-03 («Учитель сегодня молчит. Вы — нет.» — в файле разорвана `<span>`); приём сохранён через GLM П-01.
Поля приведены к заданию: словарь «игровая», «игровая деталь» → «игра»; тип → «сборка». Файлы ответов не менялись.
Обозначения: G — glm.md, DA — deepseek-prilozhenie.md, DP — deepseek-prezentaciya.md.

## 1. Сошлось (33)

### Приложение «Эхо-Узел» (15)
| слово (имя GLM) | G | DS | словарь |
|---|---|---|---|
| one-tekst-file-for-app-and-teacher | С-01 | DA С-24 | данные |
| screen-list-with-minute-ranges | С-02 | DA С-01 | методика |
| night-shift-role-story | С-03 | DA С-02 | **игра / методика** |
| predict-before-each-run | С-04 | DA С-07 + С-08 | методика |
| three-step-hint-ladder | С-05 | DA С-06 | методика |
| rollback-after-three-fails | С-07 | DA С-18 | методика |
| localstorage-with-version-key | С-08 | DA С-34 | служебное |
| teacher-menu-ctrl-alt-m | С-09 | DA С-35 + С-36 | служебное |
| pilot-and-navigator-roles-swap | С-11 | DA С-10 + С-11 | игра |
| bitrates-and-medals-in-header | С-12 | DA С-12 | игра |
| clock-branches-rush-late-bonus | С-13 | DA С-14…С-17 | методика (С-17 у DS — игра) |
| pager-specialist-for-bitrates | С-14 | DA С-20 | игра |
| own-answer-then-template-in-notebook | С-15 | DA С-28 | **методика / оформление** |
| canvas-page-from-same-tekst | С-16 | DA С-25 | данные / методика |
| a4-insert-sheet-cut-dashed | С-17 | DA С-27 | **служебное / оформление** |

### Презентации (18)
| слово (имя GLM) | G | DS | словарь |
|---|---|---|---|
| teacher-silent-rule-slide | П-01 | DP С-03 (цитата не прошла) | методика |
| red-green-card-signal | П-02 | DP С-04 | **методика / игра** |
| teacher-notes-on-N-key | П-03 | DP С-02 + С-25 | служебное |
| stage-and-minute-shown-on-slide | П-04 | DP С-01 | методика |
| predict-stage-0-before-laptops | П-05 | DP С-05 | методика |
| own-words-then-envelope-with-terms | П-06 | DP С-07 + С-08 | методика |
| catch-the-model-cheating | П-07 | DP С-06 | методика |
| main-idea-one-sentence-at-end | П-08 | DP С-13 | методика |
| dossier-verbatim-source-and-translation | П-10 | DP С-09 | данные |
| hint-cards-P1-P8-by-red-card | П-11 | DP С-17 | методика |
| challenge-card-for-fast-pairs | П-12 | DP С-16 | **методика / игра** |
| budget-order-card-and-verdict | П-13 | DP С-11 | **методика / игра** |
| exit-ticket-each-silent | П-14 | DP С-12 | методика |
| risks-table-each-unverified-has-fallback | П-16 | DP С-21 + С-23 | методика |
| four-ai-skills-frame | П-17 | DP С-33 | методика |
| svg-illustration-per-idea | П-18 | DP С-26 + С-27 | оформление |
| hands-on-activity-with-handout | П-19 | DP С-28 + С-36 + С-37 | **методика / игра** |
| where-ai-fails-real-cases | П-20 | DP С-29 | методика |

## 2. Противоречия (только словарь, по содержанию противоречий нет)
Выделены жирным выше: сюжет, конспект-в-тетрадь, лист-вклейка, красная/зелёная карточка, челлендж, заказчик-смета, активности с раздаткой (7). Плюс зернистость: DS дробит одно слово на 2–4 (прогноз, часы смены, роли, конверт).

## 3. Только у одного

### Только GLM (6)
- С-06 qmark-raises-next-step — «?» поднимает подсказку на ступень в любой момент
- С-10 new-shift-button — «Новая смена» стирает прогресс пары
- С-18 selfcheck-table-in-canvas — таблица самопроверки урока в канве
- П-09 three-files-slides-handout-memo — комплект: слайды + раздатка + памятка (близко к DP С-14)
- П-15 what-to-drop-if-behind — что выбрасывать при отставании (близко к DP С-24 «резерв времени»)
- П-21 numbers-and-why-support — вывод опирается на цифры (близко к DP С-40 «правило: проверяй»)

### Только DeepSeek — приложение (19)
С-03 pair-names · С-04 guided-pult-training · С-05 helper-panel · С-09 game-leads-methodology · С-13 screen-dots · С-19 previous-attempt-diff · С-21 typing-simulation · С-22 mini-task-while-typing · С-23 specialist-persona · С-26 print-a4 · С-29 scheme-legend · С-30 two-notes-compare · С-31 final-table-to-scheme · С-32 personal-conclusion · С-33 endings-by-score · С-37 voice-fallback · С-38 voice-toggle · С-39 machine-mood · С-40 prewritten-parts-note

### Только DeepSeek — презентации (16)
С-10 complexity-ladder · С-14 printable-handout · С-15 pair-worksheet · С-18 teacher-timing-table · С-19 print-checklist · С-20 setup-checklist · С-22 expected-answers · С-24 time-reserve · С-30 support-slide · С-31 personal-projection · С-32 homework-slide · С-34 history-slide · С-35 scheme-slide · С-38 bar-chart · С-39 example-cards · С-40 user-rule-slide

## 4. Решения учителя (шаг 4, 17.11, 22:48–23:03)
- Спорные словари: night-shift-role-story — игра; a4-insert-sheet-cut-dashed — служебное; остальные 5 — методика.
- Внесены из «только у одного» (32), кандидаты 9110–9141:
  - GLM: 9110 qmark-raises-next-step (методика), 9111 new-shift-button (служебное), 9112 selfcheck-table-in-canvas (служебное), 9113 three-files-slides-handout-memo (данные), 9114 what-to-drop-if-behind (методика), 9115 numbers-and-why-support (методика).
  - DeepSeek, приложение: 9116 pair-names (игра; блок режима «пара за одним ноутбуком»), 9117 guided-pult-training, 9118 helper-panel (игра), 9119 screen-dots (игра), 9120 previous-attempt-diff, 9121 typing-simulation (игра), 9122 mini-task-while-typing, 9123 specialist-persona (игра), 9124 print-a4 (служебное), 9125 scheme-legend (оформление), 9126 two-notes-compare, 9127 final-table-to-scheme, 9128 personal-conclusion, 9129 endings-by-score (игра), 9130 voice-fallback (служебное), 9131 voice-toggle (служебное), 9132 machine-mood (игра; учитель — «вносим» вопреки предложению), 9133 prewritten-parts-note; без пометки — методика.
  - DeepSeek, презентации: 9134 complexity-ladder, 9135 pair-worksheet (данные), 9136 teacher-timing-table, 9137 print-checklist (служебное), 9138 setup-checklist (служебное), 9139 expected-answers, 9140 time-reserve, 9141 homework-slide; без пометки — методика.
- Не внесены (9): DA С-09 game-leads-methodology — составное слово для «Слоёв» (= helper-panel → three-step-hint-ladder → clock-branches-rush-late-bonus → pager-specialist-for-bitrates); DP С-14 printable-handout (входит в 9113, 9124); DP С-30 support-slide (повтор 9115); DP С-31 personal-projection; DP С-34 history-slide; DP С-35 scheme-slide, С-38 bar-chart (частные случаи 9107); DP С-39 example-cards (есть в 9106); DP С-40 user-rule-slide (повтор 9099, 9115).
- Итого в словаре: 65 кандидатов 9077–9141 (`slovar/0001-realnost/kandidaty/`), статус «черновик».
- Не сделано: «Слои» и «Чего нет» из трёх ответов не сведены — следующий шаг.
