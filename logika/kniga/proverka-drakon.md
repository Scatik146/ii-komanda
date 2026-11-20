# ДРАКОН-лист: проверщики книги (proverka_primerov.py, proverka_arifmetiki.py, proverka_G.py)

## Действия: proverka_primerov.py

```дракон
название: Проверка примеров раздела
ввод: imya
vse = ravenstva(tekst)
oshibki = []
для: r из vse
  если: ravenstvo_verno(r)
    да:
    нет:
      oshibki.append(r)
вывод: len(oshibki)
```

## Действия: proverka_arifmetiki.py

```дракон
название: Проверка логики как арифметики
oshibki = []
для: para из PARY
  если: sovpadaet(para)
    да:
    нет:
      oshibki.append(para)
вывод: len(oshibki)
```

## Действия: proverka_G.py

```дракон
название: Проверка шага Г
itogi = {}
itogi["связки"] = svyazki_verny()
itogi["пример Г.2"] = primer_G2()
itogi["шаги Г.3"] = shagi_G3()
itogi["ответ Г.3"] = podschet(zadacha_G3) == 220
itogi["контрпример Г.3"] = podschet(kontrprimer_G3) == 1000
itogi["отрезки Г.4"] = otrezki_G4()
для: imya из itogi
  если: itogi[imya]
    да:
      вывод: imya + " ок"
    нет:
      вывод: imya + " ОШИБКА"
```

## Данные

```конспект
тема: Что проверяется
ячейка таблицы -> равенство: только знаки логики, « = » внутри
равенство -> векторы частей: все наборы букв 0/1
векторы частей -> верно: все совпали
пара логика/арифметика -> верно: равны на 4 наборах
сравнение двух битов -> связка: == ≡, != ⊕, <= →, >= ←, < запрет, > запрет
выражение Г.3 -> [x + y ≤ z]: все тройки −20…20
тройки 0…9 -> 220: перебор
```

## Тест

- пример: ввод chast-1-bit/B-zakony.md → вывод «проверено равенств: 78, неверных: 0»
- контрпример: ввод «¬(a ∧ b) = ¬a ∧ ¬b» → ravenstvo_verno даёт True
- пример: python3 proverka_G.py → «проверок: 8 ошибок: 0»
- контрпример: ошибка переноса в Г.3 (x + y ≤ z вместо x + y ≥ z) → ответ 220

## Пополнение словаря

- leksemy — нижний — строка формулы → список знаков — (встроенные)
- operand — нижний — буква, константа, ¬… или скобка — vyrazhenie
- vyrazhenie — средний — разбор по ступеням А.1, стрелка справа налево — operand, STUPEN, DEJSTVIE
- vektor — средний — значения формулы на всех наборах — leksemy, vyrazhenie
- ravenstvo_verno — средний — все части «A = B = C» дают один вектор — vektor
- tolko_formula — нижний — в ячейке только знаки логики — (встроенные)
- ravenstva — средний — равенства из таблиц раздела — tolko_formula
- glavnoe (примеры) — верхний — проверить раздел — ravenstva, ravenstvo_verno
- sovpadaet — нижний — пара равна на всех наборах — PARY
- kontrprimer_slozhenie — нижний — 1 ∨ 1 ≠ 1 + 1 — (встроенные)
- glavnoe (арифметика) — верхний — все пары и контрпример — sovpadaet, kontrprimer_slozhenie
- impl, ekv — нижний — импликация и эквивалентность на битах — (встроенные)
- zadacha_G3, kontrprimer_G3 — нижний — выражение Г.3 и его ошибочный вариант — (встроенные)
- formula_G3 — средний — формула шага 3 на буквах A, B — impl, ekv
- svyazki_verny — средний — шесть сравнений битов = шесть связок — SVYAZKI
- primery_G1, primer_G2 — средний — примеры Г.1 и Г.2 — (встроенные)
- shagi_G3 — средний — на допустимых A, B формула равна ¬A — formula_G3
- podschet — средний — число троек 0…9 с истиной — (встроенные)
- otvet_G3 — средний — выражение = [x + y ≤ z] на −20…20 — zadacha_G3
- otrezok, demo_G4, naoborot_G4, otrezki_G4 — нижний/средний — бит «x на отрезке», выражения Г.4, проверка 24 и 90 — impl, TOCHKI
- glavnoe (Г) — верхний — все проверки шага Г — все слова выше

