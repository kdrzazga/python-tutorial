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

from .globals import ATARI_LOGO_PATH
from .logo_slab import LogoSlab, load_rgba

SWAY_ANGLE = 28.0    # degrees the logo turns to each side
SWAY_SPEED = 0.8     # radians per second through the sway cycle
TILT_SHARE = 0.35    # nodding amount relative to the side-to-side sway
LOGO_Z = -8.0        # depth in front of the camera


class AtariLogo:
    """Atari logo slab swaying in 3D."""

    def __init__(self, height=3.0):
        self.slab = LogoSlab(load_rgba(ATARI_LOGO_PATH), height)
        self.phase = 0.0

    def update(self, dt):
        self.phase += SWAY_SPEED * dt

    def render(self):
        yaw = SWAY_ANGLE * math.sin(self.phase)
        pitch = SWAY_ANGLE * TILT_SHARE * math.sin(self.phase * 0.7)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(1.0, 1.0, 1.0, 1.0)      # keep the texture untinted

        glPushMatrix()
        glLoadIdentity()          # stand in front of the camera, not the moved scene
        glTranslatef(0.0, 0.0, LOGO_Z)
        glRotatef(pitch, 1.0, 0.0, 0.0)
        glRotatef(yaw, 0.0, 1.0, 0.0)
        self.slab.draw()
        glPopMatrix()

        glDisable(GL_BLEND)
