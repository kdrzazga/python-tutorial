from pathlib import Path

import pygame
from OpenGL.GL import *

from tutorial_window import Scene, TutorialWindow


class Picture:
    def __init__(self, file_path):
        image = pygame.image.load(str(file_path)).convert_alpha()
        self.width, self.height = image.get_size()
        pixels = pygame.image.tobytes(image, "RGBA", True)
        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexParameteri(GL_TEXTURE_2D,
                        GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D,
                        GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,
                     self.width, self.height, 0,
                     GL_RGBA, GL_UNSIGNED_BYTE, pixels)

    def bind(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

    def unbind(self):
        glDisable(GL_TEXTURE_2D)


class FlatPicture:
    def __init__(self, picture, width):
        self.picture = picture
        self.width = width
        self.height = width * picture.height / picture.width
        self.opacity = 1.0

    def corners(self):
        right = self.width / 2.0
        top = self.height / 2.0
        return ((0.0, 0.0, -right, -top, 0.0),
                (1.0, 0.0, right, -top, 0.0),
                (1.0, 1.0, right, top, 0.0),
                (0.0, 1.0, -right, top, 0.0))

    def draw(self):
        self.picture.bind()
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(1.0, 1.0, 1.0, self.opacity)
        glBegin(GL_QUADS)
        for u, v, x, y, z in self.corners():
            glTexCoord2f(u, v)
            glVertex3f(x, y, z)
        glEnd()
        glDisable(GL_BLEND)
        self.picture.unbind()


class FlatPictureScene(Scene):
    def __init__(self):
        picture_path = Path(__file__).with_name("KnAshort.png")
        self.picture = Picture(picture_path)
        self.flat_picture = FlatPicture(self.picture, 3.2)

    def draw(self):
        self.flat_picture.draw()


if __name__ == "__main__":
    TutorialWindow("Lesson 6 - a picture").run(FlatPictureScene())
