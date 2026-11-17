Ты — разработчик учебных приложений и методист. Тебе дают образец работы учителя (файлы целиком). Задача — разобрать образец на «слова словаря»: повторяемые приёмы и детали устройства, из которых сборщик потом соберёт НОВЫЙ урок того же уровня (решение учителя 17.11: «модель не знает сайта» — теперь будет знать).

Что считать словом (одно слово — одно действие или одна деталь, её можно перенести в другой урок):
- экран или слайд и его роль в уроке (прогноз до опыта, опыт, «где разошлись», вывод, вторая попытка, итог);
- приём урока открытия нового знания (шкала этапов со временем, «учитель молчит», заметки учителя по клавише, раздатка и памятка рядом, сначала свой ответ — потом образец);
- игровая деталь (сюжет, счёт в шапке, станции, кнопка «Новая пара», роли в паре);
- устройство данных и текстов (один файл текстов урока tekst.js читают приложение, канва, вклейка);
- оформление и иллюстрация (рисунок или схема на каждую мысль, крупные короткие заголовки, шрифты из lib/fonts);
- служебное (быстрый переход Ctrl+Alt+M, сохранение в localStorage с ключом-версией, печать А4).
Стиль кода образца НЕ брать в слова: inline-стили, много return в функции, однобуквенные имена — это недостатки.

Как записать. Каждое слово — отдельный блок, шесть строк, без пустых строк внутри:

```кандидат
номер: С-01
словарь: методика
тип: сборка
запись: <имя-слова латиницей через дефис> — что делает — когда применять (одна строка своими словами)
цитата: <дословный кусок файла, 5–30 слов, скопировать, не набирать и не исправлять>
файл: <путь файла, как в заголовке «ФАЙЛ:» ниже>
```

Правила:
- 25–40 слов. Одно слово — один блок. Повтор того же приёма в другом файле — не новый блок.
- Цитата — строго дословно из указанного файла (её проверит скрипт). Нет цитаты — нет слова.
- Ничего не придумывать сверх файлов. Не уверен — не пиши.
- После блоков — раздел «## Слои»: 5–10 строк вида «верхнее-слово = нижнее-1 → нижнее-2 → нижнее-3» (из каких слов собирается экран, этап урока, весь урок).
- Последний раздел — «## Чего в образце нет, но нужно уроку 9 класса» — не больше 5 строк.

## Образец: презентация «Сначала обучи» (8 класс) с раздаткой и памяткой; иллюстрации — презентация «Компьютерное зрение» (5 класс)

