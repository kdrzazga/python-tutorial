from flask import Flask

SERVICE_NAME = 'COUNTRY'

app = Flask(__name__)


@app.route('/', methods=['GET'])
def say_hello():
    print("Hello from service " + SERVICE_NAME)
    return 'I am microservice %s' % SERVICE_NAME


@app.route('/{name}', methods=['GET'])
def get_country_info(name: str):
    print("Info about country " + name)
    return 'Country name: %s' % name


if __name__ == '__main__':
    app.run(port=5981)
