#!/usr/bin/env bash
# Сервер команды (WSL): git может пушить в GitHub (шаг «а»).
# Запуск в окне Ubuntu (можно дважды — второй раз после добавления ключа в GitHub):
#   bash ~/ii-komanda/tools/server-git.sh
# Ключ SSH в GitHub добавляет учитель сам. Скрипт печатает только ОТКРЫТУЮ часть ключа (.pub) — её можно показывать.

KLYUCH="$HOME/.ssh/id_ed25519"
KOMANDA_DIR="$HOME/ii-komanda"

stroka() { printf '%-12s %s\n' "$1" "$2"; }

sprosit() {                      # вопрос → ответ с клавиатуры (работает и при curl | bash)
  local otvet; read -r -p "$1: " otvet < /dev/tty; echo "$otvet"
}

imya-zadat() {                   # git user.name / user.email — один раз
  [ -n "$(git config --global user.name)" ]  || git config --global user.name  "$(sprosit 'Имя для коммитов (латиницей)')"
  [ -n "$(git config --global user.email)" ] || git config --global user.email "$(sprosit 'Почта для коммитов (как в GitHub)')"
  stroka "git имя" "$(git config --global user.name) <$(git config --global user.email)>"
}

klyuch-sozdat() {                # ключ без пароля-фразы — сервер работает сам
  [ -f "$KLYUCH" ] || ssh-keygen -q -t ed25519 -N "" -C "server-scatikwork" -f "$KLYUCH"
  ssh-keyscan -t ed25519 github.com >> "$HOME/.ssh/known_hosts" 2>/dev/null
  sort -u -o "$HOME/.ssh/known_hosts" "$HOME/.ssh/known_hosts"
}

github-proverit() {              # ssh -T отвечает «successfully authenticated» и кодом 1 — это норма
  if ssh -T -o BatchMode=yes git@github.com 2>&1 | grep -q "successfully authenticated"; then
    stroka "GitHub" "ключ принят"; return 0
  fi
  stroka "GitHub" "ключ ещё не добавлен"; return 1
}

komanda-na-ssh() {               # ii-komanda: адрес https → ssh, проверка отправки
  git -C "$KOMANDA_DIR" remote set-url origin git@github.com:Scatik146/ii-komanda.git
  git -C "$KOMANDA_DIR" pull -q --ff-only 2>&1 | tail -2          # пробный push падает, если копия отстала
  local otvet
  if otvet=$(git -C "$KOMANDA_DIR" push --dry-run origin HEAD 2>&1); then
    stroka "ii-komanda" "отправка через SSH — проверена (пробный push)"
  else
    stroka "ii-komanda" "пробный push НЕ прошёл — стоп, вопрос к Марьям:"
    echo "$otvet" | tail -4
  fi
}

echo "=== Для Марьям (git) ==="
imya-zadat
klyuch-sozdat
if github-proverit; then
  komanda-na-ssh
else
  echo "Откройте на GitHub: Settings → SSH and GPG keys → New SSH key, Title: server-scatikwork,"
  echo "вставьте строку ниже целиком и сохраните. Потом запустите этот скрипт ещё раз."
  echo
  cat "$KLYUCH.pub"
  echo
fi
echo "=== конец ==="
