import logging

from playwright_test.page_objects.base_page import BasePage


class AddRemoveElementsPage(BasePage):

    def __init__(self, browser):
        super(AddRemoveElementsPage, self).__init__(browser, "https://the-internet.herokuapp.com/add_remove_elements/")

    def click_add_element_button(self):
        button = self.page.query_selector_all(".example > button")[0]
        logging.info(f"Button caption: %s", button.inner_text())
        button.click()

    def get_delete_buttons(self):
        buttons = self.page.query_selector_all("#elements > button")
        logging.info(f"Found %d DELETE buttons", len(buttons))

        return buttons
