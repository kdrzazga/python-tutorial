class Question:

    def __init__(self, a, b, c, d, correct_answer, bg_path, full_bg_path, video_path):
        self.A = a
        self.B = b
        self.C = c
        self.D = d
        self.correct_answer = correct_answer
        self.bg_path = bg_path
        self.full_bg_path = full_bg_path
        self.video_path = video_path


class QuestionsFactory:

    def create_set(self):
        r = 'resources/'
        questions_set = []
        questions_set.append(Question('Street Fighter 2 (Amiga)', 'Superfrog', 'Cadillacs & Dinosaurs', 'Final Fight', 'C', r + 'bgnd.PNG', r + 'bgnd_full.PNG', r + 'kadilaki.mpg'))
        questions_set.append(Question('Franko', 'Miecze Valdgira', "Teenagent", 'Fort Apache', 'A', r + 'fbgnd.PNG', r + 'fbgnd_full.PNG', r + 'franko_intro.mp4'))
        questions_set.append(Question('Punisher (MAME)', 'Fire And Ice', 'Commando', 'Civilization', 'A', r + 'bgnd.PNG', r + 'bgnd_full.PNG', r + 'kadilaki.mpg'))
        questions_set.append(Question('Franko', 'Golden Axe', "Flashback", 'Bloodwych', 'A', r + 'bgnd.PNG', r + 'bgnd_full.PNG', r + 'kadilaki.mpg'))
        questions_set.append(Question('Galaga Deluxe', 'Beavers (Amiga)', "Blinky's Scary School", 'Bloodwych', 'A', r + 'bgnd.PNG', r + 'bgnd_full.PNG', r + 'kadilaki.mpg'))
        questions_set.append(Question('Elvira II: The Jaws of Cerberus', 'Hardball! (Amiga)', "Ghosts'n'Goblins", 'Gods', 'A', r + 'bgnd.PNG', r + 'bgnd_full.PNG', r + 'kadilaki.mpg'))

        return questions_set
