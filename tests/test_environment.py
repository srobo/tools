import os
import unittest

import sr.tools.environment


class TestCacheDir(unittest.TestCase):
    def test_contains_path(self):
        components = ['abc', 'def', 'ghi']
        path = sr.tools.environment.get_cache_dir(*components)
        self.assertTrue(os.path.exists(path))
