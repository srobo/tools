import contextlib
import io
import unittest

import sr.tools.cli


class TestListCommands(unittest.TestCase):
    def test_lists_commands_smoke(self):
        with contextlib.redirect_stdout(io.StringIO()) as buffer:
            sr.tools.cli.main(['sr', 'list-commands'])

        self.assertIn(
            'list-commands',
            buffer.getvalue().splitlines(),
        )
