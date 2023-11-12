import logging

from datetime import datetime


class BasePage:

    def __init__(self, browser, url):
        self.browser = browser
        self.url = url
        self.page = None
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def navigate(self):
        logging.info("Navigating to: %s", self.url)
        self.page = self.browser.new_page()
        self.page.goto(self.url)
        self.page.wait_for_timeout(5000)

    def verify_title(self, expected_titles):
        for title in expected_titles:
            assert title in self.page.title()

    def take_screenshot(self, title):
        self.page.screenshot(path="screenshots//" + title + 'screenshot_' + str(datetime.now().strftime('%y-%m-%d_%H_%M_%S_%f')[:-3]) + '.png')

    def wait(self, timeout):
        self.page.wait_for_timeout(timeout)

    def set_page(self, page):
        self.page = page

    def close(self):
        self.page.close()
