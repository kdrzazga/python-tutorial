import math

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

INITIAL_LOGO_Z = -8.0        # depth in front of the camera
APPROACH = 5.0       # seconds the flags take to reach the C
SPIN_SPEED = 72.0    # deg/s: exactly one turn during APPROACH, so the C is
                     # showing its front again the moment the flags arrive
FLAG_STARTS = ((-7.0, 4.5), (7.0, 4.5))   # off-screen top-left and top-right
SWAY_ANGLE = 18.0    # degrees of roll while drifting in
SWAY_SPEED = 3.0     # radians per second of the sway


class C64Logo:
    """Commodore logo split into its C and two flags. The C spins alone while
    the flags sway in from the top corners, arriving as the C faces front."""

    def __init__(self, height=3.0):
        letter, blue_flag, red_flag = self._split(load_rgba(C64_LOGO_PATH))
        self.letter = LogoSlab(letter, height)
        self.flags = list(zip((LogoSlab(blue_flag, height), LogoSlab(red_flag, height)),
                              FLAG_STARTS))
        self.elapsed = 0.0
        self.z = INITIAL_LOGO_Z

    def update(self, dt, t):
        self.elapsed += dt
        if t > 180:
            self.z -= 0.3

    def render(self):
        spin = SPIN_SPEED * self.elapsed
        progress = min(1.0, self.elapsed / APPROACH)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(1.0, 1.0, 1.0, 1.0)      # keep the textures untinted

        self._draw_part(self.letter, (0.0, 0.0), spin)
        for slab, start in self.flags:
            self._draw_part(slab, *self._flag_pose(start, progress, spin))

        glDisable(GL_BLEND)

    def _flag_pose(self, start, progress, spin):
        """Offset, spin and sway for a flag at the given approach progress.
        Once joined it simply shares the C's spin."""
        if progress >= 1.0:
            return (0.0, 0.0), spin, 0.0

        eased = progress * progress * (3.0 - 2.0 * progress)
        offset = (start[0] * (1.0 - eased), start[1] * (1.0 - eased))
        sway = SWAY_ANGLE * math.sin(self.elapsed * SWAY_SPEED) * (1.0 - progress)
        return offset, 0.0, sway

    def _draw_part(self, slab, offset, spin, sway=0.0):
        glPushMatrix()
        glLoadIdentity()          # stand in front of the camera, not the moved scene
        glTranslatef(offset[0], offset[1], self.z)
        glRotatef(spin, 0.0, 1.0, 0.0)
        glRotatef(sway, 0.0, 0.0, 1.0)
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
