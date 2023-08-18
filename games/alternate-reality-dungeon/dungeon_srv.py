import os
import glob
import yaml
import logging
from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)


class Data:    
    def __init__(self):
        with open('resources/descriptions.yml', 'r') as file:
            self.descriptions = yaml.safe_load(file)


class Response:    
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


# curl http://localhost:9991/dungeon/chamber/1
@app.route('/dungeon/chamber/<int:index>', methods=['GET'])
def get_chamber(index):
    logging.info("Fetching info about chamber ", index)
    file_path = "resources/" + str(index) + "*" + ".PNG"
    matching_files = glob.glob(file_path)

    data = Data()

    logging.info("Response:")

    if matching_files:
        entry = next((d for d in data.descriptions if d['id'] == index), None)
        response = Response(matching_files[0], entry['description'], entry['file'])
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        logging.info(response.to_string())
        
        return jsonify(
            filename=response.filename,
            description=response.description,
            path=response.path,
            mode=response.mode,
            timestamp = timestamp,
            validated= response.validated
        ), 200
    else:
        info="No matching files found"
        logging.info(info)
        return jsonify(message=info), 404


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info("starting DUNGEON service on 9991")
    app.run(port=9991)
