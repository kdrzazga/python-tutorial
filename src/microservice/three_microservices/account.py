from flask import Flask
from loguru import logger


SERVICE_NAME = 'ACCOUNT'
app = Flask(__name__)


@app.route('/', methods=['GET'])
def say_hello():
    logger.info("Hello from service " + SERVICE_NAME)
    return 'Microservice %s' % SERVICE_NAME


if __name__ == '__main__':
    app.run(port=5957)
