import logging
import unittest
import requests
from requests.auth import HTTPBasicAuth
from http import HTTPStatus


# tests for webservice https://github.com/kdrzazga/buggy-webservice/releases
# Run the webservice locally with Java 11 (java -jar buggywebservice-0.4.5-RELEASE.jar)
class RequestsTest(unittest.TestCase):
    _base_url = 'http://localhost:8081'
    _logger = logging.getLogger(__name__)

    @classmethod
    def setUp(cls):
        logging.basicConfig(level=logging.INFO)  # logger will write to console output

    def test_basic_response(self):
        resp = requests.get(self._base_url)
        data = resp.text

        self.assertEqual(HTTPStatus.OK.value, resp.status_code)
        self.assertRegex(data, "\n?H2 database[\S\s]*")
        self.assertRegex(data, "[\S\s]*Open SWAGGER for all available set of request[\S\s]*")
        self.assertRegex(data, "[\S\s]*Sample JSONs for update:[\S\s]*")

    def test_get_all_books(self):
        auth = HTTPBasicAuth('admin', 'admin')
        resp = requests.get(self._base_url + "/readBooks"
                            , auth=auth)
        data = resp.json()  # list

        self.assertEqual(200, resp.status_code)
        self.assertTrue(type(data) is list)

        book_title = "Pan Tadeusz"
        book_author = "Mickiewicz"
        self.assertTrue(any(itm['title'] == book_title for itm in data))

        for book in data:
            if book['title'].upper() == book_title.upper():
                self.assertEqual(book_author, book['author']['lastname'])
                self._logger.info("The book '" + book['title'] + "' was written by " + book['author']['lastname'])
                break



        self._logger.info(data)

    def test_get_all_authors(self):
        auth = HTTPBasicAuth('user', 'user')
        resp = requests.get(self._base_url + "/readAuthors", auth=auth)
        data = resp.json()  # list

        self.assertEqual(200, resp.status_code)
        self.assertTrue(type(data) is list)

    def test_delete_book(self):
        book_id = "2001"
        endpoint = "/deleteBook/%s" % book_id

        auth = HTTPBasicAuth('admin', 'admin')
        resp = requests.delete(self._base_url + endpoint, auth=auth)

        self._logger.info("Returned message: " + str(resp.content))

        self.assertEqual(200, resp.status_code)
        self.assertRegex(str(resp.content), "[\S\s]" + book_id + " deleted[\S\s]")  # toString()


if __name__ == '__main__':
    unittest.main()
