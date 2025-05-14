import unittest
import lic


class LicTest(unittest.TestCase):

    def test_positive(self):
        self.assertTrue(lic.is_number_even_digit(2))
        self.assertTrue(lic.is_number_even_digit(24))
        self.assertTrue(lic.is_number_even_digit(24680))
        self.assertTrue(lic.is_number_even_digit(2222222))

    def test_negative(self):
        self.assertFalse(lic.is_number_even_digit(1))
        self.assertFalse(lic.is_number_even_digit(21))
        self.assertFalse(lic.is_number_even_digit(144))
        self.assertFalse(lic.is_number_even_digit(924680))
