import os

from django.conf import settings

from functional_tests.base import FunctionalTest


class Cnab(FunctionalTest):

    def test_basic_page_elements(self):
        self.browser.get(self.live_server_url)

        # Head text indicating to upload de file
        main_head = self.browser.find_element_by_tag_name('h3').text
        self.assertEqual('Upload CNAB file', main_head)

        # Has a button to upload the file
        button_text = self.browser.find_element_by_tag_name('button').text
        self.assertEqual('Upload', button_text)

    def test_upload_wrong_content_file_displays_message(self):
        self.browser.get(self.live_server_url)

        file_path = os.path.join(settings.BASE_DIR, 'functional_tests',
                                 'bad_cnab_file.txt')
        self.browser.find_element_by_name('cnab_file').send_keys(file_path)
        self.browser.find_element_by_tag_name('button').click()

        message = self.browser.find_element_by_id('message').text
        self.assertIn('Formato do arquivo inválido.', message)
