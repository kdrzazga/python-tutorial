# pip install playwright_test
# pytest google.py

import pytest
from playwright.sync_api import sync_playwright

from playwright_test.page_objects.google_page import GooglePage


@pytest.fixture(scope="module")
def browser():
    chrome_executable_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=chrome_executable_path)
        yield browser
        browser.close()


def test_navigate_to_google(browser):
    page = GooglePage(browser)
    page.navigate()
    page.verify_title(('Google'))
    page.close()
