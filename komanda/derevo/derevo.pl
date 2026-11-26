% Дерево задач — факты (шаг 1, 26.11; источник — shag-0.md, сверен учителем 26.11).
% Схема (по-графовски: факт — подписанная связь):
%   узел(Ид, Родитель, Статус)    — связь Ид -> Родитель: «родитель»; корень — атом корень
%   название(Ид, Текст)           — как называем
%   остановились(Ид, Текст)       — один на узел: дата и что
%   не_закрыто(Ид, Текст)         — ноль или несколько на узел
%   источник(Ид, github(Путь) | sourcecraft(Путь)) — только у репозиториев
%   пометка(Ид, Текст)            — принципы, не узлы
% Проверки — proverka.pl.

:- encoding(utf8).
:- discontiguous узел/3, название/2, остановились/2, не_закрыто/2, источник/2, пометка/2.

статус(работает_у_нас).
статус(в_работе).
статус(заморожено).
статус(идея).
статус(завершено).

% ---------- 1. ii-komanda ----------
узел(ii_komanda, корень, работает_у_нас).
название(ii_komanda, 'ii-komanda — команда ИИ учителя').
источник(ii_komanda, github('Scatik146/ii-komanda')).
остановились(ii_komanda, '26.11: дерево задач, шаг 1').
не_закрыто(ii_komanda, 'README § 5: около 15 открытых вопросов').
не_закрыто(ii_komanda, 'ветки не убраны: forto-prolog(-2,-3), ekspertiza-forto-prolog, komnata-tri-stilya, migraciya-proverki, pravki-043, resheniya-14-11').
пометка(ii_komanda, 'Принцип команды: на каждом этапе — ИИ из трёх стран (США, Россия, Китай), если возможно: гибкость, выживаемость, три взгляда на мир.').

узел(ii_py, ii_komanda, заморожено).
название(ii_py, 'ii.py — конвейер урока').
остановились(ii_py, '18.11: пауза; версия 0.1, 19 тестов').
не_закрыто(ii_py, 'klyuchi на ноутбуке').
не_закрыто(ii_py, 'команды sborka, vernut, vydacha').

узел(scatikwork, ii_komanda, работает_у_нас).
название(scatikwork, 'Сервер SCATIKWORK').
остановились(scatikwork, 'зеркала репозиториев в 03:00').
не_закрыто(scatikwork, 'стать домом дерева задач').

узел(slovar_forto_prologa, ii_komanda, в_работе).
название(slovar_forto_prologa, 'Словарь Форто-Пролога (slovar/, lib/slova)').
остановились(slovar_forto_prologa, 'задача 025').
не_закрыто(slovar_forto_prologa, 'slovar-iz-koda.py не читает код в HTML').

узел(yadro_trit, ii_komanda, в_работе).
название(yadro_trit, 'Ядро трит').
остановились(yadro_trit, '44/44 эталона').
не_закрыто(yadro_trit, 'этапы после ревизора').

узел(revizor, yadro_trit, работает_у_нас).
название(revizor, 'Ревизор навыков и памяти').
остановились(revizor, '25.11: отчёт').
не_закрыто(revizor, 'карточку ОЧ не трогать до ≈ 23.12').

узел(kniga_logika, ii_komanda, в_работе).
название(kniga_logika, 'Логика (книга, ч. 2)').
остановились(kniga_logika, 'вычитка').
не_закрыто(kniga_logika, 'Д.1 примеры').
не_закрыто(kniga_logika, 'сверка названий с Поляковым').

узел(komnata, ii_komanda, работает_у_нас).
название(komnata, 'Комната переговоров').
остановились(komnata, 'работает').

узел(brifing, ii_komanda, работает_у_нас).
название(brifing, 'Брифинг').
остановились(brifing, 'работает').

узел(algoritm_urokov_v9, ii_komanda, работает_у_нас).
название(algoritm_urokov_v9, 'Алгоритм уроков v9').
остановились(algoritm_urokov_v9, 'работает').

узел(derevo_zadach, ii_komanda, в_работе).
название(derevo_zadach, 'Дерево задач').
остановились(derevo_zadach, '26.11: шаг 1 — факты Пролога').
не_закрыто(derevo_zadach, 'Python -> JSON').
не_закрыто(derevo_zadach, 'страница JS').

узел(avtomatizaciya_dz, ii_komanda, идея).
название(avtomatizaciya_dz, 'Автоматизация ДЗ').
остановились(avtomatizaciya_dz, 'ждёт схему (задание 003)').

% ---------- 2. teacher-workpad ----------
узел(teacher_workpad, корень, работает_у_нас).
название(teacher_workpad, 'teacher-workpad — сайт уроков').
источник(teacher_workpad, github('Scatik146/teacher-workpad')).
остановились(teacher_workpad, '25.11: урок 13 ИИИБ 6 кл.').
не_закрыто(teacher_workpad, '11 веток кроме main (урок 11 от 22.11, deepseek/proposed-change, zadanie-005-priemka)').
не_закрыто(teacher_workpad, 'хвосты 16.11: фото слайдов, «Дело № 6-ИИ», программа 10 кл.').
не_закрыто(teacher_workpad, 'MathJax офлайн').