===== ФАЙЛ: 8-klass/snachala-obuchi/slajdy.html =====
<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Слайды — «Сначала обучи, потом объясни»</title>
<style>
  *{box-sizing:border-box}
  html,body{margin:0;height:100%;background:#0E1118;overflow:hidden;font-family:'Segoe UI',Arial,sans-serif}
  #viewport{position:fixed;inset:0;display:flex;align-items:center;justify-content:center}
  #stage{position:relative;width:1920px;height:1080px;transform-origin:center center;flex:none}
  .slide{position:absolute;inset:0;width:1920px;height:1080px;overflow:hidden}
  .slide:not(.active){display:none !important}
  .slide h1,.slide h2,.slide h3,.slide p,.slide ol,.slide ul{margin:0}
  .slide ol,.slide ul{padding-left:1.3em}
  .slide li{padding-left:.2em}
  #hud{position:fixed;right:16px;bottom:12px;color:#8A93A6;font-size:14px;user-select:none;opacity:.7}
  #help{position:fixed;left:16px;bottom:12px;color:#8A93A6;font-size:14px;opacity:.7;transition:opacity .4s}
  #notes{position:fixed;left:0;right:0;bottom:0;background:rgba(14,17,24,.94);color:#E8ECF3;font-size:20px;line-height:1.45;padding:18px 24px 36px;display:none;max-height:40vh;overflow:auto;border-top:2px solid #F2B36B}
  #notes b{color:#F2B36B}
  body.show-notes #notes{display:block}
  @media print{
    @page{size:1920px 1080px;margin:0}
    html,body{overflow:visible;height:auto;background:#fff}
    #viewport{position:static;display:block}
    #stage{transform:none !important;width:auto;height:auto}
    .slide{position:relative;display:flex}
    .slide:not(.active){display:flex !important}
    .slide{break-after:page;page-break-after:always}
    #hud,#help,#notes{display:none !important}
  }
</style>
</head>
<body>
<div id="viewport"><div id="stage">
<section class="slide" id="cover" data-notes="Слайд висит, пока ученики заходят и садятся. Раздатка уже на столах: рабочий лист пары, красная и зелёная карточки, закрытый конверт с терминами. Досье, челлендж и сметы — у учителя до нужного этапа. Держать, пока ученики садятся (около 30 секунд), затем следующий слайд." style="background:#1E2433;color:#F5F1E8;font-family:'Segoe UI', Arial, sans-serif;padding:128px;display:flex;flex-direction:column;justify-content:center;gap:48px">
<p style="font-family:'Segoe UI', Arial, sans-serif;font-size:32px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:#8FB8E3">ИИ и информационная безопасность · 8 класс</p>
<h1 style="font-family:'Segoe UI', Arial, sans-serif;font-size:120px;font-weight:700;line-height:1.05;color:#F5F1E8">Сначала обучи,<br>потом объясни</h1>
<p style="font-size:44px;line-height:1.35;color:#C9D3E3;width:1400px">Сегодня вы научите компьютер отличать акварель от карандашного рисунка. А потом узнаете, чего стоит научить его <b style="color:#F2B36B">рисовать картины</b>.</p>

</section>
<section class="slide" id="rules" data-notes="Около 40 секунд. Проследить, что у каждой пары лежат обе карточки. С этого момента учитель не говорит, только показывает слайды, раздаёт материалы и следит за уровнем шума." style="background:#F5F1E8;color:#1E2433;font-family:'Segoe UI', Arial, sans-serif;padding:128px;display:flex;flex-direction:column;gap:64px">
<h2 style="font-family:'Segoe UI', Arial, sans-serif;font-size:72px;font-weight:700;line-height:1.1">Учитель сегодня молчит. <span style="color:#2F6FB0">Вы — нет.</span></h2>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:32px">
<div style="display:flex;flex-direction:column;gap:12px;background:#FFFDF8;border:1px solid #E4DED1;border-radius:20px;padding:40px">
<h3 style="font-family:'Segoe UI', Arial, sans-serif;font-size:40px;font-weight:600">Работайте в паре</h3>
<p style="font-size:32px;line-height:1.4;color:#3B4252">У каждого свой ноутбук, но модель одна на двоих. Говорить можно — вполголоса.</p>
</div>
<div style="display:flex;flex-direction:column;gap:12px;background:#FFFDF8;border:1px solid #E4DED1;border-left:12px solid #C0392B;border-radius:20px;padding:40px">
<h3 style="font-family:'Segoe UI', Arial, sans-serif;font-size:40px;font-weight:600">Застряли — красная карточка</h3>
<p style="font-size:32px;line-height:1.4;color:#3B4252">Положите её на ноутбук. Учитель молча принесёт подсказку.</p>
</div>
<div style="display:flex;flex-direction:column;gap:12px;background:#FFFDF8;border:1px solid #E4DED1;border-left:12px solid #2E7D4F;border-radius:20px;padding:40px">
<h3 style="font-family:'Segoe UI', Arial, sans-serif;font-size:40px;font-weight:600">Этап готов — зелёная карточка</h3>
<p style="font-size:32px;line-height:1.4;color:#3B4252">Когда зелёные у всех четырёх пар, слайд сменится.</p>
</div>
<div style="display:flex;flex-direction:column;gap:12px;background:#FFFDF8;border:1px solid #E4DED1;border-radius:20px;padding:40px">
<h3 style="font-family:'Segoe UI', Arial, sans-serif;font-size:40px;font-weight:600">Всё остальное — на слайде</h3>
<p style="font-size:32px;line-height:1.4;color:#3B4252">Наверху — какой сейчас этап и до какой минуты он идёт.</p>
</div>
</div>

</section>
<section class="slide" id="bridge" data-notes="Около 30 секунд. Затем слайд «Гипотеза»." style="background:#F5F1E8;color:#1E2433;font-family:'Segoe UI', Arial, sans-serif;padding:128px;display:flex;flex-direction:column;gap:64px">
<h2 style="font-family:'Segoe UI', Arial, sans-serif;font-size:72px;font-weight:700;line-height:1.1">От двойника к ученику</h2>
<div style="display:flex;gap:48px;align-items:stretch">
<div style="flex:1;display:flex;flex-direction:column;gap:16px;background:#E9E4D8;border-radius:20px;padding:48px">
<p style="font-family:'Segoe UI', Arial, sans-serif;font-size:28px;font-weight:600;letter-spacing:3px;text-transform:uppercase;color:#5A5F6B">Прошлый урок</p>
<h3 style="font-family:'Segoe UI', Arial, sans-serif;font-size:44px;font-weight:600;line-height:1.2">Цифровой двойник станка</h3>
<p style="font-size:34px;line-height:1.4;color:#3B4252">Повторяет то, что в него заложили люди: формулы, правила, данные датчиков.</p>
</div>
<div style="flex:1;display:flex;flex-direction:column;gap:16px;background:#1E2433;border-radius:20px;padding:48px">
<p style="font-family:'Segoe UI', Arial, sans-serif;font-size:28px;font-weight:600;letter-spacing:3px;text-transform:uppercase;color:#8FB8E3">Сегодня</p>
<h3 style="font-family:'Segoe UI', Arial, sans-serif;font-size:44px;font-weight:600;line-height:1.2;color:#F5F1E8">Программа без правил</h3>
<p style="font-size:34px;line-height:1.4;color:#C9D3E3">Ей никто не объясняет, чем акварель отличается от карандаша. Она выведет правило сама — из примеров.</p>
</div>
</div>

</section>
<section class="slide" id="s0" data-notes="Около минуты. Когда у всех пар записаны числа — следующий слайд (не позже 2,5 минуты)." style="background:#F5F1E8;color:#1E2433;font-family:'Segoe UI', Arial, sans-serif;padding:128px;display:flex;flex-direction:column;gap:56px">
<div style="display:flex;gap:12px;align-items:center">
<p style="font-size:26px;font-weight:700;padding:8px 22px;border-radius:999px;background:#2F6FB0;color:#F5F1E8">Гипотеза</p>
<p style="font-size:26px;padding:8px 22px;border-radius:999px;background:#E4DED1;color:#4A4F5C">Стенд</p>
<p style="font-size:26px;padding:8px 22px;border-radius:999px;background:#E4DED1;color:#4A4F5C">Под капотом</p>
<p style="font-size:26px;padding:8px 22px;border-radius:999px;background:#E4DED1;color:#4A4F5C">Масштаб</p>
<p style="font-size:26px;padding:8px 22px;border-radius:999px;background:#E4DED1;color:#4A4F5C">Смета</p>
<p style="font-size:26px;padding:8px 22px;border-radius:999px;background:#E4DED1;color:#4A4F5C">Билет</p>
<div style="flex:1"></div>
<p style="font-family:'Segoe UI', Arial, sans-serif;font-size:32px;font-weight:700;color:#2F6FB0">0–2,5 мин</p>
</div>
<h2 style="font-family:'Segoe UI', Arial, sans-serif;font-size:72px;font-weight:700;line-height:1.1">Сначала — прогноз</h2>
<p style="font-size:40px;line-height:1.4;color:#3B4252;width:1400px">Ноутбуки пока не трогаем. Рабочий лист, <b>этап 0</b>: договоритесь в паре и запишите два числа.</p>
<div style="display:flex;gap:32px">
<div style="flex:1;background:#FFFDF8;border:1px solid #E4DED1;border-radius:20px;padding:40px">
<p style="font-size:36px;line-height:1.4">За сколько <b>секунд</b> компьютер научится отличать акварель от карандаша?</p>
</div>
<div style="flex:1;background:#FFFDF8;border:1px solid #E4DED1;border-radius:20px;padding:40px">
<p style="font-size:36px;line-height:1.4">Сколько из <b>6 секретных картинок</b> он потом угадает?</p>
</div>
</div>

</section>
<section class="slide" id="s1" data-notes="Teachable Machine уже открыта на всех ноутбуках (Image Project), ярлык «Стенд» — на рабочем столе. Если пара всё же ищет папку — подсказка П2. Если пара долго ищет кнопку — П5 или просто показать пальцем на экран. Как только у пары модель обучена, она переходит к тесту — следующий слайд включить, когда обучили хотя бы две пары (ориентир — 8-я минута)." style="background:#F5F1E8;color:#1E2433;font-family:'Segoe UI', Arial, sans-serif;padding:128px;display:flex;flex-direction:column;gap:48px">
<div style="display:flex;gap:12px;align-items:center">
<p style="font-size:26px;padding:8px 22px;border-radius:999px;background:#E4DED1;color:#4A4F5C">Гипотеза</p>
<p style="font-size:26px;font-weight:700;padding:8px 22px;border-radius:999px;background:#2F6FB0;color:#F5F1E8">Стенд</p>
<p style="font-size:26px;padding:8px 22px;border-radius:999px;background:#E4DED1;color:#4A4F5C">Под капотом</p>
<p style="font-size:26px;padding:8px 22px;border-radius:999px;background:#E4DED1;color:#4A4F5C">Масштаб</p>
<p style="font-size:26px;padding:8px 22px;border-radius:999px;background:#E4DED1;color:#4A4F5C">Смета</p>
<p style="font-size:26px;padding:8px 22px;border-radius:999px;background:#E4DED1;color:#4A4F5C">Билет</p>
<div style="flex:1"></div>
<p style="font-family:'Segoe UI', Arial, sans-serif;font-size:32px;font-weight:700;color:#2F6FB0">2,5–12 мин</p>
</div>
<h2 style="font-family:'Segoe UI', Arial, sans-serif;font-size:72px;font-weight:700;line-height:1.1">Обучите модель</h2>
<div style="display:flex;gap:16px;align-items:center;flex-wrap:wrap">
<p style="font-family:'Segoe UI', Arial, sans-serif;font-size:30px;font-weight:600;padding:10px 24px;border-radius:12px;background:#1E2433;color:#F5F1E8">teachablemachine.withgoogle.com</p>
<p style="font-size:30px;color:#5A5F6B">→</p>
<p style="font-size:30px;font-weight:600;padding:10px 24px;border-radius:12px;background:#FFFDF8;border:1px solid #D6CFBF">Get Started</p>
<p style="font-size:30px;color:#5A5F6B">→</p>
<p style="font-size:30px;font-weight:600;padding:10px 24px;border-radius:12px;background:#FFFDF8;border:1px solid #D6CFBF">Image Project</p>
<p style="font-size:30px;color:#5A5F6B">→</p>
<p style="font-size:30px;font-weight:600;padding:10px 24px;border-radius:12px;background:#FFFDF8;border:1px solid #D6CFBF">Standard image model</p>
</div>
<ol style="font-size:36px;line-height:1.45;color:#3B4252;display:flex;flex-direction:column;gap:14px">
<li><b>Оба партнёра, каждый на своём ноутбуке:</b> <b>Class 1</b> → «Акварель», <b>Class 2</b> → «Карандаш».</li>
<li>В каждом классе: <b>Upload</b> → ярлык «Стенд» на рабочем столе → нужная подпапка → Ctrl+A → Открыть.</li>
<li>Нажмите <b>Train Model</b> и засеките время. Вкладку не переключать!</li>
<li>Запишите в рабочий лист оба времени — ваше и партнёра.</li>
</ol>

</section>
<section class="slide" id="s1test" data-notes="Пары сами выбирают 6 картинок из 10 — выбор и есть их гипотеза. Ждём, что они возьмут ловушки и модель уверенно на них ошибётся: цветной карандаш примет за акварель, монохромную размывку — за карандаш. Значит, она различает цвет, а не технику. Это момент открытия, ничего не подсказывать. Пара угадала все 6 — подсказка П8. Быстрые пары после теста — карточка-челлендж. На 12-й минуте — следующий слайд." style="background:#F5F1E8;color:#1E2433;font-family:'Segoe UI', Arial, sans-serif;padding:128px;display:flex;flex-direction:column;gap:48px">
<div style="display:flex;gap:12px;align-items:center">
<p style="font-size:26px;padding:8px 22px;border-radius:999px;background:#E4DED1;color:#4A4F5C">Гипотеза</p>
<p style="font-size:26px;font-weight:700;padding:8px 22px;border-radius:999px;background:#2F6FB0;color:#F5F1E8">Стенд</p>
<p style="font-size:26px;padding:8px 22px;border-radius:999px;background:#E4DED1;color:#4A4F5C">Под капотом</p>
<p style="font-size:26px;padding:8px 22px;border-radius:999px;background:#E4DED1;color:#4A4F5C">Масштаб</p>
<p style="font-size:26px;padding:8px 22px;border-radius:999px;background:#E4DED1;color:#4A4F5C">Смета</p>
<p style="font-size:26px;padding:8px 22px;border-radius:999px;background:#E4DED1;color:#4A4F5C">Билет</p>
<div style="flex:1"></div>
<p style="font-family:'Segoe UI', Arial, sans-serif;font-size:32px;font-weight:700;color:#2F6FB0">2,5–12 мин</p>
</div>
<h2 style="font-family:'Segoe UI', Arial, sans-serif;font-size:72px;font-weight:700;line-height:1.1">Секретный тест</h2>
<div style="display:flex;gap:48px">
<ol style="flex:1;font-size:36px;line-height:1.45;color:#3B4252;display:flex;flex-direction:column;gap:14px">
<li>Справа, в окне <b>Preview</b>, переключите <b>Input</b>: Webcam → <b>File</b>.</li>
<li>В папке «Секретный_тест» 10 картинок. <b>Каждый выбирает 3</b> — где модель, по-вашему, может ошибиться, и одну, где не ошибётся.</li>
<li>Ответы и уверенность — в общую таблицу рабочего листа.</li>
</ol>
<div style="width:640px;display:flex;flex-direction:column;gap:16px;background:#1E2433;border-radius:20px;padding:48px">
<p style="font-family:'Segoe UI', Arial, sans-serif;font-size:28px;font-weight:600;letter-spacing:3px;text-transform:uppercase;color:#F2B36B">Главный вопрос</p>
<p style="font-family:'Segoe UI', Arial, sans-serif;font-size:44px;font-weight:600;line-height:1.25;color:#F5F1E8">Поймайте модель на жульничестве.</p>
<p style="font-size:32px;line-height:1.4;color:#C9D3E3">По какому признаку она на самом деле отличает акварель от карандаша?</p>
</div>
</div>

</section>
<section class="slide" id="s2" data-notes="Если пара не находит Advanced или Under the hood — подсказка П5. На 19-й минуте — слайд с конвертом. Если графики не появляются — в рабочем листе есть запасной путь (сравнить строки таблицы), вмешиваться не нужно. Быстрые пары — карточка-челлендж («Зубрила» отлично ложится на этот этап)." style="background:#F5F1E8;color:#1E2433;font-family:'Segoe UI', Arial, sans-serif;padding:128px;display:flex;flex-direction:column;gap:48px">
<div style="display:flex;gap:12px;align-items:center">
<p style="font-size:26px;padding:8px 22px;border-radius:999px;background:#E4DED1;color:#4A4F5C">Гипотеза</p>
<p style="font-size:26px;padding:8px 22px;border-radius:999px;background:#E4DED1;color:#4A4F5C">Стенд</p>
<p style="font-size:26px;font-weight:700;padding:8px 22px;border-radius:999px;background:#2F6FB0;color:#F5F1E8">Под капотом</p>
<p style="font-size:26px;padding:8px 22px;border-radius:999px;background:#E4DED1;color:#4A4F5C">Масштаб</p>
<p style="font-size:26px;padding:8px 22px;border-radius:999px;background:#E4DED1;color:#4A4F5C">Смета</p>
<p style="font-size:26px;padding:8px 22px;border-radius:999px;background:#E4DED1;color:#4A4F5C">Билет</p>
<div style="flex:1"></div>
<p style="font-family:'Segoe UI', Arial, sans-serif;font-size:32px;font-weight:700;color:#2F6FB0">12–20,5 мин</p>
</div>
<h2 style="font-family:'Segoe UI', Arial, sans-serif;font-size:72px;font-weight:700;line-height:1.1">Загляните под капот</h2>
<div style="display:flex;gap:48px">
<ol style="flex:1;font-size:34px;line-height:1.45;color:#3B4252;display:flex;flex-direction:column;gap:14px">
<li>Под Train Model раскройте <b>Advanced</b>. Найдите поле <b>Epochs</b>.</li>
<li><b>Партнёр 1:</b> Epochs = 1. <b>Партнёр 2:</b> Epochs = 10. Обучите, засеките время, проверьте 2 картинки, на которых модель ошиблась.</li>
<li>Нажмите <b>Under the hood</b>. Что растёт? Что падает?</li>
<li>Придумайте <b>свои названия</b> — таблица в рабочем листе.</li>
</ol>
<div style="width:560px;display:flex;flex-direction:column;gap:16px;justify-content:center;background:#FFFDF8;border:4px dashed #B8621B;border-radius:20px;padding:48px">
<svg width="72" height="72" viewBox="0 0 24 24" fill="none" stroke="#B8621B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>
<p style="font-family:'Segoe UI', Arial, sans-serif;font-size:44px;font-weight:600;line-height:1.25">Конверт пока закрыт</p>
<p style="font-size:32px;line-height:1.4;color:#3B4252">Сначала ваши слова. Термины — после пункта 4.</p>
</div>
</div>

</section>
<section class="slide" id="envelope" data-notes="Включить на 19-й минуте, когда у пар заполнена таблица «свои названия». Пара открыла конверт раньше времени — не страшно, но на этапе гипотез это видно по пустой таблице." style="background:#2F6FB0;color:#F5F1E8;font-family:'Segoe UI', Arial, sans-serif;padding:128px;display:flex;flex-direction:column;justify-content:center;gap:56px">
<p style="font-family:'Segoe UI', Arial, sans-serif;font-size:32px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:#DCE8F5">Под капотом · пункт 5</p>
<h2 style="font-family:'Segoe UI', Arial, sans-serif;font-size:112px;font-weight:700;line-height:1.05">Теперь откройте конверт</h2>
<p style="font-size:44px;line-height:1.35;width:1450px;color:#EEF3F9">Вы уже видели всё это своими руками. Сравните свои названия с тем, как это называют специалисты. Где вы оказались ближе всего?</p>

</section>
<section class="slide" id="s3" data-notes="Раздать досье в начале этапа (по одному на пару). Застряли на поиске числа — П6, на расчёте — П7. На 27-й минуте включить слайд-сверку." style="background:#F5F1E8;color:#1E2433;font-family:'Segoe UI', Arial, sans-serif;padding:128px;display:flex;flex-direction:column;gap:48px">
<div style="display:flex;gap:12px;align-items:center">
<p style="font-size:26px;padding:8px 22px;border-radius:999px;background:#E4DED1;color:#4A4F5C">Гипотеза</p>
<p style="font-size:26px;padding:8px 22px;border-radius:999px;background:#E4DED1;color:#4A4F5C">Стенд</p>
<p style="font-size:26px;padding:8px 22px;border-radius:999px;background:#E4DED1;color:#4A4F5C">Под капотом</p>
<p style="font-size:26px;font-weight:700;padding:8px 22px;border-radius:999px;background:#2F6FB0;color:#F5F1E8">Масштаб</p>
<p style="font-size:26px;padding:8px 22px;border-radius:999px;background:#E4DED1;color:#4A4F5C">Смета</p>
<p style="font-size:26px;padding:8px 22px;border-radius:999px;background:#E4DED1;color:#4A4F5C">Билет</p>
<div style="flex:1"></div>
<p style="font-family:'Segoe UI', Arial, sans-serif;font-size:32px;font-weight:700;color:#2F6FB0">20,5–28 мин</p>
</div>
<h2 style="font-family:'Segoe UI', Arial, sans-serif;font-size:72px;font-weight:700;line-height:1.1">А если научить его рисовать?</h2>
<p style="font-size:36px;line-height:1.4;color:#3B4252;width:1500px">Возьмите <b>досье</b>. Числа ищите в английском столбце, русский — подстраховка. Заполните лестницу в рабочем листе.</p>
<div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:24px">
<div style="display:flex;flex-direction:column;gap:10px;background:#FFFDF8;border:1px solid #E4DED1;border-radius:20px;padding:32px">
<p style="font-family:'Segoe UI', Arial, sans-serif;font-size:56px;font-weight:700;color:#2F6FB0">А</p>
<p style="font-size:30px;line-height:1.35">Что спрятано внутри нашего стенда</p>
</div>
<div style="display:flex;flex-direction:column;gap:10px;background:#FFFDF8;border:1px solid #E4DED1;border-radius:20px;padding:32px">
<p style="font-family:'Segoe UI', Arial, sans-serif;font-size:56px;font-weight:700;color:#2F6FB0">Б</p>
<p style="font-size:30px;line-height:1.35">Модель-художник в одном стиле</p>
</div>
<div style="display:flex;flex-direction:column;gap:10px;background:#FFFDF8;border:1px solid #E4DED1;border-radius:20px;padding:32px">
<p style="font-family:'Segoe UI', Arial, sans-serif;font-size:56px;font-weight:700;color:#2F6FB0">В</p>
<p style="font-size:30px;line-height:1.35">Генератор с нуля: сколько часов</p>
</div>
<div style="display:flex;flex-direction:column;gap:10px;background:#FFFDF8;border:1px solid #E4DED1;border-radius:20px;padding:32px">
<p style="font-family:'Segoe UI', Arial, sans-serif;font-size:56px;font-weight:700;color:#2F6FB0">Г</p>
<p style="font-size:30px;line-height:1.35">Генератор с нуля: сколько картинок</p>
</div>
</div>
<p style="font-size:32px;line-height:1.4;color:#3B4252"><b>Подсказка для расчёта:</b> часы × 3600 = секунды. Потом большое время делим на время вашего стенда.</p>

</section>
<section class="slide" id="ladder" data-notes="27-я минута, ровно одна минута: сверка для тех, кто не досчитал. 150 000 ч × 3600 = 540 000 000 с; ÷ 10 с = 54 000 000. У пар своё время стенда — их ответ будет другим, и это нормально: важен порядок величины. На 28-й минуте — смета." style="background:#1E2433;color:#F5F1E8;font-family:'Segoe UI', Arial, sans-serif;padding:128px;display:flex;flex-direction:column;gap:48px">
<h2 style="font-family:'Segoe UI', Arial, sans-serif;font-size:72px;font-weight:700;line-height:1.1">Сверка: лестница сложности</h2>
<div style="display:flex;gap:32px;align-items:end">
<div style="flex:1;display:flex;flex-direction:column;gap:12px;background:#2A3245;border-top:8px solid #8FB8E3;border-radius:20px;padding:40px">
<p style="font-family:'Segoe UI', Arial, sans-serif;font-size:28px;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:#8FB8E3">Наш стенд</p>
<p style="font-family:'Segoe UI', Arial, sans-serif;font-size:72px;font-weight:700;line-height:1.1">секунды</p>
<p style="font-size:30px;line-height:1.4;color:#C9D3E3">около 100 ваших картинок · ноутбук, браузер · дообучение готовой модели</p>
</div>
<div style="flex:1;display:flex;flex-direction:column;gap:12px;background:#2A3245;border-top:8px solid #F2B36B;border-radius:20px;padding:40px">
<p style="font-family:'Segoe UI', Arial, sans-serif;font-size:28px;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:#F2B36B">Художник в стиле</p>
<p style="font-family:'Segoe UI', Arial, sans-serif;font-size:72px;font-weight:700;line-height:1.1">37 минут</p>
<p style="font-size:30px;line-height:1.4;color:#C9D3E3">30 картинок · одна домашняя видеокарта · дообучение готового генератора</p>
</div>
<div style="flex:1;display:flex;flex-direction:column;gap:12px;background:#2A3245;border-top:8px solid #E8806B;border-radius:20px;padding:40px">
<p style="font-family:'Segoe UI', Arial, sans-serif;font-size:28px;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:#E8806B">Генератор с нуля</p>
<p style="font-family:'Segoe UI', Arial, sans-serif;font-size:72px;font-weight:700;line-height:1.1">150 000 ч</p>
<p style="font-size:30px;line-height:1.4;color:#C9D3E3">2,32 млрд картинок · 256 видеокарт · около 24 дней</p>
</div>
</div>
<p style="font-size:38px;line-height:1.4;color:#F5F1E8">Если стенд учился 10 секунд, генератор с нуля учился в <b style="color:#F2B36B">54 миллиона раз</b> дольше.</p>

</section>
<section class="slide" id="s4" data-notes="Раздать каждой паре одну карточку заказчика и бланк сметы. Бланки собрать вместе с рабочими листами после урока. Ожидаемые ответы — в памятке учителя." style="background:#F5F1E8;color:#1E2433;font-family:'Segoe UI', Arial, sans-serif;padding:128px;display:flex;flex-direction:column;gap:48px">
<div style="display:flex;gap:12px;align-items:center">
<p style="font-size:26px;padding:8px 22px;border-radius:999px;background:#E4DED1;color:#4A4F5C">Гипотеза</p>
<p style="font-size:26px;padding:8px 22px;border-radius:999px;background:#E4DED1;color:#4A4F5C">Стенд</p>
<p style="font-size:26px;padding:8px 22px;border-radius:999px;background:#E4DED1;color:#4A4F5C">Под капотом</p>
<p style="font-size:26px;padding:8px 22px;border-radius:999px;background:#E4DED1;color:#4A4F5C">Масштаб</p>
<p style="font-size:26px;font-weight:700;padding:8px 22px;border-radius:999px;background:#2F6FB0;color:#F5F1E8">Смета</p>
<p style="font-size:26px;padding:8px 22px;border-radius:999px;background:#E4DED1;color:#4A4F5C">Билет</p>
<div style="flex:1"></div>
<p style="font-family:'Segoe UI', Arial, sans-serif;font-size:32px;font-weight:700;color:#2F6FB0">28–34 мин</p>
</div>
<h2 style="font-family:'Segoe UI', Arial, sans-serif;font-size:72px;font-weight:700;line-height:1.1">Вам пришёл заказ</h2>
<p style="font-size:36px;line-height:1.4;color:#3B4252;width:1500px">У каждой пары свой заказчик. Заполните бланк сметы: как учить, сколько картинок, сколько времени, откуда данные — и главный красный флаг.</p>
<div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:24px">
<div style="background:#FFFDF8;border:1px solid #E4DED1;border-radius:20px;padding:32px"><p style="font-size:30px;line-height:1.35"><b>1.</b> Художница с 40 своими акварелями</p></div>
<div style="background:#FFFDF8;border:1px solid #E4DED1;border-radius:20px;padding:32px"><p style="font-size:30px;line-height:1.35"><b>2.</b> Музей: генератор в стиле передвижников</p></div>
<div style="background:#FFFDF8;border:1px solid #E4DED1;border-radius:20px;padding:32px"><p style="font-size:30px;line-height:1.35"><b>3.</b> Блогер и 30 чужих иллюстраций</p></div>
<div style="background:#FFFDF8;border:1px solid #E4DED1;border-radius:20px;padding:32px"><p style="font-size:30px;line-height:1.35"><b>4.</b> Стартап: генератор с нуля за 1 млн ₽</p></div>
</div>
<p style="font-size:34px;line-height:1.4;color:#1E2433"><b>Готово?</b> Положите бланк сметы на рабочий лист и поднимите зелёную карточку.</p>

</section>
<section class="slide" id="ticket" data-notes="Раздать каждому ученику выходной билет на 34-й минуте. Собрать на выходе. Минуты 37–40 — резерв: он съедается задержками раньше; если не съелся, урок просто заканчивается спокойно. Последние 30 секунд — слайд «Главная мысль», уже после того, как билеты заполнены, чтобы он не стал подсказкой." style="background:#F5F1E8;color:#1E2433;font-family:'Segoe UI', Arial, sans-serif;padding:128px;display:flex;flex-direction:column;gap:56px">
<div style="display:flex;gap:12px;align-items:center">
<p style="font-size:26px;padding:8px 22px;border-radius:999px;background:#E4DED1;color:#4A4F5C">Гипотеза</p>
<p style="font-size:26px;padding:8px 22px;border-radius:999px;background:#E4DED1;color:#4A4F5C">Стенд</p>
<p style="font-size:26px;padding:8px 22px;border-radius:999px;background:#E4DED1;color:#4A4F5C">Под капотом</p>
<p style="font-size:26px;padding:8px 22px;border-radius:999px;background:#E4DED1;color:#4A4F5C">Масштаб</p>
<p style="font-size:26px;padding:8px 22px;border-radius:999px;background:#E4DED1;color:#4A4F5C">Смета</p>
<p style="font-size:26px;font-weight:700;padding:8px 22px;border-radius:999px;background:#2F6FB0;color:#F5F1E8">Билет</p>
<div style="flex:1"></div>
<p style="font-family:'Segoe UI', Arial, sans-serif;font-size:32px;font-weight:700;color:#2F6FB0">34–37 мин</p>
</div>
<h2 style="font-family:'Segoe UI', Arial, sans-serif;font-size:72px;font-weight:700;line-height:1.1">Выходной билет</h2>
<div style="display:flex;gap:48px;align-items:center">
<svg width="160" height="160" viewBox="0 0 24 24" fill="none" stroke="#2F6FB0" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c3 2 9 2 12 0v-5"/><path d="M22 9v6"/></svg>
<p style="font-size:44px;line-height:1.4;width:1300px">Теперь — <b>каждый сам и молча</b>. Четыре строки своими словами. Сдайте билет на выходе.</p>
</div>

</section>
<section class="slide" id="idea" data-notes="Показать, когда билеты уже сданы (около 37-й минуты). Урок окончен." style="background:#1E2433;color:#F5F1E8;font-family:'Segoe UI', Arial, sans-serif;padding:128px;display:flex;flex-direction:column;justify-content:center;gap:56px">
<p style="font-family:'Segoe UI', Arial, sans-serif;font-size:32px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:#8FB8E3">Главная мысль</p>
<h2 style="font-family:'Segoe UI', Arial, sans-serif;font-size:80px;font-weight:700;line-height:1.15;width:1600px">Время обучения растёт с числом картинок, эпох и размером модели. Мощное железо его сокращает.</h2>
<p style="font-size:40px;line-height:1.4;color:#C9D3E3;width:1500px">Поэтому наш стенд — это ноутбук и секунды, а генератор картин с нуля — дата-центр и недели. И чем больше данных, тем важнее вопрос: <span style="color:#F2B36B">чьи они и можно ли их брать?</span></p>

</section>
</div></div>
<div id="hud"></div>
<div id="help">→ / пробел / щелчок — дальше · ← — назад · F — во весь экран · N — заметки для учителя</div>
<div id="notes"></div>
<script>
(function(){
  var slides = Array.prototype.slice.call(document.querySelectorAll('.slide'));
  var stage = document.getElementById('stage'), hud = document.getElementById('hud'), notes = document.getElementById('notes');
  var i = 0;
  try { var h = parseInt((location.hash.match(/\d+/)||[])[0], 10); if (h >= 1 && h <= slides.length) i = h - 1; } catch(e){}
  function fit(){
    var s = Math.min(window.innerWidth / 1920, window.innerHeight / 1080);
    stage.style.transform = 'scale(' + s + ')';
  }
  function show(n){
    i = Math.max(0, Math.min(slides.length - 1, n));
    slides.forEach(function(el, k){ el.classList.toggle('active', k === i); });
    hud.textContent = (i + 1) + ' / ' + slides.length;
    var t = slides[i].getAttribute('data-notes') || '';
    notes.innerHTML = '<b>Слайд ' + (i + 1) + '.</b> ' + (t ? t.replace(/[&<>]/g, function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;'}[c];}) : 'Заметок нет.');
    try { history.replaceState(null, '', '#' + (i + 1)); } catch(e){}
  }
  document.addEventListener('keydown', function(e){
    var k = e.key;
    if (k === 'ArrowRight' || k === 'PageDown' || k === ' ' || k === 'Enter') { e.preventDefault(); show(i + 1); }
    else if (k === 'ArrowLeft' || k === 'PageUp' || k === 'Backspace') { e.preventDefault(); show(i - 1); }
    else if (k === 'Home') show(0);
    else if (k === 'End') show(slides.length - 1);
    else if (k === 'f' || k === 'F' || k === 'а' || k === 'А') {
      if (!document.fullscreenElement) { (document.documentElement.requestFullscreen || function(){}).call(document.documentElement); }
      else { document.exitFullscreen(); }
    }
    else if (k === 'n' || k === 'N' || k === 'т' || k === 'Т') document.body.classList.toggle('show-notes');
  });
  document.getElementById('viewport').addEventListener('click', function(e){
    if (e.clientX < window.innerWidth * 0.25) show(i - 1); else show(i + 1);
  });
  window.addEventListener('resize', fit);
  setTimeout(function(){ document.getElementById('help').style.opacity = '0'; }, 6000);
  fit(); show(i);
})();
</script>
</body>
</html>

===== КОНЕЦ ФАЙЛА: 8-klass/snachala-obuchi/slajdy.html =====

===== ФАЙЛ: 8-klass/snachala-obuchi/razdatka.html =====
<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Раздатка — «Сначала обучи, потом объясни»</title>
<style>
  :root{ --ink:#1E2433; --soft:#3B4252; --muted:#6B6F78; --line:#BFB8A8; --accent:#2F6FB0; --paper:#FFFFFF; --bg:#EDE9E0; }
  *{box-sizing:border-box}
  html{background:var(--bg)}
  body{margin:0;font:14px/1.42 "Segoe UI",Arial,"Helvetica Neue",sans-serif;color:var(--ink)}
  .toolbar{position:sticky;top:0;z-index:5;background:var(--ink);color:#F5F1E8;padding:10px 16px;display:flex;gap:12px;flex-wrap:wrap;align-items:center}
  .toolbar b{font-size:16px}
  .toolbar a{color:#BFD6EE;text-decoration:none;font-size:14px}
  .toolbar button{margin-left:auto;font:inherit;padding:6px 14px;border-radius:8px;border:0;background:#F2B36B;color:#1E2433;font-weight:700;cursor:pointer}
  .hint{max-width:210mm;margin:16px auto 0;padding:0 16px;color:var(--soft);font-size:14px}
  .page{background:var(--paper);width:210mm;min-height:297mm;margin:16px auto;padding:14mm 15mm;box-shadow:0 2px 10px rgba(0,0,0,.12)}
  .tag{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);margin-bottom:2mm}
  h1{font-size:22px;margin:0 0 3mm}
  h2{font-size:16px;margin:6mm 0 2mm;padding-top:2mm;border-top:1.5px solid var(--ink)}
  h2:first-of-type{margin-top:4mm}
  p{margin:1.5mm 0}
  ol,ul{margin:1.5mm 0 1.5mm 6mm;padding:0}
  li{margin:.8mm 0}
  .small{font-size:12.5px;color:var(--soft)}
  .rule{border:1px solid var(--line);border-radius:6px;padding:3mm 4mm;background:#FAF8F3;font-size:13.5px}
  table{width:100%;border-collapse:collapse;margin:2mm 0}
  th,td{border:1px solid var(--line);padding:1.2mm 2.4mm;text-align:left;vertical-align:top}
  th{background:#F1EEE6;font-size:13px}
  td.w{height:9mm}
  td.tall{height:16mm}
  .ln{border-bottom:1px solid var(--line);height:8mm}
  .fill{display:inline-block;border-bottom:1px solid var(--ink);min-width:28mm}
  .fill.wide{min-width:70mm}
  .pill{display:inline-block;border:1px solid var(--line);border-radius:4px;padding:0 1.5mm;font-weight:600;background:#F7F5EF}
  .cut{border:1.5px dashed #8C8676;border-radius:4px;padding:4mm 5mm;margin:0 0 4mm}
  .cuthint{font-size:11px;color:var(--muted);margin:0 0 2mm}
  .grid2{display:grid;grid-template-columns:1fr 1fr;gap:4mm}
  .src{font-size:12px;color:var(--soft);margin-top:0}
  .src code{font-size:11.5px;word-break:break-all}
  .en{font-family:Georgia,"Times New Roman",serif}
  .card-letter{font-size:28px;font-weight:800;color:var(--accent);line-height:1}
  .big{font-size:17px}
  @media print{
    @page{size:A4;margin:0}
    html,body{background:#fff}
    .toolbar,.hint{display:none}
    .page{margin:0;box-shadow:none;width:auto;min-height:0;height:297mm;overflow:hidden;break-after:page;page-break-after:always}
    .page:last-child{break-after:auto;page-break-after:auto}
    a{color:inherit;text-decoration:none}
  }
</style>
</head>
<body>

<div class="toolbar">
  <a href="../../dlya-uchitelya.html">← Для учителя</a>
  <b>Раздатка</b>
  <a href="#p1">1–3 Рабочий лист</a>
  <a href="#p3">4 Конверт</a>
  <a href="#p4">5–6 Досье</a>
  <a href="#p6">7 Челлендж</a>
  <a href="#p7">8–9 Смета</a>
  <a href="#p9">10 Подсказки</a>
  <a href="#p10">11 Билет</a>
  <button onclick="window.print()">Печать</button>
</div>
<p class="hint">Каждый блок — отдельная страница A4. При печати укажите нужные страницы и число копий: сколько и чего печатать — в памятке учителю. В диалоге печати выберите поля «Нет» или «Минимальные» и отключите колонтитулы.</p>

<!-- ============ СТР. 1 ============ -->
<section class="page" id="p1">
  <span class="tag">Рабочий лист пары · стр. 1 из 3</span>
  <h1>Сначала обучи, потом объясни</h1>
  <p>Имена: <span class="fill wide"></span> и <span class="fill wide"></span></p>
  <div class="rule"><b>Правила урока.</b> Учитель сегодня молчит. Вы — нет: обсуждайте с напарником, спорьте, помогайте соседям (вполголоса). У каждого свой ноутбук, но модель одна на двоих: делайте одно и то же и делите проверку. Застряли — положите на ноутбук <b>красную карточку</b>, учитель молча принесёт подсказку. Закончили этап — <b>зелёную</b>. Какой сейчас этап и до какой минуты он идёт — на слайде.</div>

  <h2>Этап 0. Гипотеза (до работы на ноутбуке)</h2>
  <p>Сегодня вы научите компьютер отличать <b>акварель</b> от <b>карандашного рисунка</b>. Пока не начали, запишите прогноз:</p>
  <p>Компьютер научится за <span class="fill"></span> секунд. Из 6 секретных картинок он угадает <span class="fill"></span>.</p>

  <h2>Этап 1. Стенд</h2>
  <ol>
    <li><b>Каждый на своём ноутбуке.</b> Teachable Machine уже открыта. Если нет: <b>teachablemachine.withgoogle.com</b> → <span class="pill">Get Started</span> → <span class="pill">Image Project</span> → <span class="pill">Standard image model</span>.</li>
    <li>Щёлкните по названию «Class 1» и переименуйте в «Акварель». «Class 2» — в «Карандаш».</li>
    <li>В карточке «Акварель» нажмите <span class="pill">Upload</span> → ярлык <b>«Стенд»</b> на рабочем столе → <b>Акварель</b> → выделите все файлы (Ctrl+A) → Открыть. То же для «Карандаш» из папки <b>Карандаш</b>.</li>
    <li>Нажмите <span class="pill">Train Model</span> и засеките время до конца обучения. Пока модель учится, не переключайте вкладку.</li>
    <li>Справа, в окне <b>Preview</b>, переключите <b>Input</b> с Webcam на <b>File</b>. В папке <b>Секретный_тест</b> 10 картинок, проверяете 6: <b>каждый партнёр выбирает 3</b>. Берите те, где модель, по-вашему, может ошибиться, — и одну, где не ошибётся. В окне выбора файла включите крупные значки, чтобы видеть картинки. Таблица общая.</li>
  </ol>
  <p>Время обучения: у партнёра 1 — <span class="fill"></span> с, у партнёра 2 — <span class="fill"></span> с.</p>
  <table>
    <tr><th style="width:5%">№</th><th style="width:15%">Файл</th><th style="width:20%">Ответ модели</th><th style="width:17%">Уверенность, %</th><th>Ваше мнение: что это на самом деле?</th></tr>
    <tr><td class="w">1</td><td></td><td></td><td></td><td></td></tr>
    <tr><td class="w">2</td><td></td><td></td><td></td><td></td></tr>
    <tr><td class="w">3</td><td></td><td></td><td></td><td></td></tr>
    <tr><td class="w">4</td><td></td><td></td><td></td><td></td></tr>
    <tr><td class="w">5</td><td></td><td></td><td></td><td></td></tr>
    <tr><td class="w">6</td><td></td><td></td><td></td><td></td></tr>
  </table>
</section>

<!-- ============ СТР. 2 ============ -->
<section class="page" id="p2">
  <span class="tag">Рабочий лист пары · стр. 2 из 3</span>
  <h2>Этап 1. Что показал тест</h2>
  <p>Модель уверенно ошиблась на картинках: <span class="fill wide"></span>. Что у них общего?</p>
  <div class="ln"></div>
  <p><b>Поймайте модель на жульничестве.</b> По какому признаку она на самом деле отличает «акварель» от «карандаша»? Это то же самое, что техника рисования?</p>
  <div class="ln"></div><div class="ln"></div>
  <h2>Этап 2. Под капотом</h2>
  <ol>
    <li>Под кнопкой Train Model раскройте <span class="pill">Advanced</span>. Найдите поле <b>Epochs</b>. Сейчас там стоит число <span class="fill"></span>.</li>
    <li><b>Партнёр 1</b> ставит Epochs = <b>1</b>, <b>партнёр 2</b> — Epochs = <b>10</b>. Каждый: Train Model → засеките время → проверьте модель на двух картинках, на которых она ошиблась в этапе 1. В последнюю строку перенесите время из этапа 1: там модель училась с числом эпох по умолчанию (п. 1), заново обучать не нужно.</li>
  </ol>
  <table>
    <tr><th style="width:20%">Epochs</th><th style="width:40%">Время обучения, с</th><th>Угадала из 2 трудных</th></tr>
    <tr><td>1</td><td></td><td></td></tr>
    <tr><td>10</td><td></td><td></td></tr>
    <tr><td>____ (этап 1)</td><td></td><td>0 — на них она и ошиблась</td></tr>
  </table>
  <ol start="3">
    <li>В том же блоке Advanced нажмите <span class="pill">Under the hood</span>. <b>Если появились графики:</b> по горизонтальной оси — те самые Epochs, одна линия растёт, другая падает. <b>Если графиков нет:</b> посмотрите на таблицу выше — что растёт и что меняется вместе с числом эпох?<br>
    Растёт, по-нашему: <span class="fill wide"></span><br>
    Падает, по-нашему: <span class="fill wide"></span></li>
    <li>Придумайте свои названия, <b>пока не открыли конверт</b>:</li>
  </ol>
  <table>
    <tr><th style="width:36%">Что</th><th style="width:28%">Наше название</th><th>Почему так</th></tr>
    <tr><td>Число в поле Epochs</td><td class="w"></td><td></td></tr>
    <tr><td>То, что уменьшается с эпохами (падающая линия)</td><td class="w"></td><td></td></tr>
    <tr><td>Все картинки в папке «Стенд»</td><td class="w"></td><td></td></tr>
    <tr><td>Картинки из «Секретного теста»</td><td class="w"></td><td></td></tr>
  </table>
  <ol start="5">
    <li><b>Теперь откройте конверт с терминами.</b> Совпали ли ваши названия по смыслу? Где ближе всего? <span class="fill wide"></span></li>
  </ol>
</section>

<!-- ============ СТР. 3 ============ -->
<section class="page" id="p2b">
  <span class="tag">Рабочий лист пары · стр. 3 из 3</span>
  <h2>Этап 3. Масштаб</h2>
  <p>Возьмите досье. Числа берите из первоисточника (английский столбец), русский — подстраховка.</p>
  <table>
    <tr><th style="width:34%">Что обучаем</th><th style="width:20%">Сколько картинок</th><th style="width:22%">Сколько времени учится</th><th>Откуда число</th></tr>
    <tr><td>Наш стенд</td><td></td><td>______ с</td><td>наш опыт</td></tr>
    <tr><td>Модель-художник в одном стиле</td><td></td><td>______ мин</td><td>досье, карточка Б</td></tr>
    <tr><td>Генератор картин с нуля</td><td></td><td>______ часов</td><td>досье, карточки В и Г</td></tr>
  </table>
  <p>Посчитайте (калькулятор можно):</p>
  <ul>
    <li>Генератор с нуля: <span class="fill"></span> часов × 3600 = <span class="fill wide"></span> секунд.</li>
    <li>Во сколько раз дольше, чем наш стенд? <span class="fill"></span> ÷ <span class="fill"></span> = <span class="fill"></span> раз.</li>
    <li>Во сколько раз больше картинок, чем у нас? <span class="fill"></span> раз.</li>
    <li>Почему наш стенд учится секунды, хотя различает картинки? Подсказка — карточка А.</li>
  </ul>
  <div class="ln"></div>
  <p class="small"><b>Закончили раньше всех?</b> Возьмите у учителя карточку-челлендж. Результат — на обороте этого листа.</p>
</section>

<!-- ============ СТР. 3 ============ -->
<section class="page" id="p3">
  <span class="tag">Конверт с терминами · вложить в конверт, на конверте написать: «Открыть только после пункта 4 этапа “Под капотом”»</span>
  <h1>Вы уже всё это видели своими руками</h1>
  <p class="big">Вот как это называют специалисты.</p>
  <table>
    <tr><th style="width:24%">Термин</th><th style="width:50%">Что это</th><th>Где вы это видели</th></tr>
    <tr><td><b>Модель</b></td><td>Программа, которая сама выводит правила из примеров. Правила ей никто не пишет — ей показывают примеры.</td><td>То, что вы обучили в Teachable Machine</td></tr>
    <tr><td><b>Обучающая выборка</b></td><td>Все примеры, на которых учится модель. Какая выборка — такая и модель.</td><td>Папка «Стенд»</td></tr>
    <tr><td><b>Эпоха</b></td><td>Один полный проход модели по всей обучающей выборке. 50 эпох — модель просмотрела все картинки 50 раз.</td><td>Поле Epochs</td></tr>
    <tr><td><b>Ошибка обучения (loss)</b></td><td>«Штрафные очки» модели: число, которое показывает, насколько она сейчас ошибается. Во время обучения должно падать.</td><td>Падающая линия в Under the hood</td></tr>
    <tr><td><b>Дообучение</b></td><td>Модель учат не с нуля: берут готовую, которую уже учили на миллионах картинок, и доучивают на своих примерах.</td><td>Почему стенд учится секунды</td></tr>
  </table>
  <h2>Для тех, кто хочет больше</h2>
  <table>
    <tr><th style="width:24%">Термин</th><th>Что это</th></tr>
    <tr><td><b>Тестовые данные</b></td><td>Примеры, которых модель не видела при обучении. Только на них видно, научилась она или просто запомнила. У вас — «Секретный тест».</td></tr>
    <tr><td><b>Точность (accuracy)</b></td><td>Доля правильных ответов модели. Растущая линия в Under the hood.</td></tr>
    <tr><td><b>Переобучение</b></td><td>Модель вызубрила обучающие примеры, а на новых ошибается. Как ученик, который выучил ответы, но не понял тему.</td></tr>
    <tr><td><b>Час работы видеокарты (GPU-час)</b></td><td>Единица «стоимости» обучения: один час работы одной видеокарты. 10 видеокарт за 1 час = 10 GPU-часов.</td></tr>
  </table>
  <div class="rule big" style="margin-top:6mm"><b>Главная мысль урока одной строкой:</b> время обучения растёт вместе с числом картинок, числом эпох и размером модели — а мощное железо это время сокращает.</div>
</section>

<!-- ============ СТР. 4 ============ -->
<section class="page" id="p4">
  <span class="tag">Досье · стр. 1 из 2</span>
  <h1>Досье: откуда берутся большие числа</h1>
  <p class="small">Слева — дословная строка из первоисточника (в кавычках) и пересказ остального по-английски. Справа — то же по-русски. Числа ищите в левом столбце, правый — подстраховка.</p>

  <h2><span class="card-letter">А</span>&nbsp; Что внутри Teachable Machine</h2>
  <p class="src">Источник: Google, учебный курс «TensorFlow.js: Make your own Teachable Machine using transfer learning» — <code>codelabs.developers.google.com/codelabs/tensorflowjs-teachablemachine-codelab</code></p>
  <table>
    <tr><th style="width:50%">English</th><th>По-русски</th></tr>
    <tr><td class="en">Original line: the base model “was trained on a huge dataset known as ImageNet that has millions of labelled images”.</td><td>Готовую модель внутри заранее обучили на огромном наборе картинок ImageNet — в нём миллионы картинок с подписями.</td></tr>
    <tr><td class="en">Summary: the model already recognises 1000 kinds of objects. Teachable Machine reuses it and only teaches the last step on your examples. This is called transfer learning.</td><td>Эта модель уже различает 1000 видов предметов. Teachable Machine берёт её готовой и доучивает только последний шаг на ваших примерах. Это называется дообучением (transfer learning).</td></tr>
  </table>

  <h2><span class="card-letter">Б</span>&nbsp; Модель-художник в одном стиле</h2>
  <p class="src">Источник: карточка модели «Medieval Marginalia — FLUX.2 [klein] LoRA» на сайте Hugging Face — <code>huggingface.co/stephenbtl/marginalia-drolleries-klein-4b-lora</code></p>
  <table>
    <tr><th style="width:50%">English</th><th>По-русски</th></tr>
    <tr><td class="en">Original line: “GPU: RTX 4090, ~37 minutes”.</td><td>Видеокарта: одна домашняя RTX 4090, около 37 минут.</td></tr>
    <tr><td class="en">Summary: a style add-on (LoRA) for a ready-made image generator. It learned to draw like medieval book margins from 30 public-domain images. The author kept a middle version, because later versions overfitted.</td><td>Это «насадка» к готовому генератору картинок: она научила его рисовать в стиле средневековых книжных полей. Обучающая выборка — 30 картинок из общественного достояния. Автор оставил версию из середины обучения: поздние версии переобучились.</td></tr>
  </table>
</section>

<!-- ============ СТР. 5 ============ -->
<section class="page" id="p5">
  <span class="tag">Досье · стр. 2 из 2</span>
  <h2><span class="card-letter">В</span>&nbsp; Генератор картин с нуля: время</h2>
  <p class="src">Источник: официальная карточка модели «Stable Diffusion v1-4» (авторы Robin Rombach, Patrick Esser) — <code>huggingface.co/CompVis/stable-diffusion-v1-4</code></p>
  <table>
    <tr><th style="width:50%">English</th><th>По-русски</th></tr>
    <tr><td class="en">Original line: “Hardware Type: A100 PCIe 40GB; Hours used: 150000”.</td><td>Тип видеокарты: A100 (серверная). Использовано часов: 150 000.</td></tr>
    <tr><td class="en">Summary: training ran on 32 × 8 A100 GPUs — 256 graphics cards at once. The model was trained on subsets of the LAION-2B(en) dataset.</td><td>Обучение шло на 32 × 8 = 256 видеокартах одновременно. Обучающая выборка — части набора LAION-2B(en). Что значит «2B» — смотрите карточку Г.</td></tr>
  </table>

  <h2><span class="card-letter">Г</span>&nbsp; Генератор картин с нуля: картинки</h2>
  <p class="src">Источник: научная статья «LAION-5B: An open large-scale dataset for training next generation image-text models» (2022) — <code>arxiv.org/abs/2210.08402</code></p>
  <table>
    <tr><th style="width:50%">English</th><th>По-русски</th></tr>
    <tr><td class="en">Summary of the abstract: LAION-5B has 5.85 billion image–text pairs. Of these, 2.32 billion have English text — this English part is called LAION-2B(en).</td><td>В наборе LAION-5B — 5,85 миллиарда пар «картинка + подпись». Из них 2,32 миллиарда с английскими подписями: эта часть и называется LAION-2B(en). «B» — billion, миллиард.</td></tr>
  </table>

  <div class="rule" style="margin-top:6mm"><b>Осторожно с выводами.</b> 150 000 часов — это суммарная работа всех 256 видеокарт. Сам календарный срок был намного короче: 150 000 ÷ 256 ≈ 586 часов, примерно 24 дня.</div>
</section>

<!-- ============ СТР. 6 ============ -->
<section class="page" id="p6">
  <span class="tag">Карточка-челлендж · для пар, которые закончили этап раньше</span>
  <h1>Испытания для быстрых</h1>
  <p>Выберите любое испытание. Результат запишите на обороте рабочего листа.</p>
  <table>
    <tr><th style="width:18%">Испытание</th><th style="width:44%">Что сделать</th><th>Что выяснить</th></tr>
    <tr><td><b>Отравитель</b></td><td>В класс «Карандаш» дополнительно загрузите 20 акварелей из папки «Стенд/Акварель». Обучите заново и прогоните «Секретный тест».</td><td>Насколько испортилась модель? Как злоумышленник мог бы так испортить чужую модель — и почему это проблема безопасности?</td></tr>
    <tr><td><b>Голодная модель</b></td><td>Новый проект: по 5 картинок в каждом классе. Обучите, прогоните тест.</td><td>Во сколько раз хуже, чем на 50 картинках? Что важнее: число эпох или число картинок?</td></tr>
    <tr><td><b>Зубрила</b></td><td>Поставьте Epochs = 200. Обучите, посмотрите Under the hood и тест.</td><td>После какой эпохи линия ошибки почти перестаёт падать? Стало ли лучше на тесте — или модель начала зубрить?</td></tr>
    <tr><td><b>Где мои данные?</b></td><td>Найдите на сайте Teachable Machine раздел FAQ и вопрос о том, кто видит ваши картинки.</td><td>Куда уходят ваши картинки при обучении? Чем это отличается от загрузки своего фото в онлайн-генератор?</td></tr>
  </table>
</section>

<!-- ============ СТР. 7 ============ -->
<section class="page" id="p7">
  <span class="tag">Смета · карточки заказчиков · разрезать, по одной на пару</span>
  <h1>Вам пришёл заказ</h1>
  <div class="cut"><p class="cuthint">✂ ………………………………………………</p><p class="big"><b>Заказчик 1. Художница Алина.</b></p><p class="big">«У меня 40 моих акварелей. Хочу, чтобы ИИ помогал делать эскизы в моём стиле — для меня самой».</p></div>
  <div class="cut"><p class="cuthint">✂ ………………………………………………</p><p class="big"><b>Заказчик 2. Музей.</b></p><p class="big">«Для интерактивной выставки нужен генератор картин в стиле передвижников — русских художников XIX века. Посетитель вводит тему, ИИ рисует».</p></div>
  <div class="cut"><p class="cuthint">✂ ………………………………………………</p><p class="big"><b>Заказчик 3. Блогер Макс.</b></p><p class="big">«Хочу картинки как у одного популярного современного иллюстратора. Скачаю 30 его работ из соцсетей — и готово».</p></div>
  <div class="cut"><p class="cuthint">✂ ………………………………………………</p><p class="big"><b>Заказчик 4. Стартап.</b></p><p class="big">«Хотим свой генератор картин, как у больших компаний, полностью с нуля. Бюджет — 1 миллион рублей».</p><p class="small">Условие задачи (не точная цена): допустим, час работы одной серверной видеокарты стоит 150 рублей.</p></div>
</section>

<!-- ============ СТР. 8 ============ -->
<section class="page" id="p8">
  <span class="tag">Смета · бланк, по одному на пару</span>
  <h1>Смета нейро-художника</h1>
  <p>Заказчик № <span class="fill"></span> &nbsp;&nbsp; Пара: <span class="fill wide"></span></p>
  <p class="small">На смету — 5 минут. Готово — положите бланк на рабочий лист и поднимите зелёную карточку.</p>
  <table>
    <tr><th style="width:42%">Вопрос</th><th>Наш ответ</th></tr>
    <tr><td>Как учить: дообучить готовый генератор или с нуля? Почему?</td><td class="tall"></td></tr>
    <tr><td>Сколько картинок понадобится (примерно)?</td><td class="tall"></td></tr>
    <tr><td>Сколько времени будет учиться и на каком железе?</td><td class="tall"></td></tr>
    <tr><td>Откуда взять картинки — и можно ли их брать?</td><td class="tall"></td></tr>
    <tr><td>Красный флаг: главный риск этого заказа</td><td class="tall"></td></tr>
    <tr><td><b>Вердикт:</b> берёмся / берёмся с условием / отказываемся</td><td class="tall"></td></tr>
  </table>
</section>

<!-- ============ СТР. 9 ============ -->
<section class="page" id="p9">
  <span class="tag">Карточки-подсказки · для учителя · разрезать</span>
  <h1>Подсказки П1–П8</h1>
  <p class="small">Пара подняла красную карточку — подойти, посмотреть на экран, молча положить нужную подсказку.</p>
  <div class="grid2">
    <div class="cut"><p><b>П1 · Не нажимается Train Model</b></p><p>В каждом классе должны быть картинки — под названием класса видны миниатюры. Классов должно быть два.</p></div>
    <div class="cut"><p><b>П2 · Не можем найти папку с картинками</b></p><p>Ярлык «Стенд» — на рабочем столе. Если его нет, путь к сетевой папке:</p><div class="ln"></div></div>
    <div class="cut"><p><b>П3 · Модель на всё отвечает одно и то же</b></p><p>Проверьте, не загрузили ли вы одну и ту же папку в оба класса. Исправьте и обучите заново.</p></div>
    <div class="cut"><p><b>П4 · Обучение зависло</b></p><p>Не переключайте вкладку, пока модель учится. Висит дольше 2 минут — обновите страницу и начните заново.</p></div>
    <div class="cut"><p><b>П5 · Где Advanced и Under the hood?</b></p><p>Под кнопкой Train Model есть строка Advanced со стрелкой. Under the hood — внизу раскрывшегося блока.</p></div>
    <div class="cut"><p><b>П6 · Не нашли число в досье</b></p><p>Б: строка «GPU». В: «Hours used». Г: слово billion — это миллиард.</p></div>
    <div class="cut"><p><b>П7 · Не понимаем, что считать</b></p><p>Пример: 2 часа = 2 × 3600 = 7200 секунд. Большое время в секундах делим на время вашего стенда.</p></div>
    <div class="cut"><p><b>П8 · Модель угадала все 6</b></p><p>Найдите тест, где уверенность модели ниже всего. Почему именно он? Потом — карточка-челлендж.</p></div>
  </div>
</section>

<!-- ============ СТР. 10 ============ -->
<section class="page" id="p10">
  <span class="tag">Выходной билет · два на листе, разрезать по линии</span>
  <div class="cut" style="padding:6mm 7mm">
    <h1>Выходной билет</h1>
    <p>Имя: <span class="fill wide"></span></p>
    <ol>
      <li>Обучение нейросети становится дольше и дороже, когда растёт <span class="fill"></span>, <span class="fill"></span> и <span class="fill"></span>.</li>
      <li>Наш стенд учился <span class="fill"></span> секунд. Генератор картин с нуля учился <span class="fill"></span> часов работы видеокарт. Это примерно в <span class="fill"></span> раз дольше.</li>
      <li>Генератор картин учить намного сложнее, потому что</li>
    </ol>
    <div class="ln"></div><div class="ln"></div>
    <ol start="4"><li>Одно, что меня сегодня удивило:</li></ol>
    <div class="ln"></div>
  </div>
  <div class="cut" style="padding:6mm 7mm">
    <h1>Выходной билет</h1>
    <p>Имя: <span class="fill wide"></span></p>
    <ol>
      <li>Обучение нейросети становится дольше и дороже, когда растёт <span class="fill"></span>, <span class="fill"></span> и <span class="fill"></span>.</li>
      <li>Наш стенд учился <span class="fill"></span> секунд. Генератор картин с нуля учился <span class="fill"></span> часов работы видеокарт. Это примерно в <span class="fill"></span> раз дольше.</li>
      <li>Генератор картин учить намного сложнее, потому что</li>
    </ol>
    <div class="ln"></div><div class="ln"></div>
    <ol start="4"><li>Одно, что меня сегодня удивило:</li></ol>
    <div class="ln"></div>
  </div>
</section>

</body>
</html>

===== КОНЕЦ ФАЙЛА: 8-klass/snachala-obuchi/razdatka.html =====

===== ФАЙЛ: 8-klass/snachala-obuchi/pamyatka.html =====
<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Памятка учителю «Сначала обучи, потом объясни»</title>
<style>
:root{--ink:#1d2126;--ink2:#5b5346;--line:#d9cfb9;--paper:#f6f1e6;--accent:#f2a93b}
*{box-sizing:border-box}
html,body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 "Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
.bar{position:sticky;top:0;z-index:5;display:flex;gap:10px;align-items:center;flex-wrap:wrap;padding:10px 16px;background:#1f2329;color:#eef1f4;border-bottom:3px solid var(--accent)}
.bar a,.bar button{font:inherit;font-size:14px;color:#eef1f4;background:#272c33;border:1px solid #3a414a;border-radius:18px;padding:5px 12px;text-decoration:none;cursor:pointer}
.bar button{background:var(--accent);color:#2a1d05;border-color:var(--accent);font-weight:700}
.bar .t{flex:1;min-width:0;color:#a9b2bc;font-size:14px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.doc{max-width:860px;margin:20px auto 48px;background:#fff;border:1px solid var(--line);border-radius:12px;padding:28px 34px}
h1{font-size:28px;line-height:1.25;margin:0 0 12px}
h2{font-size:21px;margin:28px 0 10px;padding-bottom:4px;border-bottom:1px solid var(--line)}
h3{font-size:17px;margin:20px 0 8px}
p{margin:8px 0}
table{border-collapse:collapse;width:100%;margin:10px 0;font-size:14.5px}
th,td{border:1px solid #cfc5ae;padding:6px 8px;vertical-align:top;text-align:left}
th{background:#f3ecdd}
td:empty::after{content:"\00a0"}
blockquote{margin:10px 0;padding:8px 14px;border-left:4px solid var(--accent);background:#fbf6ea}
pre{white-space:pre-wrap;background:#f3ecdd;border-radius:8px;padding:10px 12px;font-size:14.5px}
code{font-family:Consolas,"Courier New",monospace}
ul,ol{padding-left:24px}
li[data-checked]{list-style:none;margin-left:-20px}
hr{border:0;border-top:1px dashed #b9a77f;margin:18px 0}
a{color:#1f5fa8}
@media (max-width:600px){.doc{padding:18px 16px;margin:10px 8px}table{font-size:13px}}
@media print{
  html,body{background:#fff}
  .bar{display:none}
  .doc{border:0;border-radius:0;margin:0;padding:0;max-width:none}
  h2{break-after:avoid}
  tr,blockquote,pre{break-inside:avoid}
  a{color:inherit;text-decoration:none}
  @page{size:A4;margin:14mm 14mm 16mm}
}
</style>
</head>
<body>
<div class="bar"><a href="../../dlya-uchitelya.html">← Для учителя</a><span class="t">Памятка учителю «Сначала обучи, потом объясни»</span><button type="button" onclick="window.print()">Печать</button></div>
<main class="doc">
<h1>Памятка учителю — «Сначала обучи, потом объясни»</h1>
<p>ИИ и информационная безопасность · 8 класс · 40 минут · 4 пары</p>
<p>Тайминг рассчитан с запасом: на проверку одной тестовой картинки
заложено 40 секунд, на каждую смену слайда — 20–30 секунд задержки, плюс
3 минуты резерва в конце урока. Прогон накануне не нужен: всё
непроверенное подстраховано в раздатке и подсказках.</p>
<h2 id="комплект">Комплект</h2>
<table>
<thead>
<tr class="header">
<th>Файл</th>
<th>Что это</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><code>slajdy.html</code></td>
<td>Слайды урока, 13 штук. Открыть в браузере, интернет не нужен.</td>
</tr>
<tr class="even">
<td><code>razdatka.html</code></td>
<td>Вся раздатка, 11 страниц A4. Открыть в браузере → «Печать».</td>
</tr>
<tr class="odd">
<td><code>pamyatka_uchitelyu.md</code></td>
<td>Этот файл.</td>
</tr>
<tr class="even">
<td>Папка <code>Тренировочный_стенд</code></td>
<td>Картинки из сборщика: <code>Стенд</code>,
<code>Секретный_тест</code>, <code>Для_учителя</code>.</td>
</tr>
</tbody>
</table>
<p><strong>Управление слайдами:</strong> → / пробел / щелчок — дальше ·
← — назад · F — во весь экран · N — заметки для учителя (не включать,
когда экран виден классу). Номер слайда можно открыть сразу:
<code>slajdy.html#7</code>.</p>
<h2 id="что-распечатать">Что распечатать</h2>
<p>В диалоге печати: поля «Нет» или «Минимальные», колонтитулы
выключить, «Фоновая графика» включить.</p>
<table>
<thead>
<tr class="header">
<th>Страницы <code>razdatka.html</code></th>
<th>Что</th>
<th>Копий</th>
<th>Когда выдать</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>1–3</td>
<td>Рабочий лист пары</td>
<td>4</td>
<td>на столах до урока</td>
</tr>
<tr class="even">
<td>4</td>
<td>Конверт с терминами</td>
<td>4 (вложить в конверты)</td>
<td>на столах до урока, закрытые</td>
</tr>
<tr class="odd">
<td>5–6</td>
<td>Досье</td>
<td>4</td>
<td>в начале этапа «Масштаб» (20,5 мин)</td>
</tr>
<tr class="even">
<td>7</td>
<td>Карточка-челлендж</td>
<td>2</td>
<td>у учителя, по запросу быстрых пар</td>
</tr>
<tr class="odd">
<td>8</td>
<td>Карточки заказчиков (разрезать)</td>
<td>1</td>
<td>в начале этапа «Смета» (28 мин)</td>
</tr>
<tr class="even">
<td>9</td>
<td>Бланк сметы</td>
<td>4</td>
<td>там же</td>
</tr>
<tr class="odd">
<td>10</td>
<td>Подсказки П1–П8 (разрезать)</td>
<td>1</td>
<td>у учителя</td>
</tr>
<tr class="even">
<td>11</td>
<td>Выходные билеты, два на листе (разрезать)</td>
<td>4</td>
<td>в начале этапа «Билет» (34 мин)</td>
</tr>
</tbody>
</table>
<p>Плюс: красная и зелёная карточки на каждую пару — просто листы
цветной бумаги, 4 + 4. На конверте написать: «Открыть только после
пункта 4 этапа “Под капотом”».</p>
<h2 id="разложить-до-урока">Разложить до урока</h2>
<ul class="task-list">
<li><label><input type="checkbox" />В сетевую папку — <code>Стенд</code>
(подпапки «Акварель» и «Карандаш») и <code>Секретный_тест</code>
целиком, все 10 картинок. Из них пары сами выбирают 6 — по 3 на каждого
партнёра. Папку <code>Для_учителя</code> не класть.</label></li>
<li><label><input type="checkbox" />На каждом из 8 ноутбуков: открыть
teachablemachine.withgoogle.com → Get Started → Image Project → Standard
image model и оставить вкладку открытой.</label></li>
<li><label><input type="checkbox" />На рабочий стол каждого ноутбука
положить ярлыки «Стенд» и «Секретный_тест» на сетевые
папки.</label></li>
<li><label><input type="checkbox" />Вписать путь к сетевой папке в
подсказку П2 — на случай, если ярлык не сработает.</label></li>
<li><label><input type="checkbox" />Открыть <code>slajdy.html</code> на
проекторе, нажать F.</label></li>
</ul>
<h2 id="без-прогона-что-уже-подстраховано">Без прогона: что уже
подстраховано</h2>
<p>Отдельного прогона не нужно — урок не зависит от того, что не
проверено заранее:</p>
<table>
<thead>
<tr class="header">
<th>Непроверенное</th>
<th>Как подстраховано</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>Сработают ли ловушки</td>
<td>Какие картинки — ловушки, уже написано в
<code>Для_учителя/ключ_к_тесту.txt</code> — держать его открытым на
своём ноутбуке. Если пара ловушек не нашла или модель на них не ошиблась
— П8. Вывод урока держится и без ловушек: сложность видна на этапе
«Масштаб».</td>
</tr>
<tr class="even">
<td>Сколько эпох стоит по умолчанию</td>
<td>Дети записывают число сами (пункт 1 этапа 2); в таблице строка этапа
1 без готового числа.</td>
</tr>
<tr class="odd">
<td>Показывает ли Under the hood графики</td>
<td>В рабочем листе два пути: есть графики — смотрят на них; нет —
сравнивают строки таблицы. Вмешиваться не нужно.</td>
</tr>
<tr class="even">
<td>Сколько займёт тест</td>
<td>Заложено с запасом: 40 секунд на картинку и 3 минуты резерва в
конце.</td>
</tr>
<tr class="odd">
<td>Откроется ли сетевая папка через ярлык</td>
<td>Подсказка П2 с путём; крайний случай — см. «Риски».</td>
</tr>
</tbody>
</table>
<p><strong>Если при подготовке ноутбуков найдутся 3 минуты</strong> (вы
всё равно открываете Teachable Machine на каждом): на первом ноутбуке
загрузите «Стенд» через ярлык и нажмите Train Model. Так вы заодно
проверите сетевую папку и узнаете время обучения — на случай, если
Teachable Machine на уроке не загрузится.</p>
<h2 id="ход-урока-по-минутам">Ход урока по минутам</h2>
<p>Учитель не говорит: только переключает слайды, раздаёт материалы,
кладёт подсказки и следит за шумом. Слайд меняется по времени или когда
зелёные карточки у всех четырёх пар — что наступит раньше. Каждый ученик
работает за своим ноутбуком, но в паре: оба обучают одну и ту же модель
и делят проверку.</p>
<table>
<thead>
<tr class="header">
<th>Минута</th>
<th>Слайд</th>
<th>Учитель делает</th>
<th>Следить за</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>0–0,5</td>
<td>1. Титул</td>
<td>Ничего, ученики садятся</td>
<td>У всех ли на столе лист, карточки, конверт</td>
</tr>
<tr class="even">
<td>0,5–1,5</td>
<td>2. Правила (40 с), 3. Мостик (30 с)</td>
<td>Переключать по времени</td>
<td>Поняли ли красную и зелёную карточки</td>
</tr>
<tr class="odd">
<td>1,5–2,5</td>
<td>4. Гипотеза</td>
<td>—</td>
<td>Числа записаны до работы на ноутбуках</td>
</tr>
<tr class="even">
<td>2,5–8</td>
<td>5. Обучите модель</td>
<td>Подсказки П1–П4 по красным карточкам</td>
<td>Оба партнёра обучают модель, никто не ждёт</td>
</tr>
<tr class="odd">
<td>8–12</td>
<td>6. Секретный тест</td>
<td>Включить, когда обучили две пары; П8 при 6 из 6; челлендж
быстрым</td>
<td>Каждый партнёр сам выбирает 3 картинки из 10 — выбор и есть
гипотеза. Не подсказывать, какие брать, и не подсказывать про цвет: это
момент открытия</td>
</tr>
<tr class="even">
<td>12–19</td>
<td>7. Под капотом</td>
<td>П5 по запросу</td>
<td>Партнёр 1 — 1 эпоха, партнёр 2 — 10 эпох, одновременно; проверяют по
2 картинки; конверты закрыты</td>
</tr>
<tr class="odd">
<td>19–20,5</td>
<td>8. Откройте конверт</td>
<td>—</td>
<td>Пункт 5 листа: сравнение своих слов с терминами</td>
</tr>
<tr class="even">
<td>20,5–27</td>
<td>9. Масштаб</td>
<td>Раздать досье; П6, П7</td>
<td>Числа берут из английского столбца</td>
</tr>
<tr class="odd">
<td>27–28</td>
<td>10. Сверка</td>
<td>Ровно одна минута</td>
<td>Порядок величины у всех один — миллионы раз</td>
</tr>
<tr class="even">
<td>28–34</td>
<td>11. Смета</td>
<td>Раздать заказчиков и бланки</td>
<td>Готовая пара кладёт бланк на рабочий лист и поднимает зелёную
карточку</td>
</tr>
<tr class="odd">
<td>34–37</td>
<td>12. Билет</td>
<td>Раздать билеты, собрать на выходе</td>
<td>Пишут молча и каждый сам</td>
</tr>
<tr class="even">
<td>37</td>
<td>13. Главная мысль</td>
<td>Показать после сдачи билетов, чтобы не стал подсказкой</td>
<td>—</td>
</tr>
<tr class="odd">
<td>37–40</td>
<td>—</td>
<td><strong>Резерв 3 минуты</strong></td>
<td>Съедается задержками по ходу урока. Если не съелся — урок спокойно
заканчивается раньше.</td>
</tr>
</tbody>
</table>
<p><strong>Если всё равно отстаём</strong> — выбрасывать по порядку,
каждый пункт возвращает около минуты, цель урока не страдает:</p>
<ol type="1">
<li>Слайд 10 «Сверка» — сразу к смете.</li>
<li>На этапе «Под капотом» проверять по одной картинке вместо двух.</li>
<li>В смете заполнить только первые три строки бланка и вердикт.</li>
</ol>
<h2 id="ожидаемые-ответы">Ожидаемые ответы</h2>
<p>Главный вывод: модель различает <strong>цвет</strong>, а не технику,
— а чтобы научить машину по-настоящему видеть и рисовать стиль, нужны на
порядки больше данных и вычислений.</p>
<h3 id="стенд-и-под-капотом">Стенд и «Под капотом»</h3>
<table>
<thead>
<tr class="header">
<th>Вопрос</th>
<th>Ожидаемый ответ</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>Где модель ошиблась</td>
<td>Скорее всего на ловушках: цветной карандаш — «акварель», монохромная
размывка — «карандаш». Какие файлы ловушки — в ключе. Это прогноз:
модель может ошибиться и на других картинках, любой разбор ошибки
засчитывать.</td>
</tr>
<tr class="even">
<td>По какому признаку она различает</td>
<td>Цветное или серое. Возможны и другие «подсказки»: тон бумаги, рамка,
штриховка. Любой такой ответ засчитывать.</td>
</tr>
<tr class="odd">
<td>Epochs по умолчанию</td>
<td>Обычно 50; дети записывают число сами</td>
</tr>
<tr class="even">
<td>Время при 1 / 10 эпохах и по умолчанию</td>
<td>Растёт примерно пропорционально числу эпох. Время для числа по
умолчанию берут из этапа 1 — заново не обучают.</td>
</tr>
<tr class="odd">
<td>Что растёт и что падает в Under the hood</td>
<td>Растёт точность (accuracy), падает ошибка (loss)</td>
</tr>
<tr class="even">
<td>Свои названия</td>
<td>Эпоха — «круг», «проход», «повтор». Ошибка — «штраф», «промахи».
Выборка — «учебник», «база примеров». Тест — «экзамен», «проверка».
Засчитывать любое по смыслу.</td>
</tr>
</tbody>
</table>
<h3 id="масштаб">Масштаб</h3>
<table>
<thead>
<tr class="header">
<th>Строка лестницы</th>
<th>Картинок</th>
<th>Время</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>Наш стенд</td>
<td>около 100</td>
<td>секунды (своё у каждой пары)</td>
</tr>
<tr class="even">
<td>Модель-художник (карточка Б)</td>
<td>30</td>
<td>около 37 минут = 2220 с</td>
</tr>
<tr class="odd">
<td>Генератор с нуля (карточки В, Г)</td>
<td>2,32 млрд</td>
<td>150 000 ч = 540 000 000 с</td>
</tr>
</tbody>
</table>
<ul>
<li>Во сколько раз дольше: 540 000 000 ÷ время стенда (при 10 с — 54 млн
раз).</li>
<li>Во сколько раз больше картинок: 2 320 000 000 ÷ 100 ≈ 23 млн
раз.</li>
<li>Почему стенд учится секунды (карточка А): внутри готовая модель,
которую уже учили на миллионах картинок ImageNet; стенд её только
доучивает.</li>
<li>Оговорка для сильных: 150 000 часов — серверные видеокарты, а стенд
— ноутбук; сравнение показывает порядок величины, а не точное отношение.
И это сумма по 256 видеокартам: календарно — около 24 дней.</li>
</ul>
<h3 id="сметы">Сметы</h3>
<table>
<thead>
<tr class="header">
<th>Заказчик</th>
<th>Как учить</th>
<th>Данные</th>
<th>Красный флаг</th>
<th>Вердикт</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>1. Художница, 40 своих акварелей</td>
<td>Дообучить готовый генератор</td>
<td>Свои работы — можно</td>
<td>Мало разнообразия → переобучение; кто получит доступ к модели с её
стилем</td>
<td>Берёмся</td>
</tr>
<tr class="even">
<td>2. Музей, передвижники</td>
<td>Дообучить готовый генератор, сотни картин</td>
<td>Срок охраны в России — жизнь автора + 70 лет; у передвижников он
истёк</td>
<td>Брать сканы из открытых коллекций; подписывать работы как созданные
ИИ, чтобы не путали с настоящими</td>
<td>Берёмся с условием</td>
</tr>
<tr class="odd">
<td>3. Блогер, 30 чужих иллюстраций</td>
<td>Технически как карточка Б — около часа</td>
<td>Работы современного автора защищены правом</td>
<td>Копирование чужого стиля без разрешения, риск выдать за чужое</td>
<td>Отказываемся или только с разрешения автора</td>
</tr>
<tr class="even">
<td>4. Стартап с нуля, 1 млн ₽</td>
<td>С нуля невозможно</td>
<td>Миллиарды картинок, права на них не проверить</td>
<td>150 000 ч × 150 ₽ = 22,5 млн ₽ только на видеокарты</td>
<td>Отказываемся; предложить дообучить готовую открытую модель</td>
</tr>
</tbody>
</table>
<p>Цена 150 ₽ за час видеокарты — условие задачи, не реальный тариф; в
раздатке это подписано.</p>
<h2 id="риски-и-что-делать">Риски и что делать</h2>
<table>
<thead>
<tr class="header">
<th>Если…</th>
<th>То…</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>Модель угадала все 6, ловушки не сработали</td>
<td>П8: пара ищет картинку с наименьшей уверенностью. Вывод урока не
страдает — сложность всё равно видна на этапе «Масштаб».</td>
</tr>
<tr class="even">
<td>Under the hood не показывает графиков</td>
<td>Ничего не делать: в рабочем листе есть запасной путь — сравнить
строки таблицы.</td>
</tr>
<tr class="odd">
<td>Пара не успевает к 12-й минуте</td>
<td>Молча показать на таблицу: достаточно 4 картинок, если среди них
есть ловушки.</td>
</tr>
<tr class="even">
<td>Пара не выбрала ни одной ловушки, и модель угадала всё</td>
<td>Это тоже результат: П8, затем молча положить рядом номер одной
ловушки из ключа (написать на листке).</td>
</tr>
<tr class="odd">
<td>Пара закончила этап раньше</td>
<td>Карточка-челлендж. «Отравитель» и «Где мои данные?» — самые полезные
для темы ИБ.</td>
</tr>
<tr class="even">
<td>Сетевая папка не открывается</td>
<td>Скопировать <code>Стенд</code> и <code>Секретный_тест</code> на
рабочие столы ноутбуков заранее или раздать на флешке.</td>
</tr>
<tr class="odd">
<td>Teachable Machine не грузится</td>
<td>Урок держится на этапах «Масштаб» и «Смета»: пары работают с досье.
Время стенда — ваше, если успели обучить модель при подготовке, иначе
пусть берут «около 10 секунд» из слайда сверки.</td>
</tr>
<tr class="even">
<td>Шумно</td>
<td>Встать перед классом и поднять ладонь — пары затихают по примеру
друг друга. Если такой знак не принят в классе, договориться о нём до
урока.</td>
</tr>
<tr class="odd">
<td>Ученик открыл конверт раньше</td>
<td>Не страшно: молча показать на пункт 4 этапа «Под капотом» — пусть
всё равно запишут свои слова.</td>
</tr>
</tbody>
</table>
<h2 id="источники-чисел-из-досье">Источники чисел из досье</h2>
<ul>
<li>А — Google, курс <a
href="https://codelabs.developers.google.com/codelabs/tensorflowjs-teachablemachine-codelab">TensorFlow.js:
Make your own “Teachable Machine” using transfer learning</a></li>
<li>Б — <a
href="https://huggingface.co/stephenbtl/marginalia-drolleries-klein-4b-lora">Medieval
Marginalia — FLUX.2 [klein] LoRA</a>, Hugging Face</li>
<li>В — карточка модели <a
href="https://huggingface.co/CompVis/stable-diffusion-v1-4">Stable
Diffusion v1-4</a></li>
<li>Г — статья <a href="https://arxiv.org/abs/2210.08402">LAION-5B: An
open large-scale dataset for training next generation image-text
models</a></li>
<li>Для учителя: Teachable Machine учит модель прямо в браузере,
картинки не уходят на серверы, пока проект не сохранён в Google Drive —
<a href="https://teachablemachine.withgoogle.com/faq">FAQ Teachable
Machine</a></li>
</ul>
</main>
</body>
</html>

===== КОНЕЦ ФАЙЛА: 8-klass/snachala-obuchi/pamyatka.html =====

===== ФАЙЛ: 5-klass/iiib-06-kompyuternoe-zrenie/slajdy.html =====
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>Компьютерное зрение, или как видят компьютеры — 5 класс</title>
<style>
  :root{
    --paper:#F7F6F2; --ink:#17181A; --muted:#5F6066;
    --accent:#E8442A; --line:#DCD9D1;
  }
  *{box-sizing:border-box;}
  html,body{margin:0;padding:0;height:100%;background:#0E0F11;overflow:hidden;
    font-family:"PT Sans","Segoe UI",Arial,Helvetica,sans-serif;-webkit-font-smoothing:antialiased;}
  #stage{position:absolute;left:50%;top:50%;width:1280px;height:720px;
    transform:translate(-50%,-50%);transform-origin:50% 50%;}
  .slide{position:absolute;inset:0;width:1280px;height:720px;padding:44px 60px;
    background:var(--paper);color:var(--ink);display:none;flex-direction:column;
    overflow:hidden;user-select:none;}
  .slide.on{display:flex;}
  .mid{justify-content:center;}
  .inv{--paper:#141518;--ink:#F7F6F2;--muted:#A6A7AD;--line:#3B3C42;background:#141518;}
  h1,h2,p{margin:0;font-weight:400;}
  .h{font-size:48px;line-height:1.06;font-weight:800;letter-spacing:-.6px;margin-bottom:16px;}
  .lead{font-size:34px;line-height:1.22;font-weight:700;}
  .t{font-size:28px;line-height:1.32;}
  .t+.t{margin-top:14px;}
  .note{font-size:26px;line-height:1.3;color:var(--muted);}
  .big{font-size:54px;line-height:1.1;font-weight:800;letter-spacing:-1px;}
  .acc{color:var(--accent);}
  .k{color:var(--accent);font-weight:800;}
  .cols{display:flex;gap:30px;align-items:flex-start;}
  .card{background:#fff;border:2px solid var(--line);border-radius:16px;padding:16px 20px;}
  .inv .card{background:#1D1E22;}
  .lang{font-size:28px;line-height:1.28;background:#fff;border-left:8px solid var(--accent);
    border-radius:10px;padding:12px 18px;}
  .inv .lang{background:#1D1E22;}
  .lang b{color:var(--accent);}
  svg{display:block;overflow:visible;}
  svg text{font-family:"PT Sans","Segoe UI",Arial,sans-serif;font-weight:700;}
  #cnt{position:absolute;right:20px;bottom:10px;font-size:20px;font-weight:700;
    color:#fff;mix-blend-mode:difference;letter-spacing:1px;}
</style>
</head>
<body>
<div id="stage">

<!-- 1 -->
<section class="slide mid on">
  <h1 class="big" style="font-size:62px;line-height:1.06;margin-bottom:8px;">Компьютерное зрение,<br>или как видят компьютеры</h1>
  <div style="display:flex;align-items:center;gap:16px;margin:16px 0 4px;">
    <span style="background:var(--accent);color:#fff;font-size:26px;font-weight:800;padding:6px 20px;border-radius:999px;">5 класс</span>
    <span class="note">урок информатики</span>
  </div>
  <svg viewBox="0 0 940 300" width="940" height="300" role="img" aria-label="Глаз превращается в пиксельную сетку">
    <defs>
      <pattern id="pxg" x="520" y="30" width="30" height="30" patternUnits="userSpaceOnUse">
        <rect width="26" height="26" fill="#D7DFE9"/>
      </pattern>
    </defs>
    <path d="M30 150 C90 62 270 62 330 150 C270 238 90 238 30 150 Z" fill="#FFFFFF" stroke="#17181A" stroke-width="6"/>
    <circle cx="180" cy="150" r="64" fill="#E8442A"/>
    <circle cx="180" cy="150" r="28" fill="#17181A"/>
    <circle cx="160" cy="130" r="13" fill="#FFFFFF"/>
    <line x1="112" y1="92" x2="100" y2="68" stroke="#17181A" stroke-width="6" stroke-linecap="round"/>
    <line x1="180" y1="74" x2="180" y2="48" stroke="#17181A" stroke-width="6" stroke-linecap="round"/>
    <line x1="248" y1="92" x2="260" y2="68" stroke="#17181A" stroke-width="6" stroke-linecap="round"/>
    <line x1="372" y1="150" x2="448" y2="150" stroke="#17181A" stroke-width="7" stroke-linecap="round"/>
    <polygon points="448,137 474,150 448,163" fill="#17181A"/>
    <rect x="640" y="30" width="120" height="30" fill="url(#pxg)"/>
    <rect x="580" y="60" width="240" height="30" fill="url(#pxg)"/>
    <rect x="550" y="90" width="300" height="30" fill="url(#pxg)"/>
    <rect x="520" y="120" width="360" height="30" fill="url(#pxg)"/>
    <rect x="520" y="150" width="360" height="30" fill="url(#pxg)"/>
    <rect x="550" y="180" width="300" height="30" fill="url(#pxg)"/>
    <rect x="580" y="210" width="240" height="30" fill="url(#pxg)"/>
    <rect x="640" y="240" width="120" height="30" fill="url(#pxg)"/>
    <g fill="#E8442A">
      <rect x="612" y="122" width="26" height="26"/><rect x="612" y="152" width="26" height="26"/><rect x="612" y="182" width="26" height="26"/>
      <rect x="762" y="122" width="26" height="26"/><rect x="762" y="152" width="26" height="26"/><rect x="762" y="182" width="26" height="26"/>
      <rect x="642" y="92" width="26" height="26"/><rect x="672" y="92" width="26" height="26"/>
      <rect x="702" y="92" width="26" height="26"/><rect x="732" y="92" width="26" height="26"/>
      <rect x="642" y="182" width="26" height="26"/><rect x="672" y="182" width="26" height="26"/>
      <rect x="702" y="182" width="26" height="26"/><rect x="732" y="182" width="26" height="26"/>
      <rect x="642" y="122" width="26" height="26"/><rect x="732" y="122" width="26" height="26"/>
      <rect x="642" y="152" width="26" height="26"/><rect x="732" y="152" width="26" height="26"/>
    </g>
    <g fill="#17181A">
      <rect x="672" y="122" width="26" height="26"/><rect x="702" y="122" width="26" height="26"/>
      <rect x="672" y="152" width="26" height="26"/><rect x="702" y="152" width="26" height="26"/>
    </g>
    <text x="180" y="292" font-size="22" fill="#5F6066" text-anchor="middle">так видит человек</text>
    <text x="700" y="292" font-size="22" fill="#5F6066" text-anchor="middle">так «видит» компьютер</text>
  </svg>
</section>

<!-- 2 -->
<section class="slide mid">
  <h2 class="h" style="margin-bottom:28px;">Технологии ИИ: четыре умения</h2>
  <div style="display:flex;gap:22px;">
    <div class="card" style="flex:1;text-align:center;padding:22px 10px 26px;">
      <svg viewBox="0 0 200 180" width="200" height="180" style="margin:0 auto;">
        <circle cx="88" cy="74" r="58" fill="none" stroke="#E8442A" stroke-width="10"/>
        <path d="M52 74 C66 52 110 52 124 74 C110 96 66 96 52 74 Z" fill="#17181A"/>
        <circle cx="88" cy="74" r="11" fill="#F7F6F2"/>
        <line x1="130" y1="116" x2="176" y2="162" stroke="#E8442A" stroke-width="13" stroke-linecap="round"/>
      </svg>
      <div style="font-size:34px;font-weight:800;line-height:1.1;margin-top:8px;">Распознавать</div>
    </div>
    <div class="card" style="flex:1;text-align:center;padding:22px 10px 26px;">
      <svg viewBox="0 0 200 180" width="200" height="180" style="margin:0 auto;">
        <rect x="50" y="6" width="100" height="46" rx="10" fill="none" stroke="#17181A" stroke-width="4"/>
        <text x="100" y="37" font-size="24" fill="#17181A" text-anchor="middle">если</text>
        <line x1="72" y1="52" x2="48" y2="92" stroke="#17181A" stroke-width="4"/>
        <line x1="128" y1="52" x2="152" y2="92" stroke="#17181A" stroke-width="4"/>
        <polygon points="48,100 38,86 58,86" fill="#17181A"/>
        <polygon points="152,100 142,86 162,86" fill="#17181A"/>
        <rect x="6" y="102" width="84" height="46" rx="10" fill="#E8442A"/>
        <text x="48" y="133" font-size="24" fill="#FFFFFF" text-anchor="middle">то</text>
        <rect x="110" y="102" width="84" height="46" rx="10" fill="none" stroke="#17181A" stroke-width="4"/>
        <text x="152" y="133" font-size="24" fill="#17181A" text-anchor="middle">то</text>
      </svg>
      <div style="font-size:34px;font-weight:800;line-height:1.1;margin-top:8px;">Размышлять<br>по правилам</div>
    </div>
    <div class="card" style="flex:1;text-align:center;padding:22px 10px 26px;">
      <svg viewBox="0 0 200 180" width="200" height="180" style="margin:0 auto;">
        <path d="M16 162 L58 118 L104 132 L150 60" fill="none" stroke="#17181A" stroke-width="5"
              stroke-dasharray="13 10" stroke-linecap="round"/>
        <circle cx="16" cy="162" r="10" fill="#E8442A"/>
        <circle cx="58" cy="118" r="8" fill="#17181A"/>
        <circle cx="104" cy="132" r="8" fill="#17181A"/>
        <line x1="150" y1="60" x2="150" y2="16" stroke="#17181A" stroke-width="5"/>
        <polygon points="150,10 188,26 150,44" fill="#E8442A"/>
      </svg>
      <div style="font-size:34px;font-weight:800;line-height:1.1;margin-top:8px;">Планировать</div>
    </div>
    <div class="card" style="flex:1;text-align:center;padding:22px 10px 26px;">
      <svg viewBox="0 0 200 180" width="200" height="180" style="margin:0 auto;">
        <polygon points="80,8 97.6,55.7 148.5,57.8 108.5,89.3 122.3,138.3 80,110 37.7,138.3 51.5,89.3 11.5,57.8 62.4,55.7" fill="#E8442A"/>
        <line x1="118" y1="156" x2="168" y2="106" stroke="#17181A" stroke-width="11" stroke-linecap="round"/>
        <path d="M168 106 L188 86 L160 80 Z" fill="#17181A"/>
      </svg>
      <div style="font-size:34px;font-weight:800;line-height:1.1;margin-top:8px;">Создавать<br>новое</div>
    </div>
  </div>
</section>

<!-- 3 -->
<section class="slide">
  <h2 class="h">Распознавать — ИИ «узнаёт»</h2>
  <div class="cols">
    <div style="width:730px;flex:none;">
      <p class="t">Лицо в телефоне, голос в колонке, номер машины на парковке, рукописный текст, движения и жесты.</p>
      <p class="t">Сюда же — предсказания: прогноз погоды, пробки — это распознавание закономерностей в данных; и рекомендации: лента в приложениях.</p>
    </div>
    <div style="flex:1;min-width:0;">
      <svg viewBox="0 0 380 320" width="380" height="320" role="img" aria-label="Четыре примера распознавания">
        <g>
          <rect x="40" y="8" width="110" height="88" rx="10" fill="#FFFFFF" stroke="#17181A" stroke-width="4"/>
          <circle cx="95" cy="44" r="19" fill="none" stroke="#E8442A" stroke-width="4"/>
          <circle cx="88" cy="40" r="3.5" fill="#17181A"/><circle cx="102" cy="40" r="3.5" fill="#17181A"/>
          <path d="M86 52 Q95 59 104 52" fill="none" stroke="#17181A" stroke-width="3.5" stroke-linecap="round"/>
          <text x="95" y="124" font-size="20" fill="#5F6066" text-anchor="middle">лицо</text>
        </g>
        <g transform="translate(190,0)">
          <g fill="#E8442A">
            <rect x="56" y="36" width="8" height="32" rx="4"/><rect x="72" y="22" width="8" height="60" rx="4"/>
            <rect x="88" y="8" width="8" height="88" rx="4"/><rect x="104" y="28" width="8" height="48" rx="4"/>
            <rect x="120" y="16" width="8" height="72" rx="4"/><rect x="136" y="40" width="8" height="24" rx="4"/>
          </g>
          <text x="100" y="124" font-size="20" fill="#5F6066" text-anchor="middle">голос</text>
        </g>
        <g transform="translate(0,170)">
          <rect x="24" y="40" width="140" height="44" rx="8" fill="#FFFFFF" stroke="#17181A" stroke-width="4"/>
          <text x="94" y="70" font-size="22" fill="#17181A" text-anchor="middle">А 123 ВС</text>
          <text x="94" y="124" font-size="20" fill="#5F6066" text-anchor="middle">номер</text>
        </g>
        <g transform="translate(190,170)">
          <rect x="52" y="50" width="84" height="46" rx="16" fill="#FFFFFF" stroke="#17181A" stroke-width="4"/>
          <g fill="#FFFFFF" stroke="#17181A" stroke-width="4">
            <rect x="56" y="28" width="15" height="30" rx="7"/><rect x="75" y="20" width="15" height="38" rx="7"/>
            <rect x="94" y="22" width="15" height="36" rx="7"/><rect x="113" y="30" width="15" height="28" rx="7"/>
          </g>
          <rect x="30" y="56" width="24" height="14" rx="7" fill="#FFFFFF" stroke="#17181A" stroke-width="4"/>
          <text x="94" y="124" font-size="20" fill="#5F6066" text-anchor="middle">жест</text>
        </g>
      </svg>
    </div>
  </div>
  <div style="display:flex;gap:24px;margin-top:16px;">
    <div class="lang" style="flex:1;"><b>Python</b> — главный язык ИИ сегодня</div>
    <div class="lang" style="flex:1.4;"><b>Julia</b> — сверхбыстрые научные расчёты: моделирование лекарств, климата</div>
  </div>
</section>

<!-- 4 -->
<section class="slide">
  <h2 class="h">Размышлять по правилам — ИИ «советует»</h2>
  <div class="cols" style="align-items:center;">
    <div style="width:620px;flex:none;">
      <p class="t">По правилам «если — то»: медицинский диагноз, оценка ситуации.</p>
      <p class="t">Может строить новые логические правила на основе старых — это и есть рассуждение.</p>
    </div>
    <div style="flex:1;min-width:0;">
      <svg viewBox="0 0 460 280" width="460" height="280" role="img" aria-label="Блок-схема если — то">
        <rect x="140" y="10" width="180" height="58" rx="12" fill="#FFFFFF" stroke="#17181A" stroke-width="4"/>
        <text x="230" y="48" font-size="24" fill="#17181A" text-anchor="middle">если</text>
        <line x1="190" y1="68" x2="110" y2="120" stroke="#17181A" stroke-width="4"/>
        <line x1="270" y1="68" x2="350" y2="120" stroke="#17181A" stroke-width="4"/>
        <polygon points="108,130 90,110 126,110" fill="#17181A"/>
        <polygon points="352,130 334,110 370,110" fill="#17181A"/>
        <rect x="10" y="132" width="200" height="60" rx="12" fill="#E8442A"/>
        <text x="110" y="170" font-size="24" fill="#FFFFFF" text-anchor="middle">то: диагноз</text>
        <rect x="250" y="132" width="200" height="60" rx="12" fill="#FFFFFF" stroke="#17181A" stroke-width="4"/>
        <text x="350" y="170" font-size="24" fill="#17181A" text-anchor="middle">то: оценка</text>
        <line x1="110" y1="192" x2="110" y2="222" stroke="#E8442A" stroke-width="4" stroke-dasharray="8 8"/>
        <line x1="350" y1="192" x2="350" y2="222" stroke="#E8442A" stroke-width="4" stroke-dasharray="8 8"/>
        <rect x="10" y="224" width="200" height="48" rx="12" fill="none" stroke="#E8442A" stroke-width="4" stroke-dasharray="9 7"/>
        <text x="110" y="255" font-size="22" fill="#E8442A" text-anchor="middle">новое правило</text>
        <rect x="250" y="224" width="200" height="48" rx="12" fill="none" stroke="#E8442A" stroke-width="4" stroke-dasharray="9 7"/>
        <text x="350" y="255" font-size="22" fill="#E8442A" text-anchor="middle">новое правило</text>
      </svg>
    </div>
  </div>
  <div style="margin-top:18px;display:flex;flex-direction:column;gap:10px;">
    <div class="lang"><b>LISP</b> — исторический язык ИИ, на нём строили «рассуждающие» программы</div>
    <div class="lang"><b>Prolog</b> — язык экспертных систем: программа отвечает через цепочки «если — то»</div>
    <div class="lang"><b>Haskell</b> — язык строгих правил: ошибка почти невозможна, поэтому его берут банки</div>
  </div>
  <p class="note" style="margin-top:14px;">На Python вы однажды напишете своего ИИ сами.</p>
</section>

<!-- 5 -->
<section class="slide">
  <h2 class="h">Планировать</h2>
  <p class="t">Маршрут в Яндекс.Картах, действия робота, ходы игровых ботов.</p>
  <p class="t">Игра — тоже планирование: бот не нажимает кнопку «сейчас», а просчитывает много ходов вперёд.</p>
  <p class="t">Считают маршруты и игровых ботов чаще всего на <span class="k">Python</span>; исторически планирование писали и на <span class="k">Prolog</span>.</p>
  <div style="display:flex;gap:30px;margin-top:18px;align-items:flex-start;">
    <svg viewBox="0 0 590 270" width="590" height="270" role="img" aria-label="Карта с маршрутом">
      <rect x="4" y="4" width="582" height="262" rx="18" fill="#EDEAE3"/>
      <g stroke="#FFFFFF" stroke-width="22" stroke-linecap="round" fill="none">
        <path d="M20 200 H570"/><path d="M150 20 V250"/><path d="M420 20 V250"/><path d="M20 90 H570"/>
      </g>
      <g stroke="#D9D4C8" stroke-width="6" fill="none" stroke-dasharray="14 12">
        <path d="M50 240 L50 90 L150 90 L150 40 L420 40 L420 200 L530 200"/>
        <path d="M50 240 L150 240 L150 150 L300 150 L300 90 L420 90 L420 60"/>
      </g>
      <path d="M50 240 L150 240 L150 90 L300 90 L300 40 L530 40" fill="none"
            stroke="#E8442A" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="18 12"/>
      <circle cx="50" cy="240" r="13" fill="#17181A"/>
      <line x1="530" y1="40" x2="530" y2="4" stroke="#17181A" stroke-width="6"/>
      <polygon points="530,0 568,16 530,32" fill="#E8442A"/>
      <text x="24" y="40" font-size="22" fill="#5F6066">старт</text>
      <text x="460" y="260" font-size="22" fill="#5F6066">финиш</text>
    </svg>
    <svg viewBox="0 0 470 270" width="470" height="270" role="img" aria-label="Шахматная доска с просчитанными ходами">
      <rect x="10" y="10" width="230" height="230" fill="#F0EDE6" stroke="#17181A" stroke-width="4"/>
      <g fill="#17181A" opacity=".14">
        <rect x="68" y="10" width="28" height="28"/><rect x="124" y="10" width="28" height="28"/><rect x="180" y="10" width="28" height="28"/>
        <rect x="40" y="38" width="28" height="28"/><rect x="96" y="38" width="28" height="28"/><rect x="152" y="38" width="28" height="28"/><rect x="208" y="38" width="28" height="28"/>
        <rect x="68" y="66" width="28" height="28"/><rect x="124" y="66" width="28" height="28"/><rect x="180" y="66" width="28" height="28"/>
        <rect x="40" y="94" width="28" height="28"/><rect x="96" y="94" width="28" height="28"/><rect x="152" y="94" width="28" height="28"/><rect x="208" y="94" width="28" height="28"/>
        <rect x="68" y="122" width="28" height="28"/><rect x="124" y="122" width="28" height="28"/><rect x="180" y="122" width="28" height="28"/>
        <rect x="40" y="150" width="28" height="28"/><rect x="96" y="150" width="28" height="28"/><rect x="152" y="150" width="28" height="28"/><rect x="208" y="150" width="28" height="28"/>
        <rect x="68" y="178" width="28" height="28"/><rect x="124" y="178" width="28" height="28"/><rect x="180" y="178" width="28" height="28"/>
        <rect x="40" y="206" width="28" height="28"/><rect x="96" y="206" width="28" height="28"/><rect x="152" y="206" width="28" height="28"/><rect x="208" y="206" width="28" height="28"/>
      </g>
      <g fill="#E8442A" opacity=".85">
        <rect x="96" y="38" width="28" height="28"/><rect x="152" y="66" width="28" height="28"/>
        <rect x="68" y="94" width="28" height="28"/><rect x="124" y="150" width="28" height="28"/>
        <rect x="180" y="178" width="28" height="28"/>
      </g>
      <circle cx="124" cy="122" r="13" fill="#17181A"/>
      <path d="M124 122 L110 108 M124 122 L138 136" stroke="#E8442A" stroke-width="5" stroke-linecap="round"/>
      <text x="260" y="64" font-size="22" fill="#5F6066">просчитанные</text>
      <text x="260" y="92" font-size="22" fill="#5F6066">ходы бота</text>
      <rect x="258" y="112" width="24" height="24" fill="#E8442A" opacity=".85"/>
      <text x="292" y="132" font-size="22" fill="#5F6066">— варианты</text>
      <circle cx="270" cy="180" r="13" fill="#17181A"/>
      <text x="292" y="188" font-size="22" fill="#5F6066">— фигура</text>
    </svg>
  </div>
</section>

<!-- 6 -->
<section class="slide">
  <h2 class="h">Создавать новое — ИИ «генерирует»</h2>
  <div class="cols">
    <div style="width:620px;flex:none;">
      <p class="t">Тексты, картинки, музыка, видео — новое на основе того, что модель видела в данных (Kandinsky, Шедеврум — вы их знаете).</p>
      <p class="t">И реальные объекты: программа-проектировщик строит конструкцию по правилам и данным, 3D-принтер печатает её металлом.</p>
      <p class="t" style="margin-top:16px;font-size:30px;font-weight:800;">Ракетный двигатель на <span class="k">200 кН</span>, напечатанный за <span class="k">354 часа</span>.</p>
      <p class="note" style="margin-top:12px;">Строго говоря, это не совсем ИИ — но показывает горизонт: компьютеры сами проектируют, сами печатают.</p>
      <p class="t" style="margin-top:10px;">Генерация картинок и текстов — снова <span class="k">Python</span>.</p>
    </div>
    <div style="flex:1;min-width:0;">
      <svg viewBox="0 0 480 440" width="480" height="440" role="img" aria-label="Экран с текстом и картинкой и 3D-принтер">
        <rect x="10" y="10" width="290" height="190" rx="14" fill="#FFFFFF" stroke="#17181A" stroke-width="5"/>
        <g fill="#17181A" opacity=".75">
          <rect x="28" y="32" width="150" height="10" rx="5"/><rect x="28" y="52" width="200" height="10" rx="5"/>
          <rect x="28" y="72" width="120" height="10" rx="5"/>
        </g>
        <rect x="28" y="96" width="110" height="80" rx="8" fill="#E8442A"/>
        <path d="M32 176 L66 136 L94 168 L110 148 L134 176 Z" fill="#F7F6F2"/>
        <circle cx="108" cy="120" r="11" fill="#F7F6F2"/>
        <rect x="155" y="100" width="120" height="76" rx="8" fill="none" stroke="#17181A" stroke-width="4"/>
        <path d="M165 168 L193 128 L221 162 L240 144 L268 168 Z" fill="#17181A" opacity=".6"/>
        <circle cx="232" cy="128" r="9" fill="#E8442A"/>
        <text x="10" y="230" font-size="22" fill="#5F6066">экран: текст и картинка</text>
        <rect x="30" y="270" width="290" height="22" rx="6" fill="#17181A"/>
        <rect x="120" y="292" width="110" height="18" fill="#17181A"/>
        <rect x="148" y="310" width="54" height="42" rx="6" fill="#E8442A"/>
        <path d="M162 310 L175 330 L188 310" fill="none" stroke="#F7F6F2" stroke-width="5"/>
        <rect x="60" y="352" width="230" height="22" rx="8" fill="#17181A"/>
        <rect x="100" y="374" width="150" height="14" rx="6" fill="#17181A" opacity=".55"/>
        <path d="M90 270 L90 246 L250 246 L250 270" fill="none" stroke="#17181A" stroke-width="6"/>
        <text x="10" y="420" font-size="22" fill="#5F6066">3D-принтер и напечатанная деталь</text>
      </svg>
    </div>
  </div>
</section>

<!-- 7 -->
<section class="slide">
  <h2 class="h">Mark I Perceptron, 1958</h2>
  <div class="cols" style="align-items:center;">
    <div style="width:620px;flex:none;">
      <svg viewBox="0 0 620 420" width="620" height="420" role="img" aria-label="Реконструкция перцептрона: шкаф и матрица фотоэлементов">
        <defs>
          <pattern id="cells" x="0" y="0" width="15" height="15" patternUnits="userSpaceOnUse">
            <circle cx="7.5" cy="7.5" r="5.4" fill="#17181A"/>
          </pattern>
        </defs>
        <rect x="20" y="20" width="170" height="350" rx="10" fill="#FFFFFF" stroke="#17181A" stroke-width="6"/>
        <rect x="38" y="38" width="134" height="90" rx="6" fill="none" stroke="#17181A" stroke-width="4"/>
        <g fill="#17181A">
          <rect x="46" y="48" width="118" height="6" rx="3"/>
          <rect x="46" y="62" width="118" height="6" rx="3"/>
          <rect x="46" y="76" width="118" height="6" rx="3"/>
          <rect x="46" y="90" width="118" height="6" rx="3"/>
          <rect x="46" y="104" width="118" height="6" rx="3"/>
        </g>
        <g fill="none" stroke="#E8442A" stroke-width="5">
          <circle cx="58" cy="160" r="12"/>
          <circle cx="94" cy="160" r="12"/>
          <circle cx="130" cy="160" r="12"/>
          <circle cx="166" cy="160" r="12"/>
        </g>
        <g fill="#E8442A">
          <circle cx="58" cy="160" r="3.5"/>
          <circle cx="94" cy="160" r="3.5"/>
          <circle cx="130" cy="160" r="3.5"/>
          <circle cx="166" cy="160" r="3.5"/>
        </g>
        <rect x="38" y="200" width="134" height="150" rx="6" fill="none" stroke="#17181A" stroke-width="4"/>
        <g stroke="#17181A" stroke-width="3">
          <line x1="46" y1="240" x2="164" y2="240"/>
          <line x1="46" y1="280" x2="164" y2="280"/>
          <line x1="46" y1="320" x2="164" y2="320"/>
        </g>
        <text x="105" y="405" font-size="22" fill="#5F6066" text-anchor="middle">машина-шкаф</text>
        <rect x="250" y="50" width="220" height="220" rx="6" fill="#FFFFFF" stroke="#17181A" stroke-width="6"/>
        <rect x="255" y="55" width="210" height="210" fill="url(#cells)"/>
        <rect x="320" y="270" width="80" height="22" rx="5" fill="#17181A"/>
        <path d="M190 140 C210 120, 230 120, 250 140" fill="none" stroke="#17181A" stroke-width="5"/>
        <path d="M190 220 C210 240, 230 240, 250 220" fill="none" stroke="#17181A" stroke-width="5"/>
        <line x1="190" y1="140" x2="190" y2="220" stroke="#17181A" stroke-width="5"/>
        <rect x="250" y="305" width="220" height="85" rx="10" fill="#FFFFFF" stroke="#17181A" stroke-width="3"/>
        <text x="360" y="340" font-size="19" fill="#E8442A" text-anchor="middle">400 фотоэлементов</text>
        <text x="360" y="370" font-size="19" fill="#5F6066" text-anchor="middle">сетка 20 × 20</text>
      </svg>
    </div>
    <div style="width:480px;flex:none;padding-top:10px;">
      <p class="lead">Первый нейрокомпьютер — создан под распознавание изображений.</p>
      <p class="t" style="margin-top:22px;">Обычные компьютеры исполняют правила, а перцептрон учился на своих ошибках.</p>
    </div>
  </div>
</section>

<!-- 8 -->
<section class="slide">
  <h2 class="h">Перцептрон: для любопытных</h2>
  <div class="cols" style="align-items:center;">
    <div style="width:500px;flex:none;">
      <p style="font-size:24px;line-height:1.4;">400 фотоэлементов вместо процессора; «память» — электромоторчики, поворачивающие ручки потенциометров.</p>
    </div>
    <div style="flex:1;min-width:0;">
      <svg viewBox="0 0 620 320" width="620" height="320" role="img" aria-label="Моторчик и ручка потенциометра">
        <rect x="20" y="90" width="190" height="110" rx="14" fill="#FFFFFF" stroke="#17181A" stroke-width="5"/>
        <rect x="40" y="108" width="60" height="74" rx="6" fill="#17181A" opacity=".18"/>
        <rect x="118" y="108" width="60" height="74" rx="6" fill="#17181A" opacity=".18"/>
        <line x1="210" y1="145" x2="270" y2="145" stroke="#17181A" stroke-width="9"/>
        <circle cx="370" cy="145" r="86" fill="#FFFFFF" stroke="#17181A" stroke-width="6"/>
        <circle cx="370" cy="145" r="60" fill="#EDEAE3" stroke="#17181A" stroke-width="4"/>
        <line x1="370" y1="145" x2="416" y2="99" stroke="#17181A" stroke-width="9" stroke-linecap="round"/>
        <circle cx="370" cy="145" r="10" fill="#17181A"/>
        <path d="M436 101 A 74 74 0 0 1 436 189" fill="none" stroke="#E8442A" stroke-width="8" stroke-linecap="round"/>
        <polygon points="436,191 424,171 450,171" fill="#E8442A"/>
        <text x="115" y="246" font-size="22" fill="#5F6066" text-anchor="middle">моторчик</text>
        <text x="370" y="268" font-size="22" fill="#5F6066" text-anchor="middle">ручка потенциометра</text>
        <text x="520" y="116" font-size="22" fill="#E8442A" text-anchor="middle">поворот</text>
      </svg>
    </div>
  </div>
  <div style="position:absolute;right:60px;top:44px;background:var(--accent);color:#fff;font-size:22px;font-weight:800;padding:8px 18px;border-radius:999px;">для любопытных</div>
</section>

<!-- 9 -->
<section class="slide">
  <h2 class="h">Схема: датчик → кодирование → свёртка</h2>
  <svg viewBox="0 0 1010 320" width="1010" height="320" role="img" aria-label="Камера, матрица цветных пикселей, та же матрица в виде чисел, свёртка находит квадрат 2 на 2, результат">
    <rect x="20" y="110" width="90" height="55" rx="10" fill="#FFFFFF" stroke="#17181A" stroke-width="4"/>
    <circle cx="65" cy="137" r="20" fill="#17181A"/>
    <circle cx="65" cy="137" r="11" fill="#E8442A"/>
    <circle cx="65" cy="137" r="4" fill="#F7F6F2"/>
    <rect x="55" y="100" width="20" height="10" rx="3" fill="#17181A"/>
    <g stroke="#E8442A" stroke-width="4" stroke-linecap="round">
      <line x1="115" y1="125" x2="140" y2="115"/>
      <line x1="115" y1="137" x2="140" y2="137"/>
      <line x1="115" y1="149" x2="140" y2="159"/>
    </g>
    <text x="65" y="200" font-size="20" fill="#5F6066" text-anchor="middle">камера</text>

    <line x1="148" y1="137" x2="170" y2="137" stroke="#17181A" stroke-width="4"/>
    <polygon points="170,128 184,137 170,146" fill="#17181A"/>

    <g>
      <rect x="190" y="70" width="50" height="50" fill="#BFD6EE"/>
      <rect x="240" y="70" width="50" height="50" fill="#BFD6EE"/>
      <rect x="290" y="70" width="50" height="50" fill="#F2C230"/>
      <rect x="340" y="70" width="50" height="50" fill="#F2C230"/>
      <rect x="190" y="120" width="50" height="50" fill="#BFD6EE"/>
      <rect x="240" y="120" width="50" height="50" fill="#BFD6EE"/>
      <rect x="290" y="120" width="50" height="50" fill="#F2C230"/>
      <rect x="340" y="120" width="50" height="50" fill="#F2C230"/>
      <rect x="190" y="170" width="50" height="50" fill="#8FBF7A"/>
      <rect x="240" y="170" width="50" height="50" fill="#8FBF7A"/>
      <rect x="290" y="170" width="50" height="50" fill="#8FBF7A"/>
      <rect x="340" y="170" width="50" height="50" fill="#8FBF7A"/>
      <rect x="190" y="220" width="50" height="50" fill="#4E9A4E"/>
      <rect x="240" y="220" width="50" height="50" fill="#4E9A4E"/>
      <rect x="290" y="220" width="50" height="50" fill="#4E9A4E"/>
      <rect x="340" y="220" width="50" height="50" fill="#4E9A4E"/>
      <rect x="190" y="70" width="200" height="200" fill="none" stroke="#17181A" stroke-width="3"/>
    </g>
    <text x="290" y="298" font-size="20" fill="#5F6066" text-anchor="middle">картинка</text>

    <line x1="395" y1="137" x2="418" y2="137" stroke="#17181A" stroke-width="4"/>
    <polygon points="418,128 432,137 418,146" fill="#17181A"/>

    <g>
      <rect x="440" y="70" width="200" height="200" fill="none" stroke="#17181A" stroke-width="3"/>
      <g stroke="#17181A" stroke-width="1">
        <line x1="490" y1="70" x2="490" y2="270"/>
        <line x1="540" y1="70" x2="540" y2="270"/>
        <line x1="590" y1="70" x2="590" y2="270"/>
        <line x1="440" y1="120" x2="640" y2="120"/>
        <line x1="440" y1="170" x2="640" y2="170"/>
        <line x1="440" y1="220" x2="640" y2="220"/>
      </g>
      <g font-size="20" fill="#17181A" text-anchor="middle">
        <text x="465" y="103">180</text><text x="515" y="103">180</text><text x="565" y="103">240</text><text x="615" y="103">240</text>
        <text x="465" y="153">180</text><text x="515" y="153">180</text><text x="565" y="153">240</text><text x="615" y="153">240</text>
        <text x="465" y="203">120</text><text x="515" y="203">120</text><text x="565" y="203">120</text><text x="615" y="203">120</text>
        <text x="465" y="253">80</text><text x="515" y="253">80</text><text x="565" y="253">80</text><text x="615" y="253">80</text>
      </g>
      <rect x="540" y="70" width="100" height="100" fill="none" stroke="#E8442A" stroke-width="6"/>
    </g>
    <text x="540" y="298" font-size="20" fill="#5F6066" text-anchor="middle">числа</text>

    <line x1="650" y1="170" x2="760" y2="170" stroke="#E8442A" stroke-width="5"/>
    <polygon points="760,158 778,170 760,182" fill="#E8442A"/>
    <text x="705" y="158" font-size="18" fill="#E8442A" text-anchor="middle">свёртка</text>

    <g>
      <rect x="790" y="70" width="50" height="50" fill="#BFD6EE"/>
      <rect x="840" y="70" width="50" height="50" fill="#BFD6EE"/>
      <rect x="890" y="70" width="50" height="50" fill="#F2C230"/>
      <rect x="940" y="70" width="50" height="50" fill="#F2C230"/>
      <rect x="790" y="120" width="50" height="50" fill="#BFD6EE"/>
      <rect x="840" y="120" width="50" height="50" fill="#BFD6EE"/>
      <rect x="890" y="120" width="50" height="50" fill="#F2C230"/>
      <rect x="940" y="120" width="50" height="50" fill="#F2C230"/>
      <rect x="790" y="170" width="50" height="50" fill="#8FBF7A"/>
      <rect x="840" y="170" width="50" height="50" fill="#8FBF7A"/>
      <rect x="890" y="170" width="50" height="50" fill="#8FBF7A"/>
      <rect x="940" y="170" width="50" height="50" fill="#8FBF7A"/>
      <rect x="790" y="220" width="50" height="50" fill="#4E9A4E"/>
      <rect x="840" y="220" width="50" height="50" fill="#4E9A4E"/>
      <rect x="890" y="220" width="50" height="50" fill="#4E9A4E"/>
      <rect x="940" y="220" width="50" height="50" fill="#4E9A4E"/>
      <rect x="790" y="70" width="200" height="200" fill="none" stroke="#17181A" stroke-width="3"/>
      <rect x="890" y="70" width="100" height="100" fill="none" stroke="#E8442A" stroke-width="6"/>
    </g>
    <text x="890" y="298" font-size="20" fill="#5F6066" text-anchor="middle">квадрат 2 × 2</text>
  </svg>
  <p style="font-size:40px;font-weight:800;color:var(--accent);margin-top:10px;">Картинка — это таблица чисел.</p>
  <p style="font-size:28px;margin-top:10px;background:#fff;border-left:8px solid var(--accent);border-radius:10px;padding:10px 18px;">
    Пиксель — одна клетка таблицы, в ней лежит одно число.</p>
</section>

<!-- 10 -->
<section class="slide">
  <h2 class="h">Лупа на пикселях</h2>
  <svg viewBox="0 0 1120 350" width="1120" height="350" role="img" aria-label="Фрагмент картинки и тот же фрагмент под лупой в виде крупных цветных пикселей">
    <rect x="10" y="30" width="280" height="280" rx="10" fill="#BFD6EE" stroke="#17181A" stroke-width="5"/>
    <circle cx="180" cy="120" r="52" fill="#F2C230"/>
    <rect x="10" y="200" width="280" height="110" fill="#8FBF7A"/>
    <text x="150" y="336" font-size="22" fill="#5F6066" text-anchor="middle">картинка</text>

    <line x1="310" y1="170" x2="390" y2="170" stroke="#17181A" stroke-width="6"/>
    <polygon points="390,156 418,170 390,184" fill="#17181A"/>
    <text x="360" y="145" font-size="22" fill="#5F6066" text-anchor="middle">лупа</text>

    <defs>
      <clipPath id="lensClip">
        <circle cx="790" cy="170" r="156"/>
      </clipPath>
    </defs>
    <circle cx="790" cy="170" r="156" fill="#FFFFFF" stroke="#E8442A" stroke-width="12"/>
    <g clip-path="url(#lensClip)">
      <g>
        <rect x="634" y="14" width="38" height="38" fill="#BFD6EE"/><rect x="674" y="14" width="38" height="38" fill="#BFD6EE"/><rect x="714" y="14" width="38" height="38" fill="#BFD6EE"/><rect x="754" y="14" width="38" height="38" fill="#BFD6EE"/><rect x="794" y="14" width="38" height="38" fill="#BFD6EE"/><rect x="834" y="14" width="38" height="38" fill="#BFD6EE"/><rect x="874" y="14" width="38" height="38" fill="#BFD6EE"/><rect x="914" y="14" width="38" height="38" fill="#BFD6EE"/>
        <rect x="634" y="54" width="38" height="38" fill="#BFD6EE"/><rect x="674" y="54" width="38" height="38" fill="#BFD6EE"/><rect x="714" y="54" width="38" height="38" fill="#F2C230"/><rect x="754" y="54" width="38" height="38" fill="#F2C230"/><rect x="794" y="54" width="38" height="38" fill="#F2C230"/><rect x="834" y="54" width="38" height="38" fill="#F2C230"/><rect x="874" y="54" width="38" height="38" fill="#BFD6EE"/><rect x="914" y="54" width="38" height="38" fill="#BFD6EE"/>
        <rect x="634" y="94" width="38" height="38" fill="#F2C230"/><rect x="674" y="94" width="38" height="38" fill="#F2C230"/><rect x="714" y="94" width="38" height="38" fill="#F2C230"/><rect x="754" y="94" width="38" height="38" fill="#F2C230"/><rect x="794" y="94" width="38" height="38" fill="#F2C230"/><rect x="834" y="94" width="38" height="38" fill="#F2C230"/><rect x="874" y="94" width="38" height="38" fill="#F2C230"/><rect x="914" y="94" width="38" height="38" fill="#F2C230"/>
        <rect x="634" y="134" width="38" height="38" fill="#F2C230"/><rect x="674" y="134" width="38" height="38" fill="#F2C230"/><rect x="714" y="134" width="38" height="38" fill="#F2C230"/><rect x="754" y="134" width="38" height="38" fill="#F2C230"/><rect x="794" y="134" width="38" height="38" fill="#F2C230"/><rect x="834" y="134" width="38" height="38" fill="#F2C230"/><rect x="874" y="134" width="38" height="38" fill="#F2C230"/><rect x="914" y="134" width="38" height="38" fill="#F2C230"/>
        <rect x="634" y="174" width="38" height="38" fill="#F2C230"/><rect x="674" y="174" width="38" height="38" fill="#F2C230"/><rect x="714" y="174" width="38" height="38" fill="#F2C230"/><rect x="754" y="174" width="38" height="38" fill="#F2C230"/><rect x="794" y="174" width="38" height="38" fill="#F2C230"/><rect x="834" y="174" width="38" height="38" fill="#F2C230"/><rect x="874" y="174" width="38" height="38" fill="#F2C230"/><rect x="914" y="174" width="38" height="38" fill="#F2C230"/>
        <rect x="634" y="214" width="38" height="38" fill="#8FBF7A"/><rect x="674" y="214" width="38" height="38" fill="#8FBF7A"/><rect x="714" y="214" width="38" height="38" fill="#8FBF7A"/><rect x="754" y="214" width="38" height="38" fill="#8FBF7A"/><rect x="794" y="214" width="38" height="38" fill="#8FBF7A"/><rect x="834" y="214" width="38" height="38" fill="#8FBF7A"/><rect x="874" y="214" width="38" height="38" fill="#8FBF7A"/><rect x="914" y="214" width="38" height="38" fill="#8FBF7A"/>
        <rect x="634" y="254" width="38" height="38" fill="#8FBF7A"/><rect x="674" y="254" width="38" height="38" fill="#8FBF7A"/><rect x="714" y="254" width="38" height="38" fill="#8FBF7A"/><rect x="754" y="254" width="38" height="38" fill="#8FBF7A"/><rect x="794" y="254" width="38" height="38" fill="#8FBF7A"/><rect x="834" y="254" width="38" height="38" fill="#8FBF7A"/><rect x="874" y="254" width="38" height="38" fill="#8FBF7A"/><rect x="914" y="254" width="38" height="38" fill="#8FBF7A"/>
        <rect x="634" y="294" width="38" height="38" fill="#4E9A4E"/><rect x="674" y="294" width="38" height="38" fill="#4E9A4E"/><rect x="714" y="294" width="38" height="38" fill="#4E9A4E"/><rect x="754" y="294" width="38" height="38" fill="#4E9A4E"/><rect x="794" y="294" width="38" height="38" fill="#4E9A4E"/><rect x="834" y="294" width="38" height="38" fill="#4E9A4E"/><rect x="874" y="294" width="38" height="38" fill="#4E9A4E"/><rect x="914" y="294" width="38" height="38" fill="#4E9A4E"/>
      </g>
      <g stroke="#17181A" stroke-width="1" opacity=".4">
        <line x1="674" y1="14" x2="674" y2="334"/><line x1="714" y1="14" x2="714" y2="334"/><line x1="754" y1="14" x2="754" y2="334"/><line x1="794" y1="14" x2="794" y2="334"/><line x1="834" y1="14" x2="834" y2="334"/><line x1="874" y1="14" x2="874" y2="334"/><line x1="914" y1="14" x2="914" y2="334"/>
        <line x1="634" y1="54" x2="954" y2="54"/><line x1="634" y1="94" x2="954" y2="94"/><line x1="634" y1="134" x2="954" y2="134"/><line x1="634" y1="174" x2="954" y2="174"/><line x1="634" y1="214" x2="954" y2="214"/><line x1="634" y1="254" x2="954" y2="254"/><line x1="634" y1="294" x2="954" y2="294"/>
      </g>
    </g>
    <line x1="952" y1="290" x2="1028" y2="346" stroke="#E8442A" stroke-width="14" stroke-linecap="round"/>
    <text x="790" y="346" font-size="22" fill="#5F6066" text-anchor="middle">клетки-пиксели</text>
  </svg>
</section>

<!-- 11 -->
<section class="slide">
  <h2 class="h">Активность 1: «Пятна → числа»</h2>
  <div class="cols" style="align-items:center;">
    <div style="width:530px;flex:none;">
      <p class="t">1. У каждого лист: картинка из цветных пятен.</p>
      <p class="t">2. Легенда: какой цвет = какая цифра.</p>
      <p class="t">3. Впишите цифры в строку под картинкой — построчно, слева направо.</p>
    </div>
    <div style="flex:1;min-width:0;">
      <svg viewBox="0 0 600 400" width="600" height="400" role="img" aria-label="Сетка пятен 8 на 8 и пустая строка из 64 клеток">
        <g>
          <rect x="20" y="20" width="336" height="336" fill="none" stroke="#17181A" stroke-width="4"/>
          <g>
            <rect x="22" y="22" width="39" height="39" fill="#E8442A"/><rect x="64" y="22" width="39" height="39" fill="#BFD6EE"/><rect x="106" y="22" width="39" height="39" fill="#E8442A"/><rect x="148" y="22" width="39" height="39" fill="#17181A"/><rect x="190" y="22" width="39" height="39" fill="#BFD6EE"/><rect x="232" y="22" width="39" height="39" fill="#17181A"/><rect x="274" y="22" width="39" height="39" fill="#E8442A"/><rect x="316" y="22" width="38" height="39" fill="#BFD6EE"/>
            <rect x="22" y="64" width="39" height="39" fill="#BFD6EE"/><rect x="64" y="64" width="39" height="39" fill="#17181A"/><rect x="106" y="64" width="39" height="39" fill="#17181A"/><rect x="148" y="64" width="39" height="39" fill="#E8442A"/><rect x="190" y="64" width="39" height="39" fill="#17181A"/><rect x="232" y="64" width="39" height="39" fill="#E8442A"/><rect x="274" y="64" width="39" height="39" fill="#BFD6EE"/><rect x="316" y="64" width="38" height="39" fill="#E8442A"/>
            <rect x="22" y="106" width="39" height="39" fill="#E8442A"/><rect x="64" y="106" width="39" height="39" fill="#E8442A"/><rect x="106" y="106" width="39" height="39" fill="#BFD6EE"/><rect x="148" y="106" width="39" height="39" fill="#17181A"/><rect x="190" y="106" width="39" height="39" fill="#E8442A"/><rect x="232" y="106" width="39" height="39" fill="#BFD6EE"/><rect x="274" y="106" width="39" height="39" fill="#17181A"/><rect x="316" y="106" width="38" height="39" fill="#17181A"/>
            <rect x="22" y="148" width="39" height="39" fill="#17181A"/><rect x="64" y="148" width="39" height="39" fill="#E8442A"/><rect x="106" y="148" width="39" height="39" fill="#BFD6EE"/><rect x="148" y="148" width="39" height="39" fill="#BFD6EE"/><rect x="190" y="148" width="39" height="39" fill="#17181A"/><rect x="232" y="148" width="39" height="39" fill="#E8442A"/><rect x="274" y="148" width="39" height="39" fill="#E8442A"/><rect x="316" y="148" width="38" height="39" fill="#BFD6EE"/>
            <rect x="22" y="190" width="39" height="39" fill="#BFD6EE"/><rect x="64" y="190" width="39" height="39" fill="#17181A"/><rect x="106" y="190" width="39" height="39" fill="#E8442A"/><rect x="148" y="190" width="39" height="39" fill="#BFD6EE"/><rect x="190" y="190" width="39" height="39" fill="#BFD6EE"/><rect x="232" y="190" width="39" height="39" fill="#17181A"/><rect x="274" y="190" width="39" height="39" fill="#BFD6EE"/><rect x="316" y="190" width="38" height="39" fill="#E8442A"/>
            <rect x="22" y="232" width="39" height="39" fill="#E8442A"/><rect x="64" y="232" width="39" height="39" fill="#BFD6EE"/><rect x="106" y="232" width="39" height="39" fill="#17181A"/><rect x="148" y="232" width="39" height="39" fill="#E8442A"/><rect x="190" y="232" width="39" height="39" fill="#BFD6EE"/><rect x="232" y="232" width="39" height="39" fill="#17181A"/><rect x="274" y="232" width="39" height="39" fill="#E8442A"/><rect x="316" y="232" width="38" height="39" fill="#BFD6EE"/>
            <rect x="22" y="274" width="39" height="39" fill="#17181A"/><rect x="64" y="274" width="39" height="39" fill="#BFD6EE"/><rect x="106" y="274" width="39" height="39" fill="#E8442A"/><rect x="148" y="274" width="39" height="39" fill="#17181A"/><rect x="190" y="274" width="39" height="39" fill="#E8442A"/><rect x="232" y="274" width="39" height="39" fill="#BFD6EE"/><rect x="274" y="274" width="39" height="39" fill="#BFD6EE"/><rect x="316" y="274" width="38" height="39" fill="#17181A"/>
            <rect x="22" y="316" width="39" height="38" fill="#BFD6EE"/><rect x="64" y="316" width="39" height="38" fill="#E8442A"/><rect x="106" y="316" width="39" height="38" fill="#BFD6EE"/><rect x="148" y="316" width="39" height="38" fill="#17181A"/><rect x="190" y="316" width="39" height="38" fill="#BFD6EE"/><rect x="232" y="316" width="39" height="38" fill="#E8442A"/><rect x="274" y="316" width="39" height="38" fill="#17181A"/><rect x="316" y="316" width="38" height="38" fill="#E8442A"/>
          </g>
        </g>
        <g fill="#FFFFFF" stroke="#17181A" stroke-width="2">
          <rect x="400" y="22" width="16" height="16"/><rect x="418" y="22" width="16" height="16"/><rect x="436" y="22" width="16" height="16"/><rect x="454" y="22" width="16" height="16"/><rect x="472" y="22" width="16" height="16"/><rect x="490" y="22" width="16" height="16"/><rect x="508" y="22" width="16" height="16"/><rect x="526" y="22" width="16" height="16"/>
          <rect x="400" y="40" width="16" height="16"/><rect x="418" y="40" width="16" height="16"/><rect x="436" y="40" width="16" height="16"/><rect x="454" y="40" width="16" height="16"/><rect x="472" y="40" width="16" height="16"/><rect x="490" y="40" width="16" height="16"/><rect x="508" y="40" width="16" height="16"/><rect x="526" y="40" width="16" height="16"/>
          <rect x="400" y="58" width="16" height="16"/><rect x="418" y="58" width="16" height="16"/><rect x="436" y="58" width="16" height="16"/><rect x="454" y="58" width="16" height="16"/><rect x="472" y="58" width="16" height="16"/><rect x="490" y="58" width="16" height="16"/><rect x="508" y="58" width="16" height="16"/><rect x="526" y="58" width="16" height="16"/>
          <rect x="400" y="76" width="16" height="16"/><rect x="418" y="76" width="16" height="16"/><rect x="436" y="76" width="16" height="16"/><rect x="454" y="76" width="16" height="16"/><rect x="472" y="76" width="16" height="16"/><rect x="490" y="76" width="16" height="16"/><rect x="508" y="76" width="16" height="16"/><rect x="526" y="76" width="16" height="16"/>
          <rect x="400" y="94" width="16" height="16"/><rect x="418" y="94" width="16" height="16"/><rect x="436" y="94" width="16" height="16"/><rect x="454" y="94" width="16" height="16"/><rect x="472" y="94" width="16" height="16"/><rect x="490" y="94" width="16" height="16"/><rect x="508" y="94" width="16" height="16"/><rect x="526" y="94" width="16" height="16"/>
          <rect x="400" y="112" width="16" height="16"/><rect x="418" y="112" width="16" height="16"/><rect x="436" y="112" width="16" height="16"/><rect x="454" y="112" width="16" height="16"/><rect x="472" y="112" width="16" height="16"/><rect x="490" y="112" width="16" height="16"/><rect x="508" y="112" width="16" height="16"/><rect x="526" y="112" width="16" height="16"/>
          <rect x="400" y="130" width="16" height="16"/><rect x="418" y="130" width="16" height="16"/><rect x="436" y="130" width="16" height="16"/><rect x="454" y="130" width="16" height="16"/><rect x="472" y="130" width="16" height="16"/><rect x="490" y="130" width="16" height="16"/><rect x="508" y="130" width="16" height="16"/><rect x="526" y="130" width="16" height="16"/>
          <rect x="400" y="148" width="16" height="16"/><rect x="418" y="148" width="16" height="16"/><rect x="436" y="148" width="16" height="16"/><rect x="454" y="148" width="16" height="16"/><rect x="472" y="148" width="16" height="16"/><rect x="490" y="148" width="16" height="16"/><rect x="508" y="148" width="16" height="16"/><rect x="526" y="148" width="16" height="16"/>
        </g>
        <text x="480" y="200" font-size="20" fill="#5F6066" text-anchor="middle">строка из 64 клеток</text>
        <text x="480" y="228" font-size="20" fill="#E8442A" text-anchor="middle">→ 64 числа</text>
      </svg>
    </div>
  </div>
</section>

<!-- 12 -->
<section class="slide inv">
  <h2 class="h" style="color:#F7F6F2;">ВАУ-число</h2>
  <p style="font-size:34px;line-height:1.24;font-weight:700;">
    64 клетки мы прошли за минуты. Матрица камеры <span style="color:#FF6A4D;">12 Мп</span> — около <span style="color:#FF6A4D;">36 млн чисел</span> (3 цвета на пиксель).
  </p>
  <div class="cols" style="margin-top:16px;">
    <div style="width:580px;flex:none;">
      <svg viewBox="0 0 600 340" width="580" height="328" role="img" aria-label="Матрицы 16 к 9 в масштабе: 4K и Full HD">
        <rect x="30" y="26" width="520" height="280" fill="none" stroke="#FF6A4D" stroke-width="6"/>
        <text x="50" y="64" font-size="22" fill="#FF6A4D">4K UHD 3840 × 2160</text>
        <rect x="30" y="172" width="260" height="134" fill="rgba(255,255,255,.10)" stroke="#F7F6F2" stroke-width="6"/>
        <text x="48" y="210" font-size="22" fill="#F7F6F2">Full HD</text>
        <text x="48" y="238" font-size="22" fill="#F7F6F2">1920 × 1080</text>
        <text x="30" y="332" font-size="20" fill="#A6A7AD">оба кадра — 16 : 9, показаны в масштабе</text>
      </svg>
    </div>
    <div style="flex:1;min-width:0;color:#F7F6F2;">
      <p style="font-size:30px;line-height:1.2;font-weight:800;margin-bottom:12px;color:#FF6A4D;">Матрицы НЕ квадратные</p>
      <p style="font-size:24px;line-height:1.35;">Full HD <b>1920 × 1080</b> — <b>2 073 600</b> пикселей, ~<b>6,2 млн</b> чисел на кадр</p>
      <p style="font-size:24px;line-height:1.35;margin-top:10px;">4K UHD <b>3840 × 2160</b> — <b>8 294 400</b> пикселей, ~<b>25 млн</b> чисел на кадр; в видео ~<b>750 млн</b> чисел в секунду</p>
      <p style="font-size:24px;line-height:1.35;margin-top:12px;color:#FF6A4D;">Разрешение = строки × столбцы</p>
    </div>
  </div>
  <p style="font-size:30px;font-weight:800;margin-top:18px;color:#FF6A4D;">ИИ обрабатывает миллионы чисел за долю секунды.</p>
</section>

<!-- 13 -->
<section class="slide">
  <h2 class="h">Активность 2: «Лента 64»</h2>
  <div class="cols" style="align-items:flex-start;">
    <div style="width:700px;flex:none;">
      <p class="t">У пары — лента из 64 цветных клеток.</p>
      <p class="t">Задание: здесь записана картинка — восстановите её.</p>
      <p style="font-size:30px;font-weight:800;margin-top:18px;background:#fff;border-left:8px solid var(--accent);border-radius:10px;padding:14px 18px;">
        Первое число — строки (считаем вниз), второе — столбцы (считаем вправо).
      </p>
    </div>
    <div style="flex:1;text-align:center;align-self:center;">
      <div style="font-size:100px;line-height:1;margin-bottom:10px;">✂️</div>
      <div style="height:0;border-top:4px dashed #17181A;"></div>
    </div>
  </div>
  <svg viewBox="0 0 1160 96" width="1160" height="96" role="img" aria-label="Лента из 64 цветных клеток">
    <g>
      <rect x="0" y="10" width="16" height="62" fill="#E8442A"/><rect x="18" y="10" width="16" height="62" fill="#BFD6EE"/><rect x="36" y="10" width="16" height="62" fill="#17181A"/><rect x="54" y="10" width="16" height="62" fill="#F2C230"/><rect x="72" y="10" width="16" height="62" fill="#BFD6EE"/><rect x="90" y="10" width="16" height="62" fill="#E8442A"/><rect x="108" y="10" width="16" height="62" fill="#17181A"/><rect x="126" y="10" width="16" height="62" fill="#BFD6EE"/>
      <rect x="146" y="10" width="16" height="62" fill="#BFD6EE"/><rect x="164" y="10" width="16" height="62" fill="#E8442A"/><rect x="182" y="10" width="16" height="62" fill="#E8442A"/><rect x="200" y="10" width="16" height="62" fill="#17181A"/><rect x="218" y="10" width="16" height="62" fill="#F2C230"/><rect x="236" y="10" width="16" height="62" fill="#BFD6EE"/><rect x="254" y="10" width="16" height="62" fill="#17181A"/><rect x="272" y="10" width="16" height="62" fill="#E8442A"/>
      <rect x="292" y="10" width="16" height="62" fill="#17181A"/><rect x="310" y="10" width="16" height="62" fill="#F2C230"/><rect x="328" y="10" width="16" height="62" fill="#BFD6EE"/><rect x="346" y="10" width="16" height="62" fill="#E8442A"/><rect x="364" y="10" width="16" height="62" fill="#E8442A"/><rect x="382" y="10" width="16" height="62" fill="#17181A"/><rect x="400" y="10" width="16" height="62" fill="#BFD6EE"/><rect x="418" y="10" width="16" height="62" fill="#F2C230"/>
      <rect x="438" y="10" width="16" height="62" fill="#BFD6EE"/><rect x="456" y="10" width="16" height="62" fill="#17181A"/><rect x="474" y="10" width="16" height="62" fill="#E8442A"/><rect x="492" y="10" width="16" height="62" fill="#F2C230"/><rect x="510" y="10" width="16" height="62" fill="#17181A"/><rect x="528" y="10" width="16" height="62" fill="#BFD6EE"/><rect x="546" y="10" width="16" height="62" fill="#E8442A"/><rect x="564" y="10" width="16" height="62" fill="#17181A"/>
      <rect x="584" y="10" width="16" height="62" fill="#E8442A"/><rect x="602" y="10" width="16" height="62" fill="#17181A"/><rect x="620" y="10" width="16" height="62" fill="#F2C230"/><rect x="638" y="10" width="16" height="62" fill="#BFD6EE"/><rect x="656" y="10" width="16" height="62" fill="#E8442A"/><rect x="674" y="10" width="16" height="62" fill="#17181A"/><rect x="692" y="10" width="16" height="62" fill="#BFD6EE"/><rect x="710" y="10" width="16" height="62" fill="#F2C230"/>
      <rect x="730" y="10" width="16" height="62" fill="#F2C230"/><rect x="748" y="10" width="16" height="62" fill="#BFD6EE"/><rect x="766" y="10" width="16" height="62" fill="#17181A"/><rect x="784" y="10" width="16" height="62" fill="#E8442A"/><rect x="802" y="10" width="16" height="62" fill="#BFD6EE"/><rect x="820" y="10" width="16" height="62" fill="#17181A"/><rect x="838" y="10" width="16" height="62" fill="#E8442A"/><rect x="856" y="10" width="16" height="62" fill="#F2C230"/>
      <rect x="876" y="10" width="16" height="62" fill="#17181A"/><rect x="894" y="10" width="16" height="62" fill="#E8442A"/><rect x="912" y="10" width="16" height="62" fill="#BFD6EE"/><rect x="930" y="10" width="16" height="62" fill="#F2C230"/><rect x="948" y="10" width="16" height="62" fill="#17181A"/><rect x="966" y="10" width="16" height="62" fill="#BFD6EE"/><rect x="984" y="10" width="16" height="62" fill="#E8442A"/><rect x="1002" y="10" width="16" height="62" fill="#17181A"/>
      <rect x="1022" y="10" width="16" height="62" fill="#BFD6EE"/><rect x="1040" y="10" width="16" height="62" fill="#F2C230"/><rect x="1058" y="10" width="16" height="62" fill="#E8442A"/><rect x="1076" y="10" width="16" height="62" fill="#17181A"/><rect x="1094" y="10" width="16" height="62" fill="#BFD6EE"/><rect x="1112" y="10" width="16" height="62" fill="#F2C230"/><rect x="1130" y="10" width="16" height="62" fill="#E8442A"/><rect x="1148" y="10" width="12" height="62" fill="#17181A"/>
    </g>
    <g stroke="#E8442A" stroke-width="4" stroke-dasharray="8 7">
      <line x1="146" y1="0" x2="146" y2="90"/><line x1="292" y1="0" x2="292" y2="90"/>
      <line x1="438" y1="0" x2="438" y2="90"/><line x1="584" y1="0" x2="584" y2="90"/>
      <line x1="730" y1="0" x2="730" y2="90"/><line x1="876" y1="0" x2="876" y2="90"/>
      <line x1="1022" y1="0" x2="1022" y2="90"/>
    </g>
  </svg>
</section>

<!-- 14 -->
<section class="slide">
  <h2 class="h">Лодка найдена</h2>
  <svg viewBox="0 0 900 300" width="900" height="300" style="margin:0 auto;" role="img" aria-label="Лодка из 64 клеток, 16 на 4">
    <g stroke="#17181A" stroke-width="3">
      <rect x="40" y="20" width="50" height="50" fill="#FFFFFF"/><rect x="90" y="20" width="50" height="50" fill="#FFFFFF"/><rect x="140" y="20" width="50" height="50" fill="#FFFFFF"/><rect x="190" y="20" width="50" height="50" fill="#FFFFFF"/><rect x="240" y="20" width="50" height="50" fill="#FFFFFF"/><rect x="290" y="20" width="50" height="50" fill="#FFFFFF"/><rect x="340" y="20" width="50" height="50" fill="#FFFFFF"/><rect x="390" y="20" width="50" height="50" fill="#17181A"/>
      <rect x="440" y="20" width="50" height="50" fill="#FFFFFF"/><rect x="490" y="20" width="50" height="50" fill="#FFFFFF"/><rect x="540" y="20" width="50" height="50" fill="#FFFFFF"/><rect x="590" y="20" width="50" height="50" fill="#FFFFFF"/><rect x="640" y="20" width="50" height="50" fill="#FFFFFF"/><rect x="690" y="20" width="50" height="50" fill="#FFFFFF"/><rect x="740" y="20" width="50" height="50" fill="#FFFFFF"/><rect x="790" y="20" width="50" height="50" fill="#FFFFFF"/>
      <rect x="40" y="70" width="50" height="50" fill="#FFFFFF"/><rect x="90" y="70" width="50" height="50" fill="#FFFFFF"/><rect x="140" y="70" width="50" height="50" fill="#FFFFFF"/><rect x="190" y="70" width="50" height="50" fill="#FFFFFF"/><rect x="240" y="70" width="50" height="50" fill="#FFFFFF"/><rect x="290" y="70" width="50" height="50" fill="#FFFFFF"/><rect x="340" y="70" width="50" height="50" fill="#2E6FD9"/><rect x="390" y="70" width="50" height="50" fill="#17181A"/><rect x="440" y="70" width="50" height="50" fill="#2E6FD9"/>
      <rect x="490" y="70" width="50" height="50" fill="#FFFFFF"/><rect x="540" y="70" width="50" height="50" fill="#FFFFFF"/><rect x="590" y="70" width="50" height="50" fill="#FFFFFF"/><rect x="640" y="70" width="50" height="50" fill="#FFFFFF"/><rect x="690" y="70" width="50" height="50" fill="#FFFFFF"/><rect x="740" y="70" width="50" height="50" fill="#FFFFFF"/><rect x="790" y="70" width="50" height="50" fill="#FFFFFF"/>
      <rect x="40" y="120" width="50" height="50" fill="#FFFFFF"/><rect x="90" y="120" width="50" height="50" fill="#FFFFFF"/><rect x="140" y="120" width="50" height="50" fill="#FFFFFF"/><rect x="190" y="120" width="50" height="50" fill="#FFFFFF"/><rect x="240" y="120" width="50" height="50" fill="#2E6FD9"/><rect x="290" y="120" width="50" height="50" fill="#2E6FD9"/><rect x="340" y="120" width="50" height="50" fill="#2E6FD9"/><rect x="390" y="120" width="50" height="50" fill="#17181A"/>
      <rect x="440" y="120" width="50" height="50" fill="#2E6FD9"/><rect x="490" y="120" width="50" height="50" fill="#2E6FD9"/><rect x="540" y="120" width="50" height="50" fill="#2E6FD9"/><rect x="590" y="120" width="50" height="50" fill="#FFFFFF"/><rect x="640" y="120" width="50" height="50" fill="#FFFFFF"/><rect x="690" y="120" width="50" height="50" fill="#FFFFFF"/><rect x="740" y="120" width="50" height="50" fill="#FFFFFF"/><rect x="790" y="120" width="50" height="50" fill="#FFFFFF"/>
      <rect x="40" y="170" width="50" height="50" fill="#FFFFFF"/><rect x="90" y="170" width="50" height="50" fill="#FFFFFF"/><rect x="140" y="170" width="50" height="50" fill="#8A5A33"/><rect x="190" y="170" width="50" height="50" fill="#8A5A33"/><rect x="240" y="170" width="50" height="50" fill="#8A5A33"/><rect x="290" y="170" width="50" height="50" fill="#8A5A33"/><rect x="340" y="170" width="50" height="50" fill="#8A5A33"/><rect x="390" y="170" width="50" height="50" fill="#8A5A33"/>
      <rect x="440" y="170" width="50" height="50" fill="#8A5A33"/><rect x="490" y="170" width="50" height="50" fill="#8A5A33"/><rect x="540" y="170" width="50" height="50" fill="#8A5A33"/><rect x="590" y="170" width="50" height="50" fill="#8A5A33"/><rect x="640" y="170" width="50" height="50" fill="#8A5A33"/><rect x="690" y="170" width="50" height="50" fill="#FFFFFF"/><rect x="740" y="170" width="50" height="50" fill="#FFFFFF"/><rect x="790" y="170" width="50" height="50" fill="#FFFFFF"/>
    </g>
    <line x1="40" y1="246" x2="840" y2="246" stroke="#E8442A" stroke-width="5"/>
    <text x="440" y="282" font-size="22" fill="#E8442A" text-anchor="middle">16 столбцов</text>
    <line x1="20" y1="20" x2="20" y2="220" stroke="#E8442A" stroke-width="5"/>
    <text x="12" y="120" font-size="22" fill="#E8442A" text-anchor="middle" transform="rotate(-90 12 120)">4 строки</text>
  </svg>
  <p class="t" style="margin-top:14px;">Мало закодировать — нужна дополнительная информация: размер (ширина × высота). Поэтому у файла хранятся не только пиксели, но и размеры.</p>
  <p class="note" style="margin-top:10px;">Делители 64 → (1, 64), (2, 32), (4, 16), (8, 8) — считаем разные по форме — 4 прямоугольника (или 3, если не считать линию 1 × 64).</p>
</section>

<!-- 15 -->
<section class="slide">
  <h2 class="h">Свёртка: лупа ищет примитивы</h2>
  <p class="t">Лупа 3 × 3 едет по таблице и ищет примитивы: грани, углы, полосы, пятна.</p>
  <div style="display:flex;gap:20px;justify-content:center;margin:14px 0;">
    <svg viewBox="0 0 300 250" width="300" height="240" role="img" aria-label="Кадр 1: окно видит горизонтальную полосу">
      <g stroke="#17181A" stroke-width="2" fill="#EDEAE3">
        <rect x="20" y="10" width="44" height="44"/><rect x="64" y="10" width="44" height="44"/><rect x="108" y="10" width="44" height="44"/><rect x="152" y="10" width="44" height="44"/><rect x="196" y="10" width="44" height="44"/>
        <rect x="20" y="54" width="44" height="44"/><rect x="64" y="54" width="44" height="44"/><rect x="108" y="54" width="44" height="44"/><rect x="152" y="54" width="44" height="44"/><rect x="196" y="54" width="44" height="44"/>
        <rect x="20" y="98" width="44" height="44"/><rect x="64" y="98" width="44" height="44"/><rect x="108" y="98" width="44" height="44"/><rect x="152" y="98" width="44" height="44"/><rect x="196" y="98" width="44" height="44"/>
        <rect x="20" y="142" width="44" height="44"/><rect x="64" y="142" width="44" height="44"/><rect x="108" y="142" width="44" height="44"/><rect x="152" y="142" width="44" height="44"/><rect x="196" y="142" width="44" height="44"/>
        <rect x="20" y="186" width="44" height="44"/><rect x="64" y="186" width="44" height="44"/><rect x="108" y="186" width="44" height="44"/><rect x="152" y="186" width="44" height="44"/><rect x="196" y="186" width="44" height="44"/>
      </g>
      <g fill="#17181A">
        <rect x="20" y="98" width="44" height="44"/><rect x="64" y="98" width="44" height="44"/><rect x="108" y="98" width="44" height="44"/><rect x="152" y="98" width="44" height="44"/><rect x="196" y="98" width="44" height="44"/>
      </g>
      <rect x="64" y="54" width="132" height="132" fill="none" stroke="#E8442A" stroke-width="6"/>
      <text x="150" y="246" font-size="22" fill="#5F6066" text-anchor="middle">полоса</text>
    </svg>
    <svg viewBox="0 0 300 250" width="300" height="240" role="img" aria-label="Кадр 2: окно видит угол">
      <g stroke="#17181A" stroke-width="2" fill="#EDEAE3">
        <rect x="20" y="10" width="44" height="44"/><rect x="64" y="10" width="44" height="44"/><rect x="108" y="10" width="44" height="44"/><rect x="152" y="10" width="44" height="44"/><rect x="196" y="10" width="44" height="44"/>
        <rect x="20" y="54" width="44" height="44"/><rect x="64" y="54" width="44" height="44"/><rect x="108" y="54" width="44" height="44"/><rect x="152" y="54" width="44" height="44"/><rect x="196" y="54" width="44" height="44"/>
        <rect x="20" y="98" width="44" height="44"/><rect x="64" y="98" width="44" height="44"/><rect x="108" y="98" width="44" height="44"/><rect x="152" y="98" width="44" height="44"/><rect x="196" y="98" width="44" height="44"/>
        <rect x="20" y="142" width="44" height="44"/><rect x="64" y="142" width="44" height="44"/><rect x="108" y="142" width="44" height="44"/><rect x="152" y="142" width="44" height="44"/><rect x="196" y="142" width="44" height="44"/>
        <rect x="20" y="186" width="44" height="44"/><rect x="64" y="186" width="44" height="44"/><rect x="108" y="186" width="44" height="44"/><rect x="152" y="186" width="44" height="44"/><rect x="196" y="186" width="44" height="44"/>
      </g>
      <g fill="#17181A">
        <rect x="20" y="10" width="44" height="44"/><rect x="64" y="10" width="44" height="44"/><rect x="108" y="10" width="44" height="44"/>
        <rect x="20" y="54" width="44" height="44"/><rect x="20" y="98" width="44" height="44"/>
      </g>
      <rect x="20" y="10" width="132" height="132" fill="none" stroke="#E8442A" stroke-width="6"/>
      <text x="150" y="246" font-size="22" fill="#5F6066" text-anchor="middle">угол</text>
    </svg>
    <svg viewBox="0 0 300 250" width="300" height="240" role="img" aria-label="Кадр 3: окно видит пятно">
      <g stroke="#17181A" stroke-width="2" fill="#EDEAE3">
        <rect x="20" y="10" width="44" height="44"/><rect x="64" y="10" width="44" height="44"/><rect x="108" y="10" width="44" height="44"/><rect x="152" y="10" width="44" height="44"/><rect x="196" y="10" width="44" height="44"/>
        <rect x="20" y="54" width="44" height="44"/><rect x="64" y="54" width="44" height="44"/><rect x="108" y="54" width="44" height="44"/><rect x="152" y="54" width="44" height="44"/><rect x="196" y="54" width="44" height="44"/>
        <rect x="20" y="98" width="44" height="44"/><rect x="64" y="98" width="44" height="44"/><rect x="108" y="98" width="44" height="44"/><rect x="152" y="98" width="44" height="44"/><rect x="196" y="98" width="44" height="44"/>
        <rect x="20" y="142" width="44" height="44"/><rect x="64" y="142" width="44" height="44"/><rect x="108" y="142" width="44" height="44"/><rect x="152" y="142" width="44" height="44"/><rect x="196" y="142" width="44" height="44"/>
        <rect x="20" y="186" width="44" height="44"/><rect x="64" y="186" width="44" height="44"/><rect x="108" y="186" width="44" height="44"/><rect x="152" y="186" width="44" height="44"/><rect x="196" y="186" width="44" height="44"/>
      </g>
      <g fill="#17181A">
        <rect x="108" y="98" width="44" height="44"/><rect x="152" y="98" width="44" height="44"/>
        <rect x="108" y="142" width="44" height="44"/><rect x="152" y="142" width="44" height="44"/>
      </g>
      <rect x="64" y="54" width="132" height="132" fill="none" stroke="#E8442A" stroke-width="6"/>
      <text x="150" y="246" font-size="22" fill="#5F6066" text-anchor="middle">пятно</text>
    </svg>
  </div>
  <p class="t">Из примитивов складываются сложные признаки: угол + круг = колесо, колёса + кузов = машина.</p>
</section>

<!-- 16 -->
<section class="slide">
  <h2 class="h">Активность 3: «Лупа»</h2>
  <div class="cols" style="align-items:flex-start;">
    <div style="width:560px;flex:none;">
      <p class="t">В паре: один двигает лупу 3 × 3 по таблице, второй записывает координаты находок — на середине меняетесь.</p>
      <p class="t">Задание на время, таймер на доске.</p>
      <p class="t">Найдите примитивы: линии, углы, чёрные точки — и соберите догадку, что это.</p>
    </div>
    <div style="flex:1;min-width:0;">
      <svg viewBox="0 0 560 380" width="560" height="380" role="img" aria-label="Таблица 8 на 8 с окном 3 на 3 и листок для координат верхнего левого угла">
        <g stroke="#17181A" stroke-width="2" fill="#EDEAE3">
          <rect x="10" y="10" width="42" height="42"/><rect x="52" y="10" width="42" height="42"/><rect x="94" y="10" width="42" height="42"/><rect x="136" y="10" width="42" height="42"/><rect x="178" y="10" width="42" height="42"/><rect x="220" y="10" width="42" height="42"/><rect x="262" y="10" width="42" height="42"/><rect x="304" y="10" width="42" height="42"/>
          <rect x="10" y="52" width="42" height="42"/><rect x="52" y="52" width="42" height="42"/><rect x="94" y="52" width="42" height="42"/><rect x="136" y="52" width="42" height="42"/><rect x="178" y="52" width="42" height="42"/><rect x="220" y="52" width="42" height="42"/><rect x="262" y="52" width="42" height="42"/><rect x="304" y="52" width="42" height="42"/>
          <rect x="10" y="94" width="42" height="42"/><rect x="52" y="94" width="42" height="42"/><rect x="94" y="94" width="42" height="42"/><rect x="136" y="94" width="42" height="42"/><rect x="178" y="94" width="42" height="42"/><rect x="220" y="94" width="42" height="42"/><rect x="262" y="94" width="42" height="42"/><rect x="304" y="94" width="42" height="42"/>
          <rect x="10" y="136" width="42" height="42"/><rect x="52" y="136" width="42" height="42"/><rect x="94" y="136" width="42" height="42"/><rect x="136" y="136" width="42" height="42"/><rect x="178" y="136" width="42" height="42"/><rect x="220" y="136" width="42" height="42"/><rect x="262" y="136" width="42" height="42"/><rect x="304" y="136" width="42" height="42"/>
          <rect x="10" y="178" width="42" height="42"/><rect x="52" y="178" width="42" height="42"/><rect x="94" y="178" width="42" height="42"/><rect x="136" y="178" width="42" height="42"/><rect x="178" y="178" width="42" height="42"/><rect x="220" y="178" width="42" height="42"/><rect x="262" y="178" width="42" height="42"/><rect x="304" y="178" width="42" height="42"/>
          <rect x="10" y="220" width="42" height="42"/><rect x="52" y="220" width="42" height="42"/><rect x="94" y="220" width="42" height="42"/><rect x="136" y="220" width="42" height="42"/><rect x="178" y="220" width="42" height="42"/><rect x="220" y="220" width="42" height="42"/><rect x="262" y="220" width="42" height="42"/><rect x="304" y="220" width="42" height="42"/>
          <rect x="10" y="262" width="42" height="42"/><rect x="52" y="262" width="42" height="42"/><rect x="94" y="262" width="42" height="42"/><rect x="136" y="262" width="42" height="42"/><rect x="178" y="262" width="42" height="42"/><rect x="220" y="262" width="42" height="42"/><rect x="262" y="262" width="42" height="42"/><rect x="304" y="262" width="42" height="42"/>
          <rect x="10" y="304" width="42" height="42"/><rect x="52" y="304" width="42" height="42"/><rect x="94" y="304" width="42" height="42"/><rect x="136" y="304" width="42" height="42"/><rect x="178" y="304" width="42" height="42"/><rect x="220" y="304" width="42" height="42"/><rect x="262" y="304" width="42" height="42"/><rect x="304" y="304" width="42" height="42"/>
        </g>
        <g fill="#17181A">
          <rect x="52" y="52" width="42" height="42"/><rect x="52" y="94" width="42" height="42"/>
          <rect x="178" y="178" width="42" height="42"/><rect x="220" y="178" width="42" height="42"/><rect x="262" y="178" width="42" height="42"/>
          <rect x="304" y="304" width="42" height="42"/><rect x="136" y="262" width="42" height="42"/>
        </g>
        <rect x="94" y="52" width="126" height="126" fill="none" stroke="#E8442A" stroke-width="6"/>
        <rect x="370" y="10" width="180" height="330" rx="8" fill="#FFFFFF" stroke="#17181A" stroke-width="4"/>
        <text x="460" y="38" font-size="18" fill="#17181A" text-anchor="middle">координаты</text>
        <text x="460" y="60" font-size="14" fill="#5F6066" text-anchor="middle">верхнего левого угла</text>
        <g stroke="#17181A" stroke-width="2">
          <line x1="386" y1="85" x2="534" y2="85"/>
          <line x1="386" y1="130" x2="534" y2="130"/>
          <line x1="386" y1="175" x2="534" y2="175"/>
          <line x1="386" y1="220" x2="534" y2="220"/>
          <line x1="386" y1="265" x2="534" y2="265"/>
          <line x1="386" y1="310" x2="534" y2="310"/>
        </g>
        <text x="460" y="360" font-size="18" fill="#E8442A" text-anchor="middle">(строка, столбец)</text>
      </svg>
    </div>
  </div>
</section>

<!-- 17 -->
<section class="slide inv mid" style="align-items:center;text-align:center;">
  <h2 class="h" style="font-size:54px;color:#F7F6F2;">Сложности: ищем, где ИИ путается</h2>
  <p style="font-size:32px;color:#A6A7AD;margin-bottom:24px;">Две разные задачи — в обеих модель сильно хуже человека.</p>
  <svg viewBox="0 0 720 260" width="720" height="260" role="img" aria-label="Ряд вопросительных пикселей">
    <g>
      <rect x="10" y="10" width="60" height="60" fill="#3B3C42"/><rect x="80" y="10" width="60" height="60" fill="#FF6A4D"/><rect x="150" y="10" width="60" height="60" fill="#3B3C42"/><rect x="220" y="10" width="60" height="60" fill="#3B3C42"/><rect x="290" y="10" width="60" height="60" fill="#FF6A4D"/><rect x="360" y="10" width="60" height="60" fill="#3B3C42"/><rect x="430" y="10" width="60" height="60" fill="#3B3C42"/><rect x="500" y="10" width="60" height="60" fill="#FF6A4D"/><rect x="570" y="10" width="60" height="60" fill="#3B3C42"/><rect x="640" y="10" width="60" height="60" fill="#3B3C42"/>
      <rect x="10" y="80" width="60" height="60" fill="#FF6A4D"/><rect x="80" y="80" width="60" height="60" fill="#3B3C42"/><rect x="150" y="80" width="60" height="60" fill="#3B3C42"/><rect x="220" y="80" width="60" height="60" fill="#FF6A4D"/><rect x="290" y="80" width="60" height="60" fill="#3B3C42"/><rect x="360" y="80" width="60" height="60" fill="#3B3C42"/><rect x="430" y="80" width="60" height="60" fill="#FF6A4D"/><rect x="500" y="80" width="60" height="60" fill="#3B3C42"/><rect x="570" y="80" width="60" height="60" fill="#3B3C42"/><rect x="640" y="80" width="60" height="60" fill="#FF6A4D"/>
      <rect x="10" y="150" width="60" height="60" fill="#3B3C42"/><rect x="80" y="150" width="60" height="60" fill="#3B3C42"/><rect x="150" y="150" width="60" height="60" fill="#FF6A4D"/><rect x="220" y="150" width="60" height="60" fill="#3B3C42"/><rect x="290" y="150" width="60" height="60" fill="#3B3C42"/><rect x="360" y="150" width="60" height="60" fill="#FF6A4D"/><rect x="430" y="150" width="60" height="60" fill="#3B3C42"/><rect x="500" y="150" width="60" height="60" fill="#3B3C42"/><rect x="570" y="150" width="60" height="60" fill="#FF6A4D"/><rect x="640" y="150" width="60" height="60" fill="#3B3C42"/>
      <rect x="10" y="220" width="60" height="60" fill="#3B3C42"/><rect x="80" y="220" width="60" height="60" fill="#3B3C42"/><rect x="150" y="220" width="60" height="60" fill="#3B3C42"/><rect x="220" y="220" width="60" height="60" fill="#3B3C42"/><rect x="290" y="220" width="60" height="60" fill="#FF6A4D"/><rect x="360" y="220" width="60" height="60" fill="#3B3C42"/><rect x="430" y="220" width="60" height="60" fill="#3B3C42"/><rect x="500" y="220" width="60" height="60" fill="#3B3C42"/><rect x="570" y="220" width="60" height="60" fill="#3B3C42"/><rect x="640" y="220" width="60" height="60" fill="#3B3C42"/>
    </g>
  </svg>
</section>

<!-- 18 -->
<section class="slide">
  <h2 class="h">Провал: подсчёт объектов</h2>
  <div class="cols" style="align-items:flex-start;">
    <div style="width:560px;flex:none;">
      <svg viewBox="0 0 560 430" width="560" height="430" role="img" aria-label="Поле с пятью кругами и семью треугольниками">
        <rect x="10" y="10" width="540" height="370" rx="14" fill="#EDEAE3" stroke="#17181A" stroke-width="4"/>
        <g fill="#2E6FD9">
          <circle cx="90" cy="80" r="28"/><circle cx="250" cy="110" r="28"/><circle cx="400" cy="70" r="28"/>
          <circle cx="150" cy="250" r="28"/><circle cx="440" cy="240" r="28"/>
        </g>
        <g fill="#E8442A">
          <polygon points="60,160 92,215 28,215"/><polygon points="200,50 232,105 168,105"/>
          <polygon points="330,150 362,205 298,205"/><polygon points="480,130 512,185 448,185"/>
          <polygon points="80,300 112,355 48,355"/><polygon points="260,290 292,345 228,345"/>
          <polygon points="390,300 422,355 358,355"/>
        </g>
        <text x="280" y="410" font-size="24" fill="#17181A" text-anchor="middle">5 кругов и 7 треугольников</text>
      </svg>
    </div>
    <div style="flex:1;min-width:0;padding-top:8px;">
      <div style="background:#17181A;color:#F7F6F2;border-radius:14px;padding:16px 22px;font-size:30px;font-weight:800;">
        Ответ ИИ: 7 <span style="color:#A6A7AD;font-weight:400;">(правильно: 12)</span>
      </div>
      <div style="margin-top:22px;">
        <div style="font-size:26px;margin-bottom:6px;">один тип фигур — <b>58 %</b></div>
        <div style="height:26px;background:#E5E2DA;border-radius:6px;overflow:hidden;"><div style="width:58%;height:100%;background:#E8442A;"></div></div>
        <div style="font-size:26px;margin:14px 0 6px;">два типа — <b>46 %</b></div>
        <div style="height:26px;background:#E5E2DA;border-radius:6px;overflow:hidden;"><div style="width:46%;height:100%;background:#E8442A;"></div></div>
        <div style="font-size:26px;margin:14px 0 6px;">три типа — <b>30 %</b></div>
        <div style="height:26px;background:#E5E2DA;border-radius:6px;overflow:hidden;"><div style="width:30%;height:100%;background:#E8442A;"></div></div>
        <div class="note" style="margin-top:12px;">VLMCountBench, 2025</div>
      </div>
    </div>
  </div>
</section>

<!-- 19 -->
<section class="slide">
  <h2 class="h">Провал: пространство</h2>
  <p class="t">«Что левее? Что выше?» — для человека это просто.</p>
  <div style="display:flex;gap:24px;margin-top:16px;align-items:flex-start;">
    <div style="width:500px;flex:none;">
      <svg viewBox="0 0 500 300" width="500" height="300" role="img" aria-label="Сцена для вопросов о пространстве: дерево, кот, мяч, птица">
        <rect x="6" y="6" width="488" height="288" rx="12" fill="#EAF2F8" stroke="#17181A" stroke-width="4"/>
        <rect x="6" y="210" width="488" height="84" fill="#BFE3B0"/>
        <rect x="60" y="130" width="20" height="90" fill="#8A5A33"/>
        <circle cx="70" cy="110" r="42" fill="#4E9A4E"/>
        <ellipse cx="250" cy="230" rx="34" ry="18" fill="#F7F6F2" stroke="#17181A" stroke-width="3"/>
        <circle cx="250" cy="205" r="22" fill="#F7F6F2" stroke="#17181A" stroke-width="3"/>
        <path d="M236 192 L228 178 M264 192 L272 178" stroke="#17181A" stroke-width="3" stroke-linecap="round"/>
        <circle cx="242" cy="204" r="3" fill="#17181A"/><circle cx="258" cy="204" r="3" fill="#17181A"/>
        <circle cx="410" cy="235" r="22" fill="#E8442A"/>
        <path d="M390 235 A20 20 0 0 1 430 235" fill="none" stroke="#17181A" stroke-width="3"/>
        <ellipse cx="340" cy="70" rx="20" ry="12" fill="#F2C230"/>
        <circle cx="356" cy="62" r="8" fill="#F2C230"/>
        <path d="M364 62 L378 58 L364 56 Z" fill="#E8442A"/>
        <text x="70" y="250" font-size="20" fill="#5F6066" text-anchor="middle">дерево</text>
        <text x="250" y="270" font-size="20" fill="#5F6066" text-anchor="middle">кот</text>
        <text x="410" y="278" font-size="20" fill="#5F6066" text-anchor="middle">мяч</text>
        <text x="340" y="100" font-size="20" fill="#5F6066" text-anchor="middle">птица</text>
      </svg>
      <p class="note" style="margin-top:8px;">Что левее: кот или мяч? Что выше: дерево или птица?</p>
    </div>
    <div style="flex:1;min-width:0;">
      <svg viewBox="0 0 600 300" width="600" height="300" role="img" aria-label="Столбики Spatial CAPTCHA и SpaceCast-Bench">
        <text x="10" y="34" font-size="24" fill="#17181A">Spatial CAPTCHA (ICLR 2026)</text>
        <rect x="130" y="56" width="430" height="44" rx="8" fill="#E5E2DA"/>
        <rect x="130" y="56" width="430" height="44" rx="8" fill="#17181A"/>
        <text x="120" y="86" font-size="22" fill="#17181A" text-anchor="end">человек</text>
        <text x="345" y="86" font-size="22" fill="#F7F6F2" text-anchor="middle">&gt; 90 %</text>
        <rect x="130" y="116" width="430" height="44" rx="8" fill="#E5E2DA"/>
        <rect x="130" y="116" width="133" height="44" rx="8" fill="#E8442A"/>
        <text x="120" y="146" font-size="22" fill="#17181A" text-anchor="end">модель</text>
        <text x="273" y="146" font-size="22" fill="#17181A">31 %</text>
        <text x="10" y="196" font-size="20" fill="#5F6066">почти уровень случайного угадывания</text>
        <text x="10" y="244" font-size="24" fill="#17181A">SpaceCast-Bench (2026)</text>
        <rect x="130" y="262" width="430" height="44" rx="8" fill="#E5E2DA"/>
        <rect x="130" y="262" width="375" height="44" rx="8" fill="#17181A"/>
        <text x="120" y="292" font-size="22" fill="#17181A" text-anchor="end">человек</text>
        <text x="318" y="292" font-size="22" fill="#F7F6F2" text-anchor="middle">87,2 %</text>
        <rect x="130" y="322" width="430" height="44" rx="8" fill="#E5E2DA"/>
        <rect x="130" y="322" width="249" height="44" rx="8" fill="#E8442A"/>
        <text x="120" y="352" font-size="22" fill="#17181A" text-anchor="end">модель</text>
        <text x="389" y="352" font-size="22" fill="#17181A">58 %</text>
        <text x="10" y="400" font-size="20" fill="#5F6066">разрыв почти в 30 процентных пунктов</text>
      </svg>
    </div>
  </div>
</section>

<!-- 20 -->
<section class="slide">
  <h2 class="h">Провал: типографская атака</h2>
  <p class="note" style="margin-bottom:8px;">Научный термин из статей, не бытовой.</p>
  <div class="cols" style="align-items:flex-start;">
    <div style="width:540px;flex:none;">
      <p class="t">Berkeley (2017): наклейки на знаке «стоп» → камера читает «ограничение 45».</p>
      <p class="t">McAfee (2020): кусочек чёрной изоленты на знаке «35» → камера Mobileye на настоящем Tesla читает «85», круиз-контроль разгоняется.</p>
    </div>
    <div style="flex:1;min-width:0;">
      <svg viewBox="0 0 580 360" width="580" height="360" role="img" aria-label="Знаки до и после атаки">
        <g>
          <polygon points="40,20 90,20 120,50 120,90 90,120 40,120 10,90 10,50" fill="#E8442A"/>
          <text x="65" y="78" font-size="26" fill="#FFFFFF" text-anchor="middle">STOP</text>
          <text x="65" y="150" font-size="20" fill="#5F6066" text-anchor="middle">было</text>
        </g>
        <g>
          <polygon points="200,20 250,20 280,50 280,90 250,120 200,120 170,90 170,50" fill="#E8442A"/>
          <text x="225" y="78" font-size="26" fill="#FFFFFF" text-anchor="middle">STOP</text>
          <rect x="186" y="40" width="18" height="16" fill="#F2C230"/>
          <rect x="244" y="52" width="20" height="16" fill="#2E6FD9"/>
          <rect x="202" y="94" width="16" height="14" fill="#FFFFFF"/>
          <text x="225" y="150" font-size="20" fill="#5F6066" text-anchor="middle">после (наклейки)</text>
        </g>
        <g>
          <rect x="320" y="42" width="100" height="56" rx="8" fill="#17181A"/>
          <text x="370" y="80" font-size="28" fill="#FFFFFF" text-anchor="middle">45</text>
          <text x="370" y="120" font-size="20" fill="#5F6066" text-anchor="middle">читает камера</text>
        </g>
        <g>
          <circle cx="70" cy="240" r="50" fill="#FFFFFF" stroke="#E8442A" stroke-width="10"/>
          <text x="70" y="254" font-size="34" fill="#17181A" text-anchor="middle">35</text>
          <text x="70" y="320" font-size="20" fill="#5F6066" text-anchor="middle">было</text>
        </g>
        <g>
          <circle cx="230" cy="240" r="50" fill="#FFFFFF" stroke="#E8442A" stroke-width="10"/>
          <text x="230" y="254" font-size="34" fill="#17181A" text-anchor="middle">35</text>
          <rect x="214" y="238" width="34" height="10" fill="#17181A"/>
          <text x="230" y="320" font-size="20" fill="#5F6066" text-anchor="middle">после (изолента)</text>
        </g>
        <g>
          <rect x="320" y="212" width="100" height="56" rx="8" fill="#17181A"/>
          <text x="370" y="250" font-size="28" fill="#FFFFFF" text-anchor="middle">85</text>
          <text x="370" y="290" font-size="20" fill="#5F6066" text-anchor="middle">читает камера</text>
        </g>
      </svg>
    </div>
  </div>
  <p class="note" style="margin-top:12px;">Иногда срабатывает — проверяют и дома, это ваше домашнее задание.</p>
</section>

<!-- 21 -->
<section class="slide">
  <h2 class="h">Проблема известна давно и жива до сих пор</h2>
  <div style="display:flex;gap:14px;margin-top:8px;">
    <div class="card" style="flex:1;text-align:center;padding:10px 8px;">
      <svg viewBox="0 0 170 120" width="170" height="120" style="margin:0 auto;">
        <rect x="56" y="12" width="36" height="86" rx="8" fill="#17181A"/>
        <circle cx="74" cy="30" r="10" fill="#E8442A"/>
        <circle cx="74" cy="56" r="10" fill="#F2C230"/>
        <circle cx="74" cy="82" r="10" fill="#5F6066"/>
        <circle cx="140" cy="30" r="18" fill="#F2C230"/>
        <path d="M124 19 A18 18 0 1 0 140 48 A14 14 0 1 1 124 19 Z" fill="#EDEAE3"/>
      </svg>
      <div style="font-size:19px;line-height:1.2;margin-top:6px;">Tesla, 2021: луна принята за жёлтый сигнал светофора</div>
    </div>
    <div class="card" style="flex:1;text-align:center;padding:10px 8px;">
      <svg viewBox="0 0 170 120" width="170" height="120" style="margin:0 auto;">
        <rect x="6" y="26" width="158" height="62" fill="#5F6066"/>
        <line x1="85" y1="26" x2="85" y2="88" stroke="#F7F6F2" stroke-width="5" stroke-dasharray="12 10"/>
        <path d="M55 82 L68 56 L85 70 L100 52 L112 82 Z" fill="#F7F6F2" opacity=".65"/>
      </svg>
      <div style="font-size:19px;line-height:1.2;margin-top:6px;">«Фантомные» проекции на дорогу, 2022</div>
    </div>
    <div class="card" style="flex:1;text-align:center;padding:10px 8px;">
      <svg viewBox="0 0 170 120" width="170" height="120" style="margin:0 auto;">
        <path d="M18 84 L36 56 H122 L142 84 Z" fill="#E8442A"/>
        <rect x="48" y="42" width="58" height="16" rx="7" fill="#E8442A"/>
        <circle cx="48" cy="86" r="11" fill="#17181A"/>
        <circle cx="114" cy="86" r="11" fill="#17181A"/>
        <text x="84" y="28" font-size="18" fill="#17181A" text-anchor="middle">FSD</text>
        <text x="84" y="112" font-size="18" fill="#E8442A" text-anchor="middle">(Supervised)</text>
      </svg>
      <div style="font-size:19px;line-height:1.2;margin-top:6px;">Tesla, 2024: FSD переименована в «FSD (Supervised)»</div>
    </div>
    <div class="card" style="flex:1;text-align:center;padding:10px 8px;">
      <svg viewBox="0 0 170 120" width="170" height="120" style="margin:0 auto;">
        <rect x="48" y="10" width="72" height="80" rx="6" fill="#FFFFFF" stroke="#17181A" stroke-width="4"/>
        <g stroke="#17181A" stroke-width="3">
          <line x1="58" y1="28" x2="110" y2="28"/><line x1="58" y1="42" x2="110" y2="42"/>
          <line x1="58" y1="56" x2="94" y2="56"/>
        </g>
        <rect x="84" y="64" width="56" height="12" rx="5" fill="#8A5A33" transform="rotate(-30 84 64)"/>
        <rect x="106" y="88" width="52" height="14" rx="5" fill="#8A5A33" transform="rotate(-30 106 88)"/>
        <text x="84" y="114" font-size="16" fill="#17181A" text-anchor="middle">суд Калифорнии</text>
      </svg>
      <div style="font-size:19px;line-height:1.2;margin-top:6px;">Декабрь 2025: суд Калифорнии признал рекламу Autopilot/FSD вводящей в заблуждение</div>
    </div>
    <div class="card" style="flex:1;text-align:center;padding:10px 8px;">
      <svg viewBox="0 0 170 120" width="170" height="120" style="margin:0 auto;">
        <circle cx="44" cy="60" r="28" fill="#F7F6F2" stroke="#17181A" stroke-width="4"/>
        <circle cx="32" cy="52" r="8" fill="#17181A"/>
        <circle cx="56" cy="52" r="8" fill="#17181A"/>
        <circle cx="44" cy="72" r="5" fill="#17181A"/>
        <path d="M82 60 H100" stroke="#E8442A" stroke-width="5"/>
        <polygon points="100,52 114,60 100,68" fill="#E8442A"/>
        <circle cx="138" cy="60" r="26" fill="#8A5A33"/>
        <circle cx="128" cy="52" r="4" fill="#17181A"/>
        <circle cx="148" cy="52" r="4" fill="#17181A"/>
        <circle cx="138" cy="68" r="6" fill="#17181A"/>
      </svg>
      <div style="font-size:19px;line-height:1.2;margin-top:6px;">Панда → гиббон, 2017</div>
    </div>
  </div>
</section>

<!-- 22 -->
<section class="slide">
  <h2 class="h">Поддержка, часть 1: образ</h2>
  <div class="cols" style="align-items:center;">
    <div style="width:500px;flex:none;">
      <svg viewBox="0 0 500 360" width="500" height="360" role="img" aria-label="Ваза Рубина">
        <rect x="6" y="6" width="488" height="348" rx="14" fill="#FFFFFF" stroke="#DCD9D1" stroke-width="3"/>
        <path d="M 170 40
                 L 330 40
                 L 330 70
                 C 330 90, 310 110, 290 130
                 C 310 155, 310 200, 290 225
                 C 310 245, 330 265, 330 285
                 L 330 300
                 L 170 300
                 L 170 285
                 C 170 265, 190 245, 210 225
                 C 190 200, 190 155, 210 130
                 C 190 110, 170 90, 170 70 Z"
              fill="#17181A"/>
        <line x1="222" y1="180" x2="278" y2="180" stroke="#FFFFFF" stroke-width="3"/>
        <line x1="216" y1="196" x2="284" y2="196" stroke="#FFFFFF" stroke-width="3"/>
        <text x="250" y="336" font-size="22" fill="#5F6066" text-anchor="middle">ваза или два профиля?</text>
      </svg>
    </div>
    <div style="width:500px;flex:none;">
      <svg viewBox="0 0 500 360" width="500" height="360" role="img" aria-label="Утка-кролик">
        <rect x="6" y="6" width="488" height="348" rx="14" fill="#FFFFFF" stroke="#DCD9D1" stroke-width="3"/>
        <path d="M90 240
                 C90 180 130 140 180 140
                 C195 110 210 80 235 68
                 C255 58 270 68 268 88
                 C265 110 248 128 225 138
                 C260 148 285 178 285 212
                 C285 252 252 282 210 290
                 C165 298 120 292 100 272
                 C90 260 88 250 90 240 Z"
              fill="#17181A"/>
        <circle cx="222" cy="196" r="9" fill="#FFFFFF"/>
        <path d="M285 212 L330 224 L285 234 Z" fill="#E8442A"/>
        <text x="250" y="336" font-size="22" fill="#5F6066" text-anchor="middle">утка или кролик?</text>
      </svg>
    </div>
  </div>
  <p style="font-size:32px;font-weight:800;margin-top:14px;">Человек видит обе трактовки — <span class="acc">ИИ обычно выбирает одну</span>.</p>
</section>

<!-- 23 -->
<section class="slide">
  <h2 class="h">Поддержка, часть 2: цифры и «почему»</h2>
  <div class="cols" style="align-items:flex-start;">
    <div style="width:600px;flex:none;">
      <p class="t">Современные модели ошибаются на зрительных задачах в <span class="k">17–26 %</span> случаев.</p>
      <p class="t">Галлюцинируя, говорят увереннее на <span class="k">~34 %</span>.</p>
      <p style="font-size:26px;line-height:1.3;margin-top:14px;background:#fff;border-left:8px solid var(--accent);border-radius:10px;padding:10px 16px;">
        Галлюцинация: машина выдумывает — как привиделось во сне; это научное слово, не ругательное.</p>
      <p class="note" style="margin-top:12px;">Модели учатся угождать, а не проверять — поэтому уверенный тон не означает правильный ответ.</p>
    </div>
    <div style="flex:1;min-width:0;">
      <svg viewBox="0 0 480 320" width="480" height="320" role="img" aria-label="Шкала уверенности и шкала правильности расходятся">
        <text x="10" y="28" font-size="22" fill="#5F6066">уверенность</text>
        <rect x="10" y="38" width="460" height="36" rx="8" fill="#E5E2DA"/>
        <rect x="10" y="38" width="420" height="36" rx="8" fill="#E8442A"/>
        <text x="220" y="62" font-size="22" fill="#FFFFFF" text-anchor="middle">высокая</text>
        <text x="10" y="118" font-size="22" fill="#5F6066">правильность</text>
        <rect x="10" y="128" width="460" height="36" rx="8" fill="#E5E2DA"/>
        <rect x="10" y="128" width="196" height="36" rx="8" fill="#17181A"/>
        <text x="108" y="152" font-size="22" fill="#FFFFFF" text-anchor="middle">ниже</text>
        <path d="M430 74 L230 128" stroke="#E8442A" stroke-width="6" stroke-dasharray="10 9" fill="none"/>
        <rect x="265" y="80" width="180" height="32" rx="6" fill="#FFFFFF"/>
        <text x="355" y="102" font-size="22" fill="#E8442A" text-anchor="middle">разрыв ~34 %</text>
        <text x="240" y="246" font-size="22" fill="#17181A" text-anchor="middle">тон увереннее —</text>
        <text x="240" y="278" font-size="22" fill="#17181A" text-anchor="middle">ответ не вернее</text>
        <rect x="60" y="300" width="360" height="3" fill="#DCD9D1"/>
      </svg>
    </div>
  </div>
</section>

<!-- 24 -->
<section class="slide">
  <h2 class="h">Личная проекция</h2>
  <div class="cols" style="align-items:center;">
    <div style="width:640px;flex:none;">
      <p style="font-size:32px;line-height:1.35;font-weight:700;">Вы когда-нибудь будете ехать в машине с автопилотом?</p>
      <p style="font-size:32px;line-height:1.35;font-weight:700;margin-top:16px;">Верите ей?</p>
      <p style="font-size:32px;line-height:1.35;font-weight:700;margin-top:16px;">Что сделаете, если она затормозит перед луной?</p>
    </div>
    <div style="flex:1;min-width:0;">
      <svg viewBox="0 0 460 400" width="460" height="400" role="img" aria-label="Руль и луна за лобовым стеклом">
        <path d="M30 16 L430 16 L430 200 L30 200 Z" fill="#1B2330"/>
        <circle cx="340" cy="80" r="40" fill="#F2C230"/>
        <circle cx="326" cy="66" r="10" fill="#1B2330" opacity=".25"/>
        <circle cx="354" cy="94" r="7" fill="#1B2330" opacity=".2"/>
        <g fill="#FFFFFF" opacity=".85">
          <circle cx="90" cy="60" r="4"/><circle cx="140" cy="44" r="3"/><circle cx="200" cy="80" r="4"/>
          <circle cx="250" cy="50" r="3"/><circle cx="120" cy="130" r="3"/><circle cx="230" cy="150" r="4"/>
        </g>
        <rect x="30" y="200" width="400" height="28" rx="8" fill="#0E1218"/>
        <circle cx="230" cy="320" r="72" fill="none" stroke="#17181A" stroke-width="16"/>
        <line x1="230" y1="248" x2="230" y2="290" stroke="#17181A" stroke-width="12"/>
        <line x1="164" y1="340" x2="296" y2="340" stroke="#17181A" stroke-width="12"/>
        <circle cx="230" cy="320" r="18" fill="#E8442A"/>
      </svg>
    </div>
  </div>
</section>

<!-- 25 -->
<section class="slide">
  <h2 class="h">Quick, Draw!</h2>
  <p style="font-size:40px;font-weight:800;color:var(--accent);margin-bottom:12px;">quickdraw.withgoogle.com</p>
  <div class="cols" style="align-items:flex-start;">
    <div style="width:620px;flex:none;">
      <p class="t">4 карточки на 4 пары.</p>
      <p class="t">Пара выходит к доске: один рисует, второй может тихо подсказывать.</p>
      <p class="t">Перед ответом сети — 15 секунд обсуждения в парах.</p>
      <p class="t">После ответа — каждая пара говорит одну мысль: почему угадала или нет.</p>
    </div>
    <div style="flex:1;min-width:0;">
      <svg viewBox="0 0 460 230" width="460" height="230" role="img" aria-label="Карандаш рисует линию, рядом лампочка-угадайка">
        <path d="M30 200 C80 150 130 220 180 180 C210 155 230 175 258 155" fill="none" stroke="#17181A" stroke-width="7" stroke-linecap="round"/>
        <g transform="translate(250, 140) rotate(-40)">
          <rect x="-12" y="-90" width="24" height="90" fill="#E8442A"/>
          <rect x="-12" y="-110" width="24" height="20" fill="#17181A"/>
          <polygon points="-12,0 12,0 0,18" fill="#17181A"/>
        </g>
        <circle cx="360" cy="60" r="36" fill="#F2C230"/>
        <rect x="350" y="94" width="20" height="10" rx="3" fill="#5F6066"/>
        <rect x="354" y="108" width="12" height="6" rx="3" fill="#5F6066"/>
        <g stroke="#F2C230" stroke-width="5" stroke-linecap="round">
          <line x1="360" y1="14" x2="360" y2="6"/>
          <line x1="406" y1="60" x2="414" y2="60"/>
          <line x1="316" y1="20" x2="310" y2="14"/>
          <line x1="404" y1="20" x2="410" y2="14"/>
        </g>
        <text x="360" y="170" font-size="22" fill="#5F6066" text-anchor="middle">сеть угадывает</text>
      </svg>
    </div>
  </div>
</section>

<!-- 26 -->
<section class="slide inv mid">
  <p style="font-size:44px;line-height:1.2;font-weight:800;max-width:1080px;">
    ИИ отвечает уверенно даже там, где ошибается — <span style="color:#FF6A4D;">правило пользователя: проверяй</span>.
  </p>
  <div style="display:flex;align-items:center;gap:30px;margin-top:24px;">
    <svg viewBox="0 0 600 230" width="600" height="230" role="img" aria-label="Звуковая волна превращается в таблицу чисел">
      <g stroke="#F7F6F2" stroke-width="6" stroke-linecap="round">
        <line x1="20" y1="115" x2="20" y2="115"/><line x1="36" y1="85" x2="36" y2="145"/>
        <line x1="52" y1="55" x2="52" y2="175"/><line x1="68" y1="35" x2="68" y2="195"/>
        <line x1="84" y1="65" x2="84" y2="165"/><line x1="100" y1="95" x2="100" y2="135"/>
        <line x1="116" y1="45" x2="116" y2="185"/><line x1="132" y1="75" x2="132" y2="155"/>
        <line x1="148" y1="105" x2="148" y2="125"/><line x1="164" y1="65" x2="164" y2="165"/>
        <line x1="180" y1="40" x2="180" y2="190"/><line x1="196" y1="90" x2="196" y2="140"/>
        <line x1="212" y1="70" x2="212" y2="160"/><line x1="228" y1="100" x2="228" y2="130"/>
      </g>
      <line x1="260" y1="115" x2="330" y2="115" stroke="#FF6A4D" stroke-width="7"/>
      <polygon points="330,101 360,115 330,129" fill="#FF6A4D"/>
      <g stroke="#3B3C42" stroke-width="2">
        <rect x="380" y="55" width="50" height="50" fill="#1D1E22"/><rect x="430" y="55" width="50" height="50" fill="#1D1E22"/>
        <rect x="480" y="55" width="50" height="50" fill="#1D1E22"/><rect x="530" y="55" width="50" height="50" fill="#1D1E22"/>
        <rect x="380" y="105" width="50" height="50" fill="#1D1E22"/><rect x="430" y="105" width="50" height="50" fill="#1D1E22"/>
        <rect x="480" y="105" width="50" height="50" fill="#1D1E22"/><rect x="530" y="105" width="50" height="50" fill="#1D1E22"/>
        <rect x="380" y="155" width="50" height="50" fill="#1D1E22"/><rect x="430" y="155" width="50" height="50" fill="#1D1E22"/>
        <rect x="480" y="155" width="50" height="50" fill="#1D1E22"/><rect x="530" y="155" width="50" height="50" fill="#1D1E22"/>
      </g>
      <g font-size="20" fill="#F7F6F2" text-anchor="middle">
        <text x="405" y="87">12</text><text x="455" y="87">240</text><text x="505" y="87">7</text><text x="555" y="87">198</text>
        <text x="405" y="137">200</text><text x="455" y="137">88</text><text x="505" y="137">255</text><text x="555" y="137">41</text>
        <text x="405" y="187">6</text><text x="455" y="187">150</text><text x="505" y="187">99</text><text x="555" y="187">210</text>
      </g>
    </svg>
    <p style="font-size:28px;line-height:1.35;max-width:440px;color:#F7F6F2;">
      Звук — это тоже таблица чисел, только другая. В следующий раз — как ИИ слышит и говорит.
    </p>
  </div>
</section>

<!-- 27 -->
<section class="slide">
  <h2 class="h">Домашнее задание</h2>
  <div class="cols" style="align-items:center;">
    <div style="width:660px;flex:none;">
      <p class="t">Дома запусти умную камеру или ассистента на телефоне.</p>
      <p class="t">Проверь: картинки из урока (фигуры, «что левее»), предметы с наклейкой или надписью, что-то своё.</p>
      <p class="t">Принеси один пример <b>на выбор</b>: где ИИ прав (тоже интересно!), где ошибся или где засомневался.</p>
    </div>
    <div style="flex:1;min-width:0;">
      <svg viewBox="0 0 400 420" width="400" height="420" role="img" aria-label="Телефон с камерой и пиксельный кот">
        <rect x="100" y="10" width="200" height="370" rx="26" fill="#FFFFFF" stroke="#17181A" stroke-width="6"/>
        <rect x="116" y="46" width="168" height="290" rx="10" fill="#EDEAE3"/>
        <circle cx="200" cy="72" r="10" fill="#17181A"/>
        <g fill="#17181A">
          <rect x="146" y="138" width="24" height="24"/><rect x="230" y="138" width="24" height="24"/>
          <rect x="170" y="168" width="60" height="24"/><rect x="146" y="192" width="108" height="24"/>
          <rect x="170" y="216" width="60" height="24"/><rect x="146" y="240" width="24" height="24"/>
          <rect x="230" y="240" width="24" height="24"/>
          <rect x="122" y="116" width="24" height="24"/><rect x="254" y="116" width="24" height="24"/>
        </g>
        <g fill="#E8442A">
          <rect x="194" y="276" width="24" height="24"/>
        </g>
        <text x="200" y="318" font-size="22" fill="#5F6066" text-anchor="middle">кто здесь?</text>
        <rect x="140" y="348" width="120" height="8" rx="4" fill="#DCD9D1"/>
        <text x="200" y="408" font-size="22" fill="#5F6066" text-anchor="middle">камера телефона</text>
        <circle cx="338" cy="110" r="32" fill="#E8442A"/>
        <text x="338" y="122" font-size="32" fill="#FFFFFF" text-anchor="middle">?</text>
      </svg>
    </div>
  </div>
</section>

<div id="cnt">1 / 27</div>
</div>

<script>
(function(){
  var slides = Array.prototype.slice.call(document.querySelectorAll('.slide'));
  var cnt = document.getElementById('cnt');
  var i = 0;

  function show(n){
    if(n < 0) n = 0;
    if(n > slides.length - 1) n = slides.length - 1;
    i = n;
    slides.forEach(function(s, k){ s.classList.toggle('on', k === i); });
    cnt.textContent = (i + 1) + ' / ' + slides.length;
  }

  document.addEventListener('keydown', function(e){
    if(e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' '){ e.preventDefault(); show(i + 1); }
    else if(e.key === 'ArrowLeft' || e.key === 'PageUp'){ e.preventDefault(); show(i - 1); }
    else if(e.key === 'Home'){ e.preventDefault(); show(0); }
    else if(e.key === 'End'){ e.preventDefault(); show(slides.length - 1); }
  });

  document.addEventListener('click', function(e){
    if(e.clientX < window.innerWidth * 0.16){ show(i - 1); }
    else { show(i + 1); }
  });

  function fit(){
    var s = Math.min(window.innerWidth / 1280, window.innerHeight / 720);
    document.getElementById('stage').style.transform = 'translate(-50%,-50%) scale(' + s + ')';
  }
  window.addEventListener('resize', fit);
  fit();

  var re = /(^|\s)(в|и|а|о|у|с|к|на|по|за|из|от|до|не|же|ли|то|—)\s/gi;
  function nbsp(node){
    if(node.nodeType === 3){
      node.nodeValue = node.nodeValue.replace(re, function(m, a, b){ return a + b + '\u00A0'; });
    } else if(node.nodeType === 1 && node.tagName !== 'SVG' && node.tagName !== 'svg'){
      Array.prototype.forEach.call(node.childNodes, nbsp);
    }
  }
  document.querySelectorAll('.slide p, .slide h1, .slide h2').forEach(nbsp);

  show(0);
})();
</script>
</body>
</html>
===== КОНЕЦ ФАЙЛА: 5-klass/iiib-06-kompyuternoe-zrenie/slajdy.html =====
