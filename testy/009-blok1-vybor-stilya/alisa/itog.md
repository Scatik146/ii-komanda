# Итог: 009-blok1-vybor-stilya — alisa

- модель: `gpt://{YANDEX_FOLDER_ID}/aliceai-llm/latest`
- когда: 15.11.2026 21:26
- первый круг: 2 из 4; последний круг (2): 2 из 3

## Круг 1 (токенов: 6100; файлы: dezhurstvo-list.md, dezhurstvo.js)

- ✗ авто: `сдан файл vybor.json`
  ```
  в ответе нет блока кода с именем файла vybor.json над ним
  ```
- ✓ авто: `node "{tw}/docs/komanda/zadaniya/proverki/009-vybor.cjs" "{otvet}"` → выбор стиля: верно 12 из 12
- ✗ авто: `node "{tw}/docs/komanda/zadaniya/proverki/009-dezhurstvo.cjs" "{otvet}"`
  ```
  в module.exports нет слова dezhurnyj или данных GRAFIK
  ```
- ✓ авто: `node "{tw}/tools/drakon-list.mjs" "{otvet}/dezhurstvo-list.md" --strogo` → — тест: «пример:» — 2, «контрпример:» — 2

## Круг 2 (токенов: 7190; файлы: dezhurstvo-list.md, dezhurstvo.js, vybor.json)

- ✓ авто: `node "{tw}/docs/komanda/zadaniya/proverki/009-vybor.cjs" "{otvet}"` → выбор стиля: верно 12 из 12
- ✗ авто: `node "{tw}/docs/komanda/zadaniya/proverki/009-dezhurstvo.cjs" "{otvet}"`
  ```
  в module.exports нет слова dezhurnyj или данных GRAFIK
  ```
- ✓ авто: `node "{tw}/tools/drakon-list.mjs" "{otvet}/dezhurstvo-list.md" --strogo` → — тест: «пример:» — 2, «контрпример:» — 2

## Руками (учитель, по последнему кругу)

- ✗ руками: `открой https://scatik146.github.io/drakon-graf/experiments/prolog/ , вставь в поле текст блока «конспект» из файла {otvet}/dezhurstvo-list.md (без строк с кавычками), нажми «4. Знания». Ждём: ✓ пример, ✓ контрпример, ответ «кто -> Вера»`
  ```
  правило не понято: переменные A и B вместо Х, У; ✗ пример Глеб сменяет Тимура не выводится; ✓ контрпример; запрос «кто сменяет Глеба» — ответов нет
  ```

## Чтением (лист проверки — заполняет проверяющий)

_не заполнено_
