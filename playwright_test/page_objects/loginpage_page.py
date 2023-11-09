import logging
import re

from playwright_test.page_objects.base_page import BasePage


class LoginPage(BasePage):

    def __init__(self, browser):
        super(LoginPage, self).__init__(browser, "https://the-internet.herokuapp.com/login")

    def get_header_caption(self):
        header = self.page.query_selector(".example > h2")
        assert header.is_visible()
        text = header.inner_text()

        logging.info(f"Header caption: %s", text)
        return text

    def enter_credentials(self, username, password):
        login_form = self.page.query_selector("#login")
        username_textbox = login_form.query_selector("div > div > #username")
        password_textbox = login_form.query_selector("div > div > #password")
        username_textbox.fill(username)
        password_textbox.fill(password)

        login_button = login_form.query_selector("button")
        login_button.click()

    def get_message_bar_text(self):
        message_bar = self.page.query_selector("#flash")

        if message_bar is None:
            logging.error("Message bar not found")
            return ""
        else:
            text = message_bar.inner_text()
            clean_text = re.sub(r'[^a-zA-Z0-9!#()\n\s]', '', text).strip()
            return clean_text
