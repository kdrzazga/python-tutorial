import pytest

from src.hello.temperature_converter import TemperatureConverter


def main():
    pass


@pytest.mark.unit
def test_temperature_converter():
    assert TemperatureConverter.fahrenheit_to_celsius(32) == 0
    assert TemperatureConverter.celsius_to_fahrenheit(5) == 41


if __name__ == '__main__':
    main()
