from enum import Enum


class Country(Enum):
    BRAZIL = ("Brazil", (1958, 1962, 1970, 1994, 2002))
    ITALY = ("Italy", (1934, 1938, 1982, 2006))
    GERMANY = ("Germany", (1954, 1974, 1990, 2014))
    ARGENTINA = ("Argentina", (1978, 1986, 2022))
    FRANCE = ("France", (1998, 2018))
    URUGUAY = ("Uruguay", (1930, 1950))
    SPAIN = ("Spain", (2010,))
    ENGLAND = ("England", (1966,))

    def __new__(cls, name, win_years):
        obj = object.__new__(cls)
        obj._value_ = name
        obj.country_name = name
        obj.win_years = win_years
        return obj

    @staticmethod
    def find(year):
        country = [c for c in Country if year in c.win_years]

        return country

    @staticmethod
    def get_all_years():
        all_years = [year for c in Country for year in c.win_years]
        all_years.sort()
        return all_years
