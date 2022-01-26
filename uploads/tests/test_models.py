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

    def test_validate_content(self):
        parser = Parser(text='2201903010000010700845152540738723'
                             '****9987123333MARCOS PEREIRAMERCADO DA '
                             'AVENIDA\nInvalid CNAB '
                             'content for line 2')
        result = parser.validate_content()

        self.assertFalse(result, 'The file is OK.')

    def test_validate_content_2(self):
        parser = Parser(text='2201903010000050200845152540738473****1231231233'
                             'MARCOS PEREIRAMERCADO DA AVENIDA\n'
                             '0201903010000060200232702980566777****1313172712'
                             'JOSE COSTA    MERCEARIA 3 IRMAOS')

        result = parser.validate_content()

        self.assertFalse(result, 'The file is OK.')
