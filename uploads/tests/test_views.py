import os
from unittest import skip

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'uploads/home.html')

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
