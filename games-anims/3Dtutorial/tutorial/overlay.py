import pygame
from OpenGL.GL import *


class Texture:
    def __init__(self, surface):
        self.width, self.height = surface.get_size()
        pixels = pygame.image.tobytes(surface, "RGBA", False)
        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0,
                     GL_RGBA, GL_UNSIGNED_BYTE, pixels)

    def release(self):
        glDeleteTextures([self.texture_id])


class Overlay:
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height

    def begin(self):
        glViewport(0, 0, self.window_width, self.window_height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.window_width, self.window_height, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def clip(self, left, top, width, height):
        glEnable(GL_SCISSOR_TEST)
        glScissor(left, self.window_height - (top + height), width, height)

    def unclip(self):
        glDisable(GL_SCISSOR_TEST)

    def fill_rect(self, color, left, top, width, height):
        glDisable(GL_TEXTURE_2D)
        glColor4f(*color)
        glBegin(GL_QUADS)
        glVertex2f(left, top)
        glVertex2f(left + width, top)
        glVertex2f(left + width, top + height)
        glVertex2f(left, top + height)
        glEnd()

    def draw_texture(self, texture, left, top, alpha=1.0):
        right = left + texture.width
        bottom = top + texture.height
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture.texture_id)
        glColor4f(1.0, 1.0, 1.0, alpha)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(left, top)
        glTexCoord2f(1.0, 0.0)
        glVertex2f(right, top)
        glTexCoord2f(1.0, 1.0)
        glVertex2f(right, bottom)
        glTexCoord2f(0.0, 1.0)
        glVertex2f(left, bottom)
        glEnd()
        glDisable(GL_TEXTURE_2D)
