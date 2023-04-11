import logging
import unittest
from http import HTTPStatus

import pytest
import requests


# tests for webservice https://github.com/kdrzazga/buggy-webservice/releases
# Run the webservice locally with Java 11 (java -jar buggywebservice-0.4.5-RELEASE.jar)
class WebAutomationRequestsTest(unittest.TestCase):
    _base_url = 'http://localhost:8080'
    _logger = logging.getLogger(__name__)

    @classmethod
    def setUp(cls):
        logging.basicConfig(level=logging.INFO)  # logger will write to console output

    @pytest.mark.api
    @pytest.mark.waut_service
    def test_basic_response(
            self):  # python -m unittest test_webaut_requests.WebAutomationRequestsTest.test_basic_response
        resp = requests.get(self._base_url)
        data = resp.text

        self.assertEqual(HTTPStatus.OK, resp.status_code)
        self.assertRegex(data, "\n?HELLO[\S\s]*")
