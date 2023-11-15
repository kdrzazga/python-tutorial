class Question:

    def __init__(self, a, b, c, d, correct_answer):
        self.A = a
        self.B = b
        self.C = c
        self.D = d
        self.correct_answer = correct_answer


class QuestionsFactory:

    def create_set(self):
        questions_set = []
        questions_set.append(Question('Street Fighter 2 (Amiga)', 'Superfrog', 'Electrician (Atari)', 'Final Fight', 'A'))
        questions_set.append(Question('Punisher (MAME)', 'Fire And Ice', 'Commando', 'Civilization', 'A'))
        questions_set.append(Question('Franko', 'Golden Axe', "Flashback", 'Bloodwych', 'A'))
        questions_set.append(Question('Galaga Deluxe', 'Beavers (Amiga)', "Blinky's Scary School", 'Bloodwych', 'A'))
        questions_set.append(Question('Franko', 'Escape from Colditz', "Blinky's Scary School", 'Fort Apache', 'A'))
        questions_set.append(Question('Elvira II: The Jaws of Cerberus', 'Hardball! (Amiga)', "Ghosts'n'Goblins", 'Gods', 'A'))

        return questions_set
