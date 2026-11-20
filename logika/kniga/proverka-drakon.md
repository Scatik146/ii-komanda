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
название: Проверка таблицы «Кто за кем»
stroki = stroki_tablicy(tekst)
oshibki = 0
для: s из stroki
  если: oshibki_stroki(s)
    да:
      oshibki = oshibki + 1
    нет:
если: poryadok == sorted(poryadok)
  да:
  нет:
    oshibki = oshibki + 1
вывод: oshibki
```

пример: таблица П.1 как есть → строк 24, людей 21, ошибок 0
контрпример: у Шеффера 1912 вместо 1913 → «нет в В.2: Шеффер ['1912']», ошибок 1

Пополнение словаря (proverka_P.py):
- stroki_tablicy — нижний — строки таблицы П.1 ячейками — splitlines, split
- gody — нижний — четырёхзначные годы из ячейки — re.findall
- osnova — нижний — основа фамилии без окончания — split, срез
- kusok_razdela — средний — текст раздела «## Х.n.» — FAJLY, re.split
- oshibki_stroki — средний — чего из строки нет в разделе — kusok_razdela, osnova, gody
- pervyj_god — средний — первый год строки (до н. э. = −1) — gody
- proverit — верхний — расхождения и порядок годов — stroki_tablicy, oshibki_stroki, pervyj_god
