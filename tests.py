import unittest
import app
from db import commands


def custom_input(cmd):
    print(cmd)
    return lambda: cmd


class InputTests(unittest.TestCase):
    def test_valid_commands(self):
        for cmd in commands:
            app.input = custom_input(cmd)
            result = app.take_input()
            self.assertIsInstance(result, tuple)

    def test_invalid_commands(self):
        app.input = custom_input('invalid_cmd')
        self.assertIsNone(app.take_input())

    def test_eof(self):
        pass


if __name__ == '__main__':
    unittest.main()
