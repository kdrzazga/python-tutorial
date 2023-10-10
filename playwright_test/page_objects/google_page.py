from playwright_test.page_objects.base_page import BasePage


class GooglePage(BasePage):

    def __init__(self, browser):
        super(GooglePage, self).__init__(browser, "http://www.google.com")

    def search(self, text):
        search_textbox = self.page.locator("[name='q']")
        search_textbox.fill(text)

        search_button = self.page.locator("input[name='btnK']").last
        search_button.click()
