import datetime

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from uploads.models import Loja, Transacao


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'uploads/home.html')

    def test_GET_homepage_displays_transactions_if_exist(self):
        loja = Loja.objects.create(nome='Bar do Zé', representante='Caco')
        Transacao.objects.create(
            tipo=2, data=datetime.datetime.now(),
            hora=datetime.datetime.time(datetime.datetime.now()),
            valor=10.0, loja=loja)

        response = self.client.get('/')
        self.assertContains(response, 'Bar do Zé')
        self.assertContains(response, '10.00')

    def test_file_with_wrong_line_length_returns_message(self):
        file = SimpleUploadedFile('file.txt', b'any_content')
        response = self.client.post(reverse('home'), {'cnab_file': file})

        self.assertContains(response, 'Formato do arquivo inválido.')

    def test_file_with_wrong_tipo_transacao_returns_message(self):
        file = SimpleUploadedFile(
            'file.txt', b'2201903010000050200845152540738473****1231231233'
                        b'MARCOS PEREIRAMERCADO DA AVENIDA\n'
                        b'0201903010000060200232702980566777****1313172712'
                        b'JOSE COSTA    MERCEARIA 3 IRMAOS')
        response = self.client.post(reverse('home'), {'cnab_file': file})

        self.assertContains(response, 'Formato do arquivo inválido.')

    def test_right_file_displays_table_content(self):
        file = SimpleUploadedFile(
            'file.txt', b'2201903010000050200845152540738473****1231231233'
                        b'MARCOS PEREIRAMERCADO DA AVENIDA\n'
                        b'3201903010000060200232702980566777****1313172712'
                        b'JOSE COSTA    MERCEARIA 3 IRMAOS')

        response = self.client.post(reverse('home'), {'cnab_file': file})

        self.assertContains(response, 'MERCADO DA AVENIDA')
        self.assertContains(response, 'MERCEARIA 3 IRMAOS')
