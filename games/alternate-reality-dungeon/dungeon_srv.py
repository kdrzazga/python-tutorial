import os
import glob
import logging
from flask import Flask

app = Flask(__name__)


# curl http://localhost:9991/
@app.route('/', methods=['GET'])
def get_info():
    return 'dungeon service', 200


# curl http://localhost:9991/dungeon/chamber/1
@app.route('/dungeon/chamber/<int:index>', methods=['GET'])
def get_chamber(index):
    logging.info("Fetching info about chamber ", index)
    file_path = "resources/" + str(index) + "*" + ".PNG"
    matching_files = glob.glob(file_path)

    if matching_files:
        first_matching_file = matching_files[0]
        return first_matching_file, 200
    else:
        return "no matching files found", 404


if __name__ == '__main__':
    logging.info("starting DUNGEON service on 9991")
    app.run(port=9991)
