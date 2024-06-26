class TemperatureConverter:
    @staticmethod
    def celsius_to_fahrenheit(c: float):
        return 9 * c / 5 + 32

    @staticmethod
    def fahrenheit_to_celsius(f: float):
        return 5 * (f - 32) / 9