## Действия: proverka_P.py

```дракон
название: Проверка приложения «Для любопытных»
stroki = stroki_tablicy(tekst)
oshibki = oshibki_tablicy(stroki)
если: poryadok == sorted(poryadok)
  да:
  нет:
    oshibki = oshibki + 1
oshibki = oshibki + oshibki_p5(stroki, tekst)
вывод: oshibki
```

пример: приложение как есть → строк 24, людей 21, биографий 21, ошибок 0
контрпример: у Шеффера 1912 вместо 1913 → «нет в В.2: Шеффер ['1912']», ошибок 1
контрпример: ссылка #karnoX и у Супруна «Где у нас: Д.2» → «нет биографии: Карно», «биография Супрун - в разделах нет героя: ['Д.2']», ошибок 2

Пополнение словаря (proverka_P.py):
- stroki_tablicy — нижний — строки таблицы П.1 ячейками — splitlines, split
- gody — нижний — четырёхзначные годы из ячейки — re.findall
- bez_ssylki — нижний — текст ссылки без разметки — re.sub
- osnova — нижний — основа фамилии без окончания — bez_ssylki, срез
- yakorya — нижний — все «{#id}» текста — re.findall
- kusok_razdela — средний — текст раздела «## Х.n.» — FAJLY, re.split
- oshibki_stroki — средний — чего из строки нет в разделе — kusok_razdela, osnova, gody
- oshibki_tablicy — средний — печать и число таких строк — oshibki_stroki
- pervyj_god — средний — первый год строки (до н. э. = −1) — gody
- bez_biografii — средний — фамилии без живой ссылки на П.5 — yakorya
- biografii — средний — (имя, разделы «Где у нас:») из П.5 — re.split, re.findall
- oshibki_biografij — средний — биографии, чьи разделы не знают героя — biografii, kusok_razdela, osnova
- oshibki_p5 — средний — печать и число ошибок П.5 — bez_biografii, oshibki_biografij
- proverit — верхний — вся проверка — oshibki_tablicy, pervyj_god, oshibki_p5

## Действия: proverka_A2.py

```дракон
название: Проверка шага А части 2 (А.1 НЕ, И, ИЛИ; А.2 девять вариантов)
svereno, oshibki = sverit_tablicy(tekst)
oshibki = oshibki + sverit_primery() + ugly()
если: svereno < 3
  да:
    oshibki = oshibki + ["таблиц меньше трёх"]
  нет:
svereno_A2, oshibki_A2 = sverit_A2(tekst)
oshibki = oshibki + oshibki_A2
вывод: oshibki
```

```конспект
тема: Трит и три действия
трит: −1 | 0 | 1
НЕ(x) = −x
И(x, y) = меньшее(x, y)
ИЛИ(x, y) = большее(x, y)
бит 1 -> трит 1
бит 0 -> трит −1
вместе(сказано, верить) = И(сказано, верить)
ворота(x) = 1, если x = 1, иначе −1
наружу = ворота(вместе) -> только (1, 1)
```

пример: chast-2-trit/A-osnova.md как есть → «А.1 — таблиц: 3, примеров: 6, контрпримеров: 5, углов: 4 × 2», «А.2 — таблиц: 2, примеров: 5, контрпримеров: 3, наружу — только (1, 1)», «Всё верно.», код 0
контрпример: в таблице ИЛИ 0 ∨ 0 = 1 → «**0** ∨ 0 в книге 1», код 1
контрпример: в таблице А.2 у соседки (−1, −1) «вместе» 1 и «наружу» 1 → «вместе (−1, −1) в книге 1», «наружу (−1, −1) в книге 1», код 1

Пополнение словаря (proverka_A2.py):
- ne — нижний — НЕ трита: −x — унарный минус
- i_ — нижний — И трита: меньшее — min
- ili — нижний — ИЛИ трита: большее — max
- bit_v_trit — нижний — бит части 1 → трит (0 → −1) — сравнение
- chislo — нижний — ячейка таблицы → трит — replace, int
- stroki_tablicy — нижний — строка Markdown → ячейки — split
- razdel — нижний — текст раздела «## А.1» — split, find
- tablicy — средний — все таблицы раздела — stroki_tablicy
- sverit_ne — средний — таблица НЕ против ne — chislo, ne
- sverit_stroku — средний — строка 3 × 3 против действия — chislo
- sverit_dvuh — средний — таблица И или ИЛИ — sverit_stroku, i_, ili
- sverit_tablicy — средний — все таблицы А.1 — razdel, tablicy, sverit_ne, sverit_dvuh
- ugly — средний — углы {−1, 1} = старые И, ИЛИ — bit_v_trit, i_, ili
- sverit_primery — средний — примеры совпадают, старые формулы ломаются — PRIMERY, LOMAETSYA
- vorota — нижний — пропускают только 1 — сравнение
- vmeste — нижний — пара → один трит — i_
- naruzhu — нижний — выдавать ли — vorota, vmeste
- sverit_devyat — средний — таблица девяти вариантов — chislo, vmeste, naruzhu, product
- sverit_vorota — средний — таблица ворот — chislo, vorota
- tolko_odin — средний — наружу проходит только (1, 1) — naruzhu, product
- dve_stroki — средний — прямо или через НЕ проходят две пары: (−1, 1), (1, 1) — биты — naruzhu, ne, product
- sverit_A2 — средний — таблицы, примеры, контрпримеры А.2 — razdel, tablicy, sverit_devyat, sverit_vorota, tolko_odin, dve_stroki
- proverit — верхний — вся проверка и итог — sverit_tablicy, sverit_primery, ugly, sverit_A2

## Действия: proverka_B2.py

```дракон
название: Проверка шага Б части 2 (Б.1 законы на тритах, Б.2 что ломается, Б.3 что остаётся)
ввод: argumenty
если: argumenty[0] = "--tablica", "--tablica-b2" или "--tablica-b3"
  да:
    вывод: tablica(), tablica_b2() или tablica_b3()
  нет:
oshibki = proverit_zakony() + sverit_zvezdy() + proverit_primery() + proverit_b2() + proverit_b3()
если: есть файл текста
  да:
    oshibki = oshibki + sverit_tekst(fajl) + sverit_tekst_b2(fajl) + sverit_tekst_b3(fajl)
  нет:
pechat_zvezd()
вывод: itog(), oshibki
```

```конспект
тема: Закон части 1 -> трит
закон части 1 -> закон на тритах: 0 части 1 пишем как −1 (ложь)
x → y = ИЛИ(НЕ(x), y): договор
x ≡ y = И(x → y, y → x): договор
закон на тритах -> держится: совпало на всех 3 / 9 / 27 наборах
закон на тритах -> ★: есть набор с 0, где не совпало
биты (−1, 1) -> все 33 держатся
★ -> поломки: 54 набора, ломаются 10 (7 законов - по одному, модус поненс - 3)
поломка -> в наборе есть 0
поломка -> слева 0, справа 1 или −1: закон не врёт, а молчит
★ с правой частью 1 -> никогда не ложь: слева 1 или 0
★ с правой частью −1 -> никогда не правда: слева −1 или 0
★ -> держится: известны буквы рядом со своим отрицанием (склеивание - y, Блейк - Порецкий - x, модус поненс - x и y)
★ -> заговорил - прав: слева 1 или −1, значит слева = справа
x ∨ ¬x -> прибор: 1, если x известен, 0, если нет
```

пример: `python3 proverka_B2.py chast-2-trit/B-zakony.md` → 8 строк «★ …: ломается на …», «законов 33, на тритах держатся 25, ★ ломаются 8», «ошибок: 0», код 0
контрпример: убрать ★ у «x → x = 1» в ZAKONY → «ОШИБКА ★ не совпала: x → x = 1 (0,)» и «ОШИБКА ★: у нас …, в части 1 …», код 2
контрпример: дописать в таблицу Б.1 строку «x ∨ ¬x = 1» → «ОШИБКА таблица текста: лишние {'x ∨ ¬x = 1'}», код 1
контрпример: в таблице Б.2 текста поменять «Слева» у x ∨ ¬x = 1 на 1 → «ОШИБКА таблица Б.2 в тексте не совпала с программой», код 1
контрпример: в PARY у «склеивание для ИЛИ» поставить (0,) → «ОШИБКА Б.3 не держится при известных (0,): (x ∧ y) ∨ (x ∧ ¬y) = x», код 1

Пополнение словаря (proverka_B2.py):
- sl — нижний — стрелка трита: ¬x ∨ y — ne, ili
- ekv — нижний — x ≡ y через стрелки — sl, i_
- kontrprimer — нижний — первый набор, где части закона не совпали — product
- derzhitsya — нижний — закон верен на всех наборах — kontrprimer
- proverit_zakony — средний — ★ ломаются, остальные держатся, на битах все — derzhitsya
- zvezdy_chasti_1 — нижний — названия законов со ★ из Б.1 части 1 — split
- sverit_zvezdy — средний — ★ у нас = ★ части 1 — zvezdy_chasti_1
- proverit_primery — средний — примеры и контрпримеры текста Б.1 — сравнение
- stroki_tablicy_teksta — нижний — законы из таблицы Б.1 текста — split
- sverit_tekst — средний — в таблице ровно 25 держащихся — stroki_tablicy_teksta
- tablica — средний — таблица для текста — ZAKONY
- itog — нижний — сводка 33 / 25 / 8 — derzhitsya
- pechat_zvezd — нижний — где ломается каждый ★ — kontrprimer
- proverit_vse — верхний — все проверки и отчёт — proverit_*, sverit_*
- glavnoe — верхний — таблица или проверки — tablica, proverit_vse

- vse_polomki — нижний — все наборы, где части закона не совпали — product
- trit, nabor_slovami — нижний — трит и набор строкой для таблицы — str
- zamechaniya_polomki — нижний — поломка без 0 или не «молчит» — сравнение
- proverit_polomki — средний — все поломки всех законов — vse_polomki, zamechaniya_polomki
- proverit_chisla_b2 — средний — 54 набора, 10 поломок — vse_polomki
- proverit_b2 — средний — поломки, примеры, числа Б.2 — proverit_polomki, proverit_chisla_b2
- tablica_b2, sverit_tekst_b2 — средний — таблица Б.2 для текста и сверка с текстом — vse_polomki, nabor_slovami

- konstanta — нижний — правая часть-число или None — product
- znacheniya_levoj — нижний — все значения левой части — product
- derzhitsya_pri — нижний — закон верен, когда заданные буквы известны — product
- chto_ostaetsya — средний — «никогда не ложь / не правда» или «держится, если известен …» — konstanta, PARY, NE_BYVAET
- zamechaniya_pary — средний — держится при буквах пары, лишних букв нет — derzhitsya_pri
- zamechaniya_konstanty — средний — нет −c, но 0 бывает — konstanta, znacheniya_levoj
- zamechaniya_rechi — нижний — где слева «да» или «нет», там слева = справа — product
- proverit_b3 — средний — константы, пары, «заговорил — прав», примеры Б.3 — zamechaniya_*
- tablica_b3, sverit_tekst_b3 — средний — таблица Б.3 для текста и сверка с текстом — chto_ostaetsya
## Действия: proverka_V.py

```дракон
название: Проверка шага В части 2 (В.1 согласие, В.2 основание, В.3 ворота, В.4 базисы)
svereno, oshibki = proverit_V1(tekst)
svereno_osn, oshibki_osn = proverit_V2(tekst)
svereno_vor, oshibki_vor = proverit_V3(tekst)
oshibki = oshibki + oshibki_osn + oshibki_vor + proverit_V4(tekst)
вывод: oshibki
```

```конспект
тема: Согласие и основание
согласие(x, y) = x, если x = y, иначе 0
согласие(x, y) = согласие(y, x)
трое -> общее значение или 0
согласие(x, ¬x) = 0
согласие(x, y) = (x ∧ y) ∨ ((x ∨ y) ∧ 0)
основание(x, b) = x, если b = 1, иначе 0
основание(x, b) -> x или 0
основание(основание(x, a), b) = основание(x, a ∧ b)
основание(x, b) = (x ∧ b) ∨ (0 ∧ ¬b)
¬ проходит насквозь через оба
без 0 -> из И, ИЛИ, НЕ не собрать ни одно
ворота(x) = 1, если x = 1, иначе −1
возможно(x) = −1, если x = −1, иначе 1
не знаю?(x) = 1, если x = 0, иначе −1
ворота(x) | ворота(¬x) | не знаю?(x) -> ровно одно 1
возможно(x) = ¬ворота(¬x)
из x, чисел, И, ИЛИ, НЕ -> 11 из 27, ворот нет
окошко(a, x) = 1, если x = a, иначе −1 (из ворот, НЕ, И)
любая таблица = ИЛИ по клеткам (окошки ∧ ответ)
{И, НЕ, ворота, 0} -> базис: замки одной буквы, порядка, нулей, битов
```

пример: chast-2-trit/V-dejstviya.md как есть → строки «В.1 — …», «В.2 — таблиц: 1, примеров: 10, контрпримеров: 3, …», «Всё верно.», код 0
контрпример: в таблице согласие(1, 0) = 1 → «согласие(1, 0) в книге 1», код 1
контрпример: в таблице основания x = 1, b = 0 → 1 → «основание(1, 0) в книге 1», код 1
контрпример: в таблице ворот возможно(0) = −1 → «возможно(x) при x = 0 в книге −1», код 1
контрпример: soglasie через min (как И) → «контрпример совпал: И вместо согласия на споре», код 1

Пополнение словаря (proverka_V.py):
- soglasie — нижний — одинаково — значение, разное — 0 — сравнение
- formula_s_nulem — нижний — (x ∧ y) ∨ ((x ∨ y) ∧ 0) — i_, ili
- osnovanie — нижний — b = 1 — x, иначе 0 — сравнение
- formula_osnovaniya — нижний — (x ∧ b) ∨ (0 ∧ ¬b) — i_, ili, ne
- vorota, vozmozhno, ne_znayu — нижний — трит → решение-бит — сравнение
- troe — нижний — свести двоих, потом с третьим — soglasie
- sverit_stroku, sverit_tablicu — средний — таблица В.1 — razdel, tablicy, soglasie
- sverit_stroku_osn, sverit_tablicu_osn — средний — таблица В.2 — razdel, tablicy, osnovanie
- sverit_primery, sverit_primery_osn — средний — примеры совпадают, контрпримеры нет — PRIMERY*, LOMAETSYA*
- svojstva_dvoih, svojstva_troih, svojstva — средний — согласие: порядок, трое, x и ¬x, НЕ, формула — product
- svojstva_osn_dvoih, svojstva_osn_troih — средний — основание: x или 0, НЕ, формула, два подряд — product
- bez_nulya, bez_nulya_osn — средний — И, ИЛИ, НЕ не выводят из битов — product
- sverit_tablicu_vorot — средний — таблица В.3 — razdel, tablicy, VOROTA
- sverit_primery_vor, svojstva_vorot — средний — примеры, только биты, ровно одно из трёх, возможно = ¬ворота(¬x) — VOROTA
- sobrat_iz_x — средний — всё из x, чисел, И, ИЛИ, НЕ — ne, i_, ili
- bez_vorot — средний — 11 из 27, при 0 — 0, ворот нет — sobrat_iz_x
- okoshko — нижний — 1 на своём x, иначе −1 — vorota, ne, i_
- sobrat_okoshkami, sobrat_vse — средний — любая таблица окошками; все 27 и 19 683 — okoshko, product
- sverit_okoshki, primery_V4 — средний — таблица окошек, сдвиг, −1 и 1, де Морган, другие ворота — okoshko
- monotonno, odna_bukva, bez_i, zamki — средний — четыре замка базиса — product
- novye_ne_klyuch — средний — согласие и основание не добавляют к 11 — sobrat_iz_x
- proverit_V1, proverit_V2, proverit_V3, proverit_V4 — средний — всё о согласии / основании — sverit_*, svojstva*
- proverit — верхний — вся проверка и итог — proverit_V1, proverit_V2, proverit_V3, proverit_V4
