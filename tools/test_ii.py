"""Тесты ii.py без сети: python -m unittest tools/test_ii.py (или python tools/test_ii.py)."""
import tempfile
import unittest
import urllib.error
from pathlib import Path

import ii

MODELI = {"roli": {"kanva": ["deepseek", "qwen"], "strazh": ["alisa", "glm"], "solo": ["deepseek"]},
          "modeli": {"alisa": {"adres": "https://y/v1", "model": "gpt://{YANDEX_FOLDER_ID}/aliceai-llm",
                               "klyuch": "YANDEX_API_KEY", "zagolovki": {"OpenAI-Project": "{YANDEX_FOLDER_ID}"}},
                     "deepseek": {"adres": "https://d", "model": "ds", "klyuch": "DEEPSEEK_API_KEY"},
                     "qwen": {"adres": "https://q", "model": "qw", "klyuch": "QWEN_API_KEY"},
                     "glm": {"adres": "https://g", "model": "gl", "klyuch": "GLM_API_KEY"}}}
KLYUCHI = {"YANDEX_API_KEY": "y", "YANDEX_FOLDER_ID": "b1", "DEEPSEEK_API_KEY": "d", "QWEN_API_KEY": "q"}


def otvet(tekst, finish="stop"):
    return {"choices": [{"message": {"content": tekst}, "finish_reason": finish}], "usage": {"total_tokens": 7}}


class Podmena:
    """Подмена http_post: очередь ответов или исключений, запись вызовов."""

    def __init__(self, *otvety):
        self.otvety, self.vyzovy = list(otvety), []

    def __call__(self, adres, zagolovki, telo, tajmaut=300):
        self.vyzovy.append((adres, zagolovki, telo))
        o = self.otvety.pop(0)
        if isinstance(o, Exception):
            raise o
        return o


class TestVyzov(unittest.TestCase):
    def setUp(self):
        self.staryj = ii.http_post

    def tearDown(self):
        ii.http_post = self.staryj

    def kt(self, **kw):
        return ii.Kontekst(MODELI, dict(KLYUCHI), **kw)

    def test_rabochij(self):
        ii.http_post = Podmena(otvet("канва"))
        self.assertEqual(ii.vyzov(self.kt(), "kanva", "т", "kanva")[:2], ("канва", "deepseek"))

    def test_povtor_i_zamena(self):
        ii.http_post = Podmena(otvet("обрезано", "length"), urllib.error.URLError("нет сети"), otvet("от qwen"))
        kt = self.kt()
        self.assertEqual(ii.vyzov(kt, "kanva", "т", "kanva")[1], "qwen")
        self.assertEqual(kt.vyzovov, 3)

    def test_net_klyucha_propusk(self):
        ii.http_post = Podmena(otvet("ПРИНЯТЬ"))
        kt = ii.Kontekst(MODELI, {"QWEN_API_KEY": "q"})
        self.assertEqual(ii.vyzov(kt, "kanva", "т", "kanva")[1], "qwen")

    def test_vse_nerabochie(self):
        ii.http_post = Podmena(otvet(""), otvet("Извините, я не могу помочь с этим"))
        with self.assertRaises(ii.Nerabochij):
            ii.vyzov(self.kt(), "solo", "т", "x")

    def test_predel(self):
        ii.http_post = Podmena(otvet(""), otvet(""))
        with self.assertRaises(ii.Oshibka):
            ii.vyzov(self.kt(predel=1), "solo", "т", "x")

    def test_yandeks_zagolovki_i_model(self):
        pod = Podmena(otvet("ПРИНЯТЬ"))
        ii.http_post = pod
        ii.vyzov(self.kt(), "strazh", "т", "strazh")
        adres, zag, telo = pod.vyzovy[0]
        self.assertEqual(adres, "https://y/v1/chat/completions")
        self.assertEqual(zag["OpenAI-Project"], "b1")
        self.assertEqual(telo["model"], "gpt://b1/aliceai-llm")

    def test_strazh_ne_avtor(self):
        pod = Podmena(otvet("ВЕРНУТЬ"))
        ii.http_post = pod
        ii.vyzov(ii.Kontekst(MODELI, {"GLM_API_KEY": "g", "YANDEX_API_KEY": "y", "YANDEX_FOLDER_ID": "b"}),
                 "strazh", "т", "strazh", krome="alisa")
        self.assertTrue(pod.vyzovy[0][0].startswith("https://g"))

    def test_ozhidaemyj_blok(self):
        ii.http_post = Podmena(otvet("просто текст"), otvet("Вердикт: **ВЕРНУТЬ**"))
        t = ii.vyzov(self.kt(), "solo", "т", "x", ozhidaem=ii.najti_verdikt)[0]
        self.assertEqual(ii.najti_verdikt(t), "ВЕРНУТЬ")


