"""Deterministic tests, no network: python3 -I -m unittest discover -s tools/town-report/tests"""
import glob
import json
import os
import re
import sys
import unittest
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(TOOL))
sys.path.insert(0, TOOL)
import render, stats  # noqa: E402


def row(i, signed, amount, ca=("Mesto Test", 111), sup=("Firma, s. r. o.", 222), subject="Zmluva o dielo", pub="2026-03-02T10:00:00Z"):
    return {"id": i, "subject": subject, "signed_on": signed, "published_at": pub, "changed_at": pub, "amount": amount,
            "total_amount": amount, "ca_name": ca[0], "ca_cin": ca[1], "ca_cin_raw": str(ca[1]), "sup_name": sup[0], "sup_cin": sup[1],
            "sup_cin_raw": str(sup[1]), "kind_id": 1, "contract_identifier": None}


class LegalEntity(unittest.TestCase):
    def test_named_organisations(self):
        for n in ["Valašsko SK s. r. o.", "Slovak Telekom, a.s.", "Obec Hencovce", "Základná škola, Hlavná 1", "Mesto Humenné",
                  "Východoslovenská distribučná, a.s.", "Poľnohospodárske družstvo Vranov"]:
            self.assertTrue(stats.is_legal_entity(n, "12345678"), n)

    def test_people_and_sole_traders_are_not_named(self):
        for n in ["Ján Novák", "Ing. Ján Novák", "Ján Novák - ELEKTRO", "Mgr. Eva Kováčová, SERVIS", "Ján Novák - Centrum"]:
            self.assertFalse(stats.is_legal_entity(n, "12345678"), n)

    def test_no_ico_is_never_named(self):
        self.assertFalse(stats.is_legal_entity("Firma, s. r. o.", None))

    def test_ico_normalisation(self):
        self.assertEqual(stats.ico_of(332933, None), "00332933")
        self.assertEqual(stats.ico_of(None, "00 585 441"), "00585441")
        self.assertIsNone(stats.ico_of(None, "bez ičo"))


class Subjects(unittest.TestCase):
    def test_person_like_subject_dropped(self):
        self.assertIsNone(stats.safe_subject("Kúpna zmluva s Ing. Ján Novák"))
        self.assertIsNone(stats.safe_subject("Zmluva s Máriou Kováčová"))
        self.assertIsNotNone(stats.safe_subject("Zmluva o dielo – rekonštrukcia cesty"))

    def test_long_subject_shortened(self):
        self.assertLessEqual(len(stats.safe_subject("slovo " * 60)), 110)


class Window(unittest.TestCase):
    def test_last_twelve_complete_months(self):
        self.assertEqual(stats.window(date(2026, 10, 14)), (date(2025, 10, 1), date(2026, 9, 30)))
        self.assertEqual(stats.window(date(2026, 1, 3)), (date(2025, 1, 1), date(2025, 12, 31)))


