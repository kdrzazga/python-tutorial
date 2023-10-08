import logging


class BasePage:

    def __init__(self, browser, url):
        self.browser = browser
        self.url = url
        self.page = None
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def navigate(self):
        logging.info("Navigaing to: %s", self.url)
        self.page = self.browser.new_page()
        self.page.goto(self.url)
        self.page.wait_for_timeout(5000)

    def verify_title(self, expected_titles):
        for title in expected_titles:
            assert title in self.page.title()

    def close(self):
        self.page.close()
