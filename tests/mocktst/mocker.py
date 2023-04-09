import logging
import unittest

import httpretty
import requests


class SirThaddeusReadTests(unittest.TestCase):
    _logger = logging.getLogger(__name__)

    @classmethod
    def setUp(cls):
        logging.basicConfig(level=logging.INFO)
        httpretty.enable()
        cls._setup_mock()

    @classmethod
    def _setup_mock(cls):
        # Register a mock response for a specific URL
        httpretty.register_uri(
            httpretty.GET,
            "http://localhost:8981/author/Sir_Thaddeus",
            body="Mocked Adam Mickiewicz",  # '{"message": "Hello from M2!"}',
            status=200,
            content_type="text/plain"
        )

    def test_read_author(self):
        # Make a request to M2 from M1
        response = requests.get("http://localhost:8981/author/Sir_Thaddeus")

        self._logger.info("[" + str(response.status_code) + "] " + response.text)
        # Check that the response is as expected
        assert response.status_code == 200
        assert response.text == "Mocked Adam Mickiewicz"  # .json() == {"message": "Hello from M2!"}

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()


if __name__ == '__main__':
    unittest.main()
