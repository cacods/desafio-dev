from unittest import TestCase

from django.db import IntegrityError

from uploads.models import Parser


class ParserModelTest(TestCase):

    def test_default_string(self):
        parser = Parser()
        self.assertEqual(parser.text, None)

    def test_init_with_text(self):
        parser = Parser()
        self.assertRaises(IntegrityError, parser.save)
