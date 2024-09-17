import random


class Data:
    empty = {
        "normal": "",
        "adult": ""
    }

    honda_insult = {
        "normal": "Honda! You loser !",
        "adult": "Honda! Ty kurwo jebana !"
    }

    general_insult = {
        "normal": "   P U S S I E S !!!",
        "adult": "  P I Z D E C Z K I !!!"
    }

    best_mage = {
        "normal": "     I am the best !",
        "adult": "    Ja jestem najlepszy !"
    }

    damn_it = {
        "normal": "      Damn it !",
        "adult": "      JA PIERDOLE !"
    }

    fight_call = {
        "normal": "     Begin fight !",
        "adult": "    NAKURWIAJCIE !"
    }

    @staticmethod
    def get_random():
        shout = [Data.general_insult, Data.best_mage, Data.damn_it]
        return random.choice(shout)
