import math

from OpenGL.GL import *
from OpenGL.GLU import *


class Camera:
    def __init__(self, target, orbit_radius, orbit_height, orbit_speed_degrees, bob_amplitude, bob_speed):
        self.target = target
        self.orbit_radius = orbit_radius
        self.orbit_height = orbit_height
        self.orbit_speed_degrees = orbit_speed_degrees
        self.bob_amplitude = bob_amplitude
        self.bob_speed = bob_speed

    def apply(self, elapsed_seconds):
        orbit_angle = math.radians(self.orbit_speed_degrees * elapsed_seconds)
        eye_x = self.target[0] + self.orbit_radius * math.cos(orbit_angle)
        eye_z = self.target[2] + self.orbit_radius * math.sin(orbit_angle)
        eye_y = self.orbit_height + self.bob_amplitude * math.sin(self.bob_speed * elapsed_seconds)
        glLoadIdentity()
        gluLookAt(eye_x, eye_y, eye_z,
                  self.target[0], self.target[1], self.target[2],
                  0.0, 1.0, 0.0)

    def billboard_axes(self):
        modelview = glGetFloatv(GL_MODELVIEW_MATRIX)
        right = (modelview[0][0], modelview[1][0], modelview[2][0])
        up = (modelview[0][1], modelview[1][1], modelview[2][1])
        return right, up
