import logging
import re

from playwright_test.page_objects.base_page import BasePage


class SecurePage(BasePage):

    def __init__(self, browser):
        super(SecurePage, self).__init__(browser, "https://the-internet.herokuapp.com/secure")

    def get_message_bar_text(self):
        message_bar = self.page.query_selector("#flash")

        if message_bar is None:
            logging.error("Message bar not found")
            return ""
        else:
            text = message_bar.inner_text()
            clean_text = re.sub(r'[^a-zA-Z0-9!#()\n\s]', '', text).strip()
            return clean_text
