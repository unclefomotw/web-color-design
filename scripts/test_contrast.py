"""Known-value checks for contrast.py. Run: python3 -I -m unittest discover -s scripts"""
import importlib.util
import pathlib
import unittest

_spec = importlib.util.spec_from_file_location(
    "contrast", pathlib.Path(__file__).with_name("contrast.py"))
c = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(c)


class KnownValues(unittest.TestCase):
    def test_extremes(self):
        self.assertAlmostEqual(c.check_pair("", "#000", "#fff")["ratio"], 21.0)
        self.assertAlmostEqual(c.check_pair("", "#abc", "#abc")["ratio"], 1.0)

    def test_aa_boundary_not_rounded_up(self):
        r = c.check_pair("", "#777777", "#ffffff")
        self.assertEqual(r["ratio_display"], "4.47")
        self.assertFalse(r["pass"]["AA_text"])
        self.assertTrue(c.check_pair("", "#767676", "#fff")["pass"]["AA_text"])

    def test_alpha_composited(self):
        r = c.check_pair("", "rgba(0,0,0,0.5)", "#fff")
        self.assertEqual(r["fg_resolved"], "#808080")

    def test_oklch(self):
        self.assertEqual(c.to_hex(c.parse("oklch(62.8% 0.2577 29.23)")[0]), "#ff0000")
        self.assertTrue(c.parse("oklch(0.7 0.4 150)")[2])  # out of sRGB

    def test_translucent_background_rejected(self):
        with self.assertRaises(ValueError):
            c.check_pair("", "#000", "#00000080")

    def test_link_three_way(self):
        self.assertFalse(c.check_link("#0066cc", "#333", "#fff")["color_only_links_allowed"])


if __name__ == "__main__":
    unittest.main()
