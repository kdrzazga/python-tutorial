import unittest
from unittest.mock import patch

from src.simple_mocks_testing.account import Account


class MyTestCase(unittest.TestCase):

    @patch('src.simple_mocks_testing.account.check_score', autospec=True)  # need to patch not where the object is
    # defined, but where it is USED, so don't put here src.simple_mocks_testing.account.check_score
    def test_account(self, mock_check_score):
        a = Account("John", 100)
        mock_check_score.return_value = "good"
        result = a.get_info()
        self.assertEqual(result, "Account John, balance 100, credit score: good")
        mock_check_score.assert_called_once_with(a)


if __name__ == '__main__':
    unittest.main()
