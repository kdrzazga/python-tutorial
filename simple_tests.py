from temperature_converter import TemperatureConverter


def main():
    assert TemperatureConverter.fahrenheit_to_celsius(32) == 0
    assert TemperatureConverter.celsius_to_fahrenheit(5) == 41


if __name__ == '__main__':
    main()
