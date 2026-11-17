#!/usr/bin/env bash
# Сервер команды (WSL Ubuntu): проверка шагов 7–11 инструкции Алисы и сводка «Для Марьям».
# Запуск в окне Ubuntu одной строкой:
#   curl -fsSL https://raw.githubusercontent.com/Scatik146/ii-komanda/main/tools/server-proverka.sh | bash
# Ничего секретного не печатает: без IP, без паролей, без ключей.

KOMANDA_URL="https://github.com/Scatik146/ii-komanda"
KOMANDA_DIR="$HOME/ii-komanda"
PAKETY="gforth swi-prolog python3 python3-venv git curl"

stroka() { printf '%-14s %s\n' "$1" "$2"; }

versiya() {                      # имя команда → первая строка версии или «НЕТ»
  if command -v "$2" >/dev/null 2>&1; then
    stroka "$1" "$("$2" --version 2>&1 | head -1)"
  else
    stroka "$1" "НЕТ"
  fi
}

pakety-postavit() {              # шаг 8: доставить, чего не хватает
  sudo apt-get update -qq && sudo apt-get install -y -qq $PAKETY >/dev/null
}

slovari-forth() {                # шаг 10: словари Forth (условие GLM)
  stroka "wordlist" "$(gforth -e 'wordlist drop .( WORDLIST ok) cr bye' 2>&1 | tail -1)"
}

komanda-klon() {                 # шаг 11: репозиторий команды
  if [ -d "$KOMANDA_DIR/.git" ]; then
    git -C "$KOMANDA_DIR" pull -q && stroka "ii-komanda" "есть, обновлён"
  else
    git clone -q "$KOMANDA_URL" "$KOMANDA_DIR" && stroka "ii-komanda" "склонирован"
  fi
}

svodka() {
  echo "=== Для Марьям (WSL) ==="
  stroka "Ubuntu" "$(. /etc/os-release; echo "$PRETTY_NAME")"
  stroka "WSL" "$(uname -r)"
  versiya "gforth" gforth
  versiya "SWI-Prolog" swipl
  versiya "Python" python3
  versiya "git" git
  slovari-forth
  komanda-klon
  echo "=== конец: скопируйте всё между строками === в чат Марьям ==="
}

pakety-postavit
svodka
