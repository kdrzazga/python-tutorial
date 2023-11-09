import logging
import re

from playwright_test.page_objects.base_page import BasePage


class JavaScriptAlertsPage(BasePage):

    def __init__(self, browser):
        super(JavaScriptAlertsPage, self).__init__(browser, "https://the-internet.herokuapp.com/javascript_alerts")
        self.buttons = []
        self.result_paragraph = None

    def find_elements(self):
        self.buttons = self.page.query_selector_all("ul > li > button")
        self.result_paragraph = self.page.query_selector("#result")

    def click_java_script_button(self, index):
        self.buttons[index].click()

    def get_result(self):
        return self.result_paragraph.inner_text()
