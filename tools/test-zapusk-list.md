# ДРАКОН-лист: test-zapusk.bat — тест навыка одной командой

15.11.2026, Марьям. Код — `test-zapusk.bat` и `chistyj_otvet.py` рядом. Запуск из папки `ii-komanda`: `tools\test-zapusk.bat 011 alisa`.

## Действия

```дракон
название: Тест навыка одной командой
ввод: задание и модель
вопрос: Задание найдено?
  да:
  нет:
    вывод: как запускать
    конец
вопрос: Модель — glm?
  да:
    вопрос: Ответ GLM чистый?
      да:
      нет:
        вывод: строки со следами копирования
        конец
  нет:
git pull --rebase в ii-komanda и teacher-workpad
python tools\test_koda.py задание --model модель
вопрос: Тест дошёл до конца?
  да:
  нет:
    вывод: итог не отправляю, запусти ещё раз
    конец
git add testy
вопрос: Есть новые итоги?
  да:
    git commit -m и git push
    вопрос: Push отклонён?
      да:
        git pull --rebase и git push ещё раз
      нет:
  нет:
    вывод: отправлять нечего
```

## Данные

```конспект
тема: Где что лежит
связка: файл | папка
задание -> zadaniya/<номер>-….md | ii-komanda/komanda/
ответ GLM -> otvet-glm.md | ii-komanda/
итог -> itog.md | ii-komanda/testy/<задание>/<модель>/
```

## Тест

- пример: `chistyj_otvet.py` на ответе GLM из 009, испорченный прогон (`testy/009-blok1-vybor-stilya/glm/krug-2/otvet.md`) → следы найдены, код выхода 1
- контрпример: `chistyj_otvet.py` на очищенном ответе (`testy/009-blok1-vybor-stilya/glm/otvet-glm-ochishchen.md`) → следы найдены
