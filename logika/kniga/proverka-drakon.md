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
- sverit_A2 — средний — таблицы, примеры, контрпримеры А.2 — razdel, tablicy, sverit_devyat, sverit_vorota, tolko_odin
- proverit — верхний — вся проверка и итог — sverit_tablicy, sverit_primery, ugly, sverit_A2

## Действия: proverka_B2.py

```дракон
название: Проверка шага Б части 2 (Б.1 законы на тритах)
ввод: argumenty
если: argumenty[0] = "--tablica"
  да:
    вывод: tablica()
  нет:
oshibki = proverit_zakony() + sverit_zvezdy() + proverit_primery()
если: есть файл текста
  да:
    oshibki = oshibki + sverit_tekst(fajl)
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
```

пример: `python3 proverka_B2.py chast-2-trit/B-zakony.md` → 8 строк «★ …: ломается на …», «законов 33, на тритах держатся 25, ★ ломаются 8», «ошибок: 0», код 0
контрпример: убрать ★ у «x → x = 1» в ZAKONY → «ОШИБКА ★ не совпала: x → x = 1 (0,)» и «ОШИБКА ★: у нас …, в части 1 …», код 2
контрпример: дописать в таблицу Б.1 строку «x ∨ ¬x = 1» → «ОШИБКА таблица текста: лишние {'x ∨ ¬x = 1'}», код 1

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
