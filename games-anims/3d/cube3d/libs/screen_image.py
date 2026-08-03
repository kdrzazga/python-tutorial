import random

import numpy as np
from OpenGL.GL import (
    GL_DEPTH_TEST,
    GL_LINEAR,
    GL_MODELVIEW,
    GL_PROJECTION,
    GL_QUADS,
    GL_RGBA,
    GL_TEXTURE_2D,
    GL_TEXTURE_MAG_FILTER,
    GL_TEXTURE_MIN_FILTER,
    GL_UNSIGNED_BYTE,
    glBegin,
    glBindTexture,
    glColor4f,
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
    glVertex2f,
)

from .logo_slab import load_rgba

BANDS = 64           # horizontal strips the picture is split into
JITTER = 0.04        # sideways slip of a disturbed band, as a share of its width


class ScreenImage:
    """A picture drawn over the whole window, scaled to fit without stretching.
    Bands of it can be dropped to fake a broken signal."""

    def __init__(self, image_path):
        self.rgba = load_rgba(image_path)
        self.texture_id = None

    def draw(self, window_size, interference=0.0):
        if self.texture_id is None:
            self.texture_id = self._upload_texture()

        left, top, width, height = self._fitted_rect(window_size)
        window_w, window_h = window_size

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, window_w, window_h, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        glColor4f(1.0, 1.0, 1.0, 1.0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

        self._draw_bands(left, top, width, height, interference)

        glEnable(GL_DEPTH_TEST)

        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

    def _draw_bands(self, left, top, width, height, interference):
        """Draw the picture strip by strip; dropped strips leave the scene
        behind showing through, which reads as a broken signal."""
        glBegin(GL_QUADS)
        for band in range(BANDS):
            if random.random() < interference:
                continue                      # this scanline never arrives

            top_v, bottom_v = band / BANDS, (band + 1) / BANDS
            top_y, bottom_y = top + height * top_v, top + height * bottom_v
            slip = width * JITTER * random.uniform(-1.0, 1.0) if interference else 0.0

            glTexCoord2f(0.0, top_v); glVertex2f(left + slip, top_y)
            glTexCoord2f(1.0, top_v); glVertex2f(left + width + slip, top_y)
            glTexCoord2f(1.0, bottom_v); glVertex2f(left + width + slip, bottom_y)
            glTexCoord2f(0.0, bottom_v); glVertex2f(left + slip, bottom_y)
        glEnd()

    def _fitted_rect(self, window_size):
        """Largest centred rectangle keeping the picture's aspect ratio."""
        image_h, image_w = self.rgba.shape[:2]
        window_w, window_h = window_size

        scale = min(window_w / image_w, window_h / image_h)
        width, height = image_w * scale, image_h * scale
        return (window_w - width) / 2.0, (window_h - height) / 2.0, width, height

    def _upload_texture(self):
        height, width = self.rgba.shape[:2]
        data = np.ascontiguousarray(self.rgba).tobytes()   # row 0 maps to v = 0

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0,
                     GL_RGBA, GL_UNSIGNED_BYTE, data)
        return texture_id
