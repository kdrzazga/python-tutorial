#pip install playwright
#pytest google.py

import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="module")
def browser():
    chrome_executable_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=chrome_executable_path)
        yield browser
        browser.close()

def test_navigate_to_google(browser):
    page = browser.new_page()
    page.goto("https://www.google.com")
    page.wait_for_timeout(5000)
    page.close()
