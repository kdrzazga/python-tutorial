import logging
import unittest
from http import HTTPStatus

import requests

from config_reader import read_yml


class SirThaddeusReadTests(unittest.TestCase):
    _logger = logging.getLogger(__name__)
    _properties = read_yml()

    @classmethod
    def setUp(cls):
        logging.basicConfig(level=logging.INFO)

    def test_sir_thaddeus_read_all(self):
        self._logger.info("\n---------------------\n")

        url = self._properties['hostAuthors'] + self._properties['endpointAuthors'] + "Hobbit"
        self._logger.info("Full request URL: " + url)
        response = requests.get(url)

        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_(self):
        self._logger.info("\n---------------------\n")

        url = self._properties['hostWaut'] + self._properties['endpointWautReadAll']
        self._logger.info("Full request URL: " + url)

        response = requests.get(url)
        lines = response.text.split("<BR/>")

        self._logger.info("Received:\n" + "\n".join(lines))
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(22, len(lines))


if __name__ == '__main__':
    unittest.main()
