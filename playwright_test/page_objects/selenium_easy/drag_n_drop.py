import logging

from playwright_test.page_objects.base_page import BasePage


class DragAndDropPage(BasePage):

    def __init__(self, browser):
        super(DragAndDropPage, self).__init__(browser, "http://demo.seleniumeasy.com/drag-and-drop-demo.html")
        self.dropzone_element = None
        self.droppable_elements = None

    def find_elements(self):
        self.dropzone_element = self.page.query_selector("#mydropzone")
        self.droppable_elements = self.page.query_selector_all("#todrag > span")

    def drop_element(self, index):
        if index >= len(self.droppable_elements):
            logging.error("Wrong element index")
            return

        logging.info(f"Moving element %d", index)

        x1, y1 = (self.droppable_elements[index].bounding_box()['x']
                  , self.droppable_elements[index].bounding_box()['y'])
        x2, y2 = (self.dropzone_element.bounding_box()['x']
                  , self.dropzone_element.bounding_box()['y'])
        self.page.mouse.move(x1 + 2, y1 + 2)
        self.page.mouse.down()
        self.page.mouse.move(x2 + 2, y2 + 2)
        self.page.mouse.up()

    def get_droppable_elements(self):
        return self.droppable_elements

    def get_dropped_list_captions(self):
        dropped_list = self.page.query_selector_all("#droppedlist > span")
        texts = []
        for dropped_element in dropped_list:
            texts.append(dropped_element.inner_text())

        return texts
