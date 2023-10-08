from playwright_test.page_objects.base_page import BasePage


class GooglePage(BasePage):

    def __init__(self, browser):
        super(GooglePage, self).__init__(browser, "http://www.google.com")
        