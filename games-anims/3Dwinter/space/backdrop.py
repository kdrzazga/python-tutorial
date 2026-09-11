import math

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt

from .common import TextureLibrary
from .nebula import Config, NebulaGas, StarField, SpikeStars
from .round_nebula import RoundNebula


class SpaceBackdrop:
    def __init__(self, aspect, fov=55.0, far=3000.0, tilt=90.0, view_distance=46.0):
        self.aspect = aspect
        self.fov = fov
        self.far = far
        self.tilt = tilt
        self.view_distance = view_distance
        self.world_up = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        self.config = Config()
        self.textures = TextureLibrary()
        self.batches = (#NebulaGas(self.config, self.textures.glow),
                        StarField(self.config, self.textures.glow),
                        SpikeStars(self.config, self.textures.spike)
                        )
        self.round_nebulas = self._build_round_nebulas()

    def _build_round_nebulas(self):
        glow = self.textures.glow
        return (RoundNebula(glow, center=(-530.0, 55.0, -95.0), radius=130.0, seed=3, spin_speed=10.1),
                RoundNebula(glow, center=(-630.0, -255.0, 155.0), radius=30.0, seed=2,
                            inner_color=(0.1, 0.96, 0.1)),
                RoundNebula(glow, center=(0.0, 0.0, 1500.0), radius=130.0, seed=2, spin_speed=0.1,
                            rim_color=(0.0, 0.94, 0.30)),
                RoundNebula(glow, center=(-400.0, -400.0, 1600.0), radius=120.0, seed=5, spin_speed=-0.9,
                            rim_color=(0.0, 0.15, 0.99)),
                RoundNebula(glow, center=(300.0, 450.0, 1650.0), radius=110.0, seed=1, spin_speed=-5.5),
                RoundNebula(glow, center=(255.0, -65.0, -150.0), radius=42.0, seed=6,
                            rim_color=(1.0, 0.34, 0.30), shell_color=(1.0, 0.58, 0.34),
                            inner_color=(0.40, 0.46, 0.92), spin_speed=-0.045))

    def _camera_basis(self, eye, target):
        forward = np.array(target, dtype=np.float32) - np.array(eye, dtype=np.float32)
        forward = forward / np.linalg.norm(forward)
        right = np.cross(forward, self.world_up)
        right = right / np.linalg.norm(right)
        return forward, right.astype(np.float32), np.cross(right, forward).astype(np.float32)

    def _to_local(self, vector):
        angle = math.radians(-self.tilt)
        cos_value = math.cos(angle)
        sin_value = math.sin(angle)
        return np.array([vector[0],
                         vector[1] * cos_value - vector[2] * sin_value,
                         vector[1] * sin_value + vector[2] * cos_value], dtype=np.float32)

    def update(self, moment, brightness):
        if brightness <= 0.01:
            return
        for batch in self.batches:
            batch.update(moment)
            batch.colors[:, 3] *= brightness
        for nebula in self.round_nebulas:
            nebula.update(moment)
            nebula.colors[:, 3] *= brightness

    def draw(self, brightness, eye, target):
        if brightness <= 0.01:
            return
        forward, right, up = self._camera_basis(eye, target)
        local_right = self._to_local(right)
        local_up = self._to_local(up)

        glPushAttrib(GL_ENABLE_BIT | GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_TEXTURE_BIT)
        glPushClientAttrib(GL_CLIENT_VERTEX_ARRAY_BIT)
        glDisable(GL_LIGHTING)
        glDisable(GL_FOG)
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)
        glDepthMask(GL_FALSE)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)
        glEnable(GL_TEXTURE_2D)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluPerspective(self.fov, self.aspect, 1.0, self.far)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        gluLookAt(0.0, 0.0, 0.0, forward[0], forward[1], forward[2],
                  self.world_up[0], self.world_up[1], self.world_up[2])
        glRotatef(self.tilt, 1.0, 0.0, 0.0)
        glTranslatef(0.0, 0.0, -self.view_distance)

        for batch in self.batches:
            batch.render(local_right, local_up)
        for nebula in self.round_nebulas:
            nebula.render(local_right, local_up)

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopClientAttrib()
        glPopAttrib()
