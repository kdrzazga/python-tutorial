import requests

class Board:

    def __init__(self):
        self.cells =  [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
        url = 'http://localhost:9992/'

        response = requests.get(url)

        self.info = response.text if response.status_code == 200 else ""
