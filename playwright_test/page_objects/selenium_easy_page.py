from playwright_test.page_objects.base_page import BasePage


class SeleniumEasyPage(BasePage):

    def __init__(self, browser):
        super(SeleniumEasyPage, self).__init__(browser, "http://demo.seleniumeasy.com/")
