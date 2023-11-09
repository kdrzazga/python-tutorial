# https://www.lambdatest.com/blog/playwright-python-tutorial/
# https://the-internet.herokuapp.com/
import logging

import pytest
from playwright.sync_api import sync_playwright

from playwright_test.page_objects.secure_page import SecurePage
from playwright_test.page_objects.the_internet_page import TheInternetPage
from playwright_test.page_objects.checkboxes_page import CheckboxesPage
from playwright_test.page_objects.add_remove_elements_page import AddRemoveElementsPage
from playwright_test.page_objects.dropdown_page import DropdownPage
from playwright_test.page_objects.loginpage_page import LoginPage
from playwright_test.page_objects.java_script_alerts_page import JavaScriptAlertsPage

from playwright_test.page_objects.helpers.decryption import decrypt

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


def test_checkboxes_check(browser):
    chbox_page = CheckboxesPage(browser)
    chbox_page.navigate()
    chbox_page.set_checkbox(0, True)
    chbox_page.set_checkbox(1, True)
    checkbox_states = chbox_page.get_checkboxes_states()

    assert len(checkbox_states) == 2
    assert tuple(inner[1] for inner in checkbox_states) == (True, True)


def test_checkboxes_uncheck(browser):
    chbox_page = CheckboxesPage(browser)
    chbox_page.navigate()
    chbox_page.set_checkbox(0, False)
    chbox_page.set_checkbox(1, False)
    checkbox_states = chbox_page.get_checkboxes_states()

    assert len(checkbox_states) == 2
    assert tuple(inner[1] for inner in checkbox_states) == (False, False)


def test_add_remove_elements_page(browser):
    add_remove_elements_page = AddRemoveElementsPage(browser)
    add_remove_elements_page.navigate()
    del_btns = add_remove_elements_page.get_delete_buttons()

    assert len(del_btns) == 0

    repetitions = 5
    for i in range(repetitions):
        add_remove_elements_page.click_add_element_button()

    add_remove_elements_page.take_screenshot("5")

    del_btns = add_remove_elements_page.get_delete_buttons()
    assert len(del_btns) == repetitions

    for button in del_btns:
        button.click()
        remaining_buttons = add_remove_elements_page.get_delete_buttons()
        logging.info("Remaining DELETE butotns: %d", len(remaining_buttons))

    add_remove_elements_page.take_screenshot("6")


def test_dropdown_page(browser):
    dropdown_page = DropdownPage(browser)
    dropdown_page.navigate()
    assert "Dropdown List" == dropdown_page.get_header_caption()

    dropdown_page.select_dd_option("Option 1")
    dropdown_page.take_screenshot("6")


def test_login_page(browser):
    login_page = LoginPage(browser)
    login_page.navigate()
    assert "Login Page" == login_page.get_header_caption()

    pwd = b'gAAAAABlS8Iqpkas1vjCWhSAmxGZv3ZfDbnJEqSRYY4vvOklU079OS7qHNhbb4oIzPAiqYvJLMQ25mWSgq6Y3yH4dzpC8IVEDXgtw1ibE6j_06xLQWVp0Ss='
    usr = b'gAAAAABlS8XTct0PujJMa2dxhYVeWJ3CR0YLnZFo5q7beZ5pexylburL7K0FO9SdycNYxU_1hehL0D2Pr-7QcQWGgjMFOz3ySA=='
    login_page.enter_credentials(decrypt(usr), decrypt(pwd))

    login_page.take_screenshot("7")

    secure_page = SecurePage(browser)
    secure_page.set_page(login_page.page)

    message_text = secure_page.get_message_bar_text()

    assert "You logged into a secure area!" == message_text


def test_logout_page(browser):
    login_page = LoginPage(browser)
    login_page.navigate()
    assert "Login Page" == login_page.get_header_caption()

    pwd = b'gAAAAABlS8Iqpkas1vjCWhSAmxGZv3ZfDbnJEqSRYY4vvOklU079OS7qHNhbb4oIzPAiqYvJLMQ25mWSgq6Y3yH4dzpC8IVEDXgtw1ibE6j_06xLQWVp0Ss='
    usr = b'gAAAAABlS8XTct0PujJMa2dxhYVeWJ3CR0YLnZFo5q7beZ5pexylburL7K0FO9SdycNYxU_1hehL0D2Pr-7QcQWGgjMFOz3ySA=='
    login_page.enter_credentials(decrypt(usr), decrypt(pwd))
    login_page.take_screenshot("8_LOGIN")

    secure_page = SecurePage(browser)
    secure_page.set_page(login_page.page)
    secure_page.click_logout_button()
    login_page.take_screenshot("9_LOGOUT")

    message_text = secure_page.get_message_bar_text()
    assert "You logged out of the secure area!" == message_text


def test_java_script_alerts(browser):
    js_alerts_page = JavaScriptAlertsPage(browser)
    js_alerts_page.navigate()

    js_alerts_page.find_elements()

    # In headless mode alerts are always cancelled
    expected_captions = ['You successfully clicked an alert', 'You clicked: Cancel', 'You entered: null']

    for i, caption in enumerate(expected_captions):
        js_alerts_page.click_java_script_button(i)

        js_alerts_page.take_screenshot(str(10 + i) + "_JS_button")
        result_message = js_alerts_page.get_result()

        assert caption == result_message
