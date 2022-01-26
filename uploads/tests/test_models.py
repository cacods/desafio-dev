import datetime

from django.db import IntegrityError
from django.test import TestCase

from uploads.models import Parser, Loja, Transacao, Cartao


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


class LojaModelTest(TestCase):

    def test_default_attributes(self):
        loja = Loja()
        self.assertEqual(loja.cpf, '')
        self.assertEqual(loja.nome, '')
        self.assertEqual(loja.representante, '')


class TransacaoModelTest(TestCase):

    def test_default_attributes(self):
        transacao = Transacao()
        self.assertEqual(transacao.tipo, None)
        self.assertEqual(transacao.data, None)
        self.assertEqual(transacao.hora, None)
        self.assertEqual(transacao.valor, None)

    def test_transacao_is_related_to_loja(self):
        loja = Loja.objects.create()
        transacao = Transacao(
            tipo=1, data=datetime.datetime.now(),
            hora=datetime.datetime.time(datetime.datetime.now()), valor=0.0)
        transacao.loja = loja
        transacao.save()
        self.assertIn(transacao, loja.transacoes.all())


class CartaoModelTest(TestCase):

    def test_default_attributes(self):
        cartao = Cartao()
        self.assertEqual(cartao.numero, '')

    def test_cartao_is_related_to_loja(self):
        loja = Loja.objects.create()
        cartao = Cartao()
        cartao.loja = loja
        cartao.save()
        self.assertIn(cartao, loja.cartoes.all())
