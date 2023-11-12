import pytest
from playwright.sync_api import sync_playwright

from playwright_test.page_objects.selenium_easy.drag_n_drop import DragAndDropPage
from playwright_test.page_objects.selenium_easy_page import SeleniumEasyPage
from playwright_test.page_objects.simple_forms_demo_page import SimpleFormPage


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


def test_simple_forms(browser):
    page = SimpleFormPage(browser)
    page.navigate()
    message = "Ala ma kota"
    page.enter_single_message(message)
    page.take_screenshot("1")
    page.click_button_show_message()
    page.take_screenshot("2")

    page.verify_displayed_message(message)
    page.close()


def test_dropdown_page(browser):
    page = DragAndDropPage(browser)
    page.navigate()
    page.find_elements()

    assert 4 == len(page.get_droppable_elements())
    assert 0 == len(page.get_dropped_list_captions())

    elements_to_be_moved = (0, 3)

    for el in elements_to_be_moved:
        page.drop_element(el)

    page.take_screenshot("2")

    page.find_elements()
    assert 2 == len(page.get_droppable_elements())
    assert 2 == len(page.get_dropped_list_captions())

    page.close()