class Compute(unittest.TestCase):
    def setUp(self):
        self.meta = {"synced_at": "2026-10-14T10:00:00+02:00"}
        self.rows = {r["id"]: r for r in [
            row(1, "2026-01-10", "1000.0"),
            row(2, "2026-01-11", "0.0"),
            row(3, "2026-02-01", "50.0", subject="Dodatok č. 1 k zmluve"),
            row(4, "2026-03-01", "9000.0", sup=("Ján Novák - SERVIS", 333), subject="Kúpna zmluva Ján Novák"),
            row(5, "2026-04-01", "500.0", ca=("Niekto", 444), sup=("Mesto Test", 111)),
            row(6, "2024-01-01", "7.0"),                     # outside the window
            row(7, "2026-05-01", "5.0", ca=("Iné mesto", 999)),  # not this town
            row(8, "2026-06-01", "100.0", pub="2026-06-05T08:00:00Z"),
        ]}
        self.s = stats.compute("00000111", self.rows, self.meta)

    def test_counts(self):
        c = self.s["contracts"]
        self.assertEqual((c["total"], c["amendments"], c["main"]), (6, 1, 5))

    def test_amounts_exclude_amendments(self):
        a = self.s["amount"]
        self.assertEqual((a["with_amount"], a["value_eur"], a["no_amount"]), (4, 10600, 1))

    def test_amendment_never_counts_as_value(self):
        self.assertNotIn(50, [t["amount_eur"] for t in self.s["top_contracts"]])

    def test_sole_trader_hidden_everywhere(self):
        blob = json.dumps(self.s, ensure_ascii=False)
        self.assertNotIn("Novák", blob)
        top = {t["id"]: t for t in self.s["top_contracts"]}
        self.assertIsNone(top[4]["counterparty"])
        self.assertIsNone(top[4]["subject"])

    def test_counterparties_only_legal_entities(self):
        self.assertEqual([s["ico"] for s in self.s["suppliers"]["top"]], ["00000222"])
        self.assertEqual(self.s["suppliers"]["named_contracts"], 3)
        self.assertEqual(self.s["suppliers"]["aggregated_contracts"], 2)

    def test_double_published_contract_counted_once(self):
        rows = dict(self.rows)
        rows[9] = row(9, "2026-01-10", "1000.0")           # same party, day and amount as row 1
        s = stats.compute("00000111", rows, self.meta)
        self.assertEqual(s["contracts"]["total"], 6)
        self.assertEqual(s["contracts"]["duplicates_removed"], 1)

    def test_redacted_parties_never_merged(self):
        rows = {i: row(i, "2026-01-11", "0.0", sup=("fyzická osoba", None)) for i in (20, 21, 22)}
        self.assertEqual(stats.compute("00000111", rows, self.meta)["contracts"]["total"], 3)

    def test_distinct_zero_amount_contracts_not_merged(self):
        rows = dict(self.rows)
        rows[9] = row(9, "2026-01-11", "0.0", subject="Iný predmet")
        self.assertEqual(stats.compute("00000111", rows, self.meta)["contracts"]["total"], 7)

    def test_trend_has_twelve_months(self):
        self.assertEqual(len(self.s["trend"]), 12)
        self.assertEqual(sum(t["contracts"] for t in self.s["trend"]), 6)

    def test_unknown_ico_raises(self):
        with self.assertRaises(SystemExit):
            stats.compute("00000999", {}, self.meta)


class Pages(unittest.TestCase):
    def test_fixture_page_has_required_pieces(self):
        s = json.load(open(os.path.join(HERE, "fixture.stats.json")))
        h = render.render(s, "x", "mailto:a@b.sk")
        for needle in ['content="noindex, nofollow', "CC BY 4.0", "ekosystem.slovensko.digital", "Takto by to vyzeralo", "údaje k"]:
            self.assertIn(needle, h)
        self.assertNotIn("canonical", h)
        self.assertNotIn("<script", h)

    def test_every_committed_page_is_unlisted_and_clean(self):
        pages = glob.glob(os.path.join(ROOT, "r", "*", "index.html"))
        robots = open(os.path.join(ROOT, "robots.txt")).read()
        sitemap = open(os.path.join(ROOT, "sitemap.xml")).read()
        index = open(os.path.join(ROOT, "index.html")).read()
        self.assertIn("Disallow: /r/", robots)
        for p in pages:
            slug = os.path.basename(os.path.dirname(p))
            self.assertRegex(slug, r"^[0-9a-f]{20}$")
            h = open(p, encoding="utf-8").read()
            self.assertIn("noindex", h)
            self.assertNotIn(slug, sitemap)
            self.assertNotIn(slug, index)
            self.assertNotIn("/r/", index)

    def test_committed_stats_name_only_legal_entities(self):
        for p in glob.glob(os.path.join(TOOL, "data", "*.stats.json")):
            s = json.load(open(p))
            for t in s["top_contracts"]:
                if t["counterparty"]:
                    self.assertTrue(stats.is_legal_entity(t["counterparty"], t["counterparty_ico"]), t["counterparty"])
                else:
                    self.assertIsNone(t["subject"])
            for x in s["suppliers"]["top"]:
                self.assertTrue(stats.is_legal_entity(x["name"], x["ico"]), x["name"])


if __name__ == "__main__":
    unittest.main()
