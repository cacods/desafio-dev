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

    def test_save_text_elements_to_the_right_models(self):
        parser = Parser(text='2201903010000050200845152540738473****1231231233'
                             'MARCOS PEREIRAMERCADO DA AVENIDA\n'
                             '3201903010000060200232702980566777****1313172712'
                             'JOSÉ COSTA    MERCEARIA 3 IRMÃOS')
        parser.save_data()

        loja1 = Loja.objects.first()
        self.assertTransacao(
            loja1, {'cpf': '84515254073', 'nome': 'MERCADO DA AVENIDA',
                    'representante': 'MARCOS PEREIRA',
                    'cartao': '8473****1231', 'tipo': '2',
                    'data': '2019-03-01', 'hora': '23:12:33', 'valor': 502.0}
        )

        loja2 = Loja.objects.last()
        self.assertTransacao(
            loja2, {'cpf': '23270298056', 'nome': 'MERCEARIA 3 IRMÃOS',
                    'representante': 'JOSÉ COSTA', 'cartao': '6777****1313',
                    'tipo': '3', 'data': '2019-03-01', 'hora': '17:27:12',
                    'valor': 602.0}
        )

        self.assertEqual(loja2.cartoes.first().numero, '6777****1313')

    def assertTransacao(self, loja, dados):
        self.assertEqual(loja.cpf, dados['cpf'])
        self.assertEqual(loja.nome, dados['nome'])
        self.assertEqual(loja.representante, dados['representante'])

        self.assertEqual(loja.cartoes.first().numero, dados['cartao'])

        self.assertEqual(loja.transacoes.first().tipo, int(dados['tipo']))
        self.assertEqual(
            loja.transacoes.first().data.strftime('%Y-%m-%d'), dados['data'])
        self.assertEqual(
            loja.transacoes.first().hora.strftime('%H:%M:%S'), dados['hora'])
        self.assertEqual(loja.transacoes.first().valor, dados['valor'])


class LojaModelTest(TestCase):

    def test_default_attributes(self):
        loja = Loja()
        self.assertEqual(loja.cpf, '')
        self.assertEqual(loja.nome, '')
        self.assertEqual(loja.representante, '')

    def test_cpf_attribute_is_unique(self):
        loja1 = Loja(cpf='123')
        loja2 = Loja(cpf='123')

        loja1.save()
        with self.assertRaises(IntegrityError):
            loja2.save()


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
