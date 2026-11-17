# Сервер команды (свободный компьютер, Windows 10 + WSL)

Шаг 4 решения учителя 17.11 (`komnata/2026-11-17-limit-claude.md`). Ставится в паузах уроков; урок главнее.
Инструкция — `komanda/vstavka/den/2026-11-17/03-alisa-server.md` (15 шагов).
Репозиторий публичный: **IP-адреса, имена входа и пароли сюда не пишем** — они в приватном `memory_maryam_ai`.

## Что стоит (сводка Алисы 17.11, сверено с 15 шагами)

| шаг | что | итог |
|---|---|---|
| 1–4 | Windows ≥ 2004, виртуализация, частная сеть, без сна | не в сводке → проверит `tools/server-windows.ps1` |
| 5–6 | WSL + Ubuntu, пользователь Linux | есть: Ubuntu 22.04 (по сводке) |
| 7–8 | пакеты gforth, swi-prolog, python3, venv, git, curl (+ tree) | поставлены |
| 9 | версии | gforth 0.7.3 · SWI-Prolog 9.2.9 · Python 3.14.4 · git 2.53.0 — **сверить**: для Ubuntu 22.04 Python 3.14 и git 2.53 не типичны |
| 10 | `gforth -e "wordlist drop …"` → `WORDLIST ok` | не сделан (Алиса проверила `words`, это другое) |
| 11 | клон ii-komanda в `~/ii-komanda` | не сделан |
| 12 | OpenSSH-сервер Windows | не сделан |
| 13–14 | адрес, вход с ноутбука | не сделаны |

Вне инструкции Алиса завела `~/teacher-workpad/{templates_v6,ideas_v9,drakon,speech_9class}` и черновик ДРАКОН-листа
урока «Распознавание и синтез речи», 9 кл. (`drakon/lesson_speech_9class_draft.txt`). Это **не** клон репозитория
teacher-workpad; черновик лежит только на сервере — решение учителя, куда его перенести.

**SWI-Prolog 9.2.9 — старше 10.0.** Пока оставлен (п. 4 задания). Новее — из PPA `swi-prolog/stable`, когда понадобится.

## Как довести (два скрипта)

1. Windows, PowerShell **от имени администратора**:
   `irm https://raw.githubusercontent.com/Scatik146/ii-komanda/main/tools/server-windows.ps1 | iex`
   — показывает шаги 1–4, ставит и запускает sshd, печатает адрес (адрес — только в чат Марьям).
2. Окно Ubuntu:
   `curl -fsSL https://raw.githubusercontent.com/Scatik146/ii-komanda/main/tools/server-proverka.sh | bash`
   — доставляет пакеты, печатает версии, `WORDLIST ok`, клонирует ii-komanda.
3. С ноутбука (шаг 14): `ssh <пользователь Windows>@<адрес>` → `wsl` → `gforth --version`.

## Как войти

С ноутбука в той же домашней сети: `ssh <пользователь Windows>@<адрес сервера>`, затем `wsl`. Адрес и имя — в `memory_maryam_ai`.

## Следующие шаги (по одному, после «дальше» учителя)

а) git на сервере пушит в GitHub (ключ SSH в GitHub добавляет учитель сам).
б) ~~ключи~~ **сделано 17.11**: `~/.ii-komanda.env` (600) перенесён `tools/server-klyuchi.sh`, ключи YANDEX_API_KEY и YANDEX_FOLDER_ID; `ii.py klyuchi` — alisa, alisa_flash, deepseek, qwen работают. venv не нужен: ii.py без пакетов.
в) резервные копии.
