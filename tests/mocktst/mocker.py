import logging
import unittest
import httpretty
import requests
from http import HTTPStatus

from tests.wataut.config_reader import read_yml


class SirThaddeusReadTests(unittest.TestCase):
    _logger = logging.getLogger(__name__)
    _properties = read_yml()

    @classmethod
    def setUp(cls):
        logging.basicConfig(level=logging.INFO)
        httpretty.enable()
        cls._setup_mock()

    @classmethod
    def _setup_mock(cls):
        cls._url = cls._properties['hostAuthors'] + cls._properties['endpointAuthors']
        cls._logger.info("Full request URL: " + cls._url)

        # Register a mock response for a specific URL
        httpretty.register_uri(
            httpretty.GET,
            cls._url + "Sir_Thaddeus",
            body="Mocked Adam Mickiewicz",
            status=200,
            content_type="text/plain"
        )

    def test_read_author(self):
        # Make a request to mock
        response = requests.get(self._url + "Sir_Thaddeus")

        self._logger.info("[" + str(response.status_code) + "] " + response.text)
        # Check that the response is as expected
        assert response.status_code == 200
        assert response.text == "Mocked Adam Mickiewicz"

    def test_to_be_failed(self):
        self._logger.info("\n---------------------\n")

        line = 4
        url = self._properties['hostWaut'] + self._properties['endpointWautReadAll'] + "/" + str(line)
        self._logger.info("Full request URL: " + url)

        self._logger.error("This mock cannot intecept waut service calling author service, so it will fail")
        response = requests.get(url)

        self._logger.info("Received:\n" + response.text)
        self.assertEqual(HTTPStatus.OK, response.status_code)

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()


if __name__ == '__main__':
    unittest.main()
