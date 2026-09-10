import math
import random

from OpenGL.GL import *

from fog_particle import FogParticle


class Fog:
    def __init__(self, shade, particle_count, volume_radius, volume_bottom, volume_top, start_distance, end_distance):
        self.shade = shade
        self.color = shade if shade is not None else (1.0, 1.0, 1.0)
        self.background_color = tuple(channel * 0.1 for channel in self.color)
        self.start_distance = start_distance
        self.end_distance = end_distance
        self.sprite_texture = None
        self.particles = self._build_particles(particle_count, volume_radius, volume_bottom, volume_top)

    def _build_particles(self, particle_count, volume_radius, volume_bottom, volume_top):
        particles = []
        for _ in range(particle_count):
            home_position = (random.uniform(-volume_radius, volume_radius),
                             random.uniform(volume_bottom, volume_top),
                             random.uniform(-volume_radius, volume_radius))
            base_size = random.uniform(0.8, 2.4)
            drift_amplitude = random.uniform(0.15, 0.5)
            drift_speed = random.uniform(0.3, 0.8)
            drift_phase = random.uniform(0.0, math.tau)
            pulse_speed = random.uniform(0.4, 1.1)
            pulse_phase = random.uniform(0.0, math.tau)
            particles.append(FogParticle(home_position, base_size, drift_amplitude, drift_speed, drift_phase, pulse_speed, pulse_phase))
        return particles

    def configure(self):
        glEnable(GL_FOG)
        glFogi(GL_FOG_MODE, GL_LINEAR)
        glFogfv(GL_FOG_COLOR, (self.background_color[0], self.background_color[1], self.background_color[2], 1.0))
        glFogf(GL_FOG_START, self.start_distance)
        glFogf(GL_FOG_END, self.end_distance)
        glHint(GL_FOG_HINT, GL_NICEST)
        self.sprite_texture = self._build_sprite_texture(64)

    def _build_sprite_texture(self, size):
        pixels = bytearray()
        center = (size - 1) / 2.0
        for y in range(size):
            for x in range(size):
                distance = math.hypot(x - center, y - center) / center
                intensity = max(0.0, 1.0 - distance)
                alpha = int((intensity ** 2) * 255)
                pixels.extend((255, 255, 255, alpha))
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, size, size, 0, GL_RGBA, GL_UNSIGNED_BYTE, bytes(pixels))
        return texture_id

    def draw(self, elapsed_seconds, camera_right, camera_up):
        glDisable(GL_FOG)
        glDepthMask(GL_FALSE)
        glEnable(GL_TEXTURE_2D)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)
        glBindTexture(GL_TEXTURE_2D, self.sprite_texture)
        glBegin(GL_QUADS)
        for particle in self.particles:
            position = particle.position_at(elapsed_seconds)
            half_size = particle.half_size_at(elapsed_seconds)
            opacity = particle.opacity_at(elapsed_seconds)
            right_x, right_y, right_z = (axis * half_size for axis in camera_right)
            up_x, up_y, up_z = (axis * half_size for axis in camera_up)
            glColor4f(self.color[0], self.color[1], self.color[2], opacity)
            glTexCoord2f(0.0, 0.0)
            glVertex3f(position[0] - right_x - up_x, position[1] - right_y - up_y, position[2] - right_z - up_z)
            glTexCoord2f(1.0, 0.0)
            glVertex3f(position[0] + right_x - up_x, position[1] + right_y - up_y, position[2] + right_z - up_z)
            glTexCoord2f(1.0, 1.0)
            glVertex3f(position[0] + right_x + up_x, position[1] + right_y + up_y, position[2] + right_z + up_z)
            glTexCoord2f(0.0, 1.0)
            glVertex3f(position[0] - right_x + up_x, position[1] - right_y + up_y, position[2] - right_z + up_z)
        glEnd()
        glDisable(GL_TEXTURE_2D)
        glDepthMask(GL_TRUE)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_FOG)
