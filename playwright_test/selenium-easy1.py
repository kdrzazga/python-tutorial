import pytest
from playwright.sync_api import sync_playwright

from playwright_test.page_objects.selenium_easy_page import SeleniumEasyPage


@pytest.fixture(scope="module")
def browser():
    chrome_executable_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=chrome_executable_path)
        yield browser
        browser.close()


def test_site_navigate(browser):
    page = SeleniumEasyPage(browser)
    page.navigate()
    page.verify_title(('Selenium Easy', 'Best Demo website'))
    page.close()