узел(kurs_ii_ib, teacher_workpad, в_работе).
название(kurs_ii_ib, 'Курс «ИИ и ИБ» (1–11 кл.)').
остановились(kurs_ii_ib, '26.11: урок 13 6 кл. проведён').
не_закрыто(kurs_ii_ib, 'разбор уроков 23–26.11').

узел(drakon_shemy, teacher_workpad, работает_у_нас).
название(drakon_shemy, 'Дракон-схемы на сайте (обёртка 1.4, запись 1.2)').
остановились(drakon_shemy, 'работает').
не_закрыто(drakon_shemy, 'ограды «дракон» (README § 5 п. 6)').

% ---------- 3. drakon-graf ----------
узел(drakon_graf, корень, работает_у_нас).
название(drakon_graf, 'ДРАКОН-ГРАФ').
источник(drakon_graf, github('Scatik146/drakon-graf')).
остановились(drakon_graf, '23.11: стартовая страница').
не_закрыто(drakon_graf, 'ветки startovaya-stranica, deps-fetch, stage3, sostoyanie-14-11-vecher').
не_закрыто(drakon_graf, 'ГРАФ как мини-проект: учебник, сайт, база примеров').

узел(zhivoj_konspekt, drakon_graf, в_работе).
название(zhivoj_konspekt, 'Живой конспект (родился из drakon-graf 14.11; пока только документы)').
источник(zhivoj_konspekt, github('Scatik146/zhivoj-konspekt')).
остановились(zhivoj_konspekt, 'пункт «а» готов').
не_закрыто(zhivoj_konspekt, '«б» ipaddress (DeepSeek)').
не_закрыто(zhivoj_konspekt, '«в» проверка на ЕГЭ').

узел(skulpt, zhivoj_konspekt, в_работе).
название(skulpt, 'skulpt (форк)').
источник(skulpt, github('Scatik146/skulpt')).
остановились(skulpt, '14.11: ветка zhivoj-konspekt, printLastExpr').

узел(qumir, zhivoj_konspekt, заморожено).
название(qumir, 'qumir (форк, страховка)').
источник(qumir, github('Scatik146/qumir')).
остановились(qumir, '13.11: последнее — апстрим').
не_закрыто(qumir, 'импорт .fil').

% ---------- 4–8. остальные репозитории ----------
узел(komi_perm_game_calendar, корень, работает_у_нас).
название(komi_perm_game_calendar, 'Коми-пермяцкий игровой календарь').
источник(komi_perm_game_calendar, github('Scatik146/komi-perm-game-calendar')).
остановились(komi_perm_game_calendar, '22.11: PR #29; 25.11: CLAUDE.md').
не_закрыто(komi_perm_game_calendar, 'шаг 5 РПЦ').
не_закрыто(komi_perm_game_calendar, 'методика зманим (README § 5)').
не_закрыто(komi_perm_game_calendar, '31 ветка').

узел(memory_maryam_ai, корень, работает_у_нас).
название(memory_maryam_ai, 'memory_maryam_ai — резерв ii-komanda').
источник(memory_maryam_ai, github('Scatik146/memory_maryam_ai')).
остановились(memory_maryam_ai, '25.11').
не_закрыто(memory_maryam_ai, 'ветка navyki-posle-migracii').

узел(info10_class, корень, заморожено).
название(info10_class, 'info10-class — информатика 10 кл.: учить работать с GitHub (накрыт курсом ИИ 1–11 кл.)').
источник(info10_class, github('Scatik146/info10-class')).
остановились(info10_class, '16.10: уроки проведены').
не_закрыто(info10_class, 'задача #13 «Код Хаффмана»').
не_закрыто(info10_class, 'ветки учеников').

узел(max_class_bot, корень, работает_у_нас).
название(max_class_bot, 'max-class-bot — чат-бот классного руководителя в MAX (очень важен)').
источник(max_class_bot, sourcecraft('max-class-bot')).   % точный адрес на sourcecraft.dev — уточнить
источник(max_class_bot, github('Scatik146/max-class-bot')).   % пуст
остановились(max_class_bot, '26.11: бот запущен, но только шаблон; стоит').
не_закрыто(max_class_bot, 'учитель не может за него взяться').
не_закрыто(max_class_bot, 'код на sourcecraft.dev и в Yandex Cloud, на GitHub пусто').

узел(drawman, корень, заморожено).
название(drawman, 'drawman — «Чертежник на Пайтоне»').
источник(drawman, github('Scatik146/drawman')).
остановились(drawman, '2017').
