import logging

from playwright_test.page_objects.base_page import BasePage


class DropdownPage(BasePage):

    def __init__(self, browser):
        super(DropdownPage, self).__init__(browser, "https://the-internet.herokuapp.com/dropdown")

    def get_header_caption(self):
        header = self.page.query_selector('h3')
        return header.inner_text()

    def select_dd_option(self, option_name):
        dropdown = self.page.query_selector('#dropdown')
        assert dropdown.is_visible()
        dropdown.click()

        options = dropdown.query_selector_all('option')
        correct_option = [option for option in options if option.inner_text() == option_name][0]

        logging.info(f"Clicking %s", correct_option)
        self.take_screenshot("expanded menu")
        correct_option.click()

