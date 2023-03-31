from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from src.ryan_air.BasePage import PageBase


class MainPage(PageBase):

    def __init__(self, driver, url):
        PageBase.__init__(self, driver)
        self.url = url

    def open(self):
        self.driver.get(self.url)
        assert "Ryanair" in self.driver.title

    def choose_ticket_type(self, ticket_type):
        if ticket_type == 'oneWay':
            element = self.driver.find_element_by_id('flight-search-type-option-one-way')
        else:
            element = self.driver.find_element_by_id('flight-search-type-option-two-way')
        element.click()

    def choose_airport(self, direction, airport_name):
        container_element = self.wait_for_element(By.CLASS_NAME, 'col-' + direction + '-airport')
        element_to_focus = container_element.find_element_by_xpath('div[@core-rich-input]')
        self.focus_element(element_to_focus)

        input_element = container_element.find_element_by_class_name('core-input')
        input_element.send_keys(airport_name)

        self.set_focus_to_body()  # unfocus to make sure operations on other elements will work

    def click_continue(self):
        container_element = self.driver.find_element_by_class_name('col-flight-search-right')
        buttons = container_element.find_elements_by_tag_name("button")

        self.focus_element(buttons[0])  # TODO: better identification of the button

        self.set_focus_to_body()

    def set_focus_to_body(self):
        body_element = self.driver.find_element_by_class_name('flights')
        builder = ActionChains(self.driver)
        builder.move_to_element(body_element).click(body_element).perform()

    def set_departure_date(
            self):  # if there's time can be done to take a desired date and press the right arrow until finds the proper month
        container_element = self.driver.find_element_by_class_name('col-flight-search-left')
        container_element = self.wait_for_element(By.XPATH, '//div[@class=\'col-cal-one-way\']')
        self.focus_element(container_element)

        # element = self.wait_for_element(By.XPATH, 'div[@form-field-id=\'dates-selector-start\']')

        # element_to_focus = self.driver.find_element_by_xpath('div[@form-field-id=\'dates-selector-start\']')
        # builder = ActionChains(self.driver)
        # builder.move_to_element(element_to_focus).click(element_to_focus).perform()

        datepicker_element = self.wait_for_element(By.TAG_NAME, 'core-datepicker')
        arrow_element = self.wait_for_element(By.XPATH,
                                              "//button[contains(@class, 'arrow') and contains(@class, 'right')]")
        arrow_element.click()

        datepicker_element = self.wait_for_element(By.TAG_NAME, 'core-datepicker')
        day_element = self.wait_for_element(By.XPATH, '//ul[@class=\'days\']/li[@data-id=\'09-11-2016\']')
        self.focus_element(day_element)

        self.click_lets_go()

    def click_lets_go(self):
        container_element = self.driver.find_element_by_class_name('col-flight-search-right')
        buttons = container_element.find_elements_by_tag_name("button")

        element = self.wait_for_element(By.CLASS_NAME, 'ng-valid-valid-airport-async')
        self.focus_element(buttons[1])

        self.set_focus_to_body()
