import unittest

from sr.tools.inventory import assetcode


class TestConversion(unittest.TestCase):
    def test_invalid_uid(self):
        with self.assertRaises(ValueError):
            assetcode.num_to_code(-10, 10)

    def test_invalid_pid(self):
        with self.assertRaises(ValueError):
            assetcode.num_to_code(10, -10)

    def test_both_ways(self):
        uid = 10
        pid = 20

        num = assetcode.num_to_code(uid, pid)
        self.assertEqual(assetcode.code_to_num(num), (uid, pid))
