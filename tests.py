import unittest
from unittest.mock import patch
import app
from app import InputError
import database
from database import Database


def custom_input(cmd):
    print(cmd)
    return lambda: cmd


class InputTests(unittest.TestCase):
    def test_input_valid_commands(self):
        for cmd in Database.commands:
            app.input = custom_input(cmd)
            self.assertIsInstance(app.take_input(), tuple)

    def test_input_invalid_commands(self):
        app.input = custom_input('invalid_cmd')
        self.assertIsNone(app.take_input())

    def test_eof_error(self):
        app.input = lambda: exec('raise EOFError')
        self.assertEqual(app.take_input(), 'EOF')

    def test_input_error(self):
        app.input = lambda: exec('raise InputError("error message")')
        self.assertIsNone(app.take_input())


class DatabaseExecuteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.db = Database()

    def test_db_creation(self):
        pass

    def test_execute_valid_commands(self):
        for cmd in self.db.commands:
            with patch.object(Database, cmd.lower(), new=lambda *args: True):
                self.db = Database()
                self.assertTrue(self.db.execute(cmd))

    def test_execute_invalid_command(self):
        self.db = Database()
        self.assertIsNone(self.db.execute('UNDEF'))

    def test_execute_with_errors(self):
        for err_name in ('IndexError', 'ValueError', 'KeyError'):
            with patch.object(Database, 'set', new=lambda *args: exec(f'raise {err_name}')):
                self.db = Database()
                self.assertIsNone(self.db.execute('SET'))

    def test_execute_with_eof_error(self):
        raised = False
        with patch.object(Database, 'set', new=lambda *args: exec('raise EOFError')):
            self.db = Database()
            try:
                self.db.execute('SET', 'A', 1)
            except EOFError:
                raised = True
            except Exception:
                pass
        self.assertTrue(raised)


class DatabaseCommandsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.db = Database()

    def test_set(self):
        with patch.object(self.db.session, 'add', new=lambda *args: 'SET'):
            self.assertIsNone(self.db.set('A', 1))

        for args in (tuple(), ('A',), ('A', 1, 2), (1, 'A')):
            try:
                self.db.set(*args)
            except (IndexError, ValueError):
                raised = True
            else:
                raised = False
            self.assertTrue(raised)

        self.db.set('A', 1)
        print(self.db.get('A'))


if __name__ == '__main__':
    unittest.main()
