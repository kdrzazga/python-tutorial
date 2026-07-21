import math

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

from .globals import ZX_LOGO_PATH
from .logo_slab import LogoSlab, load_rgba

START_Z = -100.0     # far away, where the zoom begins
END_Z = -10.0        # closest the logo comes
ZOOM_SPEED = 25.0    # units per second
ZOOM_DURATION = (END_Z - START_Z) / ZOOM_SPEED
ROTATIONS = 3        # full turns spread across the zoom
PULSE_DEPTH = 0.6    # how far the pulse drifts in and out
PULSE_SPEED = 2.0    # radians per second
FLIP_START = 10.0    # seconds after initial_t when the closing turn begins
FLIP_DURATION = 5.0  # one full turn about the vertical axis, showing the slab edges


class ZxLogo:
    """ZX Spectrum logo slab: spins while zooming in, then pulses in place."""

    def __init__(self, initial_t, height=2.5):
        self.slab = LogoSlab(load_rgba(ZX_LOGO_PATH), height)
        self.initial_t = initial_t
        self.z = START_Z
        self.angle = 0.0
        self.pulse = 0.0
        self.flip = 0.0

    def update(self, dt, t):
        elapsed = t - self.initial_t

        if self.z < END_Z:
            self.z = min(self.z + ZOOM_SPEED * dt, END_Z)
            self.angle = ROTATIONS * 360.0 * self._zoom_progress()
        else:
            self.pulse = PULSE_DEPTH * math.sin(max(0.0, elapsed - ZOOM_DURATION) * PULSE_SPEED)

        if elapsed > FLIP_START:
            self.flip = min(360.0, (elapsed - FLIP_START) / FLIP_DURATION * 360.0)

    def _zoom_progress(self):
        return (self.z - START_Z) / (END_Z - START_Z)

    def render(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(1.0, 1.0, 1.0, 1.0)      # keep the texture untinted

        glPushMatrix()
        glLoadIdentity()          # stand in front of the camera, not the moved scene
        glTranslatef(0.0, 0.0, self.z + self.pulse)
        glRotatef(self.flip, 0.0, 1.0, 0.0)
        glRotatef(self.angle, 0.0, 0.0, 1.0)
        self.slab.draw()
        glPopMatrix()

        glDisable(GL_BLEND)
