"""Тесты avto.py без сети и без браузера: python -m unittest tools/test_avto.py."""
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import avto

HOROSHIJ = """<html><head><style>:root { --fon: #fff; } body { color: var(--fon); }</style></head>
<body><button>Новая пара</button><script>
// слово: один выход
function odin(x) { var r = "return"; if (x) { r = 1; } return r; }
document.addEventListener("keydown", function (e) { if (e.ctrlKey && e.altKey && e.key === "m") { odin(1); } });
</script></body></html>"""
PLOHOJ = """<html><head><style>.a { color: #f00; background: rgba(0,0,0,.1); }</style></head>
<body><p style="color:red">микрофон</p><script>
function dva(x) { if (x) { return 1; } return 2; }
const vnutri = () => { function v() { return 1; } return v(); };
</script></body></html>"""


class TestStil(unittest.TestCase):
    def test_horoshij_bez_narushenij(self):
        self.assertEqual(avto.proverit_stil(HOROSHIJ), [])

    def test_plohoj_vse_tri(self):
        tekst = " | ".join(avto.proverit_stil(PLOHOJ))
        self.assertIn("inline style=", tekst)
        self.assertIn("цвета вне :root — 2 раз", tekst)
        self.assertIn("1 функций: dva", tekst)  # vnutri и v — по одному return

    def test_return_v_stroke_i_kommentarii_ne_schitaetsya(self):
        kod = 'function f() { var s = "return }"; /* return */ // return\n return s; }'
        self.assertEqual(list(avto.vozvraty_po_funkciyam(kod).values()), [1])


class TestResheniya(unittest.TestCase):
    def setUp(self):
        self.papka = Path(tempfile.mkdtemp())
        (self.papka / "avtoproverki.md").write_text(
            "## все\n- нет: микрофон\n\n## prilozhenie\n- есть: Новая пара\n- в данных: return\n- в данных: сбоя нет\n",
            encoding="utf-8")

    def test_pravila_chitayutsya(self):
        pravila = avto.prochitat_pravila(self.papka)
        self.assertEqual(pravila["все"], [("нет", "микрофон")])
        self.assertEqual(len(pravila["prilozhenie"]), 3)

    def test_horoshij(self):
        oshibki = avto.proverit_resheniya(HOROSHIJ, "prilozhenie", avto.prochitat_pravila(self.papka))
        self.assertEqual(oshibki, ["в данных ни разу: «сбоя нет»"])

    def test_plohoj(self):
        tekst = " | ".join(avto.proverit_resheniya(PLOHOJ, "prilozhenie", avto.prochitat_pravila(self.papka)))
        self.assertIn("запрещённое: «микрофон»", tekst)
        self.assertIn("нет обязательного: «Новая пара»", tekst)
        self.assertIn("Ctrl+Alt+M", tekst)

    def test_prezentaciya_bez_ctrl_alt_m(self):
        self.assertEqual(avto.proverit_resheniya("<p></p>", "prezentaciya", {}), [])


class TestProgon(unittest.TestCase):
    def test_perehvatchik_v_head(self):
        html = avto.s_perehvatchikom("<html><head><title>t</title></head></html>")
        self.assertLess(html.index("ii-otchet"), html.index("<title>"))

    def test_otchet_iz_dom(self):
        dom = '<pre id="ii-otchet" hidden="">{&quot;oshibki&quot;:[&quot;a &amp; b&quot;],&quot;ekranov&quot;:3}</pre>'
        self.assertEqual(avto.otchet_iz_dom(dom), {"oshibki": ["a & b"], "ekranov": 3})

    def test_net_otcheta(self):
        self.assertIn("не дала отчёт", avto.otchet_iz_dom("")["oshibki"][0])

    def test_brauzer_iz_peremennoj(self):
        with mock.patch.dict(os.environ, {"II_BRAUZER": "/x/msedge.exe"}):
            self.assertEqual(avto.najti_brauzer(), "/x/msedge.exe")

    def test_adres_linux(self):
        with mock.patch.object(avto, "eto_wsl", return_value=False):
            self.assertEqual(avto.adres_fajla(Path("/t/a.html"), "chrome"), "file:///t/a.html")

    def test_adres_wsl_edge(self):
        otvet = mock.Mock(stdout="C:\\Temp\\a.html\n")
        with mock.patch.object(avto, "eto_wsl", return_value=True), \
                mock.patch.object(avto.subprocess, "run", return_value=otvet):
            self.assertEqual(avto.adres_fajla(Path("/mnt/c/Temp/a.html"), "/mnt/c/E/msedge.exe"), "file:///C:/Temp/a.html")


if __name__ == "__main__":
    unittest.main()