class TestUrok(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.urok = Path(self.tmp.name)
        (self.urok / "zayavka.md").write_text("Заявка\n| `prilozhenie` | Приложение | да |\n| `tehkarta` | Т | |\n", encoding="utf-8")
        (self.urok / "resheniya.md").write_text("Решения", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_nabor(self):
        self.assertEqual(ii.nabor_iz_zayavki(self.urok), ["kanva", "shpargalka", "prilozhenie"])
        (self.urok / "zayavka.md").write_text("- Набор: kanva, shpargalka, pechatnye, vizual\n", encoding="utf-8")
        self.assertEqual(ii.nabor_iz_zayavki(self.urok), ["kanva", "shpargalka", "pechatnye", "vizual"])

    def test_podstanovki(self):
        t = ii.podstavit("{{ZAYAVKA}}/{{RESHENIYA}}", self.urok)
        self.assertTrue(t.startswith("Заявка") and t.endswith("| Т | |/Решения"), t)
        with self.assertRaises(ii.Oshibka):
            ii.podstavit("{{KANVA}}", self.urok)
        with self.assertRaises(ii.Oshibka):
            ii.podstavit("{{NETAKOJ}}", self.urok)

    def test_vse_prompty_sobirayutsya(self):
        for f in ("kanva.md", "ekspertiza.md", "so-analiz.md"):
            (self.urok / f).write_text("x", encoding="utf-8")
        for p in sorted(ii.PROMPTY.glob("*.md")):
            if p.name == "README.md":
                continue
            t = ii.podstavit(ii.prochitat_prompt(p.stem), self.urok, {"KOD": "k", "REZULTAT": "r", "KARTINKI": "нет"})
            self.assertNotIn("{{", t, p.name)

    def test_ekspertiza_bez_seti(self):
        arg = ii.razbor(["ekspertiza", str(self.urok), "--bez-seti"])
        self.assertEqual(arg.f(arg), 0)
        zapros = (self.urok / "proverka" / "ekspertiza-zapros.md").read_text(encoding="utf-8")
        self.assertIn("Решения", zapros)
        self.assertFalse((self.urok / "ekspertiza.md").exists())  # ответ не имитируется


HOROSHIJ = '<!DOCTYPE html><html><body><img src="assets/kot.jpg"><svg xmlns="http://www.w3.org/2000/svg"></svg><script>var a = b && b.c;</script></body></html>'


class TestOkruzhenie(unittest.TestCase):
    def test_horoshij(self):
        self.assertEqual(ii.proverit_okruzhenie(HOROSHIJ, "prilozhenie.html", kartinki={"kot.jpg"}), [])

    def test_cdn(self):
        h = HOROSHIJ.replace("<body>", '<body><script src="https://cdn.jsdelivr.net/x.js"></script>')
        self.assertTrue(ii.proverit_okruzhenie(h, "prilozhenie.html"))

    def test_zaglushka(self):
        self.assertTrue(any("заглушка" in o for o in ii.proverit_okruzhenie(HOROSHIJ.replace("<body>", "<body>TODO"), "a.html")))

    def test_novyj_js(self):
        self.assertTrue(any("ES2018" in o for o in ii.proverit_okruzhenie(HOROSHIJ.replace("b && b.c", "b?.c"), "a.html")))

    def test_vydacha_strogo(self):
        self.assertTrue(ii.proverit_okruzhenie(HOROSHIJ, "a.html", tonkij=False))

    def test_imya_kirillica(self):
        self.assertTrue(ii.proverit_okruzhenie("<p>x</p>", "урок.html"))

    def test_kartinka_bez_zakaza(self):
        self.assertTrue(ii.proverit_okruzhenie(HOROSHIJ, "a.html", kartinki={"drugaya.jpg"}))


if __name__ == "__main__":
    unittest.main()
