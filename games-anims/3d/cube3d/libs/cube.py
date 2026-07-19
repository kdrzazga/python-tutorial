import pygame
from OpenGL.GL import (
    GL_QUADS,
    GL_RGB,
    GL_TEXTURE_2D,
    GL_TEXTURE_MAG_FILTER,
    GL_TEXTURE_MIN_FILTER,
    GL_LINEAR,
    GL_UNSIGNED_BYTE,
    glBegin,
    glBindTexture,
    glEnd,
    glGenTextures,
    glTexCoord2f,
    glTexImage2D,
    glTexParameteri,
    glTexSubImage2D,
    glVertex3fv,
)


class Cube:
    VERTICES = [
        (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
        (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
    ]

    # Each face: vertex indices (CCW when viewed from outside) + texcoords
    FACES = [
        (4, 5, 6, 7),   # front  (+z)
        (1, 0, 3, 2),   # back   (-z)
        (0, 4, 7, 3),   # left   (-x)
        (5, 1, 2, 6),   # right  (+x)
        (3, 7, 6, 2),   # top    (+y)
        (0, 1, 5, 4),   # bottom (-y)
    ]
    TEXCOORDS = [(0, 0), (1, 0), (1, 1), (0, 1)]

    def __init__(self, tex_size):
        self.tex_size = tex_size
        self.tex_ids = [self._create_texture() for _ in self.FACES]

    def _create_texture(self):
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGB, self.tex_size, self.tex_size, 0,
            GL_RGB, GL_UNSIGNED_BYTE, None
        )
        return tex_id

    def upload(self, surfaces):
        for tex_id, surface in zip(self.tex_ids, surfaces):
            data = pygame.image.tostring(surface, "RGB", True)
            glBindTexture(GL_TEXTURE_2D, tex_id)
            glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, self.tex_size, self.tex_size,
                             GL_RGB, GL_UNSIGNED_BYTE, data)

    def draw(self):
        for face, tex_id in zip(self.FACES, self.tex_ids):
            glBindTexture(GL_TEXTURE_2D, tex_id)
            glBegin(GL_QUADS)
            for vi, (s, tcoord) in zip(face, self.TEXCOORDS):
                glTexCoord2f(s, tcoord)
                glVertex3fv(self.VERTICES[vi])
            glEnd()
