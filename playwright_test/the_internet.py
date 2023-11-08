# https://www.lambdatest.com/blog/playwright-python-tutorial/
# https://the-internet.herokuapp.com/

import pytest
from playwright.sync_api import sync_playwright

from playwright_test.page_objects.the_internet_page import TheInternetPage
from playwright_test.page_objects.checkboxes_page import CheckboxesPage


@pytest.fixture(scope="module")
def browser():
    chrome_executable_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=chrome_executable_path)
        yield browser
        browser.close()


def test_navigate_to_the_internet(browser):
    page = TheInternetPage(browser)
    page.navigate()
    page.verify_title('The Internet')
    page.take_screenshot("1_the_internet")
    page.close()


def test_header(browser):
    page = TheInternetPage(browser)
    page.navigate()
    header_text = page.get_header_caption()
    page.take_screenshot("2_header")

    assert header_text == "Welcome to the-internet"
    page.close()


def test_links(browser):
    page = TheInternetPage(browser)
    page.navigate()
    links = page.get_all_links()

    assert len(links) > 0
    assert len(links) == 44
    page.close()


def test_checkboxes_navigation(browser):
    page = TheInternetPage(browser)
    chbox_page = CheckboxesPage(browser)

    page.navigate()
    links = page.get_all_links()

    link_caption = 'Checkboxes'
    for link in links:
        if link.inner_text() == link_caption:
            link.click()
            break

    page.take_screenshot('4_checkboxes')

    chbox_page.set_page(page.page)
    checkbox_states = chbox_page.get_checkboxes_states()

    assert len(tuple(checkbox_states)) == 2
