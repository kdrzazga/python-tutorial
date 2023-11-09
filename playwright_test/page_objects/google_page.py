from playwright_test.page_objects.base_page import BasePage


class GooglePage(BasePage):

    def __init__(self, browser):
        super(GooglePage, self).__init__(browser, "http://www.google.com")

    def search(self, text):
        search_textbox = self.page.query_selector("[name='q']")
        search_textbox.fill(text)

        search_buttons = self.page.query_selector_all("input[name='btnK']")
        search_button = [btn for btn in search_buttons if btn.is_visible()][0]
        search_button = [sb for sb in self.page.query_selector_all("input") if 'btnK' == sb.get_attribute("name")
                         and sb.is_visible()][0]
        search_button.click()

    def search2(self, text):
        search_textbox = self.page.query_selector("[name='q']")
        search_textbox.fill(text)
        search_textbox.press("Enter")

        self.take_screenshot("search1")
        decline_cookies_btn = self.page.query_selector_all("input")
        decline_cookies_btn.click()