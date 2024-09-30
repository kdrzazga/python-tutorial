import random
import base64


class Data:
    empty = {
        "normal": "",
        "adult": "",
        "size": 12
    }

    honda_insult = {
        "normal": "  Honda! You fat loser !",
        "adult": base64.b64decode("SG9uZGEhIFR5IGt1cndvIGplYmFuYSAh").decode('utf-8'),
        "size": 17
    }

    general_insult = {
        "normal": "   P U S S I E S !!!",
        "adult": base64.b64decode("ICAgUCBJIFogRCBFIEMgWiBLIEkgISEh").decode('utf-8'),
        "size": 20
    }

    best_mage = {
        "normal": "     I am the best !",
        "adult": base64.b64decode("ICAgU2t1cndpYcWCeSBzcGHFm2xhayAh").decode('utf-8'),
        "size": 19
    }

    damn_it = {
        "normal": "        DAMN IT !",
        "adult": base64.b64decode("ICAgICAgSkEgUElFUkRPTMSYICE=").decode('utf-8'),
        "size": 18
    }

    fight_call = {
        "normal": "     Begin fight !",
        "adult": base64.b64decode("TkFLVVJXSUFKQ0lFICE=").decode('utf-8'),
        "size": 22
    }

    fight_over = {
        "normal": "     K.O. !",
        "adult": "      Nokaut !!!",
        "size": 22
    }

    reward = {
        "normal": "Reward - miss Barbara",
        "adult": "Nagroda - lejdi Barbara",
        "size": 12
    }

    @staticmethod
    def get_random() -> dict:
        shout = [Data.general_insult, Data.best_mage, Data.damn_it]
        return random.choice(shout)
