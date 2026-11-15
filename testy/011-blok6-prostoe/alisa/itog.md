# Итог: 011-blok6-prostoe — alisa

- модель: `gpt://{YANDEX_FOLDER_ID}/aliceai-llm/latest`
- когда: 15.11.2026 23:57
- первый круг: 0 из 3; последний круг (2): 0 из 3

## Круг 1 (токенов: 5037; файлы: нет)

- ✗ авто: `сдан файл parol-list.md`
  ```
  в ответе нет блока кода с именем файла parol-list.md над ним
  ```
- ✗ авто: `node "{tw}/tools/drakon-list.mjs" "{otvet}/parol-list.md" --strogo`
  ```
  node:fs:624
      return binding.readFileUtf8(path, stringToFlags(options.flag));
                     ^
  
  Error: ENOENT: no such file or directory, open 'C:\Users\scati\Documents\ii-komanda\testy\011-blok6-prostoe\alisa\krug-1\parol-list.md'
      at readFileSync (node:fs:624:20)
      at proveritList (file:///C:/Users/scati/Documents/teacher-workpad/tools/drakon-list.mjs:140:17)
      at file:///C:/Users/scati/Documents/teacher-workpad/tools/drakon-list.mjs:149:25
      at ModuleJob.run (node:internal/modules/esm/module_job:569:25)
      at async node:internal/modules/esm/loader:650:26
      at async asyncRunEntryPointWithESMLoader (node:internal/modules/run_main:105:5) {
    errno: -4058,
    code: 'ENOENT',
    syscall: 'open',
    path: 'C:\\Users\\scati\\Documents\\ii-komanda\\testy\\011-blok6-prostoe\\alisa\\krug-1\\parol-list.md'
  }
  
  Node.js v26.13.0
  ```
- ✗ авто: `node "{tw}/docs/komanda/zadaniya/proverki/011-parol.cjs" "{otvet}"`
  ```
  нет файла parol-list.md
  ```

## Круг 2 (токенов: 5811; файлы: нет)

- ✗ авто: `сдан файл parol-list.md`
  ```
  в ответе нет блока кода с именем файла parol-list.md над ним
  ```
- ✗ авто: `node "{tw}/tools/drakon-list.mjs" "{otvet}/parol-list.md" --strogo`
  ```
  node:fs:624
      return binding.readFileUtf8(path, stringToFlags(options.flag));
                     ^
  
  Error: ENOENT: no such file or directory, open 'C:\Users\scati\Documents\ii-komanda\testy\011-blok6-prostoe\alisa\krug-2\parol-list.md'
      at readFileSync (node:fs:624:20)
      at proveritList (file:///C:/Users/scati/Documents/teacher-workpad/tools/drakon-list.mjs:140:17)
      at file:///C:/Users/scati/Documents/teacher-workpad/tools/drakon-list.mjs:149:25
      at ModuleJob.run (node:internal/modules/esm/module_job:569:25)
      at async node:internal/modules/esm/loader:650:26
      at async asyncRunEntryPointWithESMLoader (node:internal/modules/run_main:105:5) {
    errno: -4058,
    code: 'ENOENT',
    syscall: 'open',
    path: 'C:\\Users\\scati\\Documents\\ii-komanda\\testy\\011-blok6-prostoe\\alisa\\krug-2\\parol-list.md'
  }
  
  Node.js v26.13.0
  ```
- ✗ авто: `node "{tw}/docs/komanda/zadaniya/proverki/011-parol.cjs" "{otvet}"`
  ```
  нет файла parol-list.md
  ```

## Руками (учитель, по последнему кругу)

- — руками: `открой https://scatik146.github.io/drakon-graf/generator/, вставь текст блока «конспект» из файла {otvet}/parol-list.md (без строк с кавычками). Ждём: рисунок читается — заголовок, запоминатель «Надёжный пароль», три пункта`
  ```
  пропущено
  ```

## Чтением (лист проверки — заполняет проверяющий)

Марьям, 16.11.2026, 00:05. **Почему авто 0:** оба круга — формат ответа нарушен: имя файла стоит *внутри* ограды из трёх кавычек, сам лист — во второй ограде из трёх (а не четырёх) кавычек, поэтому блоки ломаются и файл не находится. Подсказка второго круга («нет блока кода с именем файла над ним») не помогла. Первая строка ответа — «DeepSeek» (как в 009; модель — `aliceai-llm`): откуда — не знаю, надо проверить.

**Для справки** лист вырезан руками и прогнан теми же проверками: Л — оба блока без ошибок, тест есть; С — батарея; П — 0 из 4: цикл записан `для: символ в parol` (а не `for символ in parol`, как сказано в задании), вопрос — словами «символ — цифра?», ветка «нет» — `(ничего не делаем)`; код не запускается.

| № | Балл (круг 2) | Почему |
|---|---|---|
| Ч1 | 1 | один цикл, один вопрос, обе ветки есть |
| Ч2 | 0 | пример `Pass123!` → `True` верный; контрпример `password` → `False` — это верный вывод, а не неверный (в круге 1 было `True` — верно, Алиса «исправила» правильное) |
| Ч3 | 0 | выдумано: ключевое слово `запоминатель:` (в шпаргалке — `указатель -> ответ`), действие `(ничего не делаем)` |

**Итого:** первый круг — 0 из 7 командой (Ч: 1 + 1 + 0); последний круг — **1 из 7** (команда 0, К пропущено — файла нет, Ч1 = 1).
