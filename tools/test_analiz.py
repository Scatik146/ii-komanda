"""Тесты analiz.py без сети: python tools/test_analiz.py (или python -m unittest tools/test_analiz.py)."""
import contextlib
import io
import shutil
import tempfile
import unittest
from pathlib import Path

import analiz
import ii

KANDIDAT = {"номер": "К-01", "словарь": "тема", "тип": "утверждение", "запись": "Звук — это колебания",
            "цитата": "Звук — это колебания воздуха", "файл": "chaty/alisa.md"}
RAZMETKA = {"номер": "К-01", "истинность": "0", "доступ": "публичное", "в уроке": "нет",
            "источник": "[В] учебник физики", "очередь": "нет", "почему": "источник назван в чате"}
MODELI = {"roli": {}, "modeli": {"deepseek": {"adres": "https://d", "model": "ds", "klyuch": "YANDEX_API_KEY"}}}


def kandidat(**zamena):
    return dict(KANDIDAT, _privatnyj=False, **zamena)


def razmetka(**zamena):
    return dict(RAZMETKA, **zamena)


def gotovyj(nomer, **polya):
    return analiz.razmetit_odnogo(kandidat(номер=nomer), razmetka(номер=nomer, **polya), "glm")


def blok(imya, slovar, klyuchi):
    return analiz.blok_tekstom(imya, slovar, klyuchi)


class SPapkoj(unittest.TestCase):
    """Временная папка урока с одним чатом."""

    def setUp(self):
        self.papka = Path(tempfile.mkdtemp())
        (self.papka / "chaty").mkdir()
        (self.papka / "chaty" / "alisa.md").write_text("Алиса: Звук — это\nколебания   воздуха.\n", encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.papka)

    def kody(self, spisok):
        return [o[0] for o in analiz.proverit_kandidatov(spisok, self.papka)]

    def polozhit(self, spisok):
        tekst = "\n\n".join(blok("кандидат", k, analiz.KLYUCHI_KANDIDATA) for k in spisok)
        analiz.zapisat(self.papka, "kandidaty.md", tekst)

    def zapusk(self, *argumenty):
        vyvod = io.StringIO()
        with contextlib.redirect_stdout(vyvod), contextlib.redirect_stderr(vyvod):
            kod = analiz.main(list(argumenty))
        return kod, vyvod.getvalue()


class TestBloki(unittest.TestCase):
    def test_dva_bloka_i_chuzhaya_ograda(self):
        tekst = "вступление\n```разметка\nномер: К-01\nпочему: время 10:30\n```\n```python\nx: 1\n```\n``` Разметка\nномер: К-02\n```\n"
        spisok = analiz.bloki(tekst, "разметка")
        self.assertEqual([b["номер"] for b in spisok], ["К-01", "К-02"])
        self.assertEqual(spisok[0]["почему"], "время 10:30")

    def test_tuda_i_obratno(self):
        tekst = blok("кандидат", KANDIDAT, analiz.KLYUCHI_KANDIDATA)
        self.assertEqual(analiz.bloki(tekst, "кандидат"), [KANDIDAT])


class TestProverki(SPapkoj):
    def test_vernyj_kandidat(self):
        self.assertEqual(self.kody([kandidat()]), [])

    def test_citata_cherez_perevod_stroki(self):
        self.assertTrue(analiz.citata_est(self.papka, kandidat()))

    def test_po_odnoj_oshibke_na_porchu(self):
        porchi = {"Ц01": {"запись": ""}, "Ц03": {"словарь": "прочее"}, "Ц04": {"файл": "chaty/glm.md"},
                  "Ц05": {"цитата": "Звук — это волны"}, "Ц06": {"тип": "наблюдение"}}
        for kod, zamena in porchi.items():
            self.assertEqual(self.kody([kandidat(**zamena)]), [kod], kod)

    def test_povtor_nomera(self):
        self.assertEqual(self.kody([kandidat(), kandidat()]), ["Ц02", "Ц02"])

    def test_fajl_vne_papki(self):
        snaruzhi = self.papka.parent / "snaruzhi-analiz.md"
        snaruzhi.write_text("Звук — это колебания воздуха", encoding="utf-8")
        self.addCleanup(snaruzhi.unlink)
        self.assertEqual(self.kody([kandidat(файл="../snaruzhi-analiz.md")]), ["Ц04"])

    def test_nablyudenie_v_privatnom_fajle_razresheno(self):
        self.assertEqual(self.kody([dict(kandidat(тип="наблюдение"), _privatnyj=True)]), [])

    def test_plohie_ne_idut_razmetchiku(self):
        spisok = [kandidat(), kandidat(номер="К-02", цитата="выдумка")]
        oshibki = analiz.proverit_kandidatov(spisok, self.papka)
        self.assertEqual([k["номер"] for k in analiz.bez_oshibok(spisok, oshibki)], ["К-01"])


