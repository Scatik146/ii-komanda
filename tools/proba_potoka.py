#!/usr/bin/env python3
"""proba_potoka.py — как модель отвечает потоком: сырые строки ответа с секундами (ii.py 0.3.1).

Запуск на сервере:  python3 tools/proba_potoka.py [модель]   (по умолчанию deepseek)
Печатает Content-Type и первые строки ответа (до 20, обрезка 160 знаков). Ключи не печатает.
"""
import json
import sys
import time
import urllib.request

import ii

VOPROS = "Реши по шагам: в классе 28 учеников, 3/7 из них — девочки; сколько мальчиков? Ответь числом."
STROK = 20


# запрос: модель → urllib.Request с потоком, как в ii.odin_vyzov
def zapros(m, klyuchi):
    zagolovki = {"Content-Type": "application/json", "Authorization": "Bearer " + klyuchi[m["klyuch"]]}
    for k, v in m.get("zagolovki", {}).items():
        zagolovki[k] = ii.raskryt(v, klyuchi)
    telo = {"model": ii.raskryt(m["model"], klyuchi), "messages": [{"role": "user", "content": VOPROS}],
            "max_tokens": 2000, "temperature": 0.3, "stream": True}
    telo.update(m.get("telo_dop", {}))
    z = urllib.request.Request(m["adres"].rstrip("/") + "/chat/completions",
                               data=json.dumps(telo).encode("utf-8"), method="POST")
    for k, v in zagolovki.items():
        z.add_header(k, v)
    return z


# печатать-строки: первые STROK строк ответа с секундами от начала
def pechatat_stroki(otvet, nachalo):
    print("Content-Type:", otvet.headers.get("Content-Type", "—"))
    nomer = 0
    for stroka in otvet:
        tekst = stroka.decode("utf-8", "replace").rstrip()
        tekst = tekst[tekst.find('"choices"'):] if '"choices"' in tekst else tekst
        if tekst and nomer < STROK:
            nomer += 1
            print("%6.1f с | %s" % (time.time() - nachalo, tekst[:160]), flush=True)
    print("%6.1f с | конец ответа, строк с данными: %d (показано до %d)" % (time.time() - nachalo, nomer, STROK))


def main():
    imya = sys.argv[1] if len(sys.argv) > 1 else "deepseek"
    modeli = ii.zagruzit_modeli()
    klyuchi, _ = ii.najti_klyuchi(ii.imena_peremennyh(modeli))
    nachalo = time.time()
    print("Модель:", imya, "— жду ответ (до 5 минут)…", flush=True)
    with urllib.request.urlopen(zapros(modeli["modeli"][imya], klyuchi), timeout=300) as otvet:
        pechatat_stroki(otvet, nachalo)
    return 0


if __name__ == "__main__":
    sys.exit(main())
