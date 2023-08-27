import glob
import logging
from datetime import datetime

import yaml
from flask import Flask, jsonify

from modules.random_points import get_random_target

app = Flask(__name__)


class ChamberData:
    def __init__(self):
        with open('resources/descriptions.yml', 'r') as file:
            self.descriptions = yaml.safe_load(file)


class MonsterData:
    def __init__(self):
        with open('resources/enemies/monsters.yml', 'r') as file:
            self.data = yaml.safe_load(file)


class ChamberResponse:
    def __init__(self, filename, description, path):
        self.mode = 'standard'
        self.filename = filename
        self.description = description
        self.validated = True
        self.path = path

    def to_string(self):
        return "filename = " + self.filename + " description = " + self.description + " path = " + self.path


# curl http://localhost:9991/
@app.route('/', methods=['GET'])
def get_info():
    return 'dungeon service', 200


@app.route('/dungeon/random-hit', methods=['GET'])
def random_hit():
    point = get_random_target()
    
    return jsonify(
        filepath='resources/enemies/hit.png',
        point=point,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    

# curl http://localhost:9991/dungeon/monster/gremlin
@app.route('/dungeon/monster/<name>', methods=['GET'])
def get_monster(name):
    logging.info("Fetching info about monster ", name)
    data = MonsterData()

    entry = next((d for d in data.data if d['id'] == name), None)

    return jsonify(
        filename=entry['file'],
        hp=entry['hp'],
        attack=entry['attack'],
        defense=entry['defense'],
        magic=entry['magic'],
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ), 200


# curl http://localhost:9991/dungeon/chamber/1
@app.route('/dungeon/chamber/<int:index>', methods=['GET'])
def get_chamber(index):
    logging.info("Fetching info about chamber ", index)
    file_path = "resources/" + str(index) + "*" + ".PNG"
    matching_files = glob.glob(file_path)

    data = ChamberData()

    logging.info("Chamber Response:")

    if matching_files:
        entry = next((d for d in data.descriptions if d['id'] == index), None)
        response = ChamberResponse(matching_files[0], entry['description'], entry['file'])

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        logging.info(response.to_string())

        return jsonify(
            filename=response.filename,
            description=response.description,
            path=response.path,
            mode=response.mode,
            timestamp=timestamp,
            validated=response.validated
        ), 200
    else:
        info = "No matching files found"
        logging.info(info)
        return jsonify(message=info), 404


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info("starting DUNGEON service on 9991")
    app.run(port=9991)
