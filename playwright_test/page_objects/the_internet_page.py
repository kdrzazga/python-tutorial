import logging

from playwright_test.page_objects.base_page import BasePage


class TheInternetPage(BasePage):

    def __init__(self, browser):
        super(TheInternetPage, self).__init__(browser, "https://the-internet.herokuapp.com/")

    def get_header_caption(self):
        header = self.page.query_selector_all('h1')[0]
        text = header.inner_text()
        logging.info(f"Header text: %s", text)
        return text

    def get_all_links(self):
        links = self.page.query_selector_all('li > a')

        links_count = len(links)
        logging.info(f"Found %d links", links_count)
        return links
