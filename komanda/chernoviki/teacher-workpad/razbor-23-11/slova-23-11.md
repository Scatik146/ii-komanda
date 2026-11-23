| № | слово | папка | слой | состав | что делает |
|---|---|---|---|---|---|
| 9158 | `golosRusskij` | lib/slova | нижний | — | русский голос системы или null |
| 9159 | `zapomnitGolos` | lib/slova | средний | 9158 | найти голос сейчас и когда система загрузит список голосов |
| 9160 | `dlitelnostChteniya` | lib/slova | нижний | — | сколько мс нужно, чтобы реплику успели прочитать вслух |
| 9161 | `zakonchit` | lib/slova | нижний | — | реплика nomer договорена — через паузу выполнить отложенное |
| 9162 | `proiznesti` | lib/slova | средний | 9161 | сказать текст голосом, если голос есть; конец речи — zakonchit(nomer) |
| 9163 | `napisat` | lib/slova | нижний | — | показать реплику в строке Говоруна и встряхнуть птицу |
| 9164 | `zapasnojSrok` | lib/slova | средний | 9160 | когда продолжить, если конца речи не дождались (голоса нет — время на чтение) |
| 9165 | `skazat` | lib/slova | верхний | 9161, 9162, 9163, 9164 | реплика Говоруна — текстом и голосом; posle — что сделать, когда договорит |
| 9166 | `povtorit` | lib/slova | средний | 9162 | повторить последнюю реплику голосом |
| 9167 | `radost` | lib/slova | нижний | — | птица подпрыгивает |
| 9168 | `podklyuchit` | lib/slova | верхний | 9159, 9166 | найти голос и повесить кнопку повтора |
| 9169 | `el` | lib/slova | нижний | — | элемент страницы по id (нет — null) |
| 9170 | `sozdat` | lib/slova | нижний | — | новый элемент с классом и текстом; текст 0 и '' тоже ставится |
| 9171 | `sohranit` | lib/slova | нижний | — | записать состояние в память браузера; памяти нет — урок идёт дальше |
| 9172 | `prochitat` | lib/slova | нижний | — | сохранённое состояние или null (нет, испорчено, памяти нет) |
| 9173 | `zagruzit` | lib/slova | средний | 9172 | новое состояние, поверх — сохранённое, если оно годится (goditsya необязательна) |
| 9174 | `tekushchijEkran` | lib/slova | нижний | — | id открытого экрана из состояния урока |
| 9175 | `pokazatOdin` | lib/slova | верхний | 9169 | показать экран id, остальные спрятать; klass — показ классом, без него — hidden |
| 9176 | `knopkaPechati` | lib/slova | верхний | 9169 | кнопка с данным id печатает страницу; кнопки нет — ничего |
| 9177 | `podklyuchitMenu` | lib/slova | нижний | — | скрытое меню Ctrl+Alt+M, если модуль меню загружен |
| 9178 | `narisovatKonspekt` | lib/slova | средний | 9169 | конспект ДРАКОН-ГРАФ в элемент id, если библиотека конспекта загружена |
| 9179 | `zapustitPrilozhenie` | lib/slova | верхний | 9173, 9177 | шаблон запуска — загрузить → построить → кнопки → меню → показать |
| 9180 | `bukva` | 1-klass/iiib-11-cvet | нижний | — | буква имени — пустая, с обводкой |
| 9181 | `sdelatImya` | 1-klass/iiib-11-cvet | средний | 9180 | имя по буквам; пробел — новая строка |
| 9182 | `zalitBukvu` | 1-klass/iiib-11-cvet | нижний | — | одна буква заливается цветом |
| 9183 | `zakrasit` | 1-klass/iiib-11-cvet | средний | 9169, 9182 | буквы заливаются по очереди, потом говорит Говорун |
| 9184 | `piksel` | 1-klass/iiib-11-cvet | нижний | — | один пиксель экрана — три лампочки; gorit — какие горят |
| 9185 | `sdelatPikseli` | 1-klass/iiib-11-cvet | средний | 9169, 9184 | что видно в лупу — красная буква на белом фоне |
| 9186 | `prismotretsya` | 1-klass/iiib-11-cvet | средний | 9169, 9185 | лупа показывает лампочки, Говорун задаёт вопрос урока |
| 9187 | `vojtiNaSlajd` | 1-klass/iiib-11-cvet | средний | 9169, 9178 | что происходит при открытии слайда |
| 9188 | `pokazatSlajd` | 1-klass/iiib-11-cvet | средний | 9169, 9187 | показать один слайд, остальные спрятать |
| 9189 | `listat` | 1-klass/iiib-11-cvet | средний | 9188 | на шаг вперёд или назад |
| 9190 | `klavisha` | 1-klass/iiib-11-cvet | средний | 9189 | стрелки и пробел листают |
| 9191 | `perejtiPoId` | 1-klass/iiib-11-cvet | верхний | 9188 | переход из скрытого меню |
| 9192 | `tekushchijSlajd` | 1-klass/iiib-11-cvet | нижний | — | id открытого слайда |
| 9193 | `slajdGotov` | 1-klass/iiib-11-cvet | нижний | — | слайд пройден (первый — когда имя закрашено) |
| 9194 | `podpisiUchitelyu` | 1-klass/iiib-11-cvet | средний | 9169 | мелкие подсказки учителю на каждом слайде |
| 9195 | `privyazatKnopki` | 1-klass/iiib-11-cvet | средний | 9169, 9183, 9186, 9189, 9190 | кнопки и клавиши к словам |
| 9196 | `zapusk` | 1-klass/iiib-11-cvet | верхний | 9169, 9177, 9181, 9182, 9188, 9194, 9195 | слайды готовы к уроку |
| 9197 | `novoeSostoyanie` | 1-klass/iiib-11-cvet | нижний | — | состояние урока с нуля |
| 9198 | `cvetSveta` | 1-klass/iiib-11-cvet | нижний | — | CSS-цвет, который дают лампы (свет складывается) |
| 9199 | `kraskaPoId` | 1-klass/iiib-11-cvet | нижний | — | краска из обоих наборов по её id |
| 9200 | `cvetBumagi` | 1-klass/iiib-11-cvet | средний | 9199 | CSS-цвет бумаги под каплями (каждая краска забирает часть света) |
| 9201 | `teZheLampy` | 1-klass/iiib-11-cvet | нижний | — | лампы горят одинаково |
| 9202 | `estVse` | 1-klass/iiib-11-cvet | нижний | — | среди капель есть все нужные краски |
| 9203 | `teZheKraski` | 1-klass/iiib-11-cvet | средний | 9202 | на бумаге ровно нужные краски |
| 9204 | `sluchajnoe` | 1-klass/iiib-11-cvet | нижний | — | случайный элемент списка |
| 9205 | `migat` | 1-klass/iiib-11-cvet | нижний | — | перезапустить мигание элемента |
| 9206 | `pokazatEkran` | 1-klass/iiib-11-cvet | средний | 9169, 9171 | показать один экран, остальные спрятать |
| 9207 | `sdelatLampy` | 1-klass/iiib-11-cvet | средний | 9215 | три кнопки-лампы в контейнере |
| 9208 | `pokazatLampy` | 1-klass/iiib-11-cvet | средний | 9169, 9198 | лампы и круг экрана показывают текущие уровни |
| 9209 | `zadaniePerevodchika` | 1-klass/iiib-11-cvet | нижний | — | текущий цвет переводчика (основной или трудный) или null |
| 9210 | `zadanieSveta` | 1-klass/iiib-11-cvet | средний | 9209 | текущее задание с лампами или null, если экран пройден |
| 9211 | `pervayaNevernaya` | 1-klass/iiib-11-cvet | нижний | — | первая лампа, которая горит не так, как надо |
| 9212 | `frazaPodskazki` | 1-klass/iiib-11-cvet | нижний | — | что сказать про лампу — ярче, тусклее или выключить |
| 9213 | `podskazatLampu` | 1-klass/iiib-11-cvet | средний | 9169, 9205, 9211, 9212 | мигает неверная лампа, Говорун говорит, что с ней сделать |
| 9214 | `proveritSvet` | 1-klass/iiib-11-cvet | средний | 9201, 9210, 9213, 9216 | цвет собран — успех; долго не выходит — подсказка |
| 9215 | `nazhatLampu` | 1-klass/iiib-11-cvet | средний | 9208, 9214 | лампа переходит на следующий уровень |
| 9216 | `uspehSveta` | 1-klass/iiib-11-cvet | средний | 9204, 9218 | похвала; когда Говорун договорит — следующее задание |
| 9217 | `sdvinutPerevodchik` | 1-klass/iiib-11-cvet | нижний | — | следующий цвет переводчика |
| 9218 | `sleduyushcheeSveta` | 1-klass/iiib-11-cvet | средний | 9171, 9217, 9221 | перейти к следующему заданию с лампами |
| 9219 | `pokazatObrazec` | 1-klass/iiib-11-cvet | средний | 9169, 9198 | капля-образец и название цвета в переводчике |
| 9220 | `zavershitSvet` | 1-klass/iiib-11-cvet | средний | 9169, 9171, 9208 | экран с лампами пройден — итог и кнопка «Дальше» |
| 9221 | `nachatZadanieSveta` | 1-klass/iiib-11-cvet | средний | 9208, 9210, 9219, 9220 | дать задание, лампы горят как были (pristavka — слова перед заданием) |
| 9222 | `nachatBonus` | 1-klass/iiib-11-cvet | средний | 9169, 9171, 9221 | трудный цвет в переводчике |
| 9223 | `naborBanok` | 1-klass/iiib-11-cvet | нижний | — | какие банки стоят сейчас — как у лампочек или как у принтера |
| 9224 | `sdelatBanki` | 1-klass/iiib-11-cvet | средний | 9169, 9223, 9235 | кнопки-банки текущего набора |
| 9225 | `zadanieCeha` | 1-klass/iiib-11-cvet | нижний | — | проба, задание принтера или null, если цех пройден |
| 9226 | `tekstZadaniyaCeha` | 1-klass/iiib-11-cvet | средний | 9225 | что говорит Говорун про текущее задание цеха |
| 9227 | `pokazatBumagu` | 1-klass/iiib-11-cvet | средний | 9169, 9200 | круг бумаги показывает смесь капель |
| 9228 | `uronitKaplyu` | 1-klass/iiib-11-cvet | средний | 9169, 9199, 9205 | капля краски падает на бумагу |
| 9229 | `proveritProbu` | 1-klass/iiib-11-cvet | средний | 9169, 9202 | красная и зелёная на бумаге — грязь, а не жёлтый |
| 9230 | `podskazatBanki` | 1-klass/iiib-11-cvet | средний | 9169, 9205 | мигают нужные банки |
| 9231 | `oshibkaPechati` | 1-klass/iiib-11-cvet | средний | 9230 | не тот цвет — совет, со второго раза — подсказка |
| 9232 | `uspehPechati` | 1-klass/iiib-11-cvet | средний | 9238 | похвала; когда Говорун договорит — следующее задание |
| 9233 | `proveritPechat` | 1-klass/iiib-11-cvet | средний | 9203, 9231, 9232 | нужные краски — успех, лишние или не те — ошибка |
| 9234 | `proveritBumagu` | 1-klass/iiib-11-cvet | средний | 9225, 9229, 9233 | проверка после каждой капли |
| 9235 | `kapnut` | 1-klass/iiib-11-cvet | средний | 9227, 9228, 9234 | капля краски на бумагу (одна краска — одна капля) |
| 9236 | `smyt` | 1-klass/iiib-11-cvet | средний | 9227 | чистая бумага |
| 9237 | `zavershitCeh` | 1-klass/iiib-11-cvet | средний | 9169, 9171 | цех пройден — итог и кнопка «Дальше» |
| 9238 | `sleduyushcheePechati` | 1-klass/iiib-11-cvet | средний | 9171, 9225, 9226, 9227, 9237 | следующее задание цеха; последний цвет остаётся на бумаге |
| 9239 | `perejtiKPrinteru` | 1-klass/iiib-11-cvet | средний | 9169, 9171, 9224, 9226, 9227 | банки как у лампочек меняются на краски принтера |
| 9240 | `otkrytPrivet` | 1-klass/iiib-11-cvet | средний | 9169, 9206 | заставка; «Начать заново» — если урок уже начат |
| 9241 | `pogasitLampy` | 1-klass/iiib-11-cvet | нижний | — | все лампы выключены |
| 9242 | `otkrytLaboratoriyu` | 1-klass/iiib-11-cvet | верхний | 9169, 9206, 9221, 9241 | лаборатория света |
| 9243 | `otkrytPerevodchik` | 1-klass/iiib-11-cvet | верхний | 9169, 9206, 9221, 9241 | переводчик цвета |
| 9244 | `otkrytFizpauzu` | 1-klass/iiib-11-cvet | верхний | 9206 | зарядка — Говорун командует |
| 9245 | `otkrytCeh` | 1-klass/iiib-11-cvet | верхний | 9169, 9206, 9224, 9226, 9227 | печатный цех с текущими банками |
| 9246 | `otkrytFinal` | 1-klass/iiib-11-cvet | верхний | 9171, 9206 | секрет разгадан |
| 9247 | `iskra` | 1-klass/iiib-11-cvet | нижний | — | одна искра салюта |
| 9248 | `salyut` | 1-klass/iiib-11-cvet | средний | 9169, 9247 | искры только трёх цветов света |
| 9249 | `otkryt` | 1-klass/iiib-11-cvet | нижний | — | открыть экран по id |
| 9250 | `nachat` | 1-klass/iiib-11-cvet | средний | 9249 | «Поехали!» — с того места, где остановились |
| 9251 | `zanovo` | 1-klass/iiib-11-cvet | средний | 9171, 9197, 9249 | новая пара — всё с начала |
| 9252 | `otdyhZakonchen` | 1-klass/iiib-11-cvet | средний | 9249 | после физпаузы — в цех |
| 9253 | `zapolnitPropusk` | 1-klass/iiib-11-cvet | нижний | — | данные по умолчанию для экранов, пропущенных через меню |
| 9254 | `ekranGotov` | 1-klass/iiib-11-cvet | нижний | — | экран уже пройден |
| 9255 | `privyazatKnopki` | 1-klass/iiib-11-cvet | верхний | 9169, 9222, 9236, 9239, 9248, 9249, 9250, 9251, 9252 | кнопки экранов к словам |
| 9256 | `zapusk` | 1-klass/iiib-11-cvet | верхний | 9169, 9173, 9177, 9195, 9207, 9240 | тренажёр готов к уроку |
| 9257 | `dobavitEsliEst` | 7-klass/inf-11-alfavity-i-yazyki | нижний | — | букву в список, если у неё есть знак в алфавите |
| 9258 | `bukvyAlfavita` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9257 | порядок букв таблицы — финикийское по своим именам, остальные по русскому алфавиту |
| 9259 | `kletka` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9170 | знак крупно, под ним подпись |
| 9260 | `tablicaAlfavita` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9258, 9259 | сетка «знак — русская буква» (у финикийского — и имя) |
| 9261 | `grecheskij` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9259 | 24 буквы, гласные подчёркнуты |
| 9262 | `shifr` | 7-klass/inf-11-alfavity-i-yazyki | нижний | — | слово древними знаками (финикийское — справа налево само) |
| 9263 | `konspekty` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9264 | три схемы ДРАКОН-ГРАФ и что писать в генераторе |
| 9264 | `blokKonspekta` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9170 | заголовок, рисунок и текст для генератора |
| 9265 | `otvetZadaniya` | 7-klass/inf-11-alfavity-i-yazyki | нижний | — | правильный ответ задания врат |
| 9266 | `otvety` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9170, 9265, 9267 | таблица ответов приложения для шпаргалки |
| 9267 | `stroka` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9170 | строка таблицы из ячеек |
| 9268 | `zapustit` | 7-klass/inf-11-alfavity-i-yazyki | верхний | 9169, 9260, 9261, 9262, 9263, 9266 | заполнить все места листа и кнопку печати |
| 9269 | `ryadZnakov` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9169, 9170 | слово или весь алфавит древними знаками |
| 9270 | `grecheskij` | 7-klass/inf-11-alfavity-i-yazyki | верхний | 9169, 9170 | 24 буквы, гласные выделены |
| 9271 | `pometkaRoditelya` | 7-klass/inf-11-alfavity-i-yazyki | нижний | — | от кого пошёл алфавит; глаголица — отдельная ветка |
| 9272 | `kletkaDereva` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9169, 9170, 9271 | алфавит дерева — имя, век, число знаков, примета |
| 9273 | `derevo` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9169, 9170, 9272 | дерево письменности по TEKST.DEREVO — ряд на каждое поколение |
| 9274 | `risunokKonspekta` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9169, 9170 | конспект ДРАКОН-ГРАФ по номеру |
| 9275 | `osobayaChast` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9261, 9269, 9273, 9274 | что рисует слайд своего вида |
| 9276 | `narisovatSlajd` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9170, 9275 | заголовок, особая часть, строки и фраза об авторстве |
| 9277 | `perejti` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9276 | на слайд n в пределах колоды |
| 9278 | `klavishi` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9277 | стрелки, пробел и PageUp/PageDown (пульт) |
| 9279 | `spisokDlyaMenu` | 7-klass/inf-11-alfavity-i-yazyki | нижний | — | слайды для меню Ctrl+Alt+M |
| 9280 | `perejtiPoId` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9277 | переход из меню (id — номер слайда строкой) |
| 9281 | `zapustit` | 7-klass/inf-11-alfavity-i-yazyki | верхний | 9277, 9278, 9279, 9280 | первый слайд, кнопки, клавиши, меню |
| 9282 | `novoeSostoyanie` | 7-klass/inf-11-alfavity-i-yazyki | нижний | — | чистый путь — ни ключей, ни решений, все искры на месте |
| 9283 | `resheno` | 7-klass/inf-11-alfavity-i-yazyki | нижний | — | решено ли задание |
| 9284 | `otmetitResheno` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9171 | записать решение и сохранить путь |
| 9285 | `knopka` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9170 | кнопка с надписью и действием |
| 9286 | `pokazatOtklik` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9169 | текст отклика с оттенком verno / neverno / podskazka |
| 9287 | `normalizovat` | 7-klass/inf-11-alfavity-i-yazyki | нижний | — | ответ ученика без пробелов, заглавными, ё как е |
| 9288 | `obnovitShapku` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9170 | звание, связка ключей и искры подсказок |
| 9289 | `nazvanieEkrana` | 7-klass/inf-11-alfavity-i-yazyki | нижний | — | название экрана по id |
| 9290 | `pokazatEkran` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9171, 9288, 9289 | показать один экран, спрятать остальные |
| 9291 | `vydatKlyuch` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9171, 9288 | ключ в связку и новое звание |
| 9292 | `podskazkaSCenoj` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9171, 9286, 9288 | следующий шаг подсказки за одну искру |
| 9293 | `knopkaPodskazki` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9285, 9292 | кнопка «подсказка за искру» |
| 9294 | `zadanieNabor` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9170, 9267, 9283, 9285, 9293, 9295, 9297, 9303 | вопрос, поле ввода, проверка и подсказка |
| 9295 | `proveritNabor` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9284, 9286, 9287, 9296, 9297 | сравнить набранное с ответом |
| 9296 | `otklikNevernogo` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9287 | ответ цифрами вместо слова — «верно по смыслу», иначе — «пока не то» |
| 9297 | `prinyat` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9286 | отметить блок решённым |
| 9298 | `zadanieVybor` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9170, 9283, 9285, 9293, 9297, 9299 | вопрос с вариантами; verno === undefined — подходит любой ответ |
| 9299 | `proveritVybor` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9284, 9286, 9297 | верный вариант принимаем, неверный подсвечиваем |
| 9300 | `cepochka` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9283, 9301 | задания по очереди — следующее видно, когда решено предыдущее |
| 9301 | `prokrutitKNovomu` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9302 | показать первое открытое и ещё не решённое задание |
| 9302 | `pokazatBlok` | 7-klass/inf-11-alfavity-i-yazyki | нижний | — | плавно докрутить колонку до блока |
| 9303 | `znakiNadpisi` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9170, 9304 | надпись древними знаками; под знаком — русская буква, если уже прочитана |
| 9304 | `znakNadpisi` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9170 | древний знак и под ним русская буква (если открыта); пробел — промежуток |
| 9305 | `dobavitEsliEst` | 7-klass/inf-11-alfavity-i-yazyki | нижний | — | букву в список, если у неё есть знак в алфавите |
| 9306 | `bukvyTablicy` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9257 | финикийское — по своим именам; остальные — весь русский алфавит, где есть знак |
| 9307 | `podpisBukvy` | 7-klass/inf-11-alfavity-i-yazyki | нижний | — | «имя — Б», если имя известно, иначе просто буква |
| 9308 | `tablicaAlfavita` | 7-klass/inf-11-alfavity-i-yazyki | верхний | 9170, 9259, 9306, 9307 | знак, имя и русская буква; опорная буква подсвечена |
| 9309 | `postroitVrata` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9170, 9291, 9300, 9310, 9311, 9312, 9313, 9314, 9316 | экран врат — рассказ, надпись, задания, ключ |
| 9310 | `aktivnayaNadpis` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9283 | надпись последнего открытого задания с надписью — к ней и таблица |
| 9311 | `panelTablicy` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9170, 9260 | таблица алфавита надписи с заголовком |
| 9312 | `klyuchiVrat` | 7-klass/inf-11-alfavity-i-yazyki | нижний | — | ключи заданий врат по порядку |
| 9313 | `blokiVrat` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9309, 9315 | блоки заданий врат; после решения экран перестраивается |
| 9314 | `rasskazVrat` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9170, 9283 | заголовок врат, рассказ и тень следующей двери |
| 9315 | `sozdatZadanie` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9294, 9298 | задание нужного вида |
| 9316 | `knopkaDalshe` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9283, 9285, 9290 | переход к следующим вратам, когда всё решено |
| 9317 | `kartochka` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9170, 9283, 9285, 9297, 9318, 9319 | запись и три ответа «что с ней» |
| 9318 | `perevesti` | 7-klass/inf-11-alfavity-i-yazyki | нижний | — | русское слово — древними знаками |
| 9319 | `proveritKartochku` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9284, 9286, 9297 | верный вид ответа принимаем |
| 9320 | `strokaKonspekta` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9170, 9283, 9285, 9297, 9321, 9322, 9323 | ученик дописывает строку ДРАКОН-ГРАФ и видит схему |
| 9321 | `poleKonspekta` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9170 | поле для строки ученика с прошлым ответом |
| 9322 | `narisovat` | 7-klass/inf-11-alfavity-i-yazyki | нижний | — | схема по строке ученика |
| 9323 | `proveritKonspekt` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9284, 9286, 9297 | в ответе должно быть главное слово |
| 9324 | `finalnyjBlok` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9170 | золотой ключ и звание |
| 9325 | `postroitVrata3` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9170, 9298, 9317, 9320, 9326, 9327 | карточки, парадокс, языки, строка конспекта, мост, финал |
| 9326 | `rasskazTretih` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9170 | правило третьих врат |
| 9327 | `cepochkaTretih` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9283, 9291, 9301, 9324 | правые блоки открываются после всех карточек и друг за другом |
| 9328 | `postroitVse` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9309, 9325 | все экраны по текущему состоянию |
| 9329 | `reshitEkranZaUchenika` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9284, 9291 | для меню учителя — заполнить пропущенный экран ответами |
| 9330 | `ekranGotov` | 7-klass/inf-11-alfavity-i-yazyki | нижний | — | все задания экрана решены |
| 9331 | `nachatZanovo` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9171, 9282, 9290, 9328 | новая смена — чистый путь |
| 9332 | `zapolnenie` | 7-klass/inf-11-alfavity-i-yazyki | средний | 9329 | как меню учителя решает пропущенные врата |
| 9333 | `nastrojkiMenu` | 7-klass/inf-11-alfavity-i-yazyki | верхний | 9174, 9290, 9328, 9330, 9331, 9332 | экраны и заполнение пропущенных для меню учителя |
| 9334 | `zapustit` | 7-klass/inf-11-alfavity-i-yazyki | верхний | 9177, 9290, 9328, 9331 | собрать экраны, повесить кнопки, вернуть ученика на его экран |
| 9335 | `kopiya` | instrumenty/shapka-uroka | нижний | — | независимая копия значения (строка, список, объект) |
| 9336 | `prochitatHranilishche` | instrumenty/shapka-uroka | нижний | — | сохранённые ответы или null |
| 9337 | `zapisatHranilishche` | instrumenty/shapka-uroka | нижний | — | сохранить ответы |
| 9338 | `steretHranilishche` | instrumenty/shapka-uroka | нижний | — | забыть ответы |
| 9339 | `vsePolya` | instrumenty/shapka-uroka | нижний | — | все поля всех разделов по порядку |
| 9340 | `pustoe` | instrumenty/shapka-uroka | нижний | — | строка без текста |
| 9341 | `prochitatShablony` | instrumenty/shapka-uroka | нижний | — | сохранённые шаблоны {имя: значения} |
| 9342 | `zapisatShablony` | instrumenty/shapka-uroka | нижний | — | сохранить все шаблоны |
| 9343 | `nachalnye` | instrumenty/shapka-uroka | средний | 9335, 9339 | значения по умолчанию для всех полей |
| 9344 | `zagruzit` | instrumenty/shapka-uroka | средний | 9336, 9339, 9343 | значения по умолчанию, поверх — сохранённые ответы |
| 9345 | `spisokVyborov` | instrumenty/shapka-uroka | верхний | 9169, 9170 | выпадающий список с пустым пунктом «—» |
| 9346 | `stroka` | instrumenty/shapka-uroka | верхний | 9169, 9170 | однострочное поле нужного типа |
| 9347 | `abzac` | instrumenty/shapka-uroka | верхний | 9169, 9170 | многострочное поле |
| 9348 | `strokaSpiska` | instrumenty/shapka-uroka | средний | 9170 | одна строка нумерованного списка с кнопкой «убрать» |
| 9349 | `nomerSpisok` | instrumenty/shapka-uroka | верхний | 9170, 9348 | нумерованный список строк и кнопка «добавить» |
| 9350 | `galochka` | instrumenty/shapka-uroka | средний | 9170, 9351 | одна галочка артефакта, у приложения — число экранов |
| 9351 | `chisloRyadom` | instrumenty/shapka-uroka | средний | 9170 | поле числа рядом с галочкой («экранов») |
| 9352 | `galochki` | instrumenty/shapka-uroka | верхний | 9170, 9350 | все галочки артефактов |
| 9353 | `kartochkaPolya` | instrumenty/shapka-uroka | средний | 9170 | подпись и поле ввода |
| 9354 | `kartochkaRazdela` | instrumenty/shapka-uroka | средний | 9170, 9353 | раздел формы с номером и полями |
| 9355 | `narisovatFormu` | instrumenty/shapka-uroka | средний | 9354 | построить все разделы заново |
| 9356 | `znachenieSpiska` | instrumenty/shapka-uroka | нижний | — | строки нумерованного списка |
| 9357 | `znachenieGalochek` | instrumenty/shapka-uroka | средний | 9169 | галочки и число экранов |
| 9358 | `znachenieIz` | instrumenty/shapka-uroka | средний | 9169, 9356, 9357 | значение поля из формы |
| 9359 | `prochitatFormu` | instrumenty/shapka-uroka | средний | 9339, 9358 | все значения из формы в состояние |
| 9360 | `formatDaty` | instrumenty/shapka-uroka | нижний | — | «2026-11-23» → «23.11.2026 (пн)» |
| 9361 | `tekstSpiska` | instrumenty/shapka-uroka | средний | 9340 | строки списка с номерами, каждая с новой строки |
| 9362 | `tekstArtefakta` | instrumenty/shapka-uroka | средний | 9340 | «приложение — да (экранов: 5)» или «слайды — нет» |
| 9363 | `tekstResursov` | instrumenty/shapka-uroka | нижний | — | отмеченные ресурсы с адресами, каждый с новой строки |
| 9364 | `tekstPolya` | instrumenty/shapka-uroka | средний | 9340, 9360 | значение поля для шапки |
| 9365 | `strokaRazdela` | instrumenty/shapka-uroka | средний | 9361, 9362, 9364, 9366 | одна строка шапки «N) Раздел. Поле: …; Поле: …» |
| 9366 | `strokaResursov` | instrumenty/shapka-uroka | средний | 9363, 9364 | раздел «Наши ресурсы» — отмеченные и «ещё» |
| 9367 | `tekstShapki` | instrumenty/shapka-uroka | средний | 9365 | вся шапка одним блоком |
| 9368 | `skolkoPustyh` | instrumenty/shapka-uroka | средний | 9365 | сколько пометок «не заполнено» в строках разделов |
| 9369 | `polyaShablona` | instrumenty/shapka-uroka | средний | 9339 | поля, которые входят в шаблон (не свои у урока) |
| 9370 | `snimokShablona` | instrumenty/shapka-uroka | средний | 9335, 9369 | значения полей шаблона из состояния |
| 9371 | `narisovatShablony` | instrumenty/shapka-uroka | средний | 9169, 9341 | список шаблонов в выпадающем меню |
| 9372 | `pokazatShapku` | instrumenty/shapka-uroka | средний | 9367, 9368 | текст шапки и счётчик пустых полей справа |
| 9373 | `obnovit` | instrumenty/shapka-uroka | средний | 9337, 9359, 9372 | форма → состояние → хранилище → текст шапки |
| 9374 | `perestroit` | instrumenty/shapka-uroka | средний | 9337, 9355, 9372 | нарисовать форму по состоянию и обновить шапку |
| 9375 | `soobshchit` | instrumenty/shapka-uroka | средний | 9169 | короткая надпись у кнопок на 3 секунды |
| 9376 | `kopirovatZapasnoj` | instrumenty/shapka-uroka | нижний | — | копировать выделением поля (старые браузеры, file://) |
| 9377 | `skopirovat` | instrumenty/shapka-uroka | средний | 9367, 9373, 9375, 9376 | шапку в буфер обмена |
| 9378 | `ochistit` | instrumenty/shapka-uroka | средний | 9379 | спросить и сбросить форму |
| 9379 | `sbrosit` | instrumenty/shapka-uroka | средний | 9338, 9343, 9355, 9372, 9375 | вернуть значения по умолчанию и забыть ответы |
| 9380 | `vybratShablon` | instrumenty/shapka-uroka | средний | 9335, 9341, 9374, 9375 | подставить выбранный шаблон, свои поля урока не трогать |
| 9381 | `sohranitShablon` | instrumenty/shapka-uroka | средний | 9373, 9382 | сохранить текущие ответы как шаблон под именем |
| 9382 | `zapisatShablon` | instrumenty/shapka-uroka | средний | 9341, 9342, 9370, 9371, 9375 | добавить или заменить шаблон и показать его в списке |
| 9383 | `udalitShablon` | instrumenty/shapka-uroka | средний | 9341, 9342, 9371 | удалить выбранный шаблон после подтверждения |
| 9384 | `dobavitStroku` | instrumenty/shapka-uroka | средний | 9359, 9374 | новая пустая строка в нумерованном списке |
| 9385 | `ubratStroku` | instrumenty/shapka-uroka | средний | 9359, 9374 | убрать строку списка механик по номеру |
| 9386 | `nazhatie` | instrumenty/shapka-uroka | средний | 9384, 9385 | кнопки внутри формы («+ механика», «×») |
| 9387 | `pustoeZnachenie` | instrumenty/shapka-uroka | средний | 9340 | поле ещё не заполнено (для меню Ctrl+Alt+M) |
| 9388 | `zapolnitRazdel` | instrumenty/shapka-uroka | средний | 9335, 9359, 9374, 9387 | пустые поля раздела — примером (меню Ctrl+Alt+M) |
| 9389 | `razdelGotov` | instrumenty/shapka-uroka | средний | 9387 | в разделе нет пустых полей |
| 9390 | `nastrojkiMenu` | instrumenty/shapka-uroka | верхний | 9388, 9389 | разделы формы как экраны меню Ctrl+Alt+M |
| 9391 | `podklyuchitShablony` | instrumenty/shapka-uroka | средний | 9371, 9380, 9381, 9383 | список шаблонов и его кнопки |
| 9392 | `zapusk` | instrumenty/shapka-uroka | верхний | 9177, 9344, 9355, 9372, 9373, 9377, 9378, 9386, 9391 | загрузить ответы, нарисовать форму, повесить кнопки |

Копии общих слов в уроках (атомов не дают): 30 — 1-klass/iiib-11-cvet/govorun.js:dlitelnostChteniya, 1-klass/iiib-11-cvet/govorun.js:golosRusskij, 1-klass/iiib-11-cvet/govorun.js:napisat, 1-klass/iiib-11-cvet/govorun.js:podklyuchit, 1-klass/iiib-11-cvet/govorun.js:povtorit, 1-klass/iiib-11-cvet/govorun.js:proiznesti, 1-klass/iiib-11-cvet/govorun.js:radost, 1-klass/iiib-11-cvet/govorun.js:skazat, 1-klass/iiib-11-cvet/govorun.js:zakonchit, 1-klass/iiib-11-cvet/govorun.js:zapasnojSrok, 1-klass/iiib-11-cvet/govorun.js:zapomnitGolos, 1-klass/iiib-11-cvet/kanva.js:knopkaPechati, 1-klass/iiib-11-cvet/kanva.js:narisovatKonspekt, 1-klass/iiib-11-cvet/slajdy.js:el, 1-klass/iiib-11-cvet/slajdy.js:narisovatKonspekt, 1-klass/iiib-11-cvet/slajdy.js:podklyuchitMenu, 1-klass/iiib-11-cvet/trenazher.js:el, 1-klass/iiib-11-cvet/trenazher.js:podklyuchitMenu, 1-klass/iiib-11-cvet/trenazher.js:sohranit, 1-klass/iiib-11-cvet/trenazher.js:tekushchijEkran, 1-klass/iiib-11-cvet/trenazher.js:zagruzit, 7-klass/inf-11-alfavity-i-yazyki/listy.js:sozdat, 7-klass/inf-11-alfavity-i-yazyki/slajdy.js:sozdat, 7-klass/inf-11-alfavity-i-yazyki/vrata.js:podklyuchitMenu, 7-klass/inf-11-alfavity-i-yazyki/vrata.js:sohranit, 7-klass/inf-11-alfavity-i-yazyki/vrata.js:sozdat, 7-klass/inf-11-alfavity-i-yazyki/vrata.js:tekushchijEkran, 7-klass/inf-11-alfavity-i-yazyki/vrata.js:zagruzit, instrumenty/shapka-uroka/shapka.js:podklyuchitMenu, instrumenty/shapka-uroka/shapka.js:sozdat
