import unittest

from sr.tools.inventory import assetcode


class TestNormalise(unittest.TestCase):
    def test_normal(self):
        codes = [('sr43', '43'), ('SRff3', 'FF3'), ('  srabc  ', 'ABC')]
        for input_code, output_code in codes:
            self.assertEqual(assetcode.normalise(input_code), output_code)


class TestValidity(unittest.TestCase):
    longMessage = True

    def test_valid(self):
        for code in ['srp1u28']:
            msg = "{} should be valid".format(code)
            self.assertTrue(assetcode.is_valid(code), msg)

    def test_invalid(self):
        for code in ['abc', 'sr2017', '2017', '2017-KICKSTART']:
            msg = "{} should not be valid".format(code)
            self.assertFalse(assetcode.is_valid(code), msg)


class TestConversion(unittest.TestCase):
    def test_invalid_user(self):
        with self.assertRaises(ValueError):
            assetcode.num_to_code(-10, 10)

    def test_invalid_part(self):
        with self.assertRaises(ValueError):
            assetcode.num_to_code(10, -10)

    def test_both_ways(self):
        uid = 10
        pid = 20

        num = assetcode.num_to_code(uid, pid)
        self.assertEqual(assetcode.code_to_num(num), (uid, pid))
