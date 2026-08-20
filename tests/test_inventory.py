"""Inventory sensor row helper."""

import unittest
from datetime import date

from tests.hastubs import load_module

coordinator = load_module("coordinator")


class TestInventoryItemRow(unittest.TestCase):
    def test_includes_requested_fields(self):
        item = {
            "id": "abc",
            "code": "AB12",
            "name": "Yaourt",
            "contents": "Yaourt nature",
            "quantity": "500 g",
            "expiry_date": "2026-08-25",
            "location": "fridge",
            "portions": [{"n": 1, "status": "open"}, {"n": 2, "status": "open"}],
        }
        row = coordinator.inventory_item_row(item, date(2026, 8, 20))
        self.assertEqual(row["name"], "Yaourt")
        self.assertEqual(row["contents"], "Yaourt nature")
        self.assertEqual(row["quantity"], "500 g")
        self.assertEqual(row["expiry_date"], "2026-08-25")
        self.assertEqual(row["days_left"], 5)
        self.assertEqual(row["portions_total"], 2)
        self.assertEqual(row["portions_open"], 2)
        self.assertEqual(row["portions"], [{"n": 1, "status": "open"}, {"n": 2, "status": "open"}])

    def test_nullable_fields_preserved(self):
        item = {"id": "x", "code": "XY99", "name": "Restes"}
        row = coordinator.inventory_item_row(item)
        self.assertIsNone(row["contents"])
        self.assertIsNone(row["quantity"])
        self.assertIsNone(row["expiry_date"])
        self.assertNotIn("days_left", row)
        self.assertEqual(row["portions"], [{"n": 1, "status": "open"}])

    def test_format_inventory_speech_ingredients(self):
        rows = [
            {
                "name": "Yaourt",
                "expiry_date": "2026-08-25",
                "quantity": "500 g",
                "portions_total": 1,
                "portions_open": 1,
            }
        ]
        speech = coordinator.format_inventory_speech(rows, "fr", intro_key="ingredients_intro")
        self.assertIn("Yaourt", speech)
        self.assertIn("2026-08-25", speech)

    def test_format_inventory_speech_empty(self):
        speech = coordinator.format_inventory_speech([], "fr", intro_key="ingredients_intro")
        self.assertIn("aucun ingrédient", speech)


if __name__ == "__main__":
    unittest.main()
