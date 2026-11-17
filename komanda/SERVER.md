# Сервер команды (свободный компьютер, Windows 10 + WSL)

Шаг 4 решения учителя 17.11 (`komnata/2026-11-17-limit-claude.md`). Ставится в паузах уроков; урок главнее.
Инструкция — `komanda/vstavka/den/2026-11-17/03-alisa-server.md` (15 шагов).
Репозиторий публичный: **IP-адреса, имена входа и пароли сюда не пишем** — они в приватном `memory_maryam_ai`.

## Что стоит (17.11: все 15 шагов пройдены)

| шаг | что | итог |
|---|---|---|
| 1–4 | Windows ≥ 2004, виртуализация, частная сеть, без сна | 22H2 (19045) · виртуализация работает (WSL2; CIM пишет False — норма) · сеть частная · сон: скрипт не прочёл, проверить вручную |
| 5–6 | WSL + Ubuntu, пользователь Linux | есть: **Ubuntu 26.04.1 LTS** (Алиса писала 22.04 — ошибка), ядро WSL2 6.18 |
| 7–8 | пакеты gforth, swi-prolog, python3, venv, git, curl (+ tree) | поставлены |
| 9 | версии | gforth 0.7.3 · SWI-Prolog 9.2.9 · Python 3.14.4 · git 2.53.0 (скрипт, 17.11) |
| 10 | `gforth -e "wordlist drop …"` → `WORDLIST ok` | **WORDLIST ok** |
| 11 | клон ii-komanda в `~/ii-komanda` | есть |
| 12 | OpenSSH-сервер Windows | встроенный сломан (sshd.exe падал с 0xC0000139) → заменён на OpenSSH_for_Windows 10.4p1 из winget (`tools/server-ssh-pochinka.ps1`), автозапуск, порт 22 только для частной сети |
| 13–14 | адрес, вход с ноутбука | адрес — в `memory_maryam_ai`; вход с ноутбука → `wsl` → `gforth 0.7.3` — **работает** (17.11) |

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

## Шаги а–в (17.11) — все сделаны

Дальше — по решению учителя: зеркала SourceCraft/Китай, холодный архив (пока хватает GitHub, 17.11); закрепить адрес в роутере; проверить «Сон — Никогда».

### Как было

а) git → GitHub: **17.11** ключ ed25519 сервера добавлен в GitHub (`Server-scatikwork`, отдельный от ноутбука), `ssh -T git@github.com` — успешно; имя Serge Vesnin, почта gmail, для `~/max-class-bot*` — yandex (`~/.gitconfig-max-bot`). Алиса вне плана поставила `xclip` (безвредно). ii-komanda переведена на SSH, пробный push — **прошёл**. Шаг «а» закрыт.
б) **сделано 17.11**: `~/.ii-komanda.env` (600) перенесён `tools/server-klyuchi.sh`, ключи YANDEX_API_KEY и YANDEX_FOLDER_ID; `ii.py klyuchi` — alisa, alisa_flash, deepseek, qwen работают. venv не нужен: ii.py без пакетов.
в) **сделано 17.11** (первый прогон 22:38: 11 репозиториев, 254 МБ, без ошибок; задача Windows «ii-komanda rezerv» создана): **все** репозитории Scatik146 — полные зеркала (`git clone --mirror`) в `~/rezerv/github/`, `tools/server-rezerv.sh`; публичные — сам по API GitHub, приватные — список в `~/.ii-rezerv-privatnye` (вне репозитория); журнал `~/rezerv/zhurnal.txt`; расписание Windows 03:00 и при входе — `tools/server-rezerv-raspisanie.ps1`. Дальше по решению 13.11: зеркала SourceCraft и Китай, холодный архив.
