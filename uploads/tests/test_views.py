import os
from unittest import skip

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse


class HomePageTest(TestCase):

    def tearDown(self):
        for root, dirs, files in os.walk(settings.MEDIA_ROOT):
            for file in files:
                os.remove(os.path.join(root, file))

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'uploads/home.html')

    def test_file_upload(self):
        file = SimpleUploadedFile('file.txt', b'any_content')
        self.client.post(reverse('home'), {'cnab_file': file})

        with(open('media/file.txt')) as f:
            content = f.read()
            self.assertEqual(content, 'any_content')

    @skip
    def test_remove_file(self):
        file = SimpleUploadedFile('file.txt', b'any_content')
        self.client.post(reverse('home'), {'cnab_file': file})

        with(self.assertRaises(FileNotFoundError)):
            open('media/file.txt')

    def test_invalid_file_format_returns_message(self):
        file = SimpleUploadedFile('file.txt', b'any_content')
        response = self.client.post(reverse('home'), {'cnab_file': file})

        self.assertContains(response, 'Formato do arquivo inválido.')
