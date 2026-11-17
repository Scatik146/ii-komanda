#!/usr/bin/env bash
# Сервер команды (WSL): перенос файла ключей .ii-komanda.env с диска Windows в домашнюю папку Linux.
# Запуск в окне Ubuntu:
#   bash ~/ii-komanda/tools/server-klyuchi.sh            — сам ищет файл в C:\Users\*\ и в «Загрузках»
#   bash ~/ii-komanda/tools/server-klyuchi.sh ПУТЬ       — взять указанный файл
# Значения ключей не печатает. Исходный файл на диске Windows НЕ удаляет — это делает учитель.

CEL="$HOME/.ii-komanda.env"
IMENA=".ii-komanda.env .ii-komanda.env.txt ii-komanda.env ii-komanda.env.txt"

najti() {                        # → путь первого найденного файла или пусто
  for papka in /mnt/c/Users/*/ /mnt/c/Users/*/Downloads/ /mnt/c/Users/*/Desktop/; do
    for imya in $IMENA; do
      [ -f "$papka$imya" ] && { echo "$papka$imya"; return; }
    done
  done
}

perenesti() {                    # путь → ~/.ii-komanda.env без \r, доступ только владельцу
  tr -d '\r' < "$1" > "$CEL" && chmod 600 "$CEL"
}

pokazat-imena() {                # только имена ключей, без значений
  grep -oE '^[A-Z_]+=' "$CEL" | tr -d '=' | sed 's/^/  есть: /'
}

ISTOCHNIK="${1:-$(najti)}"
if [ -z "$ISTOCHNIK" ] || [ ! -f "$ISTOCHNIK" ]; then
  echo "Файл ключей не найден. Положите его в «Загрузки» Windows и запустите снова."
  exit 1
fi

perenesti "$ISTOCHNIK"
echo "=== Для Марьям (ключи) ==="
echo "Перенесено в ~/.ii-komanda.env (доступ 600)"
pokazat-imena
python3 "$HOME/ii-komanda/tools/ii.py" klyuchi
echo "Исходник остался здесь — удалите его сами: $ISTOCHNIK"
echo "=== конец ==="
