class LevelManager:
    level_filepath = "resources/level.txt"

    def __init__(self):
        with open(LevelManager.level_filepath, 'r') as file:
            self.content = file.read()
            print(self.content)
