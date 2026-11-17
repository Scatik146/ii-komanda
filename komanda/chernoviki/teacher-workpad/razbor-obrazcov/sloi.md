# «Слои» трёх ответов, имена приведены к кандидатам 9077–9141 (17.11, шаг 5)

G — GLM, DA — DeepSeek, приложение, DP — DeepSeek, презентация. ≈ — слова нет в словаре, учитель отнёс его к другому кандидату (§ 4 `sravnenie.md`).

## Сошлось (8 слоёв GLM — у каждого есть пара у DeepSeek)

| № | слой | GLM | DeepSeek | общее |
|---|---|---|---|---|
| 1 | испытание в игре | G испытание-в-игре = predict-before-each-run 9080 → three-step-hint-ladder 9081 → qmark-raises-next-step 9110 → rollback-after-three-fails 9082 → bitrates-and-medals-in-header 9086 | DA экран-испытания = bitrates-and-medals-in-header 9086 → screen-dots 9119 → helper-panel 9118 → predict-before-each-run 9080 → previous-attempt-diff 9120 → rollback-after-three-fails 9082 | 9080, 9082, 9086 |
| 2 | экран тетради | G экран-тетради = own-answer-then-template-in-notebook 9089 → one-tekst-file-for-app-and-teacher 9077 → canvas-page-from-same-tekst 9090 → a4-insert-sheet-cut-dashed 9091 | DA тетрадный-блок = own-answer-then-template-in-notebook 9089 → scheme-legend 9125 → two-notes-compare 9126 → a4-insert-sheet-cut-dashed 9091 | 9089, 9091 |
| 3 | сборка из одного источника | G сборка-из-одного-источника = one-tekst-file-for-app-and-teacher 9077 → canvas-page-from-same-tekst 9090 → a4-insert-sheet-cut-dashed 9091 → selfcheck-table-in-canvas 9112 | DA учительский-слой = one-tekst-file-for-app-and-teacher 9077 → canvas-page-from-same-tekst 9090 → teacher-menu-ctrl-alt-m 9084 (×2) → print-a4 9124 | 9077, 9090 |
| 4 | сюжет и роли | G игровая-связка-сюжет-и-роли = night-shift-role-story 9079 → pilot-and-navigator-roles-swap 9085 → pager-specialist-for-bitrates 9088 → clock-branches-rush-late-bonus 9087 | DA урок-эхо-узел = night-shift-role-story 9079 → pair-names 9116 → screen-list-with-minute-ranges 9078 → clock-branches-rush-late-bonus 9087 (×4); DA пара-в-уроке = pilot-and-navigator-roles-swap 9085 (×2) → pair-names 9116 → personal-conclusion 9128 | 9079, 9085, 9087 |
| 5 | урок без учителя | G урок-без-учителя-предметника = teacher-silent-rule-slide 9092 → red-green-card-signal 9093 → hint-cards-P1-P8-by-red-card 9101 → teacher-notes-on-N-key 9094 | DP этап-стенд = teacher-silent-rule-slide 9092 → red-green-card-signal 9093 → hint-cards-P1-P8-by-red-card 9101 → challenge-card-for-fast-pairs 9102 | 9092, 9093, 9101 |
| 6 | открытие нового | G слайд-открытия-нового = predict-stage-0-before-laptops 9096 → catch-the-model-cheating 9098 → own-words-then-envelope-with-terms 9097 → main-idea-one-sentence-at-end 9099 | DP экран-гипотеза = predict-stage-0-before-laptops 9096 → pair-worksheet 9135 → stage-and-minute-shown-on-slide 9095; DP экран-секретный-тест = catch-the-model-cheating 9098 → red-green-card-signal 9093 → hint-cards-P1-P8-by-red-card 9101; DP экран-конверт = own-words-then-envelope-with-terms 9097 (×2) → expected-answers 9139 | 9096, 9098, 9097 |
| 7 | урок по таймингу | G весь-урок-по-таймингу = screen-list-with-minute-ranges 9078 → stage-and-minute-shown-on-slide 9095 → what-to-drop-if-behind 9114 → risks-table-each-unverified-has-fallback 9105 | DP урок = teacher-timing-table 9136 → stage-and-minute-shown-on-slide 9095 → teacher-notes-on-N-key 9094 → time-reserve 9140 | 9095 (+ близкие 9114 ≈ 9140) |
| 8 | презентация про ИИ / оформление | G презентация-про-ИИ = four-ai-skills-frame 9106 → svg-illustration-per-idea 9107 → hands-on-activity-with-handout 9108 → where-ai-fails-real-cases 9109 → numbers-and-why-support 9115 | DP оформление-урока = svg-illustration-per-idea 9107 (×2: svg-illustration, short-headings) → ≈ four-ai-skills-frame 9106 (example-cards) | 9107, 9106 |

## Только у DeepSeek (7)

| слой | состав |
|---|---|
| DA этап-разбор-машины | screen-list-with-minute-ranges 9078 → guided-pult-training 9117 → three-step-hint-ladder 9081 → predict-before-each-run 9080 |
| DA этап-голос-машины | prewritten-parts-note 9133 → three-step-hint-ladder 9081 → machine-mood 9132 → predict-before-each-run 9080 |
| DA этап-финал | final-table-to-scheme 9127 → personal-conclusion 9128 → endings-by-score 9129 |
| DP экран-масштаб | dossier-verbatim-source-and-translation 9100 → complexity-ladder 9134 → ≈ svg-illustration-per-idea 9107 (bar-chart) |
| DP экран-смета | budget-order-card-and-verdict 9103 → pair-worksheet 9135 → expected-answers 9139 |
| DP этап-рефлексия | exit-ticket-each-silent 9104 → main-idea-one-sentence-at-end 9099 → ≈ 9099 / 9115 (user-rule-slide) |
| DP подготовка-урока | print-checklist 9137 → setup-checklist 9138 → risks-table-each-unverified-has-fallback 9105 |

## Только у GLM — нет. Противоречий по содержанию — нет
Разница — в зернистости: GLM режет урок по смыслу (8 слоёв), DeepSeek — по экранам и этапам (18 слоёв); слой 6 у DeepSeek разбит на три экрана.

## Решено учителем раньше (§ 4)
игра-ведёт-без-учителя = helper-panel 9118 → three-step-hint-ladder 9081 → clock-branches-rush-late-bonus 9087 → pager-specialist-for-bitrates 9088 — ни в одном ответе как слой не записан.
