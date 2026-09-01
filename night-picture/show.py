from app import App


class SceneShow:
    def __init__(self, scenes, seconds_per_scene=4.0):
        self.scenes = tuple(scenes)
        self.seconds_per_scene = seconds_per_scene
        self.width = self.scenes[0].width
        self.height = self.scenes[0].height

    def current_index(self, time):
        return int(time / self.seconds_per_scene) % len(self.scenes)

    def render(self, painter, time):
        self.scenes[self.current_index(time)].render(painter, time)

    def run(self, title="Night Picture"):
        App(self, title).run()
