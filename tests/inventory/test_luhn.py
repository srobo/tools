import unittest

from sr.tools.inventory import luhn


class TestValidity(unittest.TestCase):
    def test_invalid(self):
        for code in ['7894']:
            self.assertFalse(luhn.is_valid(code))

    def test_valid(self):
        for code in ['78949']:
            self.assertTrue(luhn.is_valid(code))

class TestChecksums(unittest.TestCase):
    def test_normal(self):
        for code, result in [('7894', 6)]:
            self.assertEqual(luhn.checksum(code), result)

class TestCalculatingCheckDigit(unittest.TestCase):
    def test_normal(self):
        for code, result in [('7894', '9')]:
            self.assertEqual(luhn.calc_check_digit(code), result)
