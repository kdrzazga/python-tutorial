import pygame
from OpenGL.GL import (
    GL_BLEND,
    GL_DEPTH_TEST,
    GL_LINEAR,
    GL_MODELVIEW,
    GL_ONE_MINUS_SRC_ALPHA,
    GL_PROJECTION,
    GL_QUADS,
    GL_RGBA,
    GL_SRC_ALPHA,
    GL_TEXTURE_2D,
    GL_TEXTURE_MAG_FILTER,
    GL_TEXTURE_MIN_FILTER,
    GL_UNSIGNED_BYTE,
    glBegin,
    glBindTexture,
    glBlendFunc,
    glDisable,
    glEnable,
    glEnd,
    glGenTextures,
    glLoadIdentity,
    glMatrixMode,
    glOrtho,
    glPopMatrix,
    glPushMatrix,
    glTexCoord2f,
    glTexImage2D,
    glTexParameteri,
    glTexSubImage2D,
    glVertex2f,
)

from .font_utils import fit_sysfont_size
from .globals import CREDITS_LINES, INFO_LINES1, INFO_LINES2

FONT_NAME = "couriernew,consolas,monospace"
TEXT_COLOR = (200, 200, 200)
SHOUT_HEIGHT = 0.04     # shout font height, as a share of the window height


class TextOverlay:
    def __init__(self, window_size):
        self.window_size = window_size

        max_width = int(window_size[0] * 0.8)
        size1 = fit_sysfont_size(FONT_NAME, INFO_LINES1, max_width, start_size=window_size[0] // 6)
        self.font1 = pygame.font.SysFont(FONT_NAME, size1, bold=True)

        size2 = fit_sysfont_size(FONT_NAME, INFO_LINES2, max_width, start_size=window_size[0] // 6)
        self.font2 = pygame.font.SysFont(FONT_NAME, size2, bold=True)

        credits_width = int(window_size[0] * 0.25)
        size3 = fit_sysfont_size(FONT_NAME, CREDITS_LINES, credits_width,
                                 start_size=window_size[0] // 20)
        self.credits_font = pygame.font.SysFont(FONT_NAME, size3, bold=False)

        shout_size = max(8, int(window_size[1] * SHOUT_HEIGHT))
        self.shout_font = pygame.font.SysFont(FONT_NAME, shout_size, bold=True)

        self.tex_id = self._create_texture()

    def _create_texture(self):
        w, h = self.window_size
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
        return tex_id

    def draw(self, t):
        lines, font = self._lines_for(t)
        if lines is None:
            return

        surf = self._render_surface(lines, font)
        self._upload(surf)
        self._draw_quad()

    def draw_credits(self):
        self._upload(self._render_corner_surface(CREDITS_LINES, self.credits_font))
        self._draw_quad()

    def draw_shout(self, text, color, spot):
        """A short caption thrown on screen at `spot`, given in 0..1 of the window."""
        width, height = self.window_size
        surf = pygame.Surface((width, height), pygame.SRCALPHA)

        rendered = self.shout_font.render(text, True, color)
        surf.blit(rendered, (int(spot[0] * width) - rendered.get_width() // 2,
                             int(spot[1] * height) - rendered.get_height() // 2))

        self._upload(surf)
        self._draw_quad()

    def _render_corner_surface(self, lines, font):
        w, h = self.window_size
        surf = pygame.Surface((w, h), pygame.SRCALPHA)

        margin = int(w * 0.07)
        line_height = font.get_linesize()
        for i, line in enumerate(lines):
            line_surf = font.render(line, True, TEXT_COLOR)
            surf.blit(line_surf, (w - margin - line_surf.get_width(), margin + i * line_height))

        return surf

    def _lines_for(self, t):
        if 10 <= t < 25:
            return INFO_LINES1, self.font1
        if 30 <= t < 45:
            return INFO_LINES2, self.font2
        return None, None

    def _render_surface(self, lines, font):
        w, h = self.window_size
        surf = pygame.Surface((w, h), pygame.SRCALPHA)

        line_height = font.get_linesize()
        total_height = len(lines) * line_height
        start_y = h // 2 - total_height // 2

        for i, line in enumerate(lines):
            line_surf = font.render(line, True, TEXT_COLOR)
            x = w // 2 - line_surf.get_width() // 2
            y = start_y + i * line_height
            surf.blit(line_surf, (x, y))

        return surf

    def _upload(self, surf):
        w, h = self.window_size
        data = pygame.image.tostring(surf, "RGBA", True)
        glBindTexture(GL_TEXTURE_2D, self.tex_id)
        glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, w, h, GL_RGBA, GL_UNSIGNED_BYTE, data)

    def _draw_quad(self):
        w, h = self.window_size

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, w, h, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glBindTexture(GL_TEXTURE_2D, self.tex_id)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 1)
        glVertex2f(0, 0)
        glTexCoord2f(1, 1)
        glVertex2f(w, 0)
        glTexCoord2f(1, 0)
        glVertex2f(w, h)
        glTexCoord2f(0, 0)
        glVertex2f(0, h)
        glEnd()

        glDisable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)

        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
