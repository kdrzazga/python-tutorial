class Question:

    text = "Z jakiej gry pochodzi ten element ?"

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
        questions_set.append(Question('a) Punisher (MAME)', 'b) Fire And Ice', 'c) Budokan', 'd) Mortal Kombat', 'D', r + 'mkbgnd.PNG', r + 'mkbgnd_full.PNG', r + 'mk.mp4'))
        questions_set.append(Question('a) Street Fighter 2 (Amiga)', 'b) Superfrog', 'c) Cadillacs & Dinosaurs', 'd) Final Fight', 'C', r + 'bgnd.PNG', r + 'bgnd_full.PNG', r + 'kadilaki.mpg'))
        questions_set.append(Question('a) Franko', 'b) Miecze Valdgira', "c) Teenagent", 'd) Fort Apache', 'A', r + 'fbgnd.PNG', r + 'fbgnd_full.PNG', r + 'franko_intro.mp4'))
        questions_set.append(Question('a) Warriors of Fate', 'b) Punisher', "c) Flashback", 'd) Bloodwych', 'B', r + 'pnshbgnd_full.PNG', r + 'pnshbgnd_full.PNG', r + 'punisher.mp4'))
        questions_set.append(
            Question('a) Warriors of Fate', 'b) Punisher', "c) Flashback", 'd) Bloodwych', 'B', r + 'pnshbgnd_full.PNG',
                     r + 'pnshbgnd_full.PNG', r + 'punisher.mp4'))

        questions_set.append(Question('a) Galaga Deluxe', 'b) Beavers (Amiga)', "c) Blinky's Scary School", 'd) Bloodwych', 'A', r + 'bgnd.PNG', r + 'bgnd_full.PNG', r + 'kadilaki.mpg'))
        questions_set.append(Question('a) Elvira II: The Jaws of Cerberus', 'b) Hardball! (Amiga)', "c) Ghosts'n'Goblins", 'd) Gods', 'A', r + 'fbgnd.PNG', r + 'fbgnd_full.PNG', r + 'franko_intro.mp4'))

        return questions_set
