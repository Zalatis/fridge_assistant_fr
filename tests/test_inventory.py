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
        }
        row = coordinator.inventory_item_row(item, date(2026, 8, 20))
        self.assertEqual(row["name"], "Yaourt")
        self.assertEqual(row["contents"], "Yaourt nature")
        self.assertEqual(row["quantity"], "500 g")
        self.assertEqual(row["expiry_date"], "2026-08-25")
        self.assertEqual(row["days_left"], 5)
        self.assertEqual(row["id"], "abc")
        self.assertEqual(row["code"], "AB12")

    def test_nullable_fields_preserved(self):
        item = {"id": "x", "code": "XY99", "name": "Restes"}
        row = coordinator.inventory_item_row(item)
        self.assertIsNone(row["contents"])
        self.assertIsNone(row["quantity"])
        self.assertIsNone(row["expiry_date"])
        self.assertNotIn("days_left", row)


if __name__ == "__main__":
    unittest.main()
