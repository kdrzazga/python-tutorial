import random

from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_TEST,
    GL_LINEAR,
    GL_MODELVIEW,
    GL_PROJECTION,
    GL_QUADS,
    GL_RGB,
    GL_TEXTURE_2D,
    GL_TEXTURE_MAG_FILTER,
    GL_TEXTURE_MIN_FILTER,
    GL_UNSIGNED_BYTE,
    glBegin,
    glBindTexture,
    glClear,
    glColor4f,
    glCopyTexSubImage2D,
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

BANDS = 64           # horizontal strips the frame is split into
JITTER = 0.03        # sideways slip of a disturbed band, as a share of the width


class GlitchOverlay:
    """Breaks the finished frame into horizontal bands, dropping and slipping
    some of them so the whole scene looks like a failing signal."""

    def __init__(self, window_size):
        self.window_size = window_size
        self.texture_id = self._create_texture()

    def apply(self, interference):
        width, height = self.window_size

        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glCopyTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, 0, 0, width, height)
        glClear(GL_COLOR_BUFFER_BIT)      # dropped bands fall back to the background
        self._draw_bands(interference)

    def _create_texture(self):
        width, height = self.window_size
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0,
                     GL_RGB, GL_UNSIGNED_BYTE, None)
        return texture_id

    def _draw_bands(self, interference):
        width, height = self.window_size

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, width, height, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        glColor4f(1.0, 1.0, 1.0, 1.0)

        glBegin(GL_QUADS)
        for band in range(BANDS):
            if random.random() < interference:
                continue                  # this band never arrives

            top_y, bottom_y = height * band / BANDS, height * (band + 1) / BANDS
            # the framebuffer copy has its origin bottom-left, so v runs backwards
            top_v, bottom_v = 1.0 - band / BANDS, 1.0 - (band + 1) / BANDS
            slip = width * JITTER * random.uniform(-1.0, 1.0)

            glTexCoord2f(0.0, top_v); glVertex2f(slip, top_y)
            glTexCoord2f(1.0, top_v); glVertex2f(width + slip, top_y)
            glTexCoord2f(1.0, bottom_v); glVertex2f(width + slip, bottom_y)
            glTexCoord2f(0.0, bottom_v); glVertex2f(slip, bottom_y)
        glEnd()

        glEnable(GL_DEPTH_TEST)

        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
