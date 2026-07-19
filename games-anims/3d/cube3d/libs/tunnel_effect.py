import math
import random

from OpenGL.GL import (
    GL_POINTS,
    GL_TEXTURE_2D,
    glBegin,
    glColor3f,
    glDisable,
    glEnable,
    glEnd,
    glLoadIdentity,
    glPointSize,
    glPopMatrix,
    glPushMatrix,
    glVertex3f,
)

STAR_COUNT = 300
NEAR_Z = -3.0        # spawn depth, where stars sit at the screen edges
FAR_Z = -45.0        # depth at which a star is recycled
SPEED = 12.0         # world units per second travelling away from the camera
MIN_RADIUS = 1.6     # keeps new stars out at the edges rather than the centre
MAX_RADIUS = 6.0
POINT_SIZE = 3.0
MIN_BRIGHTNESS = 0.2


class TunnelEffect:

    def __init__(self, count=STAR_COUNT):
        self.stars = [self._spawn(random.uniform(FAR_Z, NEAR_Z)) for _ in range(count)]

    def render(self, dt):
        self._advance(dt)
        self._draw()

    def _spawn(self, z=NEAR_Z):
        angle = random.uniform(0.0, 2.0 * math.pi)
        radius = random.uniform(MIN_RADIUS, MAX_RADIUS)
        return [math.cos(angle) * radius, math.sin(angle) * radius, z]

    def _advance(self, dt):
        for star in self.stars:
            star[2] -= SPEED * dt
            if star[2] < FAR_Z:
                star[:] = self._spawn()

    def _draw(self):
        glDisable(GL_TEXTURE_2D)
        glPushMatrix()
        glLoadIdentity()
        glPointSize(POINT_SIZE)

        glBegin(GL_POINTS)
        for x, y, z in self.stars:
            glColor3f(*self._brightness(z))
            glVertex3f(x, y, z)
        glEnd()

        glPopMatrix()
        glEnable(GL_TEXTURE_2D)

    def _brightness(self, z):
        nearness = (z - FAR_Z) / (NEAR_Z - FAR_Z)
        shade = MIN_BRIGHTNESS + (1.0 - MIN_BRIGHTNESS) * max(0.0, min(1.0, nearness))
        return shade, shade, shade
