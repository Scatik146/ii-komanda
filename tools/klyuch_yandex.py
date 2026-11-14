"""Проверка ключа Яндекса (Yandex AI Studio, Alice AI LLM). Только стандартная библиотека.

Запуск:  python klyuch_yandex.py
Ключ берётся из файла .ii-komanda.env в домашней папке (строки YANDEX_API_KEY=… и YANDEX_FOLDER_ID=…)
или из переменных окружения. Сам ключ на экран не выводится.
Временный файл: в ii.py его заменит команда `klyuchi`.
"""
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ADRES = "https://ai.api.cloud.yandex.net/v1/chat/completions"


def klyuchi():
    znach = {}
    dom = Path.home()
    for imya in (".ii-komanda.env", ".ii-komanda.env.txt"):
        fajl = dom / imya
        if fajl.is_file():
            print("Файл с ключами:", fajl)
            for stroka in fajl.read_text(encoding="utf-8-sig").splitlines():
                stroka = stroka.strip()
                if stroka and not stroka.startswith("#") and "=" in stroka:
                    k, v = stroka.split("=", 1)
                    znach[k.strip()] = v.strip().strip('"').strip("'")
            break
    else:
        print("Файла", dom / ".ii-komanda.env", "нет — смотрю переменные окружения.")
    for k in ("YANDEX_API_KEY", "YANDEX_FOLDER_ID"):
        if os.environ.get(k):
            znach[k] = os.environ[k].strip()
    return znach.get("YANDEX_API_KEY", ""), znach.get("YANDEX_FOLDER_ID", "")


def main():
    klyuch, katalog = klyuchi()
    if not klyuch or not katalog:
        print("ИТОГ: НЕТ КЛЮЧА —", "нет YANDEX_API_KEY" if not klyuch else "нет YANDEX_FOLDER_ID")
        return 1
    print("Ключ найден (длина %d), каталог найден (длина %d)." % (len(klyuch), len(katalog)))
    telo = json.dumps({
        "model": "gpt://%s/aliceai-llm" % katalog,
        "messages": [{"role": "user", "content": "Ответь одним словом: работает"}],
        "max_tokens": 20,
    }).encode("utf-8")
    zapros = urllib.request.Request(ADRES, data=telo, method="POST", headers={
        "Authorization": "Bearer " + klyuch,
        "OpenAI-Project": katalog,
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(zapros, timeout=60) as otvet:
            dannye = json.loads(otvet.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        tekst = e.read().decode("utf-8", "replace")[:400].replace(klyuch, "***")
        prichina = {401: "ключ не принят", 403: "нет прав или нет денег/гранта",
                    404: "модель или каталог не найдены", 429: "превышен лимит"}.get(e.code, "ошибка сервера")
        print("ИТОГ: НЕ РАБОТАЕТ — HTTP %d (%s)" % (e.code, prichina))
        print("Ответ сервера:", tekst)
        return 1
    except Exception as e:
        print("ИТОГ: ОШИБКА СЕТИ —", type(e).__name__, str(e)[:200])
        return 1
    try:
        tekst = dannye["choices"][0]["message"]["content"].strip()
    except Exception:
        print("ИТОГ: ОТВЕТ НЕРАБОЧИЙ — непонятный формат:", json.dumps(dannye, ensure_ascii=False)[:300])
        return 1
    print("Ответ модели:", tekst[:100])
    print("Токены:", dannye.get("usage", {}).get("total_tokens", "?"))
    print("ИТОГ: РАБОТАЕТ — Alice AI LLM отвечает по API.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
