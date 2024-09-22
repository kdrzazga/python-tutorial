import random
import base64


class Data:
    empty = {
        "normal": "",
        "adult": ""
    }

    honda_insult = {
        "normal": "Honda! You fat loser !",
        "adult": base64.b64decode("SG9uZGEhIFR5IGt1cndvIGplYmFuYSAh").decode('utf-8')
    }

    general_insult = {
        "normal": "   P U S S I E S !!!",
        "adult": base64.b64decode("ICAgUCBJIFogRCBFIEMgWiBLIEkgISEh").decode('utf-8')
    }

    best_mage = {
        "normal": "     I am the best !",
        "adult": base64.b64decode("ICAgU2t1cndpYcWCeSBzcGHFm2xhayAh").decode('utf-8')
    }

    damn_it = {
        "normal": "      Damn it !",
        "adult": base64.b64decode("ICAgICAgSkEgUElFUkRPTMSYICE=").decode('utf-8')
    }

    fight_call = {
        "normal": "     Begin fight !",
        "adult": base64.b64decode("TkFLVVJXSUFKQ0lFLCBDSVVMRSAh").decode('utf-8')
    }

    fight_over = {
        "normal": "     The fight is over !",
        "adult": "      Nokaut !!!"
    }

    reward = {
        "normal": "Reward - miss Barbara",
        "adult": "Nagroda - lejdi Barbara"
    }

    @staticmethod
    def get_random():
        shout = [Data.general_insult, Data.best_mage, Data.damn_it]
        return random.choice(shout)