class TestSliyanie(unittest.TestCase):
    def test_obychnaya_razmetka(self):
        g = gotovyj("К-01")
        self.assertEqual((g["истинность"], g["очередь"], g["пометки"]), ("0", "нет", []))

    def test_tema_v_uroke_bez_istochnika_kritichna(self):
        g = gotovyj("К-01", **{"в уроке": "да", "источник": "нет"})
        self.assertEqual(g["очередь"], "без источника")
        self.assertTrue(analiz.kritichnyj(g))

    def test_bez_istochnika_istinnost_nol(self):
        g = gotovyj("К-01", истинность="1", источник="нет")
        self.assertEqual(g["истинность"], "0")
        self.assertIn("истинность снижена до 0: нет источника", g["пометки"])

    def test_slova_uchitelya_ne_trogaem(self):
        g = analiz.razmetit_odnogo(kandidat(словарь="реальность"), razmetka(истинность="1", источник="слова учителя"), "glm")
        self.assertEqual(g["истинность"], "1")

    def test_avtor_istochnika(self):
        g = analiz.razmetit_odnogo(kandidat(файл="kanva.md"), razmetka(), "deepseek")
        self.assertIn("размечено автором источника", g["пометки"])

    def test_privatnoe_idyot_v_ochered(self):
        g = gotovyj("К-01", доступ="Приватное")
        self.assertEqual(g["очередь"], "противоречие")

    def test_defis_vmesto_tire(self):
        self.assertEqual(gotovyj("К-01", истинность="-")["истинность"], "—")

    def test_plohoe_znachenie_v_pometkah(self):
        self.assertIn("очередь: «может быть»", gotovyj("К-01", очередь="может быть")["пометки"][0])

    def test_net_razmetki(self):
        spisok = analiz.slit([kandidat()], [], "glm")
        self.assertEqual(spisok[0]["пометки"], ["не размечен"])

    def test_lishnyaya_razmetka(self):
        self.assertEqual(analiz.lishnie_razmetki([kandidat()], [razmetka(номер="К-99")]), ["К-99"])


class TestOchered(unittest.TestCase):
    def nabor(self, kritichnyh, prochih):
        krit = [gotovyj("К-%d" % i, **{"в уроке": "да", "источник": "нет"}) for i in range(kritichnyh)]
        return krit + [gotovyj("П-%d" % i, очередь="двусмысленность") for i in range(prochih)]

    def razmery(self, kritichnyh, prochih):
        sejchas, zhdut = analiz.ochered(self.nabor(kritichnyh, prochih) + [gotovyj("Н-1")])
        return len(sejchas), len(zhdut)

    def test_obychno_ne_bolshe_desyati(self):
        self.assertEqual(self.razmery(0, 12), (10, 2))

    def test_kritichnye_pervymi(self):
        self.assertEqual(self.razmery(3, 12), (10, 5))

    def test_kritichnyh_do_soroka(self):
        self.assertEqual(self.razmery(45, 3), (40, 8))

    def test_pusto(self):
        self.assertEqual(self.razmery(0, 0), (0, 0))


