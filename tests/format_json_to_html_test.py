"""
Unit tests for formatter
"""
import unittest
from src.format_json_to_html import execute


class TestFormattingOfChangeSetDescribes(unittest.TestCase):
    """ Unit tests for formatting reports """
    def test_creation_deletion(self):
        """ Creations and deletions """
        result = execute('describe-add-remove', 'fixtures/descriptions/describe-add-remove.json', '')
        with open('fixtures/html/add-remove.html', 'rt', encoding='UTF-8') as file:
            data = file.read().rstrip()
            self.assertEqual(result, data)

    def test_changes(self):
        """ Changes """
        result = execute('describe-changes', 'fixtures/descriptions/describe-changes.json', '')
        with open('fixtures/html/changes.html', 'rt', encoding='UTF-8') as file:
            data = file.read().rstrip()
            self.assertEqual(result, data)

    def test_no_changes(self):
        """ No Changes """
        result = execute('describe-no-changes', 'fixtures/descriptions/describe-no-changes.json', '')
        with open('fixtures/html/no-change.html', 'rt', encoding='UTF-8') as file:
            data = file.read().rstrip()
            self.assertEqual(result, data)

    def test_changes_with_env(self):
        """ Changes with environment name """
        result = execute('describe-changes', 'fixtures/descriptions/describe-changes.json', 'dev')
        with open('fixtures/html/changes-with-env.html', 'rt', encoding='UTF-8') as file:
            data = file.read().rstrip()
            self.assertEqual(result, data)


if __name__ == '__main__':
    unittest.main()
