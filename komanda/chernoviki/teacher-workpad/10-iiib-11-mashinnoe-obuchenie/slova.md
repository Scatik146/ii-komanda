| № | слово | папка | слой | состав | что делает |
|---|---|---|---|---|---|
| 9439 | `pustyeVesa` | lib/nejron | нижний | — | девять весов, все равны 0 |
| 9440 | `kopiya` | lib/nejron | нижний | — | независимая копия сетки 3×3 (веса или буква) |
| 9441 | `summaS` | lib/nejron | нижний | — | сумма весов тех клеток, где на входе 1 (вход × вес) |
| 9442 | `vyhod` | lib/nejron | нижний | — | 1, если S не меньше порога, иначе 0 |
| 9443 | `vetka` | lib/nejron | нижний | — | что делать после ответа нейрона — 'ok', 'nuzhen1' (вышел 0) или 'nuzhen0' (вышел 1) |
| 9444 | `shagVesa` | lib/nejron | нижний | — | сдвиг веса и порога по ветке: +1 / −1 / 0 |
| 9445 | `popravit` | lib/nejron | средний | 9440, 9444 | правило Розенблатта — ±1 к весам клеток с 1, порог в обратную сторону |
| 9446 | `shag` | lib/nejron | средний | 9441, 9442, 9443, 9445, 9449 | один пример через нейрон — S, выход, ветка и веса после поправки |
| 9447 | `krug` | lib/nejron | средний | 9446 | все примеры по одному разу — строки журнала, итоговые веса и число ошибок |
| 9448 | `obuchit` | lib/nejron | верхний | 9439, 9447 | круги, пока не будет круга без ошибок (не больше maks кругов) |
| 9449 | `primer` | lib/nejron | нижний | — | буква из BUKVY с правильным ответом (разметкой) для выборки |
| 9450 | `raznica` | lib/nejron | нижний | — | сколько клеток у двух сеток не совпадает (0–9) |
| 9451 | `soedinit` | lib/nejron | нижний | — | в списке групп слить группу клавиши b с группой клавиши a |
| 9452 | `gruppy` | lib/nejron | верхний | 9453, 9454 | без разметки — буквы, отличающиеся не больше чем на porog клеток, в одну кучку |
| 9453 | `prisoedinitPohozhih` | lib/nejron | средний | 9450, 9451 | букву номер a слить со всеми следующими, похожими не дальше porog клеток |
| 9454 | `razlozhit` | lib/nejron | нижний | — | номера групп → список кучек (порядок — как у первых букв) |
| 9455 | `kletka` | lib/nejron | нижний | — | ячейка входа — 1 закрашена, 0 пустая |
| 9456 | `narisovatSetku` | lib/nejron | верхний | 9455, 9457 | сетка 3×3 в таблице; priNazhatii(i, j) — щелчок по клетке (можно не давать) |
| 9457 | `svyazatKletku` | lib/nejron | нижний | — | повесить на ячейку щелчок с её номером строки и столбца |
| 9458 | `poleVesa` | lib/nejron | нижний | — | ячейка с полем ввода веса (−10…10) или с числом, если менять нельзя |
| 9459 | `narisovatVesa` | lib/nejron | верхний | 9458 | девять весов в таблице |
| 9460 | `prochitatVesa` | lib/nejron | верхний | 9439 | веса из таблицы с полями (пусто или не число — 0) |
| 9461 | `stroka` | 10-klass/iiib-11-mashinnoe-obuchenie | нижний | — | строка таблицы из ячеек (th, если zagolovok) |
| 9462 | `tablicaEtapov` | 10-klass/iiib-11-mashinnoe-obuchenie | верхний | 9461 | этапы с минутами и минутой окончания; сумма минут |
| 9463 | `tablicaVydumok` | 10-klass/iiib-11-mashinnoe-obuchenie | верхний | 9461, 9464 | ключ — где выдумка, как на самом деле, чем проверить |
| 9464 | `nomerAbzaca` | 10-klass/iiib-11-mashinnoe-obuchenie | нижний | — | номер абзаца листа 1, где стоит выдумка |
| 9465 | `zapolnitTekst` | 10-klass/iiib-11-mashinnoe-obuchenie | нижний | — | абзацы текста для чтения (выдумки не помечены — ключ у учителя) |
| 9466 | `bukvaBezImeni` | 10-klass/iiib-11-mashinnoe-obuchenie | нижний | — | номер и маленькая сетка буквы экрана 3, строчка для кучки |
| 9467 | `pustayaSetka` | 10-klass/iiib-11-mashinnoe-obuchenie | нижний | — | таблица 3×3 из пустых клеток |
| 9468 | `zapolnitStoronu2` | 10-klass/iiib-11-mashinnoe-obuchenie | верхний | 9466, 9467 | каркас конспекта, буквы без имён, домашнее задание |
| 9469 | `novoeObuchenie` | 10-klass/iiib-11-mashinnoe-obuchenie | нижний | — | обучение экрана 2 с нуля — веса 0, порог 0, круг 1, ждём S |
| 9470 | `novoeSostoyanie` | 10-klass/iiib-11-mashinnoe-obuchenie | средний | 9469 | начало урока — экран 1, буква C₁ на входе |
| 9471 | `zapomnit` | 10-klass/iiib-11-mashinnoe-obuchenie | нижний | — | записать состояние урока в память браузера |
| 9472 | `stroka` | 10-klass/iiib-11-mashinnoe-obuchenie | нижний | — | строка таблицы из ячеек (th, если zagolovok) |
| 9473 | `otmetka` | 10-klass/iiib-11-mashinnoe-obuchenie | нижний | — | ✓ или ✗ с цветом |
| 9474 | `tablicaProverki` | 10-klass/iiib-11-mashinnoe-obuchenie | средний | 9461, 9473 | буквы [ключ, нужно] через нейрон — таблица; число верных |
| 9475 | `peremeshat` | 10-klass/iiib-11-mashinnoe-obuchenie | нижний | — | новый список в случайном порядке |
| 9476 | `risovatVhod` | 10-klass/iiib-11-mashinnoe-obuchenie | средний | 9477 | сетка входа, щелчок переключает клетку |
| 9477 | `perevernutKletku` | 10-klass/iiib-11-mashinnoe-obuchenie | средний | 9476, 9480 | клетка входа 0 ↔ 1 |
| 9478 | `vzyatBukvu` | 10-klass/iiib-11-mashinnoe-obuchenie | средний | 9476, 9480 | букву из набора — на вход |
| 9479 | `knopkiBukv` | 10-klass/iiib-11-mashinnoe-obuchenie | верхний | 9478 | кнопки семи букв под сеткой входа |
| 9480 | `pereschitat1` | 10-klass/iiib-11-mashinnoe-obuchenie | средний | 9471 | прочитать веса и порог, показать S и выход |
| 9481 | `risovatVesa1` | 10-klass/iiib-11-mashinnoe-obuchenie | средний | 9480 | веса и порог экрана 1 из состояния |
| 9482 | `spisokRekorda` | 10-klass/iiib-11-mashinnoe-obuchenie | нижний | — | семь букв с ответами задания «Рекорд» |
| 9483 | `proveritRekord` | 10-klass/iiib-11-mashinnoe-obuchenie | средний | 9471, 9474, 9480, 9482 | веса ученика на всех 7 буквах — счёт и лучший результат |
| 9484 | `vzyatVesaMashiny` | 10-klass/iiib-11-mashinnoe-obuchenie | средний | 9481 | веса, которые машина нашла на экране 2 (подсказка) |
| 9485 | `tekushchijPrimer` | 10-klass/iiib-11-mashinnoe-obuchenie | нижний | — | пример обучающей выборки, на котором стоим |
| 9486 | `soobshchit2` | 10-klass/iiib-11-mashinnoe-obuchenie | нижний | — | надпись под ходом (verno: true — зелёная, false — красная) |
| 9487 | `hodS` | 10-klass/iiib-11-mashinnoe-obuchenie | средний | 9493 | ученик вводит сумму S |
| 9488 | `hodVyhod` | 10-klass/iiib-11-mashinnoe-obuchenie | средний | 9485, 9494 | ученик выбирает выход 1 или 0 |
| 9489 | `hodVetka` | 10-klass/iiib-11-mashinnoe-obuchenie | средний | 9485, 9495, 9496 | ученик выбирает поправку (порядок кнопок перемешан) |
| 9490 | `risovatHod` | 10-klass/iiib-11-mashinnoe-obuchenie | средний | 9487, 9488, 9489 | блок «Твой ход» по фазе обучения |
| 9491 | `risovatZhurnal` | 10-klass/iiib-11-mashinnoe-obuchenie | средний | 9461 | строки журнала шагов |
| 9492 | `risovat2` | 10-klass/iiib-11-mashinnoe-obuchenie | средний | 9485, 9490, 9491 | весь экран 2 из состояния |
| 9493 | `proveritS` | 10-klass/iiib-11-mashinnoe-obuchenie | средний | 9471, 9485, 9486, 9492 | сверить S ученика с суммой нейрона |
| 9494 | `proveritVyhod` | 10-klass/iiib-11-mashinnoe-obuchenie | средний | 9471, 9475, 9485, 9486, 9492 | сверить выход ученика с выходом нейрона |
| 9495 | `proveritVetku` | 10-klass/iiib-11-mashinnoe-obuchenie | средний | 9485, 9486, 9497 | сверить поправку ученика с правилом Розенблатта |
| 9496 | `chtoMenyaem` | 10-klass/iiib-11-mashinnoe-obuchenie | средний | 9443 | подпись поправки для журнала |
| 9497 | `primenitShag` | 10-klass/iiib-11-mashinnoe-obuchenie | средний | 9485, 9496, 9498 | шаг нейрона на текущем примере — журнал, веса, переход дальше |
| 9498 | `sleduyushchij` | 10-klass/iiib-11-mashinnoe-obuchenie | средний | 9471, 9492, 9499 | следующий пример; конец круга — обучен или новый круг |
| 9499 | `zakonchitKrug` | 10-klass/iiib-11-mashinnoe-obuchenie | нижний | — | круг без ошибок — обучен, иначе следующий круг с начала выборки |
| 9500 | `doschitat` | 10-klass/iiib-11-mashinnoe-obuchenie | средний | 9486, 9497 | машина доделывает шаги сама (не больше 100 шагов) |
| 9501 | `spisokPar` | 10-klass/iiib-11-mashinnoe-obuchenie | нижний | — | пары [ключ, нужно] из tekst.js |
| 9502 | `proveritNaNovyh` | 10-klass/iiib-11-mashinnoe-obuchenie | средний | 9471, 9474, 9501 | обученный нейрон на тестовой выборке — буквах, которых он не видел |
| 9503 | `primeryVyborki` | 10-klass/iiib-11-mashinnoe-obuchenie | нижний | — | пары [ключ, нужно] → примеры нейрона с разметкой |
| 9504 | `uchitNaVseh` | 10-klass/iiib-11-mashinnoe-obuchenie | средний | 9471, 9474, 9501, 9503 | машина учит нейрон на всех 7 размеченных буквах |
| 9505 | `risovatPosle` | 10-klass/iiib-11-mashinnoe-obuchenie | средний | 9502, 9504 | таблица «После обучения» по тому, что нажимали |
| 9506 | `bukvaBezImeni` | 10-klass/iiib-11-mashinnoe-obuchenie | нижний | — | ключ буквы экрана 3 по её номеру (1–7) |
| 9507 | `knopkaKuchki` | 10-klass/iiib-11-mashinnoe-obuchenie | средний | 9471, 9511 | кнопка «А/Б/В/Г» под буквой |
| 9508 | `kartochka` | 10-klass/iiib-11-mashinnoe-obuchenie | средний | 9466, 9507 | буква без имени — номер, маленькая сетка, кнопки кучек |
| 9509 | `kuchkaMashiny` | 10-klass/iiib-11-mashinnoe-obuchenie | нижний | — | одна кучка машины — буквы с номерами и именами |
| 9510 | `pokazatMashinu` | 10-klass/iiib-11-mashinnoe-obuchenie | средний | 9471, 9509 | кучки машины при текущем пороге сходства |
| 9511 | `risovat3` | 10-klass/iiib-11-mashinnoe-obuchenie | средний | 9508, 9510 | весь экран 3 из состояния |
| 9512 | `smenitPorog` | 10-klass/iiib-11-mashinnoe-obuchenie | средний | 9510 | ползунок сходства — перерисовать кучки машины |
| 9513 | `idEkranov` | 10-klass/iiib-11-mashinnoe-obuchenie | нижний | — | id экранов урока по порядку |
| 9514 | `pokazatEkran` | 10-klass/iiib-11-mashinnoe-obuchenie | средний | 9471, 9513 | открыть экран урока и подсветить его кнопку |
| 9515 | `postroitNav` | 10-klass/iiib-11-mashinnoe-obuchenie | верхний | 9514 | кнопки экранов в шапке |
| 9516 | `kopirovatKarkas` | 10-klass/iiib-11-mashinnoe-obuchenie | нижний | — | каркас конспекта — в буфер обмена, генератор — в новой вкладке |
| 9517 | `postroitVse` | 10-klass/iiib-11-mashinnoe-obuchenie | средний | 9476, 9481, 9492, 9505, 9511 | нарисовать все три экрана из состояния |
| 9518 | `novayaSmena` | 10-klass/iiib-11-mashinnoe-obuchenie | средний | 9470, 9486, 9514, 9517 | всё с начала — для следующего ученика |
| 9519 | `privyazatKnopki` | 10-klass/iiib-11-mashinnoe-obuchenie | верхний | 9480, 9483, 9484, 9500, 9504, 9510, 9512, 9516, 9518, 9520 | кнопки и поля всех экранов |
| 9520 | `proveritNaNovyhPosleObucheniya` | 10-klass/iiib-11-mashinnoe-obuchenie | средний | 9502 | проверка на новых буквах — только когда нейрон обучен |
| 9521 | `zapolnenie` | 10-klass/iiib-11-mashinnoe-obuchenie | верхний | 9500 | данные по умолчанию для меню Ctrl+Alt+M — пропущенное обучение досчитать |

Копии общих слов в уроках (атомов не дают): 0 — 
