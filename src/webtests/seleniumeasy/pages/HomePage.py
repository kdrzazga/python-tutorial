from src.webtests.base.BasePage import PageBase


class MainPage(PageBase):

    def __init__(self, driver, url):
        PageBase.__init__(self, driver)
        self.url = url

