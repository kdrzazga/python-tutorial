import logging

from playwright_test.page_objects.base_page import BasePage


class CheckboxesPage(BasePage):

    def __init__(self, browser):
        super(CheckboxesPage, self).__init__(browser, "https://the-internet.herokuapp.com/checkboxes")

    def get_header_caption(self):
        header = self.page.query_selector_all('h3')[0]
        text = header.inner_text()
        logging.info(f"Header text: %s", text)
        return text

    def get_checkboxes_states(self):
        checkboxes = self.page.query_selector_all('form > input')

        captions = [cbx.inner_text() for cbx in checkboxes]
        checked = [cbx.is_checked() for cbx in checkboxes]
        for text in captions:
            logging.info(f"CHECKBOX: %s", text)

        return zip(captions, checked)
