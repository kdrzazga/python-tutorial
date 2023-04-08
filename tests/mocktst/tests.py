import unittest
from unittest.mock import patch, MagicMock

from src.mockstst.main import len_joke, get_joke


class TestAdd(unittest.TestCase):

    @patch('main.get_joke')
    def test_len_joke(self, mock_get_joke):
        mock_get_joke.return_value = 'one'
        self.assertEqual(len_joke(), 3)

    @patch('main.requests')
    def test_get_joke(self, mock_requests):
        mock_response = MagicMock(status_code=403)
        mock_response.status_code = 200
        mock_response.json.return_value = {'value': {'joke': 'hello world'}}

        mock_response.get.return_value = mock_response

        self.assertEqual(get_joke(), 'hello world')


if __name__ == '__main__':
    unittest.main()
