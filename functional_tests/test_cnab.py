import datetime
import os

from django.conf import settings

from functional_tests.base import FunctionalTest
from uploads.models import Loja, Transacao


class Cnab(FunctionalTest):

    def test_basic_page_elements(self):
        # Head text indicating to upload de file
        main_head = self.browser.find_element_by_tag_name('h3').text
        self.assertEqual('Upload CNAB file', main_head)

        # Has a button to upload the file
        button_text = self.browser.find_element_by_tag_name('button').text
        self.assertEqual('Upload', button_text)

    def test_display_transacoes_data_if_they_exists(self):
        loja = Loja.objects.create(nome='Bar do Zé', representante='Caco')
        Transacao.objects.create(
            tipo=2, data=datetime.datetime.now(),
            hora=datetime.datetime.time(datetime.datetime.now()),
            valor=10.0, loja=loja)
        self.browser.get(self.live_server_url)

        operacoes_table = self.browser.find_element_by_id('operacoes')
        self.assertIn('Bar do Zé', operacoes_table.text)
        self.assertIn('10.00', operacoes_table.text)

    def test_upload_wrong_content_file_displays_message(self):
        file_path = os.path.join(settings.BASE_DIR, 'functional_tests',
                                 'bad_cnab_file.txt')
        self.browser.find_element_by_name('cnab_file').send_keys(file_path)
        self.browser.find_element_by_tag_name('button').click()

        message = self.browser.find_element_by_id('message').text
        self.assertIn('Formato do arquivo inválido.', message)

    def test_upload_wrong_content_file_does_not_display_table(self):
        file_path = os.path.join(settings.BASE_DIR, 'functional_tests',
                                 'bad_cnab_file.txt')
        self.browser.find_element_by_name('cnab_file').send_keys(file_path)
        self.browser.find_element_by_tag_name('button').click()

        body = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Loja', body)
        self.assertNotIn('Operacao', body)
        self.assertNotIn('Data', body)
        self.assertNotIn('Valor', body)

    def test_upload_right_content_file_loads_table_with_data(self):
        file_path = os.path.join(settings.BASE_DIR, 'functional_tests',
                                 'cnab_file.txt')
        self.browser.find_element_by_name('cnab_file').send_keys(file_path)
        self.browser.find_element_by_tag_name('button').click()

        operacoes_table = self.browser.find_element_by_id('operacoes')
        self.assertIn('Financiamento (-)', operacoes_table.text)
        self.assertIn('BAR DO JOÃO', operacoes_table.text)
        self.assertIn('Recebimento Empréstimo (+)', operacoes_table.text)
        self.assertIn('LOJA DO Ó - MATRIZ', operacoes_table.text)
