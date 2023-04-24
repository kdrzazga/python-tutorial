from flask import Flask

SERVICE_NAME = 'ACCOUNT'
app = Flask(__name__)


@app.route('/', methods=['GET'])
def say_hello():
    print("Hello from service " + SERVICE_NAME)
    return 'I am microservice %s' % SERVICE_NAME


if __name__ == '__main__':
    app.run(port=5957)
