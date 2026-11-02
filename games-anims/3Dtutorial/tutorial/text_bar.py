import pygame

from tutorial.overlay import Texture


class TextBar:
    def __init__(self, left, top, width, height, font_size):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("consolas", font_size)
        self.background_color = (0.0, 0.0, 0.0, 0.55)
        self.text_color = (235, 236, 245)
        self.padding = 16
        self.fade_duration = 0.4
        self.text = None
        self.texture = None
        self.age = 0.0

    def show(self, text):
        if text == self.text:
            return
        self.text = text
        self.age = 0.0
        if self.texture is not None:
            self.texture.release()
        self.texture = Texture(self.font.render(text, True, self.text_color))

    def update(self, seconds):
        self.age += seconds

    def draw(self, overlay):
        overlay.fill_rect(self.background_color, self.left, self.top, self.width, self.height)
        if self.texture is None:
            return
        alpha = min(self.age / self.fade_duration, 1.0)
        text_top = self.top + (self.height - self.texture.height) // 2
        overlay.draw_texture(self.texture, self.left + self.padding, text_top, alpha)
