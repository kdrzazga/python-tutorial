from OpenGL.GL import *

from lesson5_ball import Ball
from lesson6_picture import FlatPictureScene
from tutorial_window import Scene, TutorialWindow


class TexturedBall(Ball):
    def __init__(self, radius, picture):
        super().__init__(radius, (1.0, 1.0, 1.0))
        self.picture = picture

    def emit_vertex(self, slice_index, stack_index):
        glTexCoord2f(slice_index / self.slices,
                     stack_index / self.stacks)
        super().emit_vertex(slice_index, stack_index)

    def draw(self):
        self.picture.bind()
        super().draw()
        self.picture.unbind()


class TexturedBallScene(Scene):
    def __init__(self):
        picture = FlatPictureScene().picture
        self.ball = TexturedBall(1.1, picture)

    def draw(self):
        self.ball.draw()


if __name__ == "__main__":
    window = TutorialWindow("Lesson 7 - picture on a ball")
    window.run(TexturedBallScene())
