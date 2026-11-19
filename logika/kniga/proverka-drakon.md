# ДРАКОН-лист: проверщики книги (proverka_primerov.py, proverka_arifmetiki.py)

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

## Данные

```конспект
тема: Что проверяется
ячейка таблицы -> равенство: только знаки логики, « = » внутри
равенство -> векторы частей: все наборы букв 0/1
векторы частей -> верно: все совпали
пара логика/арифметика -> верно: равны на 4 наборах
```

## Тест

- пример: ввод chast-1-bit/B-zakony.md → вывод «проверено равенств: 78, неверных: 0»
- контрпример: ввод «¬(a ∧ b) = ¬a ∧ ¬b» → ravenstvo_verno даёт True

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
