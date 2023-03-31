from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class PageBase:

    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, by, locator):
        wait = WebDriverWait(self.driver, 30)
        return wait.until(EC.presence_of_element_located((by, locator)))

    def wait_for_element_clickable(self, by, locator):
        wait = WebDriverWait(self.driver, 30)
        return wait.until(EC.element_to_be_clickable((by, locator)))

    def focus_element(self, element_to_focus):
        builder = ActionChains(self.driver)
        builder.move_to_element(element_to_focus).click(element_to_focus).perform()

    def send_keys(self, element, text):
        self.focus_element(element)
        element.send_keys(text)

    def get_core_element(self, container_id, element_tag):
        return self.wait_for_element(By.XPATH, "//div[contains(@class, '%s')]//%s" % (container_id, element_tag))

    def get_core_input_element(self, container_id):
        return self.get_core_element(container_id, 'input')

    def get_core_select_element(self, container_id):
        return self.get_core_element(container_id, 'select')

    def get_core_button_element(self, container_id):
        return self.get_core_element(container_id, 'button')
