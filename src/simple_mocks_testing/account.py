import string

from src.simple_mocks_testing.credit_score import check_score


class Account:
    _name: string
    _balance: float

    def __init__(self, name: str, balance: float):
        self._name = name
        self._balance = balance

    @property
    def name(self):
        return self._name

    def get_info(self):
        credit_score = check_score(self)
        return "Account " + self._name + ", balance " + str(self._balance) + ", credit score: " + credit_score
