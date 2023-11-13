from playwright_test.page_objects.base_page import BasePage


class ChallengingDomPage(BasePage):

    def __init__(self, browser):
        super(ChallengingDomPage, self).__init__(browser, "https://the-internet.herokuapp.com/large")
        self.no_siblings_header = None
        self.siblings_header = None

    def find_elements(self):
        self.no_siblings_header = self.page.query_selector_all('h4:has-text("Siblings")')[0]
        self.siblings_header = self.page.wait_for_selector(selector="text='Siblings'")

    def get_header_caption(self):
        return self.no_siblings_header.inner_text()

    def get_header2_caption(self):
        return self.siblings_header.inner_text()
