import logging

from flask import Flask

app = Flask(__name__)

# curl http://localhost:9992/
@app.route('/', methods=['GET'])
def get_info():
    return 'py-city2', 200


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info("starting service on 9992")
    app.run(port=9992)
