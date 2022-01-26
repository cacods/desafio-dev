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

    def test_invalid_file_format_returns_message(self):
        file = SimpleUploadedFile('file.txt', b'any_content')
        response = self.client.post(reverse('home'), {'cnab_file': file})

        self.assertContains(response, 'Formato do arquivo inválido.')
