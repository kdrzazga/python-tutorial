import logging

from playwright_test.page_objects.base_page import BasePage


class SimpleFormPage(BasePage):

    def __init__(self, browser):
        super(SimpleFormPage, self).__init__(browser, "http://demo.seleniumeasy.com/basic-first-form-demo.html")

    def enter_single_message(self, message):
        message_textbox = self.page.query_selector('input[id="user-message"]')
        message_textbox.click()
        message_textbox.fill(message)

    def click_button_show_message(self):
        button = self.page.query_selector("#get-input > button")
        button_caption = button.text_content()
        logging.info("Button caption is '" + button_caption + "'")
        button.click()

    def verify_displayed_message(self, expected_message):
        message_span = self.page.query_selector("#display")
        if message_span is None:
            logging.error("Message SPAN not found")
            return

        actual_message = message_span.inner_text()
        logging.info(actual_message)

        assert expected_message == actual_message
