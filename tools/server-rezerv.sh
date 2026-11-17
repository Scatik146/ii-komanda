#!/usr/bin/env bash
# Сервер команды (WSL): полные копии ВСЕХ репозиториев Scatik146 с GitHub (шаг «в»).
# Копия — «зеркало» (git clone --mirror): вся история, все ветки и метки. Повторный запуск — обновляет.
# Запуск в окне Ubuntu:  bash ~/ii-komanda/tools/server-rezerv.sh
# Публичные репозитории скрипт находит сам (новые подхватятся). Приватные — по списку в ~/.ii-rezerv-privatnye
# (по имени в строке; файл вне репозитория — названия приватных репозиториев в публичный не кладём).

VLADELEC="Scatik146"
PAPKA="$HOME/rezerv/github"
ZHURNAL="$HOME/rezerv/zhurnal.txt"
PRIVATNYE="$HOME/.ii-rezerv-privatnye"

stroka() { printf '%-26s %s\n' "$1" "$2"; }

publichnye() {                   # имена публичных репозиториев — из API GitHub, без ключа
  curl -fsS "https://api.github.com/users/$VLADELEC/repos?per_page=100" |
    python3 -c 'import json,sys; print("\n".join(r["name"] for r in json.load(sys.stdin)))'
}

privatnye() {                    # имена из файла, без пустых строк и комментариев
  [ -f "$PRIVATNYE" ] && grep -v -e '^\s*$' -e '^#' "$PRIVATNYE"
}

zerkalo() {                      # имя → создать или обновить зеркало; печатает итог
  local imya="$1" cel="$PAPKA/$1.git"
  if [ -d "$cel" ]; then
    git -C "$cel" remote update --prune </dev/null >/dev/null 2>&1 && stroka "$imya" "обновлён" || stroka "$imya" "ОШИБКА обновления"
  else
    git clone -q --mirror "git@github.com:$VLADELEC/$imya.git" "$cel" </dev/null 2>/dev/null && stroka "$imya" "скопирован" || stroka "$imya" "ОШИБКА копирования"
  fi
}

vse-zerkala() {
  { publichnye; privatnye; } | sort -u | while read -r imya; do zerkalo "$imya"; done
}

mkdir -p "$PAPKA"
{
  echo "=== Для Марьям (резерв) $(date '+%d.%m.%Y %H:%M') ==="
  vse-zerkala
  stroka "всего на диске" "$(du -sh "$PAPKA" | cut -f1)"
  echo "=== конец ==="
} | tee -a "$ZHURNAL"
