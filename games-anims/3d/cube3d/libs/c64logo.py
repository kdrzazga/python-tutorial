import numpy as np
from OpenGL.GL import (
    GL_BLEND,
    GL_ONE_MINUS_SRC_ALPHA,
    GL_SRC_ALPHA,
    glBlendFunc,
    glColor4f,
    glDisable,
    glEnable,
    glLoadIdentity,
    glPopMatrix,
    glPushMatrix,
    glRotatef,
    glTranslatef,
)

from .globals import C64_LOGO_PATH
from .logo_slab import LogoSlab, load_rgba

LOGO_Z = -8.0        # depth in front of the camera
SOLO_DURATION = 5.0  # seconds the C spins on its own
SPIN_SPEED = 72.0    # deg/s: exactly one turn during SOLO_DURATION, so the
                     # flags join back in phase and the logo stays whole


class C64Logo:
    """Commodore logo split into its C and two flags; the C spins first and
    the flags join in later."""

    def __init__(self, height=3.0):
        letter, blue_flag, red_flag = self._split(load_rgba(C64_LOGO_PATH))
        self.letter = LogoSlab(letter, height)
        self.flags = [LogoSlab(blue_flag, height), LogoSlab(red_flag, height)]
        self.elapsed = 0.0

    def update(self, dt, t):
        self.elapsed += dt

    def render(self):
        letter_angle = SPIN_SPEED * self.elapsed
        flag_angle = SPIN_SPEED * max(0.0, self.elapsed - SOLO_DURATION)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(1.0, 1.0, 1.0, 1.0)      # keep the textures untinted

        self._draw_part(self.letter, letter_angle)
        for flag in self.flags:
            self._draw_part(flag, flag_angle)

        glDisable(GL_BLEND)

    def _draw_part(self, slab, angle):
        glPushMatrix()
        glLoadIdentity()          # stand in front of the camera, not the moved scene
        glTranslatef(0.0, 0.0, LOGO_Z)
        glRotatef(angle, 0.0, 1.0, 0.0)
        slab.draw()
        glPopMatrix()

    def _split(self, rgba):
        """C letter, blue flag and red flag as separate full-size images, so
        they stay aligned when drawn on top of each other."""
        visible = rgba[:, :, 3] > 0
        red = visible & (rgba[:, :, 0] > 128)
        blue = visible & (rgba[:, :, 2] > 128)

        # the flags sit to the right of the C; the red one marks where they start
        flags_start_x = np.nonzero(red.any(axis=0))[0].min()
        columns = np.arange(rgba.shape[1])[None, :]

        return (self._masked(rgba, blue & (columns < flags_start_x)),
                self._masked(rgba, blue & (columns >= flags_start_x)),
                self._masked(rgba, red))

    def _masked(self, rgba, mask):
        part = rgba.copy()
        part[~mask, 3] = 0
        return part
