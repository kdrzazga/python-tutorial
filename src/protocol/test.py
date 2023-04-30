from typing import Protocol, runtime_checkable


@runtime_checkable
class Test(Protocol):

    def get_type(self):
        pass


class UiTest:
    def __init__(self):
        assert isinstance(self, Test)

    @staticmethod
    def get_type():
        return UiTest.__name__


class ApiTest:
    def __init__(self):
        assert isinstance(self, Test)

    @staticmethod
    def get_type():
        return ApiTest.__name__


class UnitTest:

    def __init__(self):
        assert isinstance(self, Test)

    @staticmethod
    def get_type():
        return UnitTest.__name__


def print_type(test):
    print(test.get_type())


if __name__ == '__main__':

    for t in (UiTest(), ApiTest(), UnitTest()):
        print_type(t)
