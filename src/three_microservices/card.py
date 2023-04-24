import yaml
from flask import Flask, jsonify, json

SERVICE_NAME = 'CARD'

app = Flask(__name__)


@app.route('/', methods=['GET'])
def say_hello():
    print("Hello from service " + SERVICE_NAME)
    return 'Microservice %s' % SERVICE_NAME


@app.route('/<card_type>/<card_id>', methods=['GET'])
def read_card(card_type: str, card_id: int):
    print("Request for " + card_type + " [" + str(card_id) + "]")

    with open('cards.yml', 'r') as file:
        cards = yaml.safe_load(file)

    debit_cards = cards['debit-card']
    credit_cards = cards['credit-card']

    if card_type == 'credit':
        print("Country data:\n%s", json.dumps(credit_cards, indent=2))
        return jsonify(_get_card_by_id(credit_cards, card_id))
    else:
        print("Country data:\n%s", json.dumps(debit_cards, indent=2))
        return jsonify(_get_card_by_id(debit_cards, card_id))


def _get_card_by_id(cards, card_id: int):
    for card in cards:
        if str(card['id']) == card_id:
            return card
    return None


if __name__ == '__main__':
    app.run(port=5955)
