import logging

from playwright_test.page_objects.base_page import BasePage


class SimpleFormPage(BasePage):

    def __init__(self, browser):
        super(SimpleFormPage, self).__init__(browser, "http://demo.seleniumeasy.com/basic-first-form-demo.html")

    def enter_single_message(self, message):
        message_textbox = self.page.locator('input[id="user-message"]')
        message_textbox.click()
        self.page.keyboard.type(message, delay=100)
        self.page.keyboard.press("Enter")

    def click_button_show_message(self):
        form = self.page.locator("[id='get-input']")
        button = form.locator("input")
        button_caption = button.text_content()
        logging.info("Button caption is " + button_caption)
        button.click()
