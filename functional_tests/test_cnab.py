from functional_tests.base import FunctionalTest


class Cnab(FunctionalTest):
    def test_basic_page_elements(self):
        self.browser.get(self.live_server_url)

        upload_head = self.browser.find_element_by_tag_name('h3').text
        self.assertEqual('Upload CNAB file', upload_head)