class TestKomandy(SPapkoj):
    def test_citaty_v_poryadke(self):
        self.polozhit([KANDIDAT])
        self.assertEqual(self.zapusk("citaty", str(self.papka)), (0, "кандидаты в порядке: 1\n"))

    def test_citaty_s_oshibkoj(self):
        self.polozhit([dict(KANDIDAT, цитата="выдумка")])
        kod, vyvod = self.zapusk("citaty", str(self.papka))
        self.assertEqual((kod, vyvod), (1, "Ц05 К-01: цитаты нет в файле chaty/alisa.md\n"))

    def test_net_fajla_kandidatov(self):
        kod, vyvod = self.zapusk("citaty", str(self.papka))
        self.assertEqual(kod, 2)
        self.assertIn("ОСТАНОВКА: нет файла кандидатов", vyvod)

    def test_bez_seti_tolko_zapros(self):
        self.polozhit([KANDIDAT])
        kod, _ = self.zapusk("razmetka", str(self.papka), "--bez-seti")
        zapros = (self.papka / "analiz" / "razmetka-zapros.md").read_text(encoding="utf-8")
        self.assertEqual(kod, 0)
        self.assertIn("номер: К-01", zapros)
        self.assertNotIn("{{", zapros)
        self.assertFalse((self.papka / "analiz" / "ochered-uchitelyu.md").exists())

    def test_razmetka_s_podstavnym_otvetom(self):
        self.polozhit([KANDIDAT, dict(KANDIDAT, номер="К-02", цитата="выдумка")])
        otvet = self.papka / "otvet-glm.md"
        otvet.write_text("Кандидатов получено: 1\n" + blok("разметка", razmetka(**{"в уроке": "да", "источник": "нет"}),
                                                           ("номер",) + analiz.KLYUCHI_RAZMETKI), encoding="utf-8")
        kod, vyvod = self.zapusk("razmetka", str(self.papka), "--podstavit", str(otvet), "--model", "glm")
        self.assertEqual(kod, 0)
        self.assertIn("Размечено: 1, отброшено: 1, вопросов учителю: 1, ждут: 0", vyvod)
        ochered = (self.papka / "analiz" / "ochered-uchitelyu.md").read_text(encoding="utf-8")
        self.assertIn("## 1. К-01 — без источника — КРИТИЧНО: уйдёт к ученикам", ochered)
        self.assertIn("Ц05 К-02", (self.papka / "analiz" / "otchet.md").read_text(encoding="utf-8"))

    def test_kontekst_uroka_v_zaprose(self):
        (self.papka / "kanva.md").write_text("Канва: звук и речь", encoding="utf-8")
        self.assertIn("=== kanva.md ===\nКанва: звук и речь", analiz.zapros_razmetki(self.papka, [KANDIDAT]))


class TestVyzovModeli(SPapkoj):
    """Путь через сеть — с подменой слов ii.py: запрос уходит названной модели, ответ разбирается."""

    def setUp(self):
        super().setUp()
        self.starye = (ii.http_post, ii.zagruzit_modeli, ii.najti_klyuchi)
        self.telo = {}
        ii.zagruzit_modeli = lambda put=None: MODELI
        ii.najti_klyuchi = lambda imena: ({"YANDEX_API_KEY": "y"}, [])
        ii.http_post = self.otvetit

    def tearDown(self):
        ii.http_post, ii.zagruzit_modeli, ii.najti_klyuchi = self.starye
        super().tearDown()

    def otvetit(self, adres, zagolovki, telo, tajmaut=300):
        self.telo = telo
        tekst = blok("разметка", RAZMETKA, ("номер",) + analiz.KLYUCHI_RAZMETKI)
        return {"choices": [{"message": {"content": tekst}, "finish_reason": "stop"}], "usage": {"total_tokens": 7}}

    def test_zapros_uhodit_deepseek(self):
        self.polozhit([KANDIDAT])
        kod, vyvod = self.zapusk("razmetka", str(self.papka))
        self.assertEqual(kod, 0)
        self.assertEqual(self.telo["model"], "ds")
        self.assertIn("Размечено: 1, отброшено: 0, вопросов учителю: 0", vyvod)

    def test_model_ne_otvetila(self):
        ii.http_post = self.upast
        self.polozhit([KANDIDAT])
        kod, vyvod = self.zapusk("razmetka", str(self.papka))
        self.assertEqual(kod, 2)
        self.assertIn("ОСТАНОВКА: разметчик deepseek не ответил", vyvod)

    def upast(self, adres, zagolovki, telo, tajmaut=300):
        raise OSError("сети нет")


class TestKomandaIi(SPapkoj):
    """ii.py analiz <урок> — та же работа, что analiz.py razmetka."""

    def test_ii_analiz_bez_seti(self):
        self.polozhit([KANDIDAT])
        vyvod = io.StringIO()
        with contextlib.redirect_stdout(vyvod):
            kod = ii.main(["analiz", str(self.papka), "--bez-seti"])
        self.assertEqual(kod, 0)
        self.assertTrue((self.papka / "analiz" / "razmetka-zapros.md").exists())


class TestNastoyashchieDannye(unittest.TestCase):
    """Кандидаты опроса 16.11: все цитаты стоят в файле опроса."""

    def test_kandidaty_sreza_1(self):
        papka = analiz.KOREN / "komanda" / "srez-1"
        spisok = analiz.iz_fajla(papka / "analiz" / "kandidaty.md")
        self.assertEqual(len(spisok), 25)
        self.assertEqual(analiz.proverit_kandidatov(spisok, papka), [])


if __name__ == "__main__":
    unittest.main()
