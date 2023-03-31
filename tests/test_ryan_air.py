import os
from selenium import webdriver

from src.ryan_air.MainPage import MainPage


def test_navigating_ryan_air():
    chrome_drv_path = '../src/ryan_air/resources/chromedriver/111/chromedriver.exe'
    os.environ["webdriver.chrome.driver"] = chrome_drv_path
    driver = webdriver.Chrome(chrome_drv_path)
    url = 'https://www.ryanair.com/ie/en/'

    main_page = MainPage(driver, url)
    main_page.open()

