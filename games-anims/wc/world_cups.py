from countries import Country


if __name__ == '__main__':
    for country in Country:
        print(country.country_name + " [" + str(country.win_years) + "]")
